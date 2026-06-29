# Installer prompt — install the three-tier memory system from scratch

> Copy-paste this into any coding agent (Pi, Claude Code, Cursor, Cline, Aider,
> OpenCode, …) **or** into a web chat (ChatGPT, Claude, Gemini) and save the
> resulting files into a folder. Works on an empty or near-empty workspace.

---

## Copy-paste prompt

```text
Help me install a three-tier, file-based memory system in this workspace.

Goal: create a simple, durable memory system that keeps context across sessions
without stuffing everything into one huge file or into a chat product's memory.

The system uses three tiers:

- Tier 1 — Core memory: one small file for durable context (who I am, my role,
  key collaborators, active work, reusable lessons). File: memory/core.md
- Tier 2 — Project memory: one file per active project (scope, status, key
  documents, open items, insights). Folder: memory/projects/
- Tier 3 — Archive: old transcripts, briefs, reports, artefacts. Folder: materials/
- Working memory (not durable): scratch notes in sessions/ or
  materials/<project>/02-working/.

Work in this order:

Step 1 — Explain it simply
Give me a short plain-English explanation of the three tiers before we build
anything. Assume I have not read about this before.

Step 2 — Inspect the workspace
Scan the current folder. Identify existing project folders, notes, transcripts,
reports, or memory-like files, and flag anything that looks like it belongs in
Tier 1, 2, or 3.

Step 3 — Ask setup questions
Ask the minimum set needed to build the system well. Do not create files yet.
Cover at least: my role and the kind of work I do; whether I am starting fresh
or migrating existing material; how I want to track status; whether I work
across more than one machine.

Step 4 — Propose the design
After I answer, propose the exact file/folder structure, the section headings for
memory/core.md, the template for memory/projects/<project>.md, the rules for
what goes in each tier, and (if I have existing files) a migration plan. Show me
before writing anything.

Step 5 — Build only after I confirm
Create the files I approved. Do not create files I did not ask for.

Step 6 — Wire up the schema and scripts
Create memory/_sections.json defining my sections (source: "projects" or
"watchlist", with columns). Ensure scripts/memory_refresh.py, rebuild-memory-core.py,
and lint-memory.py are present. Leave the generated-block markers
<!-- memory-sections:start --> … <!-- memory-sections:end --> exactly in place
in memory/core.md.

Step 7 — Verify and explain maintenance
Run `python3 scripts/memory_refresh.py` and confirm 0 errors. Give me a short
maintenance guide: when to update Tier 1, Tier 2, when NOT to update memory, and
when to archive a project.

Rules:
- memory/core.md must stay small. Target under 16 KB; hard limit 24 KB.
- Do not duplicate project detail between core and project files. Project files
  are authoritative.
- Only store durable context in memory. One-session deliverables go in materials/.
- Use absolute YYYY-MM-DD dates only. No relative dates like "next week".
- Prefer Markdown and plain structure over fancy formatting.
- If existing files contain useful material, migrate it; do not rewrite from
  scratch. Do not delete anything without asking first.

When creating memory/core.md, include: title/owner/last updated; purpose and
context; key collaborators; the generated-section markers; key learnings and
principles; approach and patterns; tools and resources; update rules.

When creating a project memory file, include frontmatter (id, title, status_date,
status_summary, stage, next_action, next_review_date, priority, core_section,
core_order, archive_status, canonical) plus sections: profile, scope, decision
log, key documents, open items, risks/blockers, key insights.

Start now with Step 1.
```

---

## Notes

- If your agent cannot run Python, skip the script step and hand-edit the
  generated tables. The files are still valid.
- If you are migrating **from ChatGPT or Claude**, switch to
  [`migrate-from-claude-chatgpt.md`](migrate-from-claude-chatgpt.md) instead —
  it is tuned for that starting point.
- If you instead have a pile of scattered local files, use
  [`migrate.md`](migrate.md).
