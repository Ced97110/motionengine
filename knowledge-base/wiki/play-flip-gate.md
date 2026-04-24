---
type: play
category: offense
formation: 1-4-high
tags: [back-screen, gate-screen, rim-cut, catch-and-shoot, hand-off, deception]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: back-screen-set
    role: "1"
    criticality: required
  - id: deceptive-fake-cut
    role: "1"
    criticality: required
  - id: hand-off-give
    role: "4"
    criticality: required
  - id: rim-cut-off-screen
    role: "5"
    criticality: required
  - id: gate-screen-set
    role: "4"
    criticality: required
  - id: catch-and-shoot
    role: "2"
    criticality: required
  - id: baseline-runner-cut
    role: "2"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: rim-cut-off-screen
    for_role: "5"
  - region: ankle_complex
    criticality: required
    supports_technique: baseline-runner-cut
    for_role: "2"
  - region: core_outer
    criticality: required
    supports_technique: back-screen-set
    for_role: "1"
  - region: glute_max
    criticality: optional
    supports_technique: rim-cut-off-screen
    for_role: "5"
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When x5 anticipates and fights over the top of the back screen, 5 can alter the route — popping out to the elbow or slipping early — to find a cleaner angle to receive the pass from 4."
    extraction: llm-inferred
  - text: "When x4 reads the gate action and jumps into the passing lane, 4 abandons the screen and cuts aggressively to the rim for an uncontested layup."
    extraction: paraphrase
    source_hint: "[S4, p.63]"
---

# Flip Gate

## Overview
A half-court play from a 1-4 high set featuring two distinct scoring options: first, a back screen by the point guard to free the center for a rim cut; second, a double gate screen by both post players to free the best shooter for a catch-and-shoot at midrange or the three-point line. The play uses misdirection (a fake cut by 1) to set up the back screen. [S4, pp.62-63]

## Formation
Classic 1-4 high: 1 at the top with the ball, 4 and 5 on the elbows (high post), 2 and 3 on the wings. [S4, p.62]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":5},{"role":"2","x":-18,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"actions":[{"from":"1","to":"4","type":"pass"},{"from":"2","to":"right_corner","type":"cut"}],"notes":"The first diagram (Phase 1 / starting formation) shows the classic 1-4 high set: 1 at the top of the key with the ball, 4 and 5 on the elbows (high post), 2 on the left wing and 3 on the right wing. The diagram depicts the entry pass arrow from 1 to 4 (4 stepping out to the slot), and 2 beginning a baseline cut toward the opposite short corner (right side). The second diagram on the page shows Phase 2 action and is not captured here per the initial-formation rule."}
```

## Phases

### Phase 1: Entry & Baseline Cut
- 4 steps out to the slot and receives the pass from 1.
- 2 immediately and quickly cuts along the baseline to the opposite short corner. [S4, p.62]

### Phase 2: Flip Back Screen & Rim Cut
- 1 acts like they are cutting through the key but **flips around** and sets a back screen on x5 (5's defender).
- 5 uses the screen and cuts to the rim looking for the pass from 4 for the layup.
- If 5 is not open, 1 cuts back to the top and receives a hand-off from 4. [S4, p.62]

### Phase 3: Gate Screen for Best Shooter
- 4 cuts down the middle of the key and sets a gate screen together with 5.
- As 4 is cutting down the key, 2 explodes from the short corner and cuts through the gate screen. 2 should clear past the screens just as 4 arrives to screen 2's defender.
- 1 takes a dribble and passes to 2 at midrange or the three-point line for the open catch-and-shoot. [S4, p.62]

## Key Coaching Points
- The gate screen is the most critical action — all players must time it so 2 cuts through cleanly while their defender is screened off. [S4, p.63]
- Players must not reveal their movement too early. Especially important for 1 when setting the initial quick flip back screen. [S4, p.63]
- 4 and 5 must **"close the gate"** after 2 has cut through — they step closer together to seal 2's defender. 2 must change direction quickly to give post players time to close. [S4, p.63]
- The first few times this play is run, 5 will typically be open on the rim cut. Prioritize that read. [S4, p.63]
- Best shooter (2) must start on the **same side** the basketball is initially passed to. [S4, p.62]
- If x4 anticipates the pass and jumps the lane, 4 should dive to the hoop for the layup (counter). [S4, p.63]

## Key Personnel
- **1 (PG)**: Initiator; fakes cut, sets back screen on x5, receives hand-off, passes to 2 in gate action.
- **2 (SG / Best Shooter)**: Baseline runner; cuts through the gate for the catch-and-shoot; must time cut to hit the gate at the right moment.
- **3 (SF)**: Occupies the weak-side wing for spacing.
- **4 (PF)**: Receives entry pass, looks for 5 on rim cut, gives hand-off to 1, then sets gate screen.
- **5 (C)**: Primary rim-cut threat off back screen; co-sets gate screen with 4.

## Counters
- If x5 cheats over the back screen, 5 can pop to the elbow or slip the screen for a different angle.
- If x4 jumps the passing lane during gate action, 4 dives hard to the rim for an easy layup.

## Related Plays
- [[play-drive-hammer]] — another multi-action play using back screens and corner spacing
- [[blob-box-gate]] — BLOB play that also uses a gate screen for the best shooter
- [[concept-setting-screens]] — gate screen timing and angle principles
- [[concept-reading-screens-off-ball]] — how 2 reads the gate screen to maximize separation

## Sources
- [S4, pp.62-63]
