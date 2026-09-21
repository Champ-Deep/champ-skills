---
name: intern-onboarding-planner
description: "Generate a day-by-day first-month onboarding plan for a new hire or intern from resume plus role brief, as a single-file HTML dashboard that answers on screen one: what do I do today, where am I in the month, what is due Friday, who do I ask. Trigger on onboarding plan for [name], 30-day plan, first month plan, ramp-up plan, onboarding dashboard, intern dashboard, or a resume with a request to plan someone's first weeks."
---

# Intern and New Hire Onboarding Planner

Two readers, two jobs. The **intern** opens the dashboard every morning and needs, in five seconds: what do I do today, where am I in the month, what is due Friday, who do I ask. The **sponsor** (usually Deep) opens it once a week and needs, in ten seconds: is this person on track. The page is a map with today pinned, not a list of collapsed rows.

Plan content follows tried and tested practice: light immersion first, real ownership by Week 3, fully productive by Week 4, and no new joiner ever aimless when their manager is busy.

## What went wrong before (do not repeat)

Previous dashboards were 6,500 to 9,500px tall: a hero, then 22 identical collapsed day rows, then four wide tables. "Today" sat 5,000px down the page. There was no view of the month as a whole. The Skills and Glossary tables clipped their second column on a phone. A 0% progress ring greeted the intern on day one. The layout contract below replaces that structure; the plan content rules are kept.

## Inputs (gather before writing anything)

Required:
1. **Resume** (file or pasted text).
2. **Role or JD**: what they were hired to do.

Strongly recommended (ask via AskUserQuestion in ONE round if missing):
3. **Month 1 project context**: the concrete project(s) with any source documents.
4. **Duration** (30, 60, or 90 days), **start date**, **sponsor and buddy names**. Verify every name against a source Deep confirmed directly (vault person notes, `_config/people.md`, saved memory), never against a transcript. A phantom name from a Zoom transcript once reached a live onboarding deliverable.
5. **Company or entity** for branding, wikilinks, and file placement.

Defaults: start date missing means the next working day. Mid-week start means a two-day Ramp block, then full weeks. Duration missing means 60 days, with Month 1 in full detail.

## Step 1: Resume-to-role mapping

Produce a `You bring -> We use it for` list of at most eight rows. Every relevant skill maps to a concrete need in the role or the Month 1 project. Unmapped skills are named as growth areas. This list opens the Markdown plan and sits behind a collapsed "Your background" toggle on the dashboard; it is for the sponsor's confidence and the intern's orientation, not for daily use.

## Step 2: Plan architecture

**Ramp (Days 1 to 2, or folded into Week 1 for a Monday start)**
- Day 1: environment setup with proof commands, access checklist, kickoff with sponsor, buddy introduction (agree the channel, the pairing slot, and what "urgent" means), read the glossary. Deliverable: working environment proof plus five questions from day one.
- Day 2: orientation docs, first look at project materials, set up standup and ship-note templates. Deliverable: a mini report (Learned / Surprised / Need).

**Week 1: Immerse, audit, map (deliberately light)**
- Stack and team tour day (deliverable: a stack map).
- One or two days of an audit exercise IN THEIR HIRED SPECIALTY on our real surface, with the sponsor's written approval of targets. Deliverable: findings report.
- Deep dive into the Month 1 project domain (deliverable: an inventory or comparison).
- Friday: Week 1 report plus a PROPOSAL for the project approach. Week 1 ends with them proposing, not just absorbing.

**Weeks 2 to 3: Build v0 with progressive ownership**
- Daily shippable increments: one focus, two to four tasks, one named deliverable per day.
- End of Week 2: first end-to-end demo, however rough.
- Week 3 has a convergence day where their hired specialty meets the project (security-test their own build, design-review their own UI).
- Any evaluation or bake-off the sponsor asked for gets its own day and a written recommendation memo.

**Week 4: Automate, scale, document, review**
- Automation day, scale-up day, polish day, documentation and runbook day, Month 1 review day (demo, retro, Month 2 proposal with a recommendation, not a menu).

**Month arc:** one row per month, theme plus outcome. Month 2 productises or extends and returns partial time to the hired role. Month 3 (90-day plans) hardens and hands off.

## Step 3: Per-task guidance (mandatory)

Every task carries a **help payload** rendered as an expandable "How to approach it" panel. Write it like a senior colleague leaning over the shoulder: the concrete first move (the exact command, tool, message template, or question), the judgment call where one exists (what to skip, the trap, what "done enough" means for a v0). One to three sentences plus at most one code snippet. No lectures.

Every deliverable carries a **"What good looks like"** panel: the acceptance test in plain words, phrased so someone else can apply it ("could another new joiner orient from your diagram in ten minutes?", "run it twice: it must not duplicate data").

Safety rules to embed where relevant: never scan targets without written sponsor approval, never commit data to git, auth-gate stores from day one.

## Step 4: Operating rhythm (verbatim in every plan)

1. Start of day: three-line standup (yesterday shipped / today target / blockers) to sponsor and buddy.
2. End of day: ship note linking the day's deliverable. A deliverable may span two days, never silently; say so in the ship note with the new ETA.
3. Friday: one-page weekly report (shipped, learned, blocked, next week) plus a 15-minute demo.
4. Blocked? Pull from the Fallback Backlog. Never idle. Stuck more than two hours on one thing: ask. Asking early is a strength signal.

## Step 5: Orientation content

1. **Glossary**: 10 to 15 terms they will hear in week one (entities, product names, project jargon), one plain line each. Source from the vault glossary (`_config/glossary.md`) when working in Celsus.
2. **Who to ask**: at most six people, each with role, "go to them for", and channel.

## Step 6: Fallback backlog (mandatory)

Six to eight useful self-serve tasks specific to this person and project. This is the "no aimless interns" guarantee.

## Step 7: Success criteria

Four to six measurable Month 1 outcomes the sponsor can verify in minutes ("X answers query Y in under 30 seconds", "zero high-severity findings").

## Step 8: Guardrails

- Personal data in the project (PANs, DOBs, health data, consumer PII)? Add a Data Handling panel: sensitive fields excluded by default, no data in git, auth-gating from day one.
- No em dashes or en dashes anywhere, including date ranges ("Aug 13 to Sep 11").
- Never name a delivery vendor in anything the intern will forward outside the company.

## Output 1: the dashboard (primary)

Single self-contained HTML file built through `frontend-design` with the company brand skill's tokens (Champions Group: orange #F26722 on white, Soft Peach #FFF4EC tints, Ink #1A1A1A, Inter plus JetBrains Mono for code; other entities per their brand skill). Plan data is a JS array (weeks -> days -> tasks {t, h} plus deliv and dh), rendered dynamically.

### Layout contract (desktop; phone stacks in the same order)

```
+-------------------------------------------------------------------------+
| Brand · {Name} · Month 1 · Day 12 of 22          Sponsor strip: ON TRACK |
+-----------------------------------------+-------------------------------+
| TODAY  Thu 27 Aug · Standardization     | MONTH MAP                     |
| transforms                              | Ramp  [1][2]                  |
|  [ ] task 1                        (?)  | Wk 1  [3][4][5][6][7*]        |
|  [ ] task 2                        (?)  | Wk 2  [8][9][10][11][12*]     |
|  [ ] task 3                        (?)  | Wk 3  [13][14][15][16][17*]   |
|  Deliverable: Transform module     (?)  | Wk 4  [18][19][20][21][22*]   |
|  [ ] shipped                            | done · today · next · demo    |
|  Standup template  |  Ship-note template| Friday: Week 2 demo, in 2 days|
+-----------------------------------------+-------------------------------+
| WHO TO ASK  [Sponsor] [Buddy] [Collaborator] [Reviewer]  (cards, max 6) |
+-------------------------------------------------------------------------+
| DELIVERABLE STRIP  o---o---o---●---o---o---o   4 shipped · 18 to go     |
+-------------------------------------------------------------------------+
| Week 1  |  Week 2  |  Week 3  |  Week 4  (tabs; one week open at a time)|
|   day cards, today open, others collapsed, each with tasks and hints    |
+-------------------------------------------------------------------------+
| Glossary (chips, tap to reveal) · Backlog · Success criteria · Sponsor  |
| view · Your background (collapsed) · Progress code                      |
+-------------------------------------------------------------------------+
```

### Required features

1. **Today panel, first thing on screen.** Picks the day from the real date: before the start date it shows Day 1 with a "starts {date}" note; after the plan it shows the Month 1 review. Shows the day's focus, its tasks with checkboxes and "?" hints, the deliverable with its "What good looks like" panel and a shipped checkbox, and the standup and ship-note templates as one-tap copy blocks. The page accepts `?today=YYYY-MM-DD` in the URL so the resolver can be tested without changing the system clock.
2. **Month map.** A grid of one cell per working day in week rows, each cell showing the day number and a two-word label, coloured by state (done, today, upcoming, demo day), and clickable to open that day. The map is the "where am I" answer and must be visible in the first desktop viewport, and within the first 1.5 phone viewports.
3. **Progress that does not discourage.** The primary number is "Day X of N"; percent complete and per-week bars are secondary. No lone 0% ring in the hero.
4. **Next Friday callout.** The upcoming demo or report, with days remaining, inside the month map.
5. **Who to ask as cards**, not a table: name, role, ask them for, channel. At most six. Sticky rail on desktop, a horizontal scroll row on phone.
6. **Deliverable strip.** One node per deliverable on a horizontal line, filled when shipped, with the count beside it.
7. **Week tabs with day cards.** One week open at a time; inside it, today's card open and the rest collapsed. Collapsed cards show weekday, date, focus, task count, and deliverable name.
8. **Sponsor strip.** One line at the top: ON TRACK, WATCH, or BEHIND, computed from working days elapsed versus deliverables shipped (behind when shipped falls two or more below elapsed days), with a "Sponsor view" tab listing success criteria, deliverable status, and any deliverable that slipped past its ETA. This is the ten-second answer for the manager.
9. **No wide tables on the dashboard.** Glossary renders as tap-to-reveal chips or a two-column definition list; skills mapping is a collapsed two-column list; everything becomes single-column cards below 540px. Any table wider than two columns is a build error.
10. **Persistence.** localStorage keyed per person (`{name}-onboarding-v1`) plus "Copy progress code" and "Restore from code" (base64 JSON) for device moves. Server sync is bring-your-own backend if ever needed.
11. **Responsive discipline.** Fluid SVGs (viewBox plus width 100%), auto-fit grids, breakpoints around 860px and 540px, 44px touch targets, `prefers-reduced-motion` support. Phone shows the top five things (today, month map, who to ask, next Friday, progress) before anything else.
12. **Hosting.** Works as one file on Netlify or ChampBeam Beam Pages, under 2 MB, inline JS allowed.

## Output 2: Markdown narrative plan (vault)

Save both files to `Efforts/Active/{Name} Onboarding/` with frontmatter (type: effort, status, company, person, owner, start-date, tags), real calendar dates, five-day weeks, and `[[wikilinks]]` that pass `_config/link-policy.md`. Link from the person's `Atlas/People/` note. The Markdown plan holds the full skills mapping, the month arc, and the success criteria in prose; the dashboard holds the daily surface.

## Verify (mandatory before delivery)

Run the `visual-verify` gate at 390 and 1440, open the screenshots with the Read tool, and add these checks specific to this skill:

1. **First-screen test.** In the 1440px top screenshot, the Today panel and the month map are both visible without scrolling. In the 390px screenshot, the Today panel is complete within the first viewport and the month map begins within the first 1.5 viewports.
2. **Today test.** Load the page with `?today=` set to a mid-plan date, a pre-start date, and a post-plan date; confirm the Today panel resolves correctly for each.
3. **Five-second test.** From the top screenshot alone, write what the intern should do today and when the next demo is. If you cannot, the layout failed.
4. **Completeness count.** Every day has two to four tasks, one deliverable, a hint on every task, and a "What good looks like" on every deliverable. Print the counts.
5. **No clipped tables.** At 390px, no element has a scrollWidth larger than the viewport; the audit names the culprit if one does.
6. **Names.** Every person named on the page appears in a Deep-confirmed source.
7. `node --check` on the extracted script; zero console errors; zero em or en dashes (`grep -cP '\xe2\x80[\x93\x94]' <output.html>` must print 0).

Zero FAILs before delivery. If no browser is available, say so and label the output unverified.

## Delivery note

Two lines: where the files are, and the verification numbers (page heights at 1440 and 390, first-screen test result, task and deliverable counts). The sponsor reads about a third of any message; lead with those.

## Reference implementations

Content tone and hint granularity: `Efforts/Active/Prudhvi Onboarding/` (68 task hints, 22 deliverable hints, DuckDB versus Mongo bake-off day, security-hardening convergence day). Match that depth of guidance. Do not copy its layout; it predates this layout contract and is the list-not-map structure this version replaces.