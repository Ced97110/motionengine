"""Tests for ``motion.wiki_ops.ingest`` (Phase 3).

No real Claude calls. PDFs are built in-process with pypdfium2's
``PdfDocument.new`` + ``new_page``, matching the pattern established in
``test_detect_page_offsets.py``. All filesystem effects are confined to
``tmp_path``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import pypdfium2
import pytest

from motion.wiki_ops import ingest as module

# =================================================================== fake SDK


@dataclass
class _FakeUsage:
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0


@dataclass
class _FakeToolUse:
    type: str
    input: dict[str, Any]


@dataclass
class _FakeTextBlock:
    type: str
    text: str


@dataclass
class _FakeResponse:
    content: list[Any]
    usage: _FakeUsage = field(default_factory=_FakeUsage)


class _FakeMessages:
    """Deterministic stand-in for ``anthropic.Anthropic().messages``."""

    def __init__(self, scripted: list[dict[str, Any] | None]) -> None:
        self._scripted = list(scripted)
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> _FakeResponse:
        self.calls.append(kwargs)
        if not self._scripted:
            return _FakeResponse(content=[_FakeTextBlock(type="text", text="")])
        script = self._scripted.pop(0)
        if script is None:
            return _FakeResponse(content=[_FakeTextBlock(type="text", text="")])
        tool = _FakeToolUse(type="tool_use", input=script.get("input", {}))
        usage = _FakeUsage(
            cache_read_input_tokens=int(script.get("cache_read", 0)),
            cache_creation_input_tokens=int(script.get("cache_creation", 0)),
        )
        return _FakeResponse(content=[tool], usage=usage)


class _FakeClient:
    def __init__(self, scripted: list[dict[str, Any] | None]) -> None:
        self.messages = _FakeMessages(scripted)


# ================================================================== fixtures


def _make_pdf(path: Path, page_count: int) -> None:
    doc = pypdfium2.PdfDocument.new()
    try:
        for _ in range(page_count):
            doc.new_page(595, 842)
        doc.save(str(path))
    finally:
        close = getattr(doc, "close", None)
        if callable(close):
            close()


@pytest.fixture()
def raw_dir_with_s1(tmp_path: Path) -> Path:
    raw = tmp_path / "raw"
    raw.mkdir()
    _make_pdf(raw / "lets-talk-defense.pdf", 80)
    return raw


@pytest.fixture()
def wiki_root(tmp_path: Path) -> Path:
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "index.md").write_text(
        "# Basketball Coaching Knowledge Wiki\n\n"
        "## Concepts\n"
        "\n"
        "## Drills\n"
        "\n"
        "## Plays\n"
        "\n"
        "## Source Summaries\n",
        encoding="utf-8",
    )
    (wiki / "log.md").write_text(
        "# Ingestion Log\n\n> Append-only record of all wiki operations.\n",
        encoding="utf-8",
    )
    return wiki


@pytest.fixture()
def offsets_artifact(tmp_path: Path) -> Path:
    """Produce a minimal .page-offsets.json with S1 offset +0."""
    path = tmp_path / ".page-offsets.json"
    path.write_text(
        json.dumps(
            {
                "generatedAt": "2026-04-13T00:00:00.000Z",
                "offsets": {"S1": 0},
                "results": [],
            }
        ),
        encoding="utf-8",
    )
    return path


# ============================================================ chunk_pdf tests


def test_chunk_pdf_yields_expected_boundaries_no_offset(raw_dir_with_s1: Path) -> None:
    """80-page PDF with chunk_size=20 should yield 4 chunks."""
    pdf = raw_dir_with_s1 / "lets-talk-defense.pdf"
    chunks = list(module.chunk_pdf(pdf, chunk_size=20, start_page=1, offset=0))
    assert [(c.start_printed, c.end_printed) for c in chunks] == [
        (1, 20),
        (21, 40),
        (41, 60),
        (61, 80),
    ]
    # Physical == printed when offset is zero.
    assert [(c.start_physical, c.end_physical) for c in chunks] == [
        (1, 20),
        (21, 40),
        (41, 60),
        (61, 80),
    ]


def test_chunk_pdf_applies_offset(raw_dir_with_s1: Path) -> None:
    """With offset=+14, printed pp.1-20 → physical pp.15-34."""
    pdf = raw_dir_with_s1 / "lets-talk-defense.pdf"
    chunks = list(module.chunk_pdf(pdf, chunk_size=20, start_page=1, offset=14))
    assert chunks[0].start_printed == 1
    assert chunks[0].end_printed == 20
    assert chunks[0].start_physical == 15
    assert chunks[0].end_physical == 34
    # Last chunk is clamped — printed_end maps to physical 80 max.
    assert chunks[-1].end_physical <= 80


def test_chunk_pdf_respects_start_and_end_page(raw_dir_with_s1: Path) -> None:
    pdf = raw_dir_with_s1 / "lets-talk-defense.pdf"
    chunks = list(module.chunk_pdf(pdf, chunk_size=10, start_page=21, end_page=40, offset=0))
    assert [(c.start_printed, c.end_printed) for c in chunks] == [
        (21, 30),
        (31, 40),
    ]


def test_chunk_pdf_rejects_nonpositive_chunk_size(raw_dir_with_s1: Path) -> None:
    pdf = raw_dir_with_s1 / "lets-talk-defense.pdf"
    with pytest.raises(ValueError, match="chunk_size"):
        list(module.chunk_pdf(pdf, chunk_size=0))


def test_render_chunk_bytes_is_valid_pdf(raw_dir_with_s1: Path) -> None:
    """Rendered chunk bytes must be loadable as a pypdfium2 PdfDocument."""
    pdf = raw_dir_with_s1 / "lets-talk-defense.pdf"
    chunks = list(module.chunk_pdf(pdf, chunk_size=20, start_page=1))
    first = chunks[0]
    data = module.render_chunk_bytes(pdf, first)
    assert data.startswith(b"%PDF")
    reopened = pypdfium2.PdfDocument(data)
    try:
        assert len(reopened) == 20
    finally:
        close = getattr(reopened, "close", None)
        if callable(close):
            close()


# ============================================================ detect_source


def test_detect_source_matches_known_basename() -> None:
    src = module.detect_source(Path("/raw/lets-talk-defense.pdf"))
    assert src.id == "S1"
    assert "Herb Brown" in src.title


def test_detect_source_falls_back_for_unknown() -> None:
    src = module.detect_source(Path("/raw/mystery-manual.pdf"))
    assert src.id == "S?"
    assert src.title == "mystery manual"


# ============================================================ ingest_chunk


def _make_scripted_response(
    pages: list[dict[str, str]], *, notes: str = "fake notes"
) -> dict[str, Any]:
    return {
        "input": {"pages": pages, "chunk_notes": notes},
        "cache_read": 1200,
        "cache_creation": 800,
    }


def test_ingest_chunk_parses_tool_use_into_wiki_page_writes() -> None:
    fake = _FakeClient(
        scripted=[
            _make_scripted_response(
                [
                    {
                        "filename": "pick-and-roll-defense.md",
                        "content": "---\ntype: concept\n---\n# Pick and Roll Defense",
                        "summary": "How to defend the PnR.",
                        "category": "concept",
                    },
                    {
                        "filename": "3-on-3-shell-drill.md",
                        "content": "# Shell Drill",
                        "summary": "Defensive shell drill.",
                        "category": "drill",
                    },
                ]
            )
        ]
    )
    chunk = module.ChunkRange(start_printed=1, end_printed=20, start_physical=1, end_physical=20)
    result = module.ingest_chunk(
        fake,  # type: ignore[arg-type]
        chunk_bytes=b"%PDF-fake",
        chunk=chunk,
        source=module.SourceMeta(id="S1", title="Let's Talk Defense"),
        schema="SCHEMA STUB",
        index_text="INDEX STUB",
    )
    assert len(result.pages) == 2
    assert result.pages[0].filename == "pick-and-roll-defense.md"
    assert result.pages[0].category == "concept"
    assert result.pages[1].category == "drill"
    assert result.notes == "fake notes"
    assert result.cache_read_tokens == 1200
    assert result.cache_creation_tokens == 800


def test_ingest_chunk_drops_malformed_pages() -> None:
    fake = _FakeClient(
        scripted=[
            _make_scripted_response(
                [
                    {"filename": "", "content": "x", "summary": "", "category": "concept"},
                    {"filename": "ok.md", "content": "", "summary": "", "category": "concept"},
                    {"filename": "good.md", "content": "body", "summary": "s", "category": "play"},
                ]
            )
        ]
    )
    chunk = module.ChunkRange(1, 20, 1, 20)
    result = module.ingest_chunk(
        fake,  # type: ignore[arg-type]
        chunk_bytes=b"%PDF-fake",
        chunk=chunk,
        source=module.SourceMeta(id="S1", title="T"),
        schema="S",
        index_text="I",
    )
    assert [p.filename for p in result.pages] == ["good.md"]


def test_ingest_chunk_normalizes_single_dict_pages() -> None:
    """Model sometimes returns a single object instead of an array."""
    fake = _FakeClient(
        scripted=[
            {
                "input": {
                    "pages": {
                        "filename": "solo.md",
                        "content": "body",
                        "summary": "s",
                        "category": "concept",
                    },
                    "chunk_notes": "single",
                }
            }
        ]
    )
    chunk = module.ChunkRange(1, 1, 1, 1)
    result = module.ingest_chunk(
        fake,  # type: ignore[arg-type]
        chunk_bytes=b"%PDF-fake",
        chunk=chunk,
        source=module.SourceMeta(id="S1", title="T"),
        schema="S",
        index_text="I",
    )
    assert [p.filename for p in result.pages] == ["solo.md"]


def test_ingest_chunk_with_no_tool_call_returns_empty() -> None:
    fake = _FakeClient(scripted=[None])
    chunk = module.ChunkRange(1, 20, 1, 20)
    result = module.ingest_chunk(
        fake,  # type: ignore[arg-type]
        chunk_bytes=b"%PDF-fake",
        chunk=chunk,
        source=module.SourceMeta(id="S1", title="T"),
        schema="S",
        index_text="I",
    )
    assert result.pages == []
    assert result.notes == "No tool call returned"


def test_ingest_chunk_caches_system_and_tool_only() -> None:
    """System block + tool carry cache_control; user message does not."""
    fake = _FakeClient(
        scripted=[
            _make_scripted_response(
                [
                    {
                        "filename": "p.md",
                        "content": "b",
                        "summary": "s",
                        "category": "concept",
                    }
                ]
            )
        ]
    )
    chunk = module.ChunkRange(1, 20, 1, 20)
    module.ingest_chunk(
        fake,  # type: ignore[arg-type]
        chunk_bytes=b"%PDF-fake",
        chunk=chunk,
        source=module.SourceMeta(id="S1", title="T"),
        schema="S",
        index_text="I",
    )
    call = fake.messages.calls[0]
    system = call["system"]
    assert isinstance(system, list)
    assert system[0]["cache_control"] == {"type": "ephemeral"}
    tools = call["tools"]
    assert tools[0]["name"] == "write_wiki_pages"
    assert tools[0]["cache_control"] == {"type": "ephemeral"}
    # Forced tool call.
    assert call["tool_choice"] == {"type": "tool", "name": "write_wiki_pages"}
    # User message carries the PDF document block and no cache_control.
    user_content = call["messages"][0]["content"]
    assert user_content[0]["type"] == "document"
    assert user_content[0]["source"]["media_type"] == "application/pdf"
    assert "cache_control" not in user_content[0]


# ============================================================ write_pages


def test_write_pages_creates_new_files(wiki_root: Path) -> None:
    pages = [
        module.WikiPageWrite(
            filename="alpha.md",
            content="# Alpha\nbody A",
            summary="Alpha summary",
            category="concept",
        ),
        module.WikiPageWrite(
            filename="beta.md",
            content="# Beta\nbody B",
            summary="Beta summary",
            category="drill",
        ),
    ]
    normalized, created, updated = module.write_pages(pages, wiki_root)
    assert sorted(created) == ["alpha.md", "beta.md"]
    assert updated == []
    assert (wiki_root / "alpha.md").read_text(encoding="utf-8").endswith("body A")
    assert [p.filename for p in normalized] == ["alpha.md", "beta.md"]


def test_write_pages_tracks_updates_without_data_loss(wiki_root: Path) -> None:
    (wiki_root / "existing.md").write_text("# Existing — v1\n", encoding="utf-8")
    pages = [
        module.WikiPageWrite(
            filename="existing.md",
            content="# Existing — v2\nfresh body",
            summary="refreshed",
            category="concept",
        ),
    ]
    _, created, updated = module.write_pages(pages, wiki_root)
    assert created == []
    assert updated == ["existing.md"]
    # The TS behaviour is overwrite-on-collision — we match it, which
    # means the v2 body replaces v1 rather than merging. This test
    # pins that behaviour so a future change requires an intentional
    # edit to both the TS original and this port.
    body = (wiki_root / "existing.md").read_text(encoding="utf-8")
    assert body == "# Existing — v2\nfresh body"


def test_write_pages_sanitizes_path_traversal_and_unsafe_chars(wiki_root: Path) -> None:
    pages = [
        module.WikiPageWrite(
            filename="../evil/slash.md",
            content="x",
            summary="s",
            category="concept",
        ),
        module.WikiPageWrite(
            filename="Weird Name!.md",
            content="x",
            summary="s",
            category="concept",
        ),
    ]
    normalized, created, _ = module.write_pages(pages, wiki_root)
    # ``../evil/`` strips to ``slash.md`` via basename.
    assert "slash.md" in created
    # Unsafe chars collapse to hyphens.
    assert "Weird-Name-.md" in created
    # No files written outside the wiki dir.
    assert not (wiki_root.parent / "evil").exists()
    assert [p.filename for p in normalized] == ["slash.md", "Weird-Name-.md"]


# ============================================================ append_log


def test_append_log_writes_expected_prefix_and_format(wiki_root: Path) -> None:
    chunk = module.ChunkRange(start_printed=21, end_printed=40, start_physical=35, end_physical=54)
    module.append_log(
        module.SourceMeta(id="S1", title="Let's Talk Defense"),
        chunk,
        created=["a.md", "b.md"],
        updated=[],
        notes="Chapter 3: help defense",
        wiki_root=wiki_root,
        today=date(2026, 4, 13),
    )
    log = (wiki_root / "log.md").read_text(encoding="utf-8")
    assert "## [2026-04-13] ingest | Let's Talk Defense (pp.21-40)" in log
    assert "- Created: a.md, b.md" in log
    assert "- Updated: (none)" in log
    assert "- Notes: Chapter 3: help defense" in log


def test_append_log_uses_em_dash_when_notes_empty(wiki_root: Path) -> None:
    chunk = module.ChunkRange(1, 20, 1, 20)
    module.append_log(
        module.SourceMeta(id="S1", title="T"),
        chunk,
        created=[],
        updated=["x.md"],
        notes="",
        wiki_root=wiki_root,
        today=date(2026, 4, 13),
    )
    log = (wiki_root / "log.md").read_text(encoding="utf-8")
    assert "- Notes: —" in log
    assert "- Created: (none)" in log


# ============================================================ update_index


def test_update_index_inserts_under_correct_sections(wiki_root: Path) -> None:
    pages = [
        module.WikiPageWrite(
            filename="zone-defense.md",
            content="",
            summary="How to play zone.",
            category="concept",
        ),
        module.WikiPageWrite(
            filename="pressure-drill.md",
            content="",
            summary="Full-court pressure drill.",
            category="drill",
        ),
        module.WikiPageWrite(
            filename="horns-flare.md",
            content="",
            summary="Horns set with flare screen.",
            category="play",
        ),
    ]
    module.update_index(pages, wiki_root)
    body = (wiki_root / "index.md").read_text(encoding="utf-8")
    # Concepts section contains the concept entry.
    concepts_start = body.index("## Concepts")
    drills_start = body.index("## Drills")
    plays_start = body.index("## Plays")
    concept_line = body.index("[Zone defense](zone-defense.md)")
    drill_line = body.index("[Pressure drill](pressure-drill.md)")
    play_line = body.index("[Horns flare](horns-flare.md)")
    assert concepts_start < concept_line < drills_start
    assert drills_start < drill_line < plays_start
    assert plays_start < play_line


def test_update_index_dedups_existing_links(wiki_root: Path) -> None:
    (wiki_root / "index.md").write_text(
        "## Concepts\n- [Already there](already.md) — prior summary.\n"
        "## Drills\n\n## Plays\n\n## Source Summaries\n",
        encoding="utf-8",
    )
    pages = [
        module.WikiPageWrite(
            filename="already.md",
            content="",
            summary="duplicate should not be added",
            category="concept",
        ),
        module.WikiPageWrite(
            filename="fresh.md",
            content="",
            summary="fresh page.",
            category="concept",
        ),
    ]
    module.update_index(pages, wiki_root)
    body = (wiki_root / "index.md").read_text(encoding="utf-8")
    # "already.md" appears exactly once — not duplicated.
    assert body.count("](already.md)") == 1
    # "fresh.md" was appended under the Concepts section.
    assert "](fresh.md)" in body


# ============================================================ dry-run


def test_dry_run_makes_zero_filesystem_changes(
    raw_dir_with_s1: Path, wiki_root: Path, offsets_artifact: Path
) -> None:
    """Dry-run must not write to the wiki or call Claude."""
    fake = _FakeClient(scripted=[])
    before_index = (wiki_root / "index.md").read_text(encoding="utf-8")
    before_log = (wiki_root / "log.md").read_text(encoding="utf-8")
    before_files = sorted(p.name for p in wiki_root.iterdir())

    summary = module.run(
        "S1",
        chunk_size=20,
        dry_run=True,
        raw_dir=raw_dir_with_s1,
        wiki_root=wiki_root,
        page_offsets_path=offsets_artifact,
        client=fake,  # type: ignore[arg-type]
    )

    assert summary.total_chunks == 4
    assert summary.total_pages_written == 0
    # Zero Claude calls.
    assert fake.messages.calls == []
    # No file changes.
    assert (wiki_root / "index.md").read_text(encoding="utf-8") == before_index
    assert (wiki_root / "log.md").read_text(encoding="utf-8") == before_log
    assert sorted(p.name for p in wiki_root.iterdir()) == before_files


# ============================================================ full run


def test_run_end_to_end_writes_pages_log_and_index(
    raw_dir_with_s1: Path, wiki_root: Path, offsets_artifact: Path
) -> None:
    """Integration: one PDF, two chunks, two pages emitted, everything wired."""
    # 80-page PDF, chunk_size=40 → two chunks.
    fake = _FakeClient(
        scripted=[
            _make_scripted_response(
                [
                    {
                        "filename": "help-defense.md",
                        "content": "# Help Defense\n[S1, p.12]",
                        "summary": "Rotation help rules.",
                        "category": "concept",
                    }
                ],
                notes="Ch.1: help defense",
            ),
            _make_scripted_response(
                [
                    {
                        "filename": "closeout-drill.md",
                        "content": "# Closeout drill\n[S1, p.55]",
                        "summary": "Closeout fundamentals.",
                        "category": "drill",
                    }
                ],
                notes="Ch.5: closeouts",
            ),
        ]
    )
    summary = module.run(
        "S1",
        chunk_size=40,
        dry_run=False,
        raw_dir=raw_dir_with_s1,
        wiki_root=wiki_root,
        page_offsets_path=offsets_artifact,
        client=fake,  # type: ignore[arg-type]
        today=date(2026, 4, 13),
    )

    # Two chunks → two API calls.
    assert len(fake.messages.calls) == 2
    assert summary.total_pages_written == 2
    assert sorted(summary.created) == ["closeout-drill.md", "help-defense.md"]
    assert summary.total_cache_read_tokens == 1200 * 2
    assert summary.total_cache_creation_tokens == 800 * 2

    # Pages on disk carry the expected content (and preserve the
    # citation prefix — acceptance gate from spec §7.3).
    help_body = (wiki_root / "help-defense.md").read_text(encoding="utf-8")
    assert "[S1, p.12]" in help_body
    closeout_body = (wiki_root / "closeout-drill.md").read_text(encoding="utf-8")
    assert "[S1, p.55]" in closeout_body

    # Log has two appended entries, dated and citation-correct.
    log = (wiki_root / "log.md").read_text(encoding="utf-8")
    assert log.count("## [2026-04-13] ingest | Let's Talk Defense") == 2
    assert "(pp.1-40)" in log
    assert "(pp.41-80)" in log

    # Index has both pages under their categories.
    index = (wiki_root / "index.md").read_text(encoding="utf-8")
    assert "](help-defense.md)" in index
    assert "](closeout-drill.md)" in index
    # Concept entry lives above Drill entry.
    assert index.index("](help-defense.md)") < index.index("](closeout-drill.md)")


def test_run_uses_source_offset_from_page_offsets_file(
    raw_dir_with_s1: Path, wiki_root: Path, tmp_path: Path
) -> None:
    """An offset of +14 shifts physical pages by 14 for S1."""
    offsets_path = tmp_path / ".page-offsets.json"
    offsets_path.write_text(json.dumps({"offsets": {"S1": 14}, "results": []}), encoding="utf-8")
    fake = _FakeClient(scripted=[])
    summary = module.run(
        "S1",
        chunk_size=20,
        dry_run=True,
        raw_dir=raw_dir_with_s1,
        wiki_root=wiki_root,
        page_offsets_path=offsets_path,
        client=fake,  # type: ignore[arg-type]
    )
    # 80 physical - 14 offset = 66 printed pages → 4 chunks of 20 except
    # the last, which covers printed 61-66 (6 pages).
    assert summary.total_chunks == 4


def test_run_rejects_unknown_source_id(raw_dir_with_s1: Path, wiki_root: Path) -> None:
    with pytest.raises(KeyError):
        module.run(
            "S99",
            dry_run=True,
            raw_dir=raw_dir_with_s1,
            wiki_root=wiki_root,
        )


def test_run_without_api_key_outside_dry_run_raises(
    raw_dir_with_s1: Path, wiki_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        module.run(
            "S1",
            dry_run=False,
            raw_dir=raw_dir_with_s1,
            wiki_root=wiki_root,
            # No client → run must fail fast when env is unset.
        )
