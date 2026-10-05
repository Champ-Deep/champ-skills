---
name: intern-month-plan-dashboards
description: "Per-intern month dashboards, handover emails and 1:1 agenda."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [interns, people-os, dashboards, cadence, kpi]
    related_skills: [intern-onboarding-planner, frontend-design, visual-verify]
---

# Per-Intern Month Plan Dashboards

The monthly process behind a standing intern cohort: every intern gets their own private dashboard, their own handover email, and a 1:1 with a fixed agenda. Used for Champions Accelerator. Built once in Oct 2026 and rerun each month.

## When to Use

Trigger on: monthly plan for the interns, send the October plans out, per-person dashboards, KRA handoff, intern cadence, monthly intern process, run sheet for one-on-ones.

Do not use for a new joiner's first month: that is `intern-onboarding-planner`, which starts from a resume and a role brief. This skill starts from plans that already exist and covers distribution plus the operating rhythm for a cohort.

## The failure this exists to fix

September 2026: from 16 Sep onward the vault held almost no evidence of what anyone shipped. Every check-in that mattered went unrecorded. Not because people were idle, but because progress depended on Deep remembering to ask. The fix is structural, not motivational: the dashboard is the record, and the dashboard is the artifact the intern opens daily.

## Inputs

1. One combined team run sheet HTML holding a `PEOPLE` array. This is the single source of truth. Each person: `id, name, role, pod, senior, goal, skill, reviewer, kra[], arc[], monthly[], handoffs[], weeks{w1..w5}{deliverable, checkpoint, days{"MM-DD":[tasks]}}`.
2. Per-person plan notes in the vault (`Efforts/Active/<Team> <Month>/October Plan - <Name>.md`).
3. Per-person KRA sheets (`Efforts/Active/<Team> KRAs <Quarter>/`).
4. What Deep owes each person, pulled from the hub note's open-decisions list.

Do not re-derive plan content from scratch. It exists. Extend, do not rewrite.

## Step 1: Build the dashboards

`build-person-dashboards.js` extracts the published CSS and the `PEOPLE` array from the combined run sheet, then emits one standalone self-contained HTML per person. Reusing the CSS verbatim is the point: the individual pages must be siblings of the combined page Deep already published, not a redesign.

The script is parameterised by env vars for reruns in a later month:

```
RUNSHEET=<path to combined.html> OUTDIR=<output dir> node build-person-dashboards.js
```

Per-person output adds, beyond the combined page:

- **Today panel first**, resolving the real date, with one-tap standup and ship-note copy blocks
- **Month map**, one cell per working day, coloured by state, clickable to jump to that day
- **Health chip**, never grading the first three working days (a red BEHIND on day one is a bug, not a report)
- **"What Champ owes you" panel**, the items on their plan that are not theirs to close. This is what stops the plan reading as one-directional blame.
- **Cadence panel**: daily standup, twice-weekly check-ins, Friday three-liner, weekly deliverable, mid-month checkpoint, month review
- Per-person localStorage key, so eight people can use eight copies of the same page

## Step 2: Handover emails

One per intern, in `handover/October Plan Handover Emails.md`. Never a group mail.

Every email carries four things: the dashboard link, the one thing that must move this week, the cadence they now live by, and **what Deep owes them**. The last one is non-negotiable. Every intern on this roster is waiting on something from Deep (keys, a signature, a leave approval, a decision). An email that only assigns work reads as management and gets quietly ignored.

Two emails are not really drafts until a decision exists (Jrenoth's carries a KRA signature, Alfiya's carries an offer decision). Flag them as such.

Voice: Deep's register. Direct, no filler, acknowledges his own failures by name (Viresh waited three weeks for a plan; that sentence belongs in the email). No em dashes anywhere.

## Step 3: The 1:1 run sheet

`handover/One-on-One Run Sheet.md`. Five identical questions for everyone, so nobody receives a softer or harder version:

1. What did you ship last week, and where is the evidence?
2. What will slip this week, and what would unblock it?
3. Do you have everything you need from me? Name it now if not.
4. Is your Friday note written, and is the vault the record?
5. One thing you want off your plate.

Question 3 is the only one where Deep can unblock something the same day. Per-person length varies by what is owed: 25 minutes for a routine check-in, 35 where signatures or blocker lists are on the table.

## Step 4: The per-person pack (distribution form)

Dashboards plus emails is not a thing Deep can hand over. He needs one reference area per intern with everything in it, so the request "give me the plans to send out" resolves to eight folders rather than a folder tree he has to know.

`build-packs.js` emits `handover/packs/<person-id>/`, four files each:

| File | What it is |
|---|---|
| `README.md` | The reference area. KRA with weights, October plan, every-day and every-week rhythm, month-end checklist, handoffs table, the conversation, and how to send. Links the KRA sheet and plan note by name |
| `email.txt` | The draft, copied verbatim from the split emails so there is one copy, not two |
| `conversation.md` | The 45-minute first sit-down: opening line, 5-question agenda, "what I owe them" as unchecked boxes, the close |
| `accelerator-oct-2026-<id>.html` | Copied from `dashboards/`, never re-rendered |

Plus `handover/packs/README.md` as the index across all eight, carrying the send-order and the not-yet-sendable flags.

The pack copies the dashboard rather than rendering its own. One renderer means the pack version cannot drift from the `dashboards/` version.

Per-person conversation content is the part that must be authored, not generated. Each intern gets an opening line and an agenda built from what Deep actually owes them and what is actually at stake. Identical questions across the cohort is right for a recurring check-in (Step 3) and wrong for a first sit-down.

**Regeneration order matters:** `build-person-dashboards.js` then `build-packs.js`. The pack build throws if a dashboard is missing rather than silently shipping an empty folder.

## Editing the plans when new work arrives

New scope from a call changes three artifacts, and missing any one leaves an intern reading a plan that contradicts the conversation.

1. The combined run sheet `PEOPLE` entry: `goal`, `skill`, and the `kra[]` weights must still sum to 100. Add a new KRA row rather than growing an existing one past its weight.
2. `weeks{w}.days` entries, so the new work lands on a named day and not only in the KRA prose.
3. The email in `handover/emails/`, then re-run the pack build.

`daily[]` and `weekly[]` are optional per person but are what makes a plan concrete. When a plan feels vague, that is usually the missing array, not a wording problem.

Re-verify KRA weights sum to 100 after every edit, by parsing `PEOPLE` rather than reading it.

## The month map must be a real calendar

An earlier build laid the map out as five columns, one per working week, and padded short weeks with cells labelled "holiday". That is wrong twice over: it hid Saturdays and Sundays entirely, and it labelled padding as "holiday" so a reader saw 5 Oct as a holiday when it is an ordinary Monday. Deep caught it: *"why is the 5th a holiday?"*

Rules for any month map:

1. **Walk the real calendar, not the `WEEKS` array.** `WEEKS` only contains working days, so it has no weekends to render. Iterate 1..N and derive each day's weekday.
2. **Three distinct day states, never two.** `working` (clickable, has tasks), `public holiday` (named, tinted, costs a working day), `weekend` (dashed, muted, says Sat or Sun). A fourth, `no plan`, is a working day the plan has not filled yet.
3. **Pad the first row with empty cells** when the month does not start on Monday. October 2026 starts Thursday, so Mon-Wed of row 1 are blank. Without this, 1 Oct renders under MON.
4. **The header row must have exactly as many children as grid columns.** An extra spacer cell in a `repeat(7, ...)` grid pushes SUN onto a second row. This passed a DOM count assertion and still rendered wrong; the screenshot caught it.
5. **Derive the working-day count, never hand-count it.** `weekdays - public holidays`. 22 - 3 = 19 for October 2026. If a holiday is added or removed the number follows.
6. **Today is a ring, not a fill,** so it stays visible on a day that is also a holiday or weekend.
7. **Demo Day markers need a `data-` attribute that the JS actually sets.** The CSS defined `.cell[data-state="demo"]` and the legend promised `*`, but no code ever assigned that state, so the asterisk never appeared. A legend entry with no renderer behind it is a silent lie.

Verify with a weekday-column assertion: for every cell, `column index == real weekday of that date in that month`. Compare with Python's `datetime`, not with the same helper the generator uses, or a shared bug passes twice. Then screenshot it and look, because column alignment is a visual property.

## Space utilization: no collapsed walls

Deep's rule, and it is a rule not a preference: *when most of the accordions aren't going to be expanded, most of the page is left blank and empty. That's never ideal.*

The October build violated it. Five week panels, only the current week open on load, so **2,400 of the page's 4,682px sat hidden behind four bare summary bars**. It rendered without error and passed every assertion in the gate; it simply looked like an empty page with five headings.

Rules:

1. **All week panels render open by default.** They stay `<details>` so the intern can close the weeks they are not working in. Never one-open-rest-collapsed.
2. **Measure the hidden ratio, do not eyeball it.** `hidden / (hidden + visible)` across every `<details>` body. Must stay under about a third. Print the number at verification.
3. Opening everything cost only a few hundred px, because the space was already allocated. Height was never the real constraint; perceived emptiness was.
4. Collapsed-by-default is allowed only where the collapsed state is still worth looking at, meaning it carries a real one-line summary the reader can act on.

## The pack gate exists because a JS typo is invisible

`build-packs.js` shipped `First sit-down: undefined` and `October Plan - undefined.md` into all 8 packs for several hours. Cause: it read `p.first` where the parsed field is `p.name`. Nothing threw, so nothing flagged it.

`pack_check.py` asserts the words, not just the exit code. It caught four classes at once: the wrong field name, the literal string `he or she` from a template never filled per person, duplicate agenda items, and lowercase names in the combined email note.

**Prove a new assertion fails before trusting it.** Seed the bug, rerun, confirm the gate exits 1. The first version of this gate searched for the literal word `undefined` while the real bug emitted the bare expression `p.first`, so it passed a knowingly broken build. A gate that has never been seen to fail is not a gate.

Generalise the check: look for code fragments (`\bp\.\w+`, `{{...}}`, `<%...%>`) rather than a fixed list of placeholder words, because a generator bug leaks as whatever the bad expression was.

Keep the combined email note generated, never hand-edited: `build-combined-emails.js` rebuilds it from the 8 split drafts in `emails/`, so it cannot drift from what actually gets pasted into a mail. A hand-splice of that file once duplicated a section and, when retrying, truncated the whole file to 0 bytes.

## Regeneration order

`build-person-dashboards.js`, then `build-packs.js`, then `build-combined-emails.js`. Then `verify.py` and `pack_check.py`. The pack build throws if a dashboard is missing rather than silently shipping an empty folder.

## Adding someone to the roster mid-month

Adding a person is four edits, and the count guard will catch you if you miss the generator side. `build-combined-emails.js` refuses to run on anything other than the expected count, which is the right behaviour: it failed loudly on 9 drafts when it expected 8.

1. **Run sheet `PEOPLE`**: add the entry with all fields, then assert `kra` weights sum to 100 and every `weeks{w}.days` key set matches the calendar exactly. Getting the week keys wrong is silent, so assert them against a hardcoded date list per week, not against `WEEKS.length`.
2. **`build-packs.js` `ORDER`**: add `{ n, id, first }`. Then add a `CONVOS[id]`, an `OWES[id]` and a `SEND_NOTE[id]`, or the pack builds with empty sections.
3. **`pack_check.py` `NAMES`**: add the id. Every count in that file derives from `len(NAMES)` on purpose: hardcoded 8s meant the gate had to be edited twice the same day. Derive them.
4. **`build-combined-emails.js`**: bump the expected count.

Two traps worth naming:

- **A KRA row written as two arrays parses without error.** `[["Name",45,[...]], ["Name",35,[...]]]` inside `kra:[...]` reads as a nested row of length 4 rather than a length-3 row, and the KPI renderer silently drops half of it. Assert `k.length === 3` for every KRA row, not just that the weights sum to 100.
- **Do not map weeks by feel.** October's weeks are w1 = 1 to 2 Oct (1 working day, 2 Oct is a holiday), w2 = 5 to 9, w3 = 12 to 16, w4 = 21 to 23 (19 and 20 are holidays), w5 = 26 to 30. A first draft put a new joiner's LMS audit on 19 and 20 Oct, which are Ayudha Puja and Vijayadashami.

When one surface moves between two people, update all five places or the two will each plan work the other is doing: the run sheet entry, the person's KRA sheet, their plan note, their email draft, and the other person's sheet. Say the handover in writing in both emails and name the date.

## Verify (mandatory)

`verify.py` (Playwright + chromium, both verified working on this machine) for the dashboards, and `pack_check.py` for the packs, emails and combined note:

1. `node --check` on the extracted script for every file
2. Zero em and en dashes across all output
3. First-screen test at 1440: Today panel and month map both above the fold
4. Today resolver at a pre-start, mid-plan, holiday, weekend and post-plan date
5. Tick a task, confirm it lands in localStorage
7. **Zero console errors**
8. **Zero horizontal overflow at 390** and **zero clipped text** (scrollWidth/scrollHeight vs clientWidth/clientHeight)
9. `node --check` on both generators, then run them and confirm all eight appear
10. Zero em and en dashes across `packs/` including `.md` and `.txt`, not just the HTML
11. Assert each person's KRA weights sum to 100, parsed from `PEOPLE`
12. Month-map calendar assertion: 31 cells, header equals Mon-Sun, and every cell's grid column matches its real weekday. Derive the expected weekday in Python, never with the generator's own helper.
13. **Space utilization: hidden content under collapsed sections stays under a third of the page.** See the section below.
14. `pack_check.py`: zero template leakage in any pack prose. See the section below.

A screenshot read can produce false alarms, and the reverse is worse: month-map tiles legitimately end in an ellipsis, and content below the fold is not clipped. Confirm a suspected clip against the gate's `clipped` counter. But a screenshot also catches things DOM assertions cannot, such as a grid child count that is correct in isolation and wrong once an extra cell shifts the row. Read the screenshot every time.

Checks 6 and 7 are the ones that catch real defects. In the first build they caught an unescaped apostrophe that broke every file, a `let t = clean(t)` shadowing bug, a day-one BEHIND chip, and mid-word ellipses in the month map. Add new assertions as defects appear rather than trusting the visual once.

Then read a 1440 screenshot with the Read tool and apply the five-second test: state what the intern should do today and when the next deliverable is. If you cannot from the screenshot alone, the layout failed.

## Deep's own cross-team view (not the intern's view)

The per-intern dashboard answers "what do I do today". Deep needs the inverse: "what are all eight doing, how do they connect, and what am I holding up". That is a different artifact with a different job, built by `build-team-dashboard.js` (gate: `team_dashboard_gate.py`).

Shape that worked: **Deep's lanes first** (the four things only he can move), then people by pod, then a dependency map, then a single "what I owe" panel.

1. **Lead with his own lanes, not with the intern cards.** The page has to answer his day, with the team inside it. Intern-first buries the only part nobody else can do.
2. **The dependency map is the part with no existing source.** Every intern has a plan; the links between them live only in the hub note. Extract them explicitly as an edge list (`{a, b, label, critical}`) or the page is just eight task lists side by side, which is what the per-intern dashboards already are.
3. **Pair the owes with the owes.** Each card carries "what I owe <them>" from `packs/<id>/conversation.md`, so a glance shows both directions of the same debt. This is what makes the page useful for maintenance rather than just visibility.
4. **Read `WHAT YOU OWE` out of the packs, never re-derive it.** `sed -n '18,40p' packs/<id>/conversation.md` per person returns all eight in one batch. A regex like `(?is)(what i owe.*)` grabs the heading and nothing else, because the section starts with a one-line instruction and the items are a markdown checkbox list, not prose.

## Pitfalls

- **Do not let a generated page hardcode a scratch path for its CSS.** The builders live in the vault and must survive next month, so read the published CSS straight out of the run sheet (`src.split("\n").slice(3,144)`) instead of `/Users/deep/.hermes/cache/scratch/published.css`. A scratch path makes the vault copy fail on rerun with `ENAMETOOLONG`, because a later `fs.readFileSync(CSS)` treats the CSS *string* as a filename. Keep CSS as content end to end.
- **A gate check can pass while measuring nothing.** `s.count(chr(39)+'s critical link'+chr(39))` printed `got 0` and still passed, because the needle did not match the text it claimed to count. Any check whose expected value and needle disagree should be printed and read, not just asserted. Prove each new assertion fails on a seeded copy before trusting it.
- **Never slice the `PEOPLE` array with a bracket or quote counter.** Apostrophes inside task strings (`"reps' hands"`) and brackets inside them make every such scanner truncate silently or throw on a valid file. Slice between `const PEOPLE = [` and the `/* ---------- state ---------- */` comment, then `new Function("return " + body)`. This cost two debug cycles in Oct 2026.
- **A trailing comma can leave an array unclosed and still look correct in the diff.** `["Team",10,[...]],` on the last KRA row closes the inner list and the row but not the `kra:[` block, and every later field then reads as a syntax error far from the cause. Parse `PEOPLE` and assert each object's KRA weights sum to 100 after any edit.
- **Do not name intern colleagues in a dashboard or pack** if they are not already in the vault as people. Confirm the spelling first.
- **Do not redesign the individual pages.** Reuse the published CSS. Consistency is the product.
- **Do not let the health chip grade day one.** Interns open this on their first morning.
- **Do not send the plan before access exists.** Day 1 accounts and repo access, not day 3. This is named in Viresh's own plan.
- **Do not email work without naming what Deep owes.** Every intern here is blocked on him for something.
- **Do not schedule one-on-ones on a public holiday.** Oct 2026: 2 Oct Gandhi Jayanti, 19 Oct Ayudha Puja, 20 Oct Vijayadashami. Check the hub note before proposing a date.
- **Do not leave deliverables without acceptance criteria.** A weekly deliverable is an artefact someone else can use, not a status update.
- **Never guess a name, email or role from a transcript.** A phantom name once reached a live onboarding deliverable. Verify against the vault or a Deep-confirmed source. The intern emails in this vault do not exist anywhere in it, which is a blocker, not a detail.

## Known blockers at time of writing (Oct 2026)

- **No mail path configured.** himalaya installed with no config, Apple Mail empty, Outlook not provisioned, no Gmail/SMTP connector in Hermes. Emails must be sent by hand or after configuring himalaya (`himalaya wizard`).
- **No calendar connector.** Meeting times are a proposal, not invites.
- **No intern email addresses in the vault.** Confirmed by grep across all notes. Resolve before sending.

Say these plainly. Do not imply the messages were sent.

## Files

- `build-person-dashboards.js`, `build-packs.js`, `build-combined-emails.js`, `build-team-dashboard.js`, `verify.py`, `pack_check.py` and `team_dashboard_gate.py` live in the vault at `Efforts/Active/<Team> <Month>/handover/` so they survive for the next month. `build-combined-emails.js` and `pack_check.py` arrived Oct 2026 after the undefined-fields incident and are not optional.
- Per-person packs in `Efforts/Active/<Team> <Month>/handover/packs/`, one folder per intern plus an index `README.md`.
- Dashboards in `Efforts/Active/<Team> <Month>/dashboards/`, plus a `manifest.json` with per-person task counts.

## Reference implementation

`Efforts/Active/Accelerator Team October 2026/`: eight dashboards, 240 tasks over 19 working days, `accelerator-q3-dashboard.html` as the combined source.