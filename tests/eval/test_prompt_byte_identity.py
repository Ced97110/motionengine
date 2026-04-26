"""Byte-identity guard for the per-sport prompt refactor (Step 4).

The play-brief eval baseline is 36/36 today (see memory
``m6-eval-shipped.md``). Any drift in basketball prompt wording can move
that baseline silently. This test parametrizes across the dynamic
assembly axes (defending x signature x readiness x cross-ref bullet
counts) and asserts that the post-refactor basketball prompt is
byte-identical to a hand-pinned golden.

Goldens are constructed inline below from the same literal substrings
that lived in the pre-refactor inline prompts. If you change a basketball
prompt string, update both the prompt module AND the golden in the same
commit — and re-run the live eval (``RUN_LIVE_EVAL=1``) to confirm the
36/36 baseline survives.

Football is exercised on the practice-brief axis only — its play_brief
voice clause is short enough (one sentence) that a single golden suffices.
"""

from __future__ import annotations

import difflib

import pytest

from motion.prompts import basketball as bb_prompts
from motion.prompts import football as fb_prompts
from motion.services.form_brief import _build_prompt_instructions as form_instructions
from motion.services.play_brief import _build_claude_prompt
from motion.services.practice_brief import (
    _build_prompt_instructions as practice_instructions,
)
from motion.wiki_ops.retrieval import (
    AnatomyDemand,
    DefendingEdge,
    DrillPrescription,
    PlayContext,
    PracticeContext,
    SignatureEntry,
    TechniqueDemand,
)

# ---------------------------------------------------------------------------
# Helpers — construct deterministic PlayContext fixtures across the axes.
# ---------------------------------------------------------------------------


def _anatomy(region: str = "hip_flexor_complex", criticality: str = "required") -> AnatomyDemand:
    return AnatomyDemand(
        region=region,
        concept_slug=f"concept-anatomy-{region.replace('_', '-')}",
        criticality=criticality,
    )


def _technique(tid: str = "tech-curl", role: str | None = "5") -> TechniqueDemand:
    return TechniqueDemand(
        technique_id=tid,
        concept_slug=f"concept-technique-{tid}",
        role=role,
        criticality="required",
    )


def _drill(slug: str = "drill-back-squat", emphasis: str = "primary") -> DrillPrescription:
    return DrillPrescription(
        drill_slug=slug,
        emphasis=emphasis,
        via=f"via {slug}",
    )


def _defending(slug: str = "defending-pick-and-roll", *tags: str) -> DefendingEdge:
    return DefendingEdge(
        defending_slug=slug,
        shared_tags=list(tags) or ["pick-and-roll"],
        symptoms=[],
    )


def _signature(factor: str = "efg-pct", direction: str = "lifts") -> SignatureEntry:
    return SignatureEntry(
        factor=factor,
        direction=direction,
        magnitude="medium",
        rationale="play creates open looks",
    )


# Defending matrix — 0 / 1 / 3 edges
_DEFENDING_AXES: list[tuple[str, list[DefendingEdge]]] = [
    ("def-empty", []),
    ("def-single", [_defending("defending-drop-coverage", "pick-and-roll")]),
    (
        "def-multi",
        [
            _defending("defending-drop-coverage", "pick-and-roll"),
            _defending("defending-ice", "ball-screen"),
            _defending("defending-blitz", "trap"),
        ],
    ),
]

# Signature matrix — 0 / 1 / 2 factors
_SIGNATURE_AXES: list[tuple[str, list[SignatureEntry]]] = [
    ("sig-empty", []),
    ("sig-single", [_signature("efg-pct", "lifts")]),
    (
        "sig-multi",
        [
            _signature("efg-pct", "lifts"),
            _signature("tov-pct", "lowers"),
        ],
    ),
]

# Readiness matrix — none / present-no-flag / present-with-flag
_READINESS_AXES: list[tuple[str, list[dict] | None]] = [
    ("rd-none", None),
    ("rd-no-flag", [{"player_name": "Player A", "flagged_regions": ["wrist_complex"]}]),
    (
        "rd-flag",
        [{"player_name": "Player B", "flagged_regions": ["hip_flexor_complex"]}],
    ),
]

# Cross-ref bullet count axis — anatomy + drill list lengths (proxy for
# the bullet-count tiers the plan calls out: 0, 5, 15).
_BULLETS_AXES: list[tuple[str, list[AnatomyDemand], list[DrillPrescription]]] = [
    ("bullets-0", [], []),
    (
        "bullets-5",
        [_anatomy("hip_flexor_complex"), _anatomy("glute_max")],
        [
            _drill("drill-back-squat"),
            _drill("drill-ankling", "secondary"),
            _drill("drill-bird-dog", "secondary"),
        ],
    ),
    (
        "bullets-15",
        [
            _anatomy("hip_flexor_complex"),
            _anatomy("glute_max"),
            _anatomy("ankle_complex"),
            _anatomy("core_outer", "supportive"),
            _anatomy("shoulder_girdle", "supportive"),
        ],
        [
            _drill("drill-back-squat"),
            _drill("drill-ankling", "secondary"),
            _drill("drill-bird-dog", "secondary"),
            _drill("drill-360-jump"),
            _drill("drill-band-lateral-walk", "secondary"),
            _drill("drill-back-extension", "secondary"),
            _drill("drill-butt-kick-jump", "secondary"),
            _drill("drill-barrier-jump-cut-sprint"),
            _drill("drill-pallof-press", "secondary"),
            _drill("drill-form-shooting", "secondary"),
        ],
    ),
]


def _matrix_ids() -> list[tuple[str, PlayContext, list[dict] | None]]:
    """Build the cartesian product of the dynamic-assembly axes."""
    out: list[tuple[str, PlayContext, list[dict] | None]] = []
    for d_id, defending in _DEFENDING_AXES:
        for s_id, signature in _SIGNATURE_AXES:
            for r_id, readiness in _READINESS_AXES:
                for b_id, anatomy, drills in _BULLETS_AXES:
                    case_id = f"{d_id}__{s_id}__{r_id}__{b_id}"
                    ctx = PlayContext(
                        play_slug="play-test-fixture",
                        anatomy=list(anatomy),
                        techniques=[_technique()] if anatomy else [],
                        drills=list(drills),
                        defending=list(defending),
                        signature=list(signature),
                    )
                    out.append((case_id, ctx, readiness))
    return out


# ---------------------------------------------------------------------------
# play_brief — basketball golden reconstruction.
# ---------------------------------------------------------------------------


def _expected_play_brief_basketball(
    context: PlayContext, readiness: list[dict] | None
) -> str:
    """Reconstruct the pre-refactor basketball play-brief prompt verbatim.

    This is the golden — its strings are copied byte-for-byte from the
    pre-Step-4 inline ``_build_claude_prompt`` body. Any drift here means
    a real prompt regression, not a refactor artifact.
    """
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
        lines.append("Relevant defenses (match by shared tag):")
        for edge in context.defending[:3]:
            tags = ", ".join(edge.shared_tags) or "generic"
            lines.append(f"  - {edge.defending_slug} (shared tags: {tags})")
    if context.signature:
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


@pytest.mark.parametrize(
    "case_id,context,readiness",
    _matrix_ids(),
    ids=[c[0] for c in _matrix_ids()],
)
def test_play_brief_basketball_byte_identity(
    case_id: str, context: PlayContext, readiness: list[dict] | None
) -> None:
    """Refactored basketball play-brief prompt matches the pre-refactor golden."""
    actual = _build_claude_prompt(context, readiness, sport="basketball")
    expected = _expected_play_brief_basketball(context, readiness)
    if actual != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                actual.splitlines(),
                fromfile="golden",
                tofile="actual",
                lineterm="",
            )
        )
        pytest.fail(f"[{case_id}] basketball play-brief drifted:\n{diff}")


def test_play_brief_default_sport_is_basketball() -> None:
    """Calling without an explicit sport keeps pre-refactor wording."""
    ctx = PlayContext(
        play_slug="play-default",
        anatomy=[_anatomy()],
        drills=[_drill()],
    )
    default_prompt = _build_claude_prompt(ctx, None)
    explicit_prompt = _build_claude_prompt(ctx, None, sport="basketball")
    assert default_prompt == explicit_prompt


# ---------------------------------------------------------------------------
# practice_brief — duration matrix golden reconstruction.
# ---------------------------------------------------------------------------


_DURATION_AXIS = [15, 30, 45, 60, 75, 90]


def _expected_practice_instructions_basketball() -> str:
    """Pre-refactor inline ``_PROMPT_INSTRUCTIONS`` golden."""
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
        " technique it loads, in basketball language) with WHAT THE COACH"
        " SHOULD WATCH FOR during reps.\n"
        "\n"
        "AUDIENCE: a basketball coach reading this on their phone before"
        " practice. They speak basketball, NOT anatomy / biomechanics /"
        " sports medicine.\n"
        "\n"
        "TRANSLATION TABLE — anatomy region in context → basketball word"
        " in your prose:\n"
        "  elbow_complex     -> 'shooting elbow' or 'elbow'\n"
        "  shoulder_girdle   -> 'shoulder' or 'shoulder line'\n"
        "  wrist_complex     -> 'wrist' or 'shooting hand'\n"
        "  ankle_complex     -> 'ankles' or 'feet'\n"
        "  hip_flexor_complex-> 'hips' or 'hip flexors'\n"
        "  glute_max         -> 'glutes' or 'hips'\n"
        "  core_outer        -> 'core'\n"
        "\n"
        "BANNED VOCABULARY — do not use any of these or close variants:\n"
        "  stretch-shortening cycle, plantar-flexor, dorsiflexion,"
        " ground-reaction, kinetic chain, medial structures, lateral"
        " structures, anti-rotation, sagittal plane, frontal plane,"
        " eccentric loading, concentric, isometric, proprioception,"
        " neuromuscular, biomechanics, asymmetric load, valgus, varus,"
        " posterior chain, anterior chain, distal, proximal, kinematic.\n"
        "Avoid 'complex', 'girdle', 'apparatus', 'structures' when naming a"
        " body part.\n"
        "\n"
        "VOICE: coach-on-the-clipboard, not trainer-in-a-clinic. Imperative"
        " verbs. Short sentences. No promotional language. No emojis."
        " No exclamation marks. No rhetorical questions.\n"
        "\n"
        "OTHER RULES:\n"
        "- Compose every reasoning sentence in your own words; do NOT quote"
        " or paraphrase any coaching cue or principle text from the context.\n"
        "- Book-derived prose must not surface; only structural slug"
        " references may.\n"
        "- Cite [Sn, p.X] tokens verbatim if you use them; do NOT invent"
        " citations."
    )


@pytest.mark.parametrize("duration", _DURATION_AXIS)
def test_practice_brief_basketball_byte_identity(duration: int) -> None:
    """Practice instructions block is byte-identical regardless of duration.

    The duration axis is independent of the prompt-instructions string —
    it changes the data that's fed alongside the instructions, not the
    instructions themselves. We assert the instructions render the same
    pre-/post-refactor text, then spot-check that the duration field
    reaches the rendered prompt.
    """
    actual = practice_instructions(sport="basketball")
    expected = _expected_practice_instructions_basketball()
    if actual != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                actual.splitlines(),
                fromfile="golden",
                tofile="actual",
                lineterm="",
            )
        )
        pytest.fail(f"[duration={duration}] practice instructions drifted:\n{diff}")

    # Spot-check the duration plumbing path — the prompt body interpolates
    # context.duration_minutes into a literal "Total duration: {n} min" line.
    from motion.services.practice_brief import _build_text_prompt

    ctx = PracticeContext(
        level="intermediate",
        duration_minutes=duration,
        focus_areas=["shooting"],
        candidate_drills=[],
    )
    full_prompt = _build_text_prompt(ctx, sport="basketball")
    assert f"Total duration: {duration} min" in full_prompt


def test_practice_brief_default_sport_is_basketball() -> None:
    """Default-sport call matches explicit basketball call."""
    assert practice_instructions() == practice_instructions(sport="basketball")


# ---------------------------------------------------------------------------
# form_brief — single-shape golden (no dynamic axes inside the prelude).
# ---------------------------------------------------------------------------


def _expected_form_instructions_basketball() -> str:
    return (
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


def test_form_brief_basketball_byte_identity() -> None:
    actual = form_instructions(sport="basketball")
    expected = _expected_form_instructions_basketball()
    if actual != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                actual.splitlines(),
                fromfile="golden",
                tofile="actual",
                lineterm="",
            )
        )
        pytest.fail(f"form-brief instructions drifted:\n{diff}")


def test_form_brief_default_sport_is_basketball() -> None:
    assert form_instructions() == form_instructions(sport="basketball")


# ---------------------------------------------------------------------------
# football — registry-shape sanity checks (the football prelude is content-
# only scaffolding; the assertion is that the registry returns a module
# with the same surface, not byte-equality with basketball).
# ---------------------------------------------------------------------------


def test_football_registry_dispatches_to_football_module() -> None:
    from motion.prompts import get_prompts

    assert get_prompts(sport="football") is fb_prompts
    assert get_prompts(sport="basketball") is bb_prompts


def test_football_prompts_have_full_surface() -> None:
    """Football module exposes the same names as basketball.

    Adding a third sport must not require editing service code; the
    registry contract is satisfied entirely by name parity.
    """
    bb_attrs = {n for n in vars(bb_prompts) if not n.startswith("_")}
    fb_attrs = {n for n in vars(fb_prompts) if not n.startswith("_")}
    missing = bb_attrs - fb_attrs
    assert not missing, f"football module missing attrs: {sorted(missing)}"


def test_football_play_brief_audience_is_football() -> None:
    """Football play-brief includes the football audience clause, not basketball."""
    ctx = PlayContext(
        play_slug="play-football-test",
        anatomy=[_anatomy("shoulder_girdle")],
        drills=[_drill("drill-throwing-progression")],
    )
    prompt = _build_claude_prompt(ctx, None, sport="football")
    assert "Audience: football coach." in prompt
    assert "Audience: basketball coach." not in prompt


def test_unknown_sport_raises() -> None:
    from motion.prompts import get_prompts

    with pytest.raises(ValueError):
        get_prompts(sport="hockey")  # type: ignore[arg-type]
