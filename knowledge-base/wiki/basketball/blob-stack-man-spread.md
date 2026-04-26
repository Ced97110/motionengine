---
type: play
category: out-of-bounds
formation: stack
tags: [BLOB, man-to-man, youth, stack, sequential-cuts, simplicity]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: hard-cut-to-corner
    role: "1"
    criticality: required
  - id: hard-cut-to-weak-side-block
    role: "4"
    criticality: required
  - id: catch-and-finish-near-block
    role: "3"
    criticality: required
  - id: inbound-pass-read
    role: "2"
    criticality: required
  - id: safety-outlet-cut
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: hard-cut-to-corner
    for_role: "1"
  - region: ankle_complex
    criticality: required
    supports_technique: hard-cut-to-weak-side-block
    for_role: "4"
  - region: glute_max
    criticality: required
    supports_technique: catch-and-finish-near-block
    for_role: "3"
  - region: core_outer
    criticality: optional
    supports_technique: inbound-pass-read
    for_role: "2"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "Sequential cuts by roles 1 and 4 pull defenders out of the paint, leaving role 3 with a catch-and-finish opportunity at the block — a high-percentage look by design."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The set-play structure routes the inbound pass directly to a pre-designated receiver after just one or two reads, limiting live-ball turnovers compared to open motion."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Targeting a near-block finish as the primary option converts a set-play possession into a near-rim attempt, maximizing expected points per trip."
---

# BLOB Stack Man (Spread)

## Overview
A simple BLOB play perfect for youth basketball. From a stack formation, the first two players make hard sequential cuts to spread the court, leaving the third player open to receive a pass near the basket for a quick shot. [S4, p.27]

## Formation
Stack formation under the basket: 1, 4, 3, 5 stacked vertically. 2 inbounds from the sideline. [S4, p.27]

```json name=diagram-positions
{"players":[{"role":"2","x":7,"y":-1},{"role":"1","x":3,"y":33},{"role":"4","x":3,"y":36},{"role":"3","x":3,"y":39},{"role":"5","x":3,"y":42}],"actions":[{"from":"1","to":"left_corner","type":"cut"},{"from":"4","to":"rim","type":"cut"},{"from":"2","to":"3","type":"pass"}],"notes":"Diagram 1 (top, Phase 1 setup) is used. 2 is the inbounder positioned on the right sideline near the elbow extended. Players 1, 4, 3, 5 are stacked vertically on the ball-side (right side) of the key from just below the elbow down to near the baseline. Arrow shows 1 cutting hard left toward the corner, 4 cutting down toward the opposite (left) block/rim area, and the implied pass target is 3. The stack is slightly right of center near the lane line."}
```

## Phases

### Phase 1: First Two Cuts
- 1 blasts hard to the corner, calling for the basketball (drags their defender).
- 4 quickly cuts to the opposite side of the rim near the block (drags their defender).
- Both cuts must be hard and convincing to pull defenders away from the paint.

### Phase 2: Third Player Open
- With 1 and 4's defenders occupied, 3 (third in line) steps in and receives the pass from 2 for an open shot near the block or close to the rim.
- 2 now has three potential scoring options (1 in corner, 4 at weak-side block, 3 near ball-side block).

### Phase 3: Safety Outlet
- If none of the first three options are available, 5 steps out to the top of the key to receive the pass and reset the offense.

## Key Coaching Points
- The initial cuts by 1 and 4 **must be hard cuts with loud calls** — defenders must be convinced to follow them. [S4, p.27]
- **3 is the primary scoring option** — 2 should be patient and not immediately pass to 1. Can pass to 4 only if 4 has an easy layup. [S4, p.27]
- Place the **best big shooter third in line** — that player will be open most often. [S4, p.27]
- No key personnel matchups required — accessible for all youth teams. [S4, p.27]

## Counters
- 5 at the top of the key is the reset option if all three primary options are covered.

## Related Plays
- [[blob-stack-man]] — existing simple youth stack BLOB (sequential hard cuts version)
- [[blob-stack-double]] — more complex stack BLOB for teams with an elite shooter
- [[blob-stack-zone]] — stack formation adapted for 2-3 zone
- [[play-selection-principles]] — simplicity and personnel fit principles

## Sources
- [S4, p.27]
