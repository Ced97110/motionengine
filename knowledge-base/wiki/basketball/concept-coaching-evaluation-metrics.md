---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, coaching, evaluation, winning-percentage, expectations, statistics]
source_count: 1
last_updated: 2026-04-11
---

# Coaching Evaluation Metrics

## Summary
Evaluating a coach's contribution to team success requires separating actual win-loss performance from the expectations set by roster talent. Dean Oliver presents three distinct statistical methods for doing this, each comparing a team's *actual* winning percentage to an *expected* winning percentage derived from measurable factors. The gap between actual and expected performance — sustained over many games — is taken as evidence of coaching impact. [S16, pp.223-229]

All three methods identify some of the same coaches at the top and bottom, providing qualitative validation, but they also disagree substantially on individual coaches, highlighting the fundamental challenge: results depend entirely on the model chosen to define expectations.

## When to Use
- When front offices want to evaluate coaching effectiveness objectively
- When separating coaching contribution from player talent during personnel decisions
- When benchmarking a coach's performance after a roster overhaul
- As one data input alongside subjective evaluation — not as the sole criterion

## Key Principles

### Method 1: Field Goal Percentage Forecast
1. Set expectation using the formula: `Expected Win% = (FG% − DFG%) × 5 + 0.500` [S16, p.223]
2. Coaches winning more than expected: Phil Jackson (+0.103/season), Chuck Daly (+0.097), Lenny Wilkens (+0.088), Paul Westphal (+0.110) topped this list (min. 165 games)
3. Coaches losing more than expected: Sidney Lowe (−0.135), Jim Lynam (−0.110), Brian Winters (−0.109)
4. **Limitation**: Uses current-season statistics as the expectation baseline — these are performance measures, not independent talent measures [S16, p.225]
5. **Estimated coaching impact**: ±3–5% of annual win-loss record

### Method 2: Bell Curve Model
1. Uses the probabilistic bell curve model (from Ch.11 of the book) to set expected win%
2. Top coaches: Paul Westphal (+0.037), Del Harris (+0.036), Larry Bird (+0.030), Jeff Van Gundy (+0.028)
3. **Key inconsistency**: Jeff Van Gundy ranks #4 here but #36 by the FG% method — the same coach can be rated best or below-average depending on the model [S16, p.225]
4. Rick Pitino appears as a top-10 coach by Method 1 but a bottom-7 coach by Method 2
5. **Estimated coaching impact**: ±1–2% of annual win-loss record (smaller than Method 1 because model predicts win% more accurately, leaving less residual variance to attribute to coaching)

### Method 3: Pull of Parity (Prior Season + Regression to Mean)
1. Uses prior season's winning percentage plus regression-to-mean adjustment (from Ch.9) to set expectations
2. A coach taking over a 20% win team would be expected to reach ~31% — doing less is failure; exceeding it is success
3. Rankings weighted by *statistical probability* — how likely is this outcome by chance?
4. Top coaches: Phil Jackson (probability of result by luck: 1.8×10⁻¹⁴), Jerry Sloan (7.06×10⁻¹³), George Karl (4.21×10⁻¹¹), Pat Riley (2.04×10⁻⁹), Gregg Popovich (2.11×10⁻⁵) [S16, p.226]
5. Worst coaches: Tim Floyd (1.000 chance result was luck), Sidney Lowe (0.999), Wes Unseld (0.994)
6. **Advantage over other methods**: Equally rewards coaches who make bad teams average AND coaches who keep great teams great. Weights both magnitude and duration of performance vs. expectations [S16, p.227]
7. **Known flaw**: Tim Floyd ranked as worst coach because he inherited the 62-20 Bulls (Jordan era) then lost Jordan's talent — expectations were unrealistically set by a team he never coached at full strength [S16, p.227]

## Common Mistakes
1. **Using one model as definitive** → Always compare multiple methods; disagreements reveal the limits of the approach
2. **Ignoring roster discontinuity** → Phil Jackson's rating was inflated by Jordan's mid-season return in 1996; Floyd's was deflated by Jordan's departure; context matters [S16, p.227]
3. **Conflating coaching with scouting** → When coaches exceed expectations because they inherited superior scouts or strong player chemistry, they receive more credit than deserved [S16, p.228]
4. **Treating player talent as stable** → The ideal expectation measure would account for injuries, aging, and role changes, but this is practically very difficult [S16, p.228]

## Factors That Affect Winning Beyond Player Talent
Oliver lists eleven factors a coaching evaluation model should ideally control for [S16, p.228]:
1. Scouting quality
2. Play calling
3. Time-out strategy
4. Practice strategy
5. Strength of schedule
6. Players playing different positions or roles
7. Players' familiarity with each other (chemistry)
8. Player motivation/compensation satisfaction
9. Nutrition and strength training
10. Random variance
11. Biorhythms/health factors

## Related Concepts
- [[concept-time-out-strategy-value]] — Time-outs are one of the coaching levers that models fail to capture
- [[concept-offensive-skill-curves]] — Player efficiency curves help separate talent from coaching contribution
- [[concept-individual-win-loss-records]] — The next step: attributing wins to individual players rather than coaches
- [[performance-rating-system]] — Another analytical framework for evaluating player/team contributions

## Sources
- [S16, pp.223-229] — Primary presentation of all three methods with tables and analysis
