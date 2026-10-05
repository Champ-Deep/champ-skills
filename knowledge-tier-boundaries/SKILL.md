---
name: knowledge-tier-boundaries
description: "Use when deciding what may sync between vault and BearDrive."
---

# Knowledge tier boundaries

Deep runs four stores that all look like "my knowledge base" and have genuinely
different visibility. Requests to "sync them", "back them up", or "make the team
bot read all of it" land on a boundary that was already decided. Read the
decision before building the sync.

| Store | Visibility | Holds |
|---|---|---|
| Celsus vault (`/Users/deep/Celsus`) | Deep only | Everything, client-named, no de-identification |
| `champ-knowledge` (BearDrive) | Whole org, forever | T0 de-identified patterns only |
| `champ-drives` (BearDrive) | Whole org, forever | Commercial per-brand drives |
| Champ Workspace | Authenticated, per route, audit-logged | Client-named records, decisions, live work |

## The two tests, applied before anything lands in a BearDrive repo

1. **Walkout test.** If a rep resigned tomorrow and took the file, could they
   use it to contact, price against, or poach an account? If yes, it does not
   belong.
2. **Crossover test.** Could a SPAN rep identify a Lake B2B client from it, or
   the reverse? If yes, generalise further or keep it out.

The usual failure is not a name left in. It is a *combination*: industry plus
headcount plus region plus quarter plus deal size identifies a client to anyone
in the room. Generalise at least two.

## The hard part: BearDrive has one visibility class

There is exactly one tier on that hub, so T0, T1 and T2 collapse into each other
and only T3 is enforced, by never being synced. The API-level reasons are in
`references/beardrive-platform.md`. In short: access is org-scoped, there is no
per-project membership and no second org, and a member can widen their own sync
scope client-side.

**Therefore: never sync client-named records, decision history, or live bot
transcripts into a BearDrive repo.** They go in Champ Workspace, which
authenticates per route, logs every decision, and shares by rendering read-only
rather than copying.

## What already syncs, do not rebuild it

`champ-workspace` already derives into BearDrive and both outputs are
build-owned. Edit the source, never the output:

- Vault `Atlas/Products` -> `champ-knowledge/products/` via
  `champ-workspace/scripts/celsus_build.py`
- Workspace audit spine, privacy-lensed -> `champ-knowledge/process/` via
  `scripts/process-graph.sh`

A hand-edited derived file is preserved but parked: the build stops updating it
and lists it in the commercial drive's `TRIAGE.md` until reverted.

## The safe generalisation out of client work

Per-client preferences and drafts are T2, but the *trade-off* behind them is
often T0 by construction. A design rule like "three body sections beat six, and
what it costs you is the explainer" is client-blind and belongs in
`champ-knowledge/patterns/`. The named example does not. Extract the rule, drop
the client, and flag it for a human rather than auto-publishing.

## Pitfalls

- Do not treat "sync the knowledge bases" as one request. Ask which direction
  and which tier, because the answer differs per store and a wrong guess moves
  client data to everyone.
- Do not trust a folder name for its visibility class. `champ-knowledge` holds
  `products/`, which is exempt from de-identification because those are our own
  products; the exemption is per-record and does not extend to the folder.
- Do not edit a build-owned directory. `products/`, `process/` and the generated
  `README.md` are regenerated.
- Do not create a new top-level directory in a BearDrive repo to solve a filing
  problem. Use `docs/`, and say in the file why it does not fit.
- Do not read a WIP backup snapshot's commit as current. Both BearDrive repos
  sat on automated backup commits with uncommitted files; run `git log` and
  `git status` before quoting either as the source of truth.
- Do not sync because a tool offers it. Read the tier decision first; the
  platform's capability is not the constraint, the org-wide visibility is.
