---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, out-of-bounds, man-to-man, switching, trapping, late-game, pro]
source_count: 1
last_updated: 2026-04-11
---

# Defending Out-of-Bounds Plays

## Summary
Out-of-bounds situations (sideline, baseline, and full-court) represent pre-planned offensive opportunities that require equally pre-planned defensive responses. Del Harris's approach centers on denying the two most dangerous passes in each situation, with a menu of trick coverages (zone shifts, first-pass traps, switches) available after time-outs. [S7, pp.260-262]

## When to Use
- Every out-of-bounds situation during the game
- Especially critical in late-game close situations when the opponent has prepared specific plays
- After time-outs when the opponent has diagrammed a play

## Key Principles
1. **Prevent the two key passes**: In every OOB situation, identify and deny the two most dangerous passes — the direct pass under the goal and the pass to the strong-side corner.
2. **Assistant coach preparation**: An assistant coach should have diagrams of the opponent's key OOB plays used in late-game situations.
3. **Trick up after time-outs**: After a time-out the opponent will run a set play; deviating from your standard coverage makes execution harder for them.
4. **Inbounder awareness**: The inbounder is dangerous — as either a step-in shooter or a slice cutter — after the pass is made. Don't leave him unguarded.
5. **Communicate and drill**: OOB defense must be practiced in game-like settings. Jim Calhoun's teams drill nine late-game situations per practice. [S7, p.269]

## Sideline Out-of-Bounds (SLOB) Defense

### Two Key Passes to Deny
1. Direct pass into the low post
2. Pass to the strong-side corner (sets up a post drop-pass or a catch-and-shoot 3)

### Coverage Rules
- X3 plays in the passing lane to the corner (active hands required)
- X5 fronts or denies 5 in the low post
- The defender on the inbounder pressures toward the baseline for 2-3 counts, then jumps off to deny the most dangerous receiver inbounds

### Trick Options After Time-Out
- Shift to zone
- Trap the first pass below the foul line
- Trap when the ball is passed to the weak side
- Switch certain (or all) players

```json name=diagram-positions
{"players":[{"role":"OB","x":28,"y":22},{"role":"3","x":28,"y":22},{"role":"x3","x":22,"y":30},{"role":"5","x":-5,"y":40},{"role":"x5","x":-3,"y":38}],"actions":[],"notes":"Figure 16.11 is a sideline out-of-bounds diagram viewed from the right sideline. The inbounder (3/OB) is on the right sideline near the wing area. X3 is positioned in the passing lane between the inbounder and the strong-side corner area, denying the corner pass. Player 5 is near the left low block/post area, and X5 is fronting/denying 5 in the low post. The dashed lines in the diagram appear to show the passing lanes being denied rather than action arrows. No clear movement arrows are depicted for this starting formation."}
```

## Baseline Out-of-Bounds (BLOB) Defense

### Two Key Passes to Deny
1. Direct pass under the goal (layup)
2. Easy catch-and-shoot in the strong-side corner

### Coverage Rules
- Play man-to-man as the base
- The defender on the ball inbounder moves to an angle off the ball toward the basket — sees both the ball and action toward the goal (active hands)
- This position also prevents an easy weak-side pass to the corner

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":47},{"role":"x1","x":3,"y":42}],"actions":[],"notes":"Figure 16.12 shows a baseline out-of-bounds situation. Player 1 is the inbounder (out of bounds at the baseline, roughly top-center of the diagram). The sole defender shown is X1, positioned at an angle off the ball toward the basket — slightly right of the rim and just inside the paint — able to see both the ball and action toward the goal. No other players or action arrows are clearly depicted in this diagram."}
```

### Option 1: Stack/Switch
- Put a smaller defender outside the stack and one in the lane; have them switch
- The outside man does not go through with the first cutter — passes him off and covers the corner area

```json name=diagram-positions
{"players":[{"role":"OB","x":-28,"y":38},{"role":"1","x":-28,"y":38},{"role":"4","x":-12,"y":40},{"role":"5","x":-9,"y":37},{"role":"2","x":-12,"y":43},{"role":"3","x":10,"y":45},{"role":"x1","x":-5,"y":37},{"role":"x2","x":-17,"y":40},{"role":"x3","x":2,"y":41},{"role":"x4","x":-8,"y":42},{"role":"x5","x":-7,"y":39}],"actions":[{"from":"x2","to":"left_corner","type":"cut"},{"from":"3","to":"right_corner","type":"cut"}],"notes":"Figure 16.13 shows a baseline out-of-bounds play (offensive player 1 is the inbounder at the left side of the baseline). Offensive players 4, 5, and 2 are stacked near the left low block/lane area. Player 3 is positioned near the right corner. Defenders x1 through x5 are matched up tightly in and around the lane. x2 is positioned outside the stack (the \"smaller defender outside the stack\"). The diagram shows arrows indicating the switch action — x2 does not follow the first cutter through but covers back to the corner area, while x4/x3 cover lane assignments. Action arrows are somewhat ambiguous in the scan; the two arrow-cuts shown are approximations of the switching movement described."}
```

### Option 2: Lane Check and Corner Switch
- Defender on the ball checks the middle of the lane, then switches out to the corner
- The lane defender (X3) switches into X1's vacated position
- Effective if not overdone; risky against elite players

```json name=diagram-positions
{"players":[{"role":"OB","x":-14,"y":-3},{"role":"1","x":-14,"y":-3},{"role":"5","x":-8,"y":36},{"role":"x5","x":-4,"y":36},{"role":"x1","x":2,"y":36},{"role":"x3","x":6,"y":36},{"role":"4","x":-10,"y":40},{"role":"x4","x":-4,"y":41},{"role":"x2","x":4,"y":42},{"role":"2","x":14,"y":44},{"role":"3","x":18,"y":32}],"actions":[{"from":"x1","to":"right_corner","type":"cut"},{"from":"x3","to":"x1","type":"cut"}],"notes":"Figure 16.14 shows a baseline out-of-bounds situation (player 1 is the inbounder at the left side of the baseline/sideline). The offensive stack (5, 4, 2) is clustered near the left block/lane area with their corresponding defenders (x5, x1, x4, x2, x3) tightly positioned. Player 3 is in the right corner area. The diagram depicts Option 2: the defender on the ball (x1) checks the middle of the lane and then switches out toward the corner (arrow toward right), while x3 switches into x1's vacated position. Arrows in the diagram show x1 moving toward the corner and x3 rotating up. Coordinates are approximated from the diagram on p.262."}
```

### Zone Under the Basket
- Zoning up against end out-of-bounds is riskier against great players
- Effective at high school/college level; a mistake against skilled players can allow a quick layup if the offense overloads the baseline or draws the middle man

## Full-Court Out-of-Bounds Defense
- Team's press philosophy dictates coverage
- **With short seconds remaining**: Defender of the inbounder drops back to the half-court area to play "centerfield" — watches the ball and follows the long pass to help contain the receiver and prevent a shot
- If a short inbounds pass comes first, the centerfield defender ignores it and waits for the next long pass — then doubles on air time
- If the receiver tries to drive upcourt for a quick shot, the centerfield defender gives help to stop it
- Alternative: Pressure the inbounder with one or two men for the full five seconds — most effective with 1-2 seconds remaining when a lob is the most likely scenario

## Common Mistakes
1. **Watching the ball only** → defenders must see both the ball and their assignment simultaneously
2. **Letting the inbounder slice in freely** → after passing in, the inbounder becomes a cutter or step-in shooter; track him immediately after the pass
3. **Soft hands at key denial spots** → "He must have active hands" [S7, p.261] — soft hands allow easy lobs and corner passes
4. **No plan for trick coverage** → standard coverage is predictable; have 2-3 alternate calls ready for time-out situations

## Related Concepts
- [[concept-pnr-coverage-options]] — Trap and switch rotations that may trigger after the inbounds pass is made
- [[concept-late-game-defensive-strategy]] — How OOB defense integrates into game-ending situations
- [[team-defense-calls-and-signals]] — Communication system for calling coverage changes
- [[defending-specific-plays]] — Herb Brown's broader framework for scouting and defending opponent play actions

## Sources
- [S7, pp.260-262] — Del Harris's complete OOB defensive system with court diagrams
