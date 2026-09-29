<!-- Mode file, formerly the standalone skill `morning-routine`. Relative paths below resolve from modes/morning-routine/. -->

# Morning Routine, Daily Orchestrator

> "The compound effect of a great daily routine is the most underestimated force in business."

## What This Skill Does

This is a **conductor**, not an instrument. It orchestrates three specialized skills plus the
Celsus Dashboard into a single coherent daily ritual.

The dashboard (`dashboard.html`) IS the morning interface. It has a built-in wizard that
collects energy level, priority ranking, focus mode, and the wildcard framing for the day.
There is no separate quiz, the dashboard wizard replaces it.

The routine typically runs around **3pm IST** (Sreedeep's operational day-start), but can be
triggered anytime.

## System Architecture

```
+-----------------------------------------------------------+
|                  MORNING ROUTINE                          |
|               (This Orchestrator)                         |
|                                                           |
|  +----------------+                                       |
|  | Step 1         |  CONTEXT + ANALYSIS                   |
|  | Vault Keeper   |-> Link yesterday's notes              |
|  |                |-> Triage inbox                        |
|  |                |-> Read email triage note              |
|  |                |-> Generate today's daily note         |
|  |                |-> Surface wins, follow-ups, urgencies |
|  +-------+--------+                                       |
|          |                                                |
|          v                                                |
|  +----------------+                                       |
|  | Step 2         |  DASHBOARD WIZARD                     |
|  | dashboard.html |-> User opens dashboard.html           |
|  |                |-> Built-in wizard collects:           |
|  |                |     - Energy level                    |
|  |                |     - Stack-ranked priorities         |
|  |                |     - Focus mode                      |
|  |                |     - Wildcard framing                |
|  |                |-> Wizard completes, command center    |
|  |                |   activates                           |
|  +-------+--------+                                       |
|          |                                                |
|          v                                                |
|  +----------------+                                       |
|  | Step 3         |  PLANNING                             |
|  | Day Planner    |-> Reads TASKS.md task board           |
|  |                |-> Uses energy + priorities from Step 2|
|  |                |-> Maps calendar constraints           |
|  |                |-> Outputs: Day at a Glance            |
|  +-------+--------+                                       |
|          |                                                |
|          v                                                |
|  +----------------+                                       |
|  | Step 4         |  DASHBOARD REFRESH                    |
|  | Dashboard      |-> Fetches calendar events (7 days)    |
|  | Refresh        |-> Scans Calendar/Meetings/ for prep   |
|  |                |-> Scans Efforts/Active/ for blocks    |
|  |                |-> Writes dashboard-data.json          |
|  +----------------+                                       |
|                                                           |
|  RESULT: Dashboard is live, plan is in the daily note    |
+-----------------------------------------------------------+
```

---

## Step-by-Step Execution

### Step 1: Context + Analysis (vault-keeper)

**Goal:** Ensure yesterday's context is fully connected, inbox is triaged, and today's daily
note exists with fresh email context.

**Invoke the `vault-keeper` skill:**

1. Link yesterday's daily note (Workflow 1: Full Vault Scan, focused on recent files)
2. Triage the inbox (Workflow 2)
3. Read the email digest:
   - First check: `Atlas/Email Triage/YYYY-MM-DD.md` (previous business day's triage note)
   - The automated 9 PM IST triage is the preferred source
   - If stale or absent, fall back to live Outlook MCP
   - If no access: ask for a brief verbal summary
4. Generate today's daily note (Workflow 3) if it doesn't exist
5. Produce the context summary for the user:
   - Yesterday's Wins (2-4 from yesterday's daily note)
   - Needs Follow-Up (incomplete tasks, meeting action items)
   - From Your Inbox (urgent email items)
   - Effort status snapshot

**Also check for Apple Notes stubs** in `Inbox/Apple Notes/` (files with `status: needs-context`).
If found, process them now using the answers the user gives you in conversation, do NOT queue
them for a separate quiz. Ask about each stub directly in chat, then update and move the file.

**Handoff to Step 2:** Present the context summary. Then tell the user:
> "Vault is updated and your context is ready. Open **dashboard.html** in your vault, it'll
> walk you through the rest of the routine from there."

---

### Step 2: Dashboard Wizard

**Goal:** The user completes the built-in morning wizard in dashboard.html.

The wizard collects energy level, stack-ranked active tasks (top 3 priorities), focus mode
(deep/variety/meetings), and the wildcard framing for the day. When the wizard is submitted,
the dashboard transitions to the command center showing the pulse strip, task board, and
meeting strip.

**This skill does not generate a quiz or any HTML artifact.** The dashboard IS the interview.

**What to do here:** Simply wait. The user will come back to the conversation after completing
the dashboard wizard. When they return, say "Got it, let's build your plan" and move to Step 3.

If the user does not have access to dashboard.html or says it's not loading, fall back to
asking the wizard questions directly in chat: energy level, top 3 tasks, focus mode.

---

### Step 3: Planning (day-planner)

**Goal:** Combine vault context and dashboard wizard outputs into a time-blocked plan.

**Invoke the `day-planner` skill** with:
- Energy level (from dashboard wizard or chat fallback)
- Priority ranking: top 3 tasks (from dashboard wizard)
- Focus mode (from dashboard wizard)
- Calendar events (from Google Calendar MCP if available)
- TASKS.md content from vault root (authoritative task list)
- Active efforts from `Efforts/Active/`
- Time budget: default is 3pm to midnight IST unless user specifies otherwise

**Output:** Written to today's daily note under the Day at a Glance section.

**Meeting prep:** If there are external or sales meetings today, also invoke `meeting-prep`
for each one. Internal syncs get light prep. [[InfraTech]] Weekly is always skipped.

---

### Step 4: Dashboard Refresh (dashboard-refresh)

**Goal:** Write fresh `dashboard-data.json` so the dashboard reflects current calendar,
meeting prep status, and effort health.

**Invoke the `dashboard-refresh` skill.** It fetches calendar events (7 days), scans
`Calendar/Meetings/` for prep docs (which Step 3 may have just created), scans
`Efforts/Active/` for status overrides, and writes `dashboard-data.json`.

**Tell the user:** "Refresh your dashboard to see today's full command center."

---

## Adaptive Behavior

| Situation | Adaptation |
|-----------|-----------|
| Full email + calendar + MCPs | Complete 4-step routine with rich context |
| No email access | Step 1 asks for verbal summary; rest runs normally |
| No yesterday daily note | Step 1 is lighter; Steps 2-4 run fully |
| Dashboard.html not loading | Skip Step 2; ask wizard questions in chat |
| User says "quick mode" | Skip vault scan details; go straight to dashboard wizard |
| No meetings today | Skip meeting-prep inside Step 3 |
| Apple Notes stubs found | Handle in Step 1 via conversation, not a separate quiz |

## Timing

Designed for ~3pm IST day-start but adapts:
- **Before 12pm:** Extended planning horizon for the day.
- **12pm-4pm:** Standard routine, all 4 steps.
- **After 4pm:** "Late start" mode, focuses on what's achievable today.
- **After 8pm:** "Tomorrow prep" mode, skips today planning, sets up tomorrow.
  Dashboard refresh still runs so tomorrow's calendar is visible.

---

## Integration Map

| Skill/Tool | Step | What It Does |
|-----------|------|--------------|
| **vault-keeper** | 1 | Links notes, triages inbox, generates daily note, surfaces context |
| **dashboard.html** | 2 | Built-in wizard: energy, priorities, focus mode, wildcard |
| **day-planner** | 3 | Time-blocked plan from TASKS.md + effort context |
| **meeting-prep** | 3 (conditional) | Prep docs for today's external meetings |
| **dashboard-refresh** | 4 | Writes dashboard-data.json with fresh calendar + effort state |

---

## Quick Invocation

Full routine:
- "morning routine" / "start my day" / "daily kickoff" / "plan my day"

Individual steps:
- "just link yesterday's notes", Step 1 only (vault-keeper)
- "plan my afternoon", Step 3 only (day-planner)
- "refresh the dashboard", Step 4 only (dashboard-refresh)
- "open my dashboard", Step 2 reminder only

---

## Iteration Log

| Date | Change | Why |
|------|--------|-----|
| Initial | 4-phase orchestrator created | First daily routine skill |
| [[2026-03-16]] | Email triage note integration | Stop re-scanning Outlook; use pre-built triage notes |
| [[2026-03-26]] | Apple Notes integration | Scan stubs in Step 1, resolve via conversation |
| [[2026-04-17]] | Merged vault-linker + celsus-cortex into vault-keeper. Added dashboard-refresh. Phase numbering updated. | Post-dashboard build: one skill per concern |
| [[2026-04-17]] | Replaced interactive-quiz Phase 2 with dashboard.html wizard. Dashboard is the morning interface. | User feedback: dashboard wizard already does this job, no separate quiz needed |
