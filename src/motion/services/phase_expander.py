# Copyright: Your Name. Apache 2.0
"""Narrative phase → role-token action expander.

When a wiki play page carries fewer diagram-positions blocks than it has
``### Phase N:`` sections, phases 2+ land empty in the lab. This module asks
Claude to read the phase prose and emit **role-token actions** in the same
shape the wiki's existing diagram blocks use — never pixel coordinates.

Hard constraint: the LLM must NOT generate coords. It emits dicts of the form
``{"from": "<player_id>", "to": "<player_id_or_role_token>", "type": "<verb>"}``
and :func:`motion.services.wiki_importer._convert_actions` resolves the
``to`` side to deterministic pixel coords via ``_ROLE_COORDS``.

Mirrors the ``ANTHROPIC_API_KEY`` missing → ``[]`` graceful-fallback pattern
used by :mod:`motion.services.play_extractor`.
"""

from __future__ import annotations

import json
import os
from typing import Any

from motion.services.play_extractor import _strip_code_fence

_MODEL = "claude-sonnet-4-6"
_MAX_TOKENS = 1024
# Deterministic decoding — iverson-ram validation showed P2.4 (5→wing target)
# flipping run-to-run at 0.2. 0.0 makes reruns reproducible so prompt edits are
# measurable instead of lost in sampling noise.
_TEMPERATURE = 0.0

# ---------------------------------------------------------------------------
# Allowed vocabularies — the importer's ``_convert_actions`` is the source of
# truth for what it knows how to resolve; keep these in sync by construction.
# ---------------------------------------------------------------------------

_ALLOWED_ROLE_TOKENS: frozenset[str] = frozenset(
    {
        "right_wing",
        "left_wing",
        "right_corner",
        "left_corner",
        "top",
        "left_elbow",
        "right_elbow",
        "basket",
        "left_block",
        "right_block",
        "ball_side_corner",
    }
)

_ALLOWED_ACTION_TYPES: frozenset[str] = frozenset(
    {
        "cut",
        "drive",
        "move",
        "pass",
        "dribble",
        "dribble-pass",
        "screen",
        "down-screen",
        "back-screen",
        "flare-screen",
        "cross-screen",
        "pin-down",
        "handoff",
        "dho",
        "shot",
        "shoot",
        "finish",
    }
)


# ---------------------------------------------------------------------------
# Prompts.
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are a basketball play-extraction assistant.

You read ONE phase of narrative prose from a play and emit a JSON array of \
role-token actions — the same structure the wiki's diagram-positions blocks \
use. You do NOT emit pixel coordinates; a downstream resolver converts \
role tokens to coords deterministically.

OUTPUT FORMAT (strict):
- Return ONLY a JSON array. No prose, no markdown code fences, no commentary.
- Each element must be exactly: \
{"from": "<player_id>", "to": "<player_id_or_role_token>", "type": "<verb>"}
- "from" MUST be one of the provided player_ids (usually "1".."5").
- "to" MUST be EITHER another player id from player_ids OR one of: \
right_wing, left_wing, right_corner, left_corner, top, left_elbow, \
right_elbow, basket, left_block, right_block, ball_side_corner.
- "type" MUST be one of: cut, drive, move, pass, dribble, dribble-pass, \
screen, down-screen, back-screen, flare-screen, cross-screen, pin-down, \
handoff, dho, shot, shoot, finish.

RULES:
- Only emit actions EXPLICITLY described in the phase text. Do NOT invent \
supplementary actions, implied motion, or "natural next steps".
- If the phase text is purely tactical discussion (no concrete player \
movement / screen / pass / shot), return [].
- Prefer player-id targets for passes and screens when the text names a \
specific player as the recipient/screenee. Use role tokens only when the \
text names a court location (wing, corner, elbow, block, basket, top).

ATOMIC SEQUENCING:
- One atomic action per array element. If the phase text bundles multiple \
actions into one sentence ("4 screens down on 5's defender as 5 sprints up \
to screen for 2"), emit SEPARATE entries for each movement/screen/pass.
- A movement that ENDS by setting a screen is ONE action: emit it with a \
screen-family type (screen, down-screen, back-screen, flare-screen, \
cross-screen, pin-down). Do NOT emit a preceding "move" step for the same \
player in the same phase.

CAUSAL ORDERING (overrides syntactic order):
- If action N depends on action M's effect, M comes first in the array.
- A screener's arrival at the screen location ALWAYS precedes the cutter \
using that screen. Emit the screener's action before the cutter's.
- In screen-the-screener sequences (A screens for B, then B screens for C), \
emit A's screen first — it must free B before B can screen C.
- When the text uses explicit numbering that would violate causality, \
reorder by causality silently.

POSITION AWARENESS:
- When current_positions is provided, use it as GROUND TRUTH for where each \
player stands at the start of this phase. If the text says "5 screens for 2" \
and the positions show 2 at right_wing, emit to=\"2\" (player-id) — do NOT \
guess a role token. When you must pick a role token, pick the one matching \
the named player's current position, not a default.
"""

_FEW_SHOT_EXAMPLE_TEXT = (
    "4 screens down on 5's defender as 5 sprints up to set a ball screen "
    "for 2. 2 uses the screen and cuts over the top toward the right wing."
)

# Notes on why this output is correct (for human review; NOT sent to model):
# - "screens down ... as ... sprints up" is a BUNDLED sentence — two distinct
#   actions, emitted separately.
# - Causal order: 4 frees 5 FIRST (down-screen), then 5 can screen for 2,
#   then 2 can cut off 5's screen. Emission order follows causality even
#   though the sentence structure mentions 2's cut last.
# - 5's "sprint up to set a ball screen" is one atomic action with
#   screen-family type, not a move+screen pair.
_FEW_SHOT_EXAMPLE_OUTPUT = (
    '[{"from":"4","to":"5","type":"down-screen"},'
    '{"from":"5","to":"2","type":"screen"},'
    '{"from":"2","to":"right_wing","type":"cut"}]'
)


def _build_user_message(
    phase_label: str,
    phase_text: str,
    player_ids: list[str],
    preceding_actions: list[dict[str, Any]] | None,
    current_positions: dict[str, tuple[float, float]] | None = None,
) -> str:
    """Assemble the user-turn content with the few-shot example first.

    ``current_positions`` tells the model where each player stands at the
    START of this phase (after earlier phases' moves have resolved). Without
    it the model loses positional context — e.g. in Iverson Ram the wing
    exchange in phase 1 swaps 2 to right_wing, and phase 2's "5 sprints up
    to the ball-handler 2" needs to know 2 is at right_wing, not left.
    """
    parts: list[str] = [
        "EXAMPLE",
        "-------",
        "phase_label: Phase 2: Screen The Screener",
        "player_ids: [\"1\", \"2\", \"3\", \"4\", \"5\"]",
        "phase_text:",
        _FEW_SHOT_EXAMPLE_TEXT,
        "expected_output:",
        _FEW_SHOT_EXAMPLE_OUTPUT,
        "",
        "YOUR TURN",
        "---------",
        f"phase_label: {phase_label}",
        f"player_ids: {json.dumps(player_ids)}",
    ]
    if current_positions:
        # Include where each player currently stands at the start of this
        # phase so the model can pick correct directional role tokens.
        # Coords are ONLY context — the model must still emit role tokens,
        # never [x, y] pairs.
        pos_json = json.dumps(
            {pid: [round(xy[0], 1), round(xy[1], 1)] for pid, xy in current_positions.items()}
        )
        parts.append(f"current_positions (context only, DO NOT emit coords): {pos_json}")
    if preceding_actions:
        # Clip to keep the prompt small; context is just an ordering hint.
        preceding_json = json.dumps(preceding_actions[-20:])
        parts.append(f"preceding_actions (context only): {preceding_json}")
    parts.extend(
        [
            "phase_text:",
            phase_text.strip() or "(empty)",
            "",
            "Return the JSON array of role-token actions now.",
        ]
    )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Validation.
# ---------------------------------------------------------------------------


def _validate_action(action: Any, player_ids_set: frozenset[str]) -> dict[str, str] | None:
    """Return the action normalized to ``{from, to, type}`` or ``None``.

    Drops entries that fail any schema constraint silently — the caller treats
    the filtered list as ground truth.
    """
    if not isinstance(action, dict):
        return None
    from_field = action.get("from")
    to_field = action.get("to")
    type_field = action.get("type")
    if not isinstance(from_field, (str, int)):
        return None
    if not isinstance(to_field, (str, int)):
        return None
    if not isinstance(type_field, str):
        return None

    from_str = str(from_field)
    to_str = str(to_field)
    type_str = type_field.strip().lower()

    if from_str not in player_ids_set:
        return None
    if to_str not in player_ids_set and to_str not in _ALLOWED_ROLE_TOKENS:
        return None
    if type_str not in _ALLOWED_ACTION_TYPES:
        return None

    return {"from": from_str, "to": to_str, "type": type_str}


def _filter_actions(
    candidates: Any,
    player_ids: list[str],
) -> list[dict[str, Any]]:
    """Validate & drop any malformed entries from a candidate action list."""
    if not isinstance(candidates, list):
        return []
    allowed_ids = frozenset(player_ids)
    valid: list[dict[str, Any]] = []
    for entry in candidates:
        normalized = _validate_action(entry, allowed_ids)
        if normalized is not None:
            valid.append(normalized)
    return valid


# ---------------------------------------------------------------------------
# Public entry point.
# ---------------------------------------------------------------------------


def expand_phase_from_narrative(
    phase_label: str,
    phase_text: str,
    player_ids: list[str],
    preceding_actions: list[dict[str, Any]] | None = None,
    current_positions: dict[str, tuple[float, float]] | None = None,
) -> list[dict[str, Any]]:
    """Emit role-token actions from phase prose.

    Returns an empty list whenever:
    - ``ANTHROPIC_API_KEY`` is not set.
    - The ``anthropic`` SDK is not importable.
    - The Claude call raises (network, rate limit, etc.).
    - Claude returns malformed JSON or a non-list.
    - No candidate action passes the schema validation.

    Never raises. Deterministic fallback = ``[]`` so the importer can keep
    its existing empty-phase behavior.
    """
    if not phase_text or not phase_text.strip():
        return []
    if not player_ids:
        return []
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return []

    try:
        import anthropic
    except ImportError:
        return []

    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            temperature=_TEMPERATURE,
            system=_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": _build_user_message(
                        phase_label,
                        phase_text,
                        player_ids,
                        preceding_actions,
                        current_positions,
                    ),
                }
            ],
        )
    except Exception:
        return []

    text_parts: list[str] = []
    for block in getattr(message, "content", []) or []:
        block_text = getattr(block, "text", None)
        if isinstance(block_text, str):
            text_parts.append(block_text)
    raw = _strip_code_fence("".join(text_parts).strip())
    if not raw:
        return []

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []

    return _filter_actions(parsed, player_ids)
