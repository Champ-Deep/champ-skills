---
name: span-interlink-architecture
description: Crawl, graph and interlink plan for spanglobalservices.com; reusable method for the three-layer TOFU/BOFU/moat architecture on B2B data-vendor sites.
---

# Span Global Services interlink architecture

Deep's site is a B2B data vendor: technology "users list" pages plus a huge FAQ corpus. He wants
each technology to have a real editorial page that feeds the commercial page, and he wants the
whole structure visible and clickable rather than described in prose.

## Deliverable

`/Users/deep/Apps&Projects/span-sitemap.html` (self-contained, no network calls), built by
`build_app.py` in the scratch dir. Three views: **Site map** (squarified treemap by section plus
a full page list), **Entity graph** (185 technologies, existing vs suggested links, click a node
for its plan), **Link queue** (1,125 suggestions grouped by the page you would edit, tickable,
persisted to localStorage).

## The architecture the data supports

- L1 TOFU: editorial research page per technology (what it is, pros, cons, comparisons,
  alternatives, reviews, pricing).
- L2 BOFU: the commercial users-list page.
- L3 moat: competitor siblings, adjacent-intent pages, and the tech's owned FAQ pages.

Headline findings: 3,163 live pages vs 946 in the sitemap; 2,036 FAQ pages of which **100% have
zero inbound links**; 0 of 185 technology pages contain pros-and-cons content; 7 entity pages are
fully stranded. Sitemap URLs 301 into `/technology-lists/`, which the sitemap omits entirely.

## Method worth reusing

1. Pull every child sitemap, then get the true inventory from the WordPress REST API
   (`/wp-json/wp/v2/<type>?per_page=100`, paginate). The XML sitemap is badly stale.
2. Crawl all pages, strip boilerplate by identifying repeated link sets, not by tag names.
   Their theme is Bootstrap with the menu in `div.sub-menu` and `.sgs-tabx`, NOT `<nav>`,
   and there is no `<main>`, so anchor body extraction at `<h1>`.
3. Normalise entity names with word-boundary slug matching. A substring match filed `aws`
   under `lawson-erp`.
4. Roll geo variants up to the parent brand, stripping the geo tail BEFORE the page-type suffix
   (`netsuite-users-in-new-york` -> `netsuite`, not `netsuite-users`).
5. Classify families by scoring all matches, not first-match-wins. NetSuite matched CRM before
   ERP and dragged every Dynamics ERP variant with it.
6. Score every suggestion on whether the target can answer a reader who just arrived, then group
   by source page so the output is an editing plan.

## Verification discipline that actually caught things

Measure the DOM; do not trust a screenshot or a passing unit test. Every one of these was a real
bug found only by measurement: `n.fx/n.fy` never assigned so all coordinates were NaN; button
ids using hyphens while the lookup used underscores, so every filter fell through to "show all";
`min-width:74px` overriding computed treemap tiles; `blend()` returning `#7f1d3aNaNNaNNaN` because
it was handed an `rgb()` string; family headers reserved at 136px while rendering 40px wide.

Force layouts do not converge to zero overlap. Strengthening repulsion made it worse (20 -> 40
overlaps). Resolve it as a discrete constraint in a post-pass, with the anchor pull annealed to
zero on the final passes, then sweep labels through one shared collision test with a real gutter.

Run `audit.py` at 1440, 1024 AND 390. Mobile finds separate defects: 44px tap targets, and iOS
zooms on inputs below 16px.

## Verifying a graph app

See [[interactive-graph-app-verification]] for the reusable checker.
