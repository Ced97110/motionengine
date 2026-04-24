"""Annotate a single play page with demands_techniques + demands_anatomy.

Targeted backfill harness for the cross-reference moat. Reads a play page,
emits structured YAML via Claude (using ``play-black.md`` as the few-shot
example and existing ``concept-anatomy-*`` slugs as the allowlist), then
splices the additions into the page's existing frontmatter. The body
(prose, ``json name=diagram-positions`` blocks, citations) is byte-preserved.

Defaults to dry-run (prints a unified diff). Pass ``--write`` to commit.

Usage::

    uv run python -m motion.wiki_ops.backfill_crossref play-iverson-ram
    uv run python -m motion.wiki_ops.backfill_crossref play-iverson-ram --write

Refuses to write if the page already carries ``demands_techniques`` or
``demands_anatomy`` — re-runs are explicit, never silent overwrites.

Per CLAUDE.md eval discipline this is intentionally narrow: one play, one
prompt, manual review of the diff. Once the iverson-ram run is validated
by the user, the captured input/output pair becomes the seed of an eval
fixture before generalising the harness to the remaining 60 plays.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import anthropic

from motion.wiki_ops.paths import wiki_dir

_PLAY_SYSTEM_PROMPT = """You are annotating basketball play pages with structured \
cross-reference fields that compile into the Motion Engine's retrieval graph.

For the given play, emit two fields via the `emit_demands` tool:

- demands_techniques: list of {id, role, criticality}
  - id: kebab-case slug stem of a `concept-technique-*` page. You MAY invent
    a slug when no existing concept page covers the technique — lint will
    flag the dangling reference as a gap to author later.
  - role: digit "1"-"5" matching the play's player set.
  - criticality: "required" when the play's primary read fails without the
    skill; "optional" for variants and counter actions.

- demands_anatomy: list of {region, criticality, supports_technique, for_role}
  - region: snake_case stem of a `concept-anatomy-*` page (e.g.
    `hip_flexor_complex`). MUST appear in the provided allowlist — do NOT
    invent anatomy slugs. If the play loads a body region with no concept
    page yet, omit that entry rather than fabricate a slug.
  - supports_technique: must equal one of the `demands_techniques.id` you
    emit (this is the link that compiles the play→technique→anatomy chain).
  - for_role: which role's body system is loaded.

Reasoning approach: walk the play's `## Phases` prose; for each role's
movement, name the technique that movement requires, then the anatomy that
technique loads. Mirror the few-shot's level of granularity (4-6 techniques,
2-4 anatomy entries is typical). Required vs optional reflects whether the
play's primary read depends on the skill.
"""

_SIGNATURE_SYSTEM_PROMPT = """You are annotating basketball play pages with their \
Four-Factor analytic signature — which statistical factors the play lifts, \
lowers, or protects by design. This output is the structural input to the \
Motion Engine's analytics chain (edge #8).

For the given play, emit the `produces_signature` field via the `emit_signature` tool.

Each signature entry carries:

- factor: kebab-case slug from the allowed set: efg-pct, ftr, tov-pct, oreb-pct,
  floor-pct, ppp, pace. Use only these — factors outside the set will be rejected.
- direction: one of "lifts", "protects", "lowers", "raises".
  * "lifts" = the play reliably increases this factor by design
  * "protects" = the play reliably prevents degradation (used for tov-pct)
  * "lowers" = the play depresses this factor by design (e.g. pace on a deep set)
  * "raises" = synonym for lifts; prefer "lifts"
- concept_slug: always "concept-four-factors" for Four-Factor entries.
- magnitude: "high", "medium", or "low" — the author's confidence in the direction.
- rationale: ONE short sentence in your own words explaining why this direction
  holds, grounded in the play's mechanics (NOT citing any source book).
  Compose the rationale from the play's described action alone; do NOT quote
  or paraphrase any book prose, coaching cue, or symptom line.

Reasoning approach: read the play's `## Overview` + `## Phases`. Ask: does
this action target a layup or open 3 (lifts efg-pct)? Does it limit passes
(protects tov-pct)? Does it invite closeout contact (lifts ftr)? Does it
force offensive rebounds (lifts oreb-pct)? A typical annotated play carries
2-4 factors. Omit any factor you cannot cleanly justify from the mechanics.

Book-derived prose must not surface in the rationale. Only structural
references (role numbers, action slugs, factor names) may appear.
"""

_DRILL_SYSTEM_PROMPT = """You are annotating basketball drill pages with structured \
cross-reference fields that compile into the Motion Engine's retrieval graph.

For the given drill, emit two fields via the `emit_trains` tool:

- trains_techniques: list of {id, emphasis}
  - id: kebab-case slug stem of a `concept-technique-*` page. You MAY invent
    a slug when no existing concept page covers the technique. Prefer slugs
    already referenced on the play side (i.e., present in the corpus's
    technique vocabulary) so drills resolve into the play→drill graph.
  - emphasis: "primary" when the drill's main purpose is training this
    technique; "secondary" when it's a supporting effect.

- trains_anatomy: list of {region, emphasis}
  - region: snake_case stem of a `concept-anatomy-*` page (e.g.
    `hip_flexor_complex`). MUST appear in the provided allowlist — do NOT
    invent anatomy slugs. Omit regions without a concept page.
  - emphasis: "primary" for regions the drill directly loads; "secondary"
    for regions that get collateral benefit.

Reasoning approach: read the drill's `## Objective`, `## Execution`, and
`## Coaching Points` sections. The objective tells you the headline
technique + region. The execution tells you secondary regions. Typical
output: 1-2 techniques, 1-3 anatomy regions. Emphasis "primary" should be
rare and justified by the objective, not the setup.
"""

_PLAY_TOOL_DEF: dict[str, Any] = {
    "name": "emit_demands",
    "description": "Emit demands_techniques + demands_anatomy structured fields.",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["demands_techniques", "demands_anatomy"],
        "properties": {
            "demands_techniques": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "role", "criticality"],
                    "properties": {
                        "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                        "role": {"type": "string", "enum": ["1", "2", "3", "4", "5"]},
                        "criticality": {
                            "type": "string",
                            "enum": ["required", "optional"],
                        },
                    },
                },
            },
            "demands_anatomy": {
                "type": "array",
                "minItems": 0,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "region",
                        "criticality",
                        "supports_technique",
                        "for_role",
                    ],
                    "properties": {
                        "region": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
                        "criticality": {
                            "type": "string",
                            "enum": ["required", "optional"],
                        },
                        "supports_technique": {
                            "type": "string",
                            "pattern": "^[a-z][a-z0-9-]*$",
                        },
                        "for_role": {
                            "type": "string",
                            "enum": ["1", "2", "3", "4", "5"],
                        },
                    },
                },
            },
        },
    },
}

_SIGNATURE_FACTOR_ALLOWLIST: frozenset[str] = frozenset({
    "efg-pct",
    "ftr",
    "tov-pct",
    "oreb-pct",
    "floor-pct",
    "ppp",
    "pace",
})

_SIGNATURE_TOOL_DEF: dict[str, Any] = {
    "name": "emit_signature",
    "description": "Emit produces_signature structured field.",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["produces_signature"],
        "properties": {
            "produces_signature": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "factor",
                        "direction",
                        "concept_slug",
                        "magnitude",
                        "rationale",
                    ],
                    "properties": {
                        "factor": {
                            "type": "string",
                            "enum": sorted(_SIGNATURE_FACTOR_ALLOWLIST),
                        },
                        "direction": {
                            "type": "string",
                            "enum": ["lifts", "protects", "lowers", "raises"],
                        },
                        "concept_slug": {
                            "type": "string",
                            "pattern": "^[a-z][a-z0-9-]*$",
                        },
                        "magnitude": {
                            "type": "string",
                            "enum": ["high", "medium", "low"],
                        },
                        "rationale": {
                            "type": "string",
                            "minLength": 10,
                            "maxLength": 300,
                        },
                    },
                },
            },
        },
    },
}

_DRILL_TOOL_DEF: dict[str, Any] = {
    "name": "emit_trains",
    "description": "Emit trains_techniques + trains_anatomy structured fields.",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["trains_techniques", "trains_anatomy"],
        "properties": {
            "trains_techniques": {
                "type": "array",
                "minItems": 0,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "emphasis"],
                    "properties": {
                        "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                        "emphasis": {
                            "type": "string",
                            "enum": ["primary", "secondary"],
                        },
                    },
                },
            },
            "trains_anatomy": {
                "type": "array",
                "minItems": 0,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["region", "emphasis"],
                    "properties": {
                        "region": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
                        "emphasis": {
                            "type": "string",
                            "enum": ["primary", "secondary"],
                        },
                    },
                },
            },
        },
    },
}


def _list_anatomy_regions(root: Path) -> list[str]:
    """Return region slugs derived from existing ``concept-anatomy-*`` pages.

    Page slug ``concept-anatomy-hip-flexor-complex.md`` maps to region
    ``hip_flexor_complex`` (strip prefix, dashes → underscores) to match
    the convention ``play-black.md`` already uses for ``demands_anatomy.region``.
    """
    regions: list[str] = []
    for p in sorted(root.glob("concept-anatomy-*.md")):
        stem = p.stem.removeprefix("concept-anatomy-")
        regions.append(stem.replace("-", "_"))
    return regions


def _validate_play(out: dict[str, Any], allowed_regions: set[str]) -> list[str]:
    errs: list[str] = []
    tech_ids = {t["id"] for t in out["demands_techniques"]}
    for entry in out["demands_anatomy"]:
        if entry["region"] not in allowed_regions:
            errs.append(
                f"unknown anatomy region {entry['region']!r} — allowed: "
                f"{sorted(allowed_regions)}"
            )
        if entry["supports_technique"] not in tech_ids:
            errs.append(
                f"supports_technique {entry['supports_technique']!r} does not "
                f"appear in demands_techniques.id ({sorted(tech_ids)})"
            )
    return errs


def _validate_signature(out: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    seen_factors: set[str] = set()
    for entry in out["produces_signature"]:
        factor = entry.get("factor", "")
        if factor not in _SIGNATURE_FACTOR_ALLOWLIST:
            errs.append(
                f"unknown factor {factor!r} — allowed: "
                f"{sorted(_SIGNATURE_FACTOR_ALLOWLIST)}"
            )
        if factor in seen_factors:
            errs.append(f"duplicate factor {factor!r}")
        seen_factors.add(factor)
    return errs


def _validate_drill(out: dict[str, Any], allowed_regions: set[str]) -> list[str]:
    errs: list[str] = []
    for entry in out["trains_anatomy"]:
        if entry["region"] not in allowed_regions:
            errs.append(
                f"unknown anatomy region {entry['region']!r} — allowed: "
                f"{sorted(allowed_regions)}"
            )
    if not out["trains_techniques"] and not out["trains_anatomy"]:
        errs.append("drill emitted no trains_* entries — refusing empty annotation")
    return errs


def _emit_yaml_play(out: dict[str, Any]) -> str:
    """Hand-format play-side YAML to match ``play-black.md``'s two-space style."""
    lines: list[str] = []
    lines.append(
        "# Cross-ref edge #1 — anatomy chain. "
        "See backend/spec/crossref-anatomy-chain.md §4.1"
    )
    lines.append("demands_techniques:")
    for t in out["demands_techniques"]:
        lines.append(f"  - id: {t['id']}")
        lines.append(f'    role: "{t["role"]}"')
        lines.append(f"    criticality: {t['criticality']}")
    lines.append("demands_anatomy:")
    for a in out["demands_anatomy"]:
        lines.append(f"  - region: {a['region']}")
        lines.append(f"    criticality: {a['criticality']}")
        lines.append(f"    supports_technique: {a['supports_technique']}")
        lines.append(f'    for_role: "{a["for_role"]}"')
    return "\n".join(lines)


def _emit_yaml_signature(out: dict[str, Any]) -> str:
    """Hand-format signature-side YAML to match ``play-black.md``'s style."""
    lines: list[str] = []
    lines.append(
        "# Cross-ref edge #8 — analytic signature. "
        "See backend/spec/crossref-anatomy-chain.md §M4 signature expansion"
    )
    lines.append("produces_signature:")
    for s in out["produces_signature"]:
        lines.append(f"  - factor: {s['factor']}")
        lines.append(f"    direction: {s['direction']}")
        lines.append(f"    concept_slug: {s['concept_slug']}")
        lines.append(f"    magnitude: {s['magnitude']}")
        # Quote the rationale to guard against YAML-breaking characters.
        escaped = s["rationale"].replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'    rationale: "{escaped}"')
    return "\n".join(lines)


def _emit_yaml_drill(out: dict[str, Any]) -> str:
    """Hand-format drill-side YAML to match ``drill-ankling.md``'s style."""
    lines: list[str] = []
    lines.append(
        "# Cross-ref edge #1 — anatomy chain. "
        "See backend/spec/crossref-anatomy-chain.md §4.1"
    )
    if out["trains_techniques"]:
        lines.append("trains_techniques:")
        for t in out["trains_techniques"]:
            lines.append(f"  - id: {t['id']}")
            lines.append(f"    emphasis: {t['emphasis']}")
    if out["trains_anatomy"]:
        lines.append("trains_anatomy:")
        for a in out["trains_anatomy"]:
            lines.append(f"  - region: {a['region']}")
            lines.append(f"    emphasis: {a['emphasis']}")
    return "\n".join(lines)


_FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)


def _splice_frontmatter(
    raw: str, additions: str, forbid_keys: tuple[str, ...]
) -> str:
    """Append ``additions`` inside the existing leading YAML frontmatter.

    Surgical: every byte outside the frontmatter block is preserved.
    Raises if any of ``forbid_keys`` already appears in the frontmatter —
    explicit re-run only, never silent overwrite.
    """
    m = _FRONTMATTER_RE.match(raw)
    if not m:
        raise ValueError("no leading YAML frontmatter found")
    body = m.group("body")
    for key in forbid_keys:
        if key in body:
            raise ValueError(
                f"page already has {key.rstrip(':')} field — refusing to overwrite"
            )
    new_block = body.rstrip() + "\n" + additions
    return raw.replace(m.group(0), f"---\n{new_block}\n---\n", 1)


_PLAY_FEWSHOT = "play-black.md"
_DRILL_FEWSHOT = "drill-ankling.md"
_SIGNATURE_FEWSHOT = "play-black.md"
_PLAY_FORBID = ("demands_techniques:", "demands_anatomy:")
_DRILL_FORBID = ("trains_techniques:", "trains_anatomy:")
_SIGNATURE_FORBID = ("produces_signature:",)


def annotate(slug: str, write: bool, model: str, mode: str = "play") -> int:
    if mode not in ("play", "drill", "signature"):
        print(
            f"error: unknown mode {mode!r} (expected play|drill|signature)",
            file=sys.stderr,
        )
        return 2

    root = wiki_dir()
    target_path = root / f"{slug}.md"
    if not target_path.is_file():
        print(f"error: {target_path} not found", file=sys.stderr)
        return 2

    if mode == "play":
        fewshot_name = _PLAY_FEWSHOT
    elif mode == "drill":
        fewshot_name = _DRILL_FEWSHOT
    else:
        fewshot_name = _SIGNATURE_FEWSHOT
    fewshot_path = root / fewshot_name
    if not fewshot_path.is_file():
        print(
            f"error: {fewshot_name} missing — required as few-shot example",
            file=sys.stderr,
        )
        return 2

    target_raw = target_path.read_text(encoding="utf-8")
    fewshot_raw = fewshot_path.read_text(encoding="utf-8")
    allowed_regions = _list_anatomy_regions(root)

    if not allowed_regions:
        print(
            "error: no concept-anatomy-* pages found — anatomy allowlist empty",
            file=sys.stderr,
        )
        return 2

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2

    if mode == "play":
        system_prompt = _PLAY_SYSTEM_PROMPT
        tool_def = _PLAY_TOOL_DEF
        tool_name = "emit_demands"
        target_kind = "play"
        tool_call = "emit_demands"
    elif mode == "drill":
        system_prompt = _DRILL_SYSTEM_PROMPT
        tool_def = _DRILL_TOOL_DEF
        tool_name = "emit_trains"
        target_kind = "drill"
        tool_call = "emit_trains"
    else:
        system_prompt = _SIGNATURE_SYSTEM_PROMPT
        tool_def = _SIGNATURE_TOOL_DEF
        tool_name = "emit_signature"
        target_kind = "play"
        tool_call = "emit_signature"

    user_prompt = (
        "## Few-shot example (already annotated; mirror this structure)\n\n"
        f"{fewshot_raw}\n\n"
        "## Allowed anatomy region slugs (use ONLY these)\n"
        f"{json.dumps(allowed_regions, indent=2)}\n\n"
        f"## Target {target_kind} to annotate\n\n"
        f"{target_raw}\n\n"
        f"Emit the structured fields via the {tool_call} tool."
    )

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        tools=[tool_def],
        tool_choice={"type": "tool", "name": tool_name},
        messages=[{"role": "user", "content": user_prompt}],
    )
    tool_use = next((b for b in response.content if b.type == "tool_use"), None)
    if tool_use is None:
        print("error: model did not emit a tool_use block", file=sys.stderr)
        return 1
    out = dict(tool_use.input)  # type: ignore[arg-type]

    if mode == "play":
        errs = _validate_play(out, set(allowed_regions))
    elif mode == "drill":
        errs = _validate_drill(out, set(allowed_regions))
    else:
        errs = _validate_signature(out)
    if errs:
        for e in errs:
            print(f"validation error: {e}", file=sys.stderr)
        return 1

    if mode == "play":
        additions = _emit_yaml_play(out)
        forbid = _PLAY_FORBID
    elif mode == "drill":
        additions = _emit_yaml_drill(out)
        forbid = _DRILL_FORBID
    else:
        additions = _emit_yaml_signature(out)
        forbid = _SIGNATURE_FORBID
    try:
        new_raw = _splice_frontmatter(target_raw, additions, forbid)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    diff = "".join(
        difflib.unified_diff(
            target_raw.splitlines(keepends=True),
            new_raw.splitlines(keepends=True),
            fromfile=f"{slug}.md (before)",
            tofile=f"{slug}.md (after)",
            n=3,
        )
    )
    sys.stdout.write(diff)

    usage = response.usage
    print(
        f"\n[tokens] in={usage.input_tokens} out={usage.output_tokens}",
        file=sys.stderr,
    )

    if write:
        target_path.write_text(new_raw, encoding="utf-8")
        print(f"wrote: {target_path}", file=sys.stderr)
    else:
        print("(dry-run — pass --write to commit)", file=sys.stderr)

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="backfill-crossref", description=__doc__
    )
    parser.add_argument("slug", help="page slug stem, e.g. play-iverson-ram")
    parser.add_argument(
        "--mode",
        choices=("play", "drill", "signature"),
        default="play",
        help="play (demands_*), drill (trains_*), or signature (produces_signature)",
    )
    parser.add_argument(
        "--write", action="store_true", help="commit changes (default: dry-run)"
    )
    parser.add_argument(
        "--model", default="claude-sonnet-4-6", help="Claude model id"
    )
    args = parser.parse_args(argv)
    return annotate(args.slug, args.write, args.model, args.mode)


if __name__ == "__main__":
    sys.exit(main())
