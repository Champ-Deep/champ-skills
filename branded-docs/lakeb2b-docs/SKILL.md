---
name: lakeb2b-docs
description: Create polished, on-brand LakeB2B documents as print-ready PDFs in the LakeB2B purple-and-gradient enterprise style, with the LakeB2B visual identity and "B2B growth stack" voice baked in. Use this skill whenever the user wants a LakeB2B proposal, capability overview, one-pager, pitch document, case study, data or sample sheet, rate card, sales or marketing collateral, or any LakeB2B branded document or PDF. Also trigger on "LakeB2B proposal", "Lake B2B doc", "make this look like LakeB2B", "growth stack document", "LakeB2B capabilities deck", "LakeB2B one-pager", "brand this for LakeB2B", or any request to build, rebrand, or make LakeB2B documents more visual. Use it even when the user only says "a LakeB2B document" or pastes raw content to turn into branded collateral. Pairs with the LakeB2B visual style guide and voice guide included here.
---

# [[Lake B2B|LakeB2B]] Documents

Build confident, modern, print-ready [[Lake B2B|LakeB2B]] documents: proposals, capability
overviews, one-pagers, pitch documents, case studies, data sheets, and rate
cards. The output is a multi-page A4 PDF in the [[Lake B2B|LakeB2B]] style: a dark
purple-to-navy gradient cover with a data-network motif, clean white body pages
with gradient accents, color-coded vertical cards, and the ENABLING GROWTH
promise. The voice is enterprise credible and partnership led.

[[Lake B2B|LakeB2B]] is the B2B growth stack: one integrated platform across data
intelligence, marketing technology, sales enablement, and talent, built on four
verticals (SalesTech, MarTech, RecruitTech, GrowthTech) on deep data reservoirs.

## What this skill produces

A self-contained HTML document rendered to a polished PDF via WeasyPrint. The
default `assets/document_template.html` is a complete capabilities and engagement
overview with no fill-in-the-blanks. Adapt it, or compose a new document from the
components, for the task at hand.

## Workflow

1. **Understand the ask.** Identify the document type, the audience (usually CXOs
   and revenue leaders), the message, and any figures. If raw pricing is given,
   verify the math before building.

2. **Anchor to the positioning.** Lead with the category, "the B2B growth stack",
   above the promise, ENABLING GROWTH. Pull blurbs, lexicon, and tone from
   `references/brand-voice.md`. Read it before writing copy.

3. **Start from the template.** Copy `assets/document_template.html`. It carries
   the full stylesheet, the gradient cover with its network motif, and the mono
   footer. Keep, edit, drop, or duplicate body sections. For a different document
   type, assemble from the blocks in `references/components.md`. Pull palette,
   gradients, type, and the do/don't list from `references/visual-style-guide.md`.

4. **Fill only what you know.** The cover snapshot defaults to Document,
   Verticals, and Prepared by. Add client, contact, and date only when provided.
   Never leave a visible `[bracket]` or empty `{{TOKEN}}`.

5. **Render.**
   `python scripts/build_pdf.py yourdoc.html "Your Document Name.pdf"`
   Optional token fill: add `--vars vars.json`.

6. **Verify before delivering.** Render pages to images and check branding,
   contrast (white text on purple and navy panels, never gold body text on
   white), page breaks, and that no placeholder survived. Then deliver the PDF.

## Brand quick reference

Colors: Purple `#6D08BE` (anchor, 60%), Gold `#FFB703` (highlight, 20%), Red
`#E8033A` (emphasis, 20%); secondary Magenta `#DD1286`, Teal `#0095A0`, Orange
`#FF6903`, Navy `#011A6B`. Derived Purple Deep `#46067E`, Purple Ink `#2C0A4A`.
Wash `#F4ECFD`, Line `#E7E2F0`, Ink `#1C1430`. Purple leads, gold and red accent.

Gradients: hero and CTA `135deg purple to purple-deep to navy`; rule `90deg
purple to magenta to gold`. Vertical color-coding: SalesTech purple, MarTech
magenta, RecruitTech teal, GrowthTech orange to red.

Type: Montserrat (headings and body), JetBrains Mono (labels, eyebrows, stats,
footer), with Poppins and DejaVu Mono fallbacks. Mono labels are uppercase with
wide tracking.

Voice: confident, enterprise credible, partnership led, no hype. Intelligent
without jargon, direct without blunt, ambitious without arrogant, warm without
casual.

Hard rules:
- No em-dashes anywhere. Use periods, commas, colons, or restructure.
- Category lowercase: "the B2B growth stack". Promise uppercase: ENABLING GROWTH.
- White text on every purple or navy panel. Gold never carries body text on white.
- Verticals are small-caps no space: SalesTech, MarTech, RecruitTech, GrowthTech.
- Write "[[Lake B2B|LakeB2B]]" with no space, except in prose ("[[Lake B2B]]") or all-caps lockups.
- Avoid disrupt, revolutionary, game changer, synergy, point solution, vendor.

## Files

- `assets/document_template.html` : complete capabilities overview, the default
  starting point. Contains the full CSS, gradient cover, network motif, footer.
- `scripts/build_pdf.py` : renders any document HTML to PDF, with optional
  `--vars` JSON token fill.
- `references/visual-style-guide.md` : palette, gradients, type, layout, do/don't.
- `references/brand-voice.md` : positioning ladder, lexicon, blurbs, verticals.
- `references/components.md` : copy-paste HTML for every block, plus motif SVGs.
- `examples/` : a finished example document for reference.

## Dependency

`pip install weasyprint --break-system-packages`. The CSS includes font
fallbacks, so it renders even without Montserrat and JetBrains Mono installed.
