"""Shared fixtures for Engine-output eval tests.

Loads JSONL case files and the forbidden-phrase blocklist once per session.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from tests.eval._scoring import load_forbidden_phrases

_BACKEND = Path(__file__).resolve().parent.parent.parent


def _load_jsonl(name: str) -> list[dict[str, Any]]:
    path = _BACKEND / "eval" / name
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


@pytest.fixture(scope="session")
def forbidden_phrases() -> list[str]:
    return load_forbidden_phrases()


@pytest.fixture(scope="session")
def play_brief_cases() -> list[dict[str, Any]]:
    return _load_jsonl("play-brief-cases.jsonl")


@pytest.fixture(scope="session")
def halftime_cases() -> list[dict[str, Any]]:
    return _load_jsonl("halftime-cases.jsonl")
