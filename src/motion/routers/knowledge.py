"""Knowledge-retrieval HTTP endpoints.

Thin HTTP wrapper over ``motion.wiki_ops.retrieval``. Each route maps 1:1
to one of the three query patterns in ``spec/crossref-anatomy-chain.md`` §7:

- ``POST /api/knowledge/play-context``      — Q-A drill prescription
- ``POST /api/knowledge/readiness``         — Q-B readiness filter
- ``POST /api/knowledge/drill-justification`` — Q-C drill justification

Indexes are loaded once at first-request time and cached in module state.
Re-compile of the wiki (``python -m motion.wiki_ops crossref``) requires
a process restart to pick up the new JSON.
"""

from __future__ import annotations

from functools import lru_cache

from fastapi import APIRouter

from motion.schemas.knowledge import (
    AnatomyDemandOut,
    AnatomyInsightOut,
    CommonMistakeOut,
    CourtDiagramOut,
    DefensiveMatchOut,
    DefensiveSymptomOut,
    DiagramArrowOut,
    DiagramPositionOut,
    DrillInsightOut,
    DrillJustificationRequest,
    DrillJustificationResponse,
    DrillPrescriptionOut,
    KeyPrincipleOut,
    PlayBriefRequest,
    PlayBriefResponse,
    PlayContextRequest,
    PlayContextResponse,
    PrimaryFormErrorOut,
    ReadinessRequest,
    ReadinessResponse,
    SafetyTipOut,
    TechniqueDemandOut,
)
from motion.services.play_brief import build_brief
from motion.wiki_ops.retrieval import (
    CompiledIndexes,
    build_defensive_mirror,
    build_drill_justification,
    build_play_context,
    build_readiness_filter,
    load_indexes,
)

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@lru_cache(maxsize=1)
def _cached_indexes() -> CompiledIndexes:
    return load_indexes()


def _anatomy_insight_out(insight: object) -> AnatomyInsightOut | None:
    if insight is None:
        return None
    return AnatomyInsightOut(
        key_principles=[
            KeyPrincipleOut(text=p["text"], citation=p.get("citation"))
            for p in getattr(insight, "key_principles", [])
            if isinstance(p, dict) and p.get("text")
        ],
        common_mistakes=[
            CommonMistakeOut(
                symptom=m["symptom"],
                consequence=m.get("consequence"),
                remedy=m.get("remedy"),
                citation=m.get("citation"),
            )
            for m in getattr(insight, "common_mistakes", [])
            if isinstance(m, dict) and m.get("symptom")
        ],
    )


def _drill_insight_out(insight: object) -> DrillInsightOut | None:
    if insight is None:
        return None
    safety_tip_raw = getattr(insight, "safety_tip", None)
    form_error_raw = getattr(insight, "primary_form_error", None)
    safety_tip = (
        SafetyTipOut(text=safety_tip_raw["text"], citation=safety_tip_raw.get("citation"))
        if isinstance(safety_tip_raw, dict) and safety_tip_raw.get("text")
        else None
    )
    primary_form_error = (
        PrimaryFormErrorOut(
            symptom=form_error_raw["symptom"],
            consequence=form_error_raw.get("consequence"),
            citation=form_error_raw.get("citation"),
        )
        if isinstance(form_error_raw, dict) and form_error_raw.get("symptom")
        else None
    )
    return DrillInsightOut(
        safety_tip=safety_tip,
        coaching_cue=getattr(insight, "coaching_cue", None),
        primary_form_error=primary_form_error,
    )


def _anatomy_out(demands: list) -> list[AnatomyDemandOut]:
    return [
        AnatomyDemandOut(
            region=a.region,
            concept_slug=a.concept_slug,
            criticality=a.criticality,
            insight=_anatomy_insight_out(a.insight),
            supports_technique=a.supports_technique,
            for_role=a.for_role,
        )
        for a in demands
    ]


def _technique_out(demands: list) -> list[TechniqueDemandOut]:
    return [
        TechniqueDemandOut(
            technique_id=t.technique_id,
            concept_slug=t.concept_slug,
            role=t.role,
            criticality=t.criticality,
        )
        for t in demands
    ]


def _drill_out(drills: list) -> list[DrillPrescriptionOut]:
    return [
        DrillPrescriptionOut(
            drill_slug=d.drill_slug,
            emphasis=d.emphasis,
            via=d.via,
            insight=_drill_insight_out(d.insight),
            target_region=d.target_region,
            target_technique=d.target_technique,
            target_role=d.target_role,
        )
        for d in drills
    ]


def _diagram_out(raw: object) -> CourtDiagramOut | None:
    if not isinstance(raw, dict):
        return None
    positions_raw = raw.get("positions") or []
    arrows_raw = raw.get("arrows") or []
    positions = [
        DiagramPositionOut(
            id=str(p["id"]),
            x=float(p.get("x", 0)),
            y=float(p.get("y", 0)),
            label=p.get("label"),
            role=p.get("role"),
            emphasis=p.get("emphasis"),
        )
        for p in positions_raw
        if isinstance(p, dict) and p.get("id") is not None
    ]
    arrows = [
        DiagramArrowOut(
            from_x=float(a.get("fromX", 0)),
            from_y=float(a.get("fromY", 0)),
            to_x=float(a.get("toX", 0)),
            to_y=float(a.get("toY", 0)),
            label=a.get("label"),
            emphasis=a.get("emphasis"),
        )
        for a in arrows_raw
        if isinstance(a, dict)
    ]
    return CourtDiagramOut(
        kind=str(raw.get("kind") or "half_court"),
        positions=positions,
        arrows=arrows,
    )


def _defensive_mirror_out(matches: list) -> list[DefensiveMatchOut]:
    return [
        DefensiveMatchOut(
            defending_slug=m.defending_slug,
            overlap_score=m.overlap_score,
            matched_tags=m.matched_tags,
            symptoms=[DefensiveSymptomOut(symptom=s.symptom, remedy=s.remedy) for s in m.symptoms],
            diagram=_diagram_out(m.diagram),
        )
        for m in matches
    ]


@router.post("/play-context", response_model=PlayContextResponse)
async def play_context(request: PlayContextRequest) -> PlayContextResponse:
    """Q-A + defensive mirror: return the joined retrieval bundle for a play."""
    indexes = _cached_indexes()
    ctx = build_play_context(request.play_slug, indexes)
    mirror = build_defensive_mirror(request.play_slug, indexes, top_k=3)
    return PlayContextResponse(
        play_slug=ctx.play_slug,
        anatomy=_anatomy_out(ctx.anatomy),
        techniques=_technique_out(ctx.techniques),
        drills=_drill_out(ctx.drills),
        defensive_mirror=_defensive_mirror_out(mirror),
    )


@router.post("/readiness", response_model=ReadinessResponse)
async def readiness(request: ReadinessRequest) -> ReadinessResponse:
    """Q-B: filter playable-tonight set + prescribe recovery drills."""
    bundle = build_readiness_filter(request.flagged_regions, _cached_indexes())
    return ReadinessResponse(
        flagged_regions=bundle.flagged_regions,
        excluded_plays=bundle.excluded_plays,
        safe_plays=bundle.safe_plays,
        prescription_drills=_drill_out(bundle.prescription_drills),
    )


@router.post("/drill-justification", response_model=DrillJustificationResponse)
async def drill_justification(
    request: DrillJustificationRequest,
) -> DrillJustificationResponse:
    """Q-C: return plays this drill prepares (filtered to criticality=required)."""
    plays = build_drill_justification(request.drill_slug, _cached_indexes())
    return DrillJustificationResponse(drill_slug=request.drill_slug, plays=plays)


@router.post("/play-brief", response_model=PlayBriefResponse)
async def play_brief(request: PlayBriefRequest) -> PlayBriefResponse:
    """Compose a 3-sentence coaching brief over the play's cross-ref bundle.

    Falls back to a deterministic stub when no ``ANTHROPIC_API_KEY`` is set
    or the Claude call fails — the UX never dead-ends.
    """
    context = build_play_context(request.play_slug, _cached_indexes())
    readiness_dicts = (
        [r.model_dump(by_alias=False) for r in request.roster_readiness]
        if request.roster_readiness
        else None
    )
    result = build_brief(context, readiness_dicts)
    return PlayBriefResponse(
        play_slug=request.play_slug,
        brief=result.brief,
        source_citations=result.source_citations,
        source=result.source,
    )
