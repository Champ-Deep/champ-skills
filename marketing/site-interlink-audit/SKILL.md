---
name: site-interlink-audit
description: Use to audit a site's internal linking and link gaps.
---

# Site Interlink Audit

Point it at any domain. It produces a client-ready report of what exists, what is
stranded, which entities the site has pages for, and a ranked list of link edits.

## Run it

```bash
SCRATCH=~/.hermes/cache/scratch/sitearch    # or your own dir
cd $SCRATCH
python3 pipeline.py <domain>            # crawl -> bundle-<host>.json
python3 plan.py bundle-<host>.json      # entities + worklist -> -plan.json
python3 report.py bundle-<host>.json bundle-<host>-plan.json -o out.html
python3 verify_report.py out.html       # MANDATORY gate: 21 DOM assertions
```

`plan.py` prints `bundle-<host>-plan.json`; pass that as the second argument to `report.py`.

## Why each piece exists (learned the hard way)

**Discovery (`discover.py`)** tries, in order: `robots.txt` sitemaps, `/sitemap.xml`,
`sitemap_index.xml` (nested, BFS), WordPress REST (`/wp-json/wp/v2/` pages+posts+types),
then crawl-frontier fallback. Never trust the sitemap alone: on Span it listed 946 URLs
while the live site had 3,163.

**Body extraction (`extract.py`)** is the highest-risk file. Anchor on `<h1>`, collapse
whitespace to single spaces, drop `form`/`input`/`label`/`select`, and cut at footer
markers only past `max(900, 45% of length)`. Three separate bugs came from this:
- one-token-per-line output made pages 90% blank lines, so chrome removal could not group
  the menu and mention counts were dominated by nav words
- a hidden "subscribe to newsletter" checkbox at char 475 truncated pages to 72 words
- the product mega-menu renders BEFORE `<h1>` on list pages, so an `<h1>` anchor kept
  every brand name 10-15 times. Sentence-split and skip the leading run of short
  menu-shaped fragments.

**Classification (`classify.py`)** scores TOFU/MID/BOFU/HUB/THIN by density, not raw
counts: a CTA phrase appearing once in a 2,000-word article is boilerplate, and the
footer puts the same CTA on every page. Use hits-per-1k-words and require the CTA to be
early in the body.

**Entities (`entities.py`)** learns the vocabulary from the site, with no client rules.
The chain that works: candidate slug cores -> drop question-shaped slugs (`what is`) ->
drop FURNITURE words -> require a dedicated hub page -> drop terms on >34% of pages ->
rank with a specificity multiplier. Skip a candidate if its first token is a verb or the
slug starts with an article word (`5 ways`, `how to convert`).

**Link plan (`plan.py`)** only suggests a link when the source page discusses the target
entity at least twice in prose AND does not already link to it. Cap at 3 per page. Fewer,
defensible suggestions beat a long list a client cannot act on.

## Non-negotiable checks

Run `verify_report.py` before calling any of this done. It asserts, at 1440 and 390:
tile count and canvas coverage, no clipped tile labels, no tile overlaps, no tile outside
the map box, 44px tap targets, worklist rows render, checkbox persists to localStorage,
progress readout updates, entity rows render, and zero console errors.

Then run the contrast/a11y audit at 1440, 1024 and 390 and require `0 fail 0 warn`.

## Pitfalls that cost hours

- **Squarified treemap:** verify the algorithm against exact area coverage and zero
  overlap over 500 random shapes plus one adversarial shape. The bug that survived a
  naive test was a single full-height column; random inputs never produced it. Remember
  each item's extent is `area / side`, not `area / thickness`.
- **Payload key drift:** pick one key style (short or long) in the payload and use it in
  the template. Mismatches surface as `undefined.split` crashes, not silent blanks.
- **Measure the DOM, not screenshots.** Vision cannot see an element that renders at
  `y=851` inside a 440px box if it is reading viewport-relative coordinates. Compare each
  tile against the map box's rect.
- **Pick ink by contrast, not luminance.** A colour ramp spans light and dark; compute
  both options and take the better WCAG ratio.
- **Legends must describe what is actually drawn.** If the legend lists funnel-role
  colours, draw a funnel-mix strip on every tile.

## Reporting honestly

State the crawl cap and whether the crawl was truncated. Never present a suggestion as
certain when it came from a heuristic. When the tool cannot infer entities for a site
(e.g. a site with no entity pages at all), say so as a finding rather than forcing output.
## Files

All code lives in `scripts/`. Run from that directory so the relative imports resolve:

| File | Role |
|---|---|
| `interlink_audit.py` | one-command entry point (crawl, plan, report, verify, audit) |
| `discover.py` | sitemaps + REST + crawl fallback, platform agnostic |
| `extract.py` | body/title extraction, footer and menu removal |
| `classify.py` | funnel role and page-quality signals |
| `entities.py` | learns entity vocabulary from the site's own slugs |
| `squarify.py` | treemap layout, with a 500-trial correctness self-test |
| `pipeline.py` | crawl orchestration, writes the bundle |
| `plan.py` | entities + competitive sets + ranked link worklist |
| `report.py` / `report_template.html` | renders the client report |
| `verify_report.py` | mandatory DOM gate, 21 assertions at two widths |

Run `python3 squarify.py` to confirm the layout algorithm before trusting any render.
