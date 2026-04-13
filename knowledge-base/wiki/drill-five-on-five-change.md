---
type: drill
level: advanced
positions: [PG, SG, SF, PF, C]
players_needed: 10
duration_minutes: 8-12
tags: [offense, defense, transition, conditioning, live-play]
source_count: 1
last_updated: 2026-04-11
---

# Five-on-Five Change

## Objective
Simultaneously train offensive-to-defensive transition AND defensive-to-offensive transition by forcing instant role-switches on a coach's command.

## Setup
- 10 players, full court
- 5-on-5 live half-court play
- 1 coach positioned at the hashmark (line at the extension of the three-point arc) at the opposite end

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":28},{"role":"2","x":-18,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":-10,"y":10},{"role":"5","x":10,"y":10},{"role":"x1","x":2,"y":25},{"role":"x2","x":-14,"y":22},{"role":"x3","x":14,"y":22},{"role":"x4","x":-8,"y":12},{"role":"x5","x":6,"y":12}],"actions":[{"from":"1","to":"x1","type":"pass"},{"from":"x1","to":"x3","type":"pass"},{"from":"x2","to":"x4","type":"cut"},{"from":"x3","to":"x5","type":"cut"}],"notes":"Figure 17.9 shows a 5v5 half-court setup. Player 1 is at the top of the key with the ball; 2 and 3 are on the wings; 4 and 5 are near the elbows/high post area. Defenders x1–x5 are matched up nearby. The diagram shows arrow movements indicating the transition/change action — offense dropping back and defense pushing ahead. The coach (C) is shown at the left hashmark (extension of the three-point arc), which falls outside the half-court viewBox at roughly (-22, 0) and is not a player position. Action arrows in the diagram are somewhat ambiguous due to the transition nature of the drill; the depicted arrows suggest ball movement and player cuts during the change. Coordinates are approximated from the scan."}
```

## Execution
1. Offense plays **5-on-5 live** until the coach yells **"Change!"**
2. On "Change!": the **offense drops the ball** and **sprints back on defense**.
3. The **defense becomes the new offense** and picks up the ball.
4. Rule: **offense cannot guard the same player as before** (forces recognition and communication).
5. As soon as the new offense picks up the ball, it must **throw it ahead to the coach at the hashmark** on the other end.
6. This pass-ahead forces the old offense (now defense) to **get back quicker** and get to the level of the ball.
7. Now play **live 5-on-5 at the other end**.

## Coaching Points
- **"Change!"** — call it at unpredictable moments (mid-possession, post-shot, post-rebound).
- **"Find someone new"** — no one can guard their previous matchup; forces communication under pressure.
- The pass-ahead to the coach is non-negotiable — it simulates the transition trigger and forces defense to sprint.
- **Get to the level of the ball** — transition defense rule: everyone must match or exceed the ball's depth on the court.
- This drill is as much a conditioning drill as a tactical one — run it multiple possessions in a row.

## Progressions
1. **Beginner**: Walk through the role change rules before running live.
2. **Intermediate**: Run 5-10 "Change!" calls in one session; focus on communication on new matchups.
3. **Advanced**: Add a rule that the pass-ahead must be caught and shot within 3 seconds of arrival — simulates fast-break shot clock pressure.

## Concepts Taught
- [[transition-defense]] — sprint back, get level with the ball
- [[defensive-transition-principles]] — all 5 defenders must react simultaneously on "Change!"
- [[concept-productive-practice-structure]] — embedded in Frank's practice sequence

## Sources
- [S7, p.283] — the head coach, Five-on-Five Change drill, Figure 17.9
