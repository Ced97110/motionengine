"""Wiki → V7Play importer.

Reads a ``knowledge-base/wiki/<slug>.md`` page and assembles a V7Play draft
directly from the structured ``json name=diagram-positions`` blocks that
already live in the wiki. Bypasses the prose-extraction LLM when the wiki
already carries author-authored coordinates and action lists.

Three outcome tiers:

- ``wiki-structured`` — one diagram block per phase (1:1 alignment).
- ``wiki-partial``    — fewer blocks than phases; coarse mapping (single
  block spread across all phases, duplicated with a TODO).
- ``wiki-no-diagram`` — no blocks at all; returns ``play=None`` and points
  the caller at the prose extractor.

Non-goals:
- SVG curve authoring (paths are straight-line synthesized, same as the
  prose extractor).
- Defender generation. Wiki diagrams rarely carry defender coords; we
  leave ``defense`` at a conservative default and flag it in TODOs.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from motion.services.play_extractor import _synthesize_action_paths
from motion.wiki_ops.frontmatter import parse_full
from motion.wiki_ops.paths import wiki_dir

ImportSource = Literal["wiki-structured", "wiki-partial", "wiki-no-diagram"]


@dataclass(frozen=True)
class ImportResult:
    """Outcome of an import attempt."""

    play: dict[str, Any] | None
    todos: list[str]
    source: ImportSource


@dataclass
class _DiagramBlock:
    """One parsed ``json name=diagram-positions`` fenced block."""

    data: dict[str, Any]
    notes: str
    # Phase number referenced in ``notes`` ("Phase 1" / "Phase 2"), if any.
    phase_num: int | None = None


@dataclass
class _PhaseSection:
    """One ``### Phase N: Label`` section."""

    number: int
    label: str
    text: str
    # Indices into the diagram-block list that belong to this phase.
    block_indices: list[int] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Constants: role destinations → [x, y] on the V7 half-court frame.
# ---------------------------------------------------------------------------

_ROLE_DESTINATIONS: dict[str, tuple[float, float]] = {
    "right_wing": (18, 22),
    "left_wing": (-18, 22),
    "top": (0, 33),
    "right_corner": (22, 5),
    "left_corner": (-22, 5),
    "right_elbow": (8, 29),
    "left_elbow": (-8, 29),
    "basket": (0, 4),
    "rim": (0, 4),
    "left_block": (-6, 7),
    "right_block": (6, 7),
    "ball_side_corner": (22, 5),  # default to right; caller overrides if needed.
    "weak_side_corner": (-22, 5),
    "weak_side_wing": (-18, 22),
    "ball_side_wing": (18, 22),
    "high_post": (0, 18),
    "low_post": (0, 7),
    "free_throw_line": (0, 19),
    "paint": (0, 8),
    "key": (0, 18),
}

# ---------------------------------------------------------------------------
# Action type → V7 marker mapping.
# ---------------------------------------------------------------------------

_ACTION_MARKER_MAP: dict[str, tuple[str, bool]] = {
    # type → (marker, dashed)
    "cut": ("arrow", False),
    "drive": ("arrow", False),
    "move": ("arrow", False),
    "pass": ("arrow", True),
    "screen": ("screen", False),
    "down-screen": ("screen", False),
    "back-screen": ("screen", False),
    "flare-screen": ("screen", False),
    "cross-screen": ("screen", False),
    "pin-down": ("screen", False),
    "dribble": ("dribble", False),
    "dribble-pass": ("dribble", False),
    "handoff": ("handoff", False),
    "dho": ("handoff", False),
    "shot": ("shot", False),
    "shoot": ("shot", False),
    "finish": ("shot", False),
}

# ---------------------------------------------------------------------------
# Regexes for wiki structure.
# ---------------------------------------------------------------------------

# Opening fence can be ```json name=diagram-positions OR ``` json name=...
_DIAGRAM_FENCE_RE = re.compile(
    r"```\s*json\s+name=diagram-positions\s*\n(?P<body>.*?)\n```",
    re.DOTALL,
)

# Phase header: "### Phase 1: Label"  (also tolerate "### Phase 1 —" and no colon).
_PHASE_HEADER_RE = re.compile(
    r"^###\s+Phase\s+(?P<num>\d+)\s*[:\-—]?\s*(?P<label>.*?)\s*$",
    re.MULTILINE,
)

_PHASE_REFERENCE_RE = re.compile(r"Phase\s+(\d+)", re.IGNORECASE)

# H1 heading for play name (first "# Heading" after frontmatter).
_H1_RE = re.compile(r"^#\s+(?P<name>.+?)\s*$", re.MULTILINE)

# Overview paragraph section (## Overview ... first non-blank line).
_OVERVIEW_RE = re.compile(
    r"^##\s+Overview\s*\n(?P<body>[\s\S]*?)(?=^##\s|\Z)",
    re.MULTILINE,
)

# Related Plays wikilinks.
_RELATED_RE = re.compile(
    r"^##\s+Related\s+Plays\s*\n(?P<body>[\s\S]*?)(?=^##\s|\Z)",
    re.MULTILINE,
)
_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

# Source citations like "[S4, p.56]" — strip for cleaner desc.
_SOURCE_CITATION_RE = re.compile(r"\s*\[S\d+,[^\]]*\]")

# Default 5-player roster + defense (used when wiki omits them).
_DEFAULT_ROSTER: dict[str, dict[str, str]] = {
    "1": {"name": "PG", "pos": "PG"},
    "2": {"name": "SG", "pos": "SG"},
    "3": {"name": "SF", "pos": "SF"},
    "4": {"name": "PF", "pos": "PF"},
    "5": {"name": "C", "pos": "C"},
}
_DEFAULT_DEFENSE: dict[str, list[float]] = {
    "X1": [0, 30],
    "X2": [-14, 22],
    "X3": [14, 22],
    "X4": [-18, 8],
    "X5": [18, 8],
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def _resolve_wiki_path(slug: str, wiki_root: Path) -> Path:
    """Resolve ``slug`` to ``<wiki_root>/<slug>.md`` with a traversal guard.

    Rejects slugs containing path separators or parent-dir references, then
    resolves the final path and asserts the wiki root is an ancestor. A
    ``ValueError`` is raised on any suspicion of traversal.
    """
    if not slug or Path(slug).name != slug or "/" in slug or "\\" in slug or ".." in slug:
        raise ValueError(f"invalid slug: {slug!r}")
    candidate = (wiki_root / f"{slug}.md").resolve()
    wiki_root_resolved = wiki_root.resolve()
    if wiki_root_resolved != candidate.parent:
        raise ValueError(f"slug path escapes wiki dir: {slug!r}")
    return candidate


def list_importable_wiki_plays() -> list[dict[str, Any]]:
    """Inventory every ``type: play`` page in the wiki.

    Returns one entry per page with slug, display name, phase count, and
    whether at least one diagram block is present. The lab uses this to
    render a picker.
    """
    root = wiki_dir()
    entries: list[dict[str, Any]] = []
    for md_path in sorted(root.glob("*.md")):
        try:
            raw = md_path.read_text(encoding="utf-8")
        except OSError:
            continue
        data, body = parse_full(raw)
        if data.get("type") != "play":
            continue
        blocks = _extract_diagram_blocks(body)
        phases = _extract_phase_sections(body)
        name = _extract_name(body) or md_path.stem
        entries.append(
            {
                "slug": md_path.stem,
                "name": name,
                "phaseCount": len(phases),
                "hasDiagram": bool(blocks),
                "blockCount": len(blocks),
            }
        )
    return entries


def import_wiki_play(slug: str) -> ImportResult:
    """Build a V7Play draft from ``<wiki>/<slug>.md``.

    Returns ``source="wiki-no-diagram"`` (with ``play=None``) if the page
    has no diagram blocks — the caller should route those through the
    prose extractor instead.
    """
    root = wiki_dir()
    path = _resolve_wiki_path(slug, root)
    if not path.is_file():
        raise FileNotFoundError(f"wiki page not found: {slug}")
    raw = path.read_text(encoding="utf-8")
    frontmatter, body = parse_full(raw)
    if frontmatter.get("type") != "play":
        raise ValueError(f"{slug} is not a type:play page")

    blocks = _extract_diagram_blocks(body)
    phases = _extract_phase_sections(body)

    if not blocks:
        return ImportResult(
            play=None,
            todos=[
                "No diagram-positions blocks in this wiki page — use the "
                "prose extractor instead (/api/playlab/extract-prose)."
            ],
            source="wiki-no-diagram",
        )

    todos: list[str] = []

    # ---- Meta from frontmatter + body ----
    name = _extract_name(body) or slug
    tag = _extract_tag(frontmatter)
    desc = _extract_desc(body)
    related = _extract_related(body)

    # ---- Players / ball-handler from first block ----
    players, ball_start = _extract_players_and_ball(blocks[0].data)

    # ---- Phase → block assignment ----
    _assign_blocks_to_phases(blocks, phases)
    source_tier = _determine_source_tier(blocks, phases)

    v7_phases, phase_todos = _build_phases(phases, blocks, players)
    todos.extend(phase_todos)

    if source_tier == "wiki-partial":
        todos.append(
            "Fewer diagram blocks than phase sections — the single block was "
            "duplicated across all phases. Edit each phase to reflect its actual "
            "action sequence."
        )

    # Flag any diagram blocks that never got assigned to a phase.
    used_indices = {idx for p in phases for idx in p.block_indices}
    unused = [i for i in range(len(blocks)) if i not in used_indices]
    if unused and phases:
        todos.append(
            f"{len(unused)} diagram block(s) not bound to a phase section — "
            "these usually represent option trees or counter actions. Review "
            "the wiki page and decide whether to split phases further."
        )

    play = {
        "name": name,
        "tag": tag,
        "desc": desc,
        "coachNote": "",
        "concepts": {
            "counters": [],
            "bestFor": "",
            "related": related,
        },
        "players": {pid: list(coord) for pid, coord in players.items()},
        "roster": dict(_DEFAULT_ROSTER),
        "defense": {k: list(v) for k, v in _DEFAULT_DEFENSE.items()},
        "ballStart": ball_start,
        "phases": v7_phases,
        "branchPoint": None,
    }

    _synthesize_action_paths(play)

    todos.append(
        "defense coords + roster names are template defaults — wiki diagrams "
        "do not carry defender positions."
    )
    todos.append(
        "paths are straight-line synthesized — redraw curves in the lab for "
        "realistic motion."
    )

    return ImportResult(play=play, todos=todos, source=source_tier)


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


def _extract_diagram_blocks(body: str) -> list[_DiagramBlock]:
    """Pull every ``json name=diagram-positions`` fenced block in order."""
    blocks: list[_DiagramBlock] = []
    for match in _DIAGRAM_FENCE_RE.finditer(body):
        raw_json = match.group("body").strip()
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        notes = str(data.get("notes") or "")
        phase_num = _infer_phase_num(notes)
        blocks.append(_DiagramBlock(data=data, notes=notes, phase_num=phase_num))
    return blocks


def _infer_phase_num(notes: str) -> int | None:
    """Pull the first ``Phase N`` reference out of diagram ``notes``."""
    match = _PHASE_REFERENCE_RE.search(notes)
    if match is None:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def _extract_phase_sections(body: str) -> list[_PhaseSection]:
    """Return every ``### Phase N: Label`` section with its prose text."""
    matches = list(_PHASE_HEADER_RE.finditer(body))
    sections: list[_PhaseSection] = []
    for i, match in enumerate(matches):
        number = int(match.group("num"))
        label = match.group("label").strip() or f"Phase {number}"
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        raw_text = body[start:end]
        # Drop any fenced code blocks so phase text is prose only.
        cleaned = _DIAGRAM_FENCE_RE.sub("", raw_text).strip()
        sections.append(_PhaseSection(number=number, label=label, text=cleaned))
    return sections


def _extract_name(body: str) -> str | None:
    """First ``# Heading`` after the frontmatter is the display name."""
    match = _H1_RE.search(body)
    return match.group("name").strip() if match else None


def _extract_tag(frontmatter: dict[str, Any]) -> str:
    """Prefer ``category`` from frontmatter, else first tag, else empty."""
    category = frontmatter.get("category")
    if isinstance(category, str) and category.strip():
        return category.strip()
    tags = frontmatter.get("tags")
    if isinstance(tags, list) and tags:
        first = tags[0]
        if isinstance(first, str):
            return first.strip()
    return ""


def _extract_desc(body: str) -> str:
    """Pull the first paragraph under ``## Overview`` (citations stripped)."""
    match = _OVERVIEW_RE.search(body)
    if match is None:
        return ""
    block = match.group("body").strip()
    # First paragraph = everything up to the first blank line.
    paragraph = block.split("\n\n", 1)[0].strip()
    paragraph = _SOURCE_CITATION_RE.sub("", paragraph)
    return paragraph.strip()


def _extract_related(body: str) -> list[str]:
    """Extract wikilinked slugs from the ``## Related Plays`` section."""
    match = _RELATED_RE.search(body)
    if match is None:
        return []
    found = _WIKILINK_RE.findall(match.group("body"))
    return [slug.strip() for slug in found if slug.strip()]


# ---------------------------------------------------------------------------
# Player & action extraction
# ---------------------------------------------------------------------------


def _extract_players_and_ball(block: dict[str, Any]) -> tuple[dict[str, tuple[float, float]], str]:
    """Read the first block's ``players`` array → V7 ``players`` map.

    Ball-handler defaults to role "1" when present, else the first listed role.
    """
    raw_players = block.get("players")
    players: dict[str, tuple[float, float]] = {}
    if isinstance(raw_players, list):
        for entry in raw_players:
            if not isinstance(entry, dict):
                continue
            role = entry.get("role")
            x = entry.get("x")
            y = entry.get("y")
            if not isinstance(role, (str, int)):
                continue
            role_str = str(role)
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                continue
            players[role_str] = (float(x), float(y))
    if not players:
        # Fall back to a 5-out formation so the lab doesn't render an empty court.
        players = {
            "1": (0, 32),
            "2": (-16, 24),
            "3": (16, 24),
            "4": (-20, 6),
            "5": (20, 6),
        }
    ball_start = "1" if "1" in players else next(iter(players))
    return players, ball_start


def _resolve_destination(
    dest: Any,
    players: dict[str, tuple[float, float]],
) -> tuple[float, float] | None:
    """Map an action ``to`` field to an ``[x, y]`` coord.

    Accepts numeric role ids (match against ``players``) and named zones
    (``right_wing``, ``rim``, etc.). Returns ``None`` if unresolvable — the
    caller is expected to record a TODO and drop the ``move`` field.
    """
    if isinstance(dest, list) and len(dest) == 2:
        try:
            return float(dest[0]), float(dest[1])
        except (TypeError, ValueError):
            return None
    if not isinstance(dest, str):
        return None
    key = dest.strip().lower().replace("-", "_").replace(" ", "_")
    if key in _ROLE_DESTINATIONS:
        return _ROLE_DESTINATIONS[key]
    if dest in players:
        return players[dest]
    return None


def _convert_actions(
    raw_actions: Any,
    players: dict[str, tuple[float, float]],
    phase_label: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Map wiki ``actions[]`` → V7 ``actions[]`` + collect TODOs."""
    todos: list[str] = []
    v7_actions: list[dict[str, Any]] = []
    if not isinstance(raw_actions, list):
        return v7_actions, todos
    seen_unmapped: set[str] = set()
    for raw in raw_actions:
        if not isinstance(raw, dict):
            continue
        atype_raw = raw.get("type")
        atype = str(atype_raw).strip().lower() if isinstance(atype_raw, str) else ""
        mapped = _ACTION_MARKER_MAP.get(atype)
        if mapped is None:
            marker, dashed = "arrow", False
            if atype and atype not in seen_unmapped:
                seen_unmapped.add(atype)
                todos.append(
                    f"[{phase_label}] unmapped action.type: {atype!r} — defaulted to 'arrow'."
                )
        else:
            marker, dashed = mapped

        mover_id = raw.get("from")
        if not isinstance(mover_id, (str, int)):
            continue
        mover_id = str(mover_id)

        action: dict[str, Any] = {"marker": marker, "path": ""}
        if dashed:
            action["dashed"] = True

        # Pass actions get rendered as ball travel, not player motion — skip `move`
        # when the "from" is a player and the "to" is another player (classic pass).
        dest_coord = _resolve_destination(raw.get("to"), players)
        if atype == "pass" and isinstance(raw.get("to"), str) and raw.get("to") in players:
            # Emit as ball travel between the two player ids.
            action["ball"] = {"from": mover_id, "to": str(raw.get("to"))}
        elif dest_coord is not None and mover_id in players:
            action["move"] = {"id": mover_id, "to": [dest_coord[0], dest_coord[1]]}
        elif dest_coord is None:
            todos.append(
                f"[{phase_label}] unresolved destination {raw.get('to')!r} for "
                f"{mover_id} ({atype or 'unknown'}) — skipped move."
            )

        v7_actions.append(action)
    return v7_actions, todos


# ---------------------------------------------------------------------------
# Phase ↔ block alignment
# ---------------------------------------------------------------------------


def _assign_blocks_to_phases(
    blocks: list[_DiagramBlock],
    phases: list[_PhaseSection],
) -> None:
    """Mutate ``phases`` so each records the diagram-block indices it owns.

    Strategy:
    1. If block.notes references "Phase N" and a matching phase exists, assign.
    2. Remaining unassigned blocks are distributed in document order across
       phases that still have no blocks.
    3. Phases with no block at end of pass 2 remain empty — caller decides
       whether to duplicate the first block across them (``wiki-partial``).
    """
    if not phases:
        return
    phase_by_num = {p.number: p for p in phases}

    # Pass 1 — explicit "Phase N" notes.
    unassigned_indices: list[int] = []
    for idx, block in enumerate(blocks):
        target = phase_by_num.get(block.phase_num) if block.phase_num else None
        if target is not None:
            target.block_indices.append(idx)
        else:
            unassigned_indices.append(idx)

    # Pass 2 — distribute leftovers to phases that still have nothing, in order.
    empty_phases = [p for p in phases if not p.block_indices]
    for phase, idx in zip(empty_phases, unassigned_indices, strict=False):
        phase.block_indices.append(idx)


def _determine_source_tier(
    blocks: list[_DiagramBlock],
    phases: list[_PhaseSection],
) -> ImportSource:
    """Pick the tier label based on block ↔ phase coverage."""
    if not blocks:
        return "wiki-no-diagram"
    if not phases:
        # Single diagram, no explicit phases: treat as partial so the caller
        # knows they are looking at a coarse draft.
        return "wiki-partial"
    phases_with_block = sum(1 for p in phases if p.block_indices)
    if phases_with_block == len(phases) and len(blocks) >= len(phases):
        return "wiki-structured"
    return "wiki-partial"


def _build_phases(
    phase_sections: list[_PhaseSection],
    blocks: list[_DiagramBlock],
    players: dict[str, tuple[float, float]],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Assemble V7 phases from parsed phase sections + aligned diagram blocks."""
    todos: list[str] = []
    v7_phases: list[dict[str, Any]] = []

    # No structured phases → emit one synthetic phase per block.
    if not phase_sections:
        for idx, block in enumerate(blocks, start=1):
            actions, action_todos = _convert_actions(
                block.data.get("actions"), players, f"Phase {idx}"
            )
            todos.extend(action_todos)
            v7_phases.append(
                {
                    "label": f"Phase {idx}",
                    "text": block.notes,
                    "actions": actions,
                    "defenseActions": [],
                }
            )
        return v7_phases, todos

    # Track which blocks are still unused (future feature: merge into text).
    for phase in phase_sections:
        # Pick the block for this phase (first assigned; fall back to blocks[0]).
        block_idx = phase.block_indices[0] if phase.block_indices else 0
        block = blocks[block_idx]
        actions, action_todos = _convert_actions(
            block.data.get("actions"), players, phase.label
        )
        todos.extend(action_todos)
        v7_phases.append(
            {
                "label": phase.label,
                "text": phase.text,
                "actions": actions,
                "defenseActions": [],
            }
        )

    return v7_phases, todos
