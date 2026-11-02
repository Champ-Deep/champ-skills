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
3. **Which link runs what data**: one row per link Deep will present: URL, what is loaded at start, the source file it was built from, and where its variables live (Worker var vs secret, with the names). Plus the admin system and login details for each link: the admin URL path, the user, and where the password is stored. Deep asks for exactly this table when he is about to present; build it from a live check, never from memory.
4. **Running order** with minutes: Why (2), What we built (3), Live demo (8), How effective (2), What is next (2), Feedback (3). About 20 minutes total.
5. **Demo click path**: numbered clicks with exact menu labels, and the one sentence to say at each reveal.
6. **Scorecard**: before/after numbers from a run you executed, plus cost per use if known.
7. **What is next**: table of item, owner, status (card ids).
8. **Feedback to collect**: 4 to 5 specific questions that force a choice, never "any thoughts?".
9. **If something goes wrong** table, then **Likely questions** with short answers.

## Procedure

1. Gather what shipped this week from the effort folder, kanban cards (done and open) and the audit or test notes. Name the owner and status of each next step.
2. **Rehearse the exact demo on the live deployment the same day**, scripted end to end (API calls or Playwright). Record the real answers. The scorecard comes only from this run, never from memory or earlier local runs.
3. Screenshot every screen the demo touches (visitor view, login, each admin page) with Playwright into `walkthrough/`. Check them with vision and confirm the menu labels in the click path match what is on screen.
4. Write the run sheet. Use plain words, tables over bullets, and no em dashes.
5. Close with a decision card only if Deep must do something before the meeting (a key, a variable, an approval).
6. After the meeting: run `meeting-followup` on his notes. Feedback becomes kanban cards and gets logged in the effort folder.

## Rules (learned)

- **Confirm the scope of links with Deep before writing the sheet.** He often presents a subset of what was built. The run sheet covers only the links he names; the rest are not mentioned at all.
- **Verify what each link actually runs by querying it live** (catalog/summary API or the admin console), not from deploy notes or seed config. When Deep names one canonical source file, make every showcased edition load it, so the comparison is branding only.
- **Check a data file's provenance before naming its author in the sheet.** Open the file or its git history; a label copied from an earlier note can be wrong, and a wrong name in a doc he presents from costs him credibility in the room.
- **Answer "which link has what data, where are the logins" before he asks.** Ship the data and admin table in the run sheet by default.
- **Never put a password on the shared screen.** Pre-flight copies it with `security find-generic-password -s <service> -a <user> -w | pbcopy`. Scripts read from the keychain and never print it.
- **Serverless or container links sleep.** Cloudflare Containers sleep after the configured idle time and take 2 to 3 minutes to wake. Pre-flight opens every link and asks one known question.
- **Swap demos (bad file vs good file) need a clean slate.** Delete the datasets, show the empty state, and start a **New Chat** after each swap, because thread history leaks the earlier answers. Confirm the app has no query cache that survives a dataset change.
- **Find the destructive controls before the meeting.** Example: Delete sits at the bottom of each dataset card, behind a confirm dialog. If a control the demo needs is not visible, say exactly where it is in the click path.
- **Show the method, not just the answer.** Plan one moment that opens the "how this was calculated" view, so the team sees why to trust it.
- **Headless Playwright on apps that keep a connection open:** use `wait_until="load"` plus a fixed wait. `networkidle` never fires on SSE or polling apps.
- The browser tool (Camofox) is often down. Playwright via `/opt/anaconda3/bin/python3` has Chromium installed.
- Reference run: `Celsus/Efforts/Active/Queryable Chatbot Showcase/2026-11-03 Weekly Update - Team Showcase.md`.
