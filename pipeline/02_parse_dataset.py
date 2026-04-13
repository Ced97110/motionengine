from datasets import load_dataset
import json, os

ds = load_dataset("GEM/sportsett_basketball")

def safe_int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default

def parse_team(team_data):
    team = {
        'name': team_data.get('name', ''),
        'place': team_data.get('place', ''),
        'wins': safe_int(team_data.get('wins', 0)),
        'losses': safe_int(team_data.get('losses', 0)),
        'conference': team_data.get('conference', ''),
    }
    ls = team_data.get('line_score', {})
    game_ls = ls.get('game', {}) if isinstance(ls, dict) else {}
    team['total_pts'] = safe_int(game_ls.get('PTS', 0))
    team['fg'] = safe_int(game_ls.get('FGM', game_ls.get('FG', 0)))
    team['fga'] = safe_int(game_ls.get('FGA', 0))
    team['fg3'] = safe_int(game_ls.get('FG3M', game_ls.get('FG3', 0)))
    team['fg3a'] = safe_int(game_ls.get('FG3A', 0))
    team['ft'] = safe_int(game_ls.get('FTM', game_ls.get('FT', 0)))
    team['fta'] = safe_int(game_ls.get('FTA', 0))
    team['reb'] = safe_int(game_ls.get('TREB', game_ls.get('REB', 0)))
    team['ast'] = safe_int(game_ls.get('AST', 0))
    team['tov'] = safe_int(game_ls.get('TOV', 0))
    team['stl'] = safe_int(game_ls.get('STL', 0))
    team['blk'] = safe_int(game_ls.get('BLK', 0))

    quarters = {}
    for q in ['Q1', 'Q2', 'Q3', 'Q4']:
        q_data = ls.get(q, {}) if isinstance(ls, dict) else {}
        quarters[q] = safe_int(q_data.get('PTS', 0)) if isinstance(q_data, dict) else 0
    team['quarters'] = quarters

    players = []
    box = team_data.get('box_score', [])
    if isinstance(box, list):
        for p in box:
            if isinstance(p, dict):
                players.append({
                    'name': p.get('PLAYER_NAME', p.get('player', '')),
                    'minutes': safe_int(p.get('MIN', p.get('minutes', 0))),
                    'points': safe_int(p.get('PTS', p.get('points', 0))),
                    'rebounds': safe_int(p.get('REB', p.get('rebounds', 0))),
                    'assists': safe_int(p.get('AST', p.get('assists', 0))),
                    'steals': safe_int(p.get('STL', p.get('steals', 0))),
                    'blocks': safe_int(p.get('BLK', p.get('blocks', 0))),
                    'turnovers': safe_int(p.get('TOV', p.get('turnovers', 0))),
                })
    players.sort(key=lambda x: x['points'], reverse=True)
    team['players'] = players[:8]
    return team

def parse_record(record):
    game = record['game']
    teams = record['teams']
    context = {
        'date': f"{game.get('month', '')} {game.get('day', '')}, {game.get('year', '')}",
        'day': game.get('dayname', ''),
        'stadium': game.get('stadium', ''),
        'city': game.get('city', ''),
        'season': game.get('season', ''),
    }
    home = parse_team(teams.get('home', {}))
    away = parse_team(teams.get('vis', {}))
    winner = 'home' if home['total_pts'] > away['total_pts'] else 'away'
    margin = abs(home['total_pts'] - away['total_pts'])
    return {
        'id': record.get('sportsett_id', ''),
        'context': context,
        'home': home,
        'away': away,
        'winner': winner,
        'margin': margin,
        'narrative': record['target'],
        'linearized': record.get('linearized_input', ''),
    }

os.makedirs('data', exist_ok=True)
all_parsed = []
errors = 0
for split in ['train', 'validation', 'test']:
    for record in ds[split]:
        try:
            all_parsed.append(parse_record(record))
        except Exception as e:
            errors += 1
            if errors < 3:
                print(f"Error: {e}")

print(f"\nParsed {len(all_parsed)} records ({errors} errors)")
with open('data/parsed_games.json', 'w') as f:
    json.dump(all_parsed, f)

pts = [g['home']['total_pts'] for g in all_parsed] + [g['away']['total_pts'] for g in all_parsed]
tovs = [g['home']['tov'] for g in all_parsed] + [g['away']['tov'] for g in all_parsed]
margins = [g['margin'] for g in all_parsed]
print(f"PPG range: {min(pts)}-{max(pts)}, mean: {sum(pts)/len(pts):.1f}")
print(f"TOV range: {min(tovs)}-{max(tovs)}, mean: {sum(tovs)/len(tovs):.1f}")
print(f"Margin range: {min(margins)}-{max(margins)}, mean: {sum(margins)/len(margins):.1f}")
