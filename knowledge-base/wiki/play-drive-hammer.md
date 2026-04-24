---
type: play
category: offense
formation: box
tags: [pick-and-roll, hammer-screen, drive, corner, spacing, ball-screen]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: dribble-entry-wing
    role: "1"
    criticality: required
  - id: high-cut-off-elbow-screen
    role: "3"
    criticality: required
  - id: on-ball-screen-set
    role: "5"
    criticality: required
  - id: drive-to-rim-off-ball-screen
    role: "3"
    criticality: required
  - id: hammer-back-screen-set
    role: "4"
    criticality: required
  - id: catch-and-shoot-off-back-screen
    role: "1"
    criticality: optional
  - id: kickout-pass-on-drive
    role: "3"
    criticality: optional
  - id: roll-to-rim-after-screen
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: drive-to-rim-off-ball-screen
    for_role: "3"
  - region: glute_max
    criticality: required
    supports_technique: drive-to-rim-off-ball-screen
    for_role: "3"
  - region: ankle_complex
    criticality: required
    supports_technique: high-cut-off-elbow-screen
    for_role: "3"
  - region: core_outer
    criticality: optional
    supports_technique: on-ball-screen-set
    for_role: "5"
  - region: hip_flexor_complex
    criticality: optional
    supports_technique: catch-and-shoot-off-back-screen
    for_role: "1"
  - region: ankle_complex
    criticality: optional
    supports_technique: roll-to-rim-after-screen
    for_role: "5"
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When the defense switches the on-ball screen, 5 immediately rolls hard toward the rim to create a mismatch and receive a direct pass for an easy finish inside."
    extraction: llm-inferred
  - text: "When x1 anticipates the hammer screen and cheats over it early, 1 slides to a different spot in the corner to give 3 a fresh passing angle on the drive."
    extraction: llm-inferred
---

# Drive Hammer

## Overview
A box set play designed to get a guard attacking the rim off a quick on-ball screen, with a simultaneous hammer (back) screen for a corner shooter and an additional corner passing option. The defense is forced to choose between stopping the drive, helping on the roll, or leaving a corner shooter open. [S4, pp.58-59]

## Formation
Box set: 4 and 5 start at the elbows (top of the paint), 2 and 3 on the low blocks. 1 starts at the top of the key with the ball. [S4, p.58]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":14},{"role":"2","x":7,"y":40},{"role":"3","x":-7,"y":40},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"actions":[{"from":"1","to":"left_wing","type":"dribble"},{"from":"3","to":"left_elbow","type":"cut"},{"from":"4","to":"3","type":"screen"},{"from":"1","to":"3","type":"pass"},{"from":"2","to":"right_corner","type":"cut"}],"notes":"The diagram on p.58 shows two phases. This reflects the INITIAL (Phase 1) box formation: 1 at the top with the ball, 4 and 5 at the elbows, 2 and 3 on the low blocks. Phase 1 action arrows show 1 dribbling to the left wing, 3 cutting high off a screen by 4 at the elbow to receive the pass from 1, and 2 retreating from the weak-side low block toward the right corner. Phase 2 diagram (also on p.58) shows the subsequent on-ball screen by 5 and hammer screen by 4."}
```

## Phases

### Phase 1: Wing Entry & Setup
- 1 dribbles to either wing (left wing in this example).
- The ball-side low block player (3) cuts high off the screen on the elbow and receives the pass from 1.
- Simultaneously, the weak-side low post player (2) retreats out to the corner to provide spacing. [S4, p.58]

### Phase 2: On-Ball Screen & Hammer Action
- On 3's catch, 5 immediately steps across and sets an on-ball screen. The goal is to surprise the defenders with the quickness of this screen.
- While the on-ball screen is being set, 4 begins moving to set a hammer (back) screen on 1's defender as 3 drives to the rim.
- 3 uses the screen and attacks the rim looking to score, while both corner players (1 and 2) are available as passing options. [S4, p.58]

### Phase 3: Read & Finish
- If the defense helps on the drive, 3 passes to the open corner player.
- The weak-side corner defender (x2) typically helps on the drive — 3 must be ready to kick out to 2 as soon as that happens. [S4, p.59]

## Key Coaching Points
- The on-ball screen from 5 must be set **immediately** on the catch to catch the defender off-guard. Any delay lets x3 recover. [S4, p.59]
- The hammer screen for 1 must be timed precisely — set it **as 3 is driving**, not before. If set too early, x1 has time to fight over the screen and deflect the pass. [S4, p.59]
- 3 must keep their eyes up while driving and be ready to pass to 2 the moment x2 rotates to help. [S4, p.59]
- This play can become predictable if run too many times. Use it as a quick-score play when needed. [S4, p.57]

## Key Personnel
- **1 (PG)**: Shooter in the corner after dribbling entry; must be ready to catch and shoot off the hammer screen.
- **2 (SG)**: Shooter in the weak-side corner; primary outlet when help defense rotates.
- **3 (SF/G)**: The ball-handler who attacks the rim off the PnR. Must read the defense and make the right play.
- **4 (PF)**: Sets the hammer back screen on 1's defender; timing is critical.
- **5 (C)**: Sets the immediate on-ball screen for 3; screen angle must be on the backside of 3's defender.

## Counters
- If the defense switches the on-ball screen, 5 rolls hard to the rim for an easy catch and finish.
- If x1 cheats over the hammer screen, 1 can relocate to the corner for a different passing angle.

## Related Plays
- [[play-flip-gate]] — another 1-4 high / box play using back screen + gate screen combination
- [[play-iverson-ram]] — uses Iverson cuts followed by a pick-and-roll for similar PnR scoring
- [[concept-setting-screens]] — principles for setting the back/hammer screen at correct angle and timing

## Sources
- [S4, pp.58-59]
