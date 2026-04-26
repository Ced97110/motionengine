---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, man-to-man, pick-and-roll, cross-screen, pro, help-defense, rotation, blitz]
source_count: 1
last_updated: 2026-04-11
---

# Defending Cross Four Get / Fist / Out (pro Set Play)

## Summary
The "Cross Four Get" (also called "Cross Four Fist" or "Cross Four Out") is an pro set play combining a cross screen into a side pick-and-roll. Player 1 sets a cross screen for Player 4, then 4 uses a side PnR to attack the basket. The play creates a two-action sequence that stresses the defense with both a post relocation and a live-ball PnR in rapid succession.

Herb Brown uses this play to teach three distinct defensive reads: (1) how to defend the initial cross screen, (2) how to navigate the screener's defender when the PnR begins, and (3) the big-to-big rotation when the defense decides to blitz/trap the PnR. [S1, pp.32-33]

## When to Use
- When the opponent runs cross-screen into PnR actions
- As a teaching vehicle for PnR defensive rotations and screen-navigation decisions
- Advanced defensive scheme work for high school through professional levels

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-cross-four-get-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "screen",
    "wavy": "screen"
  },
  "phases": [
    {
      "label": "Figure 3.3 \u2014 Cross four get; cross four fist; cross four out (offensive play)",
      "players": [
        {
          "role": "1",
          "x": -7.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_block_area"
        },
        {
          "role": "2",
          "x": 18.0,
          "y": 26.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "3",
          "x": -18.0,
          "y": 26.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "4",
          "x": 8.0,
          "y": 22.0,
          "jersey": "4",
          "side": "offense",
          "label": "high_post_right"
        },
        {
          "role": "5",
          "x": 14.0,
          "y": 30.0,
          "jersey": "5",
          "side": "offense",
          "label": "right_elbow_area"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "4",
          "type": "screen",
          "d": "M -7 38 C -4 35, 4 32, 8 28",
          "style": "solid"
        },
        {
          "from": "4",
          "to": "right_wing",
          "type": "cut",
          "d": "M 8 22 C 12 20, 16 22, 18 24",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "1",
          "type": "pass",
          "d": "M -18 26 C -14 30, -10 35, -7 38",
          "style": "dashed"
        },
        {
          "from": "5",
          "to": "2",
          "type": "screen",
          "style": "solid"
        },
        {
          "from": "2",
          "to": "right_corner",
          "type": "cut",
          "d": "M 18 26 L 22 36",
          "style": "solid"
        }
      ],
      "annotations": [
        {
          "kind": "label",
          "text": "Cross four get; cross four fist; cross four out",
          "x": 0,
          "y": 50
        }
      ]
    },
    {
      "label": "Figure 3.4 \u2014 Cross four get defense: X4 forces 4 from low to high following cross screen by 1",
      "players": [
        {
          "role": "1",
          "x": -7.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_block"
        },
        {
          "role": "2",
          "x": 22.0,
          "y": 36.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_corner_area"
        },
        {
          "role": "3",
          "x": -18.0,
          "y": 26.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "4",
          "x": 16.0,
          "y": 20.0,
          "jersey": "4",
          "side": "offense",
          "label": "right_wing_high"
        },
        {
          "role": "5",
          "x": 10.0,
          "y": 28.0,
          "jersey": "5",
          "side": "offense",
          "label": "right_elbow"
        }
      ],
      "actions": [
        {
          "from": "4",
          "to": "right_wing",
          "type": "cut",
          "d": "M 8 30 C 10 26, 13 22, 16 20",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "4",
          "type": "cut",
          "d": "M 10 22 C 12 20, 14 19, 16 20",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -5.0,
          "y": 36.0,
          "jersey": "X1",
          "side": "defense",
          "label": "near_1"
        },
        {
          "role": "x2",
          "x": 20.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "right_wing_def"
        },
        {
          "role": "x3",
          "x": -15.0,
          "y": 24.0,
          "jersey": "X3",
          "side": "defense",
          "label": "left_wing_def"
        },
        {
          "role": "x4",
          "x": 12.0,
          "y": 18.0,
          "jersey": "X4",
          "side": "defense",
          "label": "high_post_def"
        },
        {
          "role": "x5",
          "x": 4.0,
          "y": 30.0,
          "jersey": "X5",
          "side": "defense",
          "label": "paint_center"
        }
      ],
      "annotations": [
        {
          "kind": "label",
          "text": "X4 forces 4 from low to high over screen by 1",
          "x": 0,
          "y": 50
        }
      ]
    },
    {
      "label": "Figure 3.5 \u2014 Cross four get defense: X3 forces 3 toward middle, goes inside screen by 4 as X4 zones up; X4 recovers to 4 rolling",
      "players": [
        {
          "role": "1",
          "x": -7.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "left_block"
        },
        {
          "role": "2",
          "x": 20.0,
          "y": 30.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "3",
          "x": -18.0,
          "y": 28.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "4",
          "x": 6.0,
          "y": 35.0,
          "jersey": "4",
          "side": "offense",
          "label": "rolling_to_basket"
        },
        {
          "role": "5",
          "x": 14.0,
          "y": 26.0,
          "jersey": "5",
          "side": "offense",
          "label": "right_elbow_pnr"
        }
      ],
      "actions": [
        {
          "from": "x3",
          "to": "3",
          "type": "cut",
          "d": "M -14 26 C -10 26, -8 28, -6 30",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "4",
          "type": "cut",
          "d": "M -8 28 C -2 30, 2 33, 6 35",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "rim",
          "type": "dribble",
          "d": "M -18 28 C -10 28, -4 32, 0 43",
          "style": "solid"
        },
        {
          "from": "4",
          "to": "rim",
          "type": "cut",
          "d": "M 14 26 C 10 30, 7 35, 4 40",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 2.0,
          "y": 22.0,
          "jersey": "X1",
          "side": "defense",
          "label": "top_key"
        },
        {
          "role": "x2",
          "x": 17.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "right_wing_def"
        },
        {
          "role": "x3",
          "x": -14.0,
          "y": 26.0,
          "jersey": "X3",
          "side": "defense",
          "label": "left_wing_def"
        },
        {
          "role": "x4",
          "x": -8.0,
          "y": 28.0,
          "jersey": "X4",
          "side": "defense",
          "label": "showing_on_3"
        },
        {
          "role": "x5",
          "x": 4.0,
          "y": 28.0,
          "jersey": "X5",
          "side": "defense",
          "label": "top_paint"
        }
      ],
      "annotations": [
        {
          "kind": "label",
          "text": "X3 forces 3 middle; X4 zones up then recovers to rolling 4",
          "x": 0,
          "y": 50
        }
      ]
    },
    {
      "label": "Figure 3.6 \u2014 Cross four get defense: big-to-big rotation; X4 stops ball then recovers into lane; X2 helps on 3 then recovers to 2",
      "players": [
        {
          "role": "1",
          "x": 18.0,
          "y": 26.0,
          "jersey": "1",
          "side": "offense",
          "label": "right_wing_ball_handler"
        },
        {
          "role": "2",
          "x": 22.0,
          "y": 38.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_corner"
        },
        {
          "role": "3",
          "x": -18.0,
          "y": 30.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "4",
          "x": -10.0,
          "y": 38.0,
          "jersey": "4",
          "side": "offense",
          "label": "left_block_area"
        },
        {
          "role": "5",
          "x": 8.0,
          "y": 34.0,
          "jersey": "5",
          "side": "offense",
          "label": "right_paint_drive"
        }
      ],
      "actions": [
        {
          "from": "x4",
          "to": "1",
          "type": "cut",
          "d": "M 14 24 L 18 24",
          "style": "solid"
        },
        {
          "from": "x5",
          "to": "5",
          "type": "cut",
          "d": "M 2 30 C 4 31, 6 32, 8 34",
          "style": "solid"
        },
        {
          "from": "x4",
          "to": "rim",
          "type": "cut",
          "d": "M 14 24 C 10 28, 6 32, 4 40",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M -10 28 C 4 30, 14 36, 22 38",
          "style": "solid"
        },
        {
          "from": "3",
          "to": "rim",
          "type": "dribble",
          "d": "M -18 30 C -12 30, -6 34, 0 43",
          "style": "dashed"
        },
        {
          "from": "5",
          "to": "rim",
          "type": "cut",
          "d": "M 8 34 C 6 37, 4 40, 2 43",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 4.0,
          "y": 22.0,
          "jersey": "X1",
          "side": "defense",
          "label": "top_key_def"
        },
        {
          "role": "x2",
          "x": -10.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "helping_on_3"
        },
        {
          "role": "x3",
          "x": -16.0,
          "y": 28.0,
          "jersey": "X3",
          "side": "defense",
          "label": "left_wing_def"
        },
        {
          "role": "x4",
          "x": 14.0,
          "y": 24.0,
          "jersey": "X4",
          "side": "defense",
          "label": "blitz_on_ball"
        },
        {
          "role": "x5",
          "x": 2.0,
          "y": 30.0,
          "jersey": "X5",
          "side": "defense",
          "label": "crossing_lane"
        }
      ],
      "annotations": [
        {
          "kind": "label",
          "text": "Blitz/trap PnR; big-to-big rotation; X4 recovers into lane",
          "x": 0,
          "y": 50
        }
      ],
      "extras": [
        {
          "kind": "screen_marker",
          "label": "cross screen / PnR screen marks near left block",
          "x": -10,
          "y": 38
        }
      ]
    }
  ],
  "notes": "[S1, pp.32-33] Four diagrams for the cross-screen into side PnR play and its three defensive frames. Fig 3.3 is the offensive base play; Figs 3.4\u20133.6 are successive defensive reads. Coordinates approximated from low-resolution scan; arrow paths are best-fit estimates. Wavy/zigzag marks near the left block in Figs 3.5\u20133.6 indicate screen actions."
}
```

## Phases

### Phase 1 — Defending the Cross Screen (Frame 1)
- **X4 bodies up** and forces Player 4 **from low to high** over the cross screen set by Player 1.
- The goal is to prevent Player 4 from cutting underneath and receiving the ball at the low block.
- X4 must anticipate the screen, beat Player 4 to the spot, and ride him high — not allowing a soft catch on the block. [S1, p.33]

### Phase 2 — Navigating the Side PnR (Frame 2)
- **X3 forces Player 3 toward the middle** and goes **inside the screen** set by Player 4.
- As X3 navigates the screen, **X4 either hard-contact shows OR zones up** to let X3 fight through.
- After X3 clears, **X4 recovers to Player 4 rolling to the basket.**
- Alternative: X4 can body up and ride the screener (Player 4) low and out of bounds, eliminating the roll threat entirely. [S1, p.33]

### Phase 3 — Blitz/Trap the Side PnR (Frame 3)
- **Decision: Show hard or blitz (trap) the side PnR.**
- Once X4 stops the ball, **X5 crosses the lane and pre-rotates** to pick up any paint penetration.
- X4 dives into the lane after making the show to help X1 stop Player 5 driving into the paint.
- X2 is ready to help stop Player 3's penetration, then recover back to Player 2.
- **If Player 5 pops back** instead of driving, X4 runs and rotates to defend Player 5 and stop the pass from Player 3 to Player 5. [S1, p.33]

## Key Coaching Points
- **"Rotate big to big"** — when blitzing, the weak-side big (X5) must pre-rotate before the pass is made, not after.
- **Read whether the roller pops or dives**: X4's recovery destination changes completely based on Player 5's action after the screen.
- **X4 is the busiest defender in this scheme**: he defends the cross screen, navigates the PnR, and makes the blitz — conditioning and basketball IQ are essential.
- **Communication between X3 and X4** is mandatory before and during the PnR to avoid both defenders guarding the same player.

## Common Mistakes
1. **X4 losing Player 4 under the cross screen** → X4 must beat Player 4 to the spot; playing behind creates an easy low-post feed.
2. **X5 failing to pre-rotate before the pass** → A late rotation leaves the paint open; X5 must move as the trap forms, not when the ball is released.
3. **X2 forgetting his recovery assignment** → After helping on Player 3's penetration, X2 must sprint back to Player 2 on the weak side or risk an open three.
4. **Confusing pop vs. dive read** → If X4 follows the roll when Player 5 actually pops, the open three-pointer is gifted; read the roller's body language immediately.

## Related Concepts
- [[defending-drop-one]] — The companion pro teaching play from the same practice session
- [[pick-and-roll-defense]] — General PnR defensive principles underlying this scheme
- [[daily-defensive-checklist]] — Rules #8 (slip screens), #14 (rotate to free man), #39 (hard-trap and jump out when switching)
- [[basic-rules-of-defense]] — The foundational rules that govern all rotations in this scheme

## Sources
- [S1, pp.32-33] — Herb Brown's Cross Four Get/Fist/Out offensive play and three-frame defensive scheme (Figures 3.3–3.6)
