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
6. In an unattended run, skip the wizard rather than waiting. Label energy and focus as provisional, write the run sheet, and do not book events.
7. Select the latest dated Zoom triage note by its YYYY-MM-DD filename. A recently modified MOC is an index, not the latest sweep.
8. Deduplicate Wispr by meeting ID against the prior daily note's commitment register. IDs absent from the recap prose may already be covered in its register.
9. Resolve quoted today and tonight against the source date. Midnight snapshots can retain yesterday's meeting asks and deadlines.
10. Verify Kanban comment writes against task_comments or card history. The task_events kind is commented, not comment.
11. Protect the 11 a.m. run-sheet deadline: write the provisional Day at a Glance immediately after the minimum source reads, before optional audits or dashboard delegation. In cron, delegate_task joins synchronously and can consume the whole deadline; append enrichment afterward rather than waiting to create the daily note.
12. Dashboard effort overrides come only from a YAML frontmatter block starting on line 1. A body line such as Status: blocked before implementation is not effort-status metadata. Preserve existing overrides and reject that false-positive case in the refresh check.
13. Before reusing a decision, read its live title, body and latest ruling comments. A needs_input status can survive Deep's answer, and a TASKS.md card id can now identify a different Send Pack. Preserve the later ruling, flag mismapped references in place, and never stage an old question solely from its status or yesterday's note.
14. Keep calendar descriptions with the normalized source snapshot on the first fetch. Dropping body and join details before dashboard delegation forces a second retrieval and leaves a fresh dashboard without working meeting links. Preserve exact native event ids and label any excerpt rather than claiming a full description.
15. For a provider deletion notice, prefer a fresh read-only provider timestamp over mail-time arithmetic. Pull the latest `blocked` event reason if a live decision card's body is empty or stale, then apply later comments. Stage recovery separately from elective retirement. When only the notice is available, label the clock as estimated and surface the console check without assuming recovery or approval.
16. After a provider cutoff, an absent project is a recovery gap, not proof of permanent purge. Replace the expired ask with the live console/support or backup-verification question and leave unrelated test volumes and retirement out of it. Likewise, a verified later signature supersedes a pre-signature decision, not the payment, NDA or kickoff gates.
17. Dashboard refresh: an existing `meetingPrep` entry of `status: none` without a `prepNote` is a placeholder. Upgrade it when a dated title match is verified; preserve substantive flags. For the day plan, also check the current weekly brief for explicitly sourced calendar-only bookings missing from default Outlook. Label their snapshot date and never insert them into the live Outlook feed.
