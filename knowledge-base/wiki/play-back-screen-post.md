---
type: play
category: offense
formation: 3-out-2-in
tags: [man-to-man, back-screen, staggered-screen, post-up, layup, quick-hitter, post-entry]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: staggered-screen-navigation
    role: "1"
    criticality: required
  - id: back-screen-set
    role: "3"
    criticality: required
  - id: basket-cut-off-back-screen
    role: "5"
    criticality: required
  - id: post-entry-pass
    role: "1"
    criticality: required
  - id: deep-post-establishment
    role: "5"
    criticality: optional
  - id: staggered-screen-set
    role: "4"
    criticality: optional
  - id: curl-cut-to-perimeter
    role: "2"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: basket-cut-off-back-screen
    for_role: "5"
  - region: glute_max
    criticality: required
    supports_technique: basket-cut-off-back-screen
    for_role: "5"
  - region: core_outer
    criticality: required
    supports_technique: back-screen-set
    for_role: "3"
  - region: ankle_complex
    criticality: optional
    supports_technique: staggered-screen-navigation
    for_role: "1"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The back screen frees role-5 for a direct basket cut to the rim, and the secondary staggered screen frees the best shooter at the top of the key — both terminal reads are layups or open perimeter shots, eliminating contested mid-range attempts by design."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Role-5 rolling hard to the basket off the back screen draws contact from recovering defenders in the paint, inviting foul opportunities on the finish at the rim."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The set-play structure routes through a single primary decision-maker (role-1) with a clear read hierarchy — post entry or secondary shooter — capping the passing sequence at 1–2 actions and reducing unforced turnover exposure."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "By sequencing a surprise back screen into a simultaneous staggered screen, the play creates two high-value shot opportunities (rim layup or open 3) from a single possession, driving above-average points-per-possession when either read is available."
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When 5's defender reads the back screen early, 3 abandons the screen action and immediately looks for a pass from 1 to attack an open mid-range look."
    extraction: llm-inferred
  - text: "When 2's path through the staggered screen is cut off by denial pressure, either 4 or 3 seizes the opportunity to duck into the paint on their respective sides after completing their screen."
    extraction: llm-inferred
---

# Back Screen Post

## Overview
A man-to-man set play designed to get a quick, open post-up by combining a staggered screen for the point guard with a surprise back screen that frees the post player for a layup or deep block position. If the post is denied, a secondary staggered screen frees the best shooter for a perimeter shot. [S4, pp.54-55]

## Formation
3-out 2-in. 1 (PG) at the top. 2 (best shooter) and 3 in the corners. 4 and 5 on the elbows. [S4, p.54]

```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":35},{"role":"2","x":-22,"y":22},{"role":"3","x":22,"y":42},{"role":"4","x":8,"y":29},{"role":"5","x":-2,"y":29}],"actions":[{"from":"1","to":"5","type":"dribble"},{"from":"4","to":"1","type":"screen"},{"from":"5","to":"1","type":"screen"},{"from":"3","to":"rim","type":"cut"}],"notes":"The first (top) diagram on p.54 shows the initial setup and Phase 1–3 action. 1 is on the left wing area dribbling up toward the top, 2 is in the left corner, 3 is in the right corner (has walked to near the low block area), 4 and 5 are on the elbows setting a staggered screen for 1. A dribble arrow shows 1 coming off the staggered screens (4 and 5). The diagram also shows 3 beginning to sprint up for the back screen. The second diagram (Phase 4) is not extracted per instructions."}
```

## Phases

### Phase 1: Setup — Move Defenders
- 1 dribbles down one side of the floor to create a good screening angle.
- 3 walks their defender down to the **low block** to set up the back screen position. [S4, p.54]
- Start the play with the best shooter (2) on the **same side as the best post player** (5). [S4, p.55]

### Phase 2: Staggered Screen for Point Guard
- 4 and 5 set a **staggered screen** for 1 as 1 dribbles around the top of the key.
- This occupies 4 and 5's defenders and creates a dribble path for 1 to see the full court.

### Phase 3: Surprise Back Screen — Primary Action
- As 1 dribbles off the staggered screens, **3 sprints up and sets a strong back screen** on 5's defender.
- 5 immediately **rolls/cuts to the basket**, looking for the pass from 1 for a quick layup.
- If not immediately open for the layup, 5 **establishes deep post position** on the block. [S4, p.54]
- 1 looks to hit 5 at the rim or in the post.

### Phase 4: Secondary Action — Staggered Screen for Shooter
- If 1 cannot get the ball into the post, **3 and 4 set a staggered screen for 2**, who cuts to the **top of the key** for the open shot. [S4, p.54]
- If 3's defender stays in the key to deter the interior pass, **3 can pop to the top of the key** off a quick screen by 4 for an open shot. [S4, p.55]

## Key Coaching Points
- "Start the play with your best shooter on the same side as the best post player" to maximize both primary and secondary options. [S4, p.55]
- The back screen from 3 must be timed precisely — it happens as 1 is coming off the staggered screens, creating a simultaneous action the defense must process.
- 5 must roll hard and immediately to the basket after the back screen — hesitation allows the defense to recover.
- 1 must read the defense quickly: post or perimeter?

## Counters
- If 5's defender anticipates the back screen, 3 can abort and receive a quick pass from 1 for an open mid-range shot.
- If 2's defender denies the staggered screen, 4 or 3 can duck in on their respective sides after screening.

## Related Plays
- [[play-1-4-quick-floppy]] — another multi-option man-to-man set play
- [[play-swinger]] — man-to-man play using surprise screen element
- [[concept-setting-screens]] — principles for the back screen technique used in this play

## Sources
- [S4, pp.54-55] — full play description with diagrams
