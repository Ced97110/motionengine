"""Assembly layer: combine detected players + detected arrows into Movements.

This module consumes the outputs of two sibling modules (`probe.py` for player
detection, `arrows.py` + `strokes.py` for arrow detection and classification)
and produces a list of `AssembledMovement` objects that match the authored-play
source shape used by the YAML emitter and the React viewer.

The module is deterministic, numpy-only (no LLM calls), and does not mutate
its inputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np

MovementType = Literal["cut", "pass", "screen", "dribble", "handoff"]

# ---------------------------------------------------------------------------
# Association tuning constants
# ---------------------------------------------------------------------------

# Maximum pixel distance (as a fraction of image width) a player can be from an
# arrow endpoint to be considered the "owner" of that endpoint.
OWNER_MAX_FRAC = 0.15
RECEIVER_MAX_FRAC = 0.15

# Two arrows are considered duplicates if their start *and* end points are
# within this pixel distance.
DEDUP_EPS_PX = 5.0

# Default assumed image width if we cannot infer one from the data.
DEFAULT_IMAGE_WIDTH_PX = 1024.0


# ---------------------------------------------------------------------------
# Input shapes (sibling modules will produce these — we only need the fields
# that we read here, so tests can pass lightweight stand-ins)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DetectedPlayer:
    digit: str  # "1" .. "5"
    center_px: tuple[float, float]
    center_svg: tuple[float, float]


@dataclass(frozen=True)
class DetectedArrow:
    start_px: tuple[float, float]
    end_px: tuple[float, float]
    control_points_px: list[tuple[float, float]]
    movement_type: MovementType
    confidence: float


# ---------------------------------------------------------------------------
# Output shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AssembledMovement:
    player_id: str
    type: MovementType
    from_svg: tuple[float, float] | None
    to_svg: tuple[float, float] | None
    to_player_id: str | None
    via_svg: tuple[float, float] | None
    confidence: float
    raw_arrow_ref: int
    # Optional diagnostic fields (populated on best effort, never mutated later)
    notes: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------


def pixel_to_svg(
    px: tuple[float, float],
    homography: np.ndarray,
) -> tuple[float, float]:
    """Project a pixel coordinate through a 3x3 homography into SVG space.

    Returns a plain `tuple[float, float]` (never a numpy array) so downstream
    YAML serialization stays clean.
    """
    if homography is None:
        raise ValueError("homography must not be None")
    h = np.asarray(homography, dtype=np.float64)
    if h.shape != (3, 3):
        raise ValueError(f"homography must be 3x3, got {h.shape}")

    vec = np.array([float(px[0]), float(px[1]), 1.0], dtype=np.float64)
    projected = h @ vec
    w = projected[2]
    if w == 0.0:
        # Degenerate projection — fall back to the raw pixel coords so we fail
        # soft rather than crashing the whole pipeline.
        return (float(px[0]), float(px[1]))
    return (float(projected[0] / w), float(projected[1] / w))


def _euclidean(a: tuple[float, float], b: tuple[float, float]) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return float(np.hypot(dx, dy))


def _infer_image_width(
    players: list[DetectedPlayer],
    arrows: list[DetectedArrow],
) -> float:
    """Infer an image-width proxy from the spread of detected points.

    This keeps the module standalone — callers don't have to thread the image
    dimensions through. If the spread is too small to be meaningful, we fall
    back to `DEFAULT_IMAGE_WIDTH_PX`.
    """
    xs: list[float] = []
    for p in players:
        xs.append(p.center_px[0])
    for a in arrows:
        xs.append(a.start_px[0])
        xs.append(a.end_px[0])
        for cp in a.control_points_px:
            xs.append(cp[0])
    if len(xs) < 2:
        return DEFAULT_IMAGE_WIDTH_PX
    spread = max(xs) - min(xs)
    # Arrow/player detections rarely reach the absolute edge; pad by 20% so the
    # threshold is not artificially tight for plays clustered near centre.
    inferred = spread * 1.2
    return max(inferred, DEFAULT_IMAGE_WIDTH_PX * 0.5)


def _nearest_player(
    point: tuple[float, float],
    players: list[DetectedPlayer],
    exclude_digit: str | None = None,
) -> tuple[DetectedPlayer | None, float, bool]:
    """Return (player, distance_px, is_tie) for the nearest player to `point`.

    A tie is reported when the two nearest players are within 1.0 px of each
    other — useful for handoff detection. `exclude_digit` lets callers request
    the second-nearest player (e.g., the receiver that is not the passer).
    """
    best: DetectedPlayer | None = None
    best_d = float("inf")
    second_d = float("inf")
    for p in players:
        if exclude_digit is not None and p.digit == exclude_digit:
            continue
        d = _euclidean(point, p.center_px)
        if d < best_d:
            second_d = best_d
            best_d = d
            best = p
        elif d < second_d:
            second_d = d
    is_tie = best is not None and (second_d - best_d) < 1.0
    return best, best_d, is_tie


def _dedup_arrows(arrows: list[DetectedArrow]) -> list[tuple[int, DetectedArrow]]:
    """Collapse near-duplicate arrows.

    Two arrows are duplicates when *both* endpoints are within `DEDUP_EPS_PX`.
    We keep the higher-confidence one and preserve the original index so the
    `raw_arrow_ref` on the output traces back to the caller's input list.
    """
    kept: list[tuple[int, DetectedArrow]] = []
    for idx, arrow in enumerate(arrows):
        duplicate_of: int | None = None
        for i, (_orig_idx, existing) in enumerate(kept):
            if (
                _euclidean(arrow.start_px, existing.start_px) <= DEDUP_EPS_PX
                and _euclidean(arrow.end_px, existing.end_px) <= DEDUP_EPS_PX
            ):
                duplicate_of = i
                break
        if duplicate_of is None:
            kept.append((idx, arrow))
        else:
            existing_idx, existing = kept[duplicate_of]
            if arrow.confidence > existing.confidence:
                kept[duplicate_of] = (idx, arrow)
    return kept


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def _seed_positions(players: list[DetectedPlayer]) -> dict[str, tuple[float, float]]:
    """Mutable map digit → current pixel position, seeded from original detections."""
    return {p.digit: p.center_px for p in players}


def _nearest_from_positions(
    point: tuple[float, float],
    positions: dict[str, tuple[float, float]],
    exclude_digit: str | None = None,
) -> tuple[str | None, float]:
    """Nearest (digit, distance_px) using a current-position map. Used after
    movements have updated player locations."""
    best_digit: str | None = None
    best_d = float("inf")
    for digit, pos in positions.items():
        if exclude_digit is not None and digit == exclude_digit:
            continue
        d = _euclidean(point, pos)
        if d < best_d:
            best_d = d
            best_digit = digit
    return best_digit, best_d


def assemble_movements(
    players: list[DetectedPlayer],
    arrows: list[DetectedArrow],
    homography: Any,
) -> list[AssembledMovement]:
    """Assemble Movements from detected players + classified arrows.

    Algorithm (matches the task brief):
      1. For each arrow, determine who performs it by finding the player
         nearest to the arrow's start pixel. That player is the MOVER (for
         cut/dribble/screen) or the PASSER (for pass/handoff).
      2. For passes, find the player nearest to the arrow's end pixel and
         assign them as the receiver.
      3. For cut/dribble/screen, the destination is `pixel_to_svg(end_px)`
         and the origin is the mover's digit-center SVG (downstream phases
         may override the origin if a prior movement repositioned the player).
      4. Handoff arrows: identify both participants via nearest-neighbour at
         the arrow's midpoint.
      5. Confidence = arrow.confidence * (1 - normalized start distance).

    Arrows that cannot be associated with any player within
    `OWNER_MAX_FRAC * image_width` are skipped. A note is logged on the
    returned movements whenever a weaker association is used.
    """
    if homography is None:
        raise ValueError("homography must not be None")
    H = np.asarray(homography, dtype=np.float64)
    if H.shape != (3, 3):
        raise ValueError(f"homography must be 3x3, got {H.shape}")

    if not players:
        return []

    image_width = _infer_image_width(players, arrows)
    owner_threshold_px = OWNER_MAX_FRAC * image_width
    receiver_threshold_px = RECEIVER_MAX_FRAC * image_width

    deduped = _dedup_arrows(arrows)

    # Track current player positions. Each non-pass movement (cut, dribble,
    # screen, handoff) updates the mover's current position to the arrow's end.
    # This lets downstream arrows (e.g. a 2nd pass from where P2 dribbled to)
    # attribute correctly even though P2's ORIGINAL detected position is far.
    positions = _seed_positions(players)
    digit_lookup = {p.digit: p for p in players}

    out: list[AssembledMovement] = []
    for original_idx, arrow in deduped:
        notes: list[str] = []

        # ---- 1. Identify the mover / passer --------------------------------
        # First try original detection positions (strict nearest-neighbour).
        mover, mover_d, mover_tie = _nearest_player(arrow.start_px, players)
        # If that fails, fall back to DYNAMIC positions (updated by prior
        # movements). This recovers passes and follow-up moves that originate
        # from where a player moved to, not their original standing position.
        if mover is None or mover_d > owner_threshold_px:
            dyn_digit, dyn_d = _nearest_from_positions(arrow.start_px, positions)
            if dyn_digit is not None and dyn_d <= owner_threshold_px:
                mover = digit_lookup[dyn_digit]
                mover_d = dyn_d
                mover_tie = False
                notes.append("dynamic_position")
            else:
                print(
                    f"[assemble] skipping arrow #{original_idx} ({arrow.movement_type}): "
                    f"no player within {owner_threshold_px:.1f}px of start "
                    f"{arrow.start_px} (nearest dist={mover_d:.1f}px, "
                    f"dyn dist={dyn_d:.1f}px)"
                )
                continue
        if mover_tie:
            notes.append("mover_tie")

        # ---- Build base fields ---------------------------------------------
        from_svg = mover.center_svg
        to_svg = pixel_to_svg(arrow.end_px, H)

        to_player_id: str | None = None
        via_svg: tuple[float, float] | None = None

        mtype: MovementType = arrow.movement_type

        # ---- 2. Pass receiver ----------------------------------------------
        if mtype == "pass":
            receiver, recv_d, _recv_tie = _nearest_player(
                arrow.end_px, players, exclude_digit=mover.digit
            )
            if receiver is not None and recv_d <= receiver_threshold_px:
                to_player_id = receiver.digit
                # Snap to_svg to the receiver's SVG position so the emitted YAML
                # lines up with the digit center — pixel noise otherwise makes
                # the viewer draw a slightly-off endpoint.
                to_svg = receiver.center_svg
            else:
                notes.append("no_receiver_within_threshold")
                if receiver is not None:
                    notes.append(f"nearest_receiver_dist_px={recv_d:.1f}")

        # ---- 4. Handoff: two players at the midpoint -----------------------
        elif mtype == "handoff":
            mid_px = (
                (arrow.start_px[0] + arrow.end_px[0]) / 2.0,
                (arrow.start_px[1] + arrow.end_px[1]) / 2.0,
            )
            other, other_d, _ = _nearest_player(
                mid_px, players, exclude_digit=mover.digit
            )
            if other is not None and other_d <= receiver_threshold_px:
                to_player_id = other.digit
                via_svg = pixel_to_svg(mid_px, H)
            else:
                notes.append("no_handoff_partner")

        # ---- 3. Screen / dribble / cut: optional via (waypoint) ------------
        # For dribbles that clearly route around a waypoint (control points),
        # surface the midpoint as `via_svg` for downstream assembly. We use the
        # middle control point if there are 3+ and it is not colinear with the
        # endpoints.
        if mtype in ("dribble", "screen") and len(arrow.control_points_px) >= 3:
            mid_cp = arrow.control_points_px[len(arrow.control_points_px) // 2]
            # Only record when the waypoint deviates from the straight line.
            deviation = _point_to_segment_dist(
                mid_cp, arrow.start_px, arrow.end_px
            )
            if deviation > 5.0:
                via_svg = pixel_to_svg(mid_cp, H)

        # ---- 5. Confidence --------------------------------------------------
        normalized_start_d = min(mover_d / owner_threshold_px, 1.0)
        confidence = float(arrow.confidence) * (1.0 - normalized_start_d)
        # Clamp to [0, 1] to be defensive.
        confidence = max(0.0, min(1.0, confidence))

        out.append(
            AssembledMovement(
                player_id=mover.digit,
                type=mtype,
                from_svg=from_svg,
                to_svg=to_svg,
                to_player_id=to_player_id,
                via_svg=via_svg,
                confidence=confidence,
                raw_arrow_ref=original_idx,
                notes=tuple(notes),
            )
        )

        # Update dynamic positions. Cuts, dribbles, screens, handoffs move
        # the player to the arrow's end. Passes do NOT move the passer; the
        # receiver is already at the end of the arrow.
        if mtype != "pass":
            positions[mover.digit] = arrow.end_px

    return out


def _point_to_segment_dist(
    point: tuple[float, float],
    seg_a: tuple[float, float],
    seg_b: tuple[float, float],
) -> float:
    """Perpendicular distance from `point` to the segment a-b (clamped at ends)."""
    ax, ay = seg_a
    bx, by = seg_b
    px, py = point
    dx = bx - ax
    dy = by - ay
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq == 0.0:
        return _euclidean(point, seg_a)
    t = ((px - ax) * dx + (py - ay) * dy) / seg_len_sq
    t = max(0.0, min(1.0, t))
    closest = (ax + t * dx, ay + t * dy)
    return _euclidean(point, closest)


# ---------------------------------------------------------------------------
# Manual test harness — synthesized page-60 "Black" fixture
# ---------------------------------------------------------------------------


def _format_movement(m: AssembledMovement) -> str:
    def fmt_pt(p: tuple[float, float] | None) -> str:
        if p is None:
            return "None"
        return f"({p[0]:.1f},{p[1]:.1f})"

    parts = [
        f"player={m.player_id}",
        f"type={m.type}",
    ]
    if m.to_player_id is not None:
        parts.append(f"to_player={m.to_player_id}")
    parts.append(f"from={fmt_pt(m.from_svg)}")
    parts.append(f"to={fmt_pt(m.to_svg)}")
    if m.via_svg is not None:
        parts.append(f"via={fmt_pt(m.via_svg)}")
    parts.append(f"confidence={m.confidence:.2f}")
    parts.append(f"raw_arrow_ref={m.raw_arrow_ref}")
    if m.notes:
        parts.append(f"notes={list(m.notes)}")
    return " ".join(parts)


if __name__ == "__main__":
    players = [
        DetectedPlayer(digit="1", center_px=(510, 623), center_svg=(0.0, 30.8)),
        DetectedPlayer(digit="2", center_px=(163, 428), center_svg=(-17.8, 20.8)),
        DetectedPlayer(digit="3", center_px=(865, 421), center_svg=(18.3, 20.4)),
        DetectedPlayer(digit="4", center_px=(77, 153), center_svg=(-22.3, 6.6)),
        DetectedPlayer(digit="5", center_px=(946, 149), center_svg=(22.5, 6.4)),
    ]

    arrows = [
        # 0: pass 1 -> 2
        DetectedArrow(
            start_px=(510, 623),
            end_px=(163, 428),
            control_points_px=[(510, 623), (336, 525), (163, 428)],
            movement_type="pass",
            confidence=0.9,
        ),
        # 1: screen by 4
        DetectedArrow(
            start_px=(77, 153),
            end_px=(270, 280),
            control_points_px=[(77, 153), (170, 215), (270, 280)],
            movement_type="screen",
            confidence=0.85,
        ),
        # 2: dribble by 2
        DetectedArrow(
            start_px=(163, 428),
            end_px=(430, 70),
            control_points_px=[(163, 428), (350, 250), (430, 70)],
            movement_type="dribble",
            confidence=0.9,
        ),
        # 3: cut by 5
        DetectedArrow(
            start_px=(946, 149),
            end_px=(600, 200),
            control_points_px=[(946, 149), (770, 175), (600, 200)],
            movement_type="cut",
            confidence=0.9,
        ),
        # 4: pass 2(now at 430,70) -> 5(now at 600,200)
        DetectedArrow(
            start_px=(430, 70),
            end_px=(600, 200),
            control_points_px=[(430, 70), (515, 135), (600, 200)],
            movement_type="pass",
            confidence=0.8,
        ),
    ]

    H = np.eye(3, dtype=np.float32)
    movements = assemble_movements(players, arrows, H)

    print(f"Assembled {len(movements)} movements from {len(arrows)} arrows:")
    for i, m in enumerate(movements):
        print(f"  Movement {i}: {_format_movement(m)}")
