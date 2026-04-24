---
type: play
category: out-of-bounds
formation: box
tags: [SLOB, man-to-man, shooter, read-the-defense, box-set, catch-and-shoot, on-ball-screen]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: down-screen-entry
    role: "5"
    criticality: required
  - id: on-ball-screen-set
    role: "4"
    criticality: required
  - id: read-screen-direction
    role: "2"
    criticality: required
  - id: catch-and-shoot
    role: "2"
    criticality: required
  - id: inbound-pass-delivery
    role: "2"
    criticality: required
  - id: rim-attack-off-ball-screen
    role: "1"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: read-screen-direction
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: catch-and-shoot
    for_role: "2"
  - region: core_outer
    criticality: required
    supports_technique: on-ball-screen-set
    for_role: "4"
  - region: glute_max
    criticality: optional
    supports_technique: rim-attack-off-ball-screen
    for_role: "1"
---

# Option (SLOB)

## Overview
A SLOB play that empowers the best shooter to **read their defender** and choose whether to cut to the top of the key or cut baseline — the defense cannot cheat either direction. Excellent late-game three-point play. [S4, pp.91-92]

## Formation
Box set: **2 (best shooter)** inbounds from the sideline (starts outside), **5** and **4** at the elbows, **1** and **3** at the low blocks. [S4, p.91]

```json name=diagram-positions
{"players":[{"role":"2","x":-28,"y":33},{"role":"5","x":-4,"y":29},{"role":"4","x":8,"y":29},{"role":"1","x":-7,"y":40},{"role":"3","x":7,"y":40}],"actions":[{"from":"5","to":"1","type":"screen"},{"from":"1","to":"top_of_key","type":"cut"},{"from":"2","to":"1","type":"pass"},{"from":"4","to":"1","type":"screen"},{"from":"1","to":"right_wing","type":"dribble"}],"notes":"This is the starting (Phase 1) formation from the first diagram on p.91. Box set: 2 is the sideline inbounder on the left, 5 and 4 at the elbows (5 left/center, 4 right elbow), 1 and 3 on the low blocks. The diagram shows 5 down-screening for 1 cutting to the top, 2 passing to 1, and 4 setting an on-ball screen as 1 dribbles right across the top of the key. The second diagram on p.91 shows Phase 2 (2 cutting low after inbounding)."}
```

## Phases

### Phase 1: Getting the Ball In
- 5 sets a down screen for 1, who cuts to the top of the key and receives the inbound pass from 2.
- 4 immediately sets an **on-ball screen** for 1, who dribbles across the top of the key. [S4, p.91]
- **Optional read:** If the on-ball screen creates a clear path, 1 can attack the rim for an open layup (3 pops to the corner to create space and a catch-and-shoot option).

### Phase 2: Shooter Reads the Screen
- 2 (after inbounding) cuts **low** along the baseline.
- 5 holds their position — stationary obstacle for 2's defender to navigate around (avoids moving screen).
- 2 reads their defender and makes the decision: **cut baseline** or **cut to the top of the key** for a catch-and-shoot. [S4, p.91]

### Phase 3: Screen and Shot
- Depending on 2's chosen direction, **3 or 4 sets a screen** to free 2.
- 1 makes the pass to 2's inside shoulder as 2 curls around.
- 2 catches and shoots. [S4, p.92]

## Key Coaching Points
- "2 doesn't need to rush as they cut low. Instruct them to read the defense and then allow the screens to give them an advantage." [S4, p.92]
- "1 should be focusing on passing to the inside shoulder of the shooter as they curl around. If it's too far out, the shooter won't be able to catch and shoot quickly." [S4, p.92]
- "This can be a great play to run late in the game when you need a three-point shot." [S4, p.92]
- The defense cannot anticipate the cut direction — this is the play's greatest strength.

## Counters
- If 1 sees a clear lane off the on-ball screen → attack the rim immediately (3 pops to corner).
- If 2's read is disrupted → 5 holding position can flash to the elbow as a safety valve.

## Related Plays
- [[play-deception-slob]] — SLOB box play with dual simultaneous scoring options
- [[play-diamond-slob]] — SLOB box with multiple option reads
- [[concept-reading-screens-off-ball]] — principles for reading the defender on screens
- [[play-selection-principles]] — when to use specific plays

## Sources
- [S4, pp.91-92] — full play description and coaching points
