"""Hand-curated focus maps used by retrieval bundles.

``FORM_FOCUS`` maps shot-type → anatomy/technique focus slugs for the
form-coach retrieval bundle. ``PRACTICE_FOCUS`` maps a coach-facing focus
area (chip on the UI) to anatomy + technique slugs for the practice
generator. Both are consumed by ``retrieval.py`` query functions.

Anatomy / technique slugs may not all have backing concept pages yet
(content lands incrementally); ``build_form_context`` and
``build_practice_context`` filter out missing pages so these maps can list
aspirational slugs without breaking.
"""

from __future__ import annotations

FORM_FOCUS: dict[str, dict[str, list[str]]] = {
    "free-throw": {
        "anatomy": [
            "shoulder_girdle",
            "wrist_complex",
            "elbow_complex",
            "core_outer",
        ],
        "techniques": [
            "concept-jump-shot-mechanics",
            "concept-jump-shot-release-and-follow-through",
            "concept-quiet-eye-basketball-shooting",
            "concept-shooting-confidence-rhythm",
        ],
    },
    "jump-shot": {
        "anatomy": [
            "shoulder_girdle",
            "wrist_complex",
            "elbow_complex",
            "core_outer",
            "glute_max",
            "ankle_complex",
        ],
        "techniques": [
            "concept-jump-shot-biomechanics",
            "concept-jump-shot-mechanics",
            "concept-jump-shot-release-and-follow-through",
            "concept-midrange-jump-shot",
        ],
    },
    "layup": {
        "anatomy": [
            "hip_flexor_complex",
            "glute_max",
            "ankle_complex",
            "core_outer",
        ],
        "techniques": [
            "concept-1on1-reads-and-attacks",
            "concept-first-step-quickness",
        ],
    },
    "unknown": {
        "anatomy": ["core_outer"],
        "techniques": [],
    },
}


PRACTICE_FOCUS: dict[str, dict[str, list[str]]] = {
    "shooting": {
        "anatomy": ["wrist_complex", "elbow_complex", "shoulder_girdle", "core_outer"],
        "techniques": [],
    },
    "free-throws": {
        "anatomy": ["wrist_complex", "elbow_complex", "shoulder_girdle"],
        "techniques": [],
    },
    "ball-handling": {
        "anatomy": ["wrist_complex", "ankle_complex", "hip_flexor_complex"],
        "techniques": [],
    },
    "finishing": {
        "anatomy": [
            "ankle_complex",
            "glute_max",
            "hip_flexor_complex",
            "core_outer",
            "shoulder_girdle",
        ],
        "techniques": ["concept-technique-hard-cut-to-paint"],
    },
    "defense": {
        "anatomy": ["ankle_complex", "glute_max", "hip_flexor_complex", "core_outer"],
        "techniques": ["concept-technique-closeout-contest-verticality"],
    },
    "conditioning": {
        "anatomy": ["ankle_complex", "glute_max", "hip_flexor_complex", "core_outer"],
        "techniques": [],
    },
    "rebounding": {
        "anatomy": ["glute_max", "core_outer", "shoulder_girdle", "hip_flexor_complex"],
        "techniques": [],
    },
    "scrimmage": {
        "anatomy": [
            "ankle_complex",
            "glute_max",
            "hip_flexor_complex",
            "core_outer",
            "shoulder_girdle",
            "wrist_complex",
        ],
        "techniques": [],
    },
}
