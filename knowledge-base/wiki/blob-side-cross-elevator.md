---
type: play
category: out-of-bounds
formation: box
tags: [BLOB, zone, 2-3-zone, elevator-screen, sequential-screen, corner-three, inbounds]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: sequential-elevator-screen-set
    role: "5"
    criticality: required
  - id: sequential-elevator-screen-set
    role: "4"
    criticality: required
  - id: sprint-cut-off-screen
    role: "2"
    criticality: required
  - id: inbound-pass-delivery
    role: "1"
    criticality: required
  - id: catch-and-shoot-corner-three
    role: "2"
    criticality: required
  - id: screen-slip-and-show
    role: "4"
    criticality: optional
  - id: screen-slip-and-show
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: sprint-cut-off-screen
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: sprint-cut-off-screen
    for_role: "2"
  - region: glute_max
    criticality: required
    supports_technique: sequential-elevator-screen-set
    for_role: "4"
  - region: core_outer
    criticality: optional
    supports_technique: sequential-elevator-screen-set
    for_role: "5"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The entire play is engineered to deliver the best shooter a catch-and-shoot corner three via sequential elevator screens, the highest-value shot type by design."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The scripted two-screen sequence routes the inbound pass directly to the corner shooter in a single delivery, limiting live-ball turnover exposure to one pass."
  - factor: floor-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Built-in counter reads — shooter going over the top, 3 above the arc, and screen slips by 4 and 5 — ensure the play generates a scoring opportunity even when the primary action is contested."
---

# BLOB: Side Cross Elevator (vs 2-3 Zone)

## Overview
Side Cross Elevator is a 2-3 zone BLOB play that gets the best shooter an open corner three-point shot by using a creative sequential (elevator-style) screen on both side zone defenders. The two post players, starting outside the zone defenders, screen them in sequence — top then bottom — creating a lane for the shooter to sprint through to the corner. [S4, pp.15-16]

## Formation
**Box formation shifted closer to the ball side.** Crucially, **4** and **5** (post players) must start on the **outside** of the two zone side defenders (i.e., they line up between the side defenders and the sideline):
- **1**: out of bounds (in-bounder)
- **2**: ball-side, inside the box (shooter)
- **3**: weak-side position in box
- **4**: outside the bottom-wing zone defender (**x4**), ball side
- **5**: outside the top-wing zone defender (**x2**), ball side

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":-1},{"role":"2","x":4,"y":34},{"role":"3","x":-4,"y":30},{"role":"4","x":14,"y":34},{"role":"5","x":4,"y":28},{"role":"x2","x":8,"y":29},{"role":"x4","x":10,"y":36}],"actions":[{"from":"5","to":"x2","type":"screen"},{"from":"4","to":"x4","type":"screen"},{"from":"2","to":"right_corner","type":"cut"},{"from":"1","to":"2","type":"pass"}],"notes":"This is a BLOB (baseline out-of-bounds) play vs a 2-3 zone. Player 1 is the inbounder standing out of bounds on the side (right side ballside). The box formation is shifted toward the ball side (right side). 4 and 5 start outside the two zone side defenders (x2 at top wing, x4 at bottom wing). The first diagram (Phase 1 / setup) shows the initial box formation with 3 on the weak-side interior, 2 on the ball-side interior, 5 just outside x2 (top), and 4 just outside x4 (bottom). Action arrows in the second diagram show: 5 screens x2, 4 screens x4 (elevator sequence), 2 cuts to the right corner, and 1 passes to 2. Defenders x2 and x4 positions are approximate based on diagram."}
```

## Phases

### Phase 1: Top Screen
- **5** sprints up and sets a screen on the **top wing zone defender** (**x2**).

### Phase 2: Bottom Screen (Elevator)
- **4** runs off **5**'s screen and sets a screen on the **bottom wing zone defender** (**x4**).
- This creates an elevator-screen effect: the defender must navigate through two sequential screens.

### Phase 3: Shooter's Cut
- When **2** sees **5** has just set the screen on **x2**, **2** sprints off **4**'s back (using the second screen) out to the strong-side corner, ready to shoot.
- **1** delivers the inbound pass to **2** in the corner for the three-point shot.

## Key Coaching Points
- **4** and **5** must NOT start the play facing the direction they're going to screen — this telegraphs the action to the defense. [S4, p.16]
- **Counter for x2 going under 5's screen**: If **x2** ducks under the screen to block **2**, instruct **2** to go **over the top** of the screen to the corner instead. [S4, p.16]
- **Counter for defenders fighting over screens**: Use **3** as a safety option above the arc, and teach **4** and **5** to slip their screens and show themselves to the in-bounder as alternative targets. [S4, p.16]

## Counters
- **If x2 goes under 5's screen**: 2 goes over the top of the screen to reach the corner.
- **If all side defenders fight over screens**: 3 is open above the arc; 4 and 5 slip screens and show for the inbound pass.

## Related Plays
- [[blob-double-skip]] — BLOB 2-3 zone play using double flare screens on zone defenders
- [[blob-hawk]] — BLOB 2-3 zone play with simultaneous dual screens
- [[blob-box-flash]] — BLOB 2-3 zone play starting from box formation

## Sources
- [S4, pp.15-16]
