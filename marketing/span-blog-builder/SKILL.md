---
name: "span-blog-builder"
description: "Build a Span Global Services (SGS) blog end to end: research, Word draft, readability rewrite, Span theme design and a WordPress-safe paste-ready code block."
---

# Span Blog Builder

Turns a blog topic for Span Global Services into four deliverables, in this order, pausing for review between stages:

1. Word draft for writers (no design)
2. Readability before and after report (only if asked, or if the draft reads templated)
3. Span theme page design (full HTML preview)
4. Final paste-ready WordPress code: an interactive version and an inline-styles-only version

## Before You Start: Model and Tool Reminder

Tell Champ in one line at the start of every run:

> Tip: for the design stages, Claude Design (the Design artifact type) is faster for visual iteration, and a Sonnet model is enough for drafting and building this kind of blog. Switch model in the model picker if you want to save usage.

If the Artifact tool lists a Design type, offer to build stage 3 there instead of a local HTML file.

## Stage 1: Research and Word Draft

- Load `b2b-blog-writer` for method, then research with WebSearch and WebFetch. Every company or vendor claim needs a public source (press release, case study). Never invent a stat.
- Pull Span's own numbers from the live Span page for the topic (for example the technology list page). Quote them with the month verified.
- **Internal links must be live.** Fetch `https://www.spanglobalservices.com/page-sitemap.xml` and `https://www.spanglobalservices.com/blog/post-sitemap.xml`, pick relevant pages, then `curl -o /dev/null -w '%{http_code}'` each one. Only use links that return 200.
- CTAs: "Request a Free Sample" (`/request-sample-list`) and "Book 30 Minutes With Span" (`https://scheduler.zoom.us/span-global-services/30-mins-with-span-global`). Add `?utm_source=blog&utm_medium=cta&utm_campaign=<slug>` to every CTA.
- Word file via the `docx` skill: editor brief at top (SEO title under 60 characters, meta description under 155, slug, keywords, fact check note), then the article, then a Sources list. Verify character counts with code, not by eye.
- **Dates:** check every relative phrase ("within the last two years") against today's date. Prefer absolute phrasing ("since April 2024").
- Crisp by default: 1,500 to 2,200 words. Top N lists may go from 15 to 20 entries.

## Stage 2: Readability Check (Anti Template)

Run `vinh-copywriting` then `no-ai-slop` (Gate mode) on the draft. Lessons from past runs:

- Do not give every list entry the same labelled form ("POS platform:", "Footprint:", "Who should target them:" repeated 20 times read as a template). Vary entry shape, or put the scannable fact in the heading ("Applebee's Runs Toast").
- Open with a real, dated sequence of events (relived, not reported).
- Merge thin entries that have one weak fact.
- Replace "pitch X rather than Y" contrasts with direct advice.
- Measure before and after with code: Flesch Reading Ease, Flesch Kincaid grade, Gunning Fog, sentence count under 8 words, repeated labels, top sentence openers, percent of sentences with a number. Note that scores are directional.

## Stage 3: Span Theme Design

Reference look: `https://www.spanglobalservices.com/blog/types-of-semiconductor-companies-to-target/`. Screenshot it with Playwright if unsure.

Design tokens:

```
ink #0d1b12 (body accents only)   heading #2e4a3a   body #35453b   muted #55655b
green #27B441   green-dark #036733   deep #06331C
mint #EEF8F0   mint-2 #D7EEDC   line #E1E8E3   wash #F3F6F4 / #F9FBFA   amber #FBBC05
```

Rules:

- Font Mulish across the page. Paragraphs 18px, line height 1.75.
- **Headings use #2e4a3a, never near-black.** H2 weight 800, H3 and H4 weight 700.
- All headings in Title Case. Zero em dashes and en dashes anywhere (search the final file for the characters).
- No eyebrow or overline labels (no small uppercase letter-spaced kickers). Use title-case labels instead.
- Generous breathing space: 56 to 88px between sections, 24 to 36px card padding.
- Use full width: main column plus a 380px sticky sidebar (TOC and CTA card). No narrow centered column.
- Components: dark green gradient section banners, white cards with a 5px green left border and a number badge, rounded tag chips, two-box row (white facts box plus mint "Who Should Target Them" box), mint CTA strips mid-article, big green gradient CTA block with stats, FAQ cards with green left border.
- Mobile: 16px side padding, single column, hide low-value table columns, no horizontal scroll (check `document.documentElement.scrollWidth` equals viewport width at 390px).

## Stage 4: WordPress Code (Must Survive WordPress)

Deliver two files: an interactive version (scoped `<style>` plus one IIFE `<script>`) and an inline-styles-only version (every style in `style=""`, no style or script blocks) for editors that strip them. Output starts at the first intro paragraph; the Span theme renders title, byline, featured image and sidebar TOC.

### WordPress Safety Rules (learned the hard way)

WordPress `wpautop` inserts `<p>` and `<br>` into pasted HTML. It broke the first build: filter bar stacked, legend text ran together, and `<p>` tags landed inside the CSS and JS. The Span theme also forces `text-transform:uppercase` and letter spacing on links and spans.

1. **Minify to one line.** No newlines anywhere: collapse whitespace between tags, minify CSS, run JS through `terser -c -m`, strip HTML comments.
2. **No inline element directly after a closing block tag.** `wpautop` wraps any `span`, `a`, `b`, `button`, `select`, `input` or `label` that follows `</div>`, `</h3>`, `</p>` and so on in a new `<p>`. Use `div` for badges, tags, hints, counts and icons; wrap buttons, CTAs, selects and inputs in their own `div`; never put block content inside `label` (use a `div role="checkbox" aria-checked` toggled by JS instead of a checkbox input); put `<script>` tags inside a `<div style="display:none">`.
3. **Guard CSS** in the interactive version: `#id br{display:none!important}`, `#id p:empty{display:none!important}`, `#id,#id *{text-transform:none!important;letter-spacing:normal!important}`, reset button, select and input margins and line height, set list-style explicitly, and give generic spans an explicit color. In the inline version, append `text-transform:none;letter-spacing:normal` to every styled element and set color on every span.
4. **Verify with real WordPress code.** Download `wp-includes/formatting.php` from `github.com/WordPress/wordpress-develop` and run `wpautop()` in PHP on the output (stub `apply_filters`, `__`, `_x`, `get_option`, `get_shortcode_regex`). The result must equal the input once newlines are removed.
5. **Render inside the real Span theme CSS.** Load Span's `bootstrap.min.css`, `assets/css/style.min.css`, `responsive.css` and `style.css` from `spanglobalservices.com/blog/wp-content/themes/spanglobalblog-theme/` in a Playwright test page, put the wpautop output in a `col-lg-8` column, and screenshot at 1440px and 390px. Check: no uppercase text, legend spacing correct, filter bar in one row, zero page errors, no horizontal scroll, filters return expected counts.

### Interactive Version Contents

Count-up stats, clickable bar chart that filters cards, sortable at-a-glance table with jump links, horizontal timeline with arrow buttons, sticky filter bar (sector pills, platform dropdown, search, "Showing X of N", reset; static on mobile), fade-in cards, signal checker with a 4-step meter and CTA, FAQ accordion with FAQPage JSON-LD, collapsible Sources. Respect `prefers-reduced-motion`.

### Inline Version Contents

Stat row, bar chart with inline `width:%` bars, striped table with jump links, horizontal scroll timeline, "Jump to a sector" pill links, banners, cards, CTA strips, numbered signals with a static "Score the Account" key, CTA block, FAQ and Sources as native `<details>`. Responsive with `flex-wrap` and `flex:1 1 <min>px` instead of media queries. Do not promise hover, animation, filters, sorting or sticky bars here.

### Dev Notes to Include

- Paste into the Custom HTML block or the editor's Text or HTML tab, never the visual tab.
- If the interactive version shows plain styling, the editor stripped the style or script block: use the inline version.
- Adjust the sticky filter bar `top` offset to the real header height, and exclude the block from lazy-load or JS-deferral plugins.

## Delivery

- Write files to `/mnt/user-data/outputs/` and send with SendUserFile. Keep the reply short: first two lines carry the outcome.
- Name what changed and anything writers or devs must check.

## Feedback Loop (Every Run)

End every stage by asking Champ one question:

> Any changes or critiques on this stage? I will fold them into the span-blog-builder skill so the next blog gets them by default.

When he gives feedback:

1. Apply it to the current deliverable.
2. If it is a standing preference (colour, spacing, tone, structure, a banned pattern), add it to the matching stage above and log it below.
3. Propose the updated skill with `propose_skills` (kind: improvement, target: span-blog-builder) carrying the full SKILL.md. Do not wait to be asked.

## Feedback Log

- 2026-10-05: Draft read as templatized. Vary entry shapes, open with a dated story, run vinh-copywriting and no-ai-slop.
- 2026-10-06: Needs proper Span theme, breathing space, title case headings, no em dashes.
- 2026-10-06: Final code should be inline and start where the blog body starts; add interactive visuals.
- 2026-10-06: Headings too dark black. Use #2e4a3a for headings.
- 2026-10-06: Remind to use Claude Design and Sonnet models for this kind of task.
- 2026-10-06: Editor may strip style and script blocks. Always ship an inline-styles-only version alongside the interactive one.
- 2026-10-06: Pasted blog rendered broken (stacked filter bar, run-together legend). Cause: WordPress wpautop plus Span theme uppercase rules. Minify to one line, avoid inline elements after block closes, add guard CSS, and test with real wpautop and the real Span theme CSS.