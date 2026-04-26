# IP Safety Audit — Pre-US Launch — 2026-04-23

Prior audit: `hallucination-audit-2026-04-22.md` (30-page sample, flagged 2 IP-violation pages).
This audit: wider pass before US public launch, where NBA-name exposure is highest-risk.

## Summary

- Pages scanned: 1,665 (`.md` in `wiki/`, excl. `_audit/` and `_pending/`)
- Pages with ≥1 programmatic flag: **340** (20.4%)
- Total term occurrences across files: 1,694
- Slug-tainted filenames (slug contains NBA team / player / coach / school / NBA prefix): **~38–41**
- Pages that MUST be scrubbed or excluded before US launch: ~340
  - **~41 irredeemable (EXCLUDE)**
  - **~300 body-scrub**
  - **2 auto-compiled (META-REGEN)**: `index.md`, `log.md`

Confidence HIGH on the 340 count (deterministic regex); MEDIUM on the EXCLUDE/SCRUB split (judgment calls on whether core value survives scrub).

## 1. Expanded denylist

Run case-insensitive, word-boundary, skipping citation contexts and content after `## Sources` / `## Notable Quotes` / `## Notes and Lineage` / `## References` / `## Bibliography` / `## Attribution` / `## Source material`.

### Team nicknames
Lakers, Celtics, Warriors, Bulls, Nets, Knicks, Spurs, Clippers, 76ers, Sixers, Rockets, Mavericks, Mavs, Grizzlies, Thunder, Kings, Suns, Hornets, Nuggets, Pelicans, Trail Blazers, Blazers, Timberwolves, Wolves, Jazz, Pistons, Pacers, Cavaliers, Cavs, Bucks, Hawks, Raptors, Wizards.

### Qualified team names (for FP-risky tokens)
Miami Heat, Orlando Magic, Los Angeles Lakers, Golden State Warriors, Boston Celtics, New York Knicks, Brooklyn Nets, Philadelphia 76ers, Chicago Bulls, Cleveland Cavaliers, Detroit Pistons, Indiana Pacers, Milwaukee Bucks, Atlanta Hawks, Charlotte Hornets, Toronto Raptors, Washington Wizards, Houston Rockets, Dallas Mavericks, Memphis Grizzlies, Oklahoma City Thunder, New Orleans Pelicans, San Antonio Spurs, Denver Nuggets, Minnesota Timberwolves, Portland Trail Blazers, Utah Jazz, Phoenix Suns, LA Clippers, Los Angeles Clippers, Sacramento Kings.

### NBA + notable college coaches (book authors included)
Popovich, Gregg Popovich, Steve Kerr, Erik Spoelstra, Spoelstra, Rick Pitino, Pitino, Phil Jackson, Red Auerbach, Auerbach, Pat Riley, Larry Brown, Doc Rivers, Mike D'Antoni, D'Antoni, Mike Krzyzewski, Coach K, Krzyzewski, Don Nelson, Chuck Daly, Lenny Wilkens, Wilkens, Jerry Sloan, Sloan, Jack Ramsay, Hubie Brown, Rick Carlisle, Carlisle, Nate McMillan, Tyronn Lue, Tom Thibodeau, Thibodeau, Brad Stevens, Frank Vogel, Billy Donovan, Quin Snyder, Monty Williams, Kenny Atkinson, Willie Green, Ime Udoka, Mark Jackson, Nick Nurse, Mike Budenholzer, Budenholzer, Terry Stotts, Stotts, Jeff Van Gundy, Stan Van Gundy, Van Gundy, Byron Scott, Rick Adelman, Adelman, Herb Brown, Jerry Krause, John Wooden, Wooden, Bob Knight, Bobby Knight, Roy Williams, Dean Smith, Jim Boeheim, Boeheim, Pete Carril, Carril, Jay Wright, Tom Izzo, Izzo, Mark Few, Jim Calhoun, Calhoun, John Calipari, Calipari, Rick Barnes, Bill Self, Lute Olson, Mike Montgomery, Geno Auriemma, Auriemma, Pat Summitt, Summitt, Tara VanDerveer, Kim Mulkey, Tony Bennett, Jamie Dixon, Sean Miller, Thad Matta, Bob Huggins, Fran McCaffery, Matt Painter, Alvin Gentry, Flip Saunders, Doug Collins, George Karl, Paul Silas.

### NBA players (Tier 1 greats + Basketball-on-Paper era)
LeBron, Kareem, Michael Jordan, Kobe Bryant, Shaquille, Magic Johnson, Larry Bird, Stephen Curry, Kevin Durant, Giannis, Luka, Jokic, Jayson Tatum, Joel Embiid, Kawhi, Scottie Pippen, Pippen, D'Angelo Russell, Austin Reaves, Rui Hachimura, Anthony Davis, Hakeem Olajuwon, Olajuwon, Tim Duncan, Wilt Chamberlain, Chamberlain, Bill Russell, Karl Malone, John Stockton, Stockton, Patrick Ewing, Ewing, David Robinson, Allen Iverson, Iverson, Dennis Rodman, Rodman, Charles Barkley, Barkley, Joe Dumars, Dumars, George Mikan, Mikan, Reggie Miller, Vince Carter, Lisa Leslie, Cynthia Cooper, Paul Pierce, Pierce, James Harden, Harden, Russell Westbrook, Westbrook, Dwyane Wade, Chris Paul, Blake Griffin, Isiah Thomas, Julius Erving, Oscar Robertson, Jerry West, Bob Cousy, Cousy, Bill Walton, Walton, Moses Malone, Elgin Baylor, Pete Maravich, Maravich, Rick Barry, Dave Cowens, John Havlicek, Havlicek, Dominique Wilkins, Gary Payton, Shawn Kemp, Alonzo Mourning, Mourning, Tim Hardaway, Hardaway, Penny Hardaway, Grant Hill, Chris Webber, Webber, Jason Kidd, Kidd, Steve Nash, Dirk Nowitzki, Nowitzki, Tony Parker, Manu Ginobili, Ginobili, Ray Allen, Kevin Garnett, Garnett, Dwight Howard, Paul George, Damian Lillard, Lillard, Kyrie Irving, Carmelo Anthony, Dennis Johnson, Mo Cheeks, Bobby Jones, Mark Eaton, Robert Parish, Parish, Kevin McHale, McHale, Adrian Dantley, Dantley, James Worthy, Worthy, Wes Unseld, Unseld, Bill Laimbeer, Laimbeer, Diana Taurasi, Taurasi, Maya Moore, Candace Parker, Sue Bird, Mashburn, Kukoc, Hornacek, Majerle, Dikembe Mutombo, Mutombo, Frank Layden.

### NCAA programs
UCLA, Duke, Kansas, Kentucky, Villanova, Princeton, Syracuse, North Carolina, UConn, Gonzaga, Arizona Wildcats, Indiana Hoosiers, Hoosiers, Michigan State, Tar Heels, Blue Devils, Jayhawks, Indiana University, University of North Carolina, Arizona State, Ohio State Buckeyes, Buckeyes, Louisville Cardinals, Memphis Tigers, Florida Gators, Gonzaga Bulldogs, Texas Longhorns, Longhorns, Georgetown Hoyas, Hoyas, Notre Dame, USC Trojans, Ohio State.

### League terms
NBA, WNBA (case-sensitive).

### City-as-team shorthand
Flagged only when followed within 40 chars by a basketball marker (offense, defense, team, coach, series, set, play, playbook, action, motion, press, rotation, scheme, roster, starters, rebuild, championship, playoff, finals, pnr, pick-and-roll): Charlotte, Detroit, Indiana, San Antonio, Oklahoma City, Miami, Orlando, Phoenix, Denver, Memphis, Houston, Dallas, Portland, Sacramento, Toronto, Minneapolis, Minnesota, Milwaukee, Atlanta, Cleveland, Brooklyn, Philadelphia, Utah, Golden State.

### Excluded by design (false-positive risk)
`Heat` alone, `Magic` alone (require qualified form); `Boston`, `Chicago`, `New York`, `Washington`, `LA`; `Bird` alone, `Kings` alone (require qualified form e.g. `Larry Bird`, `Sacramento Kings`).

## 2. Exhaustive scan — top 25 offenders

| Count | File | Category |
|-------|------|----------|
| 154 | index.md | META-REGEN |
| 73 | log.md | META-REGEN |
| 38 | concept-individual-win-loss-records.md | SCRUB |
| 31 | concept-offensive-rating-historical-trends.md | SCRUB |
| 30 | concept-historical-offensive-ratings.md | SCRUB |
| 30 | concept-defensive-rating-historical-trends.md | SCRUB |
| 29 | play-utah-jazz-ucla-action.md | **EXCLUDE** |
| 27 | concept-winning-streak-probability.md | SCRUB |
| 23 | source-basketball-playbook-2.md | SCRUB |
| 21 | concept-womens-basketball-offensive-efficiency.md | SCRUB |
| 21 | concept-coaching-defense-systems.md | SCRUB |
| 20 | concept-offensive-skill-curves.md | SCRUB |
| 19 | concept-womens-basketball-player-evaluation-analytics.md | SCRUB |
| 18 | source-winning-basketball-fundamentals.md | SCRUB |
| 18 | play-minnesota-hawk-combination.md | **EXCLUDE** |
| 17 | concept-scouting-philosophy.md | SCRUB |
| 16 | concept-floor-percentage.md | SCRUB |
| 14 | concept-uncorrelated-ratings.md | SCRUB |
| 14 | concept-possession-usage-team-balance.md | SCRUB |
| 13 | source-basketball-on-paper.md | SCRUB |
| 13 | concept-rule-changes-pace-efficiency.md | SCRUB |
| 13 | concept-possession-score-sheet.md | SCRUB |
| 13 | concept-pace-of-play.md | SCRUB |
| 13 | concept-loop-action-nba.md | **EXCLUDE** |
| 13 | concept-basketball-physical-anthropometric-characteristics.md | SCRUB |

### Term frequency (top across all files)

| Count | Term |
|-------|------|
| 670 | NBA |
| 214 | Herb Brown |
| 48 | Iverson |
| 30 | Jazz |
| 28 | Knicks |
| 27 | Lakers |
| 27 | UCLA |
| 23 | Jordan / Michael Jordan |
| 23 | Celtics |
| 20 | Wooden |
| 18 | Stockton |
| 16 | Rodman |
| 15 | Duncan |
| 14 | Kobe |
| 13 | Pippen |
| 13 | Olajuwon |
| 12 | Ewing |
| 10 | Pitino |
| 9 | Larry Bird |
| 8 | Karl Malone |
| 8 | Chamberlain |
| 8 | Popovich |
| 7 | Magic Johnson |
| 6 | Paul Pierce |
| 3 | Hubie Brown |

## 3. Slug-tainted files (EXCLUDE tier)

### 17 city/team-named plays
`play-celtics-post-drop`, `play-celtics-x-action`, `play-charlotte-pnr-back-screen`, `play-detroit-double-pnr-series`, `play-detroit-step-up-flare`, `play-hawks-zipper-cross-screen`, `play-indiana-box-high-x`, `play-knicks-zipper-baseline-triple`, `play-miami-pnr-baseline-screening`, `play-minnesota-hawk-combination`, `play-minnesota-triple-pnr`, `play-new-jersey-loop-action`, `play-orlando-angled-pnr`, `play-philadelphia-baseline-screening`, `play-san-antonio-early-offense-corner-fill`, `play-san-antonio-guard-through`, `play-utah-jazz-ucla-action`.

### 2 player-technique plays
`play-iverson-ram`, `play-piston-elevator`.

### 6 Herb-Brown-suffixed files
`basketball-glossary-herb-brown`, `coaching-traits-herb-brown`, `concept-defensive-philosophy-herb-brown`, `defensive-coaching-philosophy-herb-brown`, `defensive-practice-philosophy-herb-brown`, `source-herb-brown-defense`, plus `basketball-glossary-defensive-terms` (body attribution).

### 11 NBA-prefixed concept/drill files (sports-medicine ports)
`concept-nba-air-travel-performance`, `concept-nba-body-composition-trends`, `concept-nba-injury-epidemiology`, `concept-nba-long-distance-travel`, `concept-nba-medical-coverage`, `concept-nba-surgical-outcomes`, `concept-nba-travel-injury-mood`, `concept-screen-taxonomy-nba`, `concept-loop-action-nba`, `concept-game-preparation-nba`, `concept-basketball-competition-periodization-nba-fiba`, `drill-nba-shooting-drill-youth`.

### 4 shooting pages
`nba-shooting-confidence-rhythm`, `nba-shooting-error-correction`, `nba-shooting-mechanics-complete`, `nba-shooting-trigger-words`.

### 1 UCLA slug
`drill-ucla-movement`.

## 4. Hand-sampled prose leaks (15 tactical + 10 drill + 5 S&C)

See top-25 table for density; key examples:

- `concept-defensive-rating-historical-trends.md` — "Pat Riley New York Knicks teams of 1993 and 1994 were the greatest defensive teams in NBA history"; player-name tables.
- `concept-offensive-rating-historical-trends.md` — "Denver Nuggets 1982 … Alex English, Dan Issel, Kiki Vandeweghe"; "Chicago Bulls 1997 … Jordan, Pippen, Kukoc, Rodman".
- `concept-coaching-defense-systems.md` — "Phil Jackson, Pat Riley, Gregg Popovich, and Frank Layden/Jerry Sloan".
- `concept-individual-win-loss-records.md` — "Steve Kerr (63-19) … Scottie Pippen (55-22) on the 1996 Bulls".
- `concept-consistency-player-development.md` — "Magic Johnson, Michael Jordan, Larry Bird, Karl Malone".
- `concept-basketball-strength-training-methodology.md` — "developed by Lorena Torres Ronda (Philadelphia 76ers) and Francesco Cuzzolin".
- `drill-defending-middle-pnr.md` — "Dallas's game-7 zone against Miami in the 2011 NBA Finals is the model".
- `drill-breakdown-pivoting-circle.md` — `"Be quick, but not in a hurry" (John Wooden)`.
- `concept-basketball-cardiac-screening.md` — `## NBA Cardiac Screening Protocol`.
- `concept-achilles-tendon-basketball.md` — "61.1–68% of professional NBA players returning to play".

## 5. Gap analysis for `check-nba-terms.ts`

Current denylist does NOT contain: `Herb Brown`, `Rick Pitino` / `Pitino`, `Paul Pierce` / `Pierce`, `Popovich`, `Phil Jackson`, `Pat Riley`, `Jerry Sloan`, `John Wooden` / `Wooden`, `NBA`, `WNBA`, plus ~60 additional players/coaches enumerated in Section 1.

Additional enhancements:
- City-shorthand rule: `\b<City>\b` within 40 chars of a basketball marker word (offense/defense/PnR/set/play).
- Footer-whitelist: add a second-pass filter that skips the region after the first `## Sources` / `## Notable Quotes` / `## Notes and Lineage` header so legitimate `[Sn]` author attribution is not flagged.

## 6. Seed-page verdicts (go/no-go)

| # | Seed file | Verdict | Flagged term (if any) |
|---|---|---|---|
| 1 | `23-flare.md` | **CLEAN** | none |
| 2 | `play-baseline-swing.md` | **CLEAN** | none |
| 3 | `play-chin-series.md` | **CLEAN** | `## Sources` footer names "Pete Carril" (footer-allowed); body placeholder "Eddie the iconic scorer" — low polish, not IP |
| 4 | `concept-ball-you-man-flat-triangle.md` | **SCRUB** | Line 58 Related Concepts: "Herb Brown's system using similar shadow/tilt principles" |
| 5 | `concept-motion-offense-screening-rules.md` | **CLEAN** | none |
| 6 | `concept-back-screen-reads.md` | **SCRUB** | Line 75 Related Concepts: "Herb Brown's principles for defending back screens" |
| 7 | `drill-1v1-zigzag-defense.md` | **SCRUB** | Line 117 wikilink `[[defensive-practice-philosophy-herb-brown]]` — slug-level reference |
| 8 | `drill-2-on-1-trapping.md` | **SCRUB** | Line 46 Concepts Taught: "this drill is the core training vehicle for Herb Brown's trapping system" |
| 9 | `concept-anatomical-core-basketball.md` | **CLEAN** | "John Shackleton" only in `## Sources` footer — allowed |
| 10 | `concept-agility-training.md` | **CLEAN** | none |

## 7. Verdict

Ten-page seed: **CONDITIONAL GO** after 4 one-line scrubs. Applied 2026-04-23.

Do NOT ship any of the 41 slug-tainted files before a ground-up rewrite with anonymised identifiers.
Do NOT re-enable `index.md` as a public artifact until it is regenerated from scrubbed source pages.

Confidence HIGH on seed-page classification; MEDIUM on the 340 count; LOW on unknown-unknowns — a second-pass manual skim of the top 50 Tier B files is due diligence before declaring the scrub complete.

## 8. Independent verification (performed in main session)

- Herb Brown occurrences: `grep -roh "Herb Brown" .` → **214** matches across **98** files. Match HIGH.
- `concept-ball-you-man-flat-triangle.md:58`, `concept-back-screen-reads.md:75`, `drill-2-on-1-trapping.md:46`, `drill-1v1-zigzag-defense.md:117` — all 4 scrub targets confirmed verbatim via `sed`.
- Six "CLEAN" seed pages — grep of expanded denylist (pre-Sources only) returned zero hits on each.
- `check-nba-terms.ts` — grep returned zero matches for Herb Brown, Pitino, Paul Pierce, Popovich, Wooden, NBA, WNBA. Denylist gap confirmed.
