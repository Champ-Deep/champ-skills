# Design Handoff Guide

Once both output formats are approved by the user, produce a design brief the designer
can pick up and execute without a meeting. A good handoff eliminates back-and-forth.
A bad handoff generates 6 rounds of revision and a frustrated creative team.

This file defines what to include in the brief, the format specs for each deliverable,
and the common failure modes to head off before they happen.

---

## What to Produce

The design handoff package has four parts:

1. **Brief overview** — one paragraph summary for the designer
2. **Copy deck** — all approved copy, formatted as designer-ready annotations
3. **Asset specs** — format requirements for each deliverable
4. **Brand reference** — where to find the visual system for the relevant brand

Generate all four in a single formatted document the user can copy directly.

---

## Part 1: Brief Overview Template

```
DESIGN BRIEF — [Client Name] Case Study
Brand: [Lake B2B / SPAN / Ampliz / Champions Group]
Date: [Handoff date]
Designer: [Name if known, or "TBD"]

We are producing two case study assets for [Client Name], a [industry] company based in [location].
The purpose is [primary use: landing page credibility / sales email attachment / event leave-behind].
The primary audience is [buyer bucket from Phase 3 audience mapping].

The tone should be [authoritative / energetic / precise — from the brand voice table].
The visual hierarchy should lead with [headline metric / client quote / challenge statement].

Deliverables needed by [date]:
- PDF case study (one-pager or two-pager — specify)
- Landing page on-page component (web-ready)
- Social proof card (LinkedIn / email signature size)

Reference all visual decisions against the [Brand] brand guidelines.
```

---

## Part 2: Copy Deck Format

Provide all copy as annotated text blocks. Each block should include:
- The content itself
- Its purpose/placement
- Any flexibility the designer has (e.g., "headline can wrap to two lines if needed")
- Any constraints ("stat callouts must be visible at thumbnail size")

Example format:

```
--- COPY BLOCK: PDF Cover ---
Headline (H1): "How VertexGrid Reached 378 Bangalore CXOs in Under 6 Weeks"
Constraint: Must read at 80px font or equivalent. Can reduce to 60px if needed.
Flexibility: Can abbreviate "Under 6 Weeks" to "In 6 Weeks" if layout requires.

Subheadline (H2): "A Lake B2B Case Study in B2B Data + Event Support"
Constraint: Below headline. 14-18px equivalent.

Client name label: VertexGrid | Technology Infrastructure | Bangalore
Constraint: Small caps or label style. Upper right or lower left. Not prominent.

--- COPY BLOCK: Stat Callouts (3) ---
Callout 1: 378 / CXO Contacts Delivered / Verified, Bangalore-based, tech sector
Callout 2: 2 Weeks / Sample to Client Approval / "Solid — we can move ahead"
Callout 3: May 14 / Event Confirmed / Conrad, Bangalore

Constraint: Numbers at 48-64px. Labels at 12-14px. Must be readable at half-size.
Flexibility: Callouts can be horizontal (3-across) or vertical (stacked). Designer's choice.

--- COPY BLOCK: Body Copy ---
[Paste the full approved on-page narrative here]
Constraint: 10-12px body text. Max 65 characters per line for readability.
```

---

## Part 3: Asset Specs

### PDF Case Study

| Spec | Requirement |
|------|-------------|
| Dimensions | A4 (210 x 297mm) or US Letter (8.5 x 11 in). One-pager preferred; two-pager if content requires. |
| Resolution | 300 DPI for print-ready. 150 DPI for screen-optimized (web download). |
| File formats | Deliver both: print-ready PDF + compressed web PDF (under 3MB). |
| Bleed | 3mm bleed if printing. None needed for web-only. |
| Fonts | Use the brand font stack. Fallback: system serif for body if brand font unavailable. |
| Color mode | CMYK for print. RGB for web. |
| Stat callout treatment | High contrast. Stats in brand primary color or large neutral with dark label. |
| Logo placement | Client logo (if approved) top-left or bottom-left. Brand logo (Lake B2B etc.) opposite corner. |
| Image/illustration | See Photo & Illustration section below. |

### Landing Page Component (Web)

| Spec | Requirement |
|------|-------------|
| Dimensions | Fluid width, max 1200px container. Mobile breakpoint at 768px. |
| File format | HTML/CSS component or Figma frame with handoff-ready specs. |
| Stat callouts | Large text (36-48px desktop, 24px mobile). Responsive grid: 3-col desktop, 1-col mobile. |
| Images | WebP preferred. Max 200KB per image. 72 DPI. |
| CTA button | Brand primary color. 44px minimum height (tap target). Copy: "Download the full case study." |
| Accessibility | All text must meet WCAG AA contrast (4.5:1 minimum). Alt text on all images. |

### Social Proof Card

| Spec | Requirement |
|------|-------------|
| LinkedIn post card | 1200 x 628px (landscape). One headline metric + client name. Brand logo bottom-right. |
| LinkedIn article header | 1920 x 1080px or 744 x 400px (platform header). |
| Email signature card | 600px wide, max 150px tall. One stat + "Read the case study" link. |
| File format | PNG (transparent background where relevant). |

---

## Part 4: Brand Reference

Direct the designer to the relevant brand skill file. If the brand skill is not accessible,
provide these key parameters:

| Brand | Primary color | Secondary color | Font: Headlines | Font: Body | Logo location |
|-------|--------------|----------------|-----------------|------------|---------------|
| Lake B2B | [From lakeb2b-brand-guidelines skill] | | | | |
| SPAN Global Services | [From relevant brand skill] | | | | |
| Ampliz | [From ampliz-brand-guidelines skill] | | | | |
| Champions Group | [From champions-group-brand skill] | | | | |

Instruct the designer: "Load the [Brand] brand guidelines before beginning. All color,
typography, and spacing decisions follow those guidelines. This brief specifies copy and
content placement only."

---

## Photo and Illustration Guidance

**Preferred approach:** Abstract, data-forward visuals over stock photography. A well-designed
data visualization or geometric graphic outperforms a generic business stock photo.

**If client permission is available:**
- A photo from the event (if event-related case study) carries enormous credibility
- A headshot of the named executive quoted in the case study adds personality
- Logo usage: confirm written approval before placing any client logo in the design

**Stock photography guidelines:**
- Avoid generic handshake/meeting room imagery
- Prefer: aerial city views, architecture, data visualization aesthetics, event venue photography
- Source from: Unsplash, Pexels (free) or Getty/Shutterstock (licensed)
- Always confirm the image license permits commercial use in marketing materials

**If no photos are available:**
- Use a solid brand color section with the stat callouts as the hero visual
- A well-typeset pull quote on a colored background outperforms a weak stock photo

---

## Common Failure Modes to Flag Proactively

Tell the designer explicitly:

1. **Contrast on colored backgrounds.** If stat callouts or headline text sits on the brand
   primary color, the text must be explicitly white or light. Check all text at WCAG AA minimum.

2. **PDF download size.** Compress the web-download PDF. Under 3MB is the target. Under 1MB
   is excellent. Large PDFs do not travel well in email chains.

3. **Mobile readability of stat callouts.** Test the web component at 375px width. If the
   stat numbers wrap or shrink below 24px, redesign the mobile layout.

4. **Logo usage approval.** Do not place the client's logo in any design until you have
   confirmed written approval from the user. Flag this explicitly.

5. **Font licensing.** Confirm the brand font is licensed for web embedding (WOFF2) not just
   desktop use. If unlicensed for web, use the system fallback specified in the brand guidelines.
