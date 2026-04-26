---
type: play
category: out-of-bounds
formation: box
tags: [BLOB, zone, 2-3-zone, corner-three, back-screen, double-screen, overload, inbounds]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: inbound-pass-entry
    role: "2"
    criticality: required
  - id: sprint-to-wing-on-signal
    role: "5"
    criticality: required
  - id: double-screen-set
    role: "3"
    criticality: required
  - id: double-screen-set
    role: "4"
    criticality: required
  - id: curl-off-double-screen
    role: "2"
    criticality: required
  - id: back-screen-set
    role: "4"
    criticality: optional
  - id: backdoor-cut
    role: "5"
    criticality: optional
  - id: high-post-read-and-attack
    role: "3"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: curl-off-double-screen
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: sprint-to-wing-on-signal
    for_role: "5"
  - region: ankle_complex
    criticality: optional
    supports_technique: backdoor-cut
    for_role: "5"
  - region: core_outer
    criticality: optional
    supports_technique: double-screen-set
    for_role: "4"
  - region: glute_max
    criticality: optional
    supports_technique: high-post-read-and-attack
    for_role: "3"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The primary action delivers the best shooter a catch-and-shoot corner three off a double screen, while secondary options include a backdoor layup — both among the highest-efficiency shot types by design."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: low
    rationale: "Role 5's backdoor cut and role 3's rim attack from the high post both route players into the paint where contact fouls are possible, though these are secondary reads."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The scripted two-pass entry sequence (inbound to 5, then to 1) and predetermined reads cap the number of live-ball decisions, limiting turnovers relative to a free-flowing zone offense."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Multiple high-value shot options (corner three, backdoor layup, wing three) are built into the same set, ensuring at least one quality look regardless of how the zone rotates."
---

# BLOB: Box Flash (vs 2-3 Zone)

## Overview
Box Flash is a 2-3 zone BLOB play that starts from a standard box formation and overloads one side of the zone, forcing the defense to choose whom to guard. It offers multiple scoring options: a corner shot for the best shooter, a backdoor layup, or a wing three-point shot — making it suitable for teams of all levels. [S4, pp.7-8]

## Formation
**Standard Box.** Post players (**4** and **5**) on the two low blocks; guards (**1** and **3**) on the two elbows. **2** (best shooter) is the in-bounder out of bounds on the baseline.

```json name=diagram-positions
{"players":[{"role":"2","x":0,"y":-1},{"role":"1","x":-8,"y":29},{"role":"3","x":8,"y":29},{"role":"5","x":-7,"y":40},{"role":"4","x":7,"y":40}],"actions":[],"notes":"This is the initial box formation (Setup / Phase 1 start). 2 is the out-of-bounds inbounder at the top of the baseline (depicted above the half-court diagram, near the center out-of-bounds position). 1 and 3 are on the two elbows; 4 and 5 are on the two low blocks. No action arrows are extracted here as this represents the starting formation before any movement. The first diagram on p.7 shows the initial entry: 5 sprinting to the wing and 2 passing in, but the marker calls for the standard box starting formation."}
```

## Phases

### Phase 1: Initial Entry & Zone Shift
- **5** sprints up to the wing; **2** inbounds to **5**.
- **1** pops high to the slot (top of key area).
- **3** moves down to the low block to join **4** — they will set a double screen together.

### Phase 2: In-Bounder Repositions
- **2** steps onto the court and takes up position in the ball-side short corner.
- **5** passes to **1** at the top of the key.

### Phase 3: Primary Action — Corner Shot
- **2** sprints off the double screen set by **3** and **4** on the block, arriving at the ball-side corner.
- **1** dribbles toward the top of the key to improve the passing angle, then passes to **2** in the corner for the open shot. [S4, p.8]

### Phase 4: Secondary Options (if 2 is covered)
- **3** flashes to the high post; **1** passes to **3**.
- **4** sets a back screen on the bottom wing defender; **5** sprints backdoor for the open layup pass from **3**.
- **4** pops to the wing after the back screen — open for a three-point shot depending on how **x4** plays it.
- If **3** has a speed mismatch vs. **x5**, **3** can attack the rim directly from the high post. [S4, p.8]

## Key Coaching Points
- **1**'s pass to **2** in the corner must be on-time and on-target. Practice this pass repeatedly. [S4, p.8]
- Put your best playmaker at **position 3** — the decision from the high post determines whether the team gets an open shot/layup.
- Teach players to read defensive positioning and know which option opens based on how they're guarded.
- **4** must set a solid back screen AND be shot-ready when popping afterward. [S4, p.8]
- Described as a "great play for teams of all levels" due to multiple clear options. [S4, p.7]

## Counters
- **If 2 is denied in the corner**: 3 flashes high post → 4 back screens → 5 backdoor.
- **If 5 is denied backdoor**: 4 pops to the wing off the back screen for an open three.
- **If x5 is slower than 3**: 3 attacks the rim from the high post.

## Related Plays
- [[blob-belmont-flash]] — BLOB 2-3 zone play also using a box/wide-box set
- [[blob-cross]] — simpler BLOB zone play recommended for youth teams
- [[blob-hawk]] — BLOB 2-3 zone quick-hitter with similar corner-shot objective

## Sources
- [S4, pp.7-8]
