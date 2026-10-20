#!/usr/bin/env python3
"""Render gate for a finished page. Usage: python3 verify.py page.html [--shots] [--budget1440 3000] [--budget390 6500]
Needs: pip install playwright && playwright install chromium (or Chrome installed; falls back to channel=chrome).
Exit code 1 on any FAIL. If Playwright is unavailable, say so and label the page UNVERIFIED."""
import sys, re, pathlib

args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
path = pathlib.Path(args[0])
shots = "--shots" in args
def opt(name, default):
    return int(args[args.index(name) + 1]) if name in args else default
b1440, b390 = opt("--budget1440", 3000), opt("--budget390", 6500)

html = path.read_text(encoding="utf-8")
fails = []
dashes = len(re.findall("[\u2013\u2014]", html))
print("dashes in source:", dashes)
if dashes:
    fails.append("em/en dashes present")

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    try:
        br = p.chromium.launch()
    except Exception:
        br = p.chromium.launch(channel="chrome")
    for w, h, scheme in [(390, 844, "light"), (1440, 900, "light"), (390, 844, "dark")]:
        pg = br.new_page(viewport={"width": w, "height": h}, color_scheme=scheme)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto(path.resolve().as_uri() + "?static=1", wait_until="networkidle")
        r = pg.evaluate("""() => ({
          H: document.documentElement.scrollHeight,
          over: document.documentElement.scrollWidth > innerWidth,
          fold: [...document.querySelectorAll('[data-fold]')].filter(e => e.getBoundingClientRect().bottom > innerHeight).map(e => e.textContent.trim().slice(0, 40)),
          small: [...document.querySelectorAll('a,button,summary,input')].filter(e => { const b = e.getBoundingClientRect(); return b.width && (b.height < 40) && getComputedStyle(e).display !== 'inline'; }).map(e => e.textContent.trim().slice(0, 24))
        })""")
        # Google Fonts failing in a sandbox is expected, not a page error.
        errs = [e for e in errs if "fonts.g" not in e and "ERR_" not in e]
        print(f"{w} {scheme}: height {r['H']}, overflow {r['over']}, fold missing {r['fold']}, small targets {r['small']}, console errors {errs}")
        if r["over"]: fails.append(f"horizontal overflow at {w}")
        if w == 390 and r["fold"]: fails.append("fold missing at 390: " + str(r["fold"]))
        if w == 1440 and r["H"] > b1440: fails.append(f"height {r['H']} > budget {b1440} at 1440")
        if w == 390 and scheme == "light" and r["H"] > b390: fails.append(f"height {r['H']} > budget {b390} at 390")
        if errs: fails.append("console errors: " + str(errs))
        if shots:
            pg.screenshot(path=f"shot-{w}-{scheme}.png", full_page=(w == 1440 or scheme == "light"))
    br.close()

print("FAIL: " + "; ".join(fails) if fails else "PASS")
sys.exit(1 if fails else 0)
