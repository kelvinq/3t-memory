# Daily check-in — "what am I waiting on today?"

> Paste this into any coding agent or chat pointed at the folder. The
> agent reads memory; you stay in chat.

---

## Copy-paste prompt

```text
Good morning. Run my daily check-in.

In one paragraph, answer:

- What am I waiting on today?
- Which of my active projects have a `next_action` I should look at?
- Anything with a `next_review_date` in the past or today?
- Anything in `inbox/` or `inbox/pending-user/` older than the staleness
  thresholds (7d for `inbox/`, 14d for `inbox/pending-user/`)?
- Any trash archives whose 90-day expiry is approaching?

Read order:

1. `AGENTS.md`
2. `memory/core.md`
3. Every active `memory/projects/*.md` whose `archive_status` is
   `active` and whose `status_date` is within the last 30 days
4. `inbox/index.md` (if present)
5. `memory/watchlist.json`

Be specific. Cite project slug and date. If everything is up to date,
say so in one line.

Hard rules:

- No timeline-style rephrasing ("next week", "soon"). Use absolute
  YYYY-MM-DD dates only.
- Do not invent detail. If a project's `next_action_owner` is not me,
  say so.
- If something needs an inbox decision today, point me at the file and
  the intake note.

Start now.
```

---

## Notes

- The companion close-of-day prompt is
  [`end-of-day-tidy.md`](end-of-day-tidy.md).
- If you want a fully agent-run maintenance loop, use
  [`daily-tidy.md`](daily-tidy.md) instead.
- The staleness thresholds (7d / 14d) match `scripts/workspace_check.py`
  defaults.
