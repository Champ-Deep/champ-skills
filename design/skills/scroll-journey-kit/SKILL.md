---
name: "scroll-journey-kit"
description: "Builds landing pages that feel alive: glow-horizon opening scrolling into an interactive hero, scroll scenes, interactive sections and a broad MicroKit micro-interaction set via LakeKit."
---

# Scroll Journey Kit

Pages that only fade in on scroll and highlight one button read as flat. This skill is the default motion layer for every LakeB2B landing page: a scroll journey (opening scene that scrubs into the interactive hero), interactive sections, and a wide set of micro-interactions. It was proven on the Living Data Globe page (Oct 2026), where a glow horizon rises into a WebGL globe the visitor can hover, pin and filter, then scrolls on into content sections.

Source of the micro-interactions: MicroKit (github.com/henriquegpb/microkit, microkit.co, MIT, 49 shadcn registry items). Deep's note that triggered this skill: "the scroll effects, the beautiful interactive sections, ideally even more micro interactions and not just the one you use to highlight a button." Use a broad set, not one.

The working kit is in the Celsus vault at `Other/Skills/lakekit/`: `lakekit.css`, `lakekit.js`, `lakekit-demo.html` (every effect on one page), `README.md`, and `LakeB2B_Living_Data_Globe_reference.html` (the full pinned journey into a WebGL globe). Copy `lakekit.css` and `lakekit.js` into the page; do not retype them. When the vault is not mounted, build the same attributes from the table below and the rules in this file.

## Workflow

1. **Plan the journey before layout.** Pick the scenes: (1) opening, (2) the hero object the visitor can interact with (globe, map, product, dashboard, calculator), (3) content sections, (4) finale. Name the interactive thing in scene 2. A page with no interactive scene still gets scene 1 plus interactive sections.
2. **Install the kit.** Head probe first in `<head>` (sets `jr` and `rv-on`), `lakekit.css` after the page CSS, `lakekit.js` before `</body>`. GSAP 3.12.5 and ScrollTrigger from cdnjs with SRI only when a pinned journey is used.
3. **Build scene 1.** `.lk-journey > .lk-stage > .lk-horizon + .lk-title + .lk-next`. The horizon is three radial-gradient discs with `mix-blend-mode:screen` (purple, lavender, white rim). No big blur filters; they exhaust memory on laptops. Headline words arrive one by one with a blur-to-sharp.
4. **Scrub into scene 2.** Read `--p` (0 to 1) in CSS or the `lk:progress` event in JS. Move the hero object from the centre of the stage to its resting place, fade the horizon out, bring the copy in. Hover, pin, drag and filter logic stays live the moment the object lands. The entrance finishes when p passes about 0.6, then the page unpins.
5. **Add content sections.** Split `h2`, `.rv` blocks with `--d` stagger, `data-mk="spot"` on cards and steps, `data-mk-count` on figures, `data-mk-slide` on any chip or tab row, `data-rail` on each section, `body[data-mk-progress]`. Add one section that deepens the hero object (industry lanes, market table, case proof).
6. **Assign micro-interactions across the whole page.** Use the table below. Different elements get different effects; never the same effect on every button.
7. **Fallbacks and checks.** Run the checks at the end of this file.

## Attributes (LakeKit)

| Attribute | Effect | Use on |
|---|---|---|
| `data-mk="magnetic"` | leans toward the pointer | primary CTA |
| `data-mk="glow"` | two blurred lights follow the pointer | secondary or ghost button |
| `data-mk="shine"` | bright arc traces the border | tertiary button, request actions |
| `data-mk="swap"` | letters roll up one by one (text only) | nav links, text links |
| `data-mk="underline"` | gradient underline grows | inline links |
| `data-mk="spot"` | pointer wash plus gold top rail | cards, steps, lanes |
| `data-mk="tilt"` | card leans toward the pointer | feature cards (not on `.rv` elements) |
| `data-mk="aura"` | soft light follows the pointer | finale or any full section |
| `data-mk-slide` | one pill glides to the active child | chip rows, tabs |
| `data-rail="Label"` | side nav, sliding glow bar, scroll spy | each major section with an id, desktop 1280 and up |
| `body[data-mk-progress]` | page progress bar | body |
| `data-mk="split"` | headline words rise from a mask | h2 (drop `.rv` on the same element) |
| `.rv` or `data-mk="reveal"` | fade and rise, `--d` stagger | any block |
| `data-mk-count` | number counts up, exact text restored | stats |
| `data-mk-journey` | pinned scene, sets `--p`, fires `lk:progress` | `.lk-journey` |

## MicroKit catalog, grouped by job

Reach past the ported set when the element calls for it. In React: `npx shadcn@latest add @microkit/<name>`. In single-file HTML: port the CSS recipe and recolour orange to gold #FFB703 and blue to lavender #7A76DA.
- Pointer: cursor-edge-glow-button, cursor-follow-share-button, whats-new-glow-button, staggered-letter-glow-button, magnetic-fill-button
- Fill and wipe: yellow-fill-preview-button, orange-circle-fill-button, circle-surface-button, inset-circle-button, outline-wipe-button, expanding-newsletter-button, expanding-contact-button, talk-arrow-reveal-button
- Arrow and icon swaps: icon-swap-button, sliding-send-button, get-started-circle-swap, see-more-swap-button, next-reveal-button, next-dot-fill-button, projects-arrow-button, preview-browser-button, sliding-arrow-label, pricing-slide-link, read-more-swap, contact-reveal-button, white-contact-orbit-button, glow-arrow-button
- Text swaps and underlines: staggered-letter-text-swap, project-text-swap-button, view-more-text-swap, gradient-underline-button, contact-underline-button
- Shine and rim: subscribe-shine-button, aurora-download-button, layered-gradient-button, neon-invert-button, floating-newsletter-button
- Navigation: spotlight-indicator, sliding-underline-tabs, sliding-content-tabs, expanding-icon-tabs, blur-glide-menu, preview-hover-toolbar
- Cards and inputs: social-highlight-cards, social-icon-buttons, contact-details-reveal, focus-input, scrub-number-field
- Commerce: secure-purchase-button

## Interactive sections

A section is interactive when the visitor changes what they see. Pick at least one per page, two for a showpiece:
- A filter row (chips with a sliding pill) that re-cuts a chart, map, globe or list.
- A hover or tap readout (tooltip glass card) tied to a real data row.
- A card grid where each card has a button that prefills the form (market, industry, plan).
- A calculator with `scrub-number-field`.
- A pinned scene whose progress drives a visual (camera, bars, a line draw).
Always keep a plain-HTML twin of the data (table or list) for crawlers and screen readers.

## Rules

- Pointer effects run only on `(hover:hover) and (pointer:fine)` and never under reduced motion. Touch gets the plain element, and the glow lights are hidden on touch.
- Reduced motion: no pinning, no hidden content, no count-up, no split. Content is final and visible.
- Pin only on desktop (1024 and up) when the hero object needs WebGL2 or enough memory. Phones and tablets get the same scenes as a normal-flow stack.
- Hide content in CSS only under `html.rv-on`, set by the head probe. A failed script must never leave a blank page.
- Animate transform, opacity and CSS `translate`. No large blur filters on full-bleed layers.
- Swap and split keep the label in `aria-label`.
- Brand: navy #011A6B ground, lavender #7A76DA, gold #FFB703, magenta #DD1286, purple #6D08BE, muted #B9C0E4. Montserrat and IBM Plex Mono. Logo never animated. Zero em and en dashes. Sample figures labelled once in the footer.
- Budget: page JS under 300KB, LCP under 2.5s (poster first, scene loads after), 60fps on a laptop GPU, file under 16MB.

## Checks before delivery

1. Render at 1440, 768 and 400 with touch emulation, plus reduced motion. Open the screenshots and critique them.
2. Scroll the journey at 0, 40, 70 and 100 percent and look at each frame.
3. Hover or focus one element of each effect and confirm it settles back on leave.
4. Dash count 0. Zero console errors. No horizontal overflow at 400.
5. A heading never stays hidden when JS is blocked (test with scripts off).
6. Report real-GPU frame time as unverified unless it was measured on a real GPU.