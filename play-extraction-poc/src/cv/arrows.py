"""Arrow-path detection for basketball play diagrams (Basketball For Coaches book).

Deterministic OpenCV/numpy pipeline (no LLMs). Given a rasterized diagram panel
plus the player-digit bounding boxes, detects and classifies arrow paths:

  * solid   — player cut (solid line + triangular arrowhead)
  * dashed  — pass (dotted/dashed stroke + triangular arrowhead)
  * zigzag  — dribble (oscillating wavy stroke + triangular arrowhead)
  * screen  — pick set (stroke ending in a perpendicular "⊥" bar)

High-level algorithm
--------------------

1.  Threshold + mask the players (digit bbox + surrounding ball-handler
    circle), the outer court rectangle, the paint sides, the FT circle, the
    backboard/rim, and the 3-point arc. The static-court mask uses the
    `cv.registration` homography to draw procedural strokes at the book's
    empirically-measured SVG positions (the book draws the arc at roughly
    center (0, 3.34) radius 22.16 SVG units, and the paint at roughly x=±6).
2.  Erode with a 5×5 kernel: arrow shafts (~3 px) vanish, arrowheads (~10-15 px
    filled triangles) and perpendicular screen bars survive.
3.  Classify surviving blobs:
        arrowhead = solid, triangular, compact (solidity ≥ 0.70, fill ≥ 0.35,
                    area 300-2500 px², aspect 0.5-2.0).
        screen bar = thin elongated rectangle (max aspect ≥ 2.2, fill ≥ 0.35,
                    max dimension ≥ 22 px, not parallel to a nearby arrow shaft).
4.  For each arrowhead, compute TIP and BASE via `cv2.minEnclosingTriangle`:
        tip  = vertex farthest from the opposite triangle edge
        base = midpoint of that opposite edge
5.  From BASE, trace the stroke backward along the ORIGINAL (pre-erosion)
    bitmap. Each step hops `_TRACE_STEP` px in the current direction, then
    snaps to the closest ink pixel within `_TRACE_SEARCH_RADIUS`. Stops at
    another arrowhead's bbox, a player bbox, or when ink runs out or the
    trace has moved further from every player for N consecutive steps.
6.  Classify the traced polyline:
        is_dashed  = many gaps along the chord (dashed pass)
        is_zigzag  = perpendicular deviation from the chord oscillates with
                     significant amplitude (dribble)
        has_perpendicular_bar = a screen-bar blob sits near the arrow start
        has_arrowhead = always True for traced paths (seed is an arrowhead)
7.  Also report "screen-only" paths: screen bars with no arrowhead attached
    become arrows whose tail is the nearest player and whose tip is the bar.
8.  Sort results longest-path-first.

Tuned on page 60, panel 0 at 400 DPI (≈ 1017×962 px). Thresholds scale with
image size only where the scale matters (erosion kernel, trace step, bar size).

Usage:
    python -m src.cv.arrows
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Optional

import cv2
import numpy as np

if TYPE_CHECKING:  # pragma: no cover
    try:
        from .registration import Registration
    except ImportError:
        from cv.registration import Registration  # type: ignore

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


ArrowKind = Literal["solid", "dashed", "zigzag", "screen", "unknown"]


@dataclass
class DetectedArrow:
    start_px: tuple[float, float]
    end_px: tuple[float, float]
    control_points: list[tuple[float, float]]
    has_arrowhead: bool
    has_perpendicular_bar: bool
    is_dashed: bool
    is_zigzag: bool
    confidence: float
    stroke_pixels: int

    @property
    def kind(self) -> ArrowKind:
        if self.has_perpendicular_bar:
            return "screen"
        if self.is_zigzag:
            return "zigzag"
        if self.is_dashed:
            return "dashed"
        if self.has_arrowhead:
            return "solid"
        return "unknown"

    @property
    def length_px(self) -> float:
        dx = self.end_px[0] - self.start_px[0]
        dy = self.end_px[1] - self.start_px[1]
        return float(np.hypot(dx, dy))


# ---------------------------------------------------------------------------
# Tuned thresholds (page-60 calibration at 400 DPI, ≈1017×962 px)
# ---------------------------------------------------------------------------

_OUTER_BORDER_PX = 28                # how much of the image border to zero out
_PLAYER_MASK_PAD = 12                # extra padding around player bboxes

_EROSION_KERNEL = 5                  # kill ~3-px shafts, keep ~10-px heads
_DILATE_AFTER_ERODE_KERNEL = 3

# Arrowhead blob thresholds.
_HEAD_MIN_AREA = 300
_HEAD_MAX_AREA = 2500
_HEAD_MIN_SOLIDITY = 0.70
_HEAD_MIN_FILL = 0.35
_HEAD_ASPECT_MIN = 0.5
_HEAD_ASPECT_MAX = 2.0
_HEAD_MAX_DIM = 90

# Screen-bar blob thresholds (on the same eroded bitmap).
_BAR_MIN_AREA = 80
_BAR_MAX_AREA = 400
_BAR_MIN_LONG_ASPECT = 2.5
_BAR_MIN_FILL = 0.45
_BAR_MIN_LONG_DIM = 22
_BAR_MAX_LONG_DIM = 55

# Trace parameters.
_TRACE_STEP = 6
_TRACE_SEARCH_RADIUS = 16
_TRACE_MAX_STEPS = 150
_TRACE_MAX_DIVERGING_STEPS = 40      # stop if we've been moving away from
                                     # every player for this many steps
_TRACE_MAX_LEN_PX = 500              # absolute cap

# 3-point arc RANSAC thresholds.
_ARC_MIN_CONTOUR_POINTS = 150
_ARC_MIN_R = 200
_ARC_MAX_R = 900
_ARC_INLIER_PX = 3.0
_ARC_MIN_INLIERS = 120
_ARC_MASK_THICKNESS = 18

# Classification thresholds.
_DASHED_MIN_GAPS = 3
_DASHED_MIN_GAP_FRAC = 0.12
_ZIGZAG_NORM_PERP_STD = 0.05
_ZIGZAG_MIN_POINTS = 6
_ZIGZAG_MIN_SIGN_CHANGES = 3


def detect_arrows(
    bgr: np.ndarray,
    player_bboxes: list[tuple[int, int, int, int]] | None = None,
) -> list[DetectedArrow]:
    """Detect all arrow-like paths in the diagram image."""
    if bgr.ndim != 3 or bgr.shape[2] != 3:
        raise ValueError(f"expected BGR 3-channel image, got shape {bgr.shape}")

    player_bboxes = list(player_bboxes or [])
    bw_full = _binarize(bgr)
    bw = _mask_players_and_outer(bw_full, bgr.shape[:2], player_bboxes)

    # Try to register the court for procedural feature masking. If we can,
    # this gives us a precise 3-point-arc mask grounded in the book's known
    # SVG geometry; otherwise we fall back to contour-based ring masking only.
    registration = None
    try:
        try:
            from .registration import register_court
        except ImportError:
            from cv.registration import register_court  # type: ignore
        registration = register_court(bgr)
    except Exception:
        registration = None

    court_mask = _mask_court_features(bw, registration=registration)
    bw_arrows_only = cv2.bitwise_and(bw, cv2.bitwise_not(court_mask))

    heads = _find_arrowheads(bw_arrows_only)
    bars = _find_screen_bars(bw_arrows_only, heads)
    zigzag_strokes = _find_zigzag_strokes(bw_arrows_only, heads, player_bboxes)

    # Build stop-map. Player padding is generous enough to include the
    # ball-handler circle around the digit.
    stop_regions: list[tuple[int, int, int, int]] = []
    for (x, y, cw, ch) in player_bboxes:
        r = int(max(cw, ch) * 1.2)
        cx = x + cw // 2
        cy = y + ch // 2
        stop_regions.append((cx - r, cy - r, r * 2, r * 2))
    for h in heads:
        x, y, cw, ch = h["bbox"]
        stop_regions.append((x - 4, y - 4, cw + 8, ch + 8))

    arrows: list[DetectedArrow] = []

    for head in heads:
        tip, base = _tip_and_base(head["contour"], bw_uneroded=bw_arrows_only)
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
        # If the trace ended without approaching any player, try the alternate
        # shaft direction (the head's "opposite outward" direction) before
        # giving up. The book draws some dribble arrowheads as asymmetric right
        # triangles where the classical tip/base heuristic mis-identifies the
        # direction; rather than rely on the heuristic, we pick the direction
        # whose radial scan produces the longest ink streak.
        def _path_terminates_near_player(p: list[tuple[float, float]]) -> bool:
            if len(p) < 2 or not player_bboxes:
                return False
            last = p[-1]
            for (bx, by, bw_, bh_) in player_bboxes:
                cx = bx + bw_ / 2
                cy = by + bh_ / 2
                if np.hypot(last[0] - cx, last[1] - cy) < 55:
                    return True
            return False

        if not _path_terminates_near_player(path):
            best_dir = _best_shaft_direction(bw_arrows_only, head)
            if best_dir is not None:
                # Re-derive tip as the head-centroid opposite to the shaft dir
                hcx, hcy = head["center"]
                head_rad = max(head["bbox"][2], head["bbox"][3]) * 0.55
                tip_alt = (hcx - best_dir[0] * head_rad,
                           hcy - best_dir[1] * head_rad)
                base_alt = (hcx + best_dir[0] * head_rad * 0.8,
                            hcy + best_dir[1] * head_rad * 0.8)
                # Trace on the pre-court-mask bitmap so we can follow strokes
                # that cross (or graze) court features which the mask happens
                # to overlap. We keep the player/head stop regions.
                alt_path = _trace_stroke(
                    bw,
                    start=base_alt,
                    direction=best_dir,
                    step=_TRACE_STEP,
                    max_steps=_TRACE_MAX_STEPS * 2,
                    search_radius=_TRACE_SEARCH_RADIUS + 10,
                    stop_regions=other_stops,
                    player_bboxes=player_bboxes,
                    max_diverging=_TRACE_MAX_DIVERGING_STEPS * 2,
                    max_len_px=_TRACE_MAX_LEN_PX,
                )
                if _path_terminates_near_player(alt_path):
                    path = alt_path
                    tip = tip_alt

        if len(path) < 2:
            fallback = _nearest_player_along_direction(base, direction, player_bboxes)
            if fallback is None:
                continue
            path = [base, fallback]

        start_px = path[-1]
        end_px = tip

        stroke_pixels = _count_stroke_pixels(bw_full, path)

        is_dashed = _is_dashed(bw_full, path)
        is_zigzag = _is_zigzag(path)
        bar_near_start = _nearest_bar(start_px, bars, within=50)
        has_bar = bar_near_start is not None

        confidence = _confidence(head, path, is_dashed, is_zigzag, has_bar)

        control_points: list[tuple[float, float]] = [
            (float(p[0]), float(p[1])) for p in path
        ]
        control_points.append((float(tip[0]), float(tip[1])))

        arrows.append(
            DetectedArrow(
                start_px=(float(start_px[0]), float(start_px[1])),
                end_px=(float(end_px[0]), float(end_px[1])),
                control_points=control_points,
                has_arrowhead=True,
                has_perpendicular_bar=has_bar,
                is_dashed=is_dashed,
                is_zigzag=is_zigzag,
                confidence=float(confidence),
                stroke_pixels=int(stroke_pixels),
            )
        )

    # Zigzag strokes (dribble by default, screen if terminating at ⊥ bar).
    # These are emitted only when NOT already covered by a head-based arrow.
    head_arrow_heads: set[tuple[int, int]] = set()
    for a in arrows:
        head_arrow_heads.add((int(a.end_px[0]), int(a.end_px[1])))

    for stroke in zigzag_strokes:
        (p1x, p1y), (p2x, p2y) = stroke["endpoints"]
        # Determine which endpoint is the TAIL (nearest player) and which is
        # the HEAD (either the arrowhead side or the ⊥ bar side).
        nearest_to_p1 = _nearest_player_to((p1x, p1y), player_bboxes)
        nearest_to_p2 = _nearest_player_to((p2x, p2y), player_bboxes)
        if nearest_to_p1 is None or nearest_to_p2 is None:
            continue
        d1 = float(np.hypot(nearest_to_p1[0] - p1x, nearest_to_p1[1] - p1y))
        d2 = float(np.hypot(nearest_to_p2[0] - p2x, nearest_to_p2[1] - p2y))
        # Tail = endpoint closer to a player
        if d1 <= d2:
            tail = nearest_to_p1
            head_end = (p2x, p2y)
        else:
            tail = nearest_to_p2
            head_end = (p1x, p1y)

        # If this stroke already has a head-traced arrow emitted, skip.
        head_coord = stroke["head"]["center"] if stroke["head"] else None
        if head_coord is not None:
            # If any existing arrow's end_px is within 20px of this head, skip.
            skipped = False
            for a in arrows:
                if np.hypot(a.end_px[0] - head_coord[0], a.end_px[1] - head_coord[1]) < 20:
                    skipped = True
                    break
            if skipped:
                continue

        # Classify: has arrowhead inside? → dribble (zigzag). Otherwise check
        # for a nearby ⊥ bar at the non-tail end → screen.
        has_arrowhead = stroke["has_head"]

        # Search for a ⊥ bar within ~60px of head_end.
        bar_near_head = _nearest_bar_in_region(
            bw_arrows_only, head_end, min_len=25, max_len=75, within_px=60
        )

        # Decide final head position and kind.
        if has_arrowhead and stroke["head"] is not None:
            # Use the arrowhead's tip as the end (if we can compute it)
            tip_here, _base_here = _tip_and_base(
                stroke["head"]["contour"], bw_uneroded=bw_arrows_only
            )
            final_end = tip_here
            is_zig = True
            is_scr_bar = False
        elif bar_near_head is not None:
            # Screen: end at the bar center
            final_end = bar_near_head
            is_zig = False
            is_scr_bar = True
        else:
            # Pure zigzag without arrowhead — treat as a dribble whose head end
            # is just the far endpoint.
            final_end = head_end
            is_zig = True
            is_scr_bar = False

        # Build a simple polyline: tail → bbox center → final_end (so downstream
        # via-point logic can pick up the midpoint).
        cx_, cy_ = stroke["center"]
        control_points: list[tuple[float, float]] = [
            (float(tail[0]), float(tail[1])),
            (float(cx_), float(cy_)),
            (float(final_end[0]), float(final_end[1])),
        ]

        arrows.append(
            DetectedArrow(
                start_px=(float(tail[0]), float(tail[1])),
                end_px=(float(final_end[0]), float(final_end[1])),
                control_points=control_points,
                has_arrowhead=has_arrowhead,
                has_perpendicular_bar=is_scr_bar,
                is_dashed=False,
                is_zigzag=is_zig,
                confidence=0.70,
                stroke_pixels=int(stroke["area"]),
            )
        )

    # Standalone screen bars (no arrowhead → still a valid screen indicator).
    used_bar_ids: set[int] = set()
    for bar in bars:
        bar_center = bar["center"]
        # Skip if already near a produced arrow endpoint
        if any(
            np.hypot(a.start_px[0] - bar_center[0], a.start_px[1] - bar_center[1]) < 50
            or np.hypot(a.end_px[0] - bar_center[0], a.end_px[1] - bar_center[1]) < 50
            for a in arrows
        ):
            continue
        nearest = _nearest_player_to(bar_center, player_bboxes)
        if nearest is None:
            continue
        # Only accept if there is some ink between player and bar (a short stroke).
        # Sample 20 points along the line; require > 25% ink to accept.
        ink_frac = _line_ink_fraction(bw_arrows_only, nearest, bar_center)
        if ink_frac < 0.25:
            continue
        arrows.append(
            DetectedArrow(
                start_px=(float(nearest[0]), float(nearest[1])),
                end_px=(float(bar_center[0]), float(bar_center[1])),
                control_points=[nearest, bar_center],
                has_arrowhead=False,
                has_perpendicular_bar=True,
                is_dashed=False,
                is_zigzag=False,
                confidence=0.55,
                stroke_pixels=bar["area"],
            )
        )

    # Reject arrows that are too short to be real movements. Short arrows are
    # almost always fragments of adjacent strokes that the detector mistook for
    # separate paths (e.g. arrowhead on a main stroke shows up as a tiny
    # secondary arrow when two heads are close). Real play movements on the
    # Basketball-For-Coaches pages are ≥ 150 px at 400 DPI.
    _MIN_ARROW_LEN_PX = 150
    arrows = [a for a in arrows if a.length_px >= _MIN_ARROW_LEN_PX]

    arrows.sort(key=lambda a: -a.length_px)
    return arrows


# ---------------------------------------------------------------------------
# Binarization / masking
# ---------------------------------------------------------------------------


def _binarize(bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return bw


def _mask_players_and_outer(
    bw: np.ndarray,
    image_shape: tuple[int, int],
    player_bboxes: list[tuple[int, int, int, int]],
) -> np.ndarray:
    """Zero out players (digits + any ball-handler circle around them) and
    the outer court border."""
    h, w = image_shape
    out = bw.copy()

    # The ball-handler digit is circled. Use a DISC of radius
    # max(bbox_dim) * 1.6 around each player to clear the digit AND the
    # surrounding ring. This is a no-op for non-circled digits because the
    # disc is still small and the surrounding area is usually empty.
    for (x, y, cw, ch) in player_bboxes:
        pad = _PLAYER_MASK_PAD
        # Rectangular mask (tight)
        out[max(0, y - pad):min(h, y + ch + pad),
            max(0, x - pad):min(w, x + cw + pad)] = 0
        # Disc mask — catches ball-handler circle
        cx = int(x + cw / 2)
        cy = int(y + ch / 2)
        r = int(max(cw, ch) * 1.1)
        cv2.circle(out, (cx, cy), r, 0, thickness=-1)

    border = _OUTER_BORDER_PX
    out[:border, :] = 0
    out[-border:, :] = 0
    out[:, :border] = 0
    out[:, -border:] = 0
    return out


def _mask_court_features(
    bw: np.ndarray,
    registration: Optional["Registration"] = None,
) -> np.ndarray:
    """Mask static court features that are not arrows.

    If `registration` is provided we use its SVG→pixel inverse homography to
    draw thick strokes over the known court features (outer rect, paint rect,
    FT circle, backboard, rim, 3-point arc for this book). The arc geometry
    is empirically measured from the Basketball-For-Coaches book: it is a
    circular arc through SVG (-22, 6), (0, 25.5), (22, 6) (center ≈ (0, 3.34),
    radius ≈ 22.16 SVG units).

    Without registration we fall back to contour-based ring detection only.
    """
    h, w = bw.shape
    mask = np.zeros_like(bw)

    if registration is not None:
        H_inv = np.linalg.inv(registration.homography)

        def s2p(sx: float, sy: float) -> tuple[int, int]:
            vec = np.array([sx, sy, 1.0])
            out = H_inv @ vec
            return int(round(out[0] / out[2])), int(round(out[1] / out[2]))

        # Outer court rectangle
        outer = registration.paint_pixels.astype(np.int32)
        cv2.polylines(mask, [outer], isClosed=True, color=255, thickness=18)

        # Paint lane vertical sides. The spec places the paint at SVG x=±8
        # but this book draws them asymmetrically (roughly x=-6..+6). Mask
        # narrow bands at every plausible x so that the arrows CROSSING the
        # paint interior still survive.
        for sx in (-8, -7, -6, 6, 7, 8):
            cv2.line(mask, s2p(sx, -0.5), s2p(sx, 19.5), 255, thickness=10)
        # Paint baseline (top) and bottom (FT line)
        cv2.line(mask, s2p(-8, 0), s2p(8, 0), 255, thickness=10)
        cv2.line(mask, s2p(-8, 19), s2p(8, 19), 255, thickness=10)

        # FT circle at SVG (0, 19), r=6 (half-open vs paint — draw both halves)
        ft_c = s2p(0, 19)
        ft_edge = s2p(6, 19)
        ft_r = int(round(np.hypot(ft_edge[0] - ft_c[0], ft_edge[1] - ft_c[1])))
        cv2.circle(mask, ft_c, ft_r, 255, thickness=14)

        # Backboard line: (-3, 4) to (3, 4)
        cv2.line(mask, s2p(-3, 4), s2p(3, 4), 255, thickness=14)

        # Rim small circle
        rim_c = s2p(0, 5.25)
        rim_edge = s2p(0.75, 5.25)
        rim_r = int(round(np.hypot(rim_edge[0] - rim_c[0], rim_edge[1] - rim_c[1]))) + 4
        cv2.circle(mask, rim_c, rim_r, 255, thickness=14)

        # 3-point arc (empirical geometry for this book): circle center
        # (0, 3.34), radius ≈ 22.16. We draw a thick *partial* circle from
        # roughly SVG angle –77° to +77° measured from straight-down.
        arc_cy_svg = 3.34
        arc_r_svg = 22.16
        arc_poly_pts = []
        for theta_deg in np.linspace(-80, 80, 160):
            theta = np.deg2rad(theta_deg)
            x_svg = np.sin(theta) * arc_r_svg
            y_svg = arc_cy_svg + np.cos(theta) * arc_r_svg
            arc_poly_pts.append(s2p(x_svg, y_svg))
        cv2.polylines(mask, [np.array(arc_poly_pts, dtype=np.int32)],
                      isClosed=False, color=255, thickness=18)

        # FT lane tick marks (hash marks along the paint sides)
        for y_svg in (7.0, 10.5, 14.0):
            for side in (-1, 1):
                cv2.line(mask, s2p(side * 8, y_svg), s2p(side * 9.5, y_svg),
                         255, thickness=10)

    # Contour-based small ring detection (half-court, ball-handler circles).
    contours, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        area = cv2.contourArea(c)
        peri = cv2.arcLength(c, True)
        if peri == 0 or area < 120 or area > 14000:
            continue
        circularity = 4 * np.pi * area / (peri * peri)
        x, y, cw, ch = cv2.boundingRect(c)
        aspect = cw / ch if ch else 0
        if circularity > 0.45 and 0.7 < aspect < 1.4 and 22 < max(cw, ch) < 170:
            cv2.drawContours(mask, [c], -1, 255, thickness=10)

    return mask


# ---------------------------------------------------------------------------
# Arrowhead + bar detection
# ---------------------------------------------------------------------------


def _erode_for_tips(bw: np.ndarray) -> np.ndarray:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (_EROSION_KERNEL, _EROSION_KERNEL))
    eroded = cv2.erode(bw, kernel, iterations=1)
    reconnect = cv2.getStructuringElement(
        cv2.MORPH_RECT, (_DILATE_AFTER_ERODE_KERNEL, _DILATE_AFTER_ERODE_KERNEL)
    )
    return cv2.dilate(eroded, reconnect)


def _find_arrowheads(bw: np.ndarray) -> list[dict]:
    eroded = _erode_for_tips(bw)
    num, labels, stats, cents = cv2.connectedComponentsWithStats(eroded, connectivity=8)
    heads: list[dict] = []
    for i in range(1, num):
        x, y, cw, ch, area = stats[i]
        if area < _HEAD_MIN_AREA or area > _HEAD_MAX_AREA:
            continue
        if cw > _HEAD_MAX_DIM or ch > _HEAD_MAX_DIM:
            continue
        aspect = cw / ch if ch else 0
        if not (_HEAD_ASPECT_MIN < aspect < _HEAD_ASPECT_MAX):
            continue
        comp = (labels == i).astype(np.uint8) * 255
        contours, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue
        contour = max(contours, key=cv2.contourArea)
        hull_area = cv2.contourArea(cv2.convexHull(contour))
        solidity = area / hull_area if hull_area else 0
        fill = area / (cw * ch) if cw * ch else 0
        if solidity < _HEAD_MIN_SOLIDITY or fill < _HEAD_MIN_FILL:
            continue
        heads.append({
            "center": (float(cents[i][0]), float(cents[i][1])),
            "bbox": (int(x), int(y), int(cw), int(ch)),
            "area": int(area),
            "solidity": float(solidity),
            "fill": float(fill),
            "contour": contour,
        })
    return heads


def _find_zigzag_strokes(
    bw: np.ndarray,
    heads: list[dict],
    player_bboxes: list[tuple[int, int, int, int]],
) -> list[dict]:
    """Find connected components that look like zigzag strokes.

    A zigzag stroke on a basketball diagram has a long, repeatedly-folded path
    confined to a relatively compact bounding box. This produces an unusually
    high perimeter-to-bbox-diagonal ratio (typically > 3.5) compared to smooth
    strokes (≈ 2.0) or dashed patterns (which fragment into separate small
    components).

    Each returned dict has:
        "bbox": (x, y, w, h)
        "area": int
        "perim": float
        "complexity": perim / bbox_diag
        "endpoints": (p_far1, p_far2)  — two extreme pixels of the component
        "has_head": bool                — is an arrowhead bbox inside the bbox?
        "head":    dict | None          — which arrowhead, if any
        "contour_pts": np.ndarray       — all ink pixels of this component

    Used later to emit dribble arrows (zigzag + arrowhead) and to validate
    screen bars (zigzag stroke terminating at a ⊥ bar).
    """
    # Operate on the UN-ERODED bitmap so the full zigzag body stays connected.
    num, labels, stats, cents = cv2.connectedComponentsWithStats(bw, connectivity=8)
    strokes: list[dict] = []

    for i in range(1, num):
        x, y, cw, ch, area = stats[i]
        # Zigzag strokes on book-size diagrams are bounded: bbox side ≤ 250 px
        # and total area 500-3000 px.
        if area < 500 or area > 3000:
            continue
        if cw > 280 or ch > 280:
            continue
        # Exclude components that are almost entirely inside a player bbox.
        cx_, cy_ = cents[i]
        inside_player = False
        for (bx, by, bw_, bh_) in player_bboxes:
            pad = 20
            if (bx - pad) <= cx_ <= (bx + bw_ + pad) and (by - pad) <= cy_ <= (by + bh_ + pad):
                inside_player = True
                break
        if inside_player:
            continue

        comp_mask = (labels == i).astype(np.uint8) * 255
        contours, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours:
            continue
        perim = float(sum(cv2.arcLength(c, True) for c in contours))
        bbox_diag = float(np.hypot(cw, ch))
        if bbox_diag < 20:
            continue
        complexity = perim / bbox_diag
        if complexity < 3.2:
            continue
        # Reject if bbox is EXTREMELY long in one direction (likely a long
        # straight line that happens to be thick).
        if max(cw, ch) / max(min(cw, ch), 1) > 8:
            continue

        # Find extreme endpoints: two pixels in the component farthest apart.
        ys, xs = np.where(labels == i)
        if len(xs) < 4:
            continue
        # Heuristic: use bbox corners as candidates first, then refine.
        pts = np.column_stack((xs, ys))
        # Farthest-pair approx via PCA principal axis: project onto principal
        # axis, take min/max projected points.
        mean = pts.mean(axis=0)
        centered = pts - mean
        cov = np.cov(centered.T)
        _, vecs = np.linalg.eigh(cov)
        axis = vecs[:, -1]  # largest eigenvector
        projected = centered @ axis
        p_far1 = tuple(pts[int(np.argmin(projected))].astype(float))
        p_far2 = tuple(pts[int(np.argmax(projected))].astype(float))

        # Is an arrowhead inside this bbox?
        head_inside = None
        for he in heads:
            hx, hy, hcw, hch = he["bbox"]
            hcx = hx + hcw / 2
            hcy = hy + hch / 2
            if (x - 5) <= hcx <= (x + cw + 5) and (y - 5) <= hcy <= (y + ch + 5):
                head_inside = he
                break

        strokes.append({
            "bbox": (int(x), int(y), int(cw), int(ch)),
            "area": int(area),
            "perim": perim,
            "complexity": float(complexity),
            "endpoints": (p_far1, p_far2),
            "has_head": head_inside is not None,
            "head": head_inside,
            "center": (float(cx_), float(cy_)),
            "label_index": int(i),
        })
    return strokes


def _find_screen_bars(bw: np.ndarray, heads: list[dict]) -> list[dict]:
    """Find thin elongated rectangles. Reject those that are aligned with a
    nearby arrowhead (those are shaft fragments, not screens)."""
    eroded = _erode_for_tips(bw)
    num, labels, stats, cents = cv2.connectedComponentsWithStats(eroded, connectivity=8)
    bars: list[dict] = []
    for i in range(1, num):
        x, y, cw, ch, area = stats[i]
        if area < _BAR_MIN_AREA or area > _BAR_MAX_AREA:
            continue
        aspect = cw / ch if ch else 0
        if aspect <= 0:
            continue
        long_aspect = max(aspect, 1 / aspect)
        if long_aspect < _BAR_MIN_LONG_ASPECT:
            continue
        fill = area / (cw * ch) if cw * ch else 0
        if fill < _BAR_MIN_FILL:
            continue
        long_dim = max(cw, ch)
        if long_dim < _BAR_MIN_LONG_DIM or long_dim > _BAR_MAX_LONG_DIM:
            continue
        is_horizontal = cw >= ch
        bar_angle = 0.0 if is_horizontal else np.pi / 2
        # Reject if aligned with any nearby arrowhead's axis (shaft fragment)
        cx_, cy_ = cents[i]
        is_shaft_fragment = False
        for head in heads:
            hx, hy = head["center"]
            if np.hypot(hx - cx_, hy - cy_) > 180:
                continue
            # Compute arrowhead axis from its min-area rect
            rect = cv2.minAreaRect(head["contour"])
            (_, _), _, head_angle = rect
            # OpenCV angle ∈ (-90, 0]. Normalize both angles to [0, π).
            head_theta = np.deg2rad((head_angle + 180) % 180)
            diff = abs(head_theta - bar_angle)
            diff = min(diff, np.pi - diff)
            if diff < np.deg2rad(25):
                is_shaft_fragment = True
                break
        if is_shaft_fragment:
            continue
        bars.append({
            "center": (float(cx_), float(cy_)),
            "bbox": (int(x), int(y), int(cw), int(ch)),
            "area": int(area),
            "aspect": float(aspect),
            "fill": float(fill),
        })
    return bars


# ---------------------------------------------------------------------------
# Tip / base / tracing
# ---------------------------------------------------------------------------


def _tip_and_base(
    contour: np.ndarray,
    bw_uneroded: Optional[np.ndarray] = None,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return (tip, base) for an arrowhead.

    Strategy:
      1. Fit a minimum-enclosing triangle and get its three vertices.
      2. If `bw_uneroded` is provided, measure — for each vertex — how much
         OUTSIDE-THE-TRIANGLE ink lies in a small disc pointed OUTWARD from
         the triangle centroid. The vertex with the most external ink is the
         BASE (where the shaft attaches). The vertex farthest from that base
         is the TIP. This works for both isoceles and right-triangle
         arrowhead shapes — critical because the book draws some dribble
         arrowheads as asymmetric right triangles, and the classical
         "tip = farthest from opposite edge" heuristic mis-identifies the
         right-angle vertex as the tip.
      3. Without `bw_uneroded` we fall back to "tip = vertex farthest from
         the opposite edge, base = midpoint of that opposite edge".
    """
    _, triangle = cv2.minEnclosingTriangle(contour)
    tri = triangle.reshape(3, 2)
    centroid = tri.mean(axis=0)

    if bw_uneroded is not None:
        h, w = bw_uneroded.shape

        def shaft_score(vertex: np.ndarray) -> int:
            """Longest contiguous ink run in the OUTSIDE half-plane past the
            vertex. The base has a long streak (the shaft); the tip has at
            most short fragments of adjacent strokes."""
            out_dir = vertex - centroid
            mag = float(np.linalg.norm(out_dir))
            if mag < 1e-6:
                return 0
            out_dir = out_dir / mag
            best_run = 0
            max_r = 24
            for angle_deg in range(-60, 61, 15):
                ang = np.deg2rad(angle_deg)
                rx = out_dir[0] * np.cos(ang) - out_dir[1] * np.sin(ang)
                ry = out_dir[0] * np.sin(ang) + out_dir[1] * np.cos(ang)
                run = 0
                longest = 0
                for r in range(2, max_r + 1):
                    px = int(round(vertex[0] + rx * r))
                    py = int(round(vertex[1] + ry * r))
                    if not (0 <= px < w and 0 <= py < h):
                        break
                    if bw_uneroded[py, px] > 0:
                        run += 1
                        longest = max(longest, run)
                    else:
                        run = 0
                best_run = max(best_run, longest)
            return best_run

        scores = [shaft_score(tri[i]) for i in range(3)]
        base_idx = int(np.argmax(scores))
        base = tri[base_idx]
        distances = [float(np.hypot(tri[i][0] - base[0], tri[i][1] - base[1]))
                     for i in range(3)]
        tip_idx = int(np.argmax(distances))
        tip = tri[tip_idx]
        # Only trust this override when the base's shaft run is clearly longer
        # than the tip's (absolute min + 2x margin).
        if scores[base_idx] >= 10 and scores[base_idx] >= 2 * scores[tip_idx]:
            return (float(tip[0]), float(tip[1])), (float(base[0]), float(base[1]))

    # Classical fallback: tip = vertex farthest from opposite edge.
    tip_idx = 0
    best_dist = -1.0
    for i in range(3):
        v = tri[i]
        a = tri[(i + 1) % 3]
        b = tri[(i + 2) % 3]
        ab = b - a
        av = v - a
        cross = abs(ab[0] * av[1] - ab[1] * av[0])
        mag = np.hypot(ab[0], ab[1]) or 1e-9
        d = cross / mag
        if d > best_dist:
            best_dist = d
            tip_idx = i
    tip = tri[tip_idx]

    base_a = tri[(tip_idx + 1) % 3]
    base_b = tri[(tip_idx + 2) % 3]
    base_mid = (base_a + base_b) / 2.0

    if bw_uneroded is not None:
        # Pick the base-edge point whose neighborhood contains the most OUTSIDE
        # ink (i.e. ink just beyond the arrowhead triangle). Sample 5 points
        # along the base edge.
        h, w = bw_uneroded.shape
        candidates = []
        for t in np.linspace(0.1, 0.9, 5):
            bp = base_a + t * (base_b - base_a)
            # Look OUTWARD (away from tip) in a 10-px disc, count ink.
            outward = bp + (bp - tip) / (np.linalg.norm(bp - tip) + 1e-9) * 8
            x0 = int(max(0, outward[0] - 10))
            x1 = int(min(w, outward[0] + 10))
            y0 = int(max(0, outward[1] - 10))
            y1 = int(min(h, outward[1] + 10))
            patch = bw_uneroded[y0:y1, x0:x1]
            candidates.append((np.count_nonzero(patch), bp))
        candidates.sort(key=lambda t: -t[0])
        if candidates and candidates[0][0] > 0:
            best_bp = candidates[0][1]
            base_mid = best_bp

    return (float(tip[0]), float(tip[1])), (float(base_mid[0]), float(base_mid[1]))


def _trace_stroke(
    bw: np.ndarray,
    start: tuple[float, float],
    direction: tuple[float, float],
    step: float,
    max_steps: int,
    search_radius: int,
    stop_regions: list[tuple[int, int, int, int]],
    player_bboxes: list[tuple[int, int, int, int]],
    max_diverging: int,
    max_len_px: float,
) -> list[tuple[float, float]]:
    """Greedy stroke-tracer with early termination to avoid wandering.

    Additional stopping criteria (on top of "no ink ahead"):
      * If the distance to the NEAREST player has strictly increased for
        `max_diverging` consecutive steps we abort — the stroke is not
        leading to any player.
      * If cumulative polyline length exceeds `max_len_px` we abort.
    """
    h, w = bw.shape
    dx, dy = direction
    mag = np.hypot(dx, dy) or 1.0
    dx /= mag
    dy /= mag

    current = np.array(start, dtype=float)
    path: list[tuple[float, float]] = [tuple(current.tolist())]
    traveled = 0.0

    def nearest_player_dist(pt: np.ndarray) -> float:
        if not player_bboxes:
            return float("inf")
        return min(
            np.hypot(pt[0] - (bx + bw_ / 2), pt[1] - (by + bh_ / 2))
            for (bx, by, bw_, bh_) in player_bboxes
        )

    last_pd = nearest_player_dist(current)
    diverging = 0

    for _ in range(max_steps):
        if traveled > max_len_px:
            break
        # Early termination: if we are within 35 px of a player center, snap.
        if player_bboxes:
            for (bx, by, bw_, bh_) in player_bboxes:
                cx = bx + bw_ / 2
                cy = by + bh_ / 2
                if np.hypot(current[0] - cx, current[1] - cy) < 35:
                    path.append((float(cx), float(cy)))
                    return path
        target = current + np.array([dx * step, dy * step])
        tx, ty = target
        x0 = int(max(0, tx - search_radius))
        x1 = int(min(w, tx + search_radius))
        y0 = int(max(0, ty - search_radius))
        y1 = int(min(h, ty + search_radius))
        if x1 <= x0 or y1 <= y0:
            break
        window = bw[y0:y1, x0:x1]
        ys, xs = np.where(window > 0)
        if len(xs) == 0:
            break
        abs_x = xs + x0
        abs_y = ys + y0
        forward = (abs_x - current[0]) * dx + (abs_y - current[1]) * dy
        fwd_mask = forward > 0
        if not np.any(fwd_mask):
            # Dead end ahead — terminate (do not U-turn).
            # Snap to the nearest player if one is close.
            if player_bboxes:
                best_cx, best_cy = None, None
                best_d = float("inf")
                for (bx, by, bw_p, bh_p) in player_bboxes:
                    cx = bx + bw_p / 2
                    cy = by + bh_p / 2
                    d = float(np.hypot(current[0] - cx, current[1] - cy))
                    if d < best_d:
                        best_d = d
                        best_cx, best_cy = cx, cy
                if best_cx is not None and best_d < 90:
                    path.append((float(best_cx), float(best_cy)))
            break
        abs_x = abs_x[fwd_mask]
        abs_y = abs_y[fwd_mask]
        dists = np.hypot(abs_x - tx, abs_y - ty)
        best = int(np.argmin(dists))
        new = np.array([float(abs_x[best]), float(abs_y[best])])

        # Stop region?
        for (rx, ry, rw_, rh_) in stop_regions:
            if rx <= new[0] <= rx + rw_ and ry <= new[1] <= ry + rh_:
                path.append(tuple(new.tolist()))
                # If we stopped at a player's region, snap to their center.
                for (bx, by, bw_p, bh_p) in player_bboxes:
                    cx = bx + bw_p / 2
                    cy = by + bh_p / 2
                    if abs(rx + rw_ / 2 - cx) < 2 and abs(ry + rh_ / 2 - cy) < 2:
                        path[-1] = (float(cx), float(cy))
                        break
                return path

        traveled += float(np.hypot(new[0] - current[0], new[1] - current[1]))

        # Divergence check
        pd = nearest_player_dist(new)
        if pd >= last_pd:
            diverging += 1
        else:
            diverging = 0
        last_pd = pd
        if diverging >= max_diverging:
            # Don't record this step; trace is wandering.
            break

        # Direction update (lightly smoothed, favour responsive tracking so
        # we can follow zig-zag strokes).
        ndx = new[0] - current[0]
        ndy = new[1] - current[1]
        nmag = np.hypot(ndx, ndy) or 1.0
        ndx /= nmag
        ndy /= nmag
        dx = 0.3 * dx + 0.7 * ndx
        dy = 0.3 * dy + 0.7 * ndy
        mag2 = np.hypot(dx, dy) or 1.0
        dx /= mag2
        dy /= mag2
        current = new
        path.append(tuple(current.tolist()))

    # Snap the final point to the nearest player centroid if very close
    if player_bboxes and path:
        last = np.array(path[-1])
        for (bx, by, bw_, bh_) in player_bboxes:
            cx = bx + bw_ / 2
            cy = by + bh_ / 2
            if np.hypot(last[0] - cx, last[1] - cy) < 70:
                path[-1] = (float(cx), float(cy))
                break
    return path


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------


def _count_stroke_pixels(bw: np.ndarray, path: list[tuple[float, float]]) -> int:
    if len(path) < 2:
        return 0
    mask = np.zeros_like(bw)
    pts_np = np.array(path, dtype=np.int32)
    cv2.polylines(mask, [pts_np], isClosed=False, color=255, thickness=7)
    overlap = cv2.bitwise_and(bw, mask)
    return int(np.count_nonzero(overlap))


def _is_dashed(bw: np.ndarray, path: list[tuple[float, float]]) -> bool:
    """Count separate ink runs in a thin corridor around the traced polyline.

    A solid arrow produces ONE continuous run; a dashed/dotted arrow produces
    several (one per dash). We rasterize a thin corridor around the traced
    polyline, intersect with the bitmap, and count connected components.
    """
    if len(path) < 2:
        return False
    arr = np.array(path)
    segment_lens = np.hypot(np.diff(arr[:, 0]), np.diff(arr[:, 1]))
    total = float(segment_lens.sum())
    if total < 40:
        return False

    h, w = bw.shape
    corridor = np.zeros_like(bw)
    pts = arr.astype(np.int32)
    cv2.polylines(corridor, [pts], isClosed=False, color=255, thickness=11)
    overlap = cv2.bitwise_and(bw, corridor)
    # Count connected components (ignore background label 0).
    num, _, stats, _ = cv2.connectedComponentsWithStats(overlap, connectivity=8)
    # Filter components by min size to ignore specks.
    big = sum(1 for i in range(1, num) if stats[i][4] >= 8)
    # Coverage of polyline length
    covered = int(np.count_nonzero(overlap))
    total_corridor = int(np.count_nonzero(corridor))
    if total_corridor == 0:
        return False
    coverage = covered / total_corridor
    # Dashed heuristic: many small components + moderate coverage
    return big >= _DASHED_MIN_GAPS + 1 and coverage < 0.85


def _is_zigzag(path: list[tuple[float, float]]) -> bool:
    if len(path) < _ZIGZAG_MIN_POINTS:
        return False
    p0 = np.array(path[0])
    p1 = np.array(path[-1])
    chord = float(np.hypot(*(p1 - p0)))
    if chord < 30:
        return False
    t = (p1 - p0) / chord
    n = np.array([-t[1], t[0]])
    arr = np.array(path) - p0
    perp = arr @ n
    std = float(np.std(perp))
    norm_std = std / chord
    signs = np.sign(perp)
    sign_changes = int(np.sum(signs[:-1] * signs[1:] < 0))
    return norm_std > _ZIGZAG_NORM_PERP_STD and sign_changes >= _ZIGZAG_MIN_SIGN_CHANGES


def _best_shaft_direction(
    bw: np.ndarray,
    head: dict,
) -> Optional[tuple[float, float]]:
    """Find the shaft direction for an arrowhead by scanning all 360° from the
    head's center and picking the angle whose radial ink streak is the longest.

    Returns a unit vector pointing FROM the head INTO the shaft (i.e. the
    direction to trace BACK along the stroke).
    """
    h, w = bw.shape
    cx, cy = head["center"]
    hw, hh = head["bbox"][2], head["bbox"][3]
    head_r = max(hw, hh) * 0.6  # skip over the head body
    max_r = int(head_r) + 30    # how far to scan

    best_score = 0
    best_dir: Optional[tuple[float, float]] = None
    for angle_deg in range(0, 360, 10):
        ang = np.deg2rad(angle_deg)
        dx = np.cos(ang)
        dy = np.sin(ang)
        # Count ink pixels in a short corridor of 3 px width along this ray
        # past the head's interior.
        hits = 0
        for r in range(int(head_r), max_r):
            px_ = int(round(cx + dx * r))
            py_ = int(round(cy + dy * r))
            if not (0 <= px_ < w and 0 <= py_ < h):
                break
            # Check a 3x3 neighborhood to tolerate sub-pixel jitter.
            x0 = max(0, px_ - 1)
            x1 = min(w, px_ + 2)
            y0 = max(0, py_ - 1)
            y1 = min(h, py_ + 2)
            if np.any(bw[y0:y1, x0:x1]):
                hits += 1
        if hits > best_score:
            best_score = hits
            best_dir = (float(dx), float(dy))

    # Require a meaningful streak (at least ~14 ink hits in the scan range)
    if best_score < 14:
        return None
    return best_dir


def _nearest_bar_in_region(
    bw: np.ndarray,
    point: tuple[float, float],
    min_len: int,
    max_len: int,
    within_px: int,
) -> Optional[tuple[float, float]]:
    """Scan a `within_px` × `within_px` window around `point` for a horizontal
    or vertical bar-like run in the binary image. Returns the bar's center
    pixel if found, else None.

    A "bar" is any row or column of `bw` with between `min_len` and `max_len`
    consecutive ink pixels.
    """
    h, w = bw.shape
    px, py = int(point[0]), int(point[1])
    x0 = max(0, px - within_px)
    x1 = min(w, px + within_px)
    y0 = max(0, py - within_px)
    y1 = min(h, py + within_px)
    if x1 <= x0 or y1 <= y0:
        return None
    roi = bw[y0:y1, x0:x1]

    best: Optional[tuple[float, float, float]] = None  # (score, cx, cy)

    # Horizontal bars: scan each row, find the longest consecutive run
    for r in range(roi.shape[0]):
        row = roi[r]
        # Find runs of True
        in_run = False
        run_start = 0
        for c in range(len(row)):
            if row[c] > 0:
                if not in_run:
                    in_run = True
                    run_start = c
            else:
                if in_run:
                    run_len = c - run_start
                    if min_len <= run_len <= max_len:
                        cx = x0 + run_start + run_len / 2
                        cy = y0 + r
                        score = run_len
                        if best is None or score > best[0]:
                            best = (score, cx, cy)
                    in_run = False
        if in_run:
            run_len = len(row) - run_start
            if min_len <= run_len <= max_len:
                cx = x0 + run_start + run_len / 2
                cy = y0 + r
                score = run_len
                if best is None or score > best[0]:
                    best = (score, cx, cy)

    # Vertical bars: same scan but along columns
    for c in range(roi.shape[1]):
        col = roi[:, c]
        in_run = False
        run_start = 0
        for r in range(len(col)):
            if col[r] > 0:
                if not in_run:
                    in_run = True
                    run_start = r
            else:
                if in_run:
                    run_len = r - run_start
                    if min_len <= run_len <= max_len:
                        cx = x0 + c
                        cy = y0 + run_start + run_len / 2
                        score = run_len
                        if best is None or score > best[0]:
                            best = (score, cx, cy)
                    in_run = False
        if in_run:
            run_len = len(col) - run_start
            if min_len <= run_len <= max_len:
                cx = x0 + c
                cy = y0 + run_start + run_len / 2
                score = run_len
                if best is None or score > best[0]:
                    best = (score, cx, cy)

    if best is None:
        return None
    return (float(best[1]), float(best[2]))


def _nearest_bar(point: tuple[float, float], bars: list[dict], within: float) -> Optional[dict]:
    best = None
    best_d = within
    for b in bars:
        d = np.hypot(b["center"][0] - point[0], b["center"][1] - point[1])
        if d < best_d:
            best_d = d
            best = b
    return best


def _nearest_player_along_direction(
    base: tuple[float, float],
    direction: tuple[float, float],
    player_bboxes: list[tuple[int, int, int, int]],
) -> Optional[tuple[float, float]]:
    if not player_bboxes:
        return None
    dx, dy = direction
    mag = np.hypot(dx, dy) or 1.0
    dx /= mag
    dy /= mag
    best = None
    best_score = float("inf")
    for (x, y, cw, ch) in player_bboxes:
        cx = x + cw / 2
        cy = y + ch / 2
        vx = cx - base[0]
        vy = cy - base[1]
        proj = vx * dx + vy * dy
        if proj < 0:
            continue
        perp = abs(vx * (-dy) + vy * dx)
        score = perp + 0.2 * proj
        if score < best_score:
            best_score = score
            best = (cx, cy)
    return best


def _nearest_player_to(
    point: tuple[float, float],
    player_bboxes: list[tuple[int, int, int, int]],
) -> Optional[tuple[float, float]]:
    if not player_bboxes:
        return None
    best = None
    best_d = float("inf")
    for (x, y, cw, ch) in player_bboxes:
        cx = x + cw / 2
        cy = y + ch / 2
        d = np.hypot(cx - point[0], cy - point[1])
        if d < best_d:
            best_d = d
            best = (cx, cy)
    return best


def _line_ink_fraction(bw: np.ndarray, a: tuple[float, float], b: tuple[float, float]) -> float:
    n = 20
    samples = np.linspace(np.array(a), np.array(b), n)
    h, w = bw.shape
    hits = 0
    for sx, sy in samples:
        x0 = max(0, int(sx) - 3)
        x1 = min(w, int(sx) + 4)
        y0 = max(0, int(sy) - 3)
        y1 = min(h, int(sy) + 4)
        if x1 <= x0 or y1 <= y0:
            continue
        if np.any(bw[y0:y1, x0:x1]):
            hits += 1
    return hits / n


def _confidence(
    head: dict,
    path: list[tuple[float, float]],
    is_dashed: bool,
    is_zigzag: bool,
    has_bar: bool,
) -> float:
    c = 0.4
    c += 0.2 * min(1.0, head["solidity"])
    c += 0.15 * (1.0 if head["fill"] >= 0.45 else 0.5)
    if len(path) >= 4:
        c += 0.1
    if is_zigzag or is_dashed or has_bar:
        c += 0.1
    return float(min(1.0, c))


# ---------------------------------------------------------------------------
# __main__ — run on page 60 panel 0 and emit overlay
# ---------------------------------------------------------------------------


def _load_page_60_panel_0() -> np.ndarray:
    import pdfplumber  # lazy

    here = Path(__file__).resolve()
    # Try the neighbouring backend knowledge-base first.
    for candidate in (
        here.parents[3] / "knowledge-base" / "raw" / "basketball-for-coaches.pdf",
        here.parents[2] / "knowledge-base" / "raw" / "basketball-for-coaches.pdf",
    ):
        if candidate.exists():
            pdf_path = candidate
            break
    else:
        raise FileNotFoundError("basketball-for-coaches.pdf not found in expected locations")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[59]
        img0 = page.images[0]
        bbox = (img0["x0"], img0["top"], img0["x1"], img0["bottom"])
        pil = page.crop(bbox).to_image(resolution=400).original
    arr = np.array(pil)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


_OVERLAY_COLORS: dict[str, tuple[int, int, int]] = {
    "solid": (0, 200, 0),     # green
    "dashed": (200, 100, 0),  # orange
    "zigzag": (0, 0, 220),    # red
    "screen": (200, 0, 200),  # magenta
    "unknown": (120, 120, 120),
}


def _overlay(bgr: np.ndarray, arrows: list[DetectedArrow]) -> np.ndarray:
    out = bgr.copy()
    for idx, a in enumerate(arrows, 1):
        color = _OVERLAY_COLORS.get(a.kind, (180, 180, 180))
        pts = np.array(a.control_points, dtype=np.int32)
        if len(pts) >= 2:
            cv2.polylines(out, [pts], isClosed=False, color=color, thickness=3)
        cv2.circle(out, (int(a.start_px[0]), int(a.start_px[1])), 6, color, -1)
        cv2.circle(out, (int(a.end_px[0]), int(a.end_px[1])), 6, color, 2)
        label = f"#{idx} {a.kind}"
        cv2.putText(out, label, (int(a.start_px[0]) + 8, int(a.start_px[1]) - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
    # Legend
    legend_items = [("solid (cut)", _OVERLAY_COLORS["solid"]),
                    ("dashed (pass)", _OVERLAY_COLORS["dashed"]),
                    ("zigzag (dribble)", _OVERLAY_COLORS["zigzag"]),
                    ("screen (⊥ bar)", _OVERLAY_COLORS["screen"])]
    y0 = 20
    for name, color in legend_items:
        cv2.rectangle(out, (20, y0 - 14), (36, y0), color, -1)
        cv2.putText(out, name, (44, y0), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1, cv2.LINE_AA)
        y0 += 20
    return out


def _main() -> int:
    here = Path(__file__).resolve()
    repo_root = here.parents[2]
    results_dir = repo_root / "results" / "cv"
    results_dir.mkdir(parents=True, exist_ok=True)
    out_path = results_dir / "arrows_page_60_panel_0.png"

    bgr = _load_page_60_panel_0()

    # Use the existing probe to get player bboxes (OCR-verified → masks only
    # real digits, not random glyphs).
    try:
        from .probe import detect_glyph_candidates, ocr_digit
    except ImportError:  # pragma: no cover
        sys.path.insert(0, str(here.parent.parent))
        from cv.probe import detect_glyph_candidates, ocr_digit  # type: ignore

    cands = detect_glyph_candidates(bgr)
    player_bboxes: list[tuple[int, int, int, int]] = []
    for c in cands:
        if ocr_digit(bgr, c["bbox"]):
            player_bboxes.append(c["bbox"])
    if not player_bboxes:
        player_bboxes = [c["bbox"] for c in cands]

    arrows = detect_arrows(bgr, player_bboxes=player_bboxes)

    print(f"Page 60 panel 0: detected {len(arrows)} arrow(s)")
    print("-" * 72)
    for i, a in enumerate(arrows, 1):
        print(
            f"  #{i:>2}  kind={a.kind:<7}  "
            f"start=({a.start_px[0]:>6.1f},{a.start_px[1]:>6.1f})  "
            f"end=({a.end_px[0]:>6.1f},{a.end_px[1]:>6.1f})  "
            f"len={a.length_px:>5.1f}px  "
            f"dashed={a.is_dashed!s:<5}  zigzag={a.is_zigzag!s:<5}  "
            f"bar={a.has_perpendicular_bar!s:<5}  head={a.has_arrowhead!s:<5}  "
            f"px={a.stroke_pixels:>5}  conf={a.confidence:.2f}"
        )

    overlay = _overlay(bgr, arrows)
    cv2.imwrite(str(out_path), overlay)
    print(f"\nOverlay saved to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
