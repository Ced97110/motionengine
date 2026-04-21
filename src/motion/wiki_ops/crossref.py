"""Cross-reference compiler for the Motion wiki.

Walks ``wiki/*.md`` and emits **13 JSON indexes** under ``wiki/compiled/``.
No inference, no LLM — pure structural compilation of authored content.

Two classes of output:

**Front-matter inversion (edge #1 anatomy chain — 6 indexes):**
- ``play-to-anatomy.json``      — ``{play_slug: [{region, criticality, supports_technique?, for_role?}]}``
- ``play-to-technique.json``    — ``{play_slug: [{id, criticality, role}]}``
- ``anatomy-to-play.json``      — inverted; ``{region: [{play, criticality, ...}]}``
- ``anatomy-to-drill.json``     — inverted; ``{region: [{drill, emphasis}]}``
- ``technique-to-play.json``    — inverted; ``{id: [{play, criticality, role}]}``
- ``technique-to-drill.json``   — inverted; ``{id: [{drill, emphasis}]}``

**Content/body extractions (3 indexes):**
- ``page-insights.json``        — structured ``insights:`` blocks per page
- ``page-tags.json``             — ``{slug: [tags]}`` for all tagged pages
- ``defending-insights.json``    — parsed ``## Common Mistakes`` + ``diagram:`` per defending-*.md

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


# --- main compile pass -------------------------------------------------------


def compile_indexes(
    wiki_directory: Path,
) -> dict[str, dict[str, Any]]:
    """Walk the wiki directory and build the cross-ref + insight JSON indexes.

    Returns a mapping from output filename to the JSON-serialisable payload.
    """
    play_to_anatomy: dict[str, list[dict[str, str]]] = {}
    play_to_technique: dict[str, list[dict[str, str]]] = {}
    anatomy_to_play: dict[str, list[dict[str, str]]] = defaultdict(list)
    anatomy_to_drill: dict[str, list[dict[str, str]]] = defaultdict(list)
    technique_to_play: dict[str, list[dict[str, str]]] = defaultdict(list)
    technique_to_drill: dict[str, list[dict[str, str]]] = defaultdict(list)
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
            if techs:
                play_to_technique[slug] = techs
            if anatomies:
                play_to_anatomy[slug] = anatomies
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
            for a in trains_a:
                anatomy_to_drill[a["region"]].append(
                    _clean({"drill": slug, "emphasis": a.get("emphasis")})
                )
            for t in trains_t:
                technique_to_drill[t["id"]].append(
                    _clean({"drill": slug, "emphasis": t.get("emphasis")})
                )

    return {
        "play-to-anatomy.json": play_to_anatomy,
        "play-to-technique.json": play_to_technique,
        "anatomy-to-play.json": dict(anatomy_to_play),
        "anatomy-to-drill.json": dict(anatomy_to_drill),
        "technique-to-play.json": dict(technique_to_play),
        "technique-to-drill.json": dict(technique_to_drill),
        "page-insights.json": page_insights,
        "page-tags.json": page_tags,
        "defending-insights.json": defending_insights,
        "wikilink-graph.json": wikilink_forward,
        "wikilink-graph-reverse.json": dict(wikilink_reverse),
        "citation-graph.json": dict(citation_graph),
        "formation-graph.json": dict(formation_graph),
    }


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
    args = parser.parse_args(argv)

    wiki_root = wiki_dir(args.wiki_dir)
    out_dir = args.out_dir if args.out_dir is not None else wiki_root / "compiled"

    indexes = compile_indexes(wiki_root)
    write_indexes(indexes, out_dir)

    n_plays_anatomy = len(indexes["play-to-anatomy.json"])
    n_plays_technique = len(indexes["play-to-technique.json"])
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
    n_wikilink_source_pages = len(indexes["wikilink-graph.json"])
    n_wikilink_edges = sum(len(targets) for targets in indexes["wikilink-graph.json"].values())
    n_wikilink_targets = len(indexes["wikilink-graph-reverse.json"])
    n_citation_keys = len(indexes["citation-graph.json"])
    n_formation_keys = len(indexes["formation-graph.json"])

    sys.stdout.write(
        f"[crossref] compiled 13 indexes to {out_dir}\n"
        f"  plays with demands_anatomy:    {n_plays_anatomy}\n"
        f"  plays with demands_techniques: {n_plays_technique}\n"
        f"  anatomy regions referenced:    {n_anatomy_regions}\n"
        f"  techniques referenced:         {n_techniques}\n"
        f"  anatomy → drill edges:         {n_drills_anatomy}\n"
        f"  technique → drill edges:       {n_drills_technique}\n"
        f"  pages with insights:           {n_insights}\n"
        f"  pages with tags:               {n_tagged_pages}\n"
        f"  defending pages parsed:        {n_defending} ({n_defending_symptoms} symptoms)\n"
        f"  wikilink source pages:         {n_wikilink_source_pages} "
        f"({n_wikilink_edges} unique (source, target) pairs → "
        f"{n_wikilink_targets} unique targets)\n"
        f"  citation keys:                 {n_citation_keys}\n"
        f"  formations:                    {n_formation_keys}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
