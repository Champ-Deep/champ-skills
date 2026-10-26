# Third-party sources

The template uses vanilla ports inspired by the 21st.dev patterns below. It drops React, Tailwind, framer-motion and icon runtime dependencies. The Compare slider is historical and no longer rendered. Attribution records provenance; it does not establish an upstream license. Check the original component rights before redistributing the ports.

| Component | Source | Where in template.html |
|---|---|---|
| Compare (Aceternity UI) | 21st.dev, `compare.tsx` | Historical source for the removed cropping slider. Replaced by separate adjustable bento boards; no `.cmp` slider renders. |
| AI Sources | 21st.dev, `ai-sources.tsx` | `.srcs` favicon stack and expanding source rows in the hero and the account section |
| Halftone Wordmark Footer | 21st.dev, `halftone-wordmark-footer.tsx` | `.hwf` footer canvas: coverage-sized dots, pointer springs, click ring, print grain |

Favicons in the sources stack are fetched from Google's favicon service at runtime; a neutral globe is drawn when one fails. Fonts are Google Fonts (Montserrat, Inter).

## Draggable Widget Grid (21st.dev), via the deependhq island port
- Upstream: the 21st.dev "Draggable Widget Grid" component, first ported for deependhq.com as `islands/widget-grid.island.jsx` (React plus `motion/react`).
- Here: `template.html`, the `/* ---- Bento ---- */` script and `.wg*` styles. The exact-tiling layout (`tile`, `pack`, `canonical`, `candidatesFor`, `choose`), the 40ms settle, 350ms long press with 8px slop, 1.015 lift scale, 620ms landed ring and Alt plus arrow keyboard reorder are ported one to one. Dragging is pointer events plus an inline transform instead of `motion`, and React state is a plain `order` array of tile ids.
- Omitted: React, `motion`, localStorage persistence of the order (a landing page resets on every visit).

## Dither Grid gradient (21st.dev community gradients)
- Upstream: the operator-supplied gradient spec (palette Pine, Moss, Fern, Sprout; pixel mode, 25x15 cells, 62deg, dither 76, gap 7, speed 71, motion 60). Rebuilt on canvas in `template.html` rather than the CSS radial approximation. Grain and vignette layers omitted; the wash over the canvas replaces the vignette.
