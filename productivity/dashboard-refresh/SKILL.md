---
name: dashboard-refresh
description: >
  Regenerates dashboard-data.json in the Celsus vault root so that dashboard.html displays
  fresh calendar events, correct meeting prep status, and accurate effort health indicators.
  Run this at session start, after vault-keeper completes, after the morning routine, or whenever
  the dashboard shows stale data. MANDATORY TRIGGER for: "refresh dashboard", "sync dashboard",
  "dashboard is stale", "update my dashboard", "dashboard data", "regenerate dashboard",
  "calendar not showing", "meeting prep missing from dashboard", "effort status wrong on dashboard",
  or any request that the dashboard displays incorrect/missing data. Also runs automatically as
  Phase 5 of the morning-routine orchestrator and at session start via the scheduled task.
---

# Dashboard refresh

> One job: write a fresh `dashboard-data.json` to the vault root so `dashboard.html` loads
> current data the next time it opens. This skill touches no other files.

## Context

`dashboard.html` is the Celsus command center. It reads calendar events, [[Meeting Prep]] status,
and effort health from `dashboard-data.json` at vault root. Because `dashboard.html` runs in
the browser (File System Access API), it cannot call MCPs directly. This skill bridges that gap:
it pulls data from connected MCPs and vault files, then writes the JSON the dashboard consumes.

---

## Steps

### Step 1: Fetch Calendar Events

Pull events from Google Calendar for today + the next 7 days.

Use `mcp__2d7b3c3e__list_events` with a date range from today (00:00 IST) to +7 days.

Normalize each event to this schema:

```json
{
  "id": "<event id>",
  "summary": "<event title>",
  "start": { "dateTime": "<ISO 8601 with offset, e.g. 2026-04-17T15:00:00+05:30>" },
  "end":   { "dateTime": "<ISO 8601 with offset>" },
  "description": "<full description including Zoom/Meet/Teams URLs>"
}
```

Store the result under `calendars.google`.

If Outlook MCP is connected, also call `mcp__ccb19075__outlook_calendar_search` for the same
range and store under `calendars.outlook`. Deduplicate by matching on `summary + start time`
if both sources return the same event.

### Step 2: Read Existing `dashboard-data.json` to Preserve State

Read the current file at vault root:

```
/path/to/Celsus/dashboard-data.json
```

Extract and preserve:
- `meetingPrep` — all existing prep status flags. Do NOT overwrite these from scratch.
- `effortStatus` — all existing effort overrides.

If the file doesn't exist yet, start with empty objects for both.

### Step 3: Scan Calendar/Meetings/ for Prep Documents

Check `Calendar/Meetings/` for any note whose filename contains today's date or a meeting title
from today's calendar.

Match logic: lowercase the meeting summary, strip punctuation, then fuzzy-match against note
filenames and the first heading in each note. If a match is found, mark:

```json
"meetingPrep": {
  "<eventId>": { "status": "done", "prepNote": "Calendar/Meetings/YYYY-MM-DD - Title.md" }
}
```

Any event without a matching prep note stays as `"status": "none"` (or whatever it was).

### Step 4: Scan Efforts/Active/ for Status Overrides

Read every `.md` file in `Efforts/Active/`. For each file:
- Check YAML frontmatter for a `status:` field set to `blocked` or `paused`
- If found, record in `effortStatus`:

```json
"effortStatus": {
  "ChampGraph Build": { "status": "blocked", "reason": "Hemang -- server-side memory + variable scope" }
}
```

If a file has no `status:` field or `status: active`, omit it from `effortStatus` (active is
the default and the dashboard renders it without an override).

### Step 5: Write New `dashboard-data.json`

Merge the fresh calendar data with the preserved `meetingPrep` and `effortStatus`. Write to
vault root:

```json
{
  "generated": "<current ISO timestamp with IST offset, e.g. 2026-04-17T15:00:00+05:30>",
  "calendars": {
    "google":  [ ...today+7d events normalized ],
    "outlook": [ ...today+7d events normalized, or [] if not connected ]
  },
  "meetingPrep": {
    "<eventId>": { "status": "done|none", "prepNote": "<optional vault path>" }
  },
  "effortStatus": {
    "<effortName>": { "status": "blocked|paused|active", "reason": "<optional>" }
  }
}
```

### Step 6: Confirm and Report

After writing, output a brief confirmation:

```
Dashboard refreshed.
Events: N today, M this week
Prep docs found: P / Q meetings
Blocked efforts: B
Generated: YYYY-MM-DD HH:MM IST
```

---

## Event ID Convention

| Source | ID |
|--------|----|
| Google Calendar | Native `id` field from API response |
| Outlook | Native `id` field. If absent: `outlook-{summary-slug}-{date}` where slug is summary lowercased, spaces replaced with hyphens, truncated to 40 chars |
| Manual entries | `manual-{summary-slug}` |

---

## Schema Reference

| Field | Type | Description |
|-------|------|-------------|
| `generated` | ISO timestamp | When this file was last regenerated (IST offset) |
| `calendars.google` | Array | Google Calendar events, normalized |
| `calendars.outlook` | Array | Outlook calendar events, normalized (empty if not connected) |
| `meetingPrep[id].status` | `'done'` or `'none'` | Whether a prep doc exists for this meeting |
| `meetingPrep[id].prepNote` | String (optional) | Vault-relative path to the prep note |
| `effortStatus[name].status` | `'blocked'`, `'paused'`, or `'active'` | Effort override for dashboard display |
| `effortStatus[name].reason` | String (optional) | Why the effort is blocked or paused |

---

## Scheduling

This skill is also executed by the `dashboard-data-refresh` scheduled task. That task fires:
1. At session start (session-start hook)
2. When `localStorage.celsus_sync_requested` is set and less than 5 minutes old

Full runbook with setup instructions: `Other/Plans/dashboard-data-refresh-runbook.md`

---

## What This Skill Does NOT Do

This skill only writes `dashboard-data.json`. It does not:
- Modify any vault notes
- Trigger vault-keeper or any other skill
- Open or control `dashboard.html`
- Update `TASKS.md`

Those responsibilities belong to their own skills. Keep this one sharp.

## Related

[[Skills MOC]]
