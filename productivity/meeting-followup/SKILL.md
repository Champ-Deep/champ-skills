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
- Scheduled sweep: pull all meetings since the last run. get_meeting_assets returns a huge payload; save to
  file and extract with jq (transcript_items, content_markdown), never read raw into context.
- Speaker resolution: "my notes" transcripts label people Speaker 1/2/etc. Identify Deep by voice: he is the
  one coaching, setting strategy, and saying "I'll send you the plan from my end." Verbal tics: "things like
  that", "you know", "incredibly important". If identity is genuinely ambiguous, ask once via AskUserQuestion.
  Normalize mangled names against known people (transcripts garble Indian names constantly).

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
with CONFIRM flags rather than inventing specifics. Apply standing rules: no em dashes ever, no section-number
tags, correct entity names, Lake B2B vs SPAN client separation where relevant.

### Step 4: Add the prepared-plus extra

Ask: what will the next meeting need that nobody asked for? Typical winners: an acceptance-criteria table to
judge what the other side is presenting, a one-page recap that reframes the problem, a tracker or template the
team can adopt on the spot. Pick one, build it well.

### Step 5: Run the logistics guard

Check the calendar for every future touchpoint mentioned in the meeting. Missing: flag it at the top of the
report (or draft the invite if calendar write access exists). Existing: confirm Deep is an attendee.

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
