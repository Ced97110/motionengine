---
type: play
category: out-of-bounds
formation: stack
tags: [BLOB, man-to-man, staggered-screen, shooter, wing-shot, three-point, dribble-fake, deception]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: inbound-pass-reception-pop
    role: "4"
    criticality: required
  - id: dribble-fake-direction-change
    role: "1"
    criticality: required
  - id: staggered-screen-set
    role: "4"
    criticality: required
  - id: staggered-screen-set
    role: "5"
    criticality: required
  - id: screen-read-off-ball
    role: "2"
    criticality: required
  - id: catch-and-shoot-wing
    role: "2"
    criticality: required
  - id: baseline-sprint-clear
    role: "3"
    criticality: optional
  - id: backdoor-cut-off-screen
    role: "2"
    criticality: optional
demands_anatomy:
  - region: ankle_complex
    criticality: required
    supports_technique: screen-read-off-ball
    for_role: "2"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: screen-read-off-ball
    for_role: "2"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: dribble-fake-direction-change
    for_role: "1"
  - region: core_outer
    criticality: required
    supports_technique: staggered-screen-set
    for_role: "4"
  - region: glute_max
    criticality: optional
    supports_technique: baseline-sprint-clear
    for_role: "3"
  - region: ankle_complex
    criticality: optional
    supports_technique: catch-and-shoot-wing
    for_role: "2"
---

# BLOB Stack Double

## Overview
A stack BLOB play designed to free the best shooter for an open midrange or three-point shot on the wing. The play uses ball movement, a deceptive dribble fake by the PG, and a staggered double screen from both post players. [S4, pp.25-26]

## Formation
Stack formation with 2 (best shooter), 4, and 5 stacked on one side. PG (1) is at the weak-side elbow. 3 inbounds from the sideline. [S4, p.25]

```json name=diagram-positions
{"players":[{"role":"3","x":0,"y":-1},{"role":"2","x":-3,"y":36},{"role":"4","x":-3,"y":38},{"role":"5","x":-3,"y":40},{"role":"1","x":8,"y":29}],"actions":[{"from":"4","to":"left_wing","type":"cut"},{"from":"3","to":"4","type":"pass"}],"notes":"This is the initial (Phase 1) formation from the top diagram on p.25. 3 is the out-of-bounds inbounder on the ball-side sideline (top of the diagram, near half-court). 2, 4, and 5 are stacked vertically on the ball-side near the key (left side of the diagram). 1 is at the weak-side (right) elbow. The first diagram shows 4 popping out to receive the inbound pass from 3, with 2 dragging lower toward the basket as a decoy."}
```

## Phases

### Phase 1: Initial Ball Movement
- 4 pops out to the perimeter and receives the inbound pass from 3.
- Simultaneously, 2 drags their defender lower by taking a few steps toward the basket, calling for the basketball (decoy).
- After inbounding, 3 sprints the baseline and clears to the weak-side wing.
- 1 cuts to the top of the key and receives a pass from 4.

### Phase 2: PG Dribble Fake
- 1 takes a dribble in the **opposite direction** (toward 3 at the top) to get the defenders moving away from 2's cut.
- This fake shifts defensive attention and opens the passing lane to 2.

### Phase 3: Staggered Double Screen and Shot
- 4 and 5 immediately set a staggered double screen for 2.
- 2 reads their defender and cuts out off the screens.
- 1 passes to 2 on the wing for the midrange or three-point shot.

## Key Coaching Points
- 1 must **sell the fake dribble** toward 3 convincingly to move the defense across. [S4, p.26]
- **Players must not face the direction they're going to move** at the start of the play — body language gives away the action. [S4, p.26]
- 2 reads their defender off the staggered screen and chooses which screen to come off. [S4, p.25]

## Counters
- If 2 is overplayed, they can cut backdoor off the double screen.
- 3 at the weak-side wing provides a safety valve if all options are denied.

## Related Plays
- [[blob-stack-double]] — existing page (update/merge)
- [[blob-stack-man]] — simpler stack BLOB for youth with sequential hard cuts
- [[concept-reading-screens-off-ball]] — how 2 should read their defender at the double screen
- [[play-selection-principles]] — deception through body language and play design

## Sources
- [S4, pp.25-26]
