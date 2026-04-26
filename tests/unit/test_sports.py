"""Sport primitive contract tests.

Locks the supported-sport list, default fallback, and validator behavior
so a future sport addition doesn't accidentally regress the contract.
"""
from __future__ import annotations

from motion.sports import DEFAULT_SPORT, SUPPORTED_SPORTS, is_valid_sport


def test_default_sport_is_basketball() -> None:
    """Backward-compat invariant — pre-Step-1 callers behave identically."""
    assert DEFAULT_SPORT == "basketball"


def test_supported_sports_includes_basketball_and_football() -> None:
    assert "basketball" in SUPPORTED_SPORTS
    assert "football" in SUPPORTED_SPORTS


def test_default_sport_is_in_supported_sports() -> None:
    assert DEFAULT_SPORT in SUPPORTED_SPORTS


def test_is_valid_sport_accepts_supported() -> None:
    for sport in SUPPORTED_SPORTS:
        assert is_valid_sport(sport)


def test_is_valid_sport_rejects_unknown() -> None:
    assert not is_valid_sport("hockey")
    assert not is_valid_sport("BASKETBALL")  # case-sensitive on purpose
    assert not is_valid_sport("")
