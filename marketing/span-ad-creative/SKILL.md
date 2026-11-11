---
name: span-ad-creative
description: Use when SPAN needs campaign ad concepts or ad creative.
---

# SPAN ad creative

Concept to approval pipeline for SPAN Global Services campaign creative: seasonal offers, LinkedIn ads, website banners, display units. Load `span-brand-guidelines` first (palette, dialect, voice, people), `higgsfield-generate` for renders, `visual-verify` for the closing gate. For a broad multi format kit also read `viz-kit/references/campaign-creative.md`.

## 1. Offer before art

For the offer, the opt-in page and the angle test around it, use `meta-ads-low-budget` first: its fit gate and readout rules apply to any paid channel. This skill starts once the offer and angles are approved.


No creative until the offer survives these checks. SPAN is quote based and sales led, so the usual B2B holiday playbook does not transfer.

- Percent off belongs to self serve, card payment products under about $100 a month. Sales led vendors that discount train accounts to wait for the next holiday. SPAN runs a festive frame (gratitude, a free check, a free count), never a discount. See `references/holiday-offer-research.md`.
- A free sample alone is table stakes (ZoomInfo credits, Clearout credits, BookYourData 10 records). The differentiator is a check of the buyer's own list or a count for the buyer's vertical.
- Every offer carries a named gate: the process exists (Santhosh in writing), the cap or price is set (Gary), consent text exists (legal) if a list is uploaded, and the form has a thank you page with a turnaround. No gate, no spend.
- Window: vendors are live from 9 Nov. Start mid November, not Thanksgiving week.

## 2. Copy rules

- Zero em or en dashes. Check with `text.count('\u2014') + text.count('\u2013') == 0` on every copy file and prompt.
- No number, count, badge, client name or turnaround that is not confirmed in writing. Write "free sample for your vertical", not "500 records".
- Name the vertical (Healthcare, Cybersecurity, Legal Tech). Lead with the offer, not a freshness claim (Gary rejected "Refreshed Every 30 Days").
- One tone per campaign. Thanksgiving already supplies warmth; do not stack Y2K or music gags on top. One dry line inside the festive frame is enough.
- No artist names, song titles or lyrics.
- Google RSA: headline 30 characters, description 90, counted by script and the count saved.

## 3. Concept matrix

Three concepts, each a different business job and a different composition family, so reviewers can tell them apart before reading labels:

| Job | Example | Composition |
|---|---|---|
| Existing account expansion | Thank you note, free list check | Warm editorial still life on off white, SPAN green, amber |
| Acquisition | Dry festive line, free list check | Minimal object photo on navy, light green check as the garnish |
| Vertical specialist proof | Count your blessings, we count your market | Typographic on SPAN green gradient, one data drawn motif |

Formats per concept: LinkedIn feed 4:5, website hero 21:9, display 5:4 (the 300 by 250 shape). GPT Image 2.5 has no 8:1 leaderboard or 1:2 half page ratio; build those in HTML.

## 4. Render concepts (approval only)

`scripts/concept_renders.py` holds the working pipeline: concept dict, format layouts, GPT Image 2.5 calls with `--wait --json`, logo compositing, a `--recomposite` mode. Copy it next to the campaign, edit the CONCEPTS dict, run.

- Model: `gpt_image_2_5`, quality medium, 1k, three parallel jobs. Nine renders finish in about two minutes.
- Prompt order: layout for the format, then the visual, then exact quoted copy ("Headline text exactly: ..."), then the shared STYLE block with the hex values and "no hyphens, no dashes, no extra words". Keep under 200 words.
- Leave the bottom left corner empty and composite the real logo in PIL afterwards. Never ask the model to draw the logo.
- Logo source today: `https://www.spanglobalservices.com/assets/img/logo.png` (200 by 57, transparent, grey wordmark #3F3F3F, greens #7BBB21 #27AF0D #026733). The 5 px tagline is illegible at any ad size. Finals need the brand book SVG from Deep's team.
- On dark grounds recolour the grey wordmark to white and the dark green tagline and overlap diamond to light green #3DBE6E, or the tagline vanishes into navy.

### Pitfalls seen

- A typographic concept given a layout line like "visual fills the top sixty percent" makes the model invent a landscape to fill the space. Typographic concepts get their own layout line: text led, motif confined to one region, "never touching any text".
- A motif placed "to the right of the text" collides with the headline on 21:9. Confine it to a stated fraction ("inside the right twenty five percent").
- A vision pass misread "Claim" as "Ciaim" at full frame. Zoom the button region before calling a typo. Vision reads are hypotheses; a zoomed literal read settles them.
- Renders carry the model's reading of the hex values, not the hex. Backgrounds drifted 8 to 20 channel points in earlier runs. Renders are concept direction; finals are HTML (next section).

## 5. Finals

After approval, build each ad in HTML with the brand hex, Montserrat and Inter, and the real logo file. Render to PNG at platform size, pixel sample each background (within 8 channel points of its hex or redo), proof every line at full size, ship the PNG set with its copy file so Preeti and Manu can edit text without re rendering. Route the build to the frontend lane with the concept renders attached as direction.

## 6. Deliver

- Vault: a REVIEW note in the effort folder with the research table (every row tagged VERIFIED, CLAIMED or EXCLUDED), a verdict table against prior decisions, the concept matrix, the render check, open decisions with owner and date.
- `concepts/` with the PNGs, `contact-sheet.png` (rows concepts, columns formats, labelled), the render script and `render-log.json` (prompts and URLs).
- Approval is Deep's, then Gary (offer), Pallab (budget and page), Preeti (page and copy). Stage a needs_input kanban card naming the exact files; never send to them directly.
