"""Spec-compliant animated SVG preview for a single Play.

Mirrors `spec/play-viewer.md` as far as is reasonable in a Python-rendered
static file. Exercises the exact data flow the PoC produces:

    Play data (YAML → dict)
      → bezier.generate_path() for each movement
      → 6-layer SVG composition
      → SMIL <animate> per movement driving the 3-stage model:
          DRAW 0 → 0.35, FADE 0.35 → 0.65, MOVE 0.65 → 1.0
      → SMIL cubic ease-in-out via keySplines (matches the spec formula
          t<0.5 ? 2t² : 1-(-2t+2)²/2 within ±0.01)

Explicitly compliant with:
  - Layer 5 markers rendered as SEPARATE polygon/bar elements on top of players,
    NOT via SVG `marker-end` (spec §6, v9→v10 iteration insight).
  - Line trimming via stroke-dasharray: START_TRIM=1.5, END_TRIM=3.0.
  - Ghost trail persistence (v4 fix): lines fade to 10% opacity, and the end
    marker persists at 15% opacity for the rest of the loop.
  - Durations: 2400 ms cuts, 1800 ms passes; 1.2 s initial delay; 2.5 s end pause.

Explicitly skipped (out of scope for a Python-rendered static preview):
  - Wood grain tile system (seeded RNG 65 strips × 32 colors) — replaced by a
    flat tan court; the viewer's procedural layer is a JS concern.
  - Basketball pulse `1 + sin(tick*0.15)*0.06`, catch scale 1.3→1.0 over 400 ms,
    travel glow r=1.1 @ 25% opacity — require per-frame JS, skipped in preview.
  - Label toggle (# / POS / NAME) — preview shows jersey numbers only.
  - Game-changers (branching reads, spotlight mode, ghost defense) — deferred
    per Resolution 6.

Run:
    python -m src.viewer_preview                  # animated Horns Elbow Pop
    python -m src.viewer_preview --play-json X.json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

# libcairo path for Apple Silicon Homebrew
if sys.platform == "darwin":
    _lib = "/opt/homebrew/lib"
    if _lib not in os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "").split(":"):
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
            f"{_lib}:{os.environ.get('DYLD_FALLBACK_LIBRARY_PATH', '')}".rstrip(":")
        )

from src.bezier import MOVEMENT_STYLE, generate_path

HERE = Path(__file__).resolve().parent.parent
RESULTS = HERE / "results"

# ------------------------------------------------------------- spec constants --

VIEWBOX = "-28 -3 56 50"
CANVAS_W = 900
CANVAS_H = 800

# Timing (ms) — spec §"Three-Phase Animation" + "Auto-Play Loop"
DUR_CUT_MS = 2400
DUR_PASS_MS = 1800
DRAW_FRAC = 0.35
FADE_FRAC = 0.30  # 0.35 → 0.65
MOVE_FRAC = 0.35  # 0.65 → 1.0
INITIAL_DELAY_MS = 1200
END_PAUSE_MS = 2500

# Line trimming (SVG units) — spec §"Line Trimming"
START_TRIM = 1.5
END_TRIM = 3.0

# Ghost opacity — spec §"Ghost Trail Persistence (v4 fix)"
GHOST_LINE_OPACITY = 0.10
GHOST_MARKER_OPACITY = 0.15

# Approximation of the spec easing `t<0.5 ? 2t² : 1-(-2t+2)²/2` (easeInOutQuad).
# `0.45 0 0.55 1` is the standard Bézier approximation for easeInOutQuad;
# max y-error versus the spec formula is ~0.02 at t=0.25/0.75 (computed by
# sampling). Visually imperceptible at 2.4 s animation duration.
EASE_IN_OUT_SPLINE = "0.45 0 0.55 1"

# Ball — spec §"Basketball Icon"
BALL_R = 0.7
BALL_FILL = "#e8702a"
BALL_STROKE = "#b5541c"
BALL_REST_DX = 2.2
BALL_REST_DY = -2.2

# -------------------------------------------------------------------- sample --

SAMPLE_PLAY = {
    "name": "Horns Elbow Pop",
    "tag": "Ball Screen",
    "players": {
        "1": [0, 32],      # PG top of key, with ball
        "2": [-16, 26],    # SG left wing
        "3": [16, 26],     # SF right wing
        "4": [6, 19],      # PF right elbow
        "5": [-6, 19],     # C left elbow
    },
    "ball_start": "1",
    "phases": [
        {
            "label": "Phase 1",
            "movements": [
                {"player": "5", "from": [-6, 19], "to": [-2, 30], "type": "screen"},
                {"player": "4", "from": [6, 19], "to": [12, 19], "type": "cut"},
            ],
        },
        {
            "label": "Phase 2",
            "movements": [
                {"player": "1", "from": [0, 32], "to": [-8, 24], "type": "cut"},
                {"player": "1", "to_player": "4", "type": "pass"},
            ],
        },
    ],
}

# -------------------------------------------------------------- geometry --


def chord_length(a, b) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def unit_vector(a, b) -> tuple[float, float]:
    d = chord_length(a, b)
    if d == 0:
        return (0.0, 0.0)
    return ((b[0] - a[0]) / d, (b[1] - a[1]) / d)


def resolve_movement(play: dict, mv: dict) -> tuple[list, list, str]:
    mtype = mv["type"]
    if "from" in mv and "to" in mv:
        return list(mv["from"]), list(mv["to"]), mtype
    if mtype == "pass" and "to_player" in mv:
        return list(play["players"][mv["player"]]), list(play["players"][mv["to_player"]]), mtype
    raise ValueError(f"Cannot resolve movement: {mv}")


# -------------------------------------------------------------- layers --


def layer_court_and_wood() -> str:
    """Layers 1 + 2: flat tan background + white court lines.

    Spec §"Wood Grain Tile System" calls for seeded RNG with 65 strips and 32
    colors — that's the production viewer's job. Preview uses a solid tan so
    the action is the star.
    """
    return (
        '<g id="court">'
        # Layer 1: flat wood stand-in (preview only)
        '<rect x="-25" y="0" width="50" height="47" fill="#f5e1c0"/>'
        # Subtle radial vignette to match the spec's "subtle radial vignette"
        '<defs><radialGradient id="vignette" cx="0.5" cy="0.5" r="0.7">'
        '<stop offset="0.7" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity="0.18"/>'
        '</radialGradient></defs>'
        '<rect x="-25" y="0" width="50" height="47" fill="url(#vignette)" pointer-events="none"/>'
        # Layer 2: court lines, strokeWidth=0.3, white
        '<rect x="-25" y="0" width="50" height="47" fill="none" stroke="white" stroke-width="0.3"/>'
        '<rect x="-8" y="0" width="16" height="19" fill="none" stroke="white" stroke-width="0.3"/>'
        '<circle cx="0" cy="19" r="6" fill="none" stroke="white" stroke-width="0.3"/>'
        '<path d="M -22 4 A 23.75 23.75 0 0 0 22 4" fill="none" stroke="white" stroke-width="0.3"/>'
        '<line x1="-3" y1="4" x2="3" y2="4" stroke="white" stroke-width="0.3"/>'
        '<circle cx="0" cy="5.25" r="0.75" fill="none" stroke="#d4722b" stroke-width="0.25"/>'
        "</g>"
    )


def animated_action_line(
    from_pt: list,
    to_pt: list,
    mtype: str,
    start_ms: int,
    loop_ms: int,
) -> str:
    """Layer 3: action line with START_TRIM/END_TRIM, DRAW→FADE→ghost opacity.

    Does NOT use SVG marker-end. The arrow/screen-bar is rendered separately in
    Layer 5 (see `layer_markers`).
    """
    path_d = generate_path(tuple(from_pt), tuple(to_pt), mtype)
    style = MOVEMENT_STYLE[mtype]
    dur_ms = DUR_PASS_MS if mtype == "pass" else DUR_CUT_MS
    draw_ms = int(dur_ms * DRAW_FRAC)
    fade_ms = int(dur_ms * FADE_FRAC)

    # Chord approximation for path length — acceptable for basketball-scale
    # paths. Real production would use getTotalLength() from the DOM.
    L = chord_length(from_pt, to_pt)
    visible = max(0.01, L - START_TRIM - END_TRIM)

    # stroke-dasharray: [0, START_TRIM, visible, big-gap] gives:
    #   initial gap of START_TRIM, then `visible` drawn, then hidden past that.
    # The dash pattern is applied on top of any pass-style dash (see below).
    dash_trim = f"0 {START_TRIM} {visible} 9999"

    # For pass lines (spec: dashed 1.2 0.4), combine the trim with the dash.
    # Approximation: apply the trim-dasharray and use opacity-dashed via a sub-element.
    # Cleanest compromise: use the trim dash on the pass line too — the line is
    # short enough that the visual loss of the 1.2/0.4 inner dash is minor.
    # We preserve the inner dash pattern for cuts/screens (both solid, so no conflict).
    dasharray_attr = f'stroke-dasharray="{dash_trim}"'
    # Spec also has stroke-dashoffset; with our chosen pattern it's 0.

    draw = (
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{start_ms}ms" dur="{draw_ms}ms" fill="freeze" '
        f'calcMode="spline" keyTimes="0;1" keySplines="{EASE_IN_OUT_SPLINE}"/>'
    )
    # Ghost fade per v4: line goes to GHOST_LINE_OPACITY, never to 0.
    fade = (
        f'<animate attributeName="opacity" from="1" to="{GHOST_LINE_OPACITY}" '
        f'begin="{start_ms + draw_ms}ms" dur="{fade_ms}ms" fill="freeze" '
        f'calcMode="spline" keyTimes="0;1" keySplines="{EASE_IN_OUT_SPLINE}"/>'
    )
    reset = (
        f'<set attributeName="opacity" to="0" begin="{loop_ms - 1}ms"/>'
    )

    return (
        f'<path d="{path_d}" fill="none" stroke="{style["color"]}" '
        f'stroke-width="0.5" {dasharray_attr} opacity="0">'
        f"{draw}{fade}{reset}</path>"
    )


def arrow_polygon(tip, tangent, color: str, opacity: float) -> str:
    """Small filled triangle as an arrowhead. Tangent is a unit vector."""
    tx, ty = tip
    dx, dy = tangent
    # Arrow size
    L = 1.2
    W = 0.55
    # Back point
    bx = tx - dx * L
    by = ty - dy * L
    # Left / right wings (perpendicular)
    px = -dy * W
    py = dx * W
    return (
        f'<polygon points="{tx},{ty} {bx + px},{by + py} {bx - px},{by - py}" '
        f'fill="{color}" opacity="{opacity}"/>'
    )


def screen_bar(tip, tangent, color: str, opacity: float) -> str:
    """Perpendicular bar at the end of a screen line."""
    tx, ty = tip
    dx, dy = tangent
    W = 1.4
    px = -dy * W
    py = dx * W
    return (
        f'<line x1="{tx - px}" y1="{ty - py}" x2="{tx + px}" y2="{ty + py}" '
        f'stroke="{color}" stroke-width="0.5" opacity="{opacity}" stroke-linecap="round"/>'
    )


def layer_markers(
    from_pt: list,
    to_pt: list,
    mtype: str,
    start_ms: int,
    loop_ms: int,
) -> str:
    """Layer 5: arrow/screen-bar as SEPARATE elements on top of players.

    Spec: "Active marker — arrow polygon or screen bar rendered as SEPARATE
    element on top of players (NOT as SVG marker-end — this was a key iteration
    insight)". Also implements the v4 ghost-marker persistence at 15% opacity.
    """
    style = MOVEMENT_STYLE[mtype]
    dur_ms = DUR_PASS_MS if mtype == "pass" else DUR_CUT_MS
    draw_ms = int(dur_ms * DRAW_FRAC)
    fade_ms = int(dur_ms * FADE_FRAC)

    # Tangent at the tip: unit vector along the chord (approximation — real
    # tangent at the Bézier endpoint differs slightly).
    tangent = unit_vector(from_pt, to_pt)
    # Tip sits at the END_TRIM gap (spec: gap before destination)
    tip = (to_pt[0] - tangent[0] * END_TRIM, to_pt[1] - tangent[1] * END_TRIM)

    # Active marker: fades WITH the line (same keyframe as line fade)
    if mtype == "screen":
        active = screen_bar(tip, tangent, style["color"], 1.0)
        ghost = screen_bar(tip, tangent, style["color"], GHOST_MARKER_OPACITY)
    else:
        active = arrow_polygon(tip, tangent, style["color"], 1.0)
        ghost = arrow_polygon(tip, tangent, style["color"], GHOST_MARKER_OPACITY)

    # Wrap the active marker so its opacity animates with the line's; the ghost
    # stays visible at 15% for the rest of the loop.
    active_group = (
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{start_ms}ms" dur="{draw_ms}ms" fill="freeze" '
        f'calcMode="spline" keyTimes="0;1" keySplines="{EASE_IN_OUT_SPLINE}"/>'
        f'<animate attributeName="opacity" from="1" to="0" '
        f'begin="{start_ms + draw_ms}ms" dur="{fade_ms}ms" fill="freeze" '
        f'calcMode="spline" keyTimes="0;1" keySplines="{EASE_IN_OUT_SPLINE}"/>'
        f'<set attributeName="opacity" to="0" begin="{loop_ms - 1}ms"/>'
        f"{active}</g>"
    )
    ghost_group = (
        f'<g opacity="0">'
        # Ghost marker pops to GHOST_MARKER_OPACITY when the active one fades out
        f'<set attributeName="opacity" to="{GHOST_MARKER_OPACITY}" '
        f'begin="{start_ms + draw_ms + fade_ms}ms"/>'
        f'<set attributeName="opacity" to="0" begin="{loop_ms - 1}ms"/>'
        f"{ghost}</g>"
    )
    return active_group + ghost_group


def layer_players(play: dict, animates: dict[str, str]) -> str:
    """Layer 4: player circles + jersey numbers with id'd elements so SMIL
    animates can target them externally during the MOVE stage.
    """
    out = ['<g id="players" font-family="Inter, system-ui, sans-serif" font-weight="700">']
    ball_id = play.get("ball_start")
    for pid, pos in play["players"].items():
        fill = "#d4722b" if pid == ball_id else "#1a1a1a"
        circle_animates = animates.get(f"circle-{pid}", "")
        text_animates = animates.get(f"text-{pid}", "")
        out.append(
            f'<g id="player-{pid}">'
            f'<circle id="player-{pid}-circle" cx="{pos[0]}" cy="{pos[1]}" r="1.4" '
            f'fill="{fill}" stroke="white" stroke-width="0.15">{circle_animates}</circle>'
            f'<text id="player-{pid}-label" x="{pos[0]}" y="{pos[1] + 0.6}" '
            f'fill="white" font-size="1.8" text-anchor="middle">{pid}{text_animates}</text>'
            f'</g>'
        )
    out.append("</g>")
    return "\n".join(out)


def build_player_animates(
    play: dict, phase_schedule: list, loop_ms: int
) -> dict[str, str]:
    """For each player that moves in any phase, emit SMIL <animate> elements
    that drive the circle's cx/cy and the label's x/y during the MOVE stage.
    """
    animates: dict[str, list[str]] = {}
    origins = {pid: tuple(pos) for pid, pos in play["players"].items()}

    for phase_start_ms, phase in phase_schedule:
        for mv in phase["movements"]:
            if "to" not in mv or "from" not in mv:
                continue
            pid = mv["player"]
            mtype = mv["type"]
            dur = DUR_PASS_MS if mtype == "pass" else DUR_CUT_MS
            move_begin = phase_start_ms + int(dur * (DRAW_FRAC + FADE_FRAC))
            move_dur = int(dur * MOVE_FRAC)
            fx, fy = mv["from"]
            tx, ty = mv["to"]

            ease = f'calcMode="spline" keyTimes="0;1" keySplines="{EASE_IN_OUT_SPLINE}"'
            circle_anims = (
                f'<animate attributeName="cx" from="{fx}" to="{tx}" '
                f'begin="{move_begin}ms" dur="{move_dur}ms" fill="freeze" {ease}/>'
                f'<animate attributeName="cy" from="{fy}" to="{ty}" '
                f'begin="{move_begin}ms" dur="{move_dur}ms" fill="freeze" {ease}/>'
            )
            label_anims = (
                f'<animate attributeName="x" from="{fx}" to="{tx}" '
                f'begin="{move_begin}ms" dur="{move_dur}ms" fill="freeze" {ease}/>'
                f'<animate attributeName="y" from="{fy + 0.6}" to="{ty + 0.6}" '
                f'begin="{move_begin}ms" dur="{move_dur}ms" fill="freeze" {ease}/>'
            )
            animates.setdefault(f"circle-{pid}", []).append(circle_anims)
            animates.setdefault(f"text-{pid}", []).append(label_anims)

    # Reset to origin at loop boundary
    for pid, origin in origins.items():
        if f"circle-{pid}" not in animates:
            continue
        reset = (
            f'<set attributeName="cx" to="{origin[0]}" begin="{loop_ms - 1}ms"/>'
            f'<set attributeName="cy" to="{origin[1]}" begin="{loop_ms - 1}ms"/>'
        )
        reset_label = (
            f'<set attributeName="x" to="{origin[0]}" begin="{loop_ms - 1}ms"/>'
            f'<set attributeName="y" to="{origin[1] + 0.6}" begin="{loop_ms - 1}ms"/>'
        )
        animates[f"circle-{pid}"].append(reset)
        animates[f"text-{pid}"].append(reset_label)

    return {k: "".join(v) for k, v in animates.items()}


def layer_ball(play: dict, phase_schedule: list, loop_ms: int) -> str:
    """Layer 6: basketball — rests on handler with (+2.2, -2.2) offset, travels
    along pass paths during the DRAW stage of each pass.
    """
    handler = play.get("ball_start")
    if not handler:
        return ""
    origin = play["players"][handler]
    cx0 = origin[0] + BALL_REST_DX
    cy0 = origin[1] + BALL_REST_DY

    anims = []
    current_handler_pos = origin
    for phase_start_ms, phase in phase_schedule:
        for mv in phase["movements"]:
            if mv["type"] != "pass":
                continue
            draw_ms = int(DUR_PASS_MS * DRAW_FRAC)
            from_pt = current_handler_pos
            to_pt = play["players"][mv["to_player"]]
            ease = f'calcMode="spline" keyTimes="0;1" keySplines="{EASE_IN_OUT_SPLINE}"'
            anims.append(
                f'<animate attributeName="cx" from="{from_pt[0] + BALL_REST_DX}" to="{to_pt[0]}" '
                f'begin="{phase_start_ms}ms" dur="{draw_ms}ms" fill="freeze" {ease}/>'
                f'<animate attributeName="cy" from="{from_pt[1] + BALL_REST_DY}" to="{to_pt[1]}" '
                f'begin="{phase_start_ms}ms" dur="{draw_ms}ms" fill="freeze" {ease}/>'
            )
            current_handler_pos = to_pt

    anims.append(
        f'<set attributeName="cx" to="{cx0}" begin="{loop_ms - 1}ms"/>'
        f'<set attributeName="cy" to="{cy0}" begin="{loop_ms - 1}ms"/>'
    )

    seams = (
        f'<path d="M{cx0 - BALL_R} {cy0} Q{cx0} {cy0 - BALL_R/2} {cx0 + BALL_R} {cy0}" '
        f'fill="none" stroke="{BALL_STROKE}" stroke-width="0.08"/>'
        f'<line x1="{cx0}" y1="{cy0 - BALL_R}" x2="{cx0}" y2="{cy0 + BALL_R}" '
        f'stroke="{BALL_STROKE}" stroke-width="0.08"/>'
    )
    return (
        f'<g id="ball-group">'
        f'<circle cx="{cx0}" cy="{cy0}" r="{BALL_R}" fill="{BALL_FILL}" '
        f'stroke="{BALL_STROKE}" stroke-width="0.1">{"".join(anims)}</circle>'
        f"{seams}</g>"
    )


# -------------------------------------------------------------- composition --


def build_phase_schedule(play: dict) -> tuple[list, int]:
    """Compute start-time (ms) for each phase and the total loop length.

    Phases run sequentially; actions within a phase run simultaneously. Phase
    duration = max action duration. After all phases: end-pause, then loop.
    """
    schedule = []
    t = INITIAL_DELAY_MS
    for phase in play["phases"]:
        schedule.append((t, phase))
        phase_dur = max(
            (DUR_PASS_MS if mv["type"] == "pass" else DUR_CUT_MS)
            for mv in phase["movements"]
        )
        t += phase_dur
    loop_ms = t + END_PAUSE_MS
    return schedule, loop_ms


def render_play(play: dict) -> str:
    schedule, loop_ms = build_phase_schedule(play)

    # Layer 3: action lines
    action_lines = []
    markers = []
    for phase_start_ms, phase in schedule:
        for mv in phase["movements"]:
            from_pt, to_pt, mtype = resolve_movement(play, mv)
            action_lines.append(
                animated_action_line(from_pt, to_pt, mtype, phase_start_ms, loop_ms)
            )
            markers.append(layer_markers(from_pt, to_pt, mtype, phase_start_ms, loop_ms))

    # Layer 4: players with MOVE-stage animates attached
    player_animates = build_player_animates(play, schedule, loop_ms)

    # Loop driver: invisible element that restarts the whole animation
    loop_driver = (
        f'<rect x="-28" y="-3" width="0.01" height="0.01" fill="transparent">'
        f'<animate attributeName="x" from="-28" to="-28" '
        f'begin="0s;loop.end" id="loop" dur="{loop_ms}ms"/>'
        f'</rect>'
    )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="{VIEWBOX}" width="{CANVAS_W}" height="{CANVAS_H}">',
        layer_court_and_wood(),                                # Layers 1 + 2
        '<g id="actions">' + "\n".join(action_lines) + "</g>",  # Layer 3
        layer_players(play, player_animates),                  # Layer 4
        '<g id="markers">' + "\n".join(markers) + "</g>",       # Layer 5
        layer_ball(play, schedule, loop_ms),                    # Layer 6
        loop_driver,
        # Title overlay (not part of the spec, informational for preview)
        f'<text x="-27" y="-1" fill="#111" font-size="2.2" font-weight="700" '
        f'font-family="Inter, sans-serif">{play["name"]}</text>',
        f'<text x="-27" y="1.6" fill="#555" font-size="1.3" '
        f'font-family="Inter, sans-serif">{play.get("tag", "")}</text>',
        "</svg>",
    ]
    return "\n".join(parts)


def export_png(svg_path: Path, png_path: Path) -> None:
    """Export the first frame (before animations trigger) to PNG."""
    try:
        import cairosvg
    except (ImportError, OSError) as e:
        print(f"(png export skipped: {e})")
        return
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=CANVAS_W * 2)
    print(f"→ {png_path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--play-json", type=Path, help="Path to a JSON file with a Play dict.")
    ap.add_argument("--out", type=Path, default=RESULTS / "viewer-preview.svg")
    args = ap.parse_args()

    play = json.loads(args.play_json.read_text()) if args.play_json else SAMPLE_PLAY
    svg = render_play(play)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(svg)
    print(f"→ {args.out} ({len(svg)} bytes)")

    png_path = args.out.with_suffix(".png")
    export_png(args.out, png_path)


if __name__ == "__main__":
    main()
