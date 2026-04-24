---
type: play
category: out-of-bounds
formation: box
tags: [BLOB, man-to-man, screen-the-screener, post, layup, inside, mismatch, guards-clear]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: inbound-pass-timing
    role: "3"
    criticality: required
  - id: up-screen-set
    role: "4"
    criticality: required
  - id: cross-screen-set
    role: "5"
    criticality: required
  - id: rim-cut-on-screen
    role: "4"
    criticality: required
  - id: post-seal-and-pivot
    role: "5"
    criticality: required
  - id: decoy-cut-with-call
    role: "1"
    criticality: optional
  - id: decoy-cut-with-call
    role: "2"
    criticality: optional
  - id: short-corner-bailout
    role: "4"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: rim-cut-on-screen
    for_role: "4"
  - region: glute_max
    criticality: required
    supports_technique: post-seal-and-pivot
    for_role: "5"
  - region: core_outer
    criticality: required
    supports_technique: cross-screen-set
    for_role: "5"
  - region: ankle_complex
    criticality: optional
    supports_technique: up-screen-set
    for_role: "4"
---

# BLOB Two Inside

## Overview
Designed for teams with dominant post players or size mismatches. From a box formation, guards clear to safety positions to keep defenders occupied while a screen-the-screener action (up-screen then cross-screen) frees either post player at the rim for an open layup. [S4, pp.28-29]

## Formation
Box formation with two post players (4, 5) on the low blocks and two guards (1, 2) at the high-post elbows. 3 (best passer) inbounds from sideline. [S4, p.28]

```json name=diagram-positions
{"players":[{"role":"3","x":0,"y":-1},{"role":"4","x":-7,"y":40},{"role":"5","x":7,"y":40},{"role":"1","x":-8,"y":29},{"role":"2","x":8,"y":29}],"actions":[{"from":"4","to":"1","type":"screen"},{"from":"1","to":"left_corner","type":"cut"},{"from":"2","to":"right_corner","type":"cut"},{"from":"5","to":"4","type":"screen"},{"from":"4","to":"rim","type":"cut"},{"from":"3","to":"4","type":"pass"}],"notes":"The diagram shows a BLOB box formation with 3 as the out-of-bounds inbounder at the top (sideline, treated as y≈-1 since it's a baseline out-of-bounds play depicted from above). Looking at the first diagram: 3 is at the top (inbounder), 4 is at the left low block, 5 is at the right low block, 1 is at the left (ball-side) elbow, and 2 is at the right (weak-side) elbow. The first diagram shows the initial action: 4 up-screens for 1 who cuts to the corner, 2 moves to the ball-side slot, and arrows indicate the pass from 3. The second diagram shows the later screen-the-screener phase. Starting formation coordinates align with the box setup described in the marker."}
```

## Phases

### Phase 1: Guards Clear, Set Deception
- 4 sets an up-screen for 1, who pops out to the corner.
- As 1 cuts to the corner, 2 cuts to the ball-side slot, calling for the basketball — this keeps 2's defender out of the paint.
- 5 waits 1-2 seconds while **facing 2** (to disguise the upcoming screen action).

### Phase 2: Screen-the-Screener Action
- 5 cuts across the lane and sets a strong cross screen on 4's defender.
- This frees 4 to cut to the weak-side of the rim for an open layup.
- 3 reads and passes to 4 for the layup.

### Phase 3: Screener Seals and Scores
- After setting the screen, 5 seals 4's defender and pivots toward the hoop.
- 3 can pass to 5 on the seal for the open layup if 4's option is denied.
- If 5's defender cuts off the pass to 4, 4 backs out to the short corner to clear the paint for 5's seal move.

### Phase 4: Reset
- If no inside options are available, 3 passes over the top to 2 and the team sets up the half-court offense. [S4, p.29]

## Key Coaching Points
- 1 and 2 **must call for the basketball** while cutting — even knowing they won't receive it — to drag defenders away from the paint. [S4, p.29]
- 5 must **start the play looking toward 2** so the screen-the-screener action is not telegraphed to the defense. [S4, p.29]
- Best for teams with **great post players** or players with a height advantage over their direct opponent. [S4, p.28]
- Best passer should inbound (3) — they control the timing of the entire play. [S4, p.28]

## Counters
- If 5's defender helps on 4's cut, 4 backs to short corner and 5 seals for the layup on the other side.
- If all inside options are denied, reset via pass to 2 at the top. [S4, p.29]

## Related Plays
- [[blob-two-inside]] — existing page (update/merge)
- [[blob-flip]] — similar dual-post rim attack BLOB
- [[blob-yo-yo]] — up-screen box BLOB for post layups
- [[blob-box-gate]] — box BLOB with back screen and gate screen sequence

## Sources
- [S4, pp.28-29]
