import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.game_report import build_report_prompt, analyze_game, get_calibration
from lib.halftime import build_halftime_prompt

print("=== Integration Test ===\n")

print("--- Test 1: U14 Club Post-Game Report ---")
box = {
    'your_team': 'Panthers',
    'your_pts': 42,
    'opp_team': 'Eagles',
    'opp_pts': 38,
    'quarters': {'Q1': 12, 'Q2': 8, 'Q3': 14, 'Q4': 8},
    'opp_quarters': {'Q1': 10, 'Q2': 12, 'Q3': 8, 'Q4': 8},
    'turnovers': 22,
    'opp_turnovers': 18,
    'rebounds': 28,
    'assists': 8,
    'fg_pct': 32.5,
    'top_players': [
        {'name': 'Marcus', 'points': 14, 'rebounds': 6, 'assists': 3},
        {'name': 'Jaylen', 'points': 10, 'rebounds': 4, 'assists': 2},
        {'name': 'Andre', 'points': 8, 'rebounds': 8, 'assists': 1},
    ],
}
analysis = analyze_game(box, 'u14_club')
prompt = build_report_prompt(box, 'u14_club')
print(f"Insights found: {len(analysis['insights'])}")
for ins in analysis['insights']:
    print(f"  [{ins['type']}] {ins['topic']}: {ins['message'][:100]}")
print(f"Prompt length: {len(prompt)} chars\n")

print("--- Test 2: Same Stats at U18 National ---")
analysis2 = analyze_game(box, 'u18_national')
print(f"Insights found: {len(analysis2['insights'])}")
for ins in analysis2['insights']:
    print(f"  [{ins['type']}] {ins['topic']}: {ins['message'][:100]}")

print("\n--- Test 3: Halftime Adjustments ---")
ht_prompt = build_halftime_prompt(
    observations=['their_3_is_hot', 'our_pnr_working', 'foul_trouble'],
    partial_box={'your_pts': 18, 'opp_pts': 22, 'turnovers': 12},
    game_plan={},
    level='u14_club',
)
print(f"Halftime prompt length: {len(ht_prompt)} chars")

print("\n--- Test 4: Calibration Sanity Check ---")
for level in ['u10', 'u14_club', 'u18_national', 'college', 'nba']:
    cal = get_calibration(level)
    print(f"  {level:14s}: PPG={cal['ppg']['mean']:5.1f}  Notable={cal['notable_individual_pts']}pts  TOV alert={cal['tov']['notable_high']:.0f}")

print("\n=== All tests passed ===")
