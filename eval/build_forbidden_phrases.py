"""Generate ``eval/forbidden_phrases.json`` from the compiled insight sidecars.

The Motion rule (parent CLAUDE.md, 2026-04-24): book-derived prose never
surfaces to users — not quoted, not paraphrased, not attributed. Only
structural metadata (slugs, regions, roles, criticalities) is surfaced. This
script harvests every prose field we know is book-derived and emits them as
a verbatim blocklist the brief / halftime scorer greps against.

Sources today:
- ``compiled/page-insights.json``  → anatomy key_principles + common_mistakes;
  drill coaching_cue + safety_tip + primary_form_error.
- ``compiled/defending-insights.json`` → symptom + remedy pairs (near-verbatim
  from S1 Let's Talk Defense, per memory ``wiki-corpus-debt.md``).

Output: ``eval/forbidden_phrases.json`` — a JSON array of phrase strings.
Only phrases ≥ ``_MIN_LEN`` characters are kept, so short generic coaching
language ("stay square") does not over-match Motion-voice output.
"""

from __future__ import annotations

import json
from pathlib import Path

_MIN_LEN = 40  # below this, phrases are too generic to be "book-derived"

_BACKEND = Path(__file__).resolve().parent.parent
_COMPILED = _BACKEND / "knowledge-base" / "wiki" / "compiled"
_OUT = _BACKEND / "eval" / "forbidden_phrases.json"


def _harvest_page_insights(raw: dict) -> list[str]:
    phrases: list[str] = []
    for payload in raw.values():
        for p in payload.get("key_principles") or []:
            t = (p.get("text") or "").strip()
            if t:
                phrases.append(t)
        for m in payload.get("common_mistakes") or []:
            t = (m.get("symptom") or "").strip()
            if t:
                phrases.append(t)
            t = (m.get("remedy") or "").strip()
            if t:
                phrases.append(t)
        cue = (payload.get("coaching_cue") or "").strip()
        if cue:
            phrases.append(cue)
        safety = payload.get("safety_tip") or {}
        if isinstance(safety, dict):
            t = (safety.get("text") or "").strip()
            if t:
                phrases.append(t)
        form_err = payload.get("primary_form_error") or {}
        if isinstance(form_err, dict):
            for k in ("symptom", "consequence", "correction"):
                t = (form_err.get(k) or "").strip()
                if t:
                    phrases.append(t)
    return phrases


def _harvest_defending_insights(raw: dict) -> list[str]:
    phrases: list[str] = []
    for payload in raw.values():
        for s in payload.get("symptoms") or []:
            t = (s.get("symptom") or "").strip()
            if t:
                phrases.append(t)
            t = (s.get("remedy") or "").strip()
            if t:
                phrases.append(t)
    return phrases


def build_forbidden_phrases() -> list[str]:
    page_raw = json.loads((_COMPILED / "page-insights.json").read_text(encoding="utf-8"))
    defending_raw = json.loads(
        (_COMPILED / "defending-insights.json").read_text(encoding="utf-8")
    )
    phrases = _harvest_page_insights(page_raw) + _harvest_defending_insights(defending_raw)
    # Dedupe, preserve order, drop short/generic lines.
    seen: set[str] = set()
    out: list[str] = []
    for p in phrases:
        key = p.lower()
        if len(p) < _MIN_LEN or key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def main() -> None:
    phrases = build_forbidden_phrases()
    _OUT.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {_OUT.relative_to(_BACKEND)} — {len(phrases)} phrases")


if __name__ == "__main__":
    main()
