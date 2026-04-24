---
type: play
category: offense
formation: 1-3-1
tags: [zone-offense, 2-3-zone, on-ball-screen, overload, three-point, penetration-kick, corner-three]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: dribble-drag-to-wing
    role: "1"
    criticality: required
  - id: on-ball-screen-use
    role: "1"
    criticality: required
  - id: drive-and-kick-read
    role: "1"
    criticality: required
  - id: on-ball-screen-set
    role: "5"
    criticality: required
  - id: spot-up-three-point-shooting
    role: "2"
    criticality: required
  - id: baseline-deep-cut
    role: "3"
    criticality: required
  - id: corner-three-catch-and-shoot
    role: "4"
    criticality: optional
  - id: offensive-glass-crash
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: drive-and-kick-read
    for_role: "1"
  - region: glute_max
    criticality: required
    supports_technique: drive-and-kick-read
    for_role: "1"
  - region: ankle_complex
    criticality: required
    supports_technique: baseline-deep-cut
    for_role: "3"
  - region: core_outer
    criticality: optional
    supports_technique: on-ball-screen-set
    for_role: "5"
  - region: hip_flexor_complex
    criticality: optional
    supports_technique: corner-three-catch-and-shoot
    for_role: "4"
---

# Pick Overload

## Overview
A 2-3 zone play from a 1-3-1 formation designed to get an open three-point shot on the wing or in the corner. The play overloads one side of the zone by forcing 2 defenders to guard 3 offensive players through an on-ball screen for the point guard followed by a baseline cut, creating a 3v2 scenario. [S4, pp.44-45]

## Formation
1-3-1 set. 1 at top, 2 on one wing, 3 on the other wing, 5 at the high post, 4 in the corner (baseline).

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":16},{"role":"2","x":20,"y":22},{"role":"3","x":-20,"y":22},{"role":"4","x":20,"y":40},{"role":"5","x":0,"y":29}],"actions":[{"from":"1","to":"right_wing","type":"dribble"},{"from":"3","to":"left_corner","type":"cut"}],"notes":"The first (top) diagram on p.44 shows the 1-3-1 starting formation. 1 is at the top of the key area, 2 on the right wing, 3 on the left wing, 5 at the high post, and 4 in the right corner/baseline. The diagram shows 1 dribbling right (toward 2's side) with a squiggly dribble arrow, and 3 beginning to slide down toward the corner. 4 appears near the right elbow/wing area in the diagram but is described as a baseline player — placed at right corner per the 1-3-1 description. The dribble arrow for 1 goes toward the right wing."}
```

## Phases

### Phase 1: Drag Defender and Screen
- 1 dribbles to either side of the floor, dragging the high zone defender X1 to the wing.
- Simultaneously, 3 slides down toward the corner to give 1 more space on the wing.
- 5 steps out from the high post and screens X1. [S4, p.44]

### Phase 2: Drive and Read
- 1 uses the screen and attacks the high post area.
- **Primary read — no help:** If X2 (the wing zone defender) doesn't slide across to stop dribble penetration, 1 can finish with a floater or midrange pull-up. [S4, p.44]
- **Secondary read — X2 helps:** When X2 stops the drive (as expected), 1 passes to 2 on the ball-side wing who should be wide open for the three-point shot. [S4, p.44]
- Simultaneously with 1 using the screen, 3 deep-cuts along the baseline to the **opposite corner**, creating a 3-on-2 overload on the ball side (1 driving, 2 on wing, 4 in corner vs. X2 and X4). [S4, p.44]

### Phase 3: Kick to Corner
- As X2 stops the drive, only X4 can contest 2's wing shot.
- **If X4 sprints out** to contest 2's shot, 2 passes to 4 on the baseline for the open corner three-point shot. [S4, p.45]
- On the shot, 1 **immediately retreats and plays safety** to prevent transition defense. [S4, p.45]

## Key Coaching Points
- It doesn't matter which side of the floor the play is run — both wings will be in shooting positions. 4 on the baseline starts either side but must go to the ball-side when the ball is reversed. [S4, p.45]
- 5 and 4 must **crash the offensive glass** on the shot. [S4, p.45]
- 1 needs good decision-making: recognize quickly whether X2 is helping before committing to the shot or pass.
- Key personnel: 1 (decision-maker who can finish), 2 and 3 (reliable three-point shooters). [S4, p.44]

## Counters
- If X1 fights over the screen, 1 can reject the screen and dribble the other direction.
- If the zone over-rotates to help on the drive, 5's roll to the rim may be open.

## Related Plays
- [[play-flare-overload]] — similar 1-3-1 zone play using an on-ball screen
- [[play-swinger]] — man-to-man PnR play with similar multiple-option read structure
- [[23-flare]] — zone play using zone overload and shooter freeing action

## Sources
- [S4, pp.44-45] — full play description with diagrams
