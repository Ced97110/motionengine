---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, defense, offense, team-evaluation, ratings]
source_count: 1
last_updated: 2026-04-11
---

# Uncorrelated Offensive and Defensive Ratings

## Summary
Standard team offensive rating (ORtg) and defensive rating (DRtg) are correlated with each other — teams that play fast or face weaker opponents show inflated or deflated values on both sides. "Uncorrelated" ratings remove this statistical covariance to give a purer measure of each side of the ball independent of the other [S16, p.143].

The motivation is to fairly assess the relative predictive value of offense vs. defense in playoff success — answering whether "Defense Wins Championships" is actually supported by data.

## When to Use
- Comparing offensive vs. defensive contributions to team winning
- Predicting playoff success from regular season ratings
- Controlling for pace-of-play effects when comparing teams
- Assessing whether regular-season defensive effort is being understated ("slacking off")

## Key Principles
1. **Standard ORtg and DRtg are correlated.** Teams that face easy opponents tend to have both good offensive and defensive ratings; this conflates the two sides [S16, p.143].
2. **Uncorrelated ratings use statistical variance and covariance to separate the components.** The formula adjusts each rating by half the difference between them, weighted by factor R [S16, p.143].
3. **The "slacking off" assumption matters.** If teams play less hard on defense in the regular season (saving effort for playoffs), uncorrelated defensive ratings better reflect true defensive ability [S16, p.143].
4. **The "Defense Wins Championships" finding is ambiguous.** Using standard ratings: best defense won 5 titles, best offense won 6. Using uncorrelated ratings: each won 7. No clear winner [S16, p.143].

## Formulas
```
UORtg = ORtg + (R−1)(ORtg − DRtg) / 2

UDRtg = DRtg − (R−1)(ORtg − DRtg) / 2

R = √[Var(ORtg) + Var(DRtg)] / √[Var(ORtg) + Var(DRtg) − 2·Cov(ORtg, DRtg)]
```
Where:
- UORtg = uncorrelated offensive rating
- UDRtg = uncorrelated defensive rating  
- Var() = game-to-game statistical variance (standard deviation squared)
- Cov() = statistical covariance between ORtg and DRtg [S16, p.143]

## Practical Results (Playoff Series Prediction)
- Better defense (uncorrelated) wins **61.8–62%** of playoff series
- Better offense (uncorrelated) wins **62.0%** of playoff series
- Essentially equal predictive power → neither offense nor defense is definitively more important [S16, p.143]

## Common Mistakes
1. **Using raw ORtg/DRtg for cross-team comparisons without pace adjustment** → inflated values for fast-paced teams
2. **Concluding "Defense Wins Championships" from raw ratings** → the data does not support this conclusion once ratings are uncorrelated
3. **Ignoring the slack-off assumption** → the result shifts slightly depending on whether both sides or only defense slacks in the regular season

## Related Concepts
- [[concept-individual-offensive-rating]] — individual-level analog
- [[concept-individual-floor-percentage]] — companion individual metric
- [[concept-difficulty-theory-credit-distribution]] — related analytical framework

## Sources
- [S16, p.143] — Chapter 12 endnote, "The Effect of Bad Referees"
