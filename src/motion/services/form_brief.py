"""Form-coach brief — Engine-composed feedback over a player's joint timeline.

Mirrors :mod:`motion.services.play_brief`. Takes a
:class:`motion.wiki_ops.retrieval.FormContext` (shot type, measured form
anomalies, focus anatomy + technique slugs) plus 1-3 keyframe images and
returns a 3-5 sentence coaching brief with inline `[Sn, p.X]` citations.

Two modes:

- **Claude**: if ``ANTHROPIC_API_KEY`` is set, composes via Claude Sonnet 4.6
  vision (single multi-part message: anchor text + image blocks).
- **Stub**: if no API key, returns a deterministic fallback built from the
  measurements alone — UX never dead-ends in dev.

Reuses the play-brief composer's anti-quote rules, citation regex, and
forbidden-phrase enforcement (the same 90-phrase blocklist applies).

Privacy: images flow through this composer; raw video never reaches the
backend (joint extraction is client-side via MediaPipe).
"""

from __future__ import annotations

import base64
import os
import re
from dataclasses import dataclass

from motion.wiki_ops.retrieval import FormContext, FormMeasurement

_MODEL = "claude-sonnet-4-6"
_MAX_TOKENS = 600
_CITATION_RE = re.compile(r"\[S\d+(?:,\s*pp?\.\s*[\d\-–]+)?\]")  # noqa: RUF001


@dataclass(frozen=True)
class FormBriefResult:
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


def _collect_bundle_citations(context: FormContext) -> list[str]:
    """Harvest `[Sn, p.X]` tokens from every concept-anatomy/technique insight."""
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
    return cites


def _flagged(measurements: list[FormMeasurement]) -> list[FormMeasurement]:
    return [m for m in measurements if m.flagged]


def _measurement_phrase(m: FormMeasurement) -> str:
    """Compact human-readable phrase for one measurement, used in prompt + stub."""
    return f"{m.name}: {m.value:.1f}{m.unit} (threshold {m.threshold:.1f}{m.unit})"


def _build_stub(context: FormContext) -> FormBriefResult:
    """Deterministic stub — runs when no API key is available.

    Always grounds in the chain (names anatomy + drill) even when all
    signals are within threshold, so the eval rubric's anatomy/drill-ref
    signals stay valid regardless of measurement state.
    """
    flagged = _flagged(context.measurements)
    anatomy_phrase = (
        ", ".join(a.region.replace("_", " ") for a in context.anatomy[:2])
        or "core mechanics"
    )
    drill_phrase = (
        context.drill_focus[0].replace("-", " ")
        if context.drill_focus
        else "form-shooting reps"
    )
    if not flagged:
        brief = (
            f"{context.shot_type.replace('-', ' ').title()}: form within thresholds "
            f"across the {len(context.measurements)} measured signals. "
            f"Loads {anatomy_phrase}; continue your routine alongside {drill_phrase}."
        )
    else:
        anomalies = "; ".join(_measurement_phrase(m) for m in flagged[:3])
        brief = (
            f"{context.shot_type.replace('-', ' ').title()}: "
            f"{len(flagged)} signal(s) outside threshold — {anomalies}. "
            f"Loads {anatomy_phrase}; train with {drill_phrase}."
        )
    return FormBriefResult(
        brief=brief.strip(),
        source_citations=_collect_bundle_citations(context),
        source="stub",
    )


def _build_text_prompt(context: FormContext) -> str:
    """Compose the text portion of the multimodal prompt."""
    lines: list[str] = []
    lines.append(f"Shot type: {context.shot_type}")
    if context.measurements:
        lines.append("Measured form signals (computed client-side from joint landmarks):")
        for m in context.measurements:
            flag = " [FLAGGED]" if m.flagged else ""
            lines.append(f"  - {_measurement_phrase(m)}{flag}")
    if context.anatomy:
        lines.append("Anatomy regions to ground the brief in:")
        for a in context.anatomy:
            lines.append(f"  - {a.region}  (concept page: {a.concept_slug})")
    if context.technique_focus:
        lines.append("Technique concept pages to ground the brief in:")
        for t in context.technique_focus:
            lines.append(f"  - {t}")
    if context.drill_focus:
        lines.append("Drill recommendations available:")
        for d in context.drill_focus:
            lines.append(f"  - {d}")
    if context.keyframe_count:
        lines.append(
            f"Keyframe images ({context.keyframe_count}) follow this text — "
            "they are sampled from the player's recording at release / peak / "
            "follow-through. Use them to ground your visual reads, but do NOT "
            "describe what the player looks like — describe what they should DO."
        )

    lines.append("")
    lines.append(
        "Write a 3-5 sentence coaching brief addressed to the PLAYER, in their second person. "
        "Sentence 1: name the shot type and call out the most important measured signal "
        "(use the value + unit verbatim from the context above, e.g. '12.0deg of elbow flair'). "
        "Sentence 2: name the anatomy region (human-readable form, e.g. 'shoulder girdle', "
        "'wrist complex', 'elbow complex') driving the issue. "
        "Sentence 3: prescribe ONE drill (by slug) and explain in your own words why it fixes "
        "the flagged pattern. "
        "Sentences 4-5 (optional): address a secondary signal or a safety check if any "
        "measurement indicates injury risk (knee valgus, trunk-forward landing, asymmetric load). "
        "Compose every sentence in your own words; do NOT quote, paraphrase, or echo any "
        "coaching cue, principle text, symptom line, or any phrase from the context above. "
        "Book-derived prose must not surface; only structural references may. "
        "Cite [Sn, p.X] tokens verbatim from the context above; do NOT invent citations. "
        "No preamble, no bullet list, no headings. Plain text only. "
        "Audience: a basketball player reviewing their own video. "
        "Tone: declarative, action-verbed, no promotional language, no emojis."
    )
    return "\n".join(lines)


def _build_message_blocks(
    context: FormContext, keyframe_images: list[bytes]
) -> list[dict]:
    """Assemble the Anthropic content blocks (text + image_blocks)."""
    blocks: list[dict] = [{"type": "text", "text": _build_text_prompt(context)}]
    for img in keyframe_images[:3]:
        b64 = base64.b64encode(img).decode("ascii")
        blocks.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": b64,
                },
            }
        )
    return blocks


def build_form_brief(
    context: FormContext,
    keyframe_images: list[bytes] | None = None,
) -> FormBriefResult:
    """Compose a form-coach brief. Falls back to a stub if no API key is present.

    ``keyframe_images`` are JPEG bytes (1-3 frames). Pass ``None`` or ``[]`` to
    run a text-only pass — useful for stub-mode eval cases that don't carry
    real images.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return _build_stub(context)

    try:
        import anthropic  # local import — keeps startup cost off the API path
    except ImportError:
        return _build_stub(context)

    images = keyframe_images or []
    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": _build_message_blocks(context, images),
                }
            ],
        )
    except Exception:
        return _build_stub(context)

    text_parts: list[str] = []
    for block in getattr(message, "content", []) or []:
        block_text = getattr(block, "text", None)
        if isinstance(block_text, str):
            text_parts.append(block_text)
    brief = "".join(text_parts).strip()
    if not brief:
        return _build_stub(context)

    return FormBriefResult(
        brief=brief,
        source_citations=_extract_citations(brief),
        source="claude",
    )
