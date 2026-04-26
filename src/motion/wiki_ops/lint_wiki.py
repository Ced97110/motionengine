"""Wiki linter — port of ``frontend/scripts/lint-wiki.ts``.

Read-only audit of ``backend/knowledge-base/wiki/`` against
``SCHEMA.md``. Ten checks: dead wikilinks, orphan pages, bidirectional
failures, gap concepts, filename violations, duplicate index entries,
stale DIAGRAM markers, missing citations, schema section
non-compliance, duplicate slugs.

Exit 1 on any error-level finding; exit 0 otherwise. Exit 2 on
uncaught exception, matching the TS behavior.

The Markdown report is written to
``<root>/docs/audits/wiki-lint-<YYYY-MM-DD>.md`` where ``<root>`` is
the ``--root`` flag (defaults to ``frontend/`` for parity with the TS
original).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from motion.sports import DEFAULT_SPORT

from .frontmatter import parse_shallow
from .paths import frontend_root, wiki_dir

Severity = Literal["error", "warning", "info"]
CheckId = Literal[
    "dead-wikilink",
    "orphan-page",
    "bidirectional-failure",
    "gap-concept",
    "filename-violation",
    "duplicate-index-entry",
    "stale-diagram-marker",
    "missing-citation",
    "schema-section-missing",
    "duplicate-slug",
    # Play-geometry rules (added with the wiki-as-source-of-truth work).
    # Graduated severity: new rules land as `warning` so a dirty corpus
    # doesn't break CI; promote to `error` once the corpus is clean.
    "play-diagram-per-phase",
    "play-path-valid-svg",
    "play-path-roles-resolve",
    "play-duration-sane",
    "play-ballstart-known",
]


@dataclass(frozen=True)
class Finding:
    check: CheckId
    severity: Severity
    file: str
    message: str
    line: int | None = None


@dataclass(frozen=True)
class LinkRef:
    target: str
    line: int


@dataclass
class PageRecord:
    file_path: str
    file_name: str
    slug: str
    raw: str
    lines: list[str]
    frontmatter: dict[str, str]
    body: str
    body_start_line: int
    out_links: list[LinkRef]


@dataclass(frozen=True)
class CheckSpec:
    id: CheckId
    title: str
    recommendation: str


_META_SLUGS: frozenset[str] = frozenset({"index", "log"})
_CRITICAL_SEVERITIES: frozenset[Severity] = frozenset({"error"})

_GAP_MIN_PAGES = 5
_GAP_MIN_WORDS = 2
_GAP_MAX_WORDS = 4

_REQUIRED_SECTIONS: dict[str, tuple[str, ...]] = {
    "concept": (
        "## Summary",
        "## When to Use",
        "## Key Principles",
        "## Related Concepts",
        "## Sources",
    ),
    "drill": (
        "## Objective",
        "## Setup",
        "## Execution",
        "## Coaching Points",
        "## Concepts Taught",
        "## Sources",
    ),
    "play": (
        "## Overview",
        "## Formation",
        "## Phases",
        "## Key Coaching Points",
        "## Sources",
    ),
    "source-summary": (
        "## Overview",
        "## Key Themes",
        "## Chapter Breakdown",
    ),
}

_CHECK_CATALOG: tuple[CheckSpec, ...] = (
    CheckSpec(
        id="dead-wikilink",
        title="Dead wikilinks",
        recommendation=(
            "Create the missing page, or update the link to point at the correct slug. "
            "Inspect `index.md` links first — mis-typed filenames (e.g. spaces) surface here."
        ),
    ),
    CheckSpec(
        id="orphan-page",
        title="Orphan pages",
        recommendation=(
            "Add inbound [[links]] from at least one related page, or add the slug to "
            "`index.md`. Pages with zero inbound references are unreachable during query."
        ),
    ),
    CheckSpec(
        id="bidirectional-failure",
        title="Bidirectional link failures",
        recommendation=(
            "Per SCHEMA.md §Cross-Linking, if A links to B, B should link back to A. "
            "Add a reciprocal [[A]] in B's Related section."
        ),
    ),
    CheckSpec(
        id="gap-concept",
        title="Gap concepts",
        recommendation=(
            "Term is mentioned across many pages but has no dedicated page. Consider "
            "creating a concept page or consolidating references."
        ),
    ),
    CheckSpec(
        id="filename-violation",
        title="Filename violations",
        recommendation=(
            "Rename to kebab-case per SCHEMA.md §File Naming. No spaces, no uppercase, "
            "`.md` extension required."
        ),
    ),
    CheckSpec(
        id="duplicate-index-entry",
        title="Duplicate index entries",
        recommendation=(
            "Consolidate the two index entries. Decide whether they describe the same "
            "page (merge) or different pages (rename one)."
        ),
    ),
    CheckSpec(
        id="stale-diagram-marker",
        title="Stale DIAGRAM markers",
        recommendation=(
            "Replace `<!-- DIAGRAM: ... -->` placeholders with a written description of "
            "player positions/movements, or extract the diagram via the diagram pipeline."
        ),
    ),
    CheckSpec(
        id="missing-citation",
        title="Missing citations",
        recommendation=(
            "Per SCHEMA.md §Citation Rules, every factual claim must cite a source. "
            "Add `[Sn, p.XX]` or `[Sn]` to the page."
        ),
    ),
    CheckSpec(
        id="schema-section-missing",
        title="Schema section non-compliance",
        recommendation=(
            "Add the missing sections as defined in SCHEMA.md for this page type. "
            "Required sections are mandatory."
        ),
    ),
    CheckSpec(
        id="duplicate-slug",
        title="Duplicate slugs",
        recommendation=(
            "Two files collapse to the same effective slug (case/space-normalized). "
            "Rename one so the wiki has a 1:1 slug→file mapping."
        ),
    ),
)

# Regex translations of the TS literals. Each retains the TS flag set.
_WIKILINK_RE = re.compile(r"\[\[([^\]\n]+?)\]\]")
_DIAGRAM_RE = re.compile(r"<!--\s*DIAGRAM:[^>]*-->")
_CITATION_RE = re.compile(r"\[S\d+(?:[^\]]*?)\]")
_FACTUAL_LINE_RE = re.compile(r"\b(\d{1,3}(?:\.\d+)?%|\d+\s*[-–]\s*\d+|\d{2,}|\d+\s*of\s*\d+)\b")  # noqa: RUF001
_TITLE_CASE_RE = re.compile(r"\b(?:[A-Z][a-z]{2,}(?:[ \t]+[A-Z][a-z]{2,}){1,3})\b")
_INDEX_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
_KEBAB_OK_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def _slug_from_filename(name: str) -> str:
    return re.sub(r"\.md$", "", name, flags=re.IGNORECASE)


def _normalized_slug(slug: str) -> str:
    return re.sub(r"\s+", "-", slug.strip().lower())


def _extract_out_links(body: str, body_start_line: int) -> list[LinkRef]:
    links: list[LinkRef] = []
    for i, line in enumerate(body.split("\n")):
        for m in _WIKILINK_RE.finditer(line):
            # Split on pipe then fragment — mirrors TS
            # ``target.split("|")[0].split("#")[0].trim()``.
            target = m.group(1).split("|")[0].split("#")[0].strip()
            links.append(LinkRef(target=target, line=body_start_line + i))
    return links


def _list_wiki_pages(directory: Path) -> list[str]:
    entries = [
        e.name for e in directory.iterdir() if e.is_file() and e.name.lower().endswith(".md")
    ]
    return sorted(entries)


def _load_page(directory: Path, file_name: str) -> PageRecord:
    file_path = directory / file_name
    raw = file_path.read_text(encoding="utf-8")
    frontmatter, body, body_start_line = parse_shallow(raw)
    lines = raw.split("\n")
    out_links = _extract_out_links(body, body_start_line)
    return PageRecord(
        file_path=str(file_path),
        file_name=file_name,
        slug=_slug_from_filename(file_name),
        raw=raw,
        lines=lines,
        frontmatter=frontmatter,
        body=body,
        body_start_line=body_start_line,
        out_links=out_links,
    )


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def _check_filenames(pages: list[PageRecord]) -> list[Finding]:
    findings: list[Finding] = []
    for p in pages:
        if p.slug in _META_SLUGS:
            continue
        name = p.file_name
        reasons: list[str] = []
        if not name.endswith(".md"):
            reasons.append("missing .md extension")
        if name != name.lower():
            reasons.append("contains uppercase")
        if re.search(r"\s", name):
            reasons.append("contains whitespace")
        if re.search(r"[^a-z0-9\-.]", name.lower()):
            reasons.append("contains non [a-z0-9-.] characters")
        if not _KEBAB_OK_RE.match(name) and not reasons:
            reasons.append("not strict kebab-case")
        if reasons:
            findings.append(
                Finding(
                    check="filename-violation",
                    severity="error",
                    file=p.file_path,
                    message=f'Filename "{name}" — {"; ".join(reasons)}',
                )
            )
    return findings


def _check_duplicate_slugs(pages: list[PageRecord]) -> list[Finding]:
    findings: list[Finding] = []
    groups: dict[str, list[PageRecord]] = {}
    for p in pages:
        if p.slug in _META_SLUGS:
            continue
        key = _normalized_slug(p.slug)
        groups.setdefault(key, []).append(p)
    for key, group in groups.items():
        if len(group) > 1:
            names = ", ".join(g.file_name for g in group)
            for p in group:
                findings.append(
                    Finding(
                        check="duplicate-slug",
                        severity="error",
                        file=p.file_path,
                        message=f'Slug "{key}" is shared by {len(group)} files: {names}',
                    )
                )
    return findings


def _check_dead_wikilinks(pages: list[PageRecord], slug_set: frozenset[str]) -> list[Finding]:
    findings: list[Finding] = []
    for p in pages:
        if p.slug == "log":
            continue
        for link in p.out_links:
            if not link.target:
                continue
            target = re.sub(r"\.md$", "", link.target, flags=re.IGNORECASE)
            if re.search(r"\s", target):
                findings.append(
                    Finding(
                        check="dead-wikilink",
                        severity="error",
                        file=p.file_path,
                        line=link.line,
                        message=(
                            f'Wikilink target "{link.target}" contains whitespace — malformed slug'
                        ),
                    )
                )
                continue
            if target not in slug_set:
                findings.append(
                    Finding(
                        check="dead-wikilink",
                        severity="error",
                        file=p.file_path,
                        line=link.line,
                        message=(
                            f'Wikilink target "[[{link.target}]]" does not resolve to any wiki page'
                        ),
                    )
                )

    index_page = next((p for p in pages if p.slug == "index"), None)
    if index_page is not None:
        index_lines = index_page.raw.split("\n")
        for i, line in enumerate(index_lines):
            for m in _INDEX_LINK_RE.finditer(line):
                href = m.group(1)
                if not href.endswith(".md"):
                    continue
                base = os.path.basename(href)
                slug = _slug_from_filename(base)
                if re.search(r"\s", base):
                    findings.append(
                        Finding(
                            check="dead-wikilink",
                            severity="error",
                            file=index_page.file_path,
                            line=i + 1,
                            message=(
                                f'index.md links to "{base}" — filename contains '
                                "whitespace (invalid kebab-case)"
                            ),
                        )
                    )
                    continue
                if slug not in slug_set:
                    findings.append(
                        Finding(
                            check="dead-wikilink",
                            severity="error",
                            file=index_page.file_path,
                            line=i + 1,
                            message=f'index.md links to "{base}" — file does not exist',
                        )
                    )
    return findings


def _check_orphans(pages: list[PageRecord]) -> list[Finding]:
    inbound: dict[str, int] = {}
    for p in pages:
        for link in p.out_links:
            target = re.sub(r"\.md$", "", link.target, flags=re.IGNORECASE)
            inbound[target] = inbound.get(target, 0) + 1
    index_page = next((p for p in pages if p.slug == "index"), None)
    if index_page is not None:
        for m in _INDEX_LINK_RE.finditer(index_page.raw):
            href = m.group(1)
            if href.endswith(".md"):
                slug = _slug_from_filename(os.path.basename(href))
                inbound[slug] = inbound.get(slug, 0) + 1
    findings: list[Finding] = []
    for p in pages:
        if p.slug in _META_SLUGS:
            continue
        if inbound.get(p.slug, 0) == 0:
            findings.append(
                Finding(
                    check="orphan-page",
                    severity="warning",
                    file=p.file_path,
                    message=(
                        f'Page "{p.slug}" has zero inbound [[links]] and no index.md reference'
                    ),
                )
            )
    return findings


def _check_bidirectional(pages: list[PageRecord], slug_set: frozenset[str]) -> list[Finding]:
    by_slug: dict[str, PageRecord] = {p.slug: p for p in pages}
    findings: list[Finding] = []
    for p in pages:
        if p.slug in _META_SLUGS:
            continue
        out_slugs: set[str] = set()
        for link in p.out_links:
            out_slugs.add(re.sub(r"\.md$", "", link.target, flags=re.IGNORECASE))
        for target in out_slugs:
            if target not in slug_set:
                continue
            if target == p.slug:
                continue
            other = by_slug.get(target)
            if other is None:
                continue
            if other.slug in _META_SLUGS:
                continue
            links_back = any(
                re.sub(r"\.md$", "", link.target, flags=re.IGNORECASE) == p.slug
                for link in other.out_links
            )
            if not links_back:
                findings.append(
                    Finding(
                        check="bidirectional-failure",
                        severity="warning",
                        file=p.file_path,
                        message=(
                            f"Links to [[{target}]] but [[{target}]] does not link "
                            f"back to [[{p.slug}]]"
                        ),
                    )
                )
    return findings


def _check_stale_diagrams(pages: list[PageRecord]) -> list[Finding]:
    findings: list[Finding] = []
    for p in pages:
        if p.slug in _META_SLUGS:
            continue
        for i, line in enumerate(p.lines):
            if _DIAGRAM_RE.search(line):
                snippet = line.strip()[:200]
                findings.append(
                    Finding(
                        check="stale-diagram-marker",
                        severity="info",
                        file=p.file_path,
                        line=i + 1,
                        message=f"Unresolved DIAGRAM marker: {snippet}",
                    )
                )
    return findings


def _check_missing_citations(pages: list[PageRecord]) -> list[Finding]:
    findings: list[Finding] = []
    structural_re = re.compile(r"^(#{1,6}\s|```|---|\s*$|\|)")
    small_ordered_re = re.compile(r"^\s*\d+\.\s+[A-Za-z]")
    non_small_re = re.compile(r"\d{2,}|%|–")  # noqa: RUF001
    for p in pages:
        if p.slug in _META_SLUGS:
            continue
        if p.frontmatter.get("type") == "source-summary":
            continue
        if not _CITATION_RE.search(p.raw):
            findings.append(
                Finding(
                    check="missing-citation",
                    severity="warning",
                    file=p.file_path,
                    message="Page has no [Sn]-style citation anywhere",
                )
            )
            continue
        suspect_line = -1
        for i, line in enumerate(p.lines):
            if not _FACTUAL_LINE_RE.search(line):
                continue
            if _CITATION_RE.search(line):
                continue
            prev_line = p.lines[i - 1] if i - 1 >= 0 else ""
            next_line = p.lines[i + 1] if i + 1 < len(p.lines) else ""
            if _CITATION_RE.search(prev_line) or _CITATION_RE.search(next_line):
                continue
            if structural_re.match(line):
                continue
            if small_ordered_re.match(line) and not non_small_re.search(line):
                continue
            suspect_line = i + 1
            break
        if suspect_line > 0:
            findings.append(
                Finding(
                    check="missing-citation",
                    severity="info",
                    file=p.file_path,
                    line=suspect_line,
                    message="Factual-looking line lacks adjacent [Sn] citation",
                )
            )
    return findings


def _check_schema_sections(pages: list[PageRecord]) -> list[Finding]:
    findings: list[Finding] = []
    for p in pages:
        if p.slug in _META_SLUGS:
            continue
        type_ = p.frontmatter.get("type")
        if not type_:
            findings.append(
                Finding(
                    check="schema-section-missing",
                    severity="warning",
                    file=p.file_path,
                    message="Frontmatter is missing required `type` key",
                )
            )
            continue
        required = _REQUIRED_SECTIONS.get(type_)
        if not required:
            continue
        missing: list[str] = []
        for heading in required:
            pattern = re.compile(rf"^{re.escape(heading)}\b", re.MULTILINE)
            if not pattern.search(p.body):
                missing.append(heading)
        if missing:
            findings.append(
                Finding(
                    check="schema-section-missing",
                    severity="warning",
                    file=p.file_path,
                    message=f"Type={type_} missing section(s): {', '.join(missing)}",
                )
            )
    return findings


def _check_duplicate_index_entries(pages: list[PageRecord]) -> list[Finding]:
    findings: list[Finding] = []
    index_page = next((p for p in pages if p.slug == "index"), None)
    if index_page is None:
        return findings
    seen: dict[str, list[int]] = {}
    lines = index_page.raw.split("\n")
    for i, line in enumerate(lines):
        for m in _INDEX_LINK_RE.finditer(line):
            href = m.group(1)
            if not href.endswith(".md"):
                continue
            slug = _slug_from_filename(os.path.basename(href))
            seen.setdefault(slug, []).append(i + 1)
    for slug, lines_seen in seen.items():
        if len(lines_seen) > 1:
            findings.append(
                Finding(
                    check="duplicate-index-entry",
                    severity="error",
                    file=index_page.file_path,
                    line=lines_seen[0],
                    message=(
                        f'Slug "{slug}" is listed {len(lines_seen)} times in index.md '
                        f"(lines {', '.join(str(n) for n in lines_seen)})"
                    ),
                )
            )
    return findings


_GAP_NOISE: frozenset[str] = frozenset(
    {
        "Common Mistakes",
        "Complex Variations",
        "Concepts Taught",
        "Coaching Cues",
        "Coaching Points",
        "Key Coaching",
        "Key Coaching Points",
        "Key Principles",
        "Muscles Involved",
        "Player Responsibilities",
        "Related Concepts",
        "Related Drills",
        "Related Plays",
        "Progressions",
        "Sources",
        "Notable Quotes",
        "Overview",
        "Objective",
        "Setup",
        "Execution",
        "Formation",
        "Phases",
        "Counters",
        "When To Use",
        "Summary",
        "Unique Contributions",
        "Chapter Breakdown",
        "Key Themes",
        "Motion Offense",
        "Triangle Offense",
        "Continuity Offense",
        "Coaches Playbook",
        "Basketball Anatomy",
    }
)


def _check_gap_concepts(
    pages: list[PageRecord], slug_set: frozenset[str], wiki_directory: Path
) -> list[Finding]:
    findings: list[Finding] = []
    mentions: dict[str, set[str]] = {}
    for p in pages:
        if p.slug in _META_SLUGS:
            continue
        seen_in_page: set[str] = set()
        for m in _TITLE_CASE_RE.finditer(p.body):
            term = m.group(0)
            word_count = len(re.split(r"\s+", term))
            if word_count < _GAP_MIN_WORDS or word_count > _GAP_MAX_WORDS:
                continue
            if term in seen_in_page:
                continue
            seen_in_page.add(term)
            mentions.setdefault(term, set()).add(p.slug)

    for term, page_set in mentions.items():
        if len(page_set) < _GAP_MIN_PAGES:
            continue
        if term in _GAP_NOISE:
            continue
        slug = re.sub(r"\s+", "-", term.lower())
        has_page = False
        for s in slug_set:
            if s == slug or f"-{slug}-" in s or s.startswith(f"{slug}-") or s.endswith(f"-{slug}"):
                has_page = True
                break
            if slug in s:
                has_page = True
                break
        if has_page:
            continue
        findings.append(
            Finding(
                check="gap-concept",
                severity="info",
                file=str(wiki_directory / "(corpus)"),
                message=(
                    f'Term "{term}" appears in {len(page_set)} pages but has no dedicated page'
                ),
            )
        )
    return findings


# ---------------------------------------------------------------------------
# Play-geometry checks — validate schema v2 `diagram-positions` content.
# Graduated severity: all five land as `warning` until the corpus has been
# migrated; promote to `error` once clean.
# ---------------------------------------------------------------------------

import json  # noqa: E402  (section-local import, keeps diffs small)

_PLAY_DIAGRAM_FENCE_RE = re.compile(
    r"```\s*json\s+name=diagram-positions\s*\n(?P<body>.*?)\n```",
    re.DOTALL,
)
_PLAY_PHASE_HEADER_RE = re.compile(
    r"^###\s+Phase\s+(\d+)", re.MULTILINE
)
# Whitelist for SVG path data — M/L/C/Q commands, signed floats, whitespace,
# commas. Rejects any angle bracket, quote, or script-like content.
_PLAY_SVG_PATH_RE = re.compile(r"^[MLCQmlcq\s\d\.\,\-\+eE]+$")

# Role tokens the importer's `_resolve_destination` recognizes. Duplicated
# here to avoid a runtime import from a services module; keep in sync if
# the importer's list grows.
_PLAY_ROLE_TOKENS: frozenset[str] = frozenset({
    "right_wing", "left_wing", "top", "right_corner", "left_corner",
    "right_elbow", "left_elbow", "basket", "rim", "left_block", "right_block",
    "ball_side_corner", "weak_side_corner", "weak_side_wing", "ball_side_wing",
    "high_post", "low_post", "free_throw_line", "paint", "key",
})


def _play_blocks(page: PageRecord) -> list[tuple[dict, int]]:
    """Parse every diagram-positions block; yield ``(data, line_no)``.

    ``line_no`` is 1-based, pointing at the opening fence in the file.
    """
    out: list[tuple[dict, int]] = []
    for match in _PLAY_DIAGRAM_FENCE_RE.finditer(page.body):
        raw = match.group("body")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        # Line number of the opening fence, counted against body_start_line.
        prefix_lines = page.body[: match.start()].count("\n")
        out.append((data, page.body_start_line + prefix_lines))
    return out


def _is_play_page(page: PageRecord) -> bool:
    return page.frontmatter.get("type") == "play"


def _check_play_diagram_per_phase(pages: list[PageRecord]) -> list[Finding]:
    """Warn when a play page's ### Phase count exceeds its block count."""
    findings: list[Finding] = []
    for p in pages:
        if not _is_play_page(p):
            continue
        phases = set(_PLAY_PHASE_HEADER_RE.findall(p.body))
        blocks = _play_blocks(p)
        if not phases and not blocks:
            continue
        if len(blocks) < len(phases):
            findings.append(
                Finding(
                    check="play-diagram-per-phase",
                    severity="warning",
                    file=p.file_path,
                    message=(
                        f"{len(phases)} phase section(s) but only {len(blocks)} "
                        "diagram-positions block(s) — each phase should carry "
                        "its own block for deterministic lab round-trip."
                    ),
                )
            )
    return findings


def _check_play_path_valid_svg(pages: list[PageRecord]) -> list[Finding]:
    """Reject authored paths that contain disallowed characters.

    Whitelist: M/L/C/Q commands, digits, signs, decimals, exponents,
    whitespace, commas. Anything else (angle brackets, quotes, script) is
    a red flag for injection and fails the rule.
    """
    findings: list[Finding] = []
    for p in pages:
        if not _is_play_page(p):
            continue
        for block, line_no in _play_blocks(p):
            actions = block.get("actions")
            if not isinstance(actions, list):
                continue
            for idx, a in enumerate(actions):
                if not isinstance(a, dict):
                    continue
                path = a.get("path")
                if not isinstance(path, str) or not path.strip():
                    continue
                if not _PLAY_SVG_PATH_RE.match(path):
                    findings.append(
                        Finding(
                            check="play-path-valid-svg",
                            severity="warning",
                            file=p.file_path,
                            line=line_no,
                            message=(
                                f"action[{idx}].path contains characters outside "
                                "the M/L/C/Q whitelist — possible injection or "
                                f"malformed authoring: {path[:60]!r}"
                            ),
                        )
                    )
    return findings


def _check_play_path_roles_resolve(pages: list[PageRecord]) -> list[Finding]:
    """Every action's ``from`` / ``to`` must reference a known player or role token."""
    findings: list[Finding] = []
    for p in pages:
        if not _is_play_page(p):
            continue
        for block, line_no in _play_blocks(p):
            players = block.get("players")
            if not isinstance(players, list):
                continue
            known_ids: set[str] = set()
            for entry in players:
                if isinstance(entry, dict) and entry.get("role") is not None:
                    known_ids.add(str(entry["role"]))
            actions = block.get("actions")
            if not isinstance(actions, list):
                continue
            for idx, a in enumerate(actions):
                if not isinstance(a, dict):
                    continue
                mover = a.get("from")
                if mover is not None and str(mover) not in known_ids:
                    findings.append(
                        Finding(
                            check="play-path-roles-resolve",
                            severity="warning",
                            file=p.file_path,
                            line=line_no,
                            message=(
                                f"action[{idx}].from={mover!r} not in the block's "
                                "players roster"
                            ),
                        )
                    )
                to = a.get("to")
                # `to` can be: a player id (string matching a role),
                # a role token (string in _PLAY_ROLE_TOKENS), or a coord list.
                role_key = (
                    to.lower().replace("-", "_").replace(" ", "_")
                    if isinstance(to, str)
                    else ""
                )
                if (
                    isinstance(to, str)
                    and to not in known_ids
                    and role_key not in _PLAY_ROLE_TOKENS
                ):
                    findings.append(
                        Finding(
                            check="play-path-roles-resolve",
                            severity="warning",
                            file=p.file_path,
                            line=line_no,
                            message=(
                                f"action[{idx}].to={to!r} is not a player id, a "
                                "coord list, or a known role token"
                            ),
                        )
                    )
    return findings


def _check_play_duration_sane(pages: list[PageRecord]) -> list[Finding]:
    """Flag timing overrides outside the [500, 10000] ms range."""
    findings: list[Finding] = []
    for p in pages:
        if not _is_play_page(p):
            continue
        for block, line_no in _play_blocks(p):
            actions = block.get("actions")
            if not isinstance(actions, list):
                continue
            for idx, a in enumerate(actions):
                if not isinstance(a, dict):
                    continue
                for key in ("durationMs", "gapAfterMs"):
                    value = a.get(key)
                    if value is None:
                        continue
                    if not isinstance(value, (int, float)):
                        findings.append(
                            Finding(
                                check="play-duration-sane",
                                severity="warning",
                                file=p.file_path,
                                line=line_no,
                                message=f"action[{idx}].{key}={value!r} is not numeric",
                            )
                        )
                        continue
                    if value < 500 or value > 10000:
                        findings.append(
                            Finding(
                                check="play-duration-sane",
                                severity="warning",
                                file=p.file_path,
                                line=line_no,
                                message=(
                                    f"action[{idx}].{key}={value} outside sane "
                                    "range [500, 10000] ms"
                                ),
                            )
                        )
    return findings


def _check_play_ballstart_known(pages: list[PageRecord]) -> list[Finding]:
    """Block-level ``ballStart`` must match a player id in the same block."""
    findings: list[Finding] = []
    for p in pages:
        if not _is_play_page(p):
            continue
        for block, line_no in _play_blocks(p):
            ball_start = block.get("ballStart")
            if ball_start is None:
                continue
            known_ids: set[str] = set()
            players = block.get("players")
            if isinstance(players, list):
                for entry in players:
                    if isinstance(entry, dict) and entry.get("role") is not None:
                        known_ids.add(str(entry["role"]))
            if str(ball_start) not in known_ids:
                findings.append(
                    Finding(
                        check="play-ballstart-known",
                        severity="warning",
                        file=p.file_path,
                        line=line_no,
                        message=(
                            f"ballStart={ball_start!r} not in the block's "
                            "players roster"
                        ),
                    )
                )
    return findings


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def _group_by_check(findings: list[Finding]) -> dict[CheckId, list[Finding]]:
    out: dict[CheckId, list[Finding]] = {}
    for f in findings:
        out.setdefault(f.check, []).append(f)
    return out


def _rel_path(p: str, reference: Path) -> str:
    base = str(reference)
    if p.startswith(base):
        return p[len(base) + 1 :]
    return p


def build_report(
    total_pages: int,
    findings: list[Finding],
    reference: Path,
    now: datetime | None = None,
) -> str:
    grouped = _group_by_check(findings)
    date = (now or datetime.now(UTC)).strftime("%Y-%m-%d")
    lines: list[str] = []
    lines.append(f"# Wiki Lint Report — {date}")
    lines.append("")
    lines.append("> Automated read-only audit of `backend/knowledge-base/wiki/` against SCHEMA.md.")
    lines.append("> Generated by `scripts/lint-wiki.ts`. Do not edit by hand.")
    lines.append("")
    lines.append(f"- **Pages scanned**: {total_pages}")
    lines.append(f"- **Total findings**: {len(findings)}")
    counts = {
        "error": sum(1 for f in findings if f.severity == "error"),
        "warning": sum(1 for f in findings if f.severity == "warning"),
        "info": sum(1 for f in findings if f.severity == "info"),
    }
    lines.append(
        f"- **Severity breakdown**: error={counts['error']}, "
        f"warning={counts['warning']}, info={counts['info']}"
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Check | Severity | Count | Recommendation |")
    lines.append("|-------|----------|-------|----------------|")
    for spec in _CHECK_CATALOG:
        items = grouped.get(spec.id, [])
        sev: Severity = "info"
        for f in items:
            if sev == "error" or f.severity == "error":
                sev = "error"
                continue
            if sev == "warning" or f.severity == "warning":
                sev = "warning"
        rec = spec.recommendation.replace("|", r"\|")
        lines.append(f"| {spec.title} | {sev} | {len(items)} | {rec} |")
    lines.append("")
    for spec in _CHECK_CATALOG:
        items = grouped.get(spec.id, [])
        lines.append(f"## {spec.title} ({len(items)})")
        lines.append("")
        if not items:
            lines.append("_No findings._")
            lines.append("")
            continue
        lines.append(f"**Recommendation**: {spec.recommendation}")
        lines.append("")
        lines.append("| # | Severity | File | Line | Message |")
        lines.append("|---|----------|------|------|---------|")
        sample = items[:20]
        for i, f in enumerate(sample):
            line_part = str(f.line) if f.line else "—"
            msg = f.message.replace("|", r"\|")[:300]
            lines.append(
                f"| {i + 1} | {f.severity} | `{_rel_path(f.file, reference)}` | "
                f"{line_part} | {msg} |"
            )
        if len(items) > len(sample):
            lines.append("")
            lines.append(f"_Showing first 20 of {len(items)}._")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def run_lint(wiki_directory: Path) -> tuple[int, list[Finding]]:
    """Run every check against ``wiki_directory`` and return findings."""
    if not wiki_directory.is_dir():
        raise FileNotFoundError(f"Wiki directory not found: {wiki_directory}")
    file_names = _list_wiki_pages(wiki_directory)
    pages = [_load_page(wiki_directory, f) for f in file_names]
    slug_set: frozenset[str] = frozenset(p.slug for p in pages)

    findings: list[Finding] = []
    findings.extend(_check_filenames(pages))
    findings.extend(_check_duplicate_slugs(pages))
    findings.extend(_check_dead_wikilinks(pages, slug_set))
    findings.extend(_check_orphans(pages))
    findings.extend(_check_bidirectional(pages, slug_set))
    findings.extend(_check_stale_diagrams(pages))
    findings.extend(_check_missing_citations(pages))
    findings.extend(_check_schema_sections(pages))
    findings.extend(_check_duplicate_index_entries(pages))
    findings.extend(_check_gap_concepts(pages, slug_set, wiki_directory))
    # Play-geometry checks.
    findings.extend(_check_play_diagram_per_phase(pages))
    findings.extend(_check_play_path_valid_svg(pages))
    findings.extend(_check_play_path_roles_resolve(pages))
    findings.extend(_check_play_duration_sane(pages))
    findings.extend(_check_play_ballstart_known(pages))
    return len(pages), findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="wiki-lint",
        description="Read-only audit of the wiki against SCHEMA.md.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help=(
            "Reference directory for the audit report output path and for "
            "relative file paths in the report body. Defaults to frontend/."
        ),
    )
    parser.add_argument("--wiki-dir", type=Path, default=None, help="Override the wiki directory.")
    parser.add_argument(
        "--sport",
        default=DEFAULT_SPORT,
        choices=("basketball", "football"),
        help="Sport wiki to lint (default: basketball).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Override the report output path entirely.",
    )
    parser.add_argument(
        "--elapsed-ms",
        type=int,
        default=None,
        help=(
            "Force a fixed elapsed-time value in milliseconds (for parity "
            "tests — removes timing jitter from stdout output)."
        ),
    )
    args = parser.parse_args(argv)

    reference = args.root if args.root is not None else frontend_root()
    wiki_directory = wiki_dir(args.wiki_dir, sport=args.sport)
    sys.stdout.write(f"[lint-wiki] sport: {args.sport}\n")
    t0 = time.monotonic()
    try:
        total_pages, findings = run_lint(wiki_directory)
    except Exception as exc:
        sys.stderr.write(f"[lint-wiki] fatal: {exc}\n")
        return 2
    report = build_report(total_pages, findings, reference=reference)
    if args.report is not None:
        report_path = args.report
    else:
        stamp = datetime.now(UTC).strftime("%Y-%m-%d")
        report_path = reference / "docs" / "audits" / f"wiki-lint-{stamp}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    by_check = _group_by_check(findings)
    if args.elapsed_ms is not None:
        elapsed = args.elapsed_ms
    else:
        elapsed = int((time.monotonic() - t0) * 1000)
    sys.stdout.write(
        f"[lint-wiki] scanned {total_pages} pages in {elapsed}ms — {len(findings)} findings\n"
    )
    for spec in _CHECK_CATALOG:
        items = by_check.get(spec.id, [])
        if not items:
            continue
        sys.stdout.write(f"  - {spec.title}: {len(items)}\n")
    sys.stdout.write(f"[lint-wiki] report written to {_rel_path(str(report_path), reference)}\n")
    critical = [f for f in findings if f.severity in _CRITICAL_SEVERITIES]
    if critical:
        sys.stdout.write(f"[lint-wiki] {len(critical)} error-level finding(s) — exit 1\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
