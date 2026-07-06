# AGENTS.md — example workspace

A minimal procedural-memory file for the example workspace. In a real workspace
this would hold your workflow rules, naming conventions, and update policy.

## Context load order

1. Read `AGENTS.md`.
2. Read `memory/core.md`.
3. Read the relevant `memory/projects/<project>.md`.
4. If `materials/<project>/brief/` exists, read it **before**
   `materials/<project>/01-inputs/`. This example has no `brief/`
   folders.

## Maintenance

```bash
python3 scripts/memory_refresh.py
python3 scripts/workspace_check.py --skip-refresh
```

The `workspace_check.py` is load-bearing here: the file
`inbox/pending-user/screen-question.md` is intentionally older than
14 days, so a fresh workspace check will WARN on it. That WARN proves
the staleness check is wired into the example workspace, not just
exists in source.
