"""Practice-plan composition — graph-grounded sibling of play_brief / form_brief.

Takes a :class:`motion.wiki_ops.retrieval.PracticeContext` and returns a
5-7 block timed practice plan in coach voice, grounded in the candidate
drill list the retrieval bundle pulled from the cross-ref graph.

Two modes:

- **Claude**: if ``ANTHROPIC_API_KEY`` is set, composes via Claude Sonnet 4.6
  with a strict structured-tool prompt.
- **Stub**: if no API key, returns a deterministic plan built from the
  candidate-drill list — coach still sees a usable plan, UX never dead-ends.

Output is a list of structured ``PracticeBlock`` (drill_slug + duration +
reasoning), not free-form prose. The router transforms these into the API
response shape; tests grade them via :func:`tests.eval._scoring.score_practice_brief`.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Any

import anthropic

from motion.prompts import get_prompts
from motion.sports import DEFAULT_SPORT, Sport
from motion.wiki_ops.retrieval import PracticeContext, PracticeDrillCandidate

_log = logging.getLogger(__name__)

_MODEL = "claude-sonnet-4-6"
_MAX_TOKENS = 1500
_CITATION_RE = re.compile(r"\[S\d+(?:,\s*pp?\.\s*[\d\-–]+)?\]")  # noqa: RUF001 (EN DASH intentional — matches typographic page ranges)
_SLUG_RE = re.compile(r"\b((?:concept|drill|exercise|play)-[a-z0-9][a-z0-9-]+)\b")


@dataclass(frozen=True)
class PracticeBlock:
    drill_slug: str
    duration_minutes: int
    reasoning: str
    cross_refs: list[str]


@dataclass(frozen=True)
class PracticeBriefResult:
    plan: list[PracticeBlock]
    source_citations: list[str]
    source: str  # "claude" | "stub"


def _extract_cross_refs(text: str) -> list[str]:
    """Pull every concept/drill/exercise/play slug out of `text`, deduped + ordered."""
    seen: set[str] = set()
    out: list[str] = []
    for match in _SLUG_RE.finditer(text):
        slug = match.group(1)
        if slug in seen:
            continue
        seen.add(slug)
        out.append(slug)
    return out


def _extract_citations(text: str) -> list[str]:
    seen: list[str] = []
    for match in _CITATION_RE.finditer(text):
        token = match.group(0)
        if token not in seen:
            seen.append(token)
    return seen


# --- stub mode ---------------------------------------------------------------


_STUB_BLOCK_PLAN: list[tuple[str, float, str]] = [
    # (label, fraction of total budget, coach-voice prose snippet) — used to
    # derive block durations and to bulk up reasoning for stub mode so it
    # passes the same length rubric as live mode.
    (
        "warm-up",
        0.10,
        "Open the body with controlled tempo. Watch knees stay over toes,"
        " feet quiet, shooting hand loose.",
    ),
    (
        "skill-block-1",
        0.25,
        "Build the core skill with high-rep precision. Slow the work down"
        " for form, then layer in tempo. Coach focus: hand and footwork"
        " alignment on every rep.",
    ),
    (
        "skill-block-2",
        0.20,
        "Stack a complementary skill that loads the same chain. Pair this"
        " with the prior block so the body groove carries over. Watch for"
        " release timing and balance through the move.",
    ),
    (
        "competitive-block",
        0.25,
        "Live or constrained competition — apply the skill under defensive"
        " pressure or a scoring rule. Run live tempo, count makes, and"
        " enforce the cue from the prior blocks. Coach scrimmage tone:"
        " talk, finish, compete on every possession.",
    ),
    (
        "cooldown",
        0.20,
        "Wind down with controlled shooting from the line — free throws,"
        " quiet feet, full follow-through. Light stretch to close. Players"
        " talk through one cue they want to carry into the next session.",
    ),
]


def _pick_stub_drills(
    candidates: list[PracticeDrillCandidate], n: int
) -> list[PracticeDrillCandidate]:
    """Pick the first n candidates with primary emphasis preferred."""
    primary = [c for c in candidates if c.emphasis == "primary"]
    secondary = [c for c in candidates if c.emphasis != "primary"]
    picked = primary[:n]
    if len(picked) < n:
        picked.extend(secondary[: n - len(picked)])
    return picked


def _build_stub(context: PracticeContext) -> PracticeBriefResult:
    """Deterministic plan from the candidate-drill list. Always works."""
    n_blocks = len(_STUB_BLOCK_PLAN)
    picks = _pick_stub_drills(context.candidate_drills, n_blocks)
    if not picks:
        picks = [
            PracticeDrillCandidate(
                drill_slug="drill-form-shooting",
                emphasis="primary",
                via_anatomy=None,
                via_technique=None,
                level=context.level,
                duration_minutes=10,
            )
        ] * n_blocks

    plan: list[PracticeBlock] = []
    budget = context.duration_minutes
    focus_phrase = ", ".join(context.focus_areas) or "general fundamentals"

    for idx, (label, frac, snippet) in enumerate(_STUB_BLOCK_PLAN):
        drill = picks[idx % len(picks)]
        block_dur = max(5, round(budget * frac))
        anatomy_hint = drill.via_anatomy or "core mechanics"
        reasoning = (
            f"{label.replace('-', ' ').title()}: run {drill.drill_slug} "
            f"({block_dur} min) to load {anatomy_hint.replace('_', ' ')} "
            f"and reinforce {focus_phrase}. {snippet}"
        )
        prose_refs = _extract_cross_refs(reasoning)
        cross_refs = [drill.drill_slug] + [
            r for r in prose_refs if r != drill.drill_slug
        ]
        plan.append(
            PracticeBlock(
                drill_slug=drill.drill_slug,
                duration_minutes=block_dur,
                reasoning=reasoning,
                cross_refs=cross_refs,
            )
        )
    return PracticeBriefResult(plan=plan, source_citations=[], source="stub")


# --- claude mode -------------------------------------------------------------


def _build_drill_table(context: PracticeContext) -> str:
    """Render the candidate-drill list as a compact table for the prompt."""
    if not context.candidate_drills:
        return "(no graph-matched drills available; pick from general knowledge)"
    lines: list[str] = []
    for c in context.candidate_drills:
        bits = [c.drill_slug, c.emphasis]
        if c.level:
            bits.append(c.level)
        if c.duration_minutes:
            bits.append(f"{c.duration_minutes}min")
        if c.via_anatomy:
            bits.append(f"trains {c.via_anatomy.replace('_', ' ')}")
        if c.via_technique:
            bits.append(f"trains {c.via_technique}")
        lines.append("  - " + " | ".join(bits))
    return "\n".join(lines)


def _build_text_prompt(
    context: PracticeContext, sport: Sport = DEFAULT_SPORT
) -> str:
    lines: list[str] = []
    lines.append(f"Level: {context.level}")
    lines.append(f"Total duration: {context.duration_minutes} min")
    lines.append(f"Focus areas: {', '.join(context.focus_areas) or '(none)'}")
    if context.anatomy:
        lines.append("Anatomy regions to ground the plan in:")
        for a in context.anatomy:
            lines.append(f"  - {a.region}  (concept page: {a.concept_slug})")
    if context.techniques:
        lines.append("Technique concepts available:")
        for t in context.techniques:
            lines.append(f"  - {t}")
    lines.append("")
    lines.append("Candidate drills (graph-matched, sorted primary-first):")
    lines.append(_build_drill_table(context))
    lines.append("")
    lines.append(_build_prompt_instructions(sport))
    return "\n".join(lines)


def _build_prompt_instructions(sport: Sport = DEFAULT_SPORT) -> str:
    """Assemble the practice prompt rules with the per-sport voice block."""
    prompts = get_prompts(sport)
    return (
        "Compose a practice plan that fits the total duration."
        " Use the `emit_practice_plan` tool to return structured blocks.\n"
        "\n"
        "RULES:\n"
        "- BLOCK COUNT — match block count to total duration so individual"
        " blocks stay long enough to be useful. Hard caps:\n"
        "  • 30 min → 4-5 blocks (do NOT exceed 6)\n"
        "  • 45 min → 5-6 blocks (do NOT exceed 7)\n"
        "  • 60 min → 5-7 blocks (do NOT exceed 7)\n"
        "  • 90 min → 6-7 blocks (do NOT exceed 7)\n"
        "  • 120 min → 7-8 blocks (do NOT exceed 8)\n"
        "- Each block has: drill_slug, duration_minutes (integer), reasoning"
        " (1-2 sentences in coach voice).\n"
        "- EVERY drill_slug MUST appear verbatim in the candidate list above."
        " Do NOT invent slugs. Do NOT use 'concept-*' slugs (those are wiki"
        " concept pages, not drills). Slugs MUST start with 'drill-' or"
        " 'exercise-'.\n"
        "- The sum of block durations MUST be within ±10% of the total"
        " duration above.\n"
        "- Cover the full arc: warm-up (5-10 min), skill blocks (the bulk),"
        " a competitive or scrimmage block, cooldown (3-5 min).\n"
        "- Do NOT invent drill slugs. If the candidate list is short, repeat"
        " a drill before inventing one.\n"
        "- Each reasoning sentence pairs the WHY (which anatomy region or"
        f" technique it loads, in {prompts.PRACTICE_BRIEF_REASONING_LANGUAGE}) "
        "with WHAT THE COACH"
        " SHOULD WATCH FOR during reps.\n"
        "\n"
        + prompts.PRACTICE_BRIEF_VOICE_BLOCK
        + "\n"
        "OTHER RULES:\n"
        "- Compose every reasoning sentence in your own words; do NOT quote"
        " or paraphrase any coaching cue or principle text from the context.\n"
        "- Book-derived prose must not surface; only structural slug"
        " references may.\n"
        "- Cite [Sn, p.X] tokens verbatim if you use them; do NOT invent"
        " citations."
    )


_PRACTICE_TOOL_DEF: dict[str, Any] = {
    "name": "emit_practice_plan",
    "description": "Emit a structured practice plan as a list of timed blocks.",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["blocks"],
        "properties": {
            "blocks": {
                "type": "array",
                "minItems": 4,
                "maxItems": 8,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["drill_slug", "duration_minutes", "reasoning"],
                    "properties": {
                        "drill_slug": {
                            "type": "string",
                            "pattern": "^(?:drill|exercise)-[a-z0-9][a-z0-9-]+$",
                        },
                        "duration_minutes": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 60,
                        },
                        "reasoning": {
                            "type": "string",
                            "minLength": 20,
                            "maxLength": 600,
                        },
                    },
                },
            }
        },
    },
}


def build_practice_brief(
    context: PracticeContext, sport: Sport = DEFAULT_SPORT
) -> PracticeBriefResult:
    """Compose a practice plan. Falls back to a stub if no API key is present."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return _build_stub(context)

    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            tools=[_PRACTICE_TOOL_DEF],
            tool_choice={"type": "tool", "name": "emit_practice_plan"},
            messages=[
                {
                    "role": "user",
                    "content": _build_text_prompt(context, sport),
                }
            ],
        )
        tool_use = next((b for b in message.content if b.type == "tool_use"), None)
        if tool_use is None:
            _log.warning("practice_brief: no tool_use in response, falling back to stub")
            return _build_stub(context)
        payload = tool_use.input
        if isinstance(payload, str):
            payload = json.loads(payload)
        raw_blocks = payload.get("blocks") or []
    except (anthropic.APIError, anthropic.APIConnectionError, json.JSONDecodeError) as exc:
        _log.warning("practice_brief: claude call failed (%s), falling back to stub", exc)
        return _build_stub(context)

    # Registry of slugs the composer is allowed to emit. The composer's
    # tool prompt says "drill_slug MUST be from the candidate list"; the
    # regex pattern is a backstop, but we also enforce membership here so
    # a hallucinated slug (e.g. concept-technique-*) doesn't reach the FE.
    candidate_slugs = [c.drill_slug for c in context.candidate_drills]
    candidate_set = set(candidate_slugs)
    candidate_iter = iter(candidate_slugs)

    plan: list[PracticeBlock] = []
    citations: list[str] = []
    for raw in raw_blocks:
        slug = raw.get("drill_slug")
        dur = raw.get("duration_minutes")
        reasoning = raw.get("reasoning") or ""
        if not slug or not isinstance(dur, int) or dur <= 0:
            continue
        if candidate_set and slug not in candidate_set:
            # Hallucinated slug — substitute with the next unused candidate
            # (degrade gracefully) and log so we can audit the prompt.
            substitute = next(
                (c for c in candidate_iter if c not in {b.drill_slug for b in plan}),
                None,
            )
            if substitute is None:
                _log.warning(
                    "practice_brief: dropping hallucinated drill_slug %r (no substitute)",
                    slug,
                )
                continue
            _log.warning(
                "practice_brief: substituting hallucinated drill_slug %r -> %r",
                slug,
                substitute,
            )
            slug = substitute
        # Always include the drill_slug itself as a primary cross-ref —
        # prose doesn't always repeat it verbatim, but the slug IS the
        # canonical wiki entry the user should be able to click.
        prose_refs = _extract_cross_refs(reasoning)
        cross_refs = [slug] + [r for r in prose_refs if r != slug]
        plan.append(
            PracticeBlock(
                drill_slug=slug,
                duration_minutes=dur,
                reasoning=reasoning,
                cross_refs=cross_refs,
            )
        )
        citations.extend(_extract_citations(reasoning))

    if not plan:
        return _build_stub(context)

    deduped_citations: list[str] = []
    for c in citations:
        if c not in deduped_citations:
            deduped_citations.append(c)
    return PracticeBriefResult(
        plan=plan, source_citations=deduped_citations, source="claude"
    )
