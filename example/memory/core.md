---
file_role: core-memory
version: 2
owner: "<owner>"
last_updated: "<YYYY-MM-DD>"
status_model: date-prefixed-status-lines
canonical: true
---

# Memory — <owner / role>

**Last updated:** <YYYY-MM-DD>  
**Historical archive root:** `materials/`

---

## Purpose & context

This is a tiny example workspace showing the generic 3T memory system in action.
It exists to prove the scripts regenerate and lint cleanly from a fresh
invocation. Replace this narrative with your own role, remit, and durable
working constraints.

## Key collaborators

- <name> — role / why they matter

<!-- memory-sections:start -->
## Active work

| Project | Stage | Status | Detail |
|---|---|---|---|
| Acme product launch | active | 2026-06-27 — Drafting launch brief; awaiting marketing assets. | [`link`](projects/acme-launch.md) |

## Reference notes

| Note | Status | Detail |
|---|---|---|

## Watchlist

| Item | Status |
|---|---|
| Northwind partnership | 2026-06-20 — Paused awaiting their legal review. |
<!-- memory-sections:end -->

## Key learnings & principles

1. **Files are the source of truth:** human-readable files beat opaque chat memory.

## Approach & patterns

- Regenerate, don't hand-maintain, the index views.

## Tools & resources

- Maintenance: `python3 scripts/memory_refresh.py`

## Update rules

- Keep this file under 16KB.
- Run `memory_refresh.py` after editing project frontmatter.

## See also

- Workspace entry: [AGENTS.md](../AGENTS.md)
- Project index: [memory/projects/README.md](projects/README.md)
