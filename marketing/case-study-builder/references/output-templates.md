# Output Templates

Two outputs are generated for every case study: an on-page version (for the landing page) and
a full PDF version (gated behind an email capture form). They share the same evidence base but
serve different purposes and audiences.

---

## Template 1: On-Page Landing Page Content

**Purpose:** Earn organic traffic, establish credibility at a glance, drive PDF downloads.
**Audience:** Cold visitors and warm prospects who found the page via SEO, social, or a sales link.
**Tone:** Direct, confident, outcome-first.
**Length:** ~300-500 words of body copy + stat callouts.

---

### On-Page Template

```
[HEADLINE]
— Lead with the outcome, not the service.
— Format: "[Specific result] for [Client / industry descriptor]"
— Examples:
    "62 Qualified Leads in 8 Weeks: How [Company] Rebuilt Their Pipeline with Precision Data"
    "How a Mid-Market SaaS Team Went from 4% to 11% Email Response Rate"
    "From Stalled Pipeline to $218K ARR: One Manufacturing Team's Turnaround"

[STAT CALLOUTS — 3 to 4 numbers, large format]
— These should be the first thing the eye lands on after the headline.
— Each callout = one number + one line of context
— Examples:
    62 qualified leads — generated in 8 weeks
    11.3% email response rate — vs. 2.8% industry average
    $218K new ARR — closed within the same quarter
    4.2x — increase over previous 8-week lead baseline

[OPENING PARAGRAPH — 60-80 words]
— Start with the client's situation before they came to you.
— Do NOT start with "We helped [company]..." or "Our client [company]..."
— Start with their world.
— Example: "The SDR team at [Company] was fighting an uphill battle.
   Their contact data was two years old, open rates had collapsed, and the pipeline
   review was the meeting nobody wanted to sit in. Three months later, that same team
   was generating 62 qualified leads every 8 weeks."

[THE STORY — 150-200 words]
— Follow the condensed IMPACT arc: friction, what was done, what happened.
— Use the Proof in Motion section to explain the solution specifically.
— End with the Actual Outcomes numbers, already stated in the callouts but now in context.
— Optional: one sentence of Cascade Effect ("This cleared the path for...")

[PULL QUOTE]
— If available, place the client quote here in a visual callout block.
— Format: "Quote text in quotation marks." — Name, Title, Company
— If no quote available, omit this block. Do not use a generic filler quote.

[CTA]
— Single, low-friction call to action.
— Copy: "Download the full case study" OR "Get the complete story"
— Sub-copy: "Drop in your email. No forms. No calls." [links to email gate]
— Do not add a phone number field. Do not ask for company or job title here.
— This is a trust-building step, not a qualification step.
```

---

## Template 2: Full PDF Case Study

**Purpose:** Complete evidence package. Travels in email chains. Gets forwarded to decision-makers.
Lives in the prospect's downloads folder until they are ready to buy.
**Audience:** Serious prospects who wanted more than the teaser, or sales recipients forwarded it.
**Tone:** Authoritative, story-driven, evidence-backed.
**Length:** 600-1000 words depending on evidence depth.

---

### PDF Template

```
[COVER SECTION]
— Client name or descriptor ("A Mid-Market Manufacturing Company")
— Brand logo (of the publishing entity: SPAN, Lake B2B, or Ampliz)
— Headline (same as on-page or slightly longer form)
— 3 top-line stat callouts in large format (same as on-page)
— Optional: client industry icon or vertical label

---

[SECTION 1: THE CHALLENGE]
Based on I — Identify the Friction from the IMPACT framework.
80-120 words.

Tell the story of their "before" world. What were they doing, what wasn't working, what was
it costing them? This section should make the reader think: "I know exactly what that feels like."

Suggested subheading: "The challenge" or simply no subheading (let the text flow).

---

[SECTION 2: WHY [CLIENT] CHOSE [BRAND]]
Based on M — Moment of Decision.
40-60 words.

Brief and factual. What made them choose you? If you have a specific reason (test sample,
referral, pricing, targeting depth), use it. If not, frame it as the criteria they were
looking for.

Suggested subheading: "Finding the right partner" or "The decision"

---

[SECTION 3: THE APPROACH]
Based on P — Proof in Motion.
100-150 words.

This is your methodology on display. Describe exactly what was delivered and how. For data
products: list type, size, targeting parameters, intent signals used, enrichment details.
For campaigns: channel, cadence, volume, personalisation approach.

Use plain language. Do not use product names or internal jargon the prospect won't recognise.
Every sentence here should add specificity, not fluff.

Suggested subheading: "The approach" or "What we delivered"

---

[SECTION 4: THE RESULTS]
Based on A — Actual Outcomes.
80-120 words + stat callout boxes.

Present the primary metric first. Then context (baseline, benchmark, time period). Then
secondary metrics. Then a qualitative outcome if available (the deal that was closed, the
conversation that changed).

Stat callouts: repeat the 3-4 numbers from the cover in a visual block embedded in the text.
Do not just list numbers — each callout should have a one-line explanation of why it matters.

Suggested subheading: "The results"

---

[SECTION 5: THE IMPACT]
Based on C — Cascade Effect.
60-100 words.

What did the results enable? How has the client's relationship with you changed? What does
their trajectory look like now? This section elevates the case study from "we delivered a
service" to "we changed what was possible for this team."

If the client has increased their spend, or renewed, mention it here (without specific pricing).
"Off the back of these results, [Company] expanded their outreach into the West Coast market
with a second dataset" is a powerful implicit endorsement.

Suggested subheading: "What changed" or "Looking ahead"

---

[SECTION 6: IN THEIR OWN WORDS]
Based on T — Testimony.
Full quote with attribution.

If you have a quote, this is the section that earns all the trust the rest of the case study
has been building. Format it as a featured pullout — large text, quotation marks, full name,
title, and company.

If no formal quote is available, use a brief paraphrase from a CS conversation, marked clearly
as paraphrased and pending client confirmation. Do NOT publish without a real attribution.

---

[CLOSING SECTION]
— 2-3 sentences: "If you're facing [variant of the client's challenge], we'd like to show you
  what this looks like for your specific situation."
— Soft CTA: "Talk to the team" or "See what your data can do" — links to a contact page or
  calendar link, NOT a demo request form.
— Brand footer: logo, website, contact info.
```

---

## Naming Convention

Use consistent file naming when generating and saving these assets:

- On-page content: `case-study-[client-or-descriptor]-onpage.md`
- PDF content: `case-study-[client-or-descriptor]-full.md`
- Final PDF file (once designed): `[brand]-case-study-[client]-[year].pdf`

Store in the vault at: `Atlas/Context Docs/[Entity]/Case Studies/`

---

## What to Hand Off to the Design Agency

When handing off to an external design team (e.g., the SPAN design agency), provide:
1. The full PDF content in `.md` or `.docx` format
2. The stat callouts listed separately (number + context line) for large-type treatment
3. The client quote marked clearly as the featured pullout element
4. Brand guidelines reference (load `lakeb2b-brand-guidelines` or `ampliz-brand-guidelines` skill
   to generate the brand brief)
5. Permission level: what can be used publicly (logo, name, photo, quote)
