"""Rasterize the 5 selected pages of the NBA Playbook PDF to JPEG at 200 DPI."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SELECTED = HERE / "data" / "selected-pages.json"
OUT_DIR = HERE / "data" / "diagrams"
REPO_ROOT = HERE.parent.parent  # motion/


def resolve_pdf_path(raw: str) -> Path:
    """Resolve source_pdf relative to repo root if not absolute."""
    p = Path(raw)
    if p.is_absolute():
        return p
    # Try interpreting as repo-root-relative first, then backend-relative.
    candidates = [REPO_ROOT / p, HERE.parent / p]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]  # pdftoppm will fail loudly with a real path


def rasterize() -> None:
    config = json.loads(SELECTED.read_text())
    pdf = resolve_pdf_path(config["source_pdf"])
    if not pdf.exists():
        raise SystemExit(f"Source PDF not found: {pdf}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for diagram in config["diagrams"]:
        page = diagram["page"]
        out_prefix = OUT_DIR / f"diagram_{diagram['id']:02d}_page_{page:03d}"
        subprocess.run(
            [
                "pdftoppm", "-jpeg", "-r", "200",
                "-f", str(page), "-l", str(page),
                str(pdf), str(out_prefix),
            ],
            check=True,
        )
        print(f"Rasterized p.{page} → {out_prefix}-{page}.jpg")


if __name__ == "__main__":
    rasterize()
