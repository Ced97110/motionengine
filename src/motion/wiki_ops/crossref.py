"""Cross-reference compiler for the Motion wiki.

Walks ``wiki/*.md`` and emits **15 JSON indexes** under ``wiki/compiled/``.
No inference, no LLM — pure structural compilation of authored content.

Two classes of output:

**Front-matter inversion (edge #1 anatomy chain — 6 indexes):**

- ``play-to-anatomy.json``, ``play-to-technique.json`` — forward edges from each
  play to its declared anatomy regions and required techniques.
- ``anatomy-to-play.json``, ``anatomy-to-drill.json`` — inverted; every region
  mapped to the plays that demand it and the drills that train it.
- ``technique-to-play.json``, ``technique-to-drill.json`` — same inversion,
  keyed on technique id.

**Stat-signature inversion (edge #8 analytics chain — 2 indexes):**

- ``play-to-signature.json``, ``signature-to-play.json`` — plays' Four-Factor
  directions (lifts / protects eFG%, OREB%, TOV%, FTR, PPP, pace, floor%),
  forward and inverted.

**Content/body extractions (3 indexes):**
- ``page-insights.json``        — structured ``insights:`` blocks per page
- ``page-tags.json``             — ``{slug: [tags]}`` for all tagged pages
- ``defending-insights.json``    — parsed ``## Common Mistakes`` + ``diagram:`` per defending-*.md

**Defending edges (2 indexes — M4 tag-intersection back-refs):**
- ``play-to-defending.json``    — ``{play_slug: [{defending, shared_tags[]}]}``
- ``defending-to-play.json``    — inverted; ``{defending_slug: [{play, shared_tags[]}]}``
Matching rule: a play matches a defending page iff their tag sets share at
least one non-generic tag (i.e. not ``defense`` / ``man-to-man`` / similar).

**Counters provenance (1 index — M4 part 3):**
- ``play-to-counters.json``     — ``{play_slug: [{text, extraction, source_hint}]}``
Engine surfaces only entries with ``extraction == "llm-inferred"`` to gate
out book-derived prose.

**Native wikilink & structural graphs (4 indexes — Karpathy-native edges):**
- ``wikilink-graph.json``         — forward; ``{page_slug: [target_slugs]}`` (unique per source)
- ``wikilink-graph-reverse.json`` — inverted; ``{target_slug: [pages_linking_here]}``
- ``citation-graph.json``         — ``{"Sn, p.X": [pages_citing_it]}`` (normalized cite keys)
- ``formation-graph.json``        — ``{formation_name: [play_slugs]}``

Spec: ``backend/spec/crossref-anatomy-chain.md`` §6.

Usage:

.. code-block:: bash

    python -m motion.wiki_ops crossref
    python -m motion.wiki_ops crossref --wiki-dir path/to/wiki --out-dir path/to/out
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from motion.sports import DEFAULT_SPORT

from .frontmatter import parse_full
from .paths import wiki_dir

# --- body-prose parsers ------------------------------------------------------

# Lines of the form: "1. **Symptom text** → Remedy prose" — the shape is
# consistent across all 13 defending-*.md pages (verified 2026-04-20).
_MISTAKE_LINE = re.compile(r"^\d+\.\s+\*\*(?P<symptom>.+?)\*\*\s+→\s+(?P<remedy>.+)$")

# Body-level wikilinks: [[page-slug]] — kebab-case, matches the SCHEMA.md
# filename convention. The set/unique-per-source pattern mirrors
# `_check_bidirectional` in lint_wiki.py so the counts line up with lint output.
_WIKILINK_RE = re.compile(r"\[\[(?P<target>[a-z0-9][a-z0-9-]+[a-z0-9])\]\]")

# Source citations: [S1] or [S2, p.32] or [S7, pp.117-119]. The source-id
# and the optional page designator are captured separately for normalized
# cluster keys ("S2, p.32" or "S2" alone).
_CITATION_RE = re.compile(r"\[(?P<source>S\d+)(?:,\s*(?P<pages>pp?\.\s*[\d\u2013\u2014-]+))?\]")


def _extract_common_mistakes(body: str) -> list[dict[str, str]]:
    """Parse the ``## Common Mistakes`` section into a list of ``{symptom, remedy}``.

    Returns ``[]`` if the section is absent or no bullet matches the expected
    shape. Tolerates extra blank lines and does not consume sub-bullets.
    """
    lines = body.splitlines()
    in_section = False
    out: list[dict[str, str]] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## Common Mistakes"):
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if not in_section:
            continue
        match = _MISTAKE_LINE.match(stripped)
        if match:
            out.append(
                {
                    "symptom": match.group("symptom").strip(),
                    "remedy": match.group("remedy").strip(),
                }
            )
    return out


def _extract_wikilink_targets(body: str) -> list[str]:
    """Return the unique wikilink targets in ``body``, in first-occurrence order.

    Dedupe per source page — matches lint_wiki.py's `_check_bidirectional`
    semantics (counting unique (source, target) pairs, not raw occurrences).
    """
    seen: set[str] = set()
    out: list[str] = []
    for match in _WIKILINK_RE.finditer(body):
        target = match.group("target")
        if target in seen:
            continue
        seen.add(target)
        out.append(target)
    return out


def _extract_citations(body: str) -> list[str]:
    """Return unique citation keys (e.g. ``"S2, p.32"`` or ``"S1"``) in order.

    Normalizes the key to ``"Sn"`` or ``"Sn, p.X"`` form so an inverted index
    groups pages citing the exact same passage.
    """
    seen: set[str] = set()
    out: list[str] = []
    for match in _CITATION_RE.finditer(body):
        source = match.group("source")
        pages = match.group("pages")
        key = source if not pages else f"{source}, {pages.strip()}"
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


# --- extraction helpers ------------------------------------------------------


def _clean(d: dict[str, Any]) -> dict[str, str]:
    """Drop ``None`` values; coerce remaining values to ``str``."""
    return {k: str(v) for k, v in d.items() if v is not None}


def _dict_items(fm: dict[str, Any], key: str) -> list[dict[str, Any]]:
    """Return ``fm[key]`` filtered to dict entries; tolerate missing key / None."""
    raw = fm.get(key) or []
    return [item for item in raw if isinstance(item, dict)]


# Tags too generic to prove a play↔defending match on their own. Without this
# filter, every man-to-man play matches every man-to-man defending page
# (~7x more edges, ~1.5x more noise per edge). Keep in sync with
# `spec/crossref-anatomy-chain.md` §M4 if added there.
_GENERIC_DEFENDING_TAGS: frozenset[str] = frozenset({
    "defense",
    "man-to-man",
    "help-defense",
    "zone",
    "press",
    "pro",
    "youth",
    "offense",
    "half-court",
    "transition",
    "formation-defense",
})


# --- main compile pass -------------------------------------------------------


def compile_indexes(
    wiki_directory: Path,
) -> dict[str, dict[str, Any]]:
    """Walk the wiki directory and build the cross-ref + insight JSON indexes.

    Returns a mapping from output filename to the JSON-serialisable payload.
    """
    play_slugs: set[str] = set()
    play_to_anatomy: dict[str, list[dict[str, str]]] = {}
    play_to_technique: dict[str, list[dict[str, str]]] = {}
    play_to_signature: dict[str, list[dict[str, str]]] = {}
    play_to_counters: dict[str, list[dict[str, str]]] = {}
    anatomy_to_play: dict[str, list[dict[str, str]]] = defaultdict(list)
    anatomy_to_drill: dict[str, list[dict[str, str]]] = defaultdict(list)
    technique_to_play: dict[str, list[dict[str, str]]] = defaultdict(list)
    technique_to_drill: dict[str, list[dict[str, str]]] = defaultdict(list)
    signature_to_play: dict[str, list[dict[str, str]]] = defaultdict(list)
    page_insights: dict[str, Any] = {}
    page_tags: dict[str, list[str]] = {}
    defending_insights: dict[str, Any] = {}
    wikilink_forward: dict[str, list[str]] = {}
    wikilink_reverse: dict[str, list[str]] = defaultdict(list)
    citation_graph: dict[str, list[str]] = defaultdict(list)
    formation_graph: dict[str, list[str]] = defaultdict(list)

    for md_path in sorted(wiki_directory.glob("*.md")):
        slug = md_path.stem
        if slug in ("index", "log"):
            continue
        try:
            raw = md_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        fm, body = parse_full(raw)
        page_type = fm.get("type")

        tags = fm.get("tags")
        if isinstance(tags, list) and tags:
            page_tags[slug] = [str(t) for t in tags]

        insights = fm.get("insights")
        if isinstance(insights, dict) and insights:
            page_insights[slug] = insights

        # Body-level structural edges — native Karpathy cross-refs compiled
        # into forward/reverse indexes without modifying wiki content.
        wikilink_targets = _extract_wikilink_targets(body)
        if wikilink_targets:
            wikilink_forward[slug] = wikilink_targets
            for target in wikilink_targets:
                wikilink_reverse[target].append(slug)

        for citation_key in _extract_citations(body):
            citation_graph[citation_key].append(slug)

        if page_type == "play":
            play_slugs.add(slug)
            formation = fm.get("formation")
            if isinstance(formation, str) and formation.strip():
                formation_graph[formation.strip()].append(slug)

        if slug.startswith("defending-"):
            symptoms = _extract_common_mistakes(body)
            diagram = fm.get("diagram")
            if symptoms or diagram:
                defending_insights[slug] = {
                    "tags": page_tags.get(slug, []),
                    "symptoms": symptoms,
                    "diagram": diagram if isinstance(diagram, dict) else None,
                }

        if page_type == "play":
            techs = [
                _clean(
                    {
                        "id": item["id"],
                        "criticality": item.get("criticality"),
                        "role": item.get("role"),
                    }
                )
                for item in _dict_items(fm, "demands_techniques")
                if item.get("id")
            ]
            anatomies = [
                _clean(
                    {
                        "region": item["region"],
                        "criticality": item.get("criticality"),
                        "supports_technique": item.get("supports_technique"),
                        "for_role": item.get("for_role"),
                    }
                )
                for item in _dict_items(fm, "demands_anatomy")
                if item.get("region")
            ]
            signatures = [
                _clean(
                    {
                        "factor": item["factor"],
                        "direction": item.get("direction"),
                        "concept_slug": item.get("concept_slug"),
                        "magnitude": item.get("magnitude"),
                        "rationale": item.get("rationale"),
                    }
                )
                for item in _dict_items(fm, "produces_signature")
                if item.get("factor")
            ]
            counters = [
                _clean(
                    {
                        "text": item["text"],
                        "extraction": item.get("extraction"),
                        "source_hint": item.get("source_hint"),
                    }
                )
                for item in _dict_items(fm, "counters")
                if item.get("text")
            ]
            if techs:
                play_to_technique[slug] = techs
            if anatomies:
                play_to_anatomy[slug] = anatomies
            if signatures:
                play_to_signature[slug] = signatures
            if counters:
                play_to_counters[slug] = counters
            for a in anatomies:
                anatomy_to_play[a["region"]].append(
                    _clean(
                        {
                            "play": slug,
                            "criticality": a.get("criticality"),
                            "supports_technique": a.get("supports_technique"),
                            "for_role": a.get("for_role"),
                        }
                    )
                )
            for t in techs:
                technique_to_play[t["id"]].append(
                    _clean(
                        {
                            "play": slug,
                            "criticality": t.get("criticality"),
                            "role": t.get("role"),
                        }
                    )
                )
            for sig in signatures:
                signature_to_play[sig["factor"]].append(
                    _clean(
                        {
                            "play": slug,
                            "direction": sig.get("direction"),
                            "magnitude": sig.get("magnitude"),
                            "concept_slug": sig.get("concept_slug"),
                            "rationale": sig.get("rationale"),
                        }
                    )
                )
            continue

        # Drill or concept-as-technique pages may declare `trains_*`.
        if page_type in ("drill", "concept"):
            trains_a = [
                _clean(
                    {
                        "region": item["region"],
                        "emphasis": item.get("emphasis"),
                    }
                )
                for item in _dict_items(fm, "trains_anatomy")
                if item.get("region")
            ]
            trains_t = [
                _clean(
                    {
                        "id": item["id"],
                        "emphasis": item.get("emphasis"),
                    }
                )
                for item in _dict_items(fm, "trains_techniques")
                if item.get("id")
            ]
            # Practice-generator filtering needs level + duration at retrieval
            # time. Emitting them per edge avoids re-reading every drill page.
            drill_level = fm.get("level")
            drill_duration = fm.get("duration_minutes")
            for a in trains_a:
                anatomy_to_drill[a["region"]].append(
                    _clean(
                        {
                            "drill": slug,
                            "emphasis": a.get("emphasis"),
                            "level": drill_level,
                            "duration_minutes": drill_duration,
                        }
                    )
                )
            for t in trains_t:
                technique_to_drill[t["id"]].append(
                    _clean(
                        {
                            "drill": slug,
                            "emphasis": t.get("emphasis"),
                            "level": drill_level,
                            "duration_minutes": drill_duration,
                        }
                    )
                )

    play_to_defending, defending_to_play = _compile_defending_edges(
        play_slugs=play_slugs,
        defending_insights=defending_insights,
        page_tags=page_tags,
    )

    return {
        "play-to-anatomy.json": play_to_anatomy,
        "play-to-technique.json": play_to_technique,
        "play-to-signature.json": play_to_signature,
        "play-to-counters.json": play_to_counters,
        "anatomy-to-play.json": dict(anatomy_to_play),
        "anatomy-to-drill.json": dict(anatomy_to_drill),
        "technique-to-play.json": dict(technique_to_play),
        "technique-to-drill.json": dict(technique_to_drill),
        "signature-to-play.json": dict(signature_to_play),
        "page-insights.json": page_insights,
        "page-tags.json": page_tags,
        "defending-insights.json": defending_insights,
        "play-to-defending.json": play_to_defending,
        "defending-to-play.json": defending_to_play,
        "wikilink-graph.json": wikilink_forward,
        "wikilink-graph-reverse.json": dict(wikilink_reverse),
        "citation-graph.json": dict(citation_graph),
        "formation-graph.json": dict(formation_graph),
    }


def _compile_defending_edges(
    *,
    play_slugs: set[str],
    defending_insights: dict[str, Any],
    page_tags: dict[str, list[str]],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    """Join plays and defending-* pages via tag intersection.

    A play ``P`` matches a defending page ``D`` iff
    ``P.tags ∩ D.tags`` contains at least one tag outside
    :data:`_GENERIC_DEFENDING_TAGS`. The shared-tag list is returned with the
    edge so downstream Engine surfaces can render the match rationale
    ("vs a back-screen defense…") without re-deriving.

    Returns a ``(play_to_defending, defending_to_play)`` pair of sidecars.
    """
    play_to_defending: dict[str, list[dict[str, Any]]] = {}
    defending_to_play: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for p_slug in sorted(play_slugs):
        p_tags = set(page_tags.get(p_slug) or [])
        if not p_tags:
            continue
        edges: list[dict[str, Any]] = []
        for d_slug, d_info in defending_insights.items():
            d_tags = set(d_info.get("tags") or [])
            shared = (p_tags & d_tags) - _GENERIC_DEFENDING_TAGS
            if not shared:
                continue
            edges.append({"defending": d_slug, "shared_tags": sorted(shared)})
            defending_to_play[d_slug].append(
                {"play": p_slug, "shared_tags": sorted(shared)}
            )
        if edges:
            play_to_defending[p_slug] = edges

    return play_to_defending, dict(defending_to_play)


def write_indexes(indexes: dict[str, dict[str, Any]], out_dir: Path) -> None:
    """Write each compiled index as a JSON file under ``out_dir``."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename, payload in indexes.items():
        (out_dir / filename).write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="motion-wiki-crossref",
        description="Compile cross-reference JSON indexes from wiki front-matter.",
    )
    parser.add_argument(
        "--wiki-dir",
        type=Path,
        default=None,
        help="Override the wiki directory (defaults to the project wiki).",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Override the compiled output directory (defaults to `<wiki>/compiled/`).",
    )
    parser.add_argument(
        "--sport",
        default=DEFAULT_SPORT,
        choices=("basketball", "football"),
        help="Sport wiki to compile indexes for (default: basketball).",
    )
    args = parser.parse_args(argv)

    # When --wiki-dir is provided it is treated as a literal override (no
    # sport suffix appended) — the caller is responsible for pointing at the
    # right per-sport directory. When absent, wiki_dir() resolves the
    # canonical per-sport path via the sport kwarg.
    wiki_root = wiki_dir(args.wiki_dir, sport=args.sport)
    out_dir = args.out_dir if args.out_dir is not None else wiki_root / "compiled"
    sys.stdout.write(f"[crossref] sport: {args.sport}\n")

    indexes = compile_indexes(wiki_root)
    write_indexes(indexes, out_dir)

    n_plays_anatomy = len(indexes["play-to-anatomy.json"])
    n_plays_technique = len(indexes["play-to-technique.json"])
    n_plays_signature = len(indexes["play-to-signature.json"])
    n_signature_factors = len(indexes["signature-to-play.json"])
    n_signature_edges = sum(len(v) for v in indexes["signature-to-play.json"].values())
    n_anatomy_regions = len(indexes["anatomy-to-play.json"])
    n_techniques = len(indexes["technique-to-play.json"])
    n_drills_anatomy = sum(len(v) for v in indexes["anatomy-to-drill.json"].values())
    n_drills_technique = sum(len(v) for v in indexes["technique-to-drill.json"].values())
    n_insights = len(indexes["page-insights.json"])
    n_tagged_pages = len(indexes["page-tags.json"])
    n_defending = len(indexes["defending-insights.json"])
    n_defending_symptoms = sum(
        len(entry.get("symptoms", [])) for entry in indexes["defending-insights.json"].values()
    )
    n_plays_defending = len(indexes["play-to-defending.json"])
    n_defending_edges = sum(len(v) for v in indexes["play-to-defending.json"].values())
    n_plays_counters = len(indexes["play-to-counters.json"])
    n_counter_bullets = sum(len(v) for v in indexes["play-to-counters.json"].values())
    n_wikilink_source_pages = len(indexes["wikilink-graph.json"])
    n_wikilink_edges = sum(len(targets) for targets in indexes["wikilink-graph.json"].values())
    n_wikilink_targets = len(indexes["wikilink-graph-reverse.json"])
    n_citation_keys = len(indexes["citation-graph.json"])
    n_formation_keys = len(indexes["formation-graph.json"])

    sys.stdout.write(
        f"[crossref] compiled 18 indexes to {out_dir}\n"
        f"  plays with demands_anatomy:    {n_plays_anatomy}\n"
        f"  plays with demands_techniques: {n_plays_technique}\n"
        f"  plays with produces_signature: {n_plays_signature}\n"
        f"  anatomy regions referenced:    {n_anatomy_regions}\n"
        f"  techniques referenced:         {n_techniques}\n"
        f"  analytic factors referenced:   {n_signature_factors} ({n_signature_edges} edges)\n"
        f"  anatomy → drill edges:         {n_drills_anatomy}\n"
        f"  technique → drill edges:       {n_drills_technique}\n"
        f"  pages with insights:           {n_insights}\n"
        f"  pages with tags:               {n_tagged_pages}\n"
        f"  defending pages parsed:        {n_defending} ({n_defending_symptoms} symptoms)\n"
        f"  play → defending edges:        {n_defending_edges} across {n_plays_defending} plays\n"
        f"  counter bullets indexed:       {n_counter_bullets} across {n_plays_counters} plays\n"
        f"  wikilink source pages:         {n_wikilink_source_pages} "
        f"({n_wikilink_edges} unique (source, target) pairs → "
        f"{n_wikilink_targets} unique targets)\n"
        f"  citation keys:                 {n_citation_keys}\n"
        f"  formations:                    {n_formation_keys}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
