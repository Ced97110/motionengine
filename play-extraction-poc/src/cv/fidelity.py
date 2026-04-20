"""Structural fidelity scorer for CV-extracted plays vs. hand-authored ground truth.

Given:
- a CV-produced YAML (emitted by ``emit.py``) and
- an expected-movements spec loaded from ``eval/cv-fidelity-cases.jsonl``,

produce a per-movement 0/1 match score + aggregate precision / recall / F1.

This is the Eval Discipline gate — visual "looks right" is not enough; every
extraction must clear a scored structural diff before we call it shipped.

Matching rules:

1. Candidate actuals must share ``player`` and ``type`` with the expected.
2. For ``pass`` / ``handoff``: ``to_player`` must match.
3. For ``cut`` / ``dribble`` / ``screen``: ``to`` must be within
   ``svg_tolerance`` (default 3.0) of the expected ``to``.
4. For spatial movements with an expected ``via`` waypoint, ``via`` is a
   PARTIAL credit bonus — if present and within tolerance it earns +0.25,
   missing/wrong ``via`` does not zero the whole movement.
5. Player-starting-position drift is reported separately (not in the F1)
   because it is a registration-layer concern, not a movement concern.

Pure stdlib + ``pyyaml`` (available in the backend venv). No LLM calls.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

MovementType = Literal["cut", "pass", "screen", "dribble", "handoff"]

# Per-movement partial-credit weights. Sum = 1.0 for a non-spatial movement
# (pass/handoff: player+type+to_player). Spatial movements can exceed 1.0
# with a correct ``via`` (capped at 1.0 for aggregation).
_WEIGHT_PLAYER = 0.25
_WEIGHT_TYPE = 0.25
_WEIGHT_TO_PLAYER = 0.50
_WEIGHT_TO_SVG = 0.50
_WEIGHT_VIA_BONUS = 0.25


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExpectedMovement:
    player: str
    type: MovementType
    to_player: str | None = None
    to_svg: tuple[float, float] | None = None
    from_svg: tuple[float, float] | None = None
    via_svg: tuple[float, float] | None = None


@dataclass(frozen=True)
class ActualMovement:
    player: str
    type: MovementType
    to_player: str | None = None
    to_svg: tuple[float, float] | None = None
    from_svg: tuple[float, float] | None = None
    via_svg: tuple[float, float] | None = None


@dataclass(frozen=True)
class MovementMatch:
    expected_index: int
    actual_index: int | None  # None = unmatched (missed expectation)
    score: float               # 0.0 .. 1.25 (spatial + via bonus)
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class FidelityReport:
    case_id: str
    matches: tuple[MovementMatch, ...]
    unmatched_actuals: tuple[int, ...]   # indices into actual movements list
    expected_total: int
    actual_total: int

    @property
    def matched_count(self) -> int:
        return sum(1 for m in self.matches if m.actual_index is not None)

    @property
    def aggregate_score(self) -> float:
        """Sum of per-movement scores, capped at 1.0 per movement for P/R."""
        return sum(min(1.0, m.score) for m in self.matches)

    @property
    def precision(self) -> float:
        if self.actual_total == 0:
            return 0.0
        return self.aggregate_score / self.actual_total

    @property
    def recall(self) -> float:
        if self.expected_total == 0:
            return 0.0
        return self.aggregate_score / self.expected_total

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        if p + r == 0:
            return 0.0
        return 2 * p * r / (p + r)


# ---------------------------------------------------------------------------
# YAML loading (matches emit.py output: triple-fenced, flow-style coords)
# ---------------------------------------------------------------------------


def _strip_fence(raw: str) -> str:
    """Drop a leading ```yaml fence and trailing ``` if present."""
    lines = raw.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines)


def load_actual_yaml(path: str | Path) -> list[ActualMovement]:
    """Load CV YAML output into a list of ActualMovement.

    We intentionally avoid constructing a rich object model — downstream code
    only needs the flat movement list for scoring.
    """
    import yaml  # lazy; keeps fidelity importable in pure-stdlib contexts

    text = Path(path).read_text(encoding="utf-8")
    doc = yaml.safe_load(_strip_fence(text))
    if not doc or "play" not in doc:
        return []
    out: list[ActualMovement] = []
    for phase in doc["play"].get("phases") or []:
        for m in phase.get("movements") or []:
            out.append(
                ActualMovement(
                    player=str(m["player"]),
                    type=m["type"],
                    to_player=(str(m["to_player"]) if m.get("to_player") else None),
                    to_svg=(tuple(m["to"]) if m.get("to") is not None else None),
                    from_svg=(tuple(m["from"]) if m.get("from") is not None else None),
                    via_svg=(tuple(m["via"]) if m.get("via") is not None else None),
                )
            )
    return out


def load_cases(path: str | Path) -> list[dict[str, Any]]:
    """Load ``eval/cv-fidelity-cases.jsonl`` into a list of dicts."""
    out: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(json.loads(line))
    return out


def expected_from_case(case: dict[str, Any]) -> list[ExpectedMovement]:
    out: list[ExpectedMovement] = []
    for m in case["expected"]["movements"]:
        out.append(
            ExpectedMovement(
                player=str(m["player"]),
                type=m["type"],
                to_player=(str(m["to_player"]) if m.get("to_player") else None),
                to_svg=(tuple(m["to"]) if m.get("to") is not None else None),
                from_svg=(tuple(m["from"]) if m.get("from") is not None else None),
                via_svg=(tuple(m["via"]) if m.get("via") is not None else None),
            )
        )
    return out


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _euclidean(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _score_pair(
    expected: ExpectedMovement,
    actual: ActualMovement,
    tolerance: float,
) -> tuple[float, list[str]]:
    """Return (score_0_to_1_25, notes) for one candidate pairing."""
    notes: list[str] = []
    score = 0.0

    if expected.player != actual.player:
        return 0.0, [f"player_mismatch:{expected.player}!={actual.player}"]
    score += _WEIGHT_PLAYER

    if expected.type != actual.type:
        return 0.0, [f"type_mismatch:{expected.type}!={actual.type}"]
    score += _WEIGHT_TYPE

    if expected.type in ("pass", "handoff"):
        if expected.to_player is not None:
            if actual.to_player == expected.to_player:
                score += _WEIGHT_TO_PLAYER
            else:
                notes.append(
                    f"to_player_mismatch:{expected.to_player}!={actual.to_player}"
                )
                return score, notes
    else:
        # Spatial movement: to_svg must be within tolerance.
        if expected.to_svg is not None and actual.to_svg is not None:
            d = _euclidean(expected.to_svg, actual.to_svg)
            if d <= tolerance:
                score += _WEIGHT_TO_SVG
                notes.append(f"to_drift={d:.2f}")
            else:
                notes.append(f"to_out_of_tolerance:{d:.2f}>{tolerance}")
                return score, notes
        elif expected.to_svg is None:
            # No spatial expectation — credit full weight.
            score += _WEIGHT_TO_SVG
        else:
            notes.append("to_svg_missing_in_actual")
            return score, notes

        # Via waypoint — partial credit.
        if expected.via_svg is not None:
            if actual.via_svg is not None:
                d = _euclidean(expected.via_svg, actual.via_svg)
                if d <= tolerance:
                    score += _WEIGHT_VIA_BONUS
                    notes.append(f"via_drift={d:.2f}")
                else:
                    notes.append(f"via_out_of_tolerance:{d:.2f}>{tolerance}")
            else:
                notes.append("via_missing_in_actual")

    return score, notes


def score_case(
    expected: list[ExpectedMovement],
    actual: list[ActualMovement],
    svg_tolerance: float = 3.0,
) -> FidelityReport:
    """Greedy best-match scorer.

    Each expected movement takes the actual movement that maximizes its score,
    on a first-come-first-served basis (no combinatorial assignment — the
    expected list is small, typically ≤ 6). Actuals can only match once.
    """
    used_actuals: set[int] = set()
    matches: list[MovementMatch] = []

    for ei, exp in enumerate(expected):
        best_idx: int | None = None
        best_score = -1.0
        best_notes: list[str] = []
        for ai, act in enumerate(actual):
            if ai in used_actuals:
                continue
            s, notes = _score_pair(exp, act, svg_tolerance)
            if s > best_score:
                best_score = s
                best_idx = ai
                best_notes = notes
        if best_idx is not None and best_score >= _WEIGHT_PLAYER + _WEIGHT_TYPE:
            used_actuals.add(best_idx)
            matches.append(
                MovementMatch(
                    expected_index=ei,
                    actual_index=best_idx,
                    score=best_score,
                    notes=tuple(best_notes),
                )
            )
        else:
            matches.append(
                MovementMatch(
                    expected_index=ei,
                    actual_index=None,
                    score=0.0,
                    notes=("unmatched",),
                )
            )

    unmatched = tuple(i for i in range(len(actual)) if i not in used_actuals)
    return FidelityReport(
        case_id="",
        matches=tuple(matches),
        unmatched_actuals=unmatched,
        expected_total=len(expected),
        actual_total=len(actual),
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def format_report(report: FidelityReport, case_id: str = "") -> str:
    lines: list[str] = []
    cid = case_id or report.case_id or "(unnamed)"
    lines.append(f"=== {cid} ===")
    lines.append(
        f"expected={report.expected_total} actual={report.actual_total} "
        f"matched={report.matched_count} "
        f"P={report.precision:.2f} R={report.recall:.2f} F1={report.f1:.2f}"
    )
    for m in report.matches:
        flag = "OK " if m.actual_index is not None else "MISS"
        note_str = ", ".join(m.notes) if m.notes else ""
        actual_ref = f"actual[{m.actual_index}]" if m.actual_index is not None else "—"
        lines.append(
            f"  [{flag}] expected[{m.expected_index}] → {actual_ref}  "
            f"score={m.score:.2f}  {note_str}"
        )
    for ai in report.unmatched_actuals:
        lines.append(f"  [SPUR] actual[{ai}] — no expected match (false positive)")
    return "\n".join(lines)
