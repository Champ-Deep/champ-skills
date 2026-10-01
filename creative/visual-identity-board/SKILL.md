---
name: visual-identity-board
description: "Use when building a visual ID, brand board or logo system."
---

# Visual identity board

Triggers: visual identity, brand board, visual ID, logo system, mascot set,
wordmark set, brand guidelines board, identity system, design system board.

Produce the artifact, not a description of it. A board delivered as prose is a
rejected deliverable. Every mark on it must render, and you must look at the
render before claiming it works.

## The system idea that makes it stick

One origin, one language, many sizes. Pick a real source of truth, derive a
primitive from it, then express everything in that primitive. An icon set that
shares a dot pitch, stroke weight and corner treatment with the primary mark
reads as a system. Nine unrelated glyphs read as a collection.

On deependhq the origin was a traced Muybridge gallop, so the mark is a dot grid
and every icon is that grid at 16 cells instead of 204. When the set was authored
as unrelated icons it looked stock. Derived, it looked owned.

## Panel order that works

1. **Primary marks.** At least three sizes of one idea: the full form, a cropped
   seal for favicon and sticker, and a badge or avatar form. The crop is the
   proof the system scales, so do it for real.
2. **Word marks.** One per register, not one per style. Terminal, editorial and
   tracked covers nav, print and machine surfaces. Name where each is used.
3. **Mascot icon set.** Six to ten, each labelled with the thing it means, not a
   generic name.
4. **Type.** Every face with its role and its prohibition. Say what each one may
   never be used for, that is where a system stops being decorative.
5. **Taglines.** One per register: primary, editorial voice, operator voice,
   derived.
6. **Palette.** The locked values with their meaning attached. A swatch without a
   meaning is inventory, not identity.

## Build it where you can see it

Headless Chrome is the cheapest way to actually look at what you built:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --screenshot=out.png --window-size=1340,3000 --virtual-time-budget=8000 page.html
```

Then inspect it with `vision_analyze` and fix what it reports. Do not skip this.
Every board built this way had at least one defect that only the render showed:
a collapsed SVG, an empty badge, an unreadable icon.

Traps that produced real bugs:

- **An inline SVG with `width="100%"` and no height collapses to nothing.** It
  renders as an empty box and looks like a data bug, not a layout bug. Always
  emit an explicit height.
- **A percentage sign inside a `%`-formatted Python string is a format spec.**
  `'width="100%"' % h` raises. Write `'100%%'`.
- **A tall board screenshots truncated** at the window height. Render the long
  page, then re-render a variant with the heavy sections removed to inspect the
  tail at full resolution.
- **Braille is 2 columns by 4 rows per cell.** If you expand a braille frame to
  dot coordinates and size the viewBox with the character count, the silhouette
  falls outside it and renders empty.
- Nested SVG inside a `<g transform>` needs a fixed pixel box, not a percentage
  width, or it draws at zero size.

## Verify before delivering

- Render the board and look at it. Then look again after each fix.
- Compute contrast for every text pair. Never eyeball it. AA is 4.5:1 for body,
  3:1 at 24px or 19px bold.
- Check each icon actually reads as its subject. A dotted rectangle does not read
  as a terminal; it needs the chevron and the cursor. A document needs a folded
  corner. A heatmap needs uneven density or it reads as a bar chart.
- Check for leaked format strings. A Python `%s` that reaches the page is a bug.
- Zero em dashes in the output.

## The judgement that matters

Marks must survive their smallest real use. Test the gallop at 16px before
declaring it a favicon: long speed trails occupy about 40 percent of the width
and smear the silhouette into a streak. The answer is not a redraw, it is a crop
of the same source data. If a mark only works at one size, it is decoration, not
identity.

## Related

`deependhq-design-system` holds the locked tokens and the honesty rule for the
site this board was built for. Apply those tokens verbatim; a board that invents
new values is a different site.