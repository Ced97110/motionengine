"""Halftime adjustment generation — observation chips + partial box → 3 bullets."""

import json
from .game_report import get_calibration


CHIP_MAP = {
    'their_3_is_hot': "Opponent is hitting three-pointers at a high rate",
    'their_3_is_cold': "Opponent is missing three-pointers",
    'our_pnr_working': "Our pick-and-roll action is generating good looks",
    'our_pnr_not_working': "Our pick-and-roll is being defended well",
    'foul_trouble': "Key player(s) in foul trouble",
    'their_post_dominant': "Their post player is dominating inside",
    'our_fast_break': "We are scoring in transition",
    'turnovers_killing_us': "Too many turnovers — giving away possessions",
    'rebounding_edge': "We have a rebounding advantage",
    'rebounding_problem': "They are out-rebounding us significantly",
    'energy_low': "Team energy and effort is down",
    'defense_solid': "Our defense is holding up well",
}


def build_halftime_prompt(
    observations: list,
    partial_box: dict,
    game_plan: dict,
    level: str,
) -> str:
    """Build Claude prompt for halftime adjustment generation."""
    cal = get_calibration(level)
    obs_text = "\n".join([f"- {CHIP_MAP.get(o, o)}" for o in observations])

    prompt = f"""You are a basketball coaching assistant generating halftime adjustments.

LEVEL: {level}
HALF-TIME STATS: {json.dumps(partial_box)}
COACH'S OBSERVATIONS:
{obs_text}

Generate exactly 3 bullet-point adjustments. Each must be:
1. Specific and actionable (not "play better defense" but "switch to zone on their PG to take away the drive")
2. Directly responsive to at least one observation
3. Expressed in 1-2 sentences maximum

Calibrate to {level} level — use appropriate terminology and complexity.

Format:
- [Adjustment 1]
- [Adjustment 2]
- [Adjustment 3]"""
    return prompt


__all__ = ['build_halftime_prompt', 'CHIP_MAP']
