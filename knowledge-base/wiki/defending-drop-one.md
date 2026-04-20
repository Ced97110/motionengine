---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, post-defense, man-to-man, isolation, pro, help-defense, double-team]
source_count: 1
last_updated: 2026-04-11
---

# Defending Drop One (pro Isolation Play)

## Summary
The "Drop One" is a common pro isolation play that places the primary scorer (Player 1) at the low post while teammates clear the strong side and occupy perimeter defenders. The offense aims to create a 1-on-1 post situation for their best scorer. Herb Brown uses this play to teach how defensive communication and positioning work together to deny the easy post feed and cover all help positions simultaneously.

Brown teaches this play in practice by first diagramming the offense and then discussing how to defend it — using the defense-of-the-play discussion as a learning tool to identify which players understand the concepts and which need more work. [S1, p.32]

## When to Use
- When the opponent's best scorer is a dominant low-post player
- When scouting reveals drop-play tendencies from the opposition
- As a teaching vehicle for help-side rotations and post-fronting concepts

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-drop-one-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "screen",
    "wavy": "screen"
  },
  "phases": [
    {
      "label": "Figure 3.1 \u2014 Drop one: one variation of the common drop play",
      "players": [
        {
          "role": "1",
          "x": -7.0,
          "y": 40.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_low_block"
        },
        {
          "role": "2",
          "x": 18.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "3",
          "x": -18.0,
          "y": 35.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_corner_wing"
        },
        {
          "role": "4",
          "x": -18.0,
          "y": 22.0,
          "jersey": "4",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 18.0,
          "jersey": "5",
          "side": "offense",
          "label": "top_of_key_left"
        }
      ],
      "actions": [
        {
          "from": "5",
          "to": "2",
          "type": "pass",
          "d": "M -8 18 C 4 18, 12 20, 18 22",
          "style": "solid"
        },
        {
          "from": "4",
          "to": "3",
          "type": "cut",
          "d": "M -18 22 L -18 35",
          "style": "solid"
        },
        {
          "from": "5",
          "to": "1",
          "type": "pass",
          "d": "M -8 18 C -8 28, -8 33, -7 40",
          "style": "dashed"
        }
      ],
      "ball": {
        "x": -8.0,
        "y": 18.0,
        "possessed_by": "5"
      }
    },
    {
      "label": "Figure 3.2 \u2014 Defending drop one playing behind 1: if X1 fronts, X5 can look to double from across the lane and all other elbows and boxes are covered",
      "players": [
        {
          "role": "1",
          "x": -7.0,
          "y": 40.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_low_block"
        },
        {
          "role": "2",
          "x": 18.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "3",
          "x": -18.0,
          "y": 35.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_corner_wing"
        },
        {
          "role": "4",
          "x": -18.0,
          "y": 22.0,
          "jersey": "4",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 18.0,
          "jersey": "5",
          "side": "offense",
          "label": "top_of_key_left"
        }
      ],
      "actions": [
        {
          "from": "x5",
          "to": "1",
          "type": "cut",
          "d": "M 3 32 C -1 35, -3 38, -5 41",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "x3",
          "type": "cut",
          "d": "M 8 29 L -8 29",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -5.0,
          "y": 41.0,
          "jersey": "X1",
          "side": "defense",
          "label": "on_ball_post"
        },
        {
          "role": "x2",
          "x": 7.0,
          "y": 39.0,
          "jersey": "X2",
          "side": "defense",
          "label": "weak_side_box"
        },
        {
          "role": "x3",
          "x": -8.0,
          "y": 29.0,
          "jersey": "X3",
          "side": "defense",
          "label": "weak_side_elbow"
        },
        {
          "role": "x4",
          "x": 8.0,
          "y": 29.0,
          "jersey": "X4",
          "side": "defense",
          "label": "strong_side_elbow"
        },
        {
          "role": "x5",
          "x": 3.0,
          "y": 32.0,
          "jersey": "X5",
          "side": "defense",
          "label": "weak_side_lane"
        }
      ],
      "annotations": [
        {
          "kind": "label",
          "text": "X1 fronts or plays behind 1",
          "target_role": "x1",
          "x": -7,
          "y": 43
        },
        {
          "kind": "label",
          "text": "X5 doubles from across the lane",
          "target_role": "x5",
          "x": 3,
          "y": 31
        }
      ]
    }
  ]
}
```

## Key Principles
1. **Option A — Play behind Player 1**: X1 defends behind the post player, relying on physicality and position to discourage the feed and deny easy catches.
2. **Option B — Front Player 1**: X1 fronts the low-post player completely, denying the entry pass. If fronting, X5 must read from across the lane and be prepared to double immediately when the ball is fed over the front.
3. **X5 positioning is critical when fronting**: X5 pre-rotates toward the lane from the weak side so he can double immediately if the lob pass is thrown over the front.
4. **All elbows and boxes must be covered**: When X1 fronts and X5 doubles, X3, X4, and X2 rotate to cover the weak-side elbow, strong-side elbow, and weak-side box to deny skip passes and reversal passes.
5. **Communication is mandatory**: The entire rotation must be called out as the ball enters the post area — silent rotations lead to open shooters.

## Player Responsibilities
- **X1 (on-ball post defender)**: Either front or play behind Player 1 per game plan; contest every catch; do not permit easy position.
- **X5 (weak-side big)**: Pre-rotate toward the lane; if X1 fronts, be ready to double over the top of the front; cover weak-side box otherwise.
- **X2 (weak-side guard)**: Cover the weak-side box and deny any swing pass to the corner.
- **X3 (weak-side wing)**: Cover the weak-side elbow; be ready to rotate to the perimeter on a kick-out pass.
- **X4 (strong-side big/wing)**: Cover the strong-side elbow; deny ball reversal to the high post.

## Common Mistakes
1. **X5 failing to pre-rotate when X1 fronts** → The lob over the front goes unchecked for an easy layup; X5 must anticipate and close before the pass.
2. **Perimeter defenders ball-watching** → X3/X4/X2 must maintain awareness of both the ball and their assignments in the help rotation.
3. **X1 going behind on a known scorer** → If the opponent's best player catches cleanly at the low post, the defense is in trouble; fronting is preferable for elite scorers.

## Related Concepts
- [[post-defense-fronting]] — Full treatment of fronting the low post
- [[daily-defensive-checklist]] — Rule #9: Front or three-quarter the post on the ball side
- [[defending-cross-four-get]] — The second pro sample play from the same teaching exercise
- [[basic-rules-of-defense]] — The baseline rules that apply to post defense

## Sources
- [S1, pp.32-33] — Herb Brown's Drop One offensive play and defensive scheme (Figures 3.1–3.2)
