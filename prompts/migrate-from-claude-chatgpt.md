# Migration prompt — convert a Claude or ChatGPT setup into the three tiers

> Use this to turn a **Claude Project**, a **ChatGPT Custom GPT**, or a pile of
> **saved-memory** snippets into a portable, file-based three-tier memory system.
> Works with any coding agent **or** a web chat (ChatGPT, Claude, Gemini): the
> model writes the file contents and you save them into a folder.

See [`../MIGRATING-FROM-CLAUDE-AND-CHATGPT.md`](../MIGRATING-FROM-CLAUDE-AND-CHATGPT.md)
for the full conceptual map, and [`../worked-examples/chatgpt-to-3t/`](../worked-examples/chatgpt-to-3t/)
for a worked before/after.

---

## What to gather first

Collect, from your chat tool, into one place (a folder or pasted into the chat):

1. **Instructions** — the Custom GPT instructions, or Claude Project custom
   instructions. Copy the full text.
2. **Knowledge files** — list the files uploaded to the GPT/Project, and attach
   or paste their contents where you can. Note each file's role (reference,
   template, example output, etc.).
3. **Saved memory** — ask the tool "what do you remember about me?" and copy the
   full list. (ChatGPT: Settings → Personalization → Memory.)
4. **(Optional) one or two conversation exports** that contain decisions or
   lessons you want to keep.
5. **Your profile** — 3–5 lines on who you are, your role, and the kind of work.

You do not need all five. Even just (1) + (3) is enough to produce a useful
core memory.

---

## Copy-paste prompt

```text
Convert my existing chat-tool setup into a portable, file-based three-tier
memory system that I own and can use with any tool.

I will provide: my instructions, my knowledge files (names + roles, contents
where possible), my saved-memory snippets, and a short profile. Treat each as
source material; do not invent anything not present.

The target structure:
- AGENTS.md            — procedural memory: how any agent should behave here
- memory/core.md       — Tier 1: durable cross-project context, kept under 16 KB
- memory/projects/*.md — Tier 2: one canonical file per active project
- memory/_sections.json— the section schema (config-driven)
- materials/<project>/ — Tier 3: the knowledge files as evidence
  ├── 01-inputs/         (reference material, source documents)
  ├── 02-working/        (things I iterate on)
  └── 03-deliverables/   (finished outputs)

Work in this order:

Step 1 — Split my instructions into two parts
(a) Behaviour ("how to act") → AGENTS.md: role, tone, working rules, context
load order, maintenance commands. (b) Identity ("who I am / what I do") → the
Purpose & context section of memory/core.md. Do not duplicate the same line in
both places.

Step 2 — Sort my saved-memory snippets into three buckets
- Global, durable, about me → memory/core.md (Purpose & context, or Key
  learnings & principles).
- Tied to a specific project → that project's memory/projects/<slug>.md file.
- Transient / throwaway → flag for me to discard (do not store in memory).

Step 3 — File my knowledge files as evidence
For each knowledge file, decide its role and place it under
materials/<project>/01-inputs/ (reference/source) or 02-working/ (iterative) or
03-deliverables/ (finished). If files serve multiple projects, pick the primary
one and link from others. Give each project a memory/projects/<slug>.md file
with a Key documents section linking every filed document by repo-relative path.

Step 4 — Define the section schema
Write memory/_sections.json with at least one source:"projects" section and one
source:"watchlist" section, using columns appropriate to my work. Each project
file's frontmatter core_section must match a section id.

Step 5 — Write project files with full frontmatter
Each memory/projects/<slug>.md needs frontmatter (id, title, owner, status_date,
status_summary, stage, next_action, next_review_date, priority, sensitivity,
core_section, core_order, archive_status, canonical) and sections: profile,
scope, decision log, key documents, open items, risks/blockers, key insights.

Step 6 — Write memory/core.md
Include: title/owner/last updated, Purpose & context, Key collaborators, the
generated-block markers
<!-- memory-sections:start -->
<!-- memory-sections:end -->
exactly as written (a script fills between them), Key learnings & principles,
Approach & patterns, Tools & resources, Update rules. Keep it under 16 KB.

Step 7 — Report
List every file you created and where it maps from in my source material. Show
me the before→after mapping as a short table. Tell me which snippets you
recommended discarding and why. Give me the one command to regenerate the index:
`python3 scripts/memory_refresh.py`.

Rules:
- Files are the source of truth. Do not invent facts, names, dates, or numbers.
- Keep memory/core.md under 16 KB; push detail into project files.
- Project files are authoritative for project detail; do not duplicate in core.
- Use absolute YYYY-MM-DD dates only.
- If you are unsure which bucket something belongs in, ask me — do not guess.
- Do not delete my source material; the conversion is additive.

Here is my source material:

<INSTRUCTIONS>
…paste your Custom GPT / Claude Project instructions here…
</INSTRUCTIONS>

<PROFILE>
…3–5 lines on who you are and your work…
</PROFILE>

<SAVED_MEMORY>
…paste "what do you remember about me?" output, one item per line…
</SAVED_MEMORY>

<KNOWLEDGE_FILES>
- filename — role (reference / template / example output / working / deliverable)
  <paste contents if available>
…
</KNOWLEDGE_FILES>

<CONVERSATION_EXPORTS optional>
…paste any chat exports that contain decisions or lessons to keep…
</CONVERSATION_EXPORTS>

Start now with Step 1.
```

---

## After running it

- Save each produced file at the path the model states (respect the folder
  structure). Sync the folder via Git, Dropbox, iCloud, or Google Drive.
- If you have Python 3.9+, run `python3 scripts/memory_refresh.py` to generate
  the index tables and lint. Copy the three scripts from this repo's `scripts/`
  folder into your workspace if they are not already there.
- If you have no coding agent, you can keep maintaining the files by hand in any
  chat tool — just re-paste `memory/core.md` + the relevant project file at the
  start of each session instead of relying on the tool's internal memory.

The point of the migration is not to leave your chat tool. It is to stop being
the only place your context lives.
