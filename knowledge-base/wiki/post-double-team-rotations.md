---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, man-to-man, post-defense, double-team, rotation, help-defense]
source_count: 1
last_updated: 2026-04-11
---

# Post Double-Team Rotations

## Summary
When two defenders trap the post and the trapped offensive player throws the ball out, the defense must rotate immediately and precisely. Brown's system determines rotations based on **where the pass goes** and **who is facing the ball** at the moment of release. Incorrect rotations allow the offense to exploit the double-team by finding open perimeter players for easy shots or drives.

The core rule: **the trapper who is already facing the ball** is usually the best rotation candidate because he can move directly to the outlet without turning and pivoting first. [S1, p.15]

## When to Use
- Any time two defenders trap the low post player
- Immediately upon the post player beginning to pass out of the double-team
- The rotation is triggered by the **direction of the pass** — rotation rules differ for wing, corner, and cross-court passes

## Key Principles
1. **Explain, teach, demonstrate, and drill** — Rotations must become instinctive through repeated practice; they are not improvised. [S1, p.15]
2. **Rotation depends on where and to whom the pass is thrown** — There is no single rotation; the outlet destination determines who goes where. [S1, p.15]
3. **The trapper facing the ball rotates first** — On a short pass to the near corner, the trapper who is already facing the ball should rotate because he has a quicker, more direct path. [S1, p.15]
4. **The trapper is usually the rotator** — General preference is for the trapper to be the defender who runs out of the double-team to cover the outlet. [S1, p.15]
5. **All rotation paths must be practiced in all directions** — The same rotations apply regardless of which side of the court the post double-team occurs.

## Rotation Scenarios (Figures 1.1–1.3)

### Scenario 1: Post Trap from Weak-Side High (Figure 1.1)
- 5 (offensive player) is trapped at the post by X5 and X4 (or similar pairing)
- 1, 2, 3, 4 are positioned on perimeter
- A cross-court pass from 5 to 3 triggers rotation from all five defenders
- Defensive numbers alongside their X assignment
```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/post-double-team-rotations-0.png",
  "court_region": "half",
  "legend": {
    "dashed": "pass",
    "solid": "cut",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 1.1 \u2014 Trapping the post from weak-side high: cross-court pass from 5 to 3",
      "players": [
        {
          "role": "1",
          "x": -22.0,
          "y": 28.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing_low"
        },
        {
          "role": "2",
          "x": 0.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_center"
        },
        {
          "role": "3",
          "x": 20.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "4",
          "x": 18.0,
          "y": 6.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_perimeter_high"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 29.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow_post"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -8 29 C 4 20, 12 20, 20 22",
          "style": "dashed"
        },
        {
          "from": "x1",
          "to": "1",
          "type": "cut",
          "d": "M -18 26 L -22 28",
          "style": "solid"
        },
        {
          "from": "x5",
          "to": "x4",
          "type": "cut",
          "d": "M -6 27 L 14 29",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -18.0,
          "y": 26.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_1"
        },
        {
          "role": "x2",
          "x": 4.0,
          "y": 38.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_2"
        },
        {
          "role": "x3",
          "x": 16.0,
          "y": 24.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_3"
        },
        {
          "role": "x4",
          "x": 14.0,
          "y": 29.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_4_trapper"
        },
        {
          "role": "x5",
          "x": -6.0,
          "y": 27.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_5_trapper"
        }
      ],
      "ball": {
        "x": -8.0,
        "y": 29.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Defensive number alongside X. Change in all directions.",
          "x": -10,
          "y": 48
        }
      ]
    },
    {
      "label": "Figure 1.2 \u2014 Rotation on cross-court outlet pass to 3: X2 rotates to 3 on the wing",
      "players": [
        {
          "role": "1",
          "x": -22.0,
          "y": 22.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "2",
          "x": 0.0,
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
          "x": 18.0,
          "y": 6.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_high_perimeter"
        },
        {
          "role": "5",
          "x": -6.0,
          "y": 29.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow_post"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -6 29 C 6 20, 16 20, 24 22",
          "style": "dashed"
        },
        {
          "from": "5",
          "to": "4",
          "type": "pass",
          "d": "M -6 29 L 18 6",
          "style": "dashed"
        },
        {
          "from": "x2",
          "to": "3",
          "type": "cut",
          "d": "M 6 36 C 14 32, 20 28, 24 22",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "3",
          "type": "cut",
          "d": "M 12 29 L 24 22",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -18.0,
          "y": 24.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_1"
        },
        {
          "role": "x2",
          "x": 6.0,
          "y": 36.0,
          "jersey": "X",
          "side": "defense",
          "label": "rotating_to_3"
        },
        {
          "role": "x3",
          "x": 14.0,
          "y": 28.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_3"
        },
        {
          "role": "x4",
          "x": 12.0,
          "y": 29.0,
          "jersey": "X",
          "side": "defense",
          "label": "trapper_4"
        },
        {
          "role": "x5",
          "x": -4.0,
          "y": 27.0,
          "jersey": "X",
          "side": "defense",
          "label": "trapper_5"
        }
      ],
      "ball": {
        "x": -6.0,
        "y": 29.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X2 rotates to 3 on the wing. Corner variant: X4 gets 3, X3 gets 4 unless X5 arrives first.",
          "x": 0,
          "y": 48
        }
      ]
    },
    {
      "label": "Figure 1.3 \u2014 Rotation on pass cross court from 5 to 3",
      "players": [
        {
          "role": "1",
          "x": -22.0,
          "y": 22.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "2",
          "x": 0.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_center"
        },
        {
          "role": "3",
          "x": 24.0,
          "y": 18.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing_corner"
        },
        {
          "role": "4",
          "x": 18.0,
          "y": 6.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_high_perimeter"
        },
        {
          "role": "5",
          "x": -6.0,
          "y": 29.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow_post"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -6 29 C 6 18, 16 16, 24 18",
          "style": "dashed"
        },
        {
          "from": "x4",
          "to": "3",
          "type": "cut",
          "d": "M 12 27 C 16 24, 22 20, 24 18",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 6 38 C 4 42, 2 44, 0 44",
          "style": "solid"
        },
        {
          "from": "x3",
          "to": "4",
          "type": "cut",
          "d": "M 14 30 L 18 6",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -18.0,
          "y": 24.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_1"
        },
        {
          "role": "x2",
          "x": 6.0,
          "y": 38.0,
          "jersey": "X",
          "side": "defense",
          "label": "rotating"
        },
        {
          "role": "x3",
          "x": 14.0,
          "y": 30.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_3"
        },
        {
          "role": "x4",
          "x": 12.0,
          "y": 27.0,
          "jersey": "X",
          "side": "defense",
          "label": "trapper_4"
        },
        {
          "role": "x5",
          "x": -4.0,
          "y": 27.0,
          "jersey": "X",
          "side": "defense",
          "label": "trapper_5"
        }
      ],
      "ball": {
        "x": -6.0,
        "y": 29.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Full cross-court rotation: trapper takes direct path to cover the corner outlet.",
          "x": 0,
          "y": 48
        }
      ]
    }
  ],
  "notes": "[S1, p.15] Three sequential diagrams (Figures 1.1\u20131.3) showing post double-team rotation rules. Fig 1.1 shows the initial trap at the weak-side high post with 5 trapped by X5 and X4, and a cross-court pass to 3; defensive numbers appear alongside their X glyph. Fig 1.2 shows X2 rotating to cover 3 on the wing after the cross-court pass; a secondary dashed arrow also shows the pass option to 4 at the top. Fig 1.3 shows the full rotation where X4 (ball-facing trapper) takes the direct path to 3 in the corner, X3 rotates to 4, and X2 covers 2 at the baseline. Arrow paths approximated from diagram scan; some curves simplified due to small diagram scale."
}
```

### Scenario 2: Rotation on Cross-Court Outlet Pass to Wing (Figure 1.2)
- Ball thrown cross-court from 5 to 3 on the wing
- X2 rotates directly to 3 on the wing
- If the pass had gone to 3 in the **corner**, X4 covers 3 and X3 covers 4 — unless X5 beats both of them to 3 first
```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/post-double-team-rotations-1.png",
  "court_region": "half",
  "legend": {
    "dashed": "pass",
    "solid": "cut",
    "wavy": "rotation"
  },
  "phases": [
    {
      "label": "Figure 1.1 \u2014 Trapping the post from weak-side high: cross-court pass from 5 to 3",
      "players": [
        {
          "role": "1",
          "x": -24.0,
          "y": 30.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing_low"
        },
        {
          "role": "2",
          "x": 0.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_mid"
        },
        {
          "role": "3",
          "x": 26.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "4",
          "x": 12.0,
          "y": 8.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow_high"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 19.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_post_high"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -8 19 C 4 18, 16 20, 26 22",
          "style": "dashed"
        },
        {
          "from": "x1",
          "to": "1",
          "type": "cut",
          "d": "M -20 27 L -24 30",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 4 38 L 0 44",
          "style": "solid"
        },
        {
          "from": "x3",
          "to": "3",
          "type": "cut",
          "d": "M 20 26 L 26 22",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "4",
          "type": "cut",
          "d": "M 8 16 L 12 8",
          "style": "solid"
        },
        {
          "from": "x5",
          "to": "5",
          "type": "cut",
          "d": "M -4 19 L -8 19",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -20.0,
          "y": 27.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_1"
        },
        {
          "role": "x2",
          "x": 4.0,
          "y": 38.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_2"
        },
        {
          "role": "x3",
          "x": 20.0,
          "y": 26.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_3"
        },
        {
          "role": "x4",
          "x": 8.0,
          "y": 16.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_4"
        },
        {
          "role": "x5",
          "x": -4.0,
          "y": 19.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_5"
        }
      ],
      "ball": {
        "x": -8.0,
        "y": 19.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Defensive number alongside X. Change in all directions.",
          "x": 0,
          "y": 50
        }
      ]
    },
    {
      "label": "Figure 1.2 \u2014 Rotation on cross-court outlet pass to 3: X2 rotates to 3 on the wing",
      "players": [
        {
          "role": "1",
          "x": -26.0,
          "y": 15.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "2",
          "x": 0.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_mid"
        },
        {
          "role": "3",
          "x": 26.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "4",
          "x": 12.0,
          "y": 8.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow_high"
        },
        {
          "role": "5",
          "x": -6.0,
          "y": 19.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_post_high"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -6 19 C 6 18, 18 20, 26 22",
          "style": "dashed"
        },
        {
          "from": "x2",
          "to": "3",
          "type": "cut",
          "d": "M 4 36 C 10 32, 18 28, 26 22",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "4",
          "type": "cut",
          "d": "M 8 14 L 12 8",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -18.0,
          "y": 20.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_1"
        },
        {
          "role": "x2",
          "x": 4.0,
          "y": 36.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_2"
        },
        {
          "role": "x3",
          "x": 14.0,
          "y": 22.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_3"
        },
        {
          "role": "x4",
          "x": 8.0,
          "y": 14.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_4"
        },
        {
          "role": "x5",
          "x": -2.0,
          "y": 19.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_5"
        }
      ],
      "ball": {
        "x": -6.0,
        "y": 19.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X2 rotates to 3 on the wing",
          "x": 14,
          "y": 30
        },
        {
          "kind": "label",
          "text": "Corner variant: X4 \u2192 3, X3 \u2192 4, unless X5 first",
          "x": 0,
          "y": 50
        }
      ]
    },
    {
      "label": "Figure 1.3 \u2014 Rotation on pass cross court from 5 to 3",
      "players": [
        {
          "role": "1",
          "x": -26.0,
          "y": 15.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "2",
          "x": 0.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_mid"
        },
        {
          "role": "3",
          "x": 26.0,
          "y": 9.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing_high"
        },
        {
          "role": "4",
          "x": 12.0,
          "y": 9.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow_high"
        },
        {
          "role": "5",
          "x": -6.0,
          "y": 19.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_post_high"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -6 19 C 6 14, 18 11, 26 9",
          "style": "dashed"
        },
        {
          "from": "x4",
          "to": "3",
          "type": "cut",
          "d": "M 8 14 C 14 12, 20 10, 26 9",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "4",
          "type": "cut",
          "d": "M 4 36 C 8 28, 10 20, 12 9",
          "style": "solid"
        },
        {
          "from": "x5",
          "to": "2",
          "type": "cut",
          "d": "M -2 19 C 0 30, 0 38, 0 44",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -18.0,
          "y": 20.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_1"
        },
        {
          "role": "x2",
          "x": 4.0,
          "y": 36.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_2"
        },
        {
          "role": "x4",
          "x": 8.0,
          "y": 14.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_4"
        },
        {
          "role": "x5",
          "x": -2.0,
          "y": 19.0,
          "jersey": "X",
          "side": "defense",
          "label": "near_5"
        }
      ],
      "ball": {
        "x": -6.0,
        "y": 19.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Trapper takes direct path to outlet on cross-court pass",
          "x": 0,
          "y": 50
        }
      ]
    }
  ],
  "notes": "[S1, p.15] Figures 1.1\u20131.3 depict defensive rotation scenarios out of a post double-team. Figure 1.1: initial trap formation with cross-court pass from 5 to 3; all five defenders rotate to match their assigned offensive player (defensive number printed alongside X glyph). Figure 1.2: rotation on cross-court outlet to 3 on the wing \u2014 X2 rotates to cover 3; corner variant described in caption (X4\u21923, X3\u21924, unless X5 arrives first). Figure 1.3: full rotation pattern on the cross-court pass to 3 in the corner \u2014 X4 chases 3 to corner, X2 drops to cover 4, X5 drops to cover 2 baseline. Scan quality is good; arrow paths approximated from printed curves. The marker index on this wiki page is 1, corresponding to Figure 1.2 per the diagram marker comment, but all three figures are extracted for completeness."
}
```

### Scenario 3: Rotation on Cross-Court Pass 5 to 3 (Figure 1.3)
- Full rotation pattern on the cross-court pass: X5 and X4 release from double-team; nearest defenders rotate based on position and path efficiency
- Trapper facing the ball takes the shorter, more direct path to the corner
```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/post-double-team-rotations-2.png",
  "court_region": "half",
  "legend": {
    "dashed": "pass",
    "solid": "cut",
    "wavy": "rotation"
  },
  "phases": [
    {
      "label": "Figure 1.3 \u2014 Rotation on pass cross court from 5 to 3",
      "players": [
        {
          "role": "1",
          "x": -27.0,
          "y": 22.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_wing_low"
        },
        {
          "role": "2",
          "x": 0.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_center"
        },
        {
          "role": "3",
          "x": 27.0,
          "y": 17.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "4",
          "x": 10.0,
          "y": 28.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow_area"
        },
        {
          "role": "5",
          "x": -5.0,
          "y": 28.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow_post"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "3",
          "type": "pass",
          "d": "M -5 28 L 10 28 L 27 17",
          "style": "dashed"
        },
        {
          "from": "x4",
          "to": "3",
          "type": "cut",
          "d": "M 5 27 C 12 24, 20 18, 27 17",
          "style": "solid"
        },
        {
          "from": "x5",
          "to": "4",
          "type": "cut",
          "d": "M -8 27 C -2 27, 4 27, 10 28",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "4",
          "type": "cut",
          "d": "M 3 38 C 5 34, 7 31, 10 28",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 3 38 C 1 41, 0 43, 0 44",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -19.0,
          "y": 24.0,
          "jersey": "X1",
          "side": "defense",
          "label": "left_wing_defender"
        },
        {
          "role": "x2",
          "x": 3.0,
          "y": 38.0,
          "jersey": "X2",
          "side": "defense",
          "label": "baseline_defender"
        },
        {
          "role": "x4",
          "x": 5.0,
          "y": 27.0,
          "jersey": "X4",
          "side": "defense",
          "label": "right_elbow_defender"
        },
        {
          "role": "x5",
          "x": -8.0,
          "y": 27.0,
          "jersey": "X5",
          "side": "defense",
          "label": "post_trapper_left"
        }
      ],
      "ball": {
        "x": -5.0,
        "y": 28.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "5",
          "x": -5,
          "y": 27,
          "target_role": "5"
        },
        {
          "kind": "label",
          "text": "X5",
          "x": -8,
          "y": 28,
          "target_role": "x5"
        },
        {
          "kind": "label",
          "text": "X4",
          "x": 5,
          "y": 28,
          "target_role": "x4"
        },
        {
          "kind": "label",
          "text": "4",
          "x": 10,
          "y": 27,
          "target_role": "4"
        },
        {
          "kind": "label",
          "text": "3",
          "x": 27,
          "y": 16,
          "target_role": "3"
        },
        {
          "kind": "label",
          "text": "X2",
          "x": 3,
          "y": 39,
          "target_role": "x2"
        },
        {
          "kind": "label",
          "text": "2",
          "x": 0,
          "y": 45,
          "target_role": "2"
        },
        {
          "kind": "label",
          "text": "1",
          "x": -27,
          "y": 21,
          "target_role": "1"
        },
        {
          "kind": "label",
          "text": "X1",
          "x": -20,
          "y": 25,
          "target_role": "x1"
        }
      ],
      "extras": [
        {
          "kind": "legend_symbol",
          "symbol": "dashed",
          "meaning": "pass"
        },
        {
          "kind": "legend_symbol",
          "symbol": "solid",
          "meaning": "defensive rotation / cut"
        }
      ]
    }
  ],
  "notes": "[S1, p.15] Figure 1.3 \u2014 Full cross-court rotation on pass from 5 to 3. 5 (offensive post) passes cross-court to 3 on the right wing. X4 (the trapper facing the ball) rotates directly to 3 taking the most direct path. X5 (other trapper) slides to cover 4 at the elbow. X2 rotates from the baseline area to pick up 4 or 2 depending on pass destination. X1 holds on the left wing opposite 1. Dashed arrows indicate the pass; solid arrows indicate defensive rotation paths. The diagram shows the trapper (X4) taking the shorter, more direct route to the outlet receiver (3) without needing to pivot first. Scan is small but legible; arrow paths approximate from the printed diagram."
}
```

## Common Mistakes
1. **Wrong defender rotates** → The defender NOT facing the ball rotates slower (must turn and pivot first); default to the ball-facing trapper on near-corner passes. [S1, p.15]
2. **Slow rotation timing** → Rotation must begin as the pass is released — not after it is caught. Move on the pass, not the catch. [S1, pp.12-13]
3. **Undrilled rotations** → Rotations must be practiced repeatedly in all directions so players react instinctively; untrained rotations leave shooters wide open. [S1, p.15]
4. **Ignoring the corner variant** → The rotation for a wing outlet differs from a corner outlet; players must know both and execute correctly based on pass destination. [S1, p.15]

## Related Concepts
- [[weak-side-help-defense]] — the broad weak-side rotation principles these specific rules apply to
- [[defensive-coaching-philosophy]] — the system that demands 5-man accountability on all rotations
- [[post-defense-fronting]] — how post defenders decide when to front vs. play half-a-man before the double-team is needed

## Sources
- [S1, pp.15] — Figures 1.1, 1.2, 1.3: Weak-side rotation diagrams from post double-team
- [S1, pp.8-14] — Philosophy of Team Defense and Weak-Side Defense context
