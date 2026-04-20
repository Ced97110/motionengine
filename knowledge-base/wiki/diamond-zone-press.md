---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, zone-press, full-court-press, pressure-defense, trapping, zone]
source_count: 1
last_updated: 2026-04-11
---

# Diamond Zone Press (1-2-1-1)

## Summary
The Diamond Zone Press is a 1-2-1-1 full-court zone defense that applies maximum pressure on the inbounds passer, channels the ball to the sideline, and then traps the dribbler with a two-man wall. Based on John Wooden's High-Post full-court zone press, the Diamond is most effective immediately after a made free throw. Herb Brown's teams used the Diamond whenever their center scored. [S1, pp.182-183]

## When to Use
- After a made free throw (by the center, in Brown's system)
- When you want to disrupt inbounds rhythm and force sideline dribbling
- When your tallest player is energetic and can bat balls out of bounds
- As a change-of-pace press after establishing a man-to-man game

## Formation
- **1 (top)**: Tallest defensive player pressures the inbounds passer — tries to bat the ball out of bounds
- **2 and 3 (wings)**: Positioned to deny the pass to the middle and the far side of the court; channel everything to the nearest sideline
- **4 (middle)**: Positioned to deny the high-post receiver and any middle breakout
- **5 (back)**: Protects the goal against any long pass or quick advance

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/diamond-zone-press-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Diamond Zone Press (1-2-1-1) \u2014 Full-Court Alignment",
      "players": [
        {
          "role": "1",
          "x": 0.0,
          "y": 47.0,
          "jersey": "1",
          "side": "defense",
          "label": "inbounds_pressure_tallest"
        },
        {
          "role": "2",
          "x": -14.0,
          "y": 35.0,
          "jersey": "2",
          "side": "defense",
          "label": "left_wing_deny"
        },
        {
          "role": "3",
          "x": 14.0,
          "y": 35.0,
          "jersey": "3",
          "side": "defense",
          "label": "right_wing_deny"
        },
        {
          "role": "4",
          "x": 0.0,
          "y": 20.0,
          "jersey": "4",
          "side": "defense",
          "label": "middle_deny_high_post"
        },
        {
          "role": "5",
          "x": 0.0,
          "y": 5.0,
          "jersey": "5",
          "side": "defense",
          "label": "back_protector"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "2",
          "type": "cut",
          "d": "M 0 47 C -5 45, -12 40, -14 35",
          "style": "solid"
        },
        {
          "from": "OB",
          "to": "2",
          "type": "pass",
          "d": "M 0 47 L -14 35",
          "style": "dashed"
        },
        {
          "from": "2",
          "to": "left_corner",
          "type": "dribble",
          "d": "M -14 35 L -22 28",
          "style": "zigzag"
        }
      ],
      "ball": {
        "x": 0.0,
        "y": 47.0,
        "possessed_by": "OB"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "1-2-1-1 Diamond Zone Press",
          "x": 0,
          "y": -2
        },
        {
          "kind": "label",
          "text": "Pressure inbounds passer; channel to sideline; trap on stop",
          "x": 0,
          "y": 50
        }
      ],
      "extras": [
        {
          "kind": "label",
          "text": "OB",
          "x": 0,
          "y": 47,
          "meaning": "Offensive inbounds passer at baseline out of bounds"
        }
      ]
    }
  ],
  "notes": "[S1, pp.182-183] Diamond Zone Press (1-2-1-1) full-court zone press alignment. No actual printed diagram was found on pp.182-183 of the scanned pages \u2014 the pages contain only prose description of the Diamond Zone Press. Positions are reconstructed from the text description: x1 (tallest defender, role \"1\") pressures the inbounds passer at the baseline; x2 and x3 (wings, roles \"2\" and \"3\") are positioned roughly at the quarter-court wings to deny middle and far-side passes and channel to the nearest sideline; x4 (role \"4\") is at mid-court to deny the high-post breakout receiver; x5 (role \"5\") is near the backcourt free-throw line extended as the safety. Ball is shown as inbounded from baseline. Action arrows are illustrative of the described phase 1 (inbounds pressure + sideline channel). If a separate printed diagram exists on a different page, coordinates should be updated from that visual. figure_image path echoed as supplied by resolver."
}
```

## Phases
### Phase 1: Inbounds Pressure
- The tallest defender pressures the inbounds passer, actively trying to get a piece of the ball and bat it out of bounds
- Batting the ball out of bounds eliminates the baseline-run option for the passer on the next attempt — dramatically increasing pressure
- Wing defenders deny the pass to the middle (the 4) and the far side of the court away from the ball
- Objective: channel the inbounds pass to the **nearest sideline**

### Phase 2: Sideline Trap
- Once the receiver catches on the sideline and begins dribbling, the wing defender on that side **gets to a spot on the sideline** and forces the dribbler to stop or change direction
- The inbounds passer (tallest defender) follows the pass and **traps the dribbler** once stopped along the sideline
- Two-man trap is now set; the other three defenders deny outlets and look to intercept passes

### Phase 3: Rotation After Pass
- If the trap is beaten by a pass, the trapping defenders sprint out of the trap
- Middle defender and back defender shift to cover the direction of the pass
- Coach must adjust individual movements based on each player's defensive strengths and weaknesses

## Key Coaching Points
- "Get a piece of the ball" — the inbounds pressure is active, not passive
- "Channel to the sideline" — never let the ball go middle; the sideline is your third defender
- "Trap when stopped" — do not trap a dribbler in motion; force the stop first, then close the trap
- Fake and feint the trap constantly — keep the offense guessing even when you can't get there
- "Sprint out of the trap" — when the ball is passed, trapping defenders rotate immediately

## Common Mistakes
1. **Letting the ball go to the middle** → Correct: wings must actively deny the middle pass and any far-side pass; channel to the sideline.
2. **Trapping before the dribbler is stopped** → Correct: wing forces the stop or change of direction first; the trailer closes the trap once the ball is dead.
3. **Back defender cheating up** → Correct: the 5 must remain goal-side and protect against the long pass; resist the temptation to help trap.
4. **No communication** → Correct: middle and back defenders must call rotations aloud as passes are made.

## Related Concepts
- [[full-court-press-defense]] — the broader press philosophy that the Diamond fits within
- [[run-and-jump-defense]] — the man-to-man alternative used with different personnel
- [[zone-press-combinations]] — how the Diamond is combined with half-court zone defenses
- [[team-defense-calls-and-signals]] — called as "54" in Brown's numbering system

## Sources
- [S1, pp.182-183] — Herb Brown, *Let's Talk Defense*, Chapter 12: Zone, Press, and Combination Defenses
