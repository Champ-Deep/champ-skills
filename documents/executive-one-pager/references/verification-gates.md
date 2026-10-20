# Verification gates: render, budget, contrast

Run these inside the Phase 6 Playwright session (`measure.py` in the vault copy). Pass
conditions live in SKILL.md; this file is the code and the levers.

## Browser fallback

If Playwright's bundled browser is not installed but Chrome is, launch with
`p.chromium.launch(channel="chrome")`. The gate exists to check the page, not the browser
install, so do not stop and ask.

## Section heights, when the render is over budget

```python
print(pg.evaluate("""() => [...document.querySelectorAll('.page > *')].map(e =>
  (e.tagName + '.' + (e.className || '')) + ' = ' + Math.round(e.getBoundingClientRect().height))"""))
```

Trim the tallest block, re-run, repeat, until the page sits at least 100px under budget at
both viewports. Budgets: 3,000px at 1440, 6,500px at 390.

## Contrast audit, with the opacity trap

Walk each sampled element's ancestors to the first opaque background, blend the stack, then
compare against the WCAG threshold for that element's size and weight.

```js
() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(parseFloat); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; };
  const over = (fg,bg) => ({r:fg.r*fg.a+bg.r*(1-fg.a), g:fg.g*fg.a+bg.g*(1-fg.a),
                            b:fg.b*fg.a+bg.b*(1-fg.a), a:1});
  const bgOf = el => { const s = []; let n = el;
    while (n) { const c = parse(getComputedStyle(n).backgroundColor); if (c && c.a > 0) s.push(c);
      n = n.parentElement; }
    let acc = {r:255,g:255,b:255,a:1};
    for (let i = s.length - 1; i >= 0; i--) acc = over(s[i], acc); return acc; };
  const lum = c => { const f = v => { v /= 255;
    return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
  const ratio = (a,b) => { const la = lum(a), lb = lum(b);
    return (Math.max(la,lb) + .05) / (Math.min(la,lb) + .05); };
  return ['.desk .kicker','.desk h2','.slots .t','.slots .mono','.q .qt','.q .qw','.badge',
          '.close','.branch p','footer p']
    .map(s => { const el = document.querySelector(s); if (!el) return {s, missing:true};
      const cs = getComputedStyle(el), size = parseFloat(cs.fontSize), w = parseInt(cs.fontWeight) || 400;
      const bg = bgOf(el), fg = over(parse(cs.color), bg);
      const need = (size >= 24 || (size >= 18.66 && w >= 700)) ? 3 : 4.5;
      const r = ratio(fg, bg);
      return {s, size, r: Math.round(r * 100) / 100, need, pass: r >= need}; });
}
```

Two traps the snippet exists to catch:

- `getComputedStyle(el).color` returns the declared colour and drops the element's own
  `opacity`. Text set to opacity below 1 to recede on the accent panel reads as passing while
  rendering under 4.5:1. Fold the opacity into the foreground before comparing, or drop the
  opacity and use a darker token.
- Inside a solid accent block with ink text, tinting the inset with ink (a small
  `rgba(26,26,26,.x)` overlay) makes the dark-on-dark row worse. Tint with white instead,
  which lifts the same row well past 4.5:1. This holds for any dark text on a light-ish
  accent, not just the Champions orange.

Sample every class you ship: panel text, inset rows, badges, mono labels, muted captions,
footer. One failing row fails the page.

## Trim levers, cheapest first

1. Assertion headline `max-width` from about 36ch to 44ch: three lines become two at 1440,
   and mobile does not move, so it never costs the fold.
2. Sub-line under about 82 characters: one line instead of two.
3. Match column count to item count. Three cards in two columns leave an empty cell; five in
   three leave one. Fill a trailing cell with a note card whose class the claim audit does
   not count, so headline totals stay true.
4. Sentence case in mono footers and labels: uppercase mono wraps to more lines at the same
   size and reads slower.
5. Row padding and section margins last. They cost legibility and buy the least.

## Badges and markers

- A badge trailing prose inside a paragraph wraps at an arbitrary point and crowds the line
  above. Make it `display:block; width:fit-content` with its own margin so it starts a clean
  line.
- Marker shapes carry meaning and colour only confirms. Ship a small legend card beside the
  markers so a phone reader can decode the page without the desktop context.

## Fold

`data-fold` goes on the headline, each of the three numbers, and the first ask heading; the
gate asserts each has `bottom <= innerHeight` at 390. Put the marker on the shortest copy
that still carries the claim. When the fold fails, the fix is usually shortening that
heading, not relocating the numbers.