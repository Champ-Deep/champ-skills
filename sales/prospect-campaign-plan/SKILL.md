---
name: prospect-campaign-plan
description: >
  Turns a company URL into a polished, self-contained HTML campaign plan: brand research, 2 audience personas, messaging hierarchy, 3 email templates (rendered as real email mocks), 3 LinkedIn post formats, 12-week content calendar, budget allocation, KPI framework, and pivot triggers. Single HTML file, fixed sidebar nav, mobile-responsive, deployable to Netlify in seconds. MANDATORY TRIGGER for: "campaign plan for [URL]", "marketing plan for [company]", "prospect campaign", "create a campaign document", "build a campaign plan", "marketing strategy for [URL]", "full campaign for [company]", "pitch deck for [prospect]". Also trigger when a URL is provided alongside "campaign", "strategy", "marketing", "outreach", or "plan" — even with minimal context. The skill handles everything: research, strategy, content, design, and deploy nudge.
---

# Prospect Campaign Plan Skill

You are building a complete, standalone HTML marketing campaign plan for a prospect or client. The deliverable is a single `.html` file — polished enough to share with a client as a live link, detailed enough to serve as a real execution roadmap.

This skill is the full pipeline: research → strategy → content → design → build → deploy.

---

## Phase 1: Research

**Goal**: Understand the business well enough to write a real campaign plan, not a generic one.

Use the `firecrawl` skill to scrape the provided URL. If firecrawl is unavailable, use `WebFetch` then `WebSearch`. Extract:

- **Core offering**: What do they sell or provide? Be specific.
- **Target audience signals**: Who does the site speak to? B2B or B2C? Industry? Seniority?
- **Geographic focus**: Local, regional, national, global?
- **Brand tone**: Formal/authoritative, approachable, technical, luxury?
- **Differentiators**: What makes them different from competitors? Look for explicit claims.
- **Price point signals**: Premium, mid-market, budget?
- **Visual brand**: Extract the brand color system with precision — you will map these directly to CSS vars in Phase 5. Look for:
  - **Background/primary color**: The dominant dark or light base hue used in hero sections and sidebars
  - **Action/CTA color**: The color on primary buttons, links, and highlights — the most distinctive brand color (e.g., mint turquoise, bright orange, electric blue)
  - **Typography colors**: Whether text is white-on-dark, dark-on-light, or brand-colored
  - Capture these as a **Brand Color Map** before moving on. If the site is inaccessible, derive from third-party reviews, app store screenshots, or press materials.
- **Brand tagline**: Note the exact tagline if present — it anchors the hero section and sidebar.
- **Brand voice signals**: Note 2-3 copy patterns that reveal tone (e.g., punchy imperatives, reassuring language, technical density). These inform email and LinkedIn voice.
- **Key CTAs**: What actions does the site drive toward? (Book a call, start trading, get a quote, etc.)

Also run a quick competitor search: `WebSearch("[company name] competitors [industry] [location]")` to understand the competitive landscape.

---

## Phase 2: Confidence Gate

After research, assess your confidence on these four axes:

| Axis | Question |
|------|----------|
| **Audience** | Do you know the primary buyer persona clearly? |
| **Differentiator** | Can you articulate what makes this firm genuinely different? |
| **Campaign goal** | Is the primary goal leads, awareness, or conversions? |
| **Channel fit** | Do you know which 2-3 channels this business should prioritize? |

**If confidence ≥ 80% on all four**: proceed to Phase 3 autonomously.

**If any axis is below 80%**: Use `AskUserQuestion` with a single batched call (max 3 questions). Frame questions around the gaps only. Examples:
- "Who is the primary target — individual consumers or business decision-makers?"
- "What makes [company] different from [Competitor A] and [Competitor B]?"
- "Is the immediate campaign goal bookings/leads, or building brand awareness first?"

Never ask more than one round of clarifying questions.

---

## Phase 3: Strategy (CHAMP Framework)

Work through these five dimensions. These become the "CHAMP Analysis" section of the document.

- **C — Customer**: Define 2 personas. Each needs: role/title, pain points (3), goals (2), tone preference, objections (2).
- **H — Hypothesis**: One sentence: "We believe [audience] will engage with [company] when they see [positioning], because [insight]."
- **A — Approach**: Recommended channel mix with rationale. Choose 3-4 from: email, LinkedIn, Google Ads, SEO content, WhatsApp, Instagram, events.
- **M — Market**: Estimated addressable segment. Include geography, size, and key sub-segments.
- **P — Pivot**: 2-3 trigger conditions that should cause a strategy shift (e.g., "If email open rate < 25% by Week 4, switch to LinkedIn-first").

---

## Phase 4: Content Planning

Build out all content sections. Details for each are in `references/content-framework.md`.

1. **Messaging hierarchy**: Brand promise → differentiator → proof point → CTA. One version for each persona.
2. **Email sequences** (3 templates):
   - Email 1: Welcome / Authority (Phase 1)
   - Email 2: Nurture / Insight (Week 3, persona-segmented)
   - Email 3: Conversion / CTA (Week 6)
3. **LinkedIn post templates** (3 formats):
   - Format 1: Thought leadership hook (listicle)
   - Format 2: Regulatory/news alert (timely)
   - Format 3: Anonymized case insight (social proof)
4. **12-week content calendar**: Month-by-month with content type, channel, and theme per week.
5. **Budget allocation**: 5-6 line items with AED/USD amounts and % of total. Include a "minimum viable" note for bootstrapped clients.
6. **KPI framework**: 8-10 metrics organized by funnel stage. Include baseline (Day 1), Month 1, Month 2, and Month 3 targets.
7. **Pivot plan**: Decision tree table — if [signal], then [action].

---

## Phase 5: Build the HTML

This is the most important phase. The output must look like a real agency deliverable, not a template.

### Design System

**Step 1: Map the Brand Color Map from Phase 1 to CSS variables.**

Every campaign plan must use the client's actual brand colors, not generic defaults. A plan that looks like a template signals that you didn't do your research — the color palette is the fastest signal of whether the document was made for this client or any client.

Apply the Brand Color Map as follows:

| Brand Color Map Field | CSS Variable | Role in Layout |
|---|---|---|
| Background/primary color | `--primary` | Sidebar, hero section, dark surfaces |
| Slightly lighter primary shade | `--primary-mid` | Secondary dark surfaces, card headers |
| Action/CTA color | `--accent` | Buttons, highlights, chart fills, hover states |
| Accent at ~10% opacity on white | `--accent-pale` | Light section backgrounds, tag chips |
| Accent darkened ~30% | `--accent-dark` | Accent text on light backgrounds (for contrast) |

For `--accent-pale`: take the accent hex and mix it at 10-15% toward white. For mint/turquoise `#00D4B4`, the pale is `#D6FAF5`. For orange `#F59E0B`, the pale is `#FEF3C7`.

All rgba() calls in the CSS that use the primary or accent colors must also be updated to match the extracted brand colors — not left at generic values.

**Only use the fallback below if brand colors genuinely could not be identified after checking the site, reviews, and app screenshots:**

```css
--primary:     #0E1238;   /* deep navy — generic fallback only */
--accent:      #CAA05C;   /* warm gold — generic fallback only */
--accent-pale: #f5e9d3;
```

**Real-world examples of color mappings:**
- Evest (fintech, MENA): `--primary: #0F1B2D` (deep slate), `--accent: #00D4B4` (mint turquoise)
- A health app with green CTA buttons: `--primary: #1A3A2A`, `--accent: #22C55E`
- A luxury brand with gold: `--primary: #1C1612`, `--accent: #C9A84C`

**Brand tagline in the hero**: If a tagline was captured in Phase 1, include it in the hero eyebrow pill and the sidebar brand sub-label. It makes the document feel bespoke, not built-for-anyone.

**Typography**: Always import and use:
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
```
Set `--font-serif: 'Playfair Display', Georgia, serif` and `--font-sans: 'DM Sans', Arial, sans-serif`.

**Never use**: Georgia or Arial as primary fonts. Never use Inter, Roboto, or Montserrat.

See `references/html-structure.md` for the full CSS scaffold and component patterns.

### Document Structure

The HTML must include these sections as `<section>` elements with matching nav links:

1. Hero (company name, campaign title, key meta)
2. CHAMP Analysis
3. Audience Personas (2 cards)
4. Messaging Hierarchy
5. Channel Strategy
6. Email Templates (3 mocked emails)
7. LinkedIn Templates (3 post cards)
8. Content Calendar (12-week table)
9. Budget Allocation
10. KPI Framework
11. Pivot Plan

### Layout Requirements

- **Fixed left sidebar** (240px): Logo area + hierarchical nav links + group labels
- **Main content** (margin-left: 240px): Full-width sections
- **Mobile header**: Fixed 56px bar with hamburger toggle (pure JS, no frameworks)
- **Sidebar slide-in** on mobile with overlay dismiss
- **All tables**: Wrapped in `<div style="overflow-x:auto">` with `min-width` set

### Email Mock Structure

Each email template should look like a real email client render, not a description. Use this structure inside `.email-mock`:

```html
<div class="em-preheader">Preheader text here</div>
<div class="em-header-top">  <!-- logo + unsubscribe link row -->
<div class="em-header-main"> <!-- hero gradient with company name + tagline -->
<div class="em-wrapper">     <!-- max-width: 600px centered content -->
  <p class="em-para">
  <div class="em-numbered-item"> <!-- card-style numbered insight -->
  <div class="em-testimonial">   <!-- big quote mark + testimonial + avatar row -->
  <div class="em-checklist">     <!-- navy-background checklist -->
  <div class="em-cta-section">   <!-- gold-pale CTA with button + no-obligation note -->
</div>
<div class="em-footer">         <!-- multi-link footer -->
```

Full CSS for all `.em-*` classes is in `references/html-structure.md`.

### Hard Rules for HTML Output

- **Zero em dashes** (`—`). Use colons, commas, periods, or restructure. This is non-negotiable.
- No `'Georgia'` or `'Arial'` as primary font values. Use CSS vars only.
- All `<td>` cells that show "N/A" or empty baseline: use `<td class="cal-na">N/A</td>` with `.cal-na { color: var(--grey-600); font-style: italic; }`.
- No inline `font-family: 'Arial'` or `font-family: Georgia` anywhere in the document. Use `var(--font-sans)` and `var(--font-serif)`.
- Sidebar nav links close the mobile menu on click.
- `scroll-behavior: smooth` on `html`.
- Hero section has subtle geometric decoration (concentric circles via `::before`/`::after`).
- Sections alternate between `var(--off-white)` and `var(--white)` backgrounds for visual rhythm.
- Card grids must use `align-items: start` so cards size naturally to their content. Never force equal-height cards — a short pivot list should look different from a long market analysis.
- Break up text-heavy card bodies. Use `<br><br>` to separate distinct thoughts, bold the key concept at the start of each block, and prefer 2-4 short sentences over one long paragraph. The goal is scannable, not exhaustive.

---

## Phase 6: Save and Deploy

1. Save the file to the workspace as `[CompanyName]_Campaign_Plan.html` (no spaces, use underscores).
2. Provide a `computer://` link so the user can open it immediately.
3. Add a brief deploy note:

> **To share this with your team or client:** Go to [netlify.com/drop](https://netlify.com/drop), drag the HTML file onto the page, and you get a live URL in seconds. No account needed.

If a Netlify MCP connector is available in the session, offer to deploy it directly.

---

## Quality Check Before Saving

Run these checks mentally before finalizing the file:

- [ ] Zero em dashes (`—`) — grep mentally for ` — ` patterns
- [ ] All tables have scroll wrappers
- [ ] Mobile hamburger menu implemented
- [ ] Google Fonts imported
- [ ] All font references use CSS vars
- [ ] Email mocks render as actual email-client-style layouts
- [ ] At least 2 distinct personas with specific detail
- [ ] Budget includes a "minimum viable" option note
- [ ] KPI table has Day 1 baselines (not just targets)
- [ ] Sidebar nav covers all 11 sections
- [ ] Brand colors from Phase 1 are applied — NOT the generic fallback defaults
- [ ] All rgba() color values in CSS match the extracted brand palette
- [ ] Client tagline (if identified) appears in hero eyebrow and sidebar sub-label
- [ ] Card grids use `align-items: start` so cards are naturally sized, not force-stretched
- [ ] Card body text is broken into short, scannable blocks — not walls of prose
