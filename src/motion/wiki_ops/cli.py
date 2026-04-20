"""Entry-point dispatchers for the wiki-ops CLIs.

Each function here is wired to ``[project.scripts]`` in
``backend/pyproject.toml`` and simply delegates to the corresponding
module's ``main``. Keeping them as one-liners means the subcommand
parsing stays local to each module — no central argparse tree that
would have to be re-derived whenever a command sprouts a new flag.
"""

from __future__ import annotations

import sys

from . import check_nba_terms as check_nba_terms_module
from . import count_pages as count_pages_module
from . import crossref as crossref_module
from . import detect_page_offsets as detect_page_offsets_module
from . import ingest as ingest_module
from . import lint_wiki as lint_wiki_module


def count_pages() -> int:
    return count_pages_module.main(sys.argv[1:])


def check_nba_terms() -> int:
    return check_nba_terms_module.main(sys.argv[1:])


def lint_wiki() -> int:
    return lint_wiki_module.main(sys.argv[1:])


def crossref() -> int:
    return crossref_module.main(sys.argv[1:])


def detect_page_offsets() -> int:
    return detect_page_offsets_module.main(sys.argv[1:])


def ingest() -> int:
    return ingest_module.main(sys.argv[1:])


_DISPATCH = {
    "count-pages": count_pages,
    "check-nba-terms": check_nba_terms,
    "lint": lint_wiki,
    "lint-wiki": lint_wiki,
    "crossref": crossref,
    "detect-page-offsets": detect_page_offsets,
    "ingest": ingest,
}


def main(argv: list[str] | None = None) -> int:
    """Dispatch a subcommand: ``python -m motion.wiki_ops <cmd> [args]``."""
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        sys.stderr.write(
            "usage: python -m motion.wiki_ops "
            "{count-pages,check-nba-terms,lint,detect-page-offsets,ingest}\n"
        )
        return 2
    cmd, *rest = args
    handler = _DISPATCH.get(cmd)
    if handler is None:
        sys.stderr.write(f"unknown subcommand: {cmd}\n")
        return 2
    # Route sub-args to the target module's own argparse.
    sys.argv = [cmd, *rest]
    return handler()
