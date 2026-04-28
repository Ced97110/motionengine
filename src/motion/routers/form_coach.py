"""Form-coach HTTP endpoint — Phase 1 of the video-grounded coaching wedge.

POST /api/form-coach/analyze takes a per-shot payload (shot type +
client-computed measurements + 0-3 keyframe images) and returns
Engine-composed feedback in Motion voice grounded in the wiki concept
graph.

Joint extraction is intentionally NOT done server-side — MediaPipe runs
in the browser and we receive only the derived signals + a small image
payload. This keeps raw video off the server (privacy + cost) and keeps
the per-request payload small.

Falls back to the deterministic stub when ``ANTHROPIC_API_KEY`` is unset
or the Claude call fails — UX never dead-ends.
"""

from __future__ import annotations

import base64
import binascii
import re

from fastapi import APIRouter, HTTPException

from motion.schemas.knowledge import FormCoachRequest, FormCoachResponse
from motion.services.form_brief import build_form_brief
from motion.wiki_ops.retrieval import (
    FormMeasurement,
    build_form_context,
    cached_indexes,
)

router = APIRouter(prefix="/api/form-coach", tags=["form-coach"])

_VALID_SHOT_TYPES: frozenset[str] = frozenset(
    {"free-throw", "jump-shot", "layup", "unknown"}
)
_MAX_KEYFRAMES: int = 3
_MAX_KEYFRAME_BYTES: int = 1_500_000  # 1.5 MB after base64-decode — comfortable for a JPEG keyframe
_MAX_MEASUREMENTS: int = 20

_SLUG_RE = re.compile(r"\b((?:concept|drill|exercise)-[a-z0-9][a-z0-9-]+)\b")


def _decode_keyframe(b64: str) -> bytes:
    try:
        raw = base64.b64decode(b64, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=f"keyframe is not valid base64: {exc}",
        ) from exc
    if len(raw) > _MAX_KEYFRAME_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"keyframe exceeds {_MAX_KEYFRAME_BYTES // 1024} KB after decode",
        )
    return raw


def _extract_cross_refs(brief: str) -> list[str]:
    """Pull every concept-/drill-/exercise- slug out of the brief, in order, deduped."""
    seen: set[str] = set()
    out: list[str] = []
    for match in _SLUG_RE.finditer(brief):
        slug = match.group(1)
        if slug in seen:
            continue
        seen.add(slug)
        out.append(slug)
    return out


@router.post("/analyze", response_model=FormCoachResponse)
async def analyze(request: FormCoachRequest) -> FormCoachResponse:
    """Compose form-coach feedback for a single shot.

    Validates input, builds a ``FormContext`` over the shot type's anatomy
    + technique focus, calls the composer, and returns Motion-voice
    feedback with cross-ref slugs the frontend can render as deep links.
    """
    shot_type = request.shot_type
    if shot_type not in _VALID_SHOT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"shot_type must be one of {sorted(_VALID_SHOT_TYPES)}",
        )

    if len(request.measurements) > _MAX_MEASUREMENTS:
        raise HTTPException(
            status_code=400,
            detail=f"measurements capped at {_MAX_MEASUREMENTS}",
        )

    if len(request.keyframes_base64) > _MAX_KEYFRAMES:
        raise HTTPException(
            status_code=400,
            detail=f"keyframes capped at {_MAX_KEYFRAMES}",
        )

    keyframe_bytes = [_decode_keyframe(b64) for b64 in request.keyframes_base64]
    measurements = [
        FormMeasurement(
            name=m.name,
            value=m.value,
            unit=m.unit,
            flagged=m.flagged,
            threshold=m.threshold,
        )
        for m in request.measurements
    ]

    context = build_form_context(
        shot_type=shot_type,
        measurements=measurements,
        indexes=cached_indexes(),
        keyframe_count=len(keyframe_bytes),
    )

    result = build_form_brief(context, keyframe_images=keyframe_bytes or None)
    cross_refs = _extract_cross_refs(result.brief)

    return FormCoachResponse(
        shot_type=shot_type,
        feedback=result.brief,
        source_citations=result.source_citations,
        source=result.source,
        cross_refs=cross_refs,
    )
