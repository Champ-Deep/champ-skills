#!/usr/bin/env python3
"""
convert.py - PDF -> ONE self-contained HTML file (faithful, editable).

Produces a single .html with everything (images, CSS, JS) inlined, so it can
be hosted, emailed, embedded, or opened from disk with zero dependencies.

MODES (how faithfully / how editable):
  reflow   (default) Rebuilds each page from real positioned text + the
                     original embedded raster images. Text is real and
                     editable. Flat VECTOR graphics (bg bars, boxes, charts)
                     are NOT redrawn. Best for text-led docs.
  exact              Each page rendered to a crisp image (all graphics/layout
                     preserved) with a transparent, selectable text layer.
                     Max visual fidelity; not meant for editing.
  editable           For image-only / flattened PDFs with no text layer.
                     OCRs each page, PAINTS OVER the original baked-in text
                     with a sampled background color, and lays real editable
                     text on top of the page image. The result is genuinely
                     editable while keeping the original look.

LAYOUTS (what the file is for):
  display  (default) Standalone viewer: page framing + a slim top bar. For
                     sharing as a link or opening locally.
  clean              No chrome at all, just the page sections. For dropping
                     into / replacing an existing web page or CMS block.

OTHER:
  --pdf-button       Include a Print / Save-as-PDF button (display only).
                     Off by default.
  --title "..."      Title for the tab / top bar.
  --dpi N            Raster DPI (exact + editable). Default 150.

Built on tooling preinstalled in the Cowork sandbox: pdfplumber, poppler
(pdf2image / pdfimages), Pillow, and tesseract (pytesseract) for editable mode.

Usage:
  python3 convert.py IN.pdf [-o OUT.html] [--mode reflow|exact|editable]
                     [--layout display|clean] [--pdf-button]
                     [--title "Title"] [--dpi 150]
"""

import argparse
import base64
import glob
import html
import io
import os
import re
import statistics
import subprocess
import sys
import tempfile

try:
    import pdfplumber
except ImportError:
    sys.stderr.write("ERROR: pdfplumber missing. pip install pdfplumber --break-system-packages\n")
    sys.exit(2)


# ---------------------------------------------------------------------------
# Color + font helpers
# ---------------------------------------------------------------------------

def to_css_color(c):
    """pdfplumber non_stroking_color -> '#rrggbb' (gray/rgb/cmyk tolerant)."""
    try:
        if c is None:
            return "#000000"
        if isinstance(c, (int, float)):
            v = int(round(float(c) * 255)); return "#%02x%02x%02x" % (v, v, v)
        c = tuple(c)
        if len(c) == 1:
            v = int(round(float(c[0]) * 255)); return "#%02x%02x%02x" % (v, v, v)
        if len(c) == 3:
            r, g, b = (int(round(float(x) * 255)) for x in c); return "#%02x%02x%02x" % (r, g, b)
        if len(c) == 4:
            cc, m, y, k = (float(x) for x in c)
            r = int(round(255 * (1 - cc) * (1 - k))); g = int(round(255 * (1 - m) * (1 - k)))
            b = int(round(255 * (1 - y) * (1 - k))); return "#%02x%02x%02x" % (r, g, b)
    except Exception:
        pass
    return "#000000"


def font_style(fontname):
    """PDF fontname -> (css-family, weight, style)."""
    name = re.sub(r"^[A-Z]{6}\+", "", fontname or "")
    low = name.lower()
    weight = "700" if re.search(r"bold|black|heavy|semibold|demi", low) else "400"
    style = "italic" if re.search(r"italic|oblique", low) else "normal"
    base = re.split(r"[-,]", name)[0] or "sans-serif"
    if re.search(r"times|serif|georgia|garamond|minion", low):
        generic = "Georgia,'Times New Roman',serif"
    elif re.search(r"courier|mono|consol", low):
        generic = "'Courier New',monospace"
    else:
        generic = "Arial,Helvetica,sans-serif"
    return "'%s',%s" % (base, generic), weight, style


# ---------------------------------------------------------------------------
# Image extraction for reflow mode (poppler pdfimages)
# ---------------------------------------------------------------------------

def extract_page_images(pdf_path, workdir):
    prefix = os.path.join(workdir, "img")
    try:
        subprocess.run(["pdfimages", "-all", "-p", pdf_path, prefix], check=True, capture_output=True)
    except Exception as e:
        sys.stderr.write("warn: pdfimages failed (%s); images skipped\n" % e)
        return {}
    buckets = {}
    for fp in sorted(glob.glob(prefix + "-*")):
        m = re.search(r"-(\d+)-(\d+)\.", os.path.basename(fp))
        if not m:
            continue
        buckets.setdefault(int(m.group(1)), []).append((int(m.group(2)), fp))
    for p in buckets:
        buckets[p] = [fp for _, fp in sorted(buckets[p])]
    return buckets


def img_data_uri(path):
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "tif": "image/tiff", "tiff": "image/tiff",
            "ppm": "image/x-portable-pixmap", "pbm": "image/x-portable-bitmap"}.get(ext, "image/png")
    if mime.startswith("image/x-portable") or ext in ("tif", "tiff"):
        try:
            from PIL import Image
            im = Image.open(path).convert("RGB")
            buf = io.BytesIO(); im.save(buf, format="PNG"); data = buf.getvalue(); mime = "image/png"
        except Exception:
            with open(path, "rb") as fh:
                data = fh.read()
    else:
        with open(path, "rb") as fh:
            data = fh.read()
    return "data:%s;base64,%s" % (mime, base64.b64encode(data).decode("ascii"))


# ---------------------------------------------------------------------------
# OCR helpers for editable mode
# ---------------------------------------------------------------------------

def _is_real_word(token):
    """A token counts as real text if it has an alphabetic run of >=3 letters."""
    return re.search(r"[A-Za-z]{3,}", token) is not None


def _good_line(text):
    """Reject OCR junk picked up from artwork: keep lines that carry at least
    one real word and are mostly alphanumeric (not a soup of symbols)."""
    compact = re.sub(r"[^A-Za-z0-9]", "", text)
    if len(compact) < 3:
        return False
    if not any(_is_real_word(t) for t in text.split()):
        return False
    alpha = sum(c.isalnum() or c.isspace() for c in text)
    return alpha / max(1, len(text)) >= 0.6


def _keep_word(txt):
    """Per-word gate: a real word (>=2 letters) or a numeric token. Drops
    stray symbols ('|', '=', '~') and single chars that OCR hallucinates
    from artwork and that otherwise stretch a line's mask box."""
    return bool(re.search(r"[A-Za-z]{2,}", txt) or re.fullmatch(r"[0-9][0-9.,%/$\-]*", txt))


def ocr_lines(pil_img):
    """Return real text lines [{text,l,t,r,b}] from tesseract word boxes.

    Filtering happens at the word level (confidence + real-word gate), then
    each tesseract line is split on large horizontal gaps and only the
    densest cluster is kept. This prevents a junk token detected far out in
    the artwork from being merged into a real line and dragging its mask box
    across the graphics."""
    import pytesseract
    d = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
    raw = {}
    for i in range(len(d["text"])):
        txt = d["text"][i]
        try:
            conf = float(d["conf"][i])
        except Exception:
            conf = -1
        if not txt.strip() or conf < 50:
            continue
        key = (d["block_num"][i], d["par_num"][i], d["line_num"][i])
        x, y, w, h = d["left"][i], d["top"][i], d["width"][i], d["height"][i]
        raw.setdefault(key, []).append({"t": txt, "l": x, "r": x + w, "top": y, "bot": y + h})

    out = []
    for words in raw.values():
        words.sort(key=lambda z: z["l"])
        widths = [w["r"] - w["l"] for w in words]
        mw = statistics.median(widths) if widths else 10
        clusters = [[words[0]]]
        for prev, cur in zip(words, words[1:]):
            if cur["l"] - prev["r"] > 2.5 * mw:
                clusters.append([cur])
            else:
                clusters[-1].append(cur)
        best = max(clusters, key=lambda c: sum(len(re.sub(r"[^A-Za-z0-9]", "", w["t"])) for w in c))
        text = " ".join(w["t"] for w in best)
        if not _good_line(text):
            continue
        out.append({"text": text,
                    "l": min(w["l"] for w in best), "t": min(w["top"] for w in best),
                    "r": max(w["r"] for w in best), "b": max(w["bot"] for w in best)})
    return out


def _avg_color(img, box):
    region = img.crop(box).resize((1, 1))
    px = region.getpixel((0, 0))
    return px[:3] if isinstance(px, tuple) else (px, px, px)


def _bg_for_line(img, l, t, r, b):
    """Sample the background just above/below a text box (median-ish blend)."""
    W, H = img.width, img.height
    band = max(2, int((b - t) * 0.35))
    boxes = [(max(0, l), max(0, t - band), min(W, r), max(1, t)),
             (max(0, l), min(H - 1, b), min(W, r), min(H, b + band))]
    cols = [_avg_color(img, bx) for bx in boxes if bx[2] > bx[0] and bx[3] > bx[1]]
    if not cols:
        return (22, 32, 44)
    return tuple(sum(c[i] for c in cols) // len(cols) for i in range(3))


def build_editable_page(idx, ocr_img, disp_w, layout):
    """OCR a rendered page, paint over the original text with sampled
    background, and overlay real editable text. Returns a .page div."""
    from PIL import ImageDraw
    scale = disp_w / float(ocr_img.width)
    disp = ocr_img.convert("RGB").resize((disp_w, int(round(ocr_img.height * scale))))
    lines = ocr_lines(ocr_img)
    draw = ImageDraw.Draw(disp)
    runs = []
    ce = "" if layout == "clean" else ' contenteditable="true"'
    for ln in lines:
        l, t, r, b = (ln["l"] * scale, ln["t"] * scale, ln["r"] * scale, ln["b"] * scale)
        pad = (b - t) * 0.20
        box = (max(0, int(l - pad)), max(0, int(t - pad)),
               min(disp.width, int(r + pad)), min(disp.height, int(b + pad)))
        bg = _bg_for_line(disp, *box)
        draw.rectangle(box, fill=bg)  # erase original baked-in text
        lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
        color = "#ffffff" if lum < 140 else "#111111"
        size = max(8.0, (b - t) * 0.92)
        runs.append('<p class="ed"%s style="left:%.1fpx;top:%.1fpx;font-size:%.1fpx;color:%s;">%s</p>'
                    % (ce, l, t, size, color, html.escape(ln["text"])))
    buf = io.BytesIO()
    disp.save(buf, format="JPEG", quality=82)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    return ('<div class="page editable" data-page="%d" style="width:%dpx;height:%dpx;">'
            '<img class="bg" src="%s" style="width:%dpx;height:%dpx;">%s</div>'
            ) % (idx, disp.width, disp.height, uri, disp.width, disp.height, "".join(runs))


# ---------------------------------------------------------------------------
# reflow / exact page builders
# ---------------------------------------------------------------------------

def build_reflow_page(page, page_images, layout):
    w, h = page.width, page.height
    ce = "" if layout == "clean" else ' contenteditable="true"'
    parts = []
    imgs = page.images or []
    for idx, im in enumerate(imgs):
        if idx >= len(page_images):
            break
        try:
            x0 = float(im["x0"]); top = float(im["top"])
            iw = float(im["x1"]) - x0; ih = float(im["bottom"]) - top
            uri = img_data_uri(page_images[idx])
            parts.append('<img class="im" src="%s" style="left:%.2fpx;top:%.2fpx;width:%.2fpx;height:%.2fpx;">'
                         % (uri, x0, top, iw, ih))
        except Exception:
            continue
    try:
        lines = page.extract_text_lines(layout=False, strip=False)
    except Exception:
        lines = []
    for ln in lines:
        chars = ln.get("chars") or []
        if not chars:
            continue
        sizes = [c.get("size", 12) for c in chars if c.get("size")]
        size = statistics.median(sizes) if sizes else 12
        fam, weight, style = font_style(chars[0].get("fontname", ""))
        color = to_css_color(chars[0].get("non_stroking_color"))
        parts.append('<p%s style="left:%.2fpx;top:%.2fpx;font-size:%.2fpx;font-family:%s;'
                     'font-weight:%s;font-style:%s;color:%s;">%s</p>'
                     % (ce, float(ln["x0"]), float(ln["top"]), size, fam, weight, style,
                        color, html.escape(ln.get("text", ""))))
    return '<div class="page" data-page="%d" style="width:%.2fpx;height:%.2fpx;">%s</div>' % (
        page.page_number, w, h, "".join(parts))


def build_exact_page(page, png_uri):
    w, h = page.width, page.height
    overlay = []
    try:
        lines = page.extract_text_lines(layout=False, strip=False)
    except Exception:
        lines = []
    for ln in lines:
        chars = ln.get("chars") or []
        if not chars:
            continue
        sizes = [c.get("size", 12) for c in chars if c.get("size")]
        size = statistics.median(sizes) if sizes else 12
        overlay.append('<p style="left:%.2fpx;top:%.2fpx;font-size:%.2fpx;">%s</p>'
                       % (float(ln["x0"]), float(ln["top"]), size, html.escape(ln.get("text", ""))))
    return ('<div class="page exact" data-page="%d" style="width:%.2fpx;height:%.2fpx;">'
            '<img class="bg" src="%s" style="width:%.2fpx;height:%.2fpx;">'
            '<div class="exact-text">%s</div></div>'
            ) % (page.page_number, w, h, png_uri, w, h, "".join(overlay))


# ---------------------------------------------------------------------------
# Document shell
# ---------------------------------------------------------------------------

SHELL = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#525659;--page:#fff;--bar:#2b2f31;--bar-ink:#f4f4f5;--accent:#ff6a00;--gap:__GAP__;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:var(--bg);
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}
#toolbar{position:sticky;top:0;z-index:50;display:flex;gap:.5rem;align-items:center;
  flex-wrap:wrap;background:var(--bar);color:var(--bar-ink);padding:.5rem .9rem;
  font-size:13px;box-shadow:0 1px 6px rgba(0,0,0,.35);}
#toolbar .title{font-weight:600;margin-right:auto;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;max-width:60vw;}
#toolbar button{background:#3a3f42;color:var(--bar-ink);border:1px solid #4b5155;
  border-radius:6px;padding:.4rem .7rem;cursor:pointer;font-size:13px;}
#toolbar button:hover{background:#474d51;}
#pages{padding:var(--gap) 12px 48px;display:flex;flex-direction:column;align-items:center;gap:var(--gap);}
.page{position:relative;background:var(--page);overflow:hidden;transform-origin:top center;}
.page p{position:absolute;margin:0;white-space:pre;line-height:1;}
.page p.ed{white-space:pre-wrap;}
.page img.im{position:absolute;object-fit:fill;}
.page img.bg{display:block;position:absolute;left:0;top:0;}
.exact-text{position:absolute;inset:0;}
.exact-text p{color:transparent;}
/* display layout: page framing */
body.display .page{box-shadow:0 6px 24px rgba(0,0,0,.4);}
/* clean layout: no chrome, white canvas, flush pages */
body.clean{background:#fff;}
body.clean #pages{padding:0;gap:var(--gap);}
@media print{
  body{background:#fff;}#toolbar{display:none;}#pages{padding:0;gap:0;}
  .page{box-shadow:none;page-break-after:always;}
}
</style></head>
<body class="__LAYOUT__">
__TOOLBAR__
<div id="pages">
__PAGES__
</div>
<script>
(function(){
  // Auto-fit pages to the viewport width, on load and on resize.
  function fit(){
    document.querySelectorAll('.page').forEach(function(pg){
      if(!pg.__base) pg.__base=parseFloat(pg.style.width)||pg.offsetWidth;
      var avail=Math.min(window.innerWidth-24,pg.__base);
      var s=avail/pg.__base;
      pg.style.transform='scale('+s+')';
      pg.style.marginBottom=(pg.offsetHeight*(s-1))+'px';
    });
  }
  window.addEventListener('resize',fit); fit();
  var pb=document.getElementById('pdfBtn');
  if(pb) pb.addEventListener('click',function(){window.print();});
})();
</script>
</body></html>
"""


def make_toolbar(title, layout, pdf_button):
    if layout == "clean":
        return ""
    btn = ('<button id="pdfBtn" title="Print or save as PDF">Print / PDF</button>'
           if pdf_button else "")
    return ('<div id="toolbar"><span class="title">%s</span>%s</div>'
            % (html.escape(title), btn))


def build_html(pdf_path, mode, layout, title, dpi, pdf_button):
    title = title or os.path.splitext(os.path.basename(pdf_path))[0]
    gap = "0" if layout == "clean" else "12px"
    pages_html = []

    if mode == "exact":
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=dpi)
        png = {}
        for i, im in enumerate(images, start=1):
            buf = io.BytesIO(); im.save(buf, format="PNG")
            png[i] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages_html.append(build_exact_page(page, png.get(page.page_number, "")))

    elif mode == "editable":
        from pdf2image import convert_from_path
        ocr_dpi = max(dpi, 180)  # higher dpi = better OCR
        images = convert_from_path(pdf_path, dpi=ocr_dpi)
        for i, im in enumerate(images, start=1):
            pages_html.append(build_editable_page(i, im, disp_w=1600, layout=layout))

    else:  # reflow
        with tempfile.TemporaryDirectory() as wd:
            buckets = extract_page_images(pdf_path, wd)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    pages_html.append(build_reflow_page(page, buckets.get(page.page_number, []), layout))

    return (SHELL.replace("__TITLE__", html.escape(title))
            .replace("__GAP__", gap)
            .replace("__LAYOUT__", layout)
            .replace("__TOOLBAR__", make_toolbar(title, layout, pdf_button))
            .replace("__PAGES__", "\n".join(pages_html)))


def main():
    ap = argparse.ArgumentParser(description="PDF -> single self-contained HTML.")
    ap.add_argument("input", help="source PDF path")
    ap.add_argument("-o", "--output", help="output .html (default: alongside input)")
    ap.add_argument("--mode", choices=["reflow", "exact", "editable"], default="reflow",
                    help="reflow=editable rebuild; exact=image+selectable text; editable=OCR image-only PDFs")
    ap.add_argument("--layout", choices=["display", "clean"], default="display",
                    help="display=standalone viewer (default); clean=bare pages to replace/embed in a web page")
    ap.add_argument("--pdf-button", action="store_true", help="include a Print/Save-as-PDF button (display only)")
    ap.add_argument("--title", help="document title (tab + top bar)")
    ap.add_argument("--dpi", type=int, default=150, help="raster DPI for exact/editable (default 150)")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        sys.stderr.write("ERROR: file not found: %s\n" % args.input)
        sys.exit(1)

    out_path = args.output or os.path.splitext(args.input)[0] + ".html"
    html_str = build_html(args.input, args.mode, args.layout, args.title, args.dpi, args.pdf_button)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html_str)

    kb = os.path.getsize(out_path) / 1024.0
    sys.stderr.write("OK  %s  (%.0f KB, mode=%s, layout=%s)\n" % (out_path, kb, args.mode, args.layout))
    print(out_path)


if __name__ == "__main__":
    main()
