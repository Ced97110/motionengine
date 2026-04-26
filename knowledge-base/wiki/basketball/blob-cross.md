---
type: play
category: out-of-bounds
formation: 1-4-high
tags: [BLOB, zone, 2-3-zone, cross, youth, simple, inbounds, corner-three]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: inbound-pass-read
    role: "1"
    criticality: required
  - id: corner-cut-spacing
    role: "2"
    criticality: required
  - id: corner-cut-spacing
    role: "3"
    criticality: required
  - id: post-cross-cut
    role: "4"
    criticality: required
  - id: post-cross-cut
    role: "5"
    criticality: required
  - id: catch-and-shoot-corner
    role: "2"
    criticality: optional
  - id: catch-and-shoot-corner
    role: "3"
    criticality: optional
  - id: block-catch-and-finish
    role: "4"
    criticality: optional
  - id: sprint-back-transition-defense
    role: "2"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: post-cross-cut
    for_role: "4"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: post-cross-cut
    for_role: "5"
  - region: ankle_complex
    criticality: required
    supports_technique: corner-cut-spacing
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: corner-cut-spacing
    for_role: "3"
  - region: glute_max
    criticality: optional
    supports_technique: block-catch-and-finish
    for_role: "4"
  - region: core_outer
    criticality: optional
    supports_technique: inbound-pass-read
    for_role: "1"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The crossing post action and corner spacing force 3 zone defenders to cover 4 receivers, consistently freeing either a corner three or a low-block finish — both high-efficiency shot types."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The inbounder reads a predetermined two-option hierarchy (corner then block), capping decision complexity and limiting risky passes to a single direct delivery."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "By design the play terminates in a corner three or an uncontested low-block catch-and-finish, both of which carry above-average points-per-possession relative to contested mid-range alternatives."
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When both corner receivers are blanketed by zone defenders, the crossing post players arriving at the opposite low blocks should find themselves unguarded due to defensive overcommitment."
    extraction: llm-inferred
  - text: "When the low-block post players are picked up by zone defenders rotating inside, the corner shooters are left open because the bottom defenders have abandoned their perimeter coverage."
    extraction: llm-inferred
---

# BLOB: Cross (vs 2-3 Zone)

## Overview
Cross is a simple, highly effective baseline out-of-bounds play specifically recommended for youth basketball teams. From a 1-4 high formation, wing players draw the zone's bottom defenders wide to the corners while the two post players cross to the opposite low blocks — forcing 3 zone defenders to cover 4 offensive players. The in-bounder reads the defense and passes to the open player. [S4, pp.9-10]

## Formation
**1-4 High.** Post players (**4** and **5**) at the elbows (high posts); best shooters (**2** and **3**) on the wings. **1** (best decision-maker) is the in-bounder out of bounds on the baseline.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":47},{"role":"2","x":-18,"y":29},{"role":"3","x":18,"y":29},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"actions":[{"from":"2","to":"left_corner","type":"cut"},{"from":"3","to":"right_corner","type":"cut"},{"from":"4","to":"right low block","type":"cut"},{"from":"5","to":"left low block","type":"cut"}],"notes":"This is the initial (Phase 1) diagram from p.9. The play is a baseline out-of-bounds (BLOB) in a 1-4 high formation: 1 is the out-of-bounds inbounder at the baseline center, 4 and 5 are at the left and right elbows respectively, and 2 and 3 are on the left and right wings. The diagram also shows the subsequent action arrows: 2 and 3 cutting to their respective corners, and 4 and 5 crossing to opposite low blocks. Defenders x1–x5 are also depicted in the diagram but are not mapped here as only offensive positions were requested. The second diagram on the same page shows the Phase 2 state after cuts have been made."}
```

## Phases

### Phase 1: Corner Cuts (Draw the Bottom Defenders)
- **2** and **3** simultaneously cut to their respective corners (away from their starting wings), calling loudly for the basketball.
- This deliberate movement and vocal demand draws both bottom wing zone defenders out toward the corners.

### Phase 2: Post Cross
- **4** and **5** wait a beat, then cross paths and cut to the **opposite** low blocks (4 goes to 5's side, 5 goes to 4's side).
- Because the zone's bottom defenders have been pulled to the corners, the crossing post players should arrive at the blocks unguarded.

### Phase 3: Read and Pass
- **1** reads where all defenders have moved and delivers the inbound pass to the open player:
  - Corner **2** or **3** for the three-point shot, OR
  - Block **4** or **5** for the catch and finish.

## Key Coaching Points
- If a shooter receives the pass and takes the shot, the **opposite corner player must immediately sprint back on defense** to prevent the opponent's fast break. [S4, p.10]
- Advise **1** to look at the player cutting to the **opposite** corner first — the ball-side bottom defender will almost always deny the near corner, so the weak-side defender must be moved before the post players can get open. [S4, p.10]
- **All four players must call loudly for the ball** — the noise and movement draws defenders and creates uncertainty.
- **1** must not give away the target with their eyes. Keep a wide visual field and mask the pass direction. [S4, p.10]
- Effective precisely because it is simple — players at any level can learn and execute it.

## Counters
- **If both corners are covered**: Post players crossing to the blocks should be open due to defender overcommitment to the corners.
- **If blocks are defended**: The corner shooters should be open because the bottom defenders moved to cover the posts.

## Related Plays
- [[blob-box-flash]] — more complex BLOB 2-3 zone option for experienced teams
- [[blob-belmont-flash]] — BLOB 2-3 zone play with flash action
- [[play-selection-principles]] — author recommends this type of simple play for youth teams

## Sources
- [S4, pp.9-10]
