"""Shared helpers for brief composers (play_brief, form_brief, practice_brief).

Citation-token extraction and anatomy-insight citation harvesting were
duplicated verbatim across the three composer modules. They live here so
the regex and the dedup-in-order logic have one home.
"""

from __future__ import annotations

import re

from motion.wiki_ops.retrieval import AnatomyDemand

# Matches "[S2]", "[S4, p.56]", "[S4, pp.56-58]" with ASCII or EN-dash ranges.
_CITATION_RE = re.compile(r"\[S\d+(?:,\s*pp?\.\s*[\d\-\u2013]+)?\]")


def extract_citations(text: str) -> list[str]:
    """Return unique ``[Sn, p.X]`` citations in ``text``, in order of appearance."""
    seen: list[str] = []
    for match in _CITATION_RE.finditer(text):
        token = match.group(0)
        if token not in seen:
            seen.append(token)
    return seen


def collect_anatomy_citations(anatomy: list[AnatomyDemand]) -> list[str]:
    """Harvest ``[Sn, p.X]`` tokens from anatomy ``key_principles`` + ``common_mistakes``."""
    cites: list[str] = []
    seen: set[str] = set()
    for a in anatomy:
        if a.insight is None:
            continue
        for entry in (*a.insight.key_principles, *a.insight.common_mistakes):
            cite = entry.get("citation")
            if cite and cite not in seen:
                seen.add(cite)
                cites.append(cite)
    return cites
