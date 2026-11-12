<!-- Mode file, formerly the standalone skill `send-kit`. Relative paths below resolve from modes/send-kit/. -->

# Send Kit

Assemble the "send kit" for one or more external meetings: everything Sreedeep (Deep) needs to fire off the documentation follow-up in one action. A kit is NOT a status report; it is a staged, ready-to-send package.

## What a send kit contains (per external meeting)

1. **Ready-to-paste email body.** Cleaned for sending: NO Obsidian wikilinks, NO em dashes (hard rule), no placeholders left unfilled unless flagged in the status line. Warm tone, matched to deal stage, never harder-sell than the client signaled.
2. **Attachments list with vault paths.** Every document committed on the call (proposals, MOUs, one-pagers, decks) with its exact path under `Atlas/Clients/{name}/`. If a committed doc does not exist, build it (exec one-pager via the `executive-one-pager` skill, house standard at `Atlas/Context Docs/Design/Warm Editorial Design Language.md`, mobile-first).
3. **To / Subject lines** filled in from meeting records.
4. **Status classification**, exactly one of: READY (send now), CONDITIONAL (name the single input it waits on), CANNOT BUILD (needs Deep's 5-min outcome dump; say so plainly), NOT DEEP'S TO SEND (name the owner).

## Sources, in order

1. `Atlas/Zoom Triage/YYYY-MM-DD.md` daily notes and `Atlas/Zoom Triage/Drafts/YYYY-MM-DD/` folders (produced by zoom-meeting-followup-sweep). Reuse existing drafts; do not rebuild what exists, clean and package it.
2. The latest `Atlas/Zoom Triage/Weekly Follow-Up Review *.md` for owed items and carry-forwards.
3. `Atlas/Clients/{name}/` for committed documents and account context.
4. Zoom MCP (`search_meetings`, `get_recording_resource` with types=summary,nextStep) only to fill gaps. On 403, fall back to `get_meeting_assets` transcript, then to vault notes, marking "summary inaccessible". Never abort over one meeting.

## Output

Write ONE consolidated note: `Atlas/Zoom Triage/Send Kits YYYY-MM-DD.md`, following the format of the 2026-08-06 edition:

- Frontmatter: tags [meeting, send-kit], window, related [[Zoom Triage MOC]].
- Scoreboard table: counts of READY / CONDITIONAL / CANNOT BUILD / NOT DEEP'S.
- P0 and overdue kits first, with FULL cleaned email body inline.
- Remaining READY kits: To, Subject, wikilink to the draft file, one-line note on anything also owed.
- CONDITIONAL, CANNOT BUILD, and NOT DEEP'S as compact tables.
- Link the note from [[Zoom Triage MOC]].

READY kits are picked up by the daily 6 PM draft-dispatch task and staged as Outlook drafts. Note this at the top of the file so the pipeline is visible.

## Hard rules

- Drafts only. NEVER send anything.
- No em dashes anywhere.
- Terminology: keep each brand's spelling consistent. Scheduler link: <your-scheduler-link>.
- Fill in brand pairs that must never appear in the same client's materials.
- Routing: fill in a table of industry, destination brand, owner role, and mailbox (you@example.com). Leave the live roster out of this public skill.
- Exclude the internal recurring meetings and solo notes sessions you list here.
- Output must be 10-second glanceable; Deep reads ~35% of output, front-load P0s.

