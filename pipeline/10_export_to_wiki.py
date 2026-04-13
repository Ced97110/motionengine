import json, os

WIKI_DIR = 'knowledge-base/wiki'
os.makedirs(os.path.join(WIKI_DIR, 'reference'), exist_ok=True)
os.makedirs(os.path.join(WIKI_DIR, 'training'), exist_ok=True)

with open('data/stat_calibration.json') as f:
    cal = json.load(f)

md = """---
type: reference
last_updated: auto
---
# Stat Calibration by Competition Level

This table defines expected statistical ranges at each competition level.
Used by the AI to calibrate game analysis -- what is "notable" at U14 differs from U18.

| Level | PPG | FG% | TOV/game | Notable scorer | AST | REB |
|-------|-----|-----|----------|---------------|-----|-----|
"""
for level, data in cal.items():
    md += f"| {level} | {data['ppg']['mean']} | {data['fg_pct']['mean']}% | {data['tov']['mean']} | {data['notable_individual_pts']}+ pts | {data['ast']['mean']} | {data['reb']['mean']} |\n"
md += "\nSource: Computed from SportsSettBasketball dataset (6,150 NBA games) with level ratios estimated from coaching knowledge.\n"

with open(os.path.join(WIKI_DIR, 'reference', 'stat-calibration-by-level.md'), 'w') as f:
    f.write(md)

with open('data/narrative_rules.json') as f:
    rules = json.load(f)

rules_md = """---
type: reference
last_updated: auto
---
# Game Narrative Analysis Rules

Rules extracted from analyzing 6,150 human-written NBA game narratives.

## What narratives focus on

"""
for pattern, pct in rules['top_patterns'].items():
    rules_md += f"- **{pattern.replace('mentions_', '')}**: {pct}%\n"

rules_md += f"""
## Thresholds

- High scorer mention threshold: **{rules['high_scorer_mention_threshold']}+ points**
- Average narrative length: **{rules['narrative_avg_words']} words**

## Application

When generating coaching analysis, prioritize topics in order of how frequently human analysts mention them. Lead with rebounds, shooting, and turnovers when notable.
"""

with open(os.path.join(WIKI_DIR, 'reference', 'narrative-analysis-rules.md'), 'w') as f:
    f.write(rules_md)

with open('data/few_shot_examples.json') as f:
    examples = json.load(f)

index_md = f"""---
type: training
last_updated: auto
---
# Game Report Few-Shot Examples

{len(examples)} curated NBA game reports used as few-shot context when generating post-game and halftime reports.

## Usage

The report generation function (`lib/game_report.py`) selects the 3 most relevant examples based on game margin similarity and includes them in the Claude API prompt.
"""

with open(os.path.join(WIKI_DIR, 'training', 'game-narrative-examples.md'), 'w') as f:
    f.write(index_md)

print("Exported 3 wiki files:")
print(f"  {WIKI_DIR}/reference/stat-calibration-by-level.md")
print(f"  {WIKI_DIR}/reference/narrative-analysis-rules.md")
print(f"  {WIKI_DIR}/training/game-narrative-examples.md")
