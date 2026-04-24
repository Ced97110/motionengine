---
type: play
category: out-of-bounds
formation: box
tags: [SLOB, man-to-man, flare-screen, pick-and-roll, curl-cut, box-set, multi-option]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: down-screen-read
    role: "1"
    criticality: required
  - id: catch-and-pass-off-screen
    role: "1"
    criticality: required
  - id: flare-screen-set
    role: "5"
    criticality: required
  - id: flare-cut-to-wing
    role: "1"
    criticality: required
  - id: pick-and-roll-ball-handler
    role: "2"
    criticality: required
  - id: curl-cut-off-screen
    role: "3"
    criticality: optional
  - id: roll-or-pop-read
    role: "5"
    criticality: optional
  - id: skip-pass
    role: "2"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: flare-cut-to-wing
    for_role: "1"
  - region: ankle_complex
    criticality: required
    supports_technique: pick-and-roll-ball-handler
    for_role: "2"
  - region: glute_max
    criticality: required
    supports_technique: pick-and-roll-ball-handler
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: curl-cut-off-screen
    for_role: "3"
  - region: hip_flexor_complex
    criticality: optional
    supports_technique: roll-or-pop-read
    for_role: "5"
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When D5 switches onto 2 on the on-ball screen, 5 immediately rolls to the rim or pops to an open area depending on which defender is now guarding them."
    extraction: llm-inferred
  - text: "When 1's flare cut to the wing is taken away by the defense, 2 skips the skip-pass look and goes directly into the pick-and-roll action with 5."
    extraction: llm-inferred
  - text: "When 3's baseline curl off the screen comes open early in the sequence, 1 delivers an immediate skip pass to 3 for a scoring opportunity before the later PnR action develops."
    extraction: llm-inferred
---

# Diamond (SLOB)

## Overview
A multi-option SLOB play from a box formation providing numerous scoring opportunities: a curl off a screen, a flare screen for a three-point shooter, and a pick-and-roll at the top of the key. Best suited for teams with an elite playmaker surrounded by shooters. [S4, pp.87-88]

## Formation
Box set: **1 (3-pt shooter)** and **2 (best playmaker/guards)** at the low blocks, **4** and **5** at the elbows. **3 (small forward)** inbounds from the sideline. [S4, p.87]

```json name=diagram-positions
{"players":[{"role":"3","x":-25,"y":29},{"role":"1","x":-7,"y":40},{"role":"2","x":7,"y":40},{"role":"5","x":-8,"y":29},{"role":"4","x":8,"y":29}],"actions":[{"from":"5","to":"1","type":"screen"},{"from":"1","to":"top_key","type":"cut"},{"from":"3","to":"1","type":"pass"}],"notes":"This is the SLOB box formation starting position extracted from the first (top) diagram on p.87. 3 inbounds from the left sideline near the elbow extended. 1 and 2 are on the left and right low blocks respectively. 5 and 4 are at the left and right elbows. The first diagram shows 5 setting a down screen for 1 cutting to the top of the key, with 3 making the inbound pass. Actions shown reflect Phase 1 only (the initial formation and first movement arrows)."}
```

## Phases

### Phase 1: Initial Ball Movement
- 5 sets a down screen for 1, who cuts to the top of the key and receives the inbound pass from 3.
- On the catch, 4 sets a down screen for 2, who pops out to the wing and receives the pass from 1. [S4, p.87]

### Phase 2: Inbounder Cut and Flare
- 3 (inbounder) cuts along the baseline using a screen from 4 — 3 can either pop out to the three-point line or **curl around the screen** looking to receive the pass for a shot.
- As 2 dribbles, 5 sets a **flare screen** for 1, who cuts to the wing looking to receive a **skip pass** from 2 for an open shot. [S4, p.87]

### Phase 3: Pick-and-Roll Finish
- If the skip pass to 1 isn't available, 5 sets an **on-ball screen** for 2.
- 2 uses the screen and attacks the rim. Main scoring options:
  - Shoot off the PnR
  - Pass to 4 (who has rolled or popped)
  - Kick out to 1 on the wing [S4, p.87]

## Key Coaching Points
- "2 has the biggest responsibility in this play and must be able to make great passes and also be able to attack the ring. Great play for teams with a great player surrounded by shooters." [S4, p.88]
- "1 must not give away that a flare screen is about to be set. When it is, they quickly cut to the wing looking to receive the skip pass." [S4, p.88]
- "The coach must decide whether they want 5 rolling to the rim or backing out and playing safety after setting the on-ball screen." [S4, p.88]
- Coach's pre-game decision: roll or pop for 5 based on matchups.

## Counters
- If defense switches the on-ball screen → 5 rolls or pops to open area depending on who is guarding them.
- If 1's flare is denied → proceed directly to PnR with 2 and 5.
- If 3's baseline curl is open early → 1 skips immediately to 3 before the later action.

## Related Plays
- [[play-deception-slob]] — SLOB box play with multiple simultaneous options
- [[play-prowl-slob]] — SLOB box play flowing into pick-and-roll
- [[23-flare]] — set play using flare screen for open three
- [[concept-reading-screens-off-ball]] — how 1 and 3 read their defenders off screens

## Sources
- [S4, pp.87-88] — full play description and coaching points
