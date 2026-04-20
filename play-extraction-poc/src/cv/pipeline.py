"""End-to-end CV pipeline integration — wires the 4 modules together.

Current state: the ARROW DETECTOR (src/cv/arrows.py) is still in flight.
This runner substitutes HAND-STUBBED arrow paths for page 60 "Black" so we can
exercise the full strokes → assemble → emit chain and prove the interfaces
compose. Once arrows.py lands, only the `stub_arrows_for_black()` call needs
to be replaced with `arrows.detect_arrows(bgr, player_bboxes)`.

Run:
    python -m src.cv.pipeline         # processes page 60 end-to-end
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import pdfplumber

from . import arrows as arrows_module
from .assemble import (
    DetectedArrow as AssembleArrow,
    DetectedPlayer,
    assemble_movements,
)
from .emit import (
    EmittedMovement,
    EmittedPlayer,
    PlaySource,
    write_yaml_for_panel,
)
from .probe import detect_glyph_candidates, ocr_digit, reconcile_labels
from .registration import pixel_to_svg, register_court
from .strokes import classify_stroke

HERE = Path(__file__).resolve().parent.parent.parent
PDF = HERE.parent / "knowledge-base" / "raw" / "basketball-for-coaches.pdf"


# --------------------------------------------------------- page extraction --

def extract_panel(page_number: int, panel_index: int = 0) -> np.ndarray:
    """Return the BGR image of one diagram panel on the given page."""
    with pdfplumber.open(PDF) as pdf:
        page = pdf.pages[page_number - 1]
        img_meta = page.images[panel_index]
        bbox = (img_meta["x0"], img_meta["top"], img_meta["x1"], img_meta["bottom"])
        pil = page.crop(bbox).to_image(resolution=400).original
    arr = np.array(pil)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


# --------------------------------------------------------- player detection --

def detect_players(bgr: np.ndarray) -> tuple[list[DetectedPlayer], list[tuple[int, int, int, int]]]:
    """Use probe's glyph + OCR pipeline to return DetectedPlayer records + bboxes."""
    cands = detect_glyph_candidates(bgr)
    for c in cands:
        c["digit"] = ocr_digit(bgr, c["bbox"])
    cands = reconcile_labels(cands)

    reg = register_court(bgr)
    players: list[DetectedPlayer] = []
    bboxes: list[tuple[int, int, int, int]] = []
    for c in cands:
        if not c.get("digit"):
            continue
        cx, cy = c["center"]
        if reg is not None:
            sx, sy = pixel_to_svg(reg, cx, cy)
        else:
            sx, sy = (0.0, 0.0)
        players.append(DetectedPlayer(
            digit=c["digit"],
            center_px=(float(cx), float(cy)),
            center_svg=(float(sx), float(sy)),
        ))
        bboxes.append(tuple(c["bbox"]))
    return players, bboxes


# --------------------------------------------------------- stubbed arrows --

def stub_arrows_for_black() -> list[tuple[tuple[float, float], tuple[float, float], list[tuple[float, float]]]]:
    """Temporary stand-in for the arrow detector.

    Returns a list of (start_px, end_px, control_points_px) tuples representing
    the 5 movements in page 60's "Black" play, derived by visual inspection of
    the 1017x962 panel image. Replace with `arrows.detect_arrows(...)` once that
    module lands.
    """
    return [
        # Pass 1 → 2 (dashed)
        ((510.0, 623.0), (163.0, 428.0), [(510, 623), (336, 525), (163, 428)]),
        # Screen by 4 — from corner up to screen position
        ((77.0, 153.0), (270.0, 280.0), [(77, 153), (170, 215), (270, 280)]),
        # Dribble by 2 — zig-zag to the baseline rim area
        ((163.0, 428.0), (430.0, 70.0), [(163, 428), (230, 340), (300, 250), (370, 160), (430, 70)]),
        # Cut by 5 — flash into the key
        ((946.0, 149.0), (600.0, 200.0), [(946, 149), (770, 175), (600, 200)]),
        # Pass 2 → 5 (dashed, after 2 has dribbled)
        ((430.0, 70.0), (600.0, 200.0), [(430, 70), (515, 135), (600, 200)]),
    ]


# --------------------------------------------------------- full pipeline --

def process_page(page_number: int, panel_index: int = 0) -> Path | None:
    print(f"\n=== page {page_number} panel {panel_index} ===")
    bgr = extract_panel(page_number, panel_index)
    h, w = bgr.shape[:2]
    print(f"image: {w}×{h} px")

    # 1. Detect players + registration
    players, bboxes = detect_players(bgr)
    reg = register_court(bgr)
    if reg is None:
        print("  ERROR: court registration failed — cannot proceed")
        return None
    print(f"  players: {len(players)} detected")
    for p in players:
        print(f"    P{p.digit}: px{p.center_px} → SVG{p.center_svg}")

    # 2. Detect arrows via CV
    raw_arrows = arrows_module.detect_arrows(bgr, bboxes)
    print(f"  arrows: {len(raw_arrows)} detected")

    # 3. Classify each arrow. Trust the arrow detector's `kind` as the primary
    #    source (it has full-image context: bar blobs, arrowhead shape, global
    #    dash pattern). strokes.py is only a tiebreaker when kind is "unknown",
    #    because its detrended-variance logic is easily fooled by the greedy
    #    tracer's small perpendicular jitter.
    _KIND_TO_TYPE = {
        "solid": "cut",
        "dashed": "pass",
        "zigzag": "dribble",
        "screen": "screen",
    }
    detected: list[AssembleArrow] = []
    for a in raw_arrows:
        if a.kind in _KIND_TO_TYPE:
            mtype = _KIND_TO_TYPE[a.kind]
            conf = a.confidence
            src = f"detector.kind={a.kind}"
        else:
            mtype, stroke_conf, _feats = classify_stroke(bgr, a.control_points)
            conf = min(a.confidence, stroke_conf) if stroke_conf else a.confidence
            src = f"strokes.fallback={mtype}"
        detected.append(AssembleArrow(
            start_px=a.start_px,
            end_px=a.end_px,
            control_points_px=a.control_points,
            movement_type=mtype,
            confidence=conf,
        ))
        print(f"    arrow px{a.start_px}→{a.end_px}: {src} → {mtype} (conf={conf:.2f})")

    # 4. Assemble movements (associate arrows with players)
    movements = assemble_movements(players, detected, reg.homography)
    print(f"  assembled: {len(movements)} movements")
    for m in movements:
        print(f"    #{m.raw_arrow_ref}: P{m.player_id} {m.type} → "
              f"{('P' + m.to_player_id) if m.to_player_id else m.to_svg}")

    # 5. Emit YAML (CV-shape, matches the existing extraction format)
    emitted_players = [EmittedPlayer(digit=p.digit, svg_pos=p.center_svg) for p in players]
    emitted_movements = [
        EmittedMovement(
            player_id=m.player_id,
            type=m.type,
            from_svg=m.from_svg,
            to_svg=m.to_svg,
            to_player_id=m.to_player_id,
            via_svg=m.via_svg,
            confidence=m.confidence,
        )
        for m in movements
    ]
    source = PlaySource(
        book="BasketballForCoaches.com",
        play_name="Black" if page_number == 60 else f"page-{page_number}",
        page=page_number,
        panel=panel_index,
    )
    path = write_yaml_for_panel(emitted_players, emitted_movements, source)
    print(f"  YAML: {path}")
    return Path(path)


def main() -> int:
    pages = [int(arg) for arg in sys.argv[1:]] or [60]
    for page in pages:
        process_page(page)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
