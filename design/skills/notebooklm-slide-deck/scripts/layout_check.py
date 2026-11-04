# Layout gate for slide-format HTML (one <section class="page"> per slide).
# Fails on: text over text, text over any svg/img/.deco, text outside its .card, text off the page, text under 13px.
# Usage: python layout_check.py file.html [out_dir_for_pdf_and_pngs]
import sys, pathlib
from playwright.sync_api import sync_playwright

JS = r"""() => {
 const out = [];
 const hit = (a, b) => a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1;
 document.querySelectorAll('section.page').forEach((pg, pi) => {
  const P = pg.getBoundingClientRect(), texts = [];
  const w = document.createTreeWalker(pg, NodeFilter.SHOW_TEXT); let n;
  while ((n = w.nextNode())) {
   if (!n.textContent.trim() || n.parentElement.closest('svg')) continue;
   const r = document.createRange(); r.selectNodeContents(n);
   for (const rc of r.getClientRects()) texts.push({ el: n.parentElement, r: rc, t: n.textContent.trim().slice(0, 28) });
  }
  const gfx = [...pg.querySelectorAll('svg, img, .deco')].map(e => ({ e, r: e.getBoundingClientRect() }));
  texts.forEach((a, i) => {
   const tag = `slide ${pi + 1}: "${a.t}"`;
   if (a.r.left < P.left || a.r.right > P.right || a.r.top < P.top || a.r.bottom > P.bottom) out.push(`${tag} off the page`);
   texts.slice(i + 1).forEach(b => { if (a.el !== b.el && !a.el.contains(b.el) && !b.el.contains(a.el) && hit(a.r, b.r)) out.push(`${tag} overlaps text "${b.t}"`); });
   gfx.forEach(g => { if (hit(a.r, g.r)) out.push(`${tag} sits on a ${g.e.tagName.toLowerCase()}${g.e.className && g.e.className.baseVal === undefined ? '.' + g.e.className : ''}`); });
   const card = a.el.closest('.card');
   if (card) { const c = card.getBoundingClientRect(); if (a.r.left < c.left || a.r.right > c.right || a.r.top < c.top || a.r.bottom > c.bottom) out.push(`${tag} spills out of its card`); }
   const fs = parseFloat(getComputedStyle(a.el).fontSize); if (fs < 13) out.push(`${tag} is ${fs}px`);
  });
 });
 return [...new Set(out)];
}"""

src = pathlib.Path(sys.argv[1]).resolve()
out_dir = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1376, 'height': 768})
    errs = []; pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(src.as_uri()); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready')
    problems = pg.evaluate(JS)
    print('slides:', pg.evaluate("document.querySelectorAll('section.page').length"), '| console errors:', errs or 0)
    print('PROBLEMS:', len(problems)); [print('  ', p) for p in problems]
    if out_dir and not problems:
        pg.pdf(path=str(out_dir / '04 - LakeB2B Visual Direction.pdf'), width='1376px', height='768px', print_background=True)
        for i, s in enumerate(pg.query_selector_all('section.page'), 1):
            s.screenshot(path=str(out_dir / f'ref-{i:02d}.png'))
        print('rendered PDF and PNGs to', out_dir)
    b.close()
sys.exit(1 if problems else 0)
