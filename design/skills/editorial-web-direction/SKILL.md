---
name: "editorial-web-direction"
description: "Art-direct personal sites, portfolios and hero sections like a magazine spread: giant type on a visible grid, margin notes, scanline or dot image treatments. Use for any portfolio or hero redesign."
---

# Editorial Web Direction

Make a personal site or portfolio look art-directed. The reference point is the editorial portfolio: the name set huge and spaced across a twelve-column grid, thin guide lines you can see, small notes in the margins, one strong image treatment, and a page that reads like a magazine spread instead of a SaaS template.

Use this skill for the composition. Use the brand skill for colours and type (brand locks are absolute), `identity-kit` for marks, `text-art-eggs` for ASCII and braille art, and run `design-trends` as the last pass.

## The template tells to design away from

Fail the page if the hero is a centred headline, a subtitle, two buttons and an image on the right; if every section is the same card grid; if nothing on the page could only belong to this person; or if motion is a fade-up on everything. These are what "cookie-cutter" means.

## Step 1: Inventory the true material

List what the page can truthfully show before choosing a layout: the person's name and how they say it, their titles, real numbers (derived from data, never typed in), dated work, real clients only if public, quotes in their own words, one strong image or object. A device with nothing true to fill it is decoration. Drop it.

## Step 2: Pick devices

One dominant device for the hero, at most two supporting devices for the rest of the page. Write one sentence per device on what it does for this audience.

| Device | What it is | Build notes |
|---|---|---|
| **Spaced type grid** | The headline in three or four giant rows, words placed in different columns with big gaps, a hairline on every row's x-height and baseline | Below |
| **Margin notes** | Small lowercase notes sitting on the guide lines at the row ends: titles, years, counts | Below |
| **Object between the words** | A cut-out portrait, a product, or an animal drawn in the gaps, overlapping rows and standing on the ground line | Absolute position inside the grid, so it never stretches the rows |
| **Scanline smear** | Horizontal streaks dragged off the subject's back edge, dense near the body and thinning out, with a few torn slices | Below |
| **Ledger** | A track-record table with hairline rules: company, period, role, contribution, impact | Real data only; numbers right-aligned in a mono face |
| **Numbered services** | 01 to 04 as big light numerals, title and two lines in hairline cells | Max two lines of description per cell |
| **Bracketed links** | `( contact me )` in spaced caps instead of buttons | 44px tall hit area |
| **Signature footer** | The name set at full width along the bottom edge, cropped | Size in vw so it always spans |
| **Visible frame** | Outer vertical hairlines and `+` marks where lines cross | Pseudo-elements, never images |

## Step 3: Build the spaced type grid

Measure the display face before drawing guides, because optical sizing changes the x-height. Render "xxxx" at 200px with the real font settings and find the ink rows:

```js
await page.setContent(`<link rel=stylesheet href="${fontsCss}"><h1 style="margin:0;font:800 200px/1 'Fraunces';font-optical-sizing:auto">xxxx</h1>`);
// screenshot, then: first ink row / 200 = x-height top, last ink row + 1 / 200 = baseline (em, at line-height 1)
```

Fraunces 800 measured .41em and .86em. Draw both guides on every row with one gradient on the h1 at `line-height: 1`, so the guides follow the rows at any width and on mobile reflow:

```css
.hx-h{font:800 var(--hx-fs)/1 var(--font-display);
  background:repeating-linear-gradient(180deg,transparent 0 .41em,var(--line) .41em calc(.41em + 1px),
    transparent calc(.41em + 1px) .86em,var(--line) .86em calc(.86em + 1px),transparent calc(.86em + 1px) 1em)}
```

Desktop (64rem and up): the h1 is a grid on the parent's twelve columns (`grid-template-columns: subgrid`, `grid-auto-rows: 1em`), each word is a grid item with a `grid-area`, the last word `justify-self: end`. Mobile: the h1 becomes `display:flex; flex-wrap:wrap; column-gap:.24em`, with empty `<span class="hbr">` elements (`flex-basis:100%`) as forced row breaks, hidden on desktop. Keep the DOM order a readable sentence for screen readers.

Margin notes sit in the same parent grid row as the h1 and line up with the guides by margin, in units of the display size:

```css
.note-r1{grid-row:2;grid-column:1 / 3;margin-top:calc(var(--hx-fs) * .41 + 6px)}
.note-r2{grid-row:2;grid-column:11 / 13;text-align:right;margin-top:calc(var(--hx-fs) * 1.41 + 6px)}
```

Size the display face per breakpoint with a hero-only token (for example `clamp(5rem, 7.3vw, 8.75rem)` on desktop, `11vw` on tablet, `14.6vw` on phones) and check the longest word at 360px wide.

Place the object between the words with `position:absolute` (left and width in percent, bottom pinned to the ground line), so it can never change row heights. Then verify with a collision check: read every word's bounding box with Playwright and make sure the object and the notes clear them.

## Step 4: Image treatments

Pick one per page.

- **Scanline smear.** For a raster cut-out: pick bands of 1 to 3 pixel rows; in each band, from the leftmost subject pixel, extend the edge colour leftwards for a random length, keeping about 97 percent of pixels for the first 55 percent of the run, then thinning to nothing; shift a few bands 2 to 5 pixels sideways as torn slices. For text art, the same algorithm runs on the dot grid (see `text-art-eggs`). Fade the far end with a CSS mask: `mask-image: linear-gradient(90deg, transparent 0, #000 34%)`.
- **Halftone or dot art.** The subject as dots on the brand ground, sized with container units (`font-size: calc(100cqi / (cols * .62))`) so it fills its box at every width.
- **Duotone.** Grayscale the image, map shadows to the ground colour and highlights to the text colour.

Any image of a real person needs that person's photo and permission. Without a photo, use an object or animal from their world instead of a stock face.

## Step 5: Motion signature

Two behaviours, repeated, nothing else. Default pair: words ink in one by one on load (`animation-delay: calc(var(--i) * 70ms)`, colour from dim to text plus a small rise), and the hero object does one short action on load and again on hover, then settles to its rest state. Reduced motion shows the rest state with no movement. No scroll listeners: use CSS scroll timelines or IntersectionObserver.

## Step 6: Live in the real page

- **Static first.** The hero must render complete with JavaScript off (prerender or plain HTML). Scripts only add motion.
- **Floating widgets.** Chat bubbles and cookie cards sit bottom right. Keep that corner free of anything important, and pad the footer by the widget's measured height.
- **Honesty.** Every number on the page is derived at build time; every date shows its age.

## Step 7: Verify

Screenshot at 375, 768, 1280, 1440 and 1600; zero horizontal scroll; no word collisions; guides on the measured lines; notes not touching words; the hero with JavaScript off; the hero with reduced motion; text contrast 4.5:1. Look at each screenshot before claiming it works, and fix what you see.

## Guardrails

- No em dashes or en dashes in copy, code comments or notes.
- Brand locks win. If the brand is dark-only, the composition moves to dark; it does not bring a light mode with it.
- Never copy a reference's copy, photos or exact layout: take the device and its intent, make the surface from the person's own material.