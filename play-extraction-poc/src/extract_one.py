"""Run all 3 strategies against ONE diagram file (for targeted testing).

Usage:
    python -m src.extract_one diagram_01_page_060-060.jpg

Outputs YAML to results/extractions/ as the main extract.py would. Useful for
iterating on a single play without re-running the full 5-diagram batch.
"""
from __future__ import annotations

import sys
from pathlib import Path

from src.extract import DIAGRAMS_DIR, OUT_DIR, STRATEGIES


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m src.extract_one <diagram-filename.jpg>")
    name = sys.argv[1]
    diagram = DIAGRAMS_DIR / name
    if not diagram.exists():
        raise SystemExit(f"Not found: {diagram}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diagram_id = diagram.stem
    print(f"=== {diagram_id} ===")
    for strategy_name, runner in STRATEGIES:
        print(f"  strategy {strategy_name}...", flush=True)
        try:
            output = runner(diagram)
            out_path = OUT_DIR / f"{diagram_id}_strategy_{strategy_name}.yaml"
            out_path.write_text(output)
            print(f"    → {out_path.name} ({len(output)} bytes)")
        except Exception as e:  # noqa: BLE001
            err_path = OUT_DIR / f"{diagram_id}_strategy_{strategy_name}.error.txt"
            err_path.write_text(f"{type(e).__name__}: {e}\n")
            print(f"    ✗ {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
