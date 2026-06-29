# AGENTS.md — example workspace

A minimal procedural-memory file for the example workspace. In a real workspace
this would hold your workflow rules, naming conventions, and update policy.

## Context load order

1. Read `AGENTS.md`.
2. Read `memory/core.md`.
3. Read the relevant `memory/projects/<project>.md`.

## Maintenance

```bash
python3 scripts/memory_refresh.py
```
