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


_PROMPT_INSTRUCTIONS = (
    "Write a 3-5 sentence coaching note addressed to the PLAYER,"
    " in their second person.\n"
    "\n"
    "AUDIENCE: a basketball player or their coach reading on their phone."
    " They speak basketball, NOT anatomy, NOT biomechanics, NOT sports medicine."
    " If a 16-year-old player or a high-school coach would not say it on"
    " the court, do not write it.\n"
    "\n"
    "EVERY SENTENCE GENERATES A SOLUTION."
    " Do not describe a problem without immediately telling them what to DO"
    " about it on their next shot or next rep."
    " The brief is a fix-list, not a diagnosis."
    " Pair every flag with an action they can take TODAY.\n"
    "\n"
    "STRUCTURE (problem-paired-with-fix):\n"
    "- Sentence 1: name the biggest visible problem in plain language AND"
    " the cue that fixes it, in the same sentence."
    " (e.g. 'Your shooting elbow is flying out — tuck it under the ball"
    " and let your forearm rise straight up the front of your face.')\n"
    "- Sentence 2: a concrete physical cue they can feel on their NEXT shot"
    " to check the fix is working."
    " (e.g. 'You should feel your shooting elbow brush past your ear"
    " on the way up.')\n"
    "- Sentence 3: name ONE drill by its slug from the context above and"
    " tell them the ONE thing to focus on during reps — not why the drill"
    " works. (e.g. 'Run drill-foo and on every rep watch your elbow stay"
    " inside your shoulder line.')\n"
    "- Sentences 4-5 (optional, only if a second signal is flagged or"
    " there is a safety risk): same problem→fix pairing."
    " If a flag is a safety risk, lead with 'Fix this before you keep"
    " shooting:' and prescribe the action.\n"
    "\n"
    "NUMBER RULE: if you reference a number from the measurements, say it"
    " in plain English ('about 30 degrees off line', 'releasing way too"
    " low'). NEVER write the raw measurement name (elbow_flair,"
    " knee_valgus, follow_through_droop, release_height_ratio, trunk_lean)"
    " and NEVER write '32.3deg' or '0.2ratio' — those are debug strings,"
    " not coach speech.\n"
    "\n"
    "TRANSLATION TABLE — anatomy region in context → basketball word"
    " in your prose:\n"
    "  elbow complex     -> 'shooting elbow' or 'elbow'\n"
    "  shoulder girdle   -> 'shoulder' (or 'shoulder line' if alignment matters)\n"
    "  wrist complex     -> 'wrist' or 'shooting hand'\n"
    "  ankle complex     -> 'ankles' or 'feet'\n"
    "  hip complex       -> 'hips'\n"
    "  knee              -> 'knees'\n"
    "  core              -> 'core'\n"
    "TRANSLATION TABLE — measurement name in context → how it looks"
    " on tape:\n"
    "  elbow_flair             -> 'elbow winging out' / 'elbow flying"
    " away from your body'\n"
    "  follow_through_droop    -> 'wrist not finishing' / 'no snap on"
    " the follow-through'\n"
    "  knee_valgus             -> 'knees caving inward' / 'knees"
    " buckling in'\n"
    "  release_height_ratio    -> 'releasing too low' / 'letting the"
    " ball go before you reach up'\n"
    "  trunk_lean              -> 'leaning forward through the shot'\n"
    "\n"
    "BANNED VOCABULARY — do not use any of these or close variants:\n"
    "  stretch-shortening cycle, plantar-flexor, dorsiflexion,"
    " ground-reaction, kinetic chain,\n"
    "  medial structures, lateral structures, anti-rotation,"
    " sagittal plane, frontal plane,\n"
    "  eccentric loading, concentric, isometric, proprioception,"
    " neuromuscular, biomechanics,\n"
    "  asymmetric load, ligament injury, valgus, varus, posterior chain,"
    " anterior chain,\n"
    "  distal, proximal, kinematic, glute max activation, force transfer,"
    " vertical plane,\n"
    "  ratio, threshold, signal, measurement, reading, value.\n"
    "Also avoid the words 'complex', 'girdle', 'apparatus', 'structures'"
    " when naming a body part.\n"
    "\n"
    "VOICE: coach-on-the-sideline, not trainer-in-a-clinic."
    " Imperative verbs ('tuck', 'snap', 'load', 'finish', 'sit', 'drive',"
    " 'square up', 'rise'). Sentences short — feel the urgency of halftime"
    " in a tight game. No promotional language. No emojis."
    " No exclamation marks. No rhetorical questions.\n"
    "\n"
    "OTHER RULES:\n"
    "- Compose every sentence in your own words; do NOT quote, paraphrase,"
    " or echo any coaching cue, principle text, symptom line, or any"
    " phrase from the context above.\n"
    "- Book-derived prose must not surface; only structural slug"
    " references may.\n"
    "- Cite [Sn, p.X] tokens verbatim from the context above; do NOT"
    " invent citations.\n"
    "- No preamble, no bullet list, no headings. Plain text only."
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
    lines.append(_PROMPT_INSTRUCTIONS)
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
