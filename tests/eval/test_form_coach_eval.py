"""Eval harness for ``services.form_brief.build_form_brief``.

Mirrors :mod:`tests.eval.test_play_brief_eval`. Each case in
``eval/form-coach-cases.jsonl`` carries a synthetic
``shot_type`` + ``measurements`` payload — no real video. The composer is
exercised with text-only input (no keyframe images) so stub eval is fully
deterministic and offline.

Live mode (``RUN_LIVE_EVAL=1`` + ``ANTHROPIC_API_KEY``) calls Claude
Sonnet 4.6 vision with the same text payload (and zero images at this
stage) to surface composer-side regressions before image-bearing eval
cases land in P1.5.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from motion.services.form_brief import build_form_brief
from motion.wiki_ops.retrieval import (
    CompiledIndexes,
    FormMeasurement,
    build_form_context,
    load_indexes,
)
from tests.eval._scoring import failed_signals, score_brief


@pytest.fixture(scope="module")
def indexes() -> CompiledIndexes:
    return load_indexes()


def _measurements_from_case(case: dict[str, Any]) -> list[FormMeasurement]:
    return [
        FormMeasurement(
            name=m["name"],
            value=float(m["value"]),
            unit=str(m["unit"]),
            flagged=bool(m["flagged"]),
            threshold=float(m["threshold"]),
        )
        for m in case.get("measurements") or []
    ]


def _run_case(
    case: dict[str, Any],
    indexes: CompiledIndexes,
    forbidden_phrases: list[str],
    force_stub: bool,
) -> tuple[str, list[str], dict[str, Any]]:
    measurements = _measurements_from_case(case)
    ctx = build_form_context(
        shot_type=case["shot_type"],
        measurements=measurements,
        indexes=indexes,
        keyframe_count=0,
    )

    if force_stub:
        original = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            result = build_form_brief(ctx, keyframe_images=None)
        finally:
            if original is not None:
                os.environ["ANTHROPIC_API_KEY"] = original
    else:
        result = build_form_brief(ctx, keyframe_images=None)

    bundle_anatomy = sorted({a.region for a in ctx.anatomy})
    bundle_drills = sorted(ctx.drill_focus)
    signals = score_brief(
        brief_text=result.brief,
        source_citations=result.source_citations,
        case=case,
        forbidden_phrases=forbidden_phrases,
        bundle_anatomy=bundle_anatomy,
        bundle_drills=bundle_drills,
    )
    return result.brief, result.source_citations, signals


def _assert_pass(case: dict[str, Any], signals: dict[str, Any], mode: str) -> None:
    failed = failed_signals(signals)
    if failed:
        detail = "\n".join(f"  {name}: {signals[name]['detail']}" for name in failed)
        pytest.fail(
            f"[{mode}] case {case['case_id']} failed signals {failed}:\n{detail}"
        )


def _cases_param() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parent.parent.parent / "eval" / "form-coach-cases.jsonl"
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


_CASES = _cases_param()


@pytest.mark.parametrize("case", _CASES, ids=[c["case_id"] for c in _CASES])
def test_form_brief_stub(
    case: dict[str, Any],
    indexes: CompiledIndexes,
    forbidden_phrases: list[str],
) -> None:
    """Stub-path eval — deterministic, offline, always runs."""
    _, _, signals = _run_case(case, indexes, forbidden_phrases, force_stub=True)
    _assert_pass(case, signals, mode="stub")


_LIVE_ENABLED = os.environ.get("RUN_LIVE_EVAL") == "1" and bool(
    os.environ.get("ANTHROPIC_API_KEY")
)


@pytest.mark.skipif(
    not _LIVE_ENABLED,
    reason="live eval requires RUN_LIVE_EVAL=1 and ANTHROPIC_API_KEY",
)
@pytest.mark.parametrize("case", _CASES, ids=[c["case_id"] for c in _CASES])
def test_form_brief_live(
    case: dict[str, Any],
    indexes: CompiledIndexes,
    forbidden_phrases: list[str],
) -> None:
    """Live Claude-backed eval — tracks regressions in synthesized prose."""
    _, _, signals = _run_case(case, indexes, forbidden_phrases, force_stub=False)
    _assert_pass(case, signals, mode="live")
