---
name: kra-authoring
description: "Use when drafting a KRA or appraisal for Deep's team."
---

# KRA authoring (Celsus)

A KRA in this vault is a weighted, reviewable contract, not a job description. Deep drafts, the brand owner prices it, HR files it. The draft's job is to make the reviewer's edits cheap.

## When to Use

Any ask to draft, revise, price, review or send a KRA, appraisal, variable-pay gate, performance target sheet, or "come up with his/her KRA" for a named person in the vault. Also when Deep asks what was previously agreed with someone about their role or targets, because that evidence is the input to the draft.

## Procedure

### 1. Gather evidence before drafting anything

Read, in this order:

1. `Atlas/People/<Name>.md` for role, solid line, escalation, start date.
2. The person's plan or onboarding effort under `Efforts/Active/` (month plan, 60-day plan, KRA folder). This tells you what they were *meant* to do.
3. Every vault hit for the person's name, biased to `Calendar/Meetings/`, `Atlas/Zoom Triage/`, `Calendar/Daily Notes/`, `TASKS.md`, and the brand-owner tables in `Efforts/Active/KRA Framework Q2 2026/` and `Efforts/Active/Q3 FY27 Marketing Plan/`. This tells you what they are *actually* asked to do, which is the only thing a KRA should price.
4. The open task row for this KRA in `TASKS.md`, plus the effort it is tagged to. That row is the deadline and the send-state ledger.

If Deep asks whether prior conversations exist on the topic, search conversation history too (see `celsus-vault`, Searching the vault): one empty query is not evidence of absence.

**A plan is intent, not achievement.** Never write "delivered the Week 4 dashboard" because a plan called for it. Either cite a completion record or leave the claim out.

### 2. Pick the template that already governs the class

| Need | Read |
|---|---|
| The house structure: five buckets A to E, weight schedule, rating scale with the cross-brand gate, scoped reporting, conflict tie-breakers | `Efforts/Active/KRA Framework Q2 2026/KRA-Brand-Owner-Framework.md` (Section 7 is the reusable template) |
| A full worked document at senior/specialist depth: identification, role summary, cadence table, allocation, KPI tables, mutual commitments, escalation, acknowledgment | `Efforts/Active/Kethan KRA Operationalization/Kethan-KRA-v1-Final.md` |
| The current short-form sheet for interns/trainees (weights must sum to 100) | `Efforts/Active/Accelerator KRAs Q3 FY27/`, and read `Accelerator-KRAs-Q3-FY27.xlsx` with the `xlsx` skill: that workbook is the format authority for the Excel deliverable, not its prose sibling |
| A plain bullet KRA for a junior under a senior's team | the Aishwarya section of the SPAN content send pack in `Efforts/Active/SPAN Content/` |

Reuse the skeleton verbatim: identification (both hats plus scoped dotted lines), role summary, reporting and cadence, allocation, KRAs with KPI tables, rating scale, mutual commitments, escalation path, acknowledgment. Never invent a new section shape.

### 3. Scope the buckets to the person's tier

- Seniors: five buckets A to E with the framework's dynamic weights.
- Juniors, trainees and task owners: a lighter set, weights still summing to 100, with the cross-brand bucket kept small but present so a rating above Meets stays reachable.
- Junior KRAs nest under a senior: the brand dotted line names who owns WHAT and WHEN, the function dotted line names who owns HOW, the solid line stays with Deep.

### 4. Write the targets as proposals, and price the ambiguity out

- Label every number as proposed, and give the reviewer the lever ("25 to 40 per week proposed") rather than a bare figure.
- Ground the KRA in one named, evidenced gap from step 1, stated in the role summary. A KRA with no named gap reads as a generic template.
- End with an **Open questions** section listing exactly what the reviewer must answer before the document is issued: cadence timing, priority order, volume, co-sign, budget approval. Batch them into one round.
- Include mutual commitments from the leaders as well as the employee. Targets the company does not enable are not a contract.

### 5. Deliver three artifacts, in the effort folder

1. The KRA note, e.g. `Efforts/Active/<Effort>/KRA - <Name> - Draft for <Reviewer>.md`: the reasoning, the evidence, the scoped lines, the open questions.
2. The Excel KRA in the same folder, `KRA - <Name>.xlsx`, built with the `xlsx` skill to the house sheet format: a `Summary` tab (one row per person, weights in prose, overall rating pulled by formula, a how-to-score block) plus a person tab holding the header block (designation, business unit, reporting manager, scoped lines, period, review dates, rating scale), the KRA table (KRA, Weight %, KPI, Target and scoring, Source, Cadence, Score, Evidence), and a scoring-summary block where each KRA averages its own KPI range and the overall is the weight-distributed result. Score cells are the only styled input cells; weights sum to 100 on the sheet itself.
3. A companion cover-email draft in the same folder: subject, recipient, cc, a short weight table, the questions asked, and the paths to both files.

Deep works in sheets as well as notes: a KRA that will be priced by a reviewer and filed by HR needs the Excel even when the note is finished, so build both rather than waiting to be asked.

When the send moment comes, put the draft where it will be sent from: create it in Outlook Drafts with the M365 connector (`create_draft_email`, subject, to, cc, body), after `verify_login` confirms the connector actually holds a token. The vault files are the record, the Outlook draft is the deliverable. Still never send.

Then annotate, never close, the `TASKS.md` row: what was written, where it lives, and that it is not yet sent.

### 6. Verify before delivering

- Every wikilink target exists: `find /Users/deep/Celsus -name "<basename>.md" -not -path "*/.git/*"`. Replace a missing target with plain text rather than creating a note just to satisfy a link.
- Run `scripts/verify_links.py` from the `celsus-vault` skill on the new file.
- No em or en dashes anywhere in the markdown files (python sweep, per `celsus-vault`); check the Excel's text cells in the same sweep.
- Aliases piped per `_config/link-policy.md` (`[[SPAN Global Services\|SPAN]]`), never-link list respected.
- For the Excel: read it back with `xlsx_read.py --sheets` and `--formulas` before claiming it is done. Confirm weights total 100, every weighted formula points at its own row (off-by-one row arithmetic is the common defect when the spec is assembled programmatically), each KRA average covers exactly its KPI rows, and the score column is the only filled input column.
- Deliver with `MEDIA:` only for files verified to exist.

### 7. Send only on an explicit go

The draft is not the send. Stage it, tell Deep it is staged, and wait. When the send happens, the claim that it went out is verified against Sent Items or the dispatch digest, never against the existence of a draft.

## Pitfalls

- **Do not draft from the job description or the resume.** The KRA must price the work the reviewer actually assigns; a JD-shaped KRA gets rewritten wholesale in review, which is the round trip the draft exists to avoid.
- **Do not assert a person's completed work from their plan file.** Plans record intent, so an unverified "achieved" line is a fabricated claim in a document HR will file.
- **Do not let weights drift.** Every allocation must sum to exactly 100 before delivery; a gap that opens when a bucket is dropped is caught only at review.
- **Do not send, tick the task, or report it went out on the strength of a finished draft.** Staged is not sent.
- **Do not treat an empty history search as proof nothing was discussed.** Session history search is FTS with AND semantics, so a multi-word query can come back with zero sessions searched, which is a property of the query, not of history. Drop to single tokens (the topic word, the person's name) and grep the vault for files that mention both parties before saying "no record exists".
- **Do not put pay terms in a KRA email.** Compensation stays in its own thread with HR; the KRA carries targets only.
- **Do not call the mail connector ready because a browser page says signed in.** Only the connector's own token check says that; the sign-in page confirming success and the connector holding a token are two different events, and the second one is the only one that lets you create the draft.
