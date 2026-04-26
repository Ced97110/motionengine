---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [defense, dribble-handoff, man-to-man, trapping, switching]
source_count: 1
last_updated: 2026-04-11
---

# Defending Dribble Handoffs and Get Actions

## Summary
Dribble handoffs and "get" actions (pass and follow for return handoff) are among the most disruptive ball-movement patterns in modern offense. Herb Brown identifies three core responses: go through your teammate's screen, aggressively trap and switch, or overplay to force backdoor. The key in all cases is **not getting screened** and **sending the receiver back to his defender**. [S1, p.143]

## When to Use
- Whenever the offense runs a dribble handoff (DHO) — one player dribbles at a stationary teammate and hands off
- Whenever a player passes and follows the ball for a return handoff (get action)
- Short-clock situations where the offense uses DHOs to create quick mismatches

## Key Principles
1. **Go through or inside** — the defender whose man hands off the ball steps back or goes inside their teammate's screen to let the cutter's defender navigate through
2. **Aggressively trap and switch** — the handoff is an opportunity to trap: two defenders converge on the receiver the moment he catches
3. **Send the dribbler back uphill** — on a switch, immediately force the new ball-handler away from the basket
4. **Overplay the receiver** — to force the screen receiver backdoor instead of catching the handoff
5. **Do not get screened** — the cardinal rule for all DHO defense; losing your man on the screen creates an immediate layup or open shot

## Variations

### Dribble Handoff Defense
- **Option A**: X1 (defender of the player who dribbles toward and hands off) steps back to permit X3 to go inside and under the screen to cover the receiver
- **Option B**: Aggressively trap and switch — both defenders converge on the ball at the moment of the handoff
- **Option C**: Overplay the receiver to force him backdoor
[S1, p.143; Figure 9.42]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-dribble-handoff-0.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble"
  },
  "phases": [
    {
      "label": "Figure 9.42",
      "players": [
        {
          "role": "1",
          "x": -10.0,
          "y": 26.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball_handler_top_key"
        },
        {
          "role": "2",
          "x": 16.0,
          "y": 26.0,
          "jersey": "2",
          "side": "offense",
          "label": "right_wing"
        },
        {
          "role": "3",
          "x": 18.0,
          "y": 38.0,
          "jersey": "3",
          "side": "offense",
          "label": "right_corner_area"
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
          "x": -6.0,
          "y": 20.0,
          "jersey": "5",
          "side": "offense",
          "label": "high_post_left"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "3",
          "type": "dribble",
          "d": "M -10.00 26.00 C -4.00 26.00, 8.00 30.00, 18.00 38.00",
          "style": "zigzag"
        },
        {
          "from": "x3",
          "to": "3",
          "type": "cut",
          "d": "M 20.00 36.00 C 16.00 34.00, 14.00 36.00, 18.00 38.00",
          "style": "solid"
        },
        {
          "from": "x1",
          "to": "x1",
          "type": "cut",
          "d": "M -8.00 28.00 L -8.00 32.00",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": -8.0,
          "y": 28.0,
          "jersey": "X1",
          "side": "defense",
          "label": "on_ball_defender"
        },
        {
          "role": "x2",
          "x": 14.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "right_wing_defender"
        },
        {
          "role": "x3",
          "x": 20.0,
          "y": 36.0,
          "jersey": "X3",
          "side": "defense",
          "label": "right_corner_defender"
        },
        {
          "role": "x4",
          "x": -16.0,
          "y": 24.0,
          "jersey": "X4",
          "side": "defense",
          "label": "left_wing_defender"
        },
        {
          "role": "x5",
          "x": -4.0,
          "y": 22.0,
          "jersey": "X5",
          "side": "defense",
          "label": "high_post_defender"
        }
      ],
      "ball": {
        "x": -10.0,
        "y": 26.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X1 steps back to allow X3 to go inside/under the screen",
          "x": -8,
          "y": 33
        }
      ],
      "extras": [
        {
          "kind": "screen_marker",
          "label": "dribble handoff screen by 1 for 3",
          "x": 10,
          "y": 32
        }
      ]
    }
  ],
  "notes": "[S1, p.143] Figure 9.42 \u2014 Dribble handoff defense. Player 1 dribbles toward 3 (shown with zigzag/dribble arrow curving from top of the key toward the right corner area). X3 navigates inside/under the handoff screen to stay with 3; X1 steps back to allow X3 through. Option B is aggressive trap/switch at the moment of the handoff. Option C is overplaying 3 to force backdoor. The exact positions of 4 and 5 are approximate based on context; the diagram on the page is Figure 9.42 (implied \u2014 not printed on this page scan, but referenced in the caption). Scan shows limited detail for this specific figure; coordinates estimated from typical DHO formation context."
}
```

### Get Action (Pass and Follow for Return Handoff)
- **Preferred**: Jump switch and trap — two defenders converge on the ball at the return handoff
- **Alternative**: Step back to allow the defender whose opponent receives the pass to go through
- Goal: Do not let the returning passer get screened
[S1, pp.143-144; Figure 9.43]

```json name=diagram-positions
{
  "schema_version": "2",
  "figure_image": "backend/knowledge-base/figures/defending-dribble-handoff-1.png",
  "court_region": "half",
  "legend": {
    "solid": "cut",
    "dashed": "pass",
    "zigzag": "dribble",
    "wavy": "screen"
  },
  "phases": [
    {
      "label": "Figure 9.43",
      "players": [
        {
          "role": "1",
          "x": 3.0,
          "y": 33.0,
          "jersey": "1",
          "side": "offense",
          "label": "ball-handler near elbow area"
        },
        {
          "role": "2",
          "x": -18.0,
          "y": 28.0,
          "jersey": "2",
          "side": "offense",
          "label": "left wing"
        },
        {
          "role": "3",
          "x": 14.0,
          "y": 28.0,
          "jersey": "3",
          "side": "offense",
          "label": "right wing / handback receiver"
        },
        {
          "role": "4",
          "x": 4.0,
          "y": 22.0,
          "jersey": "4",
          "side": "offense",
          "label": "high post area"
        },
        {
          "role": "5",
          "x": 12.0,
          "y": 18.0,
          "jersey": "5",
          "side": "offense",
          "label": "right elbow/high area"
        }
      ],
      "actions": [
        {
          "from": "1",
          "to": "3",
          "type": "dribble",
          "d": "M 3 33 C 6 31, 9 29, 12 28",
          "style": "zigzag"
        },
        {
          "from": "x1",
          "to": "3",
          "type": "cut",
          "d": "M 5 36 C 7 33, 10 30, 12 28",
          "style": "dashed"
        },
        {
          "from": "x2",
          "to": "3",
          "type": "cut",
          "d": "M -10 28 C -2 28, 4 28, 10 28",
          "style": "solid"
        }
      ],
      "defenders": [
        {
          "role": "x1",
          "x": 5.0,
          "y": 36.0,
          "jersey": "X1",
          "side": "defense",
          "label": "defender on 1, near ball"
        },
        {
          "role": "x2",
          "x": -10.0,
          "y": 28.0,
          "jersey": "X2",
          "side": "defense",
          "label": "defender on 2, ready to pick up 3"
        },
        {
          "role": "x3",
          "x": 11.0,
          "y": 28.0,
          "jersey": "X3",
          "side": "defense",
          "label": "defender on 3, trapping handback"
        },
        {
          "role": "x4",
          "x": 3.0,
          "y": 19.0,
          "jersey": "X4",
          "side": "defense",
          "label": "defender on 4"
        },
        {
          "role": "x5",
          "x": 13.0,
          "y": 16.0,
          "jersey": "X5",
          "side": "defense",
          "label": "defender on 5"
        }
      ],
      "ball": {
        "x": 7.0,
        "y": 31.0,
        "possessed_by": "1"
      },
      "annotations": [
        {
          "kind": "label",
          "text": "X1 and X3 trap the handback; X2 ready to pick up 3 on the cut",
          "x": 0,
          "y": 50
        }
      ],
      "extras": [
        {
          "kind": "screen_marker",
          "label": "handback trap point near 3's position",
          "x": 12,
          "y": 28
        }
      ]
    }
  ],
  "notes": "[S1, p.144] Figure 9.43 \u2014 Get action (pass and return/handback): X1 and X3 converge to trap the handback near the right wing. X2 shifts to pick up 3 on any cut. Player 1 has initiated the dribble handoff toward 3; X1 follows tightly to form the trap with X3. The dashed arrow from X2 toward 3 indicates anticipatory coverage. Scan quality is adequate; arrow styles (zigzag for dribble, solid/dashed for defensive coverage) inferred from book's chapter-level legend and caption context."
}
```

### Get Hand-Back and Flare Action
Switch (same as Pistol action) OR body up and fight over the jam/flare screen. May trap the hand-back if the action is recognized in advance. [S1, p.145; Figure 9.47]

## Player Responsibilities
- **Defender of the dribbler/passer (X1)**: Step back to create a lane for teammate to go through, OR commit to trap, OR call the switch
- **Defender of the receiver (X3)**: Navigate through/inside the handoff screen; or converge into trap; or be ready for backdoor if overplaying
- **Weak-side defenders**: Rotate to cover any backdoor cut or slipping screener diving to the basket

## Common Mistakes
1. **Getting caught in the screen on a DHO** → the handoff screen is a trap for defenders who lose their positioning; must go through/inside
2. **Trapping too late** → the trap must occur at the moment of the handoff — late trapping lets the receiver get a step before help arrives
3. **Not being aware of the slip** → when trapping, the passer can slip away for a backdoor or dive to the basket; weak-side help must account for this

## Related Concepts
- [[defending-specific-plays]] — DHO defense in the full context of Herb Brown's system
- [[pick-and-roll-defense-summary]] — similar principles of switching vs. fighting through screens
- [[defending-staggered-screens]] — multiple-screen defensive principles

## Sources
- [S1, p.143] — Dribble Handoff defense (Figure 9.42)
- [S1, pp.143-144] — Get Action defense (Figure 9.43)
- [S1, p.145] — Get Hand-Back and Flare defense (Figure 9.47)
