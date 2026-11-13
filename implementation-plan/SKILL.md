---
name: implementation-plan
description: "Use when Deep hands a handoff and wants a rollout plan."
version: 1.0.0
author: Hermes Agent (Nous Research)
license: MIT
metadata:
  hermes:
    tags: [plan, rollout, ownership, accountability, handoff]
    related_skills: [kanban-task-intake, plan-and-prd-review, approval-pack]
---

# Implementation plan

## When to Use

**Trigger on:** "build on this and develop an implementation strategy", "implementation timeline, owners, accountability system", "roll this out to my teams", "turn this handoff into a plan", and any request that takes a supplied handoff, idea, audit or transcript and asks what would happen, when, and who owns it.

**Not for:** reviewing a plan that already exists (`plan-and-prd-review`), distilling a meeting into one decision page (`executive-one-pager`), or collecting an external stakeholder's sign-off (`approval-pack`).

Turn supplied material into a dated rollout he can rule on in one reply. The ask usually arrives as "build on this and give me an implementation strategy, timeline, owners and an accountability system". Four surfaces, always:

1. The plan note in the effort folder, `status: proposed`, delivered as `MEDIA:/abs/path`.
2. A receiver note appended to the handoff recording where you diverged from it and what its step 0 found.
3. A TASKS.md row carrying `[kanban:<id>]` (the card is the surface, the row is the record).
4. One blocked decision card, read back from the board before you report it.

Nothing is sent, asked, built or scheduled until he rules.

## Procedure

**1. Read the handoff end to end, then every asset it points at.** Transcripts, kits, playbooks. Its own "step 0 duplicate check" list is a required step with findings to report, not flavor: he will ask only for the strategy in chat and still expect the check to have happened.

**2. A mistyped product or company name is read by context, not asked about.** Normalize silently, work on, and state the assumption in one line. Stopping for a name the surrounding text already resolves costs a round trip for nothing.

**3. Duplicate check before designing anything.** Three surfaces: the vault efforts the handoff names, the related `Atlas` playbooks, and the board (`kanban_list` per status, keyword regex over titles, first 200 of the large lists). Emit a coverage table: existing thing | where | how the plan uses it. A control that already exists is reused and named in that table, never rebuilt in a section of its own.

**4. Resolve the handoff's open unknowns from the vault before writing.** Client abbreviations live under `Atlas/Clients`, roles under `Atlas/People`, team structure in `_config/`. A plan that inherits the handoff's unresolved "?" lines ships the uncertainty forward as if it were analysis.

**5. Verify its claims about task state against the record, never its prose.** Sweeps and migrations archive rows as stale, so a row described as done may be archived and never actioned. TASKS.md and the board are the state; the handoff is a report of the state when it was written. Correct the claim in the receiver note instead of repeating it.

**6. Label what is not verified, high in the document.** Numbers lifted from meeting notes are CLAIMED, each with its source line. Arithmetic on claimed numbers is still claimed, and a ratio built from two claims inherits both. Resolve what you can (an abbreviation, a contract value) and mark the rest.

**7. Owners: propose, never assign.** One accountable owner per stage, sourced from who already does the work (`Atlas/People`, meeting notes, existing meeting cadence). A seat the vault cannot support stays visibly unowned with the reason written in the table. Every slate carries that nobody has been asked.

**8. Timeline: dated phases, each ending in a gate.** Working days, planned inside his window. Week 0 is measurement whenever the plan depends on a baseline nobody has. Each phase closes on a numeric condition or a published artifact, and the next phase is conditional on it, so the plan reads as a sequence of checks rather than a wish list.

**9. Accountability rides meetings that already exist.** New standing meetings are the first thing a team drops, so slot reviews into cadences named in the notes. Missing numbers render "not measured", never blank or estimated. Attach no pay, KRA, appraisal or attendance consequence to a metric: that link is a separate ruling, and adding one silently converts a measurement plan into a performance record.

**10. One decision card, stacked, with a default.** Two rulings that are genuinely one reply (the plan and its owner slate) stack as `1.` / `2.` in the decision-card shape with a single default-by line and `Reply with the numbers`. Give it an explicit priority at creation so the desk cap does not park it before its default fires, and tell him in the reply that it may be shelved and that answering in chat works too.

**11. Deliver, then verify with commands.** Run the vault link verifier on the note, sweep the file for em dashes and en dashes, confirm the play and metric counts you claim in the reply match a regex count over the file, and read the card back.

## Pitfalls

- **Building what already exists.** A named duplicate check exists because prior efforts usually contain part of the answer; skip it and two owners end up chasing one job. Coverage table first, design second.
- **Letting a placeholder card id ship.** Write `t_PENDING` in the note, create the card, back-patch the real id, then count its occurrences in the file: an unpatched placeholder leaves him with a ruling he cannot answer by id.
- **Taking rep-reported revenue as a baseline.** Meeting-note figures are how a claim surfaced, not proof it holds. Quote them with source line and date, and make phase 0 re-derive them from the system of record.
- **Filling a seat he did not name.** A plausible person dropped into an unowned seat silently assigns work to a human. Leave it unowned in the table and put it in the decision options instead.
- **Shipping decisions as prose.** A plan ending in a list of decisions and no card goes unanswered until he rereads the document. Card them in the same pass as the note.
- **Reporting the duplicate check as done when only the vault was searched.** The board is a separate surface where the same work may already be carded; searching one of the two produces a plan that duplicates an open card.