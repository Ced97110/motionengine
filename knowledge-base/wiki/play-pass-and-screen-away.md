---
type: play
category: offense
formation: 2-3 high-post
tags: [continuity, screen-away, backdoor, down-screen, high-post, motion, half-court]
source_count: 1
last_updated: 2026-04-11
---

# Continuity — Pass and Screen Away Set

## Overview
The "Pass and Screen Away" is the primary option within the Continuity basic action. After the entry pass to the high-post (5), the passer immediately screens away from the ball for another perimeter player. This forces multiple defenders to deal with simultaneous threats: a backdoor cutter, a screener rolling to the basket, and a pop-out shooter. Five distinct option trees are described, each triggered by how the defense responds. [S7, pp.119-122]

## Formation
1 (PG) at top of key; 2 (SG) at guard position opposite; 3 (SF) at weak-side wing/corner; 4 (PF) at ball-side wing; 5 (C) starts low post and flashes to the high-post elbow.

## Phases

### Phase 1: Entry to High Post
- 5 flashes to the high-post position (elbow or free-throw area) and receives from 1 (or 2)
- This entry can come from either side of the court

### Phase 2: Passer Screens Away (Option 1 Base)
- 1 passes to 5, then immediately screens away from the ball for 2
- 2 reads the screen: if overplayed, cuts backdoor; if the defender cheats, runs back under the basket
- 3 sets a down screen for 2 on the other side
- 5 reads and chooses from: (a) pass to 2 on backdoor, (b) pass to 2 off 3's down screen, (c) pass to 3 rolling to basket after the screen, (d) pass to 1 who pops out after screening
```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":42},{"role":"2","x":14,"y":36},{"role":"3","x":-22,"y":30},{"role":"4","x":20,"y":22},{"role":"5","x":-4,"y":28}],"actions":[{"from":"1","to":"5","type":"pass"},{"from":"1","to":"2","type":"screen"},{"from":"3","to":"2","type":"screen"},{"from":"2","to":"rim","type":"cut"},{"from":"5","to":"2","type":"pass"},{"from":"5","to":"3","type":"pass"},{"from":"5","to":"4","type":"pass"},{"from":"5","to":"1","type":"pass"}],"notes":"Figure 7.18 depicts the starting formation after 1 has already passed to 5 at the high post. 1 is at the left low area having just screened for 2; 2 is cutting backdoor on the right side; 3 is on the left wing set to down-screen for 2; 4 is on the right wing; 5 is at the left elbow/high post. The four pass arrows from 5 represent the described options: to 2 on backdoor, to 3 rolling, to 4, and to 1 popping out. The screen arrows from 1→2 and 3→2 are shown as action indicators rather than true starting positions."}
```

### Phase 2 Variant: Option 2
- 2 passes to 5, then screens for 4 (4 goes backdoor); 2 pops out
- 5 can pass to 4 for layup, to 2 popping out, to 3 rolling to basket, or 3 posts down low and receives from 4
- Continuity: 4 passes to 5, screens for 2 who goes backdoor and is later screened by 1; 5 has multiple reads ```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":42},{"role":"2","x":10,"y":42},{"role":"3","x":-22,"y":28},{"role":"4","x":22,"y":28},{"role":"5","x":0,"y":29}],"actions":[{"from":"2","to":"5","type":"pass"},{"from":"2","to":"left_corner","type":"cut"},{"from":"5","to":"4","type":"pass"},{"from":"4","to":"rim","type":"cut"},{"from":"3","to":"4","type":"screen"}],"notes":"Figure 7.19 shows Option 2 of the Pass and Screen Away Set. Starting formation: 1 and 2 at guard positions near the baseline extended, 3 and 4 at the wings, and 5 at the high post (elbow/free-throw area). 2 has the ball and passes to 5; 2 then screens for 4, who cuts backdoor toward the rim. 3 also sets a down screen for 4 on the weak side. The diagram depicts the initial action of 2 passing to 5 and screening for 4, while 3 screens 4 again as the continuity option. Positions are approximate based on the small diagram scan on p.120."}
```

### Phase 2 Variant: Option 3 (Hand-Off Entry)
- When 1 cannot enter to 3 or 5 or reverse to 2: 1 drives toward 3 for a hand-off pass while 2 and 4 exchange spots
- 3 passes to 4; 4 passes to 5 at the elbow; 3 cuts to the opposite side off 5
- 4 screens for 2 (backdoor read), then 1 screens for 2; 5 reads: (a) 2 backdoor, (b) 4 rolling, (c) 1 popping out <!-- DIAGRAMS: Figures 7.20-7.22, pp.120-121 -->
- Sub-option: 5 passes to 3; 4 back-screens for 5 who receives from 3; 3 can also pass to 4 who pops out after the screen <!-- Figure 7.23, p.121 -->

### Phase 2 Variant: Option 4
- 2 reverses ball to 1; 1 passes to 3 while 2 cuts to other side; 1 screens down for 2; 5 pops out of lane
- 3 passes to 5; 3 screens down for 2 while 4 screens down for 1; 5 reads: (a) 2 or 1 off down screens, (b) 3 or 4 rolling after screens
- Continuity: 5 screens away for 1 (backdoor); 2 can pass to 1 on backdoor or to 5 rolling <!-- Figures 7.24-7.27, pp.121-122 -->

### Phase 2 Variant: Option 5
- 1 passes to 2, cuts and screens for 5, goes to wing on other side
- 5 goes to high-post and receives from 2; 2 screens for 4 (backdoor)
- 5 reads: (a) 4 backdoor, (b) 1 popping out, (c) 2 rolling after screen <!-- Figure 7.28, p.122 -->

## Key Coaching Points
- The screener must set a legal, solid screen — then read to roll or pop based on the defense
- The cutter must always have a backdoor escape valve if overplayed coming off the screen
- 5 (high post) must scan the floor before catching and keep his dribble alive until a clear read emerges
- "There's more than one good opportunity to score per possession — but if the first backdoor cut is open for a layup, hey, we'll take it" [S7, p.132]
- Timing is everything: screens must be set before the cutter arrives; pass must arrive when the cutter is at the basket

## Counters
- If defense switches on every screen: the screener has a mismatch advantage rolling to the basket — deliver the ball there
- If defense sags off all screens: shooters catch pop-outs and shoot immediately before the defense can recover
- If 5 is denied the entry: reverse to the opposite side and start the action from there, or use the reverse dribble entry

## Related Plays
- [[play-pass-and-cut-away]] — alternate basic set where both guards cut away instead of screen
- [[play-high-split-action]] — follow-the-ball split set
- [[play-reverse-dribble-options]] — dribble-entry option when passing lanes are closed
- [[play-chin-series]] — high-post back-screen action building off the same framework
- [[concept-continuity-offense-overview]] — full system overview
- [[concept-backdoor-cut]] — technique for the backdoor cuts triggered throughout this set

## Sources
- [S7, pp.119-122] — Eddie the iconic scorer and Pete Carril, "Pass and Screen Away From the Ball Set", Continuity Offense chapter, pro Coaches Playbook
