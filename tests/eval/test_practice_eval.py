"""Eval harness for ``services.practice_brief.build_practice_brief``.

Mirrors :mod:`tests.eval.test_form_coach_eval`. Each case in
``eval/practice-cases.jsonl`` carries a synthetic ``level`` +
``duration_minutes`` + ``focus_areas`` payload. Stub mode is fully
deterministic + offline; live mode (``RUN_LIVE_EVAL=1`` +
``ANTHROPIC_API_KEY``) calls Claude Sonnet 4.6 with the structured
``emit_practice_plan`` tool.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from motion.services.practice_brief import build_practice_brief
from motion.wiki_ops.retrieval import (
    CompiledIndexes,
    build_practice_context,
    load_indexes,
)
from tests.eval._scoring import failed_signals, score_practice_brief


@pytest.fixture(scope="module")
def indexes() -> CompiledIndexes:
    return load_indexes()


def _run_case(
    case: dict[str, Any],
    indexes: CompiledIndexes,
    forbidden_phrases: list[str],
    force_stub: bool,
) -> tuple[list[dict[str, Any]], list[str], dict[str, Any]]:
    ctx = build_practice_context(
        level=case["level"],
        duration_minutes=case["duration_minutes"],
        focus_areas=case["focus_areas"],
        indexes=indexes,
        plays_in_library=case.get("plays_in_library") or [],
    )

    if force_stub:
        original = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            result = build_practice_brief(ctx)
        finally:
            if original is not None:
                os.environ["ANTHROPIC_API_KEY"] = original
    else:
        result = build_practice_brief(ctx)

    plan = [
        {
            "drill_slug": b.drill_slug,
            "duration_minutes": b.duration_minutes,
            "reasoning": b.reasoning,
            "cross_refs": b.cross_refs,
        }
        for b in result.plan
    ]

    bundle_anatomy = sorted({a.region for a in ctx.anatomy})
    bundle_drills = sorted({c.drill_slug for c in ctx.candidate_drills})
    signals = score_practice_brief(
        plan=plan,
        source_citations=result.source_citations,
        case=case,
        forbidden_phrases=forbidden_phrases,
        bundle_anatomy=bundle_anatomy,
        bundle_drills=bundle_drills,
    )
    return plan, result.source_citations, signals


def _assert_pass(case: dict[str, Any], signals: dict[str, Any], mode: str) -> None:
    failed = failed_signals(signals)
    if failed:
        detail = "\n".join(f"  {name}: {signals[name]['detail']}" for name in failed)
        pytest.fail(
            f"[{mode}] case {case['case_id']} failed signals {failed}:\n{detail}"
        )


def _cases_param() -> list[dict[str, Any]]:
    path = (
        Path(__file__).resolve().parent.parent.parent
        / "eval"
        / "practice-cases.jsonl"
    )
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


_CASES = _cases_param()


@pytest.mark.parametrize("case", _CASES, ids=[c["case_id"] for c in _CASES])
def test_practice_brief_stub(
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
def test_practice_brief_live(
    case: dict[str, Any],
    indexes: CompiledIndexes,
    forbidden_phrases: list[str],
) -> None:
    """Live Claude-backed eval — tracks composer regressions."""
    _, _, signals = _run_case(case, indexes, forbidden_phrases, force_stub=False)
    _assert_pass(case, signals, mode="live")
