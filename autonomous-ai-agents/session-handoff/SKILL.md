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

A third variant exists when the owner delegates thinking, not typing: mark it `EXECUTE, design-first` (see "Design-first handoffs" below).

## Where it lives
- Vault effort folder: `<Efforts folder>/HANDOFF <YYYY-MM-DD> <topic>.md`, with `handoff-assets/` beside it for images and files.
- Copy artifacts into `handoff-assets/`. Do not point at scratch (pruned after 24h) or at CDN URLs that may expire.
- Never write to TASKS.md or dashboard.html.

## Sections, in this order (write "none" where empty)
1. **Header.** Mode (EXECUTE, EXECUTE design-first, or REVIEW), date, sender model, intended receiver, goal in one sentence, deadline. In design-first, the header also states which instruction is current and which it supersedes.
2. **State at handoff.** What is done, with file paths. Nothing else.
3. **Decision log.** One row per decision: decision, options considered, why chosen, what would change it. Include rejected options and the reason they were rejected. The receiver does not reopen a rejected option without new evidence.
4. **Evidence ledger.** Every fact tagged one of:
   - VERIFIED: a tool output, file path, or URL with a date.
   - CLAIMED: stated by a person or a source, not checked.
   - JUDGMENT: the sender's view.
   A CLAIMED fact never reads as VERIFIED.
   Two tags are easy to blur. Confirming that a line exists in a file verifies the LINE, not the number typed into it: figures lifted from meeting notes, calls or someone's memory stay CLAIMED even after you grep them, and the ledger says what was checked (existence) and what was not (the figure against the live system). Only a pull from the system of record (CRM, ad platform, analytics) earns VERIFIED, and the row carries the source system, the period covered and the pull date.
5. **Artifacts.** Path, what it is, status (sketch, draft, final, staged, live).
6. **Open decisions.** Options, recommendation, and who decides. Every irreversible action (send, post, pay, publish, merge, delete) is listed here and is never done by the receiver.
7. **Not checked.** Known gaps, stated plainly.
8. **Acceptance criteria.** Testable. "Done" means these checks pass, not "looks right".
9. **Mode-specific block.**
   - EXECUTE: numbered steps with exact commands or paths, a verification command after each step, and a stop-and-report rule for anything off-plan.
   - REVIEW: check the sender's evidence first, then the decision log for consistency, then the artifacts. Output one verdict per artifact (accept, fix, redo) and a correction list with reasons. Name any item that needs the stronger model to re-run.

## Pasteable brief when the receiver is another harness

When Deep asks for a prompt he pastes into Claude Desktop or another agent product, rather than a file, the sections above still apply but the artifact is one fenced block in chat. Build it in this order:

1. **Receiver paragraph first**: who Deep is (city, time zone, roles), what the batch is for, one goal sentence. The receiver has no chat history and no Hermes context, so this paragraph and the paths below are its entire world.
2. **A HARD RULES block before any work item**: never send, post, merge, deploy, pay or delete (stage it and record where it is staged); no em dashes or en dashes; the protected vault files are named; never read secrets or `.env`; never invent a number (label it unverified and say what would verify it); no wikilink without reading the link policy first.
3. **Skill references by absolute path.** Another harness cannot resolve a Hermes skill name or call `skill_view`, so write each skill as its full `SKILL.md` path. Resolve every path yourself before handing the brief over, and state the pre-flight for Deep: if the product is sandboxed to one folder, those skill folders have to be allowed before the run starts.
4. **Work items in priority order**, each carrying: the context files to read first, the skill paths to load, numbered do-steps, the deliverable path, and an explicit do-not-touch boundary.
5. **Cap the review loop inside each item** (a round count, not "keep improving"). An uncapped improve loop spends the whole usage budget on item one and the rest of the batch never starts.
6. **Handoff step last**: the receiver writes into the vault effort folder, because its transcript never comes back to Hermes. Structure it as done (paths, verification output) / not done / DECISIONS FOR DEEP with A (recommended), B, C and a default, so the next session can card them. Keep its final chat reply short.

Pitfalls:
- A decision only Deep can make (a staged draft nobody sent, a parked card) goes at the top of YOUR reply to him, not inside the brief: the other harness cannot act on it either, and buried in the brief it never reaches his desk.
- Name the shared-repo hazard in the brief: other lanes edit the same repos, so the receiver works on its own branch in its own worktree (`shared-checkout-safety`), or it overwrites live work.
- A verification script the brief points at must run in the receiver's harness. One written against Hermes browser helpers (`js`, `cdp`, `goto_url`) is dead weight elsewhere: tell the receiver to port the method to a tool the repo already has, and name that tool.
- Before promising a cloud receiver, prove the code can reach it: repo visibility, whether a push triggers a build or deploy, and whether anything on the branch is barred from that repo by licence. When it cannot be pushed, write the brief for a local harness and say why.
- No brief implies deploy rights. A config or cost change gets a branch, a test or a dry run, and a note of what is left for Deep to approve.

## Design-first handoffs
When the owner says the next session should think part of it out, that part must not appear in the file as steps. Handing over a design problem as commands gets it executed literally and wastes the receiver's session.

- Put a gate before step 1: the receiver writes a design proposal covering the open part, then stops for the owner before any code.
- Convert the open part into four things: the problem in one paragraph, the constraints no option may break, a table of options where each row carries the first question that decides it, and the sources to research from. Give the option space, never the answer.
- Capability claims (what an API, provider or platform can read or do) come from primary documentation with a link and a retrieval date, not from memory. An unverified capability claim fails acceptance.
- Make acceptance test the proposal's honesty: it names its cost, its failure mode, its single point of failure and its fallback.
- When the brief changes mid-write, rewrite the file rather than layering the new plan on top. Put the current instruction and the superseded one in the header, and log the rejected version as a decision row with its reason so the receiver never rebuilds it.

## Rules
- Re-read a file before quoting it. Do not quote from memory.
- Before proposing work, inventory what already exists: grep TASKS.md, Kanban and related effort folders for each item in the plan. An open card or task for the same fix makes the plan a duplicate, so the handoff lists it as "already open" instead of inventing a second one, and the receiver's first step checks these anyway.
- A handoff the receiver will execute or design from goes in a frontmatter block the vault recognizes: `type: effort`, `status: active`, `company: "[[Client]]"`, `updated: YYYY-MM-DD`.
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
