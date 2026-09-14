---
name: meeting-prep
description: >
  SPIN-driven meeting preparation skill. Scans calendar, retrieves meeting history from
  Google Calendar, Notion, Celsus vault and Google Drive, auto-creates/updates persistent
  client context folders (Atlas/Clients/{name}/), and generates tiered prep docs: DEEP for
  external/sales/partnership meetings (SPIN question sequences, SWOT, ICPs, competitor
  analysis, management narrative), MEDIUM for internal reviews, LIGHT for recurring syncs.
  Optionally integrates notebooklm-py as a persistent client brain. Runs as Phase 5 of the
  morning-routine after the Day Planner. MANDATORY TRIGGER for any meeting prep request.
  Use when user says "prep me for my meeting", "meeting prep", "get me ready for [meeting]",
  "what do I need for the [name] call", "prep for today's meetings", "SPIN prep for [company]",
  "prep for [person]", or any variation of preparing for an upcoming meeting. Also offer
  proactively whenever a meeting is mentioned in passing.
---

# Meeting Prep — SPIN-Driven, Client-First Preparation

> "Nobody ever lost a deal because they were too prepared. They lost it because
> they showed up talking about themselves instead of the client's problems."

## Philosophy

This skill exists because Sreedeep's meetings aren't product demos — they're consultative
conversations. The tone is **mildly irreverent, consultative, client-first, and pain-point
driven**. Every prep document should read like it was written by someone who spent a week
embedded in the client's business, not someone who skimmed their website 10 minutes before
the call.

The SPIN framework (Situation → Problem → Implication → Need-payoff) isn't a rigid script —
it's a thinking structure that ensures every question, every slide, every talking point serves
the client's reality first and our capabilities second. If it sounds like a pitch, rewrite it.
If it sounds like consulting, you're on the right track.

## What This Skill Does

```
┌─────────────────────────────────────────────────────────────────┐
│                   MEETING PREP ENGINE (SPIN)                     │
│                                                                  │
│  DATA SOURCES                    CLASSIFICATION                  │
│  ┌──────────────┐               ┌──────────────────┐            │
│  │ Google Cal   │──┐            │ Meeting Classifier│            │
│  │ Notion Notes │──┤            │                  │            │
│  │ Celsus Vault │──┼─→ Merge ─→│ External/Sales?  │──→ DEEP   │
│  │ Google Drive │──┘            │ Partnership?     │──→ DEEP   │
│  │ NotebookLM   │──→ (if avail)│ Recurring Sync?  │──→ LIGHT  │
│  └──────────────┘               │ Internal Review? │──→ MEDIUM │
│                                  │ First-time?      │──→ DEEP   │
│                                  └──────────────────┘            │
│                                                                  │
│  PERSISTENT CONTEXT                                              │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Atlas/Clients/{ClientName}/                       │           │
│  │ ├── {ClientName}.md (profile — auto-created)      │           │
│  │ ├── meeting-history.md (rolling log)              │           │
│  │ ├── pain-points.md (evolving, cross-meeting)      │           │
│  │ ├── solution-mapping.md (what we've proposed)     │           │
│  │ └── context-docs/ (proposals, decks, research)    │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
│  OUTPUT                                                          │
│  ┌──────────────────────────────────────────────────┐           │
│  │ SPIN Prep Document (vault + conversation)         │           │
│  │ ├── Client Situation snapshot                     │           │
│  │ ├── Problems & pain mapping                       │           │
│  │ ├── Implication analysis (cost of inaction)       │           │
│  │ ├── Need-payoff framing (value, not features)     │           │
│  │ ├── SPIN question sequences per attendee          │           │
│  │ ├── [Deep] Company research & SWOT                │           │
│  │ ├── [Deep] Management narrative                   │           │
│  │ └── Prep checklist & materials needed             │           │
│  └──────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## The SPIN Framework — How It Threads Through Everything

SPIN isn't just for the "questions" section — it's the structural backbone of the entire prep.
Every section of the document should reflect this progression:

### S — Situation (Where are they now?)
Research-backed understanding of the client's current state. Not surface-level ("they're a
healthcare company") but operational-level ("they have FDA clearance but zero U.S. pipeline,
~$100K ARR, and a 50-person team trying to crack a market where Qure.ai has a 90-country
head start"). The Situation section proves you've done your homework.

**Where it shows up:** Company Research section, Participant Insights, Client Profile in
the context folder. This is the foundation — get it wrong and the whole prep collapses.

### P — Problem (What's broken or at risk?)
Specific, evidence-backed pain points. Not generic ("they need better marketing") but
pointed ("their U.S. market entry is stalled because they have no pipeline infrastructure,
no brand awareness among hospital CIOs, and their website doesn't rank for a single
high-intent keyword"). Each problem should make the client nod and think "this person
gets it."

**Where it shows up:** Pain Points & Solution Mapping table, Strategic Questions (discovery),
SWOT weaknesses. The problems should feel urgent, not academic.

### I — Implication (What happens if they don't fix it?)
The cost of inaction — time, money, competitive position, market window. This is what
creates urgency. "Without U.S. pipeline infrastructure, the 12-month window between FDA
clearance and competitor catch-up closes while you're still building an in-house team."
Implications make problems feel expensive.

**Where it shows up:** Management Narrative ("cost of the status quo"), the "Without
LakeB2B" column in the comparison table, Competitive Landscape (where the threats live).

### N — Need-Payoff (What does the solution unlock?)
Not "here's what we do" but "here's what becomes possible." Frame solutions as capabilities
the client gains, not services we sell. "Go from FDA clearance to 5,000 qualified U.S.
radiology leads in 4 weeks — without hiring a single marketing person" is a need-payoff.
"We offer email marketing services" is a feature dump.

**Where it shows up:** The "With LakeB2B" column, Solution Portfolio, ICP tables (why they
buy → what they gain), Content & Campaign Suggestions (what their brand becomes).

---

## Client Context Management — The Living Client Brain

This is what makes the second meeting 10x better than the first. Every time this skill
runs for a client, it creates or updates a persistent context folder in the vault.

### Auto-Create Client Folder

On first encounter with a new client/prospect, create:

```
Atlas/Clients/{ClientName}/
├── {ClientName}.md          ← Master profile (company overview, key contacts, relationship status)
├── meeting-history.md       ← Rolling log of every meeting (date, attendees, outcomes, next steps)
├── pain-points.md           ← Evolving pain point inventory (confirmed, suspected, resolved)
├── solution-mapping.md      ← What we've proposed, what they've responded to, what's landed
└── context-docs/            ← Folder for proposals, decks, research docs, case studies shared
```

### Auto-Update on Every Prep

When prepping for a client that already has a context folder:

1. **Read the existing context** before doing ANY research — know what you already know
2. **Update `meeting-history.md`** with the upcoming meeting entry (pre-filled, completed after)
3. **Update `pain-points.md`** with any new intelligence from research or previous meeting notes
4. **Update `solution-mapping.md`** if new solutions are being proposed this time
5. **Cross-reference** — if previous meeting notes mention concerns, objections, or open
   questions, surface them in the continuity section

### Why This Matters

The context folder means that ANY future task involving this client — drafting an email,
building a proposal, creating a pitch deck, brainstorming campaign ideas — can pull from
accumulated, structured intel instead of starting from scratch. It's not just meeting prep
infrastructure; it's the client relationship memory.

**Vault linking:** The master `{ClientName}.md` profile should be wikilinked from
`Atlas/Clients/` and the `[[Clients MOC]]`. Tag with `#client` and relevant ecosystem tags.

---

## NotebookLM Integration (Optional Enhancement)

NotebookLM creates source-grounded research — answers that cite only YOUR uploaded documents,
not the open web. This is especially powerful for DEEP preps where you need to synthesise
from many sources without hallucination risk.

In Cowork, NotebookLM is accessed via the **Claude in Chrome** MCP tools
(`mcp__Claude_in_Chrome__navigate`, `form_input`, `get_page_text`, `computer`, etc.) —
no Python library, no install, no local Chrome required. Just a Google account already
logged in on the user's browser.

### When to Use It

Use for DEEP preps only — new external clients, high-stakes partnerships, first meetings.
Skip for LIGHT/MEDIUM preps (overkill) and internal meetings (no external research value).
Also skip if the meeting is < 2 hours away — not enough runway.

### How It Works in Cowork

**For new clients (first meeting):**
1. Navigate to `notebooklm.google.com` via `Claude_in_Chrome__navigate`
2. Create a new notebook named `Client: {ClientName}`
3. Add sources using the notebook's "Add source" UI:
   - Client website URL
   - LinkedIn company page URL
   - Recent news article URLs (from web research)
   - Any Google Drive docs already found
   - Relevant LakeB2B case studies
4. Once sources are processed, use the notebook's chat interface to query:
   - "What are this company's biggest stated challenges?"
   - "What has their leadership said about growth priorities?"
   - "What technology gaps or market pressures are visible?"
5. Capture the notebook URL and store it in the client context folder:
   `Atlas/Clients/{ClientName}/{ClientName}.md` → `NotebookLM: {url}`

**For returning clients (follow-up meetings):**
1. Read client context folder to get the existing notebook URL
2. Navigate to it via `Claude_in_Chrome__navigate`
3. Add new sources: latest meeting notes (as text), any new docs, recent news
4. Query for continuity: "What open commitments or questions were raised in the sources?"
5. Query for evolution: "What's changed since the earliest sources were added?"

**Graceful fallback:** If Chrome tools aren't available, Google isn't logged in, or
NotebookLM is unreachable — skip this step entirely and rely on the standard
4-source data retrieval. NotebookLM is an enhancement layer, not a hard dependency.
The prep document should never block on it.

---

## Phase 5: Morning Routine Integration

When invoked via the morning routine (after Phase 4 — Day Planner):

1. **Scan today's calendar** using `gcal_list_events` for today's date range
2. **Classify each meeting** into prep tiers (see Meeting Classification below)
3. **Check client context folders** — for each meeting, check if `Atlas/Clients/{name}/`
   exists. If not, flag it for creation.
4. **Present a summary** to the user:
   ```
   Today's Meetings:

   DEEP PREP (new/external):
   * 4:00 PM — Aikenist Technologies x LakeB2B (Sales pitch, first meeting)
     [!] No client context folder — will create one

   MEDIUM PREP (internal review with history):
   * 5:30 PM — Marketing Performance Review (weekly, last met Mar 9)

   LIGHT PREP (recurring sync):
   * 3:30 PM — Gary Weekly Pipeline Sync (recurring, last met Mar 9)

   NO PREP NEEDED:
   * 6:00 PM — Team standup (15 min, status-only)

   I'll auto-generate light/medium preps now. Which deep preps should I run?
   ```
5. **Auto-generate** light and medium preps immediately
6. **Wait for user confirmation** before running deep preps (they're resource-intensive)
7. **Create/update client context folders** for any meetings that need them
8. **Save prep documents** to the Celsus vault and inject summaries into the daily note

When invoked standalone, skip the classification summary and go straight to prepping
the specified meeting.

---

## Meeting Classification

| Signal | How to Detect | Prep Tier |
|--------|---------------|-----------|
| **External attendees** (non-company email domains) | Calendar attendee emails not matching known internal domains | DEEP |
| **First meeting with this person/company** | No previous meetings found in Notion/Vault/Calendar history | DEEP |
| **"Pitch", "demo", "proposal", "partnership"** in title/description | Calendar event title/description keyword scan | DEEP |
| **Known client/partner company** from CLAUDE.md | Attendee or title matches a Clients MOC entry | DEEP |
| **Internal review with history** (performance, strategy, campaign) | All internal attendees + review/strategy keywords + previous meetings exist | MEDIUM |
| **Recurring meeting with action items** | Recurring calendar event + previous meeting notes have open action items | MEDIUM |
| **Recurring sync, no outstanding items** | Recurring event + last meeting had no carryover items | LIGHT |
| **< 20 minutes, status-only** | Short duration + "standup"/"status"/"check-in" keywords | SKIP |

When classification is ambiguous, err toward the deeper tier.

---

## Data Retrieval Strategy

For every meeting that needs prep, pull context from all sources in parallel:

### 0. Client Context Folder (FIRST — before anything else)

```
-> Check Atlas/Clients/{ClientName}/ for existing context
-> Read {ClientName}.md for relationship overview
-> Read meeting-history.md for what's happened before
-> Read pain-points.md for known/suspected pains
-> Read solution-mapping.md for what's been proposed
-> This is your head start — don't re-research what you already know
```

### 1. Google Calendar (`gcal_list_events`)

```
-> Find the current meeting: attendees, description, attachments, location
-> Search for previous meetings with same attendees (past 90 days)
-> Check for recurring event pattern (weekly sync? monthly review?)
-> Extract: meeting cadence, last occurrence date, attendee list
```

### 2. Notion Meeting Notes (`notion-query-meeting-notes`)

```
-> Query by meeting title keywords (past 30 days first, expand to 90 if needed)
-> Query by attendee names if title search yields nothing
-> Extract: summary, action items, decisions made, open questions
-> Prioritize the MOST RECENT meeting note for continuity
```

### 3. Celsus Vault (`Calendar/Meetings/` + `Efforts/Active/`)

```
-> Search Calendar/Meetings/ for files matching attendee names or company names
-> Read the most recent matching meeting note
-> Cross-reference with Efforts/Active/ — which active efforts involve these people?
-> Check Atlas/People/ for attendee profiles and relationship context
-> Extract: previous prep docs, effort linkages, relationship history
```

### 4. Google Drive (`google_drive_search`)

```
-> Search for documents mentioning the company/attendee name
-> Look for: presentations, proposals, shared docs, case studies
-> Filter to recent documents (last 90 days) unless it's a first meeting
-> Extract: what materials were shared, what was presented before
```

### 5. NotebookLM via Claude in Chrome (DEEP prep only, if available)

```
-> Check client context folder for existing notebook URL
-> If notebook URL exists: navigate to it, add new sources, query for updates
-> If first meeting: navigate to notebooklm.google.com, create new notebook,
   add sources (website, LinkedIn, news, Drive docs), query for insights
-> Feed source-grounded answers back into the SPIN analysis
-> Store notebook URL in client context folder for future use
-> If Chrome tools unavailable or Google not logged in: skip gracefully
```

### Merge & Deduplicate

After pulling from all sources:
- Deduplicate action items that appear in multiple sources
- Identify the single most recent meeting as the "last meeting" anchor
- Flag any conflicting information between sources
- Build a unified timeline: what happened -> what was promised -> what's due
- Update the client context folder with any new intel discovered

---

## Output Formats

### LIGHT Prep (Recurring Syncs)

For meetings like Gary's weekly pipeline sync or team standups. Consultative even when
it's internal — Sreedeep doesn't do lazy status updates.

```markdown
# Quick Prep: [Meeting Title] — [Date]

**Last Meeting:** [Date] | **Cadence:** [Weekly/Biweekly]
**Attendees:** [[Person 1]], [[Person 2]]
**Related Effort:** [[Effort Name]]

## The Story Since Last Time
[2-3 sentences narrating what's moved, what hasn't, and what's surprising.
Not a list — a story. "The pipeline is warmer than last week — 3 responses came in
from the Lake B2B campaign, but Gary's budget approval is still in purgatory.
Meanwhile, ChampIQ just hit Day 19 and the experiment metrics need a reality check."]

## Open Action Items from Last Time
- [ ] @Gary — Send updated pipeline numbers -> Status: ?
- [ ] @Sreedeep — Review ChampIQ dashboard mockup -> Status: Done
- [!] @Murugan — Follow up with 3 warm leads -> OVERDUE (7 days)

## Suggested Talking Points
1. Pipeline update — any movement on the 3 warm leads?
2. ChampIQ experiment progress — Day 19 metrics review
3. Budget approval status — escalation needed?
```

### MEDIUM Prep (Internal Reviews)

```markdown
# Meeting Prep: [Meeting Title] — [Date]

**Meeting Type:** [Review/Strategy/Planning]
**Attendees:** [[Person 1]], [[Person 2]]
**Related Efforts:** [[Effort 1]], [[Effort 2]]

## Situation Check
[Narrative paragraph grounding the meeting in current reality. What's the state of play?
What's working, what's stuck, what nobody wants to talk about but should?]

## Continuity from Last Meeting
**Last meeting:** [Date] — [Summary]

### Decisions Made & Their Status
| Decision | Status | Notes |
|----------|--------|-------|
| ... | ... | ... |

### Open Action Items
| # | Action | Owner | Status | Notes |
|---|--------|-------|--------|-------|
| 1 | ... | ... | Done | ... |
| 2 | ... | ... | In Progress | ... |
| 3 | ... | ... | Overdue | ... |

## Key Questions (SPIN-Lite)
- **Situation:** What data/metrics should we review? What's changed?
- **Problem:** Where are we stuck? What's underperforming?
- **Implication:** What happens to [effort] if we don't resolve [problem] this week?
- **Need-Payoff:** What would "good" look like by next meeting?

## Suggested Agenda
1. Review action items from [last date] (10 min)
2. [Topic from effort progress] (15 min)
3. [Topic from new developments] (15 min)
4. Decisions needed + next steps (10 min)

## Prep Checklist
- [ ] Review [specific document/dashboard]
- [ ] Pull [specific data point]
```

### DEEP Prep (External/Sales/Partnership Meetings)

This is the full SPIN-driven dossier. The structure reflects Sreedeep's signature
style — mildly irreverent, never boring, always grounded in the client's reality.

See `references/deep-prep-template.md` for the full template and section-by-section guidance.

**Key structural elements:**

1. **[Continuity Section]** — If follow-up: what we committed to, what they asked, what's changed
2. **Meeting Goal & Agenda** — Outcome-driven, minute-by-minute, SPIN-sequenced
3. **Participant Insights** — Deep profiles, what drives them, SPIN-tailored talking points
4. **SPIN Question Sequences** — Per-attendee, per-phase question maps (replaces generic "discovery questions")
5. **Company Research & Situation Analysis** — The "S" deep dive: where they are, with evidence
6. **Pain Points & Implication Analysis** — The "P" and "I": what's broken and what it costs them
7. **Need-Payoff Framing & Solution Mapping** — The "N": capabilities framed as outcomes
8. **Market Landscape & Competitor Analysis** — Context that sharpens the SPIN narrative
9. **Sales & Marketing Enablement** — ICPs, content ideas, campaign calendar, SEO audit
10. **Custom Solution Portfolio** — Innovation opportunities, bundled offerings
11. **Strategic Positioning & Differentiation** — Dual SWOT + Management Narrative
12. **Source Reference Index** — Every claim footnoted

---

## Voice & Style Rules

### The Sreedeep Tone

Sreedeep doesn't sound like a vendor. He sounds like a strategic advisor who happens to
have solutions. The prep documents should reflect this:

**Mildly irreverent:** Don't be afraid to call out an elephant in the room. If the client's
website hasn't been updated since 2019, say it — diplomatically, but say it. "Their SEO
footprint is... aspirational" is fine. Dry humor is welcome. Corporate-speak is not.

**Consultative:** Frame every interaction as "we're figuring this out together" not "let me
tell you what you need." The SPIN questions should feel like a conversation between equals,
not an interrogation.

**Client-first:** The client's name should appear in the prep 3x more than "LakeB2B" or
"Ampliz." Their problems, their market, their competitors, their opportunity — that's the
main character. Our solutions are the supporting cast.

**Pain-point driven:** If a section doesn't connect back to a specific client pain point,
it shouldn't be there. Every ICP, every content idea, every solution should trace back to
"...because they're struggling with X." No orphan recommendations.

### Style Rules

1. **SPIN Over Features:** Never lead with capabilities. Situation first, then problems,
   then implications, then — and only then — "here's what becomes possible."

2. **The Management Narrative:** Every deep prep includes a 2-3 paragraph persuasive narrative
   addressing the client's leadership. Structure: acknowledge position -> cost of status quo ->
   partnership as infrastructure -> "with vs. without" table. This is the section that gets
   forwarded internally at the client's company.

3. **Research Depth & Source Citation:** Deep preps include footnoted references. Every factual
   claim gets a source. Web research covers: company news (30 days), funding, leadership,
   market sizing with CAGR, 5-7 competitors, digital footprint.

4. **Role-Based SPIN:** When multiple people attend, tailor the SPIN sequence per person:
   - **CEO/Founder:** Situation = their strategic position; Problem = market gap; Implication = competitive window closing; Need-Payoff = strategic infrastructure
   - **Director/VP:** Situation = their operational reality; Problem = resource constraints; Implication = missed targets; Need-Payoff = concrete deliverables and timelines
   - **Sales/Technical:** Situation = their current tools/process; Problem = friction points; Implication = lost deals; Need-Payoff = proof points and integration ease

5. **Actionable ICPs:** Tables include why each segment buys, what data is available,
   specific numbers. Never vague.

6. **Content & Campaign Suggestions:** Video concepts with titles, product bundles,
   6-month content calendar, SEO audit recommendations.

7. **Dual SWOT:** Always both the client AND LakeB2B/Ampliz. Including our weaknesses
   shows intellectual honesty and prepares Sreedeep for tough questions.

---

## Continuity Engine

### For Recurring Meetings

```
Last Meeting (Mar 9)          This Meeting (Mar 16)
+-----------------------+     +-----------------------------+
| Action: Gary to       |---->| Status check: Did Gary      |
| send pipeline nums    |     | send the numbers?           |
|                       |     |                             |
| Decision: Pivot to    |---->| Follow-up: How is the       |
| corporate focus       |     | pivot progressing?           |
|                       |     |                             |
| Open Q: Budget        |---->| Escalation: Still pending    |
| approval pending      |     | after 7 days — flag it      |
+-----------------------+     +-----------------------------+
```

### For Follow-Up Meetings (Same External Client)

```
First Meeting (Feb 17)        Follow-Up (Mar 16)
+-----------------------+     +-----------------------------+
| SPIN Situation:       |---->| Updated Situation: What's   |
| FDA cleared, no U.S.  |     | changed in 4 weeks?         |
| pipeline              |     |                             |
|                       |     |                             |
| Their Problem:        |---->| Validate: Still their #1    |
| No market entry       |     | pain, or has priority        |
| infrastructure        |     | shifted?                     |
|                       |     |                             |
| We Committed:         |---->| Deliver: Sample ICP data    |
| Sample data pull      |     | pull (5,000 contacts)        |
|                       |     |                             |
| They Asked About:     |---->| Prepare: Updated IQVIA      |
| Data accuracy, IQVIA  |     | comparison, accuracy proof   |
+-----------------------+     +-----------------------------+
```

The continuity engine also updates the client context folder, so each interaction builds
on the last — across meetings, across months, across team members.

---

## Vault Integration

### Saving Prep Documents

- **Deep preps:** Save to `Calendar/Meetings/{Date} - {Meeting Title} Prep.md`
  - Apply Meeting template frontmatter
  - Auto-link all people, companies, efforts, products mentioned
  - Add to today's daily note under Meetings section
  - **Update client context folder** with new research and intel

- **Medium preps:** Save to `Calendar/Meetings/{Date} - {Meeting Title} Prep.md`
  - Lighter format but still vault-linked

- **Light preps:** Inject directly into today's daily note under Meetings section
  - No separate file needed — keeps the vault clean

### Client Context Folder Updates

After every prep (any tier):
1. Update `meeting-history.md` with the upcoming meeting entry
2. If new pain points discovered -> append to `pain-points.md`
3. If new solutions proposed -> append to `solution-mapping.md`
4. If new context docs created -> save to `context-docs/`
5. Update the master `{ClientName}.md` if relationship status changed

### Post-Meeting (Future Integration)

After the meeting, say "process meeting notes" or "meeting debrief" to:
- Create/update the meeting note with outcomes
- Update action items in relevant effort files
- Mark resolved pain points in `pain-points.md`
- Flag items for tomorrow's morning routine
- Update person/company profiles with new intel

---

## Quick Invocation

**Standalone triggers:**
- "prep me for my meeting with [company/person]"
- "meeting prep for [meeting name]"
- "get me ready for the [time] call"
- "what do I need for today's meetings"
- "prep for Charles" / "prep for Gary sync"
- "SPIN prep for [company]"

**Morning routine trigger:**
- Runs automatically as Phase 5 after Day Planner
- "just the meeting preps" -> Skip phases 1-4, run only meeting prep

**Depth overrides:**
- "quick prep for [meeting]" -> Force LIGHT even if classification says DEEP
- "deep prep for [meeting]" -> Force DEEP even if classification says LIGHT
- "go deeper on the Aikenist prep" -> Expand a LIGHT/MEDIUM prep to DEEP

---

## Adaptive Behavior

| Scenario | Behavior |
|----------|----------|
| No calendar access | Ask user to list today's meetings manually |
| No previous meeting history found | Treat as first meeting -> default to DEEP, create client context folder |
| Client context folder exists | Read it FIRST, skip redundant research, focus on what's new |
| Previous meeting was > 30 days ago | Include a "recap" section summarizing the full relationship arc |
| Meeting is in < 1 hour | Skip deep research, produce MEDIUM prep with what's available |
| Meeting is tomorrow or later | Full prep with time for user to review and request changes |
| User says "quick mode" | Generate LIGHT preps only, skip classification |
| Multiple meetings need DEEP prep | Prioritize by time (earliest first), ask user to confirm order |
| Claude in Chrome available + DEEP prep | Use it to create/update NotebookLM notebook via browser, query for source-grounded insights |
| Claude in Chrome unavailable or not logged in to Google | Skip NotebookLM gracefully, use standard 4-source retrieval |
