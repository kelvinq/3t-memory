# inbox — active intake queue (example)

**Last updated:** YYYY-MM-DD

> This is a worked example showing the inbox workflow in motion. The
> entries below reference the files in this example workspace. Run
> `python3 scripts/workspace_check.py` from inside `example/` to see
> what the staleness check thinks of this queue.

| File | Received | Project? | Action | Status |
|---|---|---|---|---|
| `inbox/vendor-quote.txt` | YYYY-MM-DD | acme-launch | moved to `materials/acme-launch/01-inputs/vendor-quote.txt` | done YYYY-MM-DD |
| `inbox/transcript-call.txt` | YYYY-MM-DD | acme-launch | moved to `materials/acme-launch/01-inputs/transcript-call.txt` | done YYYY-MM-DD |
| `inbox/pending-user/screen-question.md` | YYYY-MM-DD | (unfiled) | awaiting operator decision | pending |

## What this example proves

A few days after the queue was last refreshed, `inbox/pending-user/screen-question.md`
was added but never routed (the agent could not classify it confidently).
This file is intentionally older than 14 days so that
`scripts/workspace_check.py` flags it as stale. The acceptance run in
the CI (`memory_refresh.py --strict` + `workspace_check.py`) is
designed to **keep a WARN on this file present** — the WARN proves that
the staleness check is wired into the example workspace, not just
exists in source.
