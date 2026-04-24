---
type: drill
level: beginner
positions: [PG, SG, SF, PF, C]
players_needed: 2-12
duration_minutes: 10-15
tags: [defense, 1v1, footwork, on-ball-defense, full-court]
source_count: 1
last_updated: 2026-04-11
---

# One-Against-One Zigzag Drill

## Objective
Teach the defender how to keep the dribbler in front of him and force the dribbler to use a crossover dribble to change direction as many times as possible before reaching the far baseline. [S1, p.54]

## Setup
- Full court
- Pairs of players (1 offensive, 1 defensive)
- Can run multiple pairs simultaneously on the same court
- No cones required

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/drill-1v1-zigzag-defense-0.png",
  "court_region": "full",
  "legend": {
    "zigzag": "dribble",
    "solid": "cut"
  },
  "phases": [
    {
      "label": "Figure 5.2 \u2014 One-against-one zigzag drill",
      "players": [
        {
          "role": "1",
          "x": -6.0,
          "y": 2.0,
          "jersey": "O",
          "side": "offense",
          "label": "offensive player top left start"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "weak_side",
          "type": "dribble",
          "d": "M -6 2 C -2 6, 8 8, 10 12 C 12 16, 0 18, -2 22 C -4 26, 8 28, 10 32 C 12 36, 0 38, -2 42 C -4 44, 4 46, 6 47",
          "style": "zigzag"
        },
        {
          "from": "x1",
          "to": "weak_side",
          "type": "cut",
          "d": "M -4 2 C 2 7, 9 9, 10 12 C 8 16, -1 19, -2 22 C 0 26, 9 29, 10 32 C 8 36, -1 39, -2 42 C 0 44, 5 46, 6 47",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -4.0,
          "y": 2.0,
          "jersey": "X",
          "side": "defense",
          "label": "defender top left start"
        }
      ],
      "annotations": [
        {
          "kind": "label",
          "text": "PLAYER OR COACH",
          "x": -8,
          "y": -1
        }
      ],
      "extras": [
        {
          "kind": "legend_symbol",
          "symbol": "zigzag",
          "meaning": "dribble",
          "label": "zigzag arrow = dribble path",
          "x": -10,
          "y": 5
        }
      ]
    }
  ],
  "notes": "[S1, p.54] Figure 5.2 \u2014 Full-court 1-on-1 zigzag drill. The diagram spans the full court; the offensive player dribbles in a diagonal zigzag pattern from one end to the other while the defender slides to stay in front. Zigzag arrows represent the dribble path; solid arrows trace the defender's mirroring slide path. Only one offensive/defensive pair is depicted (the book shows pairs stacked on both sides of the court for a multi-player version). The court is shown in full but this tool uses the half-court viewBox; y coordinates have been compressed to fit [-3..47] with half-court at y\u22480 and far baseline at y\u224847. Path coordinates are approximate due to the full-court compression into the half-court viewBox."
}
```

## Execution
1. Run the drill first WITHOUT a basketball to establish footwork, then WITH a basketball.
2. Offensive player dribbles freely, trying to go straight to the far baseline.
3. Defensive player slides to a spot in front of the dribbler's outside hand to force a crossover dribble and direction change.
4. After the dribbler changes direction with a crossover, the defender immediately slides to a new spot in front of the new outside hand.
5. Continue forcing direction changes until the offense reaches the far baseline.
6. Players switch offense and defense and repeat going back the other way. [S1, p.54]

## Coaching Points
- "Get to a spot in front of the dribbler's outside hand" — not behind or to the side
- Stay low; don't reach for the ball
- Move feet first; hands follow
- The goal is direction changes, not steals — teach control, not gambling
- The no-ball version first is critical for establishing proper footwork before adding dribble decisions

## Progressions
1. **Beginner**: Walk-through without ball; defender shadows the offensive player
2. **Intermediate**: With ball at moderate pace; no dribble limit
3. **Advanced**: Full game speed; add a consequence (sprint) if the offensive player reaches the far baseline without a direction change forced

## Concepts Taught
- [[defensive-checklist-principles]] — forcing the dribbler to change direction; keeping the ball in front

## Sources
- [S1, p.54] — One-Against-One Zigzag Drill, Figure 5.2