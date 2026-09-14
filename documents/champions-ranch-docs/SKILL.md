---
name: champions-ranch-docs
description: Create polished, on-brand Champions Ranch documents as print-ready PDFs in the Ranch green-and-gold editorial style, with the Champions Ranch visual identity and voice baked in. Use this skill whenever the user wants a Champions Ranch proposal, corporate stay or offsite proposal, retreat or package quote, one-pager, itinerary, rate card, or any Ranch-branded document or PDF. Also trigger on "Champions Ranch proposal", "Ranch corporate stay", "make this look like the Ranch proposal", "Ranch branded document", "offsite proposal", "retreat quote", or any request to build, rebrand, or format collateral for Champions Ranch (an InfraTech property, Champions Group). Use it even when the user only says "make a Ranch document" or pastes raw pricing to turn into a proposal. Pairs with the Champions Ranch visual style guide and voice guide included here.
---

# Champions Ranch Documents

Build warm, premium, print-ready Champions Ranch documents: corporate stay and
offsite proposals, retreat and package quotes, one-pagers, itineraries, and rate
cards. The output is a multi-page A4 PDF in the Ranch editorial style: green
leads, gold accents, serif headlines, warm cream grounds, and the "A Champions
Group Experience" footer lockup. The voice is warm, grounded, and unhurried.

Champions Ranch is a working experience center 30 minutes from Sarjapur Road,
Bangalore. It is not a luxury resort and not a theme park. Every document should
carry that grounded confidence.

## What this skill produces

A self-contained HTML document rendered to a polished PDF via WeasyPrint. The
default `assets/proposal_template.html` is a complete, send-ready corporate stay
proposal with no fill-in-the-blanks. You adapt it (or compose a new document
from the components) for the task at hand.

## Workflow

1. **Understand the ask.** Identify the document type, the audience, the group
   size, the dates if any, the inclusions, and the pricing. If raw numbers are
   given, verify the math first (line items sum to sub-total, GST is 18% of the
   sub-total, grand total is sub-total plus GST, per-person is grand total over
   headcount).

2. **Start from the template.** Copy `assets/proposal_template.html`. It already
   carries the full stylesheet, the cover with its landscape scene, the running
   footer, and a worked corporate-stay body. Keep, edit, drop, or duplicate body
   sections as needed. For a different document type, assemble from the blocks in
   `references/components.md`.

3. **Apply the brand.** Pull tone, approved headlines, and copy patterns from
   `references/brand-voice.md`. Pull palette, type, layout, and the do/don't list
   from `references/visual-style-guide.md`. Read those two files before writing
   copy or restyling, since they are the source of truth.

4. **Fill only what you know.** The cover snapshot defaults to Group Size, Stay
   Format, and Prepared By. Add Prepared For, Primary Contact, and Stay Dates
   only when the user provides them. Never leave a visible `[bracket]` or an
   empty `{{TOKEN}}` in the output. If you used `{{TOKENS}}`, fill them with
   `--vars` or by direct edit before rendering.

5. **Render.**
   `python scripts/build_pdf.py yourdoc.html "Your Document Name.pdf"`
   Optional token fill:
   `python scripts/build_pdf.py yourdoc.html out.pdf --vars vars.json`

6. **Verify before delivering.** Render the PDF pages to images and check
   branding, contrast (white text on green panels), page breaks (no stranded or
   near-empty pages), and that no placeholder text survived. Then deliver the PDF.

## Brand quick reference

Always-in-context essentials. The reference files carry the full detail.

Colors: Ranch Green `#2F7D3F` (primary), Dark Green `#1A5C2A`, Deep Green
`#143F1E`, Warm Gold `#D4AF37` (accent), Earthy Brown `#8B6F47` (labels), Warm
Cream `#F5EFE0` and Paper `#FFFDF8` (grounds), Ink `#28301F` (text). Parent
lockup only: Charcoal `#2D2D2D`, Champions Gold `#C9A84C`. Green leads, gold and
brown support, never pure white.

Type: Lora (serif) for headlines and big figures, Poppins (sans) for body and
numbers, with Georgia / DejaVu fallbacks.

Voice: warm, grounded, unhurried, authentic, locally rooted. Roughly 70% formal
and 30% warm for corporate documents. Tagline "Time worth spending." Corporate
line "The offsite they'll actually talk about."

Hard rules:
- No em-dashes anywhere. Use periods, commas, colons, or restructure.
- Rupee sign with Indian digit grouping: `₹7,73,171`, `₹1,500 per person`.
- White or cream text on every green panel. Test contrast.
- No pastel or cartoon styling on corporate documents. Ranch editorial only.
- Avoid "luxury" and "resort". Champions Ranch is a working experience center.

## Files

- `assets/proposal_template.html` : complete corporate-stay proposal, the default
  starting point. Contains the full CSS, cover, scene SVG, and footer.
- `scripts/build_pdf.py` : renders any document HTML to PDF (WeasyPrint), with an
  optional `--vars` JSON token fill.
- `references/visual-style-guide.md` : palette, type, layout, components, do/don't.
- `references/brand-voice.md` : voice attributes, tone, headlines, words, copy.
- `references/components.md` : copy-paste HTML for every block, plus the tokenized
  cover and motif SVGs.
- `examples/` : a finished example document for reference.

## Dependency

`pip install weasyprint --break-system-packages`. The template CSS includes font
fallbacks, so it renders even when Lora and Poppins are absent.
