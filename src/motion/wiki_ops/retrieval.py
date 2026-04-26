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
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from motion.sports import DEFAULT_SPORT, Sport

from .paths import wiki_dir

# --- dataclasses -------------------------------------------------------------


@dataclass(frozen=True)
class AnatomyInsight:
    """Insight payload for a concept-anatomy page (coaching content)."""

    key_principles: list[dict[str, str]] = field(default_factory=list)
    common_mistakes: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class DrillInsight:
    """Insight payload for a drill or exercise page."""

    safety_tip: dict[str, str] | None = None
    coaching_cue: str | None = None
    primary_form_error: dict[str, str] | None = None


@dataclass(frozen=True)
class AnatomyDemand:
    """One entry of ``play.demands_anatomy`` with its concept-page slug."""

    region: str
    concept_slug: str
    criticality: str
    insight: AnatomyInsight | None = None
    supports_technique: str | None = None
    for_role: str | None = None


@dataclass(frozen=True)
class TechniqueDemand:
    """One entry of ``play.demands_techniques`` with its resolved concept slug."""

    technique_id: str
    concept_slug: str | None
    role: str | None
    criticality: str


@dataclass(frozen=True)
class DrillPrescription:
    """One prescribed drill, with the edge it was reached through.

    ``target_technique`` and ``target_role`` are populated when the drill was
    reached via an anatomy region that carries a ``supports_technique`` /
    ``for_role`` linkage on the play's front-matter (edge #1 enriched authoring).
    They let the UI render play-grounded sentences like "prepares role 5's
    hard flash cut" instead of machine-slug traversal labels.
    """

    drill_slug: str
    emphasis: str
    via: str
    insight: DrillInsight | None = None
    target_region: str | None = None
    target_technique: str | None = None
    target_role: str | None = None


@dataclass(frozen=True)
class DefendingEdge:
    """A compiled play↔defending match with the shared-tag rationale."""

    defending_slug: str
    shared_tags: list[str]
    symptoms: list[DefensiveSymptom] = field(default_factory=list)


@dataclass(frozen=True)
class SignatureEntry:
    """One Four-Factor signature direction declared on a play."""

    factor: str
    direction: str
    magnitude: str
    rationale: str
    concept_slug: str | None = None


@dataclass(frozen=True)
class CounterEntry:
    """One structured counter bullet with provenance label.

    ``extraction`` ∈ {"verbatim", "paraphrase", "llm-inferred"}. Engine
    consumers surface only ``llm-inferred`` entries on user chrome — the
    other two flags mark book-derived prose that must not surface.
    """

    text: str
    extraction: str
    source_hint: str | None = None


@dataclass(frozen=True)
class FormMeasurement:
    """One computed signal extracted from the player's joint timeline.

    Computed client-side from MediaPipe Pose Landmarker output. Examples:

    - ``elbow_flair`` (degrees from vertical at release)
    - ``follow_through_droop`` (degrees of wrist drop after release)
    - ``knee_valgus`` (degrees of inward knee collapse on landing)
    - ``trunk_lean`` (degrees forward at peak)
    - ``release_height_ratio`` (release point / player height)
    """

    name: str
    value: float
    unit: str  # "deg" | "ratio" | "px"
    flagged: bool
    threshold: float


@dataclass(frozen=True)
class FormContext:
    """Phase-1 form-coach retrieval bundle.

    Produced by :func:`build_form_context`. Carries the shot type, the
    flagged + within-threshold measurements, and the anatomy / technique /
    drill focus slugs picked from the existing knowledge graph for this
    shot type.
    """

    shot_type: str
    measurements: list[FormMeasurement] = field(default_factory=list)
    anatomy: list[AnatomyDemand] = field(default_factory=list)
    technique_focus: list[str] = field(default_factory=list)
    drill_focus: list[str] = field(default_factory=list)
    keyframe_count: int = 0


@dataclass(frozen=True)
class PlayContext:
    """Full retrieval bundle for a single play (Q-A output)."""

    play_slug: str
    anatomy: list[AnatomyDemand] = field(default_factory=list)
    techniques: list[TechniqueDemand] = field(default_factory=list)
    drills: list[DrillPrescription] = field(default_factory=list)
    defending: list[DefendingEdge] = field(default_factory=list)
    signature: list[SignatureEntry] = field(default_factory=list)
    counters: list[CounterEntry] = field(default_factory=list)


@dataclass(frozen=True)
class PracticeDrillCandidate:
    """One drill the practice composer can pick from.

    Carries the metadata the composer needs to score + place the drill in a
    timed block: the slug, why it surfaced (which anatomy / technique edge),
    the drill's own level + nominal duration, and emphasis (primary first).
    """

    drill_slug: str
    emphasis: str  # "primary" | "secondary"
    via_anatomy: str | None
    via_technique: str | None
    level: str | None  # beginner | intermediate | advanced (from drill frontmatter)
    duration_minutes: int | None  # nominal duration of one rep block


@dataclass(frozen=True)
class PracticeContext:
    """Practice-generator retrieval bundle (v0).

    `plays_in_library` is plumbed through for v1 team-context wiring (M5);
    v0 builders ignore it.
    """

    level: str
    duration_minutes: int
    focus_areas: list[str]
    anatomy: list[AnatomyDemand] = field(default_factory=list)
    techniques: list[str] = field(default_factory=list)
    candidate_drills: list[PracticeDrillCandidate] = field(default_factory=list)
    plays_in_library: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ReadinessBundle:
    """Q-B output: safe plays + primary-emphasis prescription drills."""

    flagged_regions: list[str]
    excluded_plays: list[str]
    safe_plays: list[str]
    prescription_drills: list[DrillPrescription]


@dataclass(frozen=True)
class DefensiveSymptom:
    """One symptom/remedy pair parsed from a defending page's ``## Common Mistakes``."""

    symptom: str
    remedy: str


@dataclass(frozen=True)
class DefensiveMatch:
    """A defending page relevant to a play, scored by tag overlap."""

    defending_slug: str
    overlap_score: int
    matched_tags: list[str]
    symptoms: list[DefensiveSymptom]
    diagram: dict[str, Any] | None = None


@dataclass(frozen=True)
class CompiledIndexes:
    """Compiled cross-ref indexes + auxiliary lookups."""

    play_to_anatomy: dict[str, list[dict[str, str]]]
    play_to_technique: dict[str, list[dict[str, str]]]
    play_to_signature: dict[str, list[dict[str, str]]]
    play_to_counters: dict[str, list[dict[str, str]]]
    anatomy_to_play: dict[str, list[dict[str, str]]]
    anatomy_to_drill: dict[str, list[dict[str, str]]]
    technique_to_play: dict[str, list[dict[str, str]]]
    technique_to_drill: dict[str, list[dict[str, str]]]
    technique_aliases: dict[str, dict[str, Any]]
    page_insights: dict[str, dict[str, Any]]
    page_tags: dict[str, list[str]]
    defending_insights: dict[str, dict[str, Any]]
    play_to_defending: dict[str, list[dict[str, Any]]]
    # Native Karpathy cross-refs compiled from body prose (2026-04-20).
    wikilink_forward: dict[str, list[str]]
    wikilink_reverse: dict[str, list[str]]
    citation_graph: dict[str, list[str]]
    formation_graph: dict[str, list[str]]


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


# Shot-type → anatomy/technique/drill focus map. Hand-curated based on
# the existing wiki concept pages. The anatomy regions referenced here
# may not all have concept-anatomy-* pages yet (shoulder_girdle,
# wrist_complex, elbow_complex are scheduled for Phase 1 day 3 authoring);
# `build_form_context` filters out missing pages so the bundle stays
# clean as content lands.
_FORM_FOCUS: dict[str, dict[str, list[str]]] = {
    "free-throw": {
        "anatomy": [
            "shoulder_girdle",
            "wrist_complex",
            "elbow_complex",
            "core_outer",
        ],
        "techniques": [
            "concept-jump-shot-mechanics",
            "concept-jump-shot-release-and-follow-through",
            "concept-quiet-eye-basketball-shooting",
            "concept-shooting-confidence-rhythm",
        ],
    },
    "jump-shot": {
        "anatomy": [
            "shoulder_girdle",
            "wrist_complex",
            "elbow_complex",
            "core_outer",
            "glute_max",
            "ankle_complex",
        ],
        "techniques": [
            "concept-jump-shot-biomechanics",
            "concept-jump-shot-mechanics",
            "concept-jump-shot-release-and-follow-through",
            "concept-midrange-jump-shot",
        ],
    },
    "layup": {
        "anatomy": [
            "hip_flexor_complex",
            "glute_max",
            "ankle_complex",
            "core_outer",
        ],
        "techniques": [
            "concept-1on1-reads-and-attacks",
            "concept-first-step-quickness",
        ],
    },
    "unknown": {
        "anatomy": ["core_outer"],
        "techniques": [],
    },
}


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

    Picks anatomy + technique + drill focus from :data:`_FORM_FOCUS` for
    the shot type, filters to pages that actually exist in the wiki, and
    pulls drills via the existing anatomy → drill graph so prescriptions
    resolve through the same chain ``play_brief`` uses.
    """
    focus = _FORM_FOCUS.get(shot_type) or _FORM_FOCUS["unknown"]

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
#
# `_PRACTICE_FOCUS` maps a coach-facing focus area (chip on the UI) to the
# anatomy regions and technique slugs the engine should traverse. Anatomy
# slugs MUST appear in the 7 concept-anatomy pages; technique slugs are
# concept-technique stems. `build_practice_context` filters out unknown pages
# at retrieval time so this map can list aspirational slugs without breaking.

_PRACTICE_FOCUS: dict[str, dict[str, list[str]]] = {
    "shooting": {
        "anatomy": ["wrist_complex", "elbow_complex", "shoulder_girdle", "core_outer"],
        "techniques": [],
    },
    "free-throws": {
        "anatomy": ["wrist_complex", "elbow_complex", "shoulder_girdle"],
        "techniques": [],
    },
    "ball-handling": {
        "anatomy": ["wrist_complex", "ankle_complex", "hip_flexor_complex"],
        "techniques": [],
    },
    "finishing": {
        "anatomy": [
            "ankle_complex",
            "glute_max",
            "hip_flexor_complex",
            "core_outer",
            "shoulder_girdle",
        ],
        "techniques": ["concept-technique-hard-cut-to-paint"],
    },
    "defense": {
        "anatomy": ["ankle_complex", "glute_max", "hip_flexor_complex", "core_outer"],
        "techniques": ["concept-technique-closeout-contest-verticality"],
    },
    "conditioning": {
        "anatomy": ["ankle_complex", "glute_max", "hip_flexor_complex", "core_outer"],
        "techniques": [],
    },
    "rebounding": {
        "anatomy": ["glute_max", "core_outer", "shoulder_girdle", "hip_flexor_complex"],
        "techniques": [],
    },
    "scrimmage": {
        "anatomy": [
            "ankle_complex",
            "glute_max",
            "hip_flexor_complex",
            "core_outer",
            "shoulder_girdle",
            "wrist_complex",
        ],
        "techniques": [],
    },
}

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
        focus = _PRACTICE_FOCUS.get(area)
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
