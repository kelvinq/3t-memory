# inbox — active intake queue

**Last updated:** YYYY-MM-DD

> `inbox/` is for unclassified files only. Anything that has a known
> project home is *evidence* and belongs in `materials/<project>/<NN>-*/`.
> The agent may route items here on your behalf; files older than 7 days
> are stale and flagged by `scripts/workspace_check.py`. Files in
> `inbox/pending-user/` need a human decision (operator) and are flagged
> after 14 days.

| File | Received | Project? | Action | Status |
|---|---|---|---|---|
| `inbox/example.pdf` | YYYY-MM-DD | unilever-launch | moved to `materials/unilever-launch/01-inputs/example.pdf` | done YYYY-MM-DD |
| `inbox/example-screenshot.png` | YYYY-MM-DD | (unfiled) | needs triage — see `inbox/intake-note-example.md` | pending |

## How this queue is kept honest

The agent tries to route every item out as soon as it arrives. If it
cannot decide confidently, it writes an intake note (see
[`templates/intake-note.md`](intake-note.md)) and parks the file in
`inbox/pending-user/`.

Things to remember:

- Files here are **transient** by design. Once everything is routed out,
  this folder can be empty or removed; it is not a source of truth.
- A file that has been here longer than 7 days (or 14 days for
  `pending-user/`) is *stale* and will surface as a warning in CI.
- Run `python3 scripts/workspace_check.py` for the full staleness report.
