---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, player-evaluation, statistics, offense, defense, ratings]
source_count: 1
last_updated: 2026-04-11
---

# Individual Win-Loss Records

## Summary
Because there is no true individual win or loss in basketball, individual win-loss records are statistical constructs that approximate how well a player fills their role. The author presents two primary methods: game-by-game records and bell curve (Pythagorean) records. Neither method measures absolute quality — they measure role fulfillment in context. A player on a bad team filling a limited role decently will look better than a key player on the same bad team who fills their important role poorly [S16, pp.243-244].

These records are most useful for understanding the relationship between a player's performance and their team's outcomes, predicting what happens when a player leaves a team, and identifying whether a player is truly "leading" their team or merely performing well in a supporting context [S16, pp.249-256].

## When to Use
- Evaluating whether a player is truly the "leader" of their team
- Predicting team performance if a key player departs
- Assessing role fulfillment vs. absolute quality
- Comparing player impact across seasons and teams
- Identifying players whose individual win% closely tracks their team's win%

## Key Principles
1. **Game-by-game records measure role fulfillment, not absolute quality.** Steve Kerr (63-19) was not a better player than Scottie Pippen (55-22) on the 1996 Bulls — Kerr simply filled a narrower role (shoot threes, don't make mistakes) very well [S16, p.245].
2. **Leaders' individual records should closely track their team's records.** Michael Jordan's game-by-game win% tracked almost perfectly with the Bulls' win% across every season — a hallmark of true team leadership [S16, p.247].
3. **Great individual records that consistently exceed team records may signal a leadership gap.** David Robinson's individual record exceeded his team's in every season, often by a wide margin — suggesting he was performing well but not carrying the team in big moments [S16, pp.247-248].
4. **A team can be as good as its best player — but that player sometimes has to take the tough shot.** The thing Robinson may have lacked was not skill but the willingness to create, even at the cost of a lower offensive rating [S16, p.249].
5. **Role transitions show up in the data.** As Dirk Nowitzki assumed the leadership role in Dallas, his individual win% came down from .744 to .711 while the team's record improved — reflecting the cost of taking on more possessions and tougher shots [S16, p.248].
6. **Top players can be responsible for roughly one-quarter to one-third of team games.** No single player can reasonably be credited with 60 of 82 games in a season [S16, p.254].

## Method 1: Game-by-Game Win-Loss Records

### Calculation
If a player has a higher individual offensive rating than individual defensive rating in a game, that counts as an individual win. If their defensive rating is higher, it counts as a loss [S16, p.243].

### Interpretation
- **High win% on a winning team** = filling role well on a good team (MJ: 70-12, .854 on the 72-10 Bulls)
- **High win% on a losing team** = filling a limited/unimportant role decently (Tim Legler: 42-37, .532 on the 13-69 Mavericks)
- **Low win% despite being a key scorer** = poor role fulfillment in an important role (Jamal Mashburn: 14-65, .177 on the same Mavericks)

### Strengths
- Simple, intuitive
- Captures game-by-game variance
- Useful for projecting what happens when players change roles

### Limitations
- Does not measure absolute quality
- Context-sensitive: a player's record would differ on a different team
- Cannot predict performance in a new role, only show how a player fills their current role

### NBA Case Studies

**1996 Chicago Bulls (72-10):**
| Player | W-L (%) |
|---|---|
| Michael Jordan | 70-12 (.854) |
| Scottie Pippen | 55-22 (.714) |
| Toni Kukoc | 56-25 (.691) |
| Ron Harper | 52-28 (.650) |
| Dennis Rodman | 37-27 (.578) |

**2002 New Jersey Nets (52-30) — distributed scoring, all role players:**
Jason Kidd and Kerry Kittles both 47-35 (.573); Todd MacCulloch 41-21 (.661) [S16, p.244]

**1994 Dallas Mavericks (13-69) — bad team:**
Tim Legler 42-37 (.532) led team; Jim Jackson 16-66 (.195); Jamal Mashburn 14-65 (.177) [S16, p.245]

### Leadership Tracking (Jordan vs. Robinson)

Jordan's record tracked his team closely every season:
| Season | Jordan W-L% | Team W-L% |
|---|---|---|
| 1996 | .854 | .878 |
| 1997 | .768 | .841 |
| 1998 | .707 | .756 |

Robinson's record consistently exceeded his team:
| Season | Robinson W-L% | Team W-L% |
|---|---|---|
| 1994 | .813 | .675 |
| 1996 | .890 | .720 |
| 1998 | .822 | .685 |

[S16, pp.247-248]

### Predicting Team Performance After Player Departure
When Jordan retired after 1993, Pippen's established game-by-game rate (~50-30) predicted the Bulls would win ~50 games. They went 51-21 in games Pippen played [S16, p.249].

Kobe Bryant's win% (.600-.700) in 2001-2002 suggested a Kobe-led team would win 49-56 games — less than a Shaq-led team but still good [S16, pp.249-250].

## Method 2: Bell Curve (Pythagorean) Win-Loss Records

### Purpose
Bell curve records aim to show **how many wins and losses players produce for their team**. When summed across teammates, they approximate the team total — giving the measure a calibration check that game-by-game records lack [S16, p.250].

### Bell Curve Formula
```
Win% = NORM[(ORtg - DRtg) / 12.7]
```
where NORM is the Excel NORMSDIST() function, and 12.7 = √(11² + 11² - 2×40) using average NBA values for standard deviation (11) and covariance (40) [S16, p.252].

### Pythagorean-Like Formula (Easier)
```
Win% = ORtg^x / (ORtg^x + DRtg^x)
```
Where x (the exponent) varies by level:
- **NBA 1980s:** ~16-17
- **NBA 1990s onward:** ~13-14 (author uses 16.5 for consistency)
- **WNBA:** ~9-10
- **College/other levels:** ~6-10 (fewer possessions = smaller exponent)
- **General rule:** shorter games → smaller exponent [S16, pp.252-253]

### Estimating Games Responsibility
The method estimates how many "games" a player is responsible for using a weighted average of four components:
1. Percentage of team offensive possessions contributed to (weight: 3)
2. Percentage of team defensive stops made (weight: 3)
3. Percentage of team minutes played (weight: 1)
4. Percentage of games started (weight: 1)

Rationale: Offense and defense are the game's core elements; minutes and starts capture additional value (starters typically matter more early in games when games are decided) [S16, p.253].

**Upper bound:** No single player can reasonably be responsible for more than ~25-33% of team games. Responsible for ~20 games out of 82 is exceptional [S16, p.254].

### 1996 Bulls Bell Curve Records
| Player | W-L (%) |
|---|---|
| Michael Jordan | 16.1-0.5 (.972) |
| Scottie Pippen | 11.9-1.6 (.885) |
| Toni Kukoc | 7.7-0.4 (.951) |
| Dennis Rodman | 6.8-1.6 (.806) |
| Ron Harper | 7.2-1.0 (.879) |
| Steve Kerr | 5.2-0.0 (.997) |

Jordan's net ~15-16 wins means surrounded by average teammates, his team would win ~50 games — consistent with Bulls records in his absence [S16, p.251].

### Context Sensitivity Limitation
Bell curve records are context-sensitive. Ron Harper's 7-1 record came from defensive contribution on a team that didn't need him to score; he couldn't replicate that on a team needing offense. Allen Iverson's defensive rating improved dramatically when Larry Brown became coach — without Brown, Iverson's record would have been much worse [S16, p.254].

## Other Individual Win Methods

### Berri's Statistical Model (Win Scores)
Sports economist David Berri built a regression model explaining how team wins relate to team statistics (OReb, assists, blocks, etc.) and applied the weights to individual players. Unique aspect: weights offensive rebounds ~4× more than a point scored, which inflates rebounders (Rodman as top win-generator). The author questions this weighting [S16, p.255].

### Smith's Win Shares
Sean Smith's "win shares" method sets a floor at 60% of league average points, determines how many points above the floor equal a win, and distributes wins based on a Tendex-like statistic. Results are more plausible (Shaq's 2000 season = 27 wins), but the method is new and unvalidated [S16, p.256].

### Validation Problem
All individual win-loss methods face the same fundamental problem: **there is no ground truth to validate against**. Without a holy grail statistic, dramatic differences between methods cannot be resolved scientifically. It is not valid to criticize a method simply because it doesn't rank Jordan #1 — but the controversy continues [S16, p.256].

## Common Mistakes
1. **Treating game-by-game records as absolute quality rankings** → They measure role fulfillment, not absolute talent. Steve Kerr ≠ Scottie Pippen.
2. **Expecting a star player's record to always exceed their team's** → True leaders (Jordan, Malone, Duncan) have records that *match* their team's, not just exceed it.
3. **Ignoring context sensitivity** → A player's record changes dramatically based on team context (coach, teammates, role demands).
4. **Crediting one player with too many team games** → No player can reasonably be responsible for >~27 games (1/3 of 82) in a season.

## Related Concepts
- [[concept-performance-rating-system]] — PRS is a related player evaluation framework
- [[concept-basketball-performance-indicators-winning]] — team-level performance indicators
- [[concept-individual-offensive-skills-framework]] — developing the skills that drive individual ratings
- [[concept-offensive-system-design]] — how team context affects individual performance

## Sources
- [S16, pp.243-260] — complete individual win-loss chapter including game-by-game, bell curve, and other methods
