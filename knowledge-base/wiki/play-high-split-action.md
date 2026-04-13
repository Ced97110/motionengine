---
type: play
category: offense
formation: 2-3 high-post
tags: [continuity, high-split, pick-and-roll, backdoor, back-screen, motion, half-court]
source_count: 1
last_updated: 2026-04-11
---

# Continuity — Pass and Follow the Ball (High Split)

## Overview
In the "Pass and Follow" (High Split) set, after the entry pass to the high post (5), the passer (1) follows the pass toward the post instead of cutting away or screening away. This brings 1 into a split situation with the opposite forward (4), creating multiple layup, jump shot, and back-screen reads for the skilled post passer. The post must be a good passer and able to read all defensive situations. [S7, pp.123-124]

## Formation
1 at top of key; 2 at weak-side guard; 3 at weak-side wing; 4 at ball-side wing; 5 at high-post elbow opposite the ball.

## Phases

### Phase 1: Entry
- 2 passes to 1; 5 flashes to the high-post elbow opposite the ball
- 1 passes to 5; 2 cuts to the opposite side and comes off 3's screen
- 5 can pass to 2 on the cut or after 2 comes off 3's screen
```json name=diagram-positions
{"players":[{"role":"1","x":-8,"y":36},{"role":"2","x":8,"y":36},{"role":"3","x":-22,"y":22},{"role":"4","x":20,"y":22},{"role":"5","x":8,"y":29}],"actions":[{"from":"2","to":"1","type":"pass"},{"from":"1","to":"5","type":"pass"},{"from":"2","to":"3","type":"cut"},{"from":"3","to":"2","type":"screen"},{"from":"5","to":"2","type":"pass"}],"notes":"Figure 7.31: Starting formation shows 1 and 2 near the bottom of the key area (guard positions), 3 at left wing, 4 at right wing, and 5 flashing to the right elbow (high post, elbow opposite ball-side). The diagram depicts: 2 passes to 1, 1 passes to 5, 2 cuts toward 3's screen on the weak side, and 5 can pass to 2 coming off 3's screen. The initial positions reflect the moment just before the first pass (2 has ball, 1 is at top-of-key area)."}
```

### Phase 2: Five Split Options
If the initial 2-off-screen read is unavailable, 1 follows the pass toward 5 and the following options are available:

**Option A — 4 Backdoor Fake (1 Follows, 4 Goes Backdoor):**
- 1 follows the pass toward 5; 4 fakes a split and cuts backdoor to receive from 5
- 5 can also pass to 1, who pops out after following
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":44},{"role":"2","x":-10,"y":38},{"role":"3","x":-22,"y":22},{"role":"4","x":20,"y":28},{"role":"5","x":10,"y":30}],"actions":[{"from":"5","to":"4","type":"pass"},{"from":"4","to":"rim","type":"cut"},{"from":"1","to":"5","type":"cut"}],"notes":"Figure 7.32 shows the starting formation after 1 has followed the pass to 5 at the right elbow. 5 is at the right high-post elbow, 4 is at the right wing area, 1 is near the baseline below 5 (having followed the pass), 2 is at the left low-block/wing area, and 3 is at the left wing. The depicted actions show: 1 following toward 5 (cut), 4 faking and going backdoor to receive from 5 (pass from 5 to 4 cutting backdoor toward rim), and 1 popping out as an alternative. The primary action arrows are 5 passing to 4 on the backdoor cut."}
```

**Option B — Pick and Roll (1 Screens for 4):**
- 1 screens for 4; 4 receives the ball from 5 for a jump shot or drive
- 5 can also pass to 1, who rolls to the basket after the screen
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":38},{"role":"2","x":-14,"y":32},{"role":"3","x":-20,"y":20},{"role":"4","x":18,"y":26},{"role":"5","x":6,"y":30}],"actions":[{"from":"5","to":"4","type":"pass"},{"from":"1","to":"5","type":"screen"},{"from":"1","to":"rim","type":"cut"}],"notes":"Figure 7.33 depicts Option B — Pick and Roll. Starting formation: 1 has followed the pass and is near the low/mid lane area below 5 at the right elbow. 5 is at the right high-post elbow. 4 is at the right wing. 3 is at the left wing. 2 is at the left guard area. 1 screens for 4 (screen arrow shown), 4 curls off the screen to receive a pass from 5 (pass arrow to 4), and 1 rolls to the basket (cut arrow toward rim). The wavy line on 5 indicates a dribble move to create angle before the pass."}
```

**Option C — Screen and Pop Out (1 Screens for 4, Pops):**
- 1 screens for 4; 4 goes backdoor (or drives); 1 pops out for a jump shot
- 5 passes to 1 for the perimeter shot
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":44},{"role":"2","x":-14,"y":32},{"role":"3","x":-22,"y":18},{"role":"4","x":18,"y":22},{"role":"5","x":4,"y":30}],"actions":[{"from":"5","to":"4","type":"pass"},{"from":"1","to":"5","type":"screen"},{"from":"4","to":"right_corner","type":"cut"}],"notes":"Figure 7.34 (Option C): Starting position shows 1 near the baseline/low area (having followed the pass), 5 at the right elbow/high post, 4 at the right wing, 2 on the left wing, 3 at the left wing/corner. The diagram depicts 1 screening for 4 (with the wavy screen symbol), 4 going backdoor, and 5 passing to the popping-out 1. The depicted starting formation has 1 already near the lane having followed, with the screen-and-pop action shown."}
```

**Option D — Split with Backdoor (1 Splits with 4):**
- 1 and 4 split: 4 goes backdoor to the low post; 1 pops out to the wing
- 5 reads and passes to the open player
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":44},{"role":"2","x":-14,"y":34},{"role":"3","x":-20,"y":18},{"role":"4","x":20,"y":28},{"role":"5","x":8,"y":29}],"actions":[{"from":"5","to":"1","type":"pass"},{"from":"4","to":"rim","type":"cut"},{"from":"1","to":"right_wing","type":"cut"}],"notes":"Figure 7.35 (p.124): Starting formation for Option D — 1 splits with 4. 5 is at the right elbow (high post), 4 is at the right wing area, 1 is near the baseline below the key, 2 is at the left mid-wing, 3 is at the left wing. Action arrows show: 4 cuts backdoor toward the low post/rim, 1 pops out to the wing area, and 5 passes to 1. The diagram depicts the moment after 1 has followed the pass to 5 and both 1 and 4 are executing the split."}
```

**Option E — Back Screen for 5 (4 Back-Screens 5):**
- After the pass to 1, 4 back-screens for 5; 5 receives the ball from 1
- 1 can also pass to 4, who pops out after setting the back screen
```json name=diagram-positions
{"players":[{"role":"1","x":18,"y":28},{"role":"2","x":-10,"y":38},{"role":"3","x":-22,"y":18},{"role":"4","x":8,"y":18},{"role":"5","x":5,"y":33}],"actions":[{"from":"4","to":"5","type":"screen"},{"from":"4","to":"right_corner","type":"cut"},{"from":"1","to":"5","type":"pass"},{"from":"5","to":"rim","type":"cut"}],"notes":"Figure 7.36 shows Option E — 4 back-screens for 5. Starting positions: 1 is at the right wing/elbow area (has the ball, having followed the pass), 5 is at the right mid-post/elbow area, 4 is near the top of the key setting a back screen for 5, 3 is at the left wing, 2 is at the left low/mid area. The depicted actions show 4 setting a back screen on 5's defender, 5 cutting toward the basket off the screen, and 1 passing to 5 (or optionally to 4 popping out). 4 then pops out after the back screen."}
```

## Key Coaching Points
- The post (5) must scan all five options before the ball arrives — don't wait for cuts to develop after catching
- 1's follow must look like a cut, not a stroll — the defender must feel threatened
- Options C and D both use 4's backdoor to clear the lane; 5 reads which side the help is coming from
- Back-screening for 5 (Option E) is a surprise action that creates a mismatch when the defense focuses on the split
- "The post must be a good passer and able to read different defensive situations" [S7, p.123]

## Counters
- If defense locks up 5 on the catch: dribble to create a new passing angle before any cutter moves
- If 4's backdoor is denied: 4 flashes back to the ball-side wing for a reset pass from 5
- If defense switches everything: screener has a favorable roll/pop match — deliver immediately

## Related Plays
- [[play-pass-and-screen-away]] — the screen-away variant from the same basic set
- [[play-pass-and-cut-away]] — cut-away variant
- [[concept-continuity-offense-overview]] — full system overview
- [[concept-backdoor-cut]] — technique for the backdoor cuts in Options A, C, and D
- [[pick-and-roll-defense]] — how defenses respond to Option B and how to counter

## Sources
- [S7, pp.123-124] — Eddie the iconic scorer and Pete Carril, "Pass and Follow the Ball (High Split)", Continuity Offense chapter, pro Coaches Playbook
