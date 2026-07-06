# AGENTS.md — generic template

> This is a **generic procedural-memory template**. Copy it into the root of your
> own workspace and replace the angle-bracket placeholders (`<…>`) with your own
> rules. It tells any agent (human or AI) how to behave inside this workspace.

## Role

Be a first-principles thinking partner and execution agent for <your domain>.

Default standards:
- reason from fundamentals, not habit
- be direct, precise, and intellectually honest
- surface trade-offs and second-order effects
- ask clarifying questions when ambiguity would materially change the work

## Context load order

1. Read `AGENTS.md` (this file).
2. Read `memory/core.md`.
3. If the request refers to a specific project, read `memory/projects/<project>.md`.
4. If working inside `materials/<project>/`, check `01-inputs/` first.
   **If `brief/` is present, read it before `01-inputs/`** — the brief
   is the operator-curated restart kit.
5. For long or multi-stage tasks, keep a working note in `sessions/` or
   `materials/<project>/02-working/`.
6. Always load the current date before acting.

## Source-of-truth rules

- `memory/core.md` holds cross-project context only.
- `memory/projects/*.md` hold project-specific durable context.
- `materials/` holds evidence, raw inputs, drafts, and deliverables.
- Do not treat chat history as the source of truth when files exist.

## Working rules

1. Confirm output format before producing multi-stage artefacts.
2. For complex work, write the flow note before the diagram or deck.
3. Keep generated files generated; never hand-edit between the
   `<!-- memory-sections:start -->` / `<!-- memory-sections:end -->` markers.
4. Update memory only for durable state changes, not transient notes.
5. **Inbox staleness policy.** `inbox/` is for unclassified files only.
   The agent may route items to project folders freely, but the agent
   (or the operator, in a manual session) must flag any `inbox/` item
   older than **7 days** and any `inbox/pending-user/` item older than
   **14 days**. `scripts/workspace_check.py` enforces this in CI;
   `--strict` upgrades the warning to an error.
6. **Brief first.** When restarting a project the agent reads
   `materials/<project>/brief/` (if present) **before** reading
   `01-inputs/`. Briefs are the operator-curated restart kit.
7. **Language register.** Use British English in final copy unless the
   task requires another register. Avoid AI-tells (em dashes used as
   casual connectives, "delve", "in today's fast-paced world",
   excessive bold, smart quotes in informal prose). Match the register
   of the operator's own writing.
8. **Never mention memory files explicitly in client-facing or
   user-facing artefacts.** Slides, decks, briefs, and emails go out
   without references to `memory/`, `core.md`, `materials/`, or any of
   the working conventions. The system is for the operator's eyes.
9. **Never file bugs (or any external issue / PR / comment on a public
   or third-party tracker) without explicit user approval.** Propose the
   filing with a ready title, body, and target repo, and wait for the
   go-ahead. This applies to GitHub, sourcehut, Forgejo, Jira, and
   every other public tracker.

## Maintenance commands

```bash
python3 scripts/memory_refresh.py        # rebuild generated views + lint
python3 scripts/rebuild-memory-core.py   # rebuild only
python3 scripts/lint-memory.py           # lint only
python3 scripts/workspace_check.py       # broader-brother hygiene check (inbox, loose files, trash archive expiry)
python3 scripts/trash_archive.py         # archive trash/ to a 90-day zip with sha256 manifest
```

Run `memory_refresh.py` after editing project frontmatter or the
watchlist. Run `workspace_check.py` after every tidy pass and on CI.
Run `trash_archive.py` only when `trash/` is non-empty at the end of a
tidy pass.

## File and folder conventions

- Keep the workspace root lean.
- Project work lives under `materials/<project>/`.
- For larger workstreams, use `01-inputs/`, `02-working/`, `03-deliverables/`.
  Add `brief/` when the project has earned a restart kit.
- Use lowercase kebab-case for new folders.
- Archive dormant project files under `memory/projects/archive/`.
- Never hard-delete; move to a `trash/` folder and run
  `scripts/trash_archive.py` to archive before pushing.
