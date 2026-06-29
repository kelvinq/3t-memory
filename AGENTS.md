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

## Maintenance commands

```bash
python3 scripts/memory_refresh.py        # rebuild generated views + lint
python3 scripts/rebuild-memory-core.py   # rebuild only
python3 scripts/lint-memory.py           # lint only
```

Run `memory_refresh.py` after editing project frontmatter or the watchlist.

## File and folder conventions

- Keep the workspace root lean.
- Project work lives under `materials/<project>/`.
- For larger workstreams, use `01-inputs/`, `02-working/`, `03-deliverables/`.
- Use lowercase kebab-case for new folders.
- Archive dormant project files under `memory/projects/archive/`.
- Never hard-delete; move to a `trash/` folder if you need to remove something.
