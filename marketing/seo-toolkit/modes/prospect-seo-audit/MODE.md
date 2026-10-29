# Mode: prospect-seo-audit

Use when a site is a sales prospect (no Search Console access, no decline to diagnose) and the deliverable is an audit Champions can send after review. Output is the `site-growth-audit` document shape (damage control first, findings with evidence, "already fine", phase table, undecided list, not checked), so read that skill for the document; this mode is the evidence-gathering procedure that fills it.

## Procedure (about 15 minutes, all from the terminal)

1. Headers and doors: `curl -sI https://site/` plus `curl -s -o /dev/null -w '%{http_code}' http://site/` and one bogus URL. http returning 403 or a soft 200 on bogus URLs is a damage-control row. Always send a browser User-Agent; export-SaaS hosts (waimaoniu, made-in-china builders) 403 bare curl.
2. `python3 scripts/crawl_sitemap.py https://site/ build/`. Crawl every sitemap URL, not the homepage: the big defects (duplicate SKU pages, tag-page bloat, templated descriptions) are invisible from one page. Keep `build/raw/` so every number in the audit has a file behind it.
3. Read `crawl.json` for three things in this order: identical bodies or duplicate title pairs (cannibalisation), URL prefix counts (`product-tag-*` at 300 words each is index bloat), and the share of pages carrying one boilerplate description.
4. hreflang: grep the homepage for `hreflang`, then curl every alternate on both schemes. Tags pointing at http:// or at hosts that fail on https are a damage-control row, not a technical footnote.
5. Schema: count `application/ld+json` types across the crawl. One Organization block on every page and nothing else means rich results are impossible; say that, do not list the missing types as nice-to-haves.
6. Analytics presence: grep for `gtag|googletagmanager|google-site-verification`. Absence is the finding "nobody at the prospect can see what works" and it becomes Phase 0 of the plan (baseline before any fix).
7. Live SERP snapshot: `web_search` the 3 to 4 head terms the prospect's own titles target, top 6 each, in a table of who ranks and whether the prospect appears. Label it a snapshot with the date. Note the content pattern of the winners (price guides, cost comparisons) because that becomes the content tier of the offer.
8. If the prospect sells SKUs, build `catalog.json` from the raw pages (code, family, specs, images, legacy duplicate URLs) and a `redirects-legacy.json`. The dedupe count is a headline number and the redirect map is a free deliverable.

## Rules

- No Ahrefs connected means no volume numbers. Say "not checked: backlinks and volumes" rather than estimating.
- Pitch tiers go in the document (rebuild, 90-day foundation, per-market retainer) with proof-of-done per tier and no traffic or ranking promise.
- The audit markdown is the source of truth; a branded HTML or PDF render is a separate frontend-lane card that must preserve every number and section order.
