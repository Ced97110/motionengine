---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [defense, man-to-man, post-defense, flash-post, blind-pig, backdoor]
source_count: 1
last_updated: 2026-04-20
# Coordinate system: -28..28 x (sideline to sideline), 0..47 y (baseline to half-court)
# Origin (0,0) = center of the rim. Same frame as frontend PlayViewerV7.
diagram:
  kind: half_court
  positions:
    - id: X5
      x: 0
      y: 7
      label: "X5"
      role: "defender"
      emphasis: "primary"
    - id: O5
      x: -4
      y: 15
      label: "5"
      role: "offense"
      emphasis: "primary"
    - id: X2
      x: 18
      y: 10
      label: "X2"
      role: "defender"
    - id: O2
      x: 22
      y: 8
      label: "2"
      role: "offense"
    - id: X3
      x: -18
      y: 10
      label: "X3"
      role: "defender"
      emphasis: "help"
  arrows:
    - fromX: 0
      fromY: 7
      toX: -3
      toY: 13
      label: "Deny"
      emphasis: "primary"
    - fromX: 22
      fromY: 8
      toX: 4
      toY: 2
      label: "Backdoor"
      emphasis: "threat"
    - fromX: -18
      fromY: 10
      toX: -6
      toY: 4
      label: "Help cross lane"
      emphasis: "help"
---

# Defending the Flash Post (Blind Pig)

## Summary
The flash-post or "blind pig" action occurs when a post player reads his defender being pressured or overplayed on the perimeter and flashes up to the elbow or mid-post area to receive a pass. The offense uses this to punish tight on-ball pressure and often sequences it into a backdoor cut for the overplayed wing. Herb Brown's approach prioritizes denying the flash pass first, and then controlling all subsequent actions if the pass is caught. [S1, pp.148-149]

## When to Use
- Whenever your perimeter defenders are applying heavy on-ball or deny pressure
- Defending teams that use the flash-post as a primary ball-reversal or entry mechanism
- Any blind pig action where the wing is deliberately overplayed to invite the flash

## Key Principles
1. **Overplay and deny the flash-post pass.** The highest priority is preventing the initial flash-post catch. The post defender must overplay and contest the flash entry pass. [S1, p.148]
2. **If the ball is received, post defender steps back wide.** Once the flash-post player catches the ball, the post defender steps back, gets in a wide stance, bothers the passer, and occupies passing lanes. [S1, p.148]
3. **Wing defender keeps man in front.** The wing's defender must maintain vision on his man and keep him in front at all times. [S1, p.148]
4. **If wing defender loses his man,** he has two options: (a) open up, make himself wide, and retreat to the goal to take away the backdoor layup, OR (b) snap back and try to impede or deflect the pass to his man. [S1, p.148]
5. **Weak-side defenders drawn to the ball.** All weak-side help collapses toward the flash to deny re-entry and shrink the floor. [S1, p.148]
6. **Nearest defender forces the receiver high.** On the initial flash catch, the nearest defender forces the ball handler high so he receives the pass farther from the basket. [S1, p.148]
7. **Low-block defender covers the backdoor.** *"It is the responsibility of the defensive player on the low block to come across the lane to stop the offensive player trying to go backdoor."* [S1, p.148]
8. **Weak-side alignment: nail, elbow, box.** All weak-side defenders occupy the nail, elbow, and box positions — the key help positions. [S1, p.148]

## Player Responsibilities
- **PG (X1)**: May be the on-ball pressure defender whose pressure triggers the flash; must track cutter and stay with passer or recover to him.
- **SG (X2)**: Fights to keep wing player in front; if overplayed and man flashes, opens up wide or snaps back to deflect pass.
- **PF (X4)**: Primary post defender — overplays the flash, steps back wide on catch, bothers passer and occupies passing lanes.
- **SF (X3)**: Covers the weak-side elbow; drawn toward the ball on flash.
- **C (X5)**: Crosses the lane from the low block to cut off any backdoor attempt; provides weak-side help and must rebound. [S1, p.148]

## Variations
### Blind Pig (Pressure-Triggered Flash)
Specifically when X2's pressure on the wing is so heavy that the post player (4) reads the overplay and flashes to receive the ball: X4 must pressure the flash receiver; X2 fights to keep 2 in front; X5 is ready to cross the lane to cover the potential backdoor; X2 rotates to try to get inside 5 on the weak side. [S1, p.148]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-flash-post-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "dotted": "defensive_movement"
  },
  "phases": [
    {
      "label": "Figure 9.56 \u2014 Flash-post or blind pig: 4 flashes to the pinch post reading X2's overplay of 2. X4 pressures 4. X2 fights to keep 2 in front. X5 ready to cross lane. X2 rotates to get inside 5.",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 33.0,
          "jersey": "1",
          "side": "offense",
          "label": "top_of_key"
        },
        {
          "role": "2",
          "x": 20.0,
          "y": 22.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "3",
          "x": -20.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "4",
          "x": 8.0,
          "y": 26.0,
          "jersey": "4",
          "side": "offense",
          "label": "flashing_to_elbow"
        },
        {
          "role": "5",
          "x": -4.0,
          "y": 22.0,
          "jersey": "5",
          "side": "offense",
          "label": "left_elbow"
        }
      ],
      "actions": [
        {
          "from": "4",
          "to": "right_elbow",
          "type": "cut",
          "d": "M 8 26 C 6 24, 4 23, 4 22",
          "style": "solid"
        },
        {
          "from": "5",
          "to": "left_elbow",
          "type": "cut",
          "d": "M -4 22 L -8 21",
          "style": "solid"
        },
        {
          "from": "x5",
          "to": "right_low_block",
          "type": "cut",
          "d": "M -2 19 C 2 22, 5 28, 7 38",
          "style": "dotted"
        },
        {
          "from": "x2",
          "to": "5",
          "type": "cut",
          "d": "M 16 25 C 10 28, 4 30, -4 35",
          "style": "dotted"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 0.0,
          "y": 36.0,
          "jersey": "X1",
          "side": "defense",
          "label": "on_1_at_key"
        },
        {
          "role": "x2",
          "x": 16.0,
          "y": 25.0,
          "jersey": "X2",
          "side": "defense",
          "label": "on_2_right_wing"
        },
        {
          "role": "x3",
          "x": -12.0,
          "y": 24.0,
          "jersey": "X3",
          "side": "defense",
          "label": "weak_side_elbow"
        },
        {
          "role": "x4",
          "x": 5.0,
          "y": 24.0,
          "jersey": "X4",
          "side": "defense",
          "label": "pressuring_flash"
        },
        {
          "role": "x5",
          "x": -2.0,
          "y": 19.0,
          "jersey": "X5",
          "side": "defense",
          "label": "top_of_key_area"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 33.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "5",
          "x": -4,
          "y": 22
        },
        {
          "kind": "label",
          "text": "X5",
          "x": -2,
          "y": 19
        },
        {
          "kind": "label",
          "text": "X3",
          "x": -12,
          "y": 24
        },
        {
          "kind": "label",
          "text": "X4",
          "x": 5,
          "y": 24
        },
        {
          "kind": "label",
          "text": "X2",
          "x": 16,
          "y": 25
        },
        {
          "kind": "label",
          "text": "X1",
          "x": 0,
          "y": 36
        }
      ]
    }
  ],
  "notes": "[S1, p.148] Fig 9.56 \u2014 Flash-post (blind pig) defensive rotation. Offensive player 4 flashes from the low post to the elbow/pinch-post area reading the heavy overplay pressure X2 is applying to wing 2. X4 must contest and pressure the flash receiver. X2 fights to keep 2 in front. X5 is shown ready to cross the lane to cover potential backdoor cuts. X2 also has a rotation responsibility toward 5 on the weak side. Arrow line styles: solid = offensive movement/cuts, dotted = defensive rotations/movement. Scan quality is moderate; some defender positions are approximate, especially X5's starting position near the top of the key area."
}
```
```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-flash-post-1.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "dotted": "defensive_movement",
    "zigzag": "screen"
  },
  "phases": [
    {
      "label": "Figure 9.57",
      "players": [
        {
          "role": "1",
          "x": 12.0,
          "y": 37.0,
          "jersey": "1",
          "side": "offense",
          "label": "right_elbow_low"
        },
        {
          "role": "2",
          "x": 22.0,
          "y": 16.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing"
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
          "y": 40.0,
          "jersey": "4",
          "side": "offense",
          "label": "low_block_right"
        },
        {
          "role": "5",
          "x": 4.0,
          "y": 22.0,
          "jersey": "5",
          "side": "offense",
          "label": "elbow_right_high"
        }
      ],
      "actions": [
        {
          "from": "x5",
          "to": "left_corner",
          "type": "cut",
          "d": "M 4.00 18.00 C 0.00 22.00, -6.00 32.00, -8.00 40.00",
          "style": "solid"
        },
        {
          "from": "x2",
          "to": "2",
          "type": "cut",
          "d": "M 18.00 20.00 C 20.00 18.00, 22.00 16.00, 22.00 14.00",
          "style": "dashed"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 10.0,
          "y": 35.0,
          "jersey": "X1",
          "side": "defense",
          "label": "near_right_elbow"
        },
        {
          "role": "x2",
          "x": 18.0,
          "y": 20.0,
          "jersey": "X2",
          "side": "defense",
          "label": "right_wing_deny"
        },
        {
          "role": "x3",
          "x": -8.0,
          "y": 22.0,
          "jersey": "X3",
          "side": "defense",
          "label": "left_high_post"
        },
        {
          "role": "x4",
          "x": 7.0,
          "y": 38.0,
          "jersey": "X4",
          "side": "defense",
          "label": "right_low_block"
        },
        {
          "role": "x5",
          "x": 4.0,
          "y": 18.0,
          "jersey": "X5",
          "side": "defense",
          "label": "top_of_key"
        }
      ],
      "ball": {
        "x": 4.0,
        "y": 22.0,
        "possessed_by": "5"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "Figure 9.57",
          "x": 0,
          "y": 50
        },
        {
          "kind": "label",
          "text": "Flash-post or blind pig: X5 crosses lane and X2 opens up or snaps back to play 2.",
          "x": 0,
          "y": 52
        }
      ],
      "extras": [
        {
          "kind": "arrow_annotation",
          "text": "X5 crosses lane to cover backdoor",
          "target_role": "x5",
          "x": -4,
          "y": 28
        }
      ]
    }
  ],
  "notes": "[S1, p.149] Fig 9.57 \u2014 Flash-post or blind pig continuation: after 4 has flashed and received the ball at the elbow area, X5 crosses the lane to cut off any backdoor attempt by the overplayed wing, while X2 opens up or snaps back to contest the pass to 2. Offensive players 1 and 4 are positioned on the right side near the elbow/low-block; 5 has the ball at the right high post. Defenders X5 crosses from the top-of-key/nail area toward the left block to stop the backdoor. X2 recovers or opens wide toward 2 on the wing. Scan quality is fair; exact arrow curvature is approximated from visible markings."
}
```

## Common Mistakes
1. **Post defender doesn't deny the flash** → Easy catch at the elbow opens up easy scores for a skilled big. Correction: overplay and contest all flash-post entries.
2. **Wing defender watches the ball instead of man** → Wing slips backdoor for an easy layup. Correction: *"keep his man in front of him if possible"* — always maintain man awareness.
3. **Low-block defender stays home** → Backdoor cutter gets an easy layup off the flash. Correction: the low-block defender MUST cross the lane on any backdoor attempt.
4. **Weak side doesn't collapse** → Quick pass to the weak side corner produces open shots. Correction: nail, elbow, box must be occupied immediately.

## Related Concepts
- [[defending-pinch-post]] — similar two-man game at the elbow; shares the pass-and-follow reads
- [[trapping-and-double-teaming]] — if the flash is not denied, trapping the post applies
- [[post-splits-defense]] — flash-post sometimes sequences into post-split cuts

## Sources
- [S1, pp.148-149] — Herb Brown's explanation of flash-post/blind pig defense and weak-side rotation responsibilities
