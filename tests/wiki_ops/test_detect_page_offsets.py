"""Tests for ``motion.wiki_ops.detect_page_offsets``.

Phase 2 of the wiki-ops migration. No real Claude API calls; every
test stubs ``anthropic.Anthropic`` with a canned response factory.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pypdfium2
import pytest

from motion.wiki_ops import detect_page_offsets as module

# ----------------------------------------------------------------- fake SDK


@dataclass
class _FakeUsage:
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0


@dataclass
class _FakeToolUse:
    type: str
    input: dict[str, Any]


@dataclass
class _FakeResponse:
    content: list[_FakeToolUse]
    usage: _FakeUsage = field(default_factory=_FakeUsage)


class _FakeMessages:
    def __init__(
        self,
        *,
        printed_by_call: list[int | None],
        cache_read: int = 0,
        cache_creation: int = 0,
    ) -> None:
        self._printed = list(printed_by_call)
        self.calls: list[dict[str, Any]] = []
        self._cache_read = cache_read
        self._cache_creation = cache_creation

    def create(self, **kwargs: Any) -> _FakeResponse:
        self.calls.append(kwargs)
        # Pop the next scripted answer; if we run out, default to None.
        printed = self._printed.pop(0) if self._printed else None
        tool_use = _FakeToolUse(
            type="tool_use",
            input={
                "printed_page_number": printed,
                "rationale": f"fake probe #{len(self.calls)}",
            },
        )
        return _FakeResponse(
            content=[tool_use],
            usage=_FakeUsage(
                cache_read_input_tokens=self._cache_read,
                cache_creation_input_tokens=self._cache_creation,
            ),
        )


class _FakeClient:
    def __init__(
        self,
        *,
        printed_by_call: list[int | None],
        cache_read: int = 0,
        cache_creation: int = 0,
    ) -> None:
        self.messages = _FakeMessages(
            printed_by_call=printed_by_call,
            cache_read=cache_read,
            cache_creation=cache_creation,
        )


# --------------------------------------------------------------- fixtures


def _write_minimal_pdf(path: Path, page_count: int) -> None:
    pdf = pypdfium2.PdfDocument.new()
    try:
        for _ in range(page_count):
            pdf.new_page(595, 842)
        pdf.save(str(path))
    finally:
        close = getattr(pdf, "close", None)
        if callable(close):
            close()


@pytest.fixture()
def raw_dir_with_one_pdf(tmp_path: Path) -> Path:
    raw = tmp_path / "raw"
    raw.mkdir()
    # S1 is ``lets-talk-defense.pdf`` per sources.SOURCE_PDFS.
    _write_minimal_pdf(raw / "lets-talk-defense.pdf", 120)
    return raw


# --------------------------------------------------------------- tests


def test_detect_offset_for_known_source_returns_consensus(
    raw_dir_with_one_pdf: Path, tmp_path: Path
) -> None:
    # Three probes all report printed page 45; physical clamps at 60
    # (max(40, 120/2) = 60), so offset should be 60 - 45 = 15.
    fake = _FakeClient(printed_by_call=[45, 45, 45])
    out_path = tmp_path / "offsets.json"

    payload = asyncio.run(
        module.run(
            sources=["S1"],
            output_path=out_path,
            raw_dir=raw_dir_with_one_pdf,
            client=fake,  # type: ignore[arg-type]
            generated_at="2026-04-13T00:00:00.000Z",
        )
    )

    assert payload["offsets"] == {"S1": 15}
    assert payload["generatedAt"] == "2026-04-13T00:00:00.000Z"
    results_by_sid = {r["sourceId"]: r for r in payload["results"]}
    assert results_by_sid["S1"]["offset"] == 15
    assert results_by_sid["S1"]["printedPageReported"] == 45
    assert results_by_sid["S1"]["samplePhysicalPage"] == 60
    assert results_by_sid["S1"]["totalPhysicalPages"] == 120
    # Exactly three calls because the voter short-circuits at 3.
    assert len(fake.messages.calls) == 3


def test_unresolvable_source_stays_null_in_output(
    raw_dir_with_one_pdf: Path, tmp_path: Path
) -> None:
    # All four probes return None — no printed page numbers visible.
    fake = _FakeClient(printed_by_call=[None, None, None, None])
    out_path = tmp_path / "offsets.json"

    payload = asyncio.run(
        module.run(
            sources=["S1"],
            output_path=out_path,
            raw_dir=raw_dir_with_one_pdf,
            client=fake,  # type: ignore[arg-type]
            generated_at="2026-04-13T00:00:00.000Z",
        )
    )

    # Unresolvable → the offsets map omits the key entirely.
    assert "S1" not in payload["offsets"]
    s1 = next(r for r in payload["results"] if r["sourceId"] == "S1")
    assert s1["offset"] is None
    assert s1["printedPageReported"] is None
    assert "no printed page numbers" in (s1.get("note") or "")
    # All 4 probes ran because none succeeded.
    assert len(fake.messages.calls) == 4


def test_merge_preserves_unresolvable_entries_for_other_sources(
    raw_dir_with_one_pdf: Path, tmp_path: Path
) -> None:
    """Running detection for S1 must not erase curated S3/S5 entries."""
    out_path = tmp_path / "offsets.json"
    pre_existing: dict[str, Any] = {
        "generatedAt": "2026-04-12T00:00:00.000Z",
        "lastManualReviewAt": "2026-04-13T00:00:00.000Z",
        "offsets": {"S7": 24, "S8": 7},
        "results": [
            {
                "sourceId": "S3",
                "pdfFile": "offensive-skill-development.pdf",
                "totalPhysicalPages": 230,
                "samplePhysicalPage": 92,
                "printedPageReported": None,
                "offset": None,
                "status": "unresolvable",
                "note": "Manual review: no printed page numbers.",
            },
            {
                "sourceId": "S7",
                "pdfFile": "nba-coaches-playbook.pdf",
                "totalPhysicalPages": 371,
                "samplePhysicalPage": 185,
                "printedPageReported": 161,
                "offset": 24,
                "note": "consensus across 3/3 probes",
            },
        ],
    }
    out_path.write_text(json.dumps(pre_existing), encoding="utf-8")

    fake = _FakeClient(printed_by_call=[50, 50, 50])
    payload = asyncio.run(
        module.run(
            sources=["S1"],
            output_path=out_path,
            raw_dir=raw_dir_with_one_pdf,
            client=fake,  # type: ignore[arg-type]
            generated_at="2026-04-14T00:00:00.000Z",
        )
    )

    # S7 offset survives because we didn't re-run it.
    assert payload["offsets"]["S7"] == 24
    assert payload["offsets"]["S8"] == 7
    # S1 got the new value (60 - 50 = 10).
    assert payload["offsets"]["S1"] == 10
    # Manual-review S3 entry preserved verbatim, with status intact.
    s3 = next(r for r in payload["results"] if r["sourceId"] == "S3")
    assert s3["status"] == "unresolvable"
    assert s3["offset"] is None
    assert "Manual review" in s3["note"]
    # Human-authored top-level field survives.
    assert payload["lastManualReviewAt"] == "2026-04-13T00:00:00.000Z"


def test_null_run_does_not_erase_existing_offset(
    raw_dir_with_one_pdf: Path, tmp_path: Path
) -> None:
    """A failed re-detect must not erase a previously-good offset."""
    out_path = tmp_path / "offsets.json"
    pre_existing: dict[str, Any] = {
        "generatedAt": "2026-04-12T00:00:00.000Z",
        "offsets": {"S1": 14},
        "results": [
            {
                "sourceId": "S1",
                "pdfFile": "lets-talk-defense.pdf",
                "totalPhysicalPages": 274,
                "samplePhysicalPage": 137,
                "printedPageReported": 123,
                "offset": 14,
                "note": "consensus across 3/3 probes",
            }
        ],
    }
    out_path.write_text(json.dumps(pre_existing), encoding="utf-8")

    fake = _FakeClient(printed_by_call=[None, None, None, None])
    payload = asyncio.run(
        module.run(
            sources=["S1"],
            output_path=out_path,
            raw_dir=raw_dir_with_one_pdf,
            client=fake,  # type: ignore[arg-type]
            generated_at="2026-04-14T00:00:00.000Z",
        )
    )
    assert payload["offsets"]["S1"] == 14
    # The curated old result block also survives when the fresh run
    # produced no offset.
    s1 = next(r for r in payload["results"] if r["sourceId"] == "S1")
    assert s1["offset"] == 14
    assert s1["printedPageReported"] == 123


def test_atomic_write_leaves_no_tmp_on_success(raw_dir_with_one_pdf: Path, tmp_path: Path) -> None:
    fake = _FakeClient(printed_by_call=[30, 30, 30])
    out_path = tmp_path / "offsets.json"
    asyncio.run(
        module.run(
            sources=["S1"],
            output_path=out_path,
            raw_dir=raw_dir_with_one_pdf,
            client=fake,  # type: ignore[arg-type]
            generated_at="2026-04-13T00:00:00.000Z",
        )
    )
    assert out_path.exists()
    # No temp files should be left behind in the parent dir.
    leftovers = [p for p in out_path.parent.iterdir() if p.name.startswith(".page-offsets-")]
    assert leftovers == []
    # File is valid JSON with the expected top-level keys.
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert set(data.keys()) >= {"generatedAt", "offsets", "results"}


def test_cache_control_attached_to_system_and_tool(
    raw_dir_with_one_pdf: Path, tmp_path: Path
) -> None:
    fake = _FakeClient(printed_by_call=[42, 42, 42], cache_read=1200, cache_creation=800)
    asyncio.run(
        module.run(
            sources=["S1"],
            output_path=tmp_path / "out.json",
            raw_dir=raw_dir_with_one_pdf,
            client=fake,  # type: ignore[arg-type]
            generated_at="2026-04-13T00:00:00.000Z",
        )
    )
    # Every call must ship cache_control on the system block and the tool.
    for call in fake.messages.calls:
        system = call["system"]
        assert isinstance(system, list)
        assert system[0]["cache_control"] == {"type": "ephemeral"}
        tools = call["tools"]
        assert tools[0]["cache_control"] == {"type": "ephemeral"}
        # Forced tool call.
        assert call["tool_choice"] == {
            "type": "tool",
            "name": "report_printed_page_number",
        }
        # PDF document block present on the user message.
        user_content = call["messages"][0]["content"]
        assert user_content[0]["type"] == "document"
        assert user_content[0]["source"]["type"] == "base64"
        assert user_content[0]["source"]["media_type"] == "application/pdf"


def test_unknown_source_id_raises(tmp_path: Path) -> None:
    fake = _FakeClient(printed_by_call=[])
    with pytest.raises(KeyError):
        asyncio.run(
            module.run(
                sources=["S99"],
                output_path=tmp_path / "out.json",
                raw_dir=tmp_path,
                client=fake,  # type: ignore[arg-type]
                generated_at="2026-04-13T00:00:00.000Z",
            )
        )


def test_probe_targets_matches_ts_formula() -> None:
    assert module._probe_targets(274) == [
        max(40, 274 // 2),
        max(40, int(274 * 0.3)),
        max(40, int(274 * 0.7)),
        max(40, int(274 * 0.4)),
    ]
