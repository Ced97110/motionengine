"""Unit tests for type-aware + screen-aware path synthesis.

Covers :func:`motion.services.play_extractor._synthesize_action_paths`:
  1. Cut with no screen sibling → gentle arc (cubic ``C`` command).
  2. Cut WITH a screener on the straight line → curves around, control point
     on the opposite side of the line.
  3. Pass (``arrow`` + ``dashed=True``) → straight line.
  4. Screen action → line stops :data:`SCREEN_STOP_BACK` short of the target.
  5. Dribble / handoff / shot → straight lines (viewer overlays the texture).
"""

from __future__ import annotations

import math
import re

import pytest

from motion.services.play_extractor import (
    CURVE_BOW,
    SCREEN_STOP_BACK,
    _synthesize_action_paths,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_NUM = r"-?\d+(?:\.\d+)?"


def _parse_straight(path: str) -> tuple[tuple[float, float], tuple[float, float]]:
    """Parse ``M x0 y0 L x1 y1`` → ((x0, y0), (x1, y1))."""
    m = re.fullmatch(
        rf"M\s+({_NUM})\s+({_NUM})\s+L\s+({_NUM})\s+({_NUM})", path.strip()
    )
    assert m is not None, f"expected straight-line path, got: {path!r}"
    x0, y0, x1, y1 = (float(m.group(i)) for i in range(1, 5))
    return (x0, y0), (x1, y1)


def _parse_cubic(
    path: str,
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    """Parse ``M x0 y0 C cx cy cx cy x1 y1`` → (start, control, end)."""
    m = re.fullmatch(
        rf"M\s+({_NUM})\s+({_NUM})\s+"
        rf"C\s+({_NUM})\s+({_NUM})\s+({_NUM})\s+({_NUM})\s+"
        rf"({_NUM})\s+({_NUM})",
        path.strip(),
    )
    assert m is not None, f"expected cubic path, got: {path!r}"
    nums = [float(m.group(i)) for i in range(1, 9)]
    return (nums[0], nums[1]), (nums[2], nums[3]), (nums[6], nums[7])


def _signed_side(
    p: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float],
) -> float:
    """Return sign of the 2D cross product (b-a) x (p-a)."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_cut_without_screen_emits_gentle_arc() -> None:
    """``arrow`` cut with no sibling ``screen`` → cubic bezier (gentle arc)."""
    play = {
        "players": {
            "1": [0, 33],
            "2": [-18, 22],
            "3": [18, 22],
            "4": [8, 29],
            "5": [-8, 29],
        },
        "phases": [
            {
                "label": "Phase 1",
                "actions": [
                    {"marker": "arrow", "path": "", "move": {"id": "2", "to": [18, 22]}},
                ],
            }
        ],
    }
    _synthesize_action_paths(play)
    path = play["phases"][0]["actions"][0]["path"]
    assert "C" in path, f"expected cubic arc, got: {path!r}"
    start, _control, end = _parse_cubic(path)
    assert start == (-18.0, 22.0)
    assert end == (18.0, 22.0)


def test_cut_with_screener_curves_around_it() -> None:
    """Cut using a screen → control peaks BEYOND the screener (same side).

    Setup: player 2 cuts from (-18, 22) → (18, 22). Player 4 (screener) sits
    at (8, 24) — 2 units above y=22, within :data:`SCREEN_PROXIMITY = 4.0`.
    Basketball convention: the cutter goes AROUND the screener on the far
    side (e.g. "over the top"), so the curve peaks ABOVE the screener, not
    between screener and line. Control point must therefore sit on the SAME
    side of the line as the screener, roughly ``CURVE_BOW`` units past it.
    """
    play = {
        "players": {
            "1": [0, 33],
            "2": [-18, 22],
            "3": [18, 22],
            "4": [8, 24],  # screener — 2 units above the cut line
            "5": [-8, 29],
        },
        "phases": [
            {
                "label": "Phase 1",
                "actions": [
                    {"marker": "arrow", "path": "", "move": {"id": "2", "to": [18, 22]}},
                    {"marker": "screen", "path": "", "move": {"id": "4", "to": [-18, 22]}},
                ],
            }
        ],
    }
    _synthesize_action_paths(play)
    cut_path = play["phases"][0]["actions"][0]["path"]
    assert "C" in cut_path
    start, control, end = _parse_cubic(cut_path)
    screener = (8.0, 24.0)
    side_screener = _signed_side(screener, start, end)
    side_control = _signed_side(control, start, end)
    assert side_screener != 0.0
    assert side_control != 0.0
    assert side_screener * side_control > 0, (
        f"control must be on SAME side as screener (curve routes AROUND "
        f"it, not between it and the line); screener side={side_screener}, "
        f"control side={side_control}, control={control}"
    )
    # Control point should be roughly `CURVE_BOW` units from the screener.
    dist_ctrl_screener = math.hypot(control[0] - screener[0], control[1] - screener[1])
    assert abs(dist_ctrl_screener - CURVE_BOW) < 0.5


def test_pass_remains_straight() -> None:
    """``arrow`` + ``dashed=True`` is a pass — must stay a straight line."""
    play = {
        "players": {"1": [0, 33], "2": [-18, 22]},
        "phases": [
            {
                "label": "Phase 1",
                "actions": [
                    {
                        "marker": "arrow",
                        "dashed": True,
                        "path": "",
                        "move": {"id": "1", "to": [-18, 22]},
                    },
                ],
            }
        ],
    }
    _synthesize_action_paths(play)
    path = play["phases"][0]["actions"][0]["path"]
    assert "C" not in path
    start, end = _parse_straight(path)
    assert start == (0.0, 33.0)
    assert end == (-18.0, 22.0)


def test_screen_stops_short_of_target() -> None:
    """``screen`` marker emits a line that ends ~SCREEN_STOP_BACK short."""
    play = {
        "players": {"4": [0, 0], "2": [10, 0]},  # distance 10 along +x.
        "phases": [
            {
                "label": "Phase 1",
                "actions": [
                    {"marker": "screen", "path": "", "move": {"id": "4", "to": [10, 0]}},
                ],
            }
        ],
    }
    _synthesize_action_paths(play)
    path = play["phases"][0]["actions"][0]["path"]
    assert "C" not in path
    start, end = _parse_straight(path)
    assert start == (0.0, 0.0)
    # Endpoint should sit `SCREEN_STOP_BACK` units before the target (10, 0).
    dist_to_target = math.hypot(10.0 - end[0], 0.0 - end[1])
    assert abs(dist_to_target - SCREEN_STOP_BACK) < 0.01


def test_screen_shorter_than_stop_back_emits_full_line() -> None:
    """If the screen distance is shorter than the stop-back, emit the full line."""
    play = {
        "players": {"4": [0, 0], "2": [1, 0]},  # distance 1 < SCREEN_STOP_BACK.
        "phases": [
            {
                "label": "Phase 1",
                "actions": [
                    {"marker": "screen", "path": "", "move": {"id": "4", "to": [1, 0]}},
                ],
            }
        ],
    }
    _synthesize_action_paths(play)
    path = play["phases"][0]["actions"][0]["path"]
    start, end = _parse_straight(path)
    assert start == (0.0, 0.0)
    assert end == (1.0, 0.0)


@pytest.mark.parametrize("marker", ["dribble", "handoff", "shot"])
def test_other_markers_remain_straight(marker: str) -> None:
    """``dribble`` / ``handoff`` / ``shot`` stay straight — viewer overlays the rest."""
    play = {
        "players": {"1": [0, 33], "2": [10, 20]},
        "phases": [
            {
                "label": "Phase 1",
                "actions": [
                    {"marker": marker, "path": "", "move": {"id": "1", "to": [10, 20]}},
                ],
            }
        ],
    }
    _synthesize_action_paths(play)
    path = play["phases"][0]["actions"][0]["path"]
    assert "C" not in path
    start, end = _parse_straight(path)
    assert start == (0.0, 33.0)
    assert end == (10.0, 20.0)


def test_authored_path_preserved_and_position_advanced() -> None:
    """User-authored (non-empty) paths are kept verbatim but still advance state."""
    play = {
        "players": {"2": [-18, 22]},
        "phases": [
            {
                "label": "Phase 1",
                "actions": [
                    {
                        "marker": "arrow",
                        "path": "M -18 22 Q 0 30 18 22",  # authored — do not clobber.
                        "move": {"id": "2", "to": [18, 22]},
                    },
                    {
                        "marker": "arrow",
                        "path": "",
                        "move": {"id": "2", "to": [22, 5]},  # chains from (18, 22).
                    },
                ],
            }
        ],
    }
    _synthesize_action_paths(play)
    first, second = play["phases"][0]["actions"]
    assert first["path"] == "M -18 22 Q 0 30 18 22"
    # Second action must have started from the first action's endpoint.
    assert "C" in second["path"]
    start, _control, end = _parse_cubic(second["path"])
    assert start == (18.0, 22.0)
    assert end == (22.0, 5.0)
