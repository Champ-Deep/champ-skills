---
name: daily-start
description: >-
  Deep's daily start in one skill: the morning routine orchestrator (link and triage yesterday through vault-keeper, analyze wins and follow-ups, the interactive morning interview, then the time-blocked day plan), the styled HTML morning brief, standalone day planning, and the dashboard.html data refresh. Produces the daily run sheet of pending priority tasks, ready by 11 a.m. MANDATORY TRIGGER for: "morning routine", "start my day", "daily kickoff", "afternoon planning", "plan my day", "what should I focus on today", "run the routine", "morning brief", "/morning", "time block", "schedule my tasks", "prioritize my work", "run sheet", "refresh dashboard", "dashboard is stale", "calendar not showing", "meeting prep missing from dashboard", and session-start dashboard sync. A plain question about today's calendar is answered directly, not with the full routine. Replaces morning, morning-routine, day-planner and dashboard-refresh.
---

# Daily Start

| Mode | Use when | Read |
|---|---|---|
| **morning-routine** | Full routine: context, analysis, interview, plan. The orchestrator | `modes/morning-routine/MODE.md` |
| **day-planner** | Time-blocked plan only, or Phase 4 of the routine | `modes/day-planner/MODE.md` |
| **morning** | Render the morning brief as a styled HTML artifact, or set it up as a recurring task | `modes/morning/MODE.md` |
| **dashboard-refresh** | Regenerate dashboard-data.json so dashboard.html is current. Also the last step of the routine | `modes/dashboard-refresh/MODE.md` |

## Changes from the old morning-routine (these override the mode file)

1. **Phases 1 and 2 are one vault-keeper run.** Where `morning-routine` says vault-linker or celsus-cortex, run the `vault-keeper` skill instead: inbox triage, daily note, and the Wins, Follow-Up and Inbox analysis. No autopilot link writes: link work goes through vault-keeper's dry-run gate, and the morning routine only reports link issues.
2. **Daily note path** is `Calendar/Daily Notes/YYYY/MM/YYYY-MM-DD.md` (nested). Ignore the flat path in the mode file.
3. **Phase 3 interview** uses the `interactive-quiz` skill. The mode file names `references/morning-quiz-blueprint.md`, which does not exist: build the quiz from the phase description instead.
4. **Phase 4** is `modes/day-planner/MODE.md`.
5. **Phase 5 (new):** write the run sheet of pending priority tasks into today's daily note, then run `modes/dashboard-refresh/MODE.md`.
6. Never move `TASKS.md` or `dashboard.html`. Dedupe before any TASKS.md append (vault-keeper).
