---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, offense, player-evaluation, possession-based]
source_count: 1
last_updated: 2026-04-11
---

# Individual Offensive Rating

## Summary
The individual offensive rating, developed by Dean Oliver, measures how many points a player produces per 100 offensive possessions. It is derived from three underlying statistics — **individual scoring possessions**, **individual total possessions**, and **individual points produced** — each of which distributes credit among cooperating players using the "difficulty concept": the harder a role is to execute (measured by its probability), the more credit a player receives [S16, p.343].

This metric moves beyond raw counting stats to capture a player's true offensive contribution regardless of role, usage rate, or team context. A player who scores efficiently, assists effectively, and rebounds offensively will show a high offensive rating even if their raw scoring totals are modest.

## When to Use
- Comparing offensive efficiency across players with different roles (scorer vs. facilitator vs. rebounder)
- Evaluating players across teams or eras on a common possession-based scale
- Identifying which players truly drive offensive production vs. benefiting from teammates
- Scouting and roster construction decisions where raw stats are misleading

## Key Principles

### 1. The Difficulty Concept
Credit in cooperative plays is split proportional to the difficulty of each role. A harder role (lower probability of success) earns more credit. For example, making a contested field goal is harder than assisting on an easy one, so the shooter gets more credit on difficult shots [S16, p.343].

### 2. Three Building Blocks
- **Individual Scoring Possessions**: Credit for times the team scores ≥1 point on a possession
- **Individual Total Possessions**: Credit for times the player ends a possession (scoring, missed FG rebounded by D, missed FT rebounded by D, or turnover)
- **Individual Points Produced**: Credit for the points generated (not just whether a score occurred)

**Floor Percentage** = Scoring Possessions ÷ Total Possessions
**Offensive Rating** = (Points Produced ÷ Total Possessions) × 100

### 3. The Four Parts of Individual Scoring Possessions
Scoring possessions come from four sources [S16, pp.343-346]:

**FG Part** (field goal credit, adjusted for assists received):
```
FG Part = FGM × (1 − (1/2) × (PTS−FTM)/(2×FGA) × q_AST)
```
Where q_AST is the estimated percentage of a player's field goals that were assisted.

**AST Part** (assist credit, based on effective FG% created):
```
AST Part = (1/2) × ((TMPTS−TMFTM)−(PTS−FTM)) / (2×(TMFGA−FGA)) × AST
```

**FT Part** (free throw credit):
```
FT Part = [1 − (1 − FT%)²] × 0.4 × FTA
```

**OR Part** (offensive rebound credit):
```
OR Part = OR × TMOREB_weight × TMPlay%
```
Where TMOREB_weight accounts for the relative difficulty of getting an offensive rebound vs. scoring on a play [S16, p.345].

### 4. The q_AST Formula (Assist Percentage Estimate)
Because box scores don't record what percentage of a player's shots were assisted, a formula is used [S16, p.344]:
```
q = (MIN / (TMMIN/5)) × q₅ + (1 − MIN/(TMMIN/5)) × q₁₂
```
Where:
- q₅ = 1.14 × (TMAST − AST) / TMFGM  [for high-minute players]
- q₁₂ = (TMAST/TMMIN × MIN×5 − AST) / (TMFGM/TMMIN × MIN×5 − FGM)  [for low-minute players]

High-percentage shooters get more credit taken away because it is harder to pass to a good shooter — thus a high-percentage shooter owes more to their assistants [S16, p.345].

### 5. Offensive Rebound Weight
The relative value of an offensive rebound vs. a scoring play is calculated using a Bill James-style competition formula [S16, p.346]:
```
TMOREB_weight = (1−TMOR%) × TMPlay% / [(1−TMOR%) × TMPlay% + TMOR% × (1−TMPlay%)]
```
NBA range in 2002: 0.57 (Golden State, poor shooting) to 0.70 (Detroit, good shooting). An offensive rebound was ~20% more valuable for Detroit than Golden State.

### 6. Final Scoring Possessions Formula
```
Scoring Possessions = (FG Part + AST Part + FT Part) 
  × (1 − TMOR/TMScPoss × TMOREB_weight × TMPlay%) + OR Part
```

## Player Responsibilities
- **PG**: Often high AST Part; lower FG Part due to more assisted shots by teammates; facilitator role shows up in assist credit
- **SG/SF**: Balanced FG Part and AST Part; shooting efficiency heavily impacts rating
- **PF/C**: High OR Part from offensive rebounds; FG Part dominant; often lower Floor% due to higher-difficulty post shots

## Variations

### Individual Points Produced
Same structure as scoring possessions but accounts for actual point values (2s vs. 3s) [S16, pp.348-349]:
```
FG Part = 2 × (FGM + ½×FG3M) × (1 − ½ × (PTS−FTM)/(2×FGA) × q_AST)
FT Part = FTM  [trivial — no assists on FTs in the NBA]
```

### Project Defensive Score Sheet Enhancement
When actual forced miss and forced turnover data is tracked (not just box score), the estimates improve dramatically [S16, p.360].

## Common Mistakes
1. **Treating offensive rating as independent of teammates** → It is not; team play%, team OR%, and team assist rate all affect individual calculations
2. **Ignoring the assist credit** → Playmakers who don't score much still produce substantial value through AST Part
3. **Overweighting offensive rebounds for poor-shooting teams** → The TMOREB weight adjusts for this automatically; offensive rebounds on bad-shooting teams are worth less than on good-shooting teams
4. **Comparing ratings across vastly different team contexts** → A player on a high-TMPlay% team will have a different baseline than on a low-TMPlay% team

## Related Concepts
- [[concept-floor-percentage]] — The scoring possession rate that underlies offensive rating
- [[concept-offensive-rebound-weight]] — How offensive rebounds are valued relative to plays
- [[concept-individual-defensive-rating]] — The defensive counterpart to this metric
- [[concept-performance-rating-system]] — A simpler weighted box-score alternative from S13
- [[concept-historical-offensive-ratings]] — Application of these formulas to history's greatest offenses

## Sources
- [S16, pp.343-349] — Complete derivation of all individual offensive rating formulas
