---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 6-12
duration_minutes: 8-12
tags: [defense, 3v3, full-court, communication, screens, transition, continuous]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: defensive-communication
    emphasis: primary
  - id: weak-side-help-defense
    emphasis: primary
  - id: defending-screens
    emphasis: secondary
  - id: transition-defense
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: secondary
  - region: glute_max
    emphasis: secondary
---

# Three-Against-Three Full-Court Drill

## Objective
Teach defenders to contain the offense by talking and helping each other through on-dribble exchanges, player exchanges, and weak-side screens across the full court, with weak-side defenders always drawn to the ball. [S1, p.56]

## Setup
- Full court
- 3 offensive players, 3 defensive players
- **Player inbounds version** (Figure 5.8): player 3 makes the initial inbounds pass against pressure
- **Coach inbounds version** (Figure 5.9): coach inbounds and may pass to any of the three offensive players
- For the continuous version (Figure 5.20): 12 players in four groups of 3; defensive group rotates to offense after crossing half-court

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/drill-3v3-full-court-defense-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 5.8 \u2014 Three-against-three full-court drill (player inbounds)",
      "players": [
        {
          "role": "3",
          "x": -22.0,
          "y": 47.0,
          "jersey": "3",
          "side": "offense",
          "label": "baseline inbounder left side"
        },
        {
          "role": "1",
          "x": 0.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "near free-throw lane"
        },
        {
          "role": "2",
          "x": 14.0,
          "y": 30.0,
          "jersey": "2",
          "side": "offense",
          "label": "right wing area"
        }
      ],
      "actions": [
        {
          "from": "3",
          "to": "1",
          "type": "pass",
          "d": "M -22 47 C -14 42, -6 40, 0 38",
          "style": "dashed"
        },
        {
          "from": "3",
          "to": "2",
          "type": "pass",
          "d": "M -22 47 C -4 40, 8 34, 14 30",
          "style": "dashed"
        }
      ],
      "defenders": [
        {
          "role": "x3",
          "x": -18.0,
          "y": 47.0,
          "jersey": "X3",
          "side": "defense",
          "label": "pressuring inbounder"
        },
        {
          "role": "x1",
          "x": 4.0,
          "y": 36.0,
          "jersey": "X1",
          "side": "defense",
          "label": "near player 1"
        },
        {
          "role": "x2",
          "x": 10.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "near player 2"
        }
      ],
      "ball": {
        "x": -22.0,
        "y": 47.0,
        "possessed_by": "3"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X3 may pressure ball or drop and help X1 and X2 defend against the first pass and then double the entry.",
          "x": -10,
          "y": 50
        }
      ]
    },
    {
      "label": "Figure 5.9 \u2014 Three-against-three full-court drill (coach inbounds)",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 36.0,
          "jersey": "1",
          "side": "offense",
          "label": "middle of paint area"
        },
        {
          "role": "2",
          "x": 14.0,
          "y": 42.0,
          "jersey": "2",
          "side": "offense",
          "label": "right baseline area"
        },
        {
          "role": "3",
          "x": -14.0,
          "y": 44.0,
          "jersey": "3",
          "side": "offense",
          "label": "left baseline area"
        }
      ],
      "actions": [
        {
          "from": "OB",
          "to": "1",
          "type": "pass",
          "d": "M -24 47 C -14 42, -4 38, 0 36",
          "style": "dashed"
        },
        {
          "from": "OB",
          "to": "2",
          "type": "pass",
          "d": "M -24 47 C -6 46, 6 44, 14 42",
          "style": "dashed"
        },
        {
          "from": "OB",
          "to": "3",
          "type": "pass",
          "d": "M -24 47 L -14 44",
          "style": "dashed"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 2.0,
          "y": 34.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding 1"
        },
        {
          "role": "x2",
          "x": 10.0,
          "y": 40.0,
          "jersey": "X2",
          "side": "defense",
          "label": "guarding 2"
        },
        {
          "role": "x3",
          "x": -10.0,
          "y": 42.0,
          "jersey": "X3",
          "side": "defense",
          "label": "guarding 3"
        }
      ],
      "ball": {
        "x": -24.0,
        "y": 47.0,
        "possessed_by": "OB"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "coach may pass to any one of three offensive players",
          "x": -5,
          "y": 50
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "COACH",
          "x": -24,
          "y": 47
        },
        {
          "kind": "screen_marker",
          "label": "coach inbounder OB symbol",
          "x": -24,
          "y": 47
        }
      ]
    },
    {
      "label": "Figure 5.20 \u2014 Three-against-three continuous fast-break drill (12 players, 4 groups)",
      "players": [
        {
          "role": "1",
          "x": -8.0,
          "y": 22.0,
          "jersey": "1",
          "side": "offense",
          "label": "group 1 \u2014 offense half-court left"
        },
        {
          "role": "2",
          "x": 0.0,
          "y": 18.0,
          "jersey": "2",
          "side": "offense",
          "label": "group 1 \u2014 offense half-court center"
        },
        {
          "role": "3",
          "x": 22.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "group 1 \u2014 offense half-court right"
        },
        {
          "role": "4",
          "x": -8.0,
          "y": 2.0,
          "jersey": "4",
          "side": "offense",
          "label": "group 4 \u2014 waiting at half-court left"
        },
        {
          "role": "5",
          "x": 0.0,
          "y": 2.0,
          "jersey": "5",
          "side": "offense",
          "label": "group 4 \u2014 waiting at half-court center"
        },
        {
          "role": "6",
          "x": 14.0,
          "y": 2.0,
          "jersey": "6",
          "side": "offense",
          "label": "group 4 \u2014 waiting at half-court right"
        },
        {
          "role": "7",
          "x": -22.0,
          "y": -1.0,
          "jersey": "7",
          "side": "offense",
          "label": "group 2 \u2014 far end sideline left"
        },
        {
          "role": "8",
          "x": 0.0,
          "y": -1.0,
          "jersey": "8",
          "side": "offense",
          "label": "group 2 \u2014 far end top center"
        },
        {
          "role": "9",
          "x": 22.0,
          "y": -1.0,
          "jersey": "9",
          "side": "offense",
          "label": "group 2 \u2014 far end sideline right"
        },
        {
          "role": "10",
          "x": -22.0,
          "y": -3.0,
          "jersey": "10",
          "side": "offense",
          "label": "group 3 \u2014 sideline label"
        },
        {
          "role": "11",
          "x": 0.0,
          "y": -3.0,
          "jersey": "11",
          "side": "offense",
          "label": "group 3 \u2014 top label"
        },
        {
          "role": "12",
          "x": 22.0,
          "y": -3.0,
          "jersey": "12",
          "side": "offense",
          "label": "group 3 \u2014 right label"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "rim",
          "type": "cut",
          "d": "M -8 22 L -8 43",
          "style": "solid"
        },
        {
          "from": "2",
          "to": "rim",
          "type": "dribble",
          "d": "M 0 18 L 0 43",
          "style": "zigzag"
        },
        {
          "from": "3",
          "to": "rim",
          "type": "cut",
          "d": "M 22 22 L 22 43",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -8.0,
          "y": 30.0,
          "jersey": "X1",
          "side": "defense",
          "label": "new defenders waiting at half-court left"
        },
        {
          "role": "x2",
          "x": 2.0,
          "y": 30.0,
          "jersey": "X2",
          "side": "defense",
          "label": "new defenders waiting center"
        },
        {
          "role": "x3",
          "x": 14.0,
          "y": 30.0,
          "jersey": "X3",
          "side": "defense",
          "label": "new defenders waiting right"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 18.0,
        "possessed_by": "2"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Groups labeled 1-12; defensive group rotates to offense after crossing half-court; 3 new defenders wait at half-court.",
          "x": 0,
          "y": 50
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "4 groups of 3; rotate continuously for 8-12 min",
          "x": 0,
          "y": 25
        }
      ]
    }
  ],
  "notes": "[S1, pp.56-59] [S1, pp.56, 59] Three figures captured: Fig 5.8 (player inbounds, X3 may pressure or drop), Fig 5.9 (coach inbounds, can pass to any of three offensive players), Fig 5.20 (continuous 3v3 full-court fast-break drill with 12 players in 4 groups of 3, rotating for 8-12 min). Full-court diagrams mapped to half-court viewBox as best approximation; player/group positions are approximate since these are full-court formations shown at reduced scale. The x/y positions for groups 2-4 (numbers 7-12) near half-court line are approximated given the full-court nature of Fig 5.20. Zigzag line style in Fig 5.20 indicates dribble drive to basket."
}
```

## Execution
1. Ball is initiated (player or coach inbounds).
2. Three defenders try to contain all three offensive players, emphasizing communication: "Screen left!" "Help right!"
3. Defenders help each other through on-dribble exchanges and player exchanges.
4. Weak-side defenders must always be drawn to the ball.
5. Defenders communicate through screens on the weak side of the court.
6. **Continuous version (Figure 5.20):** the defensive team rotates to offense as they cross half-court; three new defenders wait at half-court and rotate in. Run for 8-12 minutes with constant rotation. [S1, pp.56, 59]

## Coaching Points
- "Contain the offense by talking and helping each other" — communication is the emphasis, not just individual technique
- Weak-side defenders must be drawn toward the ball on every pass and dribble action
- X3 on inbound: may pressure the ball OR drop and help X1 and X2 defend the first pass, then double the entry
- In the continuous version, players must sprint transitions without rest — this is also a conditioning drill
- "We run this transition defense drill for 8 to 12 minutes with the constant rotation of players" [S1, p.59]

## Progressions
1. **Beginner**: 3v3 half-court to establish communication habits
2. **Intermediate**: 3v3 full-court with player inbound
3. **Advanced**: Continuous 3v3 (Figure 5.20) — 8-12 minutes with rotating groups

## Concepts Taught
- [[defensive-checklist-principles]] — weak-side defenders drawn to ball; helping through screens
- [[defensive-practice-philosophy-herb-brown]] — re-creating game situations; competitive continuous drills
- [[transition-defense]] — defending after crossing half-court with fresh defenders

## Sources
- [S1, pp.56, 59] — Three-Against-Three Full-Court Drill, Figures 5.8, 5.9, 5.20