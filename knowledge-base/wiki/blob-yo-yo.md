---
type: play
category: out-of-bounds
formation: box
tags: [BLOB, man-to-man, up-screen, post, layup, box, rim-attack]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: up-screen-set
    role: "2"
    criticality: required
  - id: up-screen-set
    role: "3"
    criticality: required
  - id: basket-cut-off-screen
    role: "4"
    criticality: required
  - id: basket-cut-off-screen
    role: "5"
    criticality: required
  - id: inbound-read-and-pass
    role: "1"
    criticality: required
  - id: safety-valve-cut-to-wing
    role: "3"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: basket-cut-off-screen
    for_role: "4"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: basket-cut-off-screen
    for_role: "5"
  - region: glute_max
    criticality: required
    supports_technique: basket-cut-off-screen
    for_role: "4"
  - region: glute_max
    criticality: required
    supports_technique: basket-cut-off-screen
    for_role: "5"
  - region: ankle_complex
    criticality: required
    supports_technique: up-screen-set
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: up-screen-set
    for_role: "3"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "Dual up-screens simultaneously free two post players for direct basket cuts, targeting high-percentage layup attempts at the rim by design."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The inbounder makes a single decisive pass to a predetermined cutter, keeping the sequence to one pass and minimizing exposed ball-handling time."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "Two simultaneous rim cuts from a box formation create layup opportunities on nearly every possession, maximizing expected points per trip."
---

# Yo-Yo (BLOB vs Man-to-Man)

## Overview
A simple, effective BLOB play from a box formation. Both guards simultaneously step up and set screens for both post players, who cut to the basket for layups. The point guard reads which post is open and delivers the pass. [S4, pp.30-31]

## Formation
- **1** (best passer): inbounder at baseline
- **2** and **3** (guards): low blocks
- **4** and **5** (posts/best rim-finishers): elbows

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":47},{"role":"2","x":7,"y":40},{"role":"3","x":-7,"y":40},{"role":"4","x":8,"y":29},{"role":"5","x":-8,"y":29}],"actions":[{"from":"3","to":"5","type":"screen"},{"from":"2","to":"4","type":"screen"},{"from":"5","to":"rim","type":"cut"},{"from":"4","to":"rim","type":"cut"},{"from":"1","to":"rim","type":"pass"}],"notes":"Starting box formation from the first (top) diagram on p.30. 1 is the baseline inbounder; 2 and 3 are on the right and left low blocks respectively; 4 and 5 are on the right and left elbows respectively. The diagram shows 2 and 3 stepping up to set up-screens for 4 and 5, who cut outside their screens toward the rim. 1's pass arrow targets whichever cutter is open (depicted toward the rim). The second diagram on the page shows the Phase 2/safety-valve action and is not extracted here."}
```

## Phases

### Phase 1: Dual Up-Screens
- **2 and 3** simultaneously step up from the low blocks and set **up-screens** for **4 and 5** respectively.
- **Screeners must not face the direction they will screen** when the play starts — they should face each other to disguise the action. [S4, p.31]
- Screeners must actively **seek out the defenders** and commit to the screen. [S4, p.31]

### Phase 2: Post Players Cut to Basket
- **4 and 5** both immediately cut to the **outside of their respective screens** and **explode to the basket**.
- **4 and 5 must stay to their own sides** to prevent defenders from being able to deflect passes to both players with one move. [S4, p.31]

### Phase 3: Inbounder Reads and Passes
- **1 reads the defense** and delivers the pass to whichever of 4 or 5 is open for the finish.

### Phase 4: Safety Valve
- If neither 4 nor 5 is available, **3 cuts to the wing** to receive the pass for a midrange shot or to bring the ball out and set up the half-court offense. [S4, p.30]

## Key Coaching Points
- **Screeners must not telegraph direction** at the start — facing each other prevents defensive reads. [S4, p.31]
- **Screeners must commit fully** to finding and setting a strong screen — it is the only job of the screener in this play. [S4, p.31]
- **Post players must stay separated** on their side of the lane — converging makes it easy for one defender to intercept both passing lanes. [S4, p.31]

## Counters
- If both post cuts are denied → 3 flares to the wing for a midrange shot or reset pass.

## Related Plays
- [[blob-flip]] — also uses cross screen for two post players in a box formation
- [[blob-two-inside]] — screen-the-screener BLOB targeting post players
- [[blob-box-gate]] — box BLOB with back screen then gate screen for shooter

## Sources
- [S4, pp.30-31] — full play description and coaching points
