"""Parity tests for ``motion.wiki_ops.lint_wiki``.

Timestamp exception per the Phase 1 spec: the audit report contains a
``Generated: YYYY-MM-DD`` header. :func:`_strip_generation_timestamp`
normalizes that line before any byte-level diff so the parity
comparison doesn't flap on date.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

import pytest

from motion.wiki_ops.lint_wiki import (
    Finding,
    build_report,
    run_lint,
)

FIXED_NOW = datetime(2026, 4, 13, 0, 0, 0, tzinfo=UTC)


def _strip_generation_timestamp(report: str) -> str:
    """Normalize the leading ``# Wiki Lint Report — <date>`` line.

    The TS report header is generated with ``new Date().toISOString().slice(0, 10)``;
    the Python port uses ``datetime.now(UTC).strftime('%Y-%m-%d')``. To
    keep parity tests date-insensitive, both surfaces are rewritten to
    ``# Wiki Lint Report — YYYY-MM-DD`` before diffing.
    """
    return re.sub(
        r"^# Wiki Lint Report — \d{4}-\d{2}-\d{2}$",
        "# Wiki Lint Report — YYYY-MM-DD",
        report,
        count=1,
        flags=re.MULTILINE,
    )


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture()
def minimal_wiki(tmp_path: Path) -> Path:
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    _write(
        wiki / "index.md",
        "# Index\n\n- [Alpha](alpha.md)\n- [Beta](beta.md)\n",
    )
    _write(
        wiki / "alpha.md",
        (
            "---\n"
            "type: concept\n"
            "---\n\n"
            "# Alpha\n\n"
            "## Summary\nIntro text [S1, p.10].\n\n"
            "## When to Use\nCase 1.\n\n"
            "## Key Principles\nPrinciple A.\n\n"
            "## Related Concepts\n- [[beta]]\n\n"
            "## Sources\n- [S1, p.10]\n"
        ),
    )
    _write(
        wiki / "beta.md",
        (
            "---\n"
            "type: concept\n"
            "---\n\n"
            "# Beta\n\n"
            "## Summary\nIntro text [S1, p.11].\n\n"
            "## When to Use\nCase 2.\n\n"
            "## Key Principles\nPrinciple B.\n\n"
            "## Related Concepts\n- [[alpha]]\n\n"
            "## Sources\n- [S1, p.11]\n"
        ),
    )
    _write(wiki / "log.md", "Log entry.\n")
    return wiki


def test_clean_wiki_has_no_errors(minimal_wiki: Path) -> None:
    total_pages, findings = run_lint(minimal_wiki)
    assert total_pages == 4  # index + alpha + beta + log
    errors = [f for f in findings if f.severity == "error"]
    assert errors == []


def test_filename_violation_upper_and_space(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(wiki / "Bad Name.md", "---\ntype: concept\n---\n# Bad\n")
    _, findings = run_lint(wiki)
    filename_errors = [f for f in findings if f.check == "filename-violation"]
    assert len(filename_errors) == 1
    msg = filename_errors[0].message
    assert "contains uppercase" in msg
    assert "contains whitespace" in msg


def test_duplicate_slug_detection(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    # Two filenames that normalize to the same slug key.
    _write(wiki / "press-break.md", "---\ntype: concept\n---\n# Press Break\n")
    _write(wiki / "Press break.md", "---\ntype: concept\n---\n# Press Break 2\n")
    _, findings = run_lint(wiki)
    dup = [f for f in findings if f.check == "duplicate-slug"]
    assert len(dup) == 2


def test_dead_wikilink_flags_missing_target(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(
        wiki / "alpha.md",
        "---\ntype: concept\n---\n# Alpha\n## Summary\nSee [[nonexistent]].\n",
    )
    _, findings = run_lint(wiki)
    dead = [f for f in findings if f.check == "dead-wikilink"]
    assert len(dead) >= 1
    assert "nonexistent" in dead[0].message


def test_stale_diagram_marker_detection(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(
        wiki / "alpha.md",
        (
            "---\ntype: play\n---\n# Alpha\n\n"
            "## Overview\n<!-- DIAGRAM: phase-1 -->\n\n"
            "## Formation\nBox\n\n## Phases\n### P1\nAlpha\n\n## Key Coaching Points\nx\n"
            "\n## Sources\n[S1]\n"
        ),
    )
    _, findings = run_lint(wiki)
    stale = [f for f in findings if f.check == "stale-diagram-marker"]
    assert len(stale) == 1


def test_missing_citation_for_plain_page(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(
        wiki / "alpha.md",
        (
            "---\ntype: concept\n---\n# Alpha\n\n"
            "## Summary\nIntro.\n\n## When to Use\nX.\n\n"
            "## Key Principles\nY.\n\n## Related Concepts\nZ.\n\n## Sources\nNone.\n"
        ),
    )
    _, findings = run_lint(wiki)
    missing = [f for f in findings if f.check == "missing-citation"]
    assert missing
    assert missing[0].severity == "warning"


def test_schema_section_missing_for_play(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(
        wiki / "alpha.md",
        (
            "---\ntype: play\n---\n# Alpha\n\n"
            "## Overview\nIntro [S1, p.1].\n\n"
            "## Formation\nBox\n\n## Phases\n### P1\nx\n"
        ),
    )
    _, findings = run_lint(wiki)
    schema = [f for f in findings if f.check == "schema-section-missing"]
    assert schema
    assert "Key Coaching Points" in schema[0].message or "Sources" in schema[0].message


def test_duplicate_index_entry_detection(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(
        wiki / "index.md",
        "# Index\n- [A](alpha.md)\n- [Same](alpha.md)\n",
    )
    _write(wiki / "alpha.md", "---\ntype: concept\n---\n# Alpha\n")
    _, findings = run_lint(wiki)
    dup = [f for f in findings if f.check == "duplicate-index-entry"]
    assert len(dup) == 1
    assert 'Slug "alpha" is listed 2 times' in dup[0].message


def test_bidirectional_failure_detection(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(wiki / "alpha.md", "---\ntype: concept\n---\n# Alpha\n\nSee [[beta]].\n")
    _write(wiki / "beta.md", "---\ntype: concept\n---\n# Beta\n\nNo backlink.\n")
    _, findings = run_lint(wiki)
    bi = [f for f in findings if f.check == "bidirectional-failure"]
    assert any("alpha" in f.message for f in bi)


def test_orphan_page_detection(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(wiki / "alpha.md", "---\ntype: concept\n---\n# Alpha\n")
    _, findings = run_lint(wiki)
    orphans = [f for f in findings if f.check == "orphan-page"]
    assert any("alpha" in f.message for f in orphans)


def test_build_report_header_is_normalizable(minimal_wiki: Path, tmp_path: Path) -> None:
    total_pages, findings = run_lint(minimal_wiki)
    report = build_report(total_pages, findings, reference=tmp_path, now=FIXED_NOW)
    normalized = _strip_generation_timestamp(report)
    assert normalized.splitlines()[0] == "# Wiki Lint Report — YYYY-MM-DD"
    # The summary table is always present even with zero findings.
    assert "| Check | Severity | Count | Recommendation |" in normalized


def test_findings_have_expected_severities(minimal_wiki: Path) -> None:
    _, findings = run_lint(minimal_wiki)
    for f in findings:
        assert f.severity in {"error", "warning", "info"}
        assert isinstance(f, Finding)


# ---------------------------------------------------------------------------
# Play-geometry lint rules
# ---------------------------------------------------------------------------


_VALID_PLAY_MD = """---
type: play
category: offense
---

# Clean

## Overview
Sample.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":-18,"y":22}],"ballStart":"1","actions":[{"from":"1","to":"2","type":"pass","path":"M 0 33 L -18 22"}],"notes":"Phase 1."}
```

## Phases

### Phase 1: Only
- 1 passes to 2.

## Sources
- [Sx, p.1]
"""


def test_play_diagram_per_phase_warns_on_missing_block(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    md = _VALID_PLAY_MD + "\n### Phase 2: Action\n- Later.\n"
    _write(wiki / "play-sparse.md", md)
    _, findings = run_lint(wiki)
    rule = [f for f in findings if f.check == "play-diagram-per-phase"]
    assert rule, "expected warning when phase count exceeds block count"
    assert rule[0].severity == "warning"


def test_play_path_valid_svg_flags_angle_brackets(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    bad = _VALID_PLAY_MD.replace(
        '"path":"M 0 33 L -18 22"',
        '"path":"<script>alert(1)</script>"',
    )
    _write(wiki / "play-evil.md", bad)
    _, findings = run_lint(wiki)
    rule = [f for f in findings if f.check == "play-path-valid-svg"]
    assert rule
    assert rule[0].severity == "warning"


def test_play_path_roles_resolve_flags_unknown_from(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    bad = _VALID_PLAY_MD.replace('"from":"1"', '"from":"99"')
    _write(wiki / "play-ghost.md", bad)
    _, findings = run_lint(wiki)
    rule = [f for f in findings if f.check == "play-path-roles-resolve"]
    assert rule
    assert "99" in rule[0].message


def test_play_duration_sane_flags_extreme(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    bad = _VALID_PLAY_MD.replace(
        '"path":"M 0 33 L -18 22"',
        '"path":"M 0 33 L -18 22","durationMs":120000',
    )
    _write(wiki / "play-slow.md", bad)
    _, findings = run_lint(wiki)
    rule = [f for f in findings if f.check == "play-duration-sane"]
    assert rule
    assert "120000" in rule[0].message


def test_play_ballstart_known_flags_off_roster(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    bad = _VALID_PLAY_MD.replace('"ballStart":"1"', '"ballStart":"99"')
    _write(wiki / "play-bad-ball.md", bad)
    _, findings = run_lint(wiki)
    rule = [f for f in findings if f.check == "play-ballstart-known"]
    assert rule
    assert "99" in rule[0].message


def test_valid_play_page_triggers_no_play_warnings(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    _write(wiki / "play-clean.md", _VALID_PLAY_MD)
    _, findings = run_lint(wiki)
    play_rules = [
        "play-diagram-per-phase",
        "play-path-valid-svg",
        "play-path-roles-resolve",
        "play-duration-sane",
        "play-ballstart-known",
    ]
    for rule in play_rules:
        hits = [f for f in findings if f.check == rule]
        assert not hits, f"unexpected {rule} finding(s): {hits}"
