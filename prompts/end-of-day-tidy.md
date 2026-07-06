# End-of-day tidy — the human closing ritual

> This is the shorter, human-typed prompt for end of session. It mirrors
> the agent-run [`daily-tidy.md`](daily-tidy.md) but expects you to drive
> the steps; the agent only reads and writes.

---

## Copy-paste prompt

```text
Run my end-of-day tidy.

In order:

1. Read `AGENTS.md` and `memory/core.md` if I have not loaded the
   folder today.

2. For each active project file:
   - If anything changed today, update the `status_date`,
     `status_summary`, `next_action`, and `next_review_date`.
   - Add any new evidence to `materials/<project>/01-inputs/`,
     `02-working/`, or `03-deliverables/` and link it from the project
     file under Key documents.

3. Sweep `inbox/` and `inbox/pending-user/`. Decide the route for
   anything that has been sitting there. Update `inbox/index.md` to
   reflect what you moved.

4. If there is anything in `trash/`, run
   `python3 scripts/trash_archive.py --dry-run` first, confirm with me,
   then run the real archive.

5. Run `python3 scripts/memory_refresh.py` and `python3 scripts/workspace_check.py`.
   Read the findings. Triage any WARN or ERROR findings into one of:
   - "routed now" — file moved;
   - "decision logged" — added a `pending` line in `inbox/index.md`;
   - "deferred" — added an open item to the project file with a
     `next_review_date`.

6. Tell me in three lines: what is now stale, what is now waiting on me,
   what is closed for today.

Hard rules:

- Use absolute YYYY-MM-DD dates only.
- Do not hard-delete. Use `trash/`. It is recoverable; deletions are not
  until I confirm them after the 90-day archive expiry.
- Do not edit between the `<!-- memory-sections:start -->` /
  `<!-- memory-sections:end -->` markers.
- If a project feels stuck, change nothing; flag it in its project file
  with an `Open items` entry and a `next_review_date` that forces you to
  come back to it.

Start now.
```

---

## Notes

- For a fully agent-run version of this ritual, see
  [`daily-tidy.md`](daily-tidy.md).
- The morning question is [`daily-checkin.md`](daily-checkin.md).
- The archive expiry rules live in `OPERATOR.md` under "Tidy-up
  procedure"; this prompt just runs them.
