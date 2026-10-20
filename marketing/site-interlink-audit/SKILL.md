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
## Hard-won lessons (each one cost a debug cycle)

**Crawl**
- `build()` MUST be called with `keep_text=True`. Without it the bundle has zero body
  text, the entity layer finds 0 entities, and the report silently degrades to a link
  graph. `plan.py` now asserts text is present, so this fails loudly.
- A `keep_text` bundle is ~17 MB for 3,218 pages. Fine on disk; don't inline it in a
  report payload.
- Rewrite `pipeline.py` only between runs. Editing it while a crawl is in flight leaves
  the running process on stale code and its output bundle is lost.

**Entity extraction**
- Body extraction must anchor on PROSE DENSITY, not on `<h1>`. On list pages the nav
  mega-menu renders *before* the h1, so a h1-anchored extractor keeps the menu and
  destroys every mention count.
- Strip `<form>` controls before extracting text. A hidden subscribe checkbox sits at
  char ~475 of a Zendesk page and truncates a 2,964-word page to 72 words.
- A brand is a product name, not a lowercase-word test. `netsuite`, `hubspot` and
  `adobe` are single lowercase words. Invert the rule: GENERIC is a curated bad-word
  list, and a bare year is never an entity.
- A term on most pages is noise as a LINK TARGET even if it is a real brand (the footer
  brand turns up on 430 pages). Require targets to be distinctive.
- Rank by specificity as a MULTIPLIER, not additively. Additive weighting can never
  overcome mention counts that are two orders of magnitude larger.

**Treemap / labels**
- The `SHORT` map is the ONLY source of abbreviations. Adding a name to a different map
  silently falls through to the 4-char fallback, which renders `r` for "remaining".
- Design space is 1200 units wide. Convert to rendered px (`boxW / 1200`) before
  comparing any size floor, or a 23px sliver passes a 44px floor and fails the gate.
- Never pad a short tile list back to N with groups that FAILED the size floor. A sliver
  is worse than a missing tile; the tail bucket already accounts for what was folded.
- Fold tiny sections SERVER-side (a 1-page section beside an 800-page one cannot hold a
  label at any scale). Fold further CLIENT-side on rendered size.
- A synthetic tail tile built from the union of scattered rects is often a thin column.
  If the union is narrower than the floor, drop the tile rather than label it badly.
- A single long word cannot wrap: shrink its font BEFORE the candidate loop ellipsises it.
- Colour ramps must be CALIBRATED IN CODE, not by eye. Compute WCAG contrast for every
  step and check the worst point. A ramp that looks right tops out near 4.2:1.

**Verification**
- `verify_report.py` thresholds are smoke tests, not requirements. A site with 5 real
  sections is correct at 6 tiles. Assert "the map is populated and covers its canvas"
  rather than a magic tile count.
- A site with zero suggestions legitimately renders zero rows. Assert rows OR an empty
  state, never rows alone.
- Add an explicit "no ellipsised tile label" assertion. An ellipsis reads to a client as
  broken text even though the verifier's own clip check passes.

## Refresh, related links, CLEF, and the on-site widget

Four commands, one crawl. See `PLATFORM.md` for the full guide.

```bash
python3 refresh.py --list sites.txt     # refresh every site in a drop-in list
python3 refresh.py --all                # re-audit stored bundles, crawl nothing new
python3 semantic.py bundle-<site>.json  # related links beyond same-technology
python3 component.py --bundle bundle-<site>.json   # the embeddable carousel
```

`refresh.py` reuses a cached crawl unless `--force`, rebuilds four artefacts per site
(plan, report, related links, widget), writes `refresh-summary.json`, and exits non-zero if
any site fails. It takes a lock so two refreshes cannot interleave.

### Related links, not just same-technology

`semantic.py` finds the links nobody has thought of: "Data Cleansing -> What is Data
Cleansing?", "Healthcare List -> What is a Healthcare Email List?". TF-IDF over body and
title (never the URL, which rewards slug similarity over content), nearest neighbours via
an inverted index over discriminating terms. 3,218 pages in ~35s; an O(n^2) scan took 4m18s.

Bands, not magnitudes: `strong` / `likely` / `possible` / `weak`. Every suggestion carries a
written reason.

Three rules keep the shortlist honest:

- **One direction per pair.** "A links to B" and "B links to A" are one editorial decision.
  19% of candidate rows were the mirror of another row (1,393 on LakeB2B), which crowded the
  top of the list with mirrors of itself. Keep the higher-scoring direction and flag the rest
  `link_back_too`.
- **`link_back_too` is built from source counts, not the score.** The rule score is symmetric
  in A and B by construction, so "the reverse also scored well" was true for every mirrored
  pair and carried no information. It now means both pages are suggested from three or more
  different sources.
- **A conversion page can be a target but never a source.** `/free-trial`, `/demo`,
  `/contact` and `corporate_brochure` pages are legitimate link destinations and terrible
  places to host an editorial reference. `usable()` gates targets; `can_host()` gates
  sources.

### CLEF is optional and gated

Cloudflare CLEF is a SystemOne-API decision model (Apache 2.0). Full weights are **55 GB**
and `clef-flash` is **19 GB**, so neither fits a laptop disk; Workers AI serves the same API
for pennies. Modes: `none` (rules only, fully functional), `hosted`
(`CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID`), `local` (`CLEF_PATH`).

```bash
python3 semantic.py bundle-<site>.json   # prints: clef mode: none | hosted | local
```

All questions go out in ONE batched request. Blend once, keep the rule score in its own
column, and never let a missing judgement outrank a judged one.

### The on-site component

`component.py` emits `related-sites.html` + `related-sites.js`. The page announces itself
via a meta tag and the widget scores `catalog.json` against it at runtime. Never recommends
the site you are already on. Themable through CSS custom properties (`--rsw-bg`, `--rsw-fg`,
`--rsw-mut`, `--rsw-line`, `--rsw-acc`, `--rsw-face`).

## What an adversarial review caught, and how it is fixed

Every item below was found by an external review of the Span report and is now a regression
test in `test_units.py` (`t_adversarial_review`). The pattern: a headline number or a
matching rule that was confident and wrong.

- **A scary orphan rate was mostly one low-value folder.** "76% invisible" was 2,024 of
  2,434 unlinked pages sitting under `/faq/`. The summary now reports `faq_pages`,
  `pages_ex_faq` and `zero_in_ex_faq` so the finding can state both rates, and the headline
  names the split. Never quote a site-wide orphan rate without saying what is in it.
- **Menu links were deleted, then the report called the result invisible.** `boilerplate`
  removed any target linked from a large share of pages, which included every menu
  destination, so menu-linked pages scored zero inbound while being perfectly reachable.
  Boilerplate is now position-based: a recurring target is furniture only if it also sits in
  nav/header/footer/aside. Degree is reported three ways: `in`, `in_content`, `in_menu`.
- **A whole content area sat outside the sitemap index.** The Span blog has 1,613 posts in
  `/blog/sitemap_index.xml`, referenced by neither `sitemap_index.xml` nor `robots.txt`, so
  the crawl saw 4 blog pages and concluded there was no research layer. `discover_sitemaps`
  now probes conventional out-of-index names.
- **Entities were matched on single words, so links followed the word not the topic.**
  Fixed with ownership as the governing rule: a name that has its own product page is an
  entity, whatever its shape or frequency. This admits `aws` and `sap` (three letters, on
  58% and 63% of pages) and still rejects `chief`, `health` and `account`, which own nothing.
- **The pages that drive revenue were missing from the entity set.** `MAX_CLUSTER_MEMBERS`
  stops one geography cluster from eating 12 of 60 slots, capped clusters emit the remainder
  as singletons so nothing is dropped, and owned names are promoted past the cap. Span went
  from 60 entities to 319 with ServiceNow, Salesforce, AWS, SAP, Workday and Five9 present.
- **List product pages were labelled research pages.** `role_from_url()` overrides the text
  classifier on URL shape: anything under a list directory is commercial, `/blog/` is TOFU,
  white papers and guides are MID. A page that sells a list is BOFU whatever its copy says.
- **The worklist fed pages that were already well linked.** Targets are now scored by
  inbound: an orphan target is worth 3x, one with 200 inbound is damped to 0.35x.
- **Redirecting targets reached the worklist.** The check compared a normalised URL against
  a raw key and never matched, so it looked like it worked while doing nothing. Redirect keys
  are normalised on entry, targets are dropped, and `redirecting_targets` reports what was
  dropped so nothing disappears quietly.

- **Ownership must mean a real hub, not a string match.** Fixing the money pages with an
  ownership rule created a second defect: a name "owns" a page when its slug appears in that
  page's URL, so `from` owned `/case-studies/from-dormant-data-to-349k-in-revenue`, `key`
  owned the SurveyMonkey page, `thanks` owned `/thanks`, `web` owned `/webinars` and `sgs`
  owned the corporate brochure. Half the worklist was junk. `owns_a_hub()` now requires a
  topic page: not a question-shaped slug, not an FAQ/white-paper/case-study/brochure
  section, not an append service, not a utility leaf. Section names are normalised because
  they arrive hyphenated, underscored or spaced depending on the theme, and the site's own
  name is never one of its topics.
- **Function words and UI words are never topics.** `FUNCTION_WORD` and `GENERIC_WORD` cover
  prepositions, question words and courtesy words. Splitting a slug on hyphens and stripping
  the page-type tail leaves the preposition behind, so `from-dormant-data-to-349k` yields
  `from`. This is the rule to check first when a suggested entity sounds absurd.

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
