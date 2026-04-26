---
type: play
category: out-of-bounds
formation: wide-box
tags: [BLOB, zone, 2-3-zone, corner-three, flash, screen, inbounds]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: inbound-pass-entry
    role: "2"
    criticality: required
  - id: pop-to-wing-catch
    role: "3"
    criticality: required
  - id: mid-key-flash
    role: "4"
    criticality: required
  - id: down-screen-set
    role: "5"
    criticality: required
  - id: curl-cut-to-corner
    role: "2"
    criticality: required
  - id: zone-read-pass
    role: "4"
    criticality: required
  - id: catch-and-shoot-corner-three
    role: "2"
    criticality: required
  - id: low-block-finish
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: curl-cut-to-corner
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: curl-cut-to-corner
    for_role: "2"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: mid-key-flash
    for_role: "4"
  - region: core_outer
    criticality: required
    supports_technique: down-screen-set
    for_role: "5"
  - region: glute_max
    criticality: optional
    supports_technique: low-block-finish
    for_role: "5"
  - region: core_outer
    criticality: optional
    supports_technique: catch-and-shoot-corner-three
    for_role: "2"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The play is designed by construction to deliver the ball to the best shooter at the corner for a three-point attempt, the highest-value shot type in eFG terms."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The counter option routes the ball inside to role 5 on the low block, where contact from a recovering zone defender is expected and draws fouls."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The scripted inbounds sequence limits live-ball touches to a fixed two-pass chain (3 → 4 → 2), minimizing the improvised decision-making that generates turnovers."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "Targeting either a corner three or a low-block layup as the only two designed outcomes concentrates possessions in the two most efficient shot locations on the floor."
---

# BLOB: Belmont Flash (vs 2-3 Zone)

## Overview
The Belmont Flash is a baseline out-of-bounds play designed to attack the 2-3 zone and produce an open corner three-point shot for the best shooter (who is in-bounding the ball). The play catches the low ball-side post defender off-guard by drawing attention to a weak-side flash before delivering the ball to the corner shooter off a strong screen. [S4, pp.5-6]

## Formation
**Wide Box Set.** Players set up in an expanded box — instead of the standard low blocks and elbows, all four on-court players are positioned approximately 3 feet wider than usual:
- **2 (in-bounder/best shooter)**: out of bounds on the baseline
- **4**: wide elbow / near wing, ball side
- **5**: wide elbow / near wing, weak side
- **1**: weak-side low block area
- **3**: ball-side low block area

```json name=diagram-positions
{"players":[{"role":"2","x":0,"y":47},{"role":"4","x":-11,"y":29},{"role":"5","x":11,"y":29},{"role":"1","x":-9,"y":40},{"role":"3","x":9,"y":40}],"actions":[{"from":"2","to":"3","type":"pass"},{"from":"1","to":"top_of_key","type":"cut"},{"from":"3","to":"4","type":"pass"},{"from":"5","to":"x3","type":"screen"},{"from":"2","to":"right_corner","type":"cut"}],"notes":"The first (top) diagram on p.5 shows the initial wide box formation. 2 is the out-of-bounds inbounder on the baseline (center). 4 and 5 are at the wide elbows (ball-side left and weak-side right respectively). 1 is at the weak-side low block area, and 3 is at the ball-side low block area. Defenders x1, x2, x3, x4, x5 are also shown. The diagram depicts the first action: 2 inbounding to 3 popping to the wing, and 1 cutting toward the top of the key. The \"right_corner\" and \"x3\" target labels are approximations — x3 is on the ball-side low post area near 3's starting spot."}
```

## Phases

### Phase 1: Initial Entry
- **3** pops out to the wing and receives the inbound pass from **2**.
- **1** simultaneously cuts to the top of the key as a safety valve if an extra pass is needed before feeding inside.

### Phase 2: Weak-Side Flash
- On **3**'s catch, **4** immediately flashes to the middle of the key to receive the pass from **3**.
- This flash draws the middle zone defender (x5) toward the key.

### Phase 3: Screen & Corner Cut
- **5** sets a screen on the low ball-side post defender (x3).
- **2** (the in-bounder) steps inbounds and curls around **5**'s screen to the ball-side corner, ready to shoot.
- **4** reads the defense: if **x3** is caught by the screen, **4** passes to **2** in the corner for the three-point shot.

### Phase 4: Counter Option
- If **x3** does fight over the screen to contest **2**, **x5** is now occupied defending **4** in the mid-key.
- **5** is left open on the low block for a bounce pass from **4** and a layup.

## Key Coaching Points
- Use this play sparingly — it relies on catching the defense off-guard. Overuse kills the element of surprise. [S4, p.6]
- **4** must make the correct read on **x3**: pass to **2** in the corner OR pass to **5** on the block. This is the critical decision point.
- If **5** catches inside, they must go up strong immediately because **x5** will typically recover and foul. [S4, p.6]
- The best shooter should always be the in-bounder in this play. [S4, p.5]

## Counters
- **If x3 fights over 5's screen**: 4 hits 5 on the low block for the bounce pass and layup.
- **If the pass to 3 is denied**: 1 is available at the top of the key for a relay pass to restart the action.

## Related Plays
- [[blob-hawk]] — another BLOB 2-3 zone quick-hitter that uses a similar element-of-surprise approach
- [[blob-box-flash]] — BLOB 2-3 zone play also starting from a box set with multiple scoring options
- [[blob-double-skip]] — BLOB 2-3 zone play using double flare screens for the in-bounder

## Sources
- [S4, pp.5-6]
