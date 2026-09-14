# Champions Ranch: Visual Style (for documents)

The document-facing subset of the full Champions Ranch visual identity. Use this
for proposals, one-pagers, package sheets, itineraries, and any printed or PDF
collateral. Lead with green, support with gold and brown, ground on warm cream.

## Design intent

Champions Ranch is a working experience center on the edge of Bangalore, not a
luxury resort and not a theme park. Documents should feel warm, grounded, and
premium without gloss. Think of the Champions Group charcoal suit taking off the
jacket and sitting by a fire. Editorial, unhurried, confident. Green leads every
composition.

For corporate documents use the **Ranch editorial** treatment described here
(green-dominant, gold accents, serif headlines). The Kawaii Pastel mode from the
master brand guide is for school and family social content only. Never use pastel
or cartoon styling on a corporate proposal.

## Color palette

Core identity (use across every document):

| Token | Hex | Role |
|-------|-----|------|
| Ranch Green | `#2F7D3F` | PRIMARY. Card headers, section headings, dominant fills |
| Dark Green | `#1A5C2A` | Headings on light, deeper card headers, borders |
| Deep Green | `#143F1E` | Cover meta panel, grand-total row, quote panels, hero text |
| Warm Gold | `#D4AF37` | SECONDARY. Rules, highlights, per-person figure, accents, CTAs |
| Gold Deep | `#B4912A` | Gold text/checks that need contrast on cream |
| Earthy Brown | `#8B6F47` | TERTIARY. Eyebrows, labels, footer, grounding detail |
| Barn Red | `#C1440B` | Sparing pop only (a "what you skip" cross, a single accent) |
| Warm Cream | `#F5EFE0` | Section/card backgrounds |
| Paper | `#FFFDF8` | Page background (a warm white, never pure #FFF) |
| Ink | `#28301F` | Body text (warm near-black, not pure black) |
| Muted | `#6E6A5C` | Secondary/caption text |

Parent lockup colors (footer lockup ONLY, never as primary):

| Token | Hex | Use |
|-------|-----|-----|
| Champions Charcoal | `#2D2D2D` | "A Champions Group Experience" lockup text |
| Champions Gold | `#C9A84C` | "Champions Group" accent inside the lockup |

Contrast rule: any text on a green or deep-green panel must be explicitly white
or cream (`#F4F1E6`). Never rely on inherited color on dark fills.

## Typography

| Role | Font | Notes |
|------|------|-------|
| Headlines, section titles, big figures | **Lora** (serif) | Warm, premium. Fallback: Georgia, "DejaVu Serif", serif |
| Body, labels, numbers, tables | **Poppins** (sans) | Clean, geometric. Fallback: "DejaVu Sans", sans-serif |
| Currency figures | Poppins, tabular-nums | Poppins renders the rupee sign cleanly |

Type scale that works on A4: hero 36 to 40pt, section H2 21pt, card title 13 to
14pt, body 10pt, labels 7.5 to 8pt uppercase with 0.2em+ letter-spacing.

Headlines may be sentence case or title case. Eyebrows and labels are uppercase
with wide tracking. Body is left-aligned, line-height ~1.5.

## Layout system

- Page: A4. Margins ~16mm top, 15mm sides, 18mm bottom.
- Running footer (every page except cover): `Champions Ranch · Sarjapur Road,
  Bangalore · Time Worth Spending` in brown, plus `page / total` at right.
- Cover: full-bleed, no footer. Eyebrow + wordmark + gold rule, big serif hero,
  subtitle, italic tagline, a landscape scene SVG, then a deep-green meta panel.
- Page rhythm: start each major section on a fresh page (`break-before: page` on
  `.sheet`). Keep cards and tables whole (`break-inside: avoid`).
- Whitespace is active, not empty. Generous top space above each section header.

## Signature components

The template and `components.md` provide these reusable blocks:

- Cover (eyebrow, wordmark, gold rule, hero, tagline, scene SVG, meta panel).
- Section header (gold motif icon + uppercase kicker + serif H2 + gold rule).
- Experience card (`xcard`): colored header with a title and a right-aligned
  price, white body with prose and a checklist.
- Rooms / line-item table with an emphasized subtotal row.
- Checklist grid (gold ticks, two or three columns).
- Commercial summary table with a deep-green grand-total row.
- Per-person highlight band (gold panel, large figure).
- "What is included" cream list.
- Numbered terms list.
- Deep-green closing quote panel.
- Sign-off and the Champions Group footer lockup.
- Stat chips (single row of metrics).

## Do and Don't

Do:
- Lead with green. Gold and brown support, they do not lead.
- Keep pure white off the page. Use Paper `#FFFDF8` and Cream `#F5EFE0`.
- Use the rupee sign with grouped Indian digits: `₹7,73,171`, `₹5,154`.
- Itemise money. Show sub-total, GST line, then a bold grand total.
- Let the cover scene carry warmth (hills, sun, fence, a lone tree, an animal).
- Use the "A Champions Group Experience" lockup on formal corporate documents.

Don't:
- Don't use em-dashes anywhere. Use periods, commas, colons, or restructure.
- Don't use pastel, kawaii, or cartoon styling on corporate documents.
- Don't put dark text on a green panel. Force white or cream.
- Don't oversaturate with decoration. One motif per section header is enough.
- Don't lead with the parent charcoal. Ranch is green-first.
