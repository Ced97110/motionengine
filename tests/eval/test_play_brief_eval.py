"""Eval harness for ``services.play_brief.build_brief``.

Runs every case in ``eval/play-brief-cases.jsonl`` through the Engine and
asserts the result satisfies the play-brief rubric (see ``_scoring.py``).

Two parametrized tests:

- ``test_play_brief_stub`` — always runs, forces the stub path by clearing
  ``ANTHROPIC_API_KEY``. Validates deterministic-output contract: the UX
  never dead-ends even without a key. Cheap, offline, deterministic.
- ``test_play_brief_live`` — opt-in, skipped unless ``RUN_LIVE_EVAL=1`` AND
  ``ANTHROPIC_API_KEY`` is set. Calls Claude Sonnet 4.6 for real. Tracks
  regressions in the actual synthesized prose. ~$0.02 per case.

Both share the rubric: no verbatim book prose, length band, chain references
present, citation format valid.
"""

from __future__ import annotations

import os
from typing import Any

import pytest

from motion.services.play_brief import build_brief
from motion.wiki_ops.retrieval import CompiledIndexes, build_play_context, load_indexes
from tests.eval._scoring import failed_signals, score_brief


@pytest.fixture(scope="module")
def indexes() -> CompiledIndexes:
    return load_indexes()


def _run_case(
    case: dict[str, Any],
    indexes: CompiledIndexes,
    forbidden_phrases: list[str],
    force_stub: bool,
) -> tuple[str, list[str], dict[str, Any]]:
    """Execute one case and return (brief_text, source_citations, signals_dict)."""
    ctx = build_play_context(case["play_slug"], indexes)
    readiness = case.get("roster_readiness")

    if force_stub:
        # Scrub the key for the duration of this call — build_brief reads
        # it at call time, not at import, so a local pop + restore is safe.
        original = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            result = build_brief(ctx, readiness)
        finally:
            if original is not None:
                os.environ["ANTHROPIC_API_KEY"] = original
    else:
        result = build_brief(ctx, readiness)

    bundle_anatomy = sorted({a.region for a in ctx.anatomy})
    bundle_drills = sorted({d.drill_slug for d in ctx.drills})
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


# --- Stub path (always runs) -----------------------------------------------


def _cases_param() -> list[dict[str, Any]]:
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parent.parent.parent / "eval" / "play-brief-cases.jsonl"
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


_CASES = _cases_param()


@pytest.mark.parametrize("case", _CASES, ids=[c["case_id"] for c in _CASES])
def test_play_brief_stub(
    case: dict[str, Any],
    indexes: CompiledIndexes,
    forbidden_phrases: list[str],
) -> None:
    """Stub-path eval — deterministic, offline, always runs."""
    _, _, signals = _run_case(case, indexes, forbidden_phrases, force_stub=True)
    _assert_pass(case, signals, mode="stub")


# --- Live path (opt-in) ----------------------------------------------------


_LIVE_ENABLED = os.environ.get("RUN_LIVE_EVAL") == "1" and bool(
    os.environ.get("ANTHROPIC_API_KEY")
)


@pytest.mark.skipif(
    not _LIVE_ENABLED,
    reason="live eval requires RUN_LIVE_EVAL=1 and ANTHROPIC_API_KEY",
)
@pytest.mark.parametrize("case", _CASES, ids=[c["case_id"] for c in _CASES])
def test_play_brief_live(
    case: dict[str, Any],
    indexes: CompiledIndexes,
    forbidden_phrases: list[str],
) -> None:
    """Live Claude-backed eval — tracks regressions in synthesized prose."""
    _, _, signals = _run_case(case, indexes, forbidden_phrases, force_stub=False)
    _assert_pass(case, signals, mode="live")
