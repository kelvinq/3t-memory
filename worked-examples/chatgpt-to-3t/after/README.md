# After — Trip Sage, as a portable three-tier workspace

This is the same content as [`../before/`](../before/), restructured into files
Maya owns. She can open every one of these in a text editor, sync them to any
device, and use them with ChatGPT, Claude, or any coding agent.

```text
after/
├── AGENTS.md                                 # behaviour half of the GPT instructions
├── memory/
│   ├── core.md                               # identity + global preferences (Tier 1)
│   ├── _sections.json                        # section schema (config-driven)
│   ├── watchlist.json                        # dormant items
│   └── projects/
│       ├── README.md                         # generated index
│       └── tokyo-trip-2026.md                # the active trip (Tier 2)
└── materials/
    └── tokyo-trip-2026/
        └── 01-inputs/
            ├── packing-checklist.txt          # knowledge file -> evidence
            ├── tokyo-3-day-itinerary.txt      # knowledge file -> evidence
            └── conversation-2026-06-10.md      # chat export -> evidence
```

## What changed, beyond the layout

- The **behaviour** instructions and the **identity** facts are no longer fused
  in one instructions box; they are split into `AGENTS.md` and `memory/core.md`
  where they belong.
- The **saved-memory** snippets are sorted: global ones live in core, the one
  project-specific one (the Tokyo trip) lives in its project file.
- The two **knowledge files** are no longer opaque uploads; they are real files
  the project file links to by path.
- The **decided lesson** from the chat export was promoted to core's *Key
  learnings & principles* ("refundable-only is a hard rule"), while the raw chat
  itself was demoted to evidence.

## Verifying it

`after/` is a valid workspace. To make it self-regenerating, copy the three
scripts from [`../../../scripts/`](../../../scripts/) into `after/scripts/`, then:

```bash
cd after
python3 scripts/memory_refresh.py     # regenerates core tables + project index, then lints
```

The generated tables between the markers in `memory/core.md` and the whole of
`memory/projects/README.md` will be rebuilt from the project frontmatter and the
section schema. They are shown here already rendered for readability.
