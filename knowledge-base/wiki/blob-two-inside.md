---
type: play
category: out-of-bounds
formation: box
tags: [BLOB, man-to-man, screen-the-screener, post, layup, up-screen, cross-screen]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: up-screen-set
    role: "4"
    criticality: required
  - id: screen-the-screener-set
    role: "5"
    criticality: required
  - id: weak-side-rim-cut
    role: "4"
    criticality: required
  - id: post-seal-and-pivot
    role: "5"
    criticality: required
  - id: decoy-cut-and-call
    role: "1"
    criticality: required
  - id: inbound-pass-to-slot
    role: "3"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: weak-side-rim-cut
    for_role: "4"
  - region: glute_max
    criticality: required
    supports_technique: post-seal-and-pivot
    for_role: "5"
  - region: ankle_complex
    criticality: optional
    supports_technique: weak-side-rim-cut
    for_role: "4"
  - region: core_outer
    criticality: optional
    supports_technique: screen-the-screener-set
    for_role: "5"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The screen-the-screener and post-seal actions are designed to free a post player at the rim for a layup, the highest-eFG shot available."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The scripted 3-4 phase sequence limits decision-making to one or two predetermined pass targets, reducing the turnover surface compared to free-flow half-court offense."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Post players cutting to the rim after screening actions draw contact from scrambling defenders, inviting foul calls on the finish."
---

# Two Inside (BLOB vs Man-to-Man)

## Overview
This BLOB play is built for teams with dominant post players. Using an up-screen and a screen-the-screener action, it aims to free one of two post players (4 and 5) for an open layup at the rim, while the two guards occupy the perimeter and prevent help defense from collapsing. [S4, pp.28-29]

## Formation
- **3** (best passer): inbounder at baseline
- **4** and **5** (post players): down low on the blocks
- **1** and **2** (guards): high-post elbows

```json name=diagram-positions
{"players":[{"role":"3","x":0,"y":47},{"role":"4","x":-7,"y":40},{"role":"5","x":7,"y":40},{"role":"1","x":-8,"y":29},{"role":"2","x":8,"y":29}],"actions":[{"from":"4","to":"left_corner","type":"screen"},{"from":"1","to":"left_corner","type":"cut"},{"from":"2","to":"right_wing","type":"cut"},{"from":"3","to":"2","type":"pass"}],"notes":"The top diagram on p.28 shows the initial box formation: 3 is the out-of-bounds inbounder at the baseline (top of the half-court diagram), 4 and 5 are on the low blocks (4 weak-side/left, 5 ball-side/right), and 1 and 2 are at the high-post elbows (1 ball-side/left, 2 weak-side/right). Action arrows in the first diagram show 4 setting an up-screen for 1 cutting to the corner, 2 cutting toward the ball-side slot, and a pass line from 3 toward 2. The second diagram (Phase 2) is not extracted here per instructions."}
```

## Phases

### Phase 1: Up-Screen + Guard Spacing
- **4** sets an **up-screen** for **1**, who pops out to the corner.
- Simultaneously, **2** cuts to the **ball-side slot**, calling for the basketball to keep their defender out of the paint. [S4, p.28]

### Phase 2: Screen-the-Screener for 4
- **5** waits 1–2 seconds (while appearing to face 2) and then cuts across the lane to set a **strong screen on 4's defender**.
- This screen-the-screener action allows **4 to cut to the weak-side rim** for an open layup. [S4, p.28]
- **5 must start the play looking in 2's direction** so the action is not telegraphed. [S4, p.29]

### Phase 3: 5 Seals and Flashes
- After screening, **5 seals 4's defender** and pivots toward the hoop.
- **3 can pass to 5** for the open layup on the opposite side of the rim.
- If **5's defender cuts off the pass** to 4, then **4 should back out to the short corner** to open up the paint for 5. [S4, p.28]

### Phase 4: Safety — Reset
- If no pass inside is available, **3 passes over the top to 2**, and the team sets up the half-court offense. [S4, p.29]

## Key Coaching Points
- **1 and 2 must call for the basketball** while cutting/flashing even if they will not receive it — this keeps their defenders occupied and out of the paint. [S4, p.29]
- **5 must face toward 2** at the start to disguise the screen-the-screener timing. [S4, p.29]
- **Best used when your post players are dominant** or when there is a significant height mismatch. [S4, p.28]

## Counters
- 4 denied at the rim → 4 backs to the short corner, freeing 5 to seal and receive.
- Both posts covered → 3 passes to 2 to reset half-court offense.

## Related Plays
- [[blob-flip]] — box BLOB also targeting post finishers at the rim
- [[blob-yo-yo]] — box BLOB with dual up-screens for post cuts
- [[blob-box-gate]] — box BLOB with shooter freed off gate screen

## Sources
- [S4, pp.28-29] — full play description and coaching points
