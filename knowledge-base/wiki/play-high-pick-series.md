---
type: play
category: offense
formation: 2-3 high-post
tags: [continuity, high-pick, pick-and-roll, double-screen, dribble-handoff, motion, half-court]
source_count: 1
last_updated: 2026-04-11
---

# Continuity — Sets Out of the High Pick

## Overview
The high pick entry uses the post (5) to set a direct on-ball screen for the point guard (1) near the top of the key after flashing to the elbow. Two option trees branch from this entry, both generating double-screen looks, hand-off sequences, and backdoor escape valves. [S7, pp.130-131]

## Formation
1 at top of key; 2 at guard; 3 at weak-side wing; 4 at ball-side wing; 5 flashes to the elbow.

## Phases

### Option 1: High Pick → Reverse Dribble → Double Screen

**Phase 1 — High Screen:**
- 5 flashes to the elbow, pops out, and sets a **high screen** for 1
- 2 cuts into the lane, is screened by 3, and gets out to the other side of the court (replacing 1)
- After the screen, 5 rolls outside
```json name=diagram-positions
{"players":[{"role":"1","x":-4,"y":22},{"role":"2","x":22,"y":42},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":22},{"role":"5","x":-4,"y":29}],"actions":[{"from":"5","to":"1","type":"screen"},{"from":"2","to":"rim","type":"cut"},{"from":"3","to":"2","type":"screen"}],"notes":"Figure 7.60 shows the initial Phase 1 formation of Sets Out of the High Pick, Option 1. 5 has flashed to just above the left elbow area and is popping out to screen for 1 near the top of the key. 2 is shown at the right corner/wing starting position before cutting into the lane. 3 is at the left wing. 4 is at the right wing. The action arrows show 5 screening for 1, 2 cutting into the lane, and 3 screening for 2 inside the lane."}
```

**Phase 2 — Reverse Dribble and Pass Chain:**
- 1 reverse dribbles and passes to 5; 5 passes to 2 and posts down low; 3 gets outside the three-point arc
- 2 passes to 3 and screens on the ball; 3 drives to the basket or passes to 2 (who rolled)
```json name=diagram-positions
{"players":[{"role":"1","x":10,"y":42},{"role":"2","x":-8,"y":42},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":22},{"role":"5","x":0,"y":38}],"actions":[{"from":"2","to":"3","type":"pass"},{"from":"2","to":"5","type":"screen"},{"from":"2","to":"rim","type":"cut"},{"from":"3","to":"rim","type":"dribble"}],"notes":"Figure 7.61 depicts Phase 2 of Option 1. The starting formation shown has 1 at the right baseline area, 2 near the left baseline (having come out to replace), 3 at the left wing after getting outside the arc, 4 at the right wing, and 5 posting down low near the lane. The depicted action is 2 passing to 3 and then screening on the ball, with 3 driving or 2 rolling to the basket. Positions are approximated from the diagram: 1 is near bottom-right, 2 near bottom-left, 3 at weak-side wing, 4 at ball-side wing, 5 low post center."}
```

**Phase 3 — Double Screen:**
- 5 runs down and forms a double screen with 3 for 2, who rubs off to the three-point arc
- 1 dribbles toward 4 for a hand-off pass; 4 dribbles to the other side and passes to 2
- If 4 is overplayed on the dribble-toward hand-off: 4 goes backdoor while 1 is dribbling toward him
- 2 can also pass to 5 (rolling) or to 3 (pop-out or curl around 5)
```json name=diagram-positions
{"players":[{"role":"1","x":3,"y":36},{"role":"2","x":16,"y":30},{"role":"3","x":-4,"y":24},{"role":"4","x":20,"y":22},{"role":"5","x":-4,"y":29}],"actions":[{"from":"1","to":"4","type":"dribble"},{"from":"3","to":"5","type":"screen"},{"from":"2","to":"left_corner","type":"cut"},{"from":"4","to":"2","type":"pass"}],"notes":"Figure 7.63 shows the Phase 3 / Option 2 double-screen state. 5 and 3 have formed a double screen near the left elbow/lane area. 2 is on the right wing having rubbed off the double screen. 1 is near the right low block dribbling toward 4 on the right wing for a hand-off. 4 is at the right wing. Arrows show 1 dribbling toward 4 (DHO), 4 passing/dribbling to 2, and 2 with passing options to 5 (roll) or 3 (pop). The depicted starting positions reflect the moment just before the hand-off: 1 near the right low area dribbling toward 4, with the 5-3 double screen set on the left side for 2."}
```

### Option 2: High Pick → Double Screen with Hand-Off

**Phase 1 — High Screen:**
- 5 flashes to the elbow, pops out, sets a high screen for 1; 2 cuts down low
```json name=diagram-positions
{"players":[{"role":"1","x":-2,"y":42},{"role":"2","x":14,"y":42},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":22},{"role":"5","x":-4,"y":22}],"actions":[{"from":"5","to":"1","type":"screen"},{"from":"1","to":"right_corner","type":"dribble"},{"from":"2","to":"left_corner","type":"cut"}],"notes":"Figure 7.62 shows Option 2 Phase 1: 5 has flashed to the elbow/top-of-key area and pops out to set a high screen for 1 near the top. 1 is at the bottom-center near the baseline area (dribbling), 2 is at the right guard area cutting down low, 3 is at the left wing, 4 is at the right wing. The diagram shows 5 screening for 1 (with an arrow showing 1 dribbling right toward 2's side) and 2 cutting down into the lane toward the left corner. Coordinates are approximated from the diagram layout."}
```

**Phase 2:**
- Continuity flows into the same double-screen / hand-off structure as Option 1 Phase 3 above

## Key Coaching Points
- The high pick is a change-of-pace entry — use it to vary the offense and prevent the defense from establishing a single denial pattern
- 5's roll after the high screen is immediate; if the defense hedges on the PnR, 5 catches the roll pass in the lane
- The DHO to 4 is a subtle action — 1 must make it look like a dribble drive, not a pass
- If 4 is overplayed on the DHO approach: 4's backdoor cut must be recognized and delivered immediately
- The double screen (5 and 3) is the primary scoring action — the read is whether 2 rubs high or low

## Counters
- If defense switches the high pick: 5 has size mismatch rolling — deliver; 1 has speed mismatch on the PnR pull-up
- If 2 can't get open off the double screen: 5 rolls hard and receives from 2; 3 pops to the arc

## Related Plays
- [[play-pass-and-screen-away]] — core "basic" set using same framework
- [[play-reverse-dribble-options]] — reverse dribble variant used in Phase 2
- [[play-chin-series]] — alternate high-post action
- [[concept-continuity-offense-overview]] — full system overview
- [[concept-backdoor-cut]] — technique for the 4-backdoor escape valve

## Sources
- [S7, pp.130-131] — Eddie the iconic scorer and Pete Carril, "Sets Out of the High Pick", Continuity Offense chapter, pro Coaches Playbook
