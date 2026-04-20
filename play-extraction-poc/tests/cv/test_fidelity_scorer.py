"""Unit tests for the CV fidelity scorer.

The scorer is load-bearing for every future eval case, so every behavior it
encodes — weight distribution, tolerance boundary, partial-credit via, greedy
matching, spurious-actual reporting — gets a dedicated test here.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.cv.fidelity import (
    ActualMovement,
    ExpectedMovement,
    FidelityReport,
    expected_from_case,
    load_actual_yaml,
    load_cases,
    score_case,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _pass(player: str, to_player: str) -> ExpectedMovement:
    return ExpectedMovement(player=player, type="pass", to_player=to_player)


def _actual_pass(player: str, to_player: str) -> ActualMovement:
    return ActualMovement(player=player, type="pass", to_player=to_player)


def _spatial(
    player: str, type_: str, to: tuple[float, float],
    via: tuple[float, float] | None = None,
) -> ExpectedMovement:
    return ExpectedMovement(player=player, type=type_, to_svg=to, via_svg=via)


def _actual_spatial(
    player: str, type_: str, to: tuple[float, float],
    via: tuple[float, float] | None = None,
) -> ActualMovement:
    return ActualMovement(player=player, type=type_, to_svg=to, via_svg=via)


# ---------------------------------------------------------------------------
# Exact-match baselines
# ---------------------------------------------------------------------------


def test_all_correct_scores_perfect() -> None:
    expected = [_pass("1", "2"), _spatial("5", "cut", (2, 13))]
    actual = [_actual_pass("1", "2"), _actual_spatial("5", "cut", (2, 13))]
    r = score_case(expected, actual)
    assert r.matched_count == 2
    assert r.precision == 1.0
    assert r.recall == 1.0
    assert r.f1 == 1.0
    assert r.unmatched_actuals == ()


def test_empty_actuals_gives_zero() -> None:
    expected = [_pass("1", "2")]
    r = score_case(expected, [])
    assert r.matched_count == 0
    assert r.precision == 0.0
    assert r.recall == 0.0
    assert r.f1 == 0.0


def test_empty_expected_gives_zero() -> None:
    actual = [_actual_pass("1", "2")]
    r = score_case([], actual)
    assert r.expected_total == 0
    assert r.f1 == 0.0
    # All actuals are spurious (unmatched)
    assert r.unmatched_actuals == (0,)


# ---------------------------------------------------------------------------
# Player / type gating
# ---------------------------------------------------------------------------


def test_player_mismatch_zeroes_movement() -> None:
    expected = [_pass("1", "2")]
    actual = [_actual_pass("3", "2")]
    r = score_case(expected, actual)
    assert r.matched_count == 0
    assert r.matches[0].score == 0.0
    assert r.unmatched_actuals == (0,)


def test_type_mismatch_zeroes_movement() -> None:
    expected = [_spatial("5", "cut", (2, 13))]
    actual = [_actual_spatial("5", "dribble", (2, 13))]
    r = score_case(expected, actual)
    assert r.matched_count == 0
    assert r.matches[0].score == 0.0


def test_to_player_mismatch_partial_credit() -> None:
    """Passes with wrong receiver still earn player+type credit but don't
    count toward matched_count (fall under the player+type gate threshold
    is exactly met, so the greedy matcher accepts — but aggregate score is
    below 1.0)."""
    expected = [_pass("1", "2")]
    actual = [_actual_pass("1", "3")]
    r = score_case(expected, actual)
    # player (0.25) + type (0.25) = 0.50, no to_player credit
    assert r.matches[0].score == pytest.approx(0.50)
    assert r.matches[0].actual_index == 0
    assert "to_player_mismatch" in r.matches[0].notes[0]


# ---------------------------------------------------------------------------
# Spatial tolerance boundary
# ---------------------------------------------------------------------------


def test_to_svg_within_tolerance_full_credit() -> None:
    expected = [_spatial("5", "cut", (2, 13))]
    actual = [_actual_spatial("5", "cut", (3.5, 14.5))]  # dist ≈ 2.12
    r = score_case(expected, actual, svg_tolerance=3.0)
    assert r.matches[0].score == pytest.approx(1.0)


def test_to_svg_outside_tolerance_partial_only() -> None:
    expected = [_spatial("5", "cut", (2, 13))]
    actual = [_actual_spatial("5", "cut", (10, 13))]  # dist = 8
    r = score_case(expected, actual, svg_tolerance=3.0)
    # player + type only: 0.50
    assert r.matches[0].score == pytest.approx(0.50)


def test_tolerance_boundary_is_inclusive() -> None:
    """A point exactly at the tolerance distance counts as within tolerance."""
    expected = [_spatial("5", "cut", (0, 0))]
    actual = [_actual_spatial("5", "cut", (3.0, 0))]  # dist = 3.0
    r = score_case(expected, actual, svg_tolerance=3.0)
    assert r.matches[0].score == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# via waypoint — partial credit
# ---------------------------------------------------------------------------


def test_via_bonus_applied_when_correct() -> None:
    expected = [_spatial("2", "dribble", to=(-5, 5), via=(-14, 22))]
    actual = [_actual_spatial("2", "dribble", to=(-5, 5), via=(-14, 22))]
    r = score_case(expected, actual, svg_tolerance=3.0)
    # player 0.25 + type 0.25 + to 0.50 + via bonus 0.25 = 1.25 (capped at 1.0 in aggregate)
    assert r.matches[0].score == pytest.approx(1.25)
    # But aggregate caps at 1.0 per movement:
    assert r.aggregate_score == pytest.approx(1.0)


def test_via_missing_does_not_zero_movement() -> None:
    expected = [_spatial("2", "dribble", to=(-5, 5), via=(-14, 22))]
    actual = [_actual_spatial("2", "dribble", to=(-5, 5))]  # no via
    r = score_case(expected, actual, svg_tolerance=3.0)
    assert r.matches[0].score == pytest.approx(1.0)  # no bonus, but full base credit
    assert "via_missing_in_actual" in r.matches[0].notes


def test_via_out_of_tolerance_is_noted_not_credited() -> None:
    expected = [_spatial("2", "dribble", to=(-5, 5), via=(-14, 22))]
    actual = [_actual_spatial("2", "dribble", to=(-5, 5), via=(0, 0))]
    r = score_case(expected, actual, svg_tolerance=3.0)
    assert r.matches[0].score == pytest.approx(1.0)  # no bonus
    assert any("via_out_of_tolerance" in n for n in r.matches[0].notes)


# ---------------------------------------------------------------------------
# Greedy matching and spurious actuals
# ---------------------------------------------------------------------------


def test_spurious_actuals_are_reported() -> None:
    expected = [_pass("1", "2")]
    actual = [
        _actual_pass("1", "2"),
        _actual_spatial("3", "cut", (5, 5)),   # spurious
        _actual_pass("4", "3"),                # spurious
    ]
    r = score_case(expected, actual)
    assert r.matched_count == 1
    assert set(r.unmatched_actuals) == {1, 2}
    # F1 reflects the spurious actuals (precision < 1.0)
    assert r.precision == pytest.approx(1 / 3)
    assert r.recall == pytest.approx(1.0)


def test_each_actual_matches_at_most_once() -> None:
    """Two expecteds that both prefer actual[0] — only one wins; the other is unmatched."""
    expected = [_pass("1", "2"), _pass("1", "2")]  # identical expecteds
    actual = [_actual_pass("1", "2")]
    r = score_case(expected, actual)
    # One expected matches, one stays unmatched.
    assert r.matched_count == 1
    assert sum(1 for m in r.matches if m.actual_index is None) == 1


def test_greedy_picks_best_score_for_expected() -> None:
    """When multiple actuals could match, the greedy matcher picks the highest-scoring."""
    expected = [_spatial("5", "cut", to=(2, 13))]
    actual = [
        _actual_spatial("5", "cut", to=(10, 13)),  # wrong pos, partial credit only
        _actual_spatial("5", "cut", to=(2, 13)),   # exact, full credit
    ]
    r = score_case(expected, actual, svg_tolerance=3.0)
    assert r.matches[0].actual_index == 1
    assert r.matches[0].score == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Aggregate metrics
# ---------------------------------------------------------------------------


def test_f1_with_partial_credit() -> None:
    """Mix of exact matches, partial credit, and one miss."""
    expected = [
        _pass("1", "2"),               # exact → 1.0
        _pass("2", "3"),               # wrong receiver → 0.5
        _spatial("5", "cut", (2, 13)), # miss (no actual) → 0.0
    ]
    actual = [
        _actual_pass("1", "2"),
        _actual_pass("2", "9"),  # wrong receiver
    ]
    r = score_case(expected, actual)
    # aggregate: 1.0 + 0.5 + 0.0 = 1.5
    # precision = 1.5 / 2 = 0.75
    # recall    = 1.5 / 3 = 0.50
    # F1 = 2 * 0.75 * 0.50 / 1.25 = 0.60
    assert r.precision == pytest.approx(0.75)
    assert r.recall == pytest.approx(0.50)
    assert r.f1 == pytest.approx(0.60)


# ---------------------------------------------------------------------------
# YAML + case loading
# ---------------------------------------------------------------------------


def test_load_actual_yaml_strips_fence_and_parses_movements(tmp_path: Path) -> None:
    yaml_text = """```yaml
play:
  name: Black
  tag: 5-out
  players:
    "1": [0.0, 30.8]
    "2": [-17.8, 20.8]
  ball_start: "1"
  phases:
    - label: "Phase 1"
      description: "1 passes to 2."
      movements:
        - player: "1"
          from: [0.0, 30.8]
          to_player: "2"
          to: [-17.8, 20.8]
          type: pass
          confidence: high
    - label: "Phase 2"
      description: "5 cuts."
      movements:
        - player: "5"
          from: [22.5, 6.4]
          to: [2.0, 13.0]
          type: cut
          confidence: high
```
"""
    path = tmp_path / "extraction.yaml"
    path.write_text(yaml_text, encoding="utf-8")

    movements = load_actual_yaml(path)
    assert len(movements) == 2
    assert movements[0].player == "1"
    assert movements[0].type == "pass"
    assert movements[0].to_player == "2"
    assert movements[0].to_svg == (-17.8, 20.8)
    assert movements[1].player == "5"
    assert movements[1].type == "cut"
    assert movements[1].to_svg == (2.0, 13.0)


def test_load_cases_parses_jsonl(tmp_path: Path) -> None:
    cases_text = (
        '{"case_id":"a","page":1,"panel":0,"expected":{"movements":[]}}\n'
        '# a comment line\n'
        '\n'
        '{"case_id":"b","page":2,"panel":1,"expected":{"movements":[]}}\n'
    )
    path = tmp_path / "cases.jsonl"
    path.write_text(cases_text, encoding="utf-8")

    cases = load_cases(path)
    assert [c["case_id"] for c in cases] == ["a", "b"]


def test_expected_from_case_builds_movements() -> None:
    case = {
        "expected": {
            "movements": [
                {"player": "1", "type": "pass", "to_player": "2"},
                {"player": "5", "type": "cut", "from": [22, 4], "to": [2, 13]},
                {"player": "2", "type": "dribble",
                 "from": [-16, 26], "to": [-5, 5], "via": [-14, 22]},
            ]
        }
    }
    movements = expected_from_case(case)
    assert len(movements) == 3
    assert movements[0].to_player == "2"
    assert movements[1].to_svg == (2, 13)
    assert movements[2].via_svg == (-14, 22)


# ---------------------------------------------------------------------------
# Report formatting (smoke)
# ---------------------------------------------------------------------------


def test_report_properties_survive_all_miss() -> None:
    expected = [_pass("1", "2"), _pass("3", "4")]
    r = score_case(expected, [])
    assert r.matched_count == 0
    assert r.aggregate_score == 0.0
    assert r.precision == 0.0
    assert r.recall == 0.0
    assert r.f1 == 0.0


def test_report_has_case_id_default_empty() -> None:
    r = score_case([_pass("1", "2")], [_actual_pass("1", "2")])
    assert isinstance(r, FidelityReport)
    assert r.case_id == ""  # set by the caller, not the scorer
