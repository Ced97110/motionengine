"""Statistical anomaly detection for game stats.

Uses z-scores computed against level-calibrated distributions from
SportsSettBasketball. Flags stats that are unusually high or low
for the competition level.
"""

import json
import os
from typing import Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "..", "data")

with open(os.path.join(DATA_DIR, "stat_calibration.json")) as f:
    _CALIBRATION = json.load(f)


# Approximate standard deviation as (p90 - p10) / 2.56
# (normal distribution: p10 to p90 spans ~2.56 sigma)
def _std_from_percentiles(p10: float, p90: float) -> float:
    return max(0.1, (p90 - p10) / 2.56)


def _z_score(value: float, mean: float, std: float) -> float:
    if std == 0:
        return 0.0
    return (value - mean) / std


def detect_anomalies(
    box_score: Dict,
    level: str,
    threshold_sd: float = 1.5,
) -> List[Dict]:
    """Identify stats that deviate significantly from level-typical ranges.

    Returns a list of anomaly records with type (high/low), stat, z-score,
    and a human-readable message. Sorted by absolute z-score descending.
    """
    from ..game_report import get_calibration

    cal = get_calibration(level)
    anomalies = []

    stats_to_check = [
        ("ppg", "your_pts", "scoring"),
        ("fg_pct", "fg_pct", "shooting"),
        ("tov", "turnovers", "turnovers"),
        ("ast", "assists", "ball movement"),
        ("reb", "rebounds", "rebounding"),
    ]

    for cal_key, box_key, topic in stats_to_check:
        if cal_key not in cal or box_key not in box_score:
            continue
        value = box_score[box_key]
        if not isinstance(value, (int, float)) or value == 0:
            continue

        cal_stat = cal[cal_key]
        mean = cal_stat.get("mean", 0)
        low = cal_stat.get("low", mean * 0.7)
        high = cal_stat.get("high", mean * 1.3)
        std = _std_from_percentiles(low, high)
        z = _z_score(value, mean, std)

        if abs(z) >= threshold_sd:
            direction = "high" if z > 0 else "low"
            # For turnovers, high is bad; for others, high is good
            is_concern = (topic == "turnovers" and direction == "high") or (
                topic != "turnovers" and direction == "low"
            )
            anomalies.append(
                {
                    "type": "concern" if is_concern else "highlight",
                    "stat": topic,
                    "value": round(value, 1),
                    "level_mean": mean,
                    "z_score": round(z, 2),
                    "direction": direction,
                    "message": (
                        f"{topic.capitalize()} ({value}) is {abs(z):.1f} standard "
                        f"deviations {direction} of the {level} mean ({mean})."
                    ),
                }
            )

    anomalies.sort(key=lambda x: -abs(x["z_score"]))
    return anomalies


def player_anomaly(
    player_stats: Dict,
    historical_avg: Dict,
    historical_std: Dict,
    threshold_sd: float = 1.5,
) -> List[Dict]:
    """Detect anomalies in a single player's performance vs their historical norm.

    historical_avg: {'points': 12.3, 'rebounds': 5.8, ...}
    historical_std: {'points': 3.2, 'rebounds': 1.5, ...}
    """
    anomalies = []
    for stat, value in player_stats.items():
        if not isinstance(value, (int, float)):
            continue
        avg = historical_avg.get(stat)
        std = historical_std.get(stat)
        if avg is None or std is None or std == 0:
            continue
        z = (value - avg) / std
        if abs(z) >= threshold_sd:
            anomalies.append(
                {
                    "stat": stat,
                    "value": round(value, 1),
                    "historical_avg": round(avg, 1),
                    "z_score": round(z, 2),
                    "direction": "above" if z > 0 else "below",
                }
            )
    anomalies.sort(key=lambda x: -abs(x["z_score"]))
    return anomalies


__all__ = ["detect_anomalies", "player_anomaly"]
