# Pending user decision — screenshot-pricing.png

**Received:** YYYY-MM-DD
**Source:** forwarded email (see `inbox/intake-note-example.md`)

## What I need from the operator

This is the human-decision placeholder for the screenshot in `inbox/`.
The agent wrote an intake note against it but cannot tell whether the
screenshot is `acme-launch` evidence or evidence for a new
`vendor-pricing-watch` project.

Action: open `inbox/intake-note-example.md`, pick option A, B, or C,
then ask the agent to route the file.

---

> **Why this file is here.** This file intentionally sits in
> `inbox/pending-user/` past the 14-day staleness threshold so that a
> fresh checkout demonstrates the workspace check's WARN behaviour. The
> `scripts/workspace_check.py` run is load-bearing: the WARN on this
> file proves the staleness check works. Do not route this file until
> the operator has decided on the routing question.
