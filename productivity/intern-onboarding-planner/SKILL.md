---
name: "intern-onboarding-planner"
description: "Generate a day-by-day, week-by-week first-month onboarding plan for a new hire or intern from their resume plus a job description or role brief, delivered as an interactive HTML dashboard with per-task guidance. MANDATORY TRIGGER for: \"onboarding plan for [name]\", \"30-day plan\", \"first month plan\", \"day-by-day plan for [new hire]\", \"ramp-up plan\", \"onboarding dashboard\", \"like we did for Pallab/Prudhvi\", or any resume attached with a request to plan someone's first weeks. Used by HR and hiring managers across all Champions Group companies."
---

# Intern / New Hire Onboarding Planner

Generate a structured first-month (extendable to 60/90 day) onboarding plan with day-by-day tasks and deliverables, so no new joiner is ever aimless even when their reporting manager is busy. Built from tried and tested onboarding practice: light immersion first, real ownership by Week 3, fully productive by Week 4.

## Inputs (gather before writing anything)

Required:
1. **Resume** (file or pasted text)
2. **Role / JD**: what they were hired to do

Strongly recommended (ask via AskUserQuestion in ONE round if missing):
3. **Month 1 project context**: the concrete project(s) they will contribute to, with any source documents
4. **Duration** (30/60/90 days), **start date**, **reporting manager / buddy names** (verify name spellings against the vault and saved memories; transcripts mangle names)
5. **Company/entity** (for branding, wikilinks, and file placement if writing to the Celsus vault)

If start date is missing, assume the next working day. If the start date is mid-week, open with a 2-day "Ramp" block (setup + orientation) and align full weeks after it. If duration is missing, assume 60 days but plan Month 1 in full detail.

## Step 1: Resume-to-Role Mapping

Parse the resume and produce a table: `Their skill -> Our use`. Map every relevant skill, project, and internship to a concrete need in the role or Month 1 project. This table opens the plan. Skills with no mapping are noted as growth areas, not padding.

## Step 2: Plan Architecture (best practices baked in)

**Ramp (Days 1-2, or fold into Week 1 if starting on a Monday)**
- Day 1: environment setup with proof commands, access checklist, kickoff call with sponsor, buddy introduction (agree on channel, pairing slot, urgency definition), read glossary. Deliverable: working environment proof + 5 questions from day one.
- Day 2: orientation docs, first look at project materials, set up standup/ship-note templates. Deliverable: mini report (Learned / Surprised / Need).

**Week 1: Immerse, Audit, Map (deliberately light)**
- Tech stack / team tour day (deliverable: stack map).
- 1-2 days: an audit exercise IN THEIR HIRED SPECIALTY applied to our real surface, with sponsor's written approval of targets. Deliverable: findings report.
- Deep dive into the Month 1 project domain (deliverable: inventory or comparison artifact).
- Friday: Week 1 report + a PROPOSAL for the project approach. Week 1 ends with them proposing, not just absorbing.

**Weeks 2-3: Build v0 with progressive ownership**
- Break the project into daily shippable increments: one focus, 2-4 tasks, one named deliverable per day.
- End of Week 2: first end-to-end demo, however rough.
- Week 3 includes a day where their hired specialty and the project converge (e.g., security-test their own build).
- Any evaluation/bake-off the sponsor asked for gets a dedicated day with a written recommendation memo.

**Week 4: Automate, Scale, Document, Review**
- Automation day, scale-up day, polish/UI day, documentation + runbook day, Month 1 review day (demo, retro, Month 2 proposal with a recommendation, not a menu).

**Month-by-month arc:** one table row per month: theme + outcome. Month 2 = productize/extend + return partial time to hired role. Month 3 (if 90 days) = harden + hand off.

## Step 3: Per-Task Guidance Layer (MANDATORY)

Every task is more than a one-liner. Each task carries a **help payload** rendered as an expandable "How to approach it" panel (a small "?" toggle next to the checkbox). Write it like a senior colleague leaning over the shoulder:
- Concrete first move: the exact command, tool, message template, or question to ask, e.g. `docker run hello-world`, "get written approval before scanning".
- Judgment guidance where relevant: what to skip, what trap to avoid, what "done enough" means for a v0.
- Keep each to 1-3 sentences plus at most one code snippet. No lectures.

Every deliverable carries a **"What good looks like"** panel: the acceptance test in plain words, ideally phrased as a test someone else can apply ("could another new joiner orient from your diagram in 10 minutes?", "rerun the command twice: it must not duplicate data").

Safety rules to embed in relevant task hints: never scan targets without written sponsor approval, never commit data to git, auth-gate stores from day one.

## Step 4: Operating Rhythm (include verbatim in every plan)

1. Start of day: 3-line standup (yesterday shipped / today target / blockers) to sponsor + buddy.
2. End of day: ship note linking the day's deliverable. If a deliverable needs more than one day, say so in the ship note with the new ETA. Deliverables may span 2 days, never silently.
3. Friday: 1-page weekly report (shipped, learned, blocked, next week) + 15-minute demo.
4. Blocked? Pull from the Fallback Backlog. Never idle.

## Step 5: Orientation Content (include in the dashboard)

1. **Glossary**: 10-15 company/project terms they will hear in week one (entities, product names, project jargon like "canonical schema" or "P0"), one plain-language line each. Source from the vault CLAUDE.md Terms Decoder when working in Celsus.
2. **Who to Ask table**: person, role, "go to them for". Include the 2-hour rule: stuck more than 2 hours on one thing, ask; asking early is a strength signal.

## Step 6: Fallback Backlog (mandatory)

6-8 useful, self-serve tasks specific to this person and project. This is the "no aimless interns" guarantee: when managers are busy, the backlog absorbs the slack.

## Step 7: Success Criteria

4-6 measurable Month 1 outcomes the sponsor can verify in minutes ("X answers query Y in under 30 seconds", "zero high-severity findings").

## Step 8: Guardrails

- Personal data in the project (PANs, DOBs, health data, consumer PII)? Add a Data Handling panel: sensitive fields excluded by default, no data in git, auth-gating from day one.
- No em dashes anywhere in any output.

## Output Formats

**Primary: interactive HTML dashboard** (single self-contained file), built with the frontend-design skill and company brand tokens (Champions Group: orange #F26722 on white, Soft Peach #FFF4EC tints, Ink #1A1A1A, Inter + JetBrains Mono for code). Required features, all proven in the reference implementation:
- Plan data as a JS array (weeks -> days -> tasks {t, h} + deliv + dh), rendered dynamically.
- Checkbox per task + a distinct "deliverable shipped" checkbox per day; expandable day cards; auto today-highlighting; overall progress ring + per-week progress bars; sticky section nav.
- Per-task "?" guidance toggles and per-deliverable "What good looks like" panels (Step 3).
- Persistence: localStorage keyed per person (e.g. `{name}-onboarding-v1`) + "Copy progress code" / "Restore from code" (base64 JSON) for device moves. Server-side sync is bring-your-own-backend (Supabase) if ever needed.
- Responsive discipline: fluid SVGs (viewBox + width 100%, never fixed px), flex-wrap hero, tables in horizontal-scroll wrappers, auto-fit grids, breakpoints around 860px and 540px, 44px touch targets, prefers-reduced-motion support. Verify: extract the script and run `node --check`; check for em dashes; confirm no fixed-size SVG inside fluid containers.
- Hosting: file works on Netlify or ChampBeam Beam Pages (single file, under 2 MB, inline JS allowed).

**Secondary: Markdown narrative plan** for the vault. If working in the Celsus vault, save both to `Efforts/Active/{Name} Onboarding/` with frontmatter (type: effort, status, company, person, owner, start-date, tags) and `[[wikilinks]]`, and link from the person's `Atlas/People/` note. Use real calendar dates, 5-day weeks.

## Reference Implementation

Prudhvi Sai Vootukuri (API Security intern, Champions Accelerator, Aug 2026): 2-day ramp + 4 weeks building a vendor-data ingestion pipeline (DuckDB staging, MongoDB serving, Express+JWT API, React UI), with a DuckDB vs Mongo bake-off day and a security-hardening day scanning his own API. Canonical files: `Efforts/Active/Prudhvi Onboarding/prudhvi-onboarding-dashboard.html` (dashboard with 68 task hints + 22 deliverable hints) and `Prudhvi-Month1-Plan.md` (narrative) in the Celsus vault. Match that tone and granularity.
