---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, player-evaluation, statistics, performance-rating]
source_count: 1
last_updated: 2026-04-11
---

# Player Rating Systems Comparison

## Summary
Ten major basketball player rating systems have been proposed to convert box-score statistics into a single number representing a player's value. Despite different philosophical approaches, most take the same basic form: add up the good statistics (points, assists, rebounds, steals, blocks) and subtract the bad ones (missed shots, turnovers, personal fouls), with varying weights attached to each stat.

Dean Oliver compared these systems by standardizing all their weights relative to points scored, revealing dramatically different assumptions about what statistics matter most. The most uncertain category is offensive rebounds, which different systems value anywhere from 0.63 to 3.82 times a point — a 3.19-range spread [S16, pp.83-85].

## When to Use
- Evaluating player contributions for playing-time decisions
- Scouting and roster construction
- Post-season player reviews
- Comparing players across positions or teams

## Key Principles
1. **All systems share a common form**: good_stats − bad_stats, weighted by assumptions about the value of each play type
2. **Weights vary enormously**: the "correct" weight for offensive rebounds ranges from 0.63 to 3.82 relative to a point — no consensus exists [S16, p.85]
3. **Possession value is the key assumption**: many systems anchor weights to the estimated value of a ball possession (0.9 to 1.02 depending on the system)
4. **Simple additive formulas don't fit basketball**: Oliver argues the add-good/subtract-bad form "doesn't really mean anything" and that more sophisticated formulas incorporating how teammates interact are needed
5. **Context adjustments matter**: only Hollinger PER adjusts for team assist rate; only Berri's system derives weights from rigorous regression rather than assumption

## The Ten Systems (Stat Weights Relative to Points)

| Statistic | Min Weight | Max Weight | Range | Average |
|-----------|-----------|-----------|-------|--------|
| PTS | 1.00 | 1.00 | 0 | 1.00 |
| AST | 0.63 | 1.39 | 0.75 | 0.99 |
| OREB | 0.63 | 3.82 | 3.19 | 1.19 |
| DREB | 0.35 | 1.71 | 1.36 | 0.88 |
| STL | 0.63 | 2.44 | 1.80 | 1.27 |
| BLK | 0.63 | 1.94 | 1.31 | 1.02 |
| Missed FG | −1.38 | −0.63 | 0.75 | −0.93 |
| Missed FT | −1.00 | 0.00 | 1.00 | −0.63 |
| TOV | −2.77 | −0.63 | 2.13 | −1.28 |
| PF | −0.60 | 0.00 | 0.60 | −0.24 |

*Source: [S16, pp.83-85]*

## System Descriptions

### Manley Credits
Assigns equal weight of 1.00 to all positive and negative statistics. Simplest form. [S16, p.83]

### Heeren TENDEX
Similar form to Manley; includes a pace-modifier; does not substantially change weights. Written by Dave Heeren since the 1960s. [S16, p.83]

### Bellotti Points Created
Anchors all weights to the "value of a ball possession" (~0.92); also weights personal fouls. [S16, p.83]

### Claerbaut Quality Points
More convoluted; gives credit for shooting better than 50% FG and 75% FT; ends up underweighting non-scoring stats relative to other systems. [S16, pp.83-84]

### Mays Magic Metric
Weights derived from a set of equations describing assumptions; requires assumed shot-type proportions. [S16, p.84]

### Schaller TPR (Total Performance Ratings)
Uses possession value of 0.9; additionally accounts for team defense, game pace, positional norm, schedule strength, and projected improvement/decline. [S16, p.84]

### Hollinger PER (Player Efficiency Rating)
Possession value of 1.02; adjusts for pace and rescales to league average of 15. **Unique**: the only system that incorporates team context (frequency of assisted baskets). [S16, p.84]

### Steele Value
Alternative weighting scheme provided by Doug Steele for NBA statistics online. [S16, p.83]

### Berri Individual Wins
Weights rigorously derived from technical regression analysis of NBA data; teammates' wins sum to team wins. **Most extreme weights** — heavily emphasizes rebounds, steals, and turnovers. Adds positional adjustments to reduce bias against smaller players. Arrives at very different conclusions about OREB value than Oliver. [S16, pp.84-85]

## Common Mistakes
1. **Treating any single system as definitive** → The enormous range of weights (e.g., OREB from 0.63 to 3.82) reflects genuine uncertainty — no system has been proven correct
2. **Ignoring context** → Raw stat totals ignore pace, team quality, opponent quality, and playing time
3. **Combining offensive and defensive contributions** → Systems that add good and subtract bad stats implicitly assume all stats are commensurable, which Oliver challenges
4. **Using the formula form uncritically** → "The equation doesn't really mean anything, so how could it fit basketball?" [S16, p.85]

## Related Concepts
- [[concept-performance-rating-system]] — the PRS framework from Lee Rose; simpler coach-facing version
- [[concept-four-factors]] — Oliver's preferred framework for team evaluation
- [[concept-rebounding-myths-roles]] — why OREB weight is so uncertain
- [[concept-lineup-significance-testing]] — alternative approach to evaluating player impact

## Sources
- [S16, pp.83-85] — Table 5.1 (weights) and Table 5.2 (ranges/averages) with descriptions of all ten systems
