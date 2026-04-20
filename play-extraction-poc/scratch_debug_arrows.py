"""Scratch debug: print all detected heads + bars for page 60 panel 0."""
from __future__ import annotations

from pathlib import Path
import cv2
import numpy as np

from src.cv.arrows import (
    _binarize,
    _mask_players_and_outer,
    _mask_court_features,
    _find_arrowheads,
    _find_screen_bars,
    _erode_for_tips,
    _load_page_60_panel_0,
    detect_arrows,
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
    print(f"players: {player_bboxes}")

    bw_full = _binarize(bgr)
    bw = _mask_players_and_outer(bw_full, bgr.shape[:2], player_bboxes)

    try:
        from src.cv.registration import register_court
        reg = register_court(bgr)
    except Exception as exc:
        print(f"registration failed: {exc}")
        reg = None

    court_mask = _mask_court_features(bw, registration=reg)
    bw_arrows_only = cv2.bitwise_and(bw, cv2.bitwise_not(court_mask))

    # Save intermediate
    cv2.imwrite("results/cv/debug_bw_arrows.png", bw_arrows_only)
    eroded = _erode_for_tips(bw_arrows_only)
    cv2.imwrite("results/cv/debug_eroded.png", eroded)

    heads = _find_arrowheads(bw_arrows_only)
    bars = _find_screen_bars(bw_arrows_only, heads)
    print(f"\n{len(heads)} arrowhead blobs:")
    for i, h in enumerate(heads):
        print(f"  head#{i}: center={h['center']} bbox={h['bbox']} area={h['area']} solidity={h['solidity']:.2f} fill={h['fill']:.2f}")

    print(f"\n{len(bars)} screen-bar blobs:")
    for i, b in enumerate(bars):
        print(f"  bar#{i}: center={b['center']} bbox={b['bbox']} area={b['area']} aspect={b['aspect']:.2f} fill={b['fill']:.2f}")

    # Also print ALL components in eroded for discovery
    print("\nALL eroded components:")
    num, labels, stats, cents = cv2.connectedComponentsWithStats(eroded, connectivity=8)
    for i in range(1, num):
        x, y, cw, ch, area = stats[i]
        if area < 20:
            continue
        aspect = cw / ch if ch else 0
        fill = area / (cw * ch) if cw * ch else 0
        print(f"  comp#{i}: center=({cents[i][0]:.1f},{cents[i][1]:.1f}) bbox=({x},{y},{cw},{ch}) area={area} aspect={aspect:.2f} fill={fill:.2f}")

    arrows = detect_arrows(bgr, player_bboxes=player_bboxes)
    print(f"\n{len(arrows)} final arrows:")
    for i, a in enumerate(arrows):
        print(f"  #{i}: kind={a.kind} start={a.start_px} end={a.end_px} len={a.length_px:.1f} dashed={a.is_dashed} zigzag={a.is_zigzag} bar={a.has_perpendicular_bar}")

    # All candidate zigzag/complex components
    print("\nAll non-trivial components in bw_arrows (area >= 400, cplx >= 2.5):")
    num2, lbls2, st2, ct2 = cv2.connectedComponentsWithStats(bw_arrows_only, connectivity=8)
    for i in range(1, num2):
        x, y, cw, ch, area = st2[i]
        if area < 400:
            continue
        if max(cw, ch) > 400:
            continue
        comp_mask = (lbls2 == i).astype(np.uint8) * 255
        contours, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        perim = float(sum(cv2.arcLength(c, True) for c in contours))
        bbox_diag = float(np.hypot(cw, ch))
        cplx = perim / max(bbox_diag, 1)
        if cplx < 2.3:
            continue
        print(f"  comp#{i}: bbox=({x},{y},{cw},{ch}) area={area} perim={perim:.0f} cplx={cplx:.1f}")

    # Zigzag strokes via detector
    from src.cv.arrows import _find_zigzag_strokes
    zs = _find_zigzag_strokes(bw_arrows_only, heads, player_bboxes)
    print(f"\n{len(zs)} zigzag strokes (passing filter):")
    for s in zs:
        print(f"  bbox={s['bbox']} area={s['area']} perim={s['perim']:.0f} cplx={s['complexity']:.1f}  endpoints={s['endpoints']} head={'Y' if s['has_head'] else 'N'}")

    # best shaft direction per head
    from src.cv.arrows import _best_shaft_direction, _trace_stroke, _TRACE_STEP, _TRACE_SEARCH_RADIUS, _TRACE_MAX_STEPS, _TRACE_MAX_DIVERGING_STEPS, _TRACE_MAX_LEN_PX
    print(f"\n--- best shaft direction per head ---")
    for i, he in enumerate(heads):
        bd = _best_shaft_direction(bw_arrows_only, he)
        print(f"  head#{i}: center={he['center']}, best_dir={bd}")
        if bd is None:
            continue
        # Simulate the alt trace (on un-masked bw for connectivity)
        hcx, hcy = he['center']
        head_rad = max(he['bbox'][2], he['bbox'][3]) * 0.55
        base_alt = (hcx + bd[0] * head_rad * 0.8, hcy + bd[1] * head_rad * 0.8)
        other_stops = []
        alt_path = _trace_stroke(
            bw,
            start=base_alt,
            direction=bd,
            step=_TRACE_STEP,
            max_steps=_TRACE_MAX_STEPS * 2,
            search_radius=_TRACE_SEARCH_RADIUS + 10,
            stop_regions=other_stops,
            player_bboxes=player_bboxes,
            max_diverging=_TRACE_MAX_DIVERGING_STEPS * 2,
            max_len_px=_TRACE_MAX_LEN_PX,
        )
        print(f"     alt trace len={len(alt_path)}, last={alt_path[-1] if alt_path else None}")
        if len(alt_path) >= 2:
            print(f"     path[:3]: {alt_path[:3]}")
            print(f"     path[-3:]: {alt_path[-3:]}")

    # Per-head tip/base breakdown + triangle vertices
    from src.cv.arrows import _tip_and_base
    print(f"\n--- per-head tip/base ---")
    h_im, w_im = bw_arrows_only.shape
    for i, he in enumerate(heads):
        _, triangle = cv2.minEnclosingTriangle(he["contour"])
        tri = triangle.reshape(3, 2)
        centroid = tri.mean(axis=0)
        # Compute shaft_score for each vertex
        scores = []
        for vi, v in enumerate(tri):
            out_dir = v - centroid
            mag = float(np.linalg.norm(out_dir))
            if mag < 1e-6:
                scores.append(0)
                continue
            out_dir = out_dir / mag
            best_run = 0
            max_r = 24
            for angle_deg in range(-60, 61, 10):
                ang = np.deg2rad(angle_deg)
                rx = out_dir[0] * np.cos(ang) - out_dir[1] * np.sin(ang)
                ry = out_dir[0] * np.sin(ang) + out_dir[1] * np.cos(ang)
                run = 0
                longest = 0
                for r in range(2, max_r + 1):
                    px = int(round(v[0] + rx * r))
                    py = int(round(v[1] + ry * r))
                    if not (0 <= px < w_im and 0 <= py < h_im):
                        break
                    if bw_arrows_only[py, px] > 0:
                        run += 1
                        longest = max(longest, run)
                    else:
                        if run > 0 and r < max_r:
                            px2 = int(round(v[0] + rx * (r + 1)))
                            py2 = int(round(v[1] + ry * (r + 1)))
                            if (0 <= px2 < w_im and 0 <= py2 < h_im and
                                    bw_arrows_only[py2, px2] > 0):
                                continue
                        run = 0
                best_run = max(best_run, longest)
            scores.append(best_run)
        tip, base = _tip_and_base(he["contour"], bw_uneroded=bw_arrows_only)
        print(f"  head#{i}: center={he['center']}")
        print(f"     tri vertices: {[tuple(v) for v in tri]}")
        print(f"     shaft_score per vertex: {scores}")
        print(f"     tip={tip}  base={base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
