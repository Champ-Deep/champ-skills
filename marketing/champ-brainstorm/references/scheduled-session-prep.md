# Scheduled brainstorm / ideation session prep

Deep runs recurring internal ideation sessions: a topic, two or three named invitees, a
half-hour slot, and a decision or a plan to come out of it. He asks for help with "the
brainstorm I am having today with X and Y". This is prep for a session he will run, not a live
ideation with him, so the CHAMP walk in the main file does not apply.

## Procedure

1. **Resolve the session.** Batch in one turn: `search_files` over `Efforts/Active/Ideation/`
   for the invitees' names, and a grep of `TASKS.md` for `[e:Ideation]` plus those names. The
   `TASKS.md` row carries the Wispr link, the proposed slot and any hard-hold note; the ideation
   folder carries the prep note. State in one line which session you resolved to, so a wrong
   read is correctable before anything is built on it. Invitees are the reliable filter: two
   sessions can share a topic and only one has the two people he named.
2. **Read the prep note in full.** It already holds the one question, the options table, what to
   bring, the open questions and the invitees. Do not rewrite it. Close its gaps.
3. **Pull the source record.** The note cites a Wispr meeting id. `notes.wisprflow.ai/shared/...`
   links cannot be read over HTTP: they return a sign-in page carrying placeholder text about an
   unrelated document, which reads as real content and is the trap. Resolve it with
   `mcp__wispr__get_meeting` using that id, `view_transcript` on. The transcript is the source of
   truth; the note's summary is a lossy read of it. Attribute shared notes to the people in them,
   never to Deep.
4. **Check the calendar for the slot.** `mcp__ms365__get_calendar_view` across the day,
   `select` on subject/start/end/attendees, `timezone` set. A "proposed slot" in the note is
   usually unbooked, and an unbooked slot is a fact to report at the top of the reply, not a slot
   to prep around. Say whether the slot collides with what is booked.
5. **Write the sections the note is missing**, in this order:
   - **Numbers from the source meeting**: a table of every figure the session needs, each traced
     to the transcript, including the timing and the allocation decisions already made so the
     session does not re-litigate them.
   - **The arithmetic the session actually hangs on**: reduce the headline number to the number
     that matters (reachable contacts, then the platform's own match rate, then the usable
     audience against its delivery floor). Where a component is a published benchmark rather than
     the account's own data, label it as a benchmark and make reading the real number a step of
     the session.
   - **Run sheet**: a table of minute window, beat, who leads it, what it produces. Every invitee
     gets a lead row. The last row is the decisions.
   - **Decisions to land**: a table, one row per decision, with a recommendation in every row.
     Money and data-consent rows are marked as Deep's to rule on.
6. **Deliver as a `MEDIA:` card** to the note path. In chat, lead with the one crux sentence and
   the decisions, not a replay of the note.

## Always-on

- Do not restart the ideation from zero when a prep note exists. Two competing notes on one
  session is the failure.
- Never invent a figure. Every number carries its source; an unpublished benchmark is labelled
  as one, and the live read of the real number is a session step.
- The session is half an hour. A run sheet whose rows sum past the slot is not a run sheet.
- Ad spend and anything touching data consent or lawful basis are Deep's rows, never the
  session's output.
- Anything the source meeting "floated and dropped" gets checked against the platform's own
  documentation before the session. A dropped item is often a required step, and the correction
  belongs in the note before he walks in.
