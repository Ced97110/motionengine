---
type: play
category: offense
formation: 1-4-high
tags: [man-to-man, double-screen, shooter, quick-hitter, perimeter, wing]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: pass-and-return
    role: "2"
    criticality: required
  - id: sharp-curl-cut
    role: "2"
    criticality: required
  - id: double-screen-set
    role: "3"
    criticality: required
  - id: double-screen-set
    role: "4"
    criticality: required
  - id: catch-and-shoot
    role: "2"
    criticality: required
  - id: on-time-on-target-pass
    role: "1"
    criticality: required
  - id: curl-to-basket
    role: "2"
    criticality: optional
  - id: post-duck-in
    role: "3"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: sharp-curl-cut
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: sharp-curl-cut
    for_role: "2"
  - region: glute_max
    criticality: required
    supports_technique: catch-and-shoot
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: double-screen-set
    for_role: "3"
  - region: core_outer
    criticality: optional
    supports_technique: double-screen-set
    for_role: "4"
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When D4 reads the double screen early and fights over the top, 2 abandons the pop and curls hard toward the basket for a layup opportunity instead."
    extraction: llm-inferred
  - text: "When 2 is completely denied off the double screen, either 3 or 4 seizes the opportunity to seal and duck in toward the paint after their screening action is complete."
    extraction: llm-inferred
---

# Doubles

## Overview
A quick-hitter set play for your team's best shooter from a 1-4 high formation. The play moves the defense with a wing pass-and-return, then the shooter makes a deep cut off a double screen for an open perimeter shot. [S4, p.39]

## Formation
1-4 high set. 1 at top of key, 2 (best shooter) on the wing, 3 on the opposite wing, 4 and 5 at the elbows.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":22},{"role":"2","x":-18,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":8,"y":29},{"role":"5","x":-8,"y":29}],"actions":[{"from":"1","to":"2","type":"pass"}],"notes":"The first (top) diagram on p.39 shows the 1-4 high starting formation. 1 is at the top of the key, 2 is on the left wing, 3 is on the right wing, 4 and 5 are at the elbows. The diagram also shows numbered labels (3, 4 near the elbows and 5 at the high post area — consistent with the 1-4 high description). The initial action arrow visible is 1 passing to 2 on the left wing. The second diagram shows Phase 2 (the double screen and cut) and is not extracted here per the instructions to return the starting/initial formation."}
```

## Phases

### Phase 1: Move the Defense
- 1 passes to 2 (best shooter) on the wing.
- 2 passes back to 1 at the top of the key.
- This initial exchange shifts the defense and sets up the primary action.

### Phase 2: Double Screen and Shoot
- As 2 passes back to 1, 2 immediately makes a deep cut behind the defense (away from the ball, toward the baseline).
- 1 dribbles across the top of the key to create a better passing angle.
- As 2 is cutting, 3 and 4 set a double screen on 2's defender (D4).
- 2 uses the double screen and cuts to the perimeter (wing or corner) for the open shot.
- 1 passes to 2 who shoots.

## Key Coaching Points
- This play can be run on either side of the floor. [S4, p.39]
- The shot can be a midrange shot or a three-point shot depending on player skill level and age. [S4, p.39]
- 1 must make the pass "on-time and on-target" — 2 will be open for only a brief window.
- 2's cut must be sharp and fast to leverage the double screen before the defense recovers.

## Counters
- If D4 anticipates the double screen and goes over early, 2 can curl to the basket instead of popping to the perimeter.
- If 2 is fully denied, 3 or 4 can look to duck in after setting the screen.

## Related Plays
- [[play-1-4-quick-floppy]] — another 1-4 high set play with perimeter options
- [[blob-stack-double]] — BLOB version of a double-screen shooter play

## Sources
- [S4, p.39] — full play description with diagrams
