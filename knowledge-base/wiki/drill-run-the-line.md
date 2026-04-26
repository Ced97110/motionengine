---
type: drill
level: beginner
positions: [PG, SG, SF]
players_needed: 2
duration_minutes: 5-10
tags: [shooting, conditioning, footwork, elbow, jump-shot, catch-and-shoot]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: catch-and-shoot
    emphasis: primary
  - id: jump-shot-footwork
    emphasis: primary
  - id: one-two-step-footwork
    emphasis: secondary
  - id: explosive-first-step
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: secondary
  - region: ankle_complex
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Run the Line Drill

## Objective
Build shooting footwork and conditioning simultaneously by requiring players to sprint between elbows and catch-and-shoot after each sprint.

## Setup
- Half court
- Coach under the basket with a ball
- Player starts at the left elbow

```json name=diagram-positions
{"players":[{"role":"C","x":0,"y":43},{"role":"1","x":-8,"y":29}],"actions":[{"from":"C","to":"1","type":"pass"},{"from":"1","to":"right_elbow","type":"cut"}],"notes":"Figure 19.8 shows the starting formation: Coach (C) is under the basket at roughly (0, 43), and the player starts at the left elbow (-8, 29). The diagram depicts a pass from the coach to the player at the left elbow, followed by a sprint/cut arrow from the left elbow to the right elbow. The right elbow destination is the 'right_elbow' anchor (8, 29). The dashed arc lines indicate the player's running path between elbows after shooting."}
```

## Execution
1. Coach passes the ball to the player at the left elbow.
2. Player catches, takes a jump shot.
3. Player immediately sprints to the right elbow.
4. Coach (or rebounder) retrieves and passes to the player at the right elbow.
5. Repeat — sprint back and forth, shooting a jump shot at each elbow.
6. Run for a set number of shots or a set time.

## Coaching Points
- Sprint between elbows — no jogging
- Feet must be set before releasing the shot — don't let the sprint momentum carry into a rushed release
- Hold the follow-through on every shot
- "The quality of your footwork determines the quality of your shot" — this drill exposes footwork fatigue under conditioning stress [S7, p.308]
- Coach should challenge players to maintain perfect form as they fatigue

## Progressions
1. **Beginner:** Walk/jog between elbows; focus purely on footwork
2. **Intermediate:** Full sprint; timed session
3. **Advanced:** Add a shot fake before shooting at each elbow; or add a one-dribble pull-up off the sprint

## Concepts Taught
- [[concept-player-development-philosophy-eastman]] — game-speed reps, conditioning→skills chain
- [[concept-skills-conditioning]] — shooting under fatigue transfers to late-game situations
- [[concept-one-two-step-footwork]] — landing footwork after a sprint

## Sources
- [S7, p.308] — Kevin Eastman, Chapter 19: Player Development
