---
name: "outbound-email"
description: "Full-stack B2B cold outbound email skill. Use whenever a user wants to write a cold email, outreach sequence, sales or prospecting email for B2B audiences, or gives a prospect name and company to reach out to. Enforces the CLF prospecting email rules (domain readiness with a live website, one link, plain text, 2 to 4 word subject, selling-brand signature, never Champions Group). Covers research, pitch strategy and a 3-touch sequence (cold email, follow-up, breakup). Always use it, even for a simple write a cold email to a name at a company."
---

# B2B Outbound Email Skill

Generate research-grounded, intent-matched, high-converting B2B cold email sequences.
Covers a readiness check plus three sequential phases: **Readiness → Research → Strategy → Copy**.

---

## Phase 0: Sending Readiness (CLF lead-gen standard, adopted Oct 2026)

These come from the lead-gen team that switched to them over three months and now books 15+ leads a month consistently. Sending domains with a live website outperform domains without one. Apply every rule to any prospecting or follow-up email this skill writes.

**Brand rule.** Never use Champions Group (name, domain, logo or signature) for data or lead-gen prospecting. Spam complaints and blocklists attach to whatever brand and domain the email carries, and Champions Group is the parent brand for Champion Lagoons, Royal Champion Yachts and the longevity businesses. Sign as the selling brand (LakeB2B, SPAN, Ampliz, Contact Consumers, MetricFox) and send from a dedicated prospecting domain, never from a primary brand domain.

**Before anything is sent (domain readiness).** Every prospecting domain needs:
- A basic one-page website that a prospect lands on when they search the domain: company overview, services or solutions, contact information, about or company information, and a privacy policy.
- SPF, DKIM and a valid DMARC record, plus a one-click unsubscribe for any bulk send.
- A matching identity: the sender address, website, company name and signature all name the same company. If any of these disagree, stop and fix it before writing copy.

**The eight email rules.**
1. Professional signature: sender name, title, company name, phone number, website.
2. One link only: the website in the signature. No links in the body, no tracking links, no calendar link until the prospect has replied.
3. First-touch email: 125 words maximum, ideally 100 to 125. Follow-ups are shorter.
4. Plain text only: no HTML templates, banners, images, colored fonts or heavy formatting.
5. Subject line: 2 to 4 words, natural, relevant to the message. No clickbait, no all caps, no punctuation tricks.
6. No spam or promotional language. Banned in subject and body: free, guaranteed, best price, act now, limited offer, risk-free, special promotion, urgent, 100%, no obligation, click here, exclusive deal.
7. Sender identity aligned: sending address, website, company name and signature are consistent and credible (see domain readiness).
8. Every prospecting domain has its website live before its first send (see domain readiness).

**Signature template (plain text):**
```
[Full Name]
[Title], [Selling Brand Name]
[Phone with country code]
[prospecting-domain website]
```

Roll this out gradually. Move each campaign onto these rules as its next sequence starts; do not stop live sequences mid-cadence.

### Step 0: Confirm the sender

Before research, ask for (or confirm from context): selling brand, sender name and title, phone, and the prospecting domain plus its website URL. If the website is missing or does not carry the five required pages, say so in one line and offer to draft the one-page site copy. Never fill the signature with Champions Group.

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
- ✅ One link maximum per email: the website in the signature. No body links, no tracking links
- ✅ Word count (body only, excluding subject and signature): Touch 1 is 125 words maximum, ideally 100 to 125. Touch 2 and Touch 3 are shorter
- ✅ Subject line: 2 to 4 words, natural, relevant to the message
- ✅ Full plain-text signature on every touch: name, title, selling brand, phone, website
- ✅ One CTA per email — binary yes/no question or specific time proposal only
- ✅ Prospect's first name in greeting only — no further name-drops
- ✅ One specific, named signal per email — never generic "I noticed your company…"
- ❌ No "Hope this finds you well" or equivalent filler openers
- ❌ No feature lists, bullet points, or numbered lists
- ❌ No "synergy", "leverage", "streamline", "game-changer", or similar buzzwords
- ❌ No aggressive CTAs ("Book a demo", "Click here", "Schedule a call")
- ❌ No spam or promotional words: free, guaranteed, best price, act now, limited offer, risk-free, urgent, 100%, no obligation, exclusive deal
- ❌ Never sign, send or reference Champions Group in data or lead-gen prospecting

**Touch 1 — Cold Email**
- Framework: Challenger or Audit (as selected in Step 5)
- Anchor: The single strongest trigger from the Prospect Brief
- CTA: Permission-ask only ("Worth sending over a quick breakdown?")
- Links: website in the signature only

**Touch 2 — Follow-Up (send Day 5–7)**
- Subject: `Re: [original subject]`
- Recap the core value prop in one sentence
- Give them an explicit "easy out" to reduce pressure
- CTA: Direct yes/no on current priority
- Links: website in the signature only

**Touch 3 — Breakup (send Day 12–14)**
- Ultra-short: 3–4 sentences maximum
- No guilt, no pressure — leave the door open warmly
- CTA: One final soft question or explicit close
- Links: website in the signature only. Calendar link only if they have already replied.

### Step 8 — Format the output

Present emails in this structure:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOUCH 1 — COLD EMAIL  (Day 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Subject: [subject line]

[email body]

Best,
[Full Name]
[Title], [Selling Brand]
[Phone]
[prospecting-domain website]

Word count: XX | Subject words: X | Links: 1 | Framework: [name] | Persona: [bucket]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOUCH 2 — FOLLOW-UP  (Day 5–7)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOUCH 3 — BREAKUP  (Day 12–14)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...
```

Before presenting, run the pre-send check on every touch and fix any miss:
- Sender address, website, company name and signature name the same company
- Exactly one link (signature website), plain text, no images
- Subject 2 to 4 words; Touch 1 body 125 words or fewer
- No spam words; no Champions Group anywhere

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