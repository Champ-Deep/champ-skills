---
name: meeting-followup
description: >-
  Everything after a meeting, in one skill. Intake: file meeting notes, summaries, transcripts or recordings into structured vault knowledge and tasks. Follow-up: act on the meeting for Deep, building the commitment ledger, drafting every deliverable he owes, a prepared-plus extra and a logistics check. Send kit: assemble ready-to-send packages for external meetings (cleaned follow-up email, committed docs, one-pager) staged as drafts. MANDATORY TRIGGER for: pasted meeting notes, summaries or Zoom transcripts, "here are my notes from", "just got out of a call", uploaded meeting audio or video, a wall of text with names, decisions and next steps, "follow up on this", "help me follow up", "what do I owe from this meeting", "get me ready for the next call with [person]", "send kit", "grab the send kit", "documentation emails for my meetings", and the nightly Zoom sweep. Pasted content with no instruction: file it, then offer the follow-up. Replaces meeting-intake and send-kit.
---

## Absorbed modes

| Mode | Use when | Read |
|---|---|---|
| **meeting-intake** | Pasted or uploaded meeting content with no action asked: file it, extract tasks. Step 6 below also calls this | `modes/meeting-intake/MODE.md` |
| **send-kit** | External meeting needs a documentation package staged as drafts, or the weekly follow-up review asks for kits | `modes/send-kit/MODE.md` |

Where the text below says "run meeting-intake" or "file via meeting-intake", read `modes/meeting-intake/MODE.md`. Before appending any task to TASKS.md, dedupe it (vault-keeper, celsus-task-dedupe mode).

# Meeting Follow-up

## The Definition (what Deep means by "follow up on a discussion")

Following up on a discussion means, in priority order:

1. **Deep's commitments come first.** Anything Deep committed to in the meeting gets DONE or DRAFTED before
   the next touchpoint with those people. The failure mode this skill exists to prevent, in his words: being
   left with his pants down, unable to showcase something he promised in the previous meeting. If only one
   thing gets done, it is this.
2. **The prepared-plus extra.** One step beyond the literal commitments: an artifact, analysis, or prep item
   that was not promised but shows the other side we came prepared. One strong extra beats three weak ones.
3. **The chase list.** Commitments OTHERS made to Deep or the team, tracked with owner and due date, with
   drafted nudges ready when they slip.
4. **The logistics guard.** Any "we'll discuss Monday" or "let's reconnect next week" must exist as a real
   calendar event. A follow-up meeting that is not scheduled is a follow-up that will not happen.
5. **File and track.** The meeting lands in the vault and TASKS.md via the meeting-intake skill. Filing is
   necessary but never sufficient; a filed note with undone commitments is a failed follow-up.

## Pipeline

### Step 1: Source the meeting

- Pasted summary or notes: use as the primary source, but if the Zoom MCP is connected, find the matching
  meeting (search_meetings by keywords and date) and pull the transcript. Summaries hide who said "I will."
- Transcript source chain: Zoom first; when Zoom has no transcript for the meeting, search Wispr next
  (`search_meetings` by subject/participant/date, then `get_meeting` for the full transcript). Wispr records
  meetings Zoom never saw (in-person, phone, Meet) and mirrors calendar subjects; local recordings under
  Downloads/Zoom are the last resort. Always pass the server prefix: Zoom and Wispr both expose
  `search_meetings`, and an unqualified call resolves to the wrong one.
- A `notes.wisprflow.ai/shared/...` link is not a transcript source: it can serve an unrelated note or a
  login wall for any id. Before calling a call's wording "unrecoverable", use `get_meeting` with the Wispr
  meeting id, or grep the watcher's stored tool result for the register quote:
  `sqlite3 -readonly ~/.hermes/state.db "select id from messages where role='tool' and content like '%<quote>%'"`.
  A follow-through card that maps a promise to a tool must quote the transcript lines that name it.
  The same applies to softer wording: "detail beyond the summary line not seen" or "summary read only" is
  an unrecoverable claim too. `get_meeting` returns the summary and the transcript in one result, so read
  the transcript body (grep its `Speaker` lines for the topic's words) before writing that a role, duty or
  figure "was not said". One role-evidence readout said nothing past "for data selling" was said, while the
  stored result held the business line, the KRA basis and the multi-channel condition verbatim.
- Sweep the mailbox for the same evening (Outlook `$search="keyword AND received>=YYYY-MM-DD"`): follow-ups
  get emailed after the call, and final pricing, attached decks, and internal decisions live in mail bodies
  and attachments. A ledger built from the transcript alone misses commitments that were sent rather than said.
- Scheduled sweep: recover the latest state-bearing response from the same watcher before pulling. A `[SILENT]` response has no state; look past quiet runs in the cron outputs and then the watcher's recorded assistant turns. First-run fallback applies only when neither has a watermark. Calculate the 48-hour overlap from that watermark, page through Wispr, and compare exact meeting IDs in code before fetching transcripts. Read only the cron file's actual response section, not its embedded previous-output prompt. If the newest non-silent response has a clipped or malformed processed line, carry forward the latest intact response line and add any missing intervening meeting IDs only after corroborating each exact ID against the source-linked task rows and board cards. Never infer a UUID from a clipped token. A malformed ID can coincide with valid-looking changes elsewhere in the same line. Keep the earlier intact ordering and validate genuinely new IDs against the current result or a source-linked recap; do not union all syntactically valid differences. Keep the prior watermark on quiet runs and honor the exact suppression token.
- A calendar-linked recording can have the full invite duration in `start` and `end` even when the transcript is only a few seconds and the guest declined. Open the transcript when the duration is suspect, treat a declined invite with no substantive discussion as processed without follow-up, and check for a separate rescheduled invite before acting. Do not attach the old capture or its action items to the new invite just because the titles match.
- get_meeting_assets returns a huge payload; save to file and extract with jq (transcript_items, content_markdown), never read raw into context.
- Speaker resolution: "my notes" transcripts label people Speaker 1/2/etc. Identify Deep by voice: he is the
  one coaching, setting strategy, and saying "I'll send you the plan from my end." Verbal tics: "things like
  that", "you know", "incredibly important". If identity is genuinely ambiguous, ask once via AskUserQuestion.
  Normalize mangled names against known people (transcripts garble Indian names constantly).
- Treat named labels as unverified too: a real person's name can sit on another's lines, and one label can
  change identity mid-transcript when participants drop off or diarization drifts. Attribute each commitment
  by content (who would plausibly owe it: client side vs ours, which role), cross-check against invite
  attendees, and mark the attribution CONFIRM whenever it changes who owes what.
- If the full transcript is about a different meeting than the attached calendar title, retain the recording ID
  and share link, file under the recorded subject, and document the mismatch. Do not infer client attendance,
  commitments, recipients or invitees from the unrelated event. Corroborate internal names independently.

### Step 2: Build the commitment ledger

A table with: owner, commitment (verbatim where possible), due date (absolute, never relative; resolve
"Monday" against the meeting date), beneficiary, and status. Three sections:

- DEEP OWES: his commitments. Every "I'll", "I will", "let me", "from my end" spoken by Deep.
- OWED TO DEEP: others' commitments, the chase list.
- PENDING CONFIRMATION: facts or inputs someone must confirm before work can finish. Mark dependent
  deliverables as partially blocked, and finish every unblocked part anyway.

### Step 3: Draft every DEEP OWES deliverable

For each commitment, produce the actual artifact: the plan, the document, the reviewed script, the email.
Drafts only, never send anything externally. Ground every claim in the transcript or vault; mark assumptions
with CONFIRM flags rather than inventing specifics. Before relying on an artifact (deck, doc, spreadsheet)
pulled from mail or the vault, open it and confirm it is the current version: filenames and subjects get
reused across rounds, so an attachment that matches by name can be an earlier iteration. Verify by content
(dates, figures, named initiatives), not by filename, and name the version you verified when recommending
it for send. Apply standing rules: no em dashes ever, no section-number
tags, correct entity names, Lake B2B vs SPAN client separation where relevant, and the 360 mode the meeting revealed (`reach`, `modes/champions-growth-profiler/references/champions-360.md`) when it differs from the one it was booked under.

### Step 4: Add the prepared-plus extra

Ask: what will the next meeting need that nobody asked for? Typical winners: an acceptance-criteria table to
judge what the other side is presenting, a one-page recap that reframes the problem, a tracker or template the
team can adopt on the spot. Pick one, build it well.

### Step 5: Run the logistics guard

Check the calendar for every future touchpoint mentioned in the meeting. Missing: flag it at the top of the
report (or draft the invite if calendar write access exists). Existing: confirm Deep is an attendee.

Before creating an ideation booking card, check for an unbooked card for the same working session.
When a later recording adds scope or verifies an invitee, update that card and its prep note instead of
creating a second invite. Mark old invite payloads superseded, recheck availability and duplicates, and
keep private sources out of the invite.

### Step 6: File via meeting-intake

Run the meeting-intake pipeline: vault note in Calendar/Meetings/, tasks into TASKS.md, cross-links. Dedupe
against existing tasks.

### Step 7: Report, glanceably

Deep reads roughly a third of any output, so the report must land in 10 seconds:

```
FOLLOW-UP: [meeting] ([date])
READY: [n] deliverables drafted  -> [filenames]
YOU OWE (next touchpoint [date]): [item] DONE / [item] DRAFTED / [item] BLOCKED on [x]
CHASE: [person]: [item] (due [date])
CALENDAR: [call] scheduled Y/N
CONFIRM: [the one or two inputs needed to unblock]
```

Deliver files via SendUserFile as they are produced. If the desktop vault is reachable, also commit the
vault note.

## Edge cases

- Multiple meetings in one day (sweep mode): one ledger per meeting, one consolidated report, commitments
  merged into a single YOU OWE list sorted by next-touchpoint date.
- A commitment already satisfied by an existing vault artifact: link it, do not rebuild it.
- Meeting with no commitments by Deep: run intake, produce the chase list, skip drafting.
- Sensitive or external-facing drafts (client emails, offers): always drafts, clearly labeled, never sent.
- A "call vs paper" comparison cites the counterparty's newest document per clause, not the first one read.
  List every dated written version first (proposal, draft agreement, MOU), then fill each "in writing"
  cell from the latest one that covers it. A schedule that quoted an 11 Nov "standard or expedited" offer
  as the written position missed that the vendor's own 16 Nov draft had already picked standard and dropped
  the premium, and that its "targets are not a payment condition" clause conflicts with milestone-gated
  advances.
- Superseding your own earlier artifact: in the same run, comment the new path and sha256 on every card
  that still points at the old one (grep open cards for the old filename). Otherwise the downstream lane
  attaches the superseded file.
