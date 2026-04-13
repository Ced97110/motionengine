import json
import numpy as np

with open('data/parsed_games.json') as f:
    games = json.load(f)

nba_stats = {'ppg': [], 'fg_pct': [], 'fg3_pct': [], 'ft_pct': [],
             'reb': [], 'ast': [], 'tov': [], 'stl': [], 'blk': [], 'margin': []}

for g in games:
    for tk in ['home', 'away']:
        t = g[tk]
        nba_stats['ppg'].append(t['total_pts'])
        if t.get('fga', 0) > 0: nba_stats['fg_pct'].append(t['fg'] / t['fga'] * 100)
        if t.get('fg3a', 0) > 0: nba_stats['fg3_pct'].append(t['fg3'] / t['fg3a'] * 100)
        if t.get('fta', 0) > 0: nba_stats['ft_pct'].append(t['ft'] / t['fta'] * 100)
        nba_stats['reb'].append(t['reb'])
        nba_stats['ast'].append(t['ast'])
        nba_stats['tov'].append(t['tov'])
        nba_stats['stl'].append(t.get('stl', 0))
        nba_stats['blk'].append(t.get('blk', 0))
    nba_stats['margin'].append(g['margin'])

def stats_summary(arr):
    a = np.array([x for x in arr if x > 0])
    if len(a) == 0: return {'mean': 0, 'median': 0, 'p10': 0, 'p90': 0}
    return {'mean': round(float(np.mean(a)), 1), 'median': round(float(np.median(a)), 1),
            'p10': round(float(np.percentile(a, 10)), 1), 'p90': round(float(np.percentile(a, 90)), 1)}

nba_summary = {k: stats_summary(v) for k, v in nba_stats.items()}
print("NBA Averages:")
for k, v in nba_summary.items():
    print(f"  {k}: mean={v['mean']}, p10-p90={v['p10']}-{v['p90']}")

level_ratios = {
    'nba':       {'ppg': 1.00, 'fg_pct': 1.00, 'tov': 1.00, 'ast': 1.00, 'reb': 1.00},
    'college':   {'ppg': 0.65, 'fg_pct': 0.93, 'tov': 1.10, 'ast': 0.60, 'reb': 0.85},
    'u18_natl':  {'ppg': 0.55, 'fg_pct': 0.87, 'tov': 1.30, 'ast': 0.50, 'reb': 0.80},
    'u18_club':  {'ppg': 0.50, 'fg_pct': 0.82, 'tov': 1.50, 'ast': 0.45, 'reb': 0.75},
    'u16_natl':  {'ppg': 0.45, 'fg_pct': 0.80, 'tov': 1.60, 'ast': 0.40, 'reb': 0.70},
    'u16_club':  {'ppg': 0.40, 'fg_pct': 0.75, 'tov': 1.80, 'ast': 0.35, 'reb': 0.65},
    'u14_natl':  {'ppg': 0.38, 'fg_pct': 0.72, 'tov': 1.90, 'ast': 0.30, 'reb': 0.60},
    'u14_club':  {'ppg': 0.35, 'fg_pct': 0.68, 'tov': 2.00, 'ast': 0.25, 'reb': 0.55},
    'u12':       {'ppg': 0.28, 'fg_pct': 0.60, 'tov': 2.30, 'ast': 0.20, 'reb': 0.50},
    'u10':       {'ppg': 0.20, 'fg_pct': 0.50, 'tov': 2.80, 'ast': 0.15, 'reb': 0.45},
    'rec':       {'ppg': 0.30, 'fg_pct': 0.55, 'tov': 2.50, 'ast': 0.15, 'reb': 0.50},
}

calibration = {}
for level, r in level_ratios.items():
    calibration[level] = {
        'ppg': {'mean': round(nba_summary['ppg']['mean']*r['ppg'], 1),
                'low': round(nba_summary['ppg']['p10']*r['ppg'], 1),
                'high': round(nba_summary['ppg']['p90']*r['ppg'], 1)},
        'fg_pct': {'mean': round(nba_summary['fg_pct']['mean']*r['fg_pct'], 1),
                   'low': round(nba_summary['fg_pct']['p10']*r['fg_pct'], 1),
                   'high': round(nba_summary['fg_pct']['p90']*r['fg_pct'], 1)},
        'tov': {'mean': round(nba_summary['tov']['mean']*r['tov'], 1),
                'notable_high': round(nba_summary['tov']['p90']*r['tov'], 1)},
        'ast': {'mean': round(nba_summary['ast']['mean']*r['ast'], 1)},
        'reb': {'mean': round(nba_summary['reb']['mean']*r['reb'], 1)},
        'notable_individual_pts': round(nba_summary['ppg']['mean']*r['ppg']*0.35),
    }

with open('data/stat_calibration.json', 'w') as f:
    json.dump(calibration, f, indent=2)

print("\nCalibration:")
for level, cal in calibration.items():
    print(f"  {level:12s}: PPG={cal['ppg']['mean']:5.1f}  FG%={cal['fg_pct']['mean']:4.1f}  TOV={cal['tov']['mean']:4.1f}  Notable={cal['notable_individual_pts']}+pts")
