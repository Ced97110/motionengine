---
type: drill
level: beginner
positions: [PG, SG, SF, PF, C]
players_needed: 4-12
duration_minutes: 10-15
tags: [defense, footwork, lateral-movement, conditioning, slides]
source_count: 1
last_updated: 2026-04-11
---

# Defensive Slide and Change-of-Direction Drill

## Objective
Build defensive lateral sliding footwork, the ability to pivot and change direction, and the conditioning to sprint-and-slide repeatedly across the full court. [S1, p.53]

## Setup
- Full court
- 7 chairs or cones spaced at intervals across the full court (see Figure 5.1 — cones positioned at each sideline at 3 different horizontal levels plus the mid-court area)
- Players line up at one baseline in a defensive stance, one behind the other
- A coach or manager stationed at each cone to check execution

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/drill-defensive-slide-change-direction-0.png",
  "court_region": "half",
  "legend": {
    "zigzag": "slide",
    "solid": "sprint/run"
  },
  "phases": [
    {
      "label": "Figure 5.1 \u2014 Cone or chair drill",
      "players": [
        {
          "role": "1",
          "x": -20.0,
          "y": 2.0,
          "jersey": "1",
          "side": "offense",
          "label": "player_start_baseline"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M -20 2 C -14 4, -10 6, -8 8",
          "style": "zigzag"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M -8 8 C -2 8, 4 8, 8 10",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M 8 10 C 14 12, 18 14, 20 16",
          "style": "zigzag"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M 20 16 C 14 18, 8 20, 0 22",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M 0 22 C -8 24, -14 26, -20 28",
          "style": "zigzag"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M -20 28 C -14 30, -6 32, 0 34",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M 0 34 C 6 36, 14 38, 20 40",
          "style": "zigzag"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M 20 40 C 12 42, 4 44, 0 46",
          "style": "solid"
        }
      ],
      "annotations": [
        {
          "kind": "label",
          "text": "2 3 4 5 6 7 8 9",
          "x": 0,
          "y": -2,
          "target_role": "1"
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "PLAYER SLIDES",
          "x": -14,
          "y": 5
        },
        {
          "kind": "label",
          "text": "RUNS",
          "x": 4,
          "y": 9
        },
        {
          "kind": "label",
          "text": "RUNS",
          "x": 12,
          "y": 19
        },
        {
          "kind": "label",
          "text": "SLIDES",
          "x": 4,
          "y": 23
        },
        {
          "kind": "label",
          "text": "SLIDES",
          "x": -10,
          "y": 27
        },
        {
          "kind": "label",
          "text": "RUNS",
          "x": -8,
          "y": 33
        },
        {
          "kind": "label",
          "text": "SLIDES",
          "x": 8,
          "y": 37
        },
        {
          "kind": "label",
          "text": "RUNS",
          "x": 10,
          "y": 43
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": -8,
          "y": 8
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": 20,
          "y": 16
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": -20,
          "y": 28
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": 0,
          "y": 34
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": 20,
          "y": 40
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": -28,
          "y": 16,
          "label": "left_sideline_pivot"
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": 28,
          "y": 16,
          "label": "right_sideline_pivot"
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": -28,
          "y": 40,
          "label": "left_sideline_pivot_2"
        },
        {
          "kind": "label",
          "text": "PIVOTS",
          "x": 28,
          "y": 40,
          "label": "right_sideline_pivot_2"
        },
        {
          "kind": "legend_symbol",
          "symbol": "zigzag",
          "meaning": "defensive slide (lateral)"
        },
        {
          "kind": "legend_symbol",
          "symbol": "solid",
          "meaning": "sprint/run between cones"
        },
        {
          "kind": "court_boundary",
          "label": "full_court"
        }
      ]
    }
  ],
  "notes": "[S1, pp.53-54] Figure 5.1 \u2014 Full-court cone/chair drill. Seven cones (represented as squares in the diagram) are spaced at alternating sideline and mid-court positions across the full court. The single defender (labeled 1, with a queue of additional players 2\u20139 behind at the starting baseline) slides laterally in a zigzag path between cones, pivots at each cone, then sprints to the next cone, alternating slide/sprint sequences until reaching the far baseline. The diagram uses zigzag lines for defensive slides and straight arrows for sprints/runs. \"PIVOTS\" labels mark each cone position. Sideline cone positions are also labeled \"PIVOTS.\" This is a full-court drill; the viewBox coords here are compressed to the half-court range, so cone positions are approximated across the y-axis to represent the full-court spacing. Ambiguity: exact lateral (x) positions of cones varied across the diagram; approximated from the scan."
}
```

## Execution
1. First player assumes defensive stance facing the nearest basket, knees bent, low center of gravity.
2. Player slides laterally with knees bent, staying low, toward the first cone.
3. Upon reaching the cone, player pivots and changes direction, then quickly sprints to the next cone.
4. At the next cone, player resumes the defensive slide position and slides laterally to the following cone.
5. Continue alternating run-and-slide sequences, changing direction at each cone, until reaching the opposite baseline.
6. The next player in line begins only after the player in front reaches the first cone.
7. Repeat the drill 4–5 times per player. [S1, pp.53-54]

## Coaching Points
- Stay low throughout every slide — "maintain a low center of gravity"
- Knees must stay bent during slides; do not stand up
- Pivots must be sharp and decisive — no false steps
- Sprints between cones are at full speed
- Coach/manager at each cone checks for correct running, sliding, and pivoting
- This drill teaches players how to keep an opponent in front of them AND how to run, pivot, release, catch up to, and turn a quicker opponent [S1, p.54]

## Progressions
1. **Beginner**: Walk through the pattern without cones to learn pivot and direction change
2. **Intermediate**: Full speed with cones as described; 4-5 repetitions
3. **Advanced**: Add a live ball at the final cone — after completing the drill, go directly into a 1-on-1 closeout

## Concepts Taught
- [[defensive-checklist-principles]] — lateral movement and staying in front of the dribbler
- [[defensive-practice-philosophy-herb-brown]] — full-court conditioning integrated into defensive practice

## Sources
- [S1, pp.53-54] — Defensive Slide and Change-of-Direction Drill, Figure 5.1