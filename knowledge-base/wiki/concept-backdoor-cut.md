---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [offense, half-court, backdoor, cutting, continuity, off-ball-movement]
source_count: 1
last_updated: 2026-04-11
---

# Backdoor Cut

## Summary
The backdoor cut is the signature action of the Continuity offense and one of the most fundamental off-ball moves in basketball. When a defender overplays a receiver's passing lane, the offensive player exploits the overaggression by faking a step toward the ball and cutting hard to the basket — running away from the pressure rather than fighting it. With proper timing and a skilled passer (typically using a one-hand bounce pass), the backdoor cut produces high-percentage layup opportunities. All players — perimeter and post — must master it. [S7, pp.117-119]

## When to Use
- When a defender is actively denying a player's passing lane
- When a defender has lost sight of the cutter or the ball simultaneously
- As a pressure-releaser when the primary entry pass is denied
- Any time a perimeter player fakes toward the ball and sees the defender overreact
- From any position: wing, guard, high post, or low post

## Key Principles
1. **No banana cuts** — the cutter must cut at a sharp, decisive angle toward the basket, not a wide looping arc
2. **Fake toward the ball first** — create an overreaction from the defender with a strong step toward the ball, then cut hard behind the defender
3. **Give a hand target** — call for the ball only when open; show the passer exactly where you want the ball with your lead hand
4. **Timing between cutter and passer** — the passer must be ready to deliver quickly; any hesitation allows the defense to recover
5. **Preferred pass: one-hand bounce pass** — delivered quickly to where the cutter will be, not where they are
6. **Cut only when sure to be open** — a poorly-timed backdoor that isn't completed becomes a turnover

## Player Responsibilities
- **Cutter (any position)**: Fake toward ball → strong step → hard cut toward basket at an angle → show hand target → catch and finish
- **Passer**: Read the defender's overplay → pass immediately and decisively, preferably one-hand bounce → do not telegraph
- **Other perimeter players**: Maintain spacing; do not clog the cutter's path to the basket

## Variations

### Wing Direct Backdoor Cut
Wing (3) is denied by defender. 3 makes a strong step toward the ball to provoke the defender's overreaction, cuts hard behind the defender, and receives the ball from the point guard (1) for a layup. ```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":38},{"role":"3","x":-18,"y":22}],"actions":[{"from":"3","to":"rim","type":"cut"},{"from":"1","to":"3","type":"pass"}],"notes":"Figure 7.11: Direct backdoor cut by the wing. 3 starts at the left wing (~-18, 22) and cuts hard backdoor toward the basket. 1 is at the top of the key / guard position (~0, 38) with the ball and delivers a bounce pass to the cutting 3. An 'x' defender marker is shown near 3's starting position, indicating the overplaying defender. Only 1 and 3 are clearly positioned in this diagram; no other players are depicted."}
```

### Both Wings Backdoor Cut
With the ball in the post's (5) hands, both wings can simultaneously fake going toward the ball and cut backdoor if both are being overplayed — creating a 2-option layup read for the post. [S7, p.117]

### Backdoor Cut With the Help of the Center (Center-Assisted)
Post (5) flashes to the high-post area and receives from 2. Forward (4) fakes going up toward the ball and cuts backdoor to receive from 5 for a layup. Requires perfect spacing and timing between 5's catch and 4's cut. ```json name=diagram-positions
{"players":[{"role":"2","x":3,"y":44},{"role":"5","x":-8,"y":24},{"role":"4","x":18,"y":22}],"actions":[{"from":"2","to":"5","type":"pass"},{"from":"4","to":"rim","type":"cut"},{"from":"5","to":"4","type":"pass"}],"notes":"Figure 7.12: 2 is near the right baseline/low block area with the ball, 5 has flashed to the left elbow (high-post), and 4 starts at the right wing. The action sequence is: 2 passes to 5 at the high post; 4 fakes going up then cuts backdoor from the right wing toward the basket/low block; 5 delivers a bounce pass to 4 on the cut. A defender (x) marker is shown near 4's starting position indicating the overplay."}
```

### Guard-to-Guard Backdoor
If guard (2) is overplayed and 1 can't complete the pass, 2 makes a direct backdoor cut. [S7, p.118] ```json name=diagram-positions
{"players":[{"role":"1","x":-7,"y":43},{"role":"2","x":8,"y":38},{"role":"x2","x":12,"y":36}],"actions":[{"from":"2","to":"rim","type":"cut"},{"from":"1","to":"2","type":"pass"}],"notes":"Figure 7.13: Guard-to-Guard backdoor. 1 is near the bottom-left (ball handler), 2 starts near the right side of the key area with x2 overplaying. 2 cuts directly backdoor toward the basket while 1 delivers the pass. The diagram shows a half-court with 1 at the bottom-left dribbling, 2 and x2 at roughly the right elbow/wing area, and the cut arrow going from 2 toward the basket with a pass arrow from 1 to the cutting 2."}
```

### Wing-to-Guard Backdoor
Wing (4) wants to pass to guard (1), but 1 is overplayed. 1 fakes toward 4 and cuts backdoor to receive the pass. [S7, p.118]

### Guard Backdoor With the Center Pass
Guard (1) plays with the post (5), who flashes to the high-post area and receives from 2. 5 passes to 1 on the backdoor. ```json name=diagram-positions
{"players":[{"role":"1","x":-7,"y":36},{"role":"2","x":14,"y":36},{"role":"5","x":-5,"y":29}],"actions":[{"from":"1","to":"5","type":"pass"},{"from":"1","to":"rim","type":"cut"},{"from":"5","to":"rim","type":"pass"}],"notes":"Figure 7.15: 1 starts near the left side of the top of the key/high post area. 2 starts at the right guard/wing area near the baseline. 5 is at or near the left elbow (high post). The action sequence: 1 passes to 5 (who has flashed to the high post), then 1 cuts backdoor toward the basket; 5 receives from 2 first (per prose: \"receives from 2\"), but the diagram shows 1 dribbling/passing to 5 and then cutting — the diagram depicts 1 passing to 5 and cutting backdoor toward the rim, with 5 then passing to 1 on the cut. 2 is shown at the bottom/guard position. The starting positions reflect the moment before the sequence: 1 at top with ball, 5 at elbow, 2 at bottom guard spot."}
```

### High-Post Backdoor Cut
If the high post's (5) defender denies the pass reversal when the ball is in the wing's (1) hands, 5 fakes toward the ball then cuts hard behind the defender to receive the ball from 1 for a layup. ```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":44},{"role":"5","x":-2,"y":27}],"actions":[{"from":"5","to":"rim","type":"cut"},{"from":"1","to":"5","type":"pass"}],"notes":"Figure 7.16 shows the High-Post Backdoor Cut. Player 1 (ball-handler) is at the lower-left area near the wing/baseline. Player 5 (high post) starts near the high-post/elbow area with a defender (x) denying, then fakes toward the ball and cuts hard backdoor (dashed arrow) toward the basket to receive a pass from 1. The diagram shows 5's cut path from the high post area toward the rim, with 1 delivering the pass to the cutter."}
```

### Low-Post Backdoor Cut
If 5's defender denies the ball while 5 is flashing to the high-post area, 5 makes a strong backdoor cut to receive the ball and shoot under the basket. ```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":44},{"role":"2","x":14,"y":44},{"role":"5","x":-5,"y":29}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"5","to":"rim","type":"cut"}],"notes":"Figure 7.17 — Low-Post Backdoor Cut. 5 is at or near the high-post/elbow area (left side), flashing upward but denied, so 5 makes a backdoor cut toward the basket. 1 is near the left baseline/corner area with the ball (dribble marks shown), and 2 is at the right baseline. The diagram shows 1 passing to 2 (dashed line) and 5 cutting backdoor toward the rim. The defender (x) is shown near 5. The action is: 1 passes to 2, and 5 cuts backdoor to receive from 2 (or the pass goes directly to the cutter). The key starting positions are: 5 near left elbow/high post being denied, 1 near bottom-left with ball, 2 near bottom-right. 5's cut path goes from elbow toward the basket (backdoor)."}
```

## Common Mistakes
1. **Banana cut (wide looping arc)** → correction: cut at a sharp decisive angle; no half-measures
2. **Cutting before the defender overreacts** → correction: always fake toward the ball first; read the defender's weight transfer
3. **No hand target** → correction: always show the passer exactly where you want the ball
4. **Passer hesitates** → correction: passer must be pre-reading the defense and deliver instantly; one-hand bounce pass preferred
5. **Clogged lane** → correction: other perimeter players must maintain their spots and not wander into the cutter's path

## Related Concepts
- [[concept-continuity-offense-overview]] — the system in which the backdoor cut is the trademark action
- [[concept-reading-screens-off-ball]] — off-ball movement principles that set up the backdoor
- [[concept-v-cut-footwork]] — the fake-and-cut footwork family that underpins the backdoor
- [[play-pass-and-screen-away]] — the pass-and-screen-away set in which backdoor cuts are primary reads
- [[play-chin-series]] — the Chin action uses high-post back screens as an organized backdoor sequence

## Sources
- [S7, pp.117-119] — Eddie the iconic scorer and Pete Carril, "Backdoor Cut" section, Continuity Offense chapter, pro Coaches Playbook
