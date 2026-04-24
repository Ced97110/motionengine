---
type: play
category: offense
formation: 1-4-high
tags: [iverson-cut, pick-and-roll, ram-screen, down-screen, wing-exchange, half-court]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: iverson-cut-off-elbow-screen
    role: "2"
    criticality: required
  - id: iverson-cut-off-elbow-screen
    role: "3"
    criticality: required
  - id: elbow-screen-set
    role: "4"
    criticality: required
  - id: ram-screen-set
    role: "4"
    criticality: required
  - id: on-ball-screen-set
    role: "5"
    criticality: required
  - id: pick-and-roll-ball-handler-read
    role: "2"
    criticality: required
  - id: roll-to-rim
    role: "5"
    criticality: optional
  - id: dribble-signal-read
    role: "1"
    criticality: required
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: iverson-cut-off-elbow-screen
    for_role: "2"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: iverson-cut-off-elbow-screen
    for_role: "3"
  - region: glute_max
    criticality: required
    supports_technique: on-ball-screen-set
    for_role: "5"
  - region: ankle_complex
    criticality: required
    supports_technique: iverson-cut-off-elbow-screen
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: ram-screen-set
    for_role: "4"
  - region: ankle_complex
    criticality: optional
    supports_technique: roll-to-rim
    for_role: "5"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The ram screen eliminates x5 (the primary helper), leaving 2 a clear lane to attack the rim or find 5 rolling for a high-percentage finish."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "With x5 screened away by 4's ram action, 2 drives into the paint against reduced help, increasing the likelihood of contact and foul-drawing at the rim."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The scripted Iverson-cut exchange into a structured PnR sequences the ball through predetermined reads, limiting improvised passes and reducing live-ball turnover exposure."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Layering the ram screen on top of the PnR systematically removes the help defender, giving 2 multiple high-value reads — rim attack, roll pass, or corner kick-out — that each produce above-average shot quality."
---

# Iverson Ram

## Overview
A 1-4 high set play that begins with an Iverson-style wing player exchange (both wings crossing simultaneously using elbow screens), then flows into a ram screen action (a post player sets a down screen for the PnR screener) before finishing with a pick-and-roll. The ram screen removes the help defender from the lane, giving the ball-handler unobstructed space to attack. [S4, pp.66-67]

## Formation
1-4 high: 1 at the top with the ball, 4 and 5 on the elbows, 2 on the right wing, 3 on the left wing. [S4, p.66]

```json name=diagram-positions
{
  "players": [
    {
      "role": "1",
      "x": 1.1,
      "y": 37.3
    },
    {
      "role": "2",
      "x": -23.2,
      "y": 19.6
    },
    {
      "role": "3",
      "x": 22.9,
      "y": 19.1
    },
    {
      "role": "4",
      "x": 10.2,
      "y": 18.6
    },
    {
      "role": "5",
      "x": -10.2,
      "y": 18.9
    }
  ],
  "ballStart": "1",
  "actions": [
    {
      "type": "screen",
      "from": "4",
      "to": [
        0.6,
        24.0
      ],
      "path": "M 9.9 21.2 C 7 23.2 3.5 22.4 0.6 24"
    },
    {
      "type": "cut",
      "from": "2",
      "to": [
        21.5,
        20.5
      ],
      "path": "M -20.8 19.7 C -8.5 29 8.1 25.7 21.5 20.5"
    },
    {
      "type": "screen",
      "from": "5",
      "to": [
        -3.1,
        5.7
      ],
      "path": "M -10.9 21.5 C -15 17.8 -11.8 3.5 -3.1 5.7"
    },
    {
      "type": "cut",
      "from": "3",
      "to": [
        -22.3,
        17.2
      ],
      "path": "M 21.1 17.6 C 10.7 6.7 -17.1 -8.9 -22.3 17.2"
    }
  ],
  "notes": "Phase 1. - Both wing players exchange sides simultaneously using the elbow post players as screeners.\n- 2 cuts over the top, receiving a screen from 4.\n- 3 cuts under, receiving a screen from 5 on the low block.\n- 1 opens up the angle with a dribble and passes to 2 coming off 4's screen. Occasionally this is an immediate drive opportunity for 2. [S4, p.66]\n- **Signal**: The side of the floor 1 dribbles toward goes **under** the screens; the other side goes **over**. [S4, p.67]"
}
```

## Phases

### Phase 1: Iverson Wing Exchange
- Both wing players exchange sides simultaneously using the elbow post players as screeners.
- 2 cuts over the top, receiving a screen from 4.
- 3 cuts under, receiving a screen from 5 on the low block.
- 1 opens up the angle with a dribble and passes to 2 coming off 4's screen. Occasionally this is an immediate drive opportunity for 2. [S4, p.66]
- **Signal**: The side of the floor 1 dribbles toward goes **under** the screens; the other side goes **over**. [S4, p.67]

### Phase 2: Ram Screen Setup
- 1 clears out to the opposite wing to create space.
- 3 rotates down to the corner.
- 4 sets a **down screen (ram screen)** on x5 — screening 5's defender.
- 5 sprints up to the ball-handler (2) and sets an on-ball screen (the pick-and-roll). [S4, p.66]

### Phase 3: Pick-and-Roll Read
- 2 dribbles off 5's on-ball screen and makes the best basketball play.
- Because 4 is screening x5 (the helper), 2 has significant space to create without help defense. [S4, p.67]
- Options: drive to the rim and finish, pull-up jumper, pass to 5 rolling, or kick out to a corner player.

## Key Coaching Points
- 5 must **sprint** to set the on-ball screen. With 4 occupying x5, the ball-handler has maximum space. [S4, p.67]
- 1's dribble direction is the **signal**: whichever side 1 dribbles to, that wing goes under the screens; the other side goes over. This must be clearly communicated and practiced. [S4, p.67]
- 2 should look to drive immediately off the catch from the wing exchange — this is sometimes an instant scoring opportunity before the defense recovers. [S4, p.66]

## Key Personnel
- **1 (PG)**: Orchestrator; dribble signals which wing goes over; clears after the pass.
- **2 (SG)**: Primary ball-handler in the PnR; must be able to attack off the screen and make the right read.
- **3 (SF)**: Iverson cutter; rotates to corner for spacing.
- **4 (PF)**: Sets elbow screen for 2's Iverson cut, then sets the ram (down) screen on x5.
- **5 (C)**: Sets elbow screen for 3's Iverson cut, then sprints to set the on-ball screen for 2.

## Counters
- If the defense switches the PnR, 5 slips to the rim or seals for a post-up.
- If 2 is denied on the wing exchange, 1 can reverse and run the action to the other side.
- If 4's ram screen is anticipated, 4 can slip to the rim.

## Related Plays
- [[play-piston-elevator]] — another 1-4 high play using Iverson cuts as a decoy
- [[play-high-post-double-screen]] — 1-4 high play combining a High-Post cut with PnR
- [[play-side-blaze]] — horns set using a dribble hand-off leading into a PnR
- [[concept-setting-screens]] — principles for the ram and on-ball screen actions

## Sources
- [S4, pp.66-67]

```json name=diagram-positions
{
  "players": [
    {
      "role": "1",
      "x": 1.1,
      "y": 37.3
    },
    {
      "role": "2",
      "x": 21.5,
      "y": 20.5
    },
    {
      "role": "3",
      "x": -22.3,
      "y": 17.2
    },
    {
      "role": "4",
      "x": 10.2,
      "y": 18.6
    },
    {
      "role": "5",
      "x": -10.2,
      "y": 18.9
    }
  ],
  "actions": [
    {
      "type": "dribble",
      "from": "1",
      "to": [
        10.5,
        35.2
      ],
      "path": "M 3.3 37.1 C 5.7 36.6 8.4 36.7 10.5 35.2"
    },
    {
      "type": "pass",
      "from": "1",
      "to": "2",
      "path": "M 11.2 34.7 C 14.5 29.5 19 25.8 21.9 20.6"
    },
    {
      "type": "cut",
      "from": "1",
      "to": [
        -21.4,
        20.3
      ],
      "path": "M 10.7 33.8 C -1.8 37.6 -15.3 29.4 -21.4 20.3"
    },
    {
      "type": "cut",
      "from": "3",
      "to": [
        -23.4,
        2.3
      ],
      "path": "M -23.1 17.4 C -23.4 12.5 -23 7.1 -23.4 2.3"
    }
  ],
  "notes": "Phase 2. - 1 clears out to the opposite wing to create space.\n- 3 rotates down to the corner.\n- 4 sets a **down screen (ram screen)** on x5 — screening 5's defender.\n- 5 sprints up to the ball-handler (2) and sets an on-ball screen (the pick-and-roll). [S4, p.66]"
}
```

```json name=diagram-positions
{
  "players": [
    {
      "role": "1",
      "x": -21.4,
      "y": 20.3
    },
    {
      "role": "2",
      "x": 21.5,
      "y": 20.5
    },
    {
      "role": "3",
      "x": -23.4,
      "y": 2.3
    },
    {
      "role": "4",
      "x": 10.2,
      "y": 18.6
    },
    {
      "role": "5",
      "x": -10.2,
      "y": 18.9
    }
  ],
  "actions": [
    {
      "type": "screen",
      "from": "4",
      "to": [
        -5.4,
        5.3
      ],
      "path": "M 9.8 16.6 C 5 12.7 1.8 4.9 -5.4 5.3"
    },
    {
      "type": "screen",
      "from": "5",
      "to": [
        16.9,
        17.1
      ],
      "path": "M -7.3 5.4 C -3.3 13.9 8.4 15 16.9 17.1"
    },
    {
      "type": "dribble",
      "from": "2",
      "to": [
        -0.4,
        14.3
      ],
      "path": "M 20.8 22.3 C 13.7 24 -1.9 25.7 -0.4 14.3"
    },
    {
      "type": "cut",
      "from": "5",
      "to": [
        11.2,
        6.4
      ],
      "path": "M 12.5 20 C 16.6 17.5 16.2 8.6 11.2 6.4"
    },
    {
      "type": "pass",
      "from": "2",
      "to": "5",
      "path": "M -1.3 12.3 C 2.1 10.9 5.7 10.2 9.1 9"
    }
  ],
  "notes": "Phase 3. - 2 dribbles off 5's on-ball screen and makes the best basketball play.\n- Because 4 is screening x5 (the helper), 2 has significant space to create without help defense. [S4, p.67]\n- Options: drive to the rim and finish, pull-up jumper, pass to 5 rolling, or kick out to a corner player.\n\n## Key Coaching Points\n- 5 must **sprint** to set the on-ball screen. With 4 occupying x5, the ball-handler has maximum space. [S4, p.67]\n- 1's dribble direction is the **signal**: whichever side 1 dribbles to, that wing goes under the screens; the other side goes over. This must be clearly communicated and practiced. [S4, p.67]\n- 2 should look to drive immediately off the catch from the wing exchange — this is sometimes an instant scoring opportunity before the defense recovers. [S4, p.66]\n\n## Key Personnel\n- **1 (PG)**: Orchestrator; dribble signals which wing goes over; clears after the pass.\n- **2 (SG)**: Primary ball-handler in the PnR; must be able to attack off the screen and make the right read.\n- **3 (SF)**: Iverson cutter; rotates to corner for spacing.\n- **4 (PF)**: Sets elbow screen for 2's Iverson cut, then sets the ram (down) screen on x5.\n- **5 (C)**: Sets elbow screen for 3's Iverson cut, then sprints to set the on-ball screen for 2.\n\n## Counters\n- If the defense switches the PnR, 5 slips to the rim or seals for a post-up.\n- If 2 is denied on the wing exchange, 1 can reverse and run the action to the other side.\n- If 4's ram screen is anticipated, 4 can slip to the rim.\n\n## Related Plays\n- [[play-piston-elevator]] — another 1-4 high play using Iverson cuts as a decoy\n- [[play-high-post-double-screen]] — 1-4 high play combining a High-Post cut with PnR\n- [[play-side-blaze]] — horns set using a dribble hand-off leading into a PnR\n- [[concept-setting-screens]] — principles for the ram and on-ball screen actions\n\n## Sources\n- [S4, pp.66-67]"
}
```
