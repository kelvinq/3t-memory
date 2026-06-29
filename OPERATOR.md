# OPERATOR.md — generic template

> A **generic operator guide** for a file-based memory workspace. Copy this into
> your workspace root and adapt it. Aimed at the human (or agent) who keeps the
> memory system healthy day to day.

## What this workspace is

A three-tier file-based memory system:

| Tier | Location | Holds |
|---|---|---|
| Core (index) | `memory/core.md` | Cross-project context + generated section tables |
| Project | `memory/projects/*.md` | One canonical file per active project |
| Archive | `materials/<project>/` + `memory/projects/archive/` | Evidence, inputs, drafts, deliverables, dormant files |

Plus a working-memory tier (`sessions/`, `materials/<project>/02-working/`) for
transient scratch notes.

## Daily / weekly workflow

1. **Before a session:** read `AGENTS.md`, then `memory/core.md`, then the
   relevant project file(s).
2. **During a session:** update the project file's `Status` line and frontmatter
   (`status_date`, `status_summary`, `next_action`, `next_review_date`) as state
   changes. File new evidence under `materials/<project>/`.
3. **After a session:** run `python3 scripts/memory_refresh.py` to regenerate the
   index views and lint the workspace.

## Adding a new project

1. Copy `templates/memory-project.md` to `memory/projects/<slug>.md`.
2. Fill the frontmatter. Set `core_section` to a section id declared in
   `memory/_sections.json` and `archive_status: "active"`.
3. Create `materials/<slug>/` with `01-inputs/`, `02-working/`, `03-deliverables/`
   as needed.
4. Run `python3 scripts/memory_refresh.py`.

## Defining or changing sections

Sections are **config-driven**, not hardcoded. Edit `memory/_sections.json`:

```json
{
  "sections": [
    {
      "id": "active-work",
      "title": "Active work",
      "source": "projects",
      "columns": [
        {"key": "title", "header": "Project"},
        {"key": "status", "header": "Status", "compose": ["status_date", "status_summary"]},
        {"key": "_link", "header": "Detail", "link": true}
      ]
    },
    {
      "id": "watchlist",
      "title": "Watchlist",
      "source": "watchlist",
      "columns": [
        {"key": "project", "header": "Item"},
        {"key": "status", "header": "Status", "compose": ["status_date", "status_summary"]}
      ]
    }
  ]
}
```

- `source: "projects"` → collects active project files whose `core_section`
  frontmatter matches this section's `id`.
- `source: "watchlist"` → renders rows from `memory/watchlist.json`.
- `columns[].compose` joins multiple fields with " — ".
- `columns[].link: true` renders a markdown link to the project file.

Re-run `memory_refresh.py` after changing the schema.

## Archiving a project

1. Set `archive_status: "archived"` in the project frontmatter.
2. Move the file into `memory/projects/archive/`.
3. Optionally add an entry to `memory/watchlist.json` if it should still appear
   in a dormant view.
4. Run `python3 scripts/memory_refresh.py`.

## Watchlist

`memory/watchlist.json` is a flat list of dormant items:

```json
[
  {
    "project": "Example dormant item",
    "status_date": "2026-05-16",
    "status_summary": "Paused waiting on external decision.",
    "order": 10
  }
]
```

Items render in any section declared with `"source": "watchlist"`.

## Size policy for core memory

- **target:** under 16 KB
- **warning:** over 20 KB
- **hard stop:** over 24 KB (lint errors)

If core memory grows, push detail down into project files or the archive.

## Troubleshooting

- **"missing the generated-block markers"** — your `memory/core.md` lost the
  `<!-- memory-sections:start -->` / `<!-- memory-sections:end -->` markers.
  Re-copy them from `templates/memory-core.md`.
- **Section not appearing** — the project's `core_section` value does not match
  any `id` in `_sections.json`, or `archive_status` is not `active`.
- **Lint errors on size** — trim `memory/core.md`; move detail to project files.
