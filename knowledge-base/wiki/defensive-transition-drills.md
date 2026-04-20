---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 8-10
duration_minutes: 20-30
tags: [defense, transition, fast-break, conditioning, communication, rebounding]
source_count: 1
last_updated: 2026-04-11
---

# Defensive Transition Drills

## Objective
Teach players to stop the ball, protect the goal, communicate matchups, and prevent easy layups in every numerical disadvantage situation from 2v1 through 5v5. [S1, pp.169-173]

## Setup
- Full court
- Divide squad into groups of five
- Equipment: basketballs, cones optional

## Execution

### Drill 1: Continuous 2v1 → 3v2 → 4v3 → 5v4 → 5v5
1. Begin with a 2v1 fast break situation. The one defender must stop the ball and protect the goal.
2. When possession changes (score, rebound, or turnover), immediately transition to 3v2. The two defenders now set up tandem defense.
3. Continue progressing: 4v3, then 5v4, then 5v5.
4. **This drill is continuous** — it does not stop until all five sequences are completed.
5. Emphasize talking on defense throughout every sequence. [S1, pp.169, 172]

### Drill 2: Four-Against-Four Full-Court Transition Drill (Coach-Triggered)
1. Set up two equal lines of four players. Defenders line up on the foul line facing the baseline; offensive players line up on the baseline facing the opposite basket.
2. Coach passes the ball to an offensive player. The defensive player directly in front of that offensive player must run and **touch the foul line** before sprinting back in defensive transition.
3. The four offensive players immediately run a 4v3 fast break.
4. The three remaining defenders must get back, match up, stop the ball, and protect the goal.
5. The trailing fourth defender (who touched the foul line) sprints to get level with the ball and picks up the free offensive player — who is probably not his original opponent.
6. Transition ends when the offensive group scores OR the defense recovers/rebounds. [S1, p.173]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defensive-transition-drills-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass"
  },
  "phases": [
    {
      "label": "Figure 11.1",
      "players": [
        {
          "role": "1",
          "x": 2.0,
          "y": 3.0,
          "jersey": "1",
          "side": "offense",
          "label": "top_of_key_area"
        },
        {
          "role": "2",
          "x": 13.0,
          "y": 3.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing_near_half"
        },
        {
          "role": "3",
          "x": -4.0,
          "y": 3.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_of_center_near_half"
        },
        {
          "role": "4",
          "x": -13.0,
          "y": 3.0,
          "jersey": "4",
          "side": "offense",
          "label": "far_left_near_half"
        }
      ],
      "actions": [
        {
          "from": "COACH",
          "to": "4",
          "type": "pass",
          "d": "M -22 10 L -13 3",
          "style": "dashed"
        },
        {
          "from": "4",
          "to": "rim",
          "type": "cut",
          "d": "M -13 3 C -16 15, -20 28, -18 42",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "rim",
          "type": "cut",
          "d": "M -4 3 C -5 14, -6 26, -5 38",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "rim",
          "type": "cut",
          "d": "M 2 3 C 2 10, 2 20, 2 38",
          "style": "solid"
        },
        {
          "from": "2",
          "to": "rim",
          "type": "cut",
          "d": "M 13 3 C 13 12, 13 24, 13 42",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "baseline",
          "type": "cut",
          "d": "M 10 22 L 10 47",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 0.0,
          "y": 22.0,
          "jersey": "x1",
          "side": "defense",
          "label": "center_paint"
        },
        {
          "role": "x2",
          "x": 10.0,
          "y": 22.0,
          "jersey": "x2",
          "side": "defense",
          "label": "right_wing_mid"
        },
        {
          "role": "x3",
          "x": -7.0,
          "y": 22.0,
          "jersey": "x3",
          "side": "defense",
          "label": "left_elbow"
        },
        {
          "role": "x5",
          "x": 18.0,
          "y": 22.0,
          "jersey": "x5",
          "side": "defense",
          "label": "far_right_mid"
        }
      ],
      "ball": {
        "x": -22.0,
        "y": 10.0,
        "possessed_by": "COACH"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "4",
          "x": -13,
          "y": 1
        },
        {
          "kind": "label",
          "text": "3",
          "x": -4,
          "y": 1
        },
        {
          "kind": "label",
          "text": "1",
          "x": 2,
          "y": 1
        },
        {
          "kind": "label",
          "text": "2",
          "x": 13,
          "y": 1
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "COACH",
          "x": -24,
          "y": 12
        }
      ]
    }
  ],
  "notes": "[S1, p.171] Figure 11.1 \u2014 Full-court 4v4 coach-triggered transition defense drill. Coach (with ball) stands on the left sideline near half-court. Four offensive players (1\u20134) line up near half-court; four defenders (x1\u2013x5, noting x4 is the called-out defender) line up in the paint/mid-court area facing them. Coach passes to an offensive player and calls a defender's number (x2 in the diagram caption); that defender sprints to touch the baseline before recovering. The remaining three defenders stop the fast break using big-to-big matchup principles. The diagram is a full-court view; coordinates mapped into the half-court viewBox with the offensive players near y\u22483 (top/half-court) and the basket at y\u224843. X2's sprint-to-baseline arrow runs down the right side. Slight scan ambiguity on exact x3/x1 overlap near the paint \u2014 coordinates approximated from diagram positions."
}
```

### Drill 3: Five-Against-Five Full-Court Transition Drill
1. Same setup and trigger as the 4v4 drill above, but with five players per side.
2. If the offense scores, they **immediately** switch to defense and the former defense transitions to offense.
3. On made shots: run a set play from the new offense.
4. On misses/steals: look to fast break or run secondary/early offense. [S1, p.173]

### Drill 4: Fast Break Following a Made or Missed Free Throw
1. Set up your defensive team at the free-throw line as if in a game.
2. Shoot the free throw (make or miss).
3. The offensive team immediately runs at the defensive team, attempting to score before the defense can set up.
4. Defense must stop transition after both a make and a miss — different alignment challenges for each.
5. This drill also creates opportunities to practice full- and half-court pressing defenses against various offensive free-throw line alignments. [S1, p.173]

### Drill 5: Suggested Transition Defense Scenarios
- Full-court 5v5 with players matched against each other
- 4 defenders vs. 5 offensive players; a fifth defensive trailer is added once the ball crosses half-court
- 5v5 after rebounding a missed shot, causing a deflection, or a turnover [S1, p.169]

## Coaching Points
- **"Stop the ball first!"** — The first man back must cover the goal, not find his man.
- **"Talk, talk, talk!"** — Every defensive switch and matchup must be communicated verbally.
- **"Level with the ball!"** — Retreating defenders must get at least to the line of the ball before picking up their opponent.
- Big men must perform big-to-big match-up — the first big back covers the first offensive big, regardless of assignment.
- No aimless backcourt gambling for steals — it creates worse numerical disadvantages.
- The third man back always fills the weak-side area to form a defensive triangle once the first pass is made.

## Progressions
1. **Beginner**: Walk through tandem defense rules in 2v1 and 3v2 situations. Focus on verbal communication.
2. **Intermediate**: 4v4 coach-triggered drill at moderate pace; defender must touch the foul line before recovering.
3. **Advanced**: Live 5v5 transition with instant role-reversal on scores; add free-throw trigger drill at game speed.

## Concepts Taught
- [[transition-defense-principles]] — the principles these drills directly train
- [[full-court-press-defense]] — the full-court press transitions into these same defensive assignments
- [[concept-defensive-rebounding-footwork]] — five-man defensive rebounding as a prerequisite to controlled transition

## Sources
- [S1, pp.169-173] — Herb Brown, Chapter 11: Transition Defense and Drills
