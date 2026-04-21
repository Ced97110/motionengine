"""Wiki ingestion pipeline — port of ``frontend/scripts/ingest.ts``.

Reads a raw source PDF from ``backend/knowledge-base/raw/``, slices it
into page-range chunks via pypdfium2's page-slice API, ships each chunk
to Claude as a native ``type: "document"`` base64 block together with
``SCHEMA.md`` and the current wiki ``index.md``, and writes the
structured wiki pages the model emits via a forced ``write_wiki_pages``
tool call back into ``backend/knowledge-base/wiki/``.

Phase 3 of the wiki-ops Python migration. The biggest pipeline win over
the TS predecessor is dropping ``pdf-lib`` — which is known to silently
re-encode embedded resources on ``copyPages`` and trip over
encryption-ignoring quirks on certain source PDFs — in favor of
pypdfium2's ``import_pages`` which copies pages verbatim through
PDFium's C core.

Acceptance (see ``backend/spec/wiki-ops-python-migration.md`` §7.3):

- Ingesting the same PDF chunk produces wiki pages that pass
  ``wiki-lint`` (the Phase 1 Python port).
- Identical source-citation prefixes — format ``[Sn, p.XX]`` per
  ``SCHEMA.md``. Wiring: the system prompt embeds
  ``Citation format: [<source_id>, p.XX]`` before the schema body so
  Claude anchors on the same prefix shape.
- Identical filename slugs — kebab-case, lowercase. Wiring: the
  ``write_wiki_pages`` tool schema carries the same verbatim filename
  guidance as the TS original; the writer re-sanitizes defensively.
- Same number of pages per chunk — chunk boundaries are computed via
  the identical ``i : i+chunk_size`` half-open slice, with the same
  ``start_page`` 1-indexed convention.

Non-goals for parity: Claude prose is non-deterministic, so page bodies
will differ run-to-run. This is acceptable per §7.3 and matches the TS
behaviour identically.

Anthropic Python SDK usage (verified via Context7
``/anthropics/anthropic-sdk-python`` llms.txt + api.md, 2026-04-13):

- ``client.messages.create`` accepts ``tools=[...]`` (list of dicts) and
  ``tool_choice={"type": "tool", "name": ...}``. The response's
  ``content`` attribute is a list of blocks whose ``type`` discriminates
  ``text`` vs ``tool_use``; ``.input`` on a tool-use block is a plain
  ``dict``.
- Document blocks on the stable surface accept the dict form
  ``{"type": "document", "source": {"type": "base64",
  "media_type": "application/pdf", "data": <b64>}}`` identically to the
  TS SDK call at ``ingest.ts:273-279``.
- Prompt caching attaches ``cache_control={"type": "ephemeral"}`` to
  any system block or tool definition. We cache the stable pieces
  (system prompt with SCHEMA + index, tool definition) and leave the
  user message (chunk PDF + range text) uncached, per §9 of the spec.

pypdfium2 usage (verified via Context7 ``/pypdfium2-team/pypdfium2``
README, 2026-04-13):

- ``PdfDocument(path)`` opens a document; ``len(doc)`` yields page count.
- ``PdfDocument.new()`` + ``import_pages(src, pages=[i, j, ...])`` +
  ``save("path.pdf")`` builds a new multi-page document suitable for
  passing to Claude as base64.
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import json
import logging
import os
import re
import sys
import tempfile
import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Literal, cast

import anthropic
import pypdfium2

from .paths import backend_root, raw_pdf_dir, repo_root, wiki_dir
from .sources import SOURCE_PDFS

# ---------------------------------------------------------------- constants

DEFAULT_CHUNK_SIZE: int = 20
DEFAULT_MAX_TOKENS: int = 16384
DEFAULT_MODEL: str = "claude-sonnet-4-6"
MAX_CHUNK_SIZE: int = 100

# Map filename substrings to source metadata. Mirrors ``KNOWN_SOURCES``
# in ``frontend/scripts/ingest.ts:39-61``. Kept in this module rather
# than shared via ``sources.py`` because the TS registry uses a
# different key scheme (basename substring match, not source-id).
KNOWN_SOURCES: dict[str, tuple[str, str]] = {
    "lets-talk-defense": ("S1", "Let's Talk Defense — Herb Brown"),
    "basketball-anatomy": ("S2", "Basketball Anatomy"),
    "offensive-skill-development": (
        "S3",
        "Basketball Coaches' Guide to Advanced Offensive Skill Development",
    ),
    "basketball-for-coaches": ("S4", "Basketball For Coaches"),
    "basketball-shooting": ("S5", "Basketball Shooting, Enhanced Edition"),
    "footwork-balance-pivoting": (
        "S6",
        "The Complete Basketball Coaches Guide to Footwork, Balance, and Pivoting",
    ),
    "nba-coaches-playbook": ("S7", "NBA Coaches Playbook — NBCA"),
    "speed-agility-quickness": ("S8", "Training for Speed, Agility, and Quickness"),
    "explosive-calisthenics": (
        "S9",
        "Explosive Calisthenics — Superhuman Power, Maximum Speed and Agility",
    ),
}

# Map category → index.md section heading. Mirrors the ``sectionMap``
# at ``ingest.ts:385-390``.
_SECTION_MAP: dict[str, str] = {
    "concept": "## Concepts",
    "drill": "## Drills",
    "play": "## Plays",
    "source-summary": "## Source Summaries",
}

_VALID_CATEGORIES: tuple[str, ...] = ("concept", "drill", "play", "source-summary")


# Cross-repo artifact path — during Phase 2/3 the TS resolver still
# owns this file, so the Python port reads it from the same location.
def _default_page_offsets_path() -> Path:
    return repo_root() / "frontend" / "scripts" / ".page-offsets.json"


logger = logging.getLogger(__name__)


# --------------------------------------------------------------- types


PageCategory = Literal["concept", "drill", "play", "source-summary"]


@dataclass(frozen=True)
class SourceMeta:
    """Source identifier + human-readable title for citation framing."""

    id: str
    title: str


@dataclass(frozen=True)
class ChunkRange:
    """One chunk's printed-page range (1-indexed, inclusive on both ends).

    ``start_printed`` and ``end_printed`` are the *printed* page numbers
    to display in logs and chunk prompts. Physical slice indices are
    derived from these via the per-source offset and are only used
    internally for the pypdfium2 call.
    """

    start_printed: int
    end_printed: int
    start_physical: int  # 1-indexed
    end_physical: int  # 1-indexed inclusive


@dataclass(frozen=True)
class WikiPageWrite:
    """One page emitted by the model; the on-disk write target."""

    filename: str
    content: str
    summary: str
    category: PageCategory


@dataclass
class ChunkResult:
    pages: list[WikiPageWrite]
    notes: str
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0


@dataclass
class IngestSummary:
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    total_pages_written: int = 0
    total_chunks: int = 0
    total_cache_read_tokens: int = 0
    total_cache_creation_tokens: int = 0


# ----------------------------------------------------------- source detect


def detect_source(pdf_path: Path) -> SourceMeta:
    """Detect the :class:`SourceMeta` for ``pdf_path`` by basename match.

    Mirrors ``detectSource`` in ``ingest.ts:120-128``. Falls back to a
    human-readable title derived from the filename when the basename
    doesn't match any known source (``id = "S?"``), preserving the TS
    fallback.
    """
    basename = pdf_path.name
    for pattern, (sid, title) in KNOWN_SOURCES.items():
        if pattern in basename:
            return SourceMeta(id=sid, title=title)
    fallback_name = pdf_path.stem.replace("-", " ").replace("_", " ")
    return SourceMeta(id="S?", title=fallback_name)


def resolve_source_pdf(source_id: str, raw_dir: Path | None = None) -> Path:
    """Resolve ``source_id`` → raw PDF path via ``SOURCE_PDFS``."""
    if source_id not in SOURCE_PDFS:
        raise KeyError(f"Unknown source id: {source_id!r}")
    base = raw_dir if raw_dir is not None else raw_pdf_dir()
    return base / SOURCE_PDFS[source_id]


# ------------------------------------------------------------ page offsets


def load_page_offsets(path: Path | None = None) -> dict[str, int]:
    """Load the printed→physical offset map from the JSON artifact.

    Returns an empty dict if the artifact is missing or malformed, so
    callers can treat "no offsets file" and "file present but source
    absent" identically (fall back to printed == physical).
    """
    target = path if path is not None else _default_page_offsets_path()
    if not target.exists():
        return {}
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    offsets = data.get("offsets") if isinstance(data, dict) else None
    if not isinstance(offsets, dict):
        return {}
    out: dict[str, int] = {}
    for k, v in offsets.items():
        if isinstance(k, str) and isinstance(v, int):
            out[k] = v
    return out


def printed_to_physical(printed: int, offset: int) -> int:
    """Map a printed (1-indexed) page number to a physical 1-indexed index.

    ``offset`` is ``physical - printed`` (front-matter thickness), per
    ``detect_page_offsets.OffsetResult.offset``. ``printed = 45`` +
    ``offset = 14`` → physical 59. Values are always 1-indexed on both
    sides.
    """
    return printed + offset


# -------------------------------------------------------------- chunk PDF


def _safe_close(doc: Any) -> None:
    close = getattr(doc, "close", None)
    if callable(close):
        close()


def chunk_pdf(
    source_pdf: Path,
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    start_page: int = 1,
    end_page: int | None = None,
    offset: int = 0,
) -> Iterator[ChunkRange]:
    """Yield printed-page chunk ranges for ``source_pdf``.

    The caller handles byte serialization separately via
    :func:`render_chunk_bytes` — keeping them separate lets tests
    iterate chunk boundaries without paying the save-to-disk cost.

    - ``chunk_size`` — maximum number of *printed* pages per chunk. The
      TS original uses the same value for both printed and physical
      because it has no offset concept; here they're equal too because
      chunks are contiguous printed-page ranges.
    - ``start_page`` — 1-indexed printed page to resume from (default 1).
    - ``end_page`` — optional 1-indexed printed page to stop at
      (inclusive). Default: last printed page in the PDF.
    - ``offset`` — printed-to-physical offset loaded via
      :func:`load_page_offsets`. Default 0 matches the TS behavior
      (which never applied an offset).
    """
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")
    if chunk_size > MAX_CHUNK_SIZE:
        chunk_size = MAX_CHUNK_SIZE
    if start_page < 1:
        start_page = 1

    doc = pypdfium2.PdfDocument(str(source_pdf))
    try:
        total_physical = len(doc)
    finally:
        _safe_close(doc)
    if total_physical <= 0:
        return

    # Convert printed → physical bounds.
    first_physical = max(1, printed_to_physical(start_page, offset))
    if first_physical > total_physical:
        return
    # Printed-page ceiling: clamp to whatever physical page maps back to.
    max_printed = total_physical - offset
    effective_end_printed: int = max_printed if end_page is None else min(end_page, max_printed)
    if effective_end_printed < start_page:
        return

    printed_i = start_page
    while printed_i <= effective_end_printed:
        printed_end = min(printed_i + chunk_size - 1, effective_end_printed)
        physical_start = printed_to_physical(printed_i, offset)
        physical_end = printed_to_physical(printed_end, offset)
        # Defensive clamp — should never trip given the guards above.
        physical_start = max(1, min(total_physical, physical_start))
        physical_end = max(physical_start, min(total_physical, physical_end))
        yield ChunkRange(
            start_printed=printed_i,
            end_printed=printed_end,
            start_physical=physical_start,
            end_physical=physical_end,
        )
        printed_i = printed_end + 1


def render_chunk_bytes(source_pdf: Path, chunk: ChunkRange) -> bytes:
    """Render one chunk to a standalone multi-page PDF as bytes.

    Uses pypdfium2's page-slice API:
    ``PdfDocument.new()`` → ``import_pages(src, pages=[i0, i1, ...])``
    → ``save(path)`` → read bytes. See module docstring for Context7
    verification.
    """
    src = pypdfium2.PdfDocument(str(source_pdf))
    try:
        total = len(src)
        start_0 = chunk.start_physical - 1
        end_excl = chunk.end_physical  # inclusive-to-exclusive
        start_0 = max(0, min(total, start_0))
        end_excl = max(start_0, min(total, end_excl))
        indices = list(range(start_0, end_excl))
        if not indices:
            return b""

        out = pypdfium2.PdfDocument.new()
        try:
            out.import_pages(src, pages=indices)
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                out.save(str(tmp_path))
                return tmp_path.read_bytes()
            finally:
                with contextlib.suppress(FileNotFoundError):
                    tmp_path.unlink()
        finally:
            _safe_close(out)
    finally:
        _safe_close(src)


# ----------------------------------------------------------- tool schema


def _tool_definition(*, cache: bool = False) -> dict[str, Any]:
    """Build the ``write_wiki_pages`` tool definition.

    Verbatim port of the tool at ``ingest.ts:171-214``. Field names and
    semantics are preserved so the TS runtime (if ever invoked against
    the same prompt) would accept identical output.
    """
    tool: dict[str, Any] = {
        "name": "write_wiki_pages",
        "description": (
            "Write or update basketball coaching wiki pages extracted from "
            "the source material. Each page must follow the SCHEMA "
            "conventions. Return an empty pages array if the chunk has no "
            "extractable content (e.g., table of contents, bibliography)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pages": {
                    "type": "array",
                    "description": "Wiki pages to create or update",
                    "items": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": (
                                    'Kebab-case .md filename (e.g., "pick-and-roll-defense.md")'
                                ),
                            },
                            "content": {
                                "type": "string",
                                "description": (
                                    "Full page content: YAML frontmatter + "
                                    "markdown body following SCHEMA.md templates"
                                ),
                            },
                            "summary": {
                                "type": "string",
                                "description": ("One-line summary for index.md (max 120 chars)"),
                            },
                            "category": {
                                "type": "string",
                                "enum": list(_VALID_CATEGORIES),
                                "description": "Page type for index organization",
                            },
                        },
                        "required": ["filename", "content", "summary", "category"],
                    },
                },
                "chunk_notes": {
                    "type": "string",
                    "description": (
                        "Brief notes about this chunk for the ingestion log "
                        "(e.g., 'Chapter 3: help defense rotations')"
                    ),
                },
            },
            "required": ["pages"],
        },
    }
    if cache:
        tool["cache_control"] = {"type": "ephemeral"}
    return tool


# ----------------------------------------------------------- system prompt


def build_system_prompt(source: SourceMeta, schema: str, index_text: str) -> str:
    """Build the system prompt identical in shape to ``ingest.ts:219-253``.

    The TS original interpolates ``source.id``, ``source.title``, the
    raw ``SCHEMA.md`` body, and the raw ``index.md`` body into a
    constant template. Replicated verbatim including whitespace and
    section headers so cache hits are maximized across runs: any
    whitespace drift would miss the ephemeral cache entirely.
    """
    return (
        "You are a basketball coaching knowledge wiki maintainer.\n\n"
        "Your job: read pages from a coaching book and extract "
        "structured wiki pages following the schema below.\n\n"
        "## Source Being Ingested\n"
        f"- Source ID: {source.id}\n"
        f"- Title: {source.title}\n"
        f"- Citation format: [{source.id}, p.XX]\n\n"
        "## Schema (FOLLOW EXACTLY)\n\n"
        f"{schema}\n\n"
        "## Current Wiki Index (for cross-linking and dedup)\n\n"
        f"{index_text}\n\n"
        "## Instructions\n\n"
        "1. Read the PDF pages carefully.\n"
        "2. Extract every distinct concept, drill, or play into its own wiki page.\n"
        "3. Follow the SCHEMA page templates exactly — include all required sections.\n"
        "4. Cross-link to existing wiki pages listed in the index above.\n"
        "5. If content overlaps with an existing page, note it in the summary so "
        "the merge can happen later.\n"
        "6. Use the write_wiki_pages tool to output your pages.\n"
        "7. Skip filler content (acknowledgments, table of contents, bibliography, "
        "blank pages).\n"
        "8. For court diagrams or figures: describe positions and movements if "
        "interpretable, otherwise add a <!-- DIAGRAM --> comment.\n"
        "9. Be thorough — extract ALL coaching knowledge, not just headlines."
    )


def _read_schema() -> str:
    """Read ``backend/knowledge-base/SCHEMA.md`` as UTF-8 text."""
    return (backend_root() / "knowledge-base" / "SCHEMA.md").read_text(encoding="utf-8")


def _read_index(wiki_root: Path) -> str:
    """Read ``<wiki>/index.md`` as UTF-8 text; empty if missing."""
    path = wiki_root / "index.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------- chunk -> pages


def _coerce_page(raw: Any) -> WikiPageWrite | None:
    """Validate + coerce a single tool-input page entry.

    Mirrors the TS guard at ``ingest.ts:308-319``: drop entries missing
    a string ``filename`` or string ``content``. Category is clamped to
    the allowed set (defaulting to ``concept`` for parity — the TS
    original trusts whatever the model returns, but we normalize to
    avoid writing ``category=<unknown>`` to the index map).
    """
    if not isinstance(raw, dict):
        return None
    filename = raw.get("filename")
    content = raw.get("content")
    if not isinstance(filename, str) or not filename:
        return None
    if not isinstance(content, str) or not content:
        return None
    summary_raw = raw.get("summary", "")
    summary = summary_raw if isinstance(summary_raw, str) else ""
    category_raw = raw.get("category", "concept")
    category: PageCategory = (
        cast(PageCategory, category_raw) if category_raw in _VALID_CATEGORIES else "concept"
    )
    return WikiPageWrite(
        filename=filename,
        content=content,
        summary=summary,
        category=category,
    )


def _build_chunk_message_params(
    chunk_bytes: bytes,
    chunk: ChunkRange,
    source: SourceMeta,
    schema: str,
    index_text: str,
    model: str,
    max_tokens: int,
) -> dict[str, Any]:
    """Build the ``messages.create`` params dict for one chunk.

    Shared between the synchronous path (``ingest_chunk``) and the batch
    path (``ingest_chunks_batch``). Returns a dict suitable for either
    ``client.messages.create(**params)`` or
    ``{"custom_id": ..., "params": dict_from_here}`` inside a batch
    ``messages.batches.create(requests=[...])`` call.
    """
    b64 = base64.standard_b64encode(chunk_bytes).decode("ascii")
    system_prompt = build_system_prompt(source, schema, index_text)
    system_blocks: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"},
        }
    ]
    tool_def = _tool_definition(cache=True)
    return {
        "model": model,
        "max_tokens": max_tokens,
        "system": system_blocks,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            f"Ingest pages {chunk.start_printed}-"
                            f'{chunk.end_printed} from "{source.title}". '
                            "Extract all concepts, drills, and plays into "
                            "wiki pages following the SCHEMA. Use the "
                            "write_wiki_pages tool."
                        ),
                    },
                ],
            }
        ],
        "tools": [tool_def],
        "tool_choice": {"type": "tool", "name": "write_wiki_pages"},
    }


def _parse_chunk_response(content_list: Any, usage: Any) -> ChunkResult:
    """Parse a Claude message response into a :class:`ChunkResult`.

    Shared between sync and batch paths. ``content_list`` is the message
    ``.content`` attribute (list of blocks); ``usage`` is the message
    ``.usage`` attribute.
    """
    cache_read = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    cache_creation = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)

    tool_use = next(
        (block for block in content_list if getattr(block, "type", None) == "tool_use"),
        None,
    )
    if tool_use is None:
        return ChunkResult(
            pages=[],
            notes="No tool call returned",
            cache_read_tokens=cache_read,
            cache_creation_tokens=cache_creation,
        )

    tool_input = cast(dict[str, Any], getattr(tool_use, "input", {}) or {})
    raw_pages = tool_input.get("pages", [])
    if isinstance(raw_pages, dict):
        raw_page_list: list[Any] = [raw_pages]
    elif isinstance(raw_pages, list):
        raw_page_list = raw_pages
    else:
        raw_page_list = []

    pages: list[WikiPageWrite] = []
    for entry in raw_page_list:
        coerced = _coerce_page(entry)
        if coerced is not None:
            pages.append(coerced)

    notes_raw = tool_input.get("chunk_notes", "")
    notes = notes_raw if isinstance(notes_raw, str) else ""

    return ChunkResult(
        pages=pages,
        notes=notes,
        cache_read_tokens=cache_read,
        cache_creation_tokens=cache_creation,
    )


def ingest_chunk(
    client: anthropic.Anthropic,
    *,
    chunk_bytes: bytes,
    chunk: ChunkRange,
    source: SourceMeta,
    schema: str,
    index_text: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> ChunkResult:
    """Send one chunk to Claude and parse the ``write_wiki_pages`` tool call.

    Synchronous path. Prompt caching: system-prompt and tool def are cached;
    user message (PDF chunk + range label) is not.
    """
    if not chunk_bytes:
        return ChunkResult(pages=[], notes="Empty chunk bytes — skipped")

    params = _build_chunk_message_params(
        chunk_bytes, chunk, source, schema, index_text, model, max_tokens
    )
    response = client.messages.create(**cast(Any, params))
    return _parse_chunk_response(response.content, getattr(response, "usage", None))


def ingest_chunks_batch(
    client: anthropic.Anthropic,
    *,
    prepared: list[tuple[ChunkRange, bytes]],
    source: SourceMeta,
    schema: str,
    index_text: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    poll_interval_seconds: int = 30,
) -> dict[str, ChunkResult]:
    """Submit all chunks as one Anthropic Message Batches job (50% discount).

    Returns a mapping of ``custom_id`` → :class:`ChunkResult`. ``custom_id``
    format is ``chunk-<start_printed>-<end_printed>`` so the caller can
    match results back to the originating :class:`ChunkRange`.

    Polls the batch every ``poll_interval_seconds`` until ``processing_status``
    reaches ``ended``. Batches are typically processed in minutes but can take
    up to 24 hours per Anthropic's guarantee.
    """
    if not prepared:
        return {}

    requests: list[dict[str, Any]] = []
    for chunk, chunk_bytes in prepared:
        if not chunk_bytes:
            continue
        custom_id = f"chunk-{chunk.start_printed}-{chunk.end_printed}"
        params = _build_chunk_message_params(
            chunk_bytes, chunk, source, schema, index_text, model, max_tokens
        )
        requests.append({"custom_id": custom_id, "params": params})

    if not requests:
        return {}

    sys.stdout.write(f"[batch] submitting {len(requests)} chunks to Anthropic batch API...\n")
    sys.stdout.flush()
    batch = client.messages.batches.create(requests=cast(Any, requests))
    batch_id = batch.id
    sys.stdout.write(f"[batch] id={batch_id} — polling every {poll_interval_seconds}s\n")
    sys.stdout.flush()

    # Poll loop
    while True:
        current = client.messages.batches.retrieve(batch_id)
        counts = current.request_counts
        status = current.processing_status
        sys.stdout.write(
            f"[batch] status={status}  "
            f"processing={counts.processing} "
            f"succeeded={counts.succeeded} "
            f"errored={counts.errored} "
            f"canceled={counts.canceled} "
            f"expired={counts.expired}\n"
        )
        sys.stdout.flush()
        if status == "ended":
            break
        time.sleep(poll_interval_seconds)

    # Fetch results (streamed JSONL)
    results: dict[str, ChunkResult] = {}
    for item in client.messages.batches.results(batch_id):
        custom_id = item.custom_id
        result = item.result
        result_type = getattr(result, "type", None)
        if result_type == "succeeded":
            message = getattr(result, "message", None)
            if message is None:
                results[custom_id] = ChunkResult(
                    pages=[], notes="Batch: succeeded but message missing"
                )
                continue
            results[custom_id] = _parse_chunk_response(
                message.content, getattr(message, "usage", None)
            )
        else:
            # errored / canceled / expired
            error_obj = getattr(result, "error", None)
            error_msg = (
                getattr(error_obj, "error", None)
                if error_obj is not None
                else f"Batch result {result_type}"
            )
            results[custom_id] = ChunkResult(
                pages=[],
                notes=f"Batch {result_type}: {error_msg}",
            )
    return results


# -------------------------------------------------------------- write pages


_FILENAME_SAFE_RE = re.compile(r"[^a-z0-9._-]", re.IGNORECASE)


def _sanitize_filename(raw: str) -> str:
    """Strip directory components + normalize to the SCHEMA filename shape.

    Mirrors the TS sanitizer at ``ingest.ts:339``:
    ``path.basename(page.filename).replace(/[^a-z0-9._-]/gi, "-")``.
    """
    base = os.path.basename(raw)
    return _FILENAME_SAFE_RE.sub("-", base)


def write_pages(
    pages: list[WikiPageWrite], wiki_root: Path
) -> tuple[list[WikiPageWrite], list[str], list[str]]:
    """Write pages under ``wiki_root`` and track created vs updated.

    Returns ``(normalized_pages, created, updated)`` where
    ``normalized_pages`` carries the sanitized filename so downstream
    index-building can use the same slug. Mirrors ``ingest.ts:329-357``.

    Write semantics: overwrite on collision. The TS original does the
    same thing — it does not attempt any section-level merge — so we
    match bit-for-bit: if a page already exists, it's replaced with the
    newly-emitted content and tracked as ``updated``.
    """
    wiki_root.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    updated: list[str] = []
    normalized: list[WikiPageWrite] = []

    for page in pages:
        safe_name = _sanitize_filename(page.filename)
        if not safe_name:
            continue
        target = wiki_root / safe_name
        exists = target.exists()
        target.write_text(page.content or "", encoding="utf-8")
        if exists:
            updated.append(safe_name)
        else:
            created.append(safe_name)
        # Rebuild the write record with the normalized filename so the
        # index builder and log use the same slug as disk.
        normalized.append(
            WikiPageWrite(
                filename=safe_name,
                content=page.content,
                summary=page.summary,
                category=page.category,
            )
        )

    return normalized, created, updated


# -------------------------------------------------------------- append log


def append_log(
    source: SourceMeta,
    chunk: ChunkRange,
    created: list[str],
    updated: list[str],
    notes: str,
    wiki_root: Path,
    *,
    today: date | None = None,
) -> None:
    """Append a Karpathy-spec log entry to ``<wiki>/log.md``.

    Entry shape matches ``ingest.ts:423-439`` character-for-character:

        ## [YYYY-MM-DD] ingest | <source.title> (pp.<start>-<end>)
        - Created: <list or (none)>
        - Updated: <list or (none)>
        - Notes: <notes or —>

    The ``pp.`` range uses *printed* pages — same as the TS original,
    which passed the 1-indexed range directly.
    """
    when = today if today is not None else date.today()
    date_str = when.isoformat()

    created_str = ", ".join(created) if created else "(none)"
    updated_str = ", ".join(updated) if updated else "(none)"
    notes_str = notes if notes else "—"

    entry = (
        "\n"
        f"## [{date_str}] ingest | {source.title} "
        f"(pp.{chunk.start_printed}-{chunk.end_printed})\n"
        f"- Created: {created_str}\n"
        f"- Updated: {updated_str}\n"
        f"- Notes: {notes_str}\n"
    )

    log_path = wiki_root / "log.md"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(entry)


# ------------------------------------------------------------- update index


def _format_index_entry(page: WikiPageWrite) -> str:
    """Format one index-line entry matching ``ingest.ts:401-407``."""
    name = page.filename.replace(".md", "").replace("-", " ")
    title = name[:1].upper() + name[1:] if name else page.filename
    return f"- [{title}]({page.filename}) — {page.summary}"


_EXISTING_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def update_index(pages: list[WikiPageWrite], wiki_root: Path) -> None:
    """Insert new page entries into ``<wiki>/index.md`` by category.

    Mirrors ``ingest.ts:361-419``: for each category, drop the entry if
    its filename is already linked anywhere in the index (dedup), then
    insert the remaining entries immediately after the category heading.

    Unlike the TS original, which silently drops new pages when the
    category heading is missing, we append the heading + entries at
    the end of the file. That keeps the wiki usable from an empty
    index — useful for tests and fresh-checkouts — without changing
    behavior on the real wiki which always has every heading.
    """
    index_path = wiki_root / "index.md"
    existing = index_path.read_text(encoding="utf-8") if index_path.exists() else "# Wiki Index\n"

    # Dedup set: any filename already linked anywhere in the index.
    linked: set[str] = {m.group(2) for m in _EXISTING_LINK_RE.finditer(existing)}

    by_category: dict[str, list[WikiPageWrite]] = {cat: [] for cat in _SECTION_MAP}
    for page in pages:
        cat = page.category
        if cat in by_category:
            by_category[cat].append(page)

    updated = existing
    for category, cat_pages in by_category.items():
        fresh = [p for p in cat_pages if p.filename not in linked]
        if not fresh:
            continue
        # Track within-run dedup so a chunk emitting the same filename
        # twice doesn't write two index lines.
        seen: set[str] = set()
        deduped: list[WikiPageWrite] = []
        for p in fresh:
            if p.filename in seen:
                continue
            seen.add(p.filename)
            deduped.append(p)
        if not deduped:
            continue

        heading = _SECTION_MAP[category]
        entries = "\n".join(_format_index_entry(p) for p in deduped)

        heading_index = updated.find(heading)
        if heading_index >= 0:
            newline_after = updated.find("\n", heading_index)
            insert_pos = len(updated) if newline_after < 0 else newline_after + 1
            updated = updated[:insert_pos] + entries + "\n" + updated[insert_pos:]
        else:
            # Heading missing — append it + entries at EOF.
            prefix = updated if updated.endswith("\n") else updated + "\n"
            updated = f"{prefix}\n{heading}\n{entries}\n"

    index_path.write_text(updated, encoding="utf-8")


# ------------------------------------------------------------ orchestrator


def _normalize_chunk_size(raw: int) -> int:
    return max(1, min(MAX_CHUNK_SIZE, raw))


def run(
    source_id: str,
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    start_page: int | None = None,
    end_page: int | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    dry_run: bool = False,
    batch: bool = False,
    raw_dir: Path | None = None,
    wiki_root: Path | None = None,
    page_offsets_path: Path | None = None,
    client: anthropic.Anthropic | None = None,
    today: date | None = None,
) -> IngestSummary:
    """Ingest one source PDF end-to-end.

    Dry-run semantics match the TS original (``ingest.ts:484-490``):
    compute chunk boundaries, print them, and return without writing
    files *or* calling Claude. The user can inspect the plan before
    paying for a real ingest.
    """
    source_pdf = resolve_source_pdf(source_id, raw_dir=raw_dir)
    source = detect_source(source_pdf)
    # If basename detection produces a fallback ("S?"), honor the
    # ``source_id`` the caller passed. Preserves the TS behaviour:
    # ``detectSource`` is best-effort; the explicit CLI value wins.
    if source.id == "S?":
        source = SourceMeta(id=source_id, title=source.title)

    chunk_size = _normalize_chunk_size(chunk_size)
    start = start_page if start_page is not None else 1

    wiki_root_path = wiki_root if wiki_root is not None else wiki_dir()
    offsets = load_page_offsets(page_offsets_path)
    offset = offsets.get(source_id, 0)

    chunks = list(
        chunk_pdf(
            source_pdf,
            chunk_size=chunk_size,
            start_page=start,
            end_page=end_page,
            offset=offset,
        )
    )

    summary = IngestSummary(total_chunks=len(chunks))

    sys.stdout.write(
        f"Source: {source.title} ({source.id})\n"
        f"PDF: {source_pdf}\n"
        f"Model: {model}\n"
        f"Chunk size: {chunk_size} printed pages\n"
        f"Offset (printed -> physical): +{offset}\n"
        f"Chunks: {len(chunks)}\n"
        f"Dry run: {dry_run}\n\n"
    )

    if dry_run:
        for c in chunks:
            sys.stdout.write(
                f"  pp.{c.start_printed}-{c.end_printed} "
                f"(physical {c.start_physical}-{c.end_physical})\n"
            )
        return summary

    if not os.environ.get("ANTHROPIC_API_KEY") and client is None:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    if client is None:
        client = anthropic.Anthropic()

    schema = _read_schema()
    index_text = _read_index(wiki_root_path)

    all_pages: list[WikiPageWrite] = []

    if batch:
        sys.stdout.write("[batch] rendering all chunk PDFs...\n")
        sys.stdout.flush()
        prepared: list[tuple[ChunkRange, bytes]] = []
        for chunk in chunks:
            try:
                prepared.append((chunk, render_chunk_bytes(source_pdf, chunk)))
            except Exception as exc:
                sys.stdout.write(
                    f"[batch] skip pp.{chunk.start_printed}-"
                    f"{chunk.end_printed}: render error {exc}\n"
                )
        batch_results = ingest_chunks_batch(
            client,
            prepared=prepared,
            source=source,
            schema=schema,
            index_text=index_text,
            model=model,
            max_tokens=max_tokens,
        )
        for chunk, _ in prepared:
            custom_id = f"chunk-{chunk.start_printed}-{chunk.end_printed}"
            result = batch_results.get(custom_id)
            if result is None:
                sys.stdout.write(
                    f"[batch] pp.{chunk.start_printed}-{chunk.end_printed}: "
                    "no batch result returned\n"
                )
                continue
            summary.total_cache_read_tokens += result.cache_read_tokens
            summary.total_cache_creation_tokens += result.cache_creation_tokens
            if not result.pages:
                sys.stdout.write(
                    f"[batch] pp.{chunk.start_printed}-{chunk.end_printed}: "
                    f"skipped ({result.notes or 'no extractable content'})\n"
                )
                continue
            normalized, created, updated = write_pages(result.pages, wiki_root_path)
            summary.created.extend(created)
            summary.updated.extend(updated)
            summary.total_pages_written += len(normalized)
            all_pages.extend(normalized)
            sys.stdout.write(
                f"[batch] pp.{chunk.start_printed}-{chunk.end_printed}: "
                f"{len(created)} created, {len(updated)} updated\n"
            )
            append_log(
                source,
                chunk,
                created,
                updated,
                result.notes,
                wiki_root_path,
                today=today,
            )
        if all_pages:
            update_index(all_pages, wiki_root_path)
        sys.stdout.write(
            "\nBatch ingestion complete\n"
            f"  pages created: {len(summary.created)}\n"
            f"  pages updated: {len(summary.updated)}\n"
            f"  total written: {summary.total_pages_written}\n"
            f"  cache reads:   {summary.total_cache_read_tokens}\n"
            f"  cache writes:  {summary.total_cache_creation_tokens}\n"
        )
        return summary

    for i, chunk in enumerate(chunks, start=1):
        sys.stdout.write(f"[{i}/{len(chunks)}] pp.{chunk.start_printed}-{chunk.end_printed} ... ")
        sys.stdout.flush()
        try:
            chunk_bytes = render_chunk_bytes(source_pdf, chunk)
            result = ingest_chunk(
                client,
                chunk_bytes=chunk_bytes,
                chunk=chunk,
                source=source,
                schema=schema,
                index_text=index_text,
                model=model,
                max_tokens=max_tokens,
            )
        except Exception as exc:
            sys.stdout.write(f"ERROR: {exc}\n")
            sys.stdout.write(f"       Resume with: --start-page {chunk.start_printed}\n")
            continue

        summary.total_cache_read_tokens += result.cache_read_tokens
        summary.total_cache_creation_tokens += result.cache_creation_tokens

        if not result.pages:
            sys.stdout.write("skipped (no extractable content)\n")
            continue

        normalized, created, updated = write_pages(result.pages, wiki_root_path)
        summary.created.extend(created)
        summary.updated.extend(updated)
        summary.total_pages_written += len(normalized)
        all_pages.extend(normalized)

        sys.stdout.write(f"{len(created)} created, {len(updated)} updated\n")
        if created:
            sys.stdout.write(f"       {', '.join(created)}\n")

        append_log(
            source,
            chunk,
            created,
            updated,
            result.notes,
            wiki_root_path,
            today=today,
        )

    if all_pages:
        update_index(all_pages, wiki_root_path)

    sys.stdout.write(
        "\nIngestion complete\n"
        f"  pages created: {len(summary.created)}\n"
        f"  pages updated: {len(summary.updated)}\n"
        f"  total written: {summary.total_pages_written}\n"
        f"  cache reads:   {summary.total_cache_read_tokens}\n"
        f"  cache writes:  {summary.total_cache_creation_tokens}\n"
    )
    return summary


# ----------------------------------------------------------------- CLI


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="wiki-ingest",
        description=(
            "Ingest a source PDF into the wiki via Claude. Port of "
            "frontend/scripts/ingest.ts (Phase 3)."
        ),
    )
    parser.add_argument(
        "source_id",
        help=f"Source id to ingest; one of {sorted(SOURCE_PDFS)}.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Pages per API call (max {MAX_CHUNK_SIZE}). Default: {DEFAULT_CHUNK_SIZE}.",
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=None,
        help="1-indexed printed page to resume from. Default: 1.",
    )
    parser.add_argument(
        "--end-page",
        type=int,
        default=None,
        help="1-indexed printed page to stop at (inclusive). Default: last page.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model id. Default: {DEFAULT_MODEL}.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"max_tokens per call. Default: {DEFAULT_MAX_TOKENS}.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show chunk plan without calling Claude or writing files.",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help=(
            "Use Anthropic Message Batches API (50%% discount). "
            "Submits all chunks as one batch and polls until done. "
            "Turnaround typically minutes, up to 24h guaranteed."
        ),
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=None,
        help="Override the raw PDF directory.",
    )
    parser.add_argument(
        "--wiki-dir",
        type=Path,
        default=None,
        help="Override the wiki output directory.",
    )
    parser.add_argument(
        "--page-offsets",
        type=Path,
        default=None,
        help="Override the path to the page-offsets JSON artifact.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point — matches ``pyproject.toml`` ``wiki-ingest``."""
    args = _parse_args(argv)
    try:
        run(
            args.source_id,
            chunk_size=args.chunk_size,
            start_page=args.start_page,
            end_page=args.end_page,
            model=args.model,
            max_tokens=args.max_tokens,
            dry_run=args.dry_run,
            batch=args.batch,
            raw_dir=args.raw_dir,
            wiki_root=args.wiki_dir,
            page_offsets_path=args.page_offsets,
        )
    except KeyError as exc:
        sys.stderr.write(f"ingest failed: {exc}\n")
        return 2
    except RuntimeError as exc:
        sys.stderr.write(f"ingest failed: {exc}\n")
        return 1
    except FileNotFoundError as exc:
        sys.stderr.write(f"ingest failed: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
