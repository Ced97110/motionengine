---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 4-8
duration_minutes: 10-15
tags: [defense, 2v2, full-court, help-defense, dribble-handoff, run-and-jump]
source_count: 1
last_updated: 2026-04-11
---

# Two-Against-Two Full-Court Drill

## Objective
Teach defenders to pressure the ball, slide through on dribble handoffs (DHOs), maintain a V-position to see both man and ball, and use run-and-jump tactics or trapping to contain two offensive players across the full court. [S1, pp.54-55]

## Setup
- Full court
- 2 offensive players, 2 defensive players
- A coach or player initiates with a pass from out of bounds
- No defensive players back to help (forces defenders to work without a safety net)

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/drill-2v2-full-court-defense-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble",
    "wavy": "slide/defensive-movement"
  },
  "phases": [
    {
      "label": "Figure 5.3 \u2014 X1 slides back to permit X2 through on the DHO",
      "players": [
        {
          "role": "1",
          "x": -10.0,
          "y": 22.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_mid_court_area"
        },
        {
          "role": "2",
          "x": 8.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing_mid"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "2",
          "type": "dribble",
          "d": "M -10 22 C -6 22, 2 22, 8 22",
          "style": "zigzag"
        },
        {
          "from": "x1",
          "to": "x2",
          "type": "cut",
          "d": "M -8 24 C -5 25, -3 26, -2 25",
          "style": "wavy"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M -2 25 C 2 24, 5 23, 8 22",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -8.0,
          "y": 24.0,
          "jersey": "X1",
          "side": "defense",
          "label": "left_of_1"
        },
        {
          "role": "x2",
          "x": -2.0,
          "y": 25.0,
          "jersey": "X2",
          "side": "defense",
          "label": "between_1_and_2"
        }
      ],
      "ball": {
        "x": -10.0,
        "y": 22.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X1 slides back to permit X2 through on the DHO",
          "target_role": "x1",
          "x": -8,
          "y": 27
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "PLAYER OR COACH",
          "x": -10,
          "y": -1
        }
      ]
    },
    {
      "label": "Figure 5.4 \u2014 X2 runs and jumps 1 as X1 runs to defend 2",
      "players": [
        {
          "role": "1",
          "x": -12.0,
          "y": 22.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "2",
          "x": 10.0,
          "y": 20.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing"
        }
      ],
      "actions": [
        {
          "from": "x2",
          "to": "1",
          "type": "cut",
          "d": "M -4 23 L -12 22",
          "style": "solid"
        },
        {
          "from": "x1",
          "to": "2",
          "type": "cut",
          "d": "M -10 24 C 0 23, 6 21, 10 20",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "2",
          "type": "dribble",
          "d": "M -12 22 C -4 21, 4 20, 10 20",
          "style": "zigzag"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -10.0,
          "y": 24.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1"
        },
        {
          "role": "x2",
          "x": -4.0,
          "y": 23.0,
          "jersey": "X2",
          "side": "defense",
          "label": "jumping_toward_1"
        }
      ],
      "ball": {
        "x": -12.0,
        "y": 22.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X2 runs and jumps 1 as X1 runs to defend 2",
          "target_role": "x2",
          "x": -4,
          "y": 27
        }
      ]
    },
    {
      "label": "Figure 5.5 \u2014 Two-against-two full-court drill: X1 slides in front of X2 to get in position to control 1",
      "players": [
        {
          "role": "1",
          "x": -12.0,
          "y": 18.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_mid_court"
        },
        {
          "role": "2",
          "x": 6.0,
          "y": 14.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_near_half"
        }
      ],
      "actions": [
        {
          "from": "x1",
          "to": "1",
          "type": "cut",
          "d": "M -8 20 C -10 19, -11 18, -12 18",
          "style": "wavy"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M -2 19 C 2 18, 4 16, 6 14",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "2",
          "type": "dribble",
          "d": "M -12 18 C -4 16, 2 15, 6 14",
          "style": "zigzag"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -8.0,
          "y": 20.0,
          "jersey": "X1",
          "side": "defense",
          "label": "sliding_front"
        },
        {
          "role": "x2",
          "x": -2.0,
          "y": 19.0,
          "jersey": "X2",
          "side": "defense",
          "label": "being_slid_past"
        }
      ],
      "ball": {
        "x": -12.0,
        "y": 18.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X1 slides in front of X2 to get in position to control 1",
          "target_role": "x1",
          "x": -8,
          "y": 23
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "PLAYER OR COACH",
          "x": 4,
          "y": -1
        }
      ]
    }
  ],
  "notes": "[S1, pp.54-55] Figures 5.3\u20135.5 \u2014 Two-against-two full-court defensive drill. Fig 5.3: X1 slides back to let X2 through on the dribble handoff (DHO) between 1 and 2. Fig 5.4: X2 runs and jumps at 1 while X1 rotates to cover 2; X2 positions in the middle of a V to see both man and ball after the inbound pass. Fig 5.5: X1 slides in front of X2 on the dribble exchange to get in position to control 1. Diagrams are set in the half-court area of a full-court representation; wavy lines represent defensive sliding movement, zigzag lines represent dribble paths. Exact arrow curvatures are approximated from the scan."
}
```

## Execution
1. Coach/player passes inbounds to offensive player 1. Defender X2 jumps in the direction of the pass, positioning himself in the **middle of a V** to see both his man (2) and the ball, and to be ready to fake at the ball to stop penetration. [S1, p.55]
2. Defenders slide through on a pass or DHO and try to turn the dribbler by pressuring the ball.
3. After several reps of sliding through, progress to **trapping the DHO** or running-and-jumping at the dribbler as defenders switch.
4. The offense may either (a) pass and split the defenders or (b) pass and pick the point of the ball. No long passes are permitted.
5. Each time a pass is made or a player dribbles away, the off-ball defender must be drawn toward the ball into a help-and-recover position.
6. As player 1 receives the ball, defender X2 slides through on the dribble exchange between offensive players 1 and 2. [S1, p.55]

## Coaching Points
- "Jump in the direction of the pass in the middle of a V to see both man and ball" — this is the foundational off-ball positioning principle
- Every pass or dribble movement must draw the off-ball defender toward the ball
- No reaching — pressure through positioning, not arm extension
- The absence of defensive help teaches urgency and self-reliance on the ball
- When trapping the DHO, make sure to send the trapped player back to his defender or uphill away from the goal

## Progressions
1. **Beginner**: Slide-through only — no trapping; establish positioning habits
2. **Intermediate**: Add trapping on DHOs; defenders switch
3. **Advanced**: Run-and-jump at the dribbler; add offense-can-split decision reads

## Concepts Taught
- [[defensive-checklist-principles]] — help-and-recover, V-positioning, defending DHOs
- [[defensive-practice-philosophy-herb-brown]] — progressive 1v1→2v2 build

## Sources
- [S1, pp.54-55] — Two-Against-Two Full Court, Figures 5.3, 5.4, 5.5