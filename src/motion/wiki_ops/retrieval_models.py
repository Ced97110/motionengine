"""Dataclasses for the retrieval bundle.

Split out of ``retrieval.py`` so that file holds queries only. Importers
should continue to use ``from motion.wiki_ops.retrieval import X`` — the
parent module re-exports everything.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
class DefensiveSymptom:
    """One symptom/remedy pair parsed from a defending page's ``## Common Mistakes``."""

    symptom: str
    remedy: str


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

    Produced by ``build_form_context``. Carries the shot type, the flagged +
    within-threshold measurements, and the anatomy / technique / drill focus
    slugs picked from the existing knowledge graph for this shot type.
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
