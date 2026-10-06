# Showcase page kit

Vanilla HTML, CSS and JS. No framework, no build tool beyond Python 3, Playwright and Pillow. Google Fonts is the only external request on the page.

| File | What it is |
|---|---|
| `core.css` | tokens (LakeB2B by default), every component, motion, micro-interactions, responsive rules |
| `core.js` | static and reduced-motion detection, headline word split, unit charts, count-up, reveal on scroll, progress bar, nav state, pointer tilt, button glow, scroll-spy rail, sortable tables with row motion |
| `build.py` | `python3 build.py 02 03` assembles `cases/<id>.html` + `cases/<id>.json` into `dist/<slug>.html` (standalone) and `dist/<slug>.artifact.html` (Artifact fragment); fails on any em or en dash |
| `shoot.py` | `python3 shoot.py <slug> [--export]` screenshots 1440 and 390 (motion top and static full page), reports overflow, small tap targets and console errors; `--export` writes `export/<slug>.png` (2x) and a one-page `export/<slug>.pdf` with the hero flattened |
| `cases/02.*`, `cases/03.*` | worked examples: map, unit chart, sortable table, callout, timeline |
| `data/sea_dots.json` | Southeast Asia dot grid (Natural Earth 50m), used by `sea_map()` |
| `assets/lakeb2b-logo.png`, `assets/lakeb2b-logo-reversed.png` | LakeB2B transparent logo (full colour for light grounds) and reversed (white wordmark for the dark hero); the nav swaps them |

## Case JSON keys

`slug`, `title` (2 to 4 word page name), `desc`, `chip` (nav chip), `short` (mobile button label), `hold` (true adds a red HOLD pill), `cta_h`, `cta_p`, `foot`, optional `css` (page-level overrides), optional `map` (bubbles for `sea_map`), optional `tiles` (`[segment, worked, mapped]` rows), optional `brand` (overrides `logo`, `logo_reversed`, `logo_alt`, `home_url`, `home_label`, `cta_url`, `cta_label`, `brand_line`, `nav_label`).

## Placeholders in case HTML

`{{NAV}}`, `{{HOLD}}`, `{{STARS}}`, `{{CLOUDS}}`, `{{CTA}}`, `{{FOOT}}`, `{{MAP}}`, `{{TILES}}`.

## Another brand

Override the colour tokens and the hero gradient in the case `css` key (or a brand block at the top of `core.css`), pass the brand's logo and URLs in `brand`, and keep everything else.
