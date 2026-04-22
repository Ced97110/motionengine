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
import os
from dataclasses import dataclass
from typing import Any

_MODEL = "claude-sonnet-4-6"
_MAX_TOKENS = 4096


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


def _synthesize_phase_actions(
    phase: Any,
    positions: dict[str, tuple[float, float]],
) -> None:
    """Walk one phase's actions, mutating empty ``path`` fields in place.

    ``positions`` is updated as each mover advances so subsequent actions in
    the same phase chain off the new coordinates.
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
        x0, y0 = positions[mover]
        x1, y1 = end
        action["path"] = f"M {round(x0, 2)} {round(y0, 2)} L {round(x1, 2)} {round(y1, 2)}"
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
