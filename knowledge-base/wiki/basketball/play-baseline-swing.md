---
type: play
category: offense
formation: 4-out 1-in
tags: [zone-offense, 2-3-zone, baseline-cut, screen, shooter, corner-three, midrange]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: skip-pass-to-wing
    role: "3"
    criticality: required
  - id: zone-ball-reversal
    role: "1"
    criticality: required
  - id: post-screen-on-zone-defender
    role: "5"
    criticality: required
  - id: baseline-cut-off-screen
    role: "4"
    criticality: required
  - id: catch-and-shoot-corner
    role: "4"
    criticality: required
  - id: wing-cut-across-zone
    role: "3"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: baseline-cut-off-screen
    for_role: "4"
  - region: ankle_complex
    criticality: required
    supports_technique: baseline-cut-off-screen
    for_role: "4"
  - region: glute_max
    criticality: optional
    supports_technique: catch-and-shoot-corner
    for_role: "4"
  - region: core_outer
    criticality: optional
    supports_technique: post-screen-on-zone-defender
    for_role: "5"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The play's geometry channels role-4 to a corner three or short-corner catch-and-shoot — both high-efficiency looks — by design, with no mid-range scramble shots."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Ball movement follows a scripted reversal path (1→3→1→2→3→4) with predetermined reads at each node, limiting unscripted dribble-penetration decisions that generate turnovers against zone."
  - factor: floor-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Sequential ball reversal forces the 2-3 zone to rotate across multiple gaps simultaneously, consistently generating an open catch-and-shoot opportunity for role-4 on each execution."
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When X5 battles through 5's screen before 4 arrives, 4 abandons the baseline cut and pivots to flash toward the mid-post for a closer look."
    extraction: llm-inferred
  - text: "When X3 fails to fully honor 3's wing presence, 3 keeps the ball and rises for the open shot instead of swinging the pass to 4."
    extraction: llm-inferred
---

# Baseline Swing

## Overview
A 2-3 zone play designed to get a shooter an open shot on the baseline from midrange or the three-point line. The play forces the baseline zone defender to play on-ball on the wing, then cuts the shooter baseline off a post screen to the wide-open ball-side short corner. [S4, pp.37-38]

## Formation
4-out 1-in. Shooter (4) starts in the strong-side corner. Posts (5) near the high post/elbow area. 1 at top of key, 2 at weak-side wing, 3 at strong-side wing.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":30},{"role":"2","x":-18,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":22,"y":42},{"role":"5","x":0,"y":36}],"actions":[{"from":"1","to":"3","type":"pass"}],"notes":"Extracting the initial (Setup) formation from the first of three diagrams on p.37. The play begins in a 4-out 1-in set: 1 at top of key, 2 at weak-side (left) wing, 3 at strong-side (right) wing, 4 in the strong-side (right) corner, and 5 near the high post/paint area. The first action arrow shown is 1 passing to 3. Subsequent phases (3 cutting across, 5 screening X5, 4 cutting baseline) are depicted in diagrams 2 and 3 and are not part of the starting formation."}
```

## Phases

### Phase 1: Shift the Defense
- 1 passes to 3 on the wing (same side as the corner shooter, 4).
- 3 immediately passes back to 1, who has shifted a few steps toward the middle of the court.
- Simultaneously, 2 slides up from the weak-side wing to create space for 3 to cut through.
- 3 cuts all the way across the court under the high zone defenders to the opposite (weak-side) wing.
- 1 passes to 2, and 2 passes to 3 on the opposite wing.

### Phase 2: Force Defender Commitment and Free the Shooter
- Since X2 was defending 2 at the top, X3 must now close out to defend 3 on the wing to prevent the open shot — this pulls X3 away from the baseline.
- As X3 closes out, 5 screens X5 (the ball-side low zone defender).
- 4 cuts hard and quickly along the baseline to the wide-open ball-side short corner/baseline area.
- 3 passes to 4 for the midrange or three-point shot (catch-and-shoot).

## Key Coaching Points
- "5 must not telegraph the screen" — if X5 reads it early, they fight through before 4 arrives and can contest the shot. [S4, p.38]
- "4 must cut hard and quickly along the baseline" for the catch-and-shoot. Hesitation gives X5 time to recover. [S4, p.38]
- Ensure 4 practices this shot (baseline midrange or corner three) regularly so they're ready for the quick catch-and-shoot opportunity. [S4, p.38]

## Counters
- If X5 fights through the screen early, 4 can reject the cut and look to flash to the mid-post instead.
- If X3 doesn't fully commit to 3, 3 can take the open shot rather than forcing the pass to 4.

## Related Plays
- [[23-flare]] — similar zone-overload principle using ball movement to free a shooter
- [[play-baseline-swing]] — this play
- [[blob-belmont-flash]] — zone BLOB using similar baseline-cut concepts
- [[play-pick-overload]] — another 2-3 zone play exploiting the low defender's rotation responsibility

## Sources
- [S4, pp.37-38] — full play description with diagrams
