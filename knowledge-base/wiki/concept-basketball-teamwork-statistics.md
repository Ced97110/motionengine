---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, offense, defense, teamwork, statistics, passing, screening, rebounding, spacing]
source_count: 1
last_updated: 2026-04-11
---

# Basketball Teamwork — Statistical Framework

## Summary
Teamwork is the element of basketball most difficult to capture quantitatively, yet it permeates every possession. *Basketball on Paper* (Ch.5) provides a systematic taxonomy of offensive and defensive teammate interactions, identifies which are measurable by existing statistics and which are not, and argues that any serious basketball analytics framework must attempt to account for teamwork effects — even if imperfectly. [S16, pp.77-81]

The central claim: **teamwork primarily operates by changing the probability that a team scores (or prevents scoring) on any given possession**. This means teamwork effects should ultimately flow through offensive and defensive efficiency ratings, and player evaluation must account for how teammates inflate or deflate individual statistics.

## Offensive Teammate Interactions [S16, p.78]

1. **Passing to a better-positioned teammate** — Player passes when a teammate has a higher scoring probability due to a mismatch or because a defender left to double-team the passer. *Partially captured by assists — but only the final pass before a score counts.*

2. **Setting screens (picks)** — Screens provide space for the ball handler, can create mismatches by forcing defensive switches, and create confusion of responsibility. Advantages: easier shot, time to survey defense, mismatch creation.
   - *Not recorded in official statistics at all (except privately by some teams)*
   - A screener who sets up a ball handler's open shot gets no assist and no statistical credit

3. **Pursuing offensive rebounds** — Preserves scoring opportunity on missed shots.
   - *Recorded as offensive rebounds, but only partially captures the full benefit (e.g., being fouled going for a loose ball is not recorded)*

4. **Running offensive patterns** — A perimeter player cutting through the lane forces his defender to follow, opening the perimeter for the ball handler. This is "creating space" / "good spacing."
   - *Movement away from the ball is recorded by no one* — yet can be the most important action on a possession

5. **Verbal communication** — Notifying a teammate of an incoming double-team, directing cuts, signaling when to clear out of a post position.
   - *Completely unrecorded*

## Defensive Teammate Interactions [S16, pp.78-79]

1. **Double-teaming** — Collapsing on a high-probability scorer and rotating to cover vacated assignments
   - *Steals capture some results; the rotation help that prevents the score is unrecorded*

2. **Zone coverage** — Recognizing and covering assigned zones while trusting teammates to cover theirs
   - *Zone effectiveness is captured only by team defensive efficiency, not individual stats*

3. **Communicating screens** — Calling out pick-and-roll directions ("screen left/right!") to allow defenders to navigate properly
   - *Completely unrecorded*

4. **Blocking out for teammates** — Defensive boxing-out so a teammate can secure the rebound, or knocking the ball free for teammate control
   - *Defensive rebounds recorded; the box-out that enabled the rebound is not*

## The Measurement Problem

### What Statistics Miss
- **The pass before the assist** — Passing around the perimeter to get the defense rotating may involve 3-4 passes before the assist; only the final pass is credited
- **The cut that created the cut** — A player cutting to the basket after his defender double-teamed the ball deserves credit beyond just the score
- **Screen value** — Screens that free a ball handler for a shot generate zero statistical credit for the screener
- **Threat value** — Derek Fisher's three-point threat preventing double-teams on Shaquille O'Neal: Fisher's benefit to Shaq is real but statistically invisible
- **Spacing/positioning** — Drawing a defender away from a teammate's low-post advantage creates scoring probability with no statistical trace

### Key Insight on Defense
> "Help defense is really just equivalent to 'defense.' No basketball defense operates in a pure man-on-man fashion — there is always help. Fundamentally, a defense keeps the ball, not men, from the basket." [S16, p.80]

This means blocks, steals, and defensive rebounds capture only small fragments of what defense accomplishes. The cooperative nature of defense makes individual defensive statistics inherently incomplete.

## Why Baseball Methods Don't Transfer [S16, pp.80-81]
Bill James's baseball analytics work (linear weights, runs created) cannot be directly applied to basketball because:
- **Baseball has almost no active teamwork** — hitters operate largely independently; the hit-and-run is a rare exception
- **Baseball has a base-progression accounting system** that enables clean measurement of individual contributions toward runs
- **Basketball is continuous interaction** — every player's action affects every other player's probability of scoring on the same possession
- Applying baseball linear-weight methods to basketball produces absurd results (e.g., Michael Olowokandi as a rookie rated higher than Moses Malone or Gary Payton ever were)

## Value Approximation Methods — Critique [S16, pp.81-82]
All published player-value formulas of the form:
> VALUE = PTS + REB + AST + STL + BLK − TOV − Missed FG − Missed FT

...are "value approximation" methods with the following problems:
- **Weights are arbitrary** — different formulas assign 0.6–1.4 points of value to an assist with no principled basis
- **No strategic information** — they don't distinguish offensive from defensive contributions
- **Don't sum to team outcomes** — they don't aggregate to points scored or points allowed
- **Ignore teamwork context** — a stat accumulated with great teammates is treated identically to one accumulated with poor teammates
- **The NBA's IBM Award** is based on such a formula; it receives little attention because no one is sure what it means

The one partial exception: methods that estimate individual wins where teammates' values sum to the team total — that property at least anchors the formula to actual outcomes.

## Implications for Coaching
- **Statistics measure outcomes, not actions** — coaching decisions should not be based solely on box-score stats without understanding the teamwork context
- **Screens, spacing, and off-ball movement are often the most important actions** on a possession but generate no statistics — coaches who value only stats will undervalue these skills
- **The assist undervalues ball movement** — a team with 30 passes per possession creates far more value than the single assist reflects
- **Help defense is the real defense** — individual defensive stats are misleading indicators of individual defensive quality

## Common Mistakes
1. **Using value approximation formulas as definitive player rankings** → They represent opinions about value, not measures of team impact
2. **Ignoring the "pass before the assist"** → Ball movement quality determines offensive efficiency more than final-pass assists suggest
3. **Not crediting screeners** → A player who sets 8 screens per game enabling open shots for teammates may contribute more than the scorer who benefits

## Related Concepts
- [[concept-four-factors-basketball]] — Teamwork actions ultimately manifest through the Four Factors
- [[concept-player-value-approximation]] — The critique of existing player-value formulas
- [[concept-basketball-efficiency-ratings]] — The target metric that teamwork should be measured against
- [[concept-screening-basics]] — Screens are the most statistically invisible but frequent form of offensive teamwork
- [[concept-motion-offense-principles]] — Motion offense is explicitly designed around teamwork interactions

## Sources
- [S16, pp.77-81] — Complete teamwork taxonomy, measurement problem analysis, and value approximation critique
