---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, man-to-man, help-defense, post-defense, rotation, double-team, trapping]
source_count: 1
last_updated: 2026-04-11
---

# Post Double-Team Rotation

## Summary
When the defense double-teams the post and forces the post player to kick the ball out, every remaining defender must rotate to a new assignment immediately. The key rule: the trapper (the defender who came in to double) is usually the player who sprints out of the double-team to close out, because the other trapper is often better positioned to rotate to a different man. On a short pass to the near corner, the trapper facing the ball rotates because he has the most direct path. [S1, p.15]

This is a pre-assigned rotation system — players know their jobs before the double-team is set, not after the ball moves. Rotation assignments depend on (a) where the pass is thrown and (b) which defender has the most direct path to the new ball location. [S1, pp.14-15]

## When to Use
- Any time the defense doubles a post player and the post kicks the ball out
- Against teams that use high-low action with a strong post player
- In combination with fronting or three-quartering the post

## Key Principles
1. **Trapper typically runs out of the double** — the trapper who can most directly reach the next pass receiver closes out without first turning and pivoting [S1, p.15]
2. **Assignment-based, not reaction-based** — all five defenders know their rotation before the trap is set; no guessing after the kick-out [S1, p.15]
3. **Rotation depends on pass direction** — cross-court to the wing, cross-court to the corner, and short-corner each have distinct rotation rules [S1, p.15]
4. **Remaining defenders cover nearest open man** — non-trapping defenders rotate to the player nearest their position in the direction of the pass [S1, p.15]

## Rotation Assignments

### Scenario 1: Cross-Court Pass to Wing (5 → 3 on wing)
- X2 (guarding 2) rotates out to contest 3 on the wing
- X3 and X4 shift; X5 stays near the paint
- See Figure 1.2 [S1, p.15]

### Scenario 2: Cross-Court Pass to Corner (5 → 3 in corner)
- X4 rotates to 3 in the corner
- X3 picks up 4 (X4's original man)
- Exception: if X5 arrives at 3 first, X3 still picks up 4
- See Figures 1.2–1.3 [S1, p.15]

### Scenario 3: Short Pass to Near Corner
- The trapper **facing the ball** (most direct path) rotates to the near corner
- No pivot or turn required — this is the fastest possible closeout [S1, p.15]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/post-double-team-rotation-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 1.1 \u2014 Trapping the post from weak-side high: cross-court pass from 5 to 3.",
      "players": [
        {
          "role": "1",
          "x": -22.0,
          "y": 30.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing_low"
        },
        {
          "role": "2",
          "x": 2.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_center"
        },
        {
          "role": "3",
          "x": 22.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "4",
          "x": 8.0,
          "y": 8.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow_high"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 20.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow_area"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -8 20 C 4 16, 14 18, 22 22",
          "style": "dashed"
        },
        {
          "from": "x1",
          "to": "1",
          "type": "cut",
          "d": "M -18 27 L -22 30",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 4 38 L 2 44",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -18.0,
          "y": 27.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1"
        },
        {
          "role": "x2",
          "x": 4.0,
          "y": 38.0,
          "jersey": "X2",
          "side": "defense",
          "label": "guarding_2"
        },
        {
          "role": "x3",
          "x": 17.0,
          "y": 25.0,
          "jersey": "X3",
          "side": "defense",
          "label": "guarding_3"
        },
        {
          "role": "x4",
          "x": 4.0,
          "y": 20.0,
          "jersey": "X4",
          "side": "defense",
          "label": "post_trapper_from_high"
        },
        {
          "role": "x5",
          "x": -12.0,
          "y": 20.0,
          "jersey": "X5",
          "side": "defense",
          "label": "post_trapper_from_weak_side"
        }
      ],
      "ball": {
        "x": -8.0,
        "y": 20.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Defensive number alongside X. Change in all directions.",
          "x": -14,
          "y": 47
        }
      ]
    },
    {
      "label": "Figure 1.2 \u2014 Rotation on cross-court outlet pass to 3: X2 rotates to 3 on the wing.",
      "players": [
        {
          "role": "1",
          "x": -22.0,
          "y": 20.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "2",
          "x": 2.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_center"
        },
        {
          "role": "3",
          "x": 24.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "4",
          "x": 8.0,
          "y": 8.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow_high"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 20.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow_area"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -8 20 C 4 16, 14 18, 24 22",
          "style": "dashed"
        },
        {
          "from": "x2",
          "to": "3",
          "type": "cut",
          "d": "M 8 36 C 14 30, 20 26, 24 22",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -16.0,
          "y": 22.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1"
        },
        {
          "role": "x2",
          "x": 8.0,
          "y": 36.0,
          "jersey": "X2",
          "side": "defense",
          "label": "rotating_to_3"
        },
        {
          "role": "x3",
          "x": -4.0,
          "y": 20.0,
          "jersey": "X3",
          "side": "defense",
          "label": "post_trapper"
        },
        {
          "role": "x4",
          "x": 4.0,
          "y": 18.0,
          "jersey": "X4",
          "side": "defense",
          "label": "post_trapper_high"
        },
        {
          "role": "x5",
          "x": -10.0,
          "y": 18.0,
          "jersey": "X5",
          "side": "defense",
          "label": "post_trapper_weak_side"
        }
      ],
      "ball": {
        "x": 24.0,
        "y": 22.0,
        "possessed_by": "3"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Had pass been to corner, X4 gets 3 and X3 gets 4 unless X5 there first (see Fig 1.3)",
          "x": 0,
          "y": 47
        }
      ]
    },
    {
      "label": "Figure 1.3 \u2014 Rotation on pass cross court from 5 to 3 (corner).",
      "players": [
        {
          "role": "1",
          "x": -22.0,
          "y": 20.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "2",
          "x": 2.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_center"
        },
        {
          "role": "3",
          "x": 24.0,
          "y": 8.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_corner"
        },
        {
          "role": "4",
          "x": 8.0,
          "y": 8.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow_high"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 20.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow_area"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -8 20 C 4 12, 14 8, 24 8",
          "style": "dashed"
        },
        {
          "from": "x4",
          "to": "3",
          "type": "cut",
          "d": "M 4 18 C 10 14, 18 10, 24 8",
          "style": "solid"
        },
        {
          "from": "x3",
          "to": "4",
          "type": "cut",
          "d": "M -2 20 C 2 16, 6 12, 8 8",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 8 36 C 6 40, 4 42, 2 44",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -16.0,
          "y": 22.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1"
        },
        {
          "role": "x2",
          "x": 8.0,
          "y": 36.0,
          "jersey": "X2",
          "side": "defense",
          "label": "rotating"
        },
        {
          "role": "x3",
          "x": -2.0,
          "y": 20.0,
          "jersey": "X3",
          "side": "defense",
          "label": "rotating_to_4"
        },
        {
          "role": "x4",
          "x": 4.0,
          "y": 18.0,
          "jersey": "X4",
          "side": "defense",
          "label": "rotating_to_3_corner"
        },
        {
          "role": "x5",
          "x": -10.0,
          "y": 18.0,
          "jersey": "X5",
          "side": "defense",
          "label": "post_trapper_weak_side"
        }
      ],
      "ball": {
        "x": 24.0,
        "y": 8.0,
        "possessed_by": "3"
      }
    }
  ],
  "notes": "[S1, p.15] Figures 1.1\u20131.3 show the post double-team trap (X5 and X4 on post player 5) and the three rotation scenarios when 5 kicks the ball cross-court. Fig 1.1 is the base trap setup with a dashed arrow showing the pass from 5 to 3 and defender arrows converging. Fig 1.2 shows X2 rotating to 3 on the wing after the cross-court pass. Fig 1.3 shows the corner variant: X4 rotates to 3 in the corner and X3 slides to cover 4. The book's diagrams use a half-court view oriented with the basket at the bottom; coordinates are approximated accordingly. Defensive glyphs are drawn as \"X\" with numeral alongside in the book."
}
```

## Common Mistakes
1. **Trapper pausing in the double-team area** → the trapper must sprint immediately when the post player gathers to pass [S1, p.15]
2. **Wrong defender chasing the ball** → the rotation is pre-assigned by position and pass direction; undisciplined pursuit leaves another man open [S1, p.15]
3. **Fronting the post when overloaded** → when the offense overloads the strong side, Brown recommends playing "half a man" instead of fronting, to prevent the high-low lock-and-lob [S1, p.13]

## Related Concepts
- [[weak-side-defense-rotation]] — the broader framework for all weak-side help and rotation out of double-teams
- [[defensive-coaching-philosophy-herb-brown]] — the five-man trust and buddy system that enables effective rotations
- [[post-defense-fronting]] — the companion concept on when and how to front the post before a double is needed

## Sources
- [S1, pp.13-15] — post overload "half a man" discussion and Figures 1.1–1.3 post double-team rotation
