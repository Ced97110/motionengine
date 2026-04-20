---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [defense, help-defense, weak-side, rotation, man-to-man, team-defense]
source_count: 1
last_updated: 2026-04-11
---

# Weak-Side Defense and Rotation

## Summary
Weak-side defense is the connective tissue of Brown's man-to-man system. Every off-ball defender must maintain visual contact with both their man and the ball at all times — never turning their back to the basketball. The critical trigger for weak-side movement is the pass or dribble, not the catch. Defenders must be moving to help while the ball is in the air so they arrive in help position the instant the offensive player catches it. [S1, pp.12-15]

The system uses the "buddy" concept: each defender is responsible for helping the two teammates nearest to them on either side. All five defenders shrink the floor and clog driving lanes as the ball moves away from them. Off-ball defenders can establish position in the lane to take offensive charges, turning help defense into a demoralizing momentum swing. [S1, p.14]

## When to Use
- Every half-court man-to-man defensive possession
- After any dribble penetration — off-ball defenders rotate to stop the drive
- After post doubles — rotation rules apply when the ball is kicked out
- When defending crossing actions — defenders must immediately clog the pass/drive lane

## Key Principles
1. **Never turn your back to the ball** — weak-side defenders must always see the basketball [S1, p.14]
2. **Move on the pass or dribble, not on the catch** — be in help position when the ball arrives, not after [S1, pp.12-13]
3. **Shrink the floor** — as the ball moves away from a defender, that defender moves toward the ball and the lane to clog passing and driving lanes [S1, p.12]
4. **The buddy system** — each defender is responsible for helping the two nearest teammates; communicate and cover each other's backs [S1, p.14]
5. **Take charges** — off-ball defenders establish position in driving lanes to draw offensive fouls; a charge demoralizes opponents and energizes the defense [S1, p.13]
6. **Force the extra pass** — defenders clog lanes to make the offense pass one more time before a good shot is available; each extra pass is an opportunity for a deflection or turnover [S1, p.12]
7. **After a double stack turnout** — the defender on the ball pressures the passer, then immediately jumps back toward the ball to clog the passing lane and prevent the receiver from penetrating or shooting [S1, p.13]

## Post Double-Team Rotation
When a post player is double-teamed and kicks the ball out, rotation assignments depend on where the pass goes. The trapper (the defender who rotated in to double) is typically the player who sprints out of the double-team to close out. [S1, p.15]

### Rotation Scenarios (Figures 1.1–1.3)
**Setup:** 5 (post) is being trapped from the weak-side high by X5 and X4. Defensive numbers are alongside X (i.e., X1 guards 1, X2 guards 2, etc.)

- **Cross-court pass from 5 to 3 (wing):** X2 rotates to contest 3 on the wing [S1, Fig.1.2]
- **Pass from 5 to 3 in the corner:** X4 takes 3 in the corner; X3 takes 4 (X4's original man), unless X5 arrives first [S1, Fig.1.2-1.3]
- **Short pass to near corner:** The trapper facing the ball rotates because he has the quicker, more direct path to the ball without needing to turn and pivot first [S1, p.15]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/weak-side-defense-rotation-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 1.1 \u2014 Trapping the post from weak-side high: cross-court pass from 5 to 3",
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
          "x": 0.0,
          "y": 44.0,
          "jersey": "2",
          "side": "offense",
          "label": "baseline_center"
        },
        {
          "role": "3",
          "x": 21.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "4",
          "x": 4.0,
          "y": 18.0,
          "jersey": "4",
          "side": "offense",
          "label": "high_post_right"
        },
        {
          "role": "5",
          "x": -10.0,
          "y": 22.0,
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
          "d": "M -10 22 C 5 18, 14 18, 21 22",
          "style": "dashed"
        },
        {
          "from": "x1",
          "to": "1",
          "type": "cut",
          "d": "M -18 28 L -22 30",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -18.0,
          "y": 28.0,
          "jersey": "X1",
          "side": "defense",
          "label": "on_1"
        },
        {
          "role": "x2",
          "x": 2.0,
          "y": 36.0,
          "jersey": "X2",
          "side": "defense",
          "label": "on_2"
        },
        {
          "role": "x3",
          "x": 18.0,
          "y": 26.0,
          "jersey": "X3",
          "side": "defense",
          "label": "on_3"
        },
        {
          "role": "x4",
          "x": 0.0,
          "y": 20.0,
          "jersey": "X4",
          "side": "defense",
          "label": "on_4_trapping_5"
        },
        {
          "role": "x5",
          "x": -7.0,
          "y": 22.0,
          "jersey": "X5",
          "side": "defense",
          "label": "on_5_trapping"
        }
      ],
      "ball": {
        "x": -10.0,
        "y": 22.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Defensive number alongside X. Change in all directions.",
          "x": 0,
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
          "y": 26.0,
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
          "x": 22.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "4",
          "x": 4.0,
          "y": 18.0,
          "jersey": "4",
          "side": "offense",
          "label": "high_post_right"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 22.0,
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
          "d": "M -8 22 C 5 17, 14 18, 22 22",
          "style": "dashed"
        },
        {
          "from": "x4",
          "to": "3",
          "type": "cut",
          "d": "M 0 20 C 8 22, 14 22, 22 22",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "3",
          "type": "cut",
          "d": "M 2 36 C 8 32, 14 28, 22 22",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -14.0,
          "y": 24.0,
          "jersey": "X1",
          "side": "defense",
          "label": "near_5_trap"
        },
        {
          "role": "x2",
          "x": 2.0,
          "y": 36.0,
          "jersey": "X2",
          "side": "defense",
          "label": "rotating_to_3"
        },
        {
          "role": "x3",
          "x": 12.0,
          "y": 30.0,
          "jersey": "X3",
          "side": "defense",
          "label": "sinking_to_help"
        },
        {
          "role": "x4",
          "x": 0.0,
          "y": 20.0,
          "jersey": "X4",
          "side": "defense",
          "label": "trapping_5"
        },
        {
          "role": "x5",
          "x": -6.0,
          "y": 22.0,
          "jersey": "X5",
          "side": "defense",
          "label": "trapping_5"
        }
      ],
      "ball": {
        "x": -8.0,
        "y": 22.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X2 rotates to 3 on the wing",
          "x": 14,
          "y": 20
        },
        {
          "kind": "label",
          "text": "Had pass been to 3 in corner: X4 gets 3, X3 gets 4 unless X5 there first (see Fig 1.3)",
          "x": 0,
          "y": 48
        }
      ]
    },
    {
      "label": "Figure 1.3 \u2014 Rotation on pass cross court from 5 to 3 (corner option)",
      "players": [
        {
          "role": "1",
          "x": -22.0,
          "y": 26.0,
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
          "x": 22.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_wing_or_corner"
        },
        {
          "role": "4",
          "x": 4.0,
          "y": 18.0,
          "jersey": "4",
          "side": "offense",
          "label": "high_post_right"
        },
        {
          "role": "5",
          "x": -8.0,
          "y": 22.0,
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
          "d": "M -8 22 C 5 17, 14 17, 22 22",
          "style": "dashed"
        },
        {
          "from": "x4",
          "to": "3",
          "type": "cut",
          "d": "M 0 20 C 8 24, 14 28, 22 38",
          "style": "solid"
        },
        {
          "from": "x3",
          "to": "4",
          "type": "cut",
          "d": "M 12 28 C 8 24, 5 20, 4 18",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 4 36 C 2 38, 0 40, 0 44",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -14.0,
          "y": 24.0,
          "jersey": "X1",
          "side": "defense",
          "label": "near_5_trap"
        },
        {
          "role": "x2",
          "x": 4.0,
          "y": 36.0,
          "jersey": "X2",
          "side": "defense",
          "label": "sinking"
        },
        {
          "role": "x3",
          "x": 12.0,
          "y": 28.0,
          "jersey": "X3",
          "side": "defense",
          "label": "rotating_to_4"
        },
        {
          "role": "x4",
          "x": 0.0,
          "y": 20.0,
          "jersey": "X4",
          "side": "defense",
          "label": "rotating_to_3_corner"
        },
        {
          "role": "x5",
          "x": -6.0,
          "y": 22.0,
          "jersey": "X5",
          "side": "defense",
          "label": "trapping_5"
        }
      ],
      "ball": {
        "x": -8.0,
        "y": 22.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X4 gets 3 in corner; X3 covers 4; X5 may arrive first",
          "x": 12,
          "y": 18
        }
      ]
    }
  ],
  "notes": "[S1, p.15] Figures 1.1\u20131.3 \u2014 Post double-team weak-side rotation series. Fig 1.1 shows the initial trap on 5 (post) at the left elbow by X5 and X4, with dashed cross-court pass to 3 on the right wing and all defenders in pre-rotation positions. Fig 1.2 shows the rotation triggered by the outlet pass to 3 on the wing: X2 sprints from baseline area to close out on 3. Fig 1.3 shows the alternative corner rotation: X4 chases 3 to the corner, X3 covers 4 (X4's vacated man), and X2 sinks toward 2. Defensive jersey glyphs are drawn as numbers alongside an X symbol. Coordinates approximated from the small diagrams; some path curvature is estimated due to scan resolution."
}
```

## Common Mistakes
1. **Moving on the catch** → by the time you react to the catch, penetration has already beaten the help; move when the ball leaves the passer's hands [S1, p.13]
2. **Turning your back to the ball** → you cannot see the pass or dribble trigger and will always be late [S1, p.14]
3. **Wrong trapper rotating** → the trapper facing the ball rotates on a short pass; assign roles clearly before the double-team [S1, p.15]
4. **Help getting beaten** → the system requires that the help itself does not give up easy baskets — help must be positioned to stop, not just slow, penetration [S1, p.11]

## Related Concepts
- [[defensive-coaching-philosophy-herb-brown]] — the philosophy that requires all five defenders to share weak-side help
- [[post-double-team-rotation]] — the specific rotation schemes when the post double-team ball is kicked out
- [[defensive-keys-to-victory]] — weak-side help directly addresses keys #7 (eliminate penetration) and #4 (pressure the ball)
- [[transition-defense]] — similar movement principles: move before the catch, protect the paint

## Sources
- [S1, pp.12-15] — Weak-Side Defense section and post double-team rotation with Figures 1.1–1.3
