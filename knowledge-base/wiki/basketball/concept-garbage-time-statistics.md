---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, garbage-time, offensive-rating, defensive-rating, game-management]
source_count: 1
last_updated: 2026-04-11
---

# Garbage Time and Statistics

## Summary
When a team builds a large lead, they typically substitute bench players, run down the shot clock, and play conservatively — this is "garbage time." The result is that the winning team's offensive rating looks *worse* than it should (more bad shots, conservative play) and the losing team's offensive rating looks *better* (playing against bench defenders). Good teams have more garbage time and therefore their statistics are systematically deflated; bad teams are correspondingly inflated.

This effect is captured in the [[concept-basketball-bell-curve-model]] formula as the **covariance term** — a positive correlation between a team's PPG and DPPG indicates that when the team scores more, it also allows more (the signature of playing down to opponents). Removing this covariance reveals **uncorrelated ratings** [S16, pp.138-139].

## When to Use
- Evaluating whether a dominant regular-season team will maintain performance in the playoffs (where there is no garbage time)
- Comparing historical teams fairly
- Understanding why teams with similar point differentials have different playoff outcomes

## Key Principles
1. **A 20-point lead should grow.** If both teams maintained equal effort, a 20-point lead with 6 minutes left becomes ~24 points at the final buzzer. In practice, it usually shrinks [S16, p.138].
2. **Garbage time misrepresents both teams.** The winning team plays conservatively (deflated); the losing team benefits from relaxed defense (inflated). Neither set of numbers reflects true competitive ability.
3. **The covariance term measures this.** When PPG and DPPG are positively correlated across a season, the team is playing up/down to its competition. Setting covariance to zero = assuming no garbage time effect [S16, pp.138-139].
4. **Teams "apply themselves" in playoffs.** Uncorrelated ratings better predict playoff outcomes because postseason play has essentially no garbage time — every minute is competitive [S16, p.142].
5. **The practical adjustment is usually modest.** Rankings shuffle somewhat but the overall picture doesn't change dramatically. The concept matters most for the truly dominant teams at the extremes [S16, p.141].

## Coaching Implications
- **Don't evaluate players based on garbage-time numbers** — either positively (inflated stats for bench players on losing teams) or negatively (suppressed stats for starters on blowout winners)
- **Use full-effort practice to simulate no-garbage-time performance** — a team that competes on every possession in practice will have naturally low covariance
- **Scouting:** When preparing for the playoffs, standard regular-season ratings may *understate* your opponent's true capability if they played in many blowouts

## Common Mistakes
1. **Trusting raw season averages for playoff predictions** → correction: apply uncorrelated rating concept; a dominant regular-season team will perform *better* in the playoffs than their standard numbers suggest
2. **Crediting bench players for garbage-time stats** → correction: garbage-time stats represent inflated numbers against non-competitive opposition
3. **Ignoring the positive covariance indicator** → correction: if a team's PPG and DPPG are strongly positively correlated, they are playing down to their competition and their true quality is better than the ratings show

## Related Concepts
- [[concept-uncorrelated-ratings]] — the adjustment tool built from this concept
- [[concept-basketball-bell-curve-model]] — the formula containing the covariance term
- [[concept-performance-rating-system]] — individual player rating adjustments for playing time quality

## Sources
- [S16, pp.138-139] — garbage time description, covariance interpretation, uncorrelated ratings definition
