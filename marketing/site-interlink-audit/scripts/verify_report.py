#!/usr/bin/env python3
"""
Verify the report renders and behaves: no JS errors, treemap tiles sane, filters and
checkboxes work, persistence works. Measure the DOM, do not trust a screenshot.
"""
import sys, json, os
from playwright.sync_api import sync_playwright

_arg = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/deep/Apps&Projects/span-interlink-report.html"
if not _arg.startswith(("file://", "http://", "https://")):
    _arg = "file://" + os.path.abspath(_arg).replace("&", "%26")
URL = _arg
WIDE, NARROW = 1440, 390
fails, notes = [], []
seen_err = set()


def check(ok, label, detail=""):
    (notes if ok else fails).append(f"{'ok  ' if ok else 'FAIL'} {label}{(' | ' + detail) if detail else ''}")


with sync_playwright() as pw:
    b = pw.chromium.launch()
    for w in (WIDE, NARROW):
        pg = b.new_page(viewport={"width": w, "height": 900})
        errs = []
        pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}")
              if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(1400)

        for e in errs:
            if e not in seen_err:
                seen_err.add(e)
                fails.append(f"console @{w}: {e}")

        kpi = pg.eval_on_selector_all(".kpi b", "els => els.map(e => e.textContent.trim())")
        check(len(kpi) == 7, f"kpis @{w}", f"{len(kpi)} shown")

        nf = pg.eval_on_selector_all(".find", "els => els.length")
        check(nf > 0, f"findings @{w}", f"{nf} shown")
        empty = pg.eval_on_selector_all(".find span", "els => els.filter(e=>!e.textContent.trim()).length")
        check(empty == 0, f"findings have body @{w}", f"{empty} empty")
        ofl = pg.eval_on_selector_all(".find", "els => els.filter(e => {const r=e.getBoundingClientRect(); return getComputedStyle(e).overflow!=='visible';}).length")
        check(ofl == 0, f"findings not clipped @{w}")

        # treemap
        tiles = pg.eval_on_selector_all(".tile", """els => {
            const box = document.getElementById('map').getBoundingClientRect();
            return els.map(e => {
                const r = e.getBoundingClientRect();
                const tn = e.querySelector('.tn');
                return {sec: tn ? tn.textContent : '',
                        x: r.x - box.x, y: r.y - box.y,
                        w: r.width, h: r.height,
                        clipped: tn ? (tn.scrollWidth > tn.clientWidth+1 ||
                                       tn.scrollHeight > tn.clientHeight+1) : false};
            });
        }""")
        mbox = pg.eval_on_selector("#map", "e => {const r=e.getBoundingClientRect();return [r.width, r.height];}")
        cov = (sum(t['w'] * t['h'] for t in tiles) / (mbox[0] * mbox[1])) if mbox[0] else 0
        check(len(tiles) >= (8 if w == WIDE else 4), f"tiles @{w}", f"{len(tiles)} tiles")
        check(cov > 0.55, f"tiles cover canvas @{w}", f"{cov:.0%} coverage")
        bad = [t for t in tiles if t["clipped"]]
        check(not bad, f"tile labels clipped @{w}",
              "; ".join(f"{t['sec']}({t['w']:.0f}x{t['h']:.0f})" for t in bad[:4]))
        eli = [t["sec"] for t in tiles if "\u2026" in (t["sec"] or "")]
        check(not eli, f"no ellipsised tile labels @{w}", "; ".join(eli[:4]))

        tiny = [t for t in tiles if t["w"] < 26 or t["h"] < 20]
        check(not tiny, f"tiles too small @{w}",
              "; ".join(f"{t['sec']}({t['w']:.0f}x{t['h']:.0f})" for t in tiny[:4]))

        # overlap
        off = [t for t in tiles if t['x'] < -1 or t['y'] < -1]
        check(not off, f"tiles inside map box @{w}",
              "; ".join(f"{t['sec']}({t['x']:.0f},{t['y']:.0f})" for t in off[:4]))

        ov = 0
        for a in range(len(tiles)):
            for c in range(a + 1, len(tiles)):
                A, B = tiles[a], tiles[c]
                if (min(A['x']+A['w'], B['x']+B['w']) - max(A['x'], B['x']) > 1 and
                        min(A['y']+A['h'], B['y']+B['h']) - max(A['y'], B['y']) > 1):
                    ov += 1
        check(ov == 0, f"tile overlaps @{w}", f"{ov} pairs")

        # tap targets
        small = pg.evaluate("""() => {
            const out = [];
            document.querySelectorAll('button, input[type=checkbox]').forEach(e => {
                const r = e.getBoundingClientRect();
                if (r.width && r.height && (r.width < 44 || r.height < 44))
                    out.push(e.tagName + '.' + (e.className||'') + ' ' +
                             Math.round(r.width) + 'x' + Math.round(r.height));
            });
            return out.slice(0,5);
        }""")
        check(not small, f"tap targets >=44px @{w}", "; ".join(small))

        # tab switch + interactions
        if w == WIDE:
            pg.click('nav button[data-view="work"]')
            pg.wait_for_timeout(450)
            vis = pg.eval_on_selector("#v-work", "e => !e.hidden")
            check(vis, "worklist tab opens")
            rows = pg.eval_on_selector_all(".wa", "e => e.length")
            check(rows > 0, "worklist rows", f"{rows}")
            if rows:
                cb = pg.query_selector(".wa input[type=checkbox]")
                cb.click()
                pg.wait_for_timeout(300)
                ls = pg.evaluate("() => localStorage.getItem(Object.keys(localStorage)[0])")
                check(ls and len(ls) > 2, "progress persists to localStorage", (ls or "")[:40])
                txt = pg.inner_text("#ptxt")
                check("1 of" in txt, "progress readout updates", txt)
                pg.click('nav button[data-view="ents"]')
                pg.wait_for_timeout(400)
                ents = pg.eval_on_selector_all(".ent", "e => e.length")
                check(ents > 0, "entity rows", f"{ents}")
            pg.click('nav button[data-view="map"]')
            pg.wait_for_timeout(500)
        pg.close()
    b.close()

for n in notes:
    print(n)
print()
for f in fails:
    print(f)
print(f"\n{len(notes)} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)