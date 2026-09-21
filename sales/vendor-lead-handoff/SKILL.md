---
name: "vendor-lead-handoff"
description: "Turn a delivery vendor's lead or appointment handover into a client-safe email with the vendor scrubbed out. MANDATORY TRIGGER for any pasted or forwarded vendor email delivering leads, MQLs, SQLs, AG leads, booked appointments, call recordings, voice logs or lead sheets; and for \"respond to [client] with these leads\", \"send these leads to the client\", \"the vendor sent leads\", \"forward this to the client\", \"scrub the vendor out\", \"client-safe version of this\", \"check this file for vendor details\", \"is this attachment safe to send\". Also runs when a vendor asks us to schedule, invite, or contact prospects, and when a handed-over meeting is too soon for the client to staff and needs a fallback. Applies the Champions Group client firewall, audits attachment metadata and hosting, cross-checks the cover email against the attachment, sets the delivery clock, and appends every judgement call to its own decision log so it gets sharper each time."
---

# Vendor Lead Handoff

Convert a delivery vendor's lead handover into something the end client can receive without ever learning who executed it.

We sit in the middle. The client believes they are buying from us. The vendor believes they are executing a brief. Both are true, and the value of the middle position collapses the moment either side can see past us to the other. Every rule below exists to protect that position.

---

## The one rule everything else serves

**The client is never told the vendor's name.** Not the company, not the person, not the domain, not the file naming convention, not "our partner", not "the calling team". We delivered these leads. A recording is our recording. A delay is our delay. A quality problem is our quality problem.

The mirror rule: the vendor is never told the end client's name, rate, or that another vendor exists on the same account.

---

## Run order

Do not reorder these. Steps 3 and 3a have killed more accounts than everything else combined.

### 1. Read the context before writing a word

Never draft from the vendor email alone. Pull, in this order:

1. The client note in the vault, for the contracted deliverable, the agreed unit, the CPL, the acceptance criteria and the named contacts.
2. The account's daily notes or update log, for what the client was last told and what was last promised to them.
3. The firewall and anonymization files, for the standing routing rules and the vendor's tag.

What you are looking for specifically:

- **What was promised to this client, in writing, and when.** A handover email that ignores an outstanding commitment reads as evasion.
- **What unit the contract actually buys.** A vendor delivering something better than the contracted unit is good news and a pricing question, not a free upgrade.
- **What the client's stated rejection criteria are.** These decide how carefully every claim in the handover has to be worded.
- **Who the client contacts are and who sends from our side.** Use the account's established sender, cc list and channel. Do not improvise a distribution list.
- **How responsive this client has been.** This determines whether the email can afford to depend on a reply. See step 4a.

### 2. Set the clock before you set the tone

Extract every timestamp in the handover and convert to a single reference zone, then to the client's zone. Build the table:

| Item | Client's local time | Hours from now |
|---|---|---|

Then answer one question: **what is the earliest moment the client must act, and does our sending schedule beat it?**

A booked appointment inside 24 hours overrides every routine cadence on the account. If the standing update goes at 18:15 and the meeting is at 10:00 tomorrow, the handover does not wait for 18:15. Say so plainly in the output.

Watch for the zone traps: SGT is UTC+8, WIB is UTC+7, IST is UTC+5:30. A meeting quoted in a prospect's local zone is not the client's zone and is not ours. Always show the client their own time.

### 3. The redaction pass

Five passes over the draft and over every attachment. This is the step that gets skipped under time pressure, and time pressure is exactly when the handover is most likely to leak.

**Pass 1, names.** Vendor company, vendor staff, vendor domain, vendor product names, in the body, the subject, the signature and the quoted thread. Delete the quoted thread entirely rather than trimming it.

**Pass 2, numbers.** Vendor rate, our margin, the spread, internal lead counts, budget, anything belonging to the other side of the relationship.

**Pass 3, posture.** Any sentence revealing what we think of the vendor, what we are comparing them to, that a lead was disputed or re-run, or that a second source exists.

**Pass 4, file metadata. The invisible one, and the one that actually fails.** A spreadsheet can be spotless in every visible cell and still name the vendor in its properties. Check, by name:

- Office files: `dc:creator` (Author) and `cp:lastModifiedBy` (Last saved by) in `docProps/core.xml`, plus `<Company>` in `docProps/app.xml`. Unzip the file and read the XML if you can; do not trust a visual scan of the grid.
- PDFs: Author, Creator, Producer, Title.
- Media: embedded tags and device metadata.

Fix by running Inspect Document and removing Document Properties and Personal Information, or by rebuilding the content in our own template, which is cleaner and lets you fix data errors at the same time. **Verify after.** Reopen properties and confirm the fields are ours or blank. An unverified strip is not a strip.

**Pass 5, filenames and hosting.**

- Rename to an internal reference. `Acme_JaneDoe.wav` leaks the whole story before anyone presses play, and a filename that is the prospect's own email address is worse.
- **Never forward a vendor-hosted link.** Download, rename, rehost on our storage, share our link. A vendor's personal cloud folder is not access controlled, is re-shareable and downloadable by anyone holding the URL, can be deleted by them at any time, and renders differently to a signed-in viewer than to the anonymous view you are testing it in. Your client opens links signed into their work account. Do not bet the firewall on a UI behaviour you cannot control.
- Never put prospect contact details in the body of an email. They go in the sheet.
- Do not forward the vendor's originals, ever, even after a visual check.

**The one-way mirror test, faster than the checklist and catches what it misses:** if this exact message were forwarded to the vendor, or to another client, what would it cost us? If the answer is anything but "nothing", rewrite it.

### 3a. Cross-check the cover email against the attachment

**The vendor's summary is a sales document. The attachment is the evidence. They disagree more often than you would expect, and the summary is always the flattering one.**

Open the attachment and reconcile every claim in the cover email against it. Specifically:

- A meeting stated as confirmed, where the caller notes say the time was "discussed", "proposed", "preferred" or "to be confirmed".
- A qualification stated as met, where the notes show it was inferred rather than asked.
- A named contact in the email who is not the person actually spoken to in the notes.
- Counts that do not match the number of rows.
- Values in the wrong column, which is a data quality tell and also lands in front of the client.

Whatever the attachment says wins. Rewrite the client email to the evidence, not to the cover note. Passing on an overstatement makes it ours the moment we send it, and on an account where the client has already set rejection criteria, an overstated confirmation is the exact stick they have been waiting for.

### 4. Write the email

Short and plain. No jargon, no report formatting inside an email body, no bullet-point walls, no headers. Depth belongs in the attachment or a companion note, never in the email.

Structure:

1. **What we have**, in one line. The good news first and unhedged, but only as strong as the evidence supports.
2. **The details that need no attachment.** Dates and times in the client's own zone. Mark firm items firm and soft items soft, explicitly.
3. **Where the rest lives.** "Details and qualification notes are in the attached sheet."
4. **The single action we need from them**, named as one thing, with a deadline attached to the soonest meeting.
5. **What we are doing between now and then.** Attendance follow-up, invites, confirming anything still soft.
6. **One forward-looking line** that promises effort, not volume or dates.

Hard constraints on the copy:

- No em dashes. Use periods, commas, colons, or restructure.
- Never write "our partner", "our vendor", "the team on the ground", "our calling partner". Write "we".
- Never repeat the vendor's phrasing. Vendor delivery emails have a house style ("Hope you are doing well", "Please keep us posted with feedback, returns and/or any incremental programs"). Copying it is a tell.
- Do not commit to a lead count, a rate, or how these leads count against the contract, unless that has been answered. Silence on commercials is not evasion, it is sequencing.
- Do not bundle bad news into a good-news delivery email. Send them separately. Mixing dilutes both.

### 4a. The short-notice fallback

Vendors deliver appointments late. A meeting handed over the evening before is normal, not exceptional, and the client usually cannot staff it. **Write the email so it does not need a reply to work.**

Four moves, in order, inside the same paragraph:

1. **Name the problem before they do.** "That is short notice" costs one line and buys the whole rest of the paragraph. A client who has to point out the timing themselves is already annoyed.
2. **Ask for the easy version.** One name, sent tonight. Nothing else.
3. **Offer the graceful exit.** Two concrete alternative slots, same time of day, chosen so one of them sits next to something already in their calendar. The honest answer is usually that they cannot cover it, and people do not like writing that sentence themselves. Write it for them.
4. **State the default and the cutoff.** "If I have not heard by {time} I will {action} and confirm to you." Silence becomes a decision instead of a dead prospect.

Then have the fallback assets already drafted: the prospect-facing reschedule note, and a one-paragraph message for whatever informal channel exists with this client. Do not make the fallback a thing that has to be written in a panic at 08:30.

**The judgement that decides the default action.** Rescheduling a booked appointment is not free. The prospect agreed to a time, and moving it risks losing them. It is still the better branch than a no-show: a client who fails to appear burns the prospect completely and lands on the credibility of whoever booked it, while a proactive move with real notice is recoverable. But that only holds if the move goes out **early**. A reschedule reaching the prospect fifteen minutes before the call is a no-show with extra steps. Set the cutoff so the prospect gets at least ninety minutes.

**Fix the pattern, not just the instance.** Every short-notice handover should carry one line asking the client to name a standing default attendee for short-notice appointments. It costs nothing, and it removes the entire scramble the next time.

### 5. Write the vendor-side reply

Usually needed, usually forgotten. The vendor's handover email almost always contains an instruction that must be refused or redirected. The recurring one: **the vendor asks us, or the client, to schedule or contact prospects.** Meeting invites go out from us. The vendor does not touch the meeting.

Cover, briefly:

- Receipt confirmation.
- Who owns prospect contact from here. Always us. If the notes mention the vendor emailing a prospect, ask which address it went from and what it said, before the next batch.
- File naming, metadata, transport and PII rules for the next batch. Internal references, our storage, no personal cloud links, no prospect names or emails as filenames.
- Any claim in their cover email that the attachment did not support, named plainly so it does not recur.
- Any assessment-gate item still outstanding, especially the brand and identity clause.
- If short notice is a pattern, the minimum lead time we need on a booked appointment.

Keep it to five short paragraphs. It is a process note, not a lecture.

### 6. Risk pass

Write the risks out, ranked, with the highest first. Do not bury them below the drafts. The standing checks:

| Check | The failure it prevents |
|---|---|
| Attachment branding **and file metadata**, verified after stripping | Firewall breach on open or on right-click Properties |
| Recording renamed and rehosted on our storage | PII in filenames, and a deliverable the vendor can delete |
| Cover email reconciled against the attachment | Passing on an overstatement that becomes ours |
| Soonest meeting vs send time | A confirmed appointment becomes a no-show |
| Fallback drafted and cutoff set | A silent client killing a live prospect |
| New vendor assessment gate cleared | An unbriefed vendor names us or the client to a prospect |
| Delivered unit vs contracted unit | Billing dispute, or acceptance refused on criteria |
| Second vendor exposure to the incumbent | Loss of negotiating leverage |
| Prospect overlap with the incumbent's dial list | Two suppliers calling one prospect, client sees chaos |
| Tracker visibility | The incumbent reading a shared sheet and seeing the second source |

### 7. Output shape

Produce one vault note holding: the clock, the attachment audit with an explicit pass or fail per surface, the client email, any fallback assets, the vendor reply, the risks ranked, and an owner-and-deadline action table with the scrubbing and fallback steps as their own timed rows. Then state the send order and the deadline in the chat reply, in two sentences.

Never send anything. Drafts only. Anything containing a vendor name going to a client, or a client name going to a vendor, is on the permanent never-auto list.

---

## Escalation triggers

Stop and raise these rather than drafting through them:

- The handover contains prospect PII inline in the email body.
- A recording or file is named with a prospect name, company or email address.
- Files are shared from a vendor's personal cloud account rather than a controlled link.
- The cover email claims something the attachment contradicts.
- The vendor has emailed prospects directly, or named us or the client to a prospect.
- The delivered unit differs from the contracted unit and nobody has priced it.
- The vendor is new and the NDA or brand clause is unsigned.
- The soonest meeting is inside 12 hours.

---

## Decision log

Append-only. Every judgement call made while running this skill gets a row. Read this section before drafting; it is where the account-specific rulings live, and it is the reason this skill gets better rather than just repeating itself.

Format: date, account, the question, the ruling, the reasoning.

---

**2026-09-07 · Epicor · Does a second source's leads go into the shared tracker?**
No. Separate tab or separate sheet. The incumbent has edit access to the shared tracker and would see a second supplier delivering on an account where it has filed four consecutive blank days. Vendor-to-vendor exposure destroys leverage rather than merely leaking a fact.

**2026-09-07 · Epicor · Who sends the calendar invite when the vendor offers to?**
We do, from the client-facing corporate mailbox, never a personal or Gmail account. The vendor is told explicitly not to contact the prospect about the meeting. An invite from a vendor domain identifies the supply chain in the prospect's calendar, permanently, and a prior invite sent from a Gmail address on this account was not received by the client.

**2026-09-07 · Epicor · Appointment-generation leads arrived where the contract buys tentative-slot SQLs.**
Deliver first, price second, but price it inside the week. Do not imply in the delivery email that they count against the contracted number, and do not imply that they do not. The acceptance criteria were written against the weaker unit, so a better unit is a commercial conversation, not an automatic win. Commercial owners answer before the next batch.

**2026-09-07 · Epicor · Should a good-news lead delivery carry the outstanding bad news about missed daily numbers?**
No. Separate emails. The client was already owed a numbers-and-plan email at a committed time; folding it into an appointment handover reads as using the good news to bury the bad, and dilutes both. Send the appointments the night they arrive because a meeting is inside 24 hours, and keep the committed slot for the numbers.

**2026-09-07 · Epicor · The vendor's handover email had a distinctive house style.**
Rewrite from scratch, never edit the vendor's text down. Retained phrasing is a tell, and a client who has seen one vendor's writing recognises it in the next email. Structure, greeting and sign-off all get rebuilt in our voice.

**2026-09-07 · Epicor · The handed-over meeting is the next morning and the client probably cannot staff it.**
Do not send an ask that only works if they reply in time. Name the short notice yourself, ask for one name, offer two concrete alternative slots, then state the default action and a cutoff so silence resolves instead of stalling. Default to moving the meeting rather than risking a no-show, because a client no-show burns the prospect outright while a move with ninety minutes of notice is recoverable. Draft the prospect reschedule note and the informal-channel nudge at the same time, not when the cutoff hits. Add a standing ask for a default short-notice attendee so the scramble does not repeat.

**2026-09-07 · Epicor · Which alternative slots to offer.**
Offer two, same time of day, and pick at least one that sits immediately before or after something already in the client's calendar for that account, such as the weekly review. It lowers the cost of saying yes and makes the alternative feel like less of a new commitment.

**2026-09-07 · Epicor · The lead sheet was clean in every visible cell. Was it safe to send?**
No. `dc:creator` and `cp:lastModifiedBy` in the workbook's `docProps/core.xml` carried two vendor staff names, one of them the sender of the handover email. A visual scan of the grid passes a file that a right-click on Properties fails. **Always unzip and read the metadata rather than eyeballing the content, and verify the fields again after stripping.** Rebuilding the rows in our own template is the more reliable fix, because it removes the metadata and the vendor's formatting in one move.

**2026-09-07 · Epicor · The recordings were shared on the vendor's personal cloud folder with no vendor name in the URL or filenames. Forward the link?**
No. Absence of a vendor name is necessary, not sufficient. The filenames carried a prospect's name plus company and a prospect's live email address, the folder was anyone-with-the-link with download and re-share enabled, the vendor can delete it at any time, and an anonymous test view is not the view a signed-in corporate recipient gets. Download, rename to an internal reference, rehost on our storage, send our link.

**2026-09-07 · Epicor · The cover email said both meetings were confirmed with a time. The attachment said one was not.**
The attachment wins, always. The vendor's own notes said the second time was "discussed, but not explicitly confirmed by the prospect". Passing the cover email's version through would have made the overstatement ours, in front of a client who had already put rejection criteria in writing. Mark firm items firm and soft items soft in the client email, and say who is locking the soft one and when. **Reconciling the cover note against the evidence is now a required step, not a nicety.**

---

*Add a row every time a new judgement is made. If a ruling is later reversed, add the reversal as a new row with the reasoning rather than editing the original, so the reasoning trail survives.*

