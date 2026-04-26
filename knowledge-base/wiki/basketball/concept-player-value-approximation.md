---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, player-evaluation, statistics, offense, defense]
source_count: 1
last_updated: 2026-04-11
---

# Player Value Approximation Methods

## Summary
A large family of basketball player-evaluation formulas attempts to aggregate individual statistics into a single value number. These "value approximation" methods all share the same basic structure — add positive statistics, subtract negative ones, with various multiplying weights — but differ in the weights assigned to each statistic. *Basketball on Paper* surveys 10+ published methods and identifies their shared fundamental limitations. [S16, pp.81-82]

## The Standard Form
The most basic version:
> VALUE = PTS + REB + AST + STL + BLK − TOV − Missed FG − Missed FT

Variations include: subtracting personal fouls; multiplying assists by 0.7 and steals by 1.5; weighting offensive rebounds at 0.8 and defensive rebounds at 0.5; position-adjusting weights (assists worth more for PGs than PFs).

## Published Methods Surveyed [S16, pp.82+]
- **Manley's Credits** (Martin Manley, *Basketball Heaven*, 1988): All weights equal to 1 — the simplest form
- **Hoopstat Grade** (Trupin & Couzens, *Hoopstats*, late 1980s): Weights field goals and free throws made rather than points
- Several others with varying weights — total of 10 methods examined (one discarded for producing absurd results)

## Core Limitations
1. **Weights are arbitrary** — Justifications come from personal belief, matching MVP voting, or unknown criteria. The value of an assist ranges from 0.6 to 1.4 points depending on which formula you use — a 2.3× uncertainty range.
2. **No strategic information** — Formulas don't identify what a player should do differently to improve.
3. **No offensive/defensive distinction** — They don't separate offensive contributions from defensive ones.
4. **Don't aggregate to team outcomes** — Individual values don't sum to points scored or points allowed (with one exception: methods that estimate individual wins where teammates' values sum to team win total).
5. **Ignore teamwork context** — Stats accumulated with excellent teammates are treated identically to stats accumulated with poor teammates, even though context heavily influences the numbers.
6. **The Dennis Rodman problem** — Some methods rate Rodman as one of the greatest ever; others barely above average. This disagreement reveals that the methods are measuring different things, not converging on truth.

## Appropriate Use
Despite their limitations, value approximation methods have one valid use: **comparing multiple methods against each other to understand the range of uncertainty** in player evaluation. Areas of agreement across methods (Jordan is great; Cadillac Anderson is not) are more reliable. Areas of wide disagreement (Rodman's value) signal genuine analytical uncertainty. [S16, p.82]

## The NBA's IBM Award
The NBA has an official player-value award (formerly the Schick Award, then IBM Award) based on a formula of this type. It receives little attention because no one is certain what it measures. [S16, p.82]

## Common Mistakes
1. **Using a single formula as definitive** → All formulas represent opinions with arbitrary weights; no single formula has been validated against actual team success.
2. **Ignoring context** → A stat accumulated in a teamwork-heavy system (e.g., assists in a motion offense) does not have the same value as the same stat in an isolation-heavy system.
3. **Confusing precision with accuracy** → Formulas with 6 decimal places of precision on weights are no more accurate than simple equal-weight versions; precision without validation is meaningless.

## Related Concepts
- [[concept-basketball-teamwork-statistics]] — The teamwork problem is why simple stat-aggregation fails for basketball
- [[concept-four-factors-basketball]] — A more principled framework: measure team success through the four factors, then attribute proportional credit
- [[concept-performance-rating-system]] — The PRS from S13 is a weighted stat system that shares some of these limitations but adds explicit performance benchmarks
- [[concept-hustle-board]] — Hustle board statistics capture actions that value-approximation formulas miss entirely

## Sources
- [S16, pp.81-82] — Survey and critique of 10 player value approximation methods
