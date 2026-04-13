import json

with open('data/parsed_games.json') as f:
    games = json.load(f)

patterns = {
    'mentions_turnovers': 0, 'mentions_rebounds': 0, 'mentions_shooting_pct': 0,
    'mentions_three_pointers': 0, 'mentions_double_double': 0, 'mentions_streak': 0,
    'mentions_quarter_run': 0, 'mentions_bench': 0, 'mentions_injury': 0, 'mentions_record': 0,
}
high_scorer_threshold = []
narrative_lengths = []

for g in games:
    n = g['narrative'].lower()
    narrative_lengths.append(len(n.split()))
    if 'turnover' in n: patterns['mentions_turnovers'] += 1
    if 'rebound' in n: patterns['mentions_rebounds'] += 1
    if 'percent' in n or 'shooting' in n: patterns['mentions_shooting_pct'] += 1
    if 'three-point' in n or 'three pointer' in n or '3-point' in n: patterns['mentions_three_pointers'] += 1
    if 'double-double' in n or 'double double' in n: patterns['mentions_double_double'] += 1
    if 'streak' in n or 'consecutive' in n or 'straight' in n: patterns['mentions_streak'] += 1
    if 'quarter' in n and ('run' in n or 'outscored' in n): patterns['mentions_quarter_run'] += 1
    if 'bench' in n or 'came off' in n or 'reserve' in n: patterns['mentions_bench'] += 1
    if 'injury' in n or 'injured' in n or 'missed' in n or 'surgery' in n: patterns['mentions_injury'] += 1
    if 'record' in n and ('season' in n or 'career' in n): patterns['mentions_record'] += 1
    for team_key in ['home', 'away']:
        if g[team_key]['players']:
            top = g[team_key]['players'][0]
            pname = top['name'].split()[-1].lower() if top['name'] else ''
            if pname and pname in n:
                high_scorer_threshold.append(top['points'])

total = len(games)
print(f"Total games: {total}")
print(f"Avg narrative length: {sum(narrative_lengths)/len(narrative_lengths):.0f} words")
for k, v in sorted(patterns.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v/total*100:.1f}%")

rules = {
    'narrative_avg_words': round(sum(narrative_lengths)/len(narrative_lengths)),
    'top_patterns': {k: round(v/total*100, 1) for k, v in sorted(patterns.items(), key=lambda x: -x[1])},
    'high_scorer_mention_threshold': round(sum(high_scorer_threshold)/len(high_scorer_threshold)) if high_scorer_threshold else 20,
}
with open('data/narrative_rules.json', 'w') as f:
    json.dump(rules, f, indent=2)
print(f"\nHigh scorer threshold: {rules['high_scorer_mention_threshold']}+ pts")
print("Saved data/narrative_rules.json")
