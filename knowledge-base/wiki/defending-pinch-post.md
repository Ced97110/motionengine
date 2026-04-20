---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [defense, man-to-man, post-defense, screens, two-man-game, pinch-post]
source_count: 1
last_updated: 2026-04-11
---

# Defending the Pinch Post

## Summary
The pinch post is a two-man game where a guard passes to a post player at the elbow or mid-post, then uses that player as a screener to attack or exchange. Herb Brown's approach requires the on-ball defender to fight over the screen, the post defender to create a lane for his teammate, and weak-side defenders to flood the nail, elbow, and box areas to deter penetrating passes. [S1, pp.147-149]

The most critical action is the **pass-and-follow** variation: when the passer passes and then cuts toward the ball looking for a return, the post defender must step back and let the passer's defender slide through. Failure to do so results in the cutter getting picked off and receiving an easy layup pass.

## When to Use
- Defending any half-court two-man game at the elbow, mid-post, or pinch-post area
- Whenever the offense runs a pass-and-follow, "give-and-go off the post," or elbow dribble screen action
- Particularly important when guarding skilled playmakers who use the elbow as an entry point

## Key Principles
1. **Fight over the screen on the dribble.** The on-ball defender bodies up and fights over the pinch-post screen rather than going behind it. Going under surrenders a pull-up jumper. [S1, p.147]
2. **Post defender gives a lane.** When the ball handler fights over the screen, the post defender must be in **front** of his own teammate — opening a gap and stepping back so the on-ball defender can slide through cleanly. [S1, pp.147-148]
3. **High screen option — pinch and let through.** If the screen is set high (near or above the elbow), the post defender can pinch his man and let the passer go quickly under the ball handler. Dangerous unless weak-side help is confirmed. [S1, p.147]
4. **Pass-and-follow: step back.** On a pass-and-follow, the post defender steps back and lets the passer's defender through to beat the cutter to the spot. [S1, pp.147-148]
5. **Aggressive trap option.** On a passer's inside screen for the ball carrier, switch aggressively and force the dribbler uphill. If trapping, objective is to force the dribbler back to his original defender. [S1, p.147]
6. **Weak-side zone up.** The other three defenders zone up covering the nail, elbow, and box. They collapse toward the ball to shrink the floor and deny penetrating passes. [S1, p.147]
7. **Force passes over the outside shoulder.** All trappers and post defenders work to make the passer throw over the trapper's outside shoulder — eliminating gut passes to the middle. [S1, p.147]

## Player Responsibilities
- **PG (X1)**: Body up and fight over the screen; on pass-and-follow, slide through the lane the post defender creates to beat cutter to the spot.
- **PF (X4)**: Hard show to stop the ball when acting as post defender; open up and give space for X1 to slide through; shade man to outside on pass-and-follow.
- **SG (X2)**: Covers the nail area; reads the trap; denies pass back to the passer.
- **SF (X3)**: Covers the weak-side elbow; ready to rotate on any skip pass.
- **C (X5)**: Ready to rotate big-to-big should the post roll to the goal; covers the weak-side box.

## Variations
### Pinch Post — Weak Side (Pass and Follow)
On the weak side, trap the dribbler with the screener's defender, stop the ball, or force uphill. Remaining three defenders zone up on the nail, elbow, and box. [S1, p.147]

### Elbow Dribble Screen / Pass and Follow
Body up to the dribbler and fight over the screen. Slide through in front of the defensive teammate on the pass-and-follow. The post defender steps back and shades his man to the outside. Key goal: force the pinch-post player to receive the ball farther out (above the 3-point line) to neutralize the action. [S1, p.149]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-pinch-post-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "screen",
    "wavy": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.52 \u2014 Pinch post: X1 bodies up and fights over screen; X4 hard shows",
      "players": [
        {
          "role": "1",
          "x": 8.0,
          "y": 29.0,
          "jersey": "1",
          "side": "offense",
          "label": "right_elbow / ball handler"
        },
        {
          "role": "2",
          "x": 2.0,
          "y": 42.0,
          "jersey": "2",
          "side": "offense",
          "label": "low block area / weak side"
        },
        {
          "role": "3",
          "x": -18.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "left wing"
        },
        {
          "role": "4",
          "x": 10.0,
          "y": 24.0,
          "jersey": "4",
          "side": "offense",
          "label": "pinch post / elbow screener"
        },
        {
          "role": "5",
          "x": 4.0,
          "y": 8.0,
          "jersey": "5",
          "side": "offense",
          "label": "high post / nail area"
        }
      ],
      "actions": [
        {
          "from": "x4",
          "to": "1",
          "type": "cut",
          "d": "M 14 22 L 10 27",
          "style": "solid"
        },
        {
          "from": "x1",
          "to": "4",
          "type": "cut",
          "d": "M 10 27 C 10 25, 11 24, 10 24",
          "style": "wavy"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 10.0,
          "y": 27.0,
          "jersey": "X1",
          "side": "defense",
          "label": "on-ball defender on 1"
        },
        {
          "role": "x2",
          "x": 4.0,
          "y": 14.0,
          "jersey": "X2",
          "side": "defense",
          "label": "nail coverage"
        },
        {
          "role": "x3",
          "x": -4.0,
          "y": 22.0,
          "jersey": "X3",
          "side": "defense",
          "label": "weak-side elbow"
        },
        {
          "role": "x4",
          "x": 14.0,
          "y": 22.0,
          "jersey": "X4",
          "side": "defense",
          "label": "post defender hard showing"
        },
        {
          "role": "x5",
          "x": 6.0,
          "y": 6.0,
          "jersey": "X5",
          "side": "defense",
          "label": "top, ready to rotate big-to-big"
        }
      ],
      "ball": {
        "x": 8.0,
        "y": 29.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X1 bodies up to 1 and fights over screen",
          "x": 10,
          "y": 29
        },
        {
          "kind": "label",
          "text": "X4 hard shows to stop ball",
          "x": 14,
          "y": 22
        },
        {
          "kind": "label",
          "text": "X2 at nail",
          "x": 4,
          "y": 14
        },
        {
          "kind": "label",
          "text": "X3 weak-side elbow",
          "x": -4,
          "y": 22
        },
        {
          "kind": "label",
          "text": "X5 ready to rotate big-to-big on roll",
          "x": 6,
          "y": 6
        }
      ]
    }
  ],
  "notes": "[S1, p.147] Fig 9.52 \u2014 Pinch post defense diagram. X1 on-ball defender fights over screen at elbow; X4 post defender hard-shows toward ball handler; X2 holds nail, X3 weak-side elbow, X5 top ready for big-to-big rotation if 4 rolls. Offensive players 1 (ball at right elbow), 4 (pinch-post screener), 5 (high), 3 (left wing), 2 (weak-side low). Arrow paths approximated from scan \u2014 wavy line on X1 path indicates fighting over the screen."
}
```
```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-pinch-post-1.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "screen",
    "wavy": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.54 \u2014 Pinch-post two-man game: X4 opens up and permits X1 to slide through in front of him to get to 1.",
      "players": [
        {
          "role": "1",
          "x": 2.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball_handler_bottom_of_key"
        },
        {
          "role": "2",
          "x": -14.0,
          "y": 40.0,
          "jersey": "2",
          "side": "offense",
          "label": "weak_side_corner"
        },
        {
          "role": "3",
          "x": -22.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "weak_side_wing"
        },
        {
          "role": "4",
          "x": 12.0,
          "y": 30.0,
          "jersey": "4",
          "side": "offense",
          "label": "pinch_post_elbow"
        },
        {
          "role": "5",
          "x": 2.0,
          "y": 18.0,
          "jersey": "5",
          "side": "offense",
          "label": "nail_area"
        }
      ],
      "actions": [
        {
          "from": "x4",
          "to": "x1",
          "type": "cut",
          "d": "M 10.00 28.00 L 8.00 30.00",
          "style": "solid"
        },
        {
          "from": "x1",
          "to": "1",
          "type": "cut",
          "d": "M 4.00 36.00 C 7.00 33.00, 11.00 31.00, 12.00 30.00",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 4.0,
          "y": 36.0,
          "jersey": "X1",
          "side": "defense",
          "label": "on_ball_defender"
        },
        {
          "role": "x3",
          "x": -6.0,
          "y": 27.0,
          "jersey": "X3",
          "side": "defense",
          "label": "weak_side_elbow"
        },
        {
          "role": "x4",
          "x": 10.0,
          "y": 28.0,
          "jersey": "X4",
          "side": "defense",
          "label": "post_defender_opening_lane"
        },
        {
          "role": "x5",
          "x": 4.0,
          "y": 17.0,
          "jersey": "X5",
          "side": "defense",
          "label": "nail_defender"
        }
      ],
      "ball": {
        "x": 2.0,
        "y": 38.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X4 opens up, X1 slides through in front to get to 1",
          "x": 8,
          "y": 26
        }
      ]
    },
    {
      "label": "Figure 9.55 \u2014 Pinch-post two-man game: X4 opens up and permits X1 to slide through in front of him to get to 1.",
      "players": [
        {
          "role": "1",
          "x": 2.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball_handler_bottom_of_key"
        },
        {
          "role": "2",
          "x": -14.0,
          "y": 40.0,
          "jersey": "2",
          "side": "offense",
          "label": "weak_side_corner"
        },
        {
          "role": "3",
          "x": -22.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "weak_side_wing"
        },
        {
          "role": "4",
          "x": 14.0,
          "y": 30.0,
          "jersey": "4",
          "side": "offense",
          "label": "pinch_post_elbow"
        },
        {
          "role": "5",
          "x": 2.0,
          "y": 20.0,
          "jersey": "5",
          "side": "offense",
          "label": "nail_area"
        }
      ],
      "actions": [
        {
          "from": "x2",
          "to": "4",
          "type": "cut",
          "d": "M 2.00 28.00 L 14.00 30.00",
          "style": "solid"
        },
        {
          "from": "x1",
          "to": "1",
          "type": "cut",
          "d": "M 1.00 35.00 C 3.00 33.00, 8.00 31.00, 12.00 29.00",
          "style": "dashed"
        },
        {
          "from": "x4",
          "to": "weak_side",
          "type": "cut",
          "d": "M 12.00 27.00 L 14.00 28.00",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 1.0,
          "y": 35.0,
          "jersey": "X1",
          "side": "defense",
          "label": "on_ball_defender_sliding_through"
        },
        {
          "role": "x2",
          "x": 2.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "nail_defender"
        },
        {
          "role": "x4",
          "x": 12.0,
          "y": 27.0,
          "jersey": "X4",
          "side": "defense",
          "label": "post_defender_stepped_back"
        },
        {
          "role": "x5",
          "x": 4.0,
          "y": 19.0,
          "jersey": "X5",
          "side": "defense",
          "label": "weak_side_box_help"
        }
      ],
      "ball": {
        "x": 14.0,
        "y": 30.0,
        "possessed_by": "4"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X4 opens, X1 slides through in front to recover on 1; X2 at nail",
          "x": 6,
          "y": 24
        }
      ]
    }
  ],
  "notes": "[S1, pp.147-148] Figures 9.54 and 9.55 \u2014 Pinch-post pass-and-follow two-man game. Two sequential diagrams showing the same action: X4 (post defender) steps back and opens up a lane, permitting X1 (on-ball defender) to slide through in front of him and recover to 1. In Fig 9.54 the ball is still with 1 at the bottom of the key area; in Fig 9.55 the pass has been made to 4 at the elbow and X1 is sliding through. Offensive players 3 and 2 occupy the weak side. X2 covers the nail in Fig 9.55. Arrow paths are approximate due to the small scan size; straight-line or gentle-curve approximations used."
}
```
```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-pinch-post-2.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "dotted": "pass",
    "zigzag": "screen"
  },
  "phases": [
    {
      "label": "Figure 9.58 \u2014 Pinch-post or elbow dribble screen",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 37.0,
          "jersey": "1",
          "side": "offense",
          "label": "top of key / on-ball"
        },
        {
          "role": "2",
          "x": 22.0,
          "y": 28.0,
          "jersey": "2",
          "side": "offense",
          "label": "right wing"
        },
        {
          "role": "3",
          "x": -24.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "left wing"
        },
        {
          "role": "4",
          "x": 18.0,
          "y": 22.0,
          "jersey": "4",
          "side": "offense",
          "label": "right elbow / pinch post"
        },
        {
          "role": "5",
          "x": -6.0,
          "y": 24.0,
          "jersey": "5",
          "side": "offense",
          "label": "left elbow area"
        }
      ],
      "actions": [
        {
          "from": "x3",
          "to": "5",
          "type": "cut",
          "d": "M -10 24 L -6 24",
          "style": "solid"
        },
        {
          "from": "x5",
          "to": "4",
          "type": "cut",
          "d": "M -4 22 L 8 22",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 10 29 L 18 28",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "4",
          "type": "cut",
          "d": "M 15 22 C 16 19, 18 17, 20 15",
          "style": "solid"
        },
        {
          "from": "x1",
          "to": "1",
          "type": "cut",
          "d": "M 2 35 C 4 33, 6 32, 8 31",
          "style": "dotted"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 2.0,
          "y": 35.0,
          "jersey": "x1",
          "side": "defense",
          "label": "on-ball defender guarding 1"
        },
        {
          "role": "x2",
          "x": 10.0,
          "y": 29.0,
          "jersey": "x2",
          "side": "defense",
          "label": "defender on 2 / nail area"
        },
        {
          "role": "x3",
          "x": -10.0,
          "y": 24.0,
          "jersey": "x3",
          "side": "defense",
          "label": "defender on 3 / weak-side"
        },
        {
          "role": "x4",
          "x": 15.0,
          "y": 22.0,
          "jersey": "x4",
          "side": "defense",
          "label": "post defender on 4"
        },
        {
          "role": "x5",
          "x": -4.0,
          "y": 22.0,
          "jersey": "x5",
          "side": "defense",
          "label": "defender on 5"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 37.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Figure 9.58",
          "x": 0,
          "y": 50
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "overplaying pass to 4 forces him above 3-point line",
          "x": 0,
          "y": 52
        }
      ]
    }
  ],
  "notes": "[S1, p.149] Fig 9.58 \u2014 Pinch-post or elbow dribble screen. Defense bodies up to the dribbler (1) and fights over the screen. X4 overplays the pass to 4, forcing 4 to receive the ball farther out (above the 3-point line). X2 slides toward the nail, X3 covers weak-side elbow, X5 is adjacent to 5. Defensive movement arrows show X-defenders shading/sliding to deny the entry pass to 4 at the elbow. Dashed/dotted line from X1 indicates slide-through path. Diagram scan is partially small; coordinate approximations are best-fit estimates from the visible layout."
}
```

## Common Mistakes
1. **Post defender doesn't open up** → Passer's defender gets screened off and cutter receives an easy layup pass. Correction: post defender must step back and create a clear lane before the cutter arrives.
2. **Going under the screen** → Ball handler gets a clean pull-up jumper at the elbow. Correction: fight over all pinch-post screens.
3. **Weak-side help collapses too late** → Post player dribbles into the paint unopposed. Correction: nail, elbow, and box must be filled immediately on any pinch-post action.
4. **Gut pass allowed** → Middle defender leaves his zone and the pass splits the defense. Correction: force all passes over the outside shoulder of the trapper.

## Related Concepts
- [[defending-flash-post]] — when the wing flashes into the pinch-post area instead of a set screen
- [[trapping-and-double-teaming]] — the broader trap philosophy that governs pinch-post trap rotations
- [[post-splits-defense]] — after the pinch-post, cutters often split the defense

## Sources
- [S1, pp.147-149] — Herb Brown's primary explanation of defending the pinch-post two-man game, pass-and-follow, and elbow dribble screen
