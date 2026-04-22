"""Play-lab HTTP endpoints — authoring surface for the Tier 0 editor.

Thin wrapper over ``motion.services.play_extractor``. The frontend lab at
``/dev/lab/play-editor`` calls these when the user pastes book prose and wants
a V7Play draft back.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from motion.services.play_extractor import extract_play_from_prose


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ExtractProseRequest(_CamelModel):
    prose: str


class ExtractProseResponse(_CamelModel):
    play: dict[str, Any]
    todos: list[str]
    source: str  # "claude" | "stub" | "claude-error"


router = APIRouter(prefix="/api/playlab", tags=["playlab"])


@router.post("/extract-prose", response_model=ExtractProseResponse)
async def extract_prose(request: ExtractProseRequest) -> ExtractProseResponse:
    """Compose a V7Play draft from book prose. Stubs out when no API key."""
    result = extract_play_from_prose(request.prose)
    return ExtractProseResponse(
        play=result.play,
        todos=result.todos,
        source=result.source,
    )
