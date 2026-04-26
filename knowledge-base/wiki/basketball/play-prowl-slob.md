---
type: play
category: out-of-bounds
formation: box
tags: [SLOB, man-to-man, pick-and-roll, box-set, quick-hitter, floor-spacing]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: down-screen-set
    role: "4"
    criticality: required
  - id: down-screen-set
    role: "5"
    criticality: required
  - id: cut-to-top-off-screen
    role: "2"
    criticality: required
  - id: on-ball-screen-set
    role: "5"
    criticality: required
  - id: pick-and-roll-ball-handler
    role: "2"
    criticality: required
  - id: floor-spacing-wing
    role: "1"
    criticality: optional
  - id: floor-spacing-wing
    role: "3"
    criticality: optional
  - id: roll-to-rim
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: pick-and-roll-ball-handler
    for_role: "2"
  - region: glute_max
    criticality: required
    supports_technique: on-ball-screen-set
    for_role: "5"
  - region: ankle_complex
    criticality: required
    supports_technique: cut-to-top-off-screen
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: on-ball-screen-set
    for_role: "5"
---

# Prowl (SLOB)

## Overview
A quick SLOB play from a box formation that uses simultaneous down screens to get the ball to the top, then immediately runs a pick-and-roll with good floor spacing. Direct and efficient — minimal phases before the primary action. [S4, pp.93-94]

## Formation
Box set: **2 (PnR ball-handler)** and **3** at the high-post elbows, **4** and **5 (PnR screener)** at the low blocks. **1** inbounds from the sideline. [S4, p.93]

```json name=diagram-positions
{"players":[{"role":"OB","x":-28,"y":22},{"role":"2","x":-7,"y":29},{"role":"3","x":7,"y":29},{"role":"4","x":-7,"y":40},{"role":"5","x":7,"y":40}],"actions":[{"from":"4","to":"2","type":"screen"},{"from":"5","to":"3","type":"screen"},{"from":"2","to":"top_key","type":"cut"},{"from":"3","to":"right_wing","type":"cut"},{"from":"OB","to":"2","type":"pass"}],"notes":"This is the Phase 1 (starting) formation from the first diagram on p.93. It is a sideline out-of-bounds (SLOB) box set: 1 (OB) inbounds from the left sideline at roughly mid-paint height. 2 and 3 start at the high-post elbows; 4 and 5 start at the low blocks. 4 down-screens for 2 (who cuts to top), 5 down-screens for 3 (who pops to weak-side wing), and 1 passes to 2 at the top. The diagram's ball-side (inbounder) is on the left sideline. \"top_key\" and \"right_wing\" are used as destination anchors for the cuts."}
```

## Phases

### Phase 1: Simultaneous Down Screens
- Post players (4 and 5) set **simultaneous down screens** for guards (2 and 3).
- 2 cuts to the top of the key and receives the inbound pass from 1.
- 3 pops out to the **weak-side wing** for floor spacing. [S4, p.93]

### Phase 2: Inbounder Enters; Pick-and-Roll
- After making the pass, 1 steps inbounds to the **ball-side wing**.
- 5 immediately **sprints up** and sets an on-ball screen for 2.
- 2 uses the screen and attacks the rim. [S4, p.93]

### Phase 3: PnR Read
- **Option A:** 2 finishes at the basket.
- **Option B:** If 4's defender helps on 2's drive, 2 drops the pass to 4 for the finish. [S4, p.93]
- 1 and 3 on the wings provide kick-out safety valves.

## Key Coaching Points
- "5 must set the screen on the correct angle to prevent 2's defender from slipping under the screen." [S4, p.94]
- "5 should also aim to create as much separation as possible between themselves and their defender by exploding out to set the screen. This prevents their defender from hedging." [S4, p.94]
- "2 must be a good decision maker when attacking. If 4's defender steps up to help, pass. If they don't, finish at the rim." [S4, p.94]
- Floor spacing (1 and 3 on wings, 4 rolling) is essential for the PnR to create true 2-on-1 situations.

## Counters
- If defense hedges hard on the PnR → 5 rolls to the rim or pops to the elbow for a short jumper.
- If both options are covered → kick to 1 or 3 on the wing for a reset or open three.

## Related Plays
- [[play-diamond-slob]] — SLOB box play also ending in PnR with multiple options
- [[play-box-loop-post]] — SLOB box play with sequential screening for post isolation
- [[concept-setting-screens]] — angle and explosion on the on-ball screen

## Sources
- [S4, pp.93-94] — full play description and coaching points
