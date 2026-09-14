# Quality checklist + troubleshooting

Use this after every conversion. The goal is a file that (a) looks like the
PDF, (b) is genuinely self-contained, and (c) preserves the text correctly.

## Fast automated checks

Run against the produced HTML (replace `OUT.html` and the phrase):

```bash
# 1. Page count matches the source PDF
echo "html pages: $(grep -c 'class=\"page' OUT.html)"
pdfinfo INPUT.pdf | grep Pages         # poppler; compare the number

# 2. A known headline survived, spelled correctly
grep -o "Prepared for: Acme Corp" OUT.html | head -1

# 3. Self-contained: this MUST print 0
grep -Eo 'src="http|href="http|url\(http' OUT.html | wc -l

# 4. reflow only: expected images embedded as data URIs (>0 if the PDF had images)
grep -c "data:image" OUT.html
```

## Visual check (recommended)

There is no browser in the sandbox, so confirm fidelity by rendering. Decode
one page's embedded background image and open/Read it. exact uses PNG data
URIs; editable uses JPEG:

```python
import re, base64
h = open("OUT.html").read()
m = re.search(r'class="bg" src="data:image/(?:png|jpeg);base64,([^"]+)"', h)
if m:
    open("page1.png", "wb").write(base64.b64decode(m.group(1)))
    print("wrote page1.png")
```

```bash
# reference render straight from the PDF to eyeball alongside
pdftoppm -png -r 100 -f 1 -l 1 INPUT.pdf ref_page
```

Confirm headers, colors, images and layout match.

### Editable mode: inspect the masking

In **editable** mode the background image is the page with the original text
**painted over**, and real editable text sits on top. Check both:

```python
# how many text lines were recovered, and what they say (page 1)
import re
h = open("OUT.html").read()
p1 = h.split('<div class="page editable"')[1]
print(re.findall(r'class="ed"[^>]*>([^<]*)</p>', p1))
```

Open the decoded page image (above) and verify two things: (a) the original
baked-in text is gone (covered by background-colored patches), and (b) the
decorative artwork is intact and not chopped by stray mask boxes. A faint patch
tone on busy backgrounds is acceptable; a mask box sitting in the middle of a
graphic means OCR noise leaked through (see troubleshooting).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Background bars, colored boxes, lines or charts are missing in **reflow** | Those are vector graphics; reflow rebuilds text + raster images only | Re-run with `--mode exact` (view) or `--mode editable` (if no text layer and edits needed) |
| Whole page looks blank but PDF has content | Scanned/image-only PDF (no text layer) | `--mode exact` for view-only, or `--mode editable` to OCR the text and make it editable |
| **editable**: a mask box sits in the middle of a graphic | OCR detected false "text" in the artwork | Acceptable if small; the engine filters by confidence (>=50), requires a real word per line, and splits lines on big horizontal gaps to keep only the dense cluster. If it persists, the artwork has text-like detail; consider `--mode exact` instead |
| **editable**: mask patches are visibly rectangular | Background behind text is a photo/gradient, so the sampled flat fill does not blend perfectly | Acceptable on most slides; for a pristine look use `--mode exact` (no masking, but not editable) |
| **editable**: text recovered with small junk fragments (e.g. trailing symbols) | OCR noise adjacent to real text | Edit them out in the output (the text is editable), or accept |
| Text is garbled / wrong glyphs | PDF uses a broken or non-standard encoding | Use `--mode exact` (renders true glyphs), or `--mode editable` to OCR |
| Colors look slightly off | CMYK -> RGB conversion approximation | Acceptable for most; for exact brand color use `--mode exact` |
| Page is rotated | PDF page has a rotation flag | exact mode honors rotation via the renderer; in reflow, note it and prefer exact |
| File is very large | High-DPI exact mode on many pages, or large embedded images | Lower `--dpi` (e.g. 120), or use reflow if the doc is text-led |
| Fonts look generic | The exact embedded font is not on the viewer's machine | reflow maps to close web fallbacks (serif/sans/mono + weight + italic). For brand-exact type, edit the inline `font-family`, or use exact mode |

## Tuning notes

- `--dpi` only affects **exact** mode. 150 is a good screen default; 200+ for
  print-quality "Save as PDF"; 120 to shrink the file.
- **reflow** output is tiny and edits cleanly; reach for it first for anything
  text-led that the team will customize per prospect.
- For a folder of files, loop in a single run (see SKILL.md "Batch conversion")
  so you are not paying startup cost per file.
