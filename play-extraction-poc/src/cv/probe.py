"""CV probe v2 — detect player markers via connected-component analysis.

Previous approach (Hough circles) was wrong: Basketball For Coaches only
circles the ball-handler. The other players are bare digit glyphs on the
court. So we detect DIGITS, not circles.

Pipeline:
  1. Extract each embedded diagram panel from the PDF via pdfplumber.
  2. Threshold to isolate the darkest ink (digits + court lines + arrows).
  3. Find connected components with stats.
  4. Filter candidates by:
       - bounding-box size (digit-range aspect + area bounds)
       - stroke density (digits are denser than line segments)
       - isolation (not adjacent to large line clusters)
  5. Report candidate centroids + overlay on the source image.

This version focuses on RECALL first (find all 5 players, accept false
positives) and a follow-up step will handle classification via OCR once
tesseract is wired in.

Usage:
    python -m src.cv.probe 60
    python -m src.cv.probe 15 50 60 70 80
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import pdfplumber
import pytesseract

from .registration import register_court, pixel_to_svg

HERE = Path(__file__).resolve().parent.parent.parent
PDF_PATH = HERE.parent / "knowledge-base" / "raw" / "basketball-for-coaches.pdf"
OUT_DIR = HERE / "results" / "cv"


def extract_diagrams(page_number: int):
    out = []
    with pdfplumber.open(PDF_PATH) as pdf:
        page = pdf.pages[page_number - 1]
        for idx, img in enumerate(page.images):
            bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
            cropped = page.crop(bbox)
            pil_img = cropped.to_image(resolution=400).original
            out.append((idx, pil_img))
    return out


def detect_glyph_candidates(bgr: np.ndarray) -> list[dict]:
    """Connected-component candidates that look like isolated text glyphs.

    Digits on this book's diagrams are:
      - darker than court background (near-black on off-white)
      - compact (bounding box roughly square, 0.3-1.5 aspect ratio)
      - medium-sized relative to image (neither tiny artifacts nor big arcs)
      - not touching another large dark region

    Returns candidates with centroid, bbox, area, aspect, fill density.
    """
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # Otsu threshold pulls out the darkest ink reliably on these pages
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Suppress single-pixel specks without merging nearby digits
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    num, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    h, w = gray.shape
    image_area = h * w

    # Empirical thresholds from page 60 analysis (at 400 DPI, diagrams ~1000 px):
    #   - player digits (1-5): height 47-51 px, area 560-900, aspect 0.4-0.75
    #   - arrow heads: height 10-20 px, aspect ~1.0 (rejected)
    #   - dashed-line segments: height 10-14 px (rejected by min height)
    #   - rim circle + FT circle bowls: aspect >1.0 (rejected)
    # Scale height threshold by image dimension so it generalizes to other DPIs.
    min_h = int(h * 0.035)      # roughly 35 px at 1000 px image
    min_area = int(image_area * 0.0004)

    candidates: list[dict] = []
    for i in range(1, num):  # skip background label 0
        x, y, cw, ch, area = stats[i]
        cx, cy = centroids[i]
        if ch < min_h:
            continue
        if area < min_area or area > image_area * 0.008:
            continue
        aspect = cw / ch if ch > 0 else 0
        # Digit glyphs are taller than wide. "1" can be as narrow as 0.35.
        # Reject near-square blobs (arrow-head composites, rim circle).
        if aspect < 0.3 or aspect > 0.85:
            continue
        # Fill density — digits 0.40-0.70; hollow circles <0.25; filled arrows >0.85
        density = area / (cw * ch) if cw * ch > 0 else 0
        if density < 0.35 or density > 0.80:
            continue
        # Reject edge-adjacent components (clipped by the diagram border)
        edge_margin = min(x, y, w - (x + cw), h - (y + ch))
        if edge_margin < 4:
            continue
        candidates.append({
            "label_id": int(i),
            "center": (float(cx), float(cy)),
            "bbox": (int(x), int(y), int(cw), int(ch)),
            "area": int(area),
            "aspect": float(aspect),
            "density": float(density),
        })
    return candidates


def ocr_digit(bgr: np.ndarray, bbox: tuple[int, int, int, int]) -> str | None:
    """Crop the bounding box + small margin and OCR for a single digit (1-5).

    Strategy: try multiple preprocessing + tesseract config combinations, take
    the most common consistent answer. Ball-handler digits (inside circles)
    and zig-zag-adjacent digits often fail a single pass.
    """
    x, y, w, h = bbox
    pad = max(3, int(max(w, h) * 0.15))
    h_img, w_img = bgr.shape[:2]
    x0 = max(0, x - pad)
    y0 = max(0, y - pad)
    x1 = min(w_img, x + w + pad)
    y1 = min(h_img, y + h + pad)
    crop = bgr[y0:y1, x0:x1]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    votes: dict[str, int] = {}
    # Combinations to try — different scale + psm mode
    # psm 10 = treat as single character; psm 8 = single word; psm 7 = single line
    for scale in (3, 4, 5):
        for psm in (10, 8, 7):
            scaled = cv2.resize(bw, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            cfg = f"--oem 3 --psm {psm} -c tessedit_char_whitelist=12345"
            try:
                txt = pytesseract.image_to_string(scaled, config=cfg).strip()
            except Exception:
                continue
            if not txt:
                continue
            first = txt[0]
            if first in "12345":
                votes[first] = votes.get(first, 0) + 1

    if not votes:
        return None
    # Return the most-voted digit
    return max(votes.items(), key=lambda kv: kv[1])[0]


def reconcile_labels(cands: list[dict]) -> list[dict]:
    """Clean up OCR labels: drop unlabeled noise + disambiguate 1-vs-4.

    Basketball diagrams in this book always have exactly one of each digit
    1..5 per panel. Duplicates usually mean tesseract confused a narrow "1"
    glyph with "4". Since "1" is the only digit that renders as a thin
    vertical stroke, aspect ratio ≤ 0.5 strongly suggests "1".
    """
    # 1. Drop unlabeled candidates — most are noise we couldn't OCR.
    labeled = [c for c in cands if c.get("digit")]

    # 2. Find duplicates + missing digits.
    counts: dict[str, list[dict]] = {}
    for c in labeled:
        counts.setdefault(c["digit"], []).append(c)
    missing = [d for d in "12345" if d not in counts]
    dupes = [(d, group) for d, group in counts.items() if len(group) > 1]

    # 3. If exactly one digit is missing AND exactly one is duplicated,
    #    relabel the narrowest duplicate as the missing digit — but only
    #    when the narrow-digit heuristic applies (missing 1, dup of wide digit).
    if len(missing) == 1 and len(dupes) == 1:
        missing_digit = missing[0]
        dup_digit, group = dupes[0]
        group_sorted = sorted(group, key=lambda c: c["aspect"])  # narrowest first
        narrowest = group_sorted[0]
        # Common case: missing "1", duplicated "4"; narrowest was "1" mis-OCR'd as "4".
        if missing_digit == "1" and narrowest["aspect"] <= 0.55:
            narrowest["digit"] = "1"
    return labeled


def annotate(bgr: np.ndarray, candidates: list[dict], reg=None) -> np.ndarray:
    out = bgr.copy()
    # Overlay the detected paint rectangle if registration succeeded
    if reg is not None:
        pts = reg.paint_pixels.astype(int).reshape((-1, 1, 2))
        cv2.polylines(out, [pts], isClosed=True, color=(255, 0, 255), thickness=2)
        cv2.putText(out, "paint", (int(pts[0][0][0]) + 4, int(pts[0][0][1]) + 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA)
    for c in candidates:
        cx, cy = c["center"]
        x, y, cw, ch = c["bbox"]
        digit = c.get("digit")
        color = (0, 200, 0) if digit else (0, 165, 255)
        cv2.rectangle(out, (x, y), (x + cw, y + ch), color, 2)
        cv2.circle(out, (int(cx), int(cy)), 2, (0, 0, 255), -1)
        label = f"P{digit}" if digit else "?"
        if "svg" in c:
            sx, sy = c["svg"]
            label += f" ({sx:.1f},{sy:.1f})"
        cv2.putText(out, label, (x + cw + 3, y + ch), cv2.FONT_HERSHEY_SIMPLEX, 0.48, color, 2, cv2.LINE_AA)
    return out


def process_page(page_number: int) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diagrams = extract_diagrams(page_number)
    if not diagrams:
        print(f"page {page_number}: no embedded images")
        return

    lines: list[str] = [f"page {page_number} — {len(diagrams)} panel(s)\n"]
    for idx, pil_img in diagrams:
        arr = np.array(pil_img)
        if arr.ndim == 2:
            bgr = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
        elif arr.shape[2] == 4:
            bgr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
        else:
            bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

        cands = detect_glyph_candidates(bgr)
        # OCR each candidate to assign a digit 1-5
        for c in cands:
            c["digit"] = ocr_digit(bgr, c["bbox"])
        # Post-process: drop unlabeled P? (most noise is here) and fix
        # the common "1 mis-OCR'd as 4" when it produces a duplicate label.
        cands = reconcile_labels(cands)
        # Court registration: pixel → SVG transform via paint-rectangle homography
        reg = register_court(bgr)
        if reg is not None:
            for c in cands:
                sx, sy = pixel_to_svg(reg, c["center"][0], c["center"][1])
                c["svg"] = (sx, sy)
        annotated = annotate(bgr, cands, reg)

        src_path = OUT_DIR / f"page_{page_number:03d}_panel_{idx}_source.png"
        det_path = OUT_DIR / f"page_{page_number:03d}_panel_{idx}_detected.png"
        cv2.imwrite(str(src_path), bgr)
        cv2.imwrite(str(det_path), annotated)

        h, w = bgr.shape[:2]
        labeled = sum(1 for c in cands if c.get("digit"))
        reg_status = "registered" if reg is not None else "NO-REGISTRATION"
        lines.append(f"  panel {idx}: {w}x{h} px, {len(cands)} candidates, {labeled} OCR'd, {reg_status}")
        for c in cands:
            cx, cy = c["center"]
            digit = c.get("digit") or "?"
            svg_str = f" → SVG({c['svg'][0]:+.1f}, {c['svg'][1]:+.1f})" if "svg" in c else ""
            lines.append(
                f"    P{digit} at px({cx:.1f}, {cy:.1f}){svg_str}"
            )

    report = "\n".join(lines) + "\n"
    (OUT_DIR / f"page_{page_number:03d}_report.txt").write_text(report)
    print(report)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python -m src.cv.probe <page_number> [...]")
    for arg in sys.argv[1:]:
        process_page(int(arg))


if __name__ == "__main__":
    main()
