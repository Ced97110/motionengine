---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [offense, half-court, continuity, back-screen, high-post, flare, motion, screening]
source_count: 1
last_updated: 2026-04-11
---

# Continuity Chin Action

## Summary
The "Chin" is a Continuity offense action that starts with a back pick by the high post (5) on the weak side of the half-court. It is designed to free a guard by having them rub off the back screen, while the high post then repositions to set a second screen on the opposite elbow for the ball-handler. This creates a sequential double-threat action: one player off the back screen and the ball-handler off the elbow screen, with the post rolling or popping as a third option.

The Chin action also includes a "Chin Pass to Strong Side" variant that incorporates simultaneous down screens and flare screens, giving the high-post hub up to four simultaneous passing options. [S7, pp.128-130]

## When to Use
- When the defense is locking up guards on the perimeter and denying wing passes
- When the post (5) is a strong passer who can handle the high-post hub role
- As a change of pace within the Continuity motion when standard sets are being denied
- The "Chin Pass to Strong Side" variant works well when the defense is switching screens and the high-post needs multiple simultaneous targets

## Key Principles
1. **Back pick triggers the guard cut** — 5 sets a back pick for 2 on the weak side; 2 rubs off toward the opposite side of the court
2. **Sequential elbow screens** — after the back pick, 5 moves to the other elbow to screen for 1 (the ball-handler); 5 rolls after the screen
3. **Back-screen-then-pop** — if 5's first screen doesn't free anyone, 4 comes back and back-screens for 5; 5 receives or 4 pops
4. **Flare screen doubles the threat** — in the strong-side variant, simultaneous down screen (3 for 2) and flare screen (1 for 4) give 5 four live passing options
5. **Backdoor counter on flare** — if 4's defender slides over the flare screen, 4 cuts backdoor instead of receiving the flare

## Phases

### Phase 1: Chin Option 1 — Basic Back Pick Into Elbow Screen
**Setup**: 1 at top, 2 at guard, 3 at wing, 4 at opposite wing, 5 at high post

1. 2 passes to 1; 2 rubs off 5's back screen → 2 gets to opposite side of court; 1 passes to 3
2. 3 can pass to 2 on the opposite wing
3. **If 2 can't receive**: 5 moves to the other elbow and screens for 1; 1 receives from 3 for a shot or drive; 5 rolls to basket in the opposite direction of 1
```json name=diagram-positions
{"players":[{"role":"1","x":-3,"y":35},{"role":"2","x":14,"y":35},{"role":"3","x":-22,"y":22},{"role":"4","x":20,"y":22},{"role":"5","x":-4,"y":24}],"actions":[{"from":"2","to":"1","type":"pass"},{"from":"1","to":"3","type":"pass"},{"from":"2","to":"right_corner","type":"cut"},{"from":"5","to":"1","type":"screen"}],"notes":"Figure 7.49 is the starting diagram. 2 starts at the right guard position and passes to 1 at the top of the key. 5 is at the left (weak-side) high-post elbow and sets a back screen for 2, who rubs off toward the right side of the court. 1 then passes to 3 on the left wing. The diagram marker references Figures 7.49-7.50 but the starting formation is from 7.49. 5's back screen for 2 and subsequent elbow screen for 1 are both depicted across the two-figure sequence; only the 7.49 starting formation and its immediate actions are captured here."}
```

### Phase 2: Chin Option 2 — Extended Sequence With Elbow Screens Both Sides
1. 2 passes to 1; 2 rubs off 5's back screen → cuts opposite; 1 passes to 3; 3 dribbles right
2. 5 screens for 1; 1 cuts opposite side to replace 4; 4 gets to the guard position
3. 3 passes to 4; 4 passes to 1; 3 rubs off 5's back screen → goes to ball-side corner; 1 can pass to 3
4. **If no solution**: 5 flashes to other elbow and back-screens for 4; 1 can pass to 4; if 4 still can't receive, 4 back-screens for 5; 1 passes to 5 or to 4 popping out
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":18,"y":33},{"role":"3","x":-18,"y":22},{"role":"4","x":18,"y":22},{"role":"5","x":-4,"y":24}],"actions":[{"from":"2","to":"1","type":"pass"},{"from":"2","to":"left_wing","type":"cut"},{"from":"5","to":"2","type":"screen"},{"from":"1","to":"3","type":"pass"}],"notes":"This is Figure 7.51 — the starting diagram for the \"Figures 7.51-7.54\" marker (Chin Option 2, sequential two-elbow action). Starting formation: 1 near top of key, 2 at right guard, 3 at left wing, 4 at right wing, 5 at high-post (weak-side elbow area). Arrows show 2 passing to 1, 5 back-screening for 2 (who cuts to the left side), and 1 passing to 3. The diagram shows the initial pass/cut sequence before 5 repositions to screen for 1 on the opposite elbow."}
```

### Phase 3: Chin Pass to Strong Side — Flare Action (Option 1)
**Triggers when the pass goes strong-side rather than weak-side:**
1. 2 passes to 3 (strong side); 5 (at strong-side elbow) sets back screen for 2; 2 posts down low ball side; 5 pops out after screen
2. 3 passes to 5; 3 screens down for 2 simultaneously as 1 sets a flare screen for 4
3. **5 has four simultaneous options**:
   - 2 coming off 3's down screen
   - 4 coming off 1's flare screen
   - 3 rolling to basket after setting the down screen for 2
   - 1 rolling to basket after setting the flare screen for 4
   - *Backdoor counter*: if 4's defender slides over the flare screen, 4 cuts backdoor
```json name=diagram-positions
{"players":[{"role":"5","x":-4,"y":20},{"role":"3","x":-18,"y":28},{"role":"2","x":-7,"y":40},{"role":"1","x":18,"y":32},{"role":"4","x":22,"y":22}],"actions":[{"from":"5","to":"2","type":"pass"},{"from":"3","to":"2","type":"screen"},{"from":"1","to":"4","type":"screen"},{"from":"5","to":"1","type":"pass"},{"from":"5","to":"3","type":"pass"},{"from":"5","to":"4","type":"pass"}],"notes":"This is Figure 7.56 — the second diagram of \"Chin Pass to Strong Side, Option 1.\" 5 is at the high-post/top-of-key area acting as the hub passer after receiving from 3. 3 is on the left wing area screening down for 2 (who is on the left low block). 1 is on the right wing setting a flare screen for 4 (who is on the right wing/corner). The diagram shows 5 with four simultaneous passing options: to 2 (off 3's down screen), to 4 (off 1's flare screen), to 3 (rolling to basket), and to 1 (rolling to basket). The starting formation shown is the moment 5 has the ball at the top with all four action options live."}
```

### Phase 4: Chin Pass to Strong Side — Option 2
1. 1 passes to 2; screens on the ball and pops out to replace 2; 2 dribbles opposite; 1 posts low weak side; 5 gets to other elbow
2. 2 passes to 4; 2 rubs off 5's back screen (ball side); 5 pops out
3. 5 receives from 4; 1 screens for 3; 3 pops out and receives from 5

## Player Responsibilities
- **PG (1)**: receives the initial pass; identifies which Chin option to trigger; screens or cuts as reads dictate
- **SG (2)**: primary user of the back pick; rubs off 5's screen; resets and receives off secondary action
- **SF (3)**: initiates the action; down screens for 2 in the strong-side variant; rolls to basket after screening
- **PF (4)**: guard replacement; back-screener for 5 in the reset; receives flare screen in the strong-side variant
- **C (5)**: sets every critical screen in this action; must read whether to roll, pop, or flash after each screen; is the primary hub passer in Phases 3-4

## Common Mistakes
1. **2 cuts too early off the back screen** → correction: time the cut to create maximum separation; rub shoulder to shoulder off the screen
2. **5 doesn't move after back pick** → correction: immediately relocate to the other elbow for the secondary screen on 1
3. **Passers ignoring the roller** → correction: 5 rolling to basket in the opposite direction of 1's drive is often the best option in Option 1
4. **Flare screen cutter not reading backdoor** → correction: if the defender goes over the flare screen, immediately redirect backdoor instead
5. **Only looking at one option** → correction: in the strong-side flare action, 5 must simultaneously see all four passing targets before committing

## Related Concepts
- [[concept-continuity-offense]] — the full Continuity motion system that contains Chin
- [[concept-high-post-continuity-basic-action]] — the three base sets that Chin augments
- [[concept-backdoor-cut-continuity]] — the backdoor counter embedded in the flare screen action
- [[concept-screen-the-screener-footwork]] — the sequential screening concept used in the Chin reset
- [[concept-flex-back-screen-footwork]] — flex back screen mechanics that share similarities with the Chin back pick

## Sources
- [S7, pp.128-130] — Eddie the iconic scorer and Pete Carril, Chapter 7: Continuity Offense — Chin options 1 and 2, and Chin Pass to Strong Side (Flare Action)