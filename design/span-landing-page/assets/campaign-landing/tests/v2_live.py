"""Live (non-static) behaviour probe for template-v2.html: scroll the page, then read end states.

Usage: python3 tests/v2_live.py  (Playwright). Prints PASS/FAIL lines, exits 1 on any FAIL.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
fails = []


def check(ok, label):
    print('PASS' if ok else 'FAIL', label)
    if not ok:
        fails.append(label)


with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
    b = p.chromium.launch()
    for name in ('span-msp-us', 'span-peo-eor'):
        out = Path(tmp) / (name + '.html')
        subprocess.run([sys.executable, str(ROOT / 'build.py'), str(ROOT / 'examples' / name), '--template', str(ROOT / 'template-v2.html'), '--out', str(out)], check=True, capture_output=True)
        for reduce in (False, True):
            tag = '%s %s' % (name, 'reduced' if reduce else 'motion')
            ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce' if reduce else 'no-preference')
            pg = ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(out.as_uri(), wait_until='networkidle')
            band_markup = pg.evaluate('[...document.querySelectorAll(".band__n b")].map(b => b.textContent)')
            stream = pg.locator('.stream').count()
            first = pg.evaluate('document.querySelector(".stream tbody tr") && document.querySelector(".stream tbody tr").textContent')
            pg.wait_for_timeout(4600)
            moved = pg.evaluate('document.querySelector(".stream tbody tr") && document.querySelector(".stream tbody tr").textContent') != first
            if stream:
                check(moved != reduce, tag + ': stream rotates only with motion allowed')
                check(pg.locator('.stream__pause').is_visible() != reduce, tag + ': Pause shown only when rotating')
                if not reduce:
                    pg.locator('.stream__pause').click()
                    held = pg.evaluate('document.querySelector(".stream tbody tr").textContent')
                    pg.wait_for_timeout(4600)
                    check(pg.evaluate('document.querySelector(".stream tbody tr").textContent') == held, tag + ': Pause holds the rows')
                    check(pg.locator('.stream__pause').get_attribute('aria-pressed') == 'true', tag + ': Pause sets aria-pressed')
            beats = []
            h = pg.evaluate('document.documentElement.scrollHeight')
            for y in range(0, h, 250):
                pg.evaluate('window.scrollTo({top:%d, behavior:"instant"})' % y)
                pg.wait_for_timeout(200)
                beats.append(pg.evaluate('(document.querySelector(".beats a[aria-current]") || {}).textContent'))
            pg.wait_for_timeout(1900)
            check(pg.evaluate('[...document.querySelectorAll(".rv")].every(e => getComputedStyle(e).opacity === "1")'), tag + ': every reveal ends at opacity 1')
            seen = [x for i, x in enumerate(beats) if x and x not in beats[:i]]
            check(seen == ['01', '02', '03', '04', '05'], tag + ': beat rail walks 01..05 %s' % seen)
            check(pg.evaluate('getComputedStyle(document.getElementById("beatsFill")).transform') == 'matrix(1, 0, 0, 1, 0, 0)', tag + ': progress line full at bottom')
            check(pg.evaluate('[...document.querySelectorAll(".band__n b")].map(b => b.textContent)') == band_markup, tag + ': band figures end at markup values %s' % band_markup)
            # accordion keyboard
            pg.locator('#accb1').focus()
            pg.keyboard.press('ArrowDown')
            check(pg.evaluate('document.activeElement.id') == 'accb2', tag + ': ArrowDown moves to next trigger')
            pg.keyboard.press('Enter')
            pg.wait_for_timeout(400)
            check(pg.evaluate('[...document.querySelectorAll(".acc__btn")].map(b => b.getAttribute("aria-expanded")).join()') == 'false,true,false,false,false', tag + ': Enter opens one panel')
            check(pg.evaluate('document.getElementById("accp1").inert && !document.getElementById("accp2").inert'), tag + ': closed panels are inert')
            check(not errs, tag + ': no page errors %s' % errs)
            ctx.close()
    b.close()
print('fails', len(fails))
sys.exit(1 if fails else 0)
