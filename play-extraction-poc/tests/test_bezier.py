"""Unit tests for Bézier path generation."""
from __future__ import annotations

import math

import pytest

from src.bezier import BASKET, MOVEMENT_STYLE, generate_path


def test_screen_is_linear():
    path = generate_path((0, 10), (5, 10), "screen")
    assert path.startswith("M0 10 L")
    assert "C" not in path and "Q" not in path


def test_pass_uses_quadratic():
    path = generate_path((0, 30), (10, 30), "pass")
    assert "Q" in path
    assert path.startswith("M0 30")


def test_cut_uses_cubic():
    path = generate_path((0, 32), (-8, 24), "cut")
    assert "C" in path
    assert path.startswith("M0 32")


def test_cut_curves_toward_basket():
    """Cubic control points should be pulled toward the basket at y=5.25."""
    # Movement from top of key to right wing: CP1.y should be south of the
    # direct midpoint (pulled toward the basket at y=5.25).
    path = generate_path((0, 32), (16, 26), "cut")
    after_m = path.replace("M0 32 C", "")
    parts = after_m.split()
    cp1 = (float(parts[0]), float(parts[1]))
    direct_mid_y = (32 + 26) / 2  # = 29
    assert cp1[1] < direct_mid_y


def test_no_nan_or_inf_for_zero_length_cut():
    """A zero-length segment must still produce finite numbers."""
    path = generate_path((0, 0), (0, 0), "cut")
    tokens = (
        path.replace("M", " ")
            .replace("C", " ")
            .replace("L", " ")
            .replace("Q", " ")
            .split()
    )
    for t in tokens:
        try:
            v = float(t)
        except ValueError:
            continue
        assert not math.isnan(v) and not math.isinf(v)


def test_all_movement_types_accepted():
    for mt in ["cut", "pass", "screen"]:
        assert generate_path((0, 0), (10, 10), mt)


def test_unknown_movement_type_raises():
    with pytest.raises(ValueError):
        generate_path((0, 0), (1, 1), "teleport")  # type: ignore[arg-type]


def test_style_mapping_matches_spec():
    # Cut: solid charcoal, arrow
    assert MOVEMENT_STYLE["cut"] == {"dashed": False, "color": "rgba(51,51,51,1)", "marker": "arrow"}
    # Pass: dashed warm orange, arrow
    assert MOVEMENT_STYLE["pass"] == {"dashed": True, "color": "#d4722b", "marker": "arrow"}
    # Screen: solid charcoal, screen-bar
    assert MOVEMENT_STYLE["screen"] == {"dashed": False, "color": "rgba(51,51,51,1)", "marker": "screen-bar"}


def test_basket_constant():
    assert BASKET == (0.0, 5.25)
