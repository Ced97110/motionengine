# SportsSettBasketball Integration — Implementation Spec

> This document is a self-contained implementation guide. Read it top to bottom. Execute each step. Verify before moving to the next. The goal: a working pipeline that transforms 6,150 NBA game records into a coaching intelligence layer our AI uses to generate game reports, halftime insights, and post-game analysis calibrated to any level.

## Goal

Turn the SportsSettBasketball dataset into three usable assets:
1. **Few-shot example library** — 100 curated game narratives rewritten in coaching tone
2. **Stat calibration tables** — reference ranges for every competition level (U10→Pro)
3. **Report generation pipeline** — function that takes a box score + level → returns coaching analysis

When complete, a coach can input a box score and get back a level-appropriate coaching narrative grounded in real NBA analytical patterns.

## Pipeline Overview

Steps 1-5: Data processing (no API calls)
Step 6: Narrative rewrites via Claude API (~$3)
Steps 7-8: Production library code
Step 9: Integration tests
Step 10: Export to wiki format

## File Structure (when complete)

```
project/
├── scripts/
│   ├── 01_download_dataset.py
│   ├── 02_parse_dataset.py
│   ├── 03_analyze_narratives.py
│   ├── 04_build_calibration.py
│   ├── 05_curate_examples.py
│   ├── 06_rewrite_narratives.py
│   ├── 09_integration_test.py
│   └── 10_export_to_wiki.py
├── lib/
│   ├── game_report.py          ← Production function: box score → coaching analysis
│   └── halftime.py             ← Production function: observations → 3 adjustments
├── data/
│   ├── sample_record.json
│   ├── parsed_games.json
│   ├── narrative_rules.json
│   ├── stat_calibration.json
│   ├── few_shot_examples.json
│   └── rewrite_prompts.json
└── knowledge-base/wiki/
    ├── reference/
    │   ├── stat-calibration-by-level.md
    │   └── narrative-analysis-rules.md
    └── training/
        └── game-narrative-examples.md
```

Full implementation details for all 10 steps preserved in the original spec delivered by the user.
