"""Play-lab HTTP endpoints — authoring surface for the Tier 0 editor.

Two thin wrappers:

- ``POST /api/playlab/extract-prose`` → Claude-based prose extractor
  (:mod:`motion.services.play_extractor`).
- ``GET  /api/playlab/wiki-plays`` + ``GET /api/playlab/import-wiki/{slug}``
  → bypass the LLM and build V7Play drafts directly from the wiki's
  structured ``json name=diagram-positions`` blocks
  (:mod:`motion.services.wiki_importer`).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from motion.services.play_extractor import extract_play_from_prose
from motion.services.wiki_importer import (
    import_wiki_play,
    list_importable_wiki_plays,
)


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ExtractProseRequest(_CamelModel):
    prose: str


class ExtractProseResponse(_CamelModel):
    play: dict[str, Any]
    todos: list[str]
    source: str  # "claude" | "stub" | "claude-error"


class WikiPlayEntry(_CamelModel):
    slug: str
    name: str
    phase_count: int
    has_diagram: bool
    block_count: int


class ImportWikiResponse(_CamelModel):
    play: dict[str, Any] | None
    todos: list[str]
    source: str  # "wiki-structured" | "wiki-partial" | "wiki-no-diagram"


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


@router.get("/wiki-plays", response_model=list[WikiPlayEntry])
async def wiki_plays() -> list[WikiPlayEntry]:
    """List every ``type: play`` wiki page with import eligibility flags."""
    entries = list_importable_wiki_plays()
    return [
        WikiPlayEntry(
            slug=e["slug"],
            name=e["name"],
            phase_count=e["phaseCount"],
            has_diagram=e["hasDiagram"],
            block_count=e["blockCount"],
        )
        for e in entries
    ]


@router.get("/import-wiki/{slug}", response_model=ImportWikiResponse)
async def import_wiki(slug: str) -> ImportWikiResponse:
    """Build a V7Play draft from the named wiki page."""
    try:
        result = import_wiki_play(slug)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ImportWikiResponse(
        play=result.play,
        todos=result.todos,
        source=result.source,
    )
