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

    defending_phrase = ""
    if context.defending:
        top = context.defending[0]
        tag = (top.shared_tags or ["generic"])[0]
        defending_phrase = (
            f" Expect {tag} coverage schemes from the defense — match precedent: "
            f"{top.defending_slug}."
        )
    signature_phrase = ""
    if context.signature:
        top_sig = context.signature[0]
        signature_phrase = (
            f" Signature: {top_sig.direction} {top_sig.factor} ({top_sig.magnitude})."
        )
    brief = (
        f"{context.play_slug.replace('-', ' ').title()} loads {body_phrase}. "
        f"Prep priority: {drill_phrase}.{caveat}{defending_phrase}{signature_phrase}"
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
    if context.defending:
        # Pass defending-page slugs + shared tags as structural context only.
        # The symptom/remedy prose on defending-*.md pages is near-verbatim
        # from S1 (see memory wiki-corpus-debt.md) and must not surface.
        lines.append("Relevant defenses (match by shared tag):")
        for edge in context.defending[:3]:
            tags = ", ".join(edge.shared_tags) or "generic"
            lines.append(f"  - {edge.defending_slug} (shared tags: {tags})")
    if context.signature:
        # Four-Factor signature — which stats this play lifts/protects/lowers.
        # Rationales are author-composed (not book-derived) so are safe to echo.
        lines.append("Analytic signature (Four-Factor directions):")
        for s in context.signature:
            lines.append(f"  - {s.factor} {s.direction} ({s.magnitude})")
    if readiness:
        lines.append("Roster readiness flags (player → flagged regions):")
        for entry in readiness:
            name = entry.get("player_name") or "player"
            regions = ", ".join(entry.get("flagged_regions") or [])
            lines.append(f"  - {name}: {regions}")

    lines.append("")
    defending_directive = (
        "Sentence 4 (only if 'Relevant defenses' are listed above): one sentence naming "
        "the most-relevant defense by its shared tag and what to expect, in your own words. "
        "Omit this sentence if no defenses are listed. "
        if context.defending
        else ""
    )
    signature_directive = (
        "Sentence 5 (only if 'Analytic signature' is listed above): one short sentence "
        "naming which Four-Factor the play lifts, protects, or lowers (by factor name), "
        "in your own words. Omit if no signature is listed. "
        if context.signature
        else ""
    )
    extra_sentences = []
    if context.defending:
        extra_sentences.append("a defense")
    if context.signature:
        extra_sentences.append("an analytic signature")
    length_note = (
        f" (up to {3 + len(extra_sentences)} sentences if {' and '.join(extra_sentences)} apply)"
        if extra_sentences
        else ""
    )
    lines.append(
        "Write a 3-sentence coaching brief"
        + length_note
        + ". Sentence 1: the play's action in plain language. "
        "Sentence 2: the body demands — you MUST explicitly name at least one required anatomy "
        "region (use the human-readable form, e.g. 'hip flexor complex', 'ankle complex', "
        "'core outer', 'glute max'); add a roster caveat if a flagged region matches a required "
        "anatomy region. Sentence 3: the top drill recommendation (by slug) and why it prepares "
        "this play. "
        + defending_directive
        + signature_directive
        + "Compose every sentence in your own words; do NOT quote, paraphrase, or echo "
        "any coaching cue, principle text, symptom line, or any phrase from the context above. "
        "Book-derived prose must not surface; only structural references may. "
        "Cite [Sn, p.X] tokens verbatim from the context above; do NOT invent citations. "
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
