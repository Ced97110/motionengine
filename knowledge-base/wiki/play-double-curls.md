---
type: play
category: offense
formation: 1-4-high
tags: [high-post-cut, staggered-screen, curl-cut, pick-and-roll, layup, half-court]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: high-post-cut-off-screen
    role: "1"
    criticality: required
  - id: curl-cut-to-rim
    role: "2"
    criticality: required
  - id: staggered-screen-set
    role: "4"
    criticality: required
  - id: pick-and-roll-ball-handler
    role: "3"
    criticality: required
  - id: pick-and-roll-screen-set
    role: "5"
    criticality: required
  - id: slip-screen-to-rim
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: high-post-cut-off-screen
    for_role: "1"
  - region: ankle_complex
    criticality: required
    supports_technique: curl-cut-to-rim
    for_role: "2"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: pick-and-roll-ball-handler
    for_role: "3"
  - region: core_outer
    criticality: optional
    supports_technique: staggered-screen-set
    for_role: "4"
  - region: glute_max
    criticality: optional
    supports_technique: pick-and-roll-screen-set
    for_role: "5"
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When x5 jumps the High-Post screen early, 5 slips straight to the rim for a direct pass and easy finish before the defense can recover."
    extraction: llm-inferred
  - text: "When 3's defender and x5 switch on the pick-and-roll, 5 seals the smaller switched defender in the post and calls for a feed."
    extraction: llm-inferred
  - text: "When 3 is stopped driving off the pick-and-roll, 1 and 2 waiting in the corners serve as pressure-release kick-out targets for open perimeter shots."
    extraction: llm-inferred
---

# High-Post Double Curls

## Overview
A 1-4 high half-court play that sequences two curl-to-rim cuts (a High-Post cut and a staggered-screen curl) before flowing into a traditional wing pick-and-roll. By using both post players as screeners for the first two options and then popping one out to set the PnR, the play keeps post defenders out of the paint during the PnR phase — leaving only the defensive point guard in the lane. [S4, pp.72-73]

## Formation
1-4 high: 1 at the top with the ball, 4 and 5 on the elbows, 2 on the left wing, 3 on the right wing. [S4, p.72]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":18},{"role":"2","x":-18,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"actions":[{"from":"1","to":"3","type":"pass"}],"notes":"Extracting the initial/starting formation from the first (top) diagram on p.72, which shows the 1-4 high setup. 1 is at the top with the ball, 4 and 5 are on the elbows, 2 is on the left wing, and 3 is on the right wing. The first visible action arrow is 1 passing to 3 on the right wing (shown as a dashed arrow). The high-post basket cut by 1 off 5's screen and subsequent actions belong to Phases 2 and 3 (second and third diagrams)."}
```

## Phases

### Phase 1: Wing Entry & High-Post Cut
- 1 passes to 3 on the wing.
- 1 immediately makes a High-Post cut off 5's screen toward the rim, looking to receive the pass from 3 for an open layup.
- If not open, 1 clears to the weak-side corner. [S4, p.72]

### Phase 2: Staggered Screen — Second Curl
- 4 and 5 set a staggered screen for 2 who curls toward the rim, looking for the pass from 3 for an open layup.
- If 2 does not receive the pass, 2 clears to the ball-side corner.
- 4 pops out to the top of the key after screening to create space. [S4, p.72]

### Phase 3: Wing Pick-and-Roll
- 5 sets a pick-and-roll for 3, who attacks the rim hard looking to score or create a play for a teammate.
- Because both 4 and 5 were used as screeners (keeping them out of the paint), the only inside defender in the PnR phase is the defensive point guard. [S4, p.72-73]

## Key Coaching Points
- This play is effective because it **clears post defenders from the paint** before the PnR, leaving 3 with a much more open lane. [S4, p.73]
- Players curling to the rim must **lead with a target hand** and call for the ball if they are open. [S4, p.73]
- No specific skill-set required — this play works for any personnel. The wing receiver (3) should be able to attack and make good decisions out of the PnR. [S4, p.72]
- The staggered screen timing is key — 2 must use the screens at full speed to create separation.

## Key Personnel
- **1 (PG)**: Makes the High-Post cut off 5's screen; clears if not open.
- **2 (SG)**: Curls to the rim off the staggered screen; clears to ball-side corner if not open.
- **3 (SF / Wing)**: Entry receiver; reads 1 and 2 on their cuts; attacks the PnR as the primary ball-handler in Phase 3.
- **4 (PF)**: Co-screener in the staggered screen; pops to the top after to create space.
- **5 (C)**: Sets the High-Post screen for 1; co-sets the staggered screen for 2; sets the PnR for 3.

## Counters
- If x5 cheats on the High-Post screen, 5 can slip to the rim.
- If the defense switches the PnR, 5 seals for a post feed.
- Corner players (1 and 2) are available as kick-out options if 3 is stopped on the PnR drive.

## Related Plays
- [[play-high-post-double-screen]] — pure High-Post cut play from 1-4 high that uses a double screen for the PG
- [[play-iverson-ram]] — another 1-4 high play using cuts to set up a PnR
- [[concept-setting-screens]] — staggered screen angle and timing principles
- [[concept-reading-screens-off-ball]] — how cutters read their defenders on curl cuts

## Sources
- [S4, pp.72-73]
