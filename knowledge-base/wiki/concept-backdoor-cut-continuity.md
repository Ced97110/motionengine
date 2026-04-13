---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [offense, half-court, cutting, backdoor, continuity, off-ball, layup, one-hand-bounce-pass]
source_count: 1
last_updated: 2026-04-11
---

# Continuity Backdoor Cut

## Summary
The backdoor cut is the trademark off-ball weapon of the Continuity offense. It is the automatic response whenever a defender tries to aggressively deny a pass to a teammate. Rather than fighting the pressure, the offensive player runs away from the defender — cutting sharply behind them toward the basket for a layup. The cut is initiated with one hard fake step toward the ball (to create a defensive overreaction), followed by a hard diagonal cut to the basket.

Every player on the court — whether a post or perimeter player — must master the backdoor cut. The cut is only useful when paired with a passer who can deliver the ball quickly (preferably via a one-hand bounce pass) with proper timing. [S7, pp.117-119]

## When to Use
- Any time a defender tries to deny a perimeter or post player from receiving the ball
- When a player's defender loses sight of them or the ball
- As a pressure releaser when the primary pass options are all denied
- With the ball in the hands of the high post (5), both wings can simultaneously cut backdoor if both are overplayed
- During any of the three basic Continuity set options when the natural pass recipient is being denied

## Key Principles
1. **Do not make a banana cut** — cut at a sharp angle directly toward the basket, not on a curved path; banana cuts are slower and easier to contest
2. **Fake first** — take one strong step toward the ball to get the defender to overreact; then immediately plant and cut hard backdoor
3. **Call for the ball only when open** — give the passer a hand target at the spot where you want to receive the ball
4. **Passer delivers quickly** — preferably with a one-hand bounce pass; hesitation defeats the timing and closes the window
5. **Good timing is everything** — the cutter and passer must be on the same page; this is the most critical technical requirement
6. **Any player can cut backdoor** — guards, wings, and post players all use the same mechanics

## Backdoor Cut Situations

### Wing — Direct Backdoor Cut
- Wing (3) is denied a catch on the perimeter
- 3 makes a strong step toward the ball to create a defensive overreaction
- 3 immediately cuts hard behind the defender
- 1 delivers a one-hand bounce pass for a layup
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":20},{"role":"3","x":-18,"y":22}],"actions":[{"from":"3","to":"rim","type":"cut"},{"from":"1","to":"3","type":"pass"}],"notes":"Figure 7.11 shows the Direct Backdoor Cut by the wing. Player 1 is at the top of the key/left-center area with the ball. Player 3 (wing) is at the left wing, with a defender (X) positioned to deny. 3 cuts hard backdoor behind the defender toward the basket (cut arrow shown), and 1 delivers a bounce pass to 3 cutting toward the rim. The 'x' defender marker is shown near 3's starting position on the left wing but no explicit x-player role coordinate is emitted as it represents the overplaying defender rather than a numbered offensive or defensive player tracked in the diagram."}
```

### Wing — Both Wings Backdoor Cut (Ball in Post)
- Ball is in the hands of the post (5) at the high post
- Both wings fake going toward the ball and simultaneously cut backdoor if both are aggressively overplayed
- 5 reads which cutter is open and delivers the pass

### Wing — Backdoor Cut With Help of the Center
- Post (5) flashes to the high-post area and receives from 2
- 4 fakes going up toward the ball and cuts backdoor
- 5 passes to 4 for a layup
- Requires perfect spacing and timing [S7, p.118]
```json name=diagram-positions
{"players":[{"role":"5","x":-8,"y":26},{"role":"4","x":10,"y":26},{"role":"2","x":18,"y":38}],"actions":[{"from":"2","to":"5","type":"pass"},{"from":"4","to":"rim","type":"cut"},{"from":"5","to":"4","type":"pass"}],"notes":"Figure 7.12: 5 is at the high-post area (left of center near the elbow), 4 starts near the right elbow area, and 2 is at the right wing/guard position. The sequence shown is: 2 passes to 5 at the high post, then 4 fakes up and cuts backdoor to the basket, and 5 passes to 4 for the layup. The diagram shows a defender (x) near 4's starting position. Starting formation captured before the backdoor cut is initiated."}
```

### Guard — Backdoor Cut With Pass From Other Guard
- Guard (2) is overplayed and 1 cannot pass to him
- 2 makes a direct backdoor cut to the basket
- 1 passes to 2 for a layup [S7, p.118]
```json name=diagram-positions
{"players":[{"role":"1","x":-7,"y":42},{"role":"2","x":8,"y":36},{"role":"x2","x":11,"y":35}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"2","to":"rim","type":"cut"}],"notes":"Figure 7.13 shows 1 at the left guard/bottom position with a dribble indicator, 2 at the right guard position with x2 overplaying him. 1 passes to 2 as 2 cuts directly backdoor (arrow toward the basket). The diagram is a simple two-player action with no other players depicted."}
```

### Guard — Backdoor Cut With Pass From the Wing
- Wing (4) wants to pass to 1, but 1 is overplayed
- 1 fakes going toward the ball (toward 4)
- 1 immediately cuts backdoor to receive from 4 [S7, p.118]

### Guard — Backdoor Cut With Pass From the Center (High Post)
- Post (5) flashes to the high-post area and receives from 2
- 1 cuts backdoor while 5 holds the ball at the elbow
- 5 passes to 1 for a layup [S7, p.118]
```json name=diagram-positions
{"players":[{"role":"1","x":-7,"y":42},{"role":"2","x":18,"y":42},{"role":"5","x":-4,"y":29}],"actions":[{"from":"1","to":"5","type":"pass"},{"from":"1","to":"rim","type":"cut"},{"from":"5","to":"1","type":"pass"}],"notes":"Figure 7.15: Guard backdoor cut with pass from the center (high post). 1 starts near the bottom of the lane/left block area, 5 is at the left elbow (high post), and 2 is at the right guard/wing position along the baseline. The diagram shows: 1 passes to 5 at the high post, then 1 cuts backdoor toward the rim while 5 delivers the return pass to 1 for a layup. The dashed line from 1 to 2 appears to represent 1's starting position relative to 2's position (2 is at the right wing/baseline extended). Defender x is shown near 1's starting position."}
```

### Post — High-Post Backdoor Cut
- Ball is in the hands of a wing (1)
- Defender of the high post (5) denies the reversal pass
- 5 fakes toward the ball then cuts behind the defender to receive from 1 for a layup [S7, p.119]

### Post — Low-Post Backdoor Cut
- 5's defender denies his receiving the ball while he is flashing toward the high-post area
- 5 makes a strong backdoor cut, receiving the ball for an under-basket finish [S7, p.119]

## Common Mistakes
1. **Banana cut (curved path)** → correction: cut at a straight angle directly to the basket; the diagonal line is shorter and faster
2. **Cutting without timing** → correction: cutter must wait until the passer's eyes are on them before initiating the move
3. **No hand target** → correction: extend the inside hand as a target showing where to deliver the ball
4. **Passer telegraphs or hesitates** → correction: pass must be delivered immediately — preferably a quick one-hand bounce pass
5. **Straight cut without a fake** → correction: always take one strong step toward the ball first to trigger the defender's denial instinct before redirecting

## Related Concepts
- [[concept-continuity-offense]] — the full Continuity system that uses the backdoor cut as its primary weapon
- [[concept-high-post-continuity-basic-action]] — the three basic set options that all include backdoor reads
- [[defending-flash-post-blind-pig]] — the defensive principles that try to prevent the backdoor and flash-post action
- [[concept-v-cut-footwork]] — V-cut mechanics that share the "fake toward ball, cut away" principle
- [[concept-reading-screens-off-ball]] — how off-ball players read defenders to choose backdoor vs. curl vs. fill

## Sources
- [S7, pp.117-119] — Eddie the iconic scorer and Pete Carril, Chapter 7: Continuity Offense — complete description of all six backdoor cut situations for wings, guards, and post players