---
name: "metricfox-brand-guidelines"
description: "MetricFox brand guidelines and branded Word builder. Use for any MetricFox-branded proposal, document, deck, email, social post or web page, or anything sent from MetricFox."
---

# MetricFox Brand Guidelines

Source of truth: the live site www.metricfox.com (logo artwork and `assets/css/style.css`), extracted 24 September 2026. If the site changes, re-extract and update this file.

## Where the assets live

The logo files (`assets/`) and the Word builder (`scripts/mf_docx.py`) are kept in the Celsus vault at `/Users/deep/Celsus/Other/Skills/metricfox-brand-guidelines/`. When this skill runs without those files next to it, stage them from that vault folder first. If the vault is not reachable, download the logo from https://www.metricfox.com/assets/images/metricfox-home-logo.jpg (blue wordmark on black) and apply the palette below by hand.

## When MetricFox is the sender

- MetricFox documents carry **only MetricFox**. Do not mention Champions Group, LakeB2B, Span, Ampliz or any sister brand unless the user asks.
- Proof points come from MetricFox's own retainer work (see "Proof points" below).
- Default contact: Shine Solomon, shine.s@metricfox.com, unless the user names someone else.

## Brand at a glance

| Item | Value |
|---|---|
| Name | MetricFox (one word, capital M and capital F; never "Metric Fox" or "Metricfox") |
| What it is | Bangalore-based B2B marketing agency and consultancy |
| Site tagline | "Elevate your Marketing Efficiencies with simple Leaps of Logic" |
| Positioning line | A team of insight-driven consultants delivering bespoke, right-sized marketing, not one-size-fits-all |
| Services (from site) | Consulting; Creative Solutions; Inbound and Outbound Marketing; Demand Generation and ABM; Data-Driven Marketing and Marketing Automation; Application Development and Data Management; Marketing Outsourcing |
| Website | www.metricfox.com |

## Colour palette

The logo is a blue wordmark under three rising blocks (yellow, amber, orange). The site UI is blue plus neutrals.

### Primary

| Name | Hex | RGB | Use |
|---|---|---|---|
| MetricFox Blue | `#00529C` | 0, 82, 156 | THE brand colour. Headings, table headers, buttons, links, wordmark |
| Fox Orange | `#F36523` | 243, 101, 35 | Main accent. Underlines under H1, key numbers, CTAs on light backgrounds |
| Amber | `#F68C1F` | 246, 140, 31 | Secondary accent, callout edges |
| Sun Yellow | `#FDB813` | 253, 184, 19 | Small highlights only. Never as text on white (fails contrast) |

### Neutrals (from site CSS)

| Name | Hex | Use |
|---|---|---|
| Ink | `#111111` | Body text |
| Grey | `#666666` | Secondary text, captions, footers |
| Light | `#F7F7F7` | Page and section backgrounds |
| Line | `#EEEEEE` / `#D9E2EC` | Dividers, table borders |
| Blue Tint | `#EAF1F8` | Zebra rows, callout boxes (derived tint of Blue) |
| White | `#FFFFFF` | Surfaces |

### Rules

- Blue carries the brand. Orange is the accent, used sparingly (about 10% of a page).
- The **three-step accent** (yellow, amber, orange in rising widths, left to right) is the signature device. Use it once per cover or section divider, never as decoration everywhere.
- Gradient, when needed: `#FDB813 → #F68C1F → #F36523` (left to right). No blue gradients.
- On dark backgrounds use the reversed logo (white wordmark, colour blocks kept).

## Typography

| Context | Headings | Body | Accent |
|---|---|---|---|
| Web (site fonts) | Dosis (600 or 700) | Open Sans 400/700 | Libre Baskerville italic, sparingly for pull quotes |
| Word, PowerPoint, PDF sent to clients | Arial Bold | Arial | Arial Italic |

Office files use Arial because Dosis and Open Sans are not installed on most client machines and Word silently substitutes them. Sizes for documents: title 22 pt, H1 15 pt blue, H2 11.5 pt ink, body 10 pt, tables 9 pt, footer 8 pt.

## Logo

Files in `assets/`:

- `metricfox-logo.png`: full colour on transparent, 1095 x 480. Default.
- `metricfox-logo-reversed.png`: white wordmark for dark or blue backgrounds.
- `metricfox-logo-small.png`: 114 x 48 site header logo, web use only.

Rules: clear space around the logo equals the height of the yellow block. Minimum width 2 cm in print, 100 px on screen. Do not recolour, stretch, add shadows, separate the blocks from the wordmark, or put the full-colour logo on orange.

## Voice

The site voice is professional, consultative and a little playful ("Leaps of Logic", "Co-Travelers in Success", "Proof of the Pudding"). For client documents:

- Lead with the outcome and the number. Short sentences. Plain words.
- Consultative, not salesy: "we recommend", "we will", with reasons.
- One light turn of phrase per document is on brand. More reads as gimmicky.
- House rules that always apply: no em or en dashes anywhere (use commas, colons, periods, "to" for ranges); no-ai-slop rules (no "It's not X, it's Y", no puffery, no leverage/delve/streamline); run the `no-ai-slop` skill as the final gate on client-facing copy.
- Never invent metrics, client results or awards. If a number is not in the vault, leave it out or mark it for the user to fill.

## Proof points (internal reference, confirm naming before use)

From the Celsus vault client notes (`Atlas/Clients/`):

- **Tavant** (fintech and technology): monthly creative retainer (social carousels, event, award, webinar and PR creative, case studies, whitepapers, explainer video) plus a standing SEO program.
- **WinWire** (technology services): website retainer (page design and builds, homepage video, landing pages, WordPress), design support, LinkedIn video ad campaigns.
- **Amazon, Roquette**: retainer clients; scope not documented in the vault.

Naming clients to third parties (for example a prime contractor in a sub-vendor bid) needs the user's OK. Offer an anonymised form ("a US fintech lender") as the alternative.

## Document layout (Word)

Use `scripts/mf_docx.py`, which applies everything above:

```python
import sys; sys.path.insert(0, "<path-to-this-skill>/scripts")
from mf_docx import MFDoc
doc = MFDoc(title="Proposal: Social Media and Website Redesign",
            eyebrow="Proposal", subtitle="Submitted to: AB7 Solution  |  24 September 2026")
doc.callout("One paragraph that carries the whole message.", label="Summary")
doc.h1("1. Relevant experience"); doc.p("...")
doc.bullets([("Bold lead: ", "detail"), "plain bullet"])
doc.table([["Header", "Header"], ["cell", "cell"]], widths_cm=[6, 11])
doc.save("/mnt/user-data/outputs/file.docx")
```

What it produces:

- Cover block: full-colour logo, grey eyebrow, 22 pt blue title, three-step accent bar, grey subtitle line.
- H1 in blue with a thin orange rule underneath; H2 in ink.
- Tables: blue header row with white text, Blue Tint zebra rows, light borders, fixed column widths, rows that never split across pages, header row repeated.
- Callout: Blue Tint box with an amber left edge. Use for the summary at the top.
- Header on pages 2+: small logo at right. Footer: "MetricFox | www.metricfox.com | Page n".

Structure every proposal so the first two lines carry the whole message (scope, price, timeline), then the detail.

## Other formats

- **Slides:** white background, blue titles, one orange accent per slide, three-step accent on the title and section slides, logo bottom right. Arial if exported to .pptx.
- **Social posts:** blue or white backgrounds, orange for the one number or word that matters, logo bottom corner. Dosis for headlines in design tools.
- **Web and HTML:** Dosis headings, Open Sans body, `--mf-blue:#00529C; --mf-orange:#F36523; --mf-amber:#F68C1F; --mf-yellow:#FDB813; --mf-ink:#111; --mf-bg:#F7F7F7`.
- **Email signature:** name, title, MetricFox, www.metricfox.com. No banners.

## Final checks before delivery

1. Only MetricFox named as the sender; no sister brands.
2. Zero em or en dashes (scan the text of the output file programmatically).
3. Logo not stretched; blue used for headings; orange used sparingly.
4. Render the file to an image (for example LibreOffice to PDF, then PDF to PNG) and look at the pages before sending.