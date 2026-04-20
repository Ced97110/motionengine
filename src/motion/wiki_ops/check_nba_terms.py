"""IP-compliance denylist scanner.

Port of ``frontend/scripts/check-nba-terms.ts``. Walks ``frontend/src``
and the wiki, applies a case-insensitive word-boundary denylist for NBA
team / college program / top-player names, and exits non-zero on any
hit. ``scripts/check-nba-terms.ts`` and ``log.md`` are whitelisted for
historical reasons — the TS original lists both explicitly.

The TS original runs from ``frontend/`` as cwd, so all "allowed path"
substrings are relative to that cwd. This port keeps parity by
accepting a ``--root`` flag that defines the reference directory for
relative path computations; when unspecified, it defaults to the
frontend root so output matches TS byte-for-byte.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from .paths import frontend_root, frontend_src_dir, wiki_dir

_SCAN_EXTS: frozenset[str] = frozenset({".ts", ".tsx", ".md"})

# Files whose matches are allowed — matches TS ALLOWED_IN_PATHS by
# substring against ``path.relative(cwd, file)``. The ``log.md`` path
# listed here is relative to the frontend cwd.
_ALLOWED_IN_PATHS: tuple[str, ...] = (
    "scripts/check-nba-terms.ts",
    "../backend/knowledge-base/wiki/log.md",
)

# NBA single-word team names. "Heat" and "Magic" are intentionally
# omitted — too many false positives in basketball body/training text;
# the qualified forms "Miami Heat" and "Orlando Magic" catch the
# meaningful cases.
_NBA_TEAMS_SINGLE: tuple[str, ...] = (
    "Lakers",
    "Celtics",
    "Warriors",
    "Bulls",
    "Nets",
    "Knicks",
    "Spurs",
    "Clippers",
    "76ers",
    "Sixers",
    "Rockets",
    "Mavericks",
    "Grizzlies",
    "Thunder",
    "Kings",
    "Suns",
    "Hornets",
    "Nuggets",
    "Pelicans",
    "Trail Blazers",
    "Timberwolves",
    "Jazz",
    "Pistons",
    "Pacers",
    "Cavaliers",
    "Bucks",
    "Hawks",
    "Raptors",
    "Wizards",
)

_NBA_TEAMS_QUALIFIED: tuple[str, ...] = (
    "Miami Heat",
    "Orlando Magic",
    "Detroit Pistons",
    "Chicago Bulls",
)

_COLLEGE_PROGRAMS: tuple[str, ...] = (
    "UCLA",
    "Duke",
    "Kansas",
    "Kentucky",
    "Villanova",
    "Princeton",
    "Syracuse",
    "North Carolina",
    "UConn",
)

_PLAYER_NAMES: tuple[str, ...] = (
    "LeBron",
    "Kareem",
    "Michael Jordan",
    "Kobe Bryant",
    "Shaquille",
    "Magic Johnson",
    "Larry Bird",
    "Stephen Curry",
    "Kevin Durant",
    "Giannis",
    "Luka",
    "Jokic",
    "Jayson Tatum",
    "Joel Embiid",
    "Kawhi",
    "Scottie Pippen",
    "Phil Johnson",
    "D'Angelo Russell",
    "Austin Reaves",
    "Rui Hachimura",
    "Anthony Davis",
)


@dataclass(frozen=True)
class _DenyEntry:
    term: str
    pattern: re.Pattern[str]


def _word_bounded(pattern_body: str) -> re.Pattern[str]:
    return re.compile(rf"\b{pattern_body}\b", re.IGNORECASE)


def _build_denylist() -> list[_DenyEntry]:
    entries: list[_DenyEntry] = []
    for group in (_NBA_TEAMS_SINGLE, _NBA_TEAMS_QUALIFIED, _COLLEGE_PROGRAMS):
        for term in group:
            entries.append(_DenyEntry(term=term, pattern=_word_bounded(re.escape(term))))
    for term in _PLAYER_NAMES:
        # Match straight-quote and typographic-quote variants of the
        # apostrophe, mirroring TS ``t.replace(/'/g, "['’]")``.  # noqa: RUF003
        # Note: Python 3.7+ re.escape does NOT escape `'`, so we replace the
        # literal apostrophe (not `\'`) — otherwise the replacement is a no-op.
        escaped = re.escape(term).replace("'", "['’]")  # noqa: RUF001
        entries.append(_DenyEntry(term=term, pattern=_word_bounded(escaped)))
    return entries


_DENYLIST: list[_DenyEntry] = _build_denylist()


@dataclass(frozen=True)
class Match:
    file: str
    line: int
    term: str
    content: str


def _walk(root: Path) -> list[Path]:
    """Iterative DFS that mirrors the TS ``walk`` traversal order.

    The TS original uses ``stack.pop()`` (LIFO) + ``fs.readdirSync``.
    ``readdirSync`` on macOS APFS returns lexicographic order; on Linux
    ext4 it returns directory-entry order. For parity with the typical
    dev-box case we sort lexicographically, which also stabilizes the
    output across platforms.
    """
    if not root.exists():
        return []
    files: list[Path] = []
    stack: list[Path] = [root]
    while stack:
        directory = stack.pop()
        try:
            entries = sorted(directory.iterdir(), key=lambda p: p.name)
        except PermissionError:
            continue
        # Reverse so the stack pops in forward order (matches TS
        # post-pop sorting intent of "top of directory first").
        for entry in reversed(entries):
            if entry.is_dir():
                if entry.name in ("node_modules", "_review"):
                    continue
                stack.append(entry)
                continue
            if entry.suffix not in _SCAN_EXTS:
                continue
            files.append(entry)
    return files


def _is_allowed(file_path: Path, reference: Path) -> bool:
    try:
        rel = str(file_path.relative_to(reference))
    except ValueError:
        # Fall back to a string relative path computation for paths
        # that live outside the reference tree (e.g. the sibling wiki).
        rel = os.path.relpath(file_path, reference)
    return any(p in rel for p in _ALLOWED_IN_PATHS)


def scan(roots: list[Path], reference: Path) -> list[Match]:
    matches: list[Match] = []
    for root in roots:
        for file_path in _walk(root):
            if _is_allowed(file_path, reference):
                continue
            try:
                text = file_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for i, content in enumerate(text.split("\n")):
                for entry in _DENYLIST:
                    if entry.pattern.search(content):
                        matches.append(
                            Match(
                                file=str(file_path),
                                line=i + 1,
                                term=entry.term,
                                content=content.strip(),
                            )
                        )
    return matches


def format_report(matches: list[Match], reference: Path) -> str:
    """Render the stderr report for hit results (matches TS output)."""
    lines: list[str] = []
    lines.append(f"✗ {len(matches)} forbidden term occurrence(s):\n")
    by_file: dict[str, list[Match]] = {}
    for m in matches:
        by_file.setdefault(m.file, []).append(m)
    for file, ms in by_file.items():
        rel = os.path.relpath(file, reference)
        lines.append(f"  {rel}")
        for m in ms[:3]:
            snippet = m.content if len(m.content) <= 120 else m.content[:117] + "..."
            lines.append(f"    L{m.line} [{m.term}]: {snippet}")
        if len(ms) > 3:
            lines.append(f"    ... +{len(ms) - 3} more")
    lines.append(
        "\nRemediation: replace with archetype-based or descriptive terms. "
        "See docs/DESIGN-SYSTEM.md + project CLAUDE.md rule."
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="wiki-check-nba-terms",
        description="Fail if NBA/institution/player names leak into src/ or wiki.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help=(
            "Reference cwd for relative-path output and the ALLOWED_IN_PATHS "
            "substring match. Defaults to the frontend/ directory to match "
            "the TS original byte-for-byte."
        ),
    )
    parser.add_argument(
        "--src-dir", type=Path, default=None, help="Override the frontend src/ directory."
    )
    parser.add_argument("--wiki-dir", type=Path, default=None, help="Override the wiki directory.")
    args = parser.parse_args(argv)

    reference = args.root if args.root is not None else frontend_root()
    src_root = args.src_dir if args.src_dir is not None else frontend_src_dir()
    wiki_root = wiki_dir(args.wiki_dir)

    hits = scan([src_root, wiki_root], reference=reference)
    if not hits:
        sys.stdout.write("✓ No NBA/institution/player names detected in src/ or wiki.\n")
        return 0
    sys.stderr.write(format_report(hits, reference=reference))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
