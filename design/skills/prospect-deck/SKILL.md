---
name: prospect-deck
description: >
  End-to-end prospect research and slide deck pipeline. Takes a name, company, LinkedIn URL,
  or brief as input. Researches via Proxycurl, Ahrefs, web search, and vault. Compiles into
  structured source docs, creates a NotebookLM notebook via notebooklm-py, adds sources,
  generates an editable PPTX deck. MANDATORY TRIGGER for: "prospect deck", "research deck",
  "client deck", "prospect slides", "sales deck for [person]", "build a deck on [company]",
  "research [person] and make slides", "NotebookLM deck", "prospect presentation", or any
  request involving prospect/company research AND a slide deck. Also trigger when a LinkedIn
  URL is sent with "deck", "slides", or "presentation". Works for research-only (skip deck)
  or deck-from-existing-research (skip research) requests too.
---

# Prospect Deck — Research to Slide Deck Pipeline

> Paste a name, drop a LinkedIn URL, or describe who you're meeting.
> Get back a NotebookLM-powered slide deck with deep prospect intel.

## Philosophy

This skill exists because Sreedeep's sales process is consultative, not transactional.
Every deck should feel like you already know the prospect's world: their company's pain
points, their professional trajectory, their industry pressures, and the specific angles
where Champions Group's portfolio can help. The deck is a conversation starter, not a
brochure.

The pipeline is: **Parse → Research → Compile → Notebook → Slides → Deliver**.
Each phase can be skipped if the user provides partial inputs (e.g., "I already have the
research, just make the deck" skips research).

---

## Pipeline Overview

```
INPUT (flexible)                    RESEARCH (parallel)
┌─────────────────┐    ┌─────────────────────────────────────┐
│ Name + Company  │    │ Proxycurl: LinkedIn enrichment       │
│ LinkedIn URL    │───→│ Web Search: news, funding, press     │
│ Brief / context │    │ Ahrefs: domain SEO, traffic, tech    │
│ Mix of above    │    │ Vault: Atlas/Clients/, Atlas/People/ │
└─────────────────┘    └──────────────┬──────────────────────┘
                                      │
                    COMPILE           │
                    ┌─────────────────▼──────────────────┐
                    │ Structured markdown source docs:    │
                    │  - person_profile.md                │
                    │  - company_intel.md                 │
                    │  - pain_points_and_angles.md        │
                    │  - sales_context.md (if brief given)│
                    └─────────────────┬──────────────────┘
                                      │
                    NOTEBOOK LM       │
                    ┌─────────────────▼──────────────────┐
                    │ notebooklm-py:                      │
                    │  1. Create notebook                  │
                    │  2. Add source docs                  │
                    │  3. Generate slide deck (PPTX)       │
                    │  4. Download to workspace            │
                    └─────────────────┬──────────────────┘
                                      │
                    DELIVER           │
                    ┌─────────────────▼──────────────────┐
                    │ PPTX in workspace folder            │
                    │ + Vault note at Atlas/Clients/      │
                    │ + NotebookLM link for future use    │
                    └────────────────────────────────────┘
```

---

## Phase 0: Parse Input

The user's input will be one of:

| Input type | Example | What to extract |
|-----------|---------|-----------------|
| Name + Company | "John Smith at Acme Corp" | person name, company name |
| LinkedIn URL | "https://linkedin.com/in/johnsmith" | URL (Proxycurl will extract the rest) |
| Brief | "Meeting with CTO of Acme tomorrow, they're evaluating our data services" | name, company, role, context |
| Mixed | "Check out linkedin.com/in/johnsmith, he's the VP Sales at Acme. Meeting Thursday." | URL + context |

**Extraction rules:**
1. If a LinkedIn URL is present, that's the primary identifier. Extract it first.
2. If only a name + company, construct a search query for Proxycurl or web search.
3. If context is provided (meeting purpose, timeline, specific interest), save it for the sales_context.md source doc.
4. If the input is ambiguous, state your assumption and proceed (per A1 confidence gating, 80-94% range).

---

## Phase 1: Research (Parallel)

Launch research across all available channels simultaneously. Use sub-agents or parallel tool calls.

### 1a. LinkedIn Enrichment (Proxycurl)

If a LinkedIn URL is available:
```
Tool: enrich-prospects
Input: the LinkedIn URL
```

Extract: full name, headline, current role, company, location, experience history,
education, skills, summary.

If no URL but we have a name + company, try:
```
Tool: match-prospects
Input: name + company
```

If Proxycurl is unavailable or returns nothing, fall back to web search.

### 1b. Company Intelligence

**Web search** for the company:
- Recent news, funding rounds, acquisitions
- Key leadership changes
- Industry trends affecting them
- Tech stack (if relevant)
- Company size, revenue estimates

**Ahrefs** (if the company domain is known):
```
Tool: site-explorer-metrics
Input: company domain
```
Get: domain rating, organic traffic, top pages. This reveals their digital maturity
and marketing investment level.

```
Tool: site-explorer-organic-keywords
Input: company domain, limit 20
```
Get: what they rank for. This tells you what they care about publicly.

### 1c. Vault Check

Search the Celsus vault for existing intel:
- `Atlas/Clients/{company-name}.md`
- `Atlas/People/{person-name}.md`
- `Atlas/Companies/{company-name}.md`
- Any meeting notes referencing this person/company

If found, incorporate existing context. Do not duplicate what's already known.

### 1d. Company Enrichment (Proxycurl)

If we have the company domain or LinkedIn company URL:
```
Tool: enrich-business
Input: company URL or domain
```

---

## Phase 2: Compile Research into Source Documents

Create structured markdown files in a temp directory. These become NotebookLM sources.

### person_profile.md
```markdown
# {Full Name} — Prospect Profile

## Overview
- **Current Role:** {title} at {company}
- **Location:** {location}
- **LinkedIn:** {url}

## Professional Background
{Experience history, key career moves, pattern of interests}

## Skills & Expertise
{Top skills, endorsements, certifications}

## Education
{Degrees, institutions}

## Key Signals
{Anything notable: recent job change, posts about specific topics,
 connections to our network}
```

### company_intel.md
```markdown
# {Company Name} — Company Intelligence

## Snapshot
- **Industry:** {industry}
- **Size:** {employee count / revenue range}
- **HQ:** {location}
- **Website:** {domain}
- **Domain Rating:** {from Ahrefs}

## Recent News & Events
{Funding, acquisitions, leadership changes, product launches}

## Digital Presence
- **Monthly Organic Traffic:** {estimate}
- **Top Keywords:** {what they rank for}
- **Tech Stack Signals:** {if available}

## Industry Context
{Market trends, competitive pressures, regulatory changes}
```

### pain_points_and_angles.md
```markdown
# Sales Angles — {Person} at {Company}

## Likely Pain Points
{Inferred from research: industry challenges, company stage, role responsibilities}

## Champions Group Portfolio Fit
{Which of the 12 companies / products could help, and why}

## Conversation Starters
{Specific, non-generic talking points based on their recent activity or company news}

## Red Flags / Watch Outs
{Potential objections, competitive alternatives they might be using}
```

### sales_context.md (only if user provided context)
```markdown
# Meeting / Outreach Context

## User's Brief
{Exactly what Sreedeep said about this prospect}

## Meeting Details
{Date, purpose, attendees if mentioned}

## Specific Asks
{What Sreedeep wants to achieve in this interaction}
```

---

## Phase 3: NotebookLM Integration

This phase uses `notebooklm-py` to create a notebook, add sources, and generate slides.

### Prerequisites

Ensure notebooklm-py is installed:
```bash
pip install notebooklm-py --break-system-packages 2>/dev/null || true
```

Check authentication:
```bash
notebooklm check-auth 2>/dev/null
```

If auth fails, tell the user:
> "NotebookLM needs a one-time browser login. Run `notebooklm login` in your terminal
> and complete the Google sign-in. After that, this skill handles everything automatically."

Then skip to Phase 4 (fallback).

### Create Notebook and Generate Slides

Run the helper script:
```bash
python /path/to/prospect-deck/scripts/nbml_create.py \
  --name "{Person} — {Company} Prospect Deck" \
  --sources person_profile.md company_intel.md pain_points_and_angles.md [sales_context.md] \
  --output /path/to/output/prospect_deck.pptx \
  --format pptx \
  --length detailed
```

The script handles:
1. Creating the notebook with a descriptive title
2. Uploading each markdown file as a text source
3. Requesting slide generation with "detailed" length
4. Downloading the resulting PPTX
5. Outputting the notebook URL for future reference

### What to tell NotebookLM to focus on

When generating slides, the prompt context should emphasize:
- Lead with the prospect's world, not ours
- Highlight pain points and angles, not product features
- Keep company intel visual and scannable
- End with conversation starters and next steps

---

## Phase 4: Fallback (No NotebookLM Auth)

If NotebookLM authentication is not available, fall back to generating the deck directly
using the `pptx` skill. This produces a branded Champions Group deck using the research
compiled in Phase 2.

Invoke the `pptx` skill and the `champions-group-brand` skill together. Build a deck with
these slides:

1. **Title slide**: {Person Name} | {Company} | Prospect Intel
2. **Person Profile**: role, background, key signals
3. **Company Snapshot**: size, industry, digital presence
4. **Recent News**: 3-4 key developments
5. **Pain Points**: top 3 inferred challenges
6. **Portfolio Fit**: which Champions Group companies/products help
7. **Conversation Starters**: 3-4 specific, non-generic openers
8. **Next Steps**: recommended approach

---

## Phase 5: Deliver

1. **Save the PPTX** to the workspace folder with a clear filename:
   `{Company}_{Person}_Prospect_Deck_{YYYY-MM-DD}.pptx`

2. **Create/update a vault note** at `Atlas/Clients/{Company}/{Person}_research.md`
   (or `Atlas/People/{Person}.md` if they're not a client yet) with the compiled research.
   Use `[[wikilinks]]` to connect to relevant company/product notes.

3. **Report to user** with:
   - Link to the PPTX file
   - NotebookLM URL (if used) for future reference and audio overview generation
   - A 2-3 sentence summary of the most interesting finding
   - Any gaps in the research (e.g., "Proxycurl didn't return education data")

4. **Offer follow-ups**:
   - "Want me to generate an audio overview from this notebook?"
   - "Should I draft an outreach email based on this research?"
   - "Want me to prep SPIN questions for a meeting with them?"

---

## Edge Cases

| Situation | Action |
|-----------|--------|
| Person not found on LinkedIn | Use web search only. Flag the gap. |
| Company is tiny / no web presence | Focus on person profile, skip Ahrefs. Note limited data. |
| User says "skip research, I have notes" | Jump to Phase 2 compilation using user's notes as input |
| User says "just research, no deck" | Stop after Phase 2. Save research to vault. |
| NotebookLM rate limited | Wait 5 minutes and retry once. If still failing, use Phase 4 fallback. |
| Multiple people at same company | Create one notebook with all person profiles as separate sources |

---

## Important Notes

- **No em dashes.** Use periods, commas, colons, or restructure.
- **Consultative tone.** The deck should feel like insider knowledge, not a Wikipedia summary.
- **Privacy awareness.** Do not include personal contact details (phone, personal email) in decks. LinkedIn URL and professional info only.
- **Vault lean policy.** Research notes go in the vault. The PPTX does not (it lives in workspace or gets shared separately).
