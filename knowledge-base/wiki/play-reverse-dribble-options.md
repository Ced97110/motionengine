---
type: play
category: offense
formation: 2-3 high-post
tags: [continuity, reverse-dribble, backdoor, pick-and-roll, double-screen, motion, half-court]
source_count: 1
last_updated: 2026-04-11
---

# Continuity — Reverse Dribble Options

## Overview
When the ball handler cannot make any entry pass (blocked by overplaying defenders), the Continuity offense transitions into reverse dribble entries. These three options — plus the Double Screen High variant — ensure the offense never stalls even when all passing lanes are denied. Each reverse dribble triggers a specific set of cuts, screens, and handoffs. [S7, pp.125-127]

## Formation
1 at top of key; 2 at guard spot; 3 and 4 at wings; 5 flashing or positioned at the elbow.

## Phases

### Option 1: Basic Reverse Dribble

**Phase 1:**
- 1 can't pass to any teammate; dribbles toward 2; 2 cuts away from ball to opposite side
- 1 reverse dribbles toward 4; 4 goes backdoor (or screens for 2) then moves to low post
- 5 flashes to the elbow on the weak side
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":22},{"role":"2","x":18,"y":22},{"role":"3","x":-18,"y":22},{"role":"4","x":5,"y":5},{"role":"5","x":-4,"y":29}],"actions":[{"from":"1","to":"2","type":"dribble"},{"from":"2","to":"left_corner","type":"cut"},{"from":"1","to":"4","type":"dribble"},{"from":"4","to":"rim","type":"cut"},{"from":"5","to":"left_elbow","type":"cut"}],"notes":"Figure 7.37 depicts the starting formation for Reverse Dribble Option 1. 1 is at the top of the key with the ball, 2 is at the right guard/wing spot, 3 is at the left wing, 4 is at the right elbow/high-post area, and 5 is near the top of the key on the weak side. The diagram shows: 1 dribbling toward 2, 2 cutting away (left) to the opposite side, 1 then reverse dribbling toward 4, 4 going backdoor toward the rim, and 5 flashing to the weak-side elbow."}
```

**Phase 2:**
- After the reverse dribble, 1 passes to 2
- 5 sets a side screen for 1; 1 receives from 2 for a jump shot or drive
- 2 can also pass to 5, who rolled to the basket after the screen
- 2 can screen down for 4 after passing to 1; 4 receives from 1
```json name=diagram-positions
{"players":[{"role":"1","x":2,"y":22},{"role":"2","x":22,"y":22},{"role":"3","x":-18,"y":22},{"role":"4","x":8,"y":5},{"role":"5","x":0,"y":29}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"5","to":"1","type":"screen"},{"from":"2","to":"4","type":"screen"}],"notes":"Figure 7.38 shows the state after 1's reverse dribble and pass to 2. Starting positions: 1 has moved toward center/top of key area, 2 is at right wing having received or about to receive the pass, 5 is near the free-throw line to set a side screen for 1, 3 is at the left wing, and 4 is at the right elbow/high post area. The diagram shows 1 passing to 2, 5 screening for 1, and 2 optionally screening down for 4."}
```

### Option 2: Guard Reverse Dribble with Down Screens

**Phase 1:**
- 2 dribbles toward 1, then reverse dribbles and passes to 3; 5 has flashed outside the lane
- 5 receives from 3; 2 and 1 cut to their original side, screened by 4 and 3 respectively
- 5 reads: (a) 2 or 3 off screens, (b) 4 or 5 rolling
```json name=diagram-positions
{"players":[{"role":"1","x":14,"y":28},{"role":"2","x":-2,"y":38},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":22},{"role":"5","x":4,"y":24}],"actions":[{"from":"2","to":"1","type":"dribble"},{"from":"2","to":"3","type":"pass"},{"from":"3","to":"5","type":"pass"},{"from":"1","to":"left_corner","type":"cut"},{"from":"2","to":"left_corner","type":"cut"},{"from":"4","to":"2","type":"screen"},{"from":"3","to":"1","type":"screen"}],"notes":"Figure 7.39: Starting formation shows 1 at the right guard/wing area, 2 near the center-bottom (ball handler initiating the reverse dribble), 3 at the left wing, 4 at the right wing, and 5 near the top of the key/elbow. 2 dribbles toward 1 then reverse dribbles and passes to 3; 3 passes to 5 who has flashed outside the lane. 2 and 1 cut back to their original sides, screened respectively by 4 (for 2) and 3 (for 1). Coordinates are approximated from the diagram's relative player positions."}
```

**Phase 2 Continuity:**
- 5 passes to 1 and goes to low post; 4 goes outside the three-point arc; 1 passes to 2
- 2 reverse dribbles; 1 cuts through lane off 3's screen; 2 passes to 1 or 3 (roll)
- 1 passes to 3; 5 side-screens for 2 then pops; 3 passes to 1, 2, 5 or 4 (spot up)
<!-- DIAGRAMS: Figures 7.40-7.42, pp.126 -->

### Option 3: When 2 Is Overplayed (Backdoor + Strong-Side Options)

**Phase 1:**
- 2 is overplayed; 1 dribbles toward 2; 2 makes a backdoor cut to opposite side
- 1 reverse dribbles and has three strong-side options:
  - (a) 4 screens for 2 and rolls to basket
  - (b) 4 fakes the screen and cuts to basket
  - (c) 4 posts up down low
```json name=diagram-positions
{"players":[{"role":"1","x":10,"y":38},{"role":"2","x":-8,"y":38},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":28},{"role":"5","x":-4,"y":24}],"actions":[{"from":"1","to":"2","type":"dribble"},{"from":"2","to":"right_corner","type":"cut"},{"from":"4","to":"rim","type":"cut"},{"from":"1","to":"2","type":"pass"}],"notes":"Figures 7.43–7.44 depict Option 3 of the Reverse Dribble. Figure 7.43 (starting formation): 1 has reverse dribbled toward the right side; 2 has cut backdoor to the left corner area; 5 is near the top of the key/elbow area; 4 is on the right wing; 3 is on the left wing. The primary action shown is 1 reverse dribbling and passing to 2 coming off 4's screen, or to 4 rolling to the basket. Figure 7.44 shows 4 posting up low as the alternative — starting positions are essentially the same. The actions emitted reflect the dominant arrow in Fig 7.43 (4 screens for 2, rolls to basket; 1 passes to 2 or 4)."}
```

**Phase 2 — PnR Continuity:**
- 1 can also pass to 2, receive a screen from 5, and get the ball back from 2; 1 then plays pick-and-roll with 5
```json name=diagram-positions
{"players":[{"role":"1","x":8,"y":38},{"role":"2","x":18,"y":35},{"role":"3","x":-18,"y":40},{"role":"4","x":10,"y":5},{"role":"5","x":0,"y":31}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"5","to":"1","type":"screen"},{"from":"1","to":"rim","type":"dribble"}],"notes":"Figure 7.45 shows the PnR continuity phase of Option 3. 1 is near the right slot area (having reverse dribbled), 2 is on the right wing, 5 is near the free-throw line/elbow area setting a screen for 1, 3 is on the left corner/wing, and 4 has moved out toward the top right. The diagram depicts: 1 passes to 2, receives a screen from 5, gets ball back from 2, then plays pick-and-roll with 5. Actions shown include 1 passing to 2 and the screen from 5 on 1."}
```

### Double Screen High Variant

**Setup:**
- 1 dribbles toward 2 (overplayed); 2 and 3 exchange spots; 1 reverse dribbles and passes to 5 at the elbow
- 3 and 1 form a double screen on the opposite side

**5's Options:**
- Pass to 2 rubbing off the double screen (high or low)
- After a couple of dribbles, pass to 4 who cuts backdoor if overplayed
- Pass to 2 who fakes the double screen and cuts backdoor
- Pass to 1 who pops out of the screen
<!-- DIAGRAMS: Figures 7.46-7.48, pp.127 -->

## Key Coaching Points
- The reverse dribble is a last resort — teach it as a continuity option, not a default habit
- Every reverse dribble triggers specific teammate reactions; players must read the dribble direction and respond immediately
- 4's three-option read (screen-roll, fake-and-cut, post-up) in Option 3 is the key decision-making moment — the defender's position determines which is right
- The double screen high is especially useful when the defense has fully committed to denying the first three perimeter reads

## Counters
- If defense switches on the double screen: the popped-out screener (1) is open; pass immediately
- If 4 is denied the backdoor in Option 3: 4 posts up low and uses [[concept-post-receiving-footwork]]
- If 5's pick-and-roll in Option 3 is hedged: 5 rolls hard to the rim; if trailed, 5 pops to midrange

## Related Plays
- [[play-pass-and-screen-away]] — the primary pass-based entry set
- [[play-chin-series]] — another alternative entry action
- [[concept-continuity-offense-overview]] — full system overview
- [[concept-backdoor-cut]] — backdoor technique used throughout
- [[pick-and-roll-defense]] — how defenses attack the PnR read in Option 3

## Sources
- [S7, pp.125-127] — Eddie the iconic scorer and Pete Carril, "Options to 'Basic'", Continuity Offense chapter, pro Coaches Playbook
