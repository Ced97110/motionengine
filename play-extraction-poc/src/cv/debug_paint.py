"""Quick diagnostic: dump the thresholded image + all 4-vertex contours with
their stats, so we can see why paint-rectangle detection failed.
"""
from pathlib import Path

import cv2
import numpy as np
import pdfplumber

HERE = Path(__file__).resolve().parent.parent.parent
PDF = HERE.parent / "knowledge-base" / "raw" / "basketball-for-coaches.pdf"
OUT = HERE / "results" / "cv"


def main():
    with pdfplumber.open(PDF) as pdf:
        page = pdf.pages[59]
        img_meta = page.images[0]
        bbox = (img_meta["x0"], img_meta["top"], img_meta["x1"], img_meta["bottom"])
        pil = page.crop(bbox).to_image(resolution=400).original
    arr = np.array(pil)
    bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(str(OUT / "debug_thresh.png"), thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    h, w = gray.shape
    img_area = h * w

    # Dump all 4-vertex polygons + a few other shapes
    overlay = bgr.copy()
    print(f"image: {w}x{h}, area={img_area}")
    print(f"total contours: {len(contours)}\n")
    for i, c in enumerate(contours):
        peri = cv2.arcLength(c, True)
        if peri < 80:
            continue
        for eps_mul in (0.01, 0.02, 0.04, 0.06):
            approx = cv2.approxPolyDP(c, eps_mul * peri, True)
            n = len(approx)
            x, y, cw, ch = cv2.boundingRect(approx)
            aspect = cw / ch if ch > 0 else 0
            area = cw * ch
            if n in (3, 4, 5, 6) and 0.4 < aspect < 1.5 and 0.02 * img_area < area < 0.5 * img_area:
                print(f"contour {i} eps={eps_mul} n={n} bbox=({cw}x{ch}) aspect={aspect:.2f} area_frac={area/img_area:.3f}")
                if n == 4:
                    cv2.polylines(overlay, [approx], True, (0, 0, 255), 3)
                break

    cv2.imwrite(str(OUT / "debug_overlay.png"), overlay)
    print(f"\nwrote {OUT}/debug_thresh.png and debug_overlay.png")


if __name__ == "__main__":
    main()
