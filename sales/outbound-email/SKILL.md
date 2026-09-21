---
name: outbound-email
description: "Full-stack B2B cold outbound email skill. Use this skill whenever a user wants to write, generate, or build a cold email, outreach sequence, sales email, or prospecting email for B2B audiences. Also trigger when the user provides a prospect name and/or company and wants to reach out, pitch, or start a conversation. Covers the full workflow: prospect research → pitch strategy → 3-touch email sequence (cold email + follow-up + breakup). Always use this skill even if the user simply says \"write a cold email to [name] at [company]\" — do not attempt outbound email generation without it."
---

# B2B Outbound Email Skill

Generate research-grounded, intent-matched, high-converting B2B cold email sequences.
Covers three sequential phases: **Research → Strategy → Copy**.

---

## Phase 1: Prospect Research

### Step 1 — Collect inputs

Minimum required: **Prospect name** + **Company name**.
Optional (use if provided): job title, industry, known pain point, user-supplied intent signals.

If the user has not provided a job title, infer it from web search before proceeding.

### Step 2 — Run parallel research

Search across all available sources simultaneously:

| Source | What to look for |
|---|---|
| Web search (company) | Recent news, press releases, product launches, partnerships, expansions |
| Web search (funding/hiring) | Funding rounds, headcount growth, new executive hires, open roles |
| Company website | Industry vertical, tech stack signals, stated mission/ICP |
| LinkedIn signals (via web search) | Prospect's recent posts, job changes, content engagement themes |
| User-provided intent signals | Treat as highest-priority anchor — always incorporate verbatim |

### Step 3 — Synthesise a Prospect Brief

After research, produce a **Prospect Brief** (internal, shown to user before writing emails):

```
PROSPECT BRIEF
──────────────
Name:           [First Last]
Title:          [Job Title]
Company:        [Company Name]
Industry:       [Detected Vertical]
Persona Bucket: [Title Tier] × [Industry Vertical]

TOP SIGNALS FOUND:
• Signal 1 — [e.g., Series B raise, $18M, Jan 2026]
• Signal 2 — [e.g., Hiring 3 SDRs in APAC]
• Signal 3 — [e.g., Recently switched CRM from HubSpot to Salesforce]

LIKELY PAIN POINT:  [1-sentence hypothesis based on signals]
STRONGEST TRIGGER:  [Single best signal to anchor the pitch]
```

Show the Prospect Brief to the user and ask if they want to correct or add anything before continuing.

---

## Phase 2: Pitch Strategy

### Step 4 — Map signals to services

Based on the strongest trigger identified, present **2–3 service options** ranked by fit.
Read `/references/service-catalogue.md` for the full signal → service mapping logic.

Present options like this:

```
RECOMMENDED PITCH OPTIONS (ranked by signal fit):

1. [Service Name] — [1-line reason tied to the trigger]
2. [Service Name] — [1-line reason tied to the trigger]
3. [Service Name] — [1-line reason tied to the trigger] (optional)

Which would you like to lead with? (or say "combine 1+2" to blend angles)
```

Wait for user confirmation before writing any emails.

### Step 5 — Select pitch framework

Once the service is confirmed, select the **pitch framework** based on the trigger type:

| Trigger Type | Best Framework |
|---|---|
| Hiring surge / new role / expansion | Signal-Based Challenger |
| Tech stack change / integration | Signal-Based Challenger |
| Funding round / market pivot | Signal-Based Challenger |
| Operational inefficiency signal | Value-First Asynchronous Audit |
| No strong signal found | Value-First Asynchronous Audit (generic angle) |

Read `/references/pitch-frameworks.md` for full framework structures and example copy.

### Step 6 — Identify persona bucket

Cross-reference **title tier** × **industry vertical** to load the correct tone rules.
Read `/references/persona-matrix.md` for the full matrix.

---

## Phase 3: Copy Generation

### Step 7 — Write the 3-touch sequence

Write all three emails in one pass after strategy is confirmed.

**Hard rules that apply to ALL three emails — no exceptions:**
- ✅ Plain text only — zero HTML, zero images, zero inline formatting
- ✅ Zero links of any kind in Touch 1 and Touch 2
- ✅ Word count: 50–125 words per email (excluding subject line and sign-off)
- ✅ One CTA per email — binary yes/no question or specific time proposal only
- ✅ Prospect's first name in greeting only — no further name-drops
- ✅ One specific, named signal per email — never generic "I noticed your company…"
- ❌ No "Hope this finds you well" or equivalent filler openers
- ❌ No feature lists, bullet points, or numbered lists
- ❌ No "synergy", "leverage", "streamline", "game-changer", or similar buzzwords
- ❌ No aggressive CTAs ("Book a demo", "Click here", "Schedule a call")

**Touch 1 — Cold Email**
- Framework: Challenger or Audit (as selected in Step 5)
- Anchor: The single strongest trigger from the Prospect Brief
- CTA: Permission-ask only ("Worth sending over a quick breakdown?")
- Links: None

**Touch 2 — Follow-Up (send Day 5–7)**
- Subject: `Re: [original subject]`
- Recap the core value prop in one sentence
- Give them an explicit "easy out" to reduce pressure
- CTA: Direct yes/no on current priority
- Links: None

**Touch 3 — Breakup (send Day 12–14)**
- Ultra-short: 3–4 sentences maximum
- No guilt, no pressure — leave the door open warmly
- CTA: One final soft question or explicit close
- Links: None. Calendar link only if they have already replied.

### Step 8 — Format the output

Present emails in this structure:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOUCH 1 — COLD EMAIL  (Day 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Subject: [subject line]

[email body]

Best,
[Name]

Word count: XX | Framework: [name] | Persona: [bucket]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOUCH 2 — FOLLOW-UP  (Day 5–7)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOUCH 3 — BREAKUP  (Day 12–14)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...
```

After presenting, offer:
- Tone adjustment ("make it more direct / warmer / more senior")
- Service angle swap
- A/B subject line variants

---

## Reference Files

| File | When to read |
|---|---|
| `references/service-catalogue.md` | Step 4 — signal-to-service mapping |
| `references/pitch-frameworks.md` | Step 5 — full framework structures + examples |
| `references/persona-matrix.md` | Step 6 — tone rules by title tier × vertical |

## Final gate: no AI slop (mandatory before delivery)

Everything this skill produces that a person will read (client, prospect, vendor, partner, public, or the sales team) passes a no-AI-slop check before it is delivered. Load the `no-ai-slop` skill in Gate mode and run its Eval on the final copy. If that skill cannot be loaded, apply this minimum:

- Zero em dashes and en dashes anywhere, including headings, titles, subject lines, and date ranges. Use periods, commas, colons, parentheses, or restructure.
- Cut binary contrasts ("It's not X, it's Y", "Not because X. Because Y."), throat-clearing openers ("Here's the thing"), faux-insight setups ("What nobody tells you"), colon reveals ("The best part: it learns"), dramatic fragments ("That's it."), rhetorical setups, fake-profound kickers, and recap endings.
- Cut puffery and weasel attribution ("a testament to", "pivotal moment", "experts agree", "studies show"). Name the source or drop the claim. Never invent a source, stat, or quote.
- Banned words: delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, seamless, unlock, synergy, game changer, tapestry, realm, beacon, multifaceted, meticulous, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving.
- Portability test: a sentence that could move unchanged to another company is filler. Replace it with a name, number, date, or mechanism, or cut it.
- Repeat the right word instead of cycling synonyms. Active voice, human subjects, direct verbs. No decorative bold or emoji headings.
- This gate governs style only. It never overrides this skill's factual, brand, or client-safety rules (vendor firewall, entity separation, verified numbers).