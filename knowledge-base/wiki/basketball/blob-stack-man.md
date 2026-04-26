---
type: play
category: out-of-bounds
formation: stack
tags: [BLOB, man-to-man, youth, hard-cut, stack, simple]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: hard-cut-to-corner
    role: "1"
    criticality: required
  - id: hard-cut-to-opposite-block
    role: "4"
    criticality: required
  - id: step-in-catch-and-finish
    role: "3"
    criticality: required
  - id: inbound-pass-read
    role: "2"
    criticality: required
  - id: safety-valve-spacing
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: hard-cut-to-corner
    for_role: "1"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: hard-cut-to-opposite-block
    for_role: "4"
  - region: glute_max
    criticality: required
    supports_technique: hard-cut-to-opposite-block
    for_role: "4"
  - region: ankle_complex
    criticality: optional
    supports_technique: step-in-catch-and-finish
    for_role: "3"
  - region: core_outer
    criticality: optional
    supports_technique: step-in-catch-and-finish
    for_role: "3"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "Sequential hard cuts clear defenders from the paint, leaving role 3 open to step in and catch near the block or rim — a high-percentage shot by design."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The scripted two-cut sequence delivers a single direct inbound pass to a pre-read primary target, capping ball-movement complexity and minimizing live-ball turnover risk."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Routing the primary scoring option to a catch-and-finish near the rim generates a consistently high expected-point shot on a set possession."
---

# Stack (BLOB vs Man-to-Man — Simple Version)

## Overview
A simple, easy-to-teach BLOB play for youth teams. Players in a stack formation execute sequential hard cuts that spread defenders across the court, consistently leaving the third player in line open to step in and receive a pass for a short shot near the block or rim. [S4, p.27]

## Formation
- **2** (inbounder): at baseline
- **1, 4, 3, 5**: stacked in a vertical line on the ball-side lane edge (in that order from top to bottom/inside)

```json name=diagram-positions
{"players":[{"role":"2","x":7,"y":47},{"role":"1","x":3,"y":33},{"role":"4","x":3,"y":36},{"role":"3","x":3,"y":39},{"role":"5","x":3,"y":42}],"actions":[{"from":"1","to":"right_corner","type":"cut"},{"from":"4","to":"left low block","type":"cut"},{"from":"2","to":"3","type":"pass"}],"notes":"The first (top) diagram on p.27 shows the starting stack formation. 2 is the baseline inbounder on the right side. 1, 4, 3, 5 are stacked vertically along the right lane edge (from the elbow down toward the block). Action arrows show: 1 cutting hard left toward the left corner/wing, 4 cutting across to the opposite (left) block, and 2's pass arrow aimed toward 3 stepping in. The diagram is oriented with the basket at the bottom; left/right have been mapped accordingly (ball-side is the right side of the court as drawn)."}
```

## Phases

### Phase 1: First Two Cuts — Clear the Paint
- **1** blasts hard to the corner, calling for the ball.
- **4** quickly cuts to the **opposite side of the rim near the block**, calling for the ball.
- Both cuts must be hard and convincing to ensure defenders follow them out of the paint.

### Phase 2: Third Player Steps In
- With 1 and 4 having cleared their defenders, **3 steps in** and receives the inbound pass from **2** for a shot near the block or close to the rim.
- **3 is the primary scoring option** — 2 should resist the urge to pass to 1 immediately, but can pass to 4 if 4 has an easy layup. [S4, p.27]

### Phase 3: Safety Valve
- If the primary and secondary options are covered, **5 steps out to the top of the key** to receive the pass and reset.
- **2 now has three options**: 1 in the corner, 4 at the opposite block, 3 stepping in, plus 5 as safety.

## Key Coaching Points
- **Hard cuts are non-negotiable** — 1 and 4 must cut hard and call for the ball to guarantee their defenders leave the paint. [S4, p.27]
- **Be patient** — the third player (3) is the primary target; don't force the first available pass to 1. [S4, p.27]
- **Best big shooter** should be placed in the third position (3) since that player will be open most often. [S4, p.27]

## Counters
- If 3 is denied → 4 may have a layup on the cut across the lane.
- If all options are denied → 5 as safety at the top of the key.

## Related Plays
- [[blob-stack-zone]] — stack BLOB vs 2-3 zone
- [[blob-stack-double]] — more complex stack BLOB with staggered screen
- [[blob-flip]] — box BLOB for post layups

## Sources
- [S4, p.27] — full play description and coaching points
