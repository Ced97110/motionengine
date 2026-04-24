---
type: play
category: out-of-bounds
formation: box
tags: [BLOB, man-to-man, back-screen, gate-screen, cross-screen, catch-and-shoot, post-up, layup]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: back-screen-set
    role: "2"
    criticality: required
  - id: basket-cut-off-screen
    role: "5"
    criticality: required
  - id: gate-screen-usage
    role: "2"
    criticality: required
  - id: catch-and-shoot-wing
    role: "2"
    criticality: required
  - id: cross-screen-set
    role: "1"
    criticality: required
  - id: post-entry-duck-in
    role: "5"
    criticality: optional
  - id: gate-screen-set
    role: "3"
    criticality: optional
  - id: gate-screen-set
    role: "4"
    criticality: optional
demands_anatomy:
  - region: ankle_complex
    criticality: required
    supports_technique: basket-cut-off-screen
    for_role: "5"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: basket-cut-off-screen
    for_role: "5"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: gate-screen-usage
    for_role: "2"
  - region: ankle_complex
    criticality: optional
    supports_technique: catch-and-shoot-wing
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: cross-screen-set
    for_role: "1"
  - region: glute_max
    criticality: optional
    supports_technique: post-entry-duck-in
    for_role: "5"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "Three sequential reads — rim cut off back screen, catch-and-shoot wing, and post duck-in — all target high-efficiency shot types (layup or open 3), eliminating mid-range attempts by design."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Role 5's hard basket cut off the back screen and subsequent post-up duck-in both invite body contact from the help defender in a confined paint area."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The play is a scripted BLOB sequence with pre-assigned reads in strict phase order, limiting live decision-making and keeping the pass count low against an organized man-to-man defense."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Cascading screen actions force the defense into sequential rotations, ensuring at least one of the three reads yields an uncontested shot or layup on nearly every possession."
---

# Box Gate (BLOB vs Man-to-Man)

## Overview
Starting from a box formation, this BLOB play creates three sequential scoring opportunities: a quick layup for the center off a back screen, a catch-and-shoot wing shot for the best shooter off a gate screen, and finally a post-up for the center. Designed so that the inbounder (PG) handles the cross screen, leaving a smaller defender to guard the post. [S4, pp.21-22]

## Formation
- **1** (PG): inbounder on the baseline
- **2** (best shooter): weak-side low block
- **3**: ball-side elbow (high post)
- **4**: weak-side elbow (high post)
- **5** (best post-up player): ball-side low block / weak-side elbow area

```json name=diagram-positions
{"players":[{"role":"OB","x":8,"y":47},{"role":"2","x":-7,"y":40},{"role":"5","x":7,"y":40},{"role":"3","x":8,"y":29},{"role":"4","x":-8,"y":29}],"actions":[{"from":"OB","to":"2","type":"pass"},{"from":"2","to":"rim","type":"screen"},{"from":"5","to":"rim","type":"cut"}],"notes":"The first (top) diagram on p.21 shows the starting box formation with 1 as the out-of-bounds inbounder on the ball-side baseline, 2 on the weak-side low block, 5 on the ball-side low block, 3 at the ball-side elbow, and 4 at the weak-side elbow. The depicted action in Phase 1 shows 1 passing (dashed line) toward 2/5 area, 2 setting a back screen, and 5 cutting to the rim. The second diagram shows Phase 2 (gate screen) and is not extracted here per instructions."}
```

## Phases

### Phase 1: Back Screen for Center
- **2** sets a **back screen** for **5**, who cuts hard to the rim looking for the inbound pass from **1**.
- **3** must wait — they cannot move too early or the defense will read the play. They begin drifting up the side of the key as 2 sets the screen.

### Phase 2: Gate Screen for Shooter
- Immediately after setting the back screen for 5, **2 sprints through a gate screen** formed by **3** and **4** on the wing.
- **2** catches the inbound pass (or a quick re-entry pass) for a **catch-and-shoot on the wing**.
- After screening, **3 and 4 clear out to the top of the key**.
- **3 must wait until 2 is ready to sprint** off the gate screen — they should arrive at the same time. [S4, p.22]

### Phase 3: Cross Screen — Post Up
- **1** steps inbounds after passing and sets a **cross screen** for **5**.
- **5** reads the screen and either **ducks in for the quick pass** or posts up on the ball-side low block.
- The reason **1** (the PG) inbounds is so that the help defender on the cross screen is a smaller player, giving **5** a size advantage. [S4, p.22]

## Key Coaching Points
- **Pass to 2's inside shoulder** — a pass to the outside shoulder is very difficult to catch and shoot. [S4, p.22]
- **3 must time their movement** — arriving at the gate screen simultaneously with 2's sprint creates maximum confusion for the defense.
- **1 should be the PG (inbounder)** specifically so the help defender on the final cross screen is small. [S4, p.22]

## Counters
- If 5 is open on the initial back screen → 1 throws directly to 5 for the layup.
- If 2 is denied on the wing → 1 can look for 5 sealing on the cross screen.

## Related Plays
- [[blob-4-low-flex]] — 4-low formation BLOB with flex screen
- [[blob-flip]] — box formation BLOB with cross screen at top for two post finishers
- [[blob-box-gate]] — this play

## Sources
- [S4, pp.21-22] — full play description and coaching points
