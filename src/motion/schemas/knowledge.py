"""Knowledge-retrieval request/response schemas.

Wraps ``motion.wiki_ops.retrieval`` dataclasses in Pydantic models with
camelCase aliases for the frontend contract (matches the pattern in
``schemas/errors.py``).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


# --- Common output fragments -------------------------------------------------


class KeyPrincipleOut(_CamelModel):
    text: str
    citation: str | None = None


class CommonMistakeOut(_CamelModel):
    symptom: str
    consequence: str | None = None
    remedy: str | None = None
    citation: str | None = None


class SafetyTipOut(_CamelModel):
    text: str
    citation: str | None = None


class PrimaryFormErrorOut(_CamelModel):
    symptom: str
    consequence: str | None = None
    citation: str | None = None


class AnatomyInsightOut(_CamelModel):
    key_principles: list[KeyPrincipleOut] = []
    common_mistakes: list[CommonMistakeOut] = []


class DrillInsightOut(_CamelModel):
    safety_tip: SafetyTipOut | None = None
    coaching_cue: str | None = None
    primary_form_error: PrimaryFormErrorOut | None = None


class AnatomyDemandOut(_CamelModel):
    region: str
    concept_slug: str
    criticality: str
    insight: AnatomyInsightOut | None = None
    supports_technique: str | None = None
    for_role: str | None = None


class TechniqueDemandOut(_CamelModel):
    technique_id: str
    concept_slug: str | None = None
    role: str | None = None
    criticality: str


class DrillPrescriptionOut(_CamelModel):
    drill_slug: str
    emphasis: str
    via: str
    insight: DrillInsightOut | None = None
    target_region: str | None = None
    target_technique: str | None = None
    target_role: str | None = None


# --- Q-A: play context -------------------------------------------------------


class DefensiveSymptomOut(_CamelModel):
    symptom: str
    remedy: str


class DiagramPositionOut(_CamelModel):
    id: str
    x: float
    y: float
    label: str | None = None
    role: str | None = None
    emphasis: str | None = None


class DiagramArrowOut(_CamelModel):
    from_x: float
    from_y: float
    to_x: float
    to_y: float
    label: str | None = None
    emphasis: str | None = None


class CourtDiagramOut(_CamelModel):
    kind: str
    positions: list[DiagramPositionOut] = []
    arrows: list[DiagramArrowOut] = []


class DefensiveMatchOut(_CamelModel):
    defending_slug: str
    overlap_score: int
    matched_tags: list[str]
    symptoms: list[DefensiveSymptomOut]
    diagram: CourtDiagramOut | None = None


class PlayContextRequest(_CamelModel):
    play_slug: str


class PlayContextResponse(_CamelModel):
    play_slug: str
    anatomy: list[AnatomyDemandOut]
    techniques: list[TechniqueDemandOut]
    drills: list[DrillPrescriptionOut]
    defensive_mirror: list[DefensiveMatchOut] = []
    # Native Karpathy cross-refs compiled from body-level edges:
    sibling_plays: list[str] = []  # same formation as this play
    incoming_references: list[str] = []  # pages whose body wikilinks point here
    outgoing_references: list[str] = []  # wikilinks this page declares in body
    shared_citation_pages: list[str] = []  # other pages citing the same [Sn, p.X]


# --- Q-B: readiness filter ---------------------------------------------------


class ReadinessRequest(_CamelModel):
    flagged_regions: list[str]


class ReadinessResponse(_CamelModel):
    flagged_regions: list[str]
    excluded_plays: list[str]
    safe_plays: list[str]
    prescription_drills: list[DrillPrescriptionOut]


# --- Q-C: drill justification ------------------------------------------------


class DrillJustificationRequest(_CamelModel):
    drill_slug: str


class DrillJustificationResponse(_CamelModel):
    drill_slug: str
    plays: list[str]


# --- Play brief (Engine-composed answer) -------------------------------------


class PlayerReadinessFlag(_CamelModel):
    """Optional roster-readiness input — flagged regions for one player."""

    player_name: str | None = None
    flagged_regions: list[str]


class PlayBriefRequest(_CamelModel):
    play_slug: str
    roster_readiness: list[PlayerReadinessFlag] | None = None


class PlayBriefResponse(_CamelModel):
    play_slug: str
    brief: str
    source_citations: list[str]
    source: str  # "claude" | "stub"


# --- Form-coach (Phase 1 video-grounded coaching) ----------------------------


class FormMeasurementIn(_CamelModel):
    """One client-computed measurement from MediaPipe joint output."""

    name: str
    value: float
    unit: str  # "deg" | "ratio" | "px"
    flagged: bool
    threshold: float


class FormCoachRequest(_CamelModel):
    """Phase-1 form-coach payload.

    Joint extraction runs in the browser (MediaPipe Pose Landmarker); we
    only receive the computed measurements + 0-3 keyframes (base64 JPEG).
    Raw video stays on the user's device.
    """

    shot_type: str  # "free-throw" | "jump-shot" | "layup" | "unknown"
    measurements: list[FormMeasurementIn]
    keyframes_base64: list[str] = []


class FormCoachResponse(_CamelModel):
    shot_type: str
    feedback: str
    source_citations: list[str]
    source: str  # "claude" | "stub"
    cross_refs: list[str]  # concept-anatomy + concept-technique + drill slugs cited


# --- Practice generator (v0) -------------------------------------------------


class PracticeRequest(_CamelModel):
    """Coach-supplied inputs for one practice plan.

    `plays_in_library` is reserved for v1 team-context wiring (M5); v0
    accepts but ignores the field.
    """

    level: str  # "beginner" | "intermediate" | "advanced"
    duration_minutes: int  # 30 | 45 | 60 | 90 | 120
    focus_areas: list[str]
    plays_in_library: list[str] = []


class PracticeBlockOut(_CamelModel):
    """One timed block in the generated practice plan."""

    drill_slug: str
    duration_minutes: int
    reasoning: str  # coach-voice 1-2 sentences, may embed cross-ref slugs
    cross_refs: list[str]  # slugs surfaced in reasoning (subset of plan-level)


class PracticeResponse(_CamelModel):
    level: str
    duration_minutes: int
    focus_areas: list[str]
    plan: list[PracticeBlockOut]
    source_citations: list[str]
    source: str  # "claude" | "stub"
    cross_refs: list[str]  # union across all blocks
