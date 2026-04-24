---
type: play
category: offense
formation: box
tags: [cross-screen, double-screen, post-up, catch-and-shoot, half-court]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: dribble-entry-wing
    role: "1"
    criticality: required
  - id: cross-screen-set
    role: "2"
    criticality: required
  - id: post-up-catch-and-hold
    role: "4"
    criticality: required
  - id: parallel-double-screen-set
    role: "3"
    criticality: required
  - id: catch-and-shoot-off-screen
    role: "2"
    criticality: required
  - id: screen-slip-to-basket
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: post-up-catch-and-hold
    for_role: "4"
  - region: glute_max
    criticality: required
    supports_technique: post-up-catch-and-hold
    for_role: "4"
  - region: core_outer
    criticality: required
    supports_technique: cross-screen-set
    for_role: "2"
  - region: ankle_complex
    criticality: optional
    supports_technique: catch-and-shoot-off-screen
    for_role: "2"
---

# Motion Offense Cross-Screen Play

## Overview
A two-action half-court play combining a cross screen to create a post-up and a parallel double screen to free the best perimeter shooter for an open catch-and-shoot. Used by the Motion Offense under the source coach. Attacks man-to-man defense by stressing both the interior and the three-point line simultaneously. [S7, pp.68-69]

## Formation
- **1 (PG)**: top of key, will dribble to left wing
- **2 (SG/Shooter)**: left low post
- **5 (C)**: left high post or corner of the free-throw area (left side)
- **4 (PF)**: right low post
- **3 (SF)**: right corner of the free-throw area

## Phases

### Phase 1: PG Dribble Entry + Cross Screen
- 1 dribbles to the **left-wing position** — this is the signal to trigger the action.
- 2 sets a **cross screen** for 4 across the lane.
- 4 cuts into the lane and **posts up** on the left block.
- 1 has an immediate option: **pass to 4 in the post** if he catches clean.

```json name=diagram-positions
{"players":[{"role":"1","x":-14,"y":38},{"role":"2","x":-8,"y":30},{"role":"4","x":8,"y":30},{"role":"5","x":-4,"y":29},{"role":"3","x":8,"y":24}],"actions":[{"from":"1","to":"left_wing","type":"dribble"},{"from":"2","to":"4","type":"screen"},{"from":"4","to":"left_low_block","type":"cut"}],"notes":"Figure 4.53 is the starting formation for Phase 1 of the Cross-Screen Play. The box set has 2 on the left side near the elbow/high post area, 5 near the left elbow of the free-throw line, 4 on the right side near the free-throw corner, and 3 at the right free-throw corner. 1 is dribbling from the bottom-left toward the left wing. 2 is shown making a cross screen for 4, who cuts toward the left low block to post up. Exact positions estimated from the diagram scan."}
```

### Phase 2: Screener Reads + Double Screen Cut
- After setting the cross screen, 2 reads 4's move.
- 2 then cuts **high** off the **parallel double screen** set by 5 and 3 at the free-throw line.
- 1 passes to **2** coming off the double screen for a catch-and-shoot.

```json name=diagram-positions
{"players":[{"role":"1","x":-14,"y":44},{"role":"2","x":0,"y":29},{"role":"4","x":-8,"y":40},{"role":"5","x":-8,"y":29},{"role":"3","x":8,"y":29}],"actions":[{"from":"2","to":"left_low_block","type":"cut"},{"from":"5","to":"2","type":"screen"},{"from":"3","to":"2","type":"screen"},{"from":"1","to":"2","type":"pass"}],"notes":"Figure 4.54 shows Phase 2 of the Cross-Screen Play. 4 has already posted up on the left low block after the cross screen. 2 is shown cutting high off the parallel double screen set by 5 and 3 at the free-throw line (shoulder-to-shoulder). 1 is at the left wing with the ball, passing to 2 coming off the double screen. The starting positions depicted: 1 at left wing (~-14, 44 area, near the baseline-wing), 5 at left elbow area of the free-throw line, 3 at right elbow of the free-throw line, 4 at left low block (already posted up from Phase 1), and 2 beginning the cut high off the 5+3 double screen. 1 passes to 2."}
```

## Key Coaching Points
- 1's dribble to the left wing is the **trigger** — everyone reads this signal.
- 2 must **read 4's move first** before cutting off the double screen — don't rush.
- 5 and 3 set the double screen **shoulder-to-shoulder** parallel to the free-throw line.
- 2 should read his defender: **if defender trails** → curl and cut to basket; **if defender cheats over** → flare for jump shot.
- 1 must keep **court balance** — if the double-screen side is covered, look to 4 in the post.

## Counters
- If 4 gets the post-up entry: standard post-game reads.
- If 2's defender trails on the double screen: 2 curls to the basket for a layup.
- If 2's defender cheats over: 2 flares to the wing for a jump shot.
- If 5's defender hedges on the screen: 5 slips to the basket for a lob from 1.
- If 4's defender helps on 5's slip: 1 lobs to 4.

## Related Plays
- [[play-up-screen]] — same box formation, uses a back screen + down screen instead
- [[play-diagonal-screen]] — same formation using diagonal screen and screen-the-screener
- [[play-pick-and-roll-layered]] — same set using high-post rub cut and side screen
- [[concept-screen-types-reads]] — full framework for cross-screen and double-screen reads

## Sources
- [S7, pp.68-69] — the source coach, Motion Offense
