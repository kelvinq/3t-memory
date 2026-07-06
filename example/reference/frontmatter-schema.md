# Frontmatter schema — `memory/projects/<slug>.md`

Every active project file begins with this YAML frontmatter. Fields are
required unless marked optional. Keep the schema tight: adding a field
is cheap, removing one is not (it may be referenced by your
`_sections.json` schema).

## Required

- `id` (string, slug, unique across `memory/projects/`): e.g.
  `"unilever-launch"`.
- `title` (string): the human-readable project name.
- `owner` (string): who owns this project (`"<your name or handle>"`).
- `status_date` (`YYYY-MM-DD`): the last time the status was updated.
- `status_summary` (string, ≤120 chars): one line describing current state.
- `stage` (enum or free string — depends on your section schema): e.g.
  `"active"`, `"paused"`, `"delivered"`.
- `next_action` (string): the next concrete thing to do.
- `next_action_owner` (string): who owns the next action.
- `next_review_date` (`YYYY-MM-DD`): when this project's status should
  next be re-checked.
- `core_section` (string): must equal a section `id` from
  `memory/_sections.json`. The rebuild script uses this to route rows
  into the right generated table.
- `core_order` (integer, ascending = earlier in the table): e.g. `10`,
  `20`, `30` to leave gaps for insertion.
- `archive_status` (`active` | `archived`): set to `"active"` to keep
  the project in the generated sections; set to `"archived"` and move
  the file to `memory/projects/archive/` to hide it.
- `canonical` (boolean, recommended `true`): marks this file as the
  single source of truth for the project.

## Optional but recommended

- `priority` (`low` | `medium` | `high`): helps the agent triage when
  many projects are active.
- `sensitivity` (`public` | `internal` | `confidential`): documents who
  is allowed to read the project file; mirrors a `.gitignore` boundary.
- `tags` (list of strings): free-form labels for filtering; not used by
  the rebuild script unless your `_sections.json` opts in.

## Optional — section-specific

If your section schema defines additional columns (e.g. `client`,
`budget`, `region`), they belong in the frontmatter too — anything the
rebuild script needs to render columns on the row.

## Free-form

Any additional fields are preserved by the rebuild script and rendered
as extra columns if you extend your `_sections.json` schema. Build
fields slowly.

## Worked example

```yaml
---
id: "unilever-launch"
title: "Unilever product launch plan"
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
