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
   `memory/_sections.json` and `archive_status: "active"`. The
   one-source-of-truth frontmatter schema lives at
   [`reference/frontmatter-schema.md`](reference/frontmatter-schema.md).
3. Create `materials/<slug>/` with `01-inputs/`, `02-working/`, `03-deliverables/`
   as needed. **Optional:** a `materials/<slug>/brief/` folder holds a
   short restart kit the agent reads *before* `01-inputs/` (see the
   "Brief folder" section below).
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

If core memory approaches the size policy, push detail down into
project files or the archive. **If it grows past the target anyway,
prefer expanding into sibling files under `memory/` rather than
archiving detail to projects** — see "Memory expansion files" below.

## Troubleshooting

- **"missing the generated-block markers"** — your `memory/core.md` lost the
  `<!-- memory-sections:start -->` / `<!-- memory-sections:end -->` markers.
  Re-copy them from `templates/memory-core.md`.
- **Section not appearing** — the project's `core_section` value does not match
  any `id` in `_sections.json`, or `archive_status` is not `active`.
- **Lint errors on size** — trim `memory/core.md`; move detail to project files,
  or split into an expansion file (see "Memory expansion files" below).

## Memory expansion files

`memory/core.md` is the canonical index, but it is not the only memory
file. When `core.md` approaches the size policy (target 16 KB, hard
stop 24 KB), split detail into sibling files under `memory/` and
reference them from core rather than archiving detail to project files.
Two named siblings are part of the recommended structure:

- `memory/patterns.md` — durable cross-project learnings (numbered,
  short). Each pattern is a one-paragraph rule with a "lesson source"
  date. Use this when a cross-project lesson has reached the threshold
  of "would I want a new agent to know this on day one in any project?".
- `memory/tools.md` — tools-and-skills reference (status, brief pointer,
  any gotchas that took more than an hour to find). Use this when the
  same tool gets reached for across multiple projects.

Both files use the same Markdown structure as `core.md` (headings,
`YYYY-MM-DD` dates, internal anchors). Neither has frontmatter; neither
is generated. Lint catches size regressions on `core.md` only —
expansion files are intentionally exempt.

**Rule of thumb:** if `core.md` is over 16 KB, the next refactor pulls
detail into `memory/patterns.md` (cross-project learnings) or
`memory/tools.md` (persistent tool notes), not into project files.
Project files are for project facts; expansion files are for facts
that apply across projects.

## Brief folder

A long-running project benefits from a `materials/<project>/brief/`
folder holding the smallest possible restart kit: a 5-line current
status, the most recent decisions, the open items, and any dated
context you would need on day one of a cold restart. The agent reads
`brief/` *before* `01-inputs/` when context-loading a project.
`brief/` is optional; small projects can skip it.

Load order for project restart:
1. `memory/projects/<slug>.md` (canonical status)
2. `materials/<slug>/brief/` (operator-curated restart notes, if any)
3. `materials/<slug>/01-inputs/` (raw evidence, in chronological order)

## Tidy-up procedure

When the workspace accumulates files that do not belong anywhere
obvious, follow this procedure. Run it after each work session, or
whenever something feels off.

1. **Project files → project folders.** Every file related to a specific
   project moves into `materials/<project>/` (or `01-inputs/`,
   `02-working/`, `03-deliverables/`). If the file is the highest-priority
   restart kit for that project, also (or instead) drop a short summary
   into `materials/<project>/brief/`.

2. **Orphaned files → escalate.** Files with no clear project home are
   grouped together and brought to the operator. Do not delete them.

3. **Move removals to `trash/`.** All removals go into `trash/`. Nothing
   is permanently deleted without explicit confirmation. `trash/` is
   the staging area for the next step.

4. **Archive `trash/` at the end of every tidy pass.**
   `python3 scripts/trash_archive.py` zips everything in `trash/` into
   a timestamped archive outside the repo (default
   `~/.3t-memory-trash/`), writes a JSON manifest next to the zip with
   file list, sizes, sha256, and a 90-day `expiry_date`, appends a line
   to `tidy_YYYY-MM-DD.log`, and only then empties `trash/`. The script
   is idempotent: if `trash/` is already empty, it exits 0 with no
   output. The default archive location can be overridden with
   `--archive-dir` or the `THREET_MEMORY_TRASH_ARCHIVE` environment
   variable, so users who version their archive in-repo can do so
   deliberately.

5. **Expire archives after 90 days.** Each manifest records an
   `expiry_date` 90 days after creation. `scripts/workspace_check.py`
   warns (but never auto-deletes) any archive whose expiry has passed,
   plus any expiring within 14 days. Confirm with the operator, then
   `rm` the zip and its manifest manually. **This is the only point at
   which an archive is permanently destroyed.**

6. **Recover from an archive.**
   `unzip -d /tmp/restore ~/.3t-memory-trash/trash-YYYY-MM-DD-HHMMSS.zip`
   (or read the manifest first with `unzip -l`). The zip also contains
   a human-readable `MANIFEST.txt` at the root. The paste-prompt
   companion is at
   [`prompts/restore-from-trash.md`](prompts/restore-from-trash.md).

7. **Log every movement.** Each tidy pass produces a dated log at
   `tidy_YYYY-MM-DD.log` (one log per calendar day). The log records
   zip paths, file counts, sha256, expiry dates, and the human-readable
   recovery command, so any past tidy pass is reversible from the log
   alone.

8. **Run the workspace check.** After every tidy pass, run
   `python3 scripts/workspace_check.py`. It runs `memory_refresh.py`,
   scans `inbox/` for items not in `inbox/index.md` and for items past
   staleness thresholds (see "Inbox workflow" below), lists un-routed
   loose root files, and reports any expired or soon-to-expire trash
   archives. Treat its warnings as a queue, not as a verdict; nothing
   auto-fails.

## Inbox workflow

`inbox/` is the unclassified intake queue. It is **transient by
design**: once everything is routed out, the folder can be empty or
removed; it is not a source of truth.

- The agent may route items to project folders freely; it updates
  `inbox/index.md` and links the new evidence from the right project
  file. The shipped template is
  [`templates/inbox-index.md`](templates/inbox-index.md).
- For items the agent cannot classify with confidence, write an intake
  note (template at
  [`templates/intake-note.md`](templates/intake-note.md)) and park the
  file in `inbox/pending-user/` for the operator's decision.
- **Staleness policy.** Flag any `inbox/` item older than **7 days**;
  flag any `inbox/pending-user/` item older than **14 days**.
  `scripts/workspace_check.py` enforces this; `--strict` upgrades the
  warning to an error.

For the daily rhythm that keeps the queue honest, use the paste-prompt
companions:

- [`prompts/daily-checkin.md`](prompts/daily-checkin.md) — morning:
  *"what am I waiting on today?"*
- [`prompts/end-of-day-tidy.md`](prompts/end-of-day-tidy.md) — close of
  session: the human closing ritual.
- [`prompts/daily-tidy.md`](prompts/daily-tidy.md) — the fully
  agent-run version of the end-of-day tidy.
- [`prompts/restore-from-trash.md`](prompts/restore-from-trash.md) —
  recovery if you need a file back.

## Workspace check

`scripts/workspace_check.py` is the broader-brother of
`scripts/lint-memory.py`. It catches what lint does not:

- `inbox/` items that are not yet tracked in `inbox/index.md`.
- `inbox/` items older than 7 days, `inbox/pending-user/` items older
  than 14 days.
- Loose files at the workspace root that have not been routed.
- Trash archives whose 90-day expiry has passed or is within 14 days.

Run it manually any time, and run it after every tidy pass.
`--strict` promotes stale-inbox WARN to ERROR and makes any WARN exit
non-zero, so CI on a `--strict` run fails on a stale queue.
