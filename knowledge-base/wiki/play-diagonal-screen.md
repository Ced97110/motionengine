---
type: play
category: offense
formation: box
tags: [diagonal-screen, screen-the-screener, post-up, half-court, continuity]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: diagonal-screen-set
    role: "5"
    criticality: required
  - id: post-up-on-catch
    role: "2"
    criticality: required
  - id: diagonal-back-screen-set
    role: "2"
    criticality: required
  - id: screen-the-screener-read
    role: "1"
    criticality: required
  - id: down-screen-set
    role: "5"
    criticality: required
  - id: baseline-cut-rub
    role: "3"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: post-up-on-catch
    for_role: "2"
  - region: glute_max
    criticality: required
    supports_technique: post-up-on-catch
    for_role: "2"
  - region: core_outer
    criticality: required
    supports_technique: diagonal-screen-set
    for_role: "5"
  - region: ankle_complex
    criticality: optional
    supports_technique: baseline-cut-rub
    for_role: "3"
---

# Motion Offense Diagonal Screen Play

## Overview
A half-court continuity play using a diagonal screen to post up a guard, followed by a diagonal back screen and screen-the-screener action. the source coach's Motion Offense used this to create multiple post-up and perimeter catch-and-shoot opportunities from the same box formation as the Cross-Screen and Up Screen plays. [S7, pp.69-70]

## Formation
Same box set:
- **1 (PG)**: left wing
- **2 (SG)**: right side (wing/corner)
- **5 (C)**: left high post
- **4 (PF)**: left low post
- **3 (SF)**: right wing

## Phases

### Phase 1: Diagonal Screen to Post-Up
- 1 dribbles to the **left wing**.
- 5 sets a **diagonal screen** for 2.
- 2 posts up on the **left low post**.
- 1 passes to **2** in the post; 5 rolls out of the lane.

```json name=diagram-positions
{"players":[{"role":"1","x":-20,"y":38},{"role":"2","x":14,"y":38},{"role":"3","x":18,"y":22},{"role":"4","x":4,"y":30},{"role":"5","x":-4,"y":30}],"actions":[{"from":"5","to":"2","type":"screen"},{"from":"2","to":"left_low_block","type":"cut"},{"from":"1","to":"2","type":"pass"},{"from":"5","to":"right_elbow","type":"cut"}],"notes":"Figure 4.57 starting formation: 1 is at the left corner/wing area with the ball (dribbling left), 2 starts right side near baseline, 3 is at right wing, 4 and 5 are at the corners of the free-throw area (high posts — 4 left elbow, 5 right-center of key). 5 sets a diagonal screen for 2 who cuts to the left low post; 1 passes to 2; 5 then rolls out of the lane. The diagram shows arrows for 5 screening 2, 2 cutting to left low block, a pass from 1 to 2, and 5 rolling out."}
```

### Phase 2: Screen-the-Screener Continuity
- If 2 does **not** receive the ball:
  - 2 sets a **diagonal back screen** for 4, who moves to the low post on the ball side.
  - 2 then receives a **down screen from 5** (screen-the-screener action).
  - 1's reads: pass to **4** in the low post, to **2** coming off 5's screen, or to **5** rolling to the basket.

```json name=diagram-positions
{"players":[{"role":"1","x":-20,"y":38},{"role":"2","x":-8,"y":29},{"role":"3","x":18,"y":22},{"role":"4","x":-4,"y":34},{"role":"5","x":4,"y":34}],"actions":[{"from":"2","to":"4","type":"screen"},{"from":"4","to":"left_low_block","type":"cut"},{"from":"5","to":"2","type":"screen"},{"from":"2","to":"right_wing","type":"cut"},{"from":"1","to":"4","type":"pass"},{"from":"1","to":"2","type":"pass"},{"from":"1","to":"5","type":"pass"}],"notes":"Figure 4.58 starting formation: 1 is at the left corner/wing with the ball, 2 is near the left elbow/high post area (having not received a pass), 3 is at the right wing, 4 and 5 are in the lane/paint area near the free-throw elbows. 2 sets a diagonal back screen for 4 (who cuts to the left low post), then 5 sets a down screen for 2 (screen-the-screener), with 2 curling out toward the right wing. 1 has three pass options: to 4 in the low post, to 2 coming off 5's screen, or to 5 rolling to the basket. The diagram shows dashed arrows for the screens and solid arrows for the pass options from 1."}
```

### Phase 3: Baseline Cut Option (Counter)
- 3 makes a **baseline cut**, rubbing around 4, cutting to the corner to receive a pass from 1.
- This takes away weak-side help and gives 1 an open corner three or mid-range shot. [S7, p.70]

```json name=diagram-positions
{"players":[{"role":"1","x":-20,"y":38},{"role":"2","x":4,"y":32},{"role":"3","x":18,"y":22},{"role":"4","x":-4,"y":30},{"role":"5","x":-2,"y":40}],"actions":[{"from":"3","to":"left_corner","type":"cut"},{"from":"1","to":"3","type":"pass"}],"notes":"Figure 4.59 starting formation: 1 is at the left corner/baseline area with the ball. 4 is near the left elbow/lane area. 5 is near the left low block. 2 is near the lane/middle area. 3 starts at the right wing and makes a baseline cut, rubbing around 4 (near the lane), curling to the left corner to receive a pass from 1. The diagram shows 3 cutting along the baseline around 4 and receiving the pass from 1 in the corner."}
```

## Key Coaching Points
- The diagonal screen is a **lower angle** than a standard back screen — it posts the screened player on the ball side at an effective angle.
- Screen-the-screener action means the defense must guard **two screens simultaneously**.
- 1 must read all four options quickly — post entry (4), pop (2), roll (5), and baseline cut (3).
- 3's baseline cut is an optional counter to weaken help-side rotation.

## Counters
- Defenders switching on 2's diagonal back screen: 5 rolls to basket immediately for a lob.
- 3's corner cut to eliminate weak-side help.

## Related Plays
- [[play-cross-screen]] — same box set, cross screen entry
- [[play-up-screen]] — same box set, back screen entry
- [[play-pick-and-roll-layered]] — final team box set play using PnR
- [[concept-screen-types-reads]] — screen-the-screener and diagonal screen reads

## Sources
- [S7, pp.69-70] — the source coach, Motion Offense
