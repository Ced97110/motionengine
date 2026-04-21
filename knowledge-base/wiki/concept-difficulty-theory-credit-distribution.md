---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, offense, defense, teamwork, player-evaluation]
source_count: 1
last_updated: 2026-04-11
---

# Difficulty Theory for Distributing Credit in Basketball

## Summary
When two or more players cooperate to create a basketball outcome (a score, a stop, a rebound), the credit for that outcome should be divided in proportion to the *difficulty* of each player's contribution. The more difficult the contribution — meaning the less likely it was to occur without that player's specific action — the more credit it deserves. This principle, developed by Dean Oliver in *Basketball on Paper*, provides a mathematically grounded alternative to box-score credit allocation [S16, pp.145-153].

The theory has a strict conservation constraint: credit cannot exceed the actual outcome. Two points scored on a play equals exactly two points of credit distributed between passer and scorer — no more, no less. This forces honest valuation and prevents stat inflation.

## When to Use
- When evaluating whether a player's box-score stats reflect their true offensive contribution
- When comparing passers and scorers on the same team
- When assessing the value of a role player vs. a star
- When building analytical models for roster construction or playing time decisions
- When explaining to players *why* their contribution matters even without big scoring numbers

## Key Principles
1. **The harder the contribution, the more credit it deserves.** A pass to an open post player under the basket is difficult (defenses rarely allow it); the resulting dunk is easy. The passer gets most of the credit [S16, p.145].
2. **The sum of parts equals the whole.** You cannot give a passer 50% credit AND the scorer 80% credit on a two-point play. Together they must share exactly two points [S16, p.148].
3. **Credit is measured by the change in expected points.** Before the pass, a possession is worth ~1.0 expected point (NBA average). After a pass to a big man under the hoop, expected value jumps to ~1.7 (85% chance of 2 pts). The passer gets credit for that 0.7 increase; the scorer gets credit for converting the remaining probability [S16, pp.146-147].
4. **Context determines difficulty.** An assist on a good shooting team is worth more than the same assist on a poor shooting team, because the shot is more likely to be made [S16, p.147].
5. **Scoring is generally more difficult than passing.** Coaches consistently express preference for having a scorer over a passer, implying scorers are in shorter supply and deserve somewhat more credit on average [S16, p.145].
6. **Credit constraints force honest team evaluation.** A player's individual production cannot exceed the team's total production. A player cannot be worth 17 wins on a 17-win team AND have meaningful other contributors [S16, pp.148-149].

## Application Examples

### Example 1: Pass to Big Man Under the Basket
- Start of possession: ~1.0 expected points
- After pass to big under hoop (85% dunk): ~1.7 expected points  
- Passer credit: **+0.7** (raised expected value)
- Scorer credit: **+0.3** (converted the high-probability attempt)
- If splitting 2 actual points: passer gets **1.4 pts**, scorer gets **0.6 pts** [S16, p.147]

### Example 2: Pass to Poor-Shooting Big Man on Perimeter
- Defense doesn't respect this player → pass is easy and expected value barely changes
- If he takes and makes the shot, it was unexpected → scorer deserves almost all credit
- Passer credit: **~0.0**
- Scorer credit: **~2.0** [S16, pp.146-147]

### Defensive Application
- Forcing a miss (successful ~55% of the time in NBA) is *harder* than getting the defensive rebound (~70% of the time)
- Therefore: **good shot defenders are more valuable than good defensive rebounders** in the NBA
- At lower levels where shooting is worse and offensive rebounding is better, the relative value shifts toward defensive rebounding [S16, p.148]

### Offensive Rebound Application
- An offensive rebound increases scoring odds but is not strictly necessary for a score
- Rebounds are more valuable when they are relatively rare
- If it is difficult to get the offensive rebound AND easy to score after getting it, the offensive rebound has high value [S16, p.148]

## Two Methods of Constraining Credit
1. **Beforehand (preferred):** As you give one player credit, you simultaneously remove it from others. More difficult to calculate but a better test of the method's validity [S16, p.153].
2. **Normalization ("cheating"):** Assign all credit freely, then scale everyone proportionally so the sum matches the true total. Always replicates team results exactly, but by forcing it [S16, p.153].

## Common Mistakes
1. **Double-counting credit** → Remember: passer + scorer must share exactly the points scored, not an inflated total
2. **Ignoring context** → An assist on a poor shooting team has less value than the same assist on a good shooting team; credit is not position-independent
3. **Rewarding effort instead of difficulty** → A long pass that leads to a 30% three-point attempt may deserve less credit than a short pass to a 90% layup
4. **Treating all assists equally** → Box-score assists ignore the difficulty of the pass and the difficulty of the resulting shot

## Related Concepts
- [[concept-individual-offensive-rating]] — the primary output of applying this theory to individual players
- [[concept-individual-floor-percentage]] — individual scoring efficiency metric derived from difficulty-weighted credit
- [[concept-uncorrelated-offensive-defensive-ratings]] — related framework for separating team offensive/defensive ratings
- [[concept-performance-rating-system]] — a different statistical framework for player evaluation [S13]

## Sources
- [S16, pp.144-153] — Chapter 13: Teamwork 3: Distributing Credit among Cooperating Players
