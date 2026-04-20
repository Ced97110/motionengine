---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [defense, isolation, man-to-man, help-defense, shadow, tilt, trapping]
source_count: 1
last_updated: 2026-04-11
---

# Isolation Defense

## Summary
When the offense clears out for an isolation, Herb Brown's defense wants to play the isolated player one-on-one while keeping him in front of help defenders. The preferred direction is always **uphill toward help**. Weak-side help comes from the plug (nail) man, elbow defenders, and box defenders. The pro Shadow and Tilt tactic — bringing the nearest big to provide sideline help while covering elbows and boxes — is a key tool in this system. [S1, pp.130, 136-137]

## When to Use
- When opponent's best player is isolated on the wing, corner, or high post
- Post-entry situations where cutters clear and the ball-handler is one-on-one
- Hawk-cut situations where 2 has the ball on the wing

## Key Principles
1. **Play one-on-one first** — don't double too early; keep the offensive player in front of help defenders
2. **Force uphill toward help** — never allow the isolated player to drive toward the baseline away from weak-side support
3. **Shadow or Tilt** — bring the nearest big defender to the strong-side to provide help while the other three fill elbows and boxes
4. **Nail/elbow/box structure** — weak-side help must be active and in position at all times
5. **Force the ball to give up the dribble** — the goal is to make the isolated player pass, not to concede an open pull-up

## Player Responsibilities
- **On-ball defender (X2)**: Force isolated player uphill toward help. Use shadowing/tilting. "X2 tries to force 2 to his help. We want 2 to give up the ball."
- **Nail defender**: Active at the plug/nail to stop any drive down the middle
- **Nearest big**: Cross the lane if needed or hold strong-side elbow (Shadow/Tilt position)
- **Weak-side defenders**: Cover elbow and box — provide rotation if isolation turns into a drive

## Variations

### Wing Isolation — Shadow or Tilt
X2 shadows or tilts on the ball-side wing. Nail defenders cover boxes and elbow. Once 2 has ball, X2 tries to force 2 to his help. [S1, p.130; Figure 9.1]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/isolation-defense-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.1",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 33.0,
          "jersey": "1",
          "side": "offense",
          "label": "top_of_key_low"
        },
        {
          "role": "2",
          "x": -18.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "3",
          "x": 26.0,
          "y": 16.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing_high"
        },
        {
          "role": "4",
          "x": 8.0,
          "y": 29.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow"
        },
        {
          "role": "5",
          "x": 4.0,
          "y": 21.0,
          "jersey": "5",
          "side": "offense",
          "label": "high_post_right"
        }
      ],
      "actions": [
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M -14 24 L -18 22",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 0.0,
          "y": 30.0,
          "jersey": "X1",
          "side": "defense",
          "label": "nail"
        },
        {
          "role": "x2",
          "x": -14.0,
          "y": 24.0,
          "jersey": "X2",
          "side": "defense",
          "label": "ball_side_wing"
        },
        {
          "role": "x4",
          "x": 10.0,
          "y": 27.0,
          "jersey": "X4",
          "side": "defense",
          "label": "right_elbow"
        },
        {
          "role": "x5",
          "x": -4.0,
          "y": 21.0,
          "jersey": "X5",
          "side": "defense",
          "label": "high_post_left"
        }
      ],
      "ball": {
        "x": -18.0,
        "y": 22.0,
        "possessed_by": "2"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Defending the wing: isolation is by shadowing or tilting and covering nail boxes and elbow once 2 has the ball. X2 tries to force 2 to his help. We want 2 to give up the ball.",
          "x": 0,
          "y": 50
        }
      ]
    },
    {
      "label": "Figure 9.2",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 33.0,
          "jersey": "1",
          "side": "offense",
          "label": "top_of_key_low"
        },
        {
          "role": "2",
          "x": -22.0,
          "y": 26.0,
          "jersey": "2",
          "side": "offense",
          "label": "left_wing_low"
        },
        {
          "role": "3",
          "x": 26.0,
          "y": 16.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing_high"
        },
        {
          "role": "4",
          "x": 10.0,
          "y": 27.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow"
        },
        {
          "role": "5",
          "x": -2.0,
          "y": 21.0,
          "jersey": "5",
          "side": "offense",
          "label": "high_post_left"
        }
      ],
      "actions": [
        {
          "from": "x1",
          "to": "2",
          "type": "cut",
          "d": "M -4 30 C -10 29, -16 28, -22 27",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -4.0,
          "y": 30.0,
          "jersey": "X1",
          "side": "defense",
          "label": "nail_trapper"
        },
        {
          "role": "x2",
          "x": -22.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "ball_side_trapper"
        },
        {
          "role": "x3",
          "x": 8.0,
          "y": 24.0,
          "jersey": "X3",
          "side": "defense",
          "label": "right_interceptor"
        },
        {
          "role": "x4",
          "x": 12.0,
          "y": 27.0,
          "jersey": "X4",
          "side": "defense",
          "label": "deep_goaltender"
        },
        {
          "role": "x5",
          "x": 0.0,
          "y": 19.0,
          "jersey": "X5",
          "side": "defense",
          "label": "left_interceptor"
        }
      ],
      "ball": {
        "x": -22.0,
        "y": 26.0,
        "possessed_by": "2"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Trapping the isolation on the wing: X1 and X2 are trappers, X3 and X5 are interceptors, and X4 is deep goaltender. (X3 and X4 invert if possible.)",
          "x": 0,
          "y": 50
        }
      ]
    }
  ],
  "notes": "[S1, p.130] Two diagrams on this page. Figure 9.1: Wing isolation defended by shadow/tilt \u2014 X2 is on the ball-side wing defending player 2; X5 and X4 cover the nail/high-post area; X1 is at the nail. The key instruction is that X2 forces 2 uphill toward help. Figure 9.2: Trapping the isolation \u2014 X1 and X2 trap player 2 on the wing; X3 and X5 are interceptors; X4 is the deep goaltender with optional inversion of X3 and X4. Player positions are approximate due to small scan size; defensive marks appear as circled X glyphs in the original."
}
```

### Wing Isolation — Trapping
X1 and X2 are trappers. X3 and X5 are interceptors. X4 is deep goaltender. X3 and X4 can invert if possible. [S1, p.130; Figure 9.2]

### Force Baseline Trap
X2 forces 2 toward the baseline as X5 crosses the lane to trap 2 with X2. X1, X3, and X4 rotate toward the ball to provide weak-side help. [S1, p.137; Figure 9.21]

### Hawk Cut Isolation Trap
When 2 has ball on the wing after a hawk cut: X4 traps from the top with X2. X1 and X3 are interceptors. X5 is the goaltender. [S1, p.137; Figure 9.22]

## Common Mistakes
1. **Doubling too early** → allows the passer to find open teammates; hold one-on-one first
2. **Allowing baseline drives** → force uphill; going baseline takes the dribbler away from weak-side help
3. **Weak-side defenders sagging too low** → must stay level with ball and cover elbows/boxes, not drop to the paint
4. **Trapping without interceptors in position** → trap only works with X3/X5 in interceptor positions and a goaltender

## Related Concepts
- [[defending-specific-plays]] — isolation defense in context of all specific play defense
- [[post-up-defense]] — fronting principles for when isolated player catches and posts
- [[pick-and-roll-defense-summary]] — how isolation and PnR defense connect

## Sources
- [S1, pp.130, 136-137] — Chapter 9: Defending Specific Plays, Isolation sections and Figures 9.1-9.2, 9.20-9.22
