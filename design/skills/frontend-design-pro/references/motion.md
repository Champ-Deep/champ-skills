# Motion

One orchestrated load sequence in the hero, then quiet reveals as the reader scrolls. Motion explains (a bar growing to its value, a line drawing through steps) or it does not ship.

## The house sequence

| Moment | What moves | Timing |
|---|---|---|
| Load, 0 to 150ms | eyebrow fades up | 80ms delay |
| Load, 150 to 900ms | headline words rise one by one (`data-words`) | 70ms stagger, 1000ms each, `cubic-bezier(.16,1,.3,1)` |
| Load, 650 to 1100ms | floating stat cards land at their tilt | 140ms stagger, 1100ms each |
| Load, 900 to 2500ms | card numbers count up | 1600ms ease-out-expo, starting at 900, 1050, 1200ms |
| Scroll | sections rise 28px and fade in when 18% visible | 900ms, per-item `--d` stagger of 120 to 150ms |
| Scroll | bars grow from 0 (`scaleX`) | 1100 to 1300ms, 120 to 250ms stagger |
| Scroll | unit dots fill in a diagonal sweep | 18ms per column plus 22ms per row |
| Scroll | timeline line draws, step dots pop | 1800ms line, dots at 200, 600, 1000, 1400ms |
| Always | scroll progress bar at the top | rAF on scroll |
| Always | stars twinkle | 3.6 to 6.4s loops, CSS only |

Stagger between siblings stays between 60 and 150ms; whole sequences stay under 600ms of total stagger so nothing feels slow. Easing: `cubic-bezier(.16,1,.3,1)` for entrances, `cubic-bezier(.34,1.56,.64,1)` for small springs (rings, arrows), linear only for loops.

## Rules

1. **Motion is opt-in by script.** `core.js` adds `html.motion` only when JS runs, IntersectionObserver exists, reduced motion is off and the URL has no `?static=1`. Hidden start states are written under `.motion` so a page without JS is complete.
2. **Final values live in the HTML.** Count-ups write their end value in markup; JS resets to 0 only in motion mode.
3. **`prefers-reduced-motion: reduce`** removes every animation and transition, and the page renders its end state.
4. **Static export mode.** `?static=1` or `#static` adds `html.static`: no animation, no transitions, progress bar hidden, scroll-spy rail hidden, every reveal in its end state. Use it for PDF and PNG exports and for thumbnails. Artifacts do not receive the query string, so static mode is a local export tool, not a viewer setting.
5. **Animate transform and opacity only.** Width, height and top animate only on small elements (the spy rail).
6. **The one-pager exception.** `executive-one-pager` forbids content parked at opacity 0 waiting on a scroll observer. In one-pagers use transform-only reveals (start at `translateY(12px)`, full opacity) or none.
7. **No ambient motion that pushes content.** Twinkling stars and the conic shine are fine; marquees pause on hover; nothing autoplays sound.

## Export recipe (from `kit/shoot.py`)

1. Load the built HTML with `?static=1` at 1440x900, device scale 2; full-page screenshot is the PNG.
2. Flatten the hero atmosphere before the PDF: hide the hero text, screenshot the hero as a JPEG, set it as the hero background, hide the SVG clouds and stars. This keeps the PDF near 1 to 2MB instead of 20MB of rasterized filters.
3. `page.pdf` with width 1440px and height equal to `scrollHeight`, `print_background`, zero margins, one page.
4. Check the PDF text for dashes with `pdftotext file.pdf - | grep -c` on the two dash characters; it must print 0.
