"""Source-PDF registry and ID resolution.

Mirrors the ``SOURCE_PDFS`` constant in ``frontend/scripts/ingest.ts``
and related TS scripts. No duplication across ports — every Python CLI
that references a source PDF imports from here.

The list is authoritative for the nine raw PDFs committed to
``backend/knowledge-base/raw/`` (gitignored in practice, but the
registry itself is not). The list order matches that of the raw
directory listing used by the deterministic count-pages flow.
"""

from __future__ import annotations

from typing import Final

# Source-id → filename on disk under backend/knowledge-base/raw/.
# Keep in sync with SOURCE_PDFS in frontend/scripts/ingest.ts and
# frontend/scripts/resolve-diagrams.ts.
SOURCE_PDFS: Final[dict[str, str]] = {
    "S1": "lets-talk-defense.pdf",
    "S2": "basketball-anatomy.pdf",
    "S3": "offensive-skill-development.pdf",
    "S4": "basketball-for-coaches.pdf",
    "S5": "basketball-shooting.pdf",
    "S6": "footwork-balance-pivoting.pdf",
    "S7": "nba-coaches-playbook.pdf",
    "S8": "speed-agility-quickness.pdf",
    "S9": "explosive-calisthenics.pdf",
    # Tier 1 ingest batch — added 2026-04-20
    "S10": "basketball-sports-medicine-and-science.pdf",
    "S11": "strength-training-for-basketball-nsca.pdf",
    "S12": "improving-practice-performance-basketball.pdf",
}


def resolve_pdf_filename(source_id: str) -> str:
    """Look up the filename for a source-id. Raises ``KeyError`` if unknown."""
    return SOURCE_PDFS[source_id]
