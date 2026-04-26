---
type: drill
level: advanced
positions: [PG, SG, SF, PF, C]
players_needed: 8
duration_minutes: 10-15
tags: [defense, post-defense, fronting, help-defense, shell-drill, communication]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: post-defense-fronting
    emphasis: primary
  - id: weak-side-help-defense
    emphasis: primary
  - id: defensive-shell-drill
    emphasis: secondary
  - id: ball-pressure-defense
    emphasis: secondary
trains_anatomy:
  - region: core_outer
    emphasis: secondary
  - region: hip_flexor_complex
    emphasis: secondary
  - region: glute_max
    emphasis: secondary
---

# Green Drill (Front the Low Post)

## Objective
Train all four defenders to simultaneously execute low-post fronting ("Green"), weak-side tag, ball pressure, and elbow help whenever a guard cuts to the ball-side post.

## Setup
- 4 offensive players, 4 defensive players — 4-on-4 half court
- 2 guards lined up at the pro-lane line (outside the lane)
- 2 forwards at free-throw line extended, outside the three-point line
- Shell drill starting positions
- "Green" = team color command meaning **front the low post**

## Execution

### Phase 1: Guard-to-Guard Ball Movement
1. Ball passes from guard to guard; defenders shift to standard shell help positions.

### Phase 2: Guard-to-Forward Pass (Triggers Green)
1. When the ball is passed from guard to forward, the **guard who didn't pass** makes a **slice cut to the ball-side post**.
2. That guard's defender must:
   - **Jump to the ball** (help)
   - **Defend the cut** (body up on the cutter)
   - Then **get to a "Green"** (front the low post)
3. As the guard gets to a Green, the **weak-side forward** gets to a **"tag" position** — inside the three-second lane — to prevent the lob pass over the front.
4. If necessary, the weak-side forward tags the posting player to avoid a defensive 3-seconds call.

### Phase 3: Ball Pressure and Elbow Help
- Ball defender: apply ball pressure using the **nearest hand to trace the ball**, limiting the passer's vision.
- Defender at the top (closest to the ball): give **elbow protection** and be ready to help if the ball handler drives to the middle.

### Phase 4: Ball Reversal
1. After the ball is held for a count (allowing X2 to complete the Green), it reverses to the guard, then swings to the opposite corner.
2. The opposite guard now slice-cuts to the post — the drill repeats on the other side.
3. All four defenders rotate through each role (Green, Tag, Ball, Elbow).

### Full Sequence (with player numbers)
- 1 and 2 line up outside the pro lane; 3 and 4 at corners.
- 1 starts with the ball. X2 is on help side near free-throw area; X3 splits the difference.
- 1 passes to 4; 2 cuts to the box.
- X2 gets to a Green; X3 tags the low-post cutter.
- X2 yells **"Green! Green! Green!"** with hands high, butt low.
- X4 in hard no-middle stance pressuring the ball to discourage the post pass.
- X3 in good help position, yelling **"Tag! Tag! Tag!"** (uses all three seconds).
- 4 holds the ball → passes back to 1 → 1 swings to 3 → 3 swings to 2 in corner → 1 slice-cuts to post → drill repeats.

```json name=diagram-positions
{"players":[{"role":"1","x":18,"y":22},{"role":"2","x":-14,"y":26},{"role":"3","x":-22,"y":10},{"role":"4","x":22,"y":10},{"role":"x1","x":14,"y":20},{"role":"x2","x":-7,"y":29},{"role":"x3","x":0,"y":22},{"role":"x4","x":18,"y":14}],"actions":[{"from":"1","to":"4","type":"pass"},{"from":"2","to":"right_low_block","type":"cut"}],"notes":"Figure 17.5 is the starting formation shown: 1 is at the right wing with the ball, 4 is at the right corner, 3 is at the left corner, and 2 is at the left guard/wing area. The action shown is 1 passing to 4 (guard-to-forward pass) while 2 slice-cuts to the ball-side (right) low post. X2 moves toward a \"Green\" (front of the low post); X3 moves to tag position inside the lane; X4 pressures the ball at the right corner. The dashed arrows on the diagram indicate X2 and X3 shifting to help/tag positions, and X4 positioning on the ball. Coordinates are approximated based on the shell drill shell spots described in the text and visible in the diagram."}
```

## Coaching Points
- **"Green! Green! Green!"** — verbal call with hands high and butt low when in front-position.
- **"Tag! Tag! Tag!"** — weak-side big calls his tag position loudly and holds it for all three seconds.
- The fronting defender must not give the lob angle — the tag man is the insurance against the lob.
- Ball defender must use the **nearest hand** (not the full body) to trace the ball — maintain stance.
- The elbow helper must not sag so far that they can't recover if the ball is reversed.
- All four defenders should get Green reps and Tag reps by the time the drill repeats on both sides.

## Progressions
1. **Beginner**: Walk through roles slowly, calling each position aloud before moving.
2. **Intermediate**: Half-speed with live ball; defenders call Green/Tag as they arrive.
3. **Advanced**: Full speed with a live post player trying to catch the entry pass; play it out live after the catch.

## Concepts Taught
- [[post-defense-fronting]] — the Green concept is front-post defense
- [[weak-side-help-defense]] — tag position is weak-side help against the lob
- [[defensive-shell-drill]] — this drill is layered on top of the standard shell
- [[concept-productive-practice-structure]] — embedded in Frank's daily defensive breakdown sequence

## Sources
- [S7, pp.281-282] — the head coach, "Green" drill, Figures 17.5-17.7
