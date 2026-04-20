---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [defense, off-ball-screens, down-screens, man-to-man, denial]
source_count: 1
last_updated: 2026-04-11
---

# Defending Down Screens

## Summary
Herb Brown's system for defending down screens (zipper, wide diagonal, and standard pin-downs) centers on standing up the screener and using movement toward the ball to slip screens rather than getting caught behind them. The golden rule: **the ball should always draw you in its direction**. Never play with your back to the ball. [S1, pp.135-136]

## When to Use
- Any time the offense sets a down screen for a wing or guard coming to the ball
- Zipper actions (straight vertical): player cuts from low to high off a down screen
- Wide diagonal down screens: player cuts diagonally from low to a wing
- Standard pin-downs and elevator screens

## Key Principles
1. **Stand up the screener** — the screener's defender must hold the screener to give the screen recipient's defender time to navigate
2. **Always move toward the ball** — the defender guarding the screen recipient should be moving toward the ball to slip inside the screen
3. **Never play with your back to the ball** — this gives the cutter cutting and step-up options that are nearly unguardable
4. **Your mind-set: never be screened** — slip inside the screener if possible
5. **Force the screen recipient away** — either force him to catch higher/further out on the floor, or force him sideline so he cannot reverse the ball

## Variations

### Zipper (Straight Vertical) Down Screen
Stand up the screener and stay attached. Deny and force the screen recipient away — OR let him catch and then force him toward the near sideline to stop ball reversal. Key: never play on top of him with your back to the ball. [S1, p.136]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-down-screens-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.19",
      "players": [
        {
          "role": "1",
          "x": 8.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball_handler_top_key_area"
        },
        {
          "role": "3",
          "x": -2.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "wing_cutting_up"
        },
        {
          "role": "4",
          "x": -5.0,
          "y": 30.0,
          "jersey": "4",
          "side": "offense",
          "label": "screener_elbow_area"
        },
        {
          "role": "5",
          "x": -18.0,
          "y": 22.0,
          "jersey": "5",
          "side": "offense",
          "label": "weak_side_wing"
        },
        {
          "role": "2",
          "x": -14.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "weak_side_near_5"
        }
      ],
      "actions": [
        {
          "from": "4",
          "to": "3",
          "type": "screen",
          "d": "M -5 30 L -3 24",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "1",
          "type": "cut",
          "d": "M -2 22 C 2 25, 5 31, 8 38",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "3",
          "type": "pass",
          "d": "M 8 38 C 4 32, 0 27, -2 22",
          "style": "dashed"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 6.0,
          "y": 35.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1"
        },
        {
          "role": "x3",
          "x": 1.0,
          "y": 20.0,
          "jersey": "X3",
          "side": "defense",
          "label": "guarding_3_slipping_screen"
        },
        {
          "role": "x4",
          "x": -5.0,
          "y": 27.0,
          "jersey": "X4",
          "side": "defense",
          "label": "standing_up_screener_4"
        },
        {
          "role": "x5",
          "x": -16.0,
          "y": 20.0,
          "jersey": "X5",
          "side": "defense",
          "label": "guarding_5"
        }
      ],
      "ball": {
        "x": 8.0,
        "y": 38.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X4 stands up 4 to permit X3 to slip in front of screen",
          "x": -8,
          "y": 18
        }
      ]
    }
  ]
}
```

### Wide Diagonal Down Screen
Shortcut the screen to make the receiver fade — OR topside the receiver and force him baseline. [S1, pp.135-136]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-down-screens-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.18 \u2014 Wide diagonal down screen",
      "players": [
        {
          "role": "1",
          "x": -4.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball_handler_top_key"
        },
        {
          "role": "2",
          "x": -22.0,
          "y": 18.0,
          "jersey": "2",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "3",
          "x": 18.0,
          "y": 14.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing_receiver"
        },
        {
          "role": "4",
          "x": 6.0,
          "y": 26.0,
          "jersey": "4",
          "side": "offense",
          "label": "screener_down"
        },
        {
          "role": "5",
          "x": 2.0,
          "y": 12.0,
          "jersey": "5",
          "side": "offense",
          "label": "high_post"
        }
      ],
      "actions": [
        {
          "from": "4",
          "to": "3",
          "type": "screen",
          "d": "M 6.00 26.00 L 14.00 18.00",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "right_corner",
          "type": "cut",
          "d": "M 18.00 14.00 C 22.00 16.00, 24.00 20.00, 24.00 26.00",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "1",
          "type": "dribble",
          "d": "M -4.00 38.00 L -6.00 40.00",
          "style": "zigzag"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -2.0,
          "y": 36.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1_dribble"
        },
        {
          "role": "x2",
          "x": -20.0,
          "y": 22.0,
          "jersey": "X2",
          "side": "defense",
          "label": "weak_side_box_elbow"
        },
        {
          "role": "x3",
          "x": 16.0,
          "y": 16.0,
          "jersey": "X3",
          "side": "defense",
          "label": "topside_on_3"
        },
        {
          "role": "x4",
          "x": 8.0,
          "y": 22.0,
          "jersey": "X4",
          "side": "defense",
          "label": "standing_up_screener"
        },
        {
          "role": "x5",
          "x": 4.0,
          "y": 14.0,
          "jersey": "X5",
          "side": "defense",
          "label": "guarding_5"
        }
      ],
      "ball": {
        "x": -4.0,
        "y": 38.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X3 plays topside on 3 as 4 screens down, forces 3 away from screen",
          "x": 14,
          "y": 10
        },
        {
          "kind": "label",
          "text": "X5 and X2 cover weak-side elbow and box",
          "x": -12,
          "y": 18
        }
      ]
    },
    {
      "label": "Figure 9.19 \u2014 Zipper down screen",
      "players": [
        {
          "role": "1",
          "x": 18.0,
          "y": 36.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball_handler_wing"
        },
        {
          "role": "2",
          "x": -22.0,
          "y": 18.0,
          "jersey": "2",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "3",
          "x": -4.0,
          "y": 14.0,
          "jersey": "3",
          "side": "offense",
          "label": "receiver_top_of_key"
        },
        {
          "role": "4",
          "x": -8.0,
          "y": 28.0,
          "jersey": "4",
          "side": "offense",
          "label": "screener_down"
        },
        {
          "role": "5",
          "x": -18.0,
          "y": 22.0,
          "jersey": "5",
          "side": "offense",
          "label": "weak_side_post"
        }
      ],
      "actions": [
        {
          "from": "4",
          "to": "3",
          "type": "screen",
          "d": "M -8.00 28.00 L -6.00 20.00",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "3",
          "type": "cut",
          "d": "M -4.00 14.00 L -4.00 10.00",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 20.0,
          "y": 34.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1"
        },
        {
          "role": "x2",
          "x": -20.0,
          "y": 16.0,
          "jersey": "X2",
          "side": "defense",
          "label": "guarding_2"
        },
        {
          "role": "x3",
          "x": -2.0,
          "y": 16.0,
          "jersey": "X3",
          "side": "defense",
          "label": "slipping_screen_front"
        },
        {
          "role": "x4",
          "x": -6.0,
          "y": 26.0,
          "jersey": "X4",
          "side": "defense",
          "label": "standing_up_screener"
        },
        {
          "role": "x5",
          "x": -16.0,
          "y": 24.0,
          "jersey": "X5",
          "side": "defense",
          "label": "guarding_5"
        }
      ],
      "ball": {
        "x": 18.0,
        "y": 36.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "4 screens down on X3 to free 3 at top of key; X4 stands up 4 to let X3 slip in front",
          "x": -10,
          "y": 12
        }
      ]
    },
    {
      "label": "Figure 9.20 \u2014 Isolations",
      "players": [
        {
          "role": "1",
          "x": -2.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "passer_cutting_away"
        },
        {
          "role": "2",
          "x": -18.0,
          "y": 18.0,
          "jersey": "2",
          "side": "offense",
          "label": "wing_receiver"
        },
        {
          "role": "3",
          "x": 16.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "weak_side_wing"
        },
        {
          "role": "4",
          "x": 6.0,
          "y": 30.0,
          "jersey": "4",
          "side": "offense",
          "label": "elbow"
        },
        {
          "role": "5",
          "x": 4.0,
          "y": 14.0,
          "jersey": "5",
          "side": "offense",
          "label": "high_post"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "2",
          "type": "pass",
          "d": "M -2.00 38.00 C -6.00 32.00, -12.00 24.00, -18.00 18.00",
          "style": "dashed"
        },
        {
          "from": "1",
          "to": "weak_side",
          "type": "cut",
          "d": "M -2.00 38.00 C 2.00 36.00, 10.00 34.00, 14.00 32.00",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 0.0,
          "y": 36.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1"
        },
        {
          "role": "x2",
          "x": -16.0,
          "y": 20.0,
          "jersey": "X2",
          "side": "defense",
          "label": "guarding_2_forcing_uphill"
        },
        {
          "role": "x3",
          "x": 18.0,
          "y": 20.0,
          "jersey": "X3",
          "side": "defense",
          "label": "guarding_3"
        },
        {
          "role": "x4",
          "x": 8.0,
          "y": 28.0,
          "jersey": "X4",
          "side": "defense",
          "label": "elbow_help"
        },
        {
          "role": "x5",
          "x": 6.0,
          "y": 16.0,
          "jersey": "X5",
          "side": "defense",
          "label": "guarding_5"
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
          "text": "1 passes to 2 on the wing and cuts away; X2 forces 2 uphill toward help",
          "x": -8,
          "y": 14
        }
      ]
    }
  ],
  "notes": "[S1, p.136] Three defensive diagrams on p.136. Fig 9.18: wide diagonal down screen \u2014 X3 topside on 3 as 4 screens down, forcing 3 away; X1 pressures ball-handler 1 on dribble; X5 and X2 cover weak-side elbow and box. Fig 9.19: zipper (straight vertical) down screen \u2014 4 screens down on X3 to free 3 at top of key; X4 stands up 4 to allow X3 to slip in front of screen. Fig 9.20: isolation \u2014 1 passes to 2 on wing and cuts away; X2 forces 2 uphill toward help defenders at elbow and box. Dribble arrow on 1 in Fig 9.18 is very short/zigzag; path approximated. All arrow d-paths are approximate from scan."
}
```

### Standard Turnout / Pin-Down
Lock and trail on the outside shoulder and hip (with the big man's help), making the cutter curl the screen. Screener's defender contact shows. Gap option: shoot the gap while screener's defender stands up the screener and steps back. [S1, pp.134-135]

## Player Responsibilities
- **Screen recipient's defender**: Move toward the ball to slip inside the screener. Stay attached through the cut. Force catch higher or more toward sideline.
- **Screener's defender**: Stand up the screener — must hold him long enough for teammate to navigate. May contact show or take a step toward the cutter to help.
- **Ball defender**: Pressure the ball — make any pass after the screen difficult. Then immediately drop back to the nail on a pass to stop curl/drive penetration.
- **Weak-side help**: Elbow and box defenders must be active and drawn toward the ball.

## Common Mistakes
1. **Playing on top of the screen recipient with back to ball** → gives the offensive player a step-up or cut option; always face the ball
2. **Screener's defender chasing the screener after he cuts** → overrun = screening your own teammate
3. **Not standing up the screener** → gives the screen recipient a clean path to his spot
4. **Ball defender not pressuring after the pass** → cutter receives ball with space to drive or shoot; ball defender must drop to nail immediately

## Related Concepts
- [[defending-specific-plays]] — down screens in the full context of Herb Brown's specific play defense
- [[concept-reading-screens-off-ball]] — the offensive concepts being countered
- [[concept-shooting-off-screens]] — what the offense is trying to create with down screens
- [[defending-staggered-screens]] — when down screens are staggered (double screens)

## Sources
- [S1, pp.135-136] — Zipper Down Screens and Wide Diagonal Down Screens, Chapter 9
- [S1, pp.134-135] — Turnouts and Curls (pin-down defense), Chapter 9
