# Migration prompt — sort a pile of scattered files into the three tiers

> Use this when your workspace is already full of loose notes, transcripts,
> briefs, and half-finished memory files, and you want them sorted cleanly into
> the three-tier structure. Works with any coding agent or web interface.

---

## When to use this

Best triggered when you have:
- a `notes.md` or `memory.md` that has grown into a wall of text,
- project folders with briefs, transcripts, and deliverables all jumbled together,
- old transcripts or meeting notes that were never sorted,
- and you want to rebuild from what you have rather than start from scratch.

---

## Copy-paste prompt

```text
Help me migrate the existing files in this workspace into a clean three-tier
memory structure.

What I want:
- Durable context in memory/core.md
- Project detail in memory/projects/*.md
- Old materials in materials/ folders
- Nothing duplicated or lost

Work in this order:

Step 1 — Scan and classify
Inspect every file and folder. For each item tell me what it is (transcript,
brief, report, scratch note, memory dump, deliverable, etc.), which tier it
belongs in (1, 2, or 3), and whether it should be kept as-is, migrated, or
archived.

Step 2 — Propose the migration plan
Propose: which files become memory/core.md; which become
memory/projects/<project>.md (grouped by project); which folders become
materials/<project>/; what goes into memory/projects/archive/; what can be
discarded with my permission. Show me the plan before doing anything.

Step 3 — Execute only after I confirm
Once I approve: create or update the memory files; move or migrate the existing
materials; keep original content where possible rather than rewriting; do not
delete anything without asking first.

Step 4 — Wire up the schema and scripts
Create memory/_sections.json for my sections. Ensure
scripts/{memory_refresh,rebuild-memory-core,lint-memory}.py are present and the
generated-block markers are in memory/core.md. Set each project's frontmatter
core_section to a section id from _sections.json and archive_status: "active".

Step 5 — Clean up
Confirm memory/core.md is under 16 KB. Confirm each project file has frontmatter
(id, title, status_date, status_summary, core_section, archive_status). Run
`python3 scripts/memory_refresh.py` and report errors. Report what was migrated,
archived, and discarded.

Rules:
- Never delete without asking. Prefer migrating original content over rewriting.
- memory/core.md is a summary, not a dump — project detail stays in project files.
- Use absolute YYYY-MM-DD dates in frontmatter.
- If something does not fit neatly, flag it and ask.

Start now with Step 1.
```

---

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| Dumping all old notes into core memory | Migrate old notes to project files or `materials/` |
| Copying raw transcripts into project files | Save transcripts to `materials/<project>/`; keep only a summary in the project file |
| One giant project file per old folder | Summary in the project file; full history in `materials/` |
| Forgetting frontmatter on migrated project files | Add frontmatter so generated tables work |
| Deleting originals after migration | Archive instead of delete unless clearly trash |

Run `python3 scripts/lint-memory.py` after migration, then regenerate with
`python3 scripts/rebuild-memory-core.py`.
