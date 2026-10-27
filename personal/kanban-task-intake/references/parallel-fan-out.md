# Parallel fan-out: one request, N worker cards, one gated review

Use when a single ask splits into several same-shape build cards with no decision only
Deep can make. Steps in the order they run:

1. **Settle the contract once, in a spec file.** Write the shared rules (stack, taste
   floor, brand skills, data and privacy rules, share artifact, performance budget,
   hosting approval and its negatives, what "done means" looks like) into one read-only
   file on disk. Cards then carry only the per-item spec plus a pointer to it, and any
   later ruling is a patch to one file instead of N card comments.
2. **Create the work directories before the cards do.** A `workspace_kind=dir` card
   pointing at an empty path is the failure mode: the worker builds somewhere else and
   nothing fails loudly. `mkdir -p` plus `git init -b main` each path in one pass, and
   say in the brief that the directory already exists and is the only place to work.
3. **Build all bodies from one code template.** Loop over the per-item specs in
   `execute_code`, write each body to a scratch file, and drive the CLI per item. One
   template means the shared gates are identical across cards; hand-typing five bodies
   means the fifth one drifts.
4. **Create with idempotency keys.** `--idempotency-key <family>-<slug>` makes a re-run
   return the existing card instead of duplicating the fan-out, which matters because
   fan-out is the kind of step that gets repeated after an interruption.
5. **Gate the review card with `parents` on every build card.** It sits in `todo` and
   promotes itself the moment the last build lands, so nothing waits on a human to start
   the check. Its brief says to re-run each build's proof itself: worker completions are
   self-reports.
6. **Record in TASKS.md in the same pass.** One fenced block with every card id, in the
   `## Active` section, above the running commentary blocks. The card is the surface;
   the row is the record.
7. **Read the state back before reporting.** `hermes kanban show <id> --json` per card,
   printing `id status assignee`. A create call returning JSON proves the row was
   written, not that the dispatcher picked it up.

Pitfalls:
- **Distribute shared context by absolute path, not by pasting it N times.** Pasted
  context drifts the moment you fix one card; a path plus "this file is the spec and it
  wins on conflict" keeps one source of truth.
- **Isolate the cards.** Parallel cards sharing a checkout or branch trample each other.
  One directory or worktree per card, no shared working state.
- **Deployment scope goes in the brief as explicit negatives.** Name the exact host and
  the resource name pattern, then one line for each thing still needing Deep (custom
  domains, DNS, spend). A lane that inferred permission makes a change nobody approved.
- **Confirm the batch started, do not trust the create output.** Creates succeed while
  the dispatcher still has to pick each card up; a status read-back is the only proof
  it is running, and a card that never dispatches is invisible otherwise.

Follow-ups a fan-out usually needs: a `needs_input` card for the approvals held back
(domain, DNS, spend) in the decision-card shape, raised from the gated review card
rather than in chat, plus a pointer from the spec file back to the card ids.
