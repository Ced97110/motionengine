---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, offense, player-evaluation, possession-based]
source_count: 1
last_updated: 2026-04-11
---

# Floor Percentage

## Summary
Floor percentage is the fraction of a player's individual total possessions that result in a scoring possession for the team. It is the foundational efficiency metric in Dean Oliver's individual offensive rating system — analogous to a team's offensive play percentage but applied at the individual level. A player with a 0.60 floor percentage converts 60% of the possessions they are involved in into scores [S16, p.343].

Floor percentage captures a player's ability to turn possessions into points regardless of volume. A player who uses few possessions but always converts them scores higher than a high-usage player who wastes possessions. Combined with usage rate (% of team possessions used), floor percentage tells you not just *how often* a player converts, but *how efficiently*.

## When to Use
- Comparing efficiency between high-usage stars and low-usage role players fairly
- Identifying which players are "possession wasters" vs. efficient contributors
- Evaluating whether a player's offensive role matches their efficiency
- Tracking individual improvement across seasons when usage changes

## Key Principles

1. **Formula**: Floor% = Individual Scoring Possessions ÷ Individual Total Possessions [S16, p.343]

2. **Scoring Possessions** reflect credit for: field goals made (adjusted for assists received), assists given, free throws made, and offensive rebounds that lead to scores

3. **Total Possessions** reflect credit for: scoring possessions + missed field goals rebounded by the defense + missed free throws rebounded by the defense + turnovers

4. **A "good" floor percentage in the NBA** is approximately 0.54–0.62 for regular rotation players. Great offensive players (Michael Jordan '91: 0.61; Horace Grant '92: 0.66; Kevin McHale '88: 0.62) regularly exceed 0.60 [S16, pp.352, 354]

5. **Specialists score higher**: Low-usage efficient players (e.g., Steve Kerr 1996: 0.58, Off. Rtg 141) can show extraordinary floor percentages because they take only their best shots [S16, p.352]

6. **High usage tends to suppress floor%**: Stars like Michael Jordan averaged 0.57–0.61 floor% while using 30–31% of team possessions — extraordinary because high usage usually reduces efficiency [S16, pp.350-355]

## Historical Benchmarks
From Appendix 2 data [S16, pp.350-358]:

| Player/Team | Season | Floor% | Off. Rtg |
|---|---|---|---|
| Michael Jordan (Bulls) | 1991 | 0.61 | 126 |
| Horace Grant (Bulls) | 1992 | 0.66 | 132 |
| Kevin McHale (Celtics) | 1988 | 0.62 | 126 |
| Magic Johnson (Lakers) | 1987 | 0.603 | 123.9 |
| A.C. Green (Lakers) | 1987 | 0.601 | 121.6 |
| James Donaldson (Mavs) | 1987 | 0.65 | 132 |
| Steve Kerr (Bulls) | 1996 | 0.58 | 141 |
| Adam Keefe (Jazz) | 1998 | 0.61 | 125 |

**Key insight**: High floor% with high Off. Rtg AND high % team possessions is the true marker of elite offensive contribution (Jordan, Pippen, Magic, McHale).

## Player Responsibilities
- **All positions**: Understand that missed shots, turnovers, and unproductive possessions directly lower your floor% — every possession matters
- **High-usage players (PG, SG, SF)**: Managing floor% while absorbing 20–31% of team possessions is the hallmark of a true offensive star
- **Low-usage players (PF, C, specialists)**: Floor% should be high because you're only being asked to execute high-percentage plays

## Variations

### Team Play Percentage (TMPlay%)
The team-level equivalent — the fraction of team possessions that result in a score. Used as a baseline and in weighting the value of offensive rebounds [S16, p.345]. NBA average is approximately 0.45.

## Common Mistakes
1. **Ignoring usage context** → A 0.60 floor% on 10% of team possessions is less impressive than 0.58 on 30% of possessions
2. **Not accounting for offensive rebounds** → Players who get offensive rebounds boost their scoring possessions without increasing possessions from turnovers/missed shots
3. **Comparing across very different team offenses** → TMPlay% affects absolute floor% values

## Related Concepts
- [[concept-individual-offensive-rating]] — Points produced per 100 possessions; uses floor% as a component
- [[concept-offensive-rebound-weight]] — How offensive rebounds contribute to floor%
- [[concept-historical-offensive-ratings]] — Empirical floor% data for history's great offenses
- [[concept-performance-rating-system]] — S13's simpler box-score alternative

## Sources
- [S16, pp.343-349] — Formula derivation
- [S16, pp.350-358] — Historical data tables (Appendix 2)
