---
name: "social-grid-design"
description: "Use when designing an Instagram or social profile grid."
---

# Social grid design

Triggers: Instagram grid, feed grid, feed tiles, profile redesign, avatar and
highlight covers, "make the profile look like this reference".

The deliverable is a set of exportable image files plus a preview of the profile as
it will actually read, never a description of either. Nothing gets posted: stage the
files, show the preview, and name what needs approval.

## Step 1. Fix the design language from real sources, not from the reference alone

A reference image (a competitor grid, a moodboard) sets composition and rhythm. The
brand's own files set the values.

1. **Palette:** sample the accent from the brand's logo or source art at full size.
   Colour picked off a downscaled screenshot or a compressed reference is the
   compressor's hue, not the brand's.
2. **Type:** read the family off the brand's live site (computed `font-family` in its
   CSS) so grid and site match. Keep the site's division of labour: a tracked sans in
   caps for overlay labels, a serif for statement tiles, never the reverse.
   Match the reference's weight, not just its role: a luxury-wellness reference sets overlays in light (300 to 400) caps at about 4% of tile width with about 0.3em tracking, no scrim, no accent line. Bold 600 caps with a scrim read as a different brand even with the right font family. Zoom the reference and measure weight, tracking and size before building.
3. **One signature:** pick a single repeated ornament (a short hairline above every
   label, one fixed inset, one small-caps size) and use it on every tile. One
   signature in three positions reads as a system; three ornaments read as three
   designers.
4. **Claims:** every number, label and tagline on a tile comes from the brand's own
   site or approved copy. No invented stats, no borrowed superlatives.
5. If the brand has a brand skill (`champions-group-brand`, `lakeb2b-brand-guidelines`,
   `span-brand-guidelines`, `ampliz-brand-guidelines`, `metricfox-brand-guidelines`,
   `ab7-brand-guidelines`, `deependhq-design-system`), its tokens override anything
   derived here.

## Step 2. Plan the grid as a system before rendering one tile

Write the grid as a table first, one cell per tile: photo or type, headline, label
position. Get that approved before touching HTML, because fixing the rhythm later
means rebuilding the whole set.

- **Cadence:** about one type-only statement tile per row keeps the grid breathing.
  Two adjacent type tiles put a dead patch in the middle of the profile.
- **Statement rotation:** each type tile earns its place with a different job: a
  claim, a number, a definition of the method, the closing line. Four tiles carrying
  the tagline are one tile repeated.
- **Label position rotation:** cycle where the overlay sits (bottom-left, top-centre,
  top-left) across photo tiles. Every label in the same corner reads as a template;
  the rotation is what makes the set look composed.
- **Platform order:** the platform shows newest first, so the tile that should read
  top-left must be built last and uploaded last. Number tiles in display order and
  hand over the reverse as the upload sequence.

## Step 3. Build every asset from one script

One build script generates all assets from shared templates at exact platform sizes:
feed 1080x1350 (4:5), avatar 1080x1080, highlight covers and story art 1080x1920. A
fix is one edit plus one re-run, never twelve hand-patched files.

Render each page with headless Chrome pinned to the export size:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1080,1350 --virtual-time-budget=10000 \
  --screenshot=out/tile-01.png "file://$PWD/src/tile-01.html"
```

- `--virtual-time-budget` is mandatory when the page pulls webfonts or images: the
  shutter otherwise fires early and the QA pass judges the fallback font rather than
  the design.
- `--window-size` must equal the export size, or the file is not the platform's aspect
  ratio and the platform re-crops the composition you approved.
- Keep the whole generation in the script, including the dash check, so a rebuild
  cannot reintroduce a banned character.

## Step 4. Legibility is decided against each photo, not against the palette

- White-on-photo label contrast is a per-tile measurement: place the label over a
  region you can name as dark (or light) for that photo, and rotate position to find
  it. If no region qualifies, add a scrim band or move the line to a type tile.
- The logo follows the same rule. A mark with dark parts disappears on dark photos:
  keep it on solid-ground tiles only, or export a knockout from the same geometry.
  Never re-trace an inverted copy, which produces a second, different drawing.

## Step 5. Profile chrome: avatar and highlight covers

The platform crops both to a circle from the centre of the file, and shows highlight
covers at roughly 84px.

- Keep the mark inside the central square of the file; assume the outer edges are cut.
- One glyph or one short word per cover, centred; the caption under the circle does
  the explaining. A sentence on a cover is unreadable at 84px.
- The avatar must survive at 32px in comment threads: solid ground, high-contrast
  mark, no tagline.

## Step 6. Preview the profile as a profile

Tiles that each look right do not prove the grid reads right. Build one static mock of
the target profile: avatar, bio, highlight row with covers, and the tiles in a
three-column grid at the platform's real geometry (Instagram: 3px gap, 4:5 cells),
then shoot it:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
  --window-size=1000,2900 --virtual-time-budget=10000 \
  --screenshot=out/profile-preview.png "file://$PWD/src/preview.html"
```

Judge the mock as one image: does one thing dominate, is there a dead patch, do two
statement tiles sit adjacent, do the label positions visibly rotate. Then run the
`visual-verify` look pass on the individual tiles at full size. A critique read off
the composite grid is a hypothesis list, not a defect list: open every type tile and
a sample of photo tiles, ask literal questions (what text, what sits behind it, what
is cut), and report which claims the per-asset reads disproved.

## Step 7. Hand over, do not post

Deliver one folder containing the tiles in display order, the avatar, the highlight
covers, the profile preview, and a README that carries: the token list (palette,
fonts, signature), the bio and caption copy, the reversed upload sequence, and the
stated limits of the set (which photos are generated, which are upscaled from small
sources, which tiles were opened individually in QA and which were not). Sourcing
limits stated plainly beat a preview that implies photography the brand does not
have.
