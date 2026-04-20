"""Render extracted plays onto the court SVG for visual inspection.

Two modes:
  - default: one SVG per (diagram × strategy) showing ground-truth (green) vs
    extracted (orange) with dashed yellow deltas
  - `python -m src.overlay --ground-truth`: one SVG per diagram showing only the
    ground-truth annotation, for user verification before `make score` runs
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent.parent
GROUND_TRUTH = HERE / "data" / "ground-truth.json"
EXTRACTIONS = HERE / "results" / "extractions"
OVERLAYS = HERE / "results" / "overlays"
GT_OVERLAYS = HERE / "data" / "ground-truth-overlays"

SVG_HEADER = """<svg viewBox="-28 -3 56 50" xmlns="http://www.w3.org/2000/svg" width="680" height="560">
<rect x="-25" y="0" width="50" height="47" fill="#1a1a1a" stroke="#444" stroke-width="0.3"/>
<rect x="-8" y="0" width="16" height="19" fill="none" stroke="#666" stroke-width="0.3"/>
<circle cx="0" cy="19" r="6" fill="none" stroke="#666" stroke-width="0.3"/>
<path d="M -22 4 A 23.75 23.75 0 0 0 22 4" fill="none" stroke="#666" stroke-width="0.3"/>
<circle cx="0" cy="5.25" r="0.75" fill="none" stroke="#d4722b" stroke-width="0.2"/>"""

SVG_FOOTER = "</svg>"


def parse_yaml_safely(text: str):
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:-1] if lines[-1].startswith("```") else lines[1:]
        text = "\n".join(lines)
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        return None


def render_ground_truth_only(truth, title: str) -> str:
    parts = [SVG_HEADER,
             f'<text x="-27" y="-1" fill="white" font-size="1.5" font-family="monospace">{title}</text>']
    for pid, pos in truth["expected_players"].items():
        parts.append(
            f'<circle cx="{pos[0]}" cy="{pos[1]}" r="1" fill="#22c55e" opacity="0.85"/>'
            f'<text x="{pos[0]+1.2}" y="{pos[1]+0.4}" fill="#22c55e" font-size="1.4" font-family="monospace">{pid}</text>'
        )
    for m in truth.get("expected_movements", []):
        fx, fy = m.get("from", [0, 0])
        tx, ty = m.get("to", [0, 0]) if "to" in m else (0, 0)
        color = "#d4722b" if m.get("type") == "pass" else "#e5e5e5"
        dash = 'stroke-dasharray="0.4 0.4"' if m.get("type") == "pass" else ""
        if "to" in m:
            parts.append(
                f'<line x1="{fx}" y1="{fy}" x2="{tx}" y2="{ty}" stroke="{color}" stroke-width="0.25" {dash}/>'
            )
    parts.append(SVG_FOOTER)
    return "\n".join(parts)


def render_overlay(extracted, truth, title: str) -> str:
    parts = [SVG_HEADER,
             f'<text x="-27" y="-1" fill="white" font-size="1.5" font-family="monospace">{title}</text>']
    # Ground truth (green)
    for pid, pos in truth["expected_players"].items():
        parts.append(
            f'<circle cx="{pos[0]}" cy="{pos[1]}" r="1" fill="#22c55e" opacity="0.7"/>'
            f'<text x="{pos[0]+1.2}" y="{pos[1]+0.4}" fill="#22c55e" font-size="1.4" font-family="monospace">{pid}T</text>'
        )
    # Extracted (orange) + connecting deltas (yellow dashed)
    if extracted and isinstance(extracted, dict) and "play" in extracted and extracted["play"]:
        for pid, pos in (extracted["play"].get("players") or {}).items():
            if not (isinstance(pos, list) and len(pos) == 2):
                continue
            parts.append(
                f'<circle cx="{pos[0]}" cy="{pos[1]}" r="1" fill="#f97316" opacity="0.7"/>'
                f'<text x="{pos[0]+1.2}" y="{pos[1]-1}" fill="#f97316" font-size="1.4" font-family="monospace">{pid}E</text>'
            )
            truth_pos = truth["expected_players"].get(pid)
            if truth_pos:
                parts.append(
                    f'<line x1="{pos[0]}" y1="{pos[1]}" x2="{truth_pos[0]}" y2="{truth_pos[1]}" '
                    f'stroke="#fbbf24" stroke-width="0.15" stroke-dasharray="0.4 0.4"/>'
                )
    parts.append(SVG_FOOTER)
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ground-truth", action="store_true",
                    help="Render ground-truth-only overlays to data/ground-truth-overlays/ for user verification.")
    args = ap.parse_args()

    if not GROUND_TRUTH.exists():
        raise SystemExit(f"Missing {GROUND_TRUTH}.")
    truth_data = json.loads(GROUND_TRUTH.read_text())

    if args.ground_truth:
        GT_OVERLAYS.mkdir(parents=True, exist_ok=True)
        for diagram_id, truth in truth_data.items():
            svg = render_ground_truth_only(truth, f"{diagram_id} · ground truth")
            out = GT_OVERLAYS / f"{diagram_id}_ground_truth.svg"
            out.write_text(svg)
            print(f"→ {out}")
        return

    OVERLAYS.mkdir(parents=True, exist_ok=True)
    for diagram_id, truth in truth_data.items():
        for strategy in ["a", "b", "c"]:
            ext_path = EXTRACTIONS / f"{diagram_id}_strategy_{strategy}.yaml"
            if not ext_path.exists():
                continue
            extracted = parse_yaml_safely(ext_path.read_text())
            svg = render_overlay(extracted, truth, f"{diagram_id} · Strategy {strategy.upper()}")
            out = OVERLAYS / f"{diagram_id}_strategy_{strategy}.svg"
            out.write_text(svg)
            print(f"→ {out}")


if __name__ == "__main__":
    main()
