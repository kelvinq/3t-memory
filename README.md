# A portable memory for your AI tools — in plain files you own

[![lint](https://github.com/kelvinq/3t-memory/actions/workflows/lint.yml/badge.svg)](https://github.com/kelvinq/3t-memory/actions/workflows/lint.yml)
![license](https://img.shields.io/badge/license-MIT-blue)
![python](https://img.shields.io/badge/python-3.9%2B-blue)

A self-contained memory system that lives in a normal folder of Markdown files.
No database, no account, no platform to subscribe to. Any AI agent — a coding
assistant like Claude Code or Cursor, or a chat like ChatGPT, Claude, or Gemini
— can read it and keep it up to date. Your memory travels with you, never
forgets between sessions, and isn't trapped inside one product.

---

## What can you do with it?

Six things people use this for today. None of them require any technical
background.

- **Run a long freelance or client practice without losing the thread.** Every
  client, decision, and follow-up you've had for the last six months is there,
  in the next chat. No re-explaining who Sarah is, or where the Acme brief
  landed.
- **Write a thesis, a book, or any long project across many months.** Pick up
  exactly where you left off, in any tool, any session. Your outline, sources,
  and notes all carry over — you stop re-introducing your own work.
- **Plan a big trip without losing the receipts.** Every booking, decision,
  reservation, and "I should remember this" lives in one place you can reopen
  the day you fly.
- **Manage a job search like a pipeline, not a spreadsheet.** Track every
  application, interview prep doc, and follow-up. Then ask your assistant
  "what's next?" whenever you sit down and get a real answer.
- **Keep a running history of a home renovation, a pet's care, or a family
  member's health.** Years of vet visits, contractor quotes, or doctor's notes
  stay organised and findable — not buried in email.
- **Move between AI tools without starting over.** The best assistant today is
  not the one you'll use in two years. Your memory travels with you, in plain
  files, ready for whatever comes next.

---

## Why plain files?

Because memory should belong to you, not to a product.

- **You own the files.** They're plain Markdown on your disk. Open them in any
  text editor. Version them with git. Back them up like anything else.
- **Every tool can read them.** Claude Code, ChatGPT, Cursor, Gemini, a future
  tool you haven't heard of yet — they all see the same context.
- **You never re-explain yourself.** The agent reads your context at the start
  of every session, not just the one it was born in.
- **Nothing silently decays.** A single test command catches broken links and
  missing pieces before you notice.

---

## Start here

Setup takes about ten minutes, and the agent does the heavy lifting. You paste
a single setup or migration prompt, answer a few questions, and the agent
builds the folder, fills the templates, runs the lint check, and reports when
everything is clean. Even the system instructions file (`AGENTS.md`) is filled
in for you — typically copied from your existing Claude Project or Custom GPT
instructions.

Three paths in, depending on where you're coming from.

### A. Fresh start — I want to install this from scratch

Read **[QUICKSTART.md](QUICKSTART.md)** (zero to a working, lint-clean system
in ~10 minutes), or paste **[prompts/install.md](prompts/install.md)** into
your agent and let it build the structure with you.

### B. I already use ChatGPT or Claude

Read **[MIGRATING-FROM-CLAUDE-AND-CHATGPT.md](MIGRATING-FROM-CLAUDE-AND-CHATGPT.md)**.
It maps your Custom GPT / Claude Project / saved memory onto the system, with
worked examples. Then use
**[prompts/migrate-from-claude-chatgpt.md](prompts/migrate-from-claude-chatgpt.md)**
to do the conversion in one paste. See a full before/after in
**[worked-examples/chatgpt-to-3t/](worked-examples/chatgpt-to-3t/)**.

### C. I have a pile of scattered notes, not a chat tool

Use **[prompts/migrate.md](prompts/migrate.md)** to sort existing files into
the tiers.

---

## What it's like day-to-day

Here is a realistic day. **The agent does the heavy lifting; you stay in plain
language.**

**Morning.** You sit down and open your agent in the folder. You ask, in your
own words: *"What am I waiting on today?"* The agent reads `memory/core.md` and
your project files and answers in a sentence — *"Acme contract — they're
sending redlines by EOD. Vet follow-up for Bella on Thursday. Trip insurance
claim still pending."*

**During the day.** Things happen. A client emails. A meeting ends. You make a
decision. You tell the agent in one sentence and drop the email or transcript
into the project's folder, or paste it into chat. Something like:

> "Had the kickoff with Acme. They want the launch in Q3, budget is tight,
> Sarah is the new decision maker. Transcript attached."

The agent reads the transcript, updates `memory/projects/acme.md`, files the
evidence under `materials/acme/01-inputs/`, and adds the decision to the
decision log. **You didn't open a single file by hand.**

**End of day.** You ask: *"Refresh the index and lint."* The agent runs
`python3 scripts/memory_refresh.py`, regenerates the core tables, and reports
the result. You almost never hand-edit a file.

---

## How much work is this for you, really?

Almost none. Here is the honest split.

**What you do**
- Point your agent at the folder (once).
- Talk to it in plain words: *"I had a call with Acme, here's the transcript."*
- Occasionally paste or attach a file (an email, a transcript, a brief).
- Run the refresh command when you want, or ask the agent to.

**What your agent does**
- Reads the right project file at the start of every session.
- Updates the right file when you tell it what changed.
- Files evidence into the right `materials/` subfolder.
- Rebuilds the index tables in `memory/core.md`.
- Runs the lint check and reports broken links.

The "human-maintained" parts — `memory/core.md`, your project files, your
evidence files — are kept accurate by your agent on your behalf, not by you
hand-editing. The generated parts (the index tables between the markers in
`memory/core.md`) are rebuilt automatically by the script and **must not be
hand-edited**.

In other words: **the files are the storage, but the agent is the keeper.**
You stay in chat. The files stay correct.

---

# Reference — How it works under the hood

The technical reference. If you only came for the non-technical intro above,
you can stop reading here.

## What this is, in one paragraph

A self-contained, domain-neutral memory system you can drop into any folder
and run. It keeps durable context in plain files, treats each project file as
the source of truth, and regenerates a small core index from structured
project metadata. **No database, no platform, no vendor lock-in — just files,
templates, and three Python scripts.**

It works for **any** knowledge-work domain (sales, research, engineering,
consulting, support, personal projects) and with **any** agent: a coding agent
that can read and write files (Pi, Claude Code, Cursor, Cline, Aider,
OpenCode…) **or** a web interface (ChatGPT, Claude, Gemini) used as a writing
surface.

---

## The three tiers

| Tier | What it is | Where it lives | What goes in it |
|---|---|---|---|
| **Core (T1)** | Semantic memory — an index | `memory/core.md` | Role/context, key collaborators, **generated** section tables, reusable learnings, durable patterns, tools |
| **Project (T2)** | Per-project semantic memory | `memory/projects/<slug>.md` | One canonical file per active project: status, scope, decisions, key documents, open items, insights |
| **Archive (T3)** | Episodic memory — evidence | `materials/<project>/` | Transcripts, briefs, decks, spreadsheets, drafts, final deliverables |

A working-memory tier (`sessions/`, `materials/<project>/02-working/`) holds
transient scratch notes that should never leak into durable memory.

### How they relate

- The **core** file stays small. It is an *index*, not a dump.
- Each **project** file owns its own detail and links out to its **archive**.
- The core's section tables are **generated** from project frontmatter and the
  watchlist, so they never drift from the source files.

---

## Core design principles

1. **Files are the source of truth.** Human-readable files beat opaque chat
   memory for auditable, hand-off-able work.
2. **Core memory stays small.** It is an index, not a dump.
3. **Project memory is canonical.** Project detail belongs in project files.
4. **Archive is separate from memory.** Evidence lives in `materials/`, not core.
5. **Generated views reduce drift.** The core index is rebuilt from structured
   metadata wherever possible.
6. **Config-driven, not hardcoded.** Your sections and their columns are defined
   in `memory/_sections.json`, so the system works for any domain without
   editing Python.

---

## Recommended structure

```text
.
├── AGENTS.md                     # procedural memory (workflow rules)
├── OPERATOR.md                   # human operator guide
├── memory/
│   ├── core.md                   # core index (hand + generated parts)
│   ├── _sections.json            # section schema (config-driven)
│   ├── watchlist.json            # structured dormant items
│   └── projects/
│       ├── README.md             # generated index — do not hand-edit
│       ├── archive/
│       └── <project>.md          # one canonical file per project
├── materials/
│   └── <project>/
│       ├── 01-inputs/
│       ├── 02-working/
│       └── 03-deliverables/
├── templates/
│   ├── memory-core.md
│   └── memory-project.md
└── scripts/
    ├── memory_refresh.py         # rebuild + lint
    ├── rebuild-memory-core.py    # regenerate core section tables + project index
    └── lint-memory.py            # canonical-file / size / frontmatter / link checks
```

---

## What is hand-maintained vs generated

*(Technical restatement of "How much work is this for you, really?", above.)*

**Hand-maintained** (by you, or — usually — by your agent on your behalf)
- `AGENTS.md`, `OPERATOR.md`
- `memory/core.md` narrative sections (everything outside the markers)
- `memory/_sections.json`, `memory/watchlist.json`
- `memory/projects/*.md`
- everything under `materials/`

**Generated (never hand-edit)**
- the block between `<!-- memory-sections:start -->` and
  `<!-- memory-sections:end -->` in `memory/core.md`
- `memory/projects/README.md`

In practice, the agent maintains the "hand-maintained" files for you. Only
the generated blocks must not be touched by hand.

---

## Maintenance commands

```bash
python3 scripts/memory_refresh.py        # rebuild generated views, then lint
python3 scripts/rebuild-memory-core.py   # rebuild only
python3 scripts/lint-memory.py           # lint only
```

Requirements: Python 3.9+ and nothing else.

---

## What's in this repo

| Path | Purpose |
|---|---|
| `README.md` | This file. |
| `QUICKSTART.md` | Zero-to-working walkthrough, including importing your own documents. |
| `MIGRATING-FROM-CLAUDE-AND-CHATGPT.md` | Move from a Custom GPT / Claude Project / saved memory into the three tiers. |
| `prompts/install.md` | Copy-paste installer prompt (any coding agent or web interface). |
| `prompts/migrate.md` | Copy-paste prompt to sort a pile of scattered files into the tiers. |
| `prompts/migrate-from-claude-chatgpt.md` | Copy-paste prompt to convert a chat-tool setup into the three tiers. |
| `AGENTS.md` | Generic procedural-memory template. |
| `OPERATOR.md` | Generic operator guide template. |
| `templates/memory-core.md` | Core memory template (neutral placeholders). |
| `templates/memory-project.md` | Project memory template (neutral placeholders). |
| `scripts/memory_refresh.py` | rebuild + lint wrapper. |
| `scripts/rebuild-memory-core.py` | config-driven section renderer + project index. |
| `scripts/lint-memory.py` | domain-neutral lint. |
| `memory/watchlist.json` | example watchlist (edit / empty it). |
| `example/` | a populated, self-regenerating, lint-clean tiny workspace. |
| `worked-examples/chatgpt-to-3t/` | a real-ish Custom GPT, shown before and after migration. |

> Forking or re-publishing? Replace `kelvinq/3t-memory` in the badge URLs and
> issue templates with your own GitHub path.

---

## License

MIT — see [LICENSE](LICENSE). Use it freely; adapt it to your workflow.
