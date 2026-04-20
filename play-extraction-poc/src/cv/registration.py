"""Court registration: pixel → SVG coordinate transform.

Finds the paint rectangle in the rasterized diagram and uses its four corners
as anchors for a homography matching our viewBox coordinate system:

   Paint corners in SVG (viewBox "-28 -3 56 50"):
       top-left  (-8,  0)      top-right  (8,  0)
       bot-left  (-8, 19)      bot-right  (8, 19)

Once registered, any pixel (px, py) in the image maps to an exact SVG
coordinate via a 3x3 matrix — this is the piece that finally translates
CV's pixel-perfect detections into viewBox coordinates the viewer uses.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np

# SVG coords for the OUTER COURT RECTANGLE — the painted-court sideline-to-sideline
# rectangle visible as the largest solid rectangle in each diagram. More reliable
# than the paint fiducial because:
#   - drawn consistently in every panel of this book
#   - well-separated from internal features (arrows, arcs, digits)
#   - represents a known, standard basketball-court extent: SVG (-25, 0) to (25, 47)
#
# The book's paint box is NOT drawn at the Motion spec's 16 SVG units wide, so it's
# an unreliable calibration anchor for this source. The outer court rect is.
COURT_RECT_SVG = np.array(
    [
        [-25.0, 0.0],   # top-left (baseline-left, sideline)
        [25.0, 0.0],    # top-right (baseline-right, sideline)
        [25.0, 47.0],   # bottom-right (half-court, sideline)
        [-25.0, 47.0],  # bottom-left
    ],
    dtype=np.float32,
)
# Keep the old names pointing at the active fiducial for back-compat
PAINT_PLUS_ARC_BBOX_SVG = COURT_RECT_SVG
PAINT_CORNERS_SVG = COURT_RECT_SVG


@dataclass
class Registration:
    homography: np.ndarray  # 3x3 pixel → SVG transform
    paint_pixels: np.ndarray  # 4x2 paint corners in pixel space
    confidence: str  # "high" | "medium" | "low"


def find_paint_corners(bgr: np.ndarray) -> Optional[np.ndarray]:
    """Detect the OUTER COURT RECTANGLE corners in pixel space.

    (Function name kept for back-compat — it actually finds the court boundary,
    which maps to SVG (-25, 0) .. (25, 47) — see COURT_RECT_SVG.)

    Returns [top-left, top-right, bottom-right, bottom-left] as a 4x2 float
    array, or None if the court can't be located.
    """
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image_area = h * w
    candidates: list[tuple[float, np.ndarray]] = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        if peri < 200:
            continue
        x, y, cw, ch = cv2.boundingRect(c)
        area = cw * ch
        # The court outline fills most of the diagram — expect ≥ 60% of image area
        if area < 0.55 * image_area:
            continue
        # But not the whole image (that would be the image frame, not the court)
        if area > 0.98 * image_area:
            continue
        aspect = cw / ch if ch > 0 else 0
        # Court width 50 SVG, height 47 SVG → aspect ≈ 1.06. Allow slack for cropping.
        if not (0.80 <= aspect <= 1.30):
            continue
        # Must fill the image in both axes — rejects tall/narrow shapes
        if cw < 0.75 * w or ch < 0.75 * h:
            continue
        candidates.append((area, np.array(
            [[x, y], [x + cw, y], [x + cw, y + ch], [x, y + ch]],
            dtype=np.float32,
        )))

    if not candidates:
        return None
    # Largest area wins — the court outline is the biggest filled-rectangle contour
    candidates.sort(key=lambda kv: kv[0], reverse=True)
    return candidates[0][1]


def order_corners(pts: np.ndarray) -> np.ndarray:
    """Sort 4 points as [TL, TR, BR, BL] (image coord system: y↓)."""
    # Sum and diff trick: TL has smallest sum, BR largest sum
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).flatten()
    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]
    tr = pts[np.argmin(d)]
    bl = pts[np.argmax(d)]
    return np.array([tl, tr, br, bl], dtype=np.float32)


def register_court(bgr: np.ndarray) -> Optional[Registration]:
    """Compute the pixel → SVG homography for this diagram.

    Returns None if the paint cannot be located.
    """
    paint_px = find_paint_corners(bgr)
    if paint_px is None:
        return None
    H, _ = cv2.findHomography(paint_px, PAINT_PLUS_ARC_BBOX_SVG, method=0)
    if H is None:
        return None
    return Registration(homography=H, paint_pixels=paint_px, confidence="high")


def pixel_to_svg(reg: Registration, px: float, py: float) -> tuple[float, float]:
    """Apply the registration homography to a single pixel coordinate."""
    vec = np.array([px, py, 1.0], dtype=np.float32)
    out = reg.homography @ vec
    out /= out[2]
    return float(out[0]), float(out[1])
