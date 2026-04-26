"""Basketball prompt preludes — extracted from the inline service prompts.

CRITICAL: every string in this module must remain **byte-identical** to
its pre-refactor inline form so the 36/36 play-brief eval baseline does
not drift. The byte-identity test at
``tests/eval/test_prompt_byte_identity.py`` enforces this on every
matrix point.

If you change wording here you MUST re-run the live eval suite (cost
~$0.10) and update the snapshot fixtures.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# play_brief.py — final clause of the long instruction string.
# Pre-refactor location: the trailing two-sentence audience+tone clause
# at the end of ``_build_claude_prompt``.
# ---------------------------------------------------------------------------

PLAY_BRIEF_AUDIENCE_CLAUSE = (
    "Audience: basketball coach. Tone: declarative, no promotional language, no emojis."
)


# ---------------------------------------------------------------------------
# practice_brief.py — audience + translation + banned vocab + voice block.
# Pre-refactor location: middle slab of ``_PROMPT_INSTRUCTIONS``, between
# the "OTHER RULES" prefix lines and the closing "Compose every reasoning"
# rules.
# ---------------------------------------------------------------------------

PRACTICE_BRIEF_VOICE_BLOCK = (
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
)

# Reasoning sentence directive embedded inside the practice prompt block-rules
# section. Pre-refactor location: trailing fragment of the "Each reasoning
# sentence" rule that names the language family.
PRACTICE_BRIEF_REASONING_LANGUAGE = "basketball language"


# ---------------------------------------------------------------------------
# form_brief.py — audience + translation tables + banned vocab + voice.
# Pre-refactor location: middle slab of ``_PROMPT_INSTRUCTIONS`` between the
# top "STRUCTURE" rules and the trailing "OTHER RULES" rules.
# ---------------------------------------------------------------------------

FORM_BRIEF_VOICE_BLOCK = (
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
)
