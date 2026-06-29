---
id: "<project-id>"
title: "<project title>"
owner: "<owner>"
status_date: "<YYYY-MM-DD>"
status_summary: "<one-line summary>"
stage: "<discovery|proposal|active|build|pilot|paused|closed>"
next_action: "<clear next step>"
next_action_owner: "<owner>"
next_review_date: "<YYYY-MM-DD>"
priority: "<high|medium|low>"
sensitivity: "<public|internal|confidential>"
core_section: "<section-id matching an entry in memory/_sections.json>"
core_order: <number>
archive_status: "active"
canonical: true
---

# Project: <project title>

**Last updated:** <YYYY-MM-DD>  
**Status:** <YYYY-MM-DD> — <full current status>  
**Owner:** <owner>

---

## Profile

Who or what this project is about, and why it exists.

## Scope

- <bullet>
- <bullet>
- <bullet>

## Decision log

| Date | Decision | Why it matters | Owner |
|---|---|---|---|
| <YYYY-MM-DD> | <example decision> | <short rationale> | <name> |

## Key documents

- `materials/<project>/01-inputs/…`
- `materials/<project>/02-working/…`
- `materials/<project>/03-deliverables/…`

## Open items

- [ ] <item>
- [ ] <item>

## Risks / blockers

- <risk>
- <risk>

## Key insights

Durable project-specific learnings only.

- <insight>
- <insight>

## Update rules

- This file is the source of truth for project detail.
- Keep the status line date-prefixed (`YYYY-MM-DD — …`).
- Keep `next_action` and `next_review_date` current.
- Set `archive_status: "archived"` and move the file into `memory/projects/archive/`
  when the project closes or goes cold.

## See also

- Core memory: [memory/core.md](../core.md)
- Project index: [memory/projects/README.md](README.md)
- Materials: `materials/<project>/`
