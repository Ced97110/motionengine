"""Player archetype convergence via normalized cosine similarity.

Each player has 9 skill attribute ratings (1-10). Each archetype has an
idealized skill profile. Convergence = how closely the player's skill SHAPE
matches the archetype's shape, expressed as a percentage.
"""

import numpy as np
from typing import Dict, List, Tuple


# 9 skill dimensions (fixed order)
SKILL_KEYS = [
    "SHT",  # Shooting
    "PAS",  # Passing
    "IQ",   # Basketball IQ
    "HND",  # Handles
    "DEF",  # Defense
    "PST",  # Post game
    "REB",  # Rebounding
    "ATH",  # Athleticism
    "SPD",  # Speed
]


# 8 archetype reference profiles (idealized 1-10 ratings per skill)
# Shape matters more than absolute values — cosine similarity normalizes magnitude.
ARCHETYPES: Dict[str, Dict[str, int]] = {
    "Sharpshooter": {
        "SHT": 10, "PAS": 5, "IQ": 6, "HND": 4, "DEF": 3,
        "PST": 2, "REB": 3, "ATH": 5, "SPD": 5,
    },
    "Floor General": {
        "SHT": 6, "PAS": 10, "IQ": 10, "HND": 9, "DEF": 5,
        "PST": 3, "REB": 4, "ATH": 6, "SPD": 7,
    },
    "Two-Way Wing": {
        "SHT": 7, "PAS": 6, "IQ": 7, "HND": 6, "DEF": 9,
        "PST": 4, "REB": 5, "ATH": 8, "SPD": 7,
    },
    "Athletic Slasher": {
        "SHT": 5, "PAS": 5, "IQ": 5, "HND": 7, "DEF": 6,
        "PST": 4, "REB": 5, "ATH": 10, "SPD": 10,
    },
    "Paint Beast": {
        "SHT": 3, "PAS": 4, "IQ": 6, "HND": 3, "DEF": 8,
        "PST": 10, "REB": 10, "ATH": 8, "SPD": 4,
    },
    "Stretch Big": {
        "SHT": 8, "PAS": 5, "IQ": 7, "HND": 5, "DEF": 6,
        "PST": 6, "REB": 7, "ATH": 6, "SPD": 5,
    },
    "Playmaking Big": {
        "SHT": 5, "PAS": 9, "IQ": 9, "HND": 6, "DEF": 6,
        "PST": 7, "REB": 7, "ATH": 6, "SPD": 5,
    },
    "Defensive Anchor": {
        "SHT": 3, "PAS": 4, "IQ": 7, "HND": 3, "DEF": 10,
        "PST": 7, "REB": 8, "ATH": 7, "SPD": 5,
    },
}


def _to_vector(skills: Dict[str, float]) -> np.ndarray:
    """Convert a skill dict to a fixed-order numpy vector."""
    return np.array([float(skills.get(k, 0)) for k in SKILL_KEYS], dtype=np.float64)


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity in [0, 1] (both vectors are non-negative)."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def compute_convergence(player_skills: Dict[str, float]) -> List[Tuple[str, float]]:
    """Return list of (archetype_name, convergence_pct) sorted descending.

    Each percentage is the cosine similarity expressed as an integer percent.
    """
    p = _to_vector(player_skills)
    results = []
    for name, archetype_skills in ARCHETYPES.items():
        a = _to_vector(archetype_skills)
        sim = _cosine(p, a)
        results.append((name, round(sim * 100, 1)))
    results.sort(key=lambda x: -x[1])
    return results


def dominant_archetype(player_skills: Dict[str, float]) -> Tuple[str, float]:
    """Return the single best-matching archetype and its percentage."""
    return compute_convergence(player_skills)[0]


def skill_gap(
    player_skills: Dict[str, float], archetype_name: str
) -> Dict[str, float]:
    """Return per-skill gap (archetype - player) for skills where player is below.

    Only returns skills where the archetype value exceeds the player's value,
    indicating areas where the player needs improvement to close the gap.
    """
    if archetype_name not in ARCHETYPES:
        raise ValueError(f"Unknown archetype: {archetype_name}")
    archetype = ARCHETYPES[archetype_name]
    gaps = {}
    for skill in SKILL_KEYS:
        player_val = player_skills.get(skill, 0)
        archetype_val = archetype.get(skill, 0)
        if archetype_val > player_val:
            gaps[skill] = round(archetype_val - player_val, 1)
    # Sort by gap size, largest first
    return dict(sorted(gaps.items(), key=lambda x: -x[1]))


__all__ = [
    "SKILL_KEYS",
    "ARCHETYPES",
    "compute_convergence",
    "dominant_archetype",
    "skill_gap",
]
