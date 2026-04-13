import json, random

with open('data/parsed_games.json') as f:
    games = json.load(f)

def score_game(g):
    score = 0
    margin = g['margin']
    n = g['narrative'].lower()
    if margin <= 5: score += 3
    elif margin <= 10: score += 2
    elif margin >= 25: score += 1
    words = len(n.split())
    if words > 400: score += 2
    elif words > 250: score += 1
    if 'turnover' in n: score += 1
    if 'rebound' in n: score += 1
    if 'three-point' in n or '3-point' in n: score += 1
    if 'quarter' in n: score += 1
    if 'double-double' in n: score += 1
    if 'bench' in n: score += 1
    if 'defense' in n or 'defensive' in n: score += 2
    return score

scored = [(score_game(g), g) for g in games]
scored.sort(key=lambda x: -x[0])
top_200 = [g for _, g in scored[:200]]
random.seed(42)
selected = random.sample(top_200, 100)

examples = []
for g in selected:
    home, away = g['home'], g['away']
    winner = home if g['winner'] == 'home' else away
    loser = away if g['winner'] == 'home' else home

    box_input = {
        'your_team': {
            'name': winner['name'],
            'total_pts': winner['total_pts'],
            'quarters': winner['quarters'],
            'fg_pct': round(winner['fg']/max(1, winner.get('fga', 1))*100, 1),
            'three_pt': winner['fg3'],
            'rebounds': winner['reb'],
            'assists': winner['ast'],
            'turnovers': winner['tov'],
            'top_players': winner['players'][:5],
        },
        'opponent': {
            'name': loser['name'],
            'total_pts': loser['total_pts'],
            'quarters': loser['quarters'],
            'fg_pct': round(loser['fg']/max(1, loser.get('fga', 1))*100, 1),
            'turnovers': loser['tov'],
        },
        'result': 'W',
        'margin': g['margin'],
    }
    examples.append({
        'id': g['id'],
        'box_score_input': box_input,
        'original_narrative': g['narrative'],
        'coaching_narrative': '',
    })

with open('data/few_shot_examples.json', 'w') as f:
    json.dump(examples, f, indent=2)

close = sum(1 for g in selected if g['margin'] <= 5)
mid = sum(1 for g in selected if 5 < g['margin'] <= 15)
blow = sum(1 for g in selected if g['margin'] > 15)
print(f"Selected {len(examples)} examples")
print(f"Margin: close={close}, mid={mid}, blowout={blow}")
