---
type: play
category: out-of-bounds
formation: triangle
tags: [SLOB, man-to-man, cross-screen, screen-the-screener, low-post, catch-and-shoot, drive]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: cross-screen-set
    role: "1"
    criticality: required
  - id: screen-the-screener-down-screen
    role: "4"
    criticality: required
  - id: high-low-cut-off-screen
    role: "5"
    criticality: required
  - id: catch-and-shoot-off-screen
    role: "1"
    criticality: required
  - id: low-post-catch-and-finish
    role: "5"
    criticality: required
  - id: inbound-read-and-pass
    role: "2"
    criticality: required
  - id: drive-to-rim-off-rescreen
    role: "1"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: high-low-cut-off-screen
    for_role: "5"
  - region: glute_max
    criticality: required
    supports_technique: low-post-catch-and-finish
    for_role: "5"
  - region: core_outer
    criticality: required
    supports_technique: cross-screen-set
    for_role: "1"
  - region: ankle_complex
    criticality: optional
    supports_technique: catch-and-shoot-off-screen
    for_role: "1"
  - region: hip_flexor_complex
    criticality: optional
    supports_technique: drive-to-rim-off-rescreen
    for_role: "1"
  - region: core_outer
    criticality: optional
    supports_technique: screen-the-screener-down-screen
    for_role: "4"
---

# Triangle (SLOB)

## Overview
A SLOB play from a triangle formation that uses a cross-screen followed by screen-the-screener action to create either a strong post player close to the basket or a three-point shooter at the top of the key, plus a drive option. [S4, pp.95-96]

## Formation
Three players in a triangle: **1 (best 3-pt shooter)** at the ball-side low block, **5 (best low-post scorer)** at the weak-side low block, **4** at the free-throw line. **2 (inbounder)** passes from the sideline. **3** is in a wide position for spacing. [S4, p.95]

```json name=diagram-positions
{"players":[{"role":"2","x":-28,"y":29},{"role":"3","x":-18,"y":22},{"role":"1","x":-7,"y":40},{"role":"4","x":0,"y":29},{"role":"5","x":7,"y":40}],"actions":[{"from":"1","to":"5","type":"screen"},{"from":"5","to":"rim","type":"cut"},{"from":"4","to":"1","type":"screen"}],"notes":"This is the starting (Phase 1) formation from the first diagram on p.95. 2 is the sideline inbounder on the left side at roughly the free-throw line extended. 3 is wide on the weak-side wing for spacing. 1 is on the ball-side (right) low block, 5 is on the weak-side (right, as drawn) low block, and 4 is at the free-throw line. The diagram shows 1 cross-screening for 5 (5 cutting toward the rim) and 4 beginning to cut down to screen 1's defender. The ball-side in the diagram appears to be the right side (where 2 inbounds), so player positions are mapped accordingly with 1 on ball-side low block and 5 on weak-side low block."}
```

## Phases

### Phase 1: Cross Screen for Post Player
- 1 sets a **cross-screen** for 5.
- 5 reads the defense and cuts **high or low** toward the basket, looking to catch close to the rim and finish.
- If 5 doesn't receive the basketball, they establish position on the **ball-side low block**. [S4, p.95]

### Phase 2: Screen-the-Screener for Shooter
- Immediately after 1 screens for 5, **4 cuts down** from the free-throw line and sets a strong screen on **1's defender** (screen-the-screener action).
- 1 uses 4's screen and cuts to the **top of the key** looking for a catch-and-shoot opportunity off the pass from 2. [S4, p.95]

### Phase 3: Decision Point
- 2 now has two options:
  - **Pass into the low post to 5** → 4 clears to the weak-side wing to create space.
  - **Pass to 1 at the top of the key** → 4 re-screens for 1, who drives hard to the rim toward the open side of the court. [S4, pp.95-96]

## Key Coaching Points
- "As always, timing is very important to the success of this play. The one players have the most trouble with is 4 setting the down screen at the correct time." [S4, p.96]
- "Very important to have a smart passer inbound the basketball. If the basketball is passed too late it's easy to miss out on scoring opportunity." [S4, p.96]
- "Ensure players are holding their screens and not allowing the defense to easy slip past." [S4, p.96]
- **"Screeners have to hunt the player they're screening. Don't screen space!"** [S4, p.96]
- 5 reading high vs. low cut is critical — use whichever gap the defender gives.

## Counters
- If 5 is fronted in the post → throw skip to 1 at the top for the three or drive.
- If 1's cut to the top is denied → 4 flashing to the elbow off the failed screen is available.

## Related Plays
- [[play-deception-slob]] — SLOB box play with screen-the-screener flavor
- [[play-diamond-slob]] — SLOB box multi-option with curl and flare
- [[concept-setting-screens]] — hunting the defender, holding screens
- [[concept-reading-screens-off-ball]] — 5's read on the cross-screen

## Sources
- [S4, pp.95-96] — full play description and coaching points
