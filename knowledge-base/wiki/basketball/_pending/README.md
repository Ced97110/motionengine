# `_pending/` — Patch queue for compounding query capture

This directory is the **staging area** for wiki changes derived from coach
queries and AI answers. Files here are transient: they live between the
moment a patch is emitted (by `src/lib/wiki/patch.ts`) and the moment the
promotion pipeline (`scripts/promote-patches.ts`) merges them into the
canonical wiki or quarantines them into `_rejected/`.

> This is the mechanism that closes Karpathy's LLM-wiki loop: good answers
> are filed back into the wiki as new pages / extensions / annotations.

## Directory contract

```
_pending/
  README.md              ← this file (versioned in git)
  *.json                 ← patch files (NOT committed — see .gitignore)
  _rejected/             ← quarantined patches with .reason.md files (NOT committed)
```

The directory itself is tracked, but every file *except* `README.md` is
ignored by git. This keeps the contract in source control while keeping
per-coach query traffic local.

## Patch file format

Each patch is a single JSON file named `<patch-id>.json`. The shape is
a `WikiPatch` discriminated union defined in
`src/lib/wiki/types.ts`. Three kinds:

### `new-page`

Create a brand-new canonical wiki page.

```json
{
  "id": "q-20260412-abc-20260412",
  "kind": "new-page",
  "source": { "queryId": "...", "coachId": "local", "query": "...", "answer": "...", "citations": [], "generatedAt": "2026-04-12T14:03:00Z" },
  "emittedAt": "2026-04-12T14:03:01Z",
  "rationale": "Uncited substantive answer; propose new canonical page.",
  "slug": "weak-side-flare-screen-vs-zone",
  "body": "---\ntype: concept\n..."
}
```

### `extension`

Append a new `## Coach Note` section to an existing page.

```json
{
  "id": "...",
  "kind": "extension",
  "source": { "...": "..." },
  "emittedAt": "...",
  "rationale": "Long answer citing [[zone-offense-principles]]; append as extension section.",
  "targetSlug": "zone-offense-principles",
  "sectionHeading": "## Coach Note",
  "sectionBody": "When the bottom defender stays home..."
}
```

### `annotation`

Attach a short blockquote note to an existing page.

```json
{
  "id": "...",
  "kind": "annotation",
  "source": { "...": "..." },
  "emittedAt": "...",
  "rationale": "Short answer citing [[...]]; attach as annotation.",
  "targetSlug": "zone-offense-principles",
  "note": "Shorter counter when opponent switches defender roles."
}
```

## Promotion gates

`scripts/promote-patches.ts` runs every pending patch through:

1. **Anonymization** (`src/lib/wiki/anonymize.ts`) — strips user-entered
   team names, opponent names, player/coach names, locations, dates
   within a recent window, phone numbers, and emails.
2. **Residual-PII scan** — anything phone/email-shaped left over ⇒
   reject.
3. **Optional lint** — if `scripts/lint-wiki.ts` exists, run it against
   the resulting page.
4. **Merge semantics** — `new-page` creates a new `.md`, `extension`
   appends a section, `annotation` adds a blockquote. Target-page
   existence is validated.

Rejected patches are moved to `_rejected/` alongside a `.reason.md`
file explaining the failure. Merged patches are deleted from the queue.

## Running the pipeline

```bash
npx tsx scripts/promote-patches.ts           # apply all pending patches
npx tsx scripts/promote-patches.ts --dry-run # preview only, no writes
```

## Gitignore policy

Patches contain raw coach queries (potentially PII before scrubbing) and
are generated per-coach-per-session. They MUST NOT be committed. Only
this `README.md` is tracked. See `.gitignore` for the relevant entries.
