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
