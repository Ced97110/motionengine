---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [analytics, offense, defense, statistics, team-evaluation, shooting, rebounding]
source_count: 1
last_updated: 2026-04-11
---

# Four Factors of Winning Basketball

## Summary
The Four Factors framework, developed by Dean Oliver in *Basketball on Paper*, identifies the four team statistical categories that most directly determine offensive and defensive ratings (points per 100 possessions). Every other box-score statistic ultimately flows through one of these four channels.

The Four Factors (with approximate relative weights) are:
1. **Shooting efficiency — EffFG%** (~40% of importance): `(FGM + 0.5 × FG3M) / FGA`. Adjusted field goal percentage that gives 3-pointers their proper 1.5× weight.
2. **Turnovers — TOV%** (~25%): `TOV / Possessions`. The fraction of possessions wasted by turnovers.
3. **Offensive Rebounding — OR%** (~20%): `OREB / (OREB + opponent DREB)`. The fraction of missed shots recaptured by the offense.
4. **Free Throws — FT Rate** (~15%): `FTA / FGA`. How often the offense gets to the line relative to its shot attempts (and FT% on those attempts).

These factors apply to **both sides of the ball**: an offense wants to maximize its EffFG% and OR% and minimize its TOV%, while a defense wants to minimize opponent EffFG% and OR% and maximize opponent TOV% [S16, Ch.3, Ch.23].

## When to Use
- Diagnosing *why* a team's ORtg or DRtg is high or low
- Prioritizing improvement areas in practice and game planning
- Scouting opponents: identify which of the four factors they are weakest in and exploit it
- Post-game analysis: determine which factor(s) caused a win or loss
- Player acquisition: target players who improve your weakest factor

## Key Principles
1. **Shooting is the most important factor.** EffFG% has the highest correlation with ORtg of any single statistic. A team that shoots efficiently can survive other weaknesses.
2. **Turnovers are pure waste.** A turnover gives zero points and hands the opponent a possession. The best offenses protect the ball obsessively.
3. **Offensive rebounding is a multiplier.** OR% above 30% meaningfully increases ORtg by extending possessions at high efficiency (close shots after offensive rebounds).
4. **Free throws have a double impact.** Getting to the line: (a) adds high-efficiency points (no defense on FTs), and (b) puts opponents in foul trouble.
5. **The factors are partially under coaching control.** Shot selection (EffFG%), ball security (TOV%), post presence (OR%), and aggression (FT rate) all respond to coaching emphasis.
6. **Weighting matters for prioritization.** Oliver's research showed that improving shooting efficiency yields the most wins per unit of improvement; improving free throw rate yields the least. Coaches should allocate practice time accordingly.

## Player Responsibilities
- **PG**: Primary driver of TOV% (ball security, decision-making); assists affect EffFG% of teammates
- **SG/SF**: Primary driver of EffFG% (shot selection, 3PT efficiency)
- **PF/C**: Primary driver of OR% (offensive rebounding position and effort); also FT rate (drawing fouls in the post)

## Variations
### Defensive Four Factors
The same four factors apply defensively with inverted signs:
- Force low opponent EffFG% (good perimeter and post defense)
- Force high opponent TOV% (pressure, trapping, active hands)
- Secure defensive rebounds (low opponent OR%)
- Avoid sending opponents to the line (discipline = low opponent FT rate)

## Common Mistakes
1. **Treating all four factors equally** → Shooting (EffFG%) is roughly twice as important as free throws; allocate coaching attention accordingly.
2. **Ignoring opponent OR%** → Defensive rebounding is undervalued by coaches who focus only on blocking shots. Giving up offensive rebounds can destroy an otherwise good DRtg.
3. **Confusing FG% with EffFG%** → Regular FG% ignores the extra value of 3-pointers. A team that shoots 42% on all 2s and 3s but makes 35% of 3s has a higher EffFG% than the raw FG% suggests.
4. **Over-indexing on turnovers** → While TOV% matters, reducing it sometimes comes at the cost of EffFG% (conservative shot selection). The right balance depends on the other three factors.

## Related Concepts
- [[concept-points-per-possession]] — the outcome the four factors predict
- [[concept-basketball-statistical-framework]] — the analytical system in which the four factors sit
- [[concept-individual-offensive-rating]] — individual-level decomposition
- [[concept-rebounding-position-savvy]] — rebounding fundamentals [S15]
- [[concept-three-point-shot-trends]] — the role of 3PT shooting in EffFG% [S13]

## Sources
- [S16, Ch.3] — application to best and worst offenses/defenses
- [S16, Ch.23] — practical team evaluation using the four factors
- [S16, pp.1-2] — conceptual introduction
