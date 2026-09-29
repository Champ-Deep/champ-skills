---
name: daily-start
description: >-
  Deep's daily start in one skill: the morning routine (vault-keeper context and inbox, the dashboard.html morning wizard, the time-blocked day plan from TASKS.md, then the dashboard data refresh), the styled HTML morning brief, standalone day planning, and dashboard-data.json regeneration. Produces the daily run sheet of pending priority tasks, ready by 11 a.m. MANDATORY TRIGGER for: "morning routine", "start my day", "daily kickoff", "afternoon planning", "plan my day", "what should I focus on today", "run the routine", "morning brief", "/morning", "time block", "schedule my tasks", "prioritize my work", "run sheet", "refresh dashboard", "sync dashboard", "dashboard is stale", "calendar not showing", "meeting prep missing from dashboard", and session-start dashboard sync. A plain question about today's calendar is answered directly, not with the full routine. Replaces morning, morning-routine, day-planner and dashboard-refresh.
---

# Daily Start

| Mode | Use when | Read |
|---|---|---|
| **morning-routine** | Full routine. The orchestrator: Step 1 vault-keeper, Step 2 dashboard wizard, Step 3 day plan, Step 4 dashboard refresh | `modes/morning-routine/MODE.md` |
| **day-planner** | Time-blocked plan only, or Step 3 of the routine. Reads TASKS.md | `modes/day-planner/MODE.md` |
| **dashboard-refresh** | Regenerate dashboard-data.json so dashboard.html is current. Step 4 of the routine, and at session start | `modes/dashboard-refresh/MODE.md` |
| **morning** | Render the morning brief as a styled HTML artifact, or set it up as a recurring task | `modes/morning/MODE.md` |

## Rules that override the mode files

1. **Step 1 is the `vault-keeper` skill**, which reports link issues during the routine and never writes links without its dry-run gate.
2. **Daily note path** is `Calendar/Daily Notes/YYYY/MM/YYYY-MM-DD.md` (nested).
3. **Run sheet:** Step 3 writes the pending priority tasks for today into the daily note under `Day at a Glance`, ready by 11 a.m. when the routine runs on schedule.
4. Wherever a mode file says to invoke `day-planner` or `dashboard-refresh`, read that mode file here.
5. Never move `TASKS.md` or `dashboard.html`. Dedupe before any TASKS.md append (vault-keeper).
