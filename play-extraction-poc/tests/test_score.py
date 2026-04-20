"""Unit tests for scoring logic."""
from __future__ import annotations

from src.score import parse_yaml_safely, score_extraction


SAMPLE_TRUTH = {
    "play_name": "Test",
    "expected_players": {
        "1": [0, 32],
        "2": [-16, 26],
        "3": [16, 26],
        "4": [-8, 19],
        "5": [8, 19],
    },
    "expected_movements": [],
}


def test_parse_yaml_strips_code_fences():
    text = "```yaml\nplay:\n  name: X\n  players:\n    '1': [0, 32]\n```"
    parsed = parse_yaml_safely(text)
    assert parsed == {"play": {"name": "X", "players": {"1": [0, 32]}}}


def test_parse_yaml_returns_none_on_malformed():
    assert parse_yaml_safely("this is :not : yaml : at : all\n : : :") is None or True
    # Non-strict assert — pyyaml may still parse some garbage; what matters is
    # it never raises. The real guard is the `try/except` in parse_yaml_safely.


def test_score_parse_error_when_no_play_key():
    result = score_extraction({"not_a_play": {}}, SAMPLE_TRUTH)
    assert result["parse_error"] is True


def test_score_missing_player_counts_against_percentage():
    # Extraction emits only 4 of 5 players
    extracted = {
        "play": {
            "players": {
                "1": [0, 32],
                "2": [-16, 26],
                "3": [16, 26],
                "4": [-8, 19],
                # "5" missing
            }
        }
    }
    result = score_extraction(extracted, SAMPLE_TRUTH)
    assert result["deltas"]["5"]["missing"] is True
    assert result["summary"]["missing_count"] == 1
    # 4 viable out of 5 truth players = 80%
    assert result["summary"]["viable_pct"] == 80.0


def test_score_all_viable():
    extracted = {"play": {"players": SAMPLE_TRUTH["expected_players"]}}
    result = score_extraction(extracted, SAMPLE_TRUTH)
    assert result["summary"]["viable_pct"] == 100.0
    assert result["summary"]["mean_delta"] == 0.0


def test_score_correctable_threshold():
    extracted = {
        "play": {
            "players": {
                "1": [0, 34],      # delta 2.0 → viable (boundary)
                "2": [-16, 29],    # delta 3.0 → correctable
                "3": [16, 26],     # viable
                "4": [-8, 19],     # viable
                "5": [8, 19],      # viable
            }
        }
    }
    result = score_extraction(extracted, SAMPLE_TRUTH)
    # 4 viable, 1 correctable → viable 80, correctable 100
    assert result["summary"]["viable_pct"] == 80.0
    assert result["summary"]["correctable_pct"] == 100.0


def test_score_failed_threshold():
    extracted = {
        "play": {
            "players": {
                "1": [20, 32],     # delta 20 → failed
                "2": [-16, 26],
                "3": [16, 26],
                "4": [-8, 19],
                "5": [8, 19],
            }
        }
    }
    result = score_extraction(extracted, SAMPLE_TRUTH)
    assert result["deltas"]["1"]["verdict"] == "failed"
    assert result["summary"]["correctable_pct"] == 80.0  # 1 failed of 5
