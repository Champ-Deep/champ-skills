---
name: span-brand-guidelines
description: Brand guidelines for SPAN Global Services, a B2B data and demand generation company. Use when creating any SPAN-branded content including presentations, documents, SEO content, emails, sales assets, landing pages, internal tools, or any design work requiring SPAN branding. Also trigger for anything involving the Phoenix team, Murugan, Preeti, Gary, or SPAN-facing campaigns. MANDATORY TRIGGER for all SPAN-related content creation and design tasks.
---

# [[SPAN Global Services]] [[Brand Guidelines]]

Brand guidelines for [[SPAN Global Services]], enabling creation of on-brand content and internal tools.

## Brand [[Overview]]

**Company:** [[SPAN Global Services]] (trading names: [[span-kb|SPAN]], SGS, [[span-kb|Span Global]])
**Tagline:** Vertical Specialist Data Intelligence
**Industry:** B2B Data Services, Demand Generation, SEO, Content Syndication
**Parent:** [[Champions Group]]
**Positioning:** "Vertical specialist beats horizontal spray-and-pray" — differentiated against ZoomInfo, [[Apollo]], Cognism, Lusha

[[span-kb|SPAN]] is an enterprise data services company selling verified B2B contact data, lead generation, email campaign execution, intent data, content syndication, and SEO services across seven vertical markets.

---

## Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| [[span-kb|SPAN]] Green | #1B6B3A | 27, 107, 58 | THE brand color. Buttons, headers, accents on light. |
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
| [[span-kb|SPAN]] Green Gradient | #1B6B3A to #2D9B55 | Buttons, CTAs, section headers |
| Teal Accent | #00D4AA to #1B6B3A | Highlight sections, progress bars |
| Dark Hero | #0F2B3C to #1A3A4A | Dark backgrounds, hero sections |
| Dark Green Hero | #0C1F18 to #0F2B3C | Richest dark theme variant |

---

## Typography

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

---

## Brand Voice

| Attribute | Description |
|-----------|-------------|
| **Authoritative** | [[span-kb|SPAN]] owns vertical data. Cite stats. Use industry terms correctly. |
| **Precise** | Specific numbers, specific verticals, specific proof points. |
| **Direct** | No corporate waffle. CIO/CISO/CMO readers want clarity, not fluff. |
| **Compliance-Aware** | Healthcare = HIPAA. Legal = GDPR. Always acknowledge compliance. |
| **Specialist, not Generic** | Never "B2B data company." Always the vertical: "healthcare data specialist." |

### Voice Anti-Patterns

- Never: "We have everyone in our database" (horizontal spray-and-pray language)
- Never: "data vendor" or "email list provider" (positions as commodity)
- Never: Generic enthusiasm without proof points
- Always: Lead with the buyer's urgency trigger (HIPAA deadline, CSRD enforcement, etc.)
- Always: Name the vertical explicitly

---

## Vertical Identity

[[span-kb|SPAN]] covers seven declared verticals. Always use these exact names:

1. Healthcare and Life Sciences
2. Renewable Energy and Clean Tech
3. Cybersecurity and InfoSec
4. Legal Tech
5. Agritech
6. Construction and PropTech
7. EdTech and Higher Ed

---

## Light Theme Design System (Client-Facing and Internal Tools)

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

## Dark Theme Design System (Rich Content and Immersive Tools)

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

## Logo Rules

- Source: `Atlas/Context Docs/SPAN Global Services/` (PPTX and HTML brand book)
- Primary logo: horizontal lockup, [[span-kb|SPAN]] Green on white or white on dark
- Minimum clear space: match height of capital "S"
- Never: recolor outside palette, stretch, place on busy backgrounds
- On dark backgrounds: white logotype or light green version only

---

## Key People ([[SPAN Global Services|Phoenix]] Team)

| Person | Role | Content Link |
|--------|------|-------------|
| [[Gary]] | Head of Sales | Pricing, deals, case studies |
| [[Murugan]] | Nurturing Specialist | Lead sequences, content distribution |
| [[Preeti]] | SEO Specialist | Content optimization, landing pages |
| Lam | Account Manager | Prospect volume, account intel |
| Tim / [[Travis]] | BD Coordinators | Outbound execution |

---

## SEO Content Standards

[[span-kb|SPAN]]'s SEO strategy is the "Q2 2026 Authority Blitz" — vertical-specialist content to out-flank horizontal platforms.

- Format: "Companies Using X" lists, "Vertical Email List" hubs, HIPAA/GDPR/SEC compliance angles
- Tone: Evidence-first, compliance-aware, vertical-specialist
- CTAs: Free sample (250-500 contacts from relevant vertical)
- Internal linking: All vertical pages cross-link within sector clusters
- Counter-publishing: when a horizontal (ZoomInfo, [[Apollo]]) publishes generic content, [[span-kb|SPAN]] counters with a specialist angle within the week

---

## Source Files

- Brand book: `Atlas/Context Docs/SPAN Global Services/Span Brand Book.html`
- Brand book (slides): `Atlas/Context Docs/SPAN Global Services/Span Brand Book.pptx`
- KB: `Atlas/Ops/RAG/KB/span-kb.md`
- Company note: `Atlas/Companies/SPAN Global Services.md`
- Thought Leader Pulse (weekly): `Atlas/Context Docs/SPAN Global Services/`

---

## Usage Notes

This skill should be loaded whenever creating:
- [[span-kb|SPAN]]-branded onboarding materials, internal tools, or templates
- SEO content, blog posts, or landing pages for [[span-kb|SPAN]]
- Sales assets, email sequences, or outreach for the [[SPAN Global Services|Phoenix]] team
- Any HTML/CSS artifact in the [[span-kb|SPAN]] color system
- Reports or dashboards surfaced to the [[span-kb|SPAN]] team

**Do not** use [[span-kb|SPAN]] brand [[colors]] for [[Ampliz]], [[Lake B2B]], or [[Champions Group]] materials. Each entity has its own brand skill.
