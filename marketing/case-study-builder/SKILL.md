---
name: case-study-builder
description: >
  End-to-end case study pipeline: identify which clients deserve one, gather and verify evidence,
  shape the narrative for the specific buyer, write on-page + full PDF formats, hand off to design.
  MANDATORY TRIGGER for: "build a case study", "write up a client win", "create a success story",
  "turn this into a case study", "proof points for [client]", "showcase what we did for [client]",
  "client results content", "write our case study for [company]", "client impact story",
  "document this win", "which clients should we case study", "find case study opportunities",
  "who should we case study next", "case study pipeline", "identify case study candidates",
  "niche clients without case studies", "high-ticket clients we should document", or any request
  involving client outcomes, proof points, publishable win stories, or auditing which sectors
  lack proof content. Also trigger when a client hit a milestone or delivered strong results.
---

# Case Study Builder

A case study that moves the needle is not a description of what you sold. It is proof that you
changed something specific for someone real. The prospect reading it should see themselves in the
client, feel the friction the client felt, and believe — with evidence — that you can do the
same for them.

This skill runs two modes. Pick the one that matches where you are:

**Mode A: Pipeline Scan** — You want to find and prioritize case study opportunities across
your client base. Good for quarterly audits, identifying niche industry gaps, or planning
content for a specific vertical.

**Mode B: Build** — You already know which client to case study. You want to gather the
evidence, verify it, shape it for the right buyer, and produce the deliverables.

---

## Step 0: Mode and Brand Selection

Start every session with two quick decisions:

**1. Mode selection** — Ask the user (via `AskUserQuestion`) which mode they want:
- Pipeline Scan (find and prioritize case study opportunities)
- Build (produce a case study for a specific client)

**2. Brand selection** — This skill works across all entities. Ask which brand is publishing
this case study. The brand determines voice, visual identity, and which brand skill to load.

If the user's opening message already makes both clear, skip the questions and proceed.

---

## Mode A: Pipeline Scan

The goal is to surface the highest-value case study opportunities from the existing client
base, with specific priority given to niche industries and high-ticket deals that have no
proof content yet.

Load `references/opportunity-scoring.md` now. It contains the scoring rubric and the priority
framework for niche and high-ticket accounts.

### What to collect from the user

Ask for one of:
- A list of active or recent clients (names, industries, deal sizes, outcomes if known)
- A vault folder or client MOC to scan
- A specific vertical or segment they want to prioritize

### What to produce

A prioritized pipeline table ranked by case study value score:

| Client | Industry | Deal Size | Outcome Known | Verifiable | Score | Recommended Action |
|--------|----------|-----------|--------------|------------|-------|--------------------|
| ...    | ...      | ...       | ...          | ...        | ...   | ...                |

**Priority tiers:**
- **Build Now**: Strong metrics, verifiable, niche industry with no existing case study
- **Track**: Good client, outcome still developing. Set a follow-up date.
- **Skip**: Insufficient data, client unlikely to approve, or sector already well-covered

For every "Build Now" client, explicitly call out whether this is a niche or high-ticket
account with no existing case study. These are the highest-priority candidates.

For Lake B2B accounts: Sean (Customer Service and file delivery) is the right person to
confirm what outcomes are on record. Note this in the table where verification requires
delivery data.

---

## Mode B: Build

Work through these six phases in sequence. Each phase gates the next.

### Phase 1: Information Gathering

Load `references/intake-checklist.md`. This file defines the tiered evidence requirements:
Tier 1 (must-have), Tier 2 (strong-to-have), and Tier 3 (nice-to-have).

Use `AskUserQuestion` to run the intake. Maximum two rounds. Batch all questions.

**First-round questions:**
1. Which client and industry? Are we naming them publicly or anonymizing?
2. What product or service did they purchase and at what scale?
3. What hard outcomes do you have? (Leads, response rates, conversions, revenue, event
   attendance, data quality scores — whatever was tracked.)
4. Do you have a direct quote or written feedback from the client?

**Second round (if needed):**
- What was their situation before they came to you? What problem were they solving?
- What was the timeline from purchase to measurable result?
- Is there campaign data, delivery reports, or file-based evidence that CS or Sean can pull?

After intake, present the completeness table from `references/intake-checklist.md` and give
a clear verdict: proceed now, or go back for more evidence first.

A case study with no hard metrics is an anecdote. An anecdote does not close deals.

### Phase 2: Verification

A case study must survive scrutiny. Before writing, verify the key claims.

Load `references/verification-sources.md`. It covers how to validate different evidence types:
CS records, campaign delivery files, client approvals, and what to do when data is thin.

**Core verification questions to resolve:**
- Can campaign data be confirmed against what was actually delivered? For Lake B2B accounts,
  Sean in CS/file delivery has access to what was sent, when, and to what contacts.
- Has the client approved being named? If not, what anonymization keeps this compelling?
- Are outcome numbers from actual tracking data or client self-reported? Both are usable,
  but they require different framing.
- Is there any risk the client could dispute the claims? Flag it and adjust the copy.

Do not write if a Tier 1 evidence item is unverified. Return to the user with a specific
request — for example: "To confirm the open rate figure, can Sean pull the delivery report
for this campaign?"

### Phase 3: Audience Mapping

A case study written for a CIO reads differently than one written for a CMO, CFO, or a
Founder. The evidence you lead with, the vocabulary you use, and what you emphasize all
shift depending on who has the budget and what is keeping them up at night.

Load `references/audience-buckets.md`. It defines the primary buyer buckets for B2B services,
their core concerns, what they scan for first, and how to weight the case study for each.

Ask the user: "Who is the primary reader? The person most likely to share this internally
or use it to make a purchase decision?"

Map the evidence to the audience lens before touching the narrative. This is not about
changing facts. It is about deciding what to lead with and what angle holds the piece together.

### Phase 4: Narrative Construction

Load `references/storytelling-framework.md`. Map all verified evidence to the six sections
of the IMPACT framework. Build the arc before writing a word.

Core principles:
- Lead with the client's world, not your product. First paragraph is about them.
- Specificity beats generality every time. "Generated 47 qualified leads in 6 weeks" beats
  "improved lead generation significantly."
- The "before" state must be visceral. If the reader does not feel the problem, they will
  not feel the resolution.
- Numbers are the emotional climax. Build toward them. Do not open with them.
- The client's voice is the most trusted in the room. If you have a quote, anchor the
  whole piece around it.

Apply the audience lens from Phase 3 to all narrative decisions.

### Phase 5: Dual-Format Output

Load `references/output-templates.md`. Generate both formats in the same response.

**On-page content** (landing page version):
- Purpose: SEO traffic, first impression, credibility signal, CTA to gate the full PDF
- Length: 300-500 words of body copy, 3-4 stat callouts in large format
- Structure: Headline (outcome, not solution) / stat callouts / teaser story / pull quote /
  CTA: "Download the full case study"

**Full PDF case study** (complete evidence package):
- Purpose: Travels in email chains, gets forwarded to decision-makers, closes the skeptics
- Length: 600-1,000 words depending on evidence depth
- Structure: Follows the full IMPACT framework from `references/storytelling-framework.md`

Gate the PDF behind a single email field only. No title, no company, no phone. Lower friction
means more captures. Every captured email enters the nurture sequence.

### Phase 6: Design Handoff

Once both output formats are approved, generate the design handoff package.

Load `references/design-handoff.md`. It contains format specs, the component checklist,
and the brief a designer needs to produce the final assets without back-and-forth.

The handoff covers:
- File formats required (PDF layout, web component, social proof cards)
- Brand spec reference (point the designer to the relevant brand skill)
- Typography, color, and layout guidance specific to case studies
- Copy blocks formatted as designer-ready annotations
- Stat callout treatment (the big-number sections that need visual punch)
- Photo and illustration needs with sourcing guidance

Present the handoff as a formatted brief the user can drop into Notion, Figma, or email
to the designer directly.

---

## Standing Priority Directive

**Niche industries with high-ticket deals and no existing case study = highest priority.**

When running Pipeline Scan or advising what to build next, always check whether the sector
already has proof content. If it does not, escalate urgency. One well-placed case study in
an uncovered vertical can open an entire segment.

For Lake B2B accounts: Sean (CS and file delivery) is the canonical source for delivery
records, contact list specs, and campaign file confirmation. Route all verification that
requires delivery data through Sean.

---

## Multi-Entity Voice Notes

| Brand | Data focus | Hero metric | Voice |
|-------|-----------|-------------|-------|
| Lake B2B | Data precision, ICP match, list quality | Conversion rate, lead volume | Authoritative, data-first |
| SPAN Global Services | Outreach execution, response rate, pipeline | Meetings booked, pipeline value | Results-driven, energetic |
| Ampliz | Healthcare data accuracy, compliance-safe reach | Niche audience penetration | Precise, trust-forward |
| Champions Group | Cross-portfolio wins, accelerator outcomes | Growth rate, expansion | Visionary, founder-to-founder |

Load the matching brand skill alongside this one for full voice and visual alignment.
