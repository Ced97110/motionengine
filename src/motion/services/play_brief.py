"""Play-brief composition — Engine-composed answer over the cross-ref bundle.

Takes a :class:`motion.wiki_ops.retrieval.PlayContext` (+ optional roster
readiness) and returns a 3-sentence coaching brief with inline `[S2]` / `[S4]`
citations. Two modes:

- **Claude**: if ``ANTHROPIC_API_KEY`` is set, composes via Claude Sonnet 4.6
  with a strict template.
- **Stub**: if no API key, returns a deterministic fallback built from the
  bundle — coach still sees a usable summary, UX never dead-ends.

Consumers mark which path fired via the ``source`` field so the UI can show
a degradation indicator if needed. Mirrors the pattern in
``frontend/src/app/api/halftime/route.ts``.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

from motion.wiki_ops.retrieval import PlayContext

_MODEL = "claude-sonnet-4-6"
_MAX_TOKENS = 400
_CITATION_RE = re.compile(r"\[S\d+(?:,\s*pp?\.\s*[\d\-\u2013]+)?\]")


@dataclass(frozen=True)
class BriefResult:
    brief: str
    source_citations: list[str]
    source: str  # "claude" | "stub"


def _extract_citations(text: str) -> list[str]:
    """Return the unique ``[Sn, p.X]`` citations appearing in ``text``, in order."""
    seen: list[str] = []
    for match in _CITATION_RE.finditer(text):
        token = match.group(0)
        if token not in seen:
            seen.append(token)
    return seen


def _collect_bundle_citations(context: PlayContext) -> list[str]:
    """Harvest all `[Sn, p.X]` citations referenced across the bundle's insights."""
    cites: list[str] = []
    seen: set[str] = set()

    def _add(token: str | None) -> None:
        if token and token not in seen:
            seen.add(token)
            cites.append(token)

    for a in context.anatomy:
        if a.insight is None:
            continue
        for p in a.insight.key_principles:
            _add(p.get("citation"))
        for m in a.insight.common_mistakes:
            _add(m.get("citation"))
    for d in context.drills:
        if d.insight is None:
            continue
        if d.insight.safety_tip:
            _add(d.insight.safety_tip.get("citation"))
        if d.insight.primary_form_error:
            _add(d.insight.primary_form_error.get("citation"))
    return cites


def _build_stub(context: PlayContext, readiness: list[dict] | None) -> BriefResult:
    """Deterministic stub — runs when no API key is available."""
    required = [a.region.replace("_", " ") for a in context.anatomy if a.criticality == "required"]
    primary_drill = next(
        (d.drill_slug for d in context.drills if d.emphasis == "primary"),
        None,
    )
    body_phrase = ", ".join(required) if required else "no critical regions flagged"
    drill_phrase = (
        f"{primary_drill.replace('-', ' ')}" if primary_drill else "no primary drill prescribed"
    )
    caveat = ""
    if readiness:
        flagged: list[str] = []
        for entry in readiness:
            regions = entry.get("flagged_regions") or []
            flagged.extend(r.replace("_", " ") for r in regions)
        overlap = [r for r in flagged if r in required]
        if overlap:
            caveat = (
                f" Roster caveat: {', '.join(overlap)} flagged — "
                "consider substitution or shortened minutes."
            )

    brief = (
        f"{context.play_slug.replace('-', ' ').title()} loads {body_phrase}. "
        f"Prep priority: {drill_phrase}.{caveat}"
    )
    return BriefResult(
        brief=brief.strip(),
        source_citations=_collect_bundle_citations(context),
        source="stub",
    )


def _build_claude_prompt(context: PlayContext, readiness: list[dict] | None) -> str:
    """Compose the user message: bundle + readiness + template instructions."""
    lines: list[str] = []
    lines.append(f"Play slug: {context.play_slug}")
    if context.techniques:
        lines.append("Techniques demanded:")
        for t in context.techniques:
            role_suffix = f" (role {t.role})" if t.role else ""
            lines.append(f"  - {t.technique_id}{role_suffix} — {t.criticality}")
    if context.anatomy:
        lines.append("Anatomy regions demanded:")
        for a in context.anatomy:
            lines.append(f"  - {a.region} — {a.criticality}")
            if a.insight:
                for p in a.insight.key_principles[:1]:
                    text = p.get("text", "")
                    cite = p.get("citation", "")
                    lines.append(f"      key principle: {text} {cite}".rstrip())
    if context.drills:
        lines.append("Drills prescribed:")
        for d in context.drills:
            lines.append(f"  - {d.drill_slug} ({d.emphasis}, via {d.via})")
            if d.insight and d.insight.coaching_cue:
                lines.append(f"      cue: {d.insight.coaching_cue}")
    if readiness:
        lines.append("Roster readiness flags (player → flagged regions):")
        for entry in readiness:
            name = entry.get("player_name") or "player"
            regions = ", ".join(entry.get("flagged_regions") or [])
            lines.append(f"  - {name}: {regions}")

    lines.append("")
    lines.append(
        "Write a 3-sentence coaching brief. Sentence 1: the play's action in plain language. "
        "Sentence 2: the body demands with a roster caveat if a flagged region matches a required "
        "anatomy region. Sentence 3: the top drill recommendation with its one-line coaching cue. "
        "Cite [Sn, p.X] tokens verbatim from the context above — do NOT invent citations. "
        "No preamble, no bullet list, no headings. Plain text only. "
        "Audience: basketball coach. Tone: declarative, no promotional language, no emojis."
    )
    return "\n".join(lines)


def build_brief(
    context: PlayContext,
    readiness: list[dict] | None = None,
) -> BriefResult:
    """Compose a play brief. Falls back to a stub if no API key is present."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return _build_stub(context, readiness)

    try:
        import anthropic  # local import — avoid bumping module import cost at startup
    except ImportError:
        return _build_stub(context, readiness)

    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": _build_claude_prompt(context, readiness),
                }
            ],
        )
    except Exception:
        # Any upstream failure → graceful stub. Never dead-end the UX.
        return _build_stub(context, readiness)

    text_parts: list[str] = []
    for block in getattr(message, "content", []) or []:
        block_text = getattr(block, "text", None)
        if isinstance(block_text, str):
            text_parts.append(block_text)
    brief = "".join(text_parts).strip()
    if not brief:
        return _build_stub(context, readiness)

    return BriefResult(
        brief=brief,
        source_citations=_extract_citations(brief),
        source="claude",
    )
