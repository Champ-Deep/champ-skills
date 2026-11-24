# Ahrefs MCP calls: cost discipline and what each result means

Use whenever a mode needs Ahrefs data (competitor traffic, keyword gaps, does a domain rank at all). Read before making any call: every call costs real money out of one shared account, so the cheap path is the correct path.

## Call order

1. **Read the tool's own schema before composing arguments.** Ahrefs tools appear as description documents first (search by capability, e.g. `site-explorer-top-pages`), then as invocable calls with UPPER_SNAKE names (`SITE_EXPLORER_TOP_PAGES`). Guessing a parameter name wastes a call and burns the floor cost; loading the description costs nothing.
2. **One narrow question per call, `select` restricted to the fields that answer it.** Default column sets are priced per row, so a wide `select` on a 50-row limit is the expensive way to read three fields. `url,top_keyword,top_keyword_best_position,sum_traffic` answers "where does their traffic sit"; `competitor_domain,domain_rating,keywords_common,traffic` answers "who else competes".
3. **Always send `country` and `date`.** Traffic and rank are per country and per day. A result without both cannot be quoted, and a later session cannot reproduce it.
4. **One domain, one market, then stop and read.** Do not fan the same call out across six domains for "coverage" before checking whether the first answer was useful.

## What an empty result means

`pages: []` or `competitors: []` with `successful: true` is a **finding, not an error**: the domain has no ranked pages in that country's index on that date. Report it as "no footprint in the index (country, date)", never as "not indexed", "not ranking on Google" or "the call failed". The index is Ahrefs' own, and it is not a Google SERP.

## Always label

- Volumes, difficulty and traffic are Ahrefs estimates. Say so in the sentence, not in a footnote.
- A rank or competitor claim carries its country and date.
- An index result is index-based evidence; a `web_search` snapshot is a named engine's result; neither is a confirmed Google result. Keep them in separate rows and name the source of each.

## Pair the two evidence sources

Ahrefs answers *does anything rank, and what earns the traffic*. `scripts/crawl_sitemap.py` answers *what the page actually says*: titles, descriptions, schema, `lastmod`, redirects, canonicals. Crawl the site itself, use Ahrefs for its search footprint, and report both numbers with their source; a claim that mixes them ("the site has no traffic" from an empty keyword table) overstates what was measured.
