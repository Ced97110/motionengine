"""Test the ML modules: archetypes + anomaly detection."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.ml.archetypes import compute_convergence, dominant_archetype, skill_gap, ARCHETYPES
from lib.ml.anomaly import detect_anomalies

print("=== ML Layer Tests ===\n")

# Test 1: Archetype convergence for a shooter
print("--- Test 1: Pure shooter profile ---")
shooter = {"SHT": 9, "PAS": 5, "IQ": 6, "HND": 4, "DEF": 4,
           "PST": 2, "REB": 3, "ATH": 6, "SPD": 6}
results = compute_convergence(shooter)
print(f"Top 3 archetype matches:")
for name, pct in results[:3]:
    print(f"  {name}: {pct}%")

dom_name, dom_pct = dominant_archetype(shooter)
print(f"\nDominant: {dom_name} ({dom_pct}%)")
gaps = skill_gap(shooter, dom_name)
print(f"Skill gaps to close (vs {dom_name}):")
for skill, gap in list(gaps.items())[:5]:
    print(f"  {skill}: +{gap}")

# Test 2: Versatile playmaker
print("\n--- Test 2: Floor General profile ---")
pg = {"SHT": 7, "PAS": 9, "IQ": 10, "HND": 9, "DEF": 6,
      "PST": 3, "REB": 4, "ATH": 7, "SPD": 8}
results = compute_convergence(pg)
for name, pct in results[:3]:
    print(f"  {name}: {pct}%")

# Test 3: Paint-dominant big
print("\n--- Test 3: Big man profile ---")
big = {"SHT": 3, "PAS": 4, "IQ": 6, "HND": 3, "DEF": 9,
       "PST": 9, "REB": 10, "ATH": 8, "SPD": 4}
results = compute_convergence(big)
for name, pct in results[:3]:
    print(f"  {name}: {pct}%")

# Test 4: Anomaly detection - U14 with high turnovers
print("\n--- Test 4: Anomaly detection (U14 club, high turnovers) ---")
box_u14 = {
    "your_pts": 38,
    "turnovers": 35,  # Very high even for U14
    "rebounds": 32,
    "assists": 6,
    "fg_pct": 28.0,
}
anomalies = detect_anomalies(box_u14, "u14_club", threshold_sd=1.5)
print(f"Anomalies detected: {len(anomalies)}")
for a in anomalies:
    print(f"  [{a['type']}] {a['stat']}: {a['message']}")

# Test 5: Anomaly detection - NBA with high scoring
print("\n--- Test 5: Anomaly detection (NBA, elite scoring) ---")
box_nba = {
    "your_pts": 135,  # Well above NBA mean of ~105
    "turnovers": 10,
    "rebounds": 50,
    "assists": 30,
    "fg_pct": 55.0,
}
anomalies = detect_anomalies(box_nba, "nba", threshold_sd=1.5)
print(f"Anomalies detected: {len(anomalies)}")
for a in anomalies:
    print(f"  [{a['type']}] {a['stat']}: {a['message']}")

print("\n=== ML layer working ===")
