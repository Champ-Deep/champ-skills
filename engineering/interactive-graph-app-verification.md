---
name: interactive-graph-app-verification
description: Reusable Playwright checker for self-contained HTML data apps (graphs, treemaps, queues); measure the DOM instead of trusting screenshots.
---

# Verifying an interactive data app

A screenshot tells you something is wrong; only the DOM tells you what. Write a checker that
drives the real interactions and asserts on geometry, then read the screenshots for aesthetics.

## What the checker must assert

**Structure** — item counts actually rendered, not just present in the payload. A treemap that
"draws 154 tiles" may be laying out 12. Assert against the DOM.

**Geometry** — overlaps, out-of-bounds, degenerate sizes, both for nodes and for the *contents*
of nodes. Text badges sitting over labels passed a node-only overlap check.

**Interaction** — every toggle must change the thing it claims to. A filter that silently returns
everything looks identical to a working one unless you count rows before and after.

**Text direction** — CSS `direction:rtl` with `text-overflow:ellipsis` truncates the *front* of a
slug, which is exactly the identifying part. Assert the first characters are visible.

**Persistence** — if state is saved, assert it was written, then reset it so the next run starts
clean.

## Traps that cost real time

- Console errors: dedupe by prefix. One NaN coordinate produced ~900 identical SVG attribute
  errors and 955 KB of output that buried the real result.
- Text overlap tests must use real glyph bounds, not estimated box widths. A family header
  reserved 136 px and rendered 40 px, so a neighbour slipped into the gap and the sweep passed.
- Zero technical overlap is not the same as legible. Measure the minimum gap between boxes; 0.8 px
  apart reads as a collision to anyone looking at it. Target 2px+ unzoomed.
- A vision model reporting "labels overlap" when the DOM says zero is a signal your text is merely
  *tight*. Check the min-gap metric before dismissing it.
- Algorithmic layout (squarified treemap, force graphs) must be unit-tested standalone in Python
  first. Debugging it through a browser is far slower and misleads you into blaming the CSS.

## Guarding the CSS

A checker written once is not a fix. Assert the specific regression (badge/name collision, legend
occlusion, header overlap) so the defect cannot come back silently.

Then run the contrast audit at 1440, 1024 **and** 390. Mobile surfaces its own class of defect:
sub-44px tap targets and iOS zooming on inputs under 16px. Add `:focus-visible` rings and a
`prefers-reduced-motion` block; both are audited. Choose tile text colour from the computed
background luminance rather than a width heuristic, and make the colour-blend helper accept
`rgb()` as well as hex or it will silently emit `NaN`.

Used on [[span-interlink-architecture]].
