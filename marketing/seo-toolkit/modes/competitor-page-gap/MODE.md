# Mode: competitor-page-gap

Use when the ask is "what is this competitor winning that we are not", "reverse engineer their SEO", or "what should we publish next against them". Output is a ranked list of winnable searches and one brief per pick. It is never an autopublish loop.

Origin: a Distribb Short (youtube.com/shorts/tWnh2erSgrk). Its method is sound; its product pitch (calendar published on autopilot) is not adopted. Its stat, 96.55 percent of pages get zero Google traffic, is real but is Ahrefs' 2023 study of about 14 billion Content Explorer pages, a sample the study itself calls biased toward the quality side of the web.

## Procedure

1. **Page set, free.** Fetch `/sitemap.xml` (and each child map if it is an index). Run `scripts/crawl_sitemap.py https://competitor/ build/`. It records every URL, title, H1, word count, schema, and `lastmod` where the map carries one. A missing `lastmod` is a finding, not a gap in your data: use the Wayback or the page's own `dateModified` instead and label it.
2. **Where the traffic sits, Ahrefs.** Call the doc tool first (kebab-case names such as `site-explorer-top-pages`), then `SITE_EXPLORER_TOP_PAGES` for the competitor with `mode=subdomains`, `order_by=sum_traffic:desc`, `limit` 30 to 50. Every call costs at least 50 API units and many columns cost 10 per row, so select only `url,top_keyword,top_keyword_best_position,sum_traffic,keywords` and say how many units were spent. An empty result means the domain has no ranked pages in that country's index, not that the call failed.
3. **Their searches, our absence.** For the top pages, pull `SITE_EXPLORER_ORGANIC_KEYWORDS` filtered to positions 1 to 10 for the competitor, then check our domain on the same keywords. Keep only keywords where we do not rank in the top 100.
4. **Triage before briefing.** Drop: brand terms, searches whose intent we cannot serve with a real asset, and anything where the top results are all forums, official docs or large publishers we cannot out-source. Keep a pick only if we hold first-hand material (a number, a file, a worked example) the competitor page lacks. Mark each pick winnable, stretch or skip with one line of why.
5. **One brief per pick.** Search intent, the one question the page answers in its first 100 words, our proof asset, internal links in and out, the money page it feeds (see the Money Page Register). Hand writing to `deep-social-voice` or the brand's own voice skill, never to a bulk generator.
6. **Report.** Table of picks with volume, difficulty, their URL, their last change, our asset. State units spent, the date, and the country.

## Rules

- Do not publish or schedule from this mode. A person approves each page. Mass AI-written pages risk Google's scaled-content spam policy (from general knowledge, not rechecked here); the safe unit is one page with a proof asset.
- Competitor sitemaps and public pages only. Respect robots.txt on any fetch beyond the sitemap.
- Label every volume and difficulty number as an Ahrefs estimate. No ranking or traffic promise.
- The video says to add an SEO connector in Claude. Ahrefs is already connected here; no new connector or vendor account is needed to run this mode.
