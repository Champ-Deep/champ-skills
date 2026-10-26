# Generated assets (optional, paid)

Generated images and video help in a narrow case and hurt everywhere else. Default to code-drawn visuals (diagrams, the product's real UI, icon flows, logo walls).

## When it helps
- The business is physical and visual (cars, clinics, homes, venues, food, job sites) **and** has no good photos of its own.
- An atmospheric hero or section background, a slow loop, or a single "this is the world we work in" image.

## When it hurts
- Abstract SaaS concepts (glowing lines, floating 3D shapes, "AI brain" imagery): reads as AI slop instantly.
- Faking the product's UI, fake people giving testimonials, fake client premises, fake team photos. Never.
- Anything with readable text, logos or brand marks in it.

## How
1. Write a shot list: what each asset is for, where it sits, the aspect ratio, still or loop, and the prompt. Reference the brand colour and the site's light (e.g. night, violet rim light).
2. Pick the model and resolution, price every item, and show the user the list and the total. Wait for a yes.
3. Draft at low resolution first, review, then finalise only the keepers.
4. Loops: start frame = end frame so it loops seamlessly. Encode H.264 MP4 + WebM + a JPG poster; `autoplay muted loop playsinline`, `preload="none"` below the fold, and respect reduced motion (show the poster).
5. Stills: export WebP at the size the slot needs (usually ≤ 1600px wide, ≤ 200 KB).

With Higgsfield: GPT Image / Seedream for stills with reference images; Seedance (start + end frame the same image) for loops; draft at 480p, then finalise the chosen draft.

If the result doesn't beat a code-drawn alternative, don't use it. Say so, that's a valid outcome.
