---
type: play
category: out-of-bounds
formation: box
tags: [SLOB, man-to-man, backdoor, three-point, box-set, screen-the-screener, quick-hitter]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: down-screen-pop
    role: "4"
    criticality: required
  - id: inbound-pass-entry
    role: "3"
    criticality: required
  - id: quick-decision-pass
    role: "1"
    criticality: required
  - id: screen-the-screener-cut
    role: "5"
    criticality: required
  - id: backdoor-cut-finish
    role: "3"
    criticality: required
  - id: catch-and-shoot-three
    role: "2"
    criticality: optional
  - id: safety-valve-flash
    role: "4"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: backdoor-cut-finish
    for_role: "3"
  - region: ankle_complex
    criticality: required
    supports_technique: backdoor-cut-finish
    for_role: "3"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: screen-the-screener-cut
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: quick-decision-pass
    for_role: "1"
---

# Deception (SLOB)

## Overview
A SLOB play from a modified box set that simultaneously creates an open layup for the inbounder cutting backdoor AND a three-point opportunity for the best shooter. Designed as a surprise play — save for when you really need a basket. [S4, pp.85-86]

## Formation
Box formation with the **three-point shooter (2)** on the weak side **outside** the three-point line (not inside the box), **1 (PG)** and **5** on the strong-side, **4** at the elbow area. **3 (inbounder)** passes from the sideline. [S4, p.85]

```json name=diagram-positions
{"players":[{"role":"OB","x":-28,"y":35},{"role":"1","x":-5,"y":33},{"role":"4","x":-3,"y":38},{"role":"5","x":7,"y":38},{"role":"2","x":22,"y":28}],"actions":[{"from":"4","to":"1","type":"screen"},{"from":"OB","to":"1","type":"pass"},{"from":"1","to":"top_of_key","type":"cut"}],"notes":"This is the initial (Phase 1) diagram from p.85. The play is a SLOB from the left sideline. 3 is the inbounder (OB) on the left sideline around the elbow/mid-post area. 1 starts near the strong-side elbow area, with 4 just below setting a down screen. 5 is on the strong-side low block area. 2 (the shooter) is stationed wide on the weak-side right wing, outside the three-point line. The first diagram shows 4 screening down for 1, who cuts to the top of the key to receive the inbound pass from 3 (OB). The \"top_of_key\" destination for the cut approximates y≈24, x≈0."}
```

## Phases

### Phase 1: Getting the Ball Inbounds
- 4 sets a down screen for 1, who pops to the top of the key.
- 1 receives the inbound pass from 3. [S4, p.85]

### Phase 2: Two-Pronged Attack
- **Shooter action:** As soon as the pass to 1 is made, 5 sprints toward 2's defender and sets a strong screen. 2 cuts to the top of the key looking to receive the pass from 1 for a three-point shot. [S4, p.85]
- **Backdoor action:** On the other side, 3 (the inbounder) takes a few steps toward the basketball to set their defender up, then receives a screen from 4. 3 cuts hard backdoor toward the basket, looking to receive the pass from 1 for an easy layup. [S4, p.85]

### Phase 3: Decision Point
- 1 quickly evaluates both options and makes the correct pass — either to 2 at the top for three, or to 3 cutting backdoor for the layup. [S4, p.85]

## Key Coaching Points
- "It's incredibly important that 3 sets their defender up and doesn't give away that they're going to be cutting backdoor." [S4, p.86]
- "Since this play is designed to catch the defense off-guard, save it for when you really need a basket!" [S4, p.86]
- "5 must wait until 1 makes the catch or 2 will be cutting to the top of the key too early." [S4, p.86]
- 1 must be a good decision maker and passer — the play lives and dies by the read.
- 3 must be able to finish at the rim after the backdoor cut.

## Counters
- If both 2 and 3 are denied, 4 (after screening for 1) can flash to the elbow as a safety valve.

## Related Plays
- [[play-box-loop-post]] — SLOB box set with sequential screening
- [[play-box-spin]] — SLOB box quick hitter with dual scoring options
- [[play-diamond-slob]] — SLOB box with multiple reads including flare screen

## Sources
- [S4, pp.85-86] — full play description and coaching points
