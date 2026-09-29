---
name: weekly-review
description: >
  Gamified weekly review skill that aggregates Mon-Fri daily notes from Celsus vault, runs an
  interactive quiz for subjective reflection, then produces THREE outputs: (1) a vault weekly
  review note, (2) an RPG-styled Lake B2B branded HTML report with XP, levels, and character
  classes, and (3) an email to Sundar via Outlook. Runs Saturday 00:30 IST or on demand.
  MANDATORY TRIGGER for: "weekly review", "weekly recap", "week in review", "what did I do this
  week", "weekly report", "send weekly update", "gamified review", "XP report", "level up",
  "weekly summary", "end of week", "friday recap", "review my week", or any request involving
  summarizing a full week of activity. Also trigger when the user mentions wanting to reflect
  on the week, track weekly progress, or generate a report for Sundar. This skill coordinates
  with daily-note-recap (reads its outputs) and interactive-quiz (for the reflection quiz).
---

# Weekly Review -- Vault Note + Gamified HTML + Email to Sundar

> **Purpose:** Every week, generate THREE outputs:
> 1. An Obsidian vault weekly review note (`Calendar/Weekly Reviews/YYYY-WXX.md`)
> 2. A gamified RPG-styled HTML report with [[Lake B2B]] branding
> 3. An email to Sundar (reporting manager) via Outlook with the HTML report
>
> **Schedule:** Saturday 00:30 IST (covering Monday-Friday)
> **On demand:** "weekly review", "weekly recap", "review my week", etc.

---

## Pipeline Overview

The skill runs a three-phase pipeline. Each phase must complete before the next begins.

```
Phase 1: Interactive Quiz (user reflection)
    |
    v
Phase 2: Data Aggregation (read daily notes Mon-Fri)
    |
    v
Phase 3: Output Generation
    ├── 3a: Vault Note (Calendar/Weekly Reviews/YYYY-WXX.md)
    ├── 3b: Gamified HTML Report (RPG + Lake B2B brand)
    └── 3c: Email to Sundar via Outlook
```

---

## Step 0 -- Determine Week Boundaries (IST)

Always use IST. The skill covers the most recent Monday-Friday.

```bash
# Get current IST date
TODAY=$(TZ='Asia/Kolkata' date '+%Y-%m-%d')

# Find the Monday and Friday of the target week
# If today is Saturday (running at 00:30 IST), the week just ended
DOW=$(TZ='Asia/Kolkata' date '+%u')  # 1=Monday, 6=Saturday, 7=Sunday

# Calculate Monday of target week
if [ "$DOW" -le 5 ]; then
  # Weekday: go back to this Monday
  MONDAY=$(TZ='Asia/Kolkata' date -d "$TODAY - $((DOW - 1)) days" '+%Y-%m-%d')
else
  # Weekend: go back to last Monday
  MONDAY=$(TZ='Asia/Kolkata' date -d "$TODAY - $((DOW - 1)) days" '+%Y-%m-%d')
fi
FRIDAY=$(TZ='Asia/Kolkata' date -d "$MONDAY + 4 days" '+%Y-%m-%d')

# ISO week number
WEEK_NUM=$(TZ='Asia/Kolkata' date -d "$MONDAY" '+%V')
YEAR=$(TZ='Asia/Kolkata' date -d "$MONDAY" '+%Y')
```

Use `MONDAY` through `FRIDAY` for all daily note lookups. The vault note filename uses `YYYY-WXX` format.

---

## Phase 1 -- Interactive Reflection Quiz

Generate a beautiful, dark-themed interactive HTML quiz using the interactive-quiz skill patterns. This quiz captures Sreedeep's subjective read on the week before the data aggregation begins.

### Quiz Specifications

**File:** Save to `Calendar/Weekly Reviews/Weekly_Quiz_YYYY-WXX.html`
**Layout:** Scrollable (5 questions, all visible)
**Theme:** Dark background with Lake B2B accent colors

#### Questions and Interaction Patterns

| # | Question | Pattern | Priority | Details |
|---|----------|---------|----------|---------|
| 1 | "How did your energy flow this week?" | **Gradient Slider x5** | Critical | Five sliders, one per day (Mon-Fri). Labels: "Drained" (0) to "On Fire" (10). Each slider uses the Lake B2B gradient for the fill track. |
| 2 | "What were your proudest wins this week?" | **Tag Builder** | Critical | Type + Enter to add wins as removable pill tags. No limit. Placeholder: "Type a win and press Enter..." |
| 3 | "What blocked you or slowed you down?" | **Priority Ranking Tiles** | Important | Pre-populate tiles from effort names detected in daily notes (read them first). Add "Custom..." tile for free-form entry. Tap-to-cycle: Skip / Major Blocker / Minor Friction. |
| 4 | "Rate your week across these dimensions" | **Heat Map Grid** | Important | Rows: Strategy, Product, Sales, Marketing, Ops. Columns: Impact, Time Spent, Satisfaction. Tap cells to cycle intensity 0-4. Color coding: 0=empty, 1=gold, 2=orange, 3=red, 4=purple. |
| 5 | "Top 3 priorities for next week?" | **Styled Textarea** | Critical | Three separate text inputs with floating labels: "Priority 1", "Priority 2", "Priority 3". Glow-on-focus with purple accent. |

#### Quiz Output

When "Generate Summary" is clicked, compile state into a JSON block displayed in a copyable summary panel. The JSON structure:

```json
{
  "week": "YYYY-WXX",
  "energy_arc": [7, 8, 5, 6, 9],
  "energy_avg": 7.0,
  "wins": ["Launched Champmail", "Closed VertexGrid deal"],
  "blockers": {
    "major": ["Stalwart SMTP config issues"],
    "minor": ["Meeting overload on Wednesday"],
    "skipped": ["Budget approval delay"]
  },
  "dimensions": {
    "strategy":  {"impact": 3, "time": 2, "satisfaction": 3},
    "product":   {"impact": 4, "time": 4, "satisfaction": 3},
    "sales":     {"impact": 2, "time": 2, "satisfaction": 2},
    "marketing": {"impact": 3, "time": 3, "satisfaction": 3},
    "ops":       {"impact": 1, "time": 1, "satisfaction": 2}
  },
  "next_week_priorities": [
    "Ship ChampGraph MVP",
    "Close Unibuild proposal",
    "Prep Q1 board deck"
  ]
}
```

After the user completes the quiz and copies the summary (or the skill reads the HTML file programmatically), proceed to Phase 2.

**Implementation note:** If running as a scheduled task (no user present), skip Phase 1 and use defaults: energy from daily note frontmatter, no wins/blockers/dimensions (mark as "Quiz skipped - scheduled run"), no next-week priorities.

---

## Phase 2 -- Data Aggregation

Read all daily notes for Mon-Fri of the target week and extract structured data.

### 2a. Daily Notes Collection

```bash
VAULT="/path/to/Celsus"
for d in $(seq 0 4); do
  DATE=$(TZ='Asia/Kolkata' date -d "$MONDAY + $d days" '+%Y-%m-%d')
  echo "Checking: $VAULT/Calendar/Daily Notes/$DATE.md"
done
```

Read each daily note that exists. Some days may not have notes (weekends, missed days). Track which days have notes and which are missing.

### 2b. Data Extraction (per daily note)

From each daily note, extract:

| Data Point | Source Section | How |
|------------|---------------|-----|
| Energy level | Frontmatter `energy:` field | Map: high=9, medium=6, low=3 |
| Focus mode | Frontmatter `focus:` or Day at a Glance | Text extraction |
| Tasks completed | `[x]` checkboxes across all sections | Count + list |
| Tasks carried forward | `[ ]` checkboxes from Tasks section | Count + list |
| Tasks new | New Today subsection | Count + list |
| Meetings | Meetings section table | Name, attendees, takeaways |
| Efforts status | Active Efforts Progress table | Effort name, status, what changed |
| Deliverables | Sales Enablement section | Asset name, format, recipient |
| Decisions | Claude & Cowork Sessions > Decisions Made | Bulleted list |
| Ideas | Ideas & Insights section | Bulleted list |
| Tomorrow's focus | Tomorrow's Focus section | Top 3 items |
| Vault files modified | Vault Activity section | Count + categorization |

### 2c. Weekly Aggregation

Combine all daily extractions into weekly totals:

```
weekly_data = {
  days_with_notes: 5,
  days_missing: [],

  // Cumulative counts
  tasks_completed_total: sum of daily [x],
  tasks_carried_forward: final day's carry-forward list,
  tasks_new_total: sum of daily new,

  // Meetings
  meetings_total: count,
  meetings_list: [{day, name, attendees, takeaway}],

  // Efforts
  efforts_progressed: efforts whose status changed during the week,
  efforts_stale: efforts with no change,
  efforts_completed: efforts marked complete,

  // Deliverables
  deliverables: [{day, asset, format, recipient}],

  // Decisions
  decisions: [{day, decision}],

  // Ideas
  ideas: [{day, idea}],

  // Vault health
  files_created: count,
  files_modified: count,
  links_added: count (if detectable)
}
```

### 2d. XP Calculation

Read `references/rpg-config.md` for the full XP system. Calculate weekly XP:

| Action | XP | Count | Total |
|--------|----|-------|-------|
| Task completed | +10 | tasks_completed_total | ... |
| Meeting attended | +15 | meetings_total | ... |
| Effort advanced | +25 | efforts_progressed count | ... |
| Deliverable shipped | +30 | deliverables count | ... |
| Decision made | +20 | decisions count | ... |
| Daily note written | +5 | days_with_notes | ... |
| Weekly review streak | +50 | if consecutive | ... |

**Persistent XP log:** Read and update `Calendar/Weekly Reviews/weekly_xp_log.json`:

```json
{
  "history": [
    {"week": "2026-W11", "xp": 340, "level": 3, "class": "Build Beast", "cumulative_xp": 1240},
    {"week": "2026-W12", "xp": 280, "level": 4, "class": "Strategy Sage", "cumulative_xp": 1520}
  ],
  "current_streak": 2
}
```

Calculate level from cumulative XP (see `references/rpg-config.md` for thresholds).

### 2e. Character Class Determination

Determine the dominant activity based on the week's data:

| Class | Condition |
|-------|-----------|
| **Strategy Sage** | >40% of decisions + effort changes are strategy-tagged |
| **Build Beast** | >40% of activity is product/dev work |
| **Deal Closer** | >40% of activity is sales-related |
| **Growth Hacker** | >40% of activity is marketing-related |
| **Ops Commander** | >40% of activity is ops-related |
| **Multi-Class** | No single category >40% |

Use the dimension heat map from the quiz (if available) as the primary signal. Fall back to counting meeting types and effort categories from daily notes.

---

## Phase 3a -- Vault Weekly Review Note

**Path:** `Calendar/Weekly Reviews/YYYY-WXX.md`

Create the directory if it does not exist:
```bash
mkdir -p "$VAULT/Calendar/Weekly Reviews"
```

### Frontmatter

```yaml
---
type: weekly-review
week: "WXX"
year: YYYY
date_range: "YYYY-MM-DD to YYYY-MM-DD"
energy_avg: X.X
xp_earned: XXX
cumulative_xp: XXXX
level: X
class: "Build Beast"
streak: X
tags:
  - weekly
  - review
  - WXX
---
```

### Section Structure

```markdown
# Weekly Review -- Week XX (Mon Date - Fri Date, YYYY)

## Week at a Glance
- **Class:** [Character Class] | **Level:** X | **XP Earned:** +XXX
- **Energy Average:** X.X/10 | **Days Active:** X/5
- **Top Achievement:** [single most impactful thing from the week]

## Wins
[From quiz + auto-detected completions]
- Win 1
- Win 2

## Effort Progress
| Effort | Monday Status | Friday Status | Change | Key Moment |
|--------|--------------|---------------|--------|------------|
| [[Champmail Build]] | In Progress | Launched | Advanced | Stalwart config complete |

## Meetings Summary
| Day | Meeting | Key Takeaway |
|-----|---------|--------------|

## Tasks Rollup
| Metric | Count |
|--------|-------|
| Completed | XX |
| Carried Forward | XX |
| New Created | XX |
| Net Velocity | +/- XX |

### Key Completions
- [x] Task 1
- [x] Task 2

### Still Open (Carried to Next Week)
- [ ] Task A
- [ ] Task B

## Decisions Made
- **Day:** Decision text

## Deliverables Shipped
| Asset | Format | For Whom |
|-------|--------|----------|

## Blockers & Friction
### Major
- Blocker 1 (from quiz)
### Minor
- Friction point 1 (from quiz)

## Dimension Assessment
[From quiz heat map data]
| Dimension | Impact | Time Spent | Satisfaction |
|-----------|--------|------------|--------------|
| Strategy  | *** | ** | *** |
| Product   | **** | **** | *** |
| Sales     | ** | ** | ** |
| Marketing | *** | *** | *** |
| Ops       | * | * | ** |

## Ideas & Insights
- Idea 1 (from Day X)
- Idea 2

## Next Week Focus
1. **Priority 1** -- context from quiz
2. **Priority 2** -- context
3. **Priority 3** -- context

## Appendix: Daily Note Links
- Monday
- Tuesday
- Wednesday
- Thursday
- Friday

---
*Hub: [[🏠 Home]] | [[Efforts MOC]]*
```

---

## Phase 3b -- Gamified HTML Report (RPG + Lake B2B)

**Path:** `Calendar/Weekly Reviews/Weekly_Report_YYYY-WXX.html`
**Also save to:** workspace output folder for sharing

### Design System

Read `references/rpg-config.md` for the full XP table, level thresholds, class definitions, and badge catalog.

#### Lake B2B Brand Colors (from daily-note-recap)

| Element | Hex |
|---------|-----|
| Header gradient (left) | #FFB703 (Gold) |
| Header gradient (mid) | #E8033A (Red) |
| Header gradient (right) | #6D08BE (Purple) |
| Body background | #0F0F1A (Dark) |
| Card background | rgba(18,18,30,0.9) |
| Card border | rgba(109,8,190,0.3) |
| Text primary | #E4E4EB |
| Text dim | #8888A0 |
| Accent | #6D08BE |
| XP bar fill | linear-gradient(90deg, #FFB703, #E8033A, #6D08BE) |
| Task complete | #22C55E |
| Task carried | #F59E0B |
| Task new | #6D08BE |

#### Typography

- **Font:** Montserrat (Google Fonts)
- **Fallback:** Arial, sans-serif
- **Weights:** 300 (Light), 400 (Regular), 600 (Semi Bold), 800 (Extra Bold)

### HTML Sections (in order)

**IMPORTANT:** All CSS and JS must be inline in a single self-contained HTML file. No external dependencies except Google Fonts. All charts rendered as inline SVG. Print-friendly with `@media print` rules. NEVER use em-dashes in any text.

#### 1. Hero Banner
Full-width Lake B2B gradient header.
- Week number + date range ("Week 12: Mar 16 - Mar 20, 2026")
- Character class name in large text with class icon
- Level badge + XP progress bar to next level
- Streak counter (flame emoji per consecutive week)

#### 2. Stats Dashboard
Four stat cards in a 2x2 grid:
- Tasks Done (green number, week-over-week delta arrow)
- Meetings (purple number)
- Efforts Advanced (gold number)
- Deliverables Shipped (red number)

If previous week data exists in `weekly_xp_log.json`, show delta arrows (up/down/same).

#### 3. XP Breakdown
Horizontal stacked bar showing XP earned by category:
- Tasks (green segment)
- Meetings (purple)
- Efforts (gold)
- Deliverables (red)
- Decisions (teal)
- Notes (gray)
- Streak bonus (rainbow)

Total XP in large text. Level progress bar below.

#### 4. Energy Arc
Inline SVG line chart of Mon-Fri energy ratings from the quiz.
- X-axis: Mon, Tue, Wed, Thu, Fri
- Y-axis: 0-10
- Line color: Lake B2B gradient
- Dots at each data point with value labels
- Background grid lines in subtle gray
- Average line as dashed horizontal

If quiz was skipped, use energy from daily note frontmatter.

#### 5. Wins Showcase
Each win displayed as an "Achievement Unlocked" card:
- Gold border glow
- Trophy icon
- Win text
- Fade-in animation with stagger

#### 6. Effort Quest Cards
Each active effort as an RPG quest card:
- Quest name (effort name with wikilink-style formatting)
- Progress bar from Monday status to Friday status
- Status badge (color-coded: Critical, Active, In Dev, etc.)
- "What changed" one-liner
- XP earned for this effort

#### 7. Blocker Board ("Enemies Encountered")
Major blockers as "boss enemy" cards (red border, skull icon)
Minor blockers as "minion" cards (orange border, shield icon)
Skipped items grayed out

#### 8. Dimension Radar
The heat map data visualized as a radar/spider chart (inline SVG):
- Five axes: Strategy, Product, Sales, Marketing, Ops
- Three overlapping polygons: Impact (gold), Time (red), Satisfaction (purple)
- Scale 0-4
- Legend below the chart

#### 9. Tasks Ledger
Three columns:
- Completed (green checkmarks) with task names
- Carried Forward (orange arrows) with task names
- New (purple plus signs) with task names

Net velocity stat: "You closed X more tasks than you opened" or "X tasks carried forward"

#### 10. Next Week Quests
Top 3 priorities as "quest cards":
- Quest number badge
- Priority text
- "Bounty: +XX XP" (estimated XP if completed)
- Purple accent border

#### 11. Footer
- "Generated [timestamp IST]"
- "Celsus Vault | Lake B2B"
- Subtle gradient line separator
- Streak motivational message based on streak count

### Responsive Design

```css
@media (max-width: 600px) {
  .stats-grid { grid-template-columns: 1fr 1fr; }
  .tasks-columns { flex-direction: column; }
  .hero h1 { font-size: 24px; }
}
@media print {
  body { background: white; color: black; }
  .card { break-inside: avoid; border: 1px solid #ddd; }
}
```

---

## Phase 3c -- Email to Sundar via Outlook

### Email Details

- **To:** Sundar (reporting manager)
- **Subject:** `Weekly Review: Week XX (Mon Date - Fri Date) | Sreedeep`
- **Body:** The HTML report inlined as the email body
- **Attachment:** None needed if HTML renders inline. If Outlook MCP only supports plain text, attach the HTML file and provide a text summary.

### Sending Logic

1. Check if Outlook MCP tools are available in the current session
2. If available: send via Outlook MCP with HTML body
3. If NOT available: save the HTML report and notify Sreedeep:
   `"Outlook integration not available in this session. Your weekly report is saved at [path]. Forward it to Sundar manually or connect Outlook to enable auto-send."`

**IMPORTANT:** Never silently fail. Always tell Sreedeep the email status.

---

## Scheduled Task Configuration

When setting up as a scheduled task:

```
Name: weekly-review
Schedule: Saturday 00:30 IST
Task: Run the weekly-review skill
  - Skip Phase 1 (quiz) if running unattended
  - Use daily note frontmatter for energy data
  - Mark quiz fields as "Scheduled run: quiz skipped"
  - Still generate all three outputs
```

---

## Key Vault Paths

| Path | What |
|------|------|
| `Calendar/Daily Notes/YYYY-MM-DD.md` | Daily notes (input) |
| `Calendar/Weekly Reviews/` | Weekly review output directory |
| `Calendar/Weekly Reviews/YYYY-WXX.md` | Vault weekly note |
| `Calendar/Weekly Reviews/Weekly_Report_YYYY-WXX.html` | Gamified HTML |
| `Calendar/Weekly Reviews/Weekly_Quiz_YYYY-WXX.html` | Reflection quiz |
| `Calendar/Weekly Reviews/weekly_xp_log.json` | Persistent XP tracking |
| `Efforts/Active/` | Active efforts (for effort extraction) |

---

## Dependencies

This skill reads outputs from but does NOT replace:
- **daily-note-recap**: Reads daily notes it generates
- **interactive-quiz**: Uses interaction patterns for Phase 1 quiz
- **lakeb2b-brand-guidelines**: Lake B2B brand colors and fonts for the HTML

---

## Quality Checklist

Before marking the weekly review as complete, verify:

1. All available daily notes (Mon-Fri) were read and data extracted
2. Missing days are explicitly noted (not silently skipped)
3. XP calculation matches the breakdown (no phantom points)
4. `weekly_xp_log.json` is updated with this week's entry
5. Character class is determined and consistent across all outputs
6. Vault note has all sections populated (even if noting gaps)
7. HTML report renders correctly as a standalone file
8. All text avoids em-dashes (use periods, commas, colons, or restructure)
9. Email sent to Sundar or manual-send notice given
10. Quiz HTML saved alongside the report

---

## Known Corrections

- **Sreedeep's work hours:** 3:00 PM - 2:00 AM IST. Weekly activity is within this window.
- **Reporting manager:** Sundar. Email via Outlook.
- **Brand:** Lake B2B for HTML reports. [[Champions Group]] for vault notes voice/tone.
- **ChampIQ:** On back burner. Primary builds: [[Champmail]] + [[ChampGraph]].
- **Outlook:** May not be available in Cowork. Always handle gracefully.
- **NEVER use em-dashes.** This is permanent and absolute.

---

## Iteration Log

| Date | Change | Why |
|------|--------|-----|
| 2026-03-20 | v1: Initial skill created | Weekly review with RPG gamification |
