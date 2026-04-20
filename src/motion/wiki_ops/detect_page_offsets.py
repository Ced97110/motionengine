"""Detect printed-page-vs-physical-page offset for each source PDF.

Port of ``frontend/scripts/detect-page-offsets.ts``. Source PDFs carry
front matter (cover, TOC, preface, acknowledgments) which shifts
physical page indices relative to the printed page numbers in the book
body. Wiki citations reference printed pages (e.g. ``[S4, p.33]``) so
the resolver needs a per-source offset before it can extract.

This module extracts one physical mid-book page per PDF (up to four
probe points with a majority-vote consensus), asks Claude to read the
printed page number off the header or footer via a forced tool call,
and writes the computed offsets to a JSON artifact that the TS
``resolve-diagrams`` script consumes unchanged.

Cross-repo artifact path: ``<repo>/frontend/scripts/.page-offsets.json``
— the TS resolver still reads from this location during Phase 2 of the
wiki-ops migration. The artifact moves in Phase 6.

Anthropic Python SDK usage (verified via Context7 against
``/anthropics/anthropic-sdk-python`` on 2026-04-13):

- Document blocks are exposed as ``DocumentBlockParam`` /
  ``Base64PDFSource`` on the **stable** (non-beta) surface (see the
  ``anthropic.types`` import list in ``api.md``). The dict form
  ``{"type": "document", "source": {"type": "base64",
  "media_type": "application/pdf", "data": <b64>}}`` is accepted by
  ``client.messages.create`` directly, matching the TS SDK shape
  used at ``frontend/scripts/detect-page-offsets.ts:139-143``.
- Tool use: ``tools=[{"name": ..., "description": ...,
  "input_schema": {...}}]`` with ``tool_choice={"type": "tool",
  "name": "..."}`` (verified via llms.txt example). Tool output is
  read from the first ``type == "tool_use"`` block in
  ``response.content``; the ``.input`` attribute is a plain ``dict``.
- Prompt caching: ``cache_control={"type": "ephemeral"}`` attaches
  to a system block or tool definition via the ``CacheControlEphemeral``
  type exposed on the stable surface. Cache-hit/miss counters live on
  ``response.usage`` as ``cache_read_input_tokens`` and
  ``cache_creation_input_tokens`` (REST field names; attribute names
  on the ``Usage`` model are the same per API parity). We read them
  via ``getattr(..., 0)`` to stay compatible with older SDK builds
  that may not expose the attributes yet — no silent breakage.
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import io
import json
import logging
import os
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, cast

import anthropic
import pypdfium2

from .paths import raw_pdf_dir, repo_root
from .sources import SOURCE_PDFS

# Match the TS default verbatim. Do NOT change without updating
# ``frontend/scripts/detect-page-offsets.ts:50`` in lock-step.
DEFAULT_MODEL: str = "claude-haiku-4-5-20251001"

# Front matter rarely exceeds ~50 pages; offsets above that threshold
# almost always indicate chapter-local page numbering which no single
# offset can fix. Mirrors ``OFFSET_SANITY_LIMIT`` in the TS original.
OFFSET_SANITY_LIMIT: int = 50

# Maximum successful probes before we stop voting. Mirrors the TS
# ``observed.length >= 3`` short-circuit.
MAX_PROBES_FOR_CONSENSUS: int = 3

# System prompt is stable across every PDF and every run; cache it.
_SYSTEM_PROMPT: str = (
    "You read printed page numbers off book pages. You respond only via the provided tool."
)

# Tool schema is stable across every PDF and every run; cache it too.
_READ_PAGE_NUMBER_TOOL: dict[str, Any] = {
    "name": "report_printed_page_number",
    "description": (
        "Report the printed page number visible on the provided PDF page "
        "(usually shown in the header or footer). Use null if no printed "
        "page number is visible (e.g., blank page, cover, title page)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "printed_page_number": {
                "type": ["integer", "null"],
                "description": (
                    "The printed page number as shown on the page itself, or null if none visible."
                ),
            },
            "rationale": {
                "type": "string",
                "description": (
                    "One short sentence on where the page number was found or why none is visible."
                ),
            },
        },
        "required": ["printed_page_number", "rationale"],
    },
}

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------- types


@dataclass
class OffsetResult:
    """One detection outcome. Matches the TS ``OffsetResult`` interface."""

    sourceId: str  # noqa: N815 — field name mirrors the TS JSON artifact
    pdfFile: str  # noqa: N815
    totalPhysicalPages: int  # noqa: N815
    samplePhysicalPage: int  # noqa: N815
    printedPageReported: int | None  # noqa: N815
    offset: int | None
    note: str | None = None
    status: str | None = None


@dataclass
class ProbeOutcome:
    printed: int | None
    note: str
    actual_page: int
    total_pages: int
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0


@dataclass
class CacheMetrics:
    total_calls: int = 0
    total_cache_read_tokens: int = 0
    total_cache_creation_tokens: int = 0

    def record(self, outcome: ProbeOutcome) -> None:
        self.total_calls += 1
        self.total_cache_read_tokens += outcome.cache_read_tokens
        self.total_cache_creation_tokens += outcome.cache_creation_tokens


# --------------------------------------------------------------- pdf helpers


def _extract_single_page_pdf_bytes(
    pdf_path: Path, physical_page_1indexed: int
) -> tuple[bytes, int, int]:
    """Extract one physical page as a standalone single-page PDF.

    Returns ``(pdf_bytes, total_pages, actual_page_picked)``. The page
    index is clamped into ``[1, total]`` to match the TS behaviour at
    ``frontend/scripts/detect-page-offsets.ts:82``.

    pypdfium2 API used (verified via Context7
    ``/pypdfium2-team/pypdfium2`` README, 2026-04-13):
    - ``PdfDocument(path)`` opens a doc
    - ``len(doc)`` yields the page count
    - ``PdfDocument.new()`` + ``import_pages(src, pages=[...])`` +
      ``save(buffer_or_path)`` builds a new one-page document.
    """
    src = pypdfium2.PdfDocument(str(pdf_path))
    try:
        total = len(src)
        if total <= 0:
            raise ValueError(f"PDF has no pages: {pdf_path}")
        actual = max(1, min(total, physical_page_1indexed))
        out = pypdfium2.PdfDocument.new()
        try:
            # pypdfium2 uses 0-indexed page lists.
            out.import_pages(src, pages=[actual - 1])
            # ``save`` accepts a filesystem path. Write to a temp file
            # and read bytes back; avoids relying on ``save(buffer)``
            # which some older pypdfium2 versions do not support.
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                out.save(str(tmp_path))
                data = tmp_path.read_bytes()
            finally:
                with contextlib.suppress(FileNotFoundError):
                    tmp_path.unlink()
        finally:
            _safe_close(out)
        return data, total, actual
    finally:
        _safe_close(src)


def _safe_close(doc: Any) -> None:
    close = getattr(doc, "close", None)
    if callable(close):
        close()


def _pdf_total_pages(pdf_path: Path) -> int:
    doc = pypdfium2.PdfDocument(str(pdf_path))
    try:
        return len(doc)
    finally:
        _safe_close(doc)


# --------------------------------------------------------------- Claude call


def _probe_one_page(
    client: anthropic.Anthropic,
    pdf_path: Path,
    physical_page: int,
    *,
    model: str,
) -> ProbeOutcome:
    """Ask Claude to read the printed page number off one physical page."""
    pdf_bytes, total_pages, actual_page = _extract_single_page_pdf_bytes(pdf_path, physical_page)
    b64 = base64.standard_b64encode(pdf_bytes).decode("ascii")

    # System prompt as a list-of-blocks so we can attach cache_control.
    # Per Context7 /anthropics/anthropic-sdk-python api.md,
    # CacheControlEphemeral is on the stable types surface, so this
    # shape is accepted by the stable ``messages.create`` endpoint.
    system_blocks: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": _SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ]

    # Tool definition also cached — it's identical across every probe.
    tool_def: dict[str, Any] = {
        **_READ_PAGE_NUMBER_TOOL,
        "cache_control": {"type": "ephemeral"},
    }

    response = client.messages.create(
        model=model,
        max_tokens=512,
        system=cast(Any, system_blocks),
        messages=[
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
                            "What printed page number appears on this book "
                            "page (usually in the header or footer)? Respond "
                            "via the tool."
                        ),
                    },
                ],
            }
        ],
        tools=cast(Any, [tool_def]),
        tool_choice=cast(Any, {"type": "tool", "name": "report_printed_page_number"}),
    )

    usage = getattr(response, "usage", None)
    cache_read = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    cache_creation = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)

    tool_use = next(
        (block for block in response.content if getattr(block, "type", None) == "tool_use"),
        None,
    )
    if tool_use is None:
        return ProbeOutcome(
            printed=None,
            note="No tool call",
            actual_page=actual_page,
            total_pages=total_pages,
            cache_read_tokens=cache_read,
            cache_creation_tokens=cache_creation,
        )

    tool_input = cast(dict[str, Any], getattr(tool_use, "input", {}) or {})
    printed_raw = tool_input.get("printed_page_number")
    printed: int | None
    if printed_raw is None:
        printed = None
    else:
        try:
            printed = int(printed_raw)
        except (TypeError, ValueError):
            printed = None
    rationale = str(tool_input.get("rationale", ""))
    return ProbeOutcome(
        printed=printed,
        note=rationale,
        actual_page=actual_page,
        total_pages=total_pages,
        cache_read_tokens=cache_read,
        cache_creation_tokens=cache_creation,
    )


# --------------------------------------------------------------- public API


def _probe_targets(total: int) -> list[int]:
    """Return the 4 physical-page probe targets. Matches TS lines 198-203."""
    return [
        max(40, total // 2),
        max(40, int(total * 0.3)),
        max(40, int(total * 0.7)),
        max(40, int(total * 0.4)),
    ]


async def detect_offsets_for_source(
    source_id: str,
    pdf_path: Path,
    client: anthropic.Anthropic,
    *,
    model: str = DEFAULT_MODEL,
    metrics: CacheMetrics | None = None,
) -> OffsetResult:
    """Detect the printed-vs-physical offset for one source PDF.

    Async signature per the Phase 2 spec; the underlying ``anthropic``
    client exposes a synchronous ``messages.create`` at this pin, so
    the work runs synchronously inside the coroutine. The async shape
    is preserved so the caller can drive many PDFs concurrently once
    the SDK's ``AsyncAnthropic`` variant is adopted.
    """
    pdf_file = pdf_path.name
    if not pdf_path.exists():
        return OffsetResult(
            sourceId=source_id,
            pdfFile=pdf_file,
            totalPhysicalPages=0,
            samplePhysicalPage=0,
            printedPageReported=None,
            offset=None,
            note="PDF file missing",
        )

    total = _pdf_total_pages(pdf_path)

    observed: list[dict[str, int]] = []
    last_note = ""
    last_physical = 0
    for target in _probe_targets(total):
        probe = _probe_one_page(client, pdf_path, target, model=model)
        if metrics is not None:
            metrics.record(probe)
        last_physical = probe.actual_page
        last_note = probe.note
        if probe.printed is not None:
            observed.append(
                {
                    "physical": probe.actual_page,
                    "printed": probe.printed,
                    "offset": probe.actual_page - probe.printed,
                }
            )
            if len(observed) >= MAX_PROBES_FOR_CONSENSUS:
                break

    if not observed:
        return OffsetResult(
            sourceId=source_id,
            pdfFile=pdf_file,
            totalPhysicalPages=total,
            samplePhysicalPage=last_physical,
            printedPageReported=None,
            offset=None,
            note=(
                f"no printed page numbers visible in 4 probe points; last rationale: {last_note}"
            ),
        )

    # Majority vote on offsets. Dict insertion order preserves
    # first-occurrence tie-breaking — matches the TS ``Map`` iteration.
    tally: dict[int, int] = {}
    for o in observed:
        tally[o["offset"]] = tally.get(o["offset"], 0) + 1
    consensus_offset = max(tally.items(), key=lambda kv: kv[1])[0]
    picked = next(o for o in observed if o["offset"] == consensus_offset)

    if abs(consensus_offset) > OFFSET_SANITY_LIMIT:
        return OffsetResult(
            sourceId=source_id,
            pdfFile=pdf_file,
            totalPhysicalPages=total,
            samplePhysicalPage=picked["physical"],
            printedPageReported=picked["printed"],
            offset=None,
            note=(
                f"detected offset +{consensus_offset} exceeds sanity limit "
                f"(±{OFFSET_SANITY_LIMIT}); probable chapter-local numbering "
                "— needs manual inspection"
            ),
        )

    if len(observed) > 1 and tally[consensus_offset] > 1:
        agreement_note = f"consensus across {tally[consensus_offset]}/{len(observed)} probes"
    elif len(observed) > 1:
        joined = ", ".join(f"+{o['offset']}" for o in observed)
        agreement_note = f"probes disagreed: {joined} — picked first"
    else:
        agreement_note = "single probe only"

    return OffsetResult(
        sourceId=source_id,
        pdfFile=pdf_file,
        totalPhysicalPages=total,
        samplePhysicalPage=picked["physical"],
        printedPageReported=picked["printed"],
        offset=consensus_offset,
        note=agreement_note,
    )


def default_output_path() -> Path:
    """Cross-repo artifact path the TS resolver still reads from."""
    return repo_root() / "frontend" / "scripts" / ".page-offsets.json"


def _load_existing(output_path: Path) -> dict[str, Any]:
    if not output_path.exists():
        return {}
    try:
        return cast(dict[str, Any], json.loads(output_path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError):
        return {}


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON atomically via temp-file + rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=".page-offsets-", suffix=".json.tmp", dir=str(path.parent)
    )
    try:
        with io.TextIOWrapper(os.fdopen(fd, "wb"), encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
            fh.write("\n")
        os.replace(tmp_name, path)
    except Exception:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp_name)
        raise


def _merge_results(
    existing: dict[str, Any],
    new_results: list[OffsetResult],
    *,
    generated_at: str,
) -> dict[str, Any]:
    """Merge new results into the existing artifact.

    The TS original fully rewrites the file. The Python port merges
    instead so the human-authored "unresolvable" entries for S3, S5,
    S6, S9 (see ``frontend/scripts/.page-offsets.json`` notes) survive
    re-runs. Any source that produced a non-null offset in ``new_results``
    is updated; everything else is preserved verbatim.
    """
    existing_offsets: dict[str, int] = {}
    raw_offsets = existing.get("offsets")
    if isinstance(raw_offsets, dict):
        for k, v in raw_offsets.items():
            if isinstance(v, int):
                existing_offsets[str(k)] = v

    existing_results: list[dict[str, Any]] = []
    raw_results = existing.get("results")
    if isinstance(raw_results, list):
        existing_results = [r for r in raw_results if isinstance(r, dict)]

    new_by_sid = {r.sourceId: r for r in new_results}
    merged_offsets = dict(existing_offsets)
    for sid, r in new_by_sid.items():
        if r.offset is not None:
            merged_offsets[sid] = r.offset
        # If new run says None, leave the existing offset entry alone —
        # we do not want to erase a working offset because Claude had a
        # bad day. The results array entry below captures the null run.

    merged_results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for old in existing_results:
        sid = str(old.get("sourceId", ""))
        if sid and sid in new_by_sid:
            fresh = new_by_sid[sid]
            # Only overwrite the result if the new run actually produced
            # a valid offset. Otherwise keep the curated old entry
            # (which may carry the manual-review note verbatim).
            if fresh.offset is not None:
                merged_results.append(_result_dict(fresh))
            else:
                merged_results.append(old)
            seen.add(sid)
        else:
            merged_results.append(old)
    for sid, fresh in new_by_sid.items():
        if sid not in seen:
            merged_results.append(_result_dict(fresh))

    payload: dict[str, Any] = {
        "generatedAt": generated_at,
        "offsets": merged_offsets,
        "results": merged_results,
    }
    # Preserve an optional human-authored field if present.
    if "lastManualReviewAt" in existing:
        payload["lastManualReviewAt"] = existing["lastManualReviewAt"]
    return payload


def _result_dict(r: OffsetResult) -> dict[str, Any]:
    d = asdict(r)
    # Match TS JSON: drop explicit None-valued optional fields so the
    # artifact is byte-shape-compatible with the TS writer for entries
    # that lack a status/note.
    return {k: v for k, v in d.items() if v is not None or k in _REQUIRED_RESULT_FIELDS}


_REQUIRED_RESULT_FIELDS: set[str] = {
    "sourceId",
    "pdfFile",
    "totalPhysicalPages",
    "samplePhysicalPage",
    "printedPageReported",
    "offset",
}


async def run(
    sources: list[str] | None = None,
    *,
    output_path: Path | None = None,
    raw_dir: Path | None = None,
    model: str = DEFAULT_MODEL,
    client: anthropic.Anthropic | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Detect offsets for ``sources`` (or all sources) and write the JSON.

    Returns the merged payload that was written.
    """
    if output_path is None:
        output_path = default_output_path()
    if raw_dir is None:
        raw_dir = raw_pdf_dir()
    if client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        client = anthropic.Anthropic()
    if generated_at is None:
        # Stable, tz-aware ISO-8601 with trailing "Z" to match the TS
        # ``new Date().toISOString()`` output format.
        from datetime import UTC, datetime

        generated_at = datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")

    target_ids: list[str]
    if sources is None:
        target_ids = list(SOURCE_PDFS.keys())
    else:
        unknown = [s for s in sources if s not in SOURCE_PDFS]
        if unknown:
            raise KeyError(f"Unknown source ids: {unknown!r}")
        target_ids = list(sources)

    metrics = CacheMetrics()
    new_results: list[OffsetResult] = []
    for sid in target_ids:
        pdf_name = SOURCE_PDFS[sid]
        pdf_path = raw_dir / pdf_name
        sys.stdout.write(f"[{sid}] {pdf_name} ... ")
        sys.stdout.flush()
        try:
            result = await detect_offsets_for_source(
                sid, pdf_path, client, model=model, metrics=metrics
            )
        except Exception as exc:
            result = OffsetResult(
                sourceId=sid,
                pdfFile=pdf_name,
                totalPhysicalPages=0,
                samplePhysicalPage=0,
                printedPageReported=None,
                offset=None,
                note=f"Error: {exc}",
            )
            sys.stdout.write(f"FAIL: {exc}\n")
        else:
            off = f"+{result.offset}" if result.offset is not None else "unknown"
            reported = (
                f"p.{result.printedPageReported}"
                if result.printedPageReported is not None
                else "none"
            )
            sys.stdout.write(
                f"physical {result.samplePhysicalPage}/{result.totalPhysicalPages} "
                f"shows printed {reported} -> offset {off}\n"
            )
        new_results.append(result)

    existing = _load_existing(output_path)
    payload = _merge_results(existing, new_results, generated_at=generated_at)
    _atomic_write(output_path, payload)

    sys.stdout.write(f"\nWrote offsets to {output_path}\n")
    sys.stdout.write(f"Detected offsets: {json.dumps(payload['offsets'])}\n")
    sys.stdout.write(
        f"Cache warmth: {metrics.total_calls} calls, "
        f"cache_read_input_tokens={metrics.total_cache_read_tokens}, "
        f"cache_creation_input_tokens={metrics.total_cache_creation_tokens}\n"
    )
    return payload


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="wiki-detect-page-offsets",
        description=(
            "Detect printed-page-vs-physical-page offsets for source PDFs "
            "via a single Claude call per PDF."
        ),
    )
    parser.add_argument(
        "--source",
        "-s",
        action="append",
        default=None,
        help=(
            "Restrict detection to this source id (repeatable). "
            "Omit to scan every source in the registry."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Override the output JSON path. Defaults to the cross-repo "
            "artifact at frontend/scripts/.page-offsets.json."
        ),
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=None,
        help="Override the raw PDF directory (default: backend/knowledge-base/raw).",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model id. Default: {DEFAULT_MODEL}",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    import asyncio

    args = _parse_args(argv)
    try:
        asyncio.run(
            run(
                sources=args.source,
                output_path=args.output,
                raw_dir=args.raw_dir,
                model=args.model,
            )
        )
    except RuntimeError as exc:
        sys.stderr.write(f"detect-page-offsets failed: {exc}\n")
        return 1
    except KeyError as exc:
        sys.stderr.write(f"detect-page-offsets failed: {exc}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
