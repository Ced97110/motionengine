"""Post-game report generation — box score + level → coaching analysis prompt."""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

with open(os.path.join(DATA_DIR, 'stat_calibration.json')) as f:
    CALIBRATION = json.load(f)

with open(os.path.join(DATA_DIR, 'narrative_rules.json')) as f:
    RULES = json.load(f)

with open(os.path.join(DATA_DIR, 'few_shot_examples.json')) as f:
    EXAMPLES = json.load(f)


LEVEL_MAP = {
    'u10': 'u10', 'u12': 'u12',
    'u14_club': 'u14_club', 'u14_national': 'u14_natl',
    'u16_club': 'u16_club', 'u16_national': 'u16_natl',
    'u18_club': 'u18_club', 'u18_national': 'u18_natl',
    'college': 'college', 'professional': 'nba', 'nba': 'nba',
    'recreational': 'rec',
}


def get_calibration(level: str) -> dict:
    """Get stat calibration for a competition level."""
    key = LEVEL_MAP.get(level, 'u14_club')
    return CALIBRATION.get(key, CALIBRATION['u14_club'])


def select_few_shot_examples(box_score: dict, n: int = 3) -> list:
    """Select the most relevant few-shot examples for this game by margin similarity."""
    yt = box_score.get('your_team')
    yt_obj = yt if isinstance(yt, dict) else {}
    opp = box_score.get('opponent')
    opp_obj = opp if isinstance(opp, dict) else {}
    your_pts = box_score.get('your_pts', yt_obj.get('total_pts', 0))
    opp_pts = box_score.get('opp_pts', opp_obj.get('total_pts', 0))
    margin = abs(your_pts - opp_pts)

    scored = []
    for ex in EXAMPLES:
        narrative = ex.get('coaching_narrative') or ex.get('original_narrative', '')
        if not narrative:
            continue
        ex_margin = ex['box_score_input']['margin']
        similarity = 1.0 / (1.0 + abs(margin - ex_margin))
        scored.append((similarity, ex))

    scored.sort(key=lambda x: -x[0])
    return [ex for _, ex in scored[:n]]


def analyze_game(box_score: dict, level: str) -> dict:
    """Identify coaching insights by comparing stats to level calibration."""
    cal = get_calibration(level)
    insights = []

    your_pts = box_score.get('your_pts', 0)
    turnovers = box_score.get('turnovers', 0)
    top_players = box_score.get('top_players', [])
    quarters = box_score.get('quarters', {})
    opp_quarters = box_score.get('opp_quarters', {})

    # Turnover concern
    if turnovers > cal['tov']['notable_high']:
        insights.append({
            'type': 'concern',
            'topic': 'turnovers',
            'message': (
                f"Turnovers ({turnovers}) above the threshold for this level "
                f"({cal['tov']['notable_high']:.0f}). Ball security should be a practice focus."
            ),
            'priority': 1,
        })

    # Scoring concern
    if your_pts > 0 and your_pts < cal['ppg']['mean'] * 0.8:
        insights.append({
            'type': 'concern',
            'topic': 'scoring',
            'message': (
                f"Scoring ({your_pts}) below average for this level "
                f"({cal['ppg']['mean']:.0f}). Review shot selection and offensive execution."
            ),
            'priority': 2,
        })

    # Individual standout
    for p in top_players:
        if p.get('points', 0) >= cal['notable_individual_pts']:
            insights.append({
                'type': 'highlight',
                'topic': 'individual',
                'message': (
                    f"{p['name']} led with {p['points']} points — a standout performance "
                    f"at this level (threshold: {cal['notable_individual_pts']}+)."
                ),
                'priority': 3,
            })
            break

    # Quarter momentum
    if quarters and opp_quarters:
        for q in ['Q1', 'Q2', 'Q3', 'Q4']:
            diff = quarters.get(q, 0) - opp_quarters.get(q, 0)
            if diff >= 10:
                insights.append({
                    'type': 'highlight',
                    'topic': 'momentum',
                    'message': f"Dominant {q} (outscored by {diff}). Identify what worked and replicate it.",
                    'priority': 4,
                })
            elif diff <= -10:
                insights.append({
                    'type': 'concern',
                    'topic': 'momentum',
                    'message': f"Lost {q} badly (outscored by {abs(diff)}). Review what broke down.",
                    'priority': 4,
                })

    insights.sort(key=lambda x: x['priority'])
    return {'insights': insights, 'calibration': cal}


def build_report_prompt(box_score: dict, level: str) -> str:
    """Build the full Claude prompt for a post-game coaching report."""
    analysis = analyze_game(box_score, level)
    examples = select_few_shot_examples(box_score, n=3)
    cal = analysis['calibration']

    few_shot = ""
    for i, ex in enumerate(examples):
        narrative = ex.get('coaching_narrative') or ex.get('original_narrative', '')
        few_shot += f"\n--- Example {i+1} ---\n"
        few_shot += f"Box score: {json.dumps(ex['box_score_input'])}\n"
        few_shot += f"Analysis: {narrative[:500]}\n"

    prompt = f"""You are a basketball coaching analyst generating a post-game report.

COMPETITION LEVEL: {level}
At this level, typical stats are:
- Team PPG: {cal['ppg']['mean']}
- FG%: {cal['fg_pct']['mean']}%
- Turnovers/game: {cal['tov']['mean']}
- A notable individual performance is {cal['notable_individual_pts']}+ points

PRE-ANALYZED INSIGHTS:
{json.dumps(analysis['insights'], indent=2)}

EXAMPLES OF COACHING ANALYSIS:
{few_shot}

NOW GENERATE A COACHING ANALYSIS FOR THIS GAME:
{json.dumps(box_score, indent=2)}

RULES:
- Address the coach directly ("Your team...")
- Lead with the #1 coaching insight
- 150-200 words maximum
- 2-3 actionable takeaways for next practice
- Reference specific players by name
- Calibrate to the competition level (don't reference NBA concepts to a U12 coach)
- End with one specific drill or focus area for next practice
- No cliches. Direct and analytical.

COACHING ANALYSIS:"""
    return prompt


__all__ = ['build_report_prompt', 'analyze_game', 'get_calibration', 'select_few_shot_examples']
