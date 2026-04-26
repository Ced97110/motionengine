---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [defense, man-to-man, 1-4-flat, formation-defense, penetration-stoppage, help-defense]
source_count: 1
last_updated: 2026-04-11
---

# Defending the 1-4 Flat Set

## Summary
The 1-4 flat set places the point guard at the top of the key with two wings at the elbows and two low-post players at the low blocks, creating a flat line across the lane. It is a dangerous formation that stretches the defense horizontally and creates penetration opportunities for the ball handler. Herb Brown's defensive response is built around stopping penetration first, protecting elbows and boxes, and tilting the defense when the offense overloads one side. [S1, p.150]

## When to Use
- Any time the offense sets up in a 1-4 flat or 1-4 high formation
- Particularly important when facing a skilled penetrating point guard
- Must be ready to tilt when the offense clears to one side

## Key Principles
1. **Keep the ball in front.** The on-ball defender (X1) must never get beat off the dribble — keep the point guard in front and influence toward his weak hand. [S1, p.150]
2. **Force sideline.** X1 channels the ball toward the sideline to limit penetration angles and make trapping easier. [S1, p.150]
3. **Corner defenders up at the elbows.** The two defenders guarding the offensive players in the corner should be positioned up near the elbows in helping positions — not pinned on their men in the corner. [S1, p.150]
4. **Post defenders one to two steps above their men.** The two defenders guarding low-post players are on the inside and one or two steps above the players they are guarding — denying easy catches and protecting against slips to the basket. [S1, p.150]
5. **Stop penetration — no draw-and-kick.** The entire defensive scheme is built to prevent the ball handler from driving and kicking to open shooters. Don't give the offense draw-and-kick opportunities. [S1, p.150]
6. **Tilt on overloads.** If the offense clears a man out and overloads one side, the four off-ball defenders must tilt and cover both elbows and boxes on the ball side. [S1, p.150]

## Player Responsibilities
- **PG (X1)**: Keeps the ball in front; forces sideline; primary penetration stopper — the most important job in this defense.
- **SG (X2)**: Positioned near the weak-side elbow in a helping position; ready to rotate or fake-and-recover on any drive.
- **SF (X3)**: Guards the strong-side wing from a helping position near the elbow; fakes to draw the shooter's attention, then recovers. [S1, p.150]
- **PF (X4)**: One to two steps above his low-post man; tilts toward the ball on overloads to cover the strong-side box.
- **C (X5)**: One to two steps above his low-post man; ready to protect the weak-side box; provides rim protection if X1 is beaten.

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-1-4-flat-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.60",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 26.0,
          "jersey": "1",
          "side": "offense",
          "label": "top_of_key"
        },
        {
          "role": "2",
          "x": -22.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "left_wing"
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
          "x": -8.0,
          "y": 29.0,
          "jersey": "4",
          "side": "offense",
          "label": "left_elbow"
        },
        {
          "role": "5",
          "x": 8.0,
          "y": 29.0,
          "jersey": "5",
          "side": "offense",
          "label": "right_elbow"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "right_sideline",
          "type": "dribble",
          "d": "M 0 26 C 5 25, 10 24, 14 22",
          "style": "zigzag"
        },
        {
          "from": "x3",
          "to": "3",
          "type": "cut",
          "d": "M 14 25 L 22 22",
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
          "label": "on_ball"
        },
        {
          "role": "x2",
          "x": -10.0,
          "y": 27.0,
          "jersey": "X2",
          "side": "defense",
          "label": "weak_side_elbow"
        },
        {
          "role": "x3",
          "x": 14.0,
          "y": 25.0,
          "jersey": "X3",
          "side": "defense",
          "label": "strong_side_elbow"
        },
        {
          "role": "x4",
          "x": -6.0,
          "y": 36.0,
          "jersey": "X4",
          "side": "defense",
          "label": "left_post_above"
        },
        {
          "role": "x5",
          "x": 9.0,
          "y": 34.0,
          "jersey": "X5",
          "side": "defense",
          "label": "right_post_above"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 26.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X1 forces 1 to sideline; X3 fakes and recovers to strong-side shooter",
          "x": 0,
          "y": 48
        }
      ]
    },
    {
      "label": "Figure 9.61",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 26.0,
          "jersey": "1",
          "side": "offense",
          "label": "top_of_key"
        },
        {
          "role": "2",
          "x": -22.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "left_wing"
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
          "x": 10.0,
          "y": 24.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_elbow_high"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 29.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "right_sideline",
          "type": "dribble",
          "d": "M 0 26 C 5 25, 10 24, 14 22",
          "style": "zigzag"
        },
        {
          "from": "4",
          "to": "right_elbow_high",
          "type": "cut",
          "d": "M 8 36 C 9 32, 10 28, 10 24",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "weak_side_elbow",
          "type": "cut",
          "d": "M -8 29 L -10 27",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "ball_side_box",
          "type": "cut",
          "d": "M 6 36 C 7 34, 8 33, 8 32",
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
          "label": "on_ball"
        },
        {
          "role": "x2",
          "x": -10.0,
          "y": 27.0,
          "jersey": "X2",
          "side": "defense",
          "label": "weak_side_elbow"
        },
        {
          "role": "x3",
          "x": 16.0,
          "y": 25.0,
          "jersey": "X3",
          "side": "defense",
          "label": "strong_side_wing"
        },
        {
          "role": "x4",
          "x": 8.0,
          "y": 32.0,
          "jersey": "X4",
          "side": "defense",
          "label": "strong_side_post_tilted"
        },
        {
          "role": "x5",
          "x": -6.0,
          "y": 34.0,
          "jersey": "X5",
          "side": "defense",
          "label": "left_post_above"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 26.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "4 clears out and comes high; X2 plays weak-side elbow; X3 fakes and stays with 3; X4 tilts to stop penetration",
          "x": 0,
          "y": 48
        }
      ]
    }
  ],
  "notes": "[S1, p.150] Figs 9.60 and 9.61 \u2014 One-four flat set defense. Fig 9.60: X1 keeps ball in front and forces sideline; X3 fakes toward the lane and recovers to the strong-side shooter (3); corner defenders (X2, X3) are up near the elbows rather than pinned on their men in the corners; post defenders (X4, X5) are one to two steps above their men. Fig 9.61: offense clears 4 high; X2 drops to cover the weak-side elbow; X3 fakes and stays with 3; X4 tilts toward ball side to stop penetration. Zigzag lines on 1's path indicate dribble; straight arrows indicate defender movement/recovery. Scan quality is good; arrow paths approximated from visible curves."
}
```
```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-1-4-flat-1.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.61",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 26.0,
          "jersey": "1",
          "side": "offense",
          "label": "top_of_key"
        },
        {
          "role": "2",
          "x": -20.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "left_wing"
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
          "x": -6.0,
          "y": 20.0,
          "jersey": "4",
          "side": "offense",
          "label": "left_elbow_area"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 14.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_high_post"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "right_wing",
          "type": "dribble",
          "d": "M 0 26 C 6 27, 12 25, 16 23",
          "style": "zigzag"
        },
        {
          "from": "4",
          "to": "left_elbow_area",
          "type": "cut",
          "d": "M -6 20 C -4 18, 2 16, 6 22",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "weak_side_elbow",
          "type": "cut",
          "d": "M -10 26 C -8 24, -5 22, -4 20",
          "style": "solid"
        },
        {
          "from": "x3",
          "to": "right_wing",
          "type": "cut",
          "d": "M 14 24 C 16 23, 18 22, 20 22",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "rim",
          "type": "cut",
          "d": "M 6 22 C 4 28, 2 34, 0 38",
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
          "label": "on_ball_top_key"
        },
        {
          "role": "x2",
          "x": -10.0,
          "y": 26.0,
          "jersey": "X2",
          "side": "defense",
          "label": "weak_side_elbow"
        },
        {
          "role": "x3",
          "x": 14.0,
          "y": 24.0,
          "jersey": "X3",
          "side": "defense",
          "label": "right_elbow"
        },
        {
          "role": "x4",
          "x": 6.0,
          "y": 22.0,
          "jersey": "X4",
          "side": "defense",
          "label": "strong_side_post"
        },
        {
          "role": "x5",
          "x": -4.0,
          "y": 28.0,
          "jersey": "X5",
          "side": "defense",
          "label": "left_post_above"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 26.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X1",
          "target_role": "x1",
          "x": 0,
          "y": 30
        },
        {
          "kind": "label",
          "text": "X2",
          "target_role": "x2",
          "x": -10,
          "y": 26
        },
        {
          "kind": "label",
          "text": "X3",
          "target_role": "x3",
          "x": 14,
          "y": 24
        },
        {
          "kind": "label",
          "text": "X4",
          "target_role": "x4",
          "x": 6,
          "y": 22
        },
        {
          "kind": "label",
          "text": "X5",
          "target_role": "x5",
          "x": -4,
          "y": 28
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "4 clears out and comes high; X2 plays weak-side elbow; X3 fakes and stays with 3; X4 tilts to stop penetration.",
          "x": 0,
          "y": 50
        }
      ]
    }
  ],
  "notes": "[S1, p.150] Fig 9.61 \u2014 One-four flat set overload scenario. Player 4 clears out and moves high (to the left elbow area). X1 (on-ball defender) forces 1 toward the sideline using a zigzag/dribble-pressure arrow. X2 shifts to play the weak-side elbow. X3 fakes and stays with 3 on the strong-side wing. X4 tilts toward the ball-side to stop penetration. Player 5 is positioned at the left high-post area. Dribble arrow for 1 shown as zigzag (wavy/zigzag line in original). Movement arrows for defenders shown as solid lines with arrowheads. Scan quality is moderate; exact control points approximated from visible arrow paths."
}
```

## Common Mistakes
1. **Corner defenders stay in the corner** → Point guard penetrates without help; kick-out passes produce wide-open 3-pointers. Correction: corner defenders must be up near the elbows.
2. **Post defenders too low** → Quick slip pass over the top for an easy catch-and-score. Correction: stay one or two steps above your man.
3. **Not tilting on overload** → One side is 3-on-2 or 4-on-3. Correction: the four off-ball defenders must all shift to cover elbows and boxes on the ball side.
4. **Ball handler beats X1 middle** → Drive to the lane; no help available. Correction: force sideline; never let the ball go middle in this set.

## Related Concepts
- [[trapping-and-double-teaming]] — when penetration does occur, trap rotations apply
- [[defending-pinch-post]] — post players in the 1-4 flat can flash to the pinch-post area

## Sources
- [S1, p.150] — Herb Brown's full explanation of defending the 1-4 flat set
