---
name: weekly-team-showcase
description: "Use when Deep presents to his team: weekly update, demo, run sheet, or decision topic."
version: 1.0.0
author: Champ
license: MIT
metadata:
  hermes:
    tags: [weekly-update, showcase, demo, team, presentation, feedback]
    related_skills: [meeting-prep, meeting-followup, executive-one-pager, celsus-vault, weekly-review-planning]
---

# Weekly Team Showcase

Deep's weekly update is him presenting work to his team: what we built, proof that it works, what is next, and feedback that shapes the next week. The deliverable is a **run sheet** he can present from with no prep beyond the pre-flight list, plus evidence gathered by actually running the thing.

## When to Use

Deep says weekly update, team showcase, demo for the team, walk the team through, or present our work. Also use it for a per-person run sheet he wants to send the team (one page, what each person owns this week), and when a meeting note schedules him to showcase something. Not for client meetings (`meeting-prep`) or his own weekly review (`weekly-review`).

Three deliverables exist under this skill. Pick by what Deep asks for.

### A. Demo showcase run sheet (he presents our work)

One vault note: `Efforts/Active/<effort>/<YYYY-MM-DD> Weekly Update - <topic>.md` with frontmatter `type: meeting-prep`, plus a `walkthrough/` folder of live screenshots next to it. Deliver it as a MEDIA card. Sections, in this order:

1. **One line** (what it does, in plain words) and **the ask of the team**.
2. **Pre-flight** table (20 to 30 min before): warm every link, sanity question with its expected answer, credentials to clipboard, files staged on the Desktop, backup screenshots open.
3. **Which link runs what data**: one row per link Deep will present: URL, what is loaded at start, the source file it was built from, and where its variables live (Worker var vs secret, with the names). Plus the admin system and login details for each link: the admin URL path, the user, and where the password is stored. Deep asks for exactly this table when he is about to present; build it from a live check, never from memory.
4. **Running order** with minutes: Why (2), What we built (3), Live demo (8), How effective (2), What is next (2), Feedback (3). About 20 minutes total.
5. **Demo click path**: numbered clicks with exact menu labels, and the one sentence to say at each reveal.
6. **Scorecard**: before/after numbers from a run you executed, plus cost per use if known.
7. **What is next**: table of item, owner, status (card ids).
8. **Feedback to collect**: 4 to 5 specific questions that force a choice, never "any thoughts?".
9. **If something goes wrong** table, then **Likely questions** with short answers.

### B. Team status run sheet (he sends the team one shared list)

He names a set of people and wants one page they can all work from: what moved last week, what each owns this week. No demo, no rehearsal.

Two files, kept apart:

| File | Audience | Location |
|---|---|---|
| `YYYY-MM-DD - <team> Weekly Run Sheet.html` | sent to the team | `Calendar/Meetings/` |
| `YYYY-MM-DD - <team> Weekly Script (private).md` | Deep only, never shared | same folder, name ends `(private)` |

The HTML carries the shared list, then one card per person: **Last week** with each line tagged, and **This week** as a Focus/By table. Put the unowned cross-team items in one card at the top so the meeting picks an owner for them. Close the page with a reply-by deadline: no reply means the card stands.

Three tags only: `Done` (finished and on record), `Open` (carried over), `Confirm` (no written update, tell us where it stands). A person with nothing filed last week gets a Confirm card listing their oldest open items, not a blank card.

The private script holds the run of show: a one-paragraph opening line, 2 to 3 minutes per person in a fixed order, the shared-item picks, a read-back close, and a **Do not say** block (no credential values, no purchase or volume commitments beyond what is verified, no performance comments). Order the round so Deep speaks first to set the pace.

### C. Decision showcase (he presents topics and calls in a standing meeting)

Deep brings learning, a strategy or a proposal into a recurring meeting (the weekly marketing meeting, a brand call) and wants the team to reach decisions on it. No live product to demo, so deliverables A's click path and scorecard do not apply; the currency is a set of called decisions with owners and dates.

One private vault note, same filename pattern as A, plus a companion spec note when a topic is a workflow to adopt (for example a loop that runs after every closed deal). This pack is for Deep: it carries the do-not-say list and internal conflicts, so deliver as MEDIA to him, never to the team channel.

Build it in this order:

1. **Map the topics onto the meeting's own agenda first.** Read the meeting operating system note (segments, minutes, hard stop) and give every topic a slot and a minute count that sums inside the existing budget. Never impose a standalone running order on a meeting that already has a published shape; the sheet says which segment each item rides in, and it folds any earlier plan (a walkthrough, a demo) into the nearest segment instead of adding time.
2. **Per topic, one block:** a one-line summary in plain words, the line Deep says out loud (a `SAY:` quote he can read verbatim), the verified facts each with its source, the so-what, the decision, the proposed owner and date. Facts he has not verified go in a separate **Not verified** block at the end, never mixed into the say-it lines.
3. **Paste-ready decision entries** for the meeting's own decision format (Context, Affected, Recommendation, Deadline), one per decision, so Deep drops them in rather than composing in the room.
4. **Pre-flight that opens the live proof**: the one screen that makes the argument real (a report, a dashboard), screenshotted, plus the source for any third-party number, plus a check that the meeting invite exists with the right people on it.
5. **A do-not-say list and a feedback block** (the forcing-choice questions from A), then **If something goes wrong**.

## Procedure

1. Gather what shipped this week from the effort folder, kanban cards (done and open) and the audit or test notes. Name the owner and status of each next step.
2. **Rehearse the exact demo on the live deployment the same day**, scripted end to end (API calls or Playwright). Record the real answers. The scorecard comes only from this run, never from memory or earlier local runs.
3. Screenshot every screen the demo touches (visitor view, login, each admin page) with Playwright into `walkthrough/`. Check them with vision and confirm the menu labels in the click path match what is on screen.
4. Write the run sheet. Use plain words, tables over bullets, and no em dashes. For C there is nothing to rehearse: replace steps 2 and 3 with the evidence pull for each topic (read the source end to end, screenshot the one live report, check the third-party number against its own source).
5. Close with a decision card only if Deep must do something before the meeting (a key, a variable, an approval).
6. After the meeting: run `meeting-followup` on his notes. Feedback becomes kanban cards and gets logged in the effort folder.

## Rules (learned)

- **Confirm the scope of links with Deep before writing the sheet.** He often presents a subset of what was built. The run sheet covers only the links he names; the rest are not mentioned at all.
- **Verify what each link actually runs by querying it live** (catalog/summary API or the admin console), not from deploy notes or seed config. When Deep names one canonical source file, make every showcased edition load it, so the comparison is branding only.
- **Send a fake-path control before believing any probe.** Behind an auth gate a real path and a path that does not exist answer the same code (`401` on APIs, `307` on pages), so a response code proves nothing about whether a page, route or feature exists. Probe a deliberately wrong URL first; if it answers identically, report the surface as unverifiable from outside instead of reading the code as evidence.
- **Blocked behind the gate: say the rehearsal did not happen.** Without credentials, write the sheet with rehearsal, screenshots and scorecard marked as not done, plus a decision card asking for a login or a deploy. Never carry an earlier build's unrun numbers or screenshots into the sheet, and never present merged as deployed.
- **Check a data file's provenance before naming its author in the sheet.** Open the file or its git history; a label copied from an earlier note can be wrong, and a wrong name in a doc he presents from costs him credibility in the room.
- **Answer "which link has what data, where are the logins" before he asks.** Ship the data and admin table in the run sheet by default.
- **Never put a password on the shared screen.** Pre-flight copies it with `security find-generic-password -s <service> -a <user> -w | pbcopy`. Scripts read from the keychain and never print it.
- **Serverless or container links sleep.** Cloudflare Containers sleep after the configured idle time and take 2 to 3 minutes to wake. Pre-flight opens every link and asks one known question.
- **Swap demos (bad file vs good file) need a clean slate.** Delete the datasets, show the empty state, and start a **New Chat** after each swap, because thread history leaks the earlier answers. Confirm the app has no query cache that survives a dataset change.
- **Find the destructive controls before the meeting.** Example: Delete sits at the bottom of each dataset card, behind a confirm dialog. If a control the demo needs is not visible, say exactly where it is in the click path.
- **Show the method, not just the answer.** Plan one moment that opens the "how this was calculated" view, so the team sees why to trust it.
- **Headless Playwright on apps that keep a connection open:** use `wait_until="load"` plus a fixed wait. `networkidle` never fires on SSE or polling apps.
- The browser tool (Camofox) is often down. Playwright via `/opt/anaconda3/bin/python3` has Chromium installed.
- **Evidence first, and a `Confirm` tag where there is none.** Pull each person's last week from meeting notes, email triage, the decision desk and kanban before writing a card. Where nothing is written down, say so on the card and list their oldest open items instead of inventing a status or leaving the card empty. Report to Deep which people had no record; that gap is his signal, not something to paper over.
- **A date nobody agreed to is a proposed date.** Mark it with `*` and put the meaning of `*` in the legend on the page, so a sheet full of my estimates cannot be read as commitments the team made.
- **Name collisions between two people are the highest-risk error on a sheet like this.** When the team holds two similar names (a first name and a same-first-name colleague), state the assumption in one line in the reply to Deep and offer to redo that card. Never silently pick one.
- **State what you actually consumed of a source before Deep repeats it.** If a transcript or audio could not be fetched, the sheet says "I read the description, I did not hear the audio", so a line he speaks as fact carries its own caveat. A source that sells something in the same video (the creator's own tool, course or service) is evidence of the technique only; when we already hold an equivalent capability, the sheet says so instead of recommending the purchase.
- **Cross-check conflicting records in the vault and surface the conflict.** When two notes disagree on who owns what (a brand owner, a function lead), the sheet states the disagreement as an open question for the room. Silently picking one puts a wrong name in front of the team.
- **Employment and performance items never ride in the shared agenda.** They get their own decision card for Deep; the room hears one neutral line ("being settled this week") at most. No notice periods, resignations, appraisal or pay content anywhere in a pack the team can read.
- **Two files, because one of them must not be sent.** Anything with names and status in it gets a private script beside it, named `(private)`, so Deep can tell at a glance which artifact leaves the building.
- **Answer "is there a meeting today" from live Outlook before writing a script.** Check the named group against the calendar view for the week, note cancelled events as cancelled, and say plainly when the slot he implies was staged but never booked. The script then says where it can be used instead of assuming one occasion.
- **"Give me the showcase" means the page he presents from, in the same turn.** Build it from what is already on record and mark unbuilt work as not built on the page. A queued card, a skill update or a plan is not the showcase, and answering with one costs him the meeting.
- **A decision showcase with a screen share ships as two HTML files**: `<date> <topic> (team).html` for the shared screen and `<date> <topic> Script (private).html` for his second screen, with SAY lines, the call to make, the do-not-say list and what was not verified. The team page runs the topics as scroll beats with a running-order rail, minutes per topic that sum to the meeting budget, one decision panel per topic, a read-back table at the end, and left and right arrow keys to step. Keep the source and build script in scratch, and make the build assert every count the copy states (topics, minutes, table rows).
- **Use one scroll offset, not two.** `scroll-padding-top` on `html` and `scroll-margin-top` on the section add together, so a scroll-spy threshold set between them marks no topic as active after a jump. Drive the arrow keys in a browser, with smooth scrolling on and with no gap between presses, before calling the page presentable.
- Reference run: `Celsus/Efforts/Active/Queryable Chatbot Showcase/2026-11-03 Weekly Update - Team Showcase.md`. Two-file decision showcase reference: `Celsus/Efforts/Active/Marketing Showcase 2026-11-11/2026-11-11 Marketing Showcase (team).html`. Decision showcase reference: `Celsus/Efforts/Active/Marketing Showcase 2026-11-11/` (run sheet plus the companion loop spec). Status run sheet reference: `Celsus/Calendar/Meetings/2026-11-10 - Tech Team Weekly Run Sheet.html` with its `(private).md` script.
