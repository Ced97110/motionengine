"""Play-lab HTTP endpoints — authoring surface for the Tier 0 editor.

Three groups of endpoints:

- ``POST /api/playlab/extract-prose`` → Claude-based prose extractor
  (:mod:`motion.services.play_extractor`).
- ``GET  /api/playlab/wiki-plays`` + ``GET /api/playlab/import-wiki/{slug}``
  → bypass the LLM and build V7Play drafts directly from the wiki's
  structured ``json name=diagram-positions`` blocks
  (:mod:`motion.services.wiki_importer`).
- ``POST /api/playlab/save-to-wiki/{slug}`` → write-back: take a V7Play
  authored in the lab and serialize it into the wiki page's
  ``diagram-positions`` fences, preserving every other byte of the file.
  Two-stage (preview → write) so every on-disk change is human-approved.
"""

from __future__ import annotations

import difflib
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from motion.middleware.sport import current_sport
from motion.services.play_extractor import extract_play_from_prose
from motion.services.wiki_importer import (
    _resolve_wiki_path,
    import_wiki_play,
    list_importable_wiki_plays,
)
from motion.services.wiki_writer import (
    render_updated_markdown,
    v7_play_to_diagram_blocks,
)
from motion.sports import Sport
from motion.wiki_ops.paths import wiki_dir


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
async def wiki_plays(request: Request) -> list[WikiPlayEntry]:
    """List every ``type: play`` wiki page with import eligibility flags."""
    sport: Sport = current_sport(request)
    entries = list_importable_wiki_plays(sport=sport)
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
async def import_wiki(slug: str, request: Request) -> ImportWikiResponse:
    """Build a V7Play draft from the named wiki page."""
    sport: Sport = current_sport(request)
    try:
        result = import_wiki_play(slug, sport=sport)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ImportWikiResponse(
        play=result.play,
        todos=result.todos,
        source=result.source,
    )


# ---------------------------------------------------------------------------
# Save-to-wiki (write-back)
# ---------------------------------------------------------------------------


class SaveToWikiRequest(_CamelModel):
    play: dict[str, Any]
    mode: Literal["preview", "write"]


class SaveToWikiResponse(_CamelModel):
    diff: str
    warnings: list[str]
    path: str | None = None
    bytes_written: int | None = None


@router.post("/save-to-wiki/{slug}", response_model=SaveToWikiResponse)
async def save_to_wiki(
    slug: str, body: SaveToWikiRequest, request: Request
) -> SaveToWikiResponse:
    """Preview or persist a V7Play's geometry into a wiki page.

    ``mode: "preview"`` returns a unified diff + warnings without writing;
    the lab's confirmation modal uses this to let the human review changes.
    ``mode: "write"`` persists ``new_md`` to disk and returns the same diff
    plus the written path/bytes. No git commits are made — humans run
    ``git add`` + commit so every change carries a reviewable message.
    """
    sport: Sport = current_sport(request)
    try:
        root = wiki_dir(sport=sport)
        path = _resolve_wiki_path(slug, root)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"wiki page not found: {slug}")

    existing_md = path.read_text(encoding="utf-8")
    blocks, writer_warnings = v7_play_to_diagram_blocks(body.play)
    new_md, render_warnings = render_updated_markdown(existing_md, blocks)
    warnings = [*writer_warnings, *render_warnings]

    diff = "".join(
        difflib.unified_diff(
            existing_md.splitlines(keepends=True),
            new_md.splitlines(keepends=True),
            fromfile=f"a/{slug}.md",
            tofile=f"b/{slug}.md",
            n=3,
        )
    )

    if body.mode == "preview":
        return SaveToWikiResponse(diff=diff, warnings=warnings)

    # mode == "write" — persist atomically. Writing via ``Path.write_text``
    # is not strictly atomic across crashes, but matches how ingest.py
    # already writes wiki files (wiki_ops/ingest.py:799,932). Upgrading to
    # write-to-tmp-and-rename is a follow-up once we see real failure modes.
    bytes_written = path.write_text(new_md, encoding="utf-8")
    return SaveToWikiResponse(
        diff=diff,
        warnings=warnings,
        path=str(path),
        bytes_written=bytes_written,
    )
