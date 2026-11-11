---
name: client-programme-review
description: "Use when a client needs a programme review or report."
version: 1.1.0
author: Champ
license: MIT
metadata:
  hermes:
    tags: [sales, client-report, renewal, showcase, reconciliation]
    related_skills: [showcase-page, client-messaging-simulation, visual-verify, client-call-prep]
---

# Client programme review

## When to Use

- A renewal, upsell or review meeting with a live client, where we show what the programme did and propose what comes next.
- The weekly or monthly report to a client on a running lead generation programme.
- An account owner hands over reports and asks for "the showcase", "the programme review" or "the client report".

Not for a prospect who is not yet a client (`prospect-campaign-plan`, `b2b-growth-showcase`), and not for an anonymised case study (`showcase-page` alone).

A programme review is the page an account owner puts in front of a live client: what we ran, what came back, what it taught us, what we need from them, and the tiers for what comes next. The same build serves the weekly and monthly report. The client can check most of it against their own records, so the work starts with reconciliation, not design. One wrong count costs more trust than a plain page costs attention.

What it produces: a reconciled ledger of every client-facing figure, the showcase page (universe, messaging, simulation, lead board with win profile, lessons, asks, tiers), and an internal call script.

The skill is self-contained: the page engine, the showcase kit it runs on and a fictional sample client are in `engine/`. These help when they are installed and are not required: `showcase-page` (the full design rules), the brand skill, `visual-verify`. The simulation step needs `client-messaging-simulation` and its tool, which runs on Deep's desk only; without a run the page hides that section.

House rules for every build: never invent a number. Never name an outside delivery partner: it is "our team". No prices unless the owner asks for them. No em or en dashes anywhere, including the PDF. The real logo from the kit, never a drawn one. Look at the built page before calling it done.

This repo is public. Nothing client-specific goes into this skill: no client name, figure, lead list or copy. Client builds live with the client's material (for Deep: the vault).

## Order of work

1. Intake: get the records from the account owner.
2. Ledger: one entry per client-facing figure.
3. Reconcile: work every open entry out with the owner.
4. Simulation.
5. Build.
6. Verify.
7. Call script.
8. After the call, and the weekly or monthly cadence.

Steps 1 to 3 finish before any design work. A beautiful draft creates pressure to ship numbers nobody confirmed.

## 1. Intake

Ask the owner for all of this in one batch, and say why each is needed:

| Record | Used for |
|---|---|
| The client's own lead sheet or tracker | Every count, company, date and status is matched to it |
| Our delivery record, lead by lead, with the qualification answers | The detail on each lead card |
| Send reports per send, the copy as sent, and the order it went out | The messaging section and the simulation |
| Calling reports, with the period each one covers | Reach figures |
| The order: contracted volume and what counts as a lead | Status against the order |
| The last mail or recap to the client that states a count | What the client has already been told |
| Any hold on figures: a dispute, a reconciliation in progress, a pricing question | What must not appear |
| What the client has said about outcomes | Which leads to mark as theirs |

When the client's sheet sits behind their sign-in, ask the owner to paste the rows. Do not wait on access, and do not build on our record alone.

## 2. Ledger

`ledger.json` sits beside the build. `scripts/ledger.py` checks it (`python3 ledger.py --selftest` proves the checker). Every figure or claim the client will read is one entry:

```json
{"id": "leads_delivered", "claim": "12 leads delivered", "shown": "12 leads delivered",
 "source": "client lead sheet, rows pasted by the owner", "as_of": "2026-01-15",
 "status": "matched", "by": "client lead sheet, compared company by company", "client_can_check": true}
```

| Status | Meaning | Needs |
|---|---|---|
| `matched` | Checked against the client's own record | `by`: the record |
| `owner` | The account owner confirmed it in this build | `by`: who and when |
| `sourced` | Traced to one of our dated files | Not allowed when `client_can_check` is true |
| `caveated` | Unconfirmed, and the page says so | `caveat`: the exact words, which must be on the page |
| `cut` | Removed | `shown` must no longer be on the page |
| `open` | Unresolved | Blocks a final build |

Rules:

- Anything the client can check themselves (counts, names, dates, contract terms, what they told us) is `matched`, `owner` or `caveated`. Our file alone is not enough, because theirs is the one they will open.
- `shown` is the figure exactly as printed. The gate fails when page and ledger drift apart, so a late copy edit cannot slip a number past the check.
- A figure that comes from a call recap, a chat summary or memory is `open` until a person or a record confirms it. Recaps misstate numbers.
- An assumption that joins two records is its own entry: which copy went with which send, which week a report covers.
- Internal-only facts never get a `shown`: delivery partner names, our costs, prices, internal disputes.

## 3. Reconcile with the owner

The discrepancy classes, with the question to ask for each, are in `references/reconciliation.md`.

- Diff our record against the client's row by row and print the diff: count, set membership, dates, titles. A matching total can hide a different set.
- The client's record wins on anything the client can see. Correct ours to theirs and tell the owner what changed.
- Bring every open entry to the owner in one batch of questions (the question tool where there is one). Each question states both values and where each came from, with the recommended option first. The options are always some of: use theirs, confirm ours, soften with a caveat, cut, leave open.
- When the owner is fairly sure but not certain, do not hard-code it. Caveat it on the page and, where it is cheap, let the reader change it there (the copy-to-send selector is the pattern).
- Reread the story against every confirmed fact. When the client names their best leads, recompute the profile and check each lesson and the closing line against it. A lesson the client's own picks contradict is a discrepancy, the same as a wrong count.
- A second round is only for facts the first answers raised. Whatever stays unanswered stays `open`.
- `make.py` builds a draft with a red ribbon naming the open figures. `make.py --final` refuses to build while anything is open or the page and ledger disagree. Only a final build is shared, exported or put on screen.

## 4. Simulation

Run it with `client-messaging-simulation` on the copy as it was actually sent. Where that tool is not available (a team Claude account), skip the run: with `SIM_RUN = None` the section hides itself. When the page needs one, ask Deep's desk for a run file, set `SIM_RUN` to its path, and put the hand-written `sim_notes.json` beside `client.py`.

- On the page it is the "<Brand> simulation" (for example "LakeB2B simulation") and its rewrite is the "<Brand> rewrite". The tool name and the model name never appear.
- Put the real result beside the simulated one for every message that was sent, and say plainly where they disagree.
- State how many personas returned a scored reaction out of how many were asked.
- Keep the disclaimer: a simulation picks which messages deserve a test, it never replaces the test.

## 5. Build

The engine builds the page from one file per client. The skill folder may be read-only, so copy the engine out first:

```bash
cp -R <skill>/engine ./pr && cp -R <skill>/scripts ./scripts   # make.py reads ../scripts/ledger.py
chmod -R u+w pr scripts                                          # a copy of a read-only folder is read-only
cp -R pr/sample pr/<client>                                      # every client starts from the sample
# edit pr/<client>/client.py and pr/<client>/ledger.json
python3 pr/make.py pr/<client>            # draft, red ribbon while the ledger has an open entry
python3 pr/make.py pr/<client> --final    # refuses until the ledger is clean
```

`client.py` is the only file that changes per client: the lead table, sends, calls, the leads the client named, the config for filters and lead cards, and every sentence of copy. Numbers in the copy are computed from the tables, never typed twice. Do not edit `review.tpl.html`, `review.css` or the kit for one client: a change there is a change for every client, and needs the probe rerun on the sample in all three modes. `PR_MODE=review|monthly|weekly` (or the `SECTIONS` list in `client.py`) picks the sections. The output is `pr/<client>/dist/<slug>.html`, one self-contained file, with the data it was built from beside it.

Sections, what each must prove, and the widget contract for each are in `references/sections.md`.

| Section | Review | Monthly | Weekly |
|---|---|---|---|
| Hero and three stat cards: status against the order | yes | yes | yes |
| The universe: how much of the market has been touched | yes | yes | no |
| What we ran: dated changes, and the reports the client received | yes | since the last report | this week |
| The messaging: each send, its copy and its result | yes | yes | this week's sends |
| Simulation | yes | when there is new copy | no |
| Lead board and win profile | yes | yes | new leads only |
| What we learned | six lessons | three | one |
| What we need: the closed loop, the tick list, the send-back note | yes | yes | yes |
| Win profile study and where the audience gathers | yes | no | no |
| Tiers, with the case for each | renewal or upsell only | no | no |
| Closing line and next step | yes | yes | yes |

Interaction rules:

- The client marks, we do not guess. The lead board opens empty. Pre-mark only leads the client has already named, labelled as theirs with the date. A shortlist of ours frames the conversation around our guess, and the guess can be wrong.
- The win profile panel separates "no pattern" from "not on record". Missing data reported as no pattern hides the question we should be asking.
- Every mark the reader makes (leads, order, ticks, tier, pairing) is kept in their browser and nothing is sent. The send-back note turns the marks into text they can copy. A default selection is never reported as the reader's choice.
- Where the audience gathers is a drag-and-swap bento: a vanilla port of 21st.dev Draggable Grid Dashboard (id 30238). Slots keep their size and rank, tiles swap. Arrow keys on the handle reorder, and touch drags from the handle only so the page still scrolls.
- Lessons compute their numbers from the data table. A lesson states the evidence, shows it as bars, and ends with what changes next.
- Tiers carry no prices. Each tier includes the one before it, and the case for the top tier is made from the programme's own numbers.

## 6. Verify

1. `python3 pr/make.py pr/<client> --final` exits 0: no open entries, every caveat on the page, every `shown` present.
2. `python3 pr/probe.py pr/<client>` drives every control in a real browser and asserts the result: the board opens on the named leads or empty, holds three, filters; the bento swaps by keyboard and by mouse and resets; the pairing swap moves the real click rates; marks survive a reload; a fresh visitor sees no claimed choices; zero console errors. It needs Playwright with Chromium. Where there is no browser (most team Claude sessions), say so in the handoff: the engine's controls were proven on the sample and only the data changed, but this build was not re-driven. Never report the probe as run when it was not.
3. `python3 pr/kit/shoot.py "<slug>"` writes 1440 and 390 screenshots when a browser is available: no overflow, no small targets, and the screenshots read (`visual-verify`).
4. Search the built page and the PDF text for the tool name, partner names, prices and dashes.
5. Copy to the delivery folder and assert the SHA-256 matches the audited build.

## 7. Call script

An internal page for the presenter, never shared and marked so.

- Timed to the invite length, block by block, following the page's sections.
- Attendees and responses come from the live calendar invite, not from memory.
- Each block has the click to make, the lines to say, and fallback lines for the likely pushback.
- A "decide before the call" list and a "get from the team" list sit at the top.
- A do-not-say list is built from the internal-only facts found during reconciliation.
- Anything unknown is a visible placeholder to fill, never a guess.

## 8. After the call, and the cadence

- Record what the client said as ledger entries with status `owner`, set the named leads, rebuild final and re-export.
- The client's named leads become the brief for the win profile study.
- For the next weekly or monthly report, reuse the build. Re-date every entry, and re-match every `client_can_check` entry against the client's record for the new period. Last period's match does not carry over.

## Pitfalls

- A class that sets `display` beats the `hidden` attribute. Add `[hidden]{display:none}` for any styled control you hide, and assert the computed display in the probe, not the property.
- Moving a node in the DOM drops its pointer capture. During a drag, listen on `document`, leave the dragged tile where it is, and move the other tile.
- Compare page text with whitespace removed. Markup inside a phrase otherwise hides it from a text check.
- A hero tile twice the height of its neighbours needs a larger title, or it reads as empty.
- `pdftotext` is not always installed. Read the PDF with `pypdf` under `uv run --with pypdf`.

## Files

- `engine/make.py`, `engine/probe.py`, `engine/review.tpl.html`, `engine/review.css`: the page engine. Client-neutral: everything specific comes from `client.py`.
- `engine/kit/`: the showcase kit the engine builds on, with the LakeB2B logos.
- `engine/sample/`: a fictional client (`client.py`, `ledger.json`) that builds and passes the probe in all three modes. Its comments are the guide to the file.
- `scripts/ledger.py`: the gate (`python3 ledger.py --selftest`).
- `scripts/package.py`: writes the zip for a Claude account, with the fuller description that account needs. Run it after every change to this skill and upload the zip again.
- `templates/ledger.sample.json`: a fictional ledger showing every status, including `open` and `cut`.
- `references/reconciliation.md`: discrepancy classes and the question for each.
- `references/sections.md`: section catalogue, widget contracts, the `client.py` contract.
- A real, private build that the engine reproduces exactly sits in Deep's vault (`Other/Skills/client-programme-review/REFERENCE.md`). It is not needed to use this skill and never enters this repo.
