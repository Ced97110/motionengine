---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, pick-and-roll, man-to-man, switching, trapping, rotation, pro]
source_count: 1
last_updated: 2026-04-11
---

# Pick-and-Roll Defensive Coverage Options

## Summary
Del Harris outlines four primary coverage schemes for defending the pick-and-roll, each carrying different risk-reward profiles. The choice of coverage depends on personnel, game situation, score, shot-clock context, and scouting of the opponent's tendencies. No single method is universally superior; what matters most is that the entire team understands the chosen system and executes it with consistent communication. [S7, pp.257-258]

## When to Use
- **Trap**: Against high-level ball-handler/screener combinations; when you want to force turnovers and accept rotation risk
- **Switch**: Late game protecting a lead; when possession clock is under 7 seconds; when equal-sized players are matched
- **Overplay down**: Wing and corner pick-and-rolls where pushing the ball handler toward the baseline is safe; requires a verbal call
- **Rotation**: Default fallback when any coverage breaks down — lowest defender near the goal rotates to the roller

## Key Principles
1. **Communication first**: The defender on the screener must call the coverage the instant a screen is spotted — color code, "Down!", "Switch!", etc.
2. **Stop penetration, not just the ball**: Every coverage scheme exists to prevent a clean dribble penetration toward the paint.
3. **Rotation rules are non-negotiable**: On any PnR, the lowest defender near the goal (X5 in most schemes) has primary responsibility for the roll man; adjacent defenders fill in behind him.
4. **Mismatches are less dangerous than open shots**: "Mismatches caused by switching are far less dangerous than giving up an open shot to a good shooter." [S7, p.257]
5. **Drill the chosen coverage**: Coaches have won championships with every approach — what matters is committing, practicing, and eliminating doubt in players' minds.

## Coverage Details

### Option 1 — Trap
The screener's defender (X5) jumps out to trap the ball handler (1) just as he comes over the pick. The most aggressive version traps *before* the screen is set. Rotation rules:
- X4 rotates to cover the screener (5) as soon as he sees the ball in the air on a pass from 1 to 5
- X5 rotates opposite the pass into the paint to pick up the next open man (usually 4)
- X3 covers until X5 can rotate
- If X5 is late, he may need to cover 3 on the weak side

```json name=diagram-positions
{"players":[{"role":"1","x":-14,"y":38},{"role":"2","x":18,"y":30},{"role":"3","x":22,"y":14},{"role":"4","x":-16,"y":16},{"role":"5","x":-6,"y":38},{"role":"x1","x":-8,"y":34},{"role":"x2","x":8,"y":28},{"role":"x3","x":4,"y":24},{"role":"x4","x":-4,"y":22},{"role":"x5","x":-10,"y":40}],"actions":[{"from":"x5","to":"1","type":"cut"},{"from":"x4","to":"5","type":"cut"},{"from":"1","to":"5","type":"pass"}],"notes":"Figure 16.1: Trap and rotation coverage. In the diagram, 1 (ball handler) is near the left low block area, 5 (screener) is just inside him setting the pick. X5 jumps out to trap 1 alongside X1. X4 is shown rotating toward 5. Arrows indicate X5 trapping 1, X4 rotating to 5, and the anticipated pass from 1 to 5. X3 is shown on the right side of the lane as help defender. Players 3 and 4 are on opposite wings/perimeter. Coordinates are approximated from the diagram layout where the pick-and-roll action occurs on the left side near the low block/elbow area."}
```

### Option 2 — Switch
Easiest form of coverage; most effective with equal-sized players. pro teams use it late in games (last 7 seconds or less on shot clock) to deny open threes.
- The mismatched defender rotates off to the weak side to pick up an open man
- A small defender (X3) must rotate over to replace a bigger teammate (X5) stuck on the perimeter guarding a quick penetrating player
- X2 rotates to cover 3; X1 covers 2
- Big players must **automatically trap down** for a small teammate being posted by a big — e.g., X4 traps down when X5 is posted on the wing

```json name=diagram-positions
{"players":[{"role":"1","x":-18,"y":38},{"role":"2","x":20,"y":30},{"role":"3","x":22,"y":14},{"role":"4","x":4,"y":14},{"role":"5","x":4,"y":29},{"role":"x1","x":-4,"y":22},{"role":"x2","x":10,"y":26},{"role":"x3","x":6,"y":20},{"role":"x4","x":-4,"y":18},{"role":"x5","x":-12,"y":30}],"actions":[{"from":"x4","to":"5","type":"screen"},{"from":"x3","to":"2","type":"cut"},{"from":"x2","to":"3","type":"cut"}],"notes":"The marker references two diagrams: Figure 16.2 (switching) and Figure 16.3 (small player replaces bigger teammate). Per instructions, the INITIAL / first formation is extracted — Figure 16.2, pick-and-roll switching coverage. In Fig 16.2: 1 is at the left low block area with the ball, 5 is at the top of the key setting a pick near x1, x4/x5 are switching, 2 is on the right wing, 3 is at the right corner, 4 is near the top right. In Fig 16.3 (second diagram): 1 is at the left corner, 5 is at the left mid-post, 2 is right wing, 3 is right corner, 4 is top right; x1 is near center, x2/x3/x4/x5 are in rotation. Positions above represent Fig 16.2 starting formation with rotational arrows reflecting the switch assignments (x3→covers 2's area, x2→covers 3's area) as described in the prose for Fig 16.2/16.3."}
```

### Option 3 — Overplay Down to the Baseline
Screener's defender calls "Down right!" or "Down left!" The ball defender overplays severely on the high side to push the ball handler toward the baseline and into the screener's defender. Used primarily on wing and corner PnRs.
- Ball defender must maintain contact to prevent a split between himself and the screener's defender
- On a pass to the screener, decide pre-game whether X5 recovers to 5 directly or whether a nearby player (X2, X4) rotates; choice depends on whether the screener is a shooting threat from 15-17 feet
- Same down calls apply at the top of the key but are considered less safe there

```json name=diagram-positions
{"players":[{"role":"1","x":-20,"y":38},{"role":"5","x":-14,"y":38},{"role":"x1","x":-17,"y":38},{"role":"x5","x":-6,"y":32},{"role":"x4","x":4,"y":18}],"actions":[{"from":"x1","to":"1","type":"screen"},{"from":"1","to":"left_corner","type":"dribble"}],"notes":"The marker references Figures 16.4–16.7 (overplay down variants and recovery rotations, p.258). Figure 16.4 is the first/initial diagram on that page and shows a wing/corner pick-and-roll with the overplay-down coverage. Offensive players: 1 (ball handler) is near the left corner baseline area, 5 (screener) is just inside 1. Defenders: X1 is between 1 and 5 on the high side (overplaying), X5 is positioned 2–3 steps below the screen toward the baseline paint area, X4 is shown higher up as the weak-side rotation man. Only four players (1, 5, X1, X5, with X4 partial) are clearly depicted in Figure 16.4 — a fifth defender (X5 upper position) is also shown in the diagram suggesting the \"before\" and \"after\" positioning of X5. The diagram is somewhat small and approximate coordinates are used."}
```

### Option 4 — Rotation (Base Coverage)
Default baseline rotation when the ball handler passes to a rolling or popping screener:
- The lowest defender rotates to the roller
- Adjacent weak-side defenders fill the vacated spots
- Applicable to wing, corner, top-angle, and sideline PnRs

## Player Responsibilities
- **PG (X1)**: Primary on-ball defender; follows coverage call; must maintain contact on "down" coverage to prevent splits
- **SG (X2)**: Weak-side rotation; covers 3 on a switch when X1 is drawn off
- **SF (X3)**: Weak-side help; covers until X5 can rotate on traps; rotates to 3 on mismatch adjustments
- **PF (X4)**: Rotates to roll man or popping screener on trap coverage; traps down for X5 on post mismatch
- **C (X5)**: Primary screener defender; calls coverage; traps ball handler; rotates into paint after trap pass; must recover quickly to avoid leaving X4 exposed

## Variations
### Late-Game 5-Man Switch Arc
When opponent needs a 3-pointer in the final seconds, all five defenders line up in an arc *above* the three-point line. Players switch out on all picks but must communicate loudly. [S7, p.268]

### Small-on-Big Emergency Coverage
X3 replaces X5 on the perimeter when X5 is stuck post-guarding a smaller player after a switch. X5 floats to the weak side and picks up the open man. [S7, p.257]

## Common Mistakes
1. **No verbal call on screen** → screener's defender calls the coverage the instant he sees the screen forming, not after contact
2. **Ball defender splitting the trap** → maintain hip contact with the ball handler; don't give two steps of space
3. **X5 freezing on the trap** → as soon as the ball leaves on a pass to the roll/pop, X5 immediately rotates opposite the pass into the paint
4. **Switching without checking size mismatch** → big players must automatically trap down for small teammates posted by a big opponent; never allow a static big-on-small mismatch in the paint
5. **Dropping to help on penetration when protecting a 3-point lead** → "The natural tendency to drop to the level of penetration allows the opportunity for penetration followed by a pass out to a three-point shooter." [S7, p.267]

## Related Concepts
- [[pick-and-roll-defense]] — Herb Brown's complementary PnR system with show/contact/rotation rules
- [[isolation-defense]] — Coverage options when an opponent isolates a one-on-one attacker
- [[concept-late-game-defensive-strategy]] — How PnR switching integrates into late-game 3-point protection
- [[team-defense-calls-and-signals]] — Communication system for calling coverage types
- [[weak-side-help-defense]] — Rotation principles that underpin all PnR recovery

## Sources
- [S7, pp.257-258] — Del Harris's complete PnR coverage options with rotation diagrams
