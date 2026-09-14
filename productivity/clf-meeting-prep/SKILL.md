---
name: clf-meeting-prep
description: >
  CLF (Champions Leadership Framework) pitch prep for sales and BD reps across all Champions
  Group brands: LakeB2B, SGS, Ampliz, and Champions Accelerator. Runs a structured
  questionnaire, blocks on any gap (zero assumptions), then builds a full enterprise pitch
  doc: executive summary, problem statement, solution fit, ICP + sample data section,
  case study/proof, pricing packages, and next steps. Ends with a NotebookLM prompt and
  full slide-by-slide outline ready to paste. MANDATORY TRIGGER for: "CLF pitch",
  "meeting prep", "prep a pitch", "build a pitch for", "pitch doc for", "CLF prep",
  "sales pitch for [company]", "create a pitch for [prospect]", "pitch [brand] to [company]",
  "build a proposal for", or any rep request to prepare for a client meeting. Also trigger
  when a rep pastes an email thread or LinkedIn profile and asks "help me pitch this" or
  "what do I say". If in doubt, trigger.
---

# CLF Meeting Prep — Champions Leadership Framework Pitch Builder

> "Don't show up with a deck. Show up with a diagnosis."

## What This Skill Does

This skill turns a rep's raw context into a polished, enterprise-grade pitch document for any
Champions Group brand (LakeB2B, SGS, Ampliz, Champions Accelerator). It is built around one
non-negotiable principle: **no assumptions**. Every claim in the pitch traces back to something
the rep confirmed. Every gap stops the process until it's filled.

The output is a complete pitch document + a NotebookLM deck generation prompt that the rep
can use immediately after the call to spin up a slide deck.

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLF PITCH PREP ENGINE                            │
│                                                                     │
│  PHASE 1 — CONTEXT INTAKE                                          │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ Brand Selection → Questionnaire → Optional Context Paste │       │
│  └─────────────────────────────────────────────────────────┘       │
│                          ↓                                          │
│  PHASE 2 — GAP AUDIT (Zero-Assumption Gate)                        │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ Flag every unanswered required field → Block until fixed │       │
│  └─────────────────────────────────────────────────────────┘       │
│                          ↓                                          │
│  PHASE 3 — PITCH DOCUMENT BUILD                                    │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ Executive Summary → Problem → Solution → ICP/Data →     │       │
│  │ Proof → Pricing → Next Steps                            │       │
│  └─────────────────────────────────────────────────────────┘       │
│                          ↓                                          │
│  PHASE 4 — DECK GENERATION PACKAGE                                 │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ NotebookLM Prompt + Full Slide-by-Slide Outline         │       │
│  └─────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 1 — Context Intake

### Step 1: Present the Questionnaire

When the skill triggers, immediately present the full questionnaire below in a clean, labeled
format. Tell the rep:

> "Fill in everything you know. If you don't know something, write **UNKNOWN** — but be
> warned: unknowns will block the pitch build. The more you give me, the sharper the pitch.
> After the form, paste any of these if you have them: email thread, LinkedIn profile of
> the contact, previous proposal."

Do NOT start building the pitch until Phase 2 is complete.

---

### THE CLF QUESTIONNAIRE

Present this as a clearly formatted block. Group by section. Number every field.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION A — THE BRAND WE ARE PITCHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Which Champions Group brand is being pitched?
   [ ] LakeB2B   [ ] SGS / Span Global Services
   [ ] Ampliz    [ ] Champions Accelerator   [ ] Multiple (specify)

2. What specific service(s) or product(s) are we pitching?
   (Be specific — e.g., "B2B email list for fintech CFOs in the US"
   or "Healthcare data for pharma reps targeting oncologists")

3. What is the core value proposition we want to lead with?
   (e.g., speed to market, data accuracy, coverage, compliance, price)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION B — THE PROSPECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. Prospect company name:
5. Prospect industry/vertical:
6. Prospect company size (headcount / revenue if known):
7. Prospect geography / primary market:
8. Prospect website URL (if known):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION C — THE PERSON WE ARE MEETING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9.  Full name of primary contact:
10. Job title / role:
11. Department (Sales, Marketing, Ops, C-Suite, Procurement, other):
12. Are there other attendees? (Name + title for each)
13. What do you know about this person's priorities or pain points?
    (Anything from LinkedIn, previous calls, email context)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION D — THE MEETING CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
14. Is this a first meeting, follow-up, or re-engagement?
15. How was this meeting set? (Inbound / cold outreach / referral / event / other)
16. What is the goal of this meeting?
    (e.g., discovery, demo, proposal review, close, renewal)
17. Have we worked with this company before? (Y/N — if yes, describe)
18. What objections do you expect? (Price, data quality, GDPR, competition, other)
19. Who are the competitors we might be compared against in this deal?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION E — THE PROSPECT'S PROBLEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
20. What business problem is the prospect trying to solve?
    (e.g., pipeline generation, market expansion, data enrichment, campaign targeting)
21. What is their current solution or approach to this problem?
    (e.g., they use ZoomInfo, they have an in-house team, they have no solution)
22. What is the pain or cost of their current approach?
    (e.g., high cost, poor accuracy, slow speed, compliance risk, low conversion)
23. What is their likely timeline or urgency?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION F — ICP & DATA FIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
24. Who is the prospect trying to reach? (Their target audience / ICP)
    (e.g., "VP of IT at mid-market SaaS companies in North America")
25. What data fields matter most to them?
    (e.g., direct dials, email, job title, company revenue, tech stack, NPI numbers)
26. What geography/region does their data need to cover?
27. What volume of contacts are they likely to need?
    (e.g., 5K, 50K, 500K — even a rough estimate)
28. Any compliance requirements we should flag?
    (GDPR, HIPAA, CCPA, CAN-SPAM, other)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION G — PRICING & PACKAGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
29. Has a budget been discussed or hinted at?
30. Which package tier do you intend to present?
    [ ] Entry / Trial   [ ] Standard   [ ] Enterprise   [ ] Custom / TBD
31. Any specific commercial terms to include?
    (e.g., pilot offer, volume discount, prepaid annual, month-to-month)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION H — PROOF & CREDIBILITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
32. Is there a relevant case study or client win we can reference?
    (Name a client/industry if you know one — e.g., "we helped a pharma company in EMEA")
33. Any relevant certifications, compliance standards, or awards to highlight?
    (ISO 27001, SOC 2, data accuracy stats, industry recognition)
34. Any specific stat or proof point that would land best with THIS prospect?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION I — ADDITIONAL CONTEXT (PASTE BELOW)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[A] PREVIOUS EMAIL THREAD — Paste full thread here (optional but highly recommended)
[B] LINKEDIN PROFILE — Paste the contact's LinkedIn bio/summary/experience (optional)
[C] PREVIOUS PROPOSAL — Paste or describe prior proposal sent to this prospect (optional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## PHASE 2 — Zero-Assumption Gap Audit

### The Golden Rule
**Never invent. Never infer. Never proceed with a gap.**

After receiving the filled questionnaire, audit every required field before writing a single
word of the pitch. Required fields are:

- Fields 1, 2, 3 (brand + service + value prop) — **HARD BLOCK**
- Fields 4, 5, 6, 7 (prospect company basics) — **HARD BLOCK**
- Fields 9, 10, 11 (contact identity + role) — **HARD BLOCK**
- Fields 14, 16 (meeting type + goal) — **HARD BLOCK**
- Fields 20, 21 (problem + current solution) — **HARD BLOCK**
- Fields 24, 26 (their target audience + geography) — **HARD BLOCK**

Optional fields (can proceed with "not provided" noted):
- Fields 12, 13, 15, 17, 18, 19, 22, 23, 25, 27, 28, 29, 30, 31, 32, 33, 34 + Section I

### Gap Response Format

If any HARD BLOCK field is missing or marked UNKNOWN, stop and return:

```
⛔ PITCH BUILD PAUSED — Missing Required Information

I can't build an accurate pitch without the following:

[List each missing field with its number and label]

Please fill these in and I'll proceed immediately.
No assumptions will be made.
```

Do NOT produce a partial pitch. Do NOT say "I'll assume X for now." Do NOT continue.

### Context Extraction from Pasted Material

If the rep pastes an email thread, LinkedIn profile, or prior proposal in Section I:
1. Extract every relevant signal (pain points, objections raised, timelines mentioned, names,
   previous commitments made, buying signals)
2. Cross-reference against questionnaire answers — flag any contradictions
3. Enrich the pitch sections with specific language and signals from the thread
4. Note what you extracted at the top of the pitch under "Context Intelligence"

---

## PHASE 3 — Pitch Document Build

### Brand Voice by Entity

Before writing, load the correct brand voice:

| Brand | Tone | Key Differentiators to Lead With |
|-------|------|----------------------------------|
| **LakeB2B** | Formal, data-forward, enterprise | 440M+ B2B contacts, global coverage, SalesTech/MarTech/RecruitTech verticals |
| **SGS / Span Global Services** | Consultative, authoritative | Custom data research, append services, list building, compliance-first |
| **Ampliz** | Precise, intelligence-forward, clinical for healthcare | 120M+ B2B contacts, 4M+ physicians, ISO 27001, Contextual Intelligence |
| **Champions Accelerator** | Strategic, ecosystem-focused | Startup acceleration, mentorship network, investor access, India innovation |

For multi-brand pitches: lead with the brand that best matches the prospect's primary pain,
then introduce complementary brands as an ecosystem advantage.

For detailed brand specifics, refer to:
- `references/brand-voice.md` — tones, key stats, approved language per brand
- `references/objection-handling.md` — pre-written responses to common objections

---

### THE PITCH DOCUMENT STRUCTURE

Build the pitch document in this exact order. Use clear section headers. Enterprise tone
throughout — formal, data-forward, authoritative. No filler language. No generic statements.
Every sentence earns its place.

---

#### SECTION 0 — COVER BLOCK

```
[BRAND LOGO PLACEHOLDER]

CONFIDENTIAL PITCH DOCUMENT
Prepared for: [Prospect Company Name]
Prepared by: [Brand Name] — Champions Group
Contact: [Rep Name if provided, else "CLF Sales Team"]
Date: [Today's date]
Meeting Reference: [Meeting goal from Field 16]
```

---

#### SECTION 1 — EXECUTIVE SUMMARY (1 tight page)

3–4 sentences maximum. Written for a C-suite reader who has 30 seconds.
Structure: [Who we are] + [What we understand about their situation] + [What we are proposing]
+ [What they stand to gain].

**Rules:**
- Lead with the prospect's business reality, not our capabilities
- Name their industry, their geography, their specific challenge
- One concrete outcome statement (e.g., "access 47,000 verified oncology contacts in the US
  within 72 hours")
- No boilerplate. No "we are pleased to present..."

---

#### SECTION 2 — THE PROBLEM STATEMENT

Title: **"What We're Solving For"** (or a version specific to their challenge)

Structure:
1. **Their current reality** — describe what they're working with now (from Fields 20 + 21)
2. **The cost of the status quo** — quantify where possible (from Field 22). If no number,
   use directional language: "every quarter without X compounds Y"
3. **The market pressure** — what's changing in their industry that makes this urgent
4. **The implication** — what happens if this isn't fixed in the next 6–12 months

**Rules:**
- Write this as if you've studied their business, not as if you're guessing
- If email thread or LinkedIn context was provided, weave in specific signals
- Do NOT mention our solution yet. This section is 100% about them.

---

#### SECTION 3 — OUR SOLUTION

Title: **"How [Brand Name] Solves This"**

Structure:
1. **Solution overview** — 2–3 sentences on what we're offering (from Fields 2 + 3)
2. **Why this fits their specific situation** — direct connection between their problem
   (Section 2) and our capability
3. **What makes us different** — 3–5 differentiators, formatted as a comparison table:

```
| Capability          | [Competitor / Status Quo] | [Our Brand]              |
|---------------------|---------------------------|--------------------------|
| Data coverage       | [Their limitation]        | [Our specific advantage] |
| Accuracy/freshness  | [Their limitation]        | [Our specific stat]      |
| Compliance          | [Their limitation]        | [Our certification]      |
| Speed to deploy     | [Their limitation]        | [Our timeline]           |
| Support model       | [Their limitation]        | [Our model]              |
```

Populate competitor column with what was named in Field 19. If no competitor named, use
"Current Approach" as the column header.

4. **The "With vs. Without" statement** — 2 sentences max. "Without [solution], [cost of
   inaction]. With [brand], [specific gain]."

---

#### SECTION 4 — ICP & DATA FIT (The Differentiator Section)

Title: **"Who We Can Put in Front of You"**

This section is the core differentiator. It makes the pitch tangible and credible.

Structure:
1. **Their target audience restated** (from Field 24) — confirm we understand exactly
   who they need to reach
2. **Sample ICP profile table** — show 3–5 example contact profiles that match their ICP:

```
| Title / Role         | Company Type      | Geography | Key Data Fields Available |
|----------------------|-------------------|-----------|---------------------------|
| [Title from ICP]     | [Company profile] | [Region]  | [Email, Direct Dial, etc.] |
| [Title from ICP]     | [Company profile] | [Region]  | [Fields]                  |
| [Title from ICP]     | [Company profile] | [Region]  | [Fields]                  |
```

Build these sample profiles using:
- Field 24 (their ICP description)
- Field 25 (data fields they need)
- Field 26 (geography)
- Brand database specifics (from references/brand-voice.md)

3. **Database coverage statement** — how many records match their ICP in our database
   (use brand-specific stats; if exact count unknown, use qualified range language:
   "Our database includes [X]M+ [segment] contacts across [geography]")
4. **Compliance callout** — address Field 28 requirements explicitly. Never skip this.

**Rules:**
- Never fabricate a contact record. Use realistic representative titles and company types
  that match their ICP, clearly labeled as "sample profiles"
- If their ICP is niche (e.g., HCPs, government, niche tech), reference the brand's
  specific vertical database (e.g., Ampliz Healthcare Intelligence for HCPs)

---

#### SECTION 5 — PROOF & CREDIBILITY

Title: **"Evidence It Works"**

Structure:
1. **Case study** — using Field 32 as the anchor:
   - If a specific case study is named: write a 3–4 sentence narrative
     (Challenge → Approach → Outcome → Quote if available)
   - If only industry is named: write a representative case study framed as
     "A [industry] client similar to [prospect] achieved..."
   - If no case study info provided: use the brand's standard proof points
     (see references/brand-voice.md for approved proof blocks per brand)

2. **Credentials & certifications** — from Field 33 + brand defaults:
   - ISO 27001 (Ampliz standard)
   - GDPR / CCPA / HIPAA compliance stance
   - Data accuracy SLAs
   - Any relevant industry recognition

3. **Social proof** — brand-level: client count, markets served, years operating
   (from references/brand-voice.md)

---

#### SECTION 6 — PRICING & PACKAGES

Title: **"Investment Options"**

Structure:
1. **Recommended package** — based on Field 30 selection:

```
┌─────────────────────────────────────────────────────────────────┐
│  RECOMMENDED: [PACKAGE TIER NAME]                               │
│                                                                 │
│  What's included:                                               │
│  • [Core deliverable — e.g., 10,000 verified B2B contacts]     │
│  • [Data fields included]                                       │
│  • [Delivery format + timeline]                                 │
│  • [Support level]                                              │
│  • [Compliance guarantee]                                       │
│                                                                 │
│  Pricing: [From Field 29/31 if provided — else "Contact us      │
│  for a tailored quote based on your exact ICP requirements"]   │
└─────────────────────────────────────────────────────────────────┘
```

2. **Package comparison table** (3 tiers):

```
| Feature              | Entry / Trial  | Standard       | Enterprise     |
|----------------------|----------------|----------------|----------------|
| Volume               | Up to [X]K     | Up to [X]K     | Custom         |
| Data fields          | Core           | Full           | Full + Custom  |
| Delivery             | 5 business days| 3 business days| 48 hours       |
| Replacements         | 10%            | 15%            | 20%+           |
| Account manager      | No             | Dedicated       | Senior + Slack |
| Compliance docs      | Standard       | Full pack      | Full + NDA      |
```

Populate with brand-appropriate defaults from references/brand-voice.md.
If budget was mentioned in Field 29, anchor the recommendation to that tier.

3. **Commercial terms** — include any from Field 31. Default language if none provided:
   "Flexible engagement models available including pilot programs, volume-based pricing,
   and annual prepay with enhanced SLAs."

---

#### SECTION 7 — NEXT STEPS

Title: **"How We Move Forward"**

Structure — 3 numbered steps:

1. **Confirm requirements** — "Share your final ICP specs and target geography so we can
   run a live database count for [Prospect Company]."
2. **Sample data delivery** — "We'll pull a representative sample of [X] contacts matching
   your ICP within [Y] business days for your review."
3. **Commercial agreement** — "Upon sample approval, we execute a [SOW / PO / MSA] and
   deploy the full dataset within the agreed timeline."

Add a CTA block:

```
READY TO PROCEED?
[Rep Name / CLF Sales Team]
[Email] | [Phone if provided]
[Brand website]
[Calendly / booking link if applicable]
```

---

#### SECTION 8 — APPENDIX (Optional — include if relevant)

- Glossary of data terms (for less data-savvy prospects)
- Full compliance documentation list available on request
- Relevant whitepapers or product sheets (by brand)
- Additional case studies in adjacent industries

---

## PHASE 4 — Deck Generation Package

After the pitch document is complete, output this section as a clearly separated block:

---

### 📊 NOTEBOOKLM DECK GENERATION PACKAGE

> **Instructions for the rep:**
> 1. Copy the full pitch document above into a Google Doc
> 2. Upload that Google Doc as a source in NotebookLM
> 3. Paste the prompt below into the NotebookLM chat
> 4. Use the slide outline below to QC or prompt individual slides

---

**NOTEBOOKLM PROMPT — PASTE THIS:**

```
You are a professional presentation designer and B2B sales strategist.
Using the attached pitch document as your only source of truth, create a
complete slide deck for a [MEETING GOAL FROM FIELD 16] meeting with
[PROSPECT COMPANY FROM FIELD 4].

TONE: Formal, enterprise, data-forward. No filler language. Every slide earns its place.
BRAND: [BRAND FROM FIELD 1]
AUDIENCE: [CONTACT TITLE FROM FIELD 10], [OTHER ATTENDEES FROM FIELD 12 IF ANY]

Generate the deck following this exact structure. For each slide, write:
- Slide title
- 3-5 bullet points (max 8 words per bullet)
- A "speaker note" (2-3 sentences the presenter says while on this slide)
- A visual suggestion (chart type, image concept, or data visualization)

Do not add any information not present in the source document.
Flag with [DATA NEEDED] any slide where the source document lacks specifics.
```

---

**SLIDE-BY-SLIDE OUTLINE:**

```
SLIDE 1 — COVER
Title: [Brand Name] × [Prospect Company]
Content: Subtitle = meeting goal | Date | "Confidential"
Visual: Brand logo + clean hero image

SLIDE 2 — EXECUTIVE SUMMARY
Title: "The Short Version"
Content: 3 bullets from Section 1 of pitch doc
Visual: Single bold stat or outcome statement as hero text

SLIDE 3 — AGENDA
Title: "What We'll Cover Today"
Content: 5-item agenda matching pitch sections
Visual: Simple numbered list, branded

SLIDE 4 — WE UNDERSTAND YOUR SITUATION
Title: [Prospect's core challenge in 6 words or fewer]
Content: 3 bullets from Problem Statement (Section 2)
Visual: "Before state" diagram or relevant industry stat

SLIDE 5 — THE COST OF THE STATUS QUO
Title: "What Staying Still Costs"
Content: 3 bullets on implications (from Section 2, implication block)
Visual: Simple cost/risk visualization

SLIDE 6 — OUR SOLUTION
Title: "How [Brand] Solves This"
Content: 3 bullets from Solution Overview (Section 3)
Visual: Solution architecture diagram or capability icons

SLIDE 7 — WHY US vs. [COMPETITOR / STATUS QUO]
Title: "The Difference"
Content: Comparison table from Section 3
Visual: Side-by-side comparison table, branded

SLIDE 8 — WHO WE CAN PUT IN FRONT OF YOU
Title: "Your Audience, In Our Database"
Content: ICP summary + 2-3 sample profile highlights (Section 4)
Visual: Sample contact card mockups or database coverage map

SLIDE 9 — COVERAGE & COMPLIANCE
Title: "Scale + Trust"
Content: Coverage stats + compliance certifications (Section 4 + Section 5)
Visual: Compliance badge grid + coverage numbers as large type

SLIDE 10 — PROOF IT WORKS
Title: "Results for Companies Like Yours"
Content: Case study narrative in 4 bullets (Section 5)
Visual: Before/after results graphic or client logo (if approved)

SLIDE 11 — INVESTMENT OPTIONS
Title: "How We Work Together"
Content: Package recommendation + 3-tier table (Section 6)
Visual: Pricing tier cards, recommended tier highlighted

SLIDE 12 — NEXT STEPS
Title: "Three Steps to Your First Data Pull"
Content: 3 numbered next steps from Section 7
Visual: Simple 3-step timeline graphic

SLIDE 13 — THANK YOU / CONTACT
Title: "[Brand] + [Prospect] — Let's Build This"
Content: Rep contact details + CTA
Visual: Brand hero graphic + contact block
```

---

## Pitch Quality Standards

Before delivering the final pitch document, run this internal checklist:

- [ ] Zero UNKNOWN fields remain in required sections
- [ ] Prospect company name appears in every major section
- [ ] Brand voice matches the selected entity (formal/authoritative/data-forward)
- [ ] ICP sample profiles reflect Field 24 accurately — no generic "Marketing Director" filler
- [ ] Comparison table competitor column reflects Field 19 (not a generic competitor)
- [ ] Compliance requirements from Field 28 are explicitly addressed
- [ ] "With vs. Without" statement is specific, not generic
- [ ] Next steps are actionable, not aspirational
- [ ] No em dashes (—) in body copy — use colons or restructure
- [ ] No filler openers ("We are pleased to...", "In today's fast-paced...")
- [ ] The word "LakeB2B" / "Ampliz" / brand name appears less than the prospect's name

---

## Adaptive Behavior

| Scenario | Response |
|----------|----------|
| Rep skips any HARD BLOCK field | Stop. List every gap. Wait. No partial builds. |
| Rep pastes email thread without questionnaire | Extract signals, then still require questionnaire |
| Rep says "just make assumptions for the gaps" | Politely decline. Explain that assumptions = wrong pitch. |
| Multi-brand pitch requested | Lead with best-fit brand, introduce others as ecosystem |
| No case study available | Use approved brand proof blocks from references/brand-voice.md |
| No pricing clarity | Use "contact for tailored quote" language — never fabricate prices |
| Rep provides a previous proposal | Extract positioning used, align or evolve — flag if contradicting |
| Healthcare / clinical vertical | Switch to Ampliz Healthcare Intelligence, apply HIPAA-aware language |
| Startup / accelerator context | Switch to Champions Accelerator framing and ecosystem pitch |

---

## Reference Files

Read these when needed — do not load all at once:

- `references/brand-voice.md` — Detailed tone, key stats, approved language, proof blocks,
  and package defaults for LakeB2B, SGS, Ampliz, and Champions Accelerator
- `references/objection-handling.md` — Pre-written responses to the 12 most common
  objections across all four brands (price, data quality, GDPR, competition, accuracy,
  integration, timing, trial, contract, references, niche coverage, freshness)
