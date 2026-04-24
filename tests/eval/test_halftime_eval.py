"""Eval harness for the halftime endpoint (``POST /api/halftime``).

Halftime composition lives in TypeScript (``frontend/src/app/api/halftime``).
To score it from Python we hit the live endpoint on the frontend dev server.
That mirrors the production call path — the endpoint owns both stub and
Claude modes and returns a ``source: "stub" | "claude"`` field. If the dev
server is not reachable, the tests skip with a clear reason.

Each case in ``eval/halftime-cases.jsonl`` carries a request body and the
halftime rubric (exactly 3 bullets, bullet-length band, no verbatim book
prose, at least one must-contain token).

Environment:

- ``HALFTIME_URL`` (optional) — overrides the default
  ``http://localhost:3000/api/halftime`` target.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import httpx
import pytest

from tests.eval._scoring import failed_signals, score_halftime

_DEFAULT_URL = "http://localhost:3000/api/halftime"
_REQUEST_TIMEOUT = 30.0  # live Claude calls can take 8-15s


def _cases() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parent.parent.parent / "eval" / "halftime-cases.jsonl"
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _target_url() -> str:
    return os.environ.get("HALFTIME_URL", _DEFAULT_URL)


def _endpoint_reachable() -> bool:
    """Check whether the halftime endpoint is reachable. A short HEAD request
    is not supported (405), so we try a lightweight GET on the dev server root
    and accept any HTTP response as proof-of-life."""
    try:
        root = _target_url().rsplit("/api/", 1)[0] or _target_url()
        httpx.get(root, timeout=2.0)
        return True
    except (httpx.RequestError, httpx.TimeoutException):
        return False


_REACHABLE = _endpoint_reachable()
_CASES = _cases()


@pytest.mark.skipif(
    not _REACHABLE,
    reason=(
        "frontend dev server not reachable — start `cd frontend && npm run dev` "
        f"or set HALFTIME_URL. Default target: {_DEFAULT_URL}"
    ),
)
@pytest.mark.parametrize("case", _CASES, ids=[c["case_id"] for c in _CASES])
def test_halftime_eval(case: dict[str, Any], forbidden_phrases: list[str]) -> None:
    body: dict[str, Any] = {
        "observations": case["observations"],
        "level": case["level"],
    }
    if case.get("partial_box") is not None:
        body["partial_box"] = case["partial_box"]

    with httpx.Client(timeout=_REQUEST_TIMEOUT) as client:
        resp = client.post(_target_url(), json=body)

    assert resp.status_code == 200, (
        f"{case['case_id']}: HTTP {resp.status_code} — body={resp.text[:200]}"
    )
    payload = resp.json()
    assert "bullets" in payload, f"{case['case_id']}: no bullets in response: {payload!r}"
    bullets = payload["bullets"]

    signals = score_halftime(
        bullets=bullets,
        case=case,
        forbidden_phrases=forbidden_phrases,
    )
    failed = failed_signals(signals)
    if failed:
        detail = "\n".join(f"  {name}: {signals[name]['detail']}" for name in failed)
        bullets_str = "\n".join(f"    {i+1}. {b}" for i, b in enumerate(bullets))
        source = payload.get("source", "?")
        pytest.fail(
            f"[{source}] case {case['case_id']} failed signals {failed}:\n"
            f"{detail}\nbullets:\n{bullets_str}"
        )
