---
name: settlement-pack
description: "Use when Deep asks to move scattered open threads forward."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [celsus, kanban, decisions, ideation]
    related_skills: [kanban-task-intake, decision-grill, celsus-day-planning]
---

## When to Use

- Deep says some variant of "move X forward", "make progress on all of these", "help me brainstorm through the pile", "what is the state of all my strategies".
- A session has to reconcile several meeting notes, prep notes and stalled cards into answers he can give in one sitting.
- NOT for a single product brief he wants interrogated live: use `decision-grill`. NOT for one handed-over task: use `kanban-task-intake`.

# Settlement pack

Turn a pile of open threads (recent meetings, prep notes, stalled cards, half-started ideas) into one dated pack note where every item has a settled position, the first move an agent can do this week, and at most one ruling left for Deep. Kanban is Deep's only task surface, so the pack is the record and the cards are the surface. Related: `decision-grill` runs live when he wants to answer questions interactively; this skill runs when he wants movement without a session.

## 1. Gather sources before writing anything

Batch the reads: the vault's open ideation/prep notes (`Efforts/Active/Ideation/`), `TASKS.md` rows without a `[kanban:<id>]` tag, `kanban_list` for blocked and running cards, and the last few days of meeting notes. The ask usually names a few entities ("strategies across entities", "year-end discussions"); map each named thread to its source file or card id before drafting. If a named thread has no source anywhere, say so in the pack as an open thread rather than inventing its content.

## 2. Check the calendar inside the notes

Prep notes each propose a slot ("Wed 4 Nov 15:00 to 15:30"). Collect every proposed slot across the notes you read and compare them before writing: two threads in the same slot is a clash to settle at the top of the pack (keep the one that feeds a downstream call, move or cancel the other). A decision card that replaces a meeting says so in its Record line, so the cancelled slot is not left dangling.

## 3. Write the pack: one settled position per item

Path: `Efforts/Active/Ideation/<date> - <pack name>.md`, frontmatter `type: ideation`, `status: proposed`, `source:` naming the meetings and files it draws on. Per item:

1. **Settled position** as a short paragraph or table: what we do, not a re-listing of options. Where the position contradicts an earlier note or recommendation, state the contradiction and the mechanism in one clause ("the mailbox belongs to IT, so a parser needs IT to forward mail anyway").
2. **First move this week** naming who or which card executes it.
3. **The single ruling still Deep's**, as a table row at the end: card id, one-line question, recommended letter.

When the ask's referent is ambiguous (a phrase that could mean two products), state the assumption in one block at the top of that item's section, and give him a one-word escape ("reply void if you meant..."). Proceed on the assumption; do not stall the pack on it.

Everything an agent can do without an answer is already running or staged before the pack is done; the pack says so in its closing line. Nothing in the pack gets sent.

## 4. Cards: only what is genuinely his

| Situation | Move |
|---|---|
| New ruling, no card exists | `kanban_create(initial_status="blocked", initial_block_kind="needs_input", initial_block_reason="<DECISION line>")`, section 3 body, recommended option first, one question |
| Thread already carded | `kanban_comment` on the existing card with the pack's position; never a duplicate card |
| Prior note's recommendation overridden | The new card body names the old recommendation and why it loses; comment the same on the old note's card if one exists |
| A sub-ruling is too small to card | Fold it into an existing card as a comment (an extra criterion on a scoring card, a scope addition on a build card) |

Each card body ends with a `Record:` line pointing at the pack section, and a `Default if silent by <date/time IST>` that is a real near-term deadline, not a placeholder. Use an `idempotency_key` per pack so a re-run returns the existing card instead of duplicating it.

Then back-fill: card ids go into the pack's final ruling table, into a commented block of `TASKS.md` rows (one row per card, `[kanban:<id>]` tag so the intake sweep never cards it twice), and onto any existing card the pack supersedes. Search a link target with `search_files(target='files')` for the note name before putting a `[[wikilink]]` in a TASKS.md row; link-policy applies.

## 5. Close

Report the pack via `MEDIA:<absolute path>`, the one table of card id / question / recommended letter, and any clash or assumption he must know. No send, no merge: everything staged is named with its exact surface (draft title, card id).

## Pitfalls
- **Before ruling on a slot clash, grep `TASKS.md` and the latest `Efforts/Active/Celsus OS/Decision Desk/` note for the same clash.** The Decision Desk runs at 12AM and often rules first; a pack that rules the opposite way splits the day plan across two documents and has to be corrected on three cards. Keep its ruling unless you can name a reason it missed.
- **Pre-stage the free document edits the pack promises.** If a card's A says "the prep note is updated with this table" or "two additions go into the plan", make those edits now; they are reversible and the next worker reads the document, not the card.
- **Comment on the card that already owns the thread, do not create a second card.** Half the threads in a pile are already carded; a duplicate splits the answer across two ids and one of them stays blocked forever.
- **One card, one question, or swipe triage shows no buttons.** Stack two rulings as `1.` / `2.` with an "answer 1A 2B" instruction only when they genuinely ride one reply.
- **An overridden recommendation must carry its reason in the card body.** The old note still says the old thing and the next session reads it first; without the mechanism in the card, the override looks like a coin flip and gets reversed.
- **A slot clash found after the cards are made is still worth fixing.** Comment the clash on both cards even if the meetings were never on a real calendar; the clash lives in the prep notes, which is where the next session looks.
- **Do not restate what is already settled elsewhere in the pack.** A thread with a running card and a live owner gets one line pointing at it, not a section; the pack's length is the cost of reading it before 15:00.