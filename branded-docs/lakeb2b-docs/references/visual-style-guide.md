# [[Lake B2B|LakeB2B]]: Visual Style (for documents)

The document-facing subset of the [[Lake B2B|LakeB2B]] identity. Use it for proposals,
capability overviews, one-pagers, case studies, data sheets, pitch documents,
and reports. Purple leads, gold and red accent, gradients and the data-network
motif carry the energy. Category: the B2B growth stack. Promise: ENABLING GROWTH.

## Design intent

[[Lake B2B|LakeB2B]] is enterprise data and growth technology. Documents should feel
confident, modern, and precise, built for CXOs and revenue leaders. The visual
system is purple-anchored and gradient-forward, with a dark gradient cover and
clean white body pages. Lean on the lake metaphor (depth) and the network motif
(data points connecting). Avoid hype and clutter. Precision over noise.

## Color system

Primary palette, used at roughly 60 / 20 / 20:

| Token | Hex | Share | Role |
|-------|-----|-------|------|
| Purple | `#6D08BE` | 60% | Anchor. Hero, primary surfaces, headings, kicker, accents |
| Gold | `#FFB703` | 20% | Highlight. The promise pill, accent words on dark, callouts |
| Red | `#E8033A` | 20% | Emphasis, energy, primary CTA accent |

Derived purples used in the template for depth:

| Token | Hex | Use |
|-------|-----|-----|
| Purple Deep | `#46067E` | Gradient mid-stop, deep fills |
| Purple Ink | `#2C0A4A` | Headings on white, table header fill |
| Navy | `#011A6B` | Gradient end-stop, strong enterprise panels |

Secondary palette (20% of designs, accents only):

| Token | Hex | Note |
|-------|-----|------|
| Magenta | `#DD1286` | Accent words on white, gradient partner to purple |
| Teal | `#0095A0` | Vertical color-coding, calm accent |
| Bright Orange | `#FF6903` | Energy accent, GrowthTech |
| Lavender | `#7A76DA` | Soft accent, network dots |
| Deep Red | `#C1003C` | Deep emphasis |

Neutrals: Ink `#1C1430` (body text), Muted `#6B6480` (captions), Line `#E7E2F0`
(borders), Wash `#F4ECFD` (light purple card fill), Paper `#FFFFFF` (page).

Contrast rules:
- White text on Purple `#6D08BE` and Navy `#011A6B` is the flagship treatment.
- Purple on white is the primary heading treatment.
- Gold `#FFB703` never carries body text on white (fails WCAG AA). Gold is for
  fills, the promise pill, and accents only.
- Do not put Red on Purple, it vibrates.

## Gradients (the signature)

- Hero / CTA / grand-total: `linear-gradient(135deg,#6D08BE,#46067E 55%,#011A6B)`
- Accent rule and badges: `linear-gradient(90deg,#6D08BE,#DD1286 60%,#FFB703)`
- Vertical color-coding (card headers):
  SalesTech purple, MarTech magenta, RecruitTech teal, GrowthTech orange to red.
- Promise pill: solid Gold `#FFB703` with near-black text.

## Typography

| Role | Font | Notes |
|------|------|-------|
| Headlines, H2, big figures | **Montserrat** ExtraBold/Bold | Fallback: Poppins, "DejaVu Sans", sans-serif |
| Body, tables | **Montserrat** Regular | Fallback: Poppins |
| Labels, eyebrows, stats, footer | **JetBrains Mono** | Fallback: "DejaVu Sans Mono", monospace. Uppercase, wide tracking |
| Display / pull quotes | **Alata** | Optional, fallback to Poppins |

Mono labels are a core part of the look. Eyebrows, snapshot keys, stat captions,
step numbers, and the footer are all mono and uppercase with wide letter-spacing.

## Layout system

- Page: A4. Margins ~15mm sides, 16mm bottom.
- Cover: full-bleed dark gradient (purple to navy), no footer. Network motif SVG,
  white wordmark, gold eyebrow, gold ENABLING GROWTH pill, glass snapshot panel.
- Body: white pages, purple kicker dot, Montserrat H2 in Purple Ink, gradient
  rule, generous whitespace. Mono running footer with page numbers.
- Start each major section on a fresh page (`break-before: page` on `.sheet`).
  Keep cards and tables whole (`break-inside: avoid`).

## Signature components

The template and `components.md` provide: the gradient cover with network motif,
section header (gradient dot + mono kicker + H2 + gradient rule), the positioning
ladder, color-coded vertical cards, the process flow, stat chips, the engagement
or pricing table with a gradient grand-total row, the "what you get" list, the
numbered next-steps list, the gradient CTA band, and the footer lockup.

## Do and Don't

Do:
- Lead with purple. Gold and red accent. Secondary colors only as accents.
- Use gradients on hero, CTA, rules, and grand-total rows.
- Keep mono labels uppercase with wide tracking.
- Write the category lowercase: "the B2B growth stack".
- Render the promise uppercase: ENABLING GROWTH.
- Use white or cream text on purple and navy panels. Test contrast.
- Name verticals small-caps no space: SalesTech, MarTech, RecruitTech, GrowthTech.

Don't:
- Don't use em-dashes anywhere. Use periods, commas, colons, or restructure.
- Don't set body or fine text in gold on white.
- Don't put red on purple.
- Don't write "[[Lake B2B|LakeB2B]]" with a space, except in prose or all-caps lockups.
- Don't clutter. Precision and whitespace signal enterprise credibility.
- Don't skew, rotate, recolor, or add effects to the logo mark.
