# Worked example — a Custom GPT migrated into the three tiers

This folder shows a complete before/after of migrating a ChatGPT **Custom GPT**
into the three-tier file-based memory system. It is deliberately small and
non-technical so the mapping is easy to follow.

Read the conceptual guide first:
[`../../MIGRATING-FROM-CLAUDE-AND-CHATGPT.md`](../../MIGRATING-FROM-CLAUDE-AND-CHATGPT.md).

---

## The scenario

Maya is a freelance editor who uses a Custom GPT called **"Trip Sage"** to help
plan her travel. Trip Sage has:

- **Instructions** telling it how to behave.
- **Two uploaded knowledge files**: a packing checklist and a Tokyo 3-day
  itinerary draft.
- **Saved memory** with her durable preferences.
- **A chat export** where a useful lesson was decided.

All of that currently lives *inside ChatGPT*. Maya can open none of it in a text
editor, and if she ever tries Claude or a coding agent, none of it comes with
her.

## The migration in one table

| Inside Trip Sage | After (files Maya owns) |
|---|---|
| Custom GPT instructions (behaviour half) | [`after/AGENTS.md`](after/AGENTS.md) |
| Custom GPT instructions (identity half) + saved "I am…" facts | [`after/memory/core.md`](after/memory/core.md) — Purpose & context |
| Saved preferences ("window seats", "vegetarian", "refundable") | [`after/memory/core.md`](after/memory/core.md) — Key learnings & principles |
| The Tokyo trip as an active piece of work | [`after/memory/projects/tokyo-trip-2026.md`](after/memory/projects/tokyo-trip-2026.md) |
| Packing checklist (reference input) | [`after/materials/tokyo-trip-2026/01-inputs/packing-checklist.txt`](after/materials/tokyo-trip-2026/01-inputs/packing-checklist.txt) |
| Tokyo 3-day itinerary (working draft) | [`after/materials/tokyo-trip-2026/01-inputs/tokyo-3-day-itinerary.txt`](after/materials/tokyo-trip-2026/01-inputs/tokyo-3-day-itinerary.txt) |
| Chat export containing a decided lesson | [`after/materials/tokyo-trip-2026/01-inputs/conversation-2026-06-10.md`](after/materials/tokyo-trip-2026/01-inputs/conversation-2026-06-10.md) |
| Section schema (so tables self-generate) | [`after/memory/_sections.json`](after/memory/_sections.json) |

## How to use this

- **Browse [`before/`](before/)** to see the scattered, locked-in source.
- **Browse [`after/`](after/)** to see the same content as portable files.
- Compare any before file to its after destination in the table above.

The `after/` folder is a real, valid three-tier workspace. If you copied the
three scripts from [`../../scripts/`](../../scripts/) into `after/scripts/` and
ran `python3 scripts/memory_refresh.py`, the generated tables in
`memory/core.md` and `memory/projects/README.md` would regenerate identically.
