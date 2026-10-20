# Scroll motion teardown

## When to Use

A reference site is being cloned or admired for its motion, and you have to capture
that behaviour and rebuild it in a single-file page with the user's own content. Read
this after step 2 of the main skill, before writing any scroll code.

## 1. Capture the reference

A static fetch shows layout, never motion. Render it:

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(url); pg.wait_for_timeout(1200)
    H = pg.evaluate("document.body.scrollHeight - innerHeight")
    for i, f in enumerate([0, .12, .25, .4, .55, .7, .85, 1]):
        pg.evaluate(f"scrollTo(0,{H*f})"); pg.wait_for_timeout(700)
        pg.screenshot(path=f"ref_{i}.png")
    b.close()
```

Tile the frames into a contact sheet (2 columns, resized) and read that one image:
pairs that differ are mechanics. Screenshot at a fixed width so differences come from
scroll, not reflow.

Extract what a source read cannot give you:

```python
# palette + fonts from computed styles (compiled CSS hides brand colours in utility names)
pg.evaluate("""() => { const g = (s, p) => getComputedStyle(document.querySelector(s))[p];
  return {h1: g('h1','fontFamily'), h1c: g('h1','color'),
          body: g('body','backgroundColor'), link: g('a','color')} }""")
# technique fingerprints
pg.evaluate("""() => ({lenis: !!window.Lenis, gsap: !!window.gsap,
  scrollTimeline: CSS.supports('animation-timeline: view()'),
  observers: typeof IntersectionObserver !== 'undefined'})""")
```

## 2. Inventory before rebuilding

Write the list as `trigger -> what moves -> what the user reads out of it`. Anything
you cannot fill in for all three is decoration, not a mechanic, and does not get
rebuilt.

Typical shapes and their trigger:

| Shape | Trigger | Read-back to verify |
|---|---|---|
| Pinned story | section top passes viewport top; progress = `-top / (height - innerHeight)` | progress climbs 0 to 1 across the pin |
| Word-by-word reveal | progress split across token spans | span opacity/colors change in order |
| Isometric or layered stack | per-item progress window | each item's opacity/transform in sequence |
| Active-state tour (lit slab, caption swap) | progress bucketed into N steps | active index changes monotonically |
| Stacking card deck | sticky card index vs scroll | each card's scale/translate, sidebar active pill |
| Line fill | same progress value driving height | fill length grows, nodes light as reached |
| Zoom band | IntersectionObserver threshold or progress | scale moves from <1 to 1 |
| Count-up | entry threshold | value lands on the stated number, not an arbitrary one |

Tie highlight rotation to scroll, not a timer: a timer desynchronises from the reader's
position and fights back when they scroll up.

## 3. Build rules that decide whether it reads as motion

- **One scroll driver per section.** Compute progress once, derive every downstream
  value from it. Multiple competing listeners jitter against each other.
- **Stage wrapper taller than the viewport**, or the progress range is zero and the
  feature silently never fires.
- **Stagger items with a per-item window, not one global fade.** `(p - i/n) * k`
  clamped, so items enter and settle instead of everything fading together.
- **Overlap geometry needs a measured visible band.** For stacked slabs, the vertical
  step minus the skew shift must exceed the header block (label + title + tag) or the
  front slab bisects the back slab's title mid-word. Compute that band on paper before
  choosing offsets.
- **Opaque front faces.** Translucent faces let hidden body text bleed through the
  slab in front and read as corruption. Keep the body copy only on the front-most item
  when the rest are occluded; delete hidden rows rather than letting them show through.
- **Attach extrusion faces to the face's inset, not its full height.** A side face that
  runs the full height pokes past the rounded corners and reads as a detached strip.
  `top: 6px; height: calc(100% - 12px)` with a matching corner radius lines up.
- **The active item's accent must propagate to its extrusion** or the lit slab looks
  flat while its neighbours have depth.
- **`transform: scale()` shrinks hit areas.** A 44px link inside a card scaled to 0.94
  measures 41px on screen and fails the tap-target gate. Pad up before scaling.

## 4. Verify by driving scroll, not by reading source

Same fractions as the capture, on your build, reading values back out of the DOM:

```python
for f in (0, .25, .5, .75, 1):
    pg.evaluate(f"scrollTo(0, start + range*{f})"); pg.wait_for_timeout(400)
    print(pg.evaluate("({p, lit, op: [...slabs].map(s=>s.style.opacity), cap})"))
```

Expect monotonic change. Then run the closing gate: 1440 and 390, zero horizontal
overflow, zero console errors, reduced motion and no-JS both fully static and fully
visible.

## Pitfalls

- **Vision review confirms what you asked it to confirm.** A broad question ("does the
  animation work?") returns a yes. Ask about concrete geometry: which slab is cut,
  which word is bisected, does the side face join without a gap. Crop to the component
  and zoom before asking; defects that decide the layout are invisible at full-page
  scale.
- **Do not trust a first visual pass as final.** Re-review after every geometry change;
  a spacing fix introduces its own clipping.
- **Report the gate failures you leave in.** Known sub-44px targets and content still
  pending from earlier decisions belong in the handoff, not in a follow-up.
