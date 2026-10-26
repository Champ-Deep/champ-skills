# Mobile & speed pass

## Screenshot everything
Take full-page screenshots at 1440px and 390px wide (headless Chrome, Playwright, or the gstack `/browse` skill). Slice the long page into screen-height pieces and look at every one. Also measure `document.documentElement.scrollWidth` at 390px, it must equal 390 (anything wider is horizontal scroll; find the element whose right edge passes the viewport, ignoring clipped marquees).

## Scroll it, frame by frame
Static screenshots miss what breaks while scrolling. Scroll each page top to bottom in steps of ~300px at 1440 and 390, screenshotting every step (or record a video and pull frames). Look for: hard cuts between sections (a colour band that ends in a straight line), elements overlapping, sticky things covering content, marquees that run out and leave a gap on wide screens (test 1920 and 2560 too), and anything at `opacity: 0` in a still frame.

## Phone checklist (390px)
- No horizontal scroll.
- Body text ≥ 15px; headlines don't break into one word per line.
- Tap targets ≥ 44px (buttons, menu items, footer links, FAQ toggles).
- Primary CTA visible in the first screen or pinned in the nav; the live action (call / demo) is in the mobile menu.
- Logos legible: in cards, let logo grids span the full card width on phones instead of squeezing beside an icon.
- Two-column grids collapse to one column; asymmetric layouts fall back to a single column.
- Flow diagrams stack vertically; arrows rotate to point down.
- Nothing overlaps: sticky nav doesn't cover anchors (`scroll-margin-top`).
- Images and video don't letterbox awkwardly; burned-in video subtitles aren't covered by overlay labels.

## Speed checklist
- Logo mark and favicon: small PNG/SVG (an SVG that embeds a big raster is not small, render it to a PNG at 2× display size).
- Logos and photos sized for their slot; strip padding; keep transparency when resizing (`format=rgba`).
- `loading="lazy"` on everything below the first screen.
- Video: click-to-load (thumbnail + play button → iframe), or `preload="none"` loops with a poster.
- Fonts: one family + one mono, `display=swap`, preconnect.
- Remove unused files from `public/` (keep originals in `_brand/`).
- Production build has no errors or warnings that matter; note the gzipped JS/CSS sizes.

## Before handing back
- Desktop and phone screenshots of every section after the fixes.
- Console has no errors.
- Every link and button goes somewhere real (CTA destination, tel: links, login).
