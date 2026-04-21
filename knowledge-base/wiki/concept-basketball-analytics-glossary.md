---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, possession, offense, defense, evaluation]
source_count: 1
last_updated: 2026-04-11
---

# Basketball Analytics Glossary (Dean Oliver Framework)

## Summary
Dean Oliver's *Basketball on Paper* introduced a rigorous set of formal definitions that underpin modern basketball analytics. These terms are not interchangeable with their casual usage — each has a precise technical meaning that enables consistent statistical analysis across teams, eras, and players. Understanding these definitions is a prerequisite for interpreting any possession-based basketball analysis [S16, pp.367-368].

The most important distinction in the framework is between a **possession** (one team's entire tenure with the ball) and a **play** (a single shot attempt or turnover within a possession). A missed shot followed by an offensive rebound and a made basket = 2 plays, 1 possession. This distinction drives how floor percentage and scoring possessions are calculated.

## Key Definitions

### Possession
> "The period of time between when one team gains control of the ball and when the opposing team gains control of the ball."

A possession ends when the other team gets the ball — either via turnover, defensive rebound, or after a made basket. Contrast with **Play**. [S16, p.368]

### Play
> "The period between when one team gains control of the ball and when they lose control of the ball, either when the opposing team gains control or when a shot goes up."

Example: A missed shot + offensive rebound + made follow-up = **2 plays, 1 possession**. [S16, p.368]

### Scoring Possession
A scoring possession occurs when a team scores at least one point. An individual scoring possession is awarded when a player contributes to a team scoring possession (partial scoring possessions are awarded when multiple players contribute). [S16, p.368]

### Floor Percentage
> "The fraction of a team's or individual's possessions on which there is a scoring possession."

This is Dean Oliver's master offensive efficiency metric — distinct from field goal percentage because it accounts for the cost of turnovers and the value of free throws. Individual floor percentage averages approximately 40–55% for quality players. [S16, p.367]

### Play Percentage
> "The fraction of a team's plays on which it produces a scoring possession."

Related to floor percentage but measured at the play level rather than possession level. [S16, p.368]

### Field Percentage
> "The percentage of times a team scores a basket on possessions where no free throws are awarded."

Illustrates how well teams score without drawing fouls. Distinct from field goal percentage. [S16, p.367]

### Offensive Rating
> "Points scored (by a team) or produced (by an individual) per hundred possessions."

The primary offensive efficiency metric. Team offensive ratings for elite offenses typically fall in the range of 110–120+; league average is approximately 100–110 depending on era. [S16, p.367]

### Defensive Rating
> "Points allowed (by a team or individual) per hundred possessions."

The lower the defensive rating, the better the defense. The gap between a team's offensive and defensive ratings predicts its winning percentage. [S16, p.367]

### Rating (Points Per 100 Possessions)
> "A rating is typically meant to convey how many points are scored or allowed per hundred possessions. Points scored (or produced) per hundred possessions is an 'offensive rating.' Points allowed per hundred possessions is a 'defensive rating.'" [S16, p.368]

### Points Produced (Individual)
In an individual context, points produced represents the number of points a player generates through all offensive contributions, **including assists, field goals, free throws, and offensive rebounds** — not just the points directly credited to them by the official scorer. [S16, p.368]

### Percentage of Team Possessions
> "A representation of how often an individual uses a team possession. With five players on the court, an average value of the percentage of team possessions would be one-fifth or 20 percent."

Used to weight individual offensive ratings — a player who uses 30% of possessions and has a high offensive rating is more valuable than one who uses 15% with the same rating. [S16, p.368]

### Defensive Stop
> "A stop occurs when a defense regains the ball without allowing the opponent a scoring possession."

The individual defensive equivalent of a scoring possession — the primary unit for calculating individual defensive ratings. [S16, p.367]

### Bell Curve Winning Percentage
Winning percentage estimated from a team's **average** values of points scored and allowed AND the **variability** of points scored and allowed. Bell curve percentages can also be calculated with a team's offensive and defensive ratings. More accurate than the simpler Pythagorean formula. [S16, p.367]

### Pythagorean Winning Percentage
Winning percentage estimated from a team's average values of points scored and allowed only (no variability component). Borrowed from Bill James's baseball sabermetrics. [S16, p.368]

### Uncorrelated Ratings
Points per 100 possession ratings adjusted by how much teams play up or down to their opponents. Teams that do not play up or down will have the same uncorrelated and regular ratings. [S16, p.368]

### Assist
> "As judged by official scorers, an assist is awarded to a player making a pass to a teammate leading directly to a made field goal."

Oliver's analysis finds each assist implies approximately 0.0803 additional turnovers, after controlling for other variables — the price of ball movement. [S16, p.365, p.367]

### Pick-and-Roll
> "A type of play where one offensive player sets a pick on the defender covering the ball handler, then moves away (the 'roll') to try to make the defender confused about who to cover." [S16, p.368]

### Post
> "The post is a vaguely defined area within five to ten feet of the basket where offensive players (usually big men) try to establish position so that, when they get the ball, they can score. 'Posting up' is when a player is trying to establish such position. Synonyms: box, block." [S16, p.368]

### Garbage Time
> "That period near the end of certain games when the victorious team is evident and second-string players are in the game."

Oliver discusses garbage time as a source of statistical distortion in player evaluation — stars accumulate stats in blowouts. Also referred to as "shirking." [S16, p.367]

### Man-to-Man Defense
> "A type of defense where each player on the defense is primarily responsible for preventing a single opposing player from scoring. This is in contrast to a zone defense." [S16, p.367]

### Zone Defense
> "A type of defense where each defender is primarily responsible for preventing any player in a given zone of the court from scoring." [S16, p.368]

### Standard Deviation
> "A statistic that represents how varied a group of numbers are." [S16, p.368]

### Variance
> "The standard deviation multiplied by itself. Another way to represent how much variation exists in a group of numbers." [S16, p.368]

### Covariance
> "A statistic that represents how two sets of numbers change together." [S16, p.367]

## Key Principles for Coaches
1. **Use possession-based rates, not counting stats** — A player who scores 20 points in 25 possessions is less efficient than one who scores 18 in 16 possessions.
2. **Distinguish possessions from plays** — Offensive rebounding extends plays without ending possessions; this is why it is so valuable.
3. **Defensive ability is system-dependent** — "It does appear to be true that defensive ability is strongly a function of defensive system" [S16, p.363]; be cautious comparing defensive stats across teams.
4. **All four factors matter** — Shooting efficiency, offensive rebounding, turnovers, and free throw drawing are independent levers; improving any one improves the offense.
5. **Context shapes statistics** — "Even though the math may be exact, how you ask the question or set up the solution is where some subjectivity is introduced" [S16, p.366].

## Common Mistakes
1. **Treating field goal % as the same as floor % or scoring possession rate** → Floor % accounts for turnovers and free throws that pure FG% ignores.
2. **Comparing raw stats across eras with different paces** → Always convert to per-100-possession rates before comparing.
3. **Transferring defensive player grades across teams** → A great defender on a great defensive team may appear merely average when moved to a poor defensive team.
4. **Treating a play as a possession** → A missed shot followed by an offensive rebound is two plays but one possession; equating them double-counts offensive rebounding.

## Related Concepts
- [[concept-basketball-four-factors]] — The four factors (shooting, ORB%, TOV%, FT rate) are derived from the possession framework defined here
- [[concept-basketball-offensive-defensive-ratings]] — Offensive and defensive ratings are the primary outputs of possession-based analysis
- [[concept-performance-rating-system]] — The PRS from S13 takes a different approach to per-player production measurement
- [[concept-basketball-performance-indicators-winning]] — Evidence-based winning performance indicators from S12 use related analytical concepts

## Sources
- [S16, pp.367-368] — Complete glossary definitions
- [S16, p.363] — Individual defensive formula limitations; system-dependence of defense
- [S16, p.366] — Subjectivity in statistical analysis acknowledged
