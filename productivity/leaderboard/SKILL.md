---
name: leaderboard
description: >
  Create beautiful internal leaderboards that rank people and teams across any metric.
  Produces screen-ready and print-friendly HTML with podium heroes, ranking tables, trend
  indicators, and delta badges. Use whenever the user asks to create a leaderboard, scoreboard,
  rankings, performance board, team standings, sales leaderboard, activity tracker, competition
  board, or any visual ranking of people by metrics. Also trigger for: "who's winning",
  "rank the team", "show me the top performers", "build a scoreboard", "put scores on the
  screen", "print the rankings", "weekly standings", "team competition", "sales race",
  "leaderboard for [team]", "rank by [metric]". MANDATORY TRIGGER for any request involving
  ranking people or teams by performance metrics. If the request is for a full report or
  strategy document, use visual-report-builder instead.
---

# Leaderboard

> Ranking is a language everyone speaks. Make it beautiful, make it live, make it competitive.

## What This Skill Does

Takes any metric and any group of people, figures out the right way to rank them, and
produces a leaderboard that looks good on a wall-mounted screen, a laptop, or a printed
sheet. The output is a single-file HTML page (or a live Cowork artifact) with:

- A podium section for the top 3 (hero treatment, large numbers, visual distinction)
- A full ranking table with position, name, score, delta from previous period, and trend
- Summary metric cards (team total, average, leader gap, best streak)
- Brand-aware theming via CSS custom properties
- Print-optimized layout with `@media print` styles
- Optional auto-refresh when built as a live artifact

## Philosophy: Rankings That Motivate

A good leaderboard does three things:

1. **Celebrates winners.** The top performers should feel seen. Big numbers, podium treatment,
   visual distinction. This is why people check the board.

2. **Shows the gap.** Everyone below #1 should see exactly how far they are from the top.
   Delta badges and trend arrows tell the story of momentum: "you're #4 but climbing fast"
   is more motivating than just "#4."

3. **Keeps it fair.** Show the metric, show the period, show the rules. No ambiguity about
   what counts. Transparency builds trust in the ranking.

What a leaderboard is NOT: it's not a dashboard, not a report, not a strategy page. It's a
single, focused question answered visually: **who's winning, and by how much?**

---

## Process

### Step 1: Understand What to Rank

If the user hasn't specified, help them figure it out. Ask about:

- **Who is being ranked?** (individual reps, teams, departments, companies)
- **What metric?** (deals closed, emails sent, revenue, tasks done, response rate)
- **What period?** (this week, this month, this quarter, rolling 30 days)
- **Is there a previous period for comparison?** (deltas and trends need a baseline)

Use AskUserQuestion to clarify. Common leaderboard types by team context:

| Team Type | Good Metrics | Why |
|-----------|-------------|-----|
| Sales (pipeline) | Deals closed, revenue, pipeline value, avg deal size | Outcome-driven, directly tied to comp |
| Sales (outreach) | Emails sent, response rate, meetings booked, calls made | Activity-driven, volume matters |
| BDR/SDR | Qualified leads, first-response time, conversion rate | Mix of volume and quality |
| Marketing | Campaigns launched, MQLs generated, content pieces | Output-driven |
| Support | Tickets resolved, CSAT score, avg resolution time | Quality + speed |
| Engineering | PRs merged, story points, bugs fixed | Velocity (use carefully, context matters) |
| General/Custom | Any numeric metric the user defines | Flexible |

If the user says something vague like "make a leaderboard for Phoenix team," check CLAUDE.md
and vault context to understand who Phoenix is (SPAN Global Services sales team: Gary, Lam,
Tim, Travis, Murugan, Preeti) and suggest relevant sales metrics.

### Step 2: Gather the Data

Try data sources in this order. Stop as soon as you have what you need:

1. **User-provided data.** If the user pasted numbers, uploaded a CSV/Excel, or typed metrics
   directly, use that. This is the most common path. Parse it, confirm the metric and ranking
   order (higher is better? lower is better?), and proceed.

2. **Connected MCPs.** Check what's available and pull relevant data:

   | Data Type | MCP to Try | How |
   |-----------|-----------|-----|
   | Email activity (sent, replies) | M365 Outlook (`outlook_email_search`) | Search by sender + date range, count results |
   | Meeting activity | Google Calendar (`list_events`) | Count meetings per person in period |
   | Task completion | Notion (`notion-query-database-view`) | Query task databases filtered by assignee + status |
   | Pipeline/deals | Supabase (`execute_sql`) | Query sales tables if available |
   | Spreadsheet data | Google Drive (`search_files` + `read_file_content`) | Find and read ranking spreadsheets |
   | Any structured data | Ask the user to point you to it | |

   When pulling from connectors, always show the user what you found and confirm before
   building. Data accuracy in a leaderboard is sacred: wrong numbers destroy trust instantly.

3. **Manual input.** If no data source works, present a clean format for the user to fill in:
   ```
   I need the following to build your leaderboard:
   - Names of participants
   - Their scores for [metric] this [period]
   - (Optional) Their scores from the previous [period] for comparison
   ```

### Step 3: Structure the Leaderboard

Every leaderboard has these sections, in this order:

```
TOPBAR          Brand kicker + period label + last-updated timestamp
PODIUM          Top 3 with hero treatment (gold/silver/bronze or 1st/2nd/3rd)
FULL RANKINGS   Complete table: rank, name, score, delta, trend arrow
METRIC CARDS    2-4 summary stats (team total, average, gap to #1, best streak)
FOOTER          Data source attribution + "Updated [timestamp]"
```

**Podium rules:**
- #1 gets the largest treatment: biggest number, accent color, visual crown/badge
- #2 and #3 are smaller but still prominent, flanking #1
- If there are fewer than 3 participants, adjust (2-person: side by side, 1-person: just the hero)
- If there's a tie, show both at the same position

**Ranking table rules:**
- Alternate row shading for readability
- Delta column: green up-arrow + positive number for improvement, red down-arrow for decline
- Highlight rows on hover for screen use
- Position numbers in accent color
- If previous period data exists, show a "change" column (moved up 2 spots, etc.)

**Metric cards:**
- Pick 2-4 stats that give context to the ranking
- Examples: "Team Total: 142 deals", "Average: 14.2", "Gap: #2 is 8 behind #1", "Longest Streak: Gary (5 weeks at #1)"

### Step 4: Choose Output Format

**Live Cowork Artifact** (preferred when connectors are available):
- Use `create_artifact` with `mcp_tools` listing the connectors needed for refresh
- The artifact fetches fresh data on each page load
- Include a visible "Last refreshed" timestamp
- Great for wall-mounted screens: auto-refresh shows live standings

**Static HTML** (when data is manual or one-time):
- Single-file HTML with embedded CSS and data
- Include `@media print` styles for clean printing
- Save to workspace folder with `computer://` link

Decision logic: if the data came from a connector and the user mentioned "live", "screen",
"auto-update", or "refresh," build a live artifact. Otherwise, build static HTML.

### Step 5: Apply Visual Design

Read `references/leaderboard-patterns.md` for the full CSS reference. Key principles:

**Inherit from visual-report-builder:**
- Three-tier type system: display serif (Fraunces), body sans (Montserrat), mono data (JetBrains Mono)
- CSS custom properties scoped under a project prefix (e.g., `.lb-root`)
- Dark-by-default palette from css-starter, with brand adaptation via accent color swap
- Google Fonts CDN, Chart.js CDN if charts needed

**Leaderboard-specific patterns:**
- Podium uses `display` font for numbers, `mono` for labels
- Ranking table uses `body` font with `mono` for numeric columns (tabular-nums)
- Delta badges: pill-shaped, green for positive, red for negative, gray for no change
- Trend arrows: inline SVG, not emoji (consistent across screens and print)
- Position badges: circular, accent-colored for top 3, muted for rest

**Print optimization:**
- `@media print` block that switches to light background, dark text
- Hide hover effects and interactive elements
- Force page break before the ranking table if podium is long
- Ensure all text is black or very dark gray on white for clean printing
- Include a header with the metric name, period, and date printed

**Screen optimization (for wall-mounted displays):**
- Large type sizes: stat numbers should be readable from 3 meters
- High contrast: dark backgrounds with bright accent numbers
- Auto-scroll if ranking list is long (CSS animation, pausable)
- No interactive elements needed: this is a display, not a tool

### Step 6: Brand Adaptation

Same approach as visual-report-builder. Brand is a color swap, not a design decision:

1. Check if a brand skill is loaded or if the user specified a brand
2. Read `references/leaderboard-patterns.md` for the brand color mappings
3. Swap `--accent` and `--accent-glow` custom properties
4. Everything else (layout, typography hierarchy, patterns) stays identical

If no brand is specified and the context is Champions Group internal, default to
Champions Orange (#F26722). If it's for a specific subsidiary (SPAN, Ampliz, Lake B2B),
use that brand's accent.

### Step 7: Verify

Before presenting:
- [ ] All names spelled correctly (cross-reference with vault People notes if available)
- [ ] Numbers add up (team total = sum of individual scores)
- [ ] Ranking order is correct (verify sort direction: highest first for most metrics)
- [ ] Delta signs are correct (positive = improvement over previous period)
- [ ] Print preview looks clean (no dark backgrounds bleeding through)
- [ ] If live artifact: test that the data refresh actually works
- [ ] Brand colors applied correctly if brand was specified

---

## What Makes a Good Leaderboard (Consultative Guidance)

When users aren't sure what to rank, help them think through it:

**The "Would People Check This Daily?" Test:**
If people wouldn't voluntarily look at this board every day, the metric is wrong. Good
leaderboards create a pull: people WANT to see where they stand. Bad ones feel like
surveillance. The difference is whether the metric is something the person can directly
influence and is proud to be good at.

**Single Metric, Clear Rules:**
The best leaderboards rank on ONE number. Composite scores ("weighted average of 3 metrics")
feel arbitrary and invite arguments. If you need multiple dimensions, make multiple boards.
A "Pipeline Leaderboard" and a "Response Rate Leaderboard" are both clearer than a
"Sales Performance Score."

**Fair Comparisons:**
Only rank people who are playing the same game. Don't mix SDRs and AEs on the same board.
Don't rank someone who started mid-month against someone who had the full month. If tenure
or territory makes comparison unfair, either normalize or create separate boards.

**Celebration, Not Punishment:**
Leaderboards should make the top feel great, not make the bottom feel terrible. Design
choices matter: show the top 3 prominently, show everyone else in a clean table without
calling out the bottom. Never use red/negative coloring for low-ranked positions. Reserve
red only for decline (delta arrows), not for rank.

---

## Reference Files

- **`references/leaderboard-patterns.md`**: Full CSS patterns, component HTML templates,
  brand color mappings, print stylesheet, and live artifact boilerplate. Read this before
  writing any HTML.
