"""Deterministic Bézier path generation for movement types.

The LLM outputs only endpoints (from_pt, to_pt, movement_type). This module
produces the SVG path string. No LLM calls. Pure math.
"""
from __future__ import annotations

from typing import Literal, Tuple

Point = Tuple[float, float]
MovementType = Literal["cut", "pass", "screen"]

BASKET: Point = (0.0, 5.25)

PASS_PERP_OFFSET = 0.08
CUT_BASKET_PULL = 0.15


def generate_path(from_pt: Point, to_pt: Point, movement_type: MovementType) -> str:
    """Generate an SVG path d-attribute for a movement.

    Args:
        from_pt: start (x, y) in SVG units.
        to_pt: end (x, y) in SVG units.
        movement_type: one of "cut", "pass", "screen".

    Returns:
        SVG path string, e.g. "M0 32 C5 28 10 22 16 26".
    """
    x1, y1 = from_pt
    x2, y2 = to_pt
    dx = x2 - x1
    dy = y2 - y1

    if movement_type == "screen":
        return f"M{x1} {y1} L{x2} {y2}"

    if movement_type == "pass":
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        perp_x = -dy * PASS_PERP_OFFSET
        perp_y = dx * PASS_PERP_OFFSET
        return f"M{x1} {y1} Q{mx + perp_x} {my + perp_y} {x2} {y2}"

    if movement_type == "cut":
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        pull_x = (BASKET[0] - mx) * CUT_BASKET_PULL
        pull_y = (BASKET[1] - my) * CUT_BASKET_PULL
        cp1x = x1 + dx * 0.33 + pull_x
        cp1y = y1 + dy * 0.33 + pull_y
        cp2x = x1 + dx * 0.66 + pull_x
        cp2y = y1 + dy * 0.66 + pull_y
        return f"M{x1} {y1} C{cp1x} {cp1y} {cp2x} {cp2y} {x2} {y2}"

    raise ValueError(f"Unknown movement_type: {movement_type!r}")


MOVEMENT_STYLE = {
    "cut":    {"dashed": False, "color": "rgba(51,51,51,1)", "marker": "arrow"},
    "pass":   {"dashed": True,  "color": "#d4722b",          "marker": "arrow"},
    "screen": {"dashed": False, "color": "rgba(51,51,51,1)", "marker": "screen-bar"},
}
