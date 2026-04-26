---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [analytics, offense, defense, efficiency, statistics, team-evaluation, player-evaluation]
source_count: 1
last_updated: 2026-04-11
---

# Points Per Possession (Offensive and Defensive Rating)

## Summary
Points per possession — expressed in *Basketball on Paper* as **points per 100 possessions** — is the foundational unit of basketball performance analysis. An offense's rating (ORtg) is how many points it scores per 100 possessions; a defense's rating (DRtg) is how many points it allows per 100 possessions. The *differential* between a team's ORtg and DRtg is the single best predictor of wins.

The metric's key advantage is that it **removes pace** from the equation. A fast-paced team and a slow-paced team cannot be fairly compared by points per game; dividing by possessions creates a level playing field. This applies equally to teams and to individual players (see [[concept-individual-offensive-rating]]).

## When to Use
- Comparing offensive or defensive efficiency across teams that play at different tempos
- Evaluating lineup combinations or five-man units
- Forecasting wins from current efficiency differential
- Identifying whether a team's record is sustainable (over/under-performing their efficiency)
- Assessing individual player contributions when combined with individual possession counts

## Key Principles
1. **Possessions are the denominator.** Every offensive action ends in a possession terminator: field goal attempt (made or missed), turnover, or free throws (last of a trip). Counting possessions accurately is the prerequisite for all efficiency metrics.
2. **Per-100 scaling.** Raw per-possession fractions are multiplied by 100 for readability — a typical NBA ORtg in 2003 was ~105; elite was ~115; poor was ~95.
3. **Efficiency differential predicts wins.** The spread between a team's ORtg and its DRtg correlates very strongly with winning percentage. Oliver developed regression equations to convert this differential to expected wins [S16, Ch.4, Ch.23].
4. **Pace neutralization.** Two possessions used in a fast-break game count exactly the same as two possessions in a half-court game. This is the essential advantage over raw points-per-game.
5. **Both sides of the ball matter equally.** An ORtg of 110 and a DRtg of 110 produces a .500 team. Neither offense nor defense alone wins championships — the *margin* does.

## Player Responsibilities
All positions benefit from understanding this framework:
- **PG**: Turnover rate and assist-to-possession ratio directly affect team ORtg
- **SG/SF**: Shooting efficiency (EffFG%) is the largest single driver of ORtg
- **PF/C**: Offensive rebounding % (OR%) extends possessions; defensive rebounding % ends opponent possessions

## Variations
### Team Offensive Rating (TMORtg)
Points produced by a team divided by total team possessions × 100. The cleanest single number to evaluate an offense across a season or stretch of games [S16].

### Team Defensive Rating (TMDRtg)
Points allowed divided by total possessions × 100. Lower is better. Used to rank defenses independently of pace.

### Individual Offensive Rating (ORtg)
Points *produced* by an individual player per 100 individual possessions. Requires allocating team scoring credit to individuals — the central technical challenge of the book (→ [[concept-individual-offensive-rating]]).

### Individual Defensive Rating (DRtg)
Points *allowed* per 100 individual possessions. Much harder to calculate from box-score data alone (→ [[concept-individual-defensive-rating]]).

## Common Mistakes
1. **Confusing points per game with points per possession** → Points per game inflates fast-paced teams and penalizes slow ones; always normalize by possessions when comparing teams.
2. **Ignoring the defensive side** → A coach who only optimizes ORtg while DRtg craters will not win more games. The differential is what matters.
3. **Treating individual ORtg as purely an individual quality** → Individual ratings reflect both the player AND the teammates around him. Context adjustment is required for fair comparisons.
4. **Double-counting possessions** → Offensive rebounds extend possessions; they do not create new ones. Correctly counting possessions requires: FGA − OREB + TOV + (0.44 × FTA).

## Related Concepts
- [[concept-individual-offensive-rating]] — how individual ORtg is calculated from team ORtg and individual statistics
- [[concept-individual-defensive-rating]] — the harder defensive version
- [[concept-floor-percentage]] — proportion of an individual's possessions that end in a score
- [[concept-basketball-statistical-framework]] — the overarching analytical framework of which this is a part
- [[concept-four-factors-winning]] — the four team statistics most correlated with ORtg/DRtg
- [[concept-performance-rating-system]] — a related but different weighted scoring framework [S13]

## Sources
- [S16, pp.1-2] — introduction of points per 100 possessions as the core metric
- [S16, Ch.3] — application to team efficiency rankings
- [S16, Ch.14] — individual offensive rating formulas
- [S16, Ch.17] — individual defensive rating formulas
- [S16, Ch.23] — practical team evaluation using this metric
