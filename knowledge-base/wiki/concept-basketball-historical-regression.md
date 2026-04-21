---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, historical-analysis, regression, evaluation]
source_count: 1
last_updated: 2026-04-11
---

# Basketball Historical Regression (Team Statistic Estimation)

## Summary
Dean Oliver's Appendix 4 of *Basketball on Paper* describes a multivariate linear regression methodology used to **estimate missing historical NBA team statistics** — specifically turnovers (TOV) and offensive rebounds (OREB) — for the period before these statistics were officially recorded (pre-1974). This technique was used primarily to enable cross-era comparisons of Wilt Chamberlain and Bill Russell in Chapter 21 [S16, pp.364-366].

The regression approach recognizes that known box-score statistics (FGA, FTA, REB, PF, FGM, FTM, PTS, AST) systematically co-vary with the unrecorded statistics. By training a multivariate model on all NBA team data since 1974 (710 observations), Oliver derives coefficients that explain approximately 80–81% of the variation in TOV and OREB, with standard errors of ~97 turnovers and ~74 offensive rebounds per team per season.

## Key Principles

### The Regression Equations

**Estimated Turnovers:**
```
TOV = a₀ + a_Seas(SEAS) + a_G(G) + a_FGA(FGA) + a_FTA(FTA) 
      + a_REB(REB) + a_PF(PF) + a_DQ(DQ) 
      + a_FGM(FGM) + a_FTM(FTM) + a_PTS(PTS) + a_AST(AST)
```

**Estimated Offensive Rebounds:**
```
OREB = b₀ + b_Seas(SEAS) + b_G(G) + b_FGA(FGA) + b_FTA(FTA) 
       + b_REB(REB) + b_PF(PF) + b_DQ(DQ) 
       + b_FGM(FGM) + b_FTM(FTM) + b_PTS(PTS) + b_AST(AST)
```

### Regression Accuracy (Table A4.1)

| Statistic | Multiple R | R² | Adjusted R² | Std. Error | Observations |
|-----------|-----------|-----|-------------|------------|-------------|
| Turnovers | 0.90 | 0.81 | 0.81 | 97 | 710 |
| OREB | 0.90 | 0.80 | 0.80 | 74 | 710 |

"I would call this 'not bad.'" — Dean Oliver [S16, p.365]

### Key Parameter Findings (Selected)

**Turnovers (Table A4.2) — significant predictors:**
- Season trend (SEAS): −17.6 per year (turnovers have declined over time)
- Games (G): +11.7 per game
- FGA: −0.0615 (more shots = slightly fewer turnovers, after other controls)
- FTA: +0.373 (drawing fouls correlates with turnovers)
- REB: +0.144
- PF: +0.180
- FTM: −0.3676 (significant negative)
- AST: +0.0803 (each assist implies ~0.08 additional turnovers)

**Offensive Rebounds (Table A4.3) — significant predictors:**
- FGA: +0.217 (most important predictor — more shots = more rebound opportunities)
- FTA: +0.447 (drawing fouls correlates with offensive rebound situations)
- REB: +0.174 (total rebounds correlate with offensive portion)
- FGM: +0.1551
- FTM: −0.3119
- PTS: −0.104
- AST: −0.085

**Non-significant findings:**
- Fouling out (DQ): Not reliably related to turnovers
- Made field goals (FGM): Not reliably related to turnovers (after other controls)
- Points (PTS): Not reliably related to turnovers
- Personal fouls (PF): Not reliably related to offensive rebounds

### How to Interpret P-Values
- **p < 0.05**: The coefficient is statistically significant — there is probably a real dependence on that statistic
- **p > 0.05**: The coefficient is NOT reliably different from zero; the variable probably does not meaningfully predict the target statistic
- Note: Statistical significance ≠ correctness of the specific coefficient value [S16, p.365]

## When to Use
This methodology is appropriate for:
- Estimating statistics that were not recorded in a historical era (pre-1974 NBA turnovers and offensive rebounds)
- Filling in missing data when the target statistic co-varies systematically with available data
- Cross-era player comparisons where data completeness differs by era

It is **not** appropriate for:
- High-stakes individual player evaluations where regression error (±97 TOV/±74 OREB per season) is too imprecise
- Situations where collinearity between predictors has not been tested and managed

## Limitations
1. **Assumes historical stability** — The coefficients trained on 1974+ data are assumed to describe pre-1974 basketball, which may not be true if the game changed structurally.
2. **Standard errors are large** — ±97 turnovers per team per season = roughly ±1 per game; useful for estimates, not precision.
3. **80% R² leaves 20% unexplained** — The models are "not bad" but imperfect.
4. **Collinearity not formally tested** — Oliver acknowledges he did not perform collinearity tests or eliminate insignificant variables, noting it was not necessary for his discussion purposes [S16, p.366].
5. **Subjectivity in model specification** — "How you ask the question or set up the solution is where some subjectivity is introduced" [S16, p.366].

## Practical Coaching Application
While this technique is primarily a research tool, the **key insight for coaches** is that:
- **Assists and turnovers are linked** — Passing more creates more turnover opportunities (each assist correlates with ~0.08 turnovers)
- **Drawing fouls correlates with turnovers** — High-contact offensive styles generate both FTA and TOV
- **FGA volume predicts offensive rebounding opportunity** — Teams that take more shots create more OREB chances

These relationships hold even after controlling for other variables, suggesting causal mechanisms worthy of coaching attention.

## Common Mistakes
1. **Over-interpreting coefficient values** — The specific numbers (e.g., 0.0803 per assist) are estimates with standard errors, not exact laws.
2. **Ignoring the standard error** — A regression that explains 80% still has 20% error; conclusions should be directional, not precise.
3. **Assuming regression transfers perfectly across eras** — Rule changes, pace shifts, and style changes may break historical regression relationships.

## Related Concepts
- [[concept-basketball-analytics-glossary]] — The possession and statistical definitions that underpin Oliver's analytical framework
- [[source-basketball-on-paper]] — The full source summary for this book
- [[concept-performance-rating-system]] — An alternative approach to player evaluation from S13
- [[concept-basketball-performance-indicators-winning]] — Evidence-based performance indicator analysis from S12

## Sources
- [S16, pp.364-366] — Appendix 4: Team Statistic Historical Regression, with Tables A4.1, A4.2, A4.3
