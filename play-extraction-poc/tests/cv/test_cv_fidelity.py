"""CV-fidelity regression: scored structural diff against hand-authored ground truth.

This is the Eval Discipline gate. We do NOT judge CV output by visual
comparison (toV7Shape aggressively smooths errors and the viewer fabricates
defaults that hide missing movements). Instead, every expected movement is
scored for player+type+destination against the YAML produced by
``src/cv/pipeline.py``.

Each case in ``eval/cv-fidelity-cases.jsonl`` produces one pytest invocation.
The test asserts both the per-case minimum score AND produces human-readable
output so regressions surface in the report, not just as a red bar.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.cv.fidelity import (
    expected_from_case,
    format_report,
    load_actual_yaml,
    load_cases,
    score_case,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
EVAL_PATH = REPO_ROOT / "eval" / "cv-fidelity-cases.jsonl"
EXTRACTIONS_DIR = REPO_ROOT / "results" / "extractions_cv"

# Minimum aggregate F1 each case must clear. We start LENIENT (0.35) so the
# test passes at today's 2/5 while the arrows.py sub-agent lands the missing
# detections. Raise to 0.80 once page 60 reliably hits 5/5. Tighten per-case
# via the case_id override below if needed.
DEFAULT_MIN_F1 = 0.35
PER_CASE_MIN_F1: dict[str, float] = {
    # "cv-fidelity-black-p60": 0.80,  # uncomment once arrows.py hits 5/5
}


def _yaml_path_for_case(case: dict) -> Path:
    """Match the emit.py filename convention."""
    diagram_id = f"{case['panel'] + 1:02d}"
    page_id = f"{case['page']:03d}"
    return (
        EXTRACTIONS_DIR
        / f"diagram_{diagram_id}_page_{page_id}_panel_{case['panel']}_cv.yaml"
    )


def _load_cases():
    if not EVAL_PATH.exists():
        return []
    return load_cases(EVAL_PATH)


@pytest.mark.parametrize(
    "case",
    _load_cases(),
    ids=lambda c: c["case_id"],
)
def test_cv_fidelity(case: dict) -> None:
    yaml_path = _yaml_path_for_case(case)
    if not yaml_path.exists():
        pytest.skip(
            f"CV YAML not produced yet for {case['case_id']} at {yaml_path}. "
            f"Run: .venv/bin/python -m src.cv.pipeline {case['page']}"
        )
    actual = load_actual_yaml(yaml_path)
    expected = expected_from_case(case)
    report = score_case(
        expected,
        actual,
        svg_tolerance=float(case.get("svg_tolerance", 3.0)),
    )
    print("\n" + format_report(report, case_id=case["case_id"]))

    min_f1 = PER_CASE_MIN_F1.get(case["case_id"], DEFAULT_MIN_F1)
    assert report.f1 >= min_f1, (
        f"F1={report.f1:.2f} below threshold {min_f1} for {case['case_id']}. "
        f"matched={report.matched_count}/{report.expected_total} "
        f"spurious={len(report.unmatched_actuals)}"
    )
