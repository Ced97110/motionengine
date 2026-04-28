"""Retrieval-bundle library for the cross-ref anatomy chain.

Consumers (future ``/knowledge/ask``, halftime-chip, readiness-report) call
these pure functions to turn a play / flagged-region / drill slug into a
joined JSON bundle drawn from the compiled sidecars under
``knowledge-base/wiki/compiled/``.

The query patterns mirror ``spec/crossref-anatomy-chain.md`` §7:

- :func:`build_play_context` — Q-A (drill prescription for a play)
- :func:`build_readiness_filter` — Q-B (flagged regions → safe plays + rx)
- :func:`build_drill_justification` — Q-C (drill → plays it prepares)

No LLM, no fuzzy matching, no HTTP. Pure front-matter inversion lookups.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from motion.sports import DEFAULT_SPORT, Sport

from .paths import wiki_dir
from .retrieval_focus_maps import FORM_FOCUS, PRACTICE_FOCUS
from .retrieval_models import (
    AnatomyDemand,
    AnatomyInsight,
    CompiledIndexes,
    CounterEntry,
    DefendingEdge,
    DefensiveMatch,
    DefensiveSymptom,
    DrillInsight,
    DrillPrescription,
    FormContext,
    FormMeasurement,
    PlayContext,
    PracticeContext,
    PracticeDrillCandidate,
    ReadinessBundle,
    SignatureEntry,
    TechniqueDemand,
)

__all__ = [
    "AnatomyDemand",
    "AnatomyInsight",
    "CompiledIndexes",
    "CounterEntry",
    "DefendingEdge",
    "DefensiveMatch",
    "DefensiveSymptom",
    "DrillInsight",
    "DrillPrescription",
    "FormContext",
    "FormMeasurement",
    "PlayContext",
    "PracticeContext",
    "PracticeDrillCandidate",
    "ReadinessBundle",
    "SignatureEntry",
    "TechniqueDemand",
    "build_defensive_mirror",
    "build_drill_justification",
    "build_form_context",
    "build_play_context",
    "build_practice_context",
    "build_readiness_filter",
    "cached_indexes",
    "context_to_dict",
    "get_cite_cluster",
    "get_formation_siblings",
    "get_incoming_links",
    "get_outgoing_links",
    "get_shared_citation_pages",
    "load_indexes",
    "readiness_to_dict",
]


# --- loading -----------------------------------------------------------------


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_indexes(
    compiled_directory: Path | None = None,
    *,
    sport: Sport = DEFAULT_SPORT,
) -> CompiledIndexes:
    """Load the 6 inverted indexes + technique-aliases.json from disk.

    ``compiled_directory`` defaults to ``<wiki>/compiled/``. When
    ``compiled_directory`` is not provided, ``sport`` selects which per-sport
    wiki tree to read from.
    """
    base = (
        compiled_directory
        if compiled_directory is not None
        else wiki_dir(sport=sport) / "compiled"
    )
    aliases_raw = _read_json(base / "technique-aliases.json")
    aliases = aliases_raw.get("aliases", {}) if isinstance(aliases_raw, dict) else {}

    def _maybe_read(filename: str) -> dict[str, Any]:
        path = base / filename
        return _read_json(path) if path.is_file() else {}

    return CompiledIndexes(
        play_to_anatomy=_read_json(base / "play-to-anatomy.json"),
        play_to_technique=_read_json(base / "play-to-technique.json"),
        play_to_signature=_maybe_read("play-to-signature.json"),
        play_to_counters=_maybe_read("play-to-counters.json"),
        anatomy_to_play=_read_json(base / "anatomy-to-play.json"),
        anatomy_to_drill=_read_json(base / "anatomy-to-drill.json"),
        technique_to_play=_read_json(base / "technique-to-play.json"),
        technique_to_drill=_read_json(base / "technique-to-drill.json"),
        technique_aliases=aliases,
        page_insights=_maybe_read("page-insights.json"),
        page_tags=_maybe_read("page-tags.json"),
        defending_insights=_maybe_read("defending-insights.json"),
        play_to_defending=_maybe_read("play-to-defending.json"),
        wikilink_forward=_maybe_read("wikilink-graph.json"),
        wikilink_reverse=_maybe_read("wikilink-graph-reverse.json"),
        citation_graph=_maybe_read("citation-graph.json"),
        formation_graph=_maybe_read("formation-graph.json"),
    )


@lru_cache(maxsize=1)
def cached_indexes() -> CompiledIndexes:
    """Process-wide cache for the default-sport compiled indexes.

    Routers used to keep their own ``lru_cache`` per module, which loaded
    the same files three times at startup. This shared cache reads once.
    """
    return load_indexes()


# --- helpers -----------------------------------------------------------------


def _region_to_concept_slug(region: str) -> str:
    """Canonical anatomy page slug for a region id (e.g. ``glute_max``)."""
    return f"concept-anatomy-{region.replace('_', '-')}"


def _resolve_technique_slug(technique_id: str, aliases: dict[str, dict[str, Any]]) -> str | None:
    """Return the concept-page slug for a technique id, or ``None`` if no page."""
    entry = aliases.get(technique_id)
    if isinstance(entry, dict):
        slug = entry.get("slug")
        if isinstance(slug, str) and slug:
            return slug
    return None


def _anatomy_insight_for(slug: str, insights: dict[str, dict[str, Any]]) -> AnatomyInsight | None:
    """Return an :class:`AnatomyInsight` for ``slug``, or ``None`` if unannotated."""
    payload = insights.get(slug)
    if not isinstance(payload, dict):
        return None
    key_principles = payload.get("key_principles") or []
    common_mistakes = payload.get("common_mistakes") or []
    if not (key_principles or common_mistakes):
        return None
    return AnatomyInsight(
        key_principles=[p for p in key_principles if isinstance(p, dict)],
        common_mistakes=[m for m in common_mistakes if isinstance(m, dict)],
    )


def _drill_insight_for(slug: str, insights: dict[str, dict[str, Any]]) -> DrillInsight | None:
    """Return a :class:`DrillInsight` for ``slug``, or ``None`` if unannotated."""
    payload = insights.get(slug)
    if not isinstance(payload, dict):
        return None
    safety_tip = payload.get("safety_tip")
    coaching_cue = payload.get("coaching_cue")
    primary_form_error = payload.get("primary_form_error")
    if not (safety_tip or coaching_cue or primary_form_error):
        return None
    return DrillInsight(
        safety_tip=safety_tip if isinstance(safety_tip, dict) else None,
        coaching_cue=coaching_cue if isinstance(coaching_cue, str) else None,
        primary_form_error=(primary_form_error if isinstance(primary_form_error, dict) else None),
    )


# --- Q-A: drill prescription for a play --------------------------------------


def build_play_context(play_slug: str, indexes: CompiledIndexes) -> PlayContext:
    """Return the joined retrieval bundle for one play.

    Follows spec §7 Q-A: union of (a) anatomy concept slugs, (b) drills
    reachable through ``demands_anatomy → anatomy-to-drill``, and (c) drills
    reachable through ``demands_techniques → technique-to-drill``. Drills are
    deduplicated by slug; the first reaching edge is kept as ``via``.
    """
    anatomy_demands = [
        AnatomyDemand(
            region=entry["region"],
            concept_slug=_region_to_concept_slug(entry["region"]),
            criticality=entry.get("criticality", "optional"),
            insight=_anatomy_insight_for(
                _region_to_concept_slug(entry["region"]), indexes.page_insights
            ),
            supports_technique=entry.get("supports_technique"),
            for_role=entry.get("for_role"),
        )
        for entry in indexes.play_to_anatomy.get(play_slug, [])
    ]
    technique_demands = [
        TechniqueDemand(
            technique_id=entry["id"],
            concept_slug=_resolve_technique_slug(entry["id"], indexes.technique_aliases),
            role=entry.get("role"),
            criticality=entry.get("criticality", "optional"),
        )
        for entry in indexes.play_to_technique.get(play_slug, [])
    ]
    seen: set[str] = set()
    drills: list[DrillPrescription] = []
    for a in anatomy_demands:
        for edge in indexes.anatomy_to_drill.get(a.region, []):
            slug = edge["drill"]
            if slug in seen:
                continue
            seen.add(slug)
            drills.append(
                DrillPrescription(
                    drill_slug=slug,
                    emphasis=edge.get("emphasis", "secondary"),
                    via=f"anatomy:{a.region}",
                    insight=_drill_insight_for(slug, indexes.page_insights),
                    target_region=a.region,
                    target_technique=a.supports_technique,
                    target_role=a.for_role,
                )
            )
    for t in technique_demands:
        for edge in indexes.technique_to_drill.get(t.technique_id, []):
            slug = edge["drill"]
            if slug in seen:
                continue
            seen.add(slug)
            drills.append(
                DrillPrescription(
                    drill_slug=slug,
                    emphasis=edge.get("emphasis", "secondary"),
                    via=f"technique:{t.technique_id}",
                    insight=_drill_insight_for(slug, indexes.page_insights),
                    target_technique=t.technique_id,
                    target_role=t.role,
                )
            )
    drills.sort(key=lambda d: (0 if d.emphasis == "primary" else 1, d.drill_slug))
    defending_edges: list[DefendingEdge] = []
    for raw in indexes.play_to_defending.get(play_slug, []):
        d_slug = raw.get("defending")
        shared = raw.get("shared_tags") or []
        if not isinstance(d_slug, str) or not d_slug:
            continue
        payload = indexes.defending_insights.get(d_slug) or {}
        symptoms_raw = payload.get("symptoms") or []
        symptoms = [
            DefensiveSymptom(
                symptom=entry.get("symptom", ""),
                remedy=entry.get("remedy", ""),
            )
            for entry in symptoms_raw
            if isinstance(entry, dict) and entry.get("symptom")
        ]
        defending_edges.append(
            DefendingEdge(
                defending_slug=d_slug,
                shared_tags=[t for t in shared if isinstance(t, str)],
                symptoms=symptoms,
            )
        )
    signature: list[SignatureEntry] = []
    for raw in indexes.play_to_signature.get(play_slug, []):
        factor = raw.get("factor")
        direction = raw.get("direction")
        magnitude = raw.get("magnitude")
        rationale = raw.get("rationale") or ""
        if not factor or not direction or not magnitude:
            continue
        signature.append(
            SignatureEntry(
                factor=factor,
                direction=direction,
                magnitude=magnitude,
                rationale=rationale,
                concept_slug=raw.get("concept_slug"),
            )
        )
    counters: list[CounterEntry] = []
    for raw in indexes.play_to_counters.get(play_slug, []):
        text = raw.get("text") or ""
        extraction = raw.get("extraction") or "llm-inferred"
        if not text:
            continue
        counters.append(
            CounterEntry(
                text=text,
                extraction=extraction,
                source_hint=raw.get("source_hint"),
            )
        )
    return PlayContext(
        play_slug=play_slug,
        anatomy=anatomy_demands,
        techniques=technique_demands,
        drills=drills,
        defending=defending_edges,
        signature=signature,
        counters=counters,
    )


# --- Q-B: readiness filter ---------------------------------------------------


def build_readiness_filter(
    flagged_regions: list[str],
    indexes: CompiledIndexes,
) -> ReadinessBundle:
    """Return safe plays + primary-emphasis recovery drills for flagged regions.

    Spec §7 Q-B: a play is excluded iff any flagged region appears on it at
    ``criticality == required``. Prescription drills are the
    ``emphasis == primary`` entries in ``anatomy-to-drill`` for the flagged
    regions.
    """
    excluded: set[str] = set()
    prescription: list[DrillPrescription] = []
    seen_drills: set[str] = set()
    for region in flagged_regions:
        for entry in indexes.anatomy_to_play.get(region, []):
            if entry.get("criticality") == "required":
                excluded.add(entry["play"])
        for entry in indexes.anatomy_to_drill.get(region, []):
            if entry.get("emphasis") != "primary":
                continue
            slug = entry["drill"]
            if slug in seen_drills:
                continue
            seen_drills.add(slug)
            prescription.append(
                DrillPrescription(
                    drill_slug=slug,
                    emphasis="primary",
                    via=f"anatomy:{region}",
                )
            )
    all_plays = set(indexes.play_to_anatomy.keys()) | set(indexes.play_to_technique.keys())
    safe = sorted(all_plays - excluded)
    return ReadinessBundle(
        flagged_regions=list(flagged_regions),
        excluded_plays=sorted(excluded),
        safe_plays=safe,
        prescription_drills=prescription,
    )


# --- Q-C: drill justification ------------------------------------------------


def build_drill_justification(drill_slug: str, indexes: CompiledIndexes) -> list[str]:
    """Return the sorted list of play slugs this drill prepares for.

    Spec §7 Q-C: invert ``anatomy-to-drill`` and ``technique-to-drill`` to
    find what the drill trains, then look up ``anatomy-to-play`` and
    ``technique-to-play`` with a ``criticality == required`` filter.
    """
    regions = [
        region
        for region, drills in indexes.anatomy_to_drill.items()
        if any(d["drill"] == drill_slug for d in drills)
    ]
    technique_ids = [
        tid
        for tid, drills in indexes.technique_to_drill.items()
        if any(d["drill"] == drill_slug for d in drills)
    ]
    plays: set[str] = set()
    for region in regions:
        for entry in indexes.anatomy_to_play.get(region, []):
            if entry.get("criticality") == "required":
                plays.add(entry["play"])
    for tid in technique_ids:
        for entry in indexes.technique_to_play.get(tid, []):
            if entry.get("criticality") == "required":
                plays.add(entry["play"])
    return sorted(plays)


# --- Q-D: form-coach context (Phase 1) ---------------------------------------


def _wiki_page_exists(slug: str, indexes: CompiledIndexes) -> bool:
    """Check whether a page slug appears anywhere in the compiled graph.

    Cheap proxy: if the slug shows up as a wikilink target, in page-tags,
    or as the source of a wikilink, it has a backing page. Avoids a
    filesystem read at retrieval time.
    """
    return (
        slug in indexes.page_tags
        or slug in indexes.wikilink_forward
        or slug in indexes.wikilink_reverse
    )


def build_form_context(
    shot_type: str,
    measurements: list[FormMeasurement],
    indexes: CompiledIndexes,
    keyframe_count: int = 0,
) -> FormContext:
    """Assemble the Phase-1 form-coach retrieval bundle.

    Picks anatomy + technique + drill focus from :data:`FORM_FOCUS` for
    the shot type, filters to pages that actually exist in the wiki, and
    pulls drills via the existing anatomy → drill graph so prescriptions
    resolve through the same chain ``play_brief`` uses.
    """
    focus = FORM_FOCUS.get(shot_type) or FORM_FOCUS["unknown"]

    anatomy_demands: list[AnatomyDemand] = []
    for region in focus["anatomy"]:
        concept_slug = _region_to_concept_slug(region)
        if not _wiki_page_exists(concept_slug, indexes):
            continue
        anatomy_demands.append(
            AnatomyDemand(
                region=region,
                concept_slug=concept_slug,
                criticality="required",
                insight=_anatomy_insight_for(concept_slug, indexes.page_insights),
            )
        )

    technique_focus = [
        slug for slug in focus["techniques"] if _wiki_page_exists(slug, indexes)
    ]

    # Drills: union of primary-emphasis drills across the focus anatomy.
    seen: set[str] = set()
    drill_focus: list[str] = []
    for a in anatomy_demands:
        for edge in indexes.anatomy_to_drill.get(a.region, []):
            slug = edge["drill"]
            if slug in seen or edge.get("emphasis") != "primary":
                continue
            seen.add(slug)
            drill_focus.append(slug)
    drill_focus.sort()

    return FormContext(
        shot_type=shot_type,
        measurements=measurements,
        anatomy=anatomy_demands,
        technique_focus=technique_focus,
        drill_focus=drill_focus,
        keyframe_count=keyframe_count,
    )


# --- serialization -----------------------------------------------------------


def context_to_dict(ctx: PlayContext) -> dict[str, Any]:
    """Return a JSON-serialisable dict for ``PlayContext`` (future HTTP output)."""
    return asdict(ctx)


def readiness_to_dict(bundle: ReadinessBundle) -> dict[str, Any]:
    """Return a JSON-serialisable dict for ``ReadinessBundle``."""
    return asdict(bundle)


# --- Tag-match & defensive mirror -------------------------------------------

# Stopwords filtered out of tag token overlap — small words that match
# coincidentally without meaning (e.g. "to" in "man-to-man" vs "to" anywhere).
_TAG_STOPWORDS: frozenset[str] = frozenset(
    {"to", "of", "a", "the", "on", "in", "and", "or", "for", "at", "from"}
)


def _tag_tokens(tag: str) -> set[str]:
    """Lowercase split of a kebab-case tag into its content tokens."""
    return {word for word in tag.lower().split("-") if word and word not in _TAG_STOPWORDS}


def _tag_overlap_score(play_tags: list[str], other_tags: list[str]) -> tuple[int, list[str]]:
    """Return (score, matched play tags).

    Score = number of *play* tags that share at least one non-stopword token
    with any tag on the other page. Matched tags list preserves the play's
    own tag wording so the UI can show "matched on: step-up-screen".
    """
    other_tokens: set[str] = set()
    for tag in other_tags:
        other_tokens.update(_tag_tokens(tag))
    matched: list[str] = []
    for tag in play_tags:
        play_tokens = _tag_tokens(tag)
        if play_tokens & other_tokens:
            matched.append(tag)
    return len(matched), matched


# --- Native-graph helpers (wikilink + citation + formation) -----------------


def get_outgoing_links(slug: str, indexes: CompiledIndexes) -> list[str]:
    """Return the unique wikilink targets declared in ``slug``'s body."""
    return list(indexes.wikilink_forward.get(slug, []))


def get_incoming_links(slug: str, indexes: CompiledIndexes) -> list[str]:
    """Return the pages whose body wikilinks point at ``slug``.

    This is the reverse view of the native Karpathy cross-refs. Only ~21% of
    pairs are reciprocal in the corpus, so this often surfaces pages the
    target itself doesn't link back to (asymmetric graph).
    """
    return list(indexes.wikilink_reverse.get(slug, []))


def get_formation_siblings(play_slug: str, indexes: CompiledIndexes) -> list[str]:
    """Return other plays sharing this play's formation, excluding itself.

    Derived from the ``formation:`` front-matter on play pages. Returns [] if
    the play has no formation set or its formation has only one member.
    """
    # Find this play's formation by reverse lookup in the formation graph.
    for _formation, plays in indexes.formation_graph.items():
        if play_slug in plays:
            return [p for p in plays if p != play_slug]
    return []


def get_cite_cluster(citation_key: str, indexes: CompiledIndexes) -> list[str]:
    """Return pages citing the exact ``[Sn, p.X]`` key.

    Key normalization matches the compiler: ``"S2"`` for source-only, or
    ``"S2, p.32"`` / ``"S2, pp.18-19"`` for page-anchored citations.
    """
    return list(indexes.citation_graph.get(citation_key, []))


def get_shared_citation_pages(
    slug: str,
    indexes: CompiledIndexes,
    max_cluster_size: int = 50,
) -> list[str]:
    """Return distinct pages that cite any of the same ``[Sn, p.X]`` anchors ``slug`` cites.

    Walks: slug → (cite keys it uses via citation_graph reverse lookup) → (other
    pages citing those same keys). Excludes ``slug`` itself. ``max_cluster_size``
    bounds expansion per cite key so one very-common citation doesn't flood
    the result; keys above the cap are skipped.
    """
    # First find which citation keys `slug` appears in (inverse of citation_graph).
    my_keys: list[str] = [key for key, pages in indexes.citation_graph.items() if slug in pages]
    if not my_keys:
        return []
    seen: set[str] = {slug}
    out: list[str] = []
    for key in my_keys:
        cluster = indexes.citation_graph.get(key, [])
        if len(cluster) > max_cluster_size:
            continue
        for page in cluster:
            if page in seen:
                continue
            seen.add(page)
            out.append(page)
    return out


def build_defensive_mirror(
    play_slug: str,
    indexes: CompiledIndexes,
    top_k: int = 3,
    min_score: int = 1,
) -> list[DefensiveMatch]:
    """Tag-match a play against all defending pages; return the top-scoring matches.

    Each match carries the defending page's parsed symptoms (the defense's
    failure modes — which are the offense's attack surface). Filtering by
    ``min_score`` drops incidental single-word overlaps.
    """
    play_tags = indexes.page_tags.get(play_slug, [])
    if not play_tags:
        return []

    candidates: list[DefensiveMatch] = []
    for slug, payload in indexes.defending_insights.items():
        defending_tags = payload.get("tags") or []
        score, matched = _tag_overlap_score(play_tags, defending_tags)
        if score < min_score:
            continue
        symptoms_raw = payload.get("symptoms") or []
        symptoms = [
            DefensiveSymptom(
                symptom=entry.get("symptom", ""),
                remedy=entry.get("remedy", ""),
            )
            for entry in symptoms_raw
            if isinstance(entry, dict) and entry.get("symptom")
        ]
        diagram = payload.get("diagram")
        candidates.append(
            DefensiveMatch(
                defending_slug=slug,
                overlap_score=score,
                matched_tags=matched,
                symptoms=symptoms,
                diagram=diagram if isinstance(diagram, dict) else None,
            )
        )
    # Sort: higher score first, then prefer pages with an authored diagram
    # (so visual content surfaces ahead of text-only ties), then alphabetical.
    candidates.sort(key=lambda m: (-m.overlap_score, 0 if m.diagram else 1, m.defending_slug))
    return candidates[:top_k]


# --- Practice generator (v0) -----------------------------------------------

_LEVEL_ORDER: dict[str, int] = {"beginner": 0, "intermediate": 1, "advanced": 2}


def _level_compatible(drill_level: str | None, request_level: str) -> bool:
    """A drill is usable at request_level if its own level is at-or-below.

    Beginner request → beginner drills only.
    Intermediate request → beginner + intermediate.
    Advanced request → all three.
    Drills with no level metadata are accepted (conservative — better to
    surface than hide; coach can skip).
    """
    if drill_level is None:
        return True
    if drill_level not in _LEVEL_ORDER or request_level not in _LEVEL_ORDER:
        return True
    return _LEVEL_ORDER[drill_level] <= _LEVEL_ORDER[request_level]


def _coerce_duration(value: Any) -> int | None:
    """Coerce a drill `duration_minutes` field into an upper-bound int.

    The wiki schema allows int (``5``) or range string (``"5-10"``,
    ``"30-45"``). For practice planning we want the upper bound — that's
    what the coach should budget for.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        s = value.strip()
        if "-" in s:
            parts = s.split("-", 1)
            try:
                return int(parts[1].strip())
            except (ValueError, IndexError):
                return None
        try:
            return int(s)
        except ValueError:
            return None
    return None


def _drill_duration_ok(drill_dur: Any, budget: int) -> bool:
    """A drill's nominal duration must fit inside the practice budget.

    Drill `duration_minutes` may be int, string range (``"5-10"``), or
    missing. If unparseable, accept conservatively.
    """
    coerced = _coerce_duration(drill_dur)
    if coerced is None:
        return True
    return coerced <= budget


def build_practice_context(
    level: str,
    duration_minutes: int,
    focus_areas: list[str],
    indexes: CompiledIndexes,
    plays_in_library: list[str] | None = None,
) -> PracticeContext:
    """Assemble the v0 practice-generator retrieval bundle.

    For each focus area, walk the anatomy + technique edges into candidate
    drills, filter by level + duration budget, dedupe, sort primary-first.
    Cap candidates so the composer prompt stays under ~30 drills.
    """
    anatomy_slugs: list[str] = []
    technique_slugs: list[str] = []
    for area in focus_areas:
        focus = PRACTICE_FOCUS.get(area)
        if not focus:
            continue
        for region in focus["anatomy"]:
            if region not in anatomy_slugs:
                anatomy_slugs.append(region)
        for tech in focus["techniques"]:
            if tech not in technique_slugs:
                technique_slugs.append(tech)

    anatomy_demands: list[AnatomyDemand] = []
    for region in anatomy_slugs:
        concept_slug = _region_to_concept_slug(region)
        if not _wiki_page_exists(concept_slug, indexes):
            continue
        anatomy_demands.append(
            AnatomyDemand(
                region=region,
                concept_slug=concept_slug,
                criticality="required",
                insight=_anatomy_insight_for(concept_slug, indexes.page_insights),
            )
        )

    technique_focus = [
        slug for slug in technique_slugs if _wiki_page_exists(slug, indexes)
    ]

    seen: set[str] = set()
    candidates: list[PracticeDrillCandidate] = []

    for region in anatomy_slugs:
        for edge in indexes.anatomy_to_drill.get(region, []):
            slug = edge["drill"]
            if slug in seen:
                continue
            edge_level = edge.get("level")
            edge_duration = _coerce_duration(edge.get("duration_minutes"))
            if not _level_compatible(edge_level, level):
                continue
            if not _drill_duration_ok(edge_duration, duration_minutes):
                continue
            seen.add(slug)
            candidates.append(
                PracticeDrillCandidate(
                    drill_slug=slug,
                    emphasis=edge.get("emphasis") or "secondary",
                    via_anatomy=region,
                    via_technique=None,
                    level=edge_level,
                    duration_minutes=edge_duration,
                )
            )

    for tech in technique_slugs:
        # Strip "concept-technique-" prefix to match the technique_to_drill key.
        tech_id = tech.removeprefix("concept-technique-")
        for edge in indexes.technique_to_drill.get(tech_id, []):
            slug = edge["drill"]
            if slug in seen:
                continue
            edge_level = edge.get("level")
            edge_duration = _coerce_duration(edge.get("duration_minutes"))
            if not _level_compatible(edge_level, level):
                continue
            if not _drill_duration_ok(edge_duration, duration_minutes):
                continue
            seen.add(slug)
            candidates.append(
                PracticeDrillCandidate(
                    drill_slug=slug,
                    emphasis=edge.get("emphasis") or "secondary",
                    via_anatomy=None,
                    via_technique=tech,
                    level=edge_level,
                    duration_minutes=edge_duration,
                )
            )

    # Sort: primary first, then alphabetical for stability.
    candidates.sort(key=lambda c: (0 if c.emphasis == "primary" else 1, c.drill_slug))

    # Cap: keep prompt size sane. 30 drills is plenty for a 5-7 block plan.
    candidates = candidates[:30]

    return PracticeContext(
        level=level,
        duration_minutes=duration_minutes,
        focus_areas=focus_areas,
        anatomy=anatomy_demands,
        techniques=technique_focus,
        candidate_drills=candidates,
        plays_in_library=plays_in_library or [],
    )
