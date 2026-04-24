---
type: play
category: offense
formation: 1-3-1
tags: [zone-offense, 2-3-zone, flare-screen, overload, skip-pass, three-point, on-ball-screen]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: skip-pass-to-open-shooter
    role: "2"
    criticality: required
  - id: on-ball-screen-set-and-roll
    role: "5"
    criticality: required
  - id: position-swap-cut
    role: "1"
    criticality: required
  - id: perimeter-spacing-pop
    role: "3"
    criticality: required
  - id: low-screen-on-zone-defender
    role: "4"
    criticality: required
  - id: dribble-read-off-screen
    role: "2"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: position-swap-cut
    for_role: "1"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: on-ball-screen-set-and-roll
    for_role: "5"
  - region: ankle_complex
    criticality: required
    supports_technique: dribble-read-off-screen
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: low-screen-on-zone-defender
    for_role: "4"
  - region: glute_max
    criticality: optional
    supports_technique: on-ball-screen-set-and-roll
    for_role: "5"
---

# Flare Overload

## Overview
A 2-3 zone play from a 1-3-1 set that attempts to get a perimeter player open for a three-point shot by forcing 1 defender to guard 3 offensive players. Achieved through player position swaps, an on-ball screen, and a simultaneous low screen to prevent the corner defender from rotating. [S4, pp.40-41]

## Formation
1-3-1 set. 1 at top, 2 on the wing (strong side), 3 at the other wing position, 5 at high post, 4 in the corner (behind three-point line, strong side — same corner as the zone's bottom player X4).

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":22},{"role":"2","x":18,"y":22},{"role":"3","x":-14,"y":22},{"role":"4","x":22,"y":42},{"role":"5","x":2,"y":29}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"1","to":"left_wing","type":"cut"},{"from":"3","to":"top_key","type":"cut"},{"from":"5","to":"2","type":"screen"},{"from":"5","to":"rim","type":"cut"}],"notes":"The first (upper) diagram on p.40 shows the 1-3-1 starting formation: 1 at the top of the key, 2 on the right wing, 3 on the left wing, 5 at the high post, and 4 in the right corner behind the three-point line. The diagram arrows depict: 1 passing to 2, 1 cutting left to the vacated wing, 3 cutting under and popping to the top of the key, 5 screening for 2, and 5 rolling to the rim. \"left_wing\" and \"top_key\" are used as destination anchors for the cuts since no player labels occupy those spots initially."}
```

## Phases

### Phase 1: Position Swap to Overload
- The first pass is always made **opposite** the side the corner player (4) is on. [S4, p.41]
- 1 passes to 2 on the wing.
- On this pass, 1 and 3 swap: 1 straight-cuts to the vacated wing (where 3 was), and 3 cuts under the weak-side top zone defender and pops out to the top of the key.
- This creates three offensive players spaced around the perimeter: 1 (wing), 2 (wing with ball), 3 (top of key).

### Phase 2: On-Ball Screen and Rotation Read
- 5 steps out from the high post and sets an on-ball screen for 2, then rolls to the basket.
- 2 uses the screen and reads X1 (the high zone defender who must now cover 3 at the top):
  - **If X1 doesn't rotate** to help, 2 is open for the outside shot off the dribble.
  - **If X1 rotates** to stop 2's drive, 2 can skip pass to 1 on the far wing, or pass to 3 at the top of the key — both should be open.
- Simultaneously, 4 screens X3 (the ball-side low zone defender) to prevent X3 from rotating out to contest the perimeter shot. [S4, p.40]

## Key Coaching Points
- The first pass must always go **opposite** the corner player's side — this is essential to create the overload geometry. [S4, p.41]
- 1, 2, and 3 must maintain good spacing around the perimeter so X1 cannot guard all three simultaneously. "Make it impossible for one defender to guard three." [S4, p.41]
- 4 must **time their screen on X3** carefully — setting it too early telegraphs the action and lets X3 fight through before the pass arrives. [S4, p.41]
- 2 must be a good decision-maker: read X1's rotation before committing to the shot or pass.

## Counters
- If the zone overloads to help on 2, 5's roll to the basket after the screen may be open for a layup.
- If X1 sags to protect the drive, 2 can pull up for a mid-range shot.

## Related Plays
- [[23-flare]] — similar zone play using flare screen to free a shooter
- [[play-pick-overload]] — another 2-3 zone overload play using an on-ball screen
- [[play-swinger]] — man-to-man play using on-ball screen with similar read options

## Sources
- [S4, pp.40-41] — full play description with diagrams
