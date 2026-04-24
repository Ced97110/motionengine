---
type: play
category: out-of-bounds
formation: box
tags: [SLOB, man-to-man, alley-oop, back-screen, double-screen, wide-box, lob]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: lob-pass-inbound
    role: "1"
    criticality: required
  - id: back-screen-set
    role: "2"
    criticality: required
  - id: double-screen-set
    role: "4"
    criticality: required
  - id: alley-oop-finish
    role: "4"
    criticality: required
  - id: hard-cut-to-rim
    role: "2"
    criticality: optional
  - id: flash-to-corner
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: alley-oop-finish
    for_role: "4"
  - region: glute_max
    criticality: required
    supports_technique: alley-oop-finish
    for_role: "4"
  - region: core_outer
    criticality: required
    supports_technique: back-screen-set
    for_role: "2"
  - region: ankle_complex
    criticality: optional
    supports_technique: hard-cut-to-rim
    for_role: "2"
---

# Loop Fly (SLOB)

## Overview
A SLOB play from a wide box formation whose primary action is an alley-oop from the inbounder to a post player cutting toward the rim off a back screen. Only recommended for teams with an athlete who can finish the lob. Secondary option is a hard cut to the rim. [S4, pp.89-90]

## Formation
Wide box: **5** and **3** in slot positions (top area), **4** and **2** two to three steps off the low block (bottom area). **1 (best passer)** inbounds from the sideline. [S4, p.89]

```json name=diagram-positions
{"players":[{"role":"1","x":-22,"y":30},{"role":"2","x":10,"y":40},{"role":"3","x":18,"y":22},{"role":"4","x":0,"y":38},{"role":"5","x":-4,"y":28}],"actions":[{"from":"5","to":"4","type":"screen"},{"from":"2","to":"rim","type":"cut"},{"from":"1","to":"2","type":"pass"},{"from":"3","to":"rim","type":"cut"}],"notes":"This is the first (Phase 1) diagram on p.89. The wide box SLOB setup: 1 is the out-of-bounds inbounder on the left sideline around the elbow/wing level. 5 is near the top of the key area (slot, left of center), having begun cutting toward 4. 3 is in the right slot position. 4 is near the right low block / elbow area forming the double screen with 5. 2 starts near the right low block and cuts hard toward the rim off the double screen. The diagram shows 1 passing to 2 cutting to the rim, and 3 curling around the right side. 5 cutting to join 4 is also depicted."}
```

## Phases

### Phase 1: Double Screen for Initial Cut
- 5 cuts to the top to set a double screen with 4.
- 2 times their cut to go off the double screen exactly as 4 arrives and establishes screening position.
- 2 cuts hard to the rim, looking to receive the pass for an open layup. [S4, p.89]

### Phase 2: Decoy and Reset
- As 2 clears out, 3 cuts to the top of the key to drag out their defender and create space.
- If 2 does not receive the pass on the initial cut, 5 flashes to the ball-side corner. [S4, p.89]

### Phase 3: Back Screen Alley-Oop
- 2 curls around in the key and sets a **strong back screen** on 4's defender.
- 4 explodes toward the key, looking to receive the lob pass from 1 and finish in the air, or catch and go back up strong. [S4, pp.89-90]

## Key Coaching Points
- "Best passer must be inbounding the basketball." [S4, p.90]
- "It's not compulsory that 4 finishes with a dunk or in the air. They can land with the basketball and then go back up strong." [S4, p.90]
- "It's very important that 2 hunts 4's defender and sets a strong screen!" [S4, p.90]
- "Players must not give away the play with their eyes or the direction they're facing. Including the inbounds passer." [S4, p.90]
- Timing of 2's cut off the double screen is critical — must coincide exactly with 4 completing the screen setup.

## Counters
- If 4 is denied the lob, 5 in the ball-side corner is available for a pass and jump shot.
- If 2 is open on the initial cut, take the early layup immediately.

## Related Plays
- [[play-box-loop-post]] — SLOB box play using sequential down screens
- [[play-box-spin]] — SLOB box quick hitter with rim cut and three-point shot
- [[32-lob]] — zone SLOB play using a backdoor lob action
- [[concept-setting-screens]] — hunting the screener's target, holding the screen

## Sources
- [S4, pp.89-90] — full play description and coaching points
