"""Motion wiki-ops package.

Python ports of the deterministic TypeScript wiki-operations CLIs that
previously lived under ``frontend/scripts/``. Byte-equal parity with the
TypeScript predecessors on fixture sets is the acceptance gate — see
``backend/spec/wiki-ops-python-migration.md`` §6 and §7.1.

Phases currently shipped:

- Phase 1 (deterministic):

  * ``count_pages`` — PDF page counter
  * ``resynth_manifest`` — read-only planner for synthesize-plays.ts
  * ``check_nba_terms`` — IP denylist scanner
  * ``lint_wiki`` — wiki markdown linter

- Phase 2 (Claude-backed, deterministic artifact):

  * ``detect_page_offsets`` — per-source printed→physical page offset

- Phase 3 (Claude-backed ingest):

  * ``ingest`` — PDF → chunked Claude calls → wiki pages + index + log
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
