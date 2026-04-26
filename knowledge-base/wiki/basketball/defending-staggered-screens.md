---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, off-ball-screens, staggered-screens, man-to-man, double-screens]
source_count: 1
last_updated: 2026-04-11
---

# Defending Staggered Screens

## Summary
Staggered screens — two sequential screens set for one cutter — are among the most difficult off-ball defensive challenges. Herb Brown's system uses a trail-then-shortcut approach for horizontal/vertical/diagonal staggered sets, while the Horns (elbow area) staggered double screen requires a topside or over-and-through approach with tandem screener defense. [S1, pp.137-138, 140-141]

## When to Use
- Any time the offense runs double screens (staggered horizontal, vertical, or diagonal sets)
- Horns/elbow-area staggered actions
- Double-double screen actions
- Late-game situations where the best shooter is running off staggered sets

## Key Principles
1. **Trail the first screen, shortcut the second** — standard approach for horizontal/vertical/diagonal staggered sets
2. **Stand up the screeners** — the farther out you can hold the screeners, the better the chances of defending successfully
3. **Switch up the line** — if the screener's defender is beaten on a staggered screen, the screen recipient's defender calls the switch to alert his teammate to step out and take over
4. **On-ball pressure is a must** — staggered screens only work if the ball handler can make the pass; pressure disrupts timing
5. **Tandem defense for screeners** — screener's defenders play tandem in the lane, allowing each cutter's defender to navigate through

## Variations

### Staggered Horizontal, Vertical, or Diagonal Screens
- Stand up screeners
- Bump/body the cutter
- Force the cutter to go over screens if possible
- Trail on the first screen, go through or shortcut the second
- If screener's defender is beaten: screen recipient's defender calls a switch up the line
[S1, p.137]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-staggered-screens-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "screen"
  },
  "phases": [
    {
      "label": "Figure 9.24",
      "players": [
        {
          "role": "1",
          "x": -2.0,
          "y": 30.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball_handler_top_of_key"
        },
        {
          "role": "2",
          "x": 10.0,
          "y": 18.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing_area"
        },
        {
          "role": "3",
          "x": -22.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "4",
          "x": 7.0,
          "y": 38.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_low_block"
        },
        {
          "role": "5",
          "x": 5.0,
          "y": 28.0,
          "jersey": "5",
          "side": "offense",
          "label": "right_elbow_area"
        }
      ],
      "actions": [
        {
          "from": "2",
          "to": "rim",
          "type": "cut",
          "d": "M 10.00 18.00 C 8.00 24.00, 6.00 32.00, 4.00 40.00",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 8.00 24.00 C 7.00 28.00, 6.00 33.00, 5.50 38.00",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "2",
          "type": "pass",
          "d": "M -2.00 30.00 L 6.00 38.00",
          "style": "dashed"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -4.0,
          "y": 34.0,
          "jersey": "X1",
          "side": "defense",
          "label": "below_ball_handler"
        },
        {
          "role": "x2",
          "x": 8.0,
          "y": 24.0,
          "jersey": "X2",
          "side": "defense",
          "label": "trailing_2_near_elbow"
        },
        {
          "role": "x3",
          "x": -16.0,
          "y": 22.0,
          "jersey": "X3",
          "side": "defense",
          "label": "left_wing_denial"
        },
        {
          "role": "x4",
          "x": 5.0,
          "y": 36.0,
          "jersey": "X4",
          "side": "defense",
          "label": "fronting_4_low_block"
        },
        {
          "role": "x5",
          "x": 4.0,
          "y": 30.0,
          "jersey": "X5",
          "side": "defense",
          "label": "tandem_with_x4_mid_lane"
        }
      ],
      "ball": {
        "x": -2.0,
        "y": 30.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X4 and X5 play tandem defense in the lane",
          "x": 5,
          "y": 33
        },
        {
          "kind": "label",
          "text": "X2 trails first screen, cuts in front of X4 to deny 2",
          "x": 8,
          "y": 26
        }
      ]
    }
  ]
}
```

### Horns (Elbow Area) Staggered Double Screen
Two options for the cutter's defender:
- **Option A**: Play topside, force cutter low below both screens
- **Option B**: Go over the first screen and through on the second — provided screener's defenders step out and slow the cutter
Screener's defenders (X4 and X5) play tandem defense in the lane. [S1, pp.140-141]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-staggered-screens-1.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble",
    "wavy": "screen"
  },
  "phases": [
    {
      "label": "Figure 9.32 \u2014 Horns (elbow area) staggered double screens",
      "players": [
        {
          "role": "1",
          "x": -2.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "top of key / nail area"
        },
        {
          "role": "2",
          "x": -8.0,
          "y": 20.0,
          "jersey": "2",
          "side": "offense",
          "label": "left elbow area"
        },
        {
          "role": "3",
          "x": 22.0,
          "y": 14.0,
          "jersey": "3",
          "side": "offense",
          "label": "right wing"
        },
        {
          "role": "4",
          "x": -5.0,
          "y": 27.0,
          "jersey": "4",
          "side": "offense",
          "label": "left elbow / lane"
        },
        {
          "role": "5",
          "x": -10.0,
          "y": 23.0,
          "jersey": "5",
          "side": "offense",
          "label": "left elbow area / near 2"
        }
      ],
      "actions": [
        {
          "from": "2",
          "to": "3",
          "type": "cut",
          "d": "M -8 20 C -2 16, 8 14, 22 14",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "3",
          "type": "cut",
          "d": "M -6 21 C 0 18, 10 15, 20 14",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "rim",
          "type": "cut",
          "d": "M 22 14 C 18 22, 10 32, 4 42",
          "style": "solid"
        },
        {
          "from": "x3",
          "to": "rim",
          "type": "cut",
          "d": "M 18 15 C 14 24, 8 33, 3 42",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "3",
          "type": "pass",
          "d": "M -2 38 C 6 30, 14 20, 22 14",
          "style": "dashed"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "dribble",
          "d": "M -2 38 L 6 36",
          "style": "zigzag"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 0.0,
          "y": 36.0,
          "jersey": "X1",
          "side": "defense",
          "label": "nail / elbow defender"
        },
        {
          "role": "x2",
          "x": -6.0,
          "y": 21.0,
          "jersey": "X2",
          "side": "defense",
          "label": "trails 2 through screens"
        },
        {
          "role": "x3",
          "x": 18.0,
          "y": 15.0,
          "jersey": "X3",
          "side": "defense",
          "label": "follows 3 toward goal"
        },
        {
          "role": "x4",
          "x": -3.0,
          "y": 28.0,
          "jersey": "X4",
          "side": "defense",
          "label": "tandem in lane"
        },
        {
          "role": "x5",
          "x": -9.0,
          "y": 24.0,
          "jersey": "X5",
          "side": "defense",
          "label": "tandem in lane"
        }
      ],
      "ball": {
        "x": -2.0,
        "y": 38.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X2 locks and trails 2 on first screen by 5, goes through second screen by 4",
          "x": -8,
          "y": 18
        },
        {
          "kind": "label",
          "text": "X3 goes to goal with 3, tilts back to box",
          "x": 20,
          "y": 12
        },
        {
          "kind": "label",
          "text": "X1 plays nail or elbow",
          "x": 0,
          "y": 34
        },
        {
          "kind": "label",
          "text": "X4 and X5 play tandem defense in lane",
          "x": -5,
          "y": 25
        }
      ],
      "extras": [
        {
          "kind": "screen_marker",
          "target_role": "5",
          "x": -10,
          "y": 23,
          "label": "first screen by 5 for 2"
        },
        {
          "kind": "screen_marker",
          "target_role": "4",
          "x": -5,
          "y": 27,
          "label": "second screen by 4 for 2"
        }
      ]
    }
  ],
  "notes": "[S1, p.140] Figure 9.32 \u2014 Horns (elbow area) staggered double screens. X2 locks and trails 2 on the first screen by 5, then goes through the second screen by 4. X3 goes to the goal with 3 and tilts back to the box. X1 plays the nail or elbow. X4 and X5 play tandem defense in the lane. Offensive players 4 and 5 are set at left-elbow area as the two staggered screeners. Player 2 cuts off both screens toward the right wing. Dashed arrow from 1 indicates pass option to 2/3. Zigzag at 1 indicates dribble action. Some arrow paths are approximated due to diagram density and scan resolution."
}
```

### Double-Doubles
Lock and trail while screener's defenders screen the screeners — enabling cutter's defenders to maintain lock-and-trail. Stand screeners up as far from the cutter as possible. May switch the second screen in each double or shoot the gap. On-ball pressure is essential. [S1, p.146]

## Player Responsibilities
- **Cutter's defender**: Trail first screen; shortcut or go through second screen. Lock and trail — stay on outside shoulder and hip.
- **First screener's defender**: Stand up the screener to create a window for cutter's defender. Then play tandem in the lane.
- **Second screener's defender**: Stand up the second screener. Be in position to switch up the line if needed. Must not overrun and screen own teammate.
- **Ball defender**: Pressure the ball — disrupt the timing of the pass to the cutter exiting the staggered screens.

## Common Mistakes
1. **Going over the first screen too aggressively** → cutter shortcuts under both screens for an easy catch; must trail first and shortcut second
2. **Screener's defenders not standing up screeners** → cutter gets clean cuts; screeners must be held up
3. **Failing to communicate the switch** → if the cutter's defender gets screened on the second screen, silence = open shot; must verbally call "switch"
4. **Ball defender not pressuring** → staggered screens are designed to create a catch-and-shoot; the passer must be pressured to disrupt timing

## Related Concepts
- [[defending-specific-plays]] — staggered screens in the full context of Herb Brown's system
- [[defending-down-screens]] — single down screen principles that form the foundation
- [[concept-reading-screens-off-ball]] — the offensive cuts being defended
- [[pick-and-roll-defense-summary]] — the general on-ball screen defensive philosophy

## Sources
- [S1, pp.137-138] — Staggered Horizontal, Vertical, or Diagonal Screens (Figure 9.24)
- [S1, pp.140-141] — Horns Staggered Double Screens (Figure 9.32)
- [S1, p.146] — Double-Doubles (Figure 9.49)
