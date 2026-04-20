"""Trace each head individually to see what happens."""
from __future__ import annotations

import cv2
import numpy as np

from src.cv.arrows import (
    _binarize,
    _mask_players_and_outer,
    _mask_court_features,
    _find_arrowheads,
    _find_screen_bars,
    _erode_for_tips,
    _tip_and_base,
    _trace_stroke,
    _is_dashed,
    _is_zigzag,
    _load_page_60_panel_0,
    _TRACE_STEP,
    _TRACE_SEARCH_RADIUS,
    _TRACE_MAX_STEPS,
    _TRACE_MAX_DIVERGING_STEPS,
    _TRACE_MAX_LEN_PX,
)
from src.cv.probe import detect_glyph_candidates, ocr_digit


def main() -> int:
    bgr = _load_page_60_panel_0()
    cands = detect_glyph_candidates(bgr)
    player_bboxes = []
    for c in cands:
        if ocr_digit(bgr, c["bbox"]):
            player_bboxes.append(c["bbox"])
    if not player_bboxes:
        player_bboxes = [c["bbox"] for c in cands]

    bw_full = _binarize(bgr)
    bw = _mask_players_and_outer(bw_full, bgr.shape[:2], player_bboxes)

    from src.cv.registration import register_court
    try:
        reg = register_court(bgr)
    except Exception:
        reg = None
    court_mask = _mask_court_features(bw, registration=reg)
    bw_arrows_only = cv2.bitwise_and(bw, cv2.bitwise_not(court_mask))

    heads = _find_arrowheads(bw_arrows_only)
    print(f"{len(heads)} heads")
    stop_regions = []
    for (x, y, cw, ch) in player_bboxes:
        r = int(max(cw, ch) * 1.2)
        cx = x + cw // 2
        cy = y + ch // 2
        stop_regions.append((cx - r, cy - r, r * 2, r * 2))
    for h in heads:
        x, y, cw, ch = h["bbox"]
        stop_regions.append((x - 4, y - 4, cw + 8, ch + 8))

    for i, head in enumerate(heads):
        tip, base = _tip_and_base(head["contour"], bw_uneroded=bw_arrows_only)
        print(f"\n--- head#{i} center={head['center']} tip={tip} base={base}")
        own = head["bbox"]
        own_rect = (own[0] - 4, own[1] - 4, own[2] + 8, own[3] + 8)
        other_stops = [r for r in stop_regions if r != own_rect]
        direction = (base[0] - tip[0], base[1] - tip[1])
        path = _trace_stroke(
            bw_arrows_only,
            start=base,
            direction=direction,
            step=_TRACE_STEP,
            max_steps=_TRACE_MAX_STEPS,
            search_radius=_TRACE_SEARCH_RADIUS,
            stop_regions=other_stops,
            player_bboxes=player_bboxes,
            max_diverging=_TRACE_MAX_DIVERGING_STEPS,
            max_len_px=_TRACE_MAX_LEN_PX,
        )
        print(f"  path len={len(path)}; start={path[0] if path else None} end={path[-1] if path else None}")
        if len(path) >= 2:
            total_len = sum(np.hypot(path[j+1][0]-path[j][0], path[j+1][1]-path[j][1]) for j in range(len(path)-1))
            chord = np.hypot(path[-1][0]-path[0][0], path[-1][1]-path[0][1])
            print(f"  total_len={total_len:.1f} chord={chord:.1f}")
            print(f"  dashed={_is_dashed(bw_full, path)} zigzag={_is_zigzag(path)}")
            for j, p in enumerate(path):
                print(f"    {j}: ({p[0]:.1f},{p[1]:.1f})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
