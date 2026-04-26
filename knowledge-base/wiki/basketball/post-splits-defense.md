---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [defense, man-to-man, post-defense, post-splits, switching, communication]
source_count: 1
last_updated: 2026-04-11
---

# Defending Post Splits

## Summary
Post splits occur when a post player receives the ball and two cutters simultaneously run off him in opposite directions — attempting to split the defense and create a layup. This is a common companion action to post-entry passes and demands disciplined communication and aggressive switching by the defenders involved. Herb Brown emphasizes that talking and getting level with the ball are the two most critical defensive responses. [S1, p.149]

## When to Use
- Defending any post-entry that is followed by two cutters splitting off the post
- Particularly relevant against teams that use the high-post split ("pass to the elbow, cut over/under") as a primary half-court action
- Also applies to low-post splits where guards use the post as a screen

## Key Principles
1. **Defenders must talk.** The most important requirement in defending post splits is constant communication between the two defenders involved. Silence creates confusion. [S1, p.149]
2. **Get level with the ball.** Both defenders must get their bodies even with the offensive post man who has the ball. This takes away quick slips and cuts before they develop. [S1, p.149]
3. **Get level to switch.** For a defensive switch to be effective, both defenders must be at ball-level before the switch is executed. Switching from behind never works. [S1, p.149]
4. **The back man calls the switch.** In any high split or split that may require a switch, *the back man is responsible for calling both the pick and the switch* — he has the best view of what the offense is setting up. [S1, p.149]
5. **Don't let cutters split the switch.** The defense cannot allow two offensive cutters to run through the gap created during the switch. Seal the switch by locking inside legs together. [S1, p.149]
6. **Aggressive switch.** When defenders are forced to switch, they must do so assertively — taking ownership of the new assignment immediately, not tentatively. [S1, p.149]

## Player Responsibilities
- **PG (X1)**: One of the two split defenders — must be at ball-level and ready to switch on the back man's call; cannot be screened off by a cutting guard.
- **SG (X2)**: The back man in the split — calls "pick!" and then "switch!" as the cutters approach; has the clearest view of the developing action.
- **C (X5)**: Post player receiving the ball — defenders guarding him must react to his pivot and pass decisions while his teammates split.

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/post-splits-defense-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.59",
      "players": [
        {
          "role": "1",
          "x": 2.0,
          "y": 38.0,
          "jersey": "1",
          "side": "offense",
          "label": "top_of_key_baseline_side"
        },
        {
          "role": "2",
          "x": -14.0,
          "y": 28.0,
          "jersey": "2",
          "side": "offense",
          "label": "left_wing"
        },
        {
          "role": "3",
          "x": -22.0,
          "y": 22.0,
          "jersey": "3",
          "side": "offense",
          "label": "left_corner_wing"
        },
        {
          "role": "5",
          "x": -6.0,
          "y": 26.0,
          "jersey": "5",
          "side": "offense",
          "label": "high_post_left_elbow"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "5",
          "type": "pass",
          "d": "M 2.00 38.00 C -1.00 34.00, -4.00 29.00, -6.00 26.00",
          "style": "dashed"
        },
        {
          "from": "2",
          "to": "x1",
          "type": "screen",
          "d": "M -14.00 28.00 L 0.00 33.00",
          "style": "solid"
        },
        {
          "from": "1",
          "to": "5",
          "type": "cut",
          "d": "M 2.00 38.00 C -1.00 35.00, -3.00 31.00, -6.00 26.00",
          "style": "solid"
        },
        {
          "from": "x1",
          "to": "x2",
          "type": "cut",
          "d": "M 2.00 33.00 C -2.00 31.00, -6.00 29.00, -10.00 28.00",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 2.0,
          "y": 33.0,
          "jersey": "X1",
          "side": "defense",
          "label": "guarding_1_near_foul_line"
        },
        {
          "role": "x2",
          "x": -10.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "guarding_2_left_wing"
        },
        {
          "role": "x3",
          "x": -18.0,
          "y": 24.0,
          "jersey": "X3",
          "side": "defense",
          "label": "guarding_3_left_wing"
        },
        {
          "role": "x5",
          "x": -4.0,
          "y": 24.0,
          "jersey": "X5",
          "side": "defense",
          "label": "guarding_5_high_post"
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
          "text": "Post splits: on the pass to 5 from 1, 2 sets a back pick on X1 as 1 cuts over the top of the screen. X1 and X2 come together to stop the split and aggressively switch this maneuver.",
          "x": 0,
          "y": 50
        }
      ],
      "extras": [
        {
          "kind": "screen_marker",
          "label": "2 sets back pick on X1",
          "x": -7.0,
          "y": 31.0
        }
      ]
    }
  ],
  "notes": "[S1, p.149] Fig 9.59 \u2014 Post splits defense. Player 1 passes to 5 at the high post (left elbow area); player 2 sets a back pick on X1 as 1 cuts over the top of the screen. X1 and X2 converge to stop the split and aggressively switch. Player 4 and a second diagram reference are visible in the text caption but player 4 does not appear clearly in the Fig 9.59 diagram itself; omitted. The cut arrow for player 1 over the screen and the X1/X2 coming-together arrow are approximated from the scan \u2014 scan resolution is moderate. Figure 9.57 (flash-post/blind pig) and Figure 9.58 (pinch-post/elbow dribble screen) also appear on this page but are separate markers not requested here."
}
```

## Common Mistakes
1. **Defenders don't talk** → Cutters get through the gap and receive an easy layup pass from the post. Correction: call "pick!" and "switch!" before contact.
2. **Switching from behind the screen** → Defender switches too late; cutter has a step on his new defender. Correction: get level with the ball first, then switch.
3. **Switching tentatively** → Brief moment of confusion allows the ball to be thrown to the splitting cutter. Correction: commit to the switch fully and seal with inside legs crossed.
4. **Back man doesn't call it** → The front defender is surprised by the screen and the switch is disorganized. Correction: the back man always owns the call.

## Related Concepts
- [[defending-pinch-post]] — post splits often occur off the same entry passes
- [[trapping-and-double-teaming]] — if the post dominates, trapping is the next line of response
- [[defending-flash-post]] — similar two-man reads off post entry

## Sources
- [S1, p.149] — Herb Brown's full explanation of defending post splits, communication requirements, and back-man switch responsibility
