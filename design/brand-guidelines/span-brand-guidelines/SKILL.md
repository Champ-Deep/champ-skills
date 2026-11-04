---
name: span-brand-guidelines
description: Brand guidelines and design system for SPAN Global Services, a B2B data and demand generation company. Use when creating any SPAN-branded content including SPAN web pages, landing pages, presentations, documents, SEO content, emails, sales assets, internal tools, or any design work requiring SPAN branding. Also trigger for anything involving the Phoenix team, Murugan, Preeti, Gary, or SPAN-facing campaigns. MANDATORY TRIGGER for all SPAN-related content creation and design tasks.
---

# SPAN Global Services Brand Guidelines

Brand guidelines for SPAN Global Services, enabling creation of on-brand content, pages and internal tools. Read "Which dialect" first: SPAN has two page looks, and picking the wrong one is the most common mistake.

## Brand Overview

**Company:** SPAN Global Services (trading names: SPAN, SGS, Span Global)
**Tagline:** Vertical Specialist Data Intelligence
**Industry:** B2B Data Services, Demand Generation, SEO, Content Syndication
**Parent:** Champions Group
**Positioning:** "Vertical specialist beats horizontal spray-and-pray", differentiated against ZoomInfo, Apollo, Cognism, Lusha

SPAN is an enterprise data services company selling verified B2B contact data, lead generation, email campaign execution, intent data, content syndication, and SEO services. The current web focus is technographic data: who uses which technology, with counts verified by the SPAN data team.

---

## When someone else sends us a guideline

If a designer or developer hands SPAN a brand or style guideline to review, follow `references/guideline-submission-review.md`: extract the full text first, recompute every claimed contrast ratio with `scripts/wcag_contrast.py`, count the live site's actual colours from its CSS, then split the answer into design fixes you can approve and decisions (font family, tagline, figures) that go to Deep as numbered options with a recommendation first. Nothing is sent back until Deep approves the wording. Two rules are always on: a stated contrast ratio or stat is never evidence, and conflicts with our own standing rules (zero dashes, sourced counts, both dialects, stat band on white) are listed as changes, not observations.

## Which dialect (read first)

| Surface | Dialect | Fonts | Palette | Start from |
|---|---|---|---|---|
| Landing pages, ad pages, decks, sales assets | **Brand** | Montserrat headings, Inter body | SPAN Green #1B6B3A, Teal #00D4AA, Navy #0F2B3C (below) | `span-landing-page` and its bundled examples |
| Content pages on spanglobalservices.com: answer pages, users lists, company profiles, comparisons | **Content** | Mulish only | Mint and forest greens, light and dark modes | `references/design-system.md` |

Both share the voice, the vertical names, the zero-dash rule and the CTA wording. Do not mix fonts or palettes inside one page. The full SPAN design system (tokens, type scale, layout, components, review process) lives in `references/design-system.md`. It is the standard: propose changes to it, do not fork it per page.

---

## Color Palette (Brand dialect)

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| SPAN Green | #1B6B3A | 27, 107, 58 | THE brand color. Buttons, headers, accents on light. |
| Light Green | #3DBE6E | 61, 190, 110 | Accent on dark backgrounds, stat highlights |
| Teal | #00D4AA | 0, 212, 170 | Secondary accent, data highlights, dividers |
| Dark Navy | #0F2B3C | 15, 43, 60 | Dark backgrounds, hero sections |
| Mid Navy | #1A3A4A | 26, 58, 74 | Dark surface cards |

### Supporting Colors

| Name | Hex | Usage |
|------|-----|-------|
| Amber | #F5A623 | Warnings, "important" tags, secondary highlights |
| Light Green Tint | #E8F5EE | Subtle backgrounds on green sections |
| Teal Tint | #E6FAF7 | Subtle backgrounds on teal sections |
| Off-White | #F5F7F9 | Page backgrounds (light theme) |
| Surface White | #FFFFFF | Cards on light theme |
| Surface Border | #D9E3E9 | Card borders, dividers (light) |
| Dark Text | #1E2A32 | Primary text (light theme) |
| Dim Text | #4D6070 | Secondary text |
| Muted Text | #8FA0AC | Tertiary text, labels |

### Gradients

| Name | Values | Usage |
|------|--------|-------|
| SPAN Green Gradient | #1B6B3A to #2D9B55 | Buttons, CTAs, section headers |
| Teal Accent | #00D4AA to #1B6B3A | Highlight sections, progress bars |
| Dark Hero | #0F2B3C to #1A3A4A | Dark backgrounds, hero sections |
| Dark Green Hero | #0C1F18 to #0F2B3C | Richest dark theme variant |

---

## Typography (Brand dialect)

### Font Stack

- **Headlines:** Montserrat (800 ExtraBold, 700 Bold, 600 SemiBold)
- **Body:** Inter (400 Regular, 500 Medium, 600 SemiBold)
- **Monospace / Labels:** JetBrains Mono or Space Mono (data, codes, tags)
- **Google Fonts import:** `Montserrat:wght@600;700;800` + `Inter:wght@400;500;600`

### Type Scale

| Use | Font | Weight | Size |
|-----|------|--------|------|
| Hero H1 | Montserrat | 800 | clamp(2rem, 5vw, 3.2rem) |
| Section H2 | Montserrat | 700 | 1.6rem |
| Card H3 | Montserrat | 600 | 1.1rem |
| Body | Inter | 400 | 0.95rem |
| Labels/Tags | Space Mono | 400 | 0.68-0.75rem |
| Stats | Montserrat | 800 | 2rem+ |

Content dialect type is in `references/design-system.md`.

---

## Brand Voice

| Attribute | Description |
|-----------|-------------|
| **Authoritative** | SPAN owns vertical data. Cite stats. Use industry terms correctly. |
| **Precise** | Specific numbers, specific verticals, specific proof points. |
| **Direct** | No corporate waffle. CIO/CISO/CMO readers want clarity, not fluff. |
| **Compliance-Aware** | Healthcare = HIPAA. Legal = GDPR. Always acknowledge compliance. |
| **Specialist, not Generic** | Never "B2B data company." Always the vertical: "healthcare data specialist." |

### Voice Anti-Patterns

- Never: "We have everyone in our database" (horizontal spray-and-pray language)
- Never: "data vendor" or "email list provider" (positions as commodity)
- Never: Generic enthusiasm without proof points
- Never: an unsourced or unconfirmed number. Counts come from the data team in writing, with a verified date.
- Never: em or en dashes. Use periods, commas, colons.
- Always: Lead with the buyer's urgency trigger (HIPAA deadline, CSRD enforcement, etc.)
- Always: Name the vertical explicitly

---

## Vertical Identity

SPAN covers seven declared verticals. Always use these exact names:

1. Healthcare and Life Sciences
2. Renewable Energy and Clean Tech
3. Cybersecurity and InfoSec
4. Legal Tech
5. Agritech
6. Construction and PropTech
7. EdTech and Higher Ed

---

## Light Theme Design System (Brand dialect; client-facing and internal tools)

Use for internal onboarding docs, dashboards, reports, and materials that should feel clean and professional.

```css
:root {
  --bg:          #F5F7F9;
  --surface:     #FFFFFF;
  --surface-2:   #EEF2F6;
  --border:      #D9E3E9;
  --border-hi:   #B8CACF;
  --accent:      #1B6B3A;   /* SPAN Green - use on light bg */
  --accent-soft: #E8F5EE;
  --accent-mid:  #2D9B55;
  --teal:        #00D4AA;
  --teal-soft:   #E6FAF7;
  --amber:       #F5A623;
  --amber-soft:  #FEF3E2;
  --rose:        #E8415A;
  --rose-soft:   #FDECEF;
  --text:        #1E2A32;
  --text-dim:    #4D6070;
  --text-muted:  #8FA0AC;
}
```

---

## Dark Theme Design System (Brand dialect; rich content and immersive tools)

Use for hero sections, presentations, dark-mode tools, and SEO landing pages.

```css
:root {
  --bg:          #0F2B3C;   /* SPAN Navy */
  --surface:     #1A3A4A;
  --surface-2:   #1F4356;
  --border:      #2A5468;
  --accent:      #3DBE6E;   /* Light Green - readable on dark */
  --accent-soft: rgba(61, 190, 110, 0.12);
  --teal:        #00D4AA;
  --teal-soft:   rgba(0, 212, 170, 0.12);
  --amber:       #F5A623;
  --text:        #FFFFFF;
  --text-dim:    rgba(255, 255, 255, 0.65);
  --text-muted:  rgba(255, 255, 255, 0.4);
}
```

---

## Section Rhythm (standing rule, Deep 2026-10-25)

A stat band (contact counts, refresh date, provider counts) that follows a dark or brand-filled hero is always the inverse scheme: Surface White ground, SPAN Green #1B6B3A figures in Montserrat 800, Dim Text labels, Surface Border hairlines between figures. Never fill it with green. It exists to break the page between the dark hero and the body; a green band reads as the hero continuing. Keep this in every skin and iteration of a SPAN landing page. If there are no verified counts, omit the band.

## Logo Rules

- Source: the SPAN brand book (HTML and PPTX), held by Deep's team. Ask Deep for the current files. A transparent PNG logo ships inside `span-landing-page/assets/campaign-landing/examples/`.
- Primary logo: horizontal lockup, SPAN Green on white or white on dark
- Minimum clear space: match height of capital "S"
- Never: recolor outside palette, stretch, place on busy backgrounds
- On dark backgrounds: white logotype or light green version only

---

## Key People

| Person | Role | Content Link |
|--------|------|-------------|
| Gary | Head of Sales, Phoenix team lead | Pricing, deals, case studies |
| Murugan | Nurturing Specialist | Lead sequences, content distribution |
| Preeti | SEO Specialist, owns SPAN SEO and page approval | Content optimization, landing pages, final say on page content |
| Manu | Developer on SPAN web | Technical approval of new pages and deployment |
| Aishwarya | Content Writer, reports to Preeti | Answer pages, profiles, comparisons |
| Santhosh | Data team | Confirms every count before it is published |
| Pallab | Reviews SPAN ad landing pages and budget | Paid campaign sign-off |
| Harsha | Page builder: structures, designs and deploys SPAN pages from team content | Landing pages and content pages |
| Lam | Account Manager | Prospect volume, account intel |
| Tim / Travis | BD Coordinators | Outbound execution |

New pages: Harsha builds, Preeti or Manu approves the first two or three before deployment, then review is weekly.

---

## SEO Content Standards

SPAN's SEO strategy is vertical-specialist and technology-led content to out-flank horizontal platforms.

- Format: "[Technology] Users List" pages, answer pages, company profiles, comparisons, category hubs under Technographic Data; HIPAA/GDPR/SEC compliance angles where a vertical needs them
- Tone: Evidence-first, compliance-aware, vertical-specialist
- CTAs: Free sample (250 to 500 contacts, or 25 free records on a technology page, as the page brief says)
- Internal linking: pages cross-link within sector and technology clusters, minimum 3 internal links
- Counter-publishing: when a horizontal (ZoomInfo, Apollo) publishes generic content, SPAN counters with a specialist angle within the week
- Page rules: `span-answer-page`. Company pages: `span-company-profile`. Ad landing pages: `span-landing-page`.

---

## Usage Notes

Load this skill whenever creating:
- SPAN-branded onboarding materials, internal tools, or templates
- SEO content, blog posts, or landing pages for SPAN
- Sales assets, email sequences, or outreach for the Phoenix team
- Any HTML/CSS artifact in the SPAN color system
- Reports or dashboards surfaced to the SPAN team

**Do not** use SPAN brand colors for Ampliz, Lake B2B, or Champions Group materials. Each entity has its own brand skill.
