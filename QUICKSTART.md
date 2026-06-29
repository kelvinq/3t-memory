# QUICKSTART — from zero to a working memory system

This guide takes you from an empty folder to a lint-clean, self-regenerating
memory system holding **your own** documents. It assumes only Python 3.9+.

Every angle-bracket token (`<owner>`, `<YYYY-MM-DD>`, `<project>`) is a
placeholder for you to replace.

---

## 0. What you will end up with

```text
my-workspace/
├── AGENTS.md
├── OPERATOR.md
├── memory/
│   ├── core.md
│   ├── _sections.json
│   ├── watchlist.json
│   └── projects/
│       ├── README.md          # generated
│       ├── archive/
│       └── acme-launch.md
├── materials/
│   └── acme-launch/
│       ├── 01-inputs/
│       ├── 02-working/
│       └── 03-deliverables/
├── templates/
└── scripts/
```

---

## 1. Drop the package into a fresh folder

```bash
mkdir my-workspace && cd my-workspace
# Copy everything from 3t-memory/ EXCEPT the example/ folder:
cp -r /path/to/3t-memory/{AGENTS.md,OPERATOR.md,README.md,QUICKSTART.md,memory,templates,scripts} .
```

You should now have `AGENTS.md`, `scripts/`, `templates/`, and a `memory/`
folder containing `_sections.json`? — not yet. The package ships a minimal
`memory/` with only `watchlist.json`. Create the schema and core file next.

## 2. Write your `AGENTS.md`

Open `AGENTS.md` and replace the placeholders. This is your procedural memory —
the rules any agent (human or AI) follows in this workspace. Keep it short.

## 3. Create `memory/core.md` from the template

```bash
cp templates/memory-core.md memory/core.md
```

Edit it:
- set `owner:` and the `# Memory — <owner / role>` heading,
- write 2–5 paragraphs of **Purpose & context**,
- list your **Key collaborators**.

Leave the `<!-- memory-sections:start --> … <!-- memory-sections:end -->`
markers exactly where they are — the rebuild script fills between them.

## 4. Define your sections in `memory/_sections.json`

This is the config that makes the system domain-neutral. Create
`memory/_sections.json`. Below is a worked example for a consulting practice
with an "Active engagements" section (sourced from project files) and a
"Watchlist" section (sourced from `watchlist.json`):

```json
{
  "sections": [
    {
      "id": "active-engagements",
      "title": "Active engagements",
      "source": "projects",
      "order": 1,
      "columns": [
        {"key": "title", "header": "Engagement"},
        {"key": "client", "header": "Client"},
        {"key": "status", "header": "Status", "compose": ["status_date", "status_summary"]},
        {"key": "_link", "header": "Detail", "link": true}
      ]
    },
    {
      "id": "watchlist",
      "title": "Watchlist",
      "source": "watchlist",
      "order": 2,
      "columns": [
        {"key": "project", "header": "Item"},
        {"key": "status", "header": "Status", "compose": ["status_date", "status_summary"]}
      ]
    }
  ]
}
```

Rules:
- `source: "projects"` → the section collects active project files whose
  `core_section` frontmatter equals this section's `id`.
- `source: "watchlist"` → the section renders rows from `memory/watchlist.json`.
- `columns[].key` is a frontmatter field name (e.g. `title`, `client`,
  `stage`, `next_review_date`).
- `columns[].compose` joins several fields with " — " (handy for status lines).
- `columns[].link: true` renders a markdown link to the project file. Use it on
  a column whose `key` is `_link`.
- `order` controls section ordering (otherwise declaration order is used).

You can define as many project-sourced sections as you like — e.g.
`active-engagements`, `internal-initiatives`, `references`. Each project file
opts into one section via its `core_section` frontmatter value.

## 5. Create your first project file

```bash
mkdir -p memory/projects/archive
cp templates/memory-project.md memory/projects/acme-launch.md
```

Fill the frontmatter. **The `core_section` value must match a section `id` from
`_sections.json`:**

```yaml
---
id: "acme-launch"
title: "Acme product launch plan"
client: "Acme"
owner: "<owner>"
status_date: "2026-06-27"
status_summary: "Drafting launch brief; awaiting marketing assets."
stage: "active"
next_action: "Send launch brief for review."
next_action_owner: "<owner>"
next_review_date: "2026-07-04"
priority: "high"
sensitivity: "confidential"
core_section: "active-engagements"
core_order: 10
archive_status: "active"
canonical: true
---
```

Fill the narrative sections (Profile, Scope, Decision log, Open items, …).

## 6. Generate the index and lint

```bash
python3 scripts/memory_refresh.py
```

You should see the rebuild succeed, the section tables injected into
`memory/core.md`, a generated `memory/projects/README.md`, and a lint summary
with **0 errors**. If lint reports warnings, read them — most are missing
frontmatter fields or unresolved document paths.

## 7. Run it again to confirm idempotency

```bash
python3 scripts/rebuild-memory-core.py
git diff --quiet memory/core.md && echo "idempotent: no changes on second run"
```

The generated block is byte-stable across runs (within the same calendar day).

---

## 8. Import your own documents (concrete walkthrough)

This is the step most templates hand-wave. Here is the exact before/after.

### Before — a pile of scattered files

Imagine you have these loose files in a downloads folder:

```text
~/Downloads/
├── acme-kickoff-transcript.txt          # meeting transcript
├── acme-brief.docx                       # the engagement brief
├── acme-launch-deck.pptx                 # draft deck
└── acme-budget.xlsx                      # budget spreadsheet
```

They are evidence for the `acme-launch` project, but they are not filed or
linked from anywhere.

### Step 8a — create the project's archive folders

```bash
mkdir -p materials/acme-launch/{01-inputs,02-working,03-deliverables}
```

### Step 8b — file each document by role

| File | Role in the project | Destination |
|---|---|---|
| `acme-kickoff-transcript.txt` | raw input — a meeting record | `materials/acme-launch/01-inputs/` |
| `acme-brief.docx` | raw input — the source brief | `materials/acme-launch/01-inputs/` |
| `acme-budget.xlsx` | working artefact — numbers you iterate on | `materials/acme-launch/02-working/` |
| `acme-launch-deck.pptx` | deliverable — the thing you ship | `materials/acme-launch/03-deliverables/` |

Move them:

```bash
mv ~/Downloads/acme-kickoff-transcript.txt materials/acme-launch/01-inputs/
mv ~/Downloads/acme-brief.docx            materials/acme-launch/01-inputs/
mv ~/Downloads/acme-budget.xlsx           materials/acme-launch/02-working/
mv ~/Downloads/acme-launch-deck.pptx      materials/acme-launch/03-deliverables/
```

Result:

```text
materials/acme-launch/
├── 01-inputs/
│   ├── acme-kickoff-transcript.txt
│   └── acme-brief.docx
├── 02-working/
│   └── acme-budget.xlsx
└── 03-deliverables/
    └── acme-launch-deck.pptx
```

### Step 8c — link them from the project file

Open `memory/projects/acme-launch.md` and edit the **Key documents** section so
every filed document is referenced by its repo-relative path:

```markdown
## Key documents

- `materials/acme-launch/01-inputs/acme-kickoff-transcript.txt` — kickoff meeting record
- `materials/acme-launch/01-inputs/acme-brief.docx` — engagement brief
- `materials/acme-launch/02-working/acme-budget.xlsx` — live budget
- `materials/acme-launch/03-deliverables/acme-launch-deck.pptx` — draft launch deck
```

### Step 8d — refresh and lint

```bash
python3 scripts/memory_refresh.py
```

The lint pass resolves every `materials/…` and `memory/…` path in your project
file and warns if any no longer exists — which is exactly what catches a renamed
or moved document before it becomes a dead link.

### Why this matters

After this step, anyone (you, a colleague, or an AI agent) who opens
`memory/projects/acme-launch.md` sees the project's current status **and** a
complete, click-through-able index of every piece of evidence behind it. The
scattered downloads pile is gone; the canonical project file is the single
entry point.

---

## 9. Daily / weekly workflow

- **Start of session:** read `AGENTS.md` → `memory/core.md` → the relevant
  project file(s).
- **During:** update the project's `Status` line and frontmatter as state
  changes; drop new evidence into the right `materials/<project>/` subfolder and
  link it from **Key documents**.
- **End:** run `python3 scripts/memory_refresh.py`.

## 10. When to archive

When a project closes or goes cold:

1. Set `archive_status: "archived"` in its frontmatter.
2. Move the file into `memory/projects/archive/`.
3. Optionally add an entry to `memory/watchlist.json` if you still want it
   visible in a dormant view.
4. Run `python3 scripts/memory_refresh.py`.

The project disappears from generated active sections but stays recoverable in
the archive.

---

## Verifying it works

A fully worked, minimal example workspace ships at
[`example/`](example/). From inside it:

```bash
cd example
python3 scripts/memory_refresh.py     # must exit 0
python3 scripts/lint-memory.py        # must report 0 errors
python3 scripts/rebuild-memory-core.py # run twice; memory/core.md is unchanged
```

If those pass, the system is wired correctly. Copy the example as a starting
point and replace its contents with your own.
