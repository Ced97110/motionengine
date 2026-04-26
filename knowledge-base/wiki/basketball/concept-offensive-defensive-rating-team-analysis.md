---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [analytics, team-evaluation, basketball-on-paper, offensive-rating, defensive-rating]
source_count: 1
last_updated: 2026-04-11
---

# Offensive and Defensive Rating: Team Analysis Tools

## Summary
Offensive rating (points scored per 100 possessions) and defensive rating (points allowed per 100 possessions) are the two foundational team evaluation metrics in Basketball on Paper. Unlike win-loss records, these ratings isolate a team's scoring and prevention efficiency from the effects of pace (fast vs. slow teams), making them directly comparable across teams and seasons. A team's net rating (offensive rating minus defensive rating) is the single best predictor of its true quality.

When compared to the league average, these ratings immediately reveal whether a team is above or below average on each side of the ball — and by how much. The 2002 Toronto Raptors, for example, had an offensive rating that went from ~3 points *above* league average in 2001 to ~2 points *below* in 2002, while their defensive rating actually *improved* — clearly identifying the source of their decline [S16, p.319].

## When to Use
- Season-end review: compare both ratings to league average
- In-season monitoring: plot five-game moving averages to track trends and identify slumps
- Roster decisions: determine which side of the ball needs improvement
- Player evaluation: frame individual analysis around whether the team's problem is offensive or defensive
- Historical comparison: normalize across eras by using deviation from league average

## Key Principles
1. **Points per 100 possessions, not points per game** — possession-based ratings eliminate pace effects and allow fair cross-team and cross-era comparisons [S16].
2. **Compare to league average** — a rating of 106 in a 104-average league means more than 106 in a 108-average league; always contextualize.
3. **Net rating = true team quality** — the difference between offensive and defensive rating predicts win percentage more accurately than either alone.
4. **Moving averages reveal timing** — a five-game moving average of both ratings through the season turns a flat season-long number into a revealing narrative showing when the team changed [S16, p.320].
5. **Cumulative net points** — plotting the running sum of point differential by game creates a visual that shows sustained good or bad stretches more clearly than game-by-game fluctuations [S16, p.320].
6. **Defense can improve while offense declines** — these are independent dimensions; teams that rebuild defensively may sacrifice offensive efficiency and vice versa.

## Interpreting Moving-Average Charts
- A chart with Offensive and Defensive ratings both plotted on five-game moving averages shows:
  - Peaks and valleys in offensive efficiency through the season
  - Whether defensive improvements are sustained or temporary
  - The approximate date of a key injury, trade, or strategic change
- The cumulative net-point chart adds a second dimension:
  - A flat line = roughly breaking even (wins and losses balanced)
  - A rising line = team outscoring opponents consistently
  - A falling line = being outscored consistently (classic losing streak signature)
  - A sharp inflection = something significant changed (injury, return, coaching adjustment)

## Common Mistakes
1. **Using points per game instead of per-possession** → Fast teams score more; slow teams score less; neither comparison is fair without pace adjustment.
2. **Comparing ratings without league-average context** → An offensive rating of 107 was elite in the 1990s but merely average by 2020.
3. **Ignoring the defensive side** → Teams frequently improve defense while declining offensively; diagnosing the wrong side leads to wrong roster decisions.
4. **Over-interpreting single-game fluctuations** → Five-game moving averages smooth noise and reveal true trends; single games are too volatile.

## Related Concepts
- [[concept-four-offensive-factors-team-evaluation]] — the next diagnostic step after identifying which rating changed
- [[concept-team-first-player-second-analysis]] — the philosophical framework for using these ratings
- [[concept-performance-rating-system]] — individual-level extension of this team-level framework

## Sources
- [S16, pp.318-322] — team rating analysis demonstrated through 2002 Toronto Raptors case study, including Figures 23.1-23.4
