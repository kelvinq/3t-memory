# Migrating from Claude or ChatGPT into the three-tier memory system

This guide is for people whose "memory" currently lives inside a chat product —
a **ChatGPT Custom GPT**, a **Claude Project**, or the **saved-memory** snippets
those tools keep — and who want to move it into a portable, file-based system
they fully own.

You do **not** need to stop using ChatGPT or Claude. You are moving *where the
durable context lives* — out of a product-locked store and into files you can
open, edit, version, share, and use with any tool, today and in five years.

> For a full before/after, see
> [`worked-examples/chatgpt-to-3t/`](worked-examples/chatgpt-to-3t/).
> To do the conversion in one paste, use
> [`prompts/migrate-from-claude-chatgpt.md`](prompts/migrate-from-claude-chatgpt.md).

---

## 1. The mental shift in one paragraph

In ChatGPT or Claude, your "memory" is scattered across four separate places and
none of them is something you can open in a text editor: the **system
instructions**, the **uploaded knowledge files**, the **saved-memory snippets**,
and the **conversation history** itself. The three-tier system collapses those
four scattered stores into one normal folder you control. Each of the four maps
to a specific home.

## 2. The map

| What you have in the chat tool | Where it goes | Why |
|---|---|---|
| **System instructions** / Custom GPT instructions / Claude Project custom instructions | `AGENTS.md` (behaviour) + the **Purpose & context** section of `memory/core.md` | Instructions are half "how to act" (procedural → `AGENTS.md`) and half "who I am and what I do" (semantic → core memory). |
| **Uploaded knowledge files** (PDFs, docs, spreadsheets in the GPT/Project) | `materials/<project>/01-inputs/` (and `02-working/` for things you iterate on) | These are *evidence*, not memory. The tier-3 archive holds them and the project file links to them. |
| The **persona / role** the GPT plays for you | The **Purpose & context** section of `memory/core.md` + the **Role** in `AGENTS.md` | This is durable semantic context. |
| **Saved-memory** snippets ("User prefers…", "Always…") | Distilled into `memory/core.md` learnings **or** a project file, depending on scope | Global preferences → core. Project-specific ones → that project's file. |
| **Conversation exports** | Skim for durable lessons → core/project; the rest → `materials/<project>/` | Chat is working memory, not a source of truth. Keep only what is durable. |
| **Several Custom GPTs / Claude Projects** | One **project file** each (or consolidated into sections) | Each project gets its own canonical file. Common behaviour across all of them stays in `AGENTS.md`. |

The rule of thumb: **if a human could not open it in a text editor, it does not
belong in memory.** That is what makes the result portable.

## 3. Which tool do you need?

The system is just files plus three Python scripts. You can run it two ways.

### With a coding agent (recommended — the system becomes self-maintaining)

Any agent that can read and write files will do: Pi, Claude Code, Cursor, Cline,
Aider, OpenCode, and others. Point it at the folder; it reads `AGENTS.md` and
`memory/core.md` at the start of each session, edits the right files, and runs
`python3 scripts/memory_refresh.py` to rebuild the index and lint. You stop
hand-maintaining anything that can be generated.

### With a web interface only (ChatGPT, Claude, Gemini)

You can still use this system with no coding agent at all:

1. Paste [`prompts/install.md`](prompts/install.md) or
   [`prompts/migrate-from-claude-chatgpt.md`](prompts/migrate-from-claude-chatgpt.md)
   into a chat.
2. The model produces the file contents (core, project files, `AGENTS.md`).
3. Save each into a normal folder, ideally synced via Dropbox, iCloud, Google
   Drive, or a private Git repo so it follows you across machines.
4. Run `python3 scripts/memory_refresh.py` occasionally (Python 3.9+ only) to
   regenerate the index. Skip it if you have no Python — the files are still
   valid and useful, you just hand-edit the generated tables.

The web-only path is more manual, but it is exactly how you stop being locked to
one product: your context lives in files, not in a vendor's feature.

## 4. What you gain by moving

- **Portability.** The same files work in ChatGPT, Claude, Gemini, and every
  coding agent. Switch tools without re-explaining yourself.
- **Auditability.** Every claim ties to a file you can open. No hidden
  "remembered" facts you cannot inspect or correct.
- **Size discipline.** Core memory is kept small and cheap to load. Chat tools
  have no such limit, which is how memory quietly becomes a 200 KB wall of text.
- **No silent drift.** Generated index tables are rebuilt from project metadata,
  so the summary can never disagree with the detail.
- **Survival.** A vendor can deprecate a feature, change a model, or change
  pricing. Your files are yours.

---

## 5. Worked example A — Claude Project → three tiers

Imagine a Claude Project called *"Grant writing"* with custom instructions, three
uploaded PDFs (last year's funded proposal, the funder's guidelines, a budget
template), and a few saved facts.

**Before (locked inside the Project):**
- Custom instructions: "You are my grant-writing assistant. Mirror the funder's
  tone. Always cite the guideline section. Never invent budget numbers."
- Knowledge: `2025-funded-proposal.pdf`, `funder-guidelines.pdf`, `budget-template.xlsx`
- Saved memory: "My org is a 501(c)(3) in environmental education." / "Deadlines are Q1 and Q3."

**After (files you own):**

```text
my-workspace/
├── AGENTS.md                          # <- the behaviour half of the instructions
├── memory/
│   ├── core.md                        # Purpose: "grant writer for an environmental 501(c)(3)"
│   └── projects/
│       └── spring-2026-grant.md       # <- the current proposal as a project
└── materials/
    └── spring-2026-grant/
        ├── 01-inputs/
        │   ├── funder-guidelines.pdf
        │   └── 2025-funded-proposal.pdf
        └── 02-working/
            └── budget-template.xlsx
```

- The **behaviour** instructions ("mirror the funder's tone, cite the guideline
  section, never invent numbers") move to `AGENTS.md`.
- The **identity** fact ("environmental 501(c)(3)") moves to `memory/core.md`
  Purpose & context.
- The **deadline cadence** (Q1/Q3) becomes a line in core's learnings or a
  watchlist item.
- The three PDFs become tier-3 evidence, linked from the project's
  **Key documents**.
- The project file `spring-2026-grant.md` holds status, scope, decision log, and
  open items — the thing the chat tool had no clean place for.

## 6. Worked example B — ChatGPT Custom GPT → three tiers

A Custom GPT called *"Trip Sage"* has instructions, two uploaded reference files
(a packing checklist, a city itinerary), and saved memory ("prefers window
seats", "partner is vegetarian", "mid-tier budget", "always refundable").

This exact case is walked through end-to-end, with the real before files and the
real after workspace, in
[`worked-examples/chatgpt-to-3t/`](worked-examples/chatgpt-to-3t/). In short:

- Instructions → `AGENTS.md` (how Trip Sage should behave) + `memory/core.md`
  (the traveller's profile).
- "Prefers window seats / vegetarian / mid-tier / refundable" → core **Key
  learnings & principles** (global preferences) or the active trip's project
  file if trip-specific.
- Packing checklist + itinerary → `materials/<trip>/01-inputs/`, linked from the
  trip's project file.

## 7. Worked example C — ChatGPT saved-memory → three tiers

The smallest move, and often the first one people try. Open your ChatGPT
**Settings → Personalization → Memory** (or ask "what do you remember about
me?") and you will get a list of one-line facts.

Sort them into three buckets:

| Bucket | Example | Destination |
|---|---|---|
| **Global / about you** | "I am left-handed", "I work in euros", "Tone: concise, British English" | `memory/core.md` — Purpose & context, or Key learnings |
| **A specific project** | "The Acme deck is due 2026-07-10" | `memory/projects/acme-deck.md` — Status / Open items |
| **Transient / throwaway** | "Remind me to call Sam tomorrow" | Delete, or a `sessions/` note — never durable memory |

The discipline here is the whole point of the system: most "saved memory" is
either global-and-durable (→ core) or project-and-durable (→ project file).
Almost nothing belongs in an undifferentiated global list forever.

---

## 8. Do it now

1. Read [`QUICKSTART.md`](QUICKSTART.md) to install the empty system, **or**
2. Paste [`prompts/migrate-from-claude-chatgpt.md`](prompts/migrate-from-claude-chatgpt.md)
   into your agent/chat with your exports attached, and let it produce the files.

Then run `python3 scripts/memory_refresh.py` and you have a portable memory you
own, seeded from the chat tool you are leaving behind.
