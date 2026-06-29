# A generic, file-based memory system for AI agents

[![lint](https://github.com/kelvinq/3t-memory/actions/workflows/lint.yml/badge.svg)](https://github.com/kelvinq/3t-memory/actions/workflows/lint.yml)
![license](https://img.shields.io/badge/license-MIT-blue)
![python](https://img.shields.io/badge/python-3.9%2B-blue)

A self-contained, domain-neutral memory system you can drop into any folder and
run. It keeps durable context in plain files, treats each project file as the
source of truth, and regenerates a small core index from structured project
metadata. **No database, no platform, no vendor lock-in — just files, templates,
and three Python scripts.**

It works for **any** knowledge-work domain (sales, research, engineering,
consulting, support, personal projects) and with **any** agent: a coding agent
that can read and write files (Pi, Claude Code, Cursor, Cline, Aider, OpenCode…)
**or** a web interface (ChatGPT, Claude, Gemini) used as a writing surface.

> If you fork or re-publish this, replace `kelvinq/3t-memory` in the badge URLs
> and issue templates with your own GitHub path.

---

## Start here

Two paths in, depending on where you are coming from.

### A. Fresh start — I want to install this from scratch

Read **[QUICKSTART.md](QUICKSTART.md)** (zero to a working, lint-clean system in
~10 minutes), or paste **[prompts/install.md](prompts/install.md)** into your
agent and let it build the structure with you.

### B. I already use ChatGPT or Claude

Read **[MIGRATING-FROM-CLAUDE-AND-CHATGPT.md](MIGRATING-FROM-CLAUDE-AND-CHATGPT.md)**.
It maps your Custom GPT / Claude Project / saved memory onto the three tiers,
with worked examples. Then use
**[prompts/migrate-from-claude-chatgpt.md](prompts/migrate-from-claude-chatgpt.md)**
to do the conversion in one paste. See a full before/after in
**[worked-examples/chatgpt-to-3t/](worked-examples/chatgpt-to-3t/)**.

### C. I have a pile of scattered notes, not a chat tool

Use **[prompts/migrate.md](prompts/migrate.md)** to sort existing files into the
three tiers.

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

**Hand-maintained**
- `AGENTS.md`, `OPERATOR.md`
- `memory/core.md` narrative sections (everything outside the markers)
- `memory/_sections.json`, `memory/watchlist.json`
- `memory/projects/*.md`
- everything under `materials/`

**Generated (never hand-edit)**
- the block between `<!-- memory-sections:start -->` and
  `<!-- memory-sections:end -->` in `memory/core.md`
- `memory/projects/README.md`

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

---

## License

MIT — see [LICENSE](LICENSE). Use it freely; adapt it to your workflow.
