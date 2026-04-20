"""Scratch: zoom into specific regions to inspect what's there."""
from __future__ import annotations

import cv2
import numpy as np

from src.cv.arrows import (
    _binarize,
    _mask_players_and_outer,
    _mask_court_features,
    _erode_for_tips,
    _load_page_60_panel_0,
)
from src.cv.probe import detect_glyph_candidates, ocr_digit
from src.cv.registration import register_court


def main() -> int:
    bgr = _load_page_60_panel_0()
    cands = detect_glyph_candidates(bgr)
    player_bboxes = []
    for c in cands:
        if ocr_digit(bgr, c["bbox"]):
            player_bboxes.append(c["bbox"])
    bw_full = _binarize(bgr)
    bw = _mask_players_and_outer(bw_full, bgr.shape[:2], player_bboxes)
    reg = register_court(bgr)
    court_mask = _mask_court_features(bw, registration=reg)
    bw_arrows = cv2.bitwise_and(bw, cv2.bitwise_not(court_mask))
    eroded = _erode_for_tips(bw_arrows)

    h_im, w_im = bw_arrows.shape[:2]

    def crop(im: np.ndarray, x: int, y: int, w: int, h: int, path: str) -> None:
        x0, x1 = max(0, x), min(w_im, x + w)
        y0, y1 = max(0, y), min(h_im, y + h)
        cv2.imwrite(path, im[y0:y1, x0:x1])

    crop(bw_arrows, 100, 250, 250, 150, "scratch_z_screen_bw.png")
    crop(eroded, 100, 250, 250, 150, "scratch_z_screen_eroded.png")

    crop(bw_arrows, 300, 100, 250, 150, "scratch_z_dribble_bw.png")
    crop(eroded, 300, 100, 250, 150, "scratch_z_dribble_eroded.png")

    crop(bw_arrows, 130, 80, 350, 380, "scratch_z_zigzag_bw.png")
    crop(eroded, 130, 80, 350, 380, "scratch_z_zigzag_eroded.png")

    # Original BGR around screen bar (enlarged 2x)
    bgr_screen = bgr[290:360, 140:300]
    enlarged = cv2.resize(bgr_screen, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
    cv2.imwrite("scratch_z_screen_bgr_3x.png", enlarged)

    # Original BGR around dribble arrowhead (enlarged 4x)
    bgr_head = bgr[130:200, 380:460]
    enlarged = cv2.resize(bgr_head, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
    cv2.imwrite("scratch_z_dribble_head_4x.png", enlarged)

    # Larger BW context around dribble head
    patch_full = bw_arrows[130:200, 380:460]
    print("\nbw_arrows around dribble head (y 130-200, x 380-460):")
    for row in patch_full:
        print("".join("#" if p > 0 else "." for p in row))

    # Larger context around dribble arrowhead + below
    patch_zig = bw_arrows[150:260, 330:440]
    print("\nbw_arrows zigzag tail below head (y 150-260, x 330-440):")
    for row in patch_zig:
        print("".join("#" if p > 0 else "." for p in row))

    # Same region in bw (pre-court-mask)
    bw_precourt = _mask_players_and_outer(bw_full, bgr.shape[:2], player_bboxes)
    patch_zig_pre = bw_precourt[150:260, 330:440]
    print("\nbw pre-court-mask zigzag tail (y 150-260, x 330-440):")
    for row in patch_zig_pre:
        print("".join("#" if p > 0 else "." for p in row))

    # List all connected components in bw_arrows (NOT eroded) around the zigzag
    # and screen regions to find zigzag-like components.
    # Zigzag dribble region: y=80-250, x=130-450
    zigzag_region = bw_arrows[80:250, 130:450]
    n, lbls, st, ct = cv2.connectedComponentsWithStats(zigzag_region, connectivity=8)
    print(f"\nComponents in zigzag-region (y 80-250, x 130-450): n={n - 1}")
    for i in range(1, n):
        x, y, cw, ch, area = st[i]
        if area < 30:
            continue
        comp_mask = (lbls == i).astype(np.uint8) * 255
        # Compute perimeter
        contours, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        perim = sum(cv2.arcLength(c, True) for c in contours)
        # Elongation: diagonal of bbox / area-sqrt ratio
        bbox_diag = np.hypot(cw, ch)
        # "Complexity" = perimeter / bbox_diag ratio. Zigzag strokes have HIGH perim/diag.
        cplx = perim / max(bbox_diag, 1)
        print(f"  comp#{i}: bbox=({x + 130},{y + 80},{cw},{ch}) area={area}  perim={perim:.0f}  cplx={cplx:.1f}")

    # Screen region
    screen_region = bw_arrows[250:360, 130:300]
    n, lbls, st, ct = cv2.connectedComponentsWithStats(screen_region, connectivity=8)
    print(f"\nComponents in screen-region (y 250-360, x 130-300): n={n - 1}")
    for i in range(1, n):
        x, y, cw, ch, area = st[i]
        if area < 30:
            continue
        comp_mask = (lbls == i).astype(np.uint8) * 255
        contours, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        perim = sum(cv2.arcLength(c, True) for c in contours)
        bbox_diag = np.hypot(cw, ch)
        cplx = perim / max(bbox_diag, 1)
        print(f"  comp#{i}: bbox=({x + 130},{y + 250},{cw},{ch}) area={area}  perim={perim:.0f}  cplx={cplx:.1f}")

    # Visualize comp#7 of the full image
    num2, lbls2, st2, ct2 = cv2.connectedComponentsWithStats(bw_arrows, connectivity=8)
    for i in range(1, num2):
        x, y, cw, ch, area = st2[i]
        if area >= 4000 and max(cw, ch) <= 250:
            print(f"\nVisualizing big component (bbox={x},{y},{cw},{ch}, area={area}):")
            comp_mask = (lbls2 == i).astype(np.uint8) * 255
            # Save cropped visualization
            cv2.imwrite(f"scratch_comp_{i}.png", comp_mask[y:y + ch, x:x + cw])
            for kz in [(3, 2), (5, 1), (5, 2), (7, 1)]:
                kk, ni = kz
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kk, kk))
                er = cv2.erode(comp_mask, kernel, iterations=ni)
                num3, lbls3, st3, ct3 = cv2.connectedComponentsWithStats(er, connectivity=8)
                subs_count = sum(1 for j in range(1, num3) if st3[j][4] >= 40)
                print(f"  Erode {kk}x{kk} iter={ni}: {subs_count} sub-components")
                for j in range(1, num3):
                    if st3[j][4] < 40:
                        continue
                    print(f"    sub#{j}: bbox=({st3[j][0]},{st3[j][1]},{st3[j][2]},{st3[j][3]}) area={st3[j][4]}")
            break

    # Print ascii patch around head#0
    patch = bw_arrows[140:195, 380:445]
    print("bw_arrows patch around head#0 (y 140-195, x 380-445):")
    for row in patch:
        print("".join("#" if p > 0 else "." for p in row))

    # Eroded patch around screen bar (y 300-360, x 150-260)
    patch2 = eroded[300:360, 150:280]
    print("\neroded patch around screen bar region (y 300-360, x 150-280):")
    for row in patch2:
        print("".join("#" if p > 0 else "." for p in row))

    # Full bw_arrows around screen bar for context
    patch3 = bw_arrows[295:360, 150:280]
    print("\nbw_arrows patch around screen bar (y 295-360, x 150-280):")
    for row in patch3:
        print("".join("#" if p > 0 else "." for p in row))
    # Inspect horizontal runs in the screen region
    region = bw_arrows[320:360, 150:350]
    print("\nscreen region long horizontals (y 320-360, x 150-350):")
    for yi in range(region.shape[0]):
        cnt = int(np.count_nonzero(region[yi]))
        if cnt > 30:
            xs = np.where(region[yi] > 0)[0]
            print(f"  y={yi + 320}: cnt={cnt}, xs=[{int(xs.min()) + 150},{int(xs.max()) + 150}]")

    # Find horizontal runs in ERODED screen region
    eroded_region = eroded[305:350, 150:350]
    print("\neroded screen region rows with any ink (y 305-350, x 150-350):")
    for yi in range(eroded_region.shape[0]):
        cnt = int(np.count_nonzero(eroded_region[yi]))
        if cnt > 5:
            xs = np.where(eroded_region[yi] > 0)[0]
            print(f"  y={yi + 305}: cnt={cnt}, xs=[{int(xs.min()) + 150},{int(xs.max()) + 150}]")

    # Connected components in JUST the eroded bottom horizontal bar region
    bar_region = eroded[337:347, 190:280]
    n, lbls, st, ct = cv2.connectedComponentsWithStats(bar_region, connectivity=8)
    print(f"\nComponents in bar-only region (y 337-347, x 190-280): n={n - 1}")
    for i in range(1, n):
        print(f"  #{i}: bbox={st[i]} area={st[i][4]}")

    # Print eroded at full detail y 330-350, x 150-300
    print("\neroded detail (y 330-350, x 150-300):")
    patch4 = eroded[330:350, 150:300]
    for row in patch4:
        print("".join("#" if p > 0 else "." for p in row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
