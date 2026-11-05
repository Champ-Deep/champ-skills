"""Browser gates for template-v2.html: overflow, form fold, sticky CTA, hero and closer contrast, FAQ, console.

Usage: python3 tests/v2_check.py  (needs Playwright with Chromium; writes screenshots to qa/v2/)
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from browser_check import geometry  # noqa: E402  (same overflow probe as v1)

OUT = ROOT / 'qa' / 'v2'
WIDTHS = (390, 834, 1440)
CONTRAST = '''(sel) => {
  const lin = c => { c /= 255; return c <= .03928 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; };
  const L = ([r, g, b]) => .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b);
  const parse = s => { const m = s.match(/[\\d.]+/g).map(Number); const srgb = s.startsWith('color('); return {rgb: m.slice(0, 3).map(v => srgb ? v * 255 : v), a: m.length > 3 ? m[3] : 1}; };
  const over = (top, under) => top.rgb.map((v, i) => v * top.a + under[i] * (1 - top.a));
  function ground(el) {
    const stack = [];
    for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c.a > 0) stack.push(c); if (c.a === 1) break; }
    let rgb = [255, 255, 255]; for (const c of stack.reverse()) rgb = over(c, rgb); return rgb;
  }
  const out = [];
  for (const root of document.querySelectorAll(sel)) {
    const walk = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (let n; (n = walk.nextNode());) {
      const el = n.parentElement, t = n.textContent.trim(), s = getComputedStyle(el), r = el.getBoundingClientRect();
      if (!t || s.visibility === 'hidden' || s.display === 'none' || !r.width || el.closest('.sr,[hidden],.thanks,.err,.srcs__list,#providerWrap:not(.show)')) continue;
      const fg = parse(s.color), bg = ground(el), ink = over(fg, bg);
      const a = L(ink), b = L(bg);
      out.push({text: t.slice(0, 40), ratio: Math.round((Math.max(a, b) + .05) / (Math.min(a, b) + .05) * 100) / 100});
    }
  }
  return out;
}'''


# Brief section 4: no gradients behind anything, no empty bars. Orbit (.ot-*) is kept as shipped per the brief.
FLAT = '''() => {
  const hits = [];
  const id = el => ((el.closest('[id]') || {}).id || '') + ' ' + el.tagName.toLowerCase() + '.' + String(el.className).trim().split(/\\\\s+/).join('.');
  for (const el of document.querySelectorAll('body *')) {
    if (el.closest('[class*="ot-"],svg,.sr')) continue;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    if (!r.width || !r.height || cs.visibility === 'hidden') continue;
    for (const pseudo of [null, '::before', '::after']) {
      const s = pseudo ? getComputedStyle(el, pseudo) : cs;
      if (pseudo && (s.content === 'none' || s.display === 'none')) continue;
      if (s.backgroundImage.includes('gradient')) hits.push('gradient ' + id(el) + (pseudo || ''));
    }
    const filled = cs.backgroundImage !== 'none' || !cs.backgroundColor.endsWith(', 0)');
    // .wg__bar is a share meter: its width is the tile's share figure, printed beside it in .wg__share
    if (r.width > 40 && r.height <= 14 && filled && !el.textContent.trim() && !el.children.length && !el.closest('.wg__bar')) hits.push('empty bar ' + id(el) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  }
  return hits;
}'''


def flat_sweep(page):
    """Open every FAQ panel in turn and collect gradient and empty-bar hits across all states."""
    hits = set(page.evaluate(FLAT))
    btns = page.locator('.acc__btn')
    for i in range(btns.count()):
        if btns.nth(i).get_attribute('aria-expanded') != 'true':
            btns.nth(i).click()
        page.wait_for_timeout(450)
        hits.update(page.evaluate(FLAT))
    return sorted(hits)


def build(tmp):
    pages = {}
    for name in ('span-msp-us', 'span-peo-eor'):
        out = Path(tmp) / (name + '.html')
        subprocess.run([sys.executable, str(ROOT / 'build.py'), str(ROOT / 'examples' / name), '--template', str(ROOT / 'template-v2.html'), '--out', str(out)], check=True, capture_output=True)
        pages[name] = out
    return pages


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    failures, report = [], {}
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
        browser = p.chromium.launch()
        for name, path in build(tmp).items():
            short = name.replace('span-', '')
            for width in WIDTHS:
                page = browser.new_page(viewport={'width': width, 'height': 900 if width > 500 else 844}, device_scale_factor=1, is_mobile=width < 700, has_touch=width < 700)
                errors = []
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(path.as_uri() + '?static=1', wait_until='networkidle')
                page.evaluate('document.fonts.ready')
                page.add_style_tag(content='html{scroll-behavior:auto!important}')
                key = '%s@%d' % (short, width)
                r = report[key] = {}
                r['overflow'] = geometry(page)
                form = page.evaluate('(() => { const b = document.getElementById("form").getBoundingClientRect(); return [Math.round(b.top), Math.round(b.bottom), innerHeight]; })()')
                r['form_top_bottom_vh'] = form
                page.screenshot(path=str(OUT / ('%s-hero-%d.png' % (short, width))))
                contrast = page.evaluate(CONTRAST, '.hero,.bar,.closer')
                r['contrast_min'] = min(contrast, key=lambda c: c['ratio'])
                r['contrast_nodes'] = len(contrast)
                r['contrast_fails'] = [c for c in contrast if c['ratio'] < 4.5]
                # FAQ: open the second item and shoot the section
                page.locator('#accb2').click()
                page.wait_for_timeout(400)
                r['faq_open'] = page.evaluate('[...document.querySelectorAll(".acc__btn")].map(b => b.getAttribute("aria-expanded"))')
                page.locator('#how').screenshot(path=str(OUT / ('%s-faq-%d.png' % (short, width))))
                page.locator('#start').scroll_into_view_if_needed()
                page.wait_for_timeout(450)
                page.locator('#start').screenshot(path=str(OUT / ('%s-closer-%d.png' % (short, width))))
                r['sticky_visible_after_hero'] = page.evaluate('(() => { const s = document.getElementById("sticky"); const c = getComputedStyle(s); return c.display !== "none" && c.visibility === "visible"; })()')
                r['sticky_height'] = page.evaluate('Math.round(document.getElementById("sticky").getBoundingClientRect().height)')
                r['band'] = page.locator('.band').count()
                r['disabled'] = page.evaluate('[...document.querySelectorAll("button,a,input,select")].filter(b => b.disabled).length')
                r['dashes'] = page.evaluate('(document.body.innerText.match(/[\\u2013\\u2014]/g) || []).length')
                r['flat_hits'] = flat_sweep(page)  # opens every FAQ panel, so run after the shots above
                if width == 1440:
                    for n in (3, 4):  # FAQ 03 funnel and 04 record, the round 2 review panels
                        page.locator('#accb%d' % n).click()
                        page.wait_for_timeout(450)
                        page.locator('#how').screenshot(path=str(OUT / ('%s-faq%02d-%d.png' % (short, n, width))))
                r['console_errors'] = errors
                page.close()
                check = [
                    (not r['overflow'], 'no horizontal overflow'),
                    (not r['contrast_fails'], 'hero, header and closer text >= 4.5:1'),
                    (r['faq_open'][1] == 'true' and r['faq_open'].count('true') == 1, 'one FAQ panel open'),
                    (r['sticky_visible_after_hero'] == (width < 1024), 'sticky CTA only below 1024'),
                    (r['band'] == (1 if short == 'peo-eor' else 0), 'stat band only with counts'),
                    (not r['console_errors'], 'console clean'),
                    (r['dashes'] == 0, 'zero dashes'),
                    (not r['flat_hits'], 'no gradients or empty bars outside .ot-*, every FAQ panel opened'),
                ]
                if width == 1440:
                    check.append((form[0] >= 0 and form[1] <= form[2], 'form card fully above the fold'))
                for ok, label in check:
                    print('PASS' if ok else 'FAIL', key, label)
                    if not ok:
                        failures.append((key, label))
        browser.close()
    (OUT / 'v2_check.json').write_text(json.dumps(report, indent=1))
    print('report', OUT / 'v2_check.json', 'failures', len(failures))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
