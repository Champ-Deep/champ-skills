# Art styles: 20 looks, each as an image prompt and a front-end recipe

Source: a 25 second Short "20 Creative AI Art Prompts" (Seb Intel, youtube.com/shorts/iD8D7X28fJI). The creator gates the real prompts behind a comment, so none of them are copied here. Each prompt below is rebuilt from the sample image the Short shows for that style, read from frames on 2026-11-04, then cut down to the cues that make the look.

Use this file when a brief asks for a mood, a campaign look, an event poster, a social series or a microsite with a strong visual identity. Do not use it to override a brand skill. Brand colours, fonts and logo rules from `lakeb2b-brand-guidelines`, `span-brand-guidelines`, `ampliz-brand-guidelines`, `metricfox-brand-guidelines` or `champions-group-brand` win; a style supplies texture, light and composition on top of them. Product UI, dashboards and anything a client reads for numbers stay on the brand system.

## How to use

1. Pick one style from the table that matches the brief's mood. One style per page or asset set. Mixing two is allowed only as a main style plus a single accent device (for example Mandala layout with Neon Glow light).
2. Image: fill `{subject}` in the prompt and generate. Keep the prompt; do not pad it with extra adjectives, each already carries a cue.
3. Page: take the dials and the recipe. The three dials are the ones in `design-taste-frontend` section 1: `DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY`.
4. Check the Avoid column before shipping. Several styles fail contrast or reduced-motion rules unless handled.

## The 20

Prompt shape: `{subject}, <style cues>, <palette>, <light>, <composition>`. Negative prompt is the same for all unless noted: `text, watermark, logo, blur, extra fingers, low contrast mud`.

### Loud and graphic

**1. Pop Art** (dials 8/5/4)
Prompt: `{subject}, pop art screen print, flat saturated red blue yellow, thick black outlines, halftone dot shading, no soft gradients, centred bold pose`
Recipe: flat fills, 3px black borders, halftone radial-gradient dots as section texture, hard offset shadows, display type in heavy condensed grotesque.
Use: campaign launches, event teasers, social carousels. Avoid: long-form reading, regulated or trust-first pages.

**8. Color Blocking** (dials 7/3/3)
Prompt: `{subject} reduced to flat geometric colour blocks, hot pink orange yellow blue green purple, no texture, no shadows, sharp edges, abstract landscape composition`
Recipe: CSS grid of solid panels, one colour per section, no gradients, type set in a single weight. Easiest style to keep fast and accessible.
Use: pricing pages, report covers, bento grids. Avoid: more than five hues (it turns noisy); check each text-on-block pair for contrast.

**14. Op Art** (dials 9/6/2)
Prompt: `{subject}, op art optical illusion, black and white wavy parallel lines, sharp precise repetition, apparent motion and depth, flat lighting, full-frame pattern`
Recipe: SVG or repeating-linear-gradient line fields as hero background, mix-blend-mode to carve the subject. Keep it to one hero band.
Use: attention hooks, reveal sections. Avoid: behind body text; can trigger discomfort, so freeze it under `prefers-reduced-motion` and never animate full-screen.

### Neon and glow

**3. Synthwave** (dials 8/6/3)
Prompt: `{subject}, synthwave retro 80s poster, hot pink electric purple cyan on black, glowing neon outlines, perspective grid horizon, high contrast`
Recipe: near-black base, two accent neons only, grid floor via CSS perspective, text-shadow glow on headings, mono or wide retro display type.
Use: tech launches, AI products, event nights. Avoid: serious finance or compliance; glow text fails contrast below 18px.

**6. Neon Glow** (dials 7/5/3)
Prompt: `{subject} drawn as neon tube light, hot pink cyan purple on pure black, soft blurred glow edges, self-illuminated, centred vertical composition`
Recipe: `#000` base, SVG strokes with layered blur filters, hover brightens the stroke. Limit glow to the hero and one accent.
Use: nightlife, club and community events, dark-mode heroes. Avoid: light pages; full-page glow hurts battery and legibility.

**11. Bioluminescent** (dials 7/6/2)
Prompt: `{subject} as glowing deep-sea creature, translucent tentacles, soft ethereal blue purple pink light on near-black water, drifting particles, centred vertical`
Recipe: deep navy base, slow float animations (transform only), soft radial glows, particles in canvas capped for mobile.
Use: health and longevity, science, calm product heroes. Avoid: busy data pages.

**15. Cosmic Nebula** (dials 8/5/2)
Prompt: `{subject} inside a cosmic nebula, swirling gas clouds purple pink blue orange, bright glowing cores, dark space, hazy luminous full-frame`
Recipe: layered radial gradients and a blurred noise texture, parallax between two layers, large light-weight type on top.
Use: AI, data and platform announcements. Avoid: overuse; it is the most common AI-default look, so pair it with a distinctive typeface or skip it.

**16. Prism Rainbow** (dials 7/6/2)
Prompt: `{subject}, crisp glass prism refracting light into a full rainbow spectrum, hard edges, dark background, bright prismatic glow`
Recipe: dark base, one conic or linear spectrum gradient used as a single accent ribbon, glass-like edges with 1px highlight borders.
Use: "one input, many outputs" stories such as data enrichment or multi-channel. Avoid: spreading the spectrum across the whole UI.

### Painterly and handmade

**5. Fauvism** (dials 8/3/3)
Prompt: `{subject}, fauvist oil painting, bold non-naturalistic colour lime green orange purple, thick visible brushstrokes, flat expressive light, loose floral background`
Recipe: paint-stroke SVG masks, big colour fields, a hand-drawn display face, no drop shadows.
Use: culture, hospitality, ranch and club brands. Avoid: data-heavy pages.

**7. Stained Glass** (dials 6/3/4)
Prompt: `{subject} as stained glass window, jewel tones deep blue gold red, thick black lead lines separating colour segments, backlit, symmetrical panel`
Recipe: SVG polygons with dark 4px strokes, brightness pulse on hover (opacity only), arched frame container.
Use: heritage, events, awards. Avoid: small sizes; leading lines vanish under 400px.

**12. Acrylic Pour** (dials 8/4/2)
Prompt: `{subject}, fluid acrylic pour abstract, marbled swirls warm orange yellow with cool blue and earth tones, thick glossy paint, cells and lacing, even lighting`
Recipe: a single high-resolution image as hero background with a gradient scrim, no animation needed; extract two colours as the page accents.
Use: backgrounds for covers, hero strips, social tiles. Avoid: text directly on the swirl without a scrim.

**13. Alebrije** (dials 9/4/4)
Prompt: `{subject} as an alebrije, Mexican folk art fantastical creature, intricate hand-painted swirls and dots, saturated teal orange pink yellow, bold outlines, bright even light`
Recipe: pattern borders and dividers, saturated palette, ornamental SVG fills. Treat it as culturally specific folk art: use it for Mexican or Latin American contexts or with credit, not as a generic "colourful" filler.
Use: LATAM campaigns, festival pages. Avoid: unrelated B2B contexts.

**20. Claymation** (dials 7/6/3)
Prompt: `{subject} as a hand-sculpted clay figure, stop-motion look, soft matte clay with fingerprints, warm earthy palette, soft warm light, simple handmade set`
Recipe: rounded blobs, soft inner shadows, stepped (12 fps) animation via `steps()`, warm paper background.
Use: friendly explainers, onboarding, kids or consumer. Avoid: enterprise trust pages.

### Pattern and symmetry

**2. Psychedelic** (dials 9/7/3)
Prompt: `{subject}, psychedelic poster, neon rainbow cyan magenta yellow purple, swirling fractal radial patterns, luminous glowing edges, centred`
Recipe: radial pattern background, rotating slowly (transform only), huge hand-lettered type.
Use: festival and music. Avoid: reading surfaces; always provide a calm static version.

**4. Kaleidoscopic** (dials 8/6/3)
Prompt: `{subject} mirrored into a kaleidoscope, deep blues purples gold, repeating radial segments, painterly, soft glowing moon or star at the centre`
Recipe: CSS `conic-gradient` plus mirrored SVG wedges, rotation on scroll progress.
Use: scroll-driven transitions and hero reveals. Avoid: loops that run forever on mobile.

**17. Mandala** (dials 5/3/5)
Prompt: `{subject} as a symmetrical mandala, intricate repeating geometric floral rings, saturated pink blue yellow orange, radial composition, even light, fine detail`
Recipe: centred radial layout, concentric section dividers, stroke-draw reveal. The most orderly style; works for wellness and process diagrams.
Use: wellness, ritual, process wheels. Avoid: asymmetric editorial layouts.

### Digital and surreal

**9. Glitch** (dials 9/7/4)
Prompt: `{subject} with digital glitch distortion, RGB channel shift cyan magenta yellow, pixel blocks and horizontal tearing, corrupted file look, high contrast`
Recipe: clip-path slice offsets on hover, text-shadow channel split, a short 300ms glitch on load only, never continuous.
Use: security and data topics, hacker or creator brands. Avoid: anything where "broken" reads as a defect; accessibility needs the glitch off for reduced motion.

**18. Hyper-Surrealism** (dials 9/5/3)
Prompt: `{subject}, hyper-real surreal portrait, impossible floating elements, warped perspective, one uncanny detail such as a crown, polished smooth finish, soft dreamlike light`
Recipe: photographic hero with one composited impossible element, restrained UI around it. Image carries it; keep type quiet.
Use: brand films, editorial covers. Avoid: product proof pages.

**19. Pixel Art** (dials 6/6/4)
Prompt: `{subject}, 16-bit pixel art side-scrolling scene, chunky visible pixels, limited bright palette, flat game lighting, sprite characters`
Recipe: `image-rendering: pixelated`, integer-scaled sprites, 8px grid, stepped animations. Matches the Champ pixel host work.
Use: pixel host character, games, playful docs. Avoid: scaling a small sprite to fractional sizes.

### Soft and cute

**10. Kawaii** (dials 6/5/3)
Prompt: `{subject} in kawaii style, soft pastel pink blue lilac white, rounded shapes, large eyes, smooth soft edges, diffused gentle light, centred`
Recipe: pill buttons, 24px+ radii, pastel tokens, bouncy easing on hover.
Use: consumer apps, community, mascots. Avoid: B2B and finance.

## Extending this list (rebuild a style from any video)

When Deep hands over a Short or a video showing looks worth keeping:

1. Download the media once: `yt-dlp -f bestvideo+bestaudio/best -o in.%(ext) "<url>"`.
2. Cut one frame per look: `ffmpeg -i in.mp4 -vf fps=2 frames/f%03d.jpg` (a 25s Short at 2fps gives 50 frames; use `fps=1` for long videos). Read them in batches of three or four with `vision_analyze`, asking which styles are visible and what cues define each, so the naming comes from the image rather than from the video's title or caption.
3. Write each prompt in the shape used above: `{subject}, <style cues>, <palette>, <light>, <composition>`. One line of cues; extra adjectives dilute the look.
4. Test before shipping the set: generate 2 or 3 of them with `image_generate` against the same neutral subject, stitch them side by side, and vision-check them against the source frames. Do not test all 20: the sample is what tells you whether the cues hold.
5. Record the result under "Coverage and limits": which prompts were tested and which were not. A reference that implies every prompt was proven is worse than one that says three were.

## Coverage and limits

- Prompts are reconstruction, not the creator's: his list is gated behind a comment, so the cues come from the frames. Style names and the look of each sample are verified; prompts are rebuilt and tuned per image model.
- Prompts were tested as a sample: Stained Glass, Op Art and Claymation were generated against a lighthouse subject and checked against the Short's frames. The other 17 prompts and every recipe are unproven, so treat them as a starting point and tune per image model.
- Dials are first estimates from each look and the `design-taste-frontend` presets; adjust after seeing a build.
- No page has yet been built from these recipes. Run `visual-verify` and `ten-out-of-ten` on the first use and amend the Avoid column with what you find.
