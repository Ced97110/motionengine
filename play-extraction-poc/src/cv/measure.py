"""Small measurement helper — convert pixel coordinates in a panel to SVG.

Used to ground-truth arrow endpoints for the fidelity eval without running
arrows.py (which would be circular since arrows.py is what we're validating).

Usage:
    .venv/bin/python -m src.cv.measure 15 0 '762,240' '572,230' '320,580' '770,265'

For each pixel pair, prints ``px → SVG`` with 1-decimal SVG.
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import pdfplumber

from .registration import pixel_to_svg, register_court

HERE = Path(__file__).resolve().parent.parent.parent
PDF = HERE.parent / "knowledge-base" / "raw" / "basketball-for-coaches.pdf"


def extract_panel(page_number: int, panel_index: int) -> np.ndarray:
    with pdfplumber.open(PDF) as pdf:
        page = pdf.pages[page_number - 1]
        img_meta = page.images[panel_index]
        bbox = (img_meta["x0"], img_meta["top"], img_meta["x1"], img_meta["bottom"])
        pil = page.crop(bbox).to_image(resolution=400).original
    arr = np.array(pil)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def main() -> int:
    if len(sys.argv) < 4:
        print("usage: measure <page> <panel> <px,py> [<px,py> ...]")
        return 1
    page = int(sys.argv[1])
    panel = int(sys.argv[2])
    bgr = extract_panel(page, panel)
    h, w = bgr.shape[:2]
    reg = register_court(bgr)
    if reg is None:
        print("ERROR: registration failed")
        return 1
    print(f"page {page} panel {panel}: image {w}x{h}, registration confidence={reg.confidence}")
    for arg in sys.argv[3:]:
        try:
            px_s, py_s = arg.split(",")
            px, py = float(px_s), float(py_s)
        except ValueError:
            print(f"  skip '{arg}': expected 'px,py'")
            continue
        sx, sy = pixel_to_svg(reg, px, py)
        print(f"  px({px:6.0f},{py:6.0f}) → SVG({sx:+6.1f},{sy:+6.1f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
