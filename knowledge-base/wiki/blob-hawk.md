---
type: play
category: out-of-bounds
formation: irregular
tags: [BLOB, zone, 2-3-zone, quick-hitter, corner-three, screen, post-up, inbounds]
source_count: 1
last_updated: 2026-04-11
---

# BLOB: Hawk (vs 2-3 Zone)

## Overview
Hawk is a 2-3 zone quick-hitter BLOB play that creates a two-option dilemma for the low zone defender: give up an open corner three-point shot, or surrender a mid-range jump shot at the low block. Two simultaneous screens are the engine — the play's effectiveness depends on both screens being set at exactly the same moment. Because it relies on surprise, it should be reserved for special situations. [S4, pp.13-14]

## Formation
**Irregular (3-across free-throw line extended + corner).** Three players line up along the free-throw line extended (one on the ball-side wing, one at the midpoint, one on the weak-side wing area). One player is in the ball-side corner. **1** (in-bounder) is out of bounds on the baseline.

Specific positions:
- **1**: out of bounds, baseline (in-bounder)
- **2**: ball-side corner
- **4**: ball-side free-throw line extended / wing area
- **5**: middle (near the key)
- **3**: weak-side area

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":47},{"role":"2","x":22,"y":42},{"role":"3","x":-14,"y":22},{"role":"4","x":18,"y":22},{"role":"5","x":0,"y":26},{"role":"x1","x":8,"y":29},{"role":"x2","x":-8,"y":29},{"role":"x3","x":18,"y":36},{"role":"x4","x":-8,"y":36},{"role":"x5","x":4,"y":36}],"actions":[{"from":"5","to":"left_low_block","type":"cut"},{"from":"4","to":"right_low_block","type":"cut"},{"from":"2","to":"right_corner","type":"cut"},{"from":"1","to":"2","type":"pass"}],"notes":"This is the starting (setup) formation from the first diagram on p.13. 1 is the out-of-bounds inbounder at the baseline center. 2 starts in the ball-side (right) corner. 4 and 5 are along the free-throw line extended on the ball side, with 3 on the weak side. Defenders x4 and x5 are the top two zone defenders near the elbows/paint; x3 is the ball-side low zone defender; x1 and x2 are the upper zone guards. Action arrows show 5 cutting down the key to screen x5, 4 cutting/walking toward the low block to screen x3, 2 cutting to the ball-side corner, and 1 passing to 2 in the corner (primary option per the diagram)."}
```

## Phases

### Phase 1: Dual Simultaneous Screens
- **5** cuts down the key and sets a screen, sealing the middle zone defender (**x5**).
- **At the same time**, **4** walks their defender (**x3**) closer to the basket with a screen (using positioning/body to influence x3's positioning).
- **1** cuts to the ball-side slot to pin the ball-side guard defender (**x1**) in place.

### Phase 2: Corner Cut & Decision
- **2** cuts toward the ball-side corner.
- If **4** and **5** have successfully sealed their defenders, **2** should be open for the inbound pass and corner three-point shot.

### Phase 3: Counter (if corner is denied)
- If **x3** cheats over the screen to deny the corner, **4** is now open on the low block for a catch-and-shoot midrange jump shot.
- **1** (in-bounder) reads the defense and delivers the correct pass.

## Key Coaching Points
- **Timing is everything**: **4** and **5** must set their screens simultaneously; **2** must cut immediately once screens are set. [S4, p.14]
- **2** must disguise the cut — face the middle of the floor first, even pretend to set a screen, before cutting to the corner. [S4, p.14]
- This is a quick-hitter to be used **sparingly** (special occasions, when you need a three-point shot) — not on every baseline inbound. [S4, p.14]
- The in-bounder (**1**) must make the correct read and deliver the right pass to either **2** or **4**.

## Counters
- **If x3 cheats to deny 2**: 4 is open at the low block for a midrange jumper.
- **If both are covered**: 1 at the slot may be open as a safety valve.

## Related Plays
- [[blob-belmont-flash]] — similarly relies on element of surprise; also should be used sparingly
- [[blob-side-cross-elevator]] — BLOB 2-3 zone play using sequential elevator-style screens
- [[play-selection-principles]] — principle of reserving quick-hitters for special situations

## Sources
- [S4, pp.13-14]
