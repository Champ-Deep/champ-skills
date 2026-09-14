---
name: pdf-to-html
description: Convert a PDF into a single, self-contained, faithful HTML file that the presales team can host, share as a web link, drop into a page, or edit. Use this skill whenever someone uploads or points to a PDF and wants it "as HTML", "as a web page", "as a 1-for-1 HTML", "turn this PDF into a page", "make this PDF a website", "rebrand this PDF", "edit this PDF", "make this PDF editable", "convert PDF to HTML", "PDF to web", "research to HTML", or wants to share a deck/proposal/one-pager/report/case study as a link or web section instead of an attachment. Also triggers for "host this PDF", "replace a page with this PDF", or "I need an HTML version of this PDF". Works on proposals, decks, reports, research, one-pagers, brochures, and brand collateral, including image-only/flattened PDFs (handled via OCR).
---

# PDF to HTML (faithful + editable)

Turn any PDF into ONE self-contained `.html` file that looks close to the
original, keeps the text real (selectable, editable, re-brandable), and has
zero external dependencies. Images, CSS and JS are all inlined, so the file
can be emailed, dropped on any static host, embedded in a page, or opened from
disk.

Built for presales: take a prospect-facing PDF, get a web page to share as a
link or a clean block to drop into a site, swap a name or a price, or rebrand.

## Two decisions drive every conversion

### 1. MODE - how the page is reconstructed

Pick based on what the PDF actually contains. Check it first:

```bash
python3 -c "import pdfplumber;d=pdfplumber.open('IN.pdf');\
print([(p.page_number,len(p.extract_text() or ''),len(p.images)) for p in d.pages])"
```
That prints `(page, text_chars, image_count)` per page. If `text_chars` is ~0
on every page, the PDF is **image-only / flattened** (a deck exported as
pictures) and has no real text layer: use **editable** mode. Otherwise choose
reflow or exact.

| Mode | What you get | Use it for |
|------|--------------|-----------|
| **reflow** (default) | Each page rebuilt from real positioned text + the original embedded images. Text is real. Flat **vector** graphics (bg bars, boxes, charts, lines) are NOT redrawn. | Text-led docs that have a real text layer: proposals, one-pagers, letters, reports. |
| **exact** | Each page rendered as a crisp image (every shape/chart/gradient + exact layout) with a transparent, selectable text layer on top. | Design-heavy PDFs where pixel fidelity beats editability and you don't need to edit. |
| **editable** | For **image-only / flattened** PDFs. OCRs each page, **paints over the original baked-in text** with a sampled background color, and lays real editable text on top of the page image. Genuinely editable while keeping the original look. | Flattened decks/brochures exported from Figma/Canva/PPT with no text layer, when the team must edit the copy. |

Honest tradeoffs to know and to tell the user:
- **reflow** is faithful for text + raster images + fonts + colors, but drops
  flat vector graphics. If the PDF leans on those, use exact (view) or
  editable (if there's no text layer).
- **exact** looks identical but is not for editing.
- **editable** depends on OCR. It is excellent on clean backgrounds; on busy
  artwork the mask patches behind text can be faintly visible and OCR may add
  small stray fragments. It recovers the copy and makes it editable, which is
  the point, but it is not pixel-perfect. Always eyeball a page (see Verify).

### 2. LAYOUT - what the file is for

Ask the user which they want (or produce both so they can compare):

| Layout | What it is | Use it for |
|--------|-----------|-----------|
| **display** (default) | Standalone viewer: page framing, a slim title bar (title only, no action buttons by default), pages auto-fit to the screen. | Sharing as a link, opening locally, sending a single file. |
| **clean** | No chrome at all, just the page sections with everything inlined. Real text, clean markup (no `contenteditable` attributes). | Dropping into / replacing an existing web page or CMS block. |

There is intentionally **no "Edit text" toggle**. In display layout the text is
directly editable inline (click and type); in clean layout the text is real
markup the team edits in their editor or CMS.

The **Print / Save-as-PDF** button is **optional and off by default**. Add it
only when asked, with `--pdf-button` (display layout only).

## Workflow

1. **Locate the PDF** (uploaded/selected path). If none, ask for the file.
2. **Probe** the PDF with the one-liner above to choose the mode.
3. **Confirm layout** with the user (display vs clean), and whether they want
   the PDF button. If they want to compare, generate both layouts.
4. **Run the converter** (`scripts/convert.py`, relies only on tooling already
   in the Cowork sandbox: pdfplumber, poppler, Pillow, tesseract):

   ```bash
   python3 scripts/convert.py "IN.pdf" -o "OUT.html" \
       --mode reflow|exact|editable \
       --layout display|clean \
       [--pdf-button] [--title "Title"] [--dpi 150]
   ```

5. **Verify** before claiming done (below).
6. **Save** to the user's folder and share with `present_files`. Do not paste
   HTML into chat. Note: editable/exact outputs of large decks can be a few MB.

## Verify before claiming done

Never report success without checking. The essentials:

- page count in the HTML matches the PDF;
- key headline text is present and spelled right (`grep` a phrase);
- **no** external references (`grep -Eo 'src="http|href="http' OUT.html | wc -l` is 0);
- reflow: expected images present as `data:image` URIs;
- exact/editable: render one page and eyeball it.

For **editable** especially, decode one page's background image and look at it
to confirm OCR masked the real text and left the artwork intact. The snippet,
the full checklist, and troubleshooting (stray masks, garbled OCR, missing
vector graphics, sizing) are in `references/quality-checklist.md`.

## Rebranding

The shell exposes CSS variables (`--bg`, `--page`, `--bar`, `--bar-ink`,
`--accent`). Edit them to rebrand the chrome. For brand-exact document styling,
prefer reflow output and adjust inline styles, or load the matching brand skill
(`champions-group-brand`, `lakeb2b-brand-guidelines`, `ampliz-brand-guidelines`).

## Batch conversion

```bash
for f in *.pdf; do python3 scripts/convert.py "$f" --mode reflow --layout display; done
```

## Reference files

- `references/quality-checklist.md` - verification snippet, the render-to-image
  check (incl. editable mask inspection), and troubleshooting.
