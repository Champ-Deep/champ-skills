#!/usr/bin/env python3
"""
Render a carousel JSON into per-slide PNGs and a multi-page PDF.

Usage:
  python3 render.py slides.json out_dir [--formats linkedin,square] [--no-fit]

Formats:
  linkedin  1080 x 1350 (4:5 portrait). Use for the LinkedIn document post PDF
            and for Instagram feed carousels (4:5 is the tallest Instagram allows).
  square    1080 x 1080. Use when a channel needs square (some ad placements,
            WhatsApp forwards, X images).

Outputs (per format):
  out_dir/<format>/slide-01.png ... slide-NN.png
  out_dir/<format>/<slug>-<format>.pdf   (pages are the PNGs, so fonts can never break)

Checks performed before rendering:
  1. No em dashes or en dashes anywhere in the JSON (house rule).
  2. Every slide's body fits the frame. If it overflows, the body is scaled down
     in steps to 72 percent; if it still overflows the script fails and names
     the slide. Cut words rather than shipping a scaled slide below 85 percent.

Requires: playwright (with chromium installed), img2pdf (preferred, lossless) or Pillow.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

SIZES = {"linkedin": (1080, 1350), "square": (1080, 1080)}
DASHES = re.compile("[–—]")


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) < 2:
        fail("usage: render.py slides.json out_dir [--formats linkedin,square] [--no-fit]")
    src, out_root = Path(args[0]), Path(args[1])
    formats = ["linkedin"]
    for f in flags:
        if f.startswith("--formats="):
            formats = f.split("=", 1)[1].split(",")
    fit = "--no-fit" not in flags

    raw = src.read_text(encoding="utf-8")
    m = DASHES.search(raw)
    if m:
        line = raw[: m.start()].count("\n") + 1
        fail(f"em or en dash found in {src.name} at line {line}. Replace it before rendering.")
    data = json.loads(raw)
    slug = data.get("slug") or src.stem
    template = (Path(__file__).resolve().parent.parent / "templates" / "carousel.html").read_text(encoding="utf-8")
    html = template.replace(
        '<script id="data" type="application/json">{"brand":{},"slides":[]}</script>',
        '<script id="data" type="application/json">' + json.dumps(data).replace("</", "<\\/") + "</script>",
    )
    tmp = Path(tempfile.mkdtemp()) / "carousel.html"
    tmp.write_text(html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for fmt in formats:
            if fmt not in SIZES:
                fail(f"unknown format {fmt}")
            w, h = SIZES[fmt]
            out = out_root / fmt
            out.mkdir(parents=True, exist_ok=True)
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            page.goto(tmp.as_uri())
            if fmt == "square":
                page.evaluate("document.documentElement.classList.add('square')")
            page.wait_for_timeout(600)  # let web fonts settle
            page.evaluate("document.fonts && document.fonts.ready")
            count = page.evaluate("document.querySelectorAll('.slide').length")
            pngs = []
            for i in range(count):
                sel = f".slide[data-index='{i}']"
                if fit:
                    zoom = page.evaluate(
                        """(sel) => {
                          const body = document.querySelector(sel + ' .body');
                          let z = 1.0;
                          body.style.zoom = z;
                          while (body.scrollHeight > body.clientHeight + 2 && z > 0.72) {
                            z = Math.round((z - 0.03) * 100) / 100;
                            body.style.zoom = z;
                          }
                          return body.scrollHeight > body.clientHeight + 2 ? -1 : z;
                        }""",
                        sel,
                    )
                    if zoom == -1:
                        fail(f"slide {i+1} ({fmt}) still overflows at 72 percent. Cut copy.")
                    if zoom < 0.85:
                        print(f"WARNING: slide {i+1} ({fmt}) scaled to {int(zoom*100)} percent. Cut words for legibility.")
                else:
                    over = page.evaluate(
                        "(sel) => { const b = document.querySelector(sel + ' .body'); return b.scrollHeight - b.clientHeight; }", sel
                    )
                    if over > 2:
                        fail(f"slide {i+1} ({fmt}) overflows by {over}px.")
                png = out / f"slide-{i+1:02d}.png"
                page.locator(sel).screenshot(path=str(png), type="png")
                pngs.append(png)
            page.close()
            pdf = out / f"{slug}-{fmt}.pdf"
            try:
                import img2pdf  # lossless: PNG bytes embedded as-is, text stays crisp
                pdf.write_bytes(img2pdf.convert([str(x) for x in pngs]))
            except ImportError:
                Image.init()
                images = [Image.open(x).convert("RGB") for x in pngs]
                images[0].save(pdf, save_all=True, append_images=images[1:], resolution=144.0, quality=95)
            print(f"{fmt}: {count} slides -> {pdf}")
        browser.close()


if __name__ == "__main__":
    main()
