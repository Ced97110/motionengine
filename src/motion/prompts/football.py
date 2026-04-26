"""Football prompt preludes — parallel scaffold to basketball.

Football content is not yet ingested (Step 6 territory). The vocabulary
chosen here mirrors the basketball module's coach-voice rules — when
content authoring begins, refine the translation tables in place; the
service-layer code does not need to change.

Anti-clinical guardrails (banned biomech vocab, voice rules) are shared
with the basketball module verbatim — they are sport-agnostic.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# play_brief.py — final clause of the long instruction string.
# ---------------------------------------------------------------------------

PLAY_BRIEF_AUDIENCE_CLAUSE = (
    "Audience: football coach. Tone: declarative, no promotional language, no emojis."
)


# ---------------------------------------------------------------------------
# practice_brief.py — audience + translation + banned vocab + voice block.
# Translation table swaps basketball anatomy mappings for football
# anatomy mappings (drive leg, throwing shoulder, hips/glutes for cuts).
# ---------------------------------------------------------------------------

PRACTICE_BRIEF_VOICE_BLOCK = (
    "AUDIENCE: a football coach reading this on their phone before"
    " practice. They speak football, NOT anatomy / biomechanics /"
    " sports medicine.\n"
    "\n"
    "TRANSLATION TABLE — anatomy region in context → football word"
    " in your prose:\n"
    "  shoulder_girdle    -> 'throwing shoulder' or 'shoulder'\n"
    "  elbow_complex      -> 'throwing elbow' or 'elbow'\n"
    "  wrist_complex      -> 'wrist' or 'throwing hand'\n"
    "  ankle_complex      -> 'ankles' or 'feet'\n"
    "  hip_flexor_complex -> 'hips' or 'drive leg'\n"
    "  glute_max          -> 'glutes' or 'drive leg'\n"
    "  core_outer         -> 'core'\n"
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
# section.
PRACTICE_BRIEF_REASONING_LANGUAGE = "football language"


# ---------------------------------------------------------------------------
# form_brief.py — audience + translation tables + banned vocab + voice.
# Football form-coach is deferred to Step 6+ (passing/kicking gestures need
# their own pose-measurement R&D), but the prelude is scaffolded so the
# registry has a complete surface for every sport.
# ---------------------------------------------------------------------------

FORM_BRIEF_VOICE_BLOCK = (
    "AUDIENCE: a football player or their coach reading on their phone."
    " They speak football, NOT anatomy, NOT biomechanics, NOT sports medicine."
    " If a 16-year-old player or a high-school coach would not say it on"
    " the field, do not write it.\n"
    "\n"
    "EVERY SENTENCE GENERATES A SOLUTION."
    " Do not describe a problem without immediately telling them what to DO"
    " about it on their next throw or next rep."
    " The brief is a fix-list, not a diagnosis."
    " Pair every flag with an action they can take TODAY.\n"
    "\n"
    "STRUCTURE (problem-paired-with-fix):\n"
    "- Sentence 1: name the biggest visible problem in plain language AND"
    " the cue that fixes it, in the same sentence.\n"
    "- Sentence 2: a concrete physical cue they can feel on their NEXT rep"
    " to check the fix is working.\n"
    "- Sentence 3: name ONE drill by its slug from the context above and"
    " tell them the ONE thing to focus on during reps — not why the drill"
    " works.\n"
    "- Sentences 4-5 (optional, only if a second signal is flagged or"
    " there is a safety risk): same problem→fix pairing."
    " If a flag is a safety risk, lead with 'Fix this before you keep"
    " throwing:' and prescribe the action.\n"
    "\n"
    "NUMBER RULE: if you reference a number from the measurements, say it"
    " in plain English. NEVER write the raw measurement name and NEVER"
    " write '32.3deg' or '0.2ratio' — those are debug strings, not coach"
    " speech.\n"
    "\n"
    "TRANSLATION TABLE — anatomy region in context → football word"
    " in your prose:\n"
    "  shoulder girdle   -> 'throwing shoulder' or 'shoulder'\n"
    "  elbow complex     -> 'throwing elbow' or 'elbow'\n"
    "  wrist complex     -> 'wrist' or 'throwing hand'\n"
    "  ankle complex     -> 'ankles' or 'feet'\n"
    "  hip complex       -> 'hips' or 'drive leg'\n"
    "  knee              -> 'knees'\n"
    "  core              -> 'core'\n"
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
    " Imperative verbs ('drive', 'plant', 'snap', 'finish', 'load',"
    " 'square up', 'rise'). Sentences short — feel the urgency of a"
    " two-minute drill. No promotional language. No emojis."
    " No exclamation marks. No rhetorical questions.\n"
)
