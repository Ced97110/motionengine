---
type: play
category: offense
formation: box
tags: [pick-and-roll, high-post, rub-cut, double-screen, post-up, half-court]
source_count: 1
last_updated: 2026-04-11
---

# Motion Offense Pick-and-Roll Play

## Overview
A multi-action half-court play combining a high-post rub cut, a side screen (pick-and-roll), and a perpendicular double screen on the baseline. the source coach's Motion Offense used this from a two-guards/two-posts box set, creating layered scoring threats that progressively move down the floor. [S7, pp.70-71]

## Formation
- **1 (PG)**: top/left wing area
- **2 (SG)**: will use high-post rub screen, then post up
- **4 (PF)**: left corner of the free-throw area (high post)
- **5 (C)**: right corner of the free-throw area (high post)
- **3 (SF)**: below the free-throw line extended (right side)

## Phases

### Phase 1: High-Post Rub Cut
- 1 dribbles on the **left side**.
- 2 uses 4's **high-post rub screen** at the elbow.
- 2 posts up in the **left low-post area**.
- 1 can pass to **2 in the low post** or continue the play.

```json name=diagram-positions
{"players":[{"role":"1","x":-22,"y":28},{"role":"2","x":-5,"y":38},{"role":"3","x":18,"y":28},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"actions":[{"from":"1","to":"left_wing","type":"dribble"},{"from":"2","to":"left_low_block","type":"cut"},{"from":"4","to":"2","type":"screen"}],"notes":"Figure 4.60 starting formation. 1 is at the left wing area dribbling left. 4 and 5 are at the corners of the free-throw area (elbows), forming the box set. 3 is below the free-throw line extended on the right side. 2 has already begun the rub cut off 4's high-post screen and is shown posting up near the left low block. The diagram shows 2 cutting off 4's screen toward the left low post, and 1 dribbling on the left side."}
```

### Phase 2: Side Screen / PnR for PG
- 4 leaves the lane and sets a **side screen** for 1.
- 1 runs the pick-and-roll.
- 4 **rolls to the basket or flares** depending on his shooting ability and the defense's reaction.

```json name=diagram-positions
{"players":[{"role":"1","x":-22,"y":28},{"role":"2","x":2,"y":25},{"role":"4","x":-6,"y":29},{"role":"5","x":14,"y":29},{"role":"3","x":20,"y":22}],"actions":[{"from":"4","to":"1","type":"screen"},{"from":"1","to":"rim","type":"dribble"},{"from":"4","to":"rim","type":"cut"}],"notes":"Figure 4.61 shows Phase 2 of the pick-and-roll play. 4 has left the lane (high post) to set a side screen for 1 on the left wing. 1 is dribbling off the screen toward the middle. 4 then rolls to the basket (or can flare). 2 is in the mid-lane area having previously posted up. 5 remains at the right elbow/high post. 3 is on the right wing below the free-throw line extended. The starting positions reflect the moment 4 sets the side screen for 1."}
```

### Phase 3: Perpendicular Double Screen for Guard
- If 2 does not receive the ball in the lane:
  - 2 cuts off the **perpendicular double screen** set by 5 and 3 on the baseline.
  - 1's reads: pass to **4** (roll/flare), to **2** (off double screen), to **5**, or to **3**.

```json name=diagram-positions
{"players":[{"role":"1","x":-22,"y":30},{"role":"2","x":3,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":-5,"y":32},{"role":"5","x":10,"y":28}],"actions":[{"from":"5","to":"right_corner","type":"screen"},{"from":"3","to":"right_corner","type":"screen"},{"from":"2","to":"right_corner","type":"cut"},{"from":"4","to":"rim","type":"cut"},{"from":"1","to":"4","type":"pass"}],"notes":"Figure 4.62 (Phase 3): 5 and 3 form a perpendicular double screen on the right baseline area. 2 cuts off the double screen from a mid-lane position. 4 is rolling/cutting toward the basket from the left side after the side screen. 1 is at the left wing with the ball, reading four options: pass to 4 (rolling), 2 (off double screen), 5, or 3. The depicted pass arrow in the diagram points toward 4's roll cut. Positions are approximated from the diagram — 2 starts near the free-throw lane before cutting off the double screen."}
```

## Key Coaching Points
- Three sequential actions — each one keys off whether the previous option was open.
- 1 must read all options without telegraphing: low post (2), PnR roll/flare (4), double screen (2), and open screeners (5, 3).
- The side screen angle for 4 must account for 1's defender position — picks are always based on **angles**.
- 4's roll/flare choice depends on defensive reaction: roll if 4's defender steps out, flare if the lane is congested.

## Counters
- 4's defender hedges on the PnR: 4 slips early for a lob from 1.
- 5's defender hedges on the double screen: 5 slips to the basket.
- 2's defender trails the double screen: 2 curls to the basket for a layup.

## Related Plays
- [[play-cross-screen]] — same box formation, cross-screen entry
- [[play-up-screen]] — same box set, back-screen entry
- [[play-diagonal-screen]] — diagonal screen + screen-the-screener variation
- [[concept-screen-types-reads]] — detailed reads for all screen types used in this play
- [[pick-and-roll-defense]] — how the defense will guard Phase 2

## Sources
- [S7, pp.70-71] — the source coach, Motion Offense
