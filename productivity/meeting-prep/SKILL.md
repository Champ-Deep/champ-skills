---
name: meeting-prep
description: >-
  SPIN-driven meeting preparation, plus CLF (Champions Leadership Framework) pitch prep for sales and BD reps. Scans the calendar, pulls meeting history from Google Calendar, Notion, the Celsus vault and Google Drive, maintains client context folders (Atlas/Clients/{name}/), and builds tiered prep: DEEP for external, sales and partnership meetings (SPIN sequences, SWOT, ICPs, competitors), MEDIUM for internal reviews, LIGHT for recurring syncs. CLF mode runs a zero-assumption questionnaire and builds a full enterprise pitch doc plus a NotebookLM prompt and slide outline, for LakeB2B, SGS, Ampliz or Champions Accelerator. MANDATORY TRIGGER for: "prep me for my meeting", "meeting prep", "prep for today's meetings", "SPIN prep", "CLF pitch", "prep a pitch", "pitch doc for", "sales pitch for [company]", "pitch [brand] to [company]", "build a proposal for", or a rep pasting a thread or profile asking "help me pitch this". Replaces clf-meeting-prep.
---

## CLF pitch mode (absorbed from clf-meeting-prep)

When a sales or BD rep needs a pitch document rather than a meeting brief (the ask says pitch, CLF, proposal, or "what do I say" with a pasted thread or profile), read `modes/clf-meeting-prep/MODE.md` and run it. It blocks on missing inputs instead of assuming. Use the client context folder and SPIN material below as inputs to it.

# Meeting Prep, SPIN-Driven, Client-First Preparation

> "Nobody ever lost a deal because they were too prepared. They lost it because
> they showed up talking about themselves instead of the client's problems."

## Philosophy

This skill exists because Sreedeep's meetings aren't product demos, they're consultative
conversations. The tone is **mildly irreverent, consultative, client-first, and pain-point
driven**. Every prep document should read like it was written by someone who spent a week
embedded in the client's business, not someone who skimmed their website 10 minutes before
the call.

The SPIN framework (Situation → Problem → Implication → Need-payoff) isn't a rigid script , 
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
│  │ ├── {ClientName}.md (profile, auto-created)      │           │
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

## The SPIN Framework, How It Threads Through Everything

SPIN isn't just for the "questions" section, it's the structural backbone of the entire prep.
Every section of the document should reflect this progression:

### S, Situation (Where are they now?)
Research-backed understanding of the client's current state. Not surface-level ("they're a
healthcare company") but operational-level ("they have FDA clearance but zero U.S. pipeline,
~$100K ARR, and a 50-person team trying to crack a market where Qure.ai has a 90-country
head start"). The Situation section proves you've done your homework.

**Where it shows up:** Company Research section, Participant Insights, Client Profile in
the context folder. This is the foundation, get it wrong and the whole prep collapses.

### P, Problem (What's broken or at risk?)
Specific, evidence-backed pain points. Not generic ("they need better marketing") but
pointed ("their U.S. market entry is stalled because they have no pipeline infrastructure,
no brand awareness among hospital CIOs, and their website doesn't rank for a single
high-intent keyword"). Each problem should make the client nod and think "this person
gets it."

**Where it shows up:** Pain Points & Solution Mapping table, Strategic Questions (discovery),
SWOT weaknesses. The problems should feel urgent, not academic.

### I, Implication (What happens if they don't fix it?)
The cost of inaction, time, money, competitive position, market window. This is what
creates urgency. "Without U.S. pipeline infrastructure, the 12-month window between FDA
clearance and competitor catch-up closes while you're still building an in-house team."
Implications make problems feel expensive.

**Where it shows up:** Management Narrative ("cost of the status quo"), the "Without
LakeB2B" column in the comparison table, Competitive Landscape (where the threats live).

### N, Need-Payoff (What does the solution unlock?)
Not "here's what we do" but "here's what becomes possible." Frame solutions as capabilities
the client gains, not services we sell. "Go from FDA clearance to 5,000 qualified U.S.
radiology leads in 4 weeks, without hiring a single marketing person" is a need-payoff.
"We offer email marketing services" is a feature dump.

**Where it shows up:** The "With LakeB2B" column, Solution Portfolio, ICP tables (why they
buy → what they gain), Content & Campaign Suggestions (what their brand becomes).

---

## Client Context Management, The Living Client Brain

This is what makes the second meeting 10x better than the first. Every time this skill
runs for a client, it creates or updates a persistent context folder in the vault.

### Auto-Create Client Folder

Create only the files this prep actually produced. A profile and a `meeting-history.md` entry are
expected on first encounter; `pain-points.md` and `solution-mapping.md` stay unwritten until a
meeting supplies their content, and the profile notes which ones are still missing rather than
shipping empty stubs.

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

1. **Read the existing context** before doing ANY research, know what you already know
2. **Update `meeting-history.md`** with the upcoming meeting entry (pre-filled, completed after)
3. **Update `pain-points.md`** with any new intelligence from research or previous meeting notes
4. **Update `solution-mapping.md`** if new solutions are being proposed this time
5. **Cross-reference**, if previous meeting notes mention concerns, objections, or open
   questions, surface them in the continuity section

### Why This Matters

The context folder means that ANY future task involving this client, drafting an email,
building a proposal, creating a pitch deck, brainstorming campaign ideas, can pull from
accumulated, structured intel instead of starting from scratch. It's not just meeting prep
infrastructure; it's the client relationship memory.

**Vault linking:** The master `{ClientName}.md` profile should be wikilinked from
`Atlas/Clients/` and the `[[Clients MOC]]`. Tag with `#client` and relevant ecosystem tags.

---

## NotebookLM Integration (Optional Enhancement)

NotebookLM creates source-grounded research, answers that cite only YOUR uploaded documents,
not the open web. This is especially powerful for DEEP preps where you need to synthesise
from many sources without hallucination risk.

In Cowork, NotebookLM is accessed via the **Claude in Chrome** MCP tools
(`mcp__Claude_in_Chrome__navigate`, `form_input`, `get_page_text`, `computer`, etc.) , 
no Python library, no install, no local Chrome required. Just a Google account already
logged in on the user's browser.

### When to Use It

Use for DEEP preps only, new external clients, high-stakes partnerships, first meetings.
Skip for LIGHT/MEDIUM preps (overkill) and internal meetings (no external research value).
Also skip if the meeting is < 2 hours away, not enough runway.

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
NotebookLM is unreachable, skip this step entirely and rely on the standard
4-source data retrieval. NotebookLM is an enhancement layer, not a hard dependency.
The prep document should never block on it.

---

## Phase 5: Morning Routine Integration

When invoked via the morning routine (after Phase 4, Day Planner):

1. **Scan today's calendar** using `gcal_list_events` for today's date range
2. **Classify each meeting** into prep tiers (see Meeting Classification below)
3. **Check client context folders**, for each meeting, check if `Atlas/Clients/{name}/`
   exists. If not, flag it for creation.
4. **Present a summary** to the user:
   ```
   Today's Meetings:

   DEEP PREP (new/external):
   * 4:00 PM, Aikenist Technologies x LakeB2B (Sales pitch, first meeting)
     [!] No client context folder, will create one

   MEDIUM PREP (internal review with history):
   * 5:30 PM, Marketing Performance Review (weekly, last met Mar 9)

   LIGHT PREP (recurring sync):
   * 3:30 PM, Gary Weekly Pipeline Sync (recurring, last met Mar 9)

   NO PREP NEEDED:
   * 6:00 PM, Team standup (15 min, status-only)

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

## Interview Mode (hiring calls)

When the meeting is an intern panel, a junior hire screen or any call where Deep sits on the
interviewer side, the prep job changes: he needs questions in his hand, not context in his
head. Run the normal classification (interviews are always DEEP), then apply this override.

1. **Pull the material first.** Invite times and co-interviewers, the role profile, resumes,
   prior notes in `Atlas/Hiring/`. If something is missing, record the gap on the page as a
   count ("0 of 2 resumes on hand") and offer to fetch it. Never invent candidate specifics,
   referrers or dates to make the page look complete.
2. **Fix the structure on a minute rail.** Thirty minutes becomes 3 minutes of intro plus
   segments that sum to the rest, each labelled with its minute window, so the page can be
   read mid-call without arithmetic.
3. **Decide the deciding questions before the call.** Six per call: four technical, two on
   the person. A question that is not marked deciding gets dropped when time runs short,
   which is the point of marking it.
4. **Give every question a "proves" line in the same row.** The interviewer grades depth,
   not vocabulary, and the line says what a strong answer must contain. A question with no
   proves line becomes a trivia quiz.
5. **One push per answer:** "show me", "why that choice", "when did it break". The push is
   what separates a rehearsed answer from a real one.
6. **Split the live rounds visibly.** One question explicitly allows AI and grades how they
   drive the tool; one forbids it and must be answered live. State the rule as a badge in
   the row before the answer starts, so a fast reply cannot be confused with a memorised one.
7. **Close with a scoring block.** Three outcomes decided the same night (advance, one
   timeboxed take-home, no), the two-minute write-up window after the call, and the one-line
   message back to the talent owner. Both candidates get a decision, never one waiting on
   the other's.

Question design principles and the hiring signals AI companies publish about themselves live
in `references/interview-question-design.md`. If Deep asks for a page he can hold on his
phone rather than a markdown brief, build the deliverable with `executive-one-pager` and
supply its content from this section; the one-pager's budget, claim-audit and contrast gates
then apply in full.

---

## Data Retrieval Strategy

For every meeting that needs prep, once the date and the set of meetings are confirmed, pull
context from all sources in parallel:

### 0. Client Context Folder (FIRST, before anything else)

```
-> Check Atlas/Clients/{ClientName}/ for existing context
-> Read {ClientName}.md for relationship overview
-> Read meeting-history.md for what's happened before
-> Read pain-points.md for known/suspected pains
-> Read solution-mapping.md for what's been proposed
-> This is your head start, don't re-research what you already know
```

### 1. Google Calendar (`gcal_list_events`)

Reconcile what the user said against the event before researching. A stated date ("tomorrow",
"Friday") is a claim, not a fact: read the event's own start time, and lead the reply with any
mismatch ("this call is today, and nothing sits at that hour on the day you named"). Prepping
the wrong day wastes the whole run and Deep walks into an empty slot. Note an open RSVP while
you are there.

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
-> Cross-reference with Efforts/Active/, which active efforts involve these people?
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

### 6. Owed-commitment verification (follow-up meetings)

A continuity section that only reads notes will repeat claims the other side has not received.
Before writing the owed list:

1. For every promise made last time ("we will send pricing", "NDA to follow", "check in next
   week"), search Sent mail for the counterparty's address, not just a keyword: subject lines
   rarely carry the company name. Run both searches, they answer different questions.
2. Nothing found in Sent is **unverified**, never "not sent": the mail may have gone out from a
   different mailbox or by hand. Say so on the page and tell Deep to confirm in Outlook before
   the call, rather than asserting a failure he then has to defend.
3. A vault task line that says "Closed (sent)" overrules nothing. Where the task state and the
   Sent search disagree, record the disagreement as an item to settle before dialling.
4. Draft files under `Atlas/Zoom Triage/Drafts/` are unsent by definition. If the draft's dates
   are stale, mark it "rewrite before sending" in the owed list instead of implying it went out.

An overdue commitment (a check-in promised for a week later that happens 32 days on) goes at the
top of the page with a one-sentence owner line. Owning the slip in the opening beats having the
other side raise it.

### Merge & Deduplicate

After pulling from all sources:
- If a prep note for this meeting already exists in `Calendar/Meetings/`, read it and build on it
  instead of starting a parallel version. Two competing notes on one meeting is the failure.
- Deduplicate action items that appear in multiple sources
- Identify the single most recent meeting as the "last meeting" anchor
- Flag any conflicting information between sources
- **Reconcile names against the invite.** Task lines and prose notes are hand-typed and drift
  (a first name wrong on one line, a contact address transcribed with a typo domain). The
  calendar invite and the client folder win; surface any mismatch as its own pre-call check
  with the address quoted, since a typo'd attendee domain means a real person may never have
  received anything.
- Build a unified timeline: what happened -> what was promised -> what's due
- Update the client context folder with any new intel discovered

---

## Output Formats

### LIGHT Prep (Recurring Syncs)

For meetings like Gary's weekly pipeline sync or team standups. Consultative even when
it's internal, Sreedeep doesn't do lazy status updates.

```markdown
# Quick Prep: [Meeting Title], [Date]

**Last Meeting:** [Date] | **Cadence:** [Weekly/Biweekly]
**Attendees:** [[Person 1]], [[Person 2]]
**Related Effort:** [[Effort Name]]

## The Story Since Last Time
[2-3 sentences narrating what's moved, what hasn't, and what's surprising.
Not a list, a story. "The pipeline is warmer than last week, 3 responses came in
from the Lake B2B campaign, but Gary's budget approval is still in purgatory.
Meanwhile, ChampIQ just hit Day 19 and the experiment metrics need a reality check."]

## Open Action Items from Last Time
- [ ] @Gary, Send updated pipeline numbers -> Status: ?
- [ ] @Sreedeep, Review ChampIQ dashboard mockup -> Status: Done
- [!] @Murugan, Follow up with 3 warm leads -> OVERDUE (7 days)

## Suggested Talking Points
1. Pipeline update, any movement on the 3 warm leads?
2. ChampIQ experiment progress, Day 19 metrics review
3. Budget approval status, escalation needed?
```

### MEDIUM Prep (Internal Reviews)

```markdown
# Meeting Prep: [Meeting Title], [Date]

**Meeting Type:** [Review/Strategy/Planning]
**Attendees:** [[Person 1]], [[Person 2]]
**Related Efforts:** [[Effort 1]], [[Effort 2]]

## Situation Check
[Narrative paragraph grounding the meeting in current reality. What's the state of play?
What's working, what's stuck, what nobody wants to talk about but should?]

## Continuity from Last Meeting
**Last meeting:** [Date], [Summary]

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
style, mildly irreverent, never boring, always grounded in the client's reality.

See `references/deep-prep-template.md` for the full template and section-by-section guidance.

**Key structural elements:**

1. **[Continuity Section]**, If follow-up: what we committed to, what they asked, what's changed
2. **Meeting Goal & Agenda**, Outcome-driven, minute-by-minute, SPIN-sequenced
3. **Participant Insights**, Deep profiles, what drives them, SPIN-tailored talking points
4. **SPIN Question Sequences**, Per-attendee, per-phase question maps (replaces generic "discovery questions")
5. **Company Research & Situation Analysis**, The "S" deep dive: where they are, with evidence
6. **Pain Points & Implication Analysis**, The "P" and "I": what's broken and what it costs them
7. **Need-Payoff Framing & Solution Mapping**, The "N": capabilities framed as outcomes
8. **Market Landscape & Competitor Analysis**, Context that sharpens the SPIN narrative
9. **Sales & Marketing Enablement**, ICPs, content ideas, campaign calendar, SEO audit
10. **Custom Solution Portfolio**, Innovation opportunities, bundled offerings
11. **Strategic Positioning & Differentiation**, Dual SWOT + Management Narrative
11a. **Follow-up call page.** When Deep asks for a prep page for a call already in motion, he is
asking for a second screen to run it from, not another markdown brief: internal only, stated as
such in the header, delivered as a `MEDIA:` path. Build it from the owed list and the minute
rail: a banner with time, link and clash badges plus a live countdown to start; pre-dial checks as
their own block (unsent promises, RSVP state, who else is on the invite); an owed list of
tickables that persist across reload (`localStorage`, one key per item); the facts to lock in the
opening minutes; a timed run whose segments end before Deep's next commitment, with the handoff
named; options as a proposals-only table; probes; a do-not-say list; after-call tickables; and a
footer naming sources and every figure left unverified. Ship it alongside the existing `notes.md`,
not instead of it.
11b. **Visual showcase pages**, When Deep asks for a page as well as the note: variants in one
dated folder under `Calendar/Meetings/`, numbered by role (`01 - ...` to share, `02 - ...` hold
back until the counterparty opens the topic), plus the design system they were built from. Most
counterparties have no brand system in the vault, so derive one from their real logo file rather
than inventing a palette: measure the dominant colours, take one corner treatment and one
recurring motif from the mark, and record the asset's source URL in the design-system page so
the derivation is auditable. Both variants get screenshot at 1440 and 390 and read before
delivery (see the `visual-verify` skill).
11c. **Script and showcase are always two separate files.** When Deep wants something to run a
call from, ship a client-facing SHOWCASE (shared on screen, nothing internal, no toggle that could
reveal notes) and a private SCRIPT AND NOTES page (countdown, word-for-word lines, cheat sheet,
objections, facts, notes box) as two HTML files he opens in two windows. One combined page with a
hide-internal switch failed his real need: he must read the script while the showcase is on screen.
Name them `1 - SHOWCASE (share this screen).html` and `2 - SCRIPT AND NOTES (keep private).html`
at the top of the dated folder, with fonts, logos, build files and older versions under
`_support/`. Each script phase carries a pointer to the showcase section to be on, and the
showcase top bar links to those sections so he can drive it in one click. Leak-test the showcase
text for internal words before delivery. Name files by role, never p1, p2 or ds.
12. **Source Reference Index**, Every claim footnoted

**Grounding rule.** Every number carries its source or a stated absence of one. Standing brand
figures (market size, coverage, headcount) get grepped in the vault and the brand skills first:
repeating one from memory imports a figure that belongs to a different company. Numbers the
counterparty published about itself are labelled as their claim inside the note ("their site
reports", "email of date"), never converted into fact. A competitor named from model knowledge is
marked unverified in the same line. No source found is written as "no source found", never left
to imply confirmation.

---

## Voice & Style Rules

### The Sreedeep Tone

Sreedeep doesn't sound like a vendor. He sounds like a strategic advisor who happens to
have solutions. The prep documents should reflect this:

**Mildly irreverent:** Don't be afraid to call out an elephant in the room. If the client's
website hasn't been updated since 2019, say it, diplomatically, but say it. "Their SEO
footprint is... aspirational" is fine. Dry humor is welcome. Corporate-speak is not.

**Consultative:** Frame every interaction as "we're figuring this out together" not "let me
tell you what you need." The SPIN questions should feel like a conversation between equals,
not an interrogation.

**Client-first:** The client's name should appear in the prep 3x more than "LakeB2B" or
"Ampliz." Their problems, their market, their competitors, their opportunity, that's the
main character. Our solutions are the supporting cast.

**Pain-point driven:** If a section doesn't connect back to a specific client pain point,
it shouldn't be there. Every ICP, every content idea, every solution should trace back to
"...because they're struggling with X." No orphan recommendations.

### Style Rules

1. **SPIN Over Features:** Never lead with capabilities. Situation first, then problems,
   then implications, then, and only then, "here's what becomes possible."

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
| approval pending      |     | after 7 days, flag it      |
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
on the last, across meetings, across months, across team members.

---

## Vault Integration

### Saving Prep Documents

- **Deep preps:** Save to `Calendar/Meetings/{Date} - {Meeting Title} Prep.md`
  - Apply Meeting template frontmatter
  - Auto-link all people, companies, efforts, products mentioned
  - Add to today's daily note under Meetings section
  - **Update client context folder** with new research and intel
  - Deliver every artifact with a `MEDIA:` absolute path. A bare path is not a delivery.
- When there is more than one variant, number them by role in the same dated folder and say in the
  reply which one to share and which one to hold. The page Deep acts on (next steps, tickable asks)
  ships; the page that opens a negotiation he has not chosen to open is built and held, and the
  filename carries that decision so it is not a memory he has to keep.

- **Medium preps:** Save to `Calendar/Meetings/{Date} - {Meeting Title} Prep.md`
  - Lighter format but still vault-linked

- **Light preps:** Inject directly into today's daily note under Meetings section
  - No separate file needed, keeps the vault clean

### Client Context Folder Updates

After every prep (any tier):
1. Update `meeting-history.md` with the upcoming meeting entry
2. If new pain points discovered -> append to `pain-points.md`
3. If new solutions proposed -> append to `solution-mapping.md`
4. If new context docs created -> save to `context-docs/`
5. Update the master `{ClientName}.md` if relationship status changed
6. A file this prep never produced does not get created here either. Appending a pain point
   means the file already exists; if it does not, say so in the reply instead of seeding it.

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
- "prep me for the intern interview" / "interview questions for [candidate]" (Interview Mode)

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
| The ask names a set of meetings without saying which ("prep all of them") | One clarifying question listing the candidates, sent before research starts. Fall back to the calendar when it goes unanswered: prep the one event that exists and state what was not covered. |
| Stated date conflicts with the calendar event | Lead with the conflict, note an open RSVP, and say both in the reply. |
| Deep names a meeting in passing with no file and no event ("the 3 pm tomorrow thing") | State the hour and date actually found, or say plainly that nothing is booked then, before prepping against it. |
