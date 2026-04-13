---
type: play
category: offense
formation: box
tags: [back-screen, down-screen, screen-the-screener, post-up, half-court]
source_count: 1
last_updated: 2026-04-11
---

# Motion Offense Up Screen Play

## Overview
A half-court play using a back screen to create a post-up, followed by a down-screen continuity that generates multiple passing options. the source coach's Motion Offense ran this from the same box formation as the Cross-Screen Play, creating defensive confusion with a completely different initial action. [S7, pp.68-69]

## Formation
Same box as the Cross-Screen Play:
- **1 (PG)**: dribbling on the left side
- **2 (SG)**: left low post
- **5 (C)**: left high post / free-throw corner (left)
- **4 (PF)**: right low post
- **3 (SF)**: right free-throw corner

## Phases

### Phase 1: Back Screen Entry
- 1 dribbles on the **left side**.
- 2 sets a **back screen** (up screen) for 4.
- 4 cuts **down** and posts up in the **low-post position** (left block).
- **1's first read**: pass to 4 in the low post.
- **1's second read**: pass to 2, who opens up after the screen **facing the basket** at the elbow.

```json name=diagram-positions
{"players":[{"role":"1","x":-18,"y":36},{"role":"2","x":-10,"y":29},{"role":"4","x":7,"y":40},{"role":"5","x":-8,"y":29},{"role":"3","x":8,"y":29}],"actions":[{"from":"1","to":"left_wing","type":"dribble"},{"from":"2","to":"4","type":"screen"},{"from":"4","to":"left_low_block","type":"cut"},{"from":"1","to":"4","type":"pass"},{"from":"1","to":"2","type":"pass"}],"notes":"Figure 4.55 (Up Screen Play, Phase 1). The box formation starts with 2 near the left elbow/high post, 5 also near the free-throw line on the left, 4 on the right low post, and 3 at the right free-throw corner. 1 begins near the left wing already in motion. 2 sets a back screen for 4, who cuts down to the left low post. After the screen, 2 opens up facing the basket at the elbow. 1 has two pass options shown: to 4 posting up, or to 2 at the elbow. The diagram shows 5 and 3 set up at the free-throw line corners (as in the box set), not yet involved in the action."}
```

### Phase 2: Elbow Continuation
- If 1 passes to **2 at the corner of the free-throw area** and 2 cannot shoot:
  - 5 screens **down** for 3, then rolls to the basket.
  - 2 can pass to **3** (coming off 5's down screen), to **5** (rolling to the basket), or to **4** (ducking in).
- If 2 passes to 3 and 3 cannot shoot: 3 passes to **5**, who posts up after rolling.

```json name=diagram-positions
{"players":[{"role":"1","x":-14,"y":16},{"role":"2","x":-8,"y":29},{"role":"5","x":5,"y":29},{"role":"4","x":-22,"y":40},{"role":"3","x":18,"y":22}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"5","to":"3","type":"screen"},{"from":"5","to":"rim","type":"cut"},{"from":"2","to":"3","type":"pass"},{"from":"2","to":"5","type":"pass"}],"notes":"Fig 4.56 (Phase 2 of Up Screen Play): 2 has received the ball at the left elbow area from 1. 5 is setting a down screen for 3 on the right side, then rolling to the basket. 4 is ducking in on the left low block. 2's options are to pass to 3 (off 5's down screen), to 5 (rolling to rim), or to 4 (ducking in). The depicted starting formation shows 2 at the left elbow with the ball, 5 near the right elbow/free-throw area screening for 3 who is at the right wing, 4 on the left low block, and 1 at the left wing. Positions are approximated from the Fig 4.56 diagram on page 69."}
```

## Key Coaching Points
- Two plays from the same box set — run them interchangeably to keep the defense guessing.
- 2 must read after setting the screen: **open facing the basket** at the elbow — this is a scoring threat, not just a placeholder.
- 5's down screen + roll creates two simultaneous threats (3 popping, 5 rolling).
- 4's duck-in is always available as a third option off the elbow.

## Counters
- If 4 catches clean in the post: standard post reads.
- If 2 catches and can shoot from the elbow: take it — it is the primary read.
- If 5's defender hedges the down screen: 5 slips immediately to the basket.

## Related Plays
- [[play-cross-screen]] — same box formation, different entry action
- [[play-diagonal-screen]] — diagonal screen + screen-the-screener variation
- [[concept-screen-types-reads]] — back screen and down screen reads

## Sources
- [S7, pp.68-69] — the source coach, Motion Offense
