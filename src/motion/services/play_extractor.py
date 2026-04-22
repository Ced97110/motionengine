"""Prose → V7Play extraction via Claude.

Given book prose (overview + numbered instructions + coaching points), returns
a draft V7Play JSON object. Two modes:

- **Claude**: if ``ANTHROPIC_API_KEY`` is set, uses Claude Sonnet 4.6 with a
  strict schema + coordinate-frame prompt.
- **Stub**: if no API key, returns a skeleton with the prose stashed in
  ``desc`` so the UX never dead-ends during local dev.

Intentional non-goals of this service:
- **SVG curve authoring.** Action entries carry ``path: ""``; the user draws
  the curves in the lab after the draft is loaded.
- **Per-phase defender coords.** Defender positions are inferred loosely —
  books rarely track defenders phase-by-phase, so these are best-effort.
- **concepts.related.** Requires knowledge of adjacent plays in the corpus;
  left empty for the user to fill.

Mirrors the pattern in ``motion.services.play_brief``.
"""

from __future__ import annotations

import copy
import json
import math
import os
from dataclasses import dataclass
from typing import Any

_MODEL = "claude-sonnet-4-6"
_MAX_TOKENS = 4096

# ---------------------------------------------------------------------------
# Curve-synthesis geometry constants (type-aware + screen-aware synthesis).
# ---------------------------------------------------------------------------

# SVG units of perpendicular tolerance for treating a screener as "in the way"
# of a cutter's straight line. Anything farther is ignored.
SCREEN_PROXIMITY = 4.0
# Bow depth for cuts that curve around a screener (perpendicular offset from
# the straight line, away from the screener).
CURVE_BOW = 3.5
# Bow depth for ordinary cuts (no screener nearby) — a gentle arc biased
# toward the court centerline so cuts don't hug the sideline.
DEFAULT_BOW = 1.5
# For screen markers: how far short of the screenee's coord to stop the line,
# so the T-bar marker renders at the screening point rather than past it.
SCREEN_STOP_BACK = 3.0


@dataclass(frozen=True)
class ExtractionResult:
    play: dict[str, Any]
    todos: list[str]
    source: str  # "claude" | "stub" | "claude-error"


_COORD_HINT = """COORDINATE FRAME:
- Origin at rim; +x points to the right sideline; +y points away from baseline.
- Half-court extends roughly x in [-28, 28], y in [0, 47].
- Top of key: (0, 33). Free-throw line: y ≈ 19. Elbows: (±6, 18).
- Wings (three-point line): (±18, 22). Corners (deep): (±22, 4).
- Low blocks: (±5, 7). Short corners: (±18, 8).

STANDARD FORMATIONS (starting positions):
- "1-4 high":  1:(0,33) 2:(-17,22) 3:(17,22) 4:(-6,18) 5:(6,18)
- "5-out":     1:(0,32) 2:(-17,24) 3:(17,24) 4:(-22,5) 5:(22,5)
- "horns":     1:(0,32) 2:(-22,5)  3:(22,5)  4:(-6,18) 5:(6,18)
- "box":       1:(0,30) 2:(-8,20)  3:(8,20)  4:(-8,8)  5:(8,8)
- "1-3-1":     1:(0,32) 2:(-15,22) 3:(15,22) 4:(-22,5) 5:(0,14)

Defenders (X1-X5) start 2-3 units closer to the rim than their assignment.
"""

_SCHEMA_HINT = """{
  "name": "Play Name",
  "tag": "Short tactical category",
  "desc": "One sentence describing the primary action.",
  "coachNote": "One sentence on why this play works / when to call it.",
  "concepts": {
    "counters": ["defense types this play beats"],
    "bestFor": "personnel description (e.g. mobile 5; shooting threat at 2)",
    "related": []
  },
  "players":  { "1":[x,y], "2":[x,y], "3":[x,y], "4":[x,y], "5":[x,y] },
  "roster":   { "1":{"name":"PG","pos":"PG"}, "2":{...}, ... },
  "defense":  { "X1":[x,y], "X2":[x,y], "X3":[x,y], "X4":[x,y], "X5":[x,y] },
  "ballStart": "1",
  "phases": [
    {
      "label": "3-5 word phase label",
      "text":  "Near-verbatim instruction from the book.",
      "spotlightText": {
        "1": "2nd-person imperative for player 1 this phase.",
        "2": "...", "3": "...", "4": "...", "5": "..."
      },
      "actions": [
        {
          "marker": "arrow|screen|shot|dribble|handoff",
          "path": "",
          "move": { "id": "2", "to": [x,y] }
        }
      ],
      "defenseActions": [
        { "id": "X2", "to": [x,y], "desc": "Plausible defender response." }
      ]
    }
  ],
  "branchPoint": null
}

If a branchPoint is warranted, it MUST have this exact shape — each option's
`phase` is a full phase object, NOT flat fields:

"branchPoint": {
  "prompt": "Read the defense — how is the screen covered?",
  "subprompt": "Watch X5.",
  "options": [
    {
      "label": "Switch", "desc": "X2/X5 switch — slip the roll", "icon": "→",
      "phase": {
        "label": "Slip to Rim",
        "text": "Screener slips hard to the rim as the switch leaves a gap.",
        "spotlightText": { "1": "...", "2": "...", "3": "...", "4": "...", "5": "..." },
        "actions": [ { "marker": "arrow", "path": "", "move": { "id": "5", "to": [2, 3] } } ],
        "defenseActions": [ { "id": "X5", "to": [12, 24], "desc": "Caught on switch" } ]
      }
    },
    {
      "label": "Drop", "desc": "X5 drops — pull-up jumper", "icon": "↗",
      "phase": { ...same shape as above... }
    }
  ]
}"""

_RULES = """RULES:
- phases[].text: keep CLOSE TO VERBATIM from the book instruction; do not
  paraphrase heavily.
- phases[].label: synthesize a short (3-5 word) label.
- phases[].spotlightText: SYNTHESIZE 2nd-person coaching voice per player
  (books do not provide this — you invent it from the instruction).
- phases[].actions[].path: ALWAYS leave as empty string "". The user draws
  curves in the lab.
- phases[].actions[].move: include for player(s) who move this phase;
  `id` is "1"-"5", `to` is end position.
- phases[].actions[].marker: choose based on the book's verb:
  - "dribble" when the ball-handler dribbles along a path ("1 dribbles
    across the top", "zigzag dribble to the wing", "drives baseline",
    "pushes it up the floor"). The mover MUST be the current ball-handler.
  - "handoff" when the book describes a dribble handoff / DHO ("2
    dribble-hands-off to 3", "DHO between 1 and 4"). Emit ONE handoff
    action on the giver; the receiver typically has an accompanying
    "arrow" action cutting to the exchange point.
  - "screen" for on/off-ball screens, "shot" for the shot attempt, and
    "arrow" for plain cuts, passes, and non-dribble movement. Prefer
    "dribble" over "arrow" when the ball is on the mover's hip.
- phases[].defenseActions: invent plausible reactions for the 1-2 most-
  affected defenders per phase. Keep `desc` short.
- If the prose contains "Occasionally...", "If the defense does X...",
  "counter: Y" — structure that as a `branchPoint` with 2 options.
  Otherwise keep `branchPoint: null`.
- concepts.related: leave as [] (fills later from corpus).
- IP rule: if the prose names real NBA players, SCRUB them — use position
  tokens (PG/SG/SF/PF/C) in `roster.name`.
- Output RULE: return ONLY the JSON object, no preamble, no markdown
  code fences.
"""


def _build_prompt(prose: str) -> str:
    return (
        "You are a basketball-play extraction assistant. Given book prose, "
        "produce a V7Play JSON object.\n\n"
        f"{_COORD_HINT}\n"
        f"SCHEMA:\n{_SCHEMA_HINT}\n\n"
        f"{_RULES}\n"
        f"BOOK PROSE:\n{prose}\n\n"
        "Return the V7Play JSON object now."
    )


def _stub_extract(prose: str) -> ExtractionResult:
    return ExtractionResult(
        play={
            "name": "Extracted Play (stub — no API key)",
            "tag": "",
            "desc": prose[:200],
            "coachNote": "",
            "concepts": {"counters": [], "bestFor": "", "related": []},
            "players": {
                "1": [0, 32],
                "2": [-16, 24],
                "3": [16, 24],
                "4": [-20, 6],
                "5": [20, 6],
            },
            "roster": {
                "1": {"name": "PG", "pos": "PG"},
                "2": {"name": "SG", "pos": "SG"},
                "3": {"name": "SF", "pos": "SF"},
                "4": {"name": "PF", "pos": "PF"},
                "5": {"name": "C", "pos": "C"},
            },
            "defense": {
                "X1": [0, 30],
                "X2": [-14, 22],
                "X3": [14, 22],
                "X4": [-18, 8],
                "X5": [18, 8],
            },
            "ballStart": "1",
            "phases": [],
        },
        todos=["No ANTHROPIC_API_KEY set — stub output only. Export the key and retry."],
        source="stub",
    )


def _strip_code_fence(raw: str) -> str:
    if not raw.startswith("```"):
        return raw
    lines = raw.split("\n")
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _sanitize_branch_point(play: dict[str, Any]) -> bool:
    """Strip a malformed ``branchPoint`` so PlayViewerV7 does not crash.

    Returns True if the block was stripped. PlayViewerV7 reads
    ``branchPoint.options[].phase.actions`` — any option missing the nested
    ``phase`` object causes a runtime TypeError. LLMs occasionally emit flat
    options (label/desc/icon at the top level without a nested phase); drop
    the whole branchPoint in that case.
    """
    bp = play.get("branchPoint")
    if bp is None:
        return False
    if not isinstance(bp, dict):
        play["branchPoint"] = None
        return True
    options = bp.get("options")
    if not isinstance(options, list) or not options:
        play["branchPoint"] = None
        return True
    for opt in options:
        if not isinstance(opt, dict):
            play["branchPoint"] = None
            return True
        phase = opt.get("phase")
        if not isinstance(phase, dict) or not isinstance(phase.get("actions"), list):
            play["branchPoint"] = None
            return True
    return False


def _collect_todos(play: dict[str, Any]) -> list[str]:
    todos: list[str] = []
    phases = play.get("phases") or []
    if isinstance(phases, list) and phases:
        phases_with_actions = sum(
            1 for p in phases if isinstance(p, dict) and p.get("actions")
        )
        if phases_with_actions > 0:
            todos.append(
                f"{phases_with_actions} phase(s) have straight-line synthesized "
                "`path` strings — redraw curves in the lab for realistic motion."
            )
        if any(isinstance(p, dict) and p.get("spotlightText") for p in phases):
            todos.append(
                "spotlightText was synthesized (not in the book) — review the "
                "per-player voice and tactical accuracy."
            )
        if any(isinstance(p, dict) and p.get("defenseActions") for p in phases):
            todos.append(
                "defenseActions are inferred — verify defender reactions match "
                "your coaching intent."
            )
    concepts = play.get("concepts") or {}
    if isinstance(concepts, dict) and not concepts.get("related"):
        todos.append(
            "concepts.related is empty — add adjacent plays from your corpus."
        )
    return todos


def _coord_pair(value: Any) -> tuple[float, float] | None:
    """Return ``(x, y)`` as floats if ``value`` looks like a 2-element coord."""
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        return None
    try:
        return float(value[0]), float(value[1])
    except (TypeError, ValueError):
        return None


def _needs_synthesis(path: Any) -> bool:
    """Empty string, missing, or whitespace-only → synthesize."""
    if path is None:
        return True
    if not isinstance(path, str):
        return False
    return path.strip() == ""


def _straight_path(start: tuple[float, float], end: tuple[float, float]) -> str:
    """Emit ``M x0 y0 L x1 y1`` with 2-decimal rounding."""
    x0, y0 = start
    x1, y1 = end
    return f"M {round(x0, 2)} {round(y0, 2)} L {round(x1, 2)} {round(y1, 2)}"


def _point_segment_perp(
    p: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float],
) -> tuple[float, float, float]:
    """Return (perpendicular distance, signed side, segment length).

    Distance is clamped to the segment endpoints (closest point on segment).
    Signed side > 0 if ``p`` is on one side of the a→b line, < 0 on the other
    (follows the 2D cross product sign convention). Length is |b - a|.
    """
    ax, ay = a
    bx, by = b
    px, py = p
    dx = bx - ax
    dy = by - ay
    length = math.hypot(dx, dy)
    if length == 0.0:
        return math.hypot(px - ax, py - ay), 0.0, 0.0
    # Signed cross product → tells us which side of the line p sits on.
    cross = (dx) * (py - ay) - (dy) * (px - ax)
    # Project p onto the segment, clamp to [0, length].
    t = ((px - ax) * dx + (py - ay) * dy) / (length * length)
    t_clamped = max(0.0, min(1.0, t))
    foot_x = ax + t_clamped * dx
    foot_y = ay + t_clamped * dy
    dist = math.hypot(px - foot_x, py - foot_y)
    return dist, cross, length


def _unit_perpendicular(
    start: tuple[float, float], end: tuple[float, float]
) -> tuple[float, float]:
    """Return the left-hand unit normal of the start→end vector.

    Paired with the cross-product sign in :func:`_point_segment_perp` this
    lets callers pick the side of the line they want to bow toward.
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0.0:
        return 0.0, 0.0
    # Rotate the unit tangent 90° CCW → left-hand normal.
    return -dy / length, dx / length


def _find_screener(
    start: tuple[float, float],
    end: tuple[float, float],
    actions: list[Any],
    positions: dict[str, tuple[float, float]],
    mover_id: str | None = None,
) -> tuple[float, float] | None:
    """Return the coord of the screener to route this cut around.

    Two rules, semantic wins over geometric:

    1. **Semantic**: a screen whose ``move.to`` coord equals the cut mover's
       starting position is explicitly setting a screen for THIS cut (the
       importer records "4 screens 2" as ``{move.id=4, move.to=<coord of 2>}``,
       so matching coords is the reliable signal regardless of how far the
       screener sits from the straight-line path). This catches Iverson-style
       elbow screens where the screener is 7+ SVG units off the cut line.
    2. **Geometric fallback**: screener within :data:`SCREEN_PROXIMITY` SVG
       units of the cut segment (not the infinite line). Handles cases where
       the wiki didn't explicitly pair screen-to-cut or extraction lost the
       linkage.
    """
    semantic_match: tuple[float, float] | None = None
    best: tuple[float, float] | None = None
    best_dist = SCREEN_PROXIMITY
    for other in actions:
        if not isinstance(other, dict):
            continue
        if other.get("marker") != "screen":
            continue
        other_move = other.get("move")
        if not isinstance(other_move, dict):
            continue
        screener_id = other_move.get("id")
        if not isinstance(screener_id, str):
            continue
        screener_coord = positions.get(screener_id)
        if screener_coord is None:
            continue
        # Rule 1 — semantic match via the screen's target coord.
        if semantic_match is None and mover_id is not None:
            other_to = other_move.get("to")
            if isinstance(other_to, (list, tuple)) and len(other_to) == 2:
                try:
                    ox = float(other_to[0])
                    oy = float(other_to[1])
                    if (
                        abs(ox - start[0]) < 0.01
                        and abs(oy - start[1]) < 0.01
                    ):
                        semantic_match = screener_coord
                        continue
                except (TypeError, ValueError):
                    pass
        # Rule 2 — geometric fallback.
        dist, _side, length = _point_segment_perp(screener_coord, start, end)
        if length == 0.0:
            continue
        if dist <= best_dist:
            best_dist = dist
            best = screener_coord
    return semantic_match or best


def _cubic_around(
    start: tuple[float, float],
    end: tuple[float, float],
    screener: tuple[float, float],
) -> str:
    """Build a cubic bezier that bows OVER/AROUND ``screener``.

    Control point = screener + :data:`CURVE_BOW` along the line's normal, on
    the SAME side of the line as the screener (so the curve peaks beyond the
    screener, not between screener and line). This matches basketball
    convention: a cut using a screen passes on the far side of the screener's
    body — for a high screen, the cutter goes OVER THE TOP (even farther from
    the basket). Both control points are identical so the cubic behaves like
    a single-control quadratic but still emits a ``C`` command.
    """
    nx, ny = _unit_perpendicular(start, end)
    _dist, side, _length = _point_segment_perp(screener, start, end)
    # Match the screener's side: the curve goes around the FAR side of the
    # screener, not between the screener and the cut line. side == 0
    # (degenerate: screener sits on the line) defaults to positive normal.
    sign = 1.0 if side >= 0 else -1.0
    cx = screener[0] + sign * nx * CURVE_BOW
    cy = screener[1] + sign * ny * CURVE_BOW
    x0, y0 = start
    x1, y1 = end
    return (
        f"M {round(x0, 2)} {round(y0, 2)} "
        f"C {round(cx, 2)} {round(cy, 2)} "
        f"{round(cx, 2)} {round(cy, 2)} "
        f"{round(x1, 2)} {round(y1, 2)}"
    )


def _cubic_gentle_arc(
    start: tuple[float, float], end: tuple[float, float]
) -> str:
    """Build a gentle arc bowing toward the court centerline.

    Midpoint of the segment gets offset by :data:`DEFAULT_BOW` along the
    line's normal, picking the side whose x-component nudges the midpoint
    toward x=0 (the centerline). For segments that start and end near the
    centerline already (both |x| < 3) we bow toward the basket end (+y).
    """
    x0, y0 = start
    x1, y1 = end
    mid_x = (x0 + x1) / 2.0
    mid_y = (y0 + y1) / 2.0
    nx, ny = _unit_perpendicular(start, end)
    if abs(x0) < 3.0 and abs(x1) < 3.0:
        # Both endpoints hug the centerline — bow toward the basket end (+y).
        sign = 1.0 if ny >= 0 else -1.0
    else:
        # Bow toward x=0. If nx points toward the centerline from the midpoint,
        # use +sign; otherwise flip.
        if mid_x > 0:
            sign = -1.0 if nx > 0 else 1.0
        elif mid_x < 0:
            sign = 1.0 if nx > 0 else -1.0
        else:
            sign = 1.0
    cx = mid_x + sign * nx * DEFAULT_BOW
    cy = mid_y + sign * ny * DEFAULT_BOW
    return (
        f"M {round(x0, 2)} {round(y0, 2)} "
        f"C {round(cx, 2)} {round(cy, 2)} "
        f"{round(cx, 2)} {round(cy, 2)} "
        f"{round(x1, 2)} {round(y1, 2)}"
    )


def _screen_stub(
    screener: tuple[float, float], target: tuple[float, float]
) -> str:
    """Build a short line from screener stopping ``SCREEN_STOP_BACK`` short.

    If the full distance is less than the stop-back threshold the full line
    is emitted — we never invert direction.
    """
    sx, sy = screener
    tx, ty = target
    dx = tx - sx
    dy = ty - sy
    length = math.hypot(dx, dy)
    if length <= SCREEN_STOP_BACK or length == 0.0:
        return _straight_path(screener, target)
    ratio = (length - SCREEN_STOP_BACK) / length
    ex = sx + dx * ratio
    ey = sy + dy * ratio
    return _straight_path(screener, (ex, ey))


def _synthesize_one_action(
    action: dict[str, Any],
    start: tuple[float, float],
    end: tuple[float, float],
    sibling_actions: list[Any],
    positions: dict[str, tuple[float, float]],
) -> str:
    """Pick the right path shape for a single action.

    Dispatches on ``marker`` + ``dashed``:
    - ``screen`` → short stub line that stops short of the screenee.
    - ``arrow`` + dashed (pass) → straight line (unchanged).
    - ``arrow`` non-dashed (cut/move) → screen-aware cubic arc, else gentle arc.
    - ``shot`` / ``dribble`` / ``handoff`` / anything else → straight line.
    """
    marker = action.get("marker")
    dashed = bool(action.get("dashed"))
    if marker == "screen":
        return _screen_stub(start, end)
    if marker == "arrow" and not dashed:
        move = action.get("move")
        mover_id = (
            move.get("id") if isinstance(move, dict) else None
        )
        mover_id_str = mover_id if isinstance(mover_id, str) else None
        screener = _find_screener(
            start, end, sibling_actions, positions, mover_id_str
        )
        if screener is not None:
            return _cubic_around(start, end, screener)
        return _cubic_gentle_arc(start, end)
    # arrow+dashed (pass), shot, dribble, handoff, and unknown markers →
    # straight line — the viewer overlays dribble zigzags / handoff ticks.
    return _straight_path(start, end)


def _synthesize_phase_actions(
    phase: Any,
    positions: dict[str, tuple[float, float]],
) -> None:
    """Walk one phase's actions, mutating empty ``path`` fields in place.

    ``positions`` is updated as each mover advances so subsequent actions in
    the same phase chain off the new coordinates. Screen-awareness peeks at
    sibling actions within the same phase to curve cuts around screeners
    whose coords sit within :data:`SCREEN_PROXIMITY` of the straight line.
    """
    if not isinstance(phase, dict):
        return
    actions = phase.get("actions")
    if not isinstance(actions, list):
        return
    for action in actions:
        if not isinstance(action, dict):
            continue
        move = action.get("move")
        if not isinstance(move, dict):
            # Ball-only (pass) branch: actions with a ``ball.{from,to}`` field
            # but no ``move`` — the wiki importer's convention for passes.
            # Synthesize a straight line between the passer and receiver so
            # the dashed pass-arrow actually renders instead of staying blank.
            ball = action.get("ball")
            if (
                isinstance(ball, dict)
                and _needs_synthesis(action.get("path"))
            ):
                ball_from = ball.get("from")
                ball_to = ball.get("to")
                if (
                    isinstance(ball_from, str)
                    and isinstance(ball_to, str)
                ):
                    from_pos = positions.get(ball_from)
                    to_pos = positions.get(ball_to)
                    if from_pos is not None and to_pos is not None:
                        action["path"] = _straight_path(from_pos, to_pos)
            continue
        mover = move.get("id")
        if not isinstance(mover, str) or mover not in positions:
            # No player binding or unknown player — skip gracefully.
            continue
        end = _coord_pair(move.get("to"))
        if end is None:
            # Claude omitted the endpoint — leave path empty.
            continue
        if not _needs_synthesis(action.get("path")):
            # User-authored path already present — advance tracker anyway so
            # later actions chain from the correct endpoint.
            positions[mover] = end
            continue
        start = positions[mover]
        action["path"] = _synthesize_one_action(
            action, start, end, actions, positions
        )
        positions[mover] = end


def _synthesize_action_paths(play: dict[str, Any]) -> None:
    """Fill empty SVG paths with straight-line ``M x0 y0 L x1 y1`` segments.

    Tracks each player's position through the main phase sequence. Branch
    options fork from a deep-copied snapshot so parallel branches do not
    contaminate each other.
    """
    players = play.get("players")
    if not isinstance(players, dict):
        return
    positions: dict[str, tuple[float, float]] = {}
    for pid, coord in players.items():
        pair = _coord_pair(coord)
        if isinstance(pid, str) and pair is not None:
            positions[pid] = pair
    if not positions:
        return

    for phase in play.get("phases") or []:
        _synthesize_phase_actions(phase, positions)

    bp = play.get("branchPoint")
    if isinstance(bp, dict):
        options = bp.get("options")
        if isinstance(options, list):
            for opt in options:
                if not isinstance(opt, dict):
                    continue
                branch_phase = opt.get("phase")
                branch_positions = copy.deepcopy(positions)
                _synthesize_phase_actions(branch_phase, branch_positions)


def extract_play_from_prose(prose: str) -> ExtractionResult:
    """Extract a V7Play draft from book prose via Claude.

    Falls back to a deterministic stub when no ``ANTHROPIC_API_KEY`` is set
    or the Claude call fails — the lab UX never dead-ends.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return _stub_extract(prose)

    try:
        import anthropic
    except ImportError:
        return _stub_extract(prose)

    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            messages=[{"role": "user", "content": _build_prompt(prose)}],
        )
    except Exception:
        # Any upstream failure (network, 5xx, rate limit) degrades to stub so
        # the lab UX never dead-ends.
        return _stub_extract(prose)

    text_parts: list[str] = []
    for block in getattr(message, "content", []) or []:
        block_text = getattr(block, "text", None)
        if isinstance(block_text, str):
            text_parts.append(block_text)
    raw = _strip_code_fence("".join(text_parts).strip())
    if not raw:
        return _stub_extract(prose)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        return ExtractionResult(
            play={},
            todos=[
                f"Claude returned non-JSON output: {exc}. "
                f"First 400 chars: {raw[:400]}"
            ],
            source="claude-error",
        )
    if not isinstance(parsed, dict):
        return ExtractionResult(
            play={},
            todos=[f"Claude returned non-object JSON: {type(parsed).__name__}"],
            source="claude-error",
        )

    stripped = _sanitize_branch_point(parsed)
    _synthesize_action_paths(parsed)
    todos = _collect_todos(parsed)
    if stripped:
        todos.append(
            "branchPoint was stripped — Claude produced a malformed structure. "
            "Add branches by hand if the play has read-based options."
        )
    return ExtractionResult(
        play=parsed,
        todos=todos,
        source="claude",
    )
