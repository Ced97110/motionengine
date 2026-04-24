---
type: play
category: offense
formation: 1-4-high
tags: [high-post-cut, double-screen, pick-and-roll, catch-and-shoot, half-court, man-to-man]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: high-post-cut-off-screen
    role: "1"
    criticality: required
  - id: on-ball-pick-and-roll-attack
    role: "2"
    criticality: required
  - id: pick-and-roll-screen-set
    role: "5"
    criticality: required
  - id: double-screen-set
    role: "3"
    criticality: required
  - id: double-screen-set
    role: "4"
    criticality: required
  - id: catch-and-shoot
    role: "1"
    criticality: required
  - id: roll-to-rim
    role: "5"
    criticality: optional
  - id: dump-off-pass
    role: "2"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: high-post-cut-off-screen
    for_role: "1"
  - region: ankle_complex
    criticality: required
    supports_technique: catch-and-shoot
    for_role: "1"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: on-ball-pick-and-roll-attack
    for_role: "2"
  - region: core_outer
    criticality: required
    supports_technique: pick-and-roll-screen-set
    for_role: "5"
  - region: glute_max
    criticality: optional
    supports_technique: roll-to-rim
    for_role: "5"
  - region: core_outer
    criticality: optional
    supports_technique: double-screen-set
    for_role: "4"
---

# High-Post

## Overview
A man-to-man half-court play named after the initial High-Post cut by the point guard. The play sequences a High-Post cut (layup attempt), then a wing PnR for the wing player, while simultaneously freeing the point guard off a weak-side double screen for a catch-and-shoot. The PnR ball-handler has three reads: pass to PG for the shot, attack themselves, or pass to the rolling 5. [S4, pp.74-75]

## Formation
1-4 high: 1 at the top with the ball, 4 and 5 on the elbows, 2 on one wing, 3 on the other wing. [S4, p.74]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":15},{"role":"2","x":18,"y":22},{"role":"3","x":-18,"y":22},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"1","to":"rim","type":"cut"}],"notes":"The first (top) diagram on p.74 shows the 1-4 high starting formation: 1 at the top of the key with the ball, 4 and 5 on the elbows, 2 on the right wing, 3 on the left wing. The depicted action arrows show 1 passing to 2 on the right wing and then making the high-post basket cut off 5's screen toward the rim. This is Phase 1 as requested."}
```

## Phases

### Phase 1: Wing Entry & High-Post Cut
- 1 passes to 2 on the wing (or 3 — can be run either direction).
- 1 makes a High-Post cut off 5's screen, looking for the pass from 2 for the layup. [S4, p.74]

### Phase 2: PnR for 2 & Double Screen Setup
- If 1 is not open on the cut, 5 steps across and sets an on-ball screen for 2 (PnR).
- Simultaneously, 3 and 4 walk their defenders down toward the weak-side low block to set a double screen for 1. [S4, p.74]

### Phase 3: Three-Option Read
- 2 uses 5's screen and attacks the middle of the floor. After the pick, 5 rolls to the rim.
- As 2 drives, 1 cuts hard off the double screen from 3 and 4, getting open for the catch-and-shoot.
- 2's three options: (a) pass to 1 for the jump shot, (b) attack the rim or pull up for the midrange, or (c) pass to 5 rolling to the rim. [S4, p.75]

## Key Coaching Points
- This play can be run on **either side of the floor** — a useful advantage for keeping defenses guessing. [S4, p.75]
- Off the double screen, 1 should cut to a distance they can shoot from. For younger players, keep it inside the three-point line. [S4, p.75]
- 5 must set the PnR screen at the **correct angle** to allow 2 to attack the rim, not the sideline. [S4, p.75]
- 3 and 4 must walk their defenders down naturally — not telegraph the double screen by sprinting early.
- The High-Post cut (Phase 1) is a genuine scoring threat — 2 must look for 1 on that cut before moving to the PnR action.

## Key Personnel
- **1 (PG / Good Shooter)**: Makes the High-Post cut, then uses the weak-side double screen for the catch-and-shoot; must cut to their shooting range.
- **2 (SG / Wing — Good Decision Maker)**: Receives entry pass; looks for 1 on High-Post cut; attacks the PnR; reads all three options.
- **3 (SF)**: Weak-side wing; sets half of the double screen for 1 with 4; occupies x3.
- **4 (PF)**: Sets the other half of the double screen for 1; occupies x4.
- **5 (C)**: Sets the High-Post screen for 1's cut; then steps across to set the PnR for 2; rolls to the rim.

## Counters
- If the defense switches the PnR, 5 seals for a dump-off inside.
- If the double screen is switched, 1 can flare farther or cut backdoor.
- If x5 hedges hard on the PnR, 5 can pop to the elbow for a mid-range shot.

## Related Plays
- [[play-double-curls]] — related play from 1-4 high using High-Post cut + staggered screens for two guards
- [[play-iverson-ram]] — 1-4 high set leading into a PnR
- [[concept-setting-screens]] — double screen and PnR angle principles
- [[concept-reading-screens-off-ball]] — how 1 reads the double screen to maximize separation

## Sources
- [S4, pp.74-75]
