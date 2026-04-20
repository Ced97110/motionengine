"""Eval harness for the cross-ref anatomy chain (edge #1).

Loads the compiled JSON indexes via ``motion.wiki_ops.retrieval`` and runs
each case in ``backend/eval/crossref-anatomy.jsonl`` through the Q-A /
Q-B / Q-C retrieval patterns from ``spec/crossref-anatomy-chain.md`` §7.

Scoring:
- ``expected_chunk_ids`` must all appear in the retrieval result.
- ``forbidden_chunks`` must never appear.
- Extra chunks beyond ``expected`` are neutral — the retrieval is a
  superset that the Engine ranks downstream.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from motion.wiki_ops.paths import backend_root
from motion.wiki_ops.retrieval import (
    CompiledIndexes,
    build_drill_justification,
    build_play_context,
    build_readiness_filter,
    load_indexes,
)


def _load_cases() -> list[dict[str, Any]]:
    path = backend_root() / "eval" / "crossref-anatomy.jsonl"
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def _qa_result(indexes: CompiledIndexes, play_slug: str) -> set[str]:
    ctx = build_play_context(play_slug, indexes)
    result: set[str] = {a.concept_slug for a in ctx.anatomy}
    result.update(d.drill_slug for d in ctx.drills)
    return result


def _qb_result(indexes: CompiledIndexes, flagged: list[str]) -> set[str]:
    bundle = build_readiness_filter(flagged, indexes)
    return set(bundle.safe_plays) | {d.drill_slug for d in bundle.prescription_drills}


def _qc_result(indexes: CompiledIndexes, drill_slug: str) -> set[str]:
    return set(build_drill_justification(drill_slug, indexes))


@pytest.fixture(scope="module")
def indexes() -> CompiledIndexes:
    return load_indexes()


_CASES = _load_cases()


@pytest.mark.parametrize("case", _CASES, ids=[c["case_id"] for c in _CASES])
def test_crossref_eval_case(indexes: CompiledIndexes, case: dict[str, Any]) -> None:
    query_type = case["query_type"]
    input_spec = case["input"]
    if query_type == "Q-A":
        result = _qa_result(indexes, input_spec["play_slug"])
    elif query_type == "Q-B":
        result = _qb_result(indexes, input_spec["flagged_regions"])
    elif query_type == "Q-C":
        result = _qc_result(indexes, input_spec["drill_slug"])
    else:
        pytest.fail(f"Unknown query_type: {query_type}")

    expected = set(case["expected_chunk_ids"])
    forbidden = set(case["forbidden_chunks"])
    missing = expected - result
    illegal = forbidden & result
    assert not missing, (
        f"{case['case_id']}: missing expected chunks {missing}; got {sorted(result)}"
    )
    assert not illegal, (
        f"{case['case_id']}: forbidden chunks present {illegal}; got {sorted(result)}"
    )
