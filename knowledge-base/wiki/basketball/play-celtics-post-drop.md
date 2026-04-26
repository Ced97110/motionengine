---
type: play
category: offense
formation: 1-4-high
tags: [post-up, backdoor, down-screen, back-screen, lob, cutting]
team: Boston Celtics
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "Every option in the play terminates at a high-value shot — left-block post finish, elbow jumper off a down-screen, or a basket-cut lob — systematically avoiding mid-range pull-ups."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The primary action is a left-block post-up where 3 seals and receives a direct feed, placing a skilled finisher in contact-heavy position that routinely draws fouls on the catch or through-move."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The play routes through a fixed sequence of at most two passes per option (entry to elbow, elbow to block/wing, wing to cutter), limiting live-ball exposure compared to free-flowing motion offense."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Continuous off-ball movement through the backdoor cut, down-screen, and back-screen chain ensures that if the primary post feed is denied the defense must still contest two additional high-efficiency scoring reads, keeping points-per-possession elevated across all branches."
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When X3 shades toward the baseline early to take away the backdoor pass, 3 uses that overplay to seal the defender on the hip and post up directly on the left block for a feed from 4."
    extraction: llm-inferred
  - text: "When 2 cannot deliver the lob to 4 cutting off the back screen, 3 immediately pops out to the top of the key where X3's help rotation has left him unguarded for an open jump shot."
    extraction: llm-inferred
---

# Boston Celtics Post-Drop Action (1-4 High)

## Overview
From the same 1-4 high alignment as the X Action, Rick Pitino's Celtics would cut Paul Pierce (3) from the left wing to a left-block post-up. The primary action is a post feed; the secondary options are a down-screen jump shot or a back-screen lob for the power forward. The play rewards continuous movement — there is no standing with the ball. [S14, pp.49-50]

## Formation
- **1 (PG)** at top of the key
- **2 (SG)** on the right wing/elbow area
- **3 (SF, Pierce)** on the left wing
- **4 (PF, Walker)** at the left elbow
- **5 (C)** at the right elbow

## Phases

### Phase 1: Entry and Post Feed
- 1 hits 4 at the left elbow and cuts to the left wing
- 3 makes a hard basket cut (backdoor) toward the left block — if this pass is available, take it
- If denied, 3 seals his defender and cuts back to post up on the left block
- 4 makes the post feed to 3 on the left block

<!-- DIAGRAM: Fig. 5.4 — 1 passes to 4 at left elbow, cuts to left wing; 3 cuts hard baseline to left block; 4 feeds 3. -->

### Phase 2: Down-Screen Option (if post feed is denied)
- If 4→3 pass is denied, 4 reverses the ball to 2, who cuts to the top off a screen from 5
- 4 then sets a down screen for 3
- 3 cuts toward the elbow to receive from 2 for a jump shot

<!-- DIAGRAM: Fig. 5.5 — 4 reverses to 2 off 5's screen; 4 sets down screen for 3; 3 pops elbow for jump shot. -->

### Phase 3: Back-Screen Option (if post feed is denied)
- 4 reverses the ball to 2 (who has cut off 5's screen)
- 3 sets a back screen for 4
- 2 looks for a lob pass to 4 cutting to the basket
- If X3 helps on the lob, 3 pops to the top and is open for a jump shot

<!-- DIAGRAM: Fig. 5.6 — Pierce sets back screen for Walker; 2 looks lob to 4; 3 pops top if X3 helps. -->

## Key Coaching Points
- 3 must make the backdoor cut aggressive to keep the defense honest before sealing and posting
- The down-screen and back-screen options are equally dangerous — the wing player (2) must read which one to use based on how the defense responds to the post feed denial
- "There is no passing and standing in the Celtics' offense" — movement must be continuous [S14, p.49]
- 3 pops to the top immediately if X3 cheats to stop the lob — the back-screen option punishes help defense

## Counters
- If X3 cheats on the backdoor: 3 seals and cuts back to the block for a direct post feed from 4
- If the lob is denied: 3 pops to the top for an open jump shot

## Related Plays
- [[play-celtics-x-action]] — the primary X Action from the same 1-4 high formation
- [[play-back-screen-post]] — similar back-screen-to-post concept
- [[concept-back-screen-reads]] — all defensive reads off the back screen

## Sources
- [S14, pp.49-50] — complete description of Boston Celtics Post-Drop Action
