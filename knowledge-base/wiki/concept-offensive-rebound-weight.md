---
type: concept
level: advanced
positions: [PF, C, SF]
tags: [analytics, statistics, offense, rebounding, player-evaluation]
source_count: 1
last_updated: 2026-04-11
---

# Offensive Rebound Weight

## Summary
The offensive rebound weight (TMOREB weight) determines how much credit an offensive rebounder receives relative to scorers and assisters on the same play. Dean Oliver derives this weight using the "difficulty concept" — borrowed from Bill James's win percentage formula — which pits the difficulty of getting an offensive rebound against the difficulty of scoring on a play [S16, pp.345-346].

The key insight is that the value of an offensive rebound is **team-context dependent**: on teams that shoot poorly (low TMPlay%), offensive rebounds are less valuable because the subsequent possession is unlikely to score. On teams that shoot well (high TMPlay%), offensive rebounds are more valuable.

## When to Use
- Evaluating the true offensive contribution of high-rebounding players (Dennis Rodman, Ben Wallace-era comparisons)
- Understanding why offensive rebounding value varies by team context
- Comparing offensive rebounders across teams with different offensive efficiencies

## Key Principles

1. **The Competition Framework**: Oliver uses the analogy of two teams competing — the "offensive rebounding team" (difficulty = 1 − TMOR%) and the "scoring team" (difficulty = 1 − TMPlay%). The weight is the winning percentage of the harder task [S16, p.346].

2. **The Formula** [S16, p.346]:
```
TMOREB_weight = (1 − TMOR%) × TMPlay% 
              ÷ [(1 − TMOR%) × TMPlay% + TMOR% × (1 − TMPlay%)]
```

3. **Worked Example** [S16, p.346]: If TMOR% = 0.30 and TMPlay% = 0.45:
   - Offensive rebounding difficulty = 1 − 0.30 = 0.70
   - Scoring difficulty = 1 − 0.45 = 0.55
   - TMOREB_weight = 0.70 × 0.55 ÷ (0.70 × 0.55 + 0.30 × 0.55) = 0.66
   - Weight on scoring = 0.34

4. **NBA Range (2002)**: 0.57 (Golden State Warriors — shot poorly, got many rebounds) to 0.70 (Detroit Pistons — shot well, got few offensive rebounds) [S16, p.346]. An offensive rebound was ~20% more valuable for Detroit than Golden State.

5. **Why poor-shooting teams get less credit**: Golden State needed **six** offensive rebounds to help their offense as much as **five** Pistons offensive rebounds helped Detroit's offense — because the Warriors were less likely to convert after the rebound [S16, p.346].

6. **The Full OR Part formula** [S16, pp.345-346]:
```
OR Part = OR × TMOREB_weight × TMPlay%
```
The TMPlay% multiplier adjusts for the fact that an offensive rebound doesn't guarantee a score.

7. **The 15% improvement finding**: John Maxwell found that offensive rebounds increase a team's offensive rating ~15%, but nearly all of this is from the rebounder's own subsequent scoring ability, not from helping teammates. This is why the improvement shows up in the rebounder's own FG/FT stats rather than requiring a separate adjustment [S16, p.346].

## Common Mistakes
1. **Assuming all offensive rebounds are equally valuable** → They are not; team shooting efficiency determines their value
2. **Overrating high-rebound players on poor-shooting teams** → The formula automatically discounts them
3. **Ignoring the probabilistic nature** → An offensive rebound starts a new play; it doesn't guarantee points, which is why the TMPlay% multiplier is applied

## Related Concepts
- [[concept-individual-offensive-rating]] — The parent metric that uses TMOREB weight as a component
- [[concept-floor-percentage]] — Offensive rebounds directly increase scoring possessions and thus floor%
- [[concept-individual-defensive-rating]] — Defensive rebounds have a parallel weighting on the defensive side via FMwt

## Sources
- [S16, pp.345-347] — Complete derivation and NBA context
