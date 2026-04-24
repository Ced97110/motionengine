"""V7Play → wiki markdown writer.

Produces the inverse of :mod:`motion.services.wiki_importer`. The writer
replaces the ``json name=diagram-positions`` fences inside an existing
``.md`` page with fresh blocks derived from a V7Play dict, preserving every
other byte of the file (frontmatter, prose, wikilinks, sources).

Design invariants:

- **One block per phase.** The writer emits ``len(play.phases)`` blocks,
  each tagged ``Phase N`` in its ``notes`` field so the importer's phase
  alignment pass can bind them back 1:1.
- **Deterministic serialization.** Action dicts use a stable key order so
  diffs against the previous version only reflect real changes.
- **Non-diagram content is byte-preserved.** Frontmatter, ``# Heading``,
  ``## Overview``, phase prose, ``## Related Plays``, ``## Sources`` pass
  through untouched — the writer only rewrites fenced diagram blocks.
- **Lossy-in-one-direction only.** If a wiki page originally used role
  tokens (``"to": "right_wing"``), round-tripping through the writer
  converts them to coord pairs (``"to": [18, 22]``). That is acceptable:
  the importer accepts both forms and coords are strictly more specific.
  Semantic fidelity (who moves, what type of action) is always preserved.

Schema v2 reminder — action dict shape emitted:

.. code-block:: json

    {"type": "...", "from": "...", "to": ...,
     "path": "...", "moveTo": [x, y],
     "durationMs": 2200, "gapAfterMs": 300,
     "ballTo": "..."}

Optional keys (``path`` / ``moveTo`` / timing / ``ballTo``) are OMITTED
when they would round-trip as defaults, keeping blocks minimal.
"""

from __future__ import annotations

import json
import re
from typing import Any, Literal

# ---------------------------------------------------------------------------
# Marker → wiki-type reverse map.
#
# The forward map in :mod:`wiki_importer` (``_ACTION_MARKER_MAP``) collapses
# several wiki types into the same ``(marker, dashed)`` tuple — e.g.
# ``cut`` / ``drive`` / ``move`` all map to ``("arrow", False)``. The
# writer can only pick ONE canonical string to emit; it picks the most
# generic. Pages that were originally authored with a specific type keep
# that string if the writer is run on import-without-edit (because
# ``_emit_action`` never touches a block if no mutation is needed — see
# :func:`render_updated_markdown`). Fresh edits from the lab always land
# on the canonical tokens.
# ---------------------------------------------------------------------------

_MARKER_TO_TYPE: dict[tuple[str, bool], str] = {
    ("arrow", False): "cut",
    ("arrow", True): "pass",
    ("screen", False): "screen",
    ("shot", False): "shot",
    ("dribble", False): "dribble",
    ("handoff", False): "handoff",
}


# Action key order — stable across writes. Missing keys are skipped.
_ACTION_KEY_ORDER = (
    "type", "from", "to",
    "path", "moveTo",
    "durationMs", "gapAfterMs",
    "ballTo",
)


# Regex — mirrors ``_DIAGRAM_FENCE_RE`` in wiki_importer.py. Kept local so
# the two modules can evolve their parse/emit surfaces independently.
_DIAGRAM_FENCE_RE = re.compile(
    r"```\s*json\s+name=diagram-positions\s*\n(?P<body>.*?)\n```",
    re.DOTALL,
)

# Phase header regex — mirrors ``_PHASE_HEADER_RE`` in wiki_importer.py.
_PHASE_HEADER_RE = re.compile(
    r"^###\s+Phase\s+(?P<num>\d+)\s*[:\-—]?\s*(?P<label>.*?)\s*$",
    re.MULTILINE,
)

# "Phase N" reference (anywhere in text) — mirrors the importer's phase-
# binding heuristic (``_infer_phase_num``). Used to decide whether we need
# to prepend a synthetic prefix to block notes for deterministic binding.
_PHASE_REFERENCE_RE = re.compile(r"Phase\s+(\d+)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def v7_play_to_diagram_blocks(
    play: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Serialize a V7Play's phases into diagram-positions blocks.

    Returns ``(blocks, warnings)``. One block per phase in ``play.phases``.
    Each block has:

    - ``players``: coord snapshot at the START of that phase (computed by
      replaying prior phases' ``move`` fields, honoring the screen-doesn't-
      relocate-screener rule shared with the importer).
    - ``ballStart`` (block 0 only): ``play.ballStart``.
    - ``actions``: reverse-converted V7 actions.
    - ``notes``: ``f"Phase {N}."`` so the importer's phase aligner can
      bind block ↔ phase unambiguously.

    Warnings surface any V7 action the writer couldn't serialize (e.g. a
    bare ``{marker, path}`` with no ``move`` or ``ball`` — the importer
    tolerates these on read, but there's no ``from`` to recover for write).
    """
    warnings: list[str] = []
    phases = play.get("phases") or []
    base_players = play.get("players") or {}
    positions: dict[str, tuple[float, float]] = {
        pid: (float(coord[0]), float(coord[1]))
        for pid, coord in base_players.items()
        if _looks_like_coord(coord)
    }

    blocks: list[dict[str, Any]] = []
    for phase_idx, phase in enumerate(phases):
        players_snapshot = [
            {"role": pid, "x": positions[pid][0], "y": positions[pid][1]}
            for pid in sorted(positions.keys(), key=_player_sort_key)
        ]
        block: dict[str, Any] = {"players": players_snapshot}
        if phase_idx == 0:
            ball_start = play.get("ballStart")
            if isinstance(ball_start, str) and ball_start:
                block["ballStart"] = ball_start
        actions_out: list[dict[str, Any]] = []
        raw_actions = phase.get("actions") or []
        for action_idx, action in enumerate(raw_actions):
            emitted = _emit_action(action)
            if emitted is not None:
                actions_out.append(emitted)
            elif isinstance(action, dict):
                warnings.append(
                    f"Phase {phase_idx + 1} action {action_idx}: "
                    f"skipped (no recoverable `from` — marker="
                    f"{action.get('marker')!r}, has_move="
                    f"{bool(action.get('move'))}, has_ball="
                    f"{bool(action.get('ball'))})"
                )
        block["actions"] = actions_out
        # Block notes: use the phase's authored prose when present so no-phase-
        # section pages (where the importer treats `block.notes` AS the phase
        # text) round-trip cleanly. Fall back to "Phase N." when empty —
        # still readable and lets the importer's `_infer_phase_num` bind the
        # block to its section when one exists.
        phase_text = phase.get("text")
        if isinstance(phase_text, str) and phase_text.strip():
            block["notes"] = phase_text
        else:
            block["notes"] = f"Phase {phase_idx + 1}."
        blocks.append(block)
        _advance_positions(raw_actions, positions)
    return blocks, warnings


def render_updated_markdown(
    existing_md: str,
    blocks: list[dict[str, Any]],
) -> tuple[str, list[str]]:
    """Replace diagram-positions fences in ``existing_md`` with new blocks.

    Behavior:

    - If the file already has ``len(blocks)`` or fewer fences, the first N
      are overwritten in document order and any extras at the end are
      APPENDED (one blank line between) under a synthesized "## Phases"-
      adjacent region near the end of the body. When the file has more
      fences than the new block list supplies, the extras are left in
      place and a warning is returned — the writer never silently deletes
      existing diagram data.
    - Non-fence content is byte-preserved.
    - Block notes are PREFIXED with ``"Phase N. "`` when the source has
      ``### Phase N`` section headers — gives the importer's phase-
      binding pass an unambiguous anchor. Files without phase sections
      keep notes verbatim so ``phase.text`` (which the importer derives
      from ``block.notes`` in that case) round-trips cleanly.

    Returns ``(new_md, warnings)``. Warnings are human-readable strings
    meant for the lab's confirmation modal.
    """
    warnings: list[str] = []
    fence_matches = list(_DIAGRAM_FENCE_RE.finditer(existing_md))

    # Apply phase-binding prefix to notes in-place when the source has
    # ``### Phase N`` headers. Operates on copies — the caller's blocks
    # list is not mutated.
    has_sections = bool(_PHASE_HEADER_RE.search(existing_md))
    if has_sections:
        blocks = [_prefix_phase_note(b, i + 1) for i, b in enumerate(blocks)]

    replace_count = min(len(fence_matches), len(blocks))
    extras_from_md = fence_matches[replace_count:]
    extras_from_blocks = blocks[replace_count:]

    # Walk matches, replace in place.
    pieces: list[str] = []
    cursor = 0
    for i, match in enumerate(fence_matches[:replace_count]):
        pieces.append(existing_md[cursor : match.start()])
        pieces.append(_render_block(blocks[i]))
        cursor = match.end()
    pieces.append(existing_md[cursor:])
    new_md = "".join(pieces)

    if extras_from_blocks:
        # Append any new blocks not covered by existing fences. Appending
        # near the end of the body keeps the file valid markdown; humans
        # can move the blocks next to their phase section in a follow-up
        # edit if they prefer that layout.
        appended = "\n\n".join(_render_block(b) for b in extras_from_blocks)
        new_md = new_md.rstrip() + "\n\n" + appended + "\n"
        warnings.append(
            f"Appended {len(extras_from_blocks)} new diagram block(s) at the "
            "end of the file — move them next to their phase sections if "
            "that's more readable."
        )

    if extras_from_md:
        warnings.append(
            f"{len(extras_from_md)} existing diagram block(s) in the wiki "
            "page were not overwritten (V7Play supplied fewer phases than "
            "the file contains). Review the diff — you may want to delete "
            "the stale blocks."
        )

    return new_md, warnings


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _looks_like_coord(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple))
        and len(value) == 2
        and all(isinstance(v, (int, float)) for v in value)
    )


def _player_sort_key(pid: str) -> tuple[int, str]:
    """Numeric ids first (in numeric order), then alphabetical strings."""
    try:
        return (0, f"{int(pid):09d}")
    except ValueError:
        return (1, pid)


def _advance_positions(
    raw_actions: Any,
    positions: dict[str, tuple[float, float]],
) -> None:
    """Mirror :func:`wiki_importer._build_phases._advance_positions`.

    Screens do NOT relocate the screener (same rule enforced in frontend
    ``computePositionsAt`` and backend ``wiki_importer``).
    """
    if not isinstance(raw_actions, list):
        return
    for action in raw_actions:
        if not isinstance(action, dict):
            continue
        if action.get("marker") == "screen":
            continue
        move = action.get("move")
        if not isinstance(move, dict):
            continue
        mover = move.get("id")
        to = move.get("to")
        if not isinstance(mover, str):
            continue
        if not isinstance(to, (list, tuple)) or len(to) != 2:
            continue
        try:
            positions[mover] = (float(to[0]), float(to[1]))
        except (TypeError, ValueError):
            continue


def _emit_action(action: dict[str, Any]) -> dict[str, Any] | None:
    """Convert one V7Action dict to the wiki block format.

    Returns ``None`` when the action is too malformed to emit (e.g. no
    identifiable ``from`` player) — the writer skips those rather than
    producing invalid entries.
    """
    marker = action.get("marker")
    dashed = bool(action.get("dashed"))
    wiki_type = _MARKER_TO_TYPE.get((str(marker), dashed))
    if wiki_type is None:
        return None

    move = action.get("move") if isinstance(action.get("move"), dict) else None
    ball = action.get("ball") if isinstance(action.get("ball"), dict) else None

    from_id: str | None = None
    to_value: Any = None
    if ball is not None:
        # Pass: ``from`` is passer, ``to`` is receiver (player id).
        from_id = str(ball.get("from")) if ball.get("from") is not None else None
        to_value = str(ball.get("to")) if ball.get("to") is not None else None
    elif move is not None:
        from_id = str(move.get("id")) if move.get("id") is not None else None
        move_to = move.get("to")
        if _looks_like_coord(move_to):
            # Emit as explicit coord list; importer's _resolve_destination
            # handles list-form `to` (wiki_importer.py:462).
            to_value = [float(move_to[0]), float(move_to[1])]

    if not from_id:
        return None

    out: dict[str, Any] = {"type": wiki_type, "from": from_id}
    if to_value is not None:
        out["to"] = to_value

    # Schema v2 passthroughs. Only emit when set — keeps the wiki block
    # minimal for actions without authored geometry / timing.
    path = action.get("path")
    if isinstance(path, str) and path.strip():
        out["path"] = path
    duration_ms = action.get("durationMs")
    if isinstance(duration_ms, (int, float)) and duration_ms > 0:
        out["durationMs"] = int(duration_ms)
    gap_ms = action.get("gapAfterMs")
    if isinstance(gap_ms, (int, float)) and gap_ms >= 0:
        out["gapAfterMs"] = int(gap_ms)

    return _reorder(out)


def _reorder(action: dict[str, Any]) -> dict[str, Any]:
    """Return a dict with keys in :data:`_ACTION_KEY_ORDER`.

    Python 3.7+ preserves dict insertion order; ``json.dumps`` honors it.
    """
    ordered: dict[str, Any] = {}
    for key in _ACTION_KEY_ORDER:
        if key in action:
            ordered[key] = action[key]
    # Tail: any unexpected keys preserved at the end so future schema
    # additions don't silently vanish.
    for key, value in action.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def _render_block(block: dict[str, Any]) -> str:
    """Pretty-print one block inside its fenced markdown wrapper."""
    body = json.dumps(block, indent=2, ensure_ascii=False)
    return f"```json name=diagram-positions\n{body}\n```"


def _prefix_phase_note(block: dict[str, Any], phase_num: int) -> dict[str, Any]:
    """Ensure ``block["notes"]`` starts with ``"Phase N."`` for binding.

    If the existing note already opens with ``"Phase N"`` for the correct
    N, leave it alone. Otherwise prepend ``f"Phase {phase_num}. "`` so
    the importer's ``_infer_phase_num`` resolves to this block's phase
    regardless of what ``Phase N`` references appear later in the prose.
    Returns a shallow copy — the input dict is not mutated.
    """
    out = dict(block)
    notes = out.get("notes") or ""
    match = _PHASE_REFERENCE_RE.match(notes)
    if match and int(match.group(1)) == phase_num:
        return out
    prefix = f"Phase {phase_num}. "
    out["notes"] = prefix + notes if notes else prefix.rstrip()
    return out


# ---------------------------------------------------------------------------
# Text-form entry point (matches import_wiki_play but operates on raw md).
# Kept as a convenience for tests and the round-trip harness — it avoids
# writing a temp file to disk every round.
# ---------------------------------------------------------------------------


ImportSourceLiteral = Literal["wiki-structured", "wiki-partial", "wiki-no-diagram"]
