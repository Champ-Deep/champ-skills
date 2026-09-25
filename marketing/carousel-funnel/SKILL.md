---
name: carousel-funnel
description: Turn any long-form asset (playbook, guide, report, case study, PDF, blog) into a social carousel funnel: a 10-slide LinkedIn document PDF plus Instagram PNGs, the post copy, the tracked first-comment link, the ungated landing page spec, ChampUTM naming, and Factors.ai visitor identification so the team knows which companies came from which post. MANDATORY TRIGGER for "make a carousel", "turn this playbook into a carousel", "LinkedIn document post", "carousel for socials", "slides for LinkedIn", "link in the comments", "promote this guide on LinkedIn", "social version of this PDF", "carousel plus tracking", or any request to distribute a long asset on social with a link back to the full version. Works for every Champions Group brand; loads the brand's guideline skill for colours and voice.
---

# Carousel Funnel

> One long asset in. A carousel that teaches, a comment that links, a page that identifies who came. All three ship together.

A carousel is not a summary of the document. It is the argument of the document, one idea per slide, ending with a reason to read the whole thing. The link lives in the first comment, the full asset lives on our site as an HTML page (never a bare PDF), and every link carries a UTM that Factors.ai and GA4 can read. If any of those three is missing the post is content, not a funnel.

## Inputs

- The asset: PDF, DOCX, Markdown, a URL, or a vault note. Read all of it before writing a slide.
- Brand: which Champions Group brand is posting. Load that brand's guideline skill (`lakeb2b-brand-guidelines`, `ampliz-brand-guidelines`, `champions-group-brand`, `metricfox-brand-guidelines`, `ab7-brand-guidelines`) for colours, wordmark, and voice. Default to LakeB2B if the asset is LakeB2B-branded.
- The landing page URL, or agreement that one will be built at `/playbooks/<slug>`.
- Optional: which formats (default `linkedin`, which also serves Instagram 4:5; add `square` only if a channel needs it).

If the brand or the destination URL is unknown, ask once, then proceed.

## Process

### Phase 1: Extract the argument (10 minutes of reading, not skimming)

Read the whole asset. Write down, in order, the one-sentence claim of each chapter or section. That list of sentences is the carousel's spine: if it does not hold as an argument when read on its own, fix the list before touching a slide. Pull the two or three concrete artefacts that visualise well (a scoring table, a tiering rule, a before-and-after message, a funnel of numbers) and note which slide each belongs to.

Then pick the hook. It is the asset's sharpest reframe, in the reader's language, under 14 words. Not the title of the asset.

### Phase 2: Write the slide JSON

Read `references/slide-patterns.md` for slide types, visual blocks and the copy budgets. Then write `<slug>.json` following the shape in `examples/intent-signal-playbook.json`:

- `slug`, `brand` (name, tagline, handle, primary, dark, accent hex from the brand skill; optional `logo_src` as a data URI if the wordmark should be the real logo).
- `slides`: one `hook`, eight or so `point` slides (each with `n`, `kicker`, `title`, and either `body` or a `visual` block, plus an optional `after` line), one `cta` with `cta` text naming the first comment, `url_display`, and a `pill` for the save ask.

Rules that are not optional: one idea per slide; titles are sentences that carry the argument when read in sequence; 90 words per slide ceiling; no em dashes or en dashes anywhere (the renderer refuses the file); no emojis; no stock imagery; the CTA slide says "link in the first comment" in words.

### Phase 3: Render and look

```
python3 scripts/render.py <slug>.json out/ --formats=linkedin
```

Outputs `out/linkedin/slide-01.png` to `slide-NN.png` (1080 x 1350, use these for Instagram too) and `out/linkedin/<slug>-linkedin.pdf` (the LinkedIn document upload). Add `--formats=linkedin,square` when a channel needs 1080 x 1080.

The script checks for dashes, then fits each slide; a warning that a slide was scaled below 85 percent means cut words and render again. Then open the PNGs and look at every slide at phone size (a third of actual). Fix anything that needs a squint. Run `visual-verify` if it is available in the session.

### Phase 4: Write the post, the comment, and the replies

Read `references/post-and-comment.md`. Produce, in one markdown file next to the JSON (see `examples/intent-signal-playbook-post.md`): the LinkedIn document title, the LinkedIn post copy (120 to 220 words, first line under 140 characters), the first comment with the `-comment` UTM link, a reply template with the `-reply` link, the Instagram caption ("link in bio"), and the shape of an employee reshare line. Run `no-ai-slop` on all of it before it ships.

### Phase 5: Page and tracking, before the post goes live

Read `references/tracking-setup.md` and produce the tracking block for this asset:

1. Landing page spec, or confirmation the page exists at the agreed path as HTML (the PDF is a download at the bottom, tagged as an event). Build it with `pdf-to-html` or `visual-report-builder` if it does not exist.
2. The complete UTM set for the asset using the house convention (`utm_campaign={brand}_{asset-slug}_{monYYYY}`, `utm_content=carousel_v{n}-{touch}`), registered in ChampUTM.
3. Factors.ai checklist status for the site: snippet on all pages, domain verified, UTMs arriving as session properties, company identification on, the asset's saved segment and ICP filter created, alert routing set.
4. GA4: scroll and the two custom events on the page, one exploration by `utm_content`.
5. A new row in the brand's social tracking sheet with the post plan and every UTM variant.

If the team cannot confirm items 1 to 3 the post waits. Posting first and tracking later is how every previous campaign ended up with "we think it did well".

### Phase 6: Hand off

Deliver one folder: `<slug>.json`, `out/linkedin/*.png`, `out/linkedin/<slug>-linkedin.pdf`, `<slug>-post.md`, and `<slug>-tracking.md` (the filled-in Phase 5 block). Save it in the vault under the asset's effort folder (or `Efforts/Active/<Brand> Social/<slug>/`) and tell the poster the routine from `post-and-comment.md`: upload, title, copy, post, first comment within 60 seconds, pin, log, read on day 2 and day 7.

## Guardrails

- Intent and visitor identification pick the account; they never write the message. No follow-up ever says "I saw you read our playbook". This is the asset's own rule and it applies to how we use the data the asset generates.
- Ungated by default. A form before the content kills the LinkedIn click-through and the visitor-intelligence match does the identification anyway. A soft "email me the PDF" at the end is the only form.
- One carousel per asset per month per page. Refresh the hook and re-post as `v2` after 30 days if the first run did well; do not post the same file twice.
- Brand colours and wordmark come from the brand skill, not from memory. Never mix two brands' colours on one carousel.
- No em dashes or en dashes anywhere: slides, post, comment, page, sheet.

## Files

Canonical copies of the full folder (template, script, references, examples) live in the shared library at `~/champ-skills/marketing/carousel-funnel/` and in the vault at `Celsus/Other/Skills/carousel-funnel/`. If this SKILL.md is loaded without its folder, read from one of those.

- `templates/carousel.html`: the single-file slide template (Fraunces display, Inter body, brand tokens as CSS variables, nine visual blocks). Edit the CSS here to change the look for every future carousel.
- `scripts/render.py`: JSON to PNGs and PDF via Playwright. Dash check, overflow fit, lossless PDF.
- `references/slide-patterns.md`: slide types, visual blocks, copy budgets, what not to do.
- `references/post-and-comment.md`: post copy formula, first-comment link, replies, document title, posting routine, timing.
- `references/tracking-setup.md`: landing page spec, UTM standard and ChampUTM, Factors.ai setup, GA4 events, tracking sheet columns and the weekly read.
- `examples/intent-signal-playbook.json` and `examples/intent-signal-playbook-post.md`: the LakeB2B Intent Signal Playbook, rendered end to end, as the reference for quality.

## Related skills

`lakeb2b-brand-guidelines` and the other brand skills (colours, voice), `no-ai-slop` (final copy gate), `visual-verify` (render check), `pdf-to-html` and `visual-report-builder` (the landing page), `page-refresh` (page design language), `lead-gen-playbook-builder` (produces the kind of asset this skill distributes), `skill-repo-sync` (after any edit to this skill).
