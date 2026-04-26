---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [offense, off-ball-screens, back-screen, down-screen, flare-screen, pro]
source_count: 1
last_updated: 2026-04-11
---

# Off-the-Ball Screen Reads — the source coach

## Summary
the source coach's detailed read system for the three primary off-the-ball screen types: back screen, down screen, and flare screen. Each screen has multiple defensive reaction options and specific responses for both the screened player and the screener. Off-the-ball screens involve three players: the passer, the screener, and the player for whom the screen is set. [S7, pp.54-56]

## When to Use
- In half-court man-to-man offense against all defensive coverages
- When a specific defensive tendency needs to be attacked (e.g., defense always goes over → flare option)
- As the building blocks of more complex screen combinations

## Key Principles
1. **Screener always goes opposite the screened player** — if the cutter goes low, screener pops high; if the cutter goes to the basket, screener pops to the perimeter.
2. **Screener must watch three things simultaneously**: the screened player's reaction, his own defender, and the screened player's defender.
3. **Each screen type has 3-5 distinct defensive reads** — the offense is only as good as its ability to read and execute the correct option.
4. **The slip is always available** — when the screener's defender commits to stopping the cutter, the screener slips before fully setting the screen.

## Player Responsibilities
- **Screener (usually 5 or 4)**: Set the screen at the right angle, then immediately read all three parties and move to the open option.
- **Screened Player (usually 2 or 3)**: Set up the defender before using the screen; execute the read-based cut precisely.
- **Ball Handler/Passer (1)**: Make a crisp, accurate pass away from the defender; read all options on the floor.

## Variations

### Back Screen (Blind Screen)
The screener approaches from behind the defender who cannot see the screen. [S7, pp.54-55]

**Read 1 — Defender runs into the screen:**
Ball handler (1) makes a lob pass to the screened player (2). Screener (5) rolls to the ball.

**Read 2 — Defender slides HIGH on the screen:**
Screened player cuts LOW (underneath). Screener pops out.

**Read 3 — Defender slides LOW on the screen:**
Screened player cuts OVER THE TOP of the screen. Screener pops out.

**Read 4 — Defender anticipates the cut:**
Screened player bumps and pops OUT away from the screen. Screener rolls to the basket.

**Read 5 — Ball handler can't pass directly to the screened player:**
Screener pops out, receives the ball, and passes to the screened player who has posted up.

```json name=diagram-positions
{"players":[{"role":"1","x":-8,"y":44},{"role":"2","x":10,"y":30},{"role":"5","x":4,"y":22},{"role":"x1","x":-8,"y":41},{"role":"x2","x":8,"y":28},{"role":"x5","x":2,"y":20}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"5","to":"2","type":"screen"},{"from":"5","to":"rim","type":"cut"}],"notes":"This extracts Figure 4.5 (the first/initial back screen diagram) as specified by the marker covering Figures 4.5–4.9. In Fig 4.5: player 1 is at the bottom left near the baseline as ball handler; player 2 is at the right wing area cutting toward the basket off a back screen set by 5 near the top of the key/elbow area. Defenders x1, x2, x5 are shown near their respective offensive players. The action shows 1 making a lob pass to 2 cutting to the basket, while 5 (screener) rolls toward the rim after setting the back screen. Coordinates are approximated from the diagram's proportions."}
```

### Down Screen
Screen set near the baseline. The player receiving the screen waits, sets up the defender when the defender is near, then runs into the screen. [S7, p.56]

**Read 1 — Defender trails the screened player:**
Screened player curls around the screen. Screener pops out to the corner.

**Read 2 — Defender anticipates the cut:**
Screened player cuts BEHIND the screen (back cut). Screener comes high.

**Read 3 — Defender slides under the screen:**
Screened player bumps and pops out to the corner. Screener cuts into the lane.

```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":44},{"role":"2","x":8,"y":22},{"role":"5","x":5,"y":30},{"role":"x1","x":-9,"y":43},{"role":"x2","x":9,"y":21},{"role":"x5","x":6,"y":29}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"2","to":"rim","type":"cut"},{"from":"5","to":"right_corner","type":"cut"}],"notes":"The marker requests Figures 4.10–4.12 (all three down screen reads, p.56). Per the rules, the INITIAL diagram (Figure 4.10 — defender trails, screened player curls) is extracted here. In Fig 4.10: player 1 is bottom-left (ball handler near left baseline/corner area), player 2 is right wing area (screened player), and player 5 is at the elbow/high-post area (screener set near the lane). Defenders x1, x2, x5 are shown nearby. Action arrows show: 1 passes to the curling 2; 2 curls toward the rim; 5 pops out to the right corner."}
```

### Flare Screen
Ball is in the hands of a player past the free-throw line extended. The high post, with back to the sideline, sets a side screen for a teammate. [S7, p.56]

**Read 1 — Defender slides BEHIND the screen:**
Screened player FLARES away from the screen (cuts to the wing/corner for a catch-and-shoot). Screener cuts to the basket.

**Read 2 — Defender anticipates (goes over) the cut:**
Screened player cuts BEHIND the screen (away from the flare, going under). Screener comes high.

```json name=diagram-positions
{"players":[{"role":"1","x":-18,"y":42},{"role":"2","x":14,"y":30},{"role":"5","x":8,"y":24}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"2","to":"right_corner","type":"cut"},{"from":"5","to":"rim","type":"cut"}],"notes":"Figure 4.13 — Flare Screen, Read 1 (defender slides behind the screen). Player 1 (ball handler) is positioned near the left corner/baseline area. Player 5 (screener/high post) is near the right elbow/top-of-key area with back toward the sideline. Player 2 (screened player) starts near the right wing. The action shows 2 flaring out toward the right corner to receive a pass from 1, while 5 cuts to the basket. Defenders x1 (near 1) and x2 (near 2) are also depicted but not extracted as the wiki focuses on offense. Coordinates are approximated from the small diagram on p.56."}
```

## Common Mistakes
1. **Screener does not read the screened player's defender** → Misses the slip or the pop at the right moment.
2. **Screened player always flares/curls regardless of defensive position** → Defense learns the tendency and fronts the cut before it starts.
3. **Back screen cutter goes at full speed every time** → If the defense anticipates, the cutter has no ability to read and redirect; must be ready to bump-and-pop.
4. **Ball handler ignores the screener after the screen** → Screener roll/pop is often the best available option.

## Related Concepts
- [[concept-screening-basics]] — Screener, receiver, and passer rules plus screened-player reads
- [[concept-reading-defender-off-screen]] — S3 framework for reading the defender on screens
- [[concept-shooting-off-screens-s3]] — Cutter and screener rules from S3
- [[concept-flex-back-screen-footwork]] — S6 flex back screen footwork details
- [[defending-off-ball-screens]] — How defenders counter these actions

## Sources
- [S7, pp.54-56] — the source coach, pro Coaches Playbook, Chapter 4: Screens and Screen Plays
