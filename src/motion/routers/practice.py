"""Practice-generator HTTP endpoint — v0 of the graph-grounded coach wedge.

POST /api/practice/generate takes coach inputs (level, duration, focus areas)
and returns an Engine-composed 5-7 block timed practice plan grounded in the
wiki cross-ref graph (anatomy ↔ technique ↔ drill).

No DB; reads compiled cross-ref sidecars from disk (cached). Falls back to
the deterministic stub when ``ANTHROPIC_API_KEY`` is unset or the Claude
call fails — UX never dead-ends.
"""

from __future__ import annotations

import re
from functools import lru_cache

from fastapi import APIRouter, HTTPException

from motion.schemas.knowledge import (
    PracticeBlockOut,
    PracticeRequest,
    PracticeResponse,
)
from motion.services.practice_brief import build_practice_brief
from motion.wiki_ops.retrieval import (
    CompiledIndexes,
    build_practice_context,
    load_indexes,
)

router = APIRouter(prefix="/api/practice", tags=["practice"])

_VALID_LEVELS: frozenset[str] = frozenset({"beginner", "intermediate", "advanced"})
_VALID_DURATIONS: frozenset[int] = frozenset({30, 45, 60, 90, 120})
_VALID_FOCUS: frozenset[str] = frozenset(
    {
        "shooting",
        "ball-handling",
        "finishing",
        "defense",
        "conditioning",
        "scrimmage",
        "free-throws",
        "rebounding",
    }
)
_MAX_FOCUS_AREAS: int = 4
_MAX_PLAYS_IN_LIBRARY: int = 20

_PLAY_SLUG_RE = re.compile(r"^play-[a-z0-9][a-z0-9-]+$")
_SLUG_RE = re.compile(r"\b((?:concept|drill|exercise|play)-[a-z0-9][a-z0-9-]+)\b")


@lru_cache(maxsize=1)
def _cached_indexes() -> CompiledIndexes:
    return load_indexes()


def _extract_cross_refs(text: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for match in _SLUG_RE.finditer(text):
        slug = match.group(1)
        if slug in seen:
            continue
        seen.add(slug)
        out.append(slug)
    return out


@router.post("/generate", response_model=PracticeResponse)
async def generate(request: PracticeRequest) -> PracticeResponse:
    """Compose a practice plan from coach inputs grounded in the wiki graph."""
    if request.level not in _VALID_LEVELS:
        raise HTTPException(
            status_code=400,
            detail=f"level must be one of {sorted(_VALID_LEVELS)}",
        )
    if request.duration_minutes not in _VALID_DURATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"duration_minutes must be one of {sorted(_VALID_DURATIONS)}",
        )
    if not request.focus_areas:
        raise HTTPException(
            status_code=400,
            detail="focus_areas must contain at least one entry",
        )
    if len(request.focus_areas) > _MAX_FOCUS_AREAS:
        raise HTTPException(
            status_code=400,
            detail=f"focus_areas capped at {_MAX_FOCUS_AREAS}",
        )
    bad_focus = [f for f in request.focus_areas if f not in _VALID_FOCUS]
    if bad_focus:
        raise HTTPException(
            status_code=400,
            detail=(
                f"unknown focus area(s) {bad_focus} — allowed: {sorted(_VALID_FOCUS)}"
            ),
        )
    if len(request.plays_in_library) > _MAX_PLAYS_IN_LIBRARY:
        raise HTTPException(
            status_code=400,
            detail=f"plays_in_library capped at {_MAX_PLAYS_IN_LIBRARY}",
        )
    bad_plays = [
        p for p in request.plays_in_library if not _PLAY_SLUG_RE.match(p)
    ]
    if bad_plays:
        raise HTTPException(
            status_code=400,
            detail=f"invalid play slug(s): {bad_plays}",
        )

    context = build_practice_context(
        level=request.level,
        duration_minutes=request.duration_minutes,
        focus_areas=list(request.focus_areas),
        indexes=_cached_indexes(),
        plays_in_library=list(request.plays_in_library),
    )

    result = build_practice_brief(context)

    blocks_out = [
        PracticeBlockOut(
            drill_slug=b.drill_slug,
            duration_minutes=b.duration_minutes,
            reasoning=b.reasoning,
            cross_refs=b.cross_refs,
        )
        for b in result.plan
    ]
    union_refs: list[str] = []
    for b in blocks_out:
        for ref in b.cross_refs:
            if ref not in union_refs:
                union_refs.append(ref)

    return PracticeResponse(
        level=request.level,
        duration_minutes=request.duration_minutes,
        focus_areas=list(request.focus_areas),
        plan=blocks_out,
        source_citations=result.source_citations,
        source=result.source,
        cross_refs=union_refs,
    )
