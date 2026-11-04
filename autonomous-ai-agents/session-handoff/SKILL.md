---
name: session-handoff
description: Use when handing work to another model. Writes handoff.
version: 1.0.0
author: Deep (Champions Group)
license: internal
---

# Session handoff

## When to Use

Use when a session's work must pass to another model. The receiver knows nothing of this chat, so the handoff file is its whole context.

Two modes. Pick one and state it in the header.
- EXECUTE: a stronger model planned the work, a cheaper model runs it.
- REVIEW: a cheaper model produced the work, a stronger model checks it and improves it.

## Where it lives
- Vault effort folder: `<Efforts folder>/HANDOFF <YYYY-MM-DD> <topic>.md`, with `handoff-assets/` beside it for images and files.
- Copy artifacts into `handoff-assets/`. Do not point at scratch (pruned after 24h) or at CDN URLs that may expire.
- Never write to TASKS.md or dashboard.html.

## Sections, in this order (write "none" where empty)
1. **Header.** Mode (EXECUTE or REVIEW), date, sender model, intended receiver, goal in one sentence, deadline.
2. **State at handoff.** What is done, with file paths. Nothing else.
3. **Decision log.** One row per decision: decision, options considered, why chosen, what would change it. Include rejected options and the reason they were rejected. The receiver does not reopen a rejected option without new evidence.
4. **Evidence ledger.** Every fact tagged one of:
   - VERIFIED: a tool output, file path, or URL with a date.
   - CLAIMED: stated by a person or a source, not checked.
   - JUDGMENT: the sender's view.
   A CLAIMED fact never reads as VERIFIED.
5. **Artifacts.** Path, what it is, status (sketch, draft, final, staged, live).
6. **Open decisions.** Options, recommendation, and who decides. Every irreversible action (send, post, pay, publish, merge, delete) is listed here and is never done by the receiver.
7. **Not checked.** Known gaps, stated plainly.
8. **Acceptance criteria.** Testable. "Done" means these checks pass, not "looks right".
9. **Mode-specific block.**
   - EXECUTE: numbered steps with exact commands or paths, a verification command after each step, and a stop-and-report rule for anything off-plan.
   - REVIEW: check the sender's evidence first, then the decision log for consistency, then the artifacts. Output one verdict per artifact (accept, fix, redo) and a correction list with reasons. Name any item that needs the stronger model to re-run.

## Rules
- Re-read a file before quoting it. Do not quote from memory.
- Quote numbers with source and date. Prices, discounts and spend are questions for the owner, not numbers.
- No secrets. Never copy keys, tokens or credential contents into the handoff.
- No em dashes or en dashes in any deliverable for Deep. Use periods, commas, colons.
- Staged is not sent. A draft is not done. Name the exact place a draft is staged.
- Image-model and vision-model text reads are not proof. Say so, and proof text at full size.
- Point to files instead of pasting them. Keep the handoff readable in one pass.

## Pitfalls
- Context compaction drops detail. Write decisions into the file as they are made, not at the end.
- A sender's summary of a search is not the search. Save the key source lines with their URLs.
- Two files can disagree. List both paths in the handoff and say which one is current.
- Names and spellings drift between sources. Flag any name that appears in more than one spelling.
