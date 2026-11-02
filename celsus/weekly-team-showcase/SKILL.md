---
name: weekly-team-showcase
description: "Use when Deep presents a weekly update or demo to his team."
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

Deep says weekly update, team showcase, demo for the team, walk the team through, or present our work. Also use it when a meeting note schedules him to showcase something. Not for client meetings (`meeting-prep`) or his own weekly review (`weekly-review`).

## Output

One vault note: `Efforts/Active/<effort>/<YYYY-MM-DD> Weekly Update - <topic>.md` with frontmatter `type: meeting-prep`, plus a `walkthrough/` folder of live screenshots next to it. Deliver it as a MEDIA card. Sections, in this order:

1. **One line** (what it does, in plain words) and **the ask of the team**.
2. **Pre-flight** table (20 to 30 min before): warm every link, sanity question with its expected answer, credentials to clipboard, files staged on the Desktop, backup screenshots open.
3. **Running order** with minutes: Why (2), What we built (3), Live demo (8), How effective (2), What is next (2), Feedback (3). About 20 minutes total.
4. **Demo click path**: numbered clicks with exact menu labels, and the one sentence to say at each reveal.
5. **Scorecard**: before/after numbers from a run you executed, plus cost per use if known.
6. **What is next**: table of item, owner, status (card ids).
7. **Feedback to collect**: 4 to 5 specific questions that force a choice, never "any thoughts?".
8. **If something goes wrong** table, then **Likely questions** with short answers.

## Procedure

1. Gather what shipped this week from the effort folder, kanban cards (done and open) and the audit or test notes. Name the owner and status of each next step.
2. **Rehearse the exact demo on the live deployment the same day**, scripted end to end (API calls or Playwright). Record the real answers. The scorecard comes only from this run, never from memory or earlier local runs.
3. Screenshot every screen the demo touches (visitor view, login, each admin page) with Playwright into `walkthrough/`. Check them with vision and confirm the menu labels in the click path match what is on screen.
4. Write the run sheet. Use plain words, tables over bullets, and no em dashes.
5. Close with a decision card only if Deep must do something before the meeting (a key, a variable, an approval).
6. After the meeting: run `meeting-followup` on his notes. Feedback becomes kanban cards and gets logged in the effort folder.

## Rules (learned)

- **Never put a password on the shared screen.** Pre-flight copies it with `security find-generic-password -s <service> -a <user> -w | pbcopy`. Scripts read from the keychain and never print it.
- **Serverless or container links sleep.** Cloudflare Containers sleep after the configured idle time and take 2 to 3 minutes to wake. Pre-flight opens every link and asks one known question.
- **Swap demos (bad file vs good file) need a clean slate.** Delete the datasets, show the empty state, and start a **New Chat** after each swap, because thread history leaks the earlier answers. Confirm the app has no query cache that survives a dataset change.
- **Find the destructive controls before the meeting.** Example: Delete sits at the bottom of each dataset card, behind a confirm dialog. If a control the demo needs is not visible, say exactly where it is in the click path.
- **Show the method, not just the answer.** Plan one moment that opens the "how this was calculated" view, so the team sees why to trust it.
- **Headless Playwright on apps that keep a connection open:** use `wait_until="load"` plus a fixed wait. `networkidle` never fires on SSE or polling apps.
- The browser tool (Camofox) is often down. Playwright via `/opt/anaconda3/bin/python3` has Chromium installed.
- Reference run: `Celsus/Efforts/Active/Queryable Chatbot Showcase/2026-11-03 Weekly Update - Team Showcase.md`.
