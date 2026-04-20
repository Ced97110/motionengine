# Play animation pipeline — Specification

> **Status**: Audit complete. 6 resolutions designed. Execution blocked on Resolution 1 (proof of concept).
> **Purpose**: Convert static play diagrams from 7 PDFs (2,440 pages) into interactive SVG animations in the Play Viewer.
> **Critical path**: Resolution 1 (LLM coordinate extraction accuracy) gates the entire pipeline.

---

## The pipeline

```
PDF book
  → pdftoppm (rasterize page to JPEG at 200 DPI)
  → Claude Vision (extract player positions + movements as YAML)
  → Bézier generation algorithm (endpoints → SVG path strings)
  → Play Data JSON (phases, actions, paths)
  → Play Viewer React component (6-layer SVG, 3-phase animation)
```

---

## Audit results (5 gaps identified)

| Gap | Link | Severity | Score | Status |
|-----|------|----------|-------|--------|
| 1 | Diagram page detection — which of 934 pages contain court diagrams? | Medium | 7/10 | Resolution 3 |
| 2 | LLM coordinate extraction — can Claude accurately place players from a rasterized diagram? | **Critical** | 3/10 | Resolution 1 |
| 3 | Phase segmentation — decomposing a single diagram into sequential animation phases | Medium | 5/10 | Resolution 4 |
| 4 | Bézier path generation — converting start/end points into smooth SVG curves | Medium | 5/10 | Resolution 2 |
| 5 | Game-changer data — branching reads, spotlight text, ghost defense require wiki cross-refs | Low | 4/10 | Resolution 6 (deferred) |

### Dependency map

```
Gap 2 (coordinate extraction) ← blocks EVERYTHING
Gap 4 (Bézier generation)     ← blocks animation quality
Gap 1 (page detection)        ← blocks scale/automation
Gap 3 (phase segmentation)    ← blocks temporal correctness
Gap 5 (game-changer data)     ← blocks premium features (deferred)
```

---

## Resolution 1 — The 5-diagram proof of concept

**Resolves**: Gap 2 (coordinate accuracy), Gap 4 (Bézier generation), Gap 3 (phase segmentation)
**Time**: 1 session (~2 hours)
**Cost**: ~$0.50 in Claude API calls
**THIS IS THE GATE. Everything else waits on this result.**

### What to do

Pick 5 diagrams from the NBA Playbook representing different complexity levels:

1. Simple 2-action play (one cut, one pass)
2. 3-phase play (setup → action → finish)
3. Play with screens (perpendicular bar notation)
4. Play with a pass (dashed line notation)
5. Full 5-player set with multiple simultaneous actions

Rasterize each: `pdftoppm -jpeg -r 200 -f PAGE -l PAGE nba-playbook.pdf diagrams/fig`

### Three prompt strategies to test

**Strategy A — Raw extraction**
Give Claude the image and ask for coordinates in our viewBox system. No scaffolding.
```
System: You are extracting basketball play data from a court diagram.
The court uses viewBox="-28 -3 56 50".
Origin (0,0) = center-top of the half-court.
X: -28 (left sideline) to +28 (right sideline).
Y: -3 (above baseline) to +47 (far end / half-court line).
Basket is at approximately (0, 5.25).
Free throw line is at y=19. Three-point arc radius ~23.75 from basket.

Output YAML with player positions and movements.
```

**Strategy B — Calibrated extraction**
Same as A, but include a REFERENCE IMAGE of our empty court with labeled coordinates at known positions (basket, free throw line, three-point arc endpoints, corners, elbow, block, wing). The LLM now has a visual ruler.

```
[Attach: reference-court-with-coordinates.png]
[Attach: play-diagram-from-book.jpg]

Using the reference court as your coordinate guide, extract
player positions and movements from the play diagram.
```

**Strategy C — Two-step extraction**
Step 1: Ask Claude to describe what it sees in natural language.
```
Describe the basketball play in this diagram. For each player,
state their approximate court position using basketball terminology
(top of key, left block, right wing, etc.). For each movement arrow,
describe the path, type (cut/pass/screen), and which player moves.
```

Step 2: Feed the description + coordinate reference into a second call.
```
Convert this basketball play description to YAML coordinates
using the viewBox system "-28 -3 56 50":
[natural language description from step 1]
[coordinate reference mapping basketball positions to viewBox coords]
```

### Coordinate reference mapping (for Strategy B and C)

```yaml
basketball_positions_to_viewbox:
  top_of_key:        [0, 32]
  right_wing:        [16, 26]
  left_wing:         [-16, 26]
  right_corner:      [22, 4]
  left_corner:       [-22, 4]
  right_block:       [6, 8]
  left_block:        [-6, 8]
  right_elbow:       [8, 19]
  left_elbow:        [-8, 19]
  free_throw_line:   [0, 19]
  basket:            [0, 5.25]
  half_court:        [0, 47]
  right_short_corner: [16, 10]
  left_short_corner:  [-16, 10]
  right_hash:        [17, 15]
  left_hash:         [-17, 15]
```

### Success criteria

For each extracted play, overlay the positions onto our court SVG and visually check:

| Accuracy | Meaning | Verdict |
|----------|---------|---------|
| Within 2 SVG units (~1.5 ft) | Player is where they should be | **Pipeline viable** |
| 2-5 SVG units off | Close but noticeable | **Viable WITH human correction** (Resolution 5) |
| 5+ SVG units off | Wrong area of the court | **Strategy fails** — try next strategy or pivot |

### Expected YAML output format

```yaml
play:
  name: "Horns Elbow Pop"
  tag: "Ball Screen"
  source: "NBA Playbook, p.47, Fig 3.2"
  players:
    "1": [0, 32]       # PG top of key with ball
    "2": [-16, 26]     # SG left wing
    "3": [16, 26]      # SF right wing
    "4": [6, 19]       # PF right elbow
    "5": [-6, 19]      # C left elbow
  ball_start: "1"
  phases:
    - label: "Phase 1"
      description: "5 sets ball screen for 1. 4 pops to the elbow."
      movements:
        - player: "5"
          from: [-6, 19]
          to: [-2, 30]
          type: screen
        - player: "4"
          from: [6, 19]
          to: [12, 19]
          type: cut
    - label: "Phase 2"
      description: "1 drives off the screen. Passes to 4 at the elbow."
      movements:
        - player: "1"
          from: [0, 32]
          to: [-8, 24]
          type: cut
        - player: "1"
          to_player: "4"
          type: pass
```

---

## Resolution 2 — Bézier generation algorithm

**Resolves**: Gap 4
**Time**: Half a session
**No dependency on Resolution 1** — build in parallel

### The rule

The LLM NEVER generates SVG path strings. It outputs only start point, end point, and movement type. A deterministic algorithm generates the Bézier.

### Algorithm

```typescript
function generatePath(
  from: [number, number],
  to: [number, number],
  type: "cut" | "pass" | "screen"
): string {
  const [x1, y1] = from;
  const [x2, y2] = to;
  const dx = x2 - x1;
  const dy = y2 - y1;

  if (type === "pass") {
    // Nearly straight line with slight arc
    const mx = (x1 + x2) / 2;
    const my = (y1 + y2) / 2;
    const perpX = -dy * 0.08; // slight perpendicular offset
    const perpY = dx * 0.08;
    return `M${x1} ${y1} Q${mx + perpX} ${my + perpY} ${x2} ${y2}`;
  }

  if (type === "screen") {
    // Short direct movement
    return `M${x1} ${y1} L${x2} ${y2}`;
  }

  // type === "cut" — curve toward basket
  const basketX = 0;
  const basketY = 5.25;
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  // Pull control points slightly toward basket
  const pullX = (basketX - mx) * 0.15;
  const pullY = (basketY - my) * 0.15;
  const cp1x = x1 + dx * 0.33 + pullX;
  const cp1y = y1 + dy * 0.33 + pullY;
  const cp2x = x1 + dx * 0.66 + pullX;
  const cp2y = y1 + dy * 0.66 + pullY;
  return `M${x1} ${y1} C${cp1x} ${cp1y} ${cp2x} ${cp2y} ${x2} ${y2}`;
}
```

### Movement type → line style mapping

| Type | Bézier | Stroke | Dashed | Color | Marker |
|------|--------|--------|--------|-------|--------|
| cut | Cubic, curves toward basket | 0.5px solid | No | `rgba(51,51,51,1)` charcoal | Arrow |
| pass | Quadratic, slight arc | 0.5px | Yes (`1.2 0.4`) | `#d4722b` warm orange | Arrow |
| screen | Linear, direct | 0.5px solid | No | `rgba(51,51,51,1)` | Screen bar |

### Line trimming (applied to all paths)

```
START_TRIM = 1.5 SVG units (gap from player circle)
END_TRIM   = 3.0 SVG units (gap before destination)
```

Implemented via `strokeDasharray` + negative `strokeDashoffset`.

---

## Resolution 3 — Diagram page detection

**Resolves**: Gap 1
**Time**: 1 session
**Depends on**: Nothing (can run in parallel)
**Cost**: ~$2-4 for the entire NBA Playbook on Haiku / small-model classification. If Resolution 1 was run on Opus 4.7 and R3 must use the same model class, budget ~$8-15 for 934 pages at Opus pricing.

### Method

Rasterize every page of the NBA Playbook at LOW resolution (72 DPI — fast, small files):

```bash
pdftoppm -jpeg -r 72 nba-playbook.pdf pages/page
```

Send each page image to Claude with a classification prompt:

```
Look at this page from a basketball playbook.

Answer these questions:
1. Does this page contain a basketball court diagram with player positions? (YES/NO)
2. If YES, how many separate court diagrams are on this page? (1, 2, 3, etc.)
3. If YES, what is the figure number/label if visible? (e.g. "Fig 3.2" or "Diagram 6")
4. If multiple diagrams, describe the bounding region of each (top half, bottom half, left, right, etc.)

Reply as JSON:
{"has_diagram": true/false, "count": N, "figures": ["Fig 3.2"], "regions": ["full page"]}
```

### Output

A JSON manifest:

```json
{
  "book": "2018-19 NBA Playbook",
  "total_pages": 934,
  "diagram_pages": [
    {"page": 47, "count": 1, "figures": ["Fig 3.2"], "regions": ["full"]},
    {"page": 48, "count": 2, "figures": ["Fig 3.3a", "Fig 3.3b"], "regions": ["top", "bottom"]},
    ...
  ],
  "total_diagrams": 412
}
```

### For multi-diagram pages

Re-rasterize at 200 DPI. Use the region info to crop each diagram before sending to the coordinate extraction pipeline. Cropping approach:

```python
from PIL import Image

img = Image.open("page_048_200dpi.jpg")
w, h = img.size

if region == "top":
    diagram = img.crop((0, 0, w, h // 2))
elif region == "bottom":
    diagram = img.crop((0, h // 2, w, h))
# ... etc
```

---

## Resolution 4 — Phase segmentation

**Resolves**: Gap 3
**Time**: Built into Resolution 1's prompt engineering
**Depends on**: Resolution 1

### Primary signal: diagram numbering

Most NBA Playbook diagrams number their arrows (①→②→③). The extraction prompt should explicitly request temporal ordering:

```
List movements in the order they occur.
Use any numbering, sequencing, or arrows visible in the diagram.
If no explicit ordering, apply basketball logic:
  - Ball handler initiates
  - Screens are set BEFORE the cutter uses them
  - Passes follow cuts (the cutter must be open first)
  - Off-ball movement happens simultaneously with on-ball action
```

### Phase grouping rules

```
Rule 1: Simultaneous actions belong in the same phase.
        (Screen + cutter reaction = one phase)

Rule 2: A pass creates a new phase.
        (Everything before the pass = Phase N,
         everything after = Phase N+1)

Rule 3: Maximum 3 actions per phase.
        (More than 3 becomes visually confusing in the viewer)

Rule 4: If the diagram shows a single frame with all arrows,
        and no numbering, default to 2 phases:
        Phase 1 = setup (screens, off-ball movement)
        Phase 2 = execution (ball movement, scoring action)
```

### Fallback: human review

If auto-phasing is unreliable (tested in Resolution 1), add a review step in the app:

The Play Viewer shows the extracted animation with a "Reorder phases" button. Coach can drag phases to reorder, split a phase into two, or merge two phases into one. This is a lightweight UI — just a sortable list of phase cards, each showing a mini-preview of the court state.

---

## Resolution 5 — Human-in-the-loop correction editor

**Resolves**: The "80% accuracy" reality
**Time**: 1-2 sessions to design
**Depends on**: Resolution 1 results + existing Play Creator

### The workflow

```
Auto-extract play from book diagram (LLM does ~80%)
  ↓
Show result in Play Viewer with [Edit] button
  ↓
Coach taps Edit → Play Creator opens pre-loaded with extracted data
  ↓
Coach drags players to correct positions, adjusts paths
  ↓
Corrected play saves to library
  ↓
Correction data logged for prompt refinement
```

### Connection to Play Creator

The Play Creator (already designed in Wave 2) has:
- Court canvas with draggable player markers
- Path drawing tools
- Phase management (add/remove/reorder)

To repurpose as a correction editor, add:
- An `initialData` prop that pre-loads extracted Play Data
- Visual diff highlighting: players that the LLM placed with low confidence get a dashed ring (orange) indicating "check this position"
- "Accept all" button for when the extraction looks correct

### Confidence scoring

The LLM should output a confidence indicator per player position:

```yaml
players:
  "1":
    position: [0, 32]
    confidence: high    # clearly at top of key
  "4":
    position: [8, 17]
    confidence: low     # ambiguous, could be elbow or wing
```

The correction editor highlights low-confidence players, guiding the coach to check only the positions that need it.

### Correction data as training signal

Log every correction:

```json
{
  "play": "Horns Elbow Pop",
  "page": 47,
  "strategy": "B",
  "corrections": [
    {"player": "4", "extracted": [8, 17], "corrected": [6, 19], "delta": 2.8},
    {"player": "2", "extracted": [-14, 26], "corrected": [-16, 26], "delta": 2.0}
  ]
}
```

After 50 corrections, analyze patterns:
- Does the LLM consistently place players too close to center? → Add a prompt instruction to spread positions wider
- Does it confuse block vs elbow positions? → Add those as explicit reference points in the calibration image
- Does it struggle with a specific book's diagram style? → Create per-book prompt variations

---

## Resolution 6 — Game-changer data (deferred)

**Resolves**: Gap 5
**Depends on**: Knowledge wiki ingestion pipeline (`spec/karpathy-llm-wiki.md`)
**Ship without these initially. Add incrementally as wiki cross-refs come online.**

### Branching reads

Data source: Wiki cross-reference between offensive plays (D1) and defensive counters (D2).

When the wiki ingests the defense book (Let's Talk Defense), each defensive concept page gets linked to the offensive plays it counters. The Play Viewer reads these links:

```yaml
# wiki page: pick-and-roll-defense.md
counters:
  - play: "Horns PnR"
    if_defense: "hard hedge"
    counter_action: "slip cut to basket"
    counter_player: "5"
  - play: "Horns PnR"
    if_defense: "switch"
    counter_action: "post up mismatch"
    counter_player: "1"
```

The Play Viewer converts these into branch points in the animation: after the screen is set, the user sees "What does the defense do?" with options. Each option triggers a different Phase 2.

### Spotlight mode text

Generated per-position after a play exists in the wiki:

```
Prompt to Claude:
You are a basketball coach explaining [Play Name] to Player [Position].
Use second person ("you"). Be specific about timing and reads.

Phase 1: [phase description]
Your role as [POS]: [what this player does]

Phase 2: [phase description]
Your role as [POS]: [what this player does]
Your read: if [defensive reaction], then [counter action].
```

Budget: ~$0.01 per play × 5 positions × ~200 plays = ~$10 total.
Run as a batch job after play extraction is complete.

### Ghost defense

Requires defensive player positions. Two sources:

1. **Defense book diagrams** — same extraction pipeline, applied to Let's Talk Defense (274 pages). Produces defensive position data.

2. **Default defensive positions** — for plays where we don't have explicit defensive data, generate reasonable defaults:

```typescript
function defaultDefense(offensivePositions: Record<string, [number, number]>): Record<string, [number, number]> {
  // Man-to-man: each defender 2-3 units between their man and the basket
  const basket = [0, 5.25];
  const defense: Record<string, [number, number]> = {};

  for (const [id, [ox, oy]] of Object.entries(offensivePositions)) {
    const dx = (basket[0] - ox) * 0.15;
    const dy = (basket[1] - oy) * 0.15;
    defense[`X${id}`] = [ox + dx, oy + dy];
  }

  return defense;
}
```

This produces "reasonable" defensive positions that are basketball-correct (between man and basket) even without source data.

---

## Execution order

```
Week 1 (parallel):
  ├── Resolution 1: 5-diagram proof of concept (THE GATE)
  └── Resolution 2: Bézier generation algorithm

  DECISION POINT after Resolution 1:
  ┌─────────────────────────────────────────────────────┐
  │ IF coordinates accurate (< 2 SVG units):            │
  │   → Pipeline viable. Continue to Week 2.            │
  │                                                     │
  │ IF coordinates close but noisy (2-5 SVG units):     │
  │   → Pipeline viable WITH correction editor.         │
  │   → Prioritize Resolution 5 in Week 2.              │
  │                                                     │
  │ IF coordinates wildly wrong (> 5 SVG units):        │
  │   → PIVOT to Plan B or Plan C (see below).          │
  └─────────────────────────────────────────────────────┘

Week 2:
  ├── Resolution 3: Diagram page detection (full 934-page scan)
  └── Resolution 4: Phase segmentation prompt refinement

Week 3:
  ├── Resolution 5: Correction editor design
  └── Begin processing detected diagram pages through pipeline

Week 3+:
  └── Human-review first 50 extracted plays. Measure error rate.
      Refine prompts based on correction data patterns.

Deferred:
  └── Resolution 6: Game-changer data (after wiki ingestion)
```

---

## Pivot scenarios

### Plan B — Name-based lookup + curated database

If the LLM cannot extract usable coordinates from diagrams:

1. The LLM reads the diagram and identifies the play BY NAME ("This is a Horns Elbow Pop")
2. We maintain a hand-curated database of the 50 most common plays with pre-built Play Data JSON
3. The LLM's job shrinks from "extract coordinates" to "classify which play" — much easier

The 50-play curated database covers ~80% of what coaches run. Build it manually using the Play Creator. Each play takes ~5-10 minutes to create = ~4-8 hours for 50 plays.

Custom or rare plays → Play Creator (manual entry).

### Plan C — Community-sourced library

1. Launch the Play Creator as a standalone tool
2. Coaches build their own plays
3. Best plays get shared/upvoted
4. Library grows organically
5. LLM extraction becomes a "nice to have" enhancement, not the primary source

### All plans use the same Play Viewer engine

The rendering is proven (v4, 3 game-changers, 12 iterations). Only the data source changes:

| Plan | Data source | LLM role | Human effort |
|------|-------------|----------|--------------|
| A (primary) | Auto-extracted from PDFs | Extract coordinates | Review + correct |
| B (fallback) | Curated database + name lookup | Classify play name | Build 50 plays manually |
| C (fallback) | Coach-created | None for creation | Full manual entry |

---

## Reference files

| File | What |
|------|------|
| `spec/play-viewer.md` | Play Viewer technical spec (6-layer SVG, 3-phase animation) |
| `spec/karpathy-llm-wiki.md` | Wiki ingestion pipeline (Karpathy pattern) |
| `spec/play-extraction-poc.md` | Claude Code task spec that executes Resolutions 1 + 2 |
| `screen-play-viewer-v4.jsx` | Play Viewer reference implementation (not yet checked in) |
| `screen-play-creator.jsx` | Play Creator wireframe (correction editor base; not yet checked in) |
| `cv-pipeline-architecture.jsx` | 7-layer CV pipeline explainer (not yet checked in) |

## Court coordinate reference

```
ViewBox: "-28 -3 56 50"
Origin (0,0) = center-top of half-court

Key positions:
  Basket:           (0, 5.25)
  Left block:       (-6, 8)
  Right block:      (6, 8)
  Left elbow:       (-8, 19)
  Right elbow:      (8, 19)
  Free throw:       (0, 19)
  Left wing:        (-16, 26)
  Right wing:       (16, 26)
  Top of key:       (0, 32)
  Left corner:      (-22, 4)
  Right corner:     (22, 4)
  Half court:       (0, 47)
  Left sideline:    (-25, y)   # painted sideline
  Right sideline:   (25, y)    # painted sideline
```

> **Note on the margin**: the painted court ends at x = ±25, but the viewBox extends to ±28 to provide a 3-unit bleed region for out-of-bounds actions (inbound passes, sideline plays). LLM extraction prompts and calibration reference images MUST anchor players to the ±25 painted sidelines, not the viewBox edge.
