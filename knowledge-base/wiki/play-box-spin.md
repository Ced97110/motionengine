---
type: play
category: out-of-bounds
formation: box
tags: [SLOB, man-to-man, quick-hitter, curl-cut, three-point, double-screen, box-set]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: inbound-pass-on-target
    role: "1"
    criticality: required
  - id: sequential-screen-set
    role: "5"
    criticality: required
  - id: curl-cut-to-rim
    role: "3"
    criticality: required
  - id: catch-and-shoot-three
    role: "2"
    criticality: required
  - id: pop-off-screen
    role: "2"
    criticality: optional
  - id: safety-outlet-read
    role: "1"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: curl-cut-to-rim
    for_role: "3"
  - region: ankle_complex
    criticality: required
    supports_technique: curl-cut-to-rim
    for_role: "3"
  - region: core_outer
    criticality: required
    supports_technique: sequential-screen-set
    for_role: "5"
  - region: glute_max
    criticality: optional
    supports_technique: catch-and-shoot-three
    for_role: "2"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The play's two primary reads are a rim-cut layup and a catch-and-shoot three, eliminating mid-range attempts by design."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Role 3's hard curl-cut through two sequential screens to the rim creates direct contact opportunities against defenders caught in the screen traffic."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The set-play structure routes all action through a single inbound pass followed by one decisive read, keeping ball-handler decisions and live-ball exposure to a minimum."
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When 3 cannot receive the pass at the rim, 5 stays put and 2 uses that screen to burst out to the three-point line for a catch-and-shoot opportunity."
    extraction: llm-inferred
  - text: "When both the rim cut and the three-point pop are taken away, 1 stationed in the weak-side corner serves as a safe outlet to reset the possession."
    extraction: llm-inferred
---

# Box Spin

## Overview
A quick SLOB hitter from a box set designed to simultaneously create a rim-cut layup for one player and an open three-point shot for the best shooter. Two sequential screens by 5 generate both looks. [S4, pp.83-84]

## Formation
Box set: **2 (best 3-pt shooter)** on the ball-side elbow, **3 (rim cutter)** on the weak-side elbow, **5 (post screener)** on the ball-side low block, **1** on the weak-side low block. 1 inbounds from the sideline. [S4, p.83]

```json name=diagram-positions
{"players":[{"role":"1","x":22,"y":29},{"role":"2","x":8,"y":29},{"role":"3","x":-8,"y":29},{"role":"4","x":-7,"y":40},{"role":"5","x":7,"y":40},{"role":"OB","x":-22,"y":29}],"actions":[{"from":"2","to":"rim","type":"cut"},{"from":"5","to":"rim","type":"cut"},{"from":"3","to":"rim","type":"cut"},{"from":"OB","to":"3","type":"pass"}],"notes":"The diagram shows a box set SLOB play. 1 is the inbounder on the left sideline near the elbow extended. The box formation has 2 on the ball-side (right) elbow, 3 on the weak-side (left) elbow, 5 on the ball-side (right) low block, and 4 on the weak-side (left) low block. The first diagram shows 2 and 5 rotating/moving toward the weak-side to set screens for 3, with 3 cutting toward the rim. The inbounder (labeled \"1\" in the diagram with a circle, positioned at the left sideline) passes inbound. The prose labels the inbounder as \"1\" and assigns no \"4\" — the box set uses players 1, 2, 3, and 5 per the prose, with 1 as the inbounder on the sideline. Adjusted: 1=OB on left sideline, 2=ball-side elbow (right), 3=weak-side elbow (left), 5=ball-side low block (right), and the weak-side low block player is implied but not labeled in the prose. Emitting the standard box starting formation based on the diagram's first phase."}
```

## Phases

### Phase 1: Double Screen for Rim Cutter
- 2 and 5 rotate and set screens for 3.
- 3 uses **2's screen** at the weak-side elbow, then **5's screen** at the ball-side elbow, cutting strong to the rim looking for the pass and finish.
- 1 clears out to the weak-side corner to create space. [S4, p.83]

### Phase 2: Screen for the Shooter
- After 3's defender has battled past 5's screen, 5 **steps across** and sets a strong screen for 2.
- 2 explodes out toward the three-point line for a quick catch-and-shoot. [S4, p.83]
- 1 (now in the weak-side corner) reads and remains available as a safety outlet.

## Key Coaching Points
- "The player inbounding the basketball must make the passes on-time and on-target." [S4, p.84]
- "3 must sprint towards the ball after the first screen before quickly cutting towards the rim off the second screen." [S4, p.84]
- "2 must not give away that they're about to pop out to the three-point line. Best to catch the defender off-guard." [S4, p.84]
- 5's ability to set two strong, sequential screens is the engine of the play — requires a powerful post screener.

## Counters
- If 3 is not open at the rim, 5 holds position and 2 pops for the three-pointer.
- If both options are denied, 1 in the weak-side corner provides an outlet for a reset.

## Related Plays
- [[play-box-loop-post]] — SLOB box set with sequential down screens for post isolation
- [[play-deception-slob]] — SLOB box set with backdoor layup and three-point shot
- [[concept-setting-screens]] — technique for sequential screens

## Sources
- [S4, pp.83-84] — full play description and coaching points
