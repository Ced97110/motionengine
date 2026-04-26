---
type: drill
level: intermediate
positions: [PF, C]
players_needed: 3-5
duration_minutes: 10-15
tags: [defense, post-defense, fronting, man-to-man, low-post]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: post-defense-fronting
    emphasis: primary
  - id: post-defense-three-quartering
    emphasis: primary
  - id: defensive-positioning
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: core_outer
    emphasis: secondary
  - region: ankle_complex
    emphasis: secondary
---

# One-on-One Post Defense: Three-Quartering and Fronting

## Objective
Teach the post defender to position correctly (three-quarter or full front) based on ball location, and to sit on the offensive player's legs to prevent jumping. [S1, p.58]

## Setup
- Half court
- 3 passers (P1, P2, P3) positioned at corner, wing, and top
- 1 offensive post player at the low block
- 1 defensive post player

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/drill-post-defense-three-quarter-fronting-0.png",
  "court_region": "half",
  "legend": {
    "dashed": "pass",
    "solid": "cut",
    "dotted": "pass"
  },
  "phases": [
    {
      "label": "Figure 5.17 \u2014 Post defense: three-quarter (corner/top) vs. full front (wing)",
      "players": [
        {
          "role": "P1",
          "x": -22.0,
          "y": 42.0,
          "jersey": "P1",
          "side": "offense",
          "label": "left_corner_passer"
        },
        {
          "role": "P2",
          "x": -18.0,
          "y": 30.0,
          "jersey": "P2",
          "side": "offense",
          "label": "left_wing_passer"
        },
        {
          "role": "P3",
          "x": -8.0,
          "y": 22.0,
          "jersey": "P3",
          "side": "offense",
          "label": "top_of_key_passer"
        },
        {
          "role": "1",
          "x": -7.0,
          "y": 40.0,
          "jersey": "1",
          "side": "offense",
          "label": "offensive_post_low_block"
        }
      ],
      "actions": [
        {
          "from": "P1",
          "to": "P2",
          "type": "pass",
          "d": "M -22 42 L -18 30",
          "style": "dashed"
        },
        {
          "from": "P2",
          "to": "P3",
          "type": "pass",
          "d": "M -18 30 L -8 22",
          "style": "dashed"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -4.0,
          "y": 37.0,
          "jersey": "X",
          "side": "defense",
          "label": "post_defender_fronting"
        }
      ],
      "ball": {
        "x": -22.0,
        "y": 42.0,
        "possessed_by": "P1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "FRONT",
          "x": -2,
          "y": 36,
          "target_role": "x1"
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "Post defense general rule: play three-quarter with ball in the corner or on top. Front with ball on the wing. Three-quarter or front with the ball at the top.",
          "x": 0,
          "y": 50
        }
      ]
    }
  ],
  "notes": "[S1, p.58] Figure 5.17 \u2014 Three passers (P1 at left corner, P2 at left wing, P3 at top of key) feed a low-post offensive player (1) while the post defender (X) adjusts between three-quarter and full-front positioning. General rule per the book: three-quarter when ball is in corner or on top; full front when ball is on the wing. The \"FRONT\" annotation appears next to the defender in the diagram. Dashed lines indicate ball movement among passers. Defender sitting on offensive player's legs is described in prose but not separately depicted as an arrow."
}
```

## Execution
1. Three passers pass among themselves: P1 (corner) → P2 (wing) → P3 (top) → back.
2. **General rule** (Figure 5.17):
   - Ball in the **corner or on top**: play **three-quarter** position
   - Ball on the **wing**: play **full front**
   - Ball at the **top**: three-quarter OR front, depending on scout/scheme
3. The post defender steps across with his **inside foot** to front and **sits on the legs** of the offensive player as the ball moves to the wing.
4. As the ball passes from P1 to P2 to P3, the defender adjusts position — three-quartering the post again when the ball moves off the wing.
5. The defender sits on the offensive player's legs throughout to prevent him from jumping for a lob pass. [S1, p.58]

## Coaching Points
- "Step across with the inside foot to front" — footwork is the key to getting position
- "Sit on the legs" — this stops the offensive player from jumping for lob passes over the top
- Three-quarter on top/corner; full front on wing — this rule must be automatic
- When fronting the post, perimeter defenders MUST pressure the passers to make entry difficult [S1, p.50]
- Always provide weak-side help when fronting

## Progressions
1. **Beginner**: Walk-through; post player is stationary, no live passing
2. **Intermediate**: Passers pass at game speed; post player fights for position
3. **Advanced**: Add the two-on-two version (Figure 5.18) where the passer's defender also participates — when the pass goes to the post, the passer's defender drops level with the ball (butt to baseline) to force the cutter away from the baseline and toward defensive help [S1, pp.58-59]

## Concepts Taught
- [[post-defense-fronting]] — the detailed fronting technique these drills build
- [[defensive-checklist-principles]] — checklist items 47, 55: defending high-post player with ball on perimeter; taking away post position
- [[defensive-shell-drill]] — post defense is one segment of the full shell drill

## Sources
- [S1, pp.58-59] — One-on-One Post Defense, Figures 5.17, 5.18, 5.19