---
title: Wiki-Ops TypeScript → Python Migration
status: Proposal — 2026-04-13
authors: Cédric + Claude
review: Requires review before implementation
depends_on:
  - frontend/docs/specs/diagram-fidelity-v2.md
  - backend/spec/karpathy-llm-wiki.md
  - backend/CLAUDE.md
  - frontend/CLAUDE.md
---

# Wiki-Ops Python Migration

## 1. Goal

Move Motion's wiki-operations tooling — the CLI scripts that ingest PDFs, resolve diagrams, synthesize plays, and lint the compiled wiki — from TypeScript under `frontend/scripts/*.ts` to Python under the backend, while leaving the runtime and UI-coupled TypeScript code (play viewer, parser, translator, validators, Playwright tests) untouched. The wiki and its raw source PDFs already live on the backend; the tools that read and write those files belong with them. A Python stack also gives the team a stronger PDF and imaging ecosystem (PyMuPDF or pypdfium2 for rasterization, Pillow for cropping, OpenCV for bbox detection), aligns with the existing `pipeline/*.py` and `lib/` Python code, and reduces the coupling between the Next.js build and scripts that have no need for Next.js at all.

## 2. Classification of `frontend/scripts/*.ts`

| Script | Decision | Justification |
|---|---|---|
| `ingest.ts` (`frontend/scripts/ingest.ts:1`) | MOVE | Pure CLI. Reads a PDF from `backend/knowledge-base/raw/`, calls Claude with a native PDF document block, writes markdown under `backend/knowledge-base/wiki/`. Zero FE coupling. |
| `resolve-diagrams.ts` (`frontend/scripts/resolve-diagrams.ts:1`) | MOVE | CLI. Reads wiki markers, rasterizes PDF pages, calls Claude with a tool-forced response, writes a `diagram-positions` fenced block back into the wiki file. See §6 for the schema-v2 contract. |
| `extract-diagrams.ts` (`frontend/scripts/extract-diagrams.ts:1`) | DELETE (superseded) | Comment at `frontend/scripts/synthesize-plays.ts:6-14` explicitly names this script as its predecessor. Two-pass Claude-plus-pdftoppm extractor replaced by synthesize + resolve. Out before port starts. |
| `synthesize-plays.ts` (`frontend/scripts/synthesize-plays.ts:1`) | MOVE with glue (see §6) | Calls Claude for a SemanticPlay, then invokes `synthesizePlay` / `synthesizePlayFromDiagram` / `validateSemanticPlay` from `frontend/src/lib/court/synthesize.ts` (imported at `frontend/scripts/synthesize-plays.ts:32-37`). The translator is load-bearing TS. Python writes JSON; a thin TS shim emits `src/data/plays/*.ts`. |
| `lint-wiki.ts` (`frontend/scripts/lint-wiki.ts:1`) | MOVE | Pure filesystem + regex + frontmatter parse. Read-only. No Claude, no FE types. |
| `check-nba-terms.ts` (`frontend/scripts/check-nba-terms.ts:1`) | MOVE | Pure regex scan over `src/` and `backend/knowledge-base/wiki/`. IP gate. Runs in CI; must remain runnable from both frontend and backend CI until FE stops invoking it (see §5). |
| `count-pages.ts` (`frontend/scripts/count-pages.ts:1`) | MOVE | 22 lines, `pdf-lib`. Trivial port with PyMuPDF or pypdfium2 page count. |
| `detect-page-offsets.ts` (`frontend/scripts/detect-page-offsets.ts:1`) | MOVE | Claude-backed one-shot per PDF; writes `scripts/.page-offsets.json`. Move the artifact path with it (§4). |
| `compute-fidelity.ts` (`frontend/scripts/compute-fidelity.ts:1`) | STAY (for now) | Imports `frontend/src/lib/fidelity/score.ts` and `revalidateAllPlays`. Tightly coupled to the FE validator. Port deferred until the validator itself moves or a Python equivalent is written (§13). |
| `promote-patches.ts` (`frontend/scripts/promote-patches.ts:1`) | STAY (for now) | Imports `frontend/src/lib/wiki/promote.ts` and `frontend/src/lib/wiki/types.ts`. Same coupling; same deferral. |
| `resynth-manifest.ts` (`frontend/scripts/resynth-manifest.ts:1`) | MOVE | Read-only filesystem scan + `gray-matter` frontmatter. No FE lib imports. Python equivalent is straightforward. |
| `revalidate-plays.ts` (`frontend/scripts/revalidate-plays.ts:1`) | STAY | Imports `validateSemanticPlay` from `frontend/src/lib/court/synthesize.ts` and dynamically loads `src/data/plays/*.ts` via `pathToFileURL`. Pure TS artifact validator. Port would require rewriting the validator in Python; out of scope. |
| `run-evals.ts` (`frontend/scripts/run-evals.ts:1`) | OPEN | Two modes. Offline scorers read TS artifacts and reuse TS fidelity scorers; v2 harness reads backend evals at `backend/eval/diagram-fidelity-v2-cases.jsonl`. Port only once the scorer side (`compute-fidelity`) has moved. Mark OPEN for Phase 4. |
| `visual-audit-report.ts` (`frontend/scripts/visual-audit-report.ts:1`) | STAY | Aggregates Playwright `playwright-report/results.json` with `revalidateAllPlays`. Depends on Playwright runner that lives with the FE. No reason to move. |

Summary: MOVE = 8, STAY = 4, DELETE = 1, OPEN = 1.

## 3. Library choices

### 3.1 PDF rasterization: pypdfium2 (primary), PyMuPDF (fallback)

Both libraries render PDF pages to raster bitmaps. The decision is driven by licensing, not features.

**PyMuPDF**. Per the project's own README mirrored on Context7: "PyMuPDF is distributed under an open-source AGPL license … For organizations or developers who cannot meet the requirements of the AGPL, Artifex Software offers commercial license agreements" (source: `/pymupdf/pymupdf` README, via Context7 `resolve-library-id` on 2026-04-13). The FAQ confirms the same terms apply to the PyMuPDF4LLM subpackage (source: `/pymupdf/pymupdf` `docs/faq/index.md`). Motion's repository is Apache-2.0 (`backend/pyproject.toml:6`). Linking to AGPL-licensed code inside a shared artifact creates a copyleft obligation on the combined work that is incompatible with Apache-2.0 distribution as a closed SaaS without a commercial license from Artifex. Confidence: HIGH on the AGPL classification (verified via Context7); MEDIUM on the legal mechanics of "wiki-ops scripts run server-side only" — reasonable lawyers disagree on whether SaaS-only invocation of an AGPL binary triggers source-disclosure obligations. **VERIFY BEFORE IMPLEMENTING** with Motion's counsel if PyMuPDF is chosen. API reference is clean — `page.get_pixmap(dpi=300)` then `pix.save("page.png")` — confirmed at `/pymupdf/pymupdf` `docs/faq/index.md` and `docs/page.md`.

**pypdfium2**. Python bindings to Google's PDFium, the renderer used in Chromium. Installation via `python -m pip install -U pypdfium2` per `/pypdfium2-team/pypdfium2` README. Rendering API confirmed from the same README:

```python
bitmap = page.render(scale=1, rotation=0)  # 72 dpi at scale=1
pil_image = bitmap.to_pil()
```

Licensing: pypdfium2 itself is Apache-2.0 OR BSD-3-Clause (dual), and PDFium is BSD-3-Clause. Confidence: MEDIUM — this matches what the project historically advertises, but web verification was unavailable this session (WebFetch / WebSearch both denied). **VERIFY BEFORE IMPLEMENTING**: confirm on PyPI that the `License` classifier still reads Apache-2.0 and that no transitive dependency introduced AGPL coverage. If pypdfium2's license ever shifts, fall back to PyMuPDF plus a commercial license.

**Decision**. pypdfium2 is the primary dependency because the licensing fit with an Apache-2.0 repo is cleaner. PyMuPDF is the fallback for any feature pypdfium2 cannot deliver — e.g., if tight-bbox detection for figure cropping requires the vector-content queries PyMuPDF exposes and PDFium does not. If PyMuPDF becomes necessary, isolate it in a single module (`backend/src/motion/wiki_ops/pdf_fitz.py`) and procure a commercial Artifex license before the module ships.

**Rejected alternative**. `pdf2image` wraps the Poppler CLI. Requires a system-installed Poppler; the import line alone will fail on a stock macOS developer machine and on Vercel build images. Not suitable for a repo that runs on both local mac and Linux CI without extra apt/brew provisioning. Eliminated.

**Today's equivalent in TS**. `resolve-diagrams.ts:36` imports `pdf as pdfToImg` from `pdf-to-img`. The Python replacement is `PdfDocument("path.pdf")[page_index].render(scale=...)` then `bitmap.to_pil().save(...)` (pypdfium2). No paid system dependency, no Node.

### 3.2 Image post-processing: Pillow

Pillow is the standard choice for PIL-compatible operations (crop, paste, convert, save). It is a transitive dependency of pypdfium2's `.to_pil()` path and is MIT-licensed. Confidence: HIGH on licensing (MIT-CMU), MEDIUM on exact current version — **VERIFY BEFORE IMPLEMENTING** the minor version to pin.

### 3.3 OpenCV (optional, deferred)

`opencv-python` is a candidate for tight-bbox detection around printed diagrams if §5.2 of `diagram-fidelity-v2.md` ever pursues automated crop refinement. Not needed for Phase 1. Note only: it is Apache-2.0 (the Python package; the underlying OpenCV is Apache-2.0 as of OpenCV 4.5). Do not pull in before a concrete use case.

### 3.4 Anthropic Python SDK

Already pinned at `backend/pyproject.toml:17` as `anthropic>=0.40`. Confirmed via Context7 `/anthropics/anthropic-sdk-python`. The call pattern that replaces `client.messages.create({ ... })` in TS is the synchronous `client.messages.create(...)` in Python — same method name, same surface. Concrete examples in Context7 docs:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}]
)

if message.stop_reason == "tool_use":
    tool_use = next(block for block in message.content if block.type == "tool_use")
    print(f"Tool called: {tool_use.name}")
    print(f"Arguments: {tool_use.input}")
```

Source: `/anthropics/anthropic-sdk-python` `llms.txt` (Context7, 2026-04-13). See §9 for before/after.

PDF document blocks: the SDK exposes `BetaBase64PDFSource`, `BetaDocumentBlock`, `BetaFileDocumentSource`, `BetaPlainTextSource`, `BetaRequestDocumentBlock` types (source: `/anthropics/anthropic-sdk-python` `api.md`). The stable path uses `{"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": ...}}` inside a user message — identical shape to the TS SDK call at `frontend/scripts/resolve-diagrams.ts:1012-1019`. Confidence: HIGH that the shape is identical; MEDIUM on whether it remains under `client.messages.create` vs `client.beta.messages.create` for Motion's current SDK version — **VERIFY BEFORE IMPLEMENTING** by generating against `anthropic>=0.40` and checking whether document blocks have left beta. The current codebase uses the stable `.messages.create` path in TS, so prefer stable in Python if available.

Prompt caching: `BetaCacheControlEphemeral` and `BetaCacheCreation` types are in the SDK (source: `/anthropics/anthropic-sdk-python` `api.md`). See §10.

### 3.5 Typing and linting

`ruff` and `mypy` are already configured at `backend/pyproject.toml:45-64` with `strict = true`, `target-version = "py312"`, `disallow_untyped_defs = true`. No change. The Python rules file at `~/.claude/rules/python.md` specifies `uv run ruff check .` as the validation command; add `uv run ruff format .` and `uv run mypy src` as gates for every ported script. Confidence: HIGH (confirmed by file read).

## 4. Directory layout

New home: **`backend/src/motion/wiki_ops/`** — a proper Python package, not loose scripts. Rationale:

1. Hatchling already packages `src/motion` (`backend/pyproject.toml:43`), so `wiki_ops` gets free install, test discovery, import-time dependency resolution, and `mypy --strict` coverage.
2. Shared utilities (page-offset resolution, source-id-to-PDF mapping, wiki-dir discovery, Claude client construction) are imported, not duplicated. The TS port currently copies `SOURCE_PDFS` into at least `ingest.ts:38`, `resolve-diagrams.ts:96`, and `detect-page-offsets.ts`. Consolidate into `backend/src/motion/wiki_ops/sources.py`.
3. The FastAPI service can import from `motion.wiki_ops` at runtime if we ever want an endpoint that triggers a lint (out of scope today; don't optimize for it, but don't block it).

Proposed tree:

```
backend/src/motion/wiki_ops/
├── __init__.py
├── __main__.py              # python -m motion.wiki_ops <subcommand>
├── sources.py               # SOURCE_PDFS, source-id resolution, page-offset loader
├── wiki_dir.py              # MOTION_WIKI_DIR resolution, sibling of frontend/src/lib/wiki-loader.ts
├── claude_client.py         # single Anthropic() factory; reads ANTHROPIC_API_KEY + .env
├── pdf/
│   ├── __init__.py
│   ├── render.py            # pypdfium2 wrapper: page → PIL, PDF slice → base64
│   └── pages.py             # page count, printed-vs-physical offset math
├── ingest.py                # port of ingest.ts
├── resolve_diagrams.py      # port of resolve-diagrams.ts
├── synthesize_plays.py      # port of synthesize-plays.ts (Python half; see §6)
├── lint_wiki.py             # port of lint-wiki.ts
├── check_nba_terms.py       # port of check-nba-terms.ts
├── count_pages.py           # port of count-pages.ts
├── detect_page_offsets.py   # port of detect-page-offsets.ts
└── resynth_manifest.py      # port of resynth-manifest.ts

backend/tests/wiki_ops/
├── test_lint_wiki.py
├── test_check_nba_terms.py
├── test_resolve_diagrams_parity.py    # parity vs TS (§7)
├── test_synthesize_plays_parity.py
└── fixtures/
```

Invocation pattern: `uv run` entry points in `pyproject.toml` `[project.scripts]`, one per CLI, matching the existing `motion-api` entry (`backend/pyproject.toml:36`):

```
[project.scripts]
motion-api = "motion.main:run"
wiki-ingest = "motion.wiki_ops.ingest:main"
wiki-resolve-diagrams = "motion.wiki_ops.resolve_diagrams:main"
wiki-synthesize-plays = "motion.wiki_ops.synthesize_plays:main"
wiki-lint = "motion.wiki_ops.lint_wiki:main"
wiki-check-nba-terms = "motion.wiki_ops.check_nba_terms:main"
wiki-count-pages = "motion.wiki_ops.count_pages:main"
wiki-detect-page-offsets = "motion.wiki_ops.detect_page_offsets:main"
wiki-resynth-manifest = "motion.wiki_ops.resynth_manifest:main"
```

End-developer UX: `uv run wiki-lint`, `uv run wiki-resolve-diagrams --sample 23-flare`. Matches the existing convention (`uv run motion-api`, `uv run alembic upgrade head`, `uv run pytest`) in `backend/CLAUDE.md:21-25`.

Artifact paths move alongside the code:

| TS artifact | Python replacement |
|---|---|
| `frontend/scripts/.page-offsets.json` | `backend/src/motion/wiki_ops/page_offsets.json` (shipped), or `backend/data/page_offsets.json` if large/regenerated |
| `frontend/scripts/.resynth-manifest.json` | `backend/data/resynth_manifest.json` |
| `frontend/.env.local` (ANTHROPIC_API_KEY) | `backend/.env` (already the source of truth per `backend/CLAUDE.md:29`) |

The `backend/scripts/` directory currently holds only `init-db.sql`. It is not repurposed for Python CLIs — keep it as a DB-bootstrap dumping ground, not a mix of SQL and Python. All Python CLIs live inside the `motion.wiki_ops` package.

## 5. Glue between Python and TS

The synthesize flow is the only case where Python needs to hand work back to TS.

**The problem**. `frontend/scripts/synthesize-plays.ts:32-37` imports `synthesizePlay`, `synthesizePlayFromDiagram`, `validateSemanticPlay`, `PlayMeta`, and `SemanticPlay` from `frontend/src/lib/court/synthesize.ts`. That module contains the court coordinate lattice (`frontend/src/lib/court/positions.ts`), the cubic-Bézier curve synthesis (`frontend/src/lib/court/path.ts`), and the SemanticPlay → `Play` translator. This code is load-bearing for the play viewer and is referenced from the runtime bundle. Porting it to Python means maintaining a second implementation of coordinate math that the FE will still need in pure TS for the viewer.

**Two options considered.**

- **Option A — full port.** Rewrite `synthesize.ts` in Python. Python owns the wiki read, the Claude call, the SemanticPlay construction, the translator, the validator, and the final `.ts` file emission. The FE keeps only the runtime viewer. Upside: one language for wiki-ops. Downside: duplicates the translator — every change to court coordinates or path geometry has to be made twice and kept in sync. The existing translator is non-trivial (see `frontend/src/lib/court/synthesize.ts:89-96` on tracker initialization, `path.ts:56-106` on `curvedPath`, `path.ts:115-122` on `inferCutBias`). High risk of divergence.

- **Option B — partial port, JSON boundary.** Python orchestrates: scans wiki, calls Claude, produces a `SemanticPlay` JSON document matching the TS `SemanticPlay` type. A small TS shim (`frontend/scripts/emit-plays-from-json.ts`, kept short — ~100 lines) reads the JSON, runs the existing TS `synthesizePlay` / `synthesizePlayFromDiagram` / `validateSemanticPlay`, and writes `src/data/plays/<slug>.ts`. The translator has exactly one implementation.

**Decision: Option B.** The translator stays in TS. Python owns everything that is language-neutral (wiki I/O, Claude call, SemanticPlay schema). The JSON contract is defined once (§7) and versioned (`schema_version: "semantic-1"`). The TS shim is deliberately tiny; it is the last remaining FE-side script for the synthesize path and exists only because the translator is tied to the viewer.

**Operational shape.**

```
uv run wiki-synthesize-plays --limit 5 --out backend/data/plays-pending/
# Writes backend/data/plays-pending/<slug>.semantic.json

cd frontend
npx tsx scripts/emit-plays-from-json.ts --in ../backend/data/plays-pending/
# Writes src/data/plays/<slug>.ts + updates src/data/plays/index.ts
```

Both halves are run from a single `npm run synthesize` / `uv run` combined target — document the one-command form in `frontend/CLAUDE.md` and `backend/CLAUDE.md` once Phase 3 lands.

## 6. Eval parity strategy

Every ported Python script must be validated against its TS predecessor before the TS original is deleted. The contract is the same for each: same input → byte-identical output on a named fixture set.

1. **Freeze TS inputs and outputs.** For each script, capture a fixture set representative of current production usage:
   - `lint-wiki`: the whole current wiki, which is deterministic.
   - `check-nba-terms`: the whole wiki + `src/`.
   - `count-pages`: every PDF in `backend/knowledge-base/raw/`.
   - `resynth-manifest`: the whole wiki + `src/data/plays/`.
   - `detect-page-offsets`: one real PDF per source.
   - `ingest`, `resolve-diagrams`, `synthesize-plays`: three to five gold wiki pages and one representative PDF chunk. Claude non-determinism prevents byte-identical comparison; replace exact-match with schema-equivalence plus an LLM-judged rubric, per `frontend/docs/specs/diagram-fidelity-v2.md` §10.
2. **Run both on the same input.** One-time reference capture: run the TS script, pickle or JSON-serialize the output under `backend/tests/wiki_ops/fixtures/<script>/expected/`.
3. **Diff outputs.** Deterministic scripts: `pytest` test that runs the Python port and asserts byte-equality against the captured fixture. Claude-driven scripts: run the Python port, load output as typed dataclass / Pydantic model, assert schema shape and key invariants (all citations present, all `schema_version` match, player count within expected range) — not byte equality.
4. **Gate.** Promote-to-MOVE is gated on: green `pytest` parity suite, green `uv run ruff check`, green `uv run mypy`, and one manual eyes-on review for Claude-driven scripts before deletion of the TS original.

This eval-first approach follows `~/.claude/CLAUDE.md` Eval Discipline: "Define eval BEFORE or alongside the feature, not after".

## 7. Phase plan

Order optimizes for lowest risk and highest information: start with deterministic, pure-Python scripts; end with the Claude-driven and cross-language ones. Effort estimates are low-confidence ranges.

### Phase 1 — Deterministic ports (foundation)

Scripts: `count-pages`, `lint-wiki`, `check-nba-terms`, `resynth-manifest`.

- Acceptance: `uv run pytest backend/tests/wiki_ops/` passes. Output byte-equal to TS on fixture set.
- Effort: 1–2 engineer-days total.
- Deletes on green: none yet. TS versions stay (npm scripts still invoke them) until CI is switched in Phase 5.
- Exit criterion: Python package `motion.wiki_ops` exists, importable, covered by tests.

### Phase 2 — Page-offset detection

Scripts: `detect-page-offsets`.

- Acceptance: `uv run wiki-detect-page-offsets` produces a JSON offsets file that the TS resolver can consume unchanged (i.e., same shape as `scripts/.page-offsets.json`). Confirmed by running TS `resolve-diagrams --dry-run` against both files and diffing the plan.
- Effort: 0.5–1 day.
- Deletes on green: nothing yet.

### Phase 3 — Ingest

Scripts: `ingest`.

- Acceptance: ingesting the same PDF chunk with Python and with TS produces wiki pages that pass `wiki-lint`, have identical source-citation prefixes, identical filename slugs, and the same number of pages per chunk. Claude non-determinism means prose will differ — acceptable.
- Effort: 2–3 days. Biggest wins come from dropping `pdf-lib`'s chunked encryption-ignoring quirks in favor of pypdfium2's straightforward page-slice API.
- Deletes on green: nothing yet — keep TS `ingest.ts` as a comparison oracle until Phase 5.

### Phase 4 — Resolve diagrams

Scripts: `resolve-diagrams`.

- Acceptance: for five named gold slugs, the Python resolver emits a `diagram-positions` block that parses cleanly with `frontend/src/lib/court/diagram-positions.ts` and passes the schema-v2 shape check (`run-evals.ts --v2`). Image archive PNG names and locations are unchanged.
- Effort: 3–4 days. The tool-schema is large (`resolve-diagrams.ts:362-423`); port it verbatim into a Pydantic model or a JSON dict and pass as the `input_schema` to the tool definition.
- Deletes on green: TS `resolve-diagrams.ts` after a two-week shadow period where both run in CI and outputs are diffed weekly.

### Phase 5 — Synthesize plays (Python half)

Scripts: `synthesize-plays`, with TS shim `frontend/scripts/emit-plays-from-json.ts` as a new artifact per §5.

- Acceptance: for three named slugs, the combined Python → JSON → TS-shim pipeline produces `src/data/plays/<slug>.ts` files that pass `revalidate-plays`, `compute-fidelity`, and `test:visual` with zero regressions vs the current TS-only output.
- Effort: 3–5 days.
- Deletes on green: TS `synthesize-plays.ts`. TS shim is kept.

### Phase 6 — CI switch and TS deletion

- Update `frontend/package.json` scripts that invoke ported CLIs to call the Python version (or remove entirely if the FE has no reason to trigger them).
- Update CI workflows to `uv run` the ported CLIs.
- Remove the TS originals for every script in the MOVE column.
- Acceptance: all FE gates green (`npm run lint`, `npx tsc --noEmit`, `npm run check:nba-terms`, `npm run test:visual`); all BE gates green (`uv run pytest`, `uv run ruff check`, `uv run mypy`).
- Effort: 1 day.

### Phase 7 (OPEN) — run-evals

Only begins after Phase 5 when `compute-fidelity` also moves. Possibly never — if FE continues to own scoring, `run-evals` stays TS.

## 8. Claude API parity

The TypeScript pattern (from `frontend/scripts/resolve-diagrams.ts:1004-1033`):

```typescript
// TypeScript — current
const response = await client.messages.create({
  model,
  max_tokens: maxTokens,
  system: buildSystemPrompt(),
  messages: [
    {
      role: "user",
      content: [
        {
          type: "document",
          source: {
            type: "base64",
            media_type: "application/pdf",
            data: base64,
          },
        },
        {
          type: "text",
          text: buildUserPrompt(record, cropResult.repoRelativePath, cropResult.skippedReason),
        },
      ],
    },
  ],
  tools: [emitDiagramTool],
  tool_choice: { type: "tool", name: "emit_diagram_positions" },
});

const toolUse = response.content.find(
  (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
);
if (!toolUse) throw new Error("Claude did not return a tool call");
const input = toolUse.input as DiagramJson;
```

The Python equivalent (based on `/anthropics/anthropic-sdk-python` `llms.txt` and `api.md` via Context7, 2026-04-13; method name and argument shape confirmed):

```python
# Python — port
response = client.messages.create(
    model=model,
    max_tokens=max_tokens,
    system=build_system_prompt(),
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_b64,
                    },
                },
                {
                    "type": "text",
                    "text": build_user_prompt(record, crop_path, skipped_reason),
                },
            ],
        }
    ],
    tools=[emit_diagram_tool],
    tool_choice={"type": "tool", "name": "emit_diagram_positions"},
)

tool_use = next(
    (block for block in response.content if block.type == "tool_use"),
    None,
)
if tool_use is None:
    raise RuntimeError("Claude did not return a tool call")
diagram_input = tool_use.input  # dict; validate into a Pydantic model
```

Shape mapping:

| TS field | Python field | Source |
|---|---|---|
| `client.messages.create({...})` | `client.messages.create(...)` | `/anthropics/anthropic-sdk-python` llms.txt example |
| `tools: [...]` | `tools=[...]` | same |
| `tool_choice: { type: "tool", name: "..." }` | `tool_choice={"type": "tool", "name": "..."}` | dict-passthrough |
| `response.content.find(b => b.type === "tool_use")` | `next((b for b in response.content if b.type == "tool_use"), None)` | idiomatic Python |
| `toolUse.input as DiagramJson` | `tool_use.input` then `DiagramJson.model_validate(...)` with Pydantic | Pydantic is already a backend dep (`pyproject.toml:15`) |

One critical note on document blocks: the SDK exposes `BetaBase64PDFSource` and `BetaRequestDocumentBlock` types (`/anthropics/anthropic-sdk-python` `api.md`). The stable (non-beta) path currently accepts the dict form shown above. If the stable surface rejects `type: "document"` at Motion's pinned SDK version, fall back to `client.beta.messages.create(...)`. Confidence: MEDIUM — **VERIFY BEFORE IMPLEMENTING** by running a single call end-to-end with the current `anthropic>=0.40` pin before writing all ports against it.

## 9. Prompt caching opportunity

The port is the correct moment to land Motion's deferred prompt-caching policy. The compiled wiki system prompts for `resolve-diagrams` and `synthesize-plays` are stable across hundreds of invocations per session and are the largest static block in each call. Each call currently re-sends the full schema-v2 system prompt.

**Proposal.** Mark schema-v2 system prompts as cache-eligible using `cache_control: {"type": "ephemeral"}` on the system block. The SDK types `BetaCacheControlEphemeral` and `BetaCacheCreation` are documented in `/anthropics/anthropic-sdk-python` `api.md` (verified via Context7 2026-04-13), so the infrastructure exists. Concrete change: in the Python `messages.create` call, replace `system=build_system_prompt()` with a list-of-blocks form so cache control can attach:

```python
response = client.messages.create(
    model=model,
    max_tokens=max_tokens,
    system=[
        {
            "type": "text",
            "text": build_system_prompt(),
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[...],
)
```

Scope at Phase 4 and Phase 5 only. Do not add caching to Phase 1 ports (they don't call Claude). Measure cache-hit ratio via `response.usage.cache_creation_input_tokens` vs `response.usage.cache_read_input_tokens` per call; report weekly during the shadow period.

Confidence: HIGH that the type infrastructure is in the SDK (verified via Context7). MEDIUM on exact field names for the read/creation counters at the pinned SDK version — **VERIFY BEFORE IMPLEMENTING** by inspecting `anthropic.types.Usage` at the installed version.

## 10. Rollback plan

Every ported script stays shadowed by its TS original for a minimum of one full production cycle — defined as one successful end-to-end resolve + synthesize + visual-audit pass on the current wiki. If the Python port fails parity on any gold fixture after merge:

1. Revert the `pyproject.toml` `[project.scripts]` entry so the CLI falls back to invoking the TS version via `npm` wrapper, or remove the Python CLI from CI.
2. File an issue with the failing fixture. Do not delete the TS script.
3. Do not retry port until parity test is green on a branch.

Explicit non-invariants: no Python port is deleted if its parity test ever regresses. No TS script is deleted until its Python replacement has been the only CI-invoked version for at least two weeks and the wiki has been re-linted and re-resolved at least once with no drift.

## 11. Risks

- **AGPL exposure via PyMuPDF.** If pypdfium2 proves insufficient and PyMuPDF is pulled in, Motion's Apache-2.0 repository risks AGPL-induced source-disclosure obligations on the combined work. Mitigation: hold PyMuPDF as fallback only; isolate in one module; procure commercial Artifex license before the module ships. Confidence that this is the correct risk framing: HIGH (AGPL confirmed via Context7). Confidence on the operational mitigation: MEDIUM — **VERIFY BEFORE IMPLEMENTING** with counsel.
- **Parser drift between TS parser and Python resolver.** The Python resolver writes `diagram-positions` blocks; the TS parser (`frontend/src/lib/court/diagram-positions.ts`) reads them. A Python schema that does not match the TS parser's allowlist silently loses fields (§1 of `diagram-fidelity-v2.md` already documents this for the old allowlist). Mitigation: pin the JSON schema in one place — `backend/src/motion/wiki_ops/schemas/diagram_positions.py` as a Pydantic model auto-exported to JSON Schema, and a post-merge test that loads every block through the TS parser and asserts no dropped fields.
- **Rasterization output differences.** pdf-to-img (Chromium-adjacent) and pypdfium2 (PDFium) share a renderer ancestry, but rendered PNGs will not be byte-identical. The figure image archive is committed to the repo (`backend/knowledge-base/figures/<slug>-<idx>.png`). If the port changes every crop byte-for-byte, the next commit will show a massive diff that obscures real changes. Mitigation: (a) one-time rebaseline commit that regenerates every archived crop with pypdfium2 at an agreed DPI; (b) afterwards, only regenerate when the source PDF changes. Document the DPI and renderer choice in `backend/knowledge-base/figures/README.md`.
- **Python environment drift across macOS and Linux.** pypdfium2 ships platform wheels — Apple Silicon darwin_arm64 and manylinux x86_64 both supported per the `PDFIUM_PLATFORM` matrix (`/pypdfium2-team/pypdfium2` README, verified via Context7). Confidence HIGH that darwin_arm64 wheels exist; MEDIUM on the exact matrix for the current release — **VERIFY BEFORE IMPLEMENTING** on a fresh macOS M-series dev machine and on the GitHub Actions Linux runner. Lock dependency versions via `uv lock`; commit `uv.lock` (already present at `backend/uv.lock`).
- **Claude non-determinism breaks "byte-equal fixture" testing.** Applies only to `ingest`, `resolve-diagrams`, `synthesize-plays`. Mitigation: schema-equivalence testing (§6) instead of byte equality, and a rubric scorer per `diagram-fidelity-v2.md` §10.
- **Translator coupling if Option B glue is abandoned later.** If Motion ever decides to drop the TS shim, the translator must be ported and maintained in two languages. Mitigation: put a comment block at the top of `frontend/src/lib/court/synthesize.ts` and `backend/src/motion/wiki_ops/synthesize_plays.py` cross-linking the two; any PR that touches one without the other fails review.

## 12. Out of scope

This spec does NOT decide:

- Whether the translator (`frontend/src/lib/court/synthesize.ts`) itself moves to Python. It stays in TS; §5 explicitly commits to Option B.
- Whether the fidelity scorer (`frontend/src/lib/fidelity/score.ts`), the promote-patch pipeline (`frontend/src/lib/wiki/promote.ts`), or the revalidator (`frontend/scripts/revalidate-plays.ts`) move to Python. All three stay in TS for at least Phase 1–6.
- Whether Motion replaces TypeScript entirely. No. The FE runtime stays TS.
- Whether eval scorers (`run-evals.ts`) move. OPEN; deferred to Phase 7 at earliest.
- Whether the wiki markdown itself is re-written or versioned. No. Python ports write the same markdown shape the TS scripts write today.
- Whether Clerk, Postgres, or Render hosting change. No — orthogonal to this port.
- Whether Pydantic models replace the TS `Play` / `SemanticPlay` types across both sides. Not in this spec. JSON is the interchange format; each side owns its local types.

## 13. Open questions

Items requiring a human decision before Phase 1 starts:

1. **License posture on PDF rasterization.** Is Motion willing to carry pypdfium2 as primary and accept a licensing decision per-module if pypdfium2 proves insufficient? If the answer is "PyMuPDF is fine, we'll buy an Artifex license", the library-choice section collapses and Phase 3 timelines improve.
2. **Claude SDK beta vs stable for PDF documents.** At the pinned `anthropic>=0.40`, does `client.messages.create` accept document blocks, or must we move to `client.beta.messages.create`? Verify once against a live call before multiplying the pattern across scripts.
3. **Single combined entry point vs multiple.** Should `uv run wiki-ops` be one umbrella CLI with subcommands (`wiki-ops ingest ...`, `wiki-ops resolve-diagrams ...`), mirroring `git`-style subcommand UX, or keep the eight separate `[project.scripts]` entries proposed in §4? The former reduces `pyproject.toml` noise; the latter mirrors the current one-file-per-task TS UX. Cédric to pick.
4. **Image archive rebaseline timing.** Does the one-time renderer-change commit ship before or after Phase 4 green? If before, the archive is stable while Phase 4 is developed. If after, one commit carries both the port and the rebaseline; the diff is harder to review. Recommend: before, in a labeled commit `chore(figures): rebaseline archived crops for pypdfium2 at 300 DPI`.
5. **Shadow period length.** Two weeks is proposed in §10. Is that acceptable, or should the team want a single-cycle verification (one wiki regeneration) only? Decision drives when the TS originals are deleted.
6. **FE continues invoking wiki-check-nba-terms via `npm run check:nba-terms`?** If yes, FE needs a small wrapper that shells out to `uv run wiki-check-nba-terms` (which assumes `uv` is on the Vercel build path — **VERIFY BEFORE IMPLEMENTING**). If no, FE CI uses the Python CLI directly via a CI-level step. Recommend the latter; lower coupling.

---

End of spec.
