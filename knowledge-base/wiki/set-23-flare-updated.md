---
type: play
category: offense
formation: 1-3-1
tags: [zone, 2-3-zone, flare-screen, three-point, quick-hitter, set-play, shooter, ball-movement]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: skip-pass-over-screen
    role: "1"
    criticality: required
  - id: flare-screen-set
    role: "5"
    criticality: required
  - id: flare-cut-to-wing
    role: "2"
    criticality: required
  - id: zone-ball-movement
    role: "2"
    criticality: required
  - id: pin-down-screen-set
    role: "4"
    criticality: optional
  - id: catch-and-shoot-off-screen
    role: "2"
    criticality: required
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: flare-cut-to-wing
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: flare-cut-to-wing
    for_role: "2"
  - region: core_outer
    criticality: required
    supports_technique: flare-screen-set
    for_role: "5"
  - region: glute_max
    criticality: optional
    supports_technique: catch-and-shoot-off-screen
    for_role: "2"
---

# Set Play: 23 Flare (vs 2-3 Zone)

## Overview
A quick-hitter set play against a 2-3 zone. Extended ball movement pulls zone defenders around, then a sudden flare screen by 5 at the strong-side elbow frees the best shooter (2) for an open three-point shot on the wing. Reserve for 1-2 uses per game maximum. [S4, pp.33-34]

## Formation
1-3-1 formation. 2 (best shooter) on the wing. 4 in the strong-side corner. 3 at weak-side wing. 5 at the high post (will step to elbow). 1 at the top of the key. [S4, p.33]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":18},{"role":"2","x":18,"y":22},{"role":"3","x":-18,"y":22},{"role":"4","x":22,"y":42},{"role":"5","x":0,"y":26}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"2","to":"4","type":"pass"},{"from":"5","to":"right_elbow","type":"cut"}],"notes":"Extracting the first (topmost) diagram on page 1, which shows the 1-3-1 starting formation. 1 is at the top of the key with a dribble arrow, passing to 2 on the right wing. 5 is at the high post stepping toward the strong-side elbow. 2 receives and passes to 4 in the right corner. 3 is on the left wing. The diagram is small but the positions match the described 1-3-1 setup."}
```

## Phases

### Phase 1: Initial Ball Movement and Zone Manipulation
- 1 dribbles a few steps and passes to 2 on the wing. 1 remains at the top of the key.
- 5 steps to the strong-side elbow.
- 2 immediately passes to 4 in the corner.
- 4 passes back to 2. While doing so, 4 begins **walking their defender (x4) toward the rim** — setting up the screen that prevents x4 from contesting later.

### Phase 2: Drag x2 Away
- 2 takes 2-3 dribbles toward the top of the key, forcing x2 to follow to deny the open shot.
- 2 passes to 1 at the top of the key.

### Phase 3: Flare Screen and Open Three
- 5 immediately sets a **quick flare screen** for 2 at the elbow. Speed is critical — x2 must be caught off guard.
- Simultaneously, 4 (having walked x4 toward the rim) sets a screen to prevent x4 from contesting 2's shot.
- 2 uses the flare screen and cuts to the wing.
- 1 passes over the top to 2 for the open three-point shot.

## Key Coaching Points
- The flare screen by 5 **must be set quickly** to catch x2 off guard. [S4, p.34]
- This play will **fool the defense only once or twice per game** — save it for crucial moments when a three-pointer is needed. [S4, p.34]
- 1 must be able to make an **accurate skip pass over the flare screen** to 2's shooting pocket. [S4, p.33]
- 5 must be able to set a solid, physical screen. [S4, p.33]

## Counters
- If 2 is denied off the flare, look to 3 on the weak-side wing as the ball swings.

## Related Plays
- [[23-flare]] — existing page (update/merge)
- [[32-lob]] — companion 2-3 zone set play using weak-side overload and backdoor lob
- [[blob-stack-zone]] — BLOB zone play also using zone manipulation
- [[concept-setting-screens]] — principles of effective flare screen technique

## Sources
- [S4, pp.33-34]
