---
name: seo-toolkit
description: >-
  SEO in three modes: (1) People Also Ask strategy: harvest PAA questions, topic clusters, FAQ hub architecture, briefs and roadmap for a domain; (2) rapid rank: page-level competitive gap, question optimization and internal linking to lift one page fast; (3) search intent audit: diagnose traffic or ranking decline by checking intent match first, AI-look trust gap, SERP displacement, cannibalization and indexation, with an Intent Match Score and a revenue-ranked fix queue. MANDATORY TRIGGER for: "PAA strategy", "People Also Ask", "FAQ SEO", "FAQ hub", "answer engine optimization", "rank this page", "rank faster", "outrank competitors", "why am I not ranking", "competitive gap", "quick SEO fix", "SEO sprint", "traffic is declining", "organic traffic dropped", "why did we lose rankings", "did the algorithm hit us", "losing traffic to AI", "impressions up clicks down", "cannibalization check", or a pasted URL with traffic down. Replaces paa-seo-builder, seo-rapid-ranker and search-intent-audit.
---

# SEO Toolkit

| Mode | Use when | Read |
|---|---|---|
| **search-intent-audit** | Traffic or rankings are falling. Diagnose first; this mode hands fixes to the other two | `modes/search-intent-audit/MODE.md` |
| **seo-rapid-ranker** | One page needs to rank higher soon. Tactical, page-level, this week | `modes/seo-rapid-ranker/MODE.md` |
| **paa-seo-builder** | A site or topic needs a question-led content architecture. Strategic, multi-page | `modes/paa-seo-builder/MODE.md` |
| **prospect-seo-audit** | A sales prospect's site, no analytics access, deliverable is an audit Champions sends after review. Evidence procedure plus `scripts/crawl_sitemap.py`; document shape comes from `site-growth-audit` | `modes/prospect-seo-audit/MODE.md` |

## Routing

Decline or loss in the ask means start with `search-intent-audit`, even if the user asks for a fix. A single named page with no decline means `seo-rapid-ranker`. A domain plus seed keywords, or anything about FAQ hubs and PAA, means `paa-seo-builder`. A prospect or pitch ("audit this company's site", "what can we do for them") means `prospect-seo-audit`: crawl every sitemap URL before writing a word, the homepage alone hides duplicate SKU pages, tag-page bloat and templated descriptions. When a mode file says to hand off to another of these skills, read that mode file here. Use Ahrefs data where connected; label anything estimated.
