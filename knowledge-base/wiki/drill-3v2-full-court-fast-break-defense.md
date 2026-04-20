---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 6-12
duration_minutes: 10-15
tags: [defense, transition, fast-break, 3v2, full-court, tandem-defense]
source_count: 1
last_updated: 2026-04-11
---

# Three-Against-Two Continuous Full-Court Fast-Break Drill

## Objective
Teach two defenders to contain three offensive players in a tandem defense until a third defensive teammate arrives to make it 3-on-3, developing fast-break containment, retreat principles, and the live-ball transition to half-court defense. [S1, pp.55-56]

## Setup
- Full court
- 3 offensive players, 2 defensive players initially, plus a third defender waiting at mid-court sideline
- For the continuous version (Figure 5.10): 12 players rotating through three groups

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/drill-3v2-full-court-fast-break-defense-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble",
    "dotted": "pass"
  },
  "phases": [
    {
      "label": "Figure 5.6 \u2014 Full court: three offensive players against two defenders plus trailer",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 3.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball-handler near half-court top"
        },
        {
          "role": "2",
          "x": 14.0,
          "y": 14.0,
          "jersey": "2",
          "side": "offense",
          "label": "right wing offensive player"
        },
        {
          "role": "3",
          "x": -14.0,
          "y": 14.0,
          "jersey": "3",
          "side": "offense",
          "label": "left wing offensive player"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "2",
          "type": "pass",
          "d": "M 0 3 C 6 8, 12 10, 14 14",
          "style": "dashed"
        },
        {
          "from": "x1",
          "to": "2",
          "type": "cut",
          "d": "M 0 20 C 6 18, 12 16, 14 14",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M -4 28 C 4 24, 10 20, 14 14",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "rim",
          "type": "cut",
          "d": "M -14 14 C -16 28, -12 38, 0 43",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 0.0,
          "y": 20.0,
          "jersey": "X1",
          "side": "defense",
          "label": "front tandem defender on ball"
        },
        {
          "role": "x2",
          "x": -4.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "back tandem defender helping"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 3.0,
        "possessed_by": "1"
      },
      "extras": [
        {
          "kind": "label",
          "text": "Full court drill \u2014 3 offensive vs 2 defenders with trailer arriving from mid-court sideline",
          "x": 0,
          "y": -2
        }
      ]
    },
    {
      "label": "Figure 5.7 \u2014 X2 in position to take away pass to 2 or run and jump or trap 3",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 14.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball-handler mid front court"
        },
        {
          "role": "2",
          "x": 18.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "right wing"
        },
        {
          "role": "3",
          "x": -14.0,
          "y": 10.0,
          "jersey": "3",
          "side": "offense",
          "label": "left wing with ball"
        }
      ],
      "actions": [
        {
          "from": "3",
          "to": "2",
          "type": "pass",
          "d": "M -14 10 C 0 12, 10 18, 18 22",
          "style": "dashed"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 4 24 C 10 23, 15 22, 18 22",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -8.0,
          "y": 18.0,
          "jersey": "X1",
          "side": "defense",
          "label": "front tandem on ball-side"
        },
        {
          "role": "x2",
          "x": 4.0,
          "y": 24.0,
          "jersey": "X2",
          "side": "defense",
          "label": "back tandem in help position"
        }
      ],
      "ball": {
        "x": -14.0,
        "y": 10.0,
        "possessed_by": "3"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X2 can: (a) take away pass to 2, (b) run and jump, or (c) trap 3",
          "x": 4,
          "y": 20
        }
      ]
    },
    {
      "label": "Figure 5.10 \u2014 Three-against-two continuous full-court fast-break drill: in a tandem defense the back defender takes first pass",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 24.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball-handler top of key area"
        },
        {
          "role": "2",
          "x": 20.0,
          "y": 5.0,
          "jersey": "2",
          "side": "offense",
          "label": "right sideline offensive player upper court"
        },
        {
          "role": "3",
          "x": -20.0,
          "y": 5.0,
          "jersey": "3",
          "side": "offense",
          "label": "left sideline offensive player upper court"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "rim",
          "type": "dribble",
          "d": "M 0 24 L 0 34",
          "style": "zigzag"
        },
        {
          "from": "1",
          "to": "x1",
          "type": "pass",
          "d": "M 0 34 C 1 35, 2 35, 2 34",
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
          "label": "back tandem near free throw line extended"
        },
        {
          "role": "x2",
          "x": 2.0,
          "y": 40.0,
          "jersey": "X2",
          "side": "defense",
          "label": "back tandem near basket"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 24.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "9/6",
          "x": -20,
          "y": 3
        },
        {
          "kind": "label",
          "text": "7 10 / 4",
          "x": 0,
          "y": 3
        },
        {
          "kind": "label",
          "text": "8 / 5",
          "x": 20,
          "y": 3
        },
        {
          "kind": "label",
          "text": "3",
          "x": -20,
          "y": 22
        },
        {
          "kind": "label",
          "text": "2",
          "x": 20,
          "y": 22
        },
        {
          "kind": "label",
          "text": "11",
          "x": 4,
          "y": 32
        },
        {
          "kind": "label",
          "text": "12",
          "x": 4,
          "y": 38
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "Continuous drill \u2014 groups of 3 rotate through offense/defense; 12 players numbered 1-12",
          "x": 0,
          "y": -2
        }
      ]
    }
  ],
  "notes": "[S1, pp.55-56] Figures 5.6, 5.7, and 5.10 depict a full-court 3v2 drill progressing to a continuous rotation drill. Fig 5.6: 3 offensive players advance against 2 tandem defenders (X1 front, X2 back); a trailing third defender arrives from the mid-court sideline once ball crosses half court. Fig 5.7: X2 is positioned to contest pass to 2, run-and-jump, or trap 3. Fig 5.10: continuous version using players numbered 1-12 positioned along sidelines at upper court; defenders (11, X1 and 12, X2) set in tandem near the basket; the zigzag arrow indicates dribble penetration and the dashed pass goes to the wing. Player and defender coordinates are approximate due to full-court layout being compressed into half-court viewBox; the diagrams in the book are shown as full-court but are here split into half-court views capturing the defensive front court portion of each drill. Arrow paths are approximated from the scan."
}
```

## Execution
1. Coach or player starts the drill. Two defenders (X1 and X2) try to contain and keep all three offensive players in front of them.
2. X1 jumps to the ball on the pass; X2 helps and follows the cutter attempting to split the defense.
3. The third defender is added from the mid-court sideline once the ball has passed half-court.
4. Once the third defender arrives, players play 3-against-3 until a score or a stop.
5. **Tandem defense rule:** the back defender takes the first attempted scoring pass to the wing (Figure 5.11).
6. For the **continuous version** (Figure 5.10): after each possession, the group that just played defense becomes the offense going the other way; three new defenders rotate in. [S1, pp.55-56]

## Coaching Points
- Two defenders must keep all three offensive players in front — do not go for steals prematurely
- The back defender in the tandem protects the basket; the front defender tries to slow the ball
- X2 must be in a position to: (a) take away the pass to 2, OR (b) run and jump, OR (c) trap 3 — reading the situation
- One-against-one full-court version (Figure 5.12): keep the dribbler down the sideline and out of the middle once the ball crosses midcourt
- Two-against-one retreat (Figure 5.11): one defender must retreat and keep both offensive players in front of him to slow or stop the break

## Progressions
1. **Beginner**: Walk through tandem positioning before adding live action
2. **Intermediate**: 3v2 as described with third defender arriving
3. **Advanced**: Continuous 3v2→2v1→1v1 (Figure 5.10) with 12 players and constant rotation

## Concepts Taught
- [[transition-defense]] — stopping fast breaks before early offense is initiated
- [[defensive-checklist-principles]] — run forward to a spot in front of the ball; help-and-recover
- [[defensive-practice-philosophy-herb-brown]] — game-situation simulation with numbers advantages

## Sources
- [S1, pp.55-57] — Full Court with Three Against Two, Figures 5.6, 5.7, 5.10, 5.11, 5.12