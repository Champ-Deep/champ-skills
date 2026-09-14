#!/usr/bin/env python3
"""
audit.py - Deterministic interface audit. Runs a live page in Chromium and
checks the rendered DOM and computed styles against machine-checkable rules.

This catches the class of defect a screenshot cannot: contrast maths, tap-target
geometry, animated layout properties, missing accessible names, horizontal
overflow. It does NOT judge taste. Pair it with the screenshot critique.

Usage:
    python3 audit.py <url-or-path> [--width 1440] [--theme light] [--json out.json]
    python3 audit.py ./index.html --width 390 --theme dark

Exit code is 1 if any FAIL-severity rule trips, so it can gate a build.
"""

import argparse
import json
import pathlib
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("pip install playwright --break-system-packages")

# --------------------------------------------------------------------------
# The audit runs in-page. Everything below the fence is browser JavaScript.
# --------------------------------------------------------------------------
PROBE = r"""
() => {
  const out = [];
  const add = (sev, rule, msg, el) => {
    let where = '';
    if (el && el.tagName) {
      where = el.tagName.toLowerCase();
      if (el.id) where += '#' + el.id;
      else if (el.className && typeof el.className === 'string')
        where += '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.');
      const t = (el.innerText || el.value || '').trim().replace(/\s+/g, ' ');
      if (t) where += ' "' + t.slice(0, 44) + '"';
    }
    out.push({ severity: sev, rule, message: msg, where });
  };

  const vis = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0.05;
  };
  const all = [...document.querySelectorAll('*')].filter(vis);

  // ---------- colour maths ----------
  const parse = (c) => {
    const m = (c || '').match(/[\d.]+/g);
    if (!m) return null;
    return { r: +m[0], g: +m[1], b: +m[2], a: m[3] === undefined ? 1 : +m[3] };
  };
  const over = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a),
    g: fg.g * fg.a + bg.g * (1 - fg.a),
    b: fg.b * fg.a + bg.b * (1 - fg.a),
    a: 1,
  });
  const lum = (c) => {
    const f = (v) => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  };
  const ratio = (a, b) => {
    const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m);
    return (x + 0.05) / (y + 0.05);
  };
  const effBg = (el) => {
    let node = el, acc = null;
    while (node && node !== document.documentElement.parentNode) {
      const c = parse(getComputedStyle(node).backgroundColor);
      if (c && c.a > 0) {
        acc = acc ? over(acc, c) : c;
        if (acc.a >= 0.999) return acc;
      }
      node = node.parentElement;
    }
    return acc && acc.a >= 0.999 ? acc : { r: 255, g: 255, b: 255, a: 1 };
  };

  // ---------- 1. text contrast ----------
  let contrastChecked = 0;
  for (const el of all) {
    if (contrastChecked > 900) break;
    const direct = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!direct) continue;
    const s = getComputedStyle(el);
    const fg = parse(s.color);
    if (!fg) continue;
    const bg = effBg(el);
    const r = ratio(over(fg, bg), bg);
    const px = parseFloat(s.fontSize);
    const bold = parseInt(s.fontWeight, 10) >= 700;
    const large = px >= 24 || (px >= 18.66 && bold);
    const need = large ? 3 : 4.5;
    contrastChecked++;
    if (r < need)
      add('FAIL', 'contrast',
        `${r.toFixed(2)}:1 against its actual background, needs ${need}:1 (${px}px${bold ? ' bold' : ''})`, el);
  }

  // ---------- 2. tap targets ----------
  const mobile = innerWidth < 700;
  const floor = mobile ? 44 : 24;
  const interactive = all.filter(el =>
    /^(a|button|select|summary)$/i.test(el.tagName) ||
    (el.tagName === 'INPUT' && !/hidden/i.test(el.type)) ||
    ['button', 'link', 'checkbox', 'radio', 'switch', 'tab'].includes(el.getAttribute('role')));
  for (const el of interactive) {
    const r = el.getBoundingClientRect();
    // inline links inside a paragraph are exempt
    const inFlow = el.tagName === 'A' && getComputedStyle(el).display === 'inline' &&
                   el.parentElement && /^(p|li|span|td|figcaption)$/i.test(el.parentElement.tagName);
    if (inFlow) continue;
    if (r.height < floor || r.width < floor)
      add(mobile ? 'FAIL' : 'WARN', 'tap-target',
        `${Math.round(r.width)}x${Math.round(r.height)}px, minimum is ${floor}px`, el);
  }

  // ---------- 3. accessible names ----------
  const named = (el) =>
    (el.getAttribute('aria-label') || '').trim() ||
    (el.getAttribute('title') || '').trim() ||
    (el.innerText || '').trim() ||
    (el.getAttribute('aria-labelledby') &&
      document.getElementById(el.getAttribute('aria-labelledby'))?.innerText.trim());
  for (const el of interactive) {
    if (el.tagName === 'INPUT' && !/^(button|submit|reset|image)$/i.test(el.type)) continue;
    if (!named(el)) add('FAIL', 'a11y-name', 'interactive element has no accessible name', el);
  }
  for (const img of document.querySelectorAll('img')) {
    if (!img.hasAttribute('alt')) add('FAIL', 'a11y-name', 'img has no alt attribute', img);
    if (!img.getAttribute('width') && !getComputedStyle(img).aspectRatio.includes('/'))
      add('WARN', 'cls', 'img has no intrinsic dimensions, will shift layout', img);
  }

  // ---------- 4. form labelling ----------
  for (const inp of document.querySelectorAll('input, textarea, select')) {
    if (/hidden|submit|button|reset/i.test(inp.type || '')) continue;
    const lab = inp.labels?.length || inp.getAttribute('aria-label') ||
                inp.getAttribute('aria-labelledby');
    if (!lab) {
      if (inp.getAttribute('placeholder'))
        add('FAIL', 'placeholder-as-label',
          'placeholder is standing in for a label; a placeholder disappears on focus', inp);
      else add('FAIL', 'a11y-name', 'form control has no label', inp);
    }
    if (mobile && parseFloat(getComputedStyle(inp).fontSize) < 16)
      add('FAIL', 'ios-zoom', 'input font-size below 16px triggers zoom-on-focus in iOS Safari', inp);
  }

  // ---------- 5. focus visibility ----------
  for (const el of interactive.slice(0, 200)) {
    const s = getComputedStyle(el);
    if ((s.outlineStyle === 'none' || s.outlineWidth === '0px')) {
      // look for any :focus-visible rule mentioning this element's tag
      const hasRule = [...document.styleSheets].some(sh => {
        try { return [...sh.cssRules].some(r => (r.selectorText || '').includes(':focus-visible')); }
        catch { return false; }
      });
      if (!hasRule) {
        add('FAIL', 'focus-ring', 'no visible focus indicator anywhere in the stylesheet', el);
        break;
      }
      break;
    }
  }

  // ---------- 6. motion ----------
  for (const el of all.slice(0, 700)) {
    const s = getComputedStyle(el);
    const props = s.transitionProperty;
    const dur = s.transitionDuration.split(',').map(parseFloat).reduce((a, b) => Math.max(a, b), 0);
    if (dur <= 0) continue;
    if (props === 'all')
      add('WARN', 'transition-all', 'transition: all animates unknown properties; list them', el);
    const bad = ['top', 'left', 'right', 'bottom', 'width', 'height', 'margin', 'padding'];
    for (const p of props.split(',').map(x => x.trim())) {
      if (bad.includes(p))
        add('FAIL', 'layout-animation',
          `animating "${p}" forces layout every frame; use transform or opacity`, el);
    }
  }
  let motionRule = false;
  for (const sh of document.styleSheets) {
    try {
      for (const r of sh.cssRules)
        if (r.media && r.media.mediaText.includes('prefers-reduced-motion')) motionRule = true;
    } catch {}
  }
  const animated = all.some(el => {
    const s = getComputedStyle(el);
    return s.animationName !== 'none' || parseFloat(s.transitionDuration) > 0;
  });
  if (animated && !motionRule)
    add('FAIL', 'reduced-motion', 'page animates but never honours prefers-reduced-motion', null);

  // ---------- 7. layout integrity ----------
  const de = document.documentElement;
  if (de.scrollWidth > de.clientWidth + 2) {
    const culprit = all.find(el => {
      const r = el.getBoundingClientRect();
      return r.right > de.clientWidth + 2 && r.width > 20;
    });
    add('FAIL', 'overflow',
      `page scrolls horizontally: ${de.scrollWidth}px content in a ${de.clientWidth}px viewport`, culprit);
  }
  for (const el of all) {
    const s = getComputedStyle(el);
    if (s.display === 'flex' || s.display === 'inline-flex') {
      for (const kid of el.children) {
        const ks = getComputedStyle(kid);
        if (ks.minWidth === 'auto' && kid.scrollWidth > kid.clientWidth + 2)
          add('WARN', 'flex-truncation',
            'flex child overflows; it needs min-width: 0 to allow truncation', kid);
      }
    }
  }

  // ---------- 8. document semantics ----------
  if (!document.title.trim()) add('FAIL', 'title', 'document has no <title>', null);
  const h1s = document.querySelectorAll('h1');
  if (h1s.length === 0) add('FAIL', 'heading', 'no <h1> on the page', null);
  if (h1s.length > 1) add('WARN', 'heading', `${h1s.length} <h1> elements; there should be one`, null);
  let last = 0;
  for (const h of document.querySelectorAll('h1,h2,h3,h4,h5,h6')) {
    const lvl = +h.tagName[1];
    if (last && lvl > last + 1)
      add('WARN', 'heading', `heading jumps h${last} to h${lvl}, skipping a level`, h);
    last = lvl;
  }
  const vp = document.querySelector('meta[name="viewport"]')?.content || '';
  if (/user-scalable\s*=\s*no|maximum-scale\s*=\s*1(\D|$)/.test(vp))
    add('FAIL', 'zoom-blocked', 'viewport meta disables pinch zoom', null);
  if (!document.querySelector('a[href^="#"]')?.innerText.match(/skip/i))
    add('INFO', 'skip-link', 'no "skip to content" link found', null);

  // ---------- 9. AI-slop tells ----------
  const chrome = [...document.querySelectorAll('nav, header, button, [role=button], h1, h2, h3, aside, .sidebar')];
  const emoji = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/u;
  for (const el of chrome)
    if (emoji.test(el.innerText || ''))
      add('WARN', 'emoji-as-icon', 'emoji used in interface chrome; use one SVG icon family', el);

  for (const el of all.slice(0, 700)) {
    const s = getComputedStyle(el);
    for (const side of ['Left', 'Right']) {
      const w = parseFloat(s['border' + side + 'Width']);
      const c = parse(s['border' + side + 'Color']);
      const other = parseFloat(s['border' + (side === 'Left' ? 'Right' : 'Left') + 'Width']);
      if (w >= 3 && other === 0 && c && c.a > 0.3 &&
          !(c.r === c.g && c.g === c.b))
        add('WARN', 'side-stripe',
          'coloured side-border stripe: the most recognisable AI-dashboard tell', el);
    }
    if (s.webkitBackgroundClip === 'text' || s.backgroundClip === 'text')
      add('WARN', 'gradient-text', 'gradient clipped to text; use weight and size for emphasis', el);
    if (s.backdropFilter && s.backdropFilter !== 'none') {
      if (!['fixed', 'sticky'].includes(s.position))
        add('WARN', 'static-glass',
          'frosted glass on an element that never floats over scrolling content', el);
    }
  }
  const glass = all.filter(el => {
    const f = getComputedStyle(el).backdropFilter;
    return f && f !== 'none';
  });
  if (glass.length > 2)
    add('WARN', 'glass-count', `${glass.length} blurred surfaces; cap at two per screen`, null);

  const bodyFont = getComputedStyle(document.body).fontFamily.toLowerCase();
  for (const f of ['inter', 'roboto', 'open sans', 'lato', 'montserrat', 'arial', 'poppins'])
    if (bodyFont.includes(f))
      add('WARN', 'default-font', `body font is "${f}", an AI default; choose deliberately`, null);

  const bodyBg = getComputedStyle(document.body).backgroundColor;
  if (['rgb(255, 255, 255)', 'rgb(0, 0, 0)'].includes(bodyBg))
    add('INFO', 'pure-bw', `page surface is pure ${bodyBg}; tint it toward the brand hue`, null);

  // three identical cards in a row
  const parents = new Set(all.map(el => el.parentElement).filter(Boolean));
  for (const p of parents) {
    // an ordered sequence is the recommended alternative to a card grid, not the tell
    if (p.tagName === 'OL' || p.closest('ol')) continue;
    const kids = [...p.children].filter(vis);
    if (kids.length !== 3) continue;
    if (kids.some(k => k.tagName === 'LI' && getComputedStyle(k).counterIncrement !== 'none')) continue;
    const sig = (el) => el.tagName + '|' + [...el.querySelectorAll('*')].map(x => x.tagName).join(',');
    const sigs = kids.map(sig);
    if (sigs[0] === sigs[1] && sigs[1] === sigs[2] && kids[0].querySelectorAll('*').length > 2) {
      const s = getComputedStyle(p);
      if (s.display.includes('grid') || s.display.includes('flex'))
        add('INFO', 'three-card-row',
          'three structurally identical cards in a row: the default AI layout', p);
    }
  }

  const text = document.body.innerText || '';
  const dashes = (text.match(/—/g) || []).length;
  if (dashes > 0)
    add('INFO', 'em-dash', `${dashes} em-dash(es) in copy; a recognisable generated-text tell`, null);
  if (/\b(99\.9{1,2}%|10x|100x|\+\d{2,3}%)\b/.test(text))
    add('INFO', 'fake-precision',
      'suspiciously precise or round marketing metric; back it with data or cut it', null);
  for (const n of ['Jane Doe', 'John Doe', 'Acme Inc', 'Lorem ipsum'])
    if (text.includes(n)) add('WARN', 'placeholder-content', `placeholder content left in: "${n}"`, null);

  // measure
  for (const el of all) {
    const direct = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 120);
    if (!direct) continue;
    const s = getComputedStyle(el);
    const ch = el.getBoundingClientRect().width / (parseFloat(s.fontSize) * 0.5);
    if (ch > 90)
      add('WARN', 'measure', `line length about ${Math.round(ch)} characters; cap body text near 65`, el);
    if (parseFloat(s.lineHeight) / parseFloat(s.fontSize) < 1.35)
      add('WARN', 'leading', 'body line-height below 1.35 is cramped', el);
  }

  // duplicate CTA intent
  const ctas = [...document.querySelectorAll('a,button')]
    .map(el => (el.innerText || '').trim().toLowerCase()).filter(t => t && t.length < 30);
  const seen = {};
  for (const t of ctas) { seen[t] = (seen[t] || 0) + 1; }
  for (const [t, n] of Object.entries(seen))
    if (n > 3) add('INFO', 'cta-repetition', `"${t}" appears ${n} times`, null);

  return out;
}
"""

SEV_ORDER = {"FAIL": 0, "WARN": 1, "INFO": 2}


def to_url(target: str) -> str:
    if target.startswith(("http://", "https://", "file://", "data:")):
        return target
    p = pathlib.Path(target).expanduser().resolve()
    if not p.exists():
        sys.exit(f"No such file: {p}")
    return p.as_uri()


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic interface audit.")
    ap.add_argument("target")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--theme", default="light", choices=["light", "dark"])
    ap.add_argument("--wait", type=int, default=800)
    ap.add_argument("--json", default=None, help="also write findings to this JSON file")
    ap.add_argument("--quiet-info", action="store_true", help="hide INFO findings")
    args = ap.parse_args()

    url = to_url(args.target)
    height = {390: 844, 834: 1112}.get(args.width, 900)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": args.width, "height": height},
            color_scheme=args.theme,
            is_mobile=args.width < 700,
            has_touch=args.width < 700,
        )
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:
            page.goto(url, wait_until="load", timeout=30000)
        page.wait_for_timeout(args.wait)
        findings = page.evaluate(PROBE)
        browser.close()

    # dedupe: same rule + same message collapses, keeping a count
    bucket = {}
    for f in findings:
        key = (f["rule"], f["message"])
        bucket.setdefault(key, {"f": f, "n": 0, "where": []})
        bucket[key]["n"] += 1
        if f["where"]:
            bucket[key]["where"].append(f["where"])
    rows = sorted(bucket.values(),
                  key=lambda b: (SEV_ORDER[b["f"]["severity"]], b["f"]["rule"]))

    counts = {"FAIL": 0, "WARN": 0, "INFO": 0}
    print(f"\n  Interface audit  {url}")
    print(f"  {args.width}px  {args.theme} theme\n")
    for b in rows:
        sev = b["f"]["severity"]
        counts[sev] += b["n"]
        if sev == "INFO" and args.quiet_info:
            continue
        tail = f"  (x{b['n']})" if b["n"] > 1 else ""
        print(f"  [{sev}] {b['f']['rule']}: {b['f']['message']}{tail}")
        for w in b["where"][:3]:
            print(f"         -> {w}")
    if not rows:
        print("  No machine-checkable violations. Now judge the screenshots.")

    print(f"\n  {counts['FAIL']} fail   {counts['WARN']} warn   {counts['INFO']} info")
    print("  A clean audit is necessary, not sufficient. Look at the screenshots.\n")

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(findings, indent=2))

    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
