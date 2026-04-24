---
type: play
category: out-of-bounds
formation: 4-low
tags: [BLOB, man-to-man, flex-screen, pin-down, screen-the-screener, layup, catch-and-shoot]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: inbound-lob-pass
    role: "1"
    criticality: required
  - id: catch-and-relay-pass
    role: "4"
    criticality: required
  - id: flex-screen-set
    role: "2"
    criticality: required
  - id: flex-cut-to-block
    role: "5"
    criticality: required
  - id: pin-down-screen-set
    role: "4"
    criticality: required
  - id: catch-and-shoot-off-screen
    role: "2"
    criticality: required
  - id: pass-read-dual-option
    role: "3"
    criticality: required
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: flex-cut-to-block
    for_role: "5"
  - region: glute_max
    criticality: required
    supports_technique: flex-cut-to-block
    for_role: "5"
  - region: ankle_complex
    criticality: required
    supports_technique: catch-and-shoot-off-screen
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: flex-screen-set
    for_role: "2"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The play generates two high-percentage looks by design — a flex-cut layup at the block and a catch-and-shoot at the top of the key — eliminating mid-range attempts entirely."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The scripted sequence routes the ball through a fixed relay chain (1→4→3→5 or 2) capping live-ball decisions to a single read by 3, which limits the turnover surface compared to open motion."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: low
    rationale: "Role 5's flex cut to the block creates a contact-prone finish opportunity in traffic, drawing foul calls when defenders chase through the screen to contest."
---

# 4-Low Flex (BLOB vs Man-to-Man)

## Overview
From a 4-low baseline out-of-bounds formation, the ball is quickly passed to the top of the key and the play uses a flex screen followed by a screen-the-screener (pin-down) action. Two distinct scoring opportunities are created: an open layup via the flex cut and a catch-and-shoot from the top of the key. [S4, p.20]

## Formation
Four players (2, 4, 5, 3) are positioned low across the paint in a 4-low set, with the bigs (4 and 5) on the ball-side. Player 1 inbounds from the baseline.

```json name=diagram-positions
{"players":[{"role":"1","x":22,"y":47},{"role":"2","x":10,"y":42},{"role":"3","x":7,"y":40},{"role":"4","x":-7,"y":40},{"role":"5","x":-22,"y":40}],"actions":[{"from":"4","to":"top_key","type":"cut"},{"from":"1","to":"4","type":"pass"}],"notes":"This is the starting (Phase 1) formation from the first diagram on p.20. 1 inbounds from the right baseline; 2 and 3 are on the right side of the lane (ball-side), 4 and 5 on the left side. The first diagram shows 4 cutting to the top of the key to receive the inbound lob from 1. The \"top_key\" destination approximates (0, 24). The second diagram on the same page shows later phases (flex screen and pin-down) and is not extracted here."}
```

## Phases

### Phase 1: Ball to Top of Key
- **4** cuts to the top of the key and receives the inbound lob pass from **1**.
- **3** waits an extra beat (timing is critical), then cuts to the top of the key and receives the pass from **4**.

### Phase 2: Flex Screen for 5
- **2** steps inbounds and sets a **flex screen** across the lane for **5**.
- **5** uses the flex cut, attacking the ball-side block, looking for the pass from **3** and the open layup.

### Phase 3: Screen-the-Screener (Pin Down) for 2
- Immediately after 2 sets the flex screen, **4** sets a **pin down screen** for **2** (screen-the-screener action).
- **2** cuts off the pin down to the top of the key, looking for a **catch-and-shoot** from the pass by **3**.

## Key Coaching Points
- **3 must be a smart decision-maker** — they must hit the open player (5 on the flex or 2 off the pin down) at the right time and on target. [S4, p.20]
- **Every player must set strong screens** — weak screens will allow defenders to recover and take away both options. [S4, p.20]
- **Key personnel**: best shooter should inbound (1); best post player should start outside the three-point line on ball-side.

## Counters
- If 5 is denied on the flex cut → 3 is patient and looks for 2 coming off the pin down.
- If both options are covered → 3 brings the ball back out to reset the half-court offense.

## Related Plays
- [[blob-stack-zone]] — stack BLOB vs 2-3 zone
- [[blob-box-gate]] — box formation BLOB with back screen and gate screen
- [[blob-yo-yo]] — box BLOB using dual up-screens for post layups

## Sources
- [S4, p.20] — full play description and coaching points
