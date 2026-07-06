# Daily tidy — paste-paste prompt

> Paste this into any coding agent (Pi, Claude Code, Cursor, Cline,
> Aider, OpenCode) **or** a chat (ChatGPT, Claude, Gemini) pointed at the
> folder. The agent does the work; you confirm.

---

## Copy-paste prompt

```text
Run the daily tidy-up for this memory workspace.

What I expect of you, in this order:

1. Read `AGENTS.md`, then `memory/core.md`, then the active project
   files.

2. Inbox sweep:
   - For every file in `inbox/` (and `inbox/pending-user/`), decide
     where it belongs.
   - Move routed files to `materials/<project>/01-inputs/` (or
     `02-working/`, `03-deliverables/`) and link them from the right
     project file under Key documents.
   - For undecided items, write an intake note using
     `templates/intake-note.md` and leave the file there with the note
     for me to decide.
   - Update `inbox/index.md` so every routed file is recorded as `done`.

3. Loose-file sweep:
   - List any files at the workspace root that are not in the
     allowlist.
   - For each one, ask: does it belong in `materials/<project>/`? If
     yes, route it. If no, ask me.

4. Status updates:
   - For any active project whose `status_date` is older than 7 days,
     update the date and summary based on what you read.
   - For any project whose `next_review_date` is in the past, flag it
     for a review.

5. Trash archive:
   - `trash/` should be empty after a tidy. If it is not, ask me if I
     want to run `python3 scripts/trash_archive.py --dry-run` and then
     commit it.

6. Refresh and lint:
   - Run `python3 scripts/memory_refresh.py`.
   - Run `python3 scripts/workspace_check.py --strict`.
   - Report any WARN or ERROR findings verbatim.

7. Hand back to me with a one-paragraph summary: what you moved, what
   you flagged, what needs my decision.

Hard rules:

- Do not delete files. Use `trash/` and stop there.
- Do not edit between the `<!-- memory-sections:start -->` /
  `<!-- memory-sections:end -->` markers in `memory/core.md`.
- If you are not sure where something belongs, ask me rather than
  inventing a project name.
- Use absolute YYYY-MM-DD dates only.

Start now with Step 1.
```

---

## Notes

- This is the "do it for me" version. The
  [`end-of-day-tidy.md`](end-of-day-tidy.md) prompt is the human-typed
  closing ritual you run when you want a quieter loop.
- If the workspace has no `inbox/` today, skip Step 2.
- If you do not want to archive trash automatically (Step 5), say so and
  the agent stops at the `--dry-run` step.
- See [`templates/intake-note.md`](../templates/intake-note.md) for the
  intake note shape this prompt expects.
