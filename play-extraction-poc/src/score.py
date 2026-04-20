"""Score each strategy's extraction against ground truth.

Writes results/scores.json with per-player-per-strategy deltas and per-strategy
summary stats. Missing players (emitted by ground truth but absent from
extraction) count against viable_pct and correctable_pct — they do not receive
a "verdict" so they fall into neither bucket.
"""
from __future__ import annotations

import json
from math import sqrt
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent.parent
GROUND_TRUTH = HERE / "data" / "ground-truth.json"
EXTRACTIONS = HERE / "results" / "extractions"
OUT = HERE / "results" / "scores.json"

THRESHOLDS = {"viable": 2.0, "correctable": 5.0}


def euclidean(a, b) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def parse_yaml_safely(text: str):
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Drop the opening fence; drop the closing fence if present.
        if lines[-1].startswith("```"):
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        text = "\n".join(lines)
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        return None


def score_extraction(extracted, truth):
    if not extracted or not isinstance(extracted, dict) or "play" not in extracted:
        return {"parse_error": True, "deltas": {}, "summary": None}

    play = extracted["play"] or {}
    extracted_players = play.get("players") or {}
    truth_players = truth["expected_players"]

    deltas = {}
    for pid, truth_pos in truth_players.items():
        if pid not in extracted_players:
            deltas[pid] = {"delta": None, "missing": True}
            continue
        ext_pos = extracted_players[pid]
        if not (isinstance(ext_pos, list) and len(ext_pos) == 2):
            deltas[pid] = {"delta": None, "missing": True, "reason": "malformed coordinate"}
            continue
        d = euclidean(ext_pos, truth_pos)
        if d <= THRESHOLDS["viable"]:
            verdict = "viable"
        elif d <= THRESHOLDS["correctable"]:
            verdict = "correctable"
        else:
            verdict = "failed"
        deltas[pid] = {
            "delta": round(d, 2),
            "extracted": ext_pos,
            "truth": truth_pos,
            "verdict": verdict,
        }

    valid_deltas = [d["delta"] for d in deltas.values() if d.get("delta") is not None]
    if not valid_deltas:
        return {"parse_error": False, "deltas": deltas, "summary": None}

    viable_count = sum(1 for d in deltas.values() if d.get("verdict") == "viable")
    correctable_count = sum(
        1 for d in deltas.values() if d.get("verdict") in ("viable", "correctable")
    )
    total = len(truth_players)

    return {
        "parse_error": False,
        "deltas": deltas,
        "summary": {
            "mean_delta": round(sum(valid_deltas) / len(valid_deltas), 2),
            "max_delta": round(max(valid_deltas), 2),
            "viable_pct": round(viable_count / total * 100, 1),
            "correctable_pct": round(correctable_count / total * 100, 1),
            "missing_count": sum(1 for d in deltas.values() if d.get("missing")),
        },
    }


def main() -> None:
    if not GROUND_TRUTH.exists():
        raise SystemExit(f"Missing {GROUND_TRUTH}. Hand-annotate it before scoring.")
    truth = json.loads(GROUND_TRUTH.read_text())
    results = {}

    for diagram_id, truth_data in truth.items():
        results[diagram_id] = {}
        for strategy in ["a", "b", "c"]:
            ext_path = EXTRACTIONS / f"{diagram_id}_strategy_{strategy}.yaml"
            err_path = EXTRACTIONS / f"{diagram_id}_strategy_{strategy}.error.txt"
            if not ext_path.exists():
                results[diagram_id][strategy] = {
                    "error": "api_error" if err_path.exists() else "file_missing",
                }
                continue
            extracted = parse_yaml_safely(ext_path.read_text())
            results[diagram_id][strategy] = score_extraction(extracted, truth_data)

    strategy_summary = {}
    for s in ["a", "b", "c"]:
        viable_pcts = []
        correctable_pcts = []
        for diagram_id in truth:
            summary = results[diagram_id][s].get("summary") if isinstance(results[diagram_id][s], dict) else None
            if summary:
                viable_pcts.append(summary["viable_pct"])
                correctable_pcts.append(summary["correctable_pct"])
        if viable_pcts:
            strategy_summary[s] = {
                "mean_viable_pct": round(sum(viable_pcts) / len(viable_pcts), 1),
                "mean_correctable_pct": round(sum(correctable_pcts) / len(correctable_pcts), 1),
                "diagrams_scored": len(viable_pcts),
            }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"per_diagram": results, "per_strategy": strategy_summary}, indent=2))
    print(json.dumps(strategy_summary, indent=2))


if __name__ == "__main__":
    main()
