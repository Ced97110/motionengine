"""Parity tests for ``motion.wiki_ops.check_nba_terms``."""

from __future__ import annotations

from pathlib import Path

import pytest

from motion.wiki_ops.check_nba_terms import Match, format_report, scan


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture()
def project_tree(tmp_path: Path) -> dict[str, Path]:
    """Return a map of role → path for an isolated project-like tree."""
    root = tmp_path / "frontend"
    src = root / "src"
    wiki = tmp_path / "backend" / "knowledge-base" / "wiki"
    _write(src / "app" / "page.tsx", "const caption = 'Body heat drill.';\n")
    _write(
        src / "components" / "quote.tsx",
        "const line = 'Michael Jordan owned the late-game moment.';\n",
    )
    _write(
        src / "components" / "arena.tsx",
        "const line = 'Lakers run back-to-back.';\n",
    )
    # Allowed file: scripts/check-nba-terms.ts — must not be flagged.
    _write(root / "scripts" / "check-nba-terms.ts", "const t = 'Lakers';\n")
    _write(wiki / "example-play.md", "The **UCLA** cut is a classic pattern.\n")
    # log.md is whitelisted by relative path from frontend cwd.
    _write(wiki / "log.md", "History note about the Celtics.\n")
    return {"root": root, "src": src, "wiki": wiki}


def test_scan_flags_team_college_player(project_tree: dict[str, Path]) -> None:
    hits = scan(
        [project_tree["src"], project_tree["wiki"]],
        reference=project_tree["root"],
    )
    terms = sorted({(m.term, Path(m.file).name) for m in hits})
    assert ("Lakers", "arena.tsx") in terms
    assert ("Michael Jordan", "quote.tsx") in terms
    assert ("UCLA", "example-play.md") in terms


def test_scan_respects_allowlist(project_tree: dict[str, Path]) -> None:
    hits = scan(
        [project_tree["src"], project_tree["wiki"]],
        reference=project_tree["root"],
    )
    files = {Path(m.file).name for m in hits}
    # scripts/check-nba-terms.ts is allowlisted by substring.
    assert "check-nba-terms.ts" not in files
    # log.md is allowlisted by relative path.
    assert "log.md" not in files


def test_scan_ignores_body_heat_false_positive(project_tree: dict[str, Path]) -> None:
    hits = scan(
        [project_tree["src"], project_tree["wiki"]],
        reference=project_tree["root"],
    )
    # "Heat" alone is intentionally NOT in the denylist; phrase "Body heat" shouldn't trip.
    for m in hits:
        assert m.term != "Heat"


def test_scan_detects_qualified_heat(tmp_path: Path) -> None:
    root = tmp_path / "frontend"
    src = root / "src"
    _write(src / "a.md", "The Miami Heat countered with a hard trap.\n")
    hits = scan([src], reference=root)
    terms = {m.term for m in hits}
    assert "Miami Heat" in terms


def test_scan_handles_typographic_apostrophe(tmp_path: Path) -> None:
    root = tmp_path / "frontend"
    src = root / "src"
    # Curly apostrophe in the content — must match via the TS-compatible
    # ``['’]`` character class.  # noqa: RUF003
    _write(src / "x.md", "D\u2019Angelo Russell ran the pick.\n")
    hits = scan([src], reference=root)
    assert any(m.term == "D'Angelo Russell" for m in hits)


def test_format_report_contains_filename_and_snippet(project_tree: dict[str, Path]) -> None:
    hits = [
        Match(
            file=str(project_tree["src"] / "components" / "arena.tsx"),
            line=1,
            term="Lakers",
            content="Lakers run back-to-back.",
        )
    ]
    report = format_report(hits, reference=project_tree["root"])
    assert "1 forbidden term occurrence(s)" in report
    assert "src/components/arena.tsx" in report
    assert "[Lakers]" in report
    assert "Remediation" in report


def test_scan_ignores_review_and_node_modules(tmp_path: Path) -> None:
    root = tmp_path / "frontend"
    src = root / "src"
    _write(src / "_review" / "x.md", "Lakers.\n")
    _write(src / "node_modules" / "pkg" / "a.md", "Lakers.\n")
    _write(src / "clean.md", "Nothing sensitive here.\n")
    hits = scan([src], reference=root)
    assert hits == []
