---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, offense, player-evaluation, efficiency]
source_count: 1
last_updated: 2026-04-11
---

# Individual Floor Percentage

## Summary
Individual floor percentage is a player's scoring possessions divided by his total possessions. It answers the question: *"What percentage of the time that a player wants to score does he actually score?"* It is the individual analog of team floor percentage and is one of the two key offensive statistics developed in *Basketball on Paper* alongside [[concept-individual-offensive-rating]] [S16, pp.149-150].

Floor percentage emphasizes *consistency* of scoring — the ability to create a scoring outcome. It differs from individual offensive rating in that it does not account for the value of each scoring possession (e.g., whether it produced 1, 2, or 3 points). A player who scores often on two-point plays may have a higher floor percentage but a lower rating than a three-point specialist.

## When to Use
- Comparing players' ability to *create* scoring outcomes regardless of how many points those outcomes are worth
- Identifying high-efficiency post players vs. high-efficiency perimeter shooters
- Understanding why two players with similar scoring averages have different impacts
- Scouting: identifying which offensive players defenses most need to disrupt

## Key Principles
1. **Floor% = Scoring Possessions / Total Possessions.** Total possessions include scoring possessions, unrebounded missed FGs, unrebounded missed FTs, and turnovers [S16, p.150-151].
2. **Post players near the basket tend to have high floor percentages.** Shaq's 59% floor percentage in 2002 was the second-best in the league among 15+ PPG players [S16, p.155].
3. **Three-point shooters can have relatively low floor percentages but high ratings.** Missing a three is still a missed possession, which lowers floor%; but made threes are worth more points per scoring possession, lifting the rating [S16, p.150].
4. **Turnovers directly reduce floor percentage.** Every turnover is a total possession with zero scoring possessions returned [S16, p.151].
5. **League averages change over time.** NBA average floor% was ~0.534 in the mid-1980s and declined to ~0.494 by 2002 as pace and three-point volume changed [S16, p.155].

## Formula
```
Scoring Possessions = (FG Part + AST Part + FT Part)
    × (1 − TMOREB/TMScPoss × TMOREB_weight × TMPlay%)
    + OREB × TMOREB_weight × TMPlay%

Total Possessions = Scoring Possessions
    + (FGA − FGM) × (1 − 1.07 × TMOR%)
    + (1 − FT%)² × 0.4 × FTA
    + TOV

Floor% = Scoring Possessions / Total Possessions
```
[S16, pp.150-151]

## Interpreting Floor% vs. Offensive Rating
| Player Style | Floor% | Off. Rtg | Explanation |
|---|---|---|---|
| Post scorer (Shaq 2002) | High (0.59) | Good (116) | Scores often but misses FTs = fewer points per scoring poss |
| 3PT specialist (Kerr 1996) | High (0.58) | Elite (141) | Scores consistently AND gets 3pts when he does |
| Volume scorer (I. Rider 1999) | Low (0.46) | Poor (99) | Takes many shots, doesn't convert efficiently |
| Low-usage role player (Horry 2002) | Moderate (0.50) | High (114) | Only shoots easy looks = efficiency from shot selection |

[S16, pp.157-159]

## NBA Historical Benchmarks
- League-average floor% ranged from 0.483 (1974) to 0.534 (1985)
- By 2002: league average was ~0.494
- A floor% of 0.55+ in 2002 indicated a very good offensive player
- A floor% of 0.55 in the 1980s was merely above average [S16, p.155]

## Common Mistakes
1. **Treating floor% as the only efficiency metric** → A player with floor% = 0.60 who only makes two-pointers is less valuable than one with floor% = 0.55 who hits threes consistently
2. **Ignoring assists** → Assists *received* actually reduce a player's points produced (since the assister gets credit), which can lower apparent floor%
3. **Cross-era comparisons without baseline** → Floor% has compressed significantly since the mid-1980s; always compare to era average

## Related Concepts
- [[concept-individual-offensive-rating]] — companion metric measuring points per 100 possessions
- [[concept-difficulty-theory-credit-distribution]] — the theory underlying both metrics
- [[concept-uncorrelated-offensive-defensive-ratings]] — separating team-level offensive and defensive components

## Sources
- [S16, pp.149-162] — Chapters 13 & 14
