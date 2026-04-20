"""Deterministic classifier for basketball-diagram stroke styles.

Given an ordered polyline describing a movement path on a diagram panel, label
the movement type by analyzing its pixel pattern:

    cut      — solid straight arrow
    pass     — dotted/dashed arrow
    screen   — solid line ending in a perpendicular BAR (no arrowhead)
    dribble  — zig-zag/wavy line with arrowhead
    handoff  — hash-mark symbol (two parallel bars) between two players

The implementation is pure OpenCV + numpy, fully deterministic, no LLM.

The feature extractor works from:
    - the binarized diagram (Otsu),
    - a densified sample of the user-supplied polyline,
    - small ROIs around the endpoints and mid-point for ornament detection
      (arrowhead, perpendicular bar, handoff hash).

The decision tree is:

    1. has_parallel_bars_mid         -> handoff
    2. ends_in_perpendicular_bar and
       not ends_in_arrowhead         -> screen
    3. perpendicular_variance high   -> dribble  (still accept optional arrowhead)
    4. gap_ratio high                -> pass
    5. otherwise                     -> cut
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict

import cv2
import numpy as np

MovementType = Literal["cut", "pass", "screen", "dribble", "handoff"]


class StrokeFeatures(TypedDict):
    gap_ratio: float
    perpendicular_variance: float
    ends_in_arrowhead: bool
    ends_in_perpendicular_bar: bool
    has_parallel_bars_mid: bool
    stroke_density: float


# -----------------------------------------------------------------------------
# Thresholds (tunable, documented)
# -----------------------------------------------------------------------------

# Dashed detection
# A dashed line has many short ink segments interspersed with gaps, so:
#   - gap_ratio should be well above 0 (density well below 1)
#   - the ink/gap alternation produces many binary transitions along the path
# Solid strokes (cut, dribble) will have density ≥ 0.7 — hence
# DASH_STROKE_DENSITY_MAX acts as a veto against mistaking a solid arrow
# that slightly drifts out of the sampling corridor for "dashed".
DASH_GAP_RATIO_MIN = 0.35          # gap_ratio above this is "dashed enough"
DASH_TRANSITIONS_MIN = 6           # minimum dark/light transitions along the path
DASH_STROKE_DENSITY_MAX = 0.65     # hard ceiling — above this it is a solid line
DASH_DARK_THRESHOLD = 128          # grayscale threshold for "ink" pixels (pre-binarization)

# Zig-zag detection
# The path is densified and the perpendicular offset relative to a local trend
# is extracted. Variance is normalized against chord length squared so the
# check is scale-free. A zig-zag of amplitude a has var ≈ a²/2 after detrending,
# so for a ~4-5 px amplitude on a ~200 px chord we expect ratio ≈ 2-3e-4.
# Curved but non-oscillating paths have ratio < 1e-4 after detrending AND
# essentially zero sign changes — we require BOTH thresholds to be met.
ZIGZAG_VARIANCE_RATIO_MIN = 1.5e-4
ZIGZAG_PEAK_COUNT_MIN = 4          # at least 4 sign changes in perp offset → oscillation

# Arrowhead detection (endpoint ROI size and shape expectations)
ARROWHEAD_ROI_SCALE = 0.04         # ROI half-size as fraction of image width
ARROWHEAD_MIN_AREA = 40            # pixels (filled triangle ~ 8x10)
ARROWHEAD_MAX_AREA_RATIO = 0.25    # relative to ROI area
ARROWHEAD_DENSITY_MIN = 0.45       # filled triangle has high fill ratio

# Perpendicular bar (screen) detection
BAR_ROI_SCALE = 0.06               # ROI half-size as fraction of image width
BAR_LENGTH_MIN_RATIO = 0.05        # bar ≥ 5% of path length
BAR_LENGTH_MAX_RATIO = 0.35        # bar ≤ 35% of path length
BAR_PERP_ANGLE_TOL_DEG = 25.0      # angle-off-perpendicular tolerance

# Handoff hash detection (midpoint neighborhood)
HANDOFF_ROI_SCALE = 0.05
HANDOFF_PARALLEL_ANGLE_TOL_DEG = 22.0
HANDOFF_MIN_BAR_LENGTH = 6         # in pixels

# Densification: re-sample the path with N pixels between original points
PATH_SAMPLE_STEP_PX = 2


# -----------------------------------------------------------------------------
# Geometry helpers
# -----------------------------------------------------------------------------


@dataclass(frozen=True)
class _PathGeom:
    points: np.ndarray        # shape (N, 2) densified pixel coordinates
    chord_length: float       # straight-line length start→end
    path_length: float        # total polyline length
    start: np.ndarray         # shape (2,)
    end: np.ndarray           # shape (2,)
    direction: np.ndarray     # unit vector start→end


def _densify(path_points: list[tuple[float, float]], step: float = PATH_SAMPLE_STEP_PX) -> np.ndarray:
    """Return a (N, 2) array with points re-sampled every `step` pixels along the polyline."""
    if len(path_points) < 2:
        raise ValueError("path_points requires at least 2 points")
    pts = np.asarray(path_points, dtype=np.float64)
    out: list[np.ndarray] = [pts[0]]
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        seg = b - a
        seg_len = float(np.linalg.norm(seg))
        if seg_len < 1e-6:
            continue
        n = max(1, int(np.ceil(seg_len / step)))
        for k in range(1, n + 1):
            t = k / n
            out.append(a + t * seg)
    return np.asarray(out, dtype=np.float64)


def _path_geometry(path_points: list[tuple[float, float]]) -> _PathGeom:
    dense = _densify(path_points)
    start = dense[0].copy()
    end = dense[-1].copy()
    chord_vec = end - start
    chord_len = float(np.linalg.norm(chord_vec))
    if chord_len < 1e-6:
        raise ValueError("path start equals path end")
    direction = chord_vec / chord_len
    diffs = np.diff(dense, axis=0)
    path_len = float(np.sum(np.linalg.norm(diffs, axis=1)))
    return _PathGeom(
        points=dense,
        chord_length=chord_len,
        path_length=path_len,
        start=start,
        end=end,
        direction=direction,
    )


def _binarize(bgr: np.ndarray) -> np.ndarray:
    """Return inverse-binary mask where ink == 255."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY) if bgr.ndim == 3 else bgr
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return bw


def _sample_along(
    gray: np.ndarray, points: np.ndarray
) -> np.ndarray:
    """Nearest-neighbor sample grayscale values along the densified polyline."""
    h, w = gray.shape[:2]
    xs = np.clip(np.round(points[:, 0]).astype(int), 0, w - 1)
    ys = np.clip(np.round(points[:, 1]).astype(int), 0, h - 1)
    return gray[ys, xs]


def _corridor_mask_samples(bw: np.ndarray, points: np.ndarray, half_width: int = 4) -> np.ndarray:
    """For each point, check if ANY pixel in a small perpendicular window is ink.

    Returns a boolean array, True where ink is present in the corridor.
    Using a corridor (rather than a single pixel) is robust to sub-pixel path
    offsets from the upstream arrow detector.
    """
    h, w = bw.shape[:2]
    if len(points) < 2:
        return np.zeros(len(points), dtype=bool)
    tangents = np.gradient(points, axis=0)
    tangents /= np.clip(np.linalg.norm(tangents, axis=1, keepdims=True), 1e-6, None)
    perps = np.stack([-tangents[:, 1], tangents[:, 0]], axis=1)

    out = np.zeros(len(points), dtype=bool)
    for i, (pt, perp) in enumerate(zip(points, perps)):
        for k in range(-half_width, half_width + 1):
            px = int(round(pt[0] + perp[0] * k))
            py = int(round(pt[1] + perp[1] * k))
            if 0 <= px < w and 0 <= py < h and bw[py, px] > 0:
                out[i] = True
                break
    return out


# -----------------------------------------------------------------------------
# Feature extraction
# -----------------------------------------------------------------------------


def _gap_and_density(
    bw: np.ndarray, geom: _PathGeom
) -> tuple[float, float, int]:
    """Return (gap_ratio, stroke_density, transitions).

    gap_ratio:      fraction of samples along path that are background.
    stroke_density: fraction of samples along path that are ink.
    transitions:   number of ink↔gap boundary crossings.
    """
    corridor = _corridor_mask_samples(bw, geom.points, half_width=4)
    if len(corridor) == 0:
        return 0.0, 0.0, 0
    ink = corridor.astype(np.int8)
    stroke_density = float(ink.mean())
    gap_ratio = 1.0 - stroke_density
    # Trim arrowhead inflation at the endpoints by ignoring the last 6% of samples.
    core = ink[: max(1, int(len(ink) * 0.94))]
    transitions = int(np.sum(np.abs(np.diff(core))))
    return gap_ratio, stroke_density, transitions


def _perpendicular_variance(geom: _PathGeom) -> tuple[float, int]:
    """Detrended perpendicular-offset variance of the polyline.

    A curved-but-not-zig-zag path (e.g. a cut on an arc) has a large perpendicular
    offset, but it is monotone. A zig-zag oscillates AROUND its local trend, so
    we subtract a moving-average "trend" from the signed perpendicular signal
    before taking variance and counting sign changes.

    Returns:
        (normalized_variance, sign_change_count) — variance is normalized against
        chord_length^2 so it is scale-invariant.
    """
    rel = geom.points - geom.start
    along = rel @ geom.direction
    proj = np.outer(along, geom.direction)
    perp_vec = rel - proj
    perp_signed = perp_vec[:, 0] * (-geom.direction[1]) + perp_vec[:, 1] * geom.direction[0]

    # Detrend with a moving average the length of ~1/3 of the path.
    n = len(perp_signed)
    if n >= 5:
        k = max(3, n // 4) | 1  # odd window ≈ n/4
        kernel = np.ones(k) / k
        # 'same' convolution biases ends, so pad-and-crop manually with reflect
        padded = np.pad(perp_signed, (k // 2, k // 2), mode="edge")
        trend = np.convolve(padded, kernel, mode="valid")
        oscillation = perp_signed - trend
    else:
        oscillation = perp_signed - perp_signed.mean()

    var_norm = float(np.var(oscillation) / max(geom.chord_length ** 2, 1.0))

    # Count sign changes in the oscillation (debounced small jitter)
    signs = np.sign(oscillation)
    signs[np.abs(oscillation) < 0.5] = 0  # treat sub-pixel noise as zero
    signs_clean = signs[signs != 0]
    sign_changes = int(np.sum(np.diff(signs_clean) != 0)) if len(signs_clean) > 1 else 0
    return var_norm, sign_changes


def _endpoint_roi(bw: np.ndarray, center: np.ndarray, half_size: int) -> tuple[np.ndarray, tuple[int, int]]:
    h, w = bw.shape[:2]
    cx = int(round(center[0]))
    cy = int(round(center[1]))
    x0 = max(0, cx - half_size)
    y0 = max(0, cy - half_size)
    x1 = min(w, cx + half_size + 1)
    y1 = min(h, cy + half_size + 1)
    return bw[y0:y1, x0:x1].copy(), (x0, y0)


def _ends_in_arrowhead(bw: np.ndarray, geom: _PathGeom) -> bool:
    """Look for a dense roughly-triangular blob near the endpoint."""
    h, w = bw.shape[:2]
    half = max(10, int(w * ARROWHEAD_ROI_SCALE))
    roi, (x0, y0) = _endpoint_roi(bw, geom.end, half)
    if roi.size == 0:
        return False
    # Connected components, pick the largest that is near the endpoint
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(roi, connectivity=8)
    roi_area = roi.shape[0] * roi.shape[1]
    best = None
    for i in range(1, num):
        x, y, cw, ch, area = stats[i]
        if area < ARROWHEAD_MIN_AREA:
            continue
        if area > roi_area * ARROWHEAD_MAX_AREA_RATIO:
            continue
        cx_abs = centroids[i][0] + x0
        cy_abs = centroids[i][1] + y0
        d_end = float(np.hypot(cx_abs - geom.end[0], cy_abs - geom.end[1]))
        if d_end > half * 1.2:
            continue
        density = area / max(cw * ch, 1)
        if density < ARROWHEAD_DENSITY_MIN:
            continue
        # Orientation: bounding box elongated along path direction is a good sign
        # but not required — short filled triangles can be near-square too.
        score = density * area
        if best is None or score > best:
            best = score
    return best is not None


def _ends_in_perpendicular_bar(bw: np.ndarray, geom: _PathGeom) -> bool:
    """Detect a short perpendicular bar at the endpoint (screen symbol).

    The bar is typically connected to the main stroke, so connected-component
    analysis alone cannot separate it. Instead we scan perpendicular rays out
    from the endpoint in BOTH directions and count how far ink extends.

    A true bar produces:
      - ink extending symmetrically to both sides for at least a few pixels
      - the combined extent is several times the local stroke half-width
      - the extension is markedly larger than the thickness at the endpoint
        along the tangent direction (to reject solid arrowheads that also
        appear wide at the tip).
    """
    h, w = bw.shape[:2]

    # Local tangent from the last 3 vertices of the densified path.
    if len(geom.points) >= 3:
        tangent = geom.points[-1] - geom.points[-3]
    else:
        tangent = geom.end - geom.start
    tn = float(np.linalg.norm(tangent))
    if tn < 1e-6:
        return False
    tangent = tangent / tn
    perp = np.array([-tangent[1], tangent[0]])

    path_len = max(geom.path_length, 1.0)
    # Scan up to this many pixels perpendicular and along tangent from endpoint.
    max_scan = max(12, int(w * BAR_ROI_SCALE))

    def _scan(origin: np.ndarray, direction: np.ndarray) -> int:
        """Return the number of consecutive ink pixels starting at origin along direction."""
        length = 0
        for k in range(1, max_scan + 1):
            px = int(round(origin[0] + direction[0] * k))
            py = int(round(origin[1] + direction[1] * k))
            if not (0 <= px < w and 0 <= py < h):
                break
            if bw[py, px] > 0:
                length = k
            else:
                # Allow a 1-pixel gap (anti-alias / broken pixel)
                if k - length > 1:
                    break
        return length

    # The upstream detector's "endpoint" can land up to ~3 px before the bar.
    # Search a small window along ±tangent for the location that maximizes
    # bilateral perpendicular extent, then evaluate bar geometry there.
    best = (-1, 0, 0, 0)  # (score, perp+, perp-, tang+_beyond_end)
    for t_offset in range(-4, 9):
        origin = geom.end + tangent * t_offset
        perp_plus = _scan(origin, perp)
        perp_minus = _scan(origin, -perp)
        score = min(perp_plus, perp_minus) * 2 + (perp_plus + perp_minus)
        if score > best[0]:
            # Measure how far ink extends BEYOND the nominal endpoint along
            # the tangent — a filled arrowhead spills forward along tangent,
            # a pure perpendicular bar does not.
            tang_plus = _scan(origin, tangent)
            best = (score, perp_plus, perp_minus, tang_plus)

    _, perp_plus, perp_minus, tang_plus = best
    bar_width = perp_plus + perp_minus
    both_sides = perp_plus >= 3 and perp_minus >= 3
    min_len = max(8.0, BAR_LENGTH_MIN_RATIO * path_len)
    long_enough = bar_width >= min_len
    # True bar is at least 2x wider perpendicular than it extends forward
    # along the tangent; filled arrowheads extend forward a lot.
    not_triangular = bar_width >= 2 * tang_plus + 2

    return bool(both_sides and long_enough and not_triangular)


def _has_parallel_bars_mid(bw: np.ndarray, geom: _PathGeom) -> bool:
    """Detect the handoff hash (two short parallel bars near the midpoint)."""
    h, w = bw.shape[:2]
    mid = geom.points[len(geom.points) // 2]
    half = max(12, int(w * HANDOFF_ROI_SCALE))
    roi, (x0, y0) = _endpoint_roi(bw, mid, half)
    if roi.size == 0:
        return False

    if len(geom.points) >= 3:
        idx = len(geom.points) // 2
        lo = max(0, idx - 2)
        hi = min(len(geom.points) - 1, idx + 2)
        tangent = geom.points[hi] - geom.points[lo]
    else:
        tangent = geom.end - geom.start
    n = float(np.linalg.norm(tangent))
    if n < 1e-6:
        return False
    tangent = tangent / n
    perp = np.array([-tangent[1], tangent[0]])

    num, labels, stats, centroids = cv2.connectedComponentsWithStats(roi, connectivity=8)
    bars: list[tuple[float, float, float]] = []  # (cx_abs, cy_abs, signed_offset_along_perp)
    for i in range(1, num):
        x, y, cw, ch, area = stats[i]
        if area < 4:
            continue
        mask = (labels == i).astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours or len(contours[0]) < 5:
            if cw < 3 or ch < 3:
                continue
            rect_long = float(max(cw, ch))
            rect_short = float(min(cw, ch))
            rect_angle = 0.0 if cw >= ch else 90.0
        else:
            rect = cv2.minAreaRect(contours[0])
            (_cx, _cy), (rw, rh), rect_angle = rect
            rect_long = float(max(rw, rh))
            rect_short = float(min(rw, rh))
            if rw < rh:
                rect_angle += 90.0
        if rect_short < 1.0 or rect_long < HANDOFF_MIN_BAR_LENGTH:
            continue
        aspect = rect_long / max(rect_short, 1.0)
        if aspect < 2.0:
            continue

        rect_rad = np.deg2rad(rect_angle)
        rect_dir = np.array([np.cos(rect_rad), np.sin(rect_rad)])
        perp_cos = abs(float(np.dot(rect_dir, perp)))
        perp_cos = min(1.0, perp_cos)
        angle_off = abs(np.rad2deg(np.arccos(perp_cos)))
        if angle_off > HANDOFF_PARALLEL_ANGLE_TOL_DEG:
            continue

        cx_abs = centroids[i][0] + x0
        cy_abs = centroids[i][1] + y0
        signed = (cx_abs - mid[0]) * tangent[0] + (cy_abs - mid[1]) * tangent[1]
        bars.append((cx_abs, cy_abs, signed))

    # Need at least two bars spaced along the tangent direction
    if len(bars) < 2:
        return False
    signed_vals = sorted(b[2] for b in bars)
    for i in range(len(signed_vals) - 1):
        sep = abs(signed_vals[i + 1] - signed_vals[i])
        if 3.0 <= sep <= half * 1.5:
            return True
    return False


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------


def classify_stroke(
    bgr: np.ndarray,
    path_points: list[tuple[float, float]],
) -> tuple[MovementType, float, StrokeFeatures]:
    """Classify the movement type of the given path.

    Args:
        bgr: BGR numpy array of the diagram panel (H, W, 3) uint8.
        path_points: ordered polyline of pixel coords describing the path.
                     At minimum 2 points; typical ~5-20 samples for curves.

    Returns:
        (movement_type, confidence_0_to_1, feature_dict)
    """
    if bgr is None or bgr.ndim not in (2, 3):
        raise ValueError("bgr must be a 2D or 3D image array")
    if len(path_points) < 2:
        raise ValueError("path_points must contain at least 2 points")

    bw = _binarize(bgr)
    geom = _path_geometry(path_points)

    gap_ratio, stroke_density, transitions = _gap_and_density(bw, geom)
    var_norm, sign_changes = _perpendicular_variance(geom)
    has_head = _ends_in_arrowhead(bw, geom)
    has_bar = _ends_in_perpendicular_bar(bw, geom)
    has_hash = _has_parallel_bars_mid(bw, geom)

    features: StrokeFeatures = {
        "gap_ratio": float(gap_ratio),
        "perpendicular_variance": float(var_norm),
        "ends_in_arrowhead": bool(has_head),
        "ends_in_perpendicular_bar": bool(has_bar),
        "has_parallel_bars_mid": bool(has_hash),
        "stroke_density": float(stroke_density),
    }

    # Decision tree (priority order)
    # 1. Handoff — two parallel bars near the midpoint
    if has_hash:
        # Confidence boosted if both endpoints anchored to players (out of scope);
        # here we use the structural signal only.
        return "handoff", 0.85, features

    # 2. Screen — perpendicular bar at end, no arrowhead
    if has_bar and not has_head:
        return "screen", 0.85, features

    # 3. Dribble — zig-zag. Must satisfy both variance and sign-change thresholds.
    zigzag = var_norm >= ZIGZAG_VARIANCE_RATIO_MIN and sign_changes >= ZIGZAG_PEAK_COUNT_MIN
    if zigzag:
        # Confidence scales with how much the path oscillates
        conf = float(min(1.0, 0.55 + 0.15 * (sign_changes - ZIGZAG_PEAK_COUNT_MIN)))
        return "dribble", conf, features

    # 4. Pass — dashed. Requires enough transitions, meaningful gap fraction,
    #    and density below the "solid" ceiling (otherwise this is a solid stroke
    #    that happened to drift slightly outside the sampling corridor).
    dashed = (
        gap_ratio >= DASH_GAP_RATIO_MIN
        and transitions >= DASH_TRANSITIONS_MIN
        and stroke_density <= DASH_STROKE_DENSITY_MAX
    )
    if dashed:
        # Confidence rises with number of transitions but saturates
        conf = float(min(1.0, 0.55 + 0.03 * (transitions - DASH_TRANSITIONS_MIN)))
        return "pass", conf, features

    # 5. Default: solid arrow ≡ cut
    # Confidence reflects how confident we are that this is not any of the above
    margin = 1.0
    if gap_ratio > 0.20:
        margin *= 0.7
    if var_norm > 0.0005:
        margin *= 0.8
    conf = float(min(0.95, 0.6 * margin + 0.3 * (1.0 if has_head else 0.5)))
    return "cut", conf, features


# -----------------------------------------------------------------------------
# __main__: regression harness for page 60, panel 0
# -----------------------------------------------------------------------------


def _extract_page_60_panel_0() -> np.ndarray:
    import pdfplumber

    pdf_path = Path(
        "/Users/ced/Desktop/motion/backend/knowledge-base/raw/basketball-for-coaches.pdf"
    )
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[59]
        img = page.images[0]
        bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
        pil = page.crop(bbox).to_image(resolution=400).original
    arr = np.array(pil)
    if arr.ndim == 2:
        return cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    if arr.shape[2] == 4:
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


# Test paths on page 60 panel 0 (image is 1017×962 at 400 DPI).
# Coordinates were traced off the rasterized panel (see
# results/cv/page_060_panel_0_source.png) and reflect what a downstream arrow
# detector is expected to output for each stroke: a densified polyline that
# follows the actual ink, including zig-zag vertices for dribbles.
#
# The diagram shows:
#   - Player 1 passes dashed arrow up-left to player 2.
#   - Player 4 sets a down screen that ends with a perpendicular bar at the
#     free-throw-line extended (no arrowhead).
#   - Player 2 dribbles up-right with a zig-zag waveform into the elbow.
#   - Player 5 cuts solid arrow from the wing into the paint.
_PAGE60_PATHS: dict[str, tuple[str, list[tuple[float, float]]]] = {
    "pass_1_to_2": (
        "pass",
        [(520.0, 605.0), (460.0, 580.0), (400.0, 555.0), (340.0, 535.0),
         (280.0, 515.0), (235.0, 500.0)],
    ),
    "screen_4_down": (
        "screen",
        [(120.0, 195.0), (155.0, 235.0), (185.0, 260.0), (210.0, 275.0),
         (225.0, 285.0), (234.0, 310.0), (234.0, 338.0)],
    ),
    "dribble_from_2_up": (
        # Zig-zag waypoints — vertices alternate above/below the main diagonal
        # from (225, 265) to (430, 165) with ~10 px amplitude. These are the
        # kind of vertices the upstream arrow detector produces for zig-zag
        # strokes (each peak/valley of the wave is a sample point).
        "dribble",
        [
            (225.0, 265.0),
            (238.0, 248.0),   # peak up-left
            (254.0, 252.0),   # valley
            (268.0, 232.0),   # peak
            (285.0, 238.0),   # valley
            (300.0, 215.0),   # peak
            (318.0, 220.0),   # valley
            (333.0, 198.0),   # peak
            (352.0, 203.0),   # valley
            (370.0, 182.0),   # peak
            (390.0, 186.0),   # valley
            (408.0, 170.0),   # peak
            (430.0, 165.0),
        ],
    ),
    "cut_5_to_paint": (
        "cut",
        [(910.0, 160.0), (820.0, 180.0), (730.0, 210.0),
         (650.0, 235.0), (600.0, 250.0), (575.0, 258.0)],
    ),
}


_COLORS: dict[str, tuple[int, int, int]] = {
    "cut": (0, 200, 0),        # green
    "pass": (0, 140, 255),     # orange
    "screen": (255, 80, 0),    # blue
    "dribble": (0, 0, 220),    # red
    "handoff": (200, 0, 200),  # magenta
}


def _draw_overlay(
    bgr: np.ndarray,
    results: list[tuple[str, str, MovementType, float, list[tuple[float, float]]]],
) -> np.ndarray:
    out = bgr.copy()
    for name, expected, predicted, conf, pts in results:
        color = _COLORS.get(predicted, (0, 0, 0))
        arr = np.asarray(pts, dtype=np.int32).reshape(-1, 1, 2)
        cv2.polylines(out, [arr], isClosed=False, color=color, thickness=3)
        # Label at the midpoint
        mid = arr[len(arr) // 2][0]
        marker = "OK" if predicted == expected else "MISS"
        text = f"{predicted} {conf:.2f} [{marker}]"
        cv2.putText(
            out, text, (int(mid[0]) + 6, int(mid[1]) - 6),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA,
        )
    return out


def _main() -> int:
    bgr = _extract_page_60_panel_0()
    results: list[tuple[str, str, MovementType, float, list[tuple[float, float]]]] = []
    print(f"image shape: {bgr.shape}")
    print("-" * 72)
    correct = 0
    for name, (expected, pts) in _PAGE60_PATHS.items():
        predicted, conf, feats = classify_stroke(bgr, pts)
        ok = predicted == expected
        correct += int(ok)
        status = "OK  " if ok else "MISS"
        print(f"[{status}] {name}: expected={expected} predicted={predicted} conf={conf:.2f}")
        print(
            f"       gap={feats['gap_ratio']:.3f} "
            f"perp_var={feats['perpendicular_variance']:.4f} "
            f"head={feats['ends_in_arrowhead']} "
            f"bar={feats['ends_in_perpendicular_bar']} "
            f"hash={feats['has_parallel_bars_mid']} "
            f"density={feats['stroke_density']:.3f}"
        )
        results.append((name, expected, predicted, conf, pts))
    print("-" * 72)
    print(f"accuracy: {correct}/{len(_PAGE60_PATHS)}")

    out_path = Path(__file__).resolve().parent.parent.parent / "results" / "cv" / "strokes_page_60_panel_0.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    overlay = _draw_overlay(bgr, results)
    cv2.imwrite(str(out_path), overlay)
    print(f"overlay written to {out_path}")
    return 0 if correct == len(_PAGE60_PATHS) else 1


if __name__ == "__main__":
    raise SystemExit(_main())
