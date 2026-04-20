# Claude Code Task: Play Extraction Proof of Concept

> **Task type**: Autonomous execution — Claude Code runs this end-to-end
> **Goal**: Validate whether Claude Vision can extract accurate player coordinates from basketball diagrams
> **Outcome**: Go/no-go decision for the entire play animation pipeline
> **Budget**: ~$1 in Claude API calls, 2-3 hours of runtime
> **Blocker level**: Critical. The entire Play Viewer data pipeline depends on this result.

---

## Context

Read these specs before starting. They contain the full reasoning and architecture:

```
spec/play-animation-pipeline.md   ← Master spec (audit, 6 resolutions, pivot plans)
spec/play-viewer.md               ← Target rendering engine (what the output feeds)
CLAUDE.md                         ← Project overview + conventions (backend + parent)
```

This task executes **Resolution 1** (the gate) and **Resolution 2** (Bézier algorithm) in parallel from that master spec.

---

## Success criteria (the decision)

Run the pipeline. Produce `results/decision.md` with one of three verdicts:

| Verdict | Threshold | Next action |
|---------|-----------|-------------|
| **PIPELINE VIABLE** | Best strategy places ≥80% of players within 2 SVG units (~1.5 ft) of ground truth | Proceed to Resolution 3 (full book scan) |
| **VIABLE WITH CORRECTION** | Best strategy places ≥80% of players within 5 SVG units | Proceed with correction editor (Resolution 5) as mandatory step |
| **PIVOT REQUIRED** | No strategy meets the 5-unit threshold | Invoke Plan B (curated database) or Plan C (community-sourced). Do NOT proceed with auto-extraction. |

> **Why ≥80%?** This threshold is not inherited from `play-animation-pipeline.md` — it is introduced here as a working assumption. Rationale: with only 5 diagrams × 5 players = 25 positions, a single strategy must clearly win (≥20 of 25 within threshold) before we trust the verdict. If you want a different threshold, change it here and re-run `make score`. Players the LLM fails to emit at all are counted against this percentage (they fall into neither "viable" nor "correctable").

---

## Project structure to create

```
play-extraction-poc/
├── README.md                      ← Summary + how to run
├── requirements.txt               ← Python deps
├── .env.example                   ← ANTHROPIC_API_KEY placeholder
├── Makefile                       ← make setup | make run | make score
│
├── src/
│   ├── __init__.py
│   ├── rasterize.py               ← PDF → JPEG (Resolution 1 input prep)
│   ├── extract.py                 ← Claude Vision calls, 3 strategies
│   ├── bezier.py                  ← Resolution 2: deterministic path generation
│   ├── score.py                   ← Compare extracted vs ground truth
│   ├── overlay.py                 ← Visual diff: extracted on real court SVG
│   └── prompts/
│       ├── strategy_a_raw.txt
│       ├── strategy_b_calibrated.txt
│       └── strategy_c_describe.txt
│
├── data/
│   ├── reference-court.svg        ← Empty court with labeled coord positions
│   ├── reference-court.png        ← Rendered PNG version (for Strategy B)
│   ├── ground-truth.json          ← Hand-annotated expected coordinates for 5 plays
│   └── diagrams/                  ← Rasterized book pages (populated by make run)
│
├── tests/
│   ├── test_bezier.py             ← Unit tests for path generation
│   └── test_score.py              ← Unit tests for scoring logic
│
└── results/                       ← Generated outputs (gitignored)
    ├── extractions/               ← Raw YAML from each strategy
    ├── overlays/                  ← Visual diff images
    ├── scores.json                ← Numerical accuracy scores
    └── decision.md                ← THE VERDICT
```

---

## Step-by-step execution

### Step 0 — Precondition checks

Before starting, verify:

```bash
# Required files must exist
test -f backend/knowledge-base/raw/basketball-for-coaches.pdf   # 105 pp, Trevor McLean 2017, BasketballForCoaches.com
echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" | grep -v "=$"      # not empty

# System deps
which pdftoppm     # poppler-utils
python3 --version  # 3.9+
```

**The target PDF is `backend/knowledge-base/raw/basketball-for-coaches.pdf`** — 105 pages, "Basketball For Coaches" by Trevor McLean (BasketballForCoaches.com, 2017). Chosen over the 934-page 2018-19 NBA Playbook because:

1. **Explicit phase segmentation** — each play has numbered prose instructions ("1. The play begins with 1 passing to 3 on the wing. 2. 5 sets a screen…"). The LLM does not need to infer phases from unnumbered arrows; the prose is the ground truth.
2. **Prose commentary** — every play has Overview, Key Personnel, Instructions, Coaching Points. Feeds Resolution 6 game-changer data (spotlight text, branching hints) for free.
3. **Multi-panel diagrams** — 1–3 court diagrams per play, one per natural phase. Phase grouping is visual.
4. **Generic play names** — "Skipper", "Black", "X-Cross". Low IP entanglement.
5. **Single-site attribution** — `Source: BasketballForCoaches.com, "<play name>"` is a clean citation.
6. **Cheap to run** — ~30–50 plays in 105 pages, so full-book extraction at Opus Vision pricing ≈ $2.

**Secondary target (deferred)**: `2018-19-nba-playbook.pdf` (934 pp, FastDraw export). Adds volume but requires IP scrubbing — team and coach names appear in page headers (e.g., "Boston Celtics (Brad Stevens)" on page 50) and arrows are unnumbered, so phase inference is purely visual. Defer until the pipeline is proven on the simpler book.

**One IP caveat on the primary book**: the play "Iverson Ram" (PDF page 70) uses a player last name. The normalizer must rename player-name-adjacent play titles (e.g., "Iverson Ram" → "Wing-Exchange Ram") before they reach any public surface. Keep a sanitization lookup table in the normalizer.

Record the source path in `data/selected-pages.json` under `source_pdf`.

### Step 1 — Scaffold the project

```bash
mkdir -p play-extraction-poc/{src/prompts,data/diagrams,tests,results/{extractions,overlays}}
cd play-extraction-poc
```

Create `requirements.txt`:

```
anthropic>=0.34.0
Pillow>=10.0.0
pypdf>=4.0.0
pytest>=7.0.0
pyyaml>=6.0
```

Create `.env.example`:

```
ANTHROPIC_API_KEY=your_key_here
```

Create `Makefile`:

```makefile
.PHONY: setup run score clean test

setup:
	pip install -r requirements.txt
	python -m src.rasterize

run:
	python -m src.extract

score:
	python -m src.score
	python -m src.overlay

test:
	pytest tests/ -v

clean:
	rm -rf results/extractions/* results/overlays/*
```

### Step 2 — Select the 5 test diagrams

From the NBA Playbook PDF, pick pages that represent the complexity spectrum. **Search strategy**: open the PDF table of contents or skim pages. Pick:

| # | Complexity | Target content |
|---|------------|----------------|
| 1 | Simple | 2 actions, 1 phase (e.g., a basic cut + pass) |
| 2 | Medium | 3 phases, linear progression |
| 3 | Screen-heavy | Contains at least one screen (perpendicular bar notation) |
| 4 | Pass-heavy | Multiple passes (dashed line notation) |
| 5 | Full 5-player | All 5 offensive players move simultaneously |

Record the chosen page numbers in `data/selected-pages.json`:

```json
{
  "source_pdf": "backend/knowledge-base/raw/2018-19-nba-playbook.pdf",
  "diagrams": [
    {"id": 1, "page": 47, "complexity": "simple", "expected_play_name": "..."},
    {"id": 2, "page": 82, "complexity": "medium", "expected_play_name": "..."},
    {"id": 3, "page": 104, "complexity": "screen", "expected_play_name": "..."},
    {"id": 4, "page": 156, "complexity": "pass", "expected_play_name": "..."},
    {"id": 5, "page": 203, "complexity": "full", "expected_play_name": "..."}
  ]
}
```

**Note on page selection**: If Claude Code cannot visually assess pages during scaffolding, it can ask me (the user) via a status update to pick the pages, OR use heuristic: take pages 50, 100, 150, 200, 250 as a spread and document the assumption.

### Step 3 — Build `src/rasterize.py`

```python
"""
Rasterize selected pages from the NBA Playbook PDF.
Outputs high-res JPEGs to data/diagrams/.
"""
import json
import subprocess
from pathlib import Path

SELECTED = Path("data/selected-pages.json")
OUT_DIR = Path("data/diagrams")

def rasterize():
    config = json.loads(SELECTED.read_text())
    pdf = config["source_pdf"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for diagram in config["diagrams"]:
        page = diagram["page"]
        out_prefix = OUT_DIR / f"diagram_{diagram['id']:02d}_page_{page:03d}"
        subprocess.run([
            "pdftoppm", "-jpeg", "-r", "200",
            "-f", str(page), "-l", str(page),
            pdf, str(out_prefix)
        ], check=True)
        print(f"Rasterized page {page} → {out_prefix}-{page}.jpg")

if __name__ == "__main__":
    rasterize()
```

### Step 4 — Build `data/reference-court.svg` + PNG

Create an SVG of the empty court with coordinate labels at every key basketball position. This is the "ruler" for Strategy B.

```svg
<svg viewBox="-28 -3 56 50" xmlns="http://www.w3.org/2000/svg">
  <!-- Court lines (standard) -->
  <rect x="-25" y="0" width="50" height="47" fill="#f5e1c0" stroke="white" stroke-width="0.3"/>
  <!-- Paint -->
  <rect x="-8" y="0" width="16" height="19" fill="none" stroke="white" stroke-width="0.3"/>
  <!-- Free throw circle -->
  <circle cx="0" cy="19" r="6" fill="none" stroke="white" stroke-width="0.3"/>
  <!-- Three-point arc (approximate) -->
  <path d="M -22 4 A 23.75 23.75 0 0 0 22 4" fill="none" stroke="white" stroke-width="0.3"/>
  <!-- Backboard + rim -->
  <line x1="-3" y1="4" x2="3" y2="4" stroke="white" stroke-width="0.3"/>
  <circle cx="0" cy="5.25" r="0.75" fill="none" stroke="#d4722b" stroke-width="0.2"/>

  <!-- Coordinate labels at each canonical position -->
  <g font-family="monospace" font-size="1.2" fill="#333">
    <circle cx="0" cy="32" r="0.5" fill="#2563eb"/><text x="1" y="32.5">TOP (0,32)</text>
    <circle cx="-16" cy="26" r="0.5" fill="#2563eb"/><text x="-15" y="26.5">LW (-16,26)</text>
    <circle cx="16" cy="26" r="0.5" fill="#2563eb"/><text x="17" y="26.5">RW (16,26)</text>
    <circle cx="-8" cy="19" r="0.5" fill="#2563eb"/><text x="-7" y="19.5">LE (-8,19)</text>
    <circle cx="8" cy="19" r="0.5" fill="#2563eb"/><text x="9" y="19.5">RE (8,19)</text>
    <circle cx="-6" cy="8" r="0.5" fill="#2563eb"/><text x="-5" y="8.5">LB (-6,8)</text>
    <circle cx="6" cy="8" r="0.5" fill="#2563eb"/><text x="7" y="8.5">RB (6,8)</text>
    <circle cx="-22" cy="4" r="0.5" fill="#2563eb"/><text x="-21" y="4.5">LC (-22,4)</text>
    <circle cx="22" cy="4" r="0.5" fill="#2563eb"/><text x="23" y="4.5">RC (22,4)</text>
    <circle cx="0" cy="5.25" r="0.5" fill="#d4722b"/><text x="1" y="5.75">RIM (0,5.25)</text>
  </g>
</svg>
```

Convert to PNG at 1200px wide using Pillow + a Python SVG renderer (cairosvg if available, otherwise fall back to rendering with a headless browser or a pre-committed PNG). Save as `data/reference-court.png`.

### Step 5 — Build the 3 prompt strategies

Create `src/prompts/strategy_a_raw.txt`:

```
You are extracting basketball play data from a court diagram.

COORDINATE SYSTEM:
- SVG viewBox: "-28 -3 56 50"
- Origin (0,0) = center-top of half-court
- X axis: -28 (left sideline) to +28 (right sideline)
- Y axis: -3 (above baseline) to +47 (half-court line)
- Basket is at (0, 5.25)
- Free throw line is at y=19
- Three-point arc has radius ~23.75 from basket

MOVEMENT TYPES:
- cut: solid line with arrowhead (offensive player movement without ball)
- pass: dashed line (ball travels between players)
- screen: perpendicular bar notation (player sets screen for teammate)

Output valid YAML matching this schema:
```yaml
play:
  name: string
  players:
    "1": [x, y]
    "2": [x, y]
    ...
  ball_start: "1"  # which player has the ball initially
  phases:
    - label: "Phase 1"
      description: string
      movements:
        - player: "1"
          from: [x, y]
          to: [x, y]
          type: cut | pass | screen
          confidence: high | medium | low
```

For pass movements, use `to_player` instead of `to`:
```yaml
- player: "1"
  to_player: "4"
  type: pass
```

Extract the play from the attached diagram. If unsure about a position, mark confidence: low.
```

Create `src/prompts/strategy_b_calibrated.txt` — identical to A, but with an instruction to use the attached reference image as a coordinate ruler:

```
[Same as strategy_a_raw.txt, with this addition at the top]

REFERENCE: The first attached image shows the empty court with labeled coordinate markers at every key basketball position (TOP, WINGS, ELBOWS, BLOCKS, CORNERS, RIM). Use this as a visual ruler when reading the play diagram (second attached image). Match each player's position to the nearest reference marker.
```

Create `src/prompts/strategy_c_describe.txt` — two-step process:

```
STEP 1 PROMPT:
Describe the basketball play in this diagram using natural language.
For each player, state their court position using basketball terminology
(top of key, left wing, right elbow, left block, etc.).
For each movement, describe the path, type (cut/pass/screen), and player.
List movements in the order they occur (look for numbered arrows).

STEP 2 PROMPT (uses step 1 output + reference mapping):
Convert this play description to YAML using the coordinate mapping below.
[Include the basketball_positions_to_viewbox mapping from play-animation-pipeline.md]

[Description from step 1 gets inserted here]
```

### Step 6 — Build `src/extract.py`

```python
"""
Run all 3 extraction strategies against all 5 diagrams.
Outputs YAML to results/extractions/.
"""
import os
import json
import base64
from pathlib import Path
from anthropic import Anthropic

client = Anthropic()  # uses ANTHROPIC_API_KEY env var
MODEL = "claude-opus-4-7"  # or latest; document choice

DIAGRAMS_DIR = Path("data/diagrams")
REFERENCE_PNG = Path("data/reference-court.png")
OUT_DIR = Path("results/extractions")
PROMPTS = Path("src/prompts")

def load_image_b64(path: Path) -> str:
    return base64.standard_b64encode(path.read_bytes()).decode("utf-8")

def run_strategy_a(diagram_path: Path) -> str:
    prompt = (PROMPTS / "strategy_a_raw.txt").read_text()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": load_image_b64(diagram_path)
                }},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return msg.content[0].text

def run_strategy_b(diagram_path: Path) -> str:
    prompt = (PROMPTS / "strategy_b_calibrated.txt").read_text()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64", "media_type": "image/png",
                    "data": load_image_b64(REFERENCE_PNG)
                }},
                {"type": "image", "source": {
                    "type": "base64", "media_type": "image/jpeg",
                    "data": load_image_b64(diagram_path)
                }},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return msg.content[0].text

def run_strategy_c(diagram_path: Path) -> str:
    # Step 1: Natural language description
    step1_prompt = (PROMPTS / "strategy_c_describe.txt").read_text().split("STEP 2 PROMPT:")[0]
    step1 = client.messages.create(
        model=MODEL, max_tokens=1500,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {
                "type": "base64", "media_type": "image/jpeg",
                "data": load_image_b64(diagram_path)
            }},
            {"type": "text", "text": step1_prompt}
        ]}]
    )
    description = step1.content[0].text

    # Step 2: Convert to YAML
    step2_prompt = (PROMPTS / "strategy_c_describe.txt").read_text().split("STEP 2 PROMPT:")[1]
    step2_prompt += f"\n\nDESCRIPTION:\n{description}"
    step2 = client.messages.create(
        model=MODEL, max_tokens=2000,
        messages=[{"role": "user", "content": step2_prompt}]
    )
    return step2.content[0].text

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diagrams = sorted(DIAGRAMS_DIR.glob("*.jpg"))

    for diagram in diagrams:
        diagram_id = diagram.stem
        print(f"\n=== Processing {diagram_id} ===")

        for strategy_name, runner in [("a", run_strategy_a), ("b", run_strategy_b), ("c", run_strategy_c)]:
            print(f"  Strategy {strategy_name}...")
            try:
                output = runner(diagram)
                out_path = OUT_DIR / f"{diagram_id}_strategy_{strategy_name}.yaml"
                out_path.write_text(output)
                print(f"    → {out_path}")
            except Exception as e:
                print(f"    ✗ Failed: {e}")
                (OUT_DIR / f"{diagram_id}_strategy_{strategy_name}.error.txt").write_text(str(e))

if __name__ == "__main__":
    main()
```

### Step 7 — Create `data/ground-truth.json`

This is the critical piece Claude Code must construct carefully. For each of the 5 diagrams, the agent must:

1. View the diagram image
2. Hand-annotate the expected player positions by eye, using the coordinate system
3. Hand-annotate the expected movements (from, to, type)
4. Save as JSON with this structure:

```json
{
  "diagram_01_page_047": {
    "play_name": "...",
    "expected_players": {
      "1": [0, 32],
      "2": [-16, 26],
      "3": [16, 26],
      "4": [6, 19],
      "5": [-6, 19]
    },
    "expected_movements": [
      {"player": "5", "from": [-6, 19], "to": [-2, 30], "type": "screen"},
      {"player": "4", "from": [6, 19], "to": [12, 19], "type": "cut"}
    ]
  }
}
```

**Important**: Ground truth is produced by the agent's best visual reading of each diagram. It is the reference we score against. If ground truth is off by 1-2 SVG units that's acceptable — we're measuring relative accuracy, not absolute precision. Document the annotation method in `data/ground-truth-notes.md`.

> **Methodological guard-rail** — because the same model class that does the extraction may also be doing the ground-truth annotation, systematic Claude-Vision biases (e.g., center drift) could shrink measured error below real error. Before running `make score`, the agent MUST:
>
> 1. Render each annotated ground truth onto the reference court SVG (use `src/overlay.py` in a ground-truth-only mode) and save to `data/ground-truth-overlays/`.
> 2. Print a user-visible prompt listing the 5 annotations and asking the user to confirm at least **2 of the 5** by eye before scoring proceeds.
> 3. Log the confirmation (or the user's corrections) in `data/ground-truth-notes.md`.
>
> If the user cannot review interactively, the agent must still save the overlays and flag unverified ground truth in `decision.md` so the verdict can be re-checked later.

### Step 8 — Build `src/score.py`

```python
"""
Score each strategy's extraction against ground truth.
Outputs results/scores.json with per-player-per-strategy deltas.
"""
import json
import yaml
from pathlib import Path
from math import sqrt

GROUND_TRUTH = Path("data/ground-truth.json")
EXTRACTIONS = Path("results/extractions")
OUT = Path("results/scores.json")

THRESHOLDS = {
    "viable":         2.0,  # SVG units
    "correctable":    5.0,  # SVG units
}

def euclidean(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def parse_yaml_safely(text: str) -> dict:
    # Strip code fences if present
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        return None

def score_extraction(extracted: dict, truth: dict) -> dict:
    """Returns dict with player-level deltas and summary stats."""
    if not extracted or "play" not in extracted:
        return {"parse_error": True, "deltas": {}, "summary": None}

    play = extracted["play"]
    extracted_players = play.get("players", {})
    truth_players = truth["expected_players"]

    deltas = {}
    for pid, truth_pos in truth_players.items():
        if pid not in extracted_players:
            deltas[pid] = {"delta": None, "missing": True}
            continue
        ext_pos = extracted_players[pid]
        d = euclidean(ext_pos, truth_pos)
        deltas[pid] = {
            "delta": round(d, 2),
            "extracted": ext_pos,
            "truth": truth_pos,
            "verdict": (
                "viable" if d <= THRESHOLDS["viable"]
                else "correctable" if d <= THRESHOLDS["correctable"]
                else "failed"
            )
        }

    valid_deltas = [d["delta"] for d in deltas.values() if d.get("delta") is not None]
    if not valid_deltas:
        return {"parse_error": False, "deltas": deltas, "summary": None}

    viable_count = sum(1 for d in deltas.values() if d.get("verdict") == "viable")
    correctable_count = sum(1 for d in deltas.values() if d.get("verdict") in ("viable", "correctable"))
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
        }
    }

def main():
    truth = json.loads(GROUND_TRUTH.read_text())
    results = {}

    for diagram_id, truth_data in truth.items():
        results[diagram_id] = {}
        for strategy in ["a", "b", "c"]:
            ext_path = EXTRACTIONS / f"{diagram_id}_strategy_{strategy}.yaml"
            if not ext_path.exists():
                results[diagram_id][strategy] = {"error": "file missing"}
                continue
            extracted = parse_yaml_safely(ext_path.read_text())
            results[diagram_id][strategy] = score_extraction(extracted, truth_data)

    # Overall strategy rankings
    strategy_summary = {}
    for s in ["a", "b", "c"]:
        viable_pcts = []
        correctable_pcts = []
        for diagram_id in truth:
            summary = results[diagram_id][s].get("summary")
            if summary:
                viable_pcts.append(summary["viable_pct"])
                correctable_pcts.append(summary["correctable_pct"])
        if viable_pcts:
            strategy_summary[s] = {
                "mean_viable_pct": round(sum(viable_pcts) / len(viable_pcts), 1),
                "mean_correctable_pct": round(sum(correctable_pcts) / len(correctable_pcts), 1),
                "diagrams_scored": len(viable_pcts)
            }

    output = {"per_diagram": results, "per_strategy": strategy_summary}
    OUT.write_text(json.dumps(output, indent=2))
    print(json.dumps(strategy_summary, indent=2))

if __name__ == "__main__":
    main()
```

### Step 9 — Build `src/bezier.py` (Resolution 2, parallel track)

```python
"""
Deterministic Bézier path generation for movement types.
The LLM outputs only endpoints — this module generates the curves.

No LLM calls. Pure math. Fully unit-tested.
"""
from typing import Literal, Tuple

Point = Tuple[float, float]
MovementType = Literal["cut", "pass", "screen"]

BASKET: Point = (0.0, 5.25)

def generate_path(from_pt: Point, to_pt: Point, movement_type: MovementType) -> str:
    """
    Generate an SVG path string for a movement.

    Args:
        from_pt: (x, y) start coordinate in SVG units
        to_pt: (x, y) end coordinate in SVG units
        movement_type: "cut" | "pass" | "screen"

    Returns:
        SVG path d-attribute string
    """
    x1, y1 = from_pt
    x2, y2 = to_pt
    dx = x2 - x1
    dy = y2 - y1

    if movement_type == "screen":
        # Short, direct line
        return f"M{x1} {y1} L{x2} {y2}"

    if movement_type == "pass":
        # Quadratic Bézier with slight perpendicular arc
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        perp_x = -dy * 0.08
        perp_y = dx * 0.08
        return f"M{x1} {y1} Q{mx + perp_x} {my + perp_y} {x2} {y2}"

    # cut: cubic Bézier curving toward basket
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    pull_x = (BASKET[0] - mx) * 0.15
    pull_y = (BASKET[1] - my) * 0.15
    cp1x = x1 + dx * 0.33 + pull_x
    cp1y = y1 + dy * 0.33 + pull_y
    cp2x = x1 + dx * 0.66 + pull_x
    cp2y = y1 + dy * 0.66 + pull_y
    return f"M{x1} {y1} C{cp1x} {cp1y} {cp2x} {cp2y} {x2} {y2}"


MOVEMENT_STYLE = {
    "cut":    {"dashed": False, "color": "rgba(51,51,51,1)", "marker": "arrow"},
    "pass":   {"dashed": True,  "color": "#d4722b",          "marker": "arrow"},
    "screen": {"dashed": False, "color": "rgba(51,51,51,1)", "marker": "screen-bar"},
}
```

### Step 10 — Build `tests/test_bezier.py`

```python
"""Unit tests for Bézier path generation."""
import pytest
from src.bezier import generate_path, BASKET

def test_screen_is_linear():
    path = generate_path((0, 10), (5, 10), "screen")
    assert path.startswith("M0 10 L")
    assert "C" not in path and "Q" not in path

def test_pass_uses_quadratic():
    path = generate_path((0, 30), (10, 30), "pass")
    assert "Q" in path
    assert path.startswith("M0 30")

def test_cut_uses_cubic():
    path = generate_path((0, 32), (-8, 24), "cut")
    assert "C" in path
    assert path.startswith("M0 32")

def test_cut_curves_toward_basket():
    """The cubic control points should be pulled toward the basket at (0, 5.25)."""
    # Movement from top of key to right wing — should curve slightly toward basket
    path = generate_path((0, 32), (16, 26), "cut")
    # Parse control points out of the path
    parts = path.replace("M0 32 C", "").split()
    cp1 = (float(parts[0]), float(parts[1]))
    # The first control point should be pulled south (toward y=5.25) from the direct midpoint
    direct_mid_y = (32 + 26) / 2  # = 29
    assert cp1[1] < direct_mid_y  # pulled toward basket (lower y)

def test_no_nan_or_inf():
    """Paths should never produce NaN or infinity."""
    import math
    path = generate_path((0, 0), (0, 0), "cut")
    for token in path.replace("M", "").replace("C", "").replace("L", "").replace("Q", "").split():
        try:
            val = float(token)
            assert not math.isnan(val) and not math.isinf(val)
        except ValueError:
            pass

def test_all_movement_types_accepted():
    for mt in ["cut", "pass", "screen"]:
        assert generate_path((0, 0), (10, 10), mt)
```

### Step 11 — Build `src/overlay.py`

```python
"""
Render extracted plays onto the real court SVG for visual inspection.
Outputs results/overlays/*.svg — one per (diagram × strategy) combination.
Each overlay shows:
  - Ground truth positions in GREEN
  - Extracted positions in ORANGE with a line connecting to ground truth
  - Delta distance labeled next to each player
"""
import json
import yaml
from pathlib import Path

GROUND_TRUTH = Path("data/ground-truth.json")
EXTRACTIONS = Path("results/extractions")
OUT_DIR = Path("results/overlays")

SVG_HEADER = '''<svg viewBox="-28 -3 56 50" xmlns="http://www.w3.org/2000/svg" width="680" height="560">
<rect x="-25" y="0" width="50" height="47" fill="#1a1a1a" stroke="#444" stroke-width="0.3"/>
<rect x="-8" y="0" width="16" height="19" fill="none" stroke="#666" stroke-width="0.3"/>
<circle cx="0" cy="19" r="6" fill="none" stroke="#666" stroke-width="0.3"/>
<path d="M -22 4 A 23.75 23.75 0 0 0 22 4" fill="none" stroke="#666" stroke-width="0.3"/>
<circle cx="0" cy="5.25" r="0.75" fill="none" stroke="#d4722b" stroke-width="0.2"/>'''

SVG_FOOTER = '</svg>'

def render_overlay(extracted: dict, truth: dict, title: str) -> str:
    parts = [SVG_HEADER]
    parts.append(f'<text x="-27" y="-1" fill="white" font-size="1.5" font-family="monospace">{title}</text>')

    # Ground truth (green)
    for pid, pos in truth["expected_players"].items():
        parts.append(
            f'<circle cx="{pos[0]}" cy="{pos[1]}" r="1" fill="#22c55e" opacity="0.7"/>'
            f'<text x="{pos[0]+1.2}" y="{pos[1]+0.4}" fill="#22c55e" font-size="1.4" font-family="monospace">{pid}T</text>'
        )

    # Extracted (orange)
    if extracted and "play" in extracted:
        for pid, pos in extracted["play"].get("players", {}).items():
            parts.append(
                f'<circle cx="{pos[0]}" cy="{pos[1]}" r="1" fill="#f97316" opacity="0.7"/>'
                f'<text x="{pos[0]+1.2}" y="{pos[1]-1}" fill="#f97316" font-size="1.4" font-family="monospace">{pid}E</text>'
            )
            # Connecting line to truth
            truth_pos = truth["expected_players"].get(pid)
            if truth_pos:
                parts.append(
                    f'<line x1="{pos[0]}" y1="{pos[1]}" x2="{truth_pos[0]}" y2="{truth_pos[1]}" '
                    f'stroke="#fbbf24" stroke-width="0.15" stroke-dasharray="0.4 0.4"/>'
                )

    parts.append(SVG_FOOTER)
    return "\n".join(parts)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    truth_data = json.loads(GROUND_TRUTH.read_text())

    for diagram_id, truth in truth_data.items():
        for strategy in ["a", "b", "c"]:
            ext_path = EXTRACTIONS / f"{diagram_id}_strategy_{strategy}.yaml"
            if not ext_path.exists():
                continue
            try:
                text = ext_path.read_text().strip()
                if text.startswith("```"):
                    text = "\n".join(text.split("\n")[1:-1])
                extracted = yaml.safe_load(text)
            except yaml.YAMLError:
                extracted = None

            svg = render_overlay(extracted, truth, f"{diagram_id} · Strategy {strategy.upper()}")
            out = OUT_DIR / f"{diagram_id}_strategy_{strategy}.svg"
            out.write_text(svg)
            print(f"→ {out}")

if __name__ == "__main__":
    main()
```

### Step 12 — Generate `results/decision.md`

After `make run` + `make score` + `make test`, generate the final verdict. The agent writes `results/decision.md` with this exact structure:

```markdown
# Decision: Play Extraction Pipeline

**Run date**: YYYY-MM-DD
**Model**: claude-opus-4-7
**Diagrams tested**: 5
**Strategies compared**: 3

---

## Headline verdict

**[PIPELINE VIABLE | VIABLE WITH CORRECTION | PIVOT REQUIRED]**

**Best strategy**: [A | B | C]
**Mean viable accuracy**: XX.X% of players within 2 SVG units
**Mean correctable accuracy**: XX.X% of players within 5 SVG units

---

## Per-strategy scores

| Strategy | Viable % | Correctable % | Parse errors | Cost per diagram |
|----------|----------|---------------|--------------|------------------|
| A (raw) | ... | ... | ... | $... |
| B (calibrated) | ... | ... | ... | $... |
| C (describe then map) | ... | ... | ... | $... |

## Per-diagram scores

[Table: diagram × strategy showing viable%]

## Failure mode analysis

[Which positions did the LLM systematically get wrong? Block vs elbow? Wing vs corner? Document patterns here.]

## Recommendation

[Based on the verdict, recommend next action. If PIPELINE VIABLE, proceed to Resolution 3. If VIABLE WITH CORRECTION, detail the correction editor requirements. If PIVOT REQUIRED, recommend Plan B or C.]

## Visual overlays

See `results/overlays/` for per-diagram-per-strategy visual diffs. Each SVG shows ground truth (green) vs extracted (orange) with connecting lines showing delta.

## Artifacts produced

- `data/selected-pages.json` — the 5 diagrams tested
- `data/ground-truth.json` — hand-annotated expected coordinates
- `results/extractions/` — raw YAML from each strategy
- `results/scores.json` — numerical accuracy data
- `results/overlays/` — visual diff SVGs
- `results/decision.md` — this file
```

### Step 13 — Build `README.md`

```markdown
# Play Extraction Proof of Concept

Validates whether Claude Vision can extract accurate basketball play data
from rasterized book diagrams. This is Resolution 1 from the Motion project's
play animation pipeline spec.

## Quick start

    cp .env.example .env
    # Edit .env and add your ANTHROPIC_API_KEY
    make setup
    make run    # ~$1 in API calls
    make score
    make test

## Outputs

- `results/decision.md` — the headline verdict
- `results/scores.json` — numerical accuracy
- `results/overlays/` — visual diff SVGs

## Dependencies

- Python 3.9+
- poppler-utils (for pdftoppm)
- ANTHROPIC_API_KEY env var

## References

- `specs/play-animation-pipeline.md` — the master spec
- `specs/play-viewer.md` — target rendering engine
```

---

## Testing requirements

Before concluding, Claude Code MUST:

1. ✅ `make test` passes (all `test_bezier.py` tests green)
2. ✅ `make run` completes without crashes
3. ✅ All 15 extractions (5 diagrams × 3 strategies) are attempted (failures documented, not silent)
4. ✅ `make score` produces `results/scores.json` with valid JSON
5. ✅ `results/decision.md` exists and renders cleanly
6. ✅ At least 12 of 15 overlay SVGs render (80% render rate)

---

## Constraints and conventions

- **No hidden state**: every artifact produced must be a file in the repo (not in-memory only).
- **Idempotent**: `make run` can be re-run safely. It overwrites previous extractions.
- **Logging**: print a line for each API call so progress is visible. Do not silence exceptions — log them to `.error.txt` files.
- **Cost awareness**: 15 extractions + Strategy C doubles = 20 API calls. At Opus pricing this is under $1. Do not loop or retry silently.
- **Model choice**: Use `claude-opus-4-7` unless a newer model is available. Document the choice in `README.md`.
- **No CV libraries beyond Pillow**: OpenCV, numpy, etc. are not required for this task. Keep deps minimal.
- **No animation yet**: this task produces DATA and DECISIONS, not animations. The Play Viewer integration is a downstream task.

---

## Error handling policy

| Failure | Response |
|---------|----------|
| API rate limit | Retry once with 5s backoff. If fails again, log and continue with remaining diagrams. |
| YAML parse error | Save raw output to `.error.txt`. Score it as `parse_error: true`. Don't crash. |
| Missing ground truth | Skip that diagram. Note in decision.md. |
| PDF page doesn't exist | STOP. Report to user. Cannot proceed. |
| SVG render failure | Skip overlay for that combination. Continue. |

---

## Reporting back

When complete, return the following summary (embed in the final response):

```
TASK: Play Extraction POC
STATUS: [complete | partial | blocked]

VERDICT: [PIPELINE VIABLE | VIABLE WITH CORRECTION | PIVOT REQUIRED]
BEST STRATEGY: [A | B | C]
MEAN VIABLE %: XX.X
MEAN CORRECTABLE %: XX.X

ARTIFACTS:
  - play-extraction-poc/results/decision.md
  - play-extraction-poc/results/scores.json
  - play-extraction-poc/results/overlays/ (N files)

NEXT ACTION: [text from decision.md's Recommendation section]

ISSUES ENCOUNTERED: [any blockers, rate limits, parse errors worth flagging]
```

---

## What this spec does NOT cover

Out of scope for this task (future Claude Code tasks):

- Resolution 3 (full 934-page diagram detection scan) — run only if verdict is VIABLE or VIABLE_WITH_CORRECTION
- Resolution 5 (correction editor UI) — a separate React task
- Resolution 6 (game-changer data: branching reads, spotlight, ghost defense) — depends on wiki ingestion
- Integration with the Play Viewer React component — separate task
- **YAML → Play Viewer `Action` normalization** — the pipeline's YAML output (`movements` with `from`/`to`/`type`) does NOT match the viewer's `Action` shape (`path`/`dashed`/`move`/`ball`). A separate downstream task must own the transformation (likely a TypeScript module in `frontend/scripts/` that composes `bezier.ts` with the dashed/marker mapping and resolves `to_player` via the roster). Name the owner before Resolution 3 runs.
- Processing any diagrams beyond the 5 test pages — scale comes later
- **Cheaper-model probe** — this PoC uses `claude-opus-4-7` for the gate. If the verdict is VIABLE or VIABLE_WITH_CORRECTION, before running Resolution 3 at scale, re-run the best strategy on Haiku 4.5 / Sonnet 4.6 against the same 5 diagrams to see whether a cheaper model crosses the same threshold. Opus at scale (934 pages) is the difference between ~$10 and ~$100 of API spend.

Stay focused on the gate: can the LLM extract accurate coordinates or not?
