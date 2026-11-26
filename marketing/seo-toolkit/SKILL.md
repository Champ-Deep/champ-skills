---
name: seo-toolkit
description: >-
  SEO in one toolkit, six modes: PAA/FAQ hub architecture, rapid rank for a single page, search intent audit for traffic or ranking decline (intent match, trust gap, SERP displacement, cannibalization), competitor page gap, personal brand SEO, prospect site audit. MANDATORY TRIGGER for: "PAA strategy", "People Also Ask", "FAQ SEO", "FAQ hub", "answer engine optimization", "rank this page", "rank faster", "outrank competitors", "why am I not ranking", "competitive gap", "quick SEO fix", "SEO sprint", "traffic is declining", "organic traffic dropped", "why did we lose rankings", "did the algorithm hit us", "losing traffic to AI", "impressions up clicks down", "cannibalization check", or a pasted URL with traffic down. Also MANDATORY TRIGGER for rendering/indexability: "CSR or SSR", "missing without JS", "empty shell", "soft 404", "is this page crawlable". Replaces paa-seo-builder, seo-rapid-ranker and search-intent-audit.
---

# SEO Toolkit

| Mode | Use when | Read |
|---|---|---|
| **search-intent-audit** | Traffic or rankings are falling. Diagnose first; this mode hands fixes to the other two | `modes/search-intent-audit/MODE.md` |
| **seo-rapid-ranker** | One page needs to rank higher soon. Tactical, page-level, this week | `modes/seo-rapid-ranker/MODE.md` |
| **paa-seo-builder** | A site or topic needs a question-led content architecture. Strategic, multi-page | `modes/paa-seo-builder/MODE.md` |
| **competitor-page-gap** | What is a named competitor winning that we are not? Sitemap plus Ahrefs top pages, ranked picks and briefs, never autopublish | `modes/competitor-page-gap/MODE.md` |
| **personal-brand-seo** | A person wants to own their name and show up in answer engines. Name SERP, entity basics, owned-site crawl, AI crawler policy as a decision | `modes/personal-brand-seo/MODE.md` |
| **prospect-seo-audit** | A sales prospect's site, no analytics access, deliverable is an audit Champions sends after review. Evidence procedure plus `scripts/crawl_sitemap.py`; document shape comes from `site-growth-audit` | `modes/prospect-seo-audit/MODE.md` |

## Routing

Decline or loss in the ask means start with `search-intent-audit`, even if the user asks for a fix. A single named page with no decline means `seo-rapid-ranker`. A domain plus seed keywords, or anything about FAQ hubs and PAA, means `paa-seo-builder`. A prospect or pitch ("audit this company's site", "what can we do for them") means `prospect-seo-audit`: crawl every sitemap URL before writing a word, the homepage alone hides duplicate SKU pages, tag-page bloat and templated descriptions. When a mode file says to hand off to another of these skills, read that mode file here. "What is a competitor winning" or "reverse engineer their SEO" means `competitor-page-gap`. "My name", "personal brand" or "how do I show up for myself" means `personal-brand-seo`. Use Ahrefs data where connected; label anything estimated. Before any Ahrefs call, read `references/ahrefs-mcp.md`: load the tool description first, keep `select` narrow because a call costs a floor price plus a charge per row, and read an empty result as "no footprint in the index (country, date)" rather than as a failed call or a Google ranking claim.

**Reading crawl output** (`scripts/crawl_sitemap.py`): judge a canonical against the URL the page *lands on*, never the requested one, because the crawler follows redirects silently. A site that 307s every sitemap entry to a trailing-slash form therefore produces two counts, and only "differs from final url" is the defect; "differs only by trailing slash" is a URL-forming inconsistency. A sitemap whose entries all redirect is its own finding: a hop per crawl, and no `lastmod` to carry freshness. When a site has no `lastmod` at all, take dates from the page's own `dateModified` or a Wayback capture and label the source instead of dropping the freshness check.

**AI brand claims** (claiming our brands in ChatGPT's Business Hub or any AI answer surface, multi-brand rollout for Champions): `references/ai-brand-claims.md`. Also route any third-party marketing video or thread asking "should we do what this claims" to step 1 of that file: verify against the platform's own policy text first, then split it into confirmed, overstated and unknown.

**Standing technical floor (SSR/SSG and vibe-coded SEO pitfalls):** Every mode here defaults to SSR or build-time SSG/prerendering for public, indexable pages (never bare client-rendered SPAs) and audits against the vibe-coded SEO pitfalls and 5-command raw-HTML `curl` gate in `references/ssr-seo-hygiene.md` (empty JS shells, soft-404 SPA fallbacks, client-mutated meta/canonicals, `<div onClick>` navigation, split-text H1s, `opacity: 0` or canvas-trapped copy, accidental `noindex`, sitemap/redirect drift, invalid JSON-LD, swapped-noun thin pages).
