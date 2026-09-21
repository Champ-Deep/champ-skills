---
name: "daily-note-recap"
description: "Generate a comprehensive daily note in the Celsus Obsidian vault recapping activity, PLUS a visual HTML executive report in Lake B2B branding, PLUS the nightly BearDrive knowledge sync (curates the day's documents into the BearDrive agent knowledge space per Atlas/Ops/BearDrive/BearDrive Sync SOP.md). Pulls from the vault, Google Calendar, Zoom MCP (meetings, AI summaries, My Notes, recordings), Wispr Flow MCP (recorded meeting transcripts, action items, scratchpad voice notes), and Apple Notes. Runs Tue to Sat at 00:30 IST, covering Monday to Friday. MANDATORY TRIGGER for: 'daily note', 'daily recap', 'end of day', 'eod report', 'daily report', 'what did I do today', 'recap my day', 'send daily update', 'manager report', 'executive summary', 'beardrive sync'. Also run by the daily-note-recap scheduled task."
---

# Daily Note Recap: Vault Note + Executive HTML Report + BearDrive Sync

> **Purpose:** Generate THREE outputs every day:
> 1. A comprehensive Obsidian vault daily note (`Calendar/Daily Notes/YYYY-MM-DD.md`)
> 2. A colorful Lake B2B-branded HTML executive report for the reporting manager
> 3. A BearDrive knowledge sync: the day's qualifying documents curated into the BearDrive agent knowledge space (Step 6.5)
>
> **Gold standard:** `2026-03-16.md` is the benchmark. Every daily note must match or exceed this quality.

---

## When This Runs

- **Scheduled:** 00:30 IST, Tuesday to Saturday (covering Monday to Friday activity)
- **On demand:** When Sreedeep says "daily recap", "eod report", "manager report", etc.
- **After morning routine:** If the morning routine creates the daily note (morning plan), the recap task MERGES the evening data. Never overwrites.

---

## Step 0: Load Connector Tools (Preflight)

Zoom and Wispr Flow tools are deferred. Load them with ToolSearch before Step 3, or the meeting sections will be empty.

```
ToolSearch query: "zoom meeting recordings assets search"
ToolSearch query: "wispr flow meetings scratchpad notes transcript"
```

Connector tool names are prefixed with a server ID that varies by install. Match on the SUFFIX, not the full string.

**Zoom MCP (suffixes):** `search`, `search_describe_capabilities`, `search_meetings`, `ask`, `get_meeting_assets`, `recordings_list`, `get_recording_resource`, `my_notes_get_note_content`, `get_file_content`, `hub_get_file_content`, `hub_create_file_from_content`, `create_new_file_with_markdown`

**Wispr Flow MCP (suffixes):** `search_meetings`, `get_meeting`, `search_scratchpad_notes`, `get_scratchpad_note`, `list_upcoming_meetings`, `get_upcoming_meeting`, `search_calendar_events`, `get_calendar_event`, `get_meeting_by_calendar_id`, `get_meeting_attendee_emails`, `list_meeting_series`, `resolve_share_link`, `resolve_calendar_link`, `get_account_info`

**Note the collision:** BOTH servers expose a tool called `search_meetings`. Always disambiguate by the server prefix. Zoom's is the deprecated legacy one (prefer Zoom `search` instead). Wispr's is the primary way in to Wispr recordings.

Record which connectors resolved. If either fails to load or returns an auth/network error, do NOT silently skip. Note the failure in the Appendix integration tracker and add a carried-forward task.

---

## Step 1: Determine Today's Date (IST)

**CRITICAL, Timezone Fix:** Always use IST. The scheduled task runs at 00:30 IST. Without this fix, plain `date` returns the prior UTC date.

```bash
TZ='Asia/Kolkata' date '+%Y-%m-%d'
TZ='Asia/Kolkata' date '+%Y-%m-%d %H:%M:%S IST'
TZ='Asia/Kolkata' date -d 'yesterday' '+%Y-%m-%d' 2>/dev/null || TZ='Asia/Kolkata' date -v-1d '+%Y-%m-%d'
```

Use the IST date for the filename and all date references.

### The UTC Query Window (needed by Zoom and Wispr)

Both connectors take and return UTC ISO 8601 timestamps. Sreedeep is in Bangalore, IST = Asia/Kolkata = UTC+05:30. A full IST day converts to a UTC window that straddles two calendar dates.

```bash
# Full IST day for TARGET_DATE, expressed in UTC
TZ='Asia/Kolkata' date -d "$TARGET_DATE 00:00:00" -u '+%Y-%m-%dT%H:%M:%SZ'   # window start
TZ='Asia/Kolkata' date -d "$TARGET_DATE 23:59:59" -u '+%Y-%m-%dT%H:%M:%SZ'   # window end
```

Rule of thumb: IST day D runs from `D-1 18:30:00Z` to `D 18:29:59Z`. Compute it, never hardcode it.

Store these as `WINDOW_START_UTC` and `WINDOW_END_UTC`. Every Zoom and Wispr query in Step 3 uses them.

**Always convert timestamps back to IST before writing them into the note or the HTML report.** Never surface a raw `Z` timestamp to Sreedeep.

---

## Step 2: Read the Daily Note Template

Read `Other/Templates/Template - Daily Note.md` from the vault (if it exists) for any additional structure hints.

---

## Step 3: Gather Activity Data

### 3a. Obsidian Vault Activity, Markdown Notes

Find `.md` files modified in the past 24 hours:
```bash
find /path/to/Celsus -name "*.md" -mtime -1 -not -path "*/.obsidian/*" -not -path "*/.skills/*" -not -path "*/.local-plugins/*" -not -path "*/.git/*" | sort
```

If `-mtime -1` is too narrow (e.g., no files match), fall back to `-newer` using CLAUDE.md or the previous day's note.

Categorize as **created** vs. **modified**. Group by folder: Atlas/, Efforts/, Calendar/, Inbox/.

**Keep this file list.** Step 6.5 (BearDrive sync) reuses it as its input. Do not discard it after writing the vault-activity section.

### 3b. Non-Markdown Assets

```bash
find /path/to/Celsus -not -name "*.md" -not -path "*/.obsidian/*" -not -path "*/.DS_Store" -not -path "*/.git/*" -not -path "*/.skills/*" -not -path "*/.local-plugins/*" -mtime -1 | sort
```

Group by folder. If assets appear in `Atlas/Clients/` or `Atlas/Context Docs/`, flag them under **Sales Enablement / Deliverables**. This list also feeds Step 6.5.

### 3c. Cowork Session (this session)

Describe what was built, discussed, or decided. Include files created, decisions made, strategic changes, skill updates.

### 3d. Claude Code Sessions

1. Check for `.claude/` directories for session logs
2. Scan recently modified code files (`.py`, `.js`, `.ts`, `.sh`) as proxy
3. List modified files in `Atlas/Products/` as dev activity proxy
4. Always note: `*(Claude Code session logs not auto-captured, add manually or connect session export)*` for gaps

### 3e. Email

- If Outlook/email MCP is available: query past 24h emails, summarize threads
- If not: write `*(Outlook integration not available in current Cowork environment, email summary requires manual input)*`
- NEVER leave blank

### 3f. Meetings, Pass 1: Google Calendar (the skeleton)

Calendar gives the day's shape. Zoom and Wispr fill it with substance.

- If a Google Calendar MCP connector is available, query the day's events
  - For each meeting: name, time (IST), attendees
  - Create wikilinks to meeting notes if they exist in `Calendar/Meetings/`
- Wispr Flow also exposes calendar tools (`search_calendar_events`, `get_calendar_event`). Use these as a fallback when the Google Calendar connector is unavailable.
- If nothing is available: `*(Calendar integration pending)*`
- **Known correction:** Sreedeep is NOT in the InfraTech Weekly (4:30 PM). He IS in the Cirralogix/Recruit Champ Weekly (3:30 to 4:30 PM). Always verify meeting labels against this.
- NEVER leave blank

Build a working list of calendar events. This becomes the spine that Zoom and Wispr results attach to.

### 3g. Meetings, Pass 2: Zoom MCP (summaries, notes, recordings)

Zoom is the system of record for hosted meetings. Pull it every run.

**Before calling Zoom `search`:** the tool requires a known user time zone and refuses to infer one. Supply `Asia/Kolkata` explicitly in the request context. Never let it guess.

**Step 3g-1: find the day's meetings.**

Use the unified `search` tool with the `zoom_meeting` datasource, filtered to the UTC window from Step 1.

```
search(
  datasource_filters: [
    { datasource: "zoom_meeting",
      filters: { and: [ { gte: { key: "<start_time_field>", value: WINDOW_START_UTC } },
                        { lte: { key: "<start_time_field>", value: WINDOW_END_UTC } } ] } },
    { datasource: "calendar" }
  ],
  page_size: 50
)
```

Field names are not guessable. Call `search_describe_capabilities` FIRST to get the authoritative filterable field list for `zoom_meeting`, then build the filter tree from what it reports. If `search_describe_capabilities` fails, fall back to the legacy `search_meetings` tool with `from` and `to` set to the UTC window.

**Step 3g-2: pull assets per meeting.**

For each meeting found, call `get_meeting_assets`. Prefer the meeting UUID over the numeric ID: a numeric ID only returns the LATEST instance, which silently gives you the wrong data for recurring meetings like the Cirralogix weekly. The `meetingId` value must be double URL-encoded before the call or it fails.

`get_meeting_assets` returns, any of which may be null:

| Field | Use it for |
|-------|-----------|
| `meeting_summary` | AI recap, full text, and next steps. Primary source for the Key Takeaways column. |
| `my_notes` | Sreedeep's own in-meeting notes plus participant transcripts. Higher signal than the AI summary because it reflects what HE thought mattered. |
| `recording` | Play URL, duration, processing status |
| `whiteboards` / `docs` / `agenda_doc` | Link as deliverables if substantive |
| `participants` | Real attendance, which often differs from the calendar invite. Prefer this over the invite list. |

If `recording.processing` is true, note "recording still processing" rather than claiming it is missing.

**Step 3g-3: sweep for recordings the search missed.**

```
recordings_list(from: "YYYY-MM-DD", to: "YYYY-MM-DD", page_size: 100)
```

`recordings_list` takes plain UTC dates, not ISO timestamps, and the range caps at one month. Pass the UTC calendar dates spanned by the window (usually two). Any recording here that is not already in the meeting list is an unplanned or ad-hoc call. Flag those explicitly. They are usually the interesting ones.

**Step 3g-4: My Notes as a standalone capture layer.**

Zoom My Notes exist even for meetings Sreedeep did not host. Search the `zoom_canvas` datasource with `doc_type=notes` over the window, and pull bodies with `my_notes_get_note_content`. Treat any note not tied to a meeting in the list as a capture item, and route it through the stub flow in Step 3i.

**Optional synthesis:** for a dense meeting day (4+ meetings), the Zoom `ask` tool answers cross-meeting questions in one shot ("what did I commit to today", "what decisions were made"). Use it to seed the Ideas and Insights section, but never let `ask` output replace per-meeting takeaways. It compresses too aggressively for a record of the day.

**On failure:** state which step failed (`search`, `get_meeting_assets`, `recordings_list`) and continue with whatever Wispr and Calendar returned. Do NOT fail the whole run because Zoom auth expired.

### 3h. Meetings, Pass 3: Wispr Flow MCP (transcripts, action items)

Wispr Flow Meeting Recorder captures conversations including ones Zoom never saw: in-person meetings, phone calls, Meet/Teams calls. It is the verbatim layer.

**Step 3h-1: list the day's recorded meetings.**

```
search_meetings(since: WINDOW_START_UTC, until: WINDOW_END_UTC, limit: 50)
```

**Critical caveat:** `since` and `until` filter on MODIFIED time, not meeting start time. A meeting edited today will appear even if it happened last week, and a meeting from late last night may fall outside the window. Always check each result's actual `start` time against the target IST day, and discard or reassign anything that does not belong. Do not trust the filter alone.

Paginate while `has_more` is true, passing `next_cursor` verbatim. Do not stop at page one on a heavy day.

**Step 3h-2: pull content per meeting.**

For each meeting, call `get_meeting`:

```
get_meeting(meeting_id: "<id>", view_transcript: {})
```

- Pass `view_transcript: {}` whenever `has_transcript` is true. The `content` notes field is an auto-generated summary that drops details; the transcript is the source of truth. Derive takeaways from the transcript.
- Use `todos` for structured action items. These map DIRECTLY into the Tasks section as "New Today". This is the single highest-value field in the whole pipeline: the only source that reliably produces real commitments Sreedeep made out loud.
- Use `summary` (the Flow Summary, always returned in full) for the one-line takeaway in the Meetings table.
- Transcripts are character-bounded at 12000 by default. For a long call, follow the continuation offset in the truncation marker rather than accepting a partial read. Raise `char_limit` up to 40000 for dense strategic calls (Chief syncs, client negotiations, Longevity/Cadence sessions).

**Step 3h-3: attendees.**

`get_meeting` returns attendees without emails. When you need addresses to match a meeting to a client or prospect in the vault, call `get_meeting_attendee_emails` separately.

**On failure:** note the failure and fall back to Zoom plus Calendar only.

### 3i. Voice and Quick Capture: Wispr Scratchpad + Apple Notes + Zoom My Notes

Three capture layers, one processing flow. All of them are raw thought that has not been contextualized yet. The job is to pull them into the vault with enough context to be useful, not to dump them verbatim.

#### 3i-1. Wispr Flow scratchpad notes

```
search_scratchpad_notes(since: WINDOW_START_UTC, until: WINDOW_END_UTC, limit: 50)
```

Same modified-time caveat as meetings: verify each note actually belongs to the target day. Paginate on `has_more`.

For each note, call `get_scratchpad_note(note_id)`. Follow the continuation offset if the content truncates.

These are dictated notes, so expect transcription artifacts. Apply the standing name-normalization rules before writing anything to the vault:
- "Jreanoth" / "Jre", never "Dre" or "Jrenoth"
- "Champion InfoMetrics", never "champion informatics"
- "Gujarathi", with the h
- Watch for phantom names entirely. A transcript once invented a person named "Janath" who does not exist. If a name appears exactly once and matches nobody in `Atlas/People/`, flag it as unverified rather than creating a person note.

#### 3i-2. Apple Notes (via computer-use MCP)

Use `mcp__computer-use__request_access` to request access to the Notes app, then `mcp__computer-use__open_application` to open it. Screenshot to see the notes list. Navigate to notes created or modified in the past 24 hours. For each note, screenshot and read its full content. Scroll if needed.

```
1. mcp__computer-use__request_access  ["Notes"]
2. mcp__computer-use__open_application  "Notes"
3. mcp__computer-use__screenshot  see the notes list sorted by date
4. Click into each recent note, screenshot, read full content
5. Repeat for all notes modified today
```

**What to capture per note:** title (or first line if untitled), full content, approximate time, folder if not the default.

#### 3i-3. Zoom My Notes

Orphaned My Notes from Step 3g-4 (not attached to a meeting in the day's list) get processed here too.

#### Shared processing rules for all three layers

**Auto-linking:** Before creating the vault stub, scan content for mentions of known entities. Look for names, company names, product names, and project terms that match vault entries. Add `[[wikilinks]]` automatically. Common candidates from: `Atlas/People/`, `Atlas/Companies/`, `Atlas/Clients/`, `Atlas/Products/`, `Efforts/Active/`.

**Two-mode operation based on whether user is present:**

**Mode A, Interactive (user present, on-demand run).** After capturing all notes, ask Sreedeep about each one before creating the vault stub. Keep questions focused, 2 to 3 per note maximum. The goal is to understand context and intent, not to transcribe.

Good questions:
- "This note says [brief quote], was this from a meeting, a random idea, or something you need to act on?"
- "Should this become a permanent vault note, or is it a one-time capture?"
- "Any follow-up tasks from this?"

After getting answers, create the vault stub immediately with the full context baked in. Mark status as `processed`.

**Mode B, Automated (scheduled run, user not present).** Create the vault stub from inferred context. Embed open questions directly in the stub so the morning routine can surface them:

```
> NEEDS CONTEXT: [specific question about this note]
> Flag for morning routine
```

List each unresolved note in the Capture Inbox section of the daily note so the morning routine knows to ask about it.

**Vault stub paths (one folder per source, so provenance survives):**

| Source | Path |
|--------|------|
| Apple Notes | `Inbox/Apple Notes/YYYY-MM-DD - {title}.md` |
| Wispr Flow scratchpad | `Inbox/Wispr Flow/YYYY-MM-DD - {title}.md` |
| Zoom My Notes (orphaned) | `Inbox/Zoom Notes/YYYY-MM-DD - {title}.md` |

**Vault stub format:**

```markdown
---
type: capture-note
captured: "YYYY-MM-DD"
source: Apple Notes | Wispr Flow | Zoom My Notes
source-id: "{note_id or meeting_id, so the note can be traced back}"
status: needs-context
tags:
  - inbox
  - {apple-note | wispr-note | zoom-note}
---

# {Note Title}

> Captured from {source} on YYYY-MM-DD at HH:MM IST.

{Full note content with auto-added wikilinks}

---

## Context and Next Steps

**Sreedeep's context:** (fill in after morning routine)

> NEEDS CONTEXT: {specific question}

**Suggested action:**
- [ ] {inferred task or "clarify intent in morning routine"}

**Possible connections:** {wikilinks to related vault entities}
```

**If a capture source is inaccessible:**
- Note it in the daily note: `{Source}: access failed, notes pending manual capture`
- Add a carried-forward task: `[ ] Manually review {source} from [date] and add to Inbox/`
- Do NOT leave the section blank

### 3j. Meeting Reconciliation (run after 3f, 3g, 3h)

Calendar, Zoom, and Wispr will all report the same meeting. Merge before writing, or the note reads like the day had three times as many meetings as it did.

**Match rule:** same meeting if EITHER
- the linked calendar event ID matches, OR
- start times are within 15 minutes AND the attendee sets or topics overlap

**Merge precedence, per field:**

| Field | Winner | Why |
|-------|--------|-----|
| Title, scheduled time | Google Calendar | Canonical naming |
| Actual attendance | Zoom `participants` | Reflects who actually showed |
| Key takeaways | Wispr transcript, then Zoom `meeting_summary` | Verbatim beats generated |
| Action items | Wispr `todos`, merged with Zoom summary next steps | Union, then dedupe |
| Sreedeep's own emphasis | Zoom `my_notes` | What HE flagged in the moment |
| Recording link | Zoom `recording.play_url` | Only Zoom has it |

Always record which sources contributed. The Meetings table carries a Source column so a thin entry is visibly thin rather than looking like a quiet meeting.

**Meetings with no coverage at all** (on the calendar, nothing from Zoom or Wispr) get flagged: `no recording or transcript captured`. That gap is itself worth reporting, especially for external meetings.

### 3k. Active Efforts

Read all files in `Efforts/Active/` and report current status. Pay attention to:
- Primary Build efforts (Champmail Build, ChampGraph Build)
- On-Hold efforts (ChampIQ, back burner)
- Effort age (days since last update)

Cross-reference against the day's meetings and action items. If a Wispr `todo` or Zoom next-step maps to an active effort, note it in that effort's "what changed today" rather than stranding it in the Tasks section alone.

---

## Step 4: Compile the Daily Note

### Section Structure (Gold Standard)

The daily note has TWO possible configurations:

#### A) Full Day (morning plan already exists, MERGE mode)

If a morning routine already created the note with time blocks, top 3, context, etc.:
- **Preserve all morning content exactly as written**
- Add `## Evening Recap, Auto-Generated (HH:MM IST)` as a divider
- Below that divider, add all the evening sections

#### B) Standalone Recap (no morning plan)

Create the note from scratch with all sections.

### Required Sections

```
Day at a Glance
Claude and Cowork Sessions
Claude Code Sessions
Email and Communications
Meetings                             (Calendar + Zoom + Wispr, reconciled)
Meeting Intelligence                 (transcript-derived decisions and commitments)
Active Efforts Progress
Sales Enablement and Deliverables    (only if deliverable assets exist)
Capture Inbox                        (always present: Wispr, Apple Notes, Zoom My Notes)
Obsidian Vault Activity
Ideas and Insights
Tasks
Tomorrow's Focus
Appendix: Raw Activity Log
```

### Section Guidance (Minimum Quality Bar)

**Day at a Glance:**
- Energy level + label (high / medium / low)
- Focus mode (Deep Dive, Multi-Track, Reactive)
- Available hours + meeting count
- Top accomplishment in bold
- If morning plan exists: include the Time Blocks table + Today's Top 3

**Claude and Cowork Sessions:**
- Table: Session | Summary | Artifacts Created
- Decisions Made, bulleted list of strategic decisions
- Files Created / Modified, every file touched with brief description

**Claude Code Sessions:**
- Separate from Cowork
- Products being developed, files changed if detectable
- Flag when logs are unavailable

**Email and Communications:**
- Outlook NOT currently available in Cowork environment
- Always note this status explicitly
- If user manually shared email context during the day, capture it here

**Meetings:**

Table: `Meeting | With | Time (IST) | Key Takeaways | Source`

- Source column values: `Cal`, `Zoom`, `Wispr`, or combinations like `Cal+Zoom+Wispr`
- Link the Zoom recording play URL on the meeting name when one exists
- Action item checkboxes below the table, sourced from Wispr `todos` merged with Zoom next-steps
- Attendance from Zoom `participants` when available, not the invite list
- IMPORTANT: Sreedeep attends Cirralogix/Recruit Champ Weekly at 3:30 to 4:30 PM (NOT InfraTech Weekly)
- Meetings with no recording or transcript: flag explicitly

**Meeting Intelligence:**

This is what the transcripts bought us, and the reason the connectors are wired in at all. Keep it tight, this is signal not transcript.

```
Meeting Intelligence

Meetings recorded: N of M | Transcripts available: N | Action items extracted: N

Decisions Made Today
- {decision} ({meeting}, {who decided})

Commitments Sreedeep Made
- [ ] {commitment} ({meeting}, due {date if stated})

Commitments Made To Sreedeep
- {person} owes {what} ({meeting}, by {date if stated})

Quotes Worth Keeping
> "{verbatim line that changes something}" ({speaker}, {meeting})
```

Pull commitments from the transcript directly, not just the summary. Summaries routinely drop the "I'll get that to you by Thursday" line that matters most. If a commitment has a date, it becomes a dated task. If it does not, flag it as undated and let the morning routine chase it.

**Active Efforts Progress:**
- Table: Effort | What Changed Today | Status
- Always include Primary Build efforts (Champmail Build, ChampGraph Build) at top
- Note days since last update if stale
- Link meeting-sourced changes back to their meeting

**Sales Enablement and Deliverables:**
- Only include if deliverable assets were created
- Table: Asset | Format | For Whom | Purpose
- Include Zoom whiteboards and Zoom Docs from `get_meeting_assets` when substantive

**Capture Inbox:**

ALWAYS present. It tells Sreedeep and the morning routine exactly what was found and what still needs input, across all three capture layers.

```
Capture Inbox

| Source | Found | Auto-linked | Needs context |
|--------|-------|-------------|---------------|
| Wispr Flow scratchpad | N | N entities | N |
| Apple Notes | N | N entities | N |
| Zoom My Notes | N | N entities | N |

| Note | Source | Preview | Vault Stub | Status |
|------|--------|---------|------------|--------|
| title | Wispr | first 10 words | Inbox/Wispr Flow/YYYY-MM-DD - title | Processed / Needs context |

Notes Needing Your Context (morning routine will surface these):

1. Note title (source) - first line preview
   - QUESTION: specific question about this note
   - Possible connection: related vault entity if detected
```

If a source found nothing or access failed: state why plus add a carried-forward task. Zero found is a valid, reportable result. Missing entirely is not.

**Obsidian Vault Activity:**
- Notes created + notes modified + links added
- Include both .md and non-.md assets
- Note vault structure health (orphans, weak links if known)

**Ideas and Insights:**
- Emerging themes, product ideas, connections noticed
- New prospects/clients that should be added to vault
- Cross-meeting patterns: if the same objection, blocker, or name surfaced in 2+ meetings today, say so. That pattern is invisible in any single transcript and is the main reason to read them together.

**Tasks, THREE required subsections (non-negotiable):**
1. Completed Today, everything that got done
2. Carried Forward, unchecked from previous days; nothing gets silently dropped
3. New Today, new items surfaced from today's work, including every Wispr `todo` and every Zoom next-step

Always carry forward incomplete tasks from yesterday's daily note. Dedupe against the Meeting Intelligence commitments so an item does not appear twice.

**Tomorrow's Focus:**
- Top 3 only. Specific and actionable. Not vague.
- Format: bold title + one sentence of context
- Weight toward dated commitments surfaced from transcripts. A promise made out loud outranks a vague intention.

**Appendix:**
- Machine-generated raw timeline
- Session timestamps (IST)
- Files modified list
- Meeting IDs and UUIDs for traceability (Zoom UUID, Wispr meeting_id) so any claim can be traced back to source
- Integration status tracker (always present):

```
Email (Outlook):        not available in Cowork
Google Calendar:        connected / pending
Zoom MCP:               connected, N meetings / N assets / N recordings   |  auth failed  |  not loaded
Wispr Flow MCP:         connected, N meetings / N transcripts / N notes   |  auth failed  |  not loaded
Apple Notes:            N notes captured / N need context / access failed
WhatsApp:               pending
Claude Code sessions:   manual only
BearDrive sync:         N synced / N pending / N failed / N review  |  CLI not wired  |  SOP missing
```

---

## Step 5: Write the Vault Note

**Path:** `Calendar/Daily Notes/YYYY-MM-DD.md` (flat format)

**If file exists:** MERGE. Do NOT overwrite morning plan content. Append evening recap below the divider.

**If file does not exist:** Create fresh using full section structure.

### Frontmatter

```yaml
---
type: daily-note
date: "YYYY-MM-DD"
energy:
mood:
meetings-recorded:    # e.g. "4 of 6 recorded, 3 transcripts"
captures:             # e.g. "wispr 3, apple 2, zoom 1 | 4 pending context"
tags:
  - daily
  - [day-of-week]
  - [dominant topic tags]
---
```

### Navigation Links (always at bottom)

```
Previous: [[YYYY-MM-DD]] - Next: [[YYYY-MM-DD]]
Hub: [[Home]] - [[Efforts MOC]]
```

---

## Step 6: Generate the HTML Executive Report

**This step is MANDATORY.** Every daily note MUST also produce a visual HTML report.

### Output Path
`Calendar/Daily Notes/Daily_Report_YYYY-MM-DD.html`

### Design Requirements, Lake B2B Brand

#### Colors
| Element | Color | Hex |
|---------|-------|-----|
| Header gradient (left) | Gold | #FFB703 |
| Header gradient (mid) | Red | #E8033A |
| Header gradient (right) | Purple | #6D08BE |
| Body background | Light gray | #F8F9FA |
| Card background | White | #FFFFFF |
| Card shadow | | 0 2px 8px rgba(0,0,0,0.08) |
| Body text | Near-black | #1A1A2E |
| Header text | White | #FFFFFF |
| Section title text | Purple | #6D08BE |
| Status: Critical | Red | #E8033A |
| Status: Active | Orange | #FF6903 |
| Status: In Dev | Teal | #0095A0 |
| Status: Draft | Gold | #FFB703 |
| Status: On Hold | Lavender | #7A76DA |
| Status: Complete | Green | #28a745 |
| Accent/badge bg | Purple (10% opacity) | rgba(109,8,190,0.1) |

#### Typography
- Font: Montserrat (Google Fonts: https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap)
- Fallback: Arial, sans-serif
- Header name: Extra Bold (800), 28px
- Header subtitle: Light (300), 14px
- Section titles: Semi Bold (600), 16px, uppercase, letter-spacing 1px
- Body: Regular (400), 14px, line-height 1.6
- Small text: 12px

#### Layout
- Mobile-first CSS. The manager reads this on a phone. Single-column, max-width 700px, centered, padding 40px 20px on desktop, 20px 12px on mobile.
- Cards: white background, border-radius 12px, padding 24px, margin-bottom 16px
- Gradient header bar: border-radius 12px 12px 0 0, padding 32px
- Stats row: 3 equal-width stat boxes in a flexbox row, wrapping on narrow screens
- Tables: full-width, subtle borders, alternating row colors, horizontally scrollable on mobile
- Status badges: inline-block, rounded pill, 10px padding, colored bg
- All CSS in a style tag in the head, no external CSS files
- Text on the gradient header must be explicitly white and not overridden by a parent rule

### Report Sections (Distilled from Vault Note)

1. **Header Banner:** Lake B2B gradient, Sreedeep's name, date, energy badge, focus mode
2. **Day at a Glance:** Top accomplishment (hero text) + stat cards: hours, meetings, tasks completed
3. **Today's Top 3:** Numbered list, bold titles, checkmark if completed
4. **Meetings:** Clean table: time (IST), name, 1-line takeaway, small source chip (Zoom / Wispr / Cal). Recording link on the name where one exists.
5. **Decisions and Commitments:** Distilled from Meeting Intelligence. Two compact columns: "Decided today" and "I owe / owed to me". This is the section the manager actually reads. Six lines maximum, hardest-hitting first.
6. **Effort Status:** Each effort as a card with color-coded status badge + 1-line "what changed"
7. **Capture Inbox:** Mini-card, one row per source: N captured, N processed, N need context. Compact, a signal not a transcript.
8. **Deliverables:** If any, table with file name, format, recipient
9. **Tasks Summary:** Three stat cards: Completed (green), Carried Forward (orange), New (purple)
10. **Tomorrow's Focus:** Top 3, numbered, bold
11. **Footer:** "Generated at HH:MM IST . Celsus Vault . Lake B2B" + subtle gradient line + a one-line integration status strip in 11px gray so gaps are visible without dominating

---

## Step 6.5: BearDrive Knowledge Sync (MANDATORY, runs every night)

BearDrive is Sreedeep's curated knowledge space for agents: the drive that Champ Workspace and other agents read for context. This step curates the day's documents into it so Sreedeep never has to think about keeping his agent knowledge base current.

**The SOP is the law:** read `Atlas/Ops/BearDrive/BearDrive Sync SOP.md` at the start of this step. It owns the curation rules (what goes up, hard exclusions, folder mapping), the config block, and any changes Sreedeep makes to the policy. This skill step executes the SOP; it never overrides it. If the SOP and this section ever disagree, the SOP wins.

**Flow:**

1. **Input:** reuse the changed-file lists from Steps 3a and 3b. Never run a second vault scan.
2. **Filter** through the SOP's curation rules. Include classes (client docs, context docs, MOCs, the day's daily note, meeting notes, active efforts, ops SOPs). Apply hard exclusions ruthlessly: credentials or anything matching `*login*`/`*password*`/`*credential*`, the Vendor Anonymization Key, `Atlas/Me/`, `#private`-tagged notes, signed contracts/NDAs, media over 5 MB, codebases, HTML exec reports. When unsure about a file, stage it as `review`, do not upload it.
3. **Write the manifest** to `Atlas/Ops/BearDrive/Sync Log/YYYY-MM-DD.md`: one table row per candidate with local path, remote path (per the SOP folder mapping), and status (`synced` / `pending` / `failed` / `review`).
4. **Check the config** block in the SOP. If `wired: false` (or the SOP/config is missing), mark all candidates `pending: CLI not wired`, note it in the integration tracker, and move on. Do not fail the recap run over BearDrive.
5. **If `wired: true`:** run the configured `upload_cmd` template per file via shell (substituting `{local_path}` and `{remote_path}` under the configured `root`). Capture output. Mark `synced` or `failed` with the error text. Also sweep prior manifests for `pending` rows and sync the backlog (idempotent: same file, same remote path, latest wins).
6. **Report** one line in the daily note Appendix integration tracker and in the exec summary: `BearDrive: N synced, N pending, N failed, N for review`. Files marked `review` get listed in the Capture Inbox needs-context flow so the morning routine surfaces them.

**Failure posture:** BearDrive problems never block the daily note or the HTML report. Log, flag, carry forward.

---

## Step 7: Summary for Sreedeep

After all outputs are created, provide a short bullet-point summary:
- What is in the vault note (sections, data sources used)
- What is in the HTML report (link to file)
- Meeting coverage: N meetings, N recorded by Zoom, N transcribed by Wispr, N with no coverage
- Capture status: how many from each source, how many processed, how many need morning context
- BearDrive sync: N synced / pending / failed / review, and whether the CLI is wired yet
- Any flags (stale efforts, missing meeting notes, connector failures, new prospects to track)

---

## Key Vault Paths

| Path | What |
|------|------|
| `Calendar/Daily Notes/` | Daily notes (markdown) |
| `Calendar/Daily Notes/Daily_Report_YYYY-MM-DD.html` | HTML exec reports |
| `Calendar/Meetings/` | Meeting notes |
| `Inbox/Apple Notes/` | Apple Notes vault stubs |
| `Inbox/Wispr Flow/` | Wispr Flow scratchpad note stubs |
| `Inbox/Zoom Notes/` | Orphaned Zoom My Notes stubs |
| `Other/Templates/Template - Daily Note.md` | Template |
| `Efforts/Active/` | Active efforts |
| `Atlas/Products/` | Product notes |
| `Atlas/People/` | People |
| `Atlas/Context Docs/` | Context docs |
| `Atlas/Ops/BearDrive/BearDrive Sync SOP.md` | BearDrive curation rules + CLI config (owns Step 6.5 policy) |
| `Atlas/Ops/BearDrive/Sync Log/` | Nightly BearDrive sync manifests |

## Known Corrections (Hardcoded, Update as needed)

- Time zone: Sreedeep is in Bangalore, IST (Asia/Kolkata, UTC+05:30). Zoom `search` requires this be supplied explicitly and will refuse to infer it. Wispr returns UTC and must be converted before display.
- Meetings: Sreedeep is NOT in InfraTech Weekly (4:30 PM). He IS in Cirralogix/Recruit Champ Weekly (3:30 to 4:30 PM). Never prep or attend InfraTech Weekly.
- Email: Outlook integration is NOT available in Cowork. Always note this.
- ChampIQ: On back burner (as of 2026-03-16). Primary build: Champmail + ChampGraph in parallel.
- ChampVoice: MVP live, maintain only.
- Cirralogix + Recruit Champ: Deep Focus, Sreedeep is deeply involved, weekly 3:30 to 4:30 PM meeting.
- Apple Notes: Access requires computer-use MCP. If blocked, note the failure and add a carried-forward task.
- Zoom `get_meeting_assets`: prefer UUID over numeric ID for recurring meetings, and double-encode the ID.
- Wispr `since`/`until`: filters on modified time, not start time. Always verify actual meeting start against the target day.
- Both Zoom and Wispr expose a tool named `search_meetings`. Disambiguate by server prefix.
- Dictated notes carry transcription artifacts. Normalize: "Jreanoth" not "Dre"; "Champion InfoMetrics" not "champion informatics"; "Gujarathi" with the h. Flag single-occurrence unknown names as unverified rather than creating person notes.
- Vendor names (not client names) are anonymized as Vendor A/B/C in any team-facing output. Key at `Atlas/Ops/Vendor Anonymization Key.md`.
- No em dashes in any output, vault note or HTML.
- BearDrive: the Sync SOP in the vault owns curation policy and CLI config. Until `wired: true` in its config block, Step 6.5 stages manifests only. Never upload anything on the hard-exclusion list, and never let a BearDrive failure block the recap.

## Quality Benchmark

What makes a good daily note:
1. Morning plan with time blocks preserved (if exists)
2. Evening recap cleanly separated with an Evening Recap divider
3. Every section populated, even if noting "pending integration"
4. Tasks have clear Completed / Carried Forward / New Today separation
5. Decisions captured explicitly, not buried
6. Files created listed with one-line descriptions
7. Tomorrow's focus is specific and actionable, not vague
8. Effort status includes "what changed today", not just current state
9. Ideas section connects dots across the day's activity, including cross-meeting patterns
10. Appendix has machine-readable raw data + integration status tracker + meeting IDs for traceability
11. HTML report generated and saved alongside the vault note
12. Capture Inbox section present with all three sources listed, even at zero
13. Capture stubs created in the right per-source Inbox folder with wikilinks and embedded questions
14. Meetings table carries a Source column so coverage gaps are visible
15. Meeting Intelligence separates decisions, Sreedeep's commitments, and commitments owed to him
16. Every timestamp shown in IST, never raw UTC
17. Every meeting-derived claim traceable to a Zoom UUID or Wispr meeting_id in the Appendix
18. BearDrive sync ran (or staged): manifest written to `Atlas/Ops/BearDrive/Sync Log/`, one-line status in the Appendix tracker and the exec summary, zero hard-exclusion files ever uploaded

## Iteration Log

| Date | Change | Why |
|------|--------|-----|
| 2026-03-04 | Initial skill created | First daily note |
| 2026-03-08 | Fix 1: Timezone bug (IST) | Notes were dated wrong due to UTC default |
| 2026-03-10 | Fix 2: Non-markdown asset scan | PDFs/DOCXs were being missed |
| 2026-03-10 | Fix 3: Google Calendar section always present | Blank sections were confusing |
| 2026-03-10 | Fix 4: Email section always present | Same as above |
| 2026-03-10 | Fix 5: Claude Code section always present | Dev work was getting lost |
| 2026-03-12 | Fix 6: Sales Enablement section | Deliverables had no home |
| 2026-03-16 | v2: Gold standard established | Mar 16 note set as quality benchmark |
| 2026-03-16 | v2: HTML executive report added | Manager needs a visual daily summary |
| 2026-03-16 | v2: Lake B2B branding for HTML | Consistent brand identity in reports |
| 2026-03-16 | v2: Known corrections hardcoded | Meeting/effort errors kept recurring |
| 2026-03-16 | v2: Three-part task section mandated | Carried forward tasks were getting lost |
| 2026-03-16 | v2: Outlook limitation documented | Stop saying "pending", it is not available |
| 2026-03-26 | v3: Apple Notes integration | Quick-capture notes now flow into vault automatically |
| 2026-03-26 | v3: Two-mode Apple Notes operation | Interactive when user present, deferred questions when automated |
| 2026-03-26 | v3: Inbox/Apple Notes/ vault path added | Standardized landing zone for captured notes |
| 2026-03-26 | v3: Morning routine hook via embedded questions | NEEDS CONTEXT prompts in stubs surface at morning routine |
| 2026-08-20 | v4: Zoom MCP wired in (Step 3g) | Meetings section was calendar-only; AI summaries, My Notes, participants and recordings were sitting unused |
| 2026-08-20 | v4: Wispr Flow MCP wired in (Step 3h) | Transcripts and structured todos are the only reliable source of commitments actually made out loud |
| 2026-08-20 | v4: Step 0 connector preflight added | Deferred tools were silently absent, producing empty meeting sections with no explanation |
| 2026-08-20 | v4: IST to UTC window computation (Step 1) | Both connectors query in UTC; an IST day straddles two UTC dates and was clipping meetings |
| 2026-08-20 | v4: Meeting reconciliation rule (Step 3j) | Calendar + Zoom + Wispr triple-counted the same meeting |
| 2026-08-20 | v4: Meeting Intelligence section added | Decisions and commitments were buried inside per-meeting takeaways |
| 2026-08-20 | v4: Apple Notes section generalized to Capture Inbox | Three capture layers now, not one |
| 2026-08-20 | v4: Per-source Inbox folders | Provenance was lost once Wispr and Zoom notes joined Apple Notes |
| 2026-08-20 | v4: Meeting IDs recorded in Appendix | Transcript-derived claims need to be traceable back to source |
| 2026-08-20 | v4: Wispr modified-time caveat documented | since/until filter on modified, not start, silently pulling stale meetings into the day |
| 2026-09-01 | v5: BearDrive Knowledge Sync added (Step 6.5) | BearDrive is the curated agent knowledge space; daily docs now flow up automatically so Sreedeep never curates by hand |
| 2026-09-01 | v5: Sync SOP as external policy source | Curation rules and CLI config live in the vault (Atlas/Ops/BearDrive/), editable without touching the skill |
| 2026-09-01 | v5: Stage-then-wire posture | CLI not yet configured; manifests accumulate as a backlog that syncs in full on first wired run |
