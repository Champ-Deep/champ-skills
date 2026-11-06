---
name: email-data-to-deliverable
description: "Use when an email carries data or a data request to act on."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Email, Data, Analysis, Staging, Kanban, Celsus]
    related_skills: [email-inbox-triage, deep-email-voice, ms365-email, kanban-task-intake, visual-verify]
---

# Email data to deliverable

When Deep asks "did X send me the info about Y, and let's act on it", the answer is not a summary of the mail. It is: the data found and verified, what it already shows, a gap list that names what is missing and why it blocks the work, a draft of the next move staged in Outlook, and a decision card that names the exact draft. `email-inbox-triage` owns thread prioritization and reply policy; `deep-email-voice` owns wording. This skill owns the path from a data-bearing email to a staged, checkable deliverable.

## When to Use

- "Did X send the info about Y?" plus "let's visualize it / optimize it / build a better system".
- "Find the data in my email and act on it" where the ask needs an artifact (map, roster, timeline, plan) plus a reply to the sender.
- Any run where the mailbox holds a dataset (table, roster, timings, locations) that must be verified, gap-analyzed, and turned into a staged next move.

Don't use for: plain inbox triage or retrieving one known message (`email-inbox-triage`, connector skills), or wording a draft in Deep's voice (`deep-email-voice`). Load those alongside when the run needs them.

## Procedure

### 1. Locate the mail, then read the source, not the render

Search the mailbox (`ms365-email` connector) for the sender and the topic. When the payload is a **table** (timings, rosters, locations, headcounts), fetch the raw message body (`get_mail_message_mime` or the HTML body) and read the cell structure directly: an HTML table often merges cells, so a name rendered beside a time in the preview may actually sit in a neighbouring column. Reconcile the preview against the raw HTML before any downstream claim about who is in which slot. Done when every row you will quote has a raw-source basis.

Pitfall: quoting a rendered preview as fact. The preview flattens merged cells, so a person can be attributed to the wrong time, and every route or plan built on that row inherits the error.

Pitfall: quoting a slot or category count that only the rendered text gave you. A `rowspan` that stacks several people under one time reads correctly in the preview while the grouping is easy to mis-tally, so every count you state (`N people in M slots`) comes from a parse of the raw cells, counted in code rather than by eye, and the same count is what the artifact and the draft assert.

### 2. Cross-check the same fact across surfaces

The email is one witness. Check the other places the same fact is recorded before you trust it:

- **Meetings**: Wispr `search_meetings` / `get_meeting` (transcript over summary) for what was said about the data, who owns the next move, and any promise with a date.
- **Tasks**: `kanban_list` / `kanban_show` and a `search_files` over `TASKS.md` for an existing card or row on the same subject. An intake sweep often already created a blocked decision card for it.
- **Vault**: `Efforts/`, `Atlas/`, `Calendar/` for prior notes on the same people or process.

Done when every number and name you will present is either single-sourced and labelled, or reconciled across at least two surfaces with any conflict stated.

Pitfall: creating a duplicate task. If a card already exists for the subject, comment the new decision on it instead of creating a second card; two cards for one decision split Deep's attention and one of them rots.

### 3. Write the gap list before the plan

List what the data does **not** contain, and for each gap state what it blocks ("no pickup locations, so no route can be planned"). Then state what the data already shows: the pattern, the outliers, the rows that disagree with another source. A gap list that only says "addresses are missing" is weak; the useful form names the consequence, because that is what justifies the ask in the staged draft.

Pitfall: presenting a plan built on missing data as if it were executable. If the input lacks a required field, the plan must say so in its own first section, not in a footnote.

### 4. Build the artifact, and verify it by eye

Produce the visualization or document Deep asked for (a slot timeline, a map, a roster sheet, a rough PRD). When the run's output is a data request, build the fill-in sheet in the same step: prefilled with every row and field you already have from the mail, dropdowns on the choice fields (pickup or drop, gender for a women-first rule), a tab each for the surrounding data the recipient owns (fleet, one-off trips), and a flagged note on any row where their own source contradicts itself. Verify by reopening the written file and asserting row count and spot cells in code, never by trusting the writer call; it is what the staged draft attaches.

Then verify the artifact renders as intended before you attach or link it:

- If the browser tool is available, navigate to the file and screenshot it.
- If it is not, render headless from the terminal: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --window-size=<w>,<h> --screenshot=out.png "file:///<abs path>"`, then read the PNG with `vision_analyze` and ask specifically about overlap, clipping and legibility.

Pitfall: shipping an unverified layout. Overlapping time columns and clipped table rows are invisible in source and obvious to the reader; a vision pass on a rendered screenshot is the cheapest gate.

For vault deliverables follow the design rule in memory: any HTML or document for Deep goes through a design skill first (`frontend-design` + a brand skill + `visual-verify`), never bare markup.

### 5. Stage the reply, then read it back

Before creating anything: search Drafts and Sent Items for the same subject or counterparty. Outlook has no edit-draft tool, so a draft already sitting there either goes out with its old facts or becomes a second competing draft. If an unsent one carries a defect, stage a replacement and name both subjects in the report: SEND the replacement, DELETE the stale one. If it already went out, branch the ask into a fresh follow-up instead of restating it.

Then draft the outgoing mail in Deep's voice (`deep-email-voice`) via `ms365-email` `create_draft_email`. When the ask is for missing data, attach the input sheet built in step 4 rather than asking in prose: prefilled with every field you already know, dropdowns on the choice fields, one row per known record, so the recipient fills only the gaps. Then **read the draft back** (`get_mail_message` with a `select` on subject, isDraft, toRecipients, ccRecipients) and confirm in your report that it is unsent and addressed as intended. A 201 from create is not proof the draft is correct; the read-back is.

Pitfall: reporting a draft as ready without reading it back. Create returns a payload that can differ from what you believe you sent (recipient resolution, body contentType), and the reader only discovers it after Deep presses Send.

### 6. Land the decision card

The card is the last mile. Post the decision as a comment on the relevant existing card (or create one only if none exists), and the comment must carry:

- What is staged: the exact draft subject and recipients.
- The options A/B/C with the recommendation first.
- A default action and date if Deep stays silent.
- What is blocked and on whom (e.g. "MVP cannot start until the locations sheet arrives").

Pitfall: a card that says "review the cab details" with no draft named. Deep rules on a named artifact; a card that points at prose makes him re-read the thread to decide.

### 7. Report in three separated blocks

1. **What the data shows** (verified findings, with the conflicts called out).
2. **What is staged** (the draft, with the link, and the read-back confirmation).
3. **What needs Deep** (the decision card, options, default date).

Never merge "staged" into "done". A staged draft is not sent, and the report must leave Deep with one decision to make, not a wall of process.

The artifact travels with the report: previews carrying personal data (employee names with home locations, shift or travel times) stay machine-local, and the handoff says so by file path or local URL, so a later session never publishes them.

## Verification

- [ ] Every quoted row traces to the raw message body, not the preview.
- [ ] Every stated count comes from a parse of those same raw cells, not the rendered text.
- [ ] Drafts and Sent were searched before staging, so no stale or duplicate draft is left unnamed.
- [ ] The data request carries an attachment, and the read-back shows it.
- [ ] Each fact is single-sourced and labelled, or reconciled across two surfaces with conflicts stated.
- [ ] The gap list names what each missing field blocks.
- [ ] The artifact was rendered and vision-checked for overlap/clipping.
- [ ] The draft was read back from the provider: unsent, correct recipients.
- [ ] The decision card names the exact draft, options, recommendation, and a silent-default date.
- [ ] The final reply separates findings, staged work, and the one decision needed.
