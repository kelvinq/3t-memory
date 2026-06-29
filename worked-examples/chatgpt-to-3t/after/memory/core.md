---
file_role: core-memory
version: 2
owner: "Maya Okafor"
last_updated: "2026-06-28"
status_model: date-prefixed-status-lines
canonical: true
---

# Memory — Maya Okafor (travel planning)

**Last updated:** 2026-06-28  
**Historical archive root:** `materials/`

---

## Purpose & context

Maya is a freelance editor based in London who uses AI to help plan personal
travel — usually 3–10 day trips at a mid-tier budget. This workspace replaces a
ChatGPT Custom GPT ("Trip Sage") with a portable file-based memory she owns and
can use with any tool.

## Key collaborators

- Maya's partner — vegetarian; travels with Maya on most trips.

<!-- memory-sections:start -->
## Active trips

| Trip | Stage | Status | Detail |
|---|---|---|---|
| Tokyo autumn 2026 | active | 2026-06-28 — Drafting 3-day itinerary; flights and hotel not yet booked. | [`link`](projects/tokyo-trip-2026.md) |

## Watchlist

| Item | Status |
|---|---|
| Next trip after Tokyo | 2026-06-20 — No destination chosen yet. |
<!-- memory-sections:end -->

## Key learnings & principles

1. **Refundable fares and stays only — even at a premium.** Decided 2026-06-10
   after two past losses to non-refundable bookings when plans shifted. This is a
   hard rule, not a default.
2. **Window seats on long-haul flights.**
3. **Default to vegetarian-friendly options** when food is involved (partner).
4. **Max 3 stops per day** in itineraries unless Maya asks for more.
5. **Never invent prices, hours, or transit times** — say "please verify" and
   cite the source file.

## Approach & patterns

- Propose refundable first, then compare.
- Keep itineraries as drafts until flights and stays are locked.
- File every reference (checklists, draft itineraries, chat exports) under
  `materials/<trip>/` and link it from the trip's project file.

## Tools & resources

- Maintenance: `python3 scripts/memory_refresh.py`
- Section schema: `memory/_sections.json`

## Update rules

- Keep this file under 16 KB.
- Global preferences live here; trip-specific detail lives in the trip's project
  file.
- Run `memory_refresh.py` after editing project frontmatter.

## See also

- Workspace entry: [AGENTS.md](../AGENTS.md)
- Project index: [memory/projects/README.md](projects/README.md)
