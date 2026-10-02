---
name: "identity-kit"
description: "Build a full visual identity at studio depth: brandmark, wordmark, mascot, icon set, tagline and ornaments, drawn as SVG on a labelled brand sheet. Use for any logo, personal brand or visual ID."
---

# Identity Kit

Build a visual identity the way a studio presents one: a system of marks at different registers that all tell one story, held together by a few constants, shown on a labelled marks sheet and an applications sheet. A logo plus a palette is not an identity. If the user asks for "a logo", build the kit anyway and lead with the logo.

The bar has two halves. **Depth** is a studio identity sheet: a monogram badge, an expressive wordmark, a character with a personal prop, a matching icon set, a tagline with a double meaning, ornaments, stripes along the bottom. **Breadth** is a brand kit in use: posts, stories, highlights, avatars, business card, letterhead, email signature, cover, patterns, palette, type.

**The quality Champ asked for, in his words: high-res, minimal while bold.** Solid fills, one heavy outline, almost no interior detail, real vector output, and icons that look unique because they are chunky filled glyphs, not thin line icons. Hand-drawn SVG from code alone did not reach this bar; the first test drive was called shabby. Generate the marks in Higgsfield, then clean and systematise them in code.

Run `design-trends` after this skill as the final pass. Brand locks from any existing brand skill (`deependhq-design-system`, `champions-group-brand`, `lakeb2b-brand-guidelines` and the rest) are absolute unless the user says the new identity replaces them.

## What depth means

Use these as the checklist.

1. **One story, many registers.** The brandmark is the formal stamp, the wordmark the signature, the mascot the warm one, the icons the useful ones, the tagline the loud one. All come from one source story.
2. **A hidden construction.** The brandmark holds a second read people find on the second look (a D that sinks below a waterline, initials built into an object).
3. **A character with one personal prop.** Silhouette, one gesture, one detail that belongs to this person (a flame-shaped blaze, a cap, a tool).
4. **A tagline with a double meaning,** set big and stacked in a heavy face with personality. Ideally the two hero marks split it between them.
5. **Constants.** A three-colour palette (plus at most one character colour), one outline weight, one shape habit.
6. **Sticker logic.** Every mark carries its own halo or rings, so it works on any ground and as a sticker or patch.
7. **Ornaments.** A divider made from one brand glyph in a row, and a band of solid blocks alternating with diagonal stripes.
8. **Presentation.** Small spaced caps under each mark: PRIMARY BRANDMARK, ALTERNATE WORDMARK, MASCOT 1, ICON SET, ALTERNATE MASCOT 2, TYPEFACE + TAGLINE.

## Step 1: Dig for the specific

Read the person's site, vault notes, bio and how they talk before drawing anything.

| Bucket | Look for |
|---|---|
| Name and letters | initials, nickname, handle, **what the name means in their own language** |
| Places | city, a building, a landscape, the room they work in |
| Rituals | working hours, weekly habits |
| Objects | tools of the trade, the desk, a vehicle, food they make |
| Animals and figures | a pet, a horse they ride, a creature from their world |
| Sayings | sign-offs, catchphrases, lines from their writing |
| Work artifacts | the product, the medium, the interface they live in |

The name check pays off: "Deep" is depth in English and lamp in Sanskrit, which gave the tagline, the flame, the water and a divider that is literally a deepavali (a row of lamps).

Write a **story card**: who this is, the one weird true thing, the feeling the identity must carry. Then pick candidates for each slot: three or four mascots, three brandmark constructions, two or three wordmark treatments, three icon sets (half life, half work), three taglines with a double read. Prefer the person's own words for the tagline.

## Step 2: Three territories and the mark architecture

One paragraph each: metaphor, three colours, type pairing, mascot, brandmark idea. Do not anchor to the current site unless the user asks; the kit may replace it. If a brand lock stays, all three territories live inside it and differ in metaphor and treatment only.

| Mark | Job | Rules |
|---|---|---|
| Primary brandmark | the formal stamp | a letter or monogram inside a container (badge, tile, ticket, coin, shield); double frame: outer band, inner keyline at the letter's weight; nothing touches the frame |
| Alternate wordmark | the signature | the name in an expressive face with a keyline and a die-cut halo, one custom flourish |
| Mascot 1 | the warm one | solid silhouette, one gesture, one personal prop, readable at 32 px |
| Alternate mascot 2 | the night or event version | the same drawing, inverted fill, inside concentric rings; the only place a fourth colour may appear |
| Icon set | utility | eight filled glyphs, one weight, one accent detail each, one perspective (flat front views) |
| Type + tagline | the voice | heaviest display weight, stacked, one word in the accent colour or italic |
| Ornaments | rhythm | a divider row built from one brand glyph; four equal band blocks: solid, stripes at -45 degrees, solid, stripes (`repeating-linear-gradient(-45deg, var(--accent) 0 9px, var(--ink) 9px 18px)`) |

## Step 3: Render the brainstorm in Higgsfield

Use Recraft V4.1 in vector mode. It returns a real SVG (`result_url` ends in `.svg`), which is what makes the marks high-res.

```
model: recraft_v4_1   model_type: vector   resolution: 2k   (10 credits each)
colors: ["#0E1A33", "#F4A62A", "#F4EBD9"]   background_color: "#F4EBD9"
aspect_ratio: 1:1 for marks and mascots, 4:3 for icon sets and wordmarks
```

- Create one Higgsfield project per identity (`create_project`, then pass its `folder_id` on every generation). Check `balance` first and tell the user the spend.
- Submit `generate_image_batch` in groups of four. Bigger batches hit Recraft's 429 rate limit; failed submissions created no job and are safe to resubmit.
- Poll with `jobs_wait`, download the SVGs, render them to PNG with Playwright, and look at every one before showing anything.
- Show the whole set once with `show_generation_by_ids`, plus a numbered brainstorm board (M1, M2... B1... W1... I1...) with one honest line under each option. Ask the user to pick by number with AskUserQuestion: mascot, brandmark plus wordmark, palette.

Prompt recipes that worked (describe qualities, never name a designer or a reference brand):

- **Mascot:** "Mascot logo: [animal] [pose] in profile. Solid [colour] silhouette with one uniform extra thick [navy] outline, a shaggy jagged hand-cut edge on the [mane and tail] only. Interior detail kept to a small dot eye, a nostril and [the personal prop]. Bold, minimal, confident, premium sports-team mascot quality, readable at 32 pixels. Flat vector, crisp, no gradients, no shading, plain [cream] background, no text."
- **Icon set:** "Icon set of eight bold solid glyph icons in a 4 by 2 grid with generous spacing: [eight subjects]. Every icon is a chunky filled shape with negative-space cutouts, no thin lines, one consistent heavy weight, rounded corners, flat [navy] on [cream] with one small [marigold] detail each. Flat vector, minimal, stamp-like, no text."
- **Brandmark:** "Primary brandmark styled like [object]: [container] with a thick outer frame and a thin inner keyline, [fill], and in the centre a heavy geometric capital letter [X] [the construction]. Flat vector, bold, minimal, crisp, plain background, no text."
- **Wordmark:** "Wordmark logo that reads exactly \"[Name]\". Heavy, soft, rounded italic brush script in [cream] with a thick [navy] keyline and a wide [marigold] die-cut sticker outline. [One custom flourish]. Flat vector, no other text."

Known failure modes to check for: garbled letters in anything longer than one short word, colours drifting off the palette (a "pool blue" came back electric), constructions that misread (a horseshoe plus bar read as a trident, not a D), parts that float loose (a lamp detached from its lure), icon subjects that do not read at size (a pool ladder, goggles), and a second round that adds unwanted decoration. Regenerate those; keep the winners untouched.

## Step 4: Clean and systematise in code

The picks become a system in Python (`svgkit.py` and `marks.py` in the worked example's `src/`). Recraft SVGs are flat lists of `<path fill="rgb(...)">` with a full-canvas background path first.

- **Load and clean:** strip the c2pa metadata, drop the background rectangle, drop specks (any path under about 900 square units, and any off-palette colour), lock colours to exact hex.
- **Recolour** by swapping fills, for example a picked brandmark from another territory's palette into the chosen one.
- **Crop** each mark to its exact bounds (svgpathtools `bbox`) with a small pad.
- **Silhouette:** union every path with skia-pathops into one outline.
- **Sticker halo:** paint the silhouette path back to front with round joins, then the mark on top. Widths are total stroke widths, so the visible ring is half of each:

```svg
<path d="SIL" fill="#0E1A33" stroke="#0E1A33" stroke-width="130" stroke-linejoin="round"/>  <!-- keyline edge -->
<path d="SIL" fill="#F4EBD9" stroke="#F4EBD9" stroke-width="104" stroke-linejoin="round"/>  <!-- die-cut ring -->
MARK PATHS
```

- **Rings and halos for figures with gaps:** rasterise the silhouette, close the gaps between legs with a disk (scipy `binary_closing`, radius about 70 units at 2048), fill holes, trace back with potracer (`potrace.Bitmap(~mask)`, the `~` matters), then stack strokes outermost first: `[(NAVY, 262), (GOLD, 222)]` gives a marigold patch with a thin navy edge.
- **Icon sets:** split the grid into one SVG per icon by each path's centre, and give every icon the same square viewBox so their sizes stay consistent. Redraw any icon that fails as a solid glyph in the set's measured weight (the terminal icon became a navy window with a knocked-out chevron and a marigold cursor).
- **Variants:** reverse icons (swap ink and paper) for navy circles, tagline versions per ground, a sticker cut of the mascot, a reverse brandmark, and a simplified **favicon cut** (drop the frame, keep the letter and one detail) because the full badge muddies below 48 px.
- **Tagline:** outline the type to paths with HarfBuzz and fontTools so it never depends on installed fonts:

```python
def text_path(font_path, text, size, axes):
    st = instancer.instantiateVariableFont(TTFont(font_path), dict(axes))
    b = io.BytesIO(); st.save(b); data = b.getvalue(); font = TTFont(io.BytesIO(data))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hb.Font(hb.Face(data)), buf, {'kern': True, 'liga': True})
    gs, order, s, x, out = font.getGlyphSet(), font.getGlyphOrder(), size / font['head'].unitsPerEm, 0, []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(gs)
        gs[order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, (x + pos.x_offset) * s, -pos.y_offset * s)))
        out.append(pen.getCommands()); x += pos.x_advance
    return ' '.join(out), x * s
```

Full variable fonts with every axis live at `https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/<File>[axes].ttf`; Fraunces Black with SOFT 100 and WONK 1 is a strong heavy display serif.

If Higgsfield is unavailable, draw in code but hold the same grammar: solid fills, one heavy outline, filled glyph icons with cutouts, never stroke-only icons. Build letters from rectangles and polygons on a 48 unit grid, keep at least one stroke width of clear space inside any frame, and trace any silhouette (the user's photo or a public-domain plate) with potracer after upscaling 6x and blurring, keeping the organic wobble of the edge.

## Step 5: The two sheets

**Marks sheet** (1667 by 1250): brandmark and wordmark across the top half, the glyph divider at 47 percent height, then mascot 1, the 2 by 4 icon grid, alternate mascot 2, tagline, with labels on one shared baseline and the stripe band along the bottom. Labels in a mono face, 12 to 13 px, uppercase, letter-spacing .26em, in the ink colour (accent colours on a light ground are usually too faint for text).

**Applications sheet** (2000 by 1500): brand-colour frame with a big title, a light panel in three columns, the middle column tinted. Include: six social posts, story highlight circles, three patterns (glyph repeat, brand motif, icon repeat), email signature, business card front and back, four profile pictures, palette with names and hex, type specimens, favicon cut at 64, 32 and 16, a horizontal lockup, three stories, a social cover, a letterhead and a sticker sheet. Use only true copy: real titles, real URLs, statements the person has made. No lorem ipsum, no invented numbers or contact details. Wrap each label with its content in one block so a `space-between` column keeps them together.

Render both with Playwright at 1x and 2x:

```js
const p = await (await chromium.launch()).newPage({ viewport: { width: 1667, height: 1250 }, deviceScaleFactor: 2 });
await p.goto('file:///path/sheet.html'); await p.waitForTimeout(600); await p.screenshot({ path: 'sheet@2x.png', fullPage: true });
```

## Step 6: Critique before showing anything

Every item fails the kit if it fails:

- **Cover the name.** Could this belong to anyone else? Then the story card was generic. Go back to Step 1.
- **High-res, minimal, bold.** Zoom the 2x render: crisp vector edges, solid fills, one outline weight, no thin lines in icons, no stray specks.
- **Cookie-cutter tells:** initials in a plain circle, a gradient blob, library icons, an unaltered script font, more than four colours, clip-art mascots, a tagline that names a category.
- **Constants hold** in every mark; name them and point at them.
- **Small sizes:** favicon cut at 16 and 32, mascot at 32, icons at 24, on both grounds.
- **Collisions:** nothing touches a frame or label; text on covers and posts clears the mascot.
- **Legibility:** every icon nameable at 24 px without a caption; marigold or other accent never used for body text on the light ground.
- **IP:** no known characters, logos or brand marks; references teach grammar, never surface.

Two or three passes are normal. Say what changed between them.

## Step 7: Deliver

- The marks sheet and the applications sheet (PNG 1x and 2x, plus their HTML).
- `assets/` with every mark as SVG, the variants, the favicon cut and the glyph.
- `README.md`: story card, constants, palette with names, hex and roles, type with axes, usage rules (minimum sizes, clear space, which version on which ground), how it was made, and an ownership note: marks that began as AI generations should get a final human redraw before any trademark filing; rules differ by country.
- `src/` with the scripts and `concepts/` with every Higgsfield output and the brainstorm board.

Save it where the user keeps their work (for Deep, the Celsus vault next to the brand's notes, archiving any earlier version in `_archive/`). Show the sheets first, then list the files in one line.

## Worked example

`Celsus/Efforts/Active/DeependHQ Site/identity/` holds the deep kit v1. Story: Deep means depth and lamp; he builds 3 PM to 2 AM IST and rides a gray mare on Sundays at sunrise. Tagline: "Go deep. Stay lit." Brandmark: a pool depth-marker tile where the D sinks below the waterline with a cursor block at the surface. Wordmark: "Deep" in flame script, the p's tail ending in a flame. Mascot: the gray mare with a flame-shaped blaze, plus a night patch colourway in a marigold ring. Icons: diya, moon, prompt, horseshoe, belt knot, hex crown, sambar pot, book. Divider: a row of drops that read as water and as flames. 21 Recraft generations, about 210 credits. The test drive before it, archived in `_archive/test-drive-v0/`, shows what code-only drawing looks like next to this bar.

## Guardrails

- No em dashes or en dashes anywhere, including labels, file contents and SVG titles.
- Brand locks win unless the user says the kit replaces them.
- Original marks only; credit any public-domain source in the README.
- Never name real team members or clients on any mark or sheet.
- Spend credits only after telling the user the expected cost; stop and ask before going past roughly 300 credits in one session.