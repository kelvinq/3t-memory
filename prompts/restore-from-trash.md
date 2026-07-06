# Restore from trash — paste-paste recovery prompt

> Paste this into any coding agent or chat pointed at the folder. The
> agent reads the trash archive manifest, lists candidates, and walks
> you through recovery without auto-deleting anything.

---

## Copy-paste prompt

```text
I need to restore one or more files from the trash archive.

Archive location (default: `~/.3t-memory-trash/`, or wherever the env
var `THREET_MEMORY_TRASH_ARCHIVE` points). Override here if you use a
different one: <path>.

What I expect of you, in this order:

1. List every `trash-*.manifest.json` in the archive directory. For each
   one, show me:
   - `created_at` (when it was archived),
   - `file_count` and `total_bytes`,
   - `expiry_date` (when the 90-day window ends),
   - the file list inside (paths and sizes).

2. Ask me which archive and which file(s) inside I want. Confirm the
   recovery target before doing anything destructive.

3. Recover:
   `unzip -d /tmp/restore <path-to-archive>`

4. Decide where each recovered file should go now:
   - `materials/<existing-project>/01-inputs/`, or
   - back into `trash/` for later, or
   - permanently (which means: archive immediately via
     `python3 scripts/trash_archive.py` — do not actually delete).

5. Update `inbox/index.md` and the relevant project file's Key documents
   section so the recovered file is not orphaned again.

6. Tell me in three lines: what was restored, where it lives now, and
   any project-file updates you made.

Hard rules:

- Never overwrite without asking. If the destination already has a file
  of the same name, ask.
- Never delete a recovered file. The trash archive expiry window is a
  safety net; if you want it gone sooner, archive it again.
- Use absolute YYYY-MM-DD dates only.

Start now with Step 1.
```

---

## Notes

- This prompt assumes you have previously run
  [`daily-tidy.md`](daily-tidy.md) or otherwise populated
  `trash/` and run `python3 scripts/trash_archive.py`. If you have never
  archived anything, there is nothing to restore.
- See `OPERATOR.md` §"Tidy-up procedure" for the recovery one-liner if
  you want a quicker path:
  `unzip -d /tmp/restore ~/.3t-memory-trash/trash-YYYY-MM-DD-HHMMSS.zip`.
- The manifests are themselves JSON. You do not need to `unzip` just to
  inspect them.
