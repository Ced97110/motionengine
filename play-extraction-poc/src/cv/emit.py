"""YAML emitter for CV-extracted plays.

Produces output that matches the existing pipeline's shape (the
Claude-Vision extractions in ``results/extractions/*.yaml``), so
downstream consumers and comparison tools keep working after the
vision-LLM layer is replaced with the CV pipeline.

Key shape notes (verified against
``diagram_01_page_060-060_strategy_a.yaml`` and ``..._b.yaml``):

* The document is wrapped in a triple-backtick ``yaml`` code fence.
* Top-level key is ``play`` with ``name``, ``tag``, ``players``,
  ``ball_start`` and a list of ``phases``.
* ``players`` is a mapping of ``"digit" -> [x, y]`` (flow-style list).
* Each phase has ``label``, ``description`` and a list of ``movements``.
* Movement fields:
    - ``player`` (required, string digit)
    - ``from`` / ``to`` as flow-style ``[x, y]`` when spatial
    - ``to_player`` (for passes / handoffs)
    - ``type`` (one of cut, pass, screen, dribble, handoff)
    - ``confidence`` bucketed into low / medium / high.

No LLM calls. Deterministic. Pure string building — we avoid
``yaml.safe_dump`` because the reference file uses a handwritten
layout (quoted string keys, flow-style coordinate lists, unquoted
enum values) that PyYAML would not reproduce byte-for-byte.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

MovementType = Literal["cut", "pass", "screen", "dribble", "handoff"]

# Confidence bucketing thresholds — matches the task spec.
_HIGH_THRESHOLD = 0.75
_MEDIUM_THRESHOLD = 0.5


@dataclass
class EmittedPlayer:
    digit: str                        # "1" .. "5"
    svg_pos: tuple[float, float]      # starting position in SVG units


@dataclass
class EmittedMovement:
    player_id: str                    # "1".."5"
    type: MovementType
    from_svg: tuple[float, float] | None
    to_svg: tuple[float, float] | None
    to_player_id: str | None
    via_svg: tuple[float, float] | None
    confidence: float                 # 0..1 (bucketed into low/medium/high)


@dataclass
class PlaySource:
    book: str                         # "BasketballForCoaches.com"
    play_name: str                    # extracted title or "Unknown"
    page: int                         # PDF page number
    panel: int                        # which diagram panel on that page


# ---------- formatting helpers ----------

def _fmt_coord(value: float) -> str:
    """Format a single coordinate with 1 decimal place.

    ``-0.0`` is normalized to ``0.0`` so we never emit negative zero.
    """
    if value == 0:
        value = 0.0
    formatted = f"{value:.1f}"
    if formatted == "-0.0":
        formatted = "0.0"
    return formatted


def _fmt_point(point: tuple[float, float]) -> str:
    x, y = point
    return f"[{_fmt_coord(x)}, {_fmt_coord(y)}]"


def _bucket_confidence(score: float) -> str:
    if score >= _HIGH_THRESHOLD:
        return "high"
    if score >= _MEDIUM_THRESHOLD:
        return "medium"
    return "low"


def _escape_description(text: str) -> str:
    """Escape a phase description for inclusion in a double-quoted YAML scalar."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _default_phase_description(movement: EmittedMovement) -> str:
    """Build a terse description when none is supplied.

    We intentionally keep this mechanical — the CV layer should not
    invent coaching prose. Descriptions come from the source PDF text
    when available; otherwise we emit a structural placeholder.
    """
    verb = {
        "pass": "passes to",
        "handoff": "hands off to",
        "screen": "sets a screen",
        "cut": "cuts",
        "dribble": "dribbles",
    }[movement.type]

    if movement.type in ("pass", "handoff") and movement.to_player_id:
        return f"{movement.player_id} {verb} {movement.to_player_id}."
    if movement.type == "screen":
        return f"{movement.player_id} {verb}."
    return f"{movement.player_id} {verb}."


# ---------- core emitter ----------

def emit_yaml(
    players: list[EmittedPlayer],
    movements: list[EmittedMovement],
    source: PlaySource,
    phase_labels: list[str] | None = None,
    phase_texts: list[str] | None = None,
) -> str:
    """Render the play as a YAML string wrapped in a ```yaml fence.

    Phase grouping rule (simple, deterministic):

    * If ``phase_labels`` is provided, it defines the phase boundaries
      and there MUST be exactly ``len(phase_labels)`` groupings. We map
      movements to phases positionally: movement ``i`` goes into phase
      ``min(i, len(phase_labels) - 1)`` when the counts match, otherwise
      one movement per phase.
    * Default: one movement per phase, labels auto-generated as
      ``"Phase {n}"``.

    The ``phase_texts`` list (if provided) is zipped 1:1 with
    ``phase_labels``. Missing descriptions fall back to a mechanical
    sentence derived from the movement.
    """

    # ----- validation -----
    if not players:
        raise ValueError("emit_yaml requires at least one player")
    if phase_texts is not None and phase_labels is None:
        raise ValueError("phase_texts requires phase_labels")
    if (
        phase_labels is not None
        and phase_texts is not None
        and len(phase_labels) != len(phase_texts)
    ):
        raise ValueError("phase_labels and phase_texts must be the same length")

    # ----- determine phase grouping -----
    if phase_labels is None:
        # One phase per movement.
        phase_groups: list[list[EmittedMovement]] = [[m] for m in movements]
        labels = [f"Phase {i + 1}" for i in range(len(movements))]
        texts: list[str | None] = [None] * len(movements)
    else:
        labels = list(phase_labels)
        texts = list(phase_texts) if phase_texts is not None else [None] * len(labels)
        phase_groups = [[] for _ in labels]
        # Simple positional mapping: movement i -> phase min(i, last).
        last = len(labels) - 1
        for i, mvmt in enumerate(movements):
            phase_groups[min(i, last)].append(mvmt)

    # ----- build lines -----
    lines: list[str] = []
    lines.append("```yaml")
    lines.append("play:")
    lines.append(f"  name: {source.play_name}")
    lines.append("  tag: 5-out")
    lines.append("  players:")

    # Sort players by numeric digit for stable output.
    sorted_players = sorted(players, key=lambda p: int(p.digit))
    for player in sorted_players:
        lines.append(f'    "{player.digit}": {_fmt_point(player.svg_pos)}')

    # Ball start = first player (lowest digit) by default; the ball's
    # true owner is the `player_id` of the first movement when that
    # movement is a pass/handoff/dribble. Fall back to "1".
    ball_start = "1"
    if movements:
        ball_start = movements[0].player_id
    lines.append(f'  ball_start: "{ball_start}"')

    lines.append("  phases:")

    for label, description_override, group in zip(labels, texts, phase_groups):
        lines.append(f'    - label: "{label}"')
        if description_override is not None:
            description = description_override
        elif group:
            description = _default_phase_description(group[0])
        else:
            description = f"{label}."
        lines.append(f'      description: "{_escape_description(description)}"')
        lines.append("      movements:")
        if not group:
            # Empty phases are unusual but legal — emit an explicit empty list.
            lines[-1] = "      movements: []"
            continue

        for mvmt in group:
            lines.append(f'        - player: "{mvmt.player_id}"')
            if mvmt.from_svg is not None:
                lines.append(f"          from: {_fmt_point(mvmt.from_svg)}")
            if mvmt.to_player_id is not None:
                lines.append(f'          to_player: "{mvmt.to_player_id}"')
            if mvmt.to_svg is not None:
                lines.append(f"          to: {_fmt_point(mvmt.to_svg)}")
            if mvmt.via_svg is not None:
                lines.append(f"          via: {_fmt_point(mvmt.via_svg)}")
            lines.append(f"          type: {mvmt.type}")
            lines.append(
                f"          confidence: {_bucket_confidence(mvmt.confidence)}"
            )

    lines.append("```")
    # Reference files end with a newline after the closing fence.
    return "\n".join(lines) + "\n"


# ---------- file-writing wrapper ----------

def write_yaml_for_panel(
    players: list[EmittedPlayer],
    movements: list[EmittedMovement],
    source: PlaySource,
    output_dir: str = "results/extractions_cv",
) -> str:
    """Write the rendered YAML to disk and return the absolute path.

    Filename format:
        ``diagram_<PP>_page_<NNN>_panel_<M>_cv.yaml``

    where ``PP`` is the panel-indexed diagram id (we use ``panel+1``
    zero-padded to 2 digits — matches the existing ``diagram_01_...``
    convention), ``NNN`` is the zero-padded page number, and ``M`` is
    the raw panel index.
    """
    yaml_text = emit_yaml(players, movements, source)

    diagram_id = f"{source.panel + 1:02d}"
    page_id = f"{source.page:03d}"
    filename = (
        f"diagram_{diagram_id}_page_{page_id}_panel_{source.panel}_cv.yaml"
    )

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.abspath(os.path.join(output_dir, filename))
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(yaml_text)
    return path


# ---------- sanity harness ----------

if __name__ == "__main__":
    players = [
        EmittedPlayer(digit="1", svg_pos=(0.0, 30.8)),
        EmittedPlayer(digit="2", svg_pos=(-17.8, 20.8)),
        EmittedPlayer(digit="3", svg_pos=(18.3, 20.4)),
        EmittedPlayer(digit="4", svg_pos=(-22.3, 6.6)),
        EmittedPlayer(digit="5", svg_pos=(22.5, 6.4)),
    ]
    movements = [
        EmittedMovement(
            player_id="1",
            type="pass",
            to_player_id="2",
            from_svg=None,
            to_svg=None,
            via_svg=None,
            confidence=0.9,
        ),
        EmittedMovement(
            player_id="4",
            type="screen",
            from_svg=(-22.3, 6.6),
            to_svg=(-14.0, 22.0),
            to_player_id=None,
            via_svg=None,
            confidence=0.85,
        ),
        EmittedMovement(
            player_id="2",
            type="dribble",
            from_svg=(-17.8, 20.8),
            to_svg=(-5.0, 5.0),
            to_player_id=None,
            via_svg=None,
            confidence=0.9,
        ),
        EmittedMovement(
            player_id="5",
            type="cut",
            from_svg=(22.5, 6.4),
            to_svg=(2.0, 13.0),
            to_player_id=None,
            via_svg=None,
            confidence=0.9,
        ),
        EmittedMovement(
            player_id="2",
            type="pass",
            to_player_id="5",
            from_svg=None,
            to_svg=None,
            via_svg=None,
            confidence=0.8,
        ),
    ]
    source = PlaySource(
        book="BasketballForCoaches.com",
        play_name="Black",
        page=60,
        panel=0,
    )

    yaml_text = emit_yaml(players, movements, source)
    print(yaml_text)

    path = write_yaml_for_panel(players, movements, source)
    print(f"wrote: {path}")
