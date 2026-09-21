---
name: search-intent-audit
description: >
  Diagnose why organic traffic or rankings are declining by auditing search
  intent match first, before blaming algorithm updates, AI Overviews, or LLMs.
  Runs a five-stage audit: decline triage (volatility vs real loss, money pages
  vs top-of-funnel noise), searcher's-eye intent scoring above the fold,
  AI-look trust gap assessment, SERP displacement check, then structural causes
  (subfolder isolation, cannibalization, indexation errors). Outputs an Intent
  Match Score per page and a revenue-ranked fix queue.
  MANDATORY TRIGGER for: "traffic is declining", "organic traffic dropped",
  "why did we lose rankings", "search console is down", "did the algorithm hit
  us", "losing traffic to AI", "search intent audit", "does this page match
  intent", "clicks falling", "impressions up clicks down", "cannibalization
  check". Full trigger list in assets/triggers.md. Use it even when the user
  just pastes a URL and says traffic is down. Diagnosis skill: hand fixes to
  seo-rapid-ranker, paa-seo-builder, or page-refresh.
---

# Search Intent Audit

The diagnostic counterpart to `seo-rapid-ranker`. That skill makes a page rank
faster. This one explains why a page, folder, or site stopped ranking, and
proves it with evidence instead of vibes.

**Methodology credit:** adapted from Edward Sturm's breakdown of declining SEO
traffic, extended into a repeatable audit workflow with scoring, tooling, and
a fix queue.

## The core principle

Before reaching for a complicated explanation (core update, AI Overviews,
LLM cannibalization, "Google hates us"), look at the page the way a searcher
does. Three questions decide most cases:

1. Does this page answer what the person actually searched for?
2. Does it answer fast?
3. Is the answer obvious above the fold, before any scrolling?

Google's ranking systems have tightened around user signals. A page that makes
someone scroll past 400 words of throat-clearing to find the answer loses those
signals, then loses the position, then loses the traffic. Most "algorithm
victims" are intent failures wearing a costume.

Corollary: **not all declines are equal.** Losing top-of-funnel informational
clicks that never converted is not the same emergency as losing a page that
generates pipeline. Segment before you panic.

## When to use this vs other skills

| Scenario | This skill | Other |
|---|---|---|
| "Traffic is down, why?" | Yes | - |
| "Make this page rank faster" | No | seo-rapid-ranker |
| "What questions should this page answer?" | Partly (Stage 2) | paa-seo-builder |
| "This page looks bland/AI-made" | Diagnose only (Stage 3) | page-refresh, design-trends |
| "Write the replacement content" | No | b2b-blog-writer |
| "Full technical site crawl" | Stage 5 only | ahrefs site-audit tools |

Run this first. It tells the others what to do.

## Inputs to gather

Ask only for what is missing, then start. Do not block the whole audit on
perfect inputs.

1. **Property or URL(s)** in scope: whole site, a subfolder, or specific pages.
2. **What is declining**: clicks, impressions, positions, conversions, or "not
   sure, Search Console just looks bad".
3. **Timeframe**: when it started, and whether it was a cliff or a slope.
4. **Money pages**: which URLs actually generate leads, demos, or revenue.
   If the user does not know, infer from URL patterns (service, solution,
   pricing, list, product, contact) and confirm.
5. **Access**: is Google Search Console connected through the Ahrefs MCP, or
   will the user paste exports?

## Tooling preflight

Check what is available and say what you will use before you start.

- **Ahrefs MCP, GSC tools** (preferred for decline evidence):
  `gsc-performance-history`, `gsc-pages`, `gsc-page-history`, `gsc-keywords`,
  `gsc-keyword-history`, `gsc-positions-history`, `gsc-ctr-by-position`,
  `gsc-anonymous-queries`, `gsc-metrics-by-country`.
- **Ahrefs MCP, market data**: `site-explorer-organic-keywords`,
  `site-explorer-top-pages`, `site-explorer-metrics-history`,
  `site-explorer-organic-competitors`, `serp-overview`,
  `site-explorer-ai-responses-count` (LLM citation share),
  `site-audit-issues`, `site-audit-page-explorer`.
- **Firecrawl skill**: read the target page and the top three ranking
  competitors as raw content. Never audit a page from memory or from a
  meta description.
- **web_search**: check the live SERP for new entrants, AI Overview presence,
  and what format Google is currently rewarding.

If no data access exists, run Stages 2 and 3 on the page content alone and say
plainly which conclusions are unverified.

---

## Stage 0: Triage the decline

Goal: separate normal volatility from a real loss. Read
`references/decline-diagnostic-tree.md` for the symptom-to-cause map.

1. Pull 16 months of performance history. Compare like-for-like periods, not
   month-over-month against seasonality.
2. Classify the shape:
   - **Noise**: daily or weekly swings inside the historical band, trend still
     up. Verdict: no action, stop the panic, show the trendline.
   - **Slope**: gradual multi-month erosion. Usually intent decay, competitor
     displacement, or content going stale.
   - **Cliff**: sharp single-date drop. Usually technical (indexation,
     migration, robots.txt) or a manual or algorithmic action.
   - **Split**: impressions steady, clicks down. Usually SERP feature or AI
     Overview absorption, or a title and snippet that stopped earning the click.
3. State the verdict in one line before going further.

## Stage 1: Segment the loss (the money map)

Never report a sitewide number. Break the loss into four buckets and quantify
each:

| Bucket | Definition | Weight |
|---|---|---|
| Money pages | Pages that produce leads, demos, signups, sales | Critical |
| Commercial support | Comparison, alternatives, pricing, case studies | High |
| Brand and navigational | Brand terms, homepage, about | High if declining |
| Top-of-funnel informational | Definitional, "what is", general how-to | Low |

Rules:

- If the loss is concentrated in top-of-funnel informational and money pages
  are flat or up, the correct verdict is often "this is fine, and here is the
  proof". Say so. Those clicks are increasingly answered inside search results
  and by LLMs, and they rarely converted anyway.
- If money pages are declining, everything else in the report is secondary.
- Check whether the informational decline is a leading indicator: is the same
  erosion starting to touch commercial pages? If yes, escalate.
- Also check for isolation: is the loss confined to one subfolder or spread
  across the site? A subfolder-only loss points at that content set. A sitewide
  loss points at technical, trust, or domain-level causes. This is exactly why
  siloed subfolder architecture beats flat architecture: it makes decline
  diagnosable.

## Stage 2: The searcher's-eye intent audit

The heart of this skill. For each priority page, load the live page with
Firecrawl and score it against `references/intent-scoring-rubric.md`.

Audit sequence per page:

1. Identify the **primary query** the page actually ranks for (GSC, not the
   keyword the team hoped for). Note the intent type: informational,
   commercial investigation, transactional, or navigational.
2. Compare intent type to page type. A transactional query landing on a
   1,800-word blog essay is an intent mismatch no amount of optimization fixes.
3. Run the **above-the-fold test**: from the first screen alone, is the core
   answer present, or does the searcher have to scroll? Count the words before
   the first substantive answer. Anything over roughly 60 words of preamble
   is a fluff tax.
4. Run the **completeness test**: does the page fully resolve the query, or
   does it answer half and leave the rest to a CTA?
5. Run the **speed-to-value test**: how many seconds to the answer, including
   cookie banners, popups, hero video, and interstitials.
6. Compare against the top three ranking competitors: what do they answer that
   this page does not, and how fast do they get there?

Output an Intent Match Score out of 100 per page with the five component
scores, plus the single highest-leverage fix.

## Stage 3: The trust gap (the AI-look problem)

Content quality is no longer sufficient if the page reads and looks
machine-produced. Searchers are getting fast at spotting it and they bounce
before evaluating the substance. That bounce is a user signal.

Score the page against `references/trust-signals-checklist.md`. The tells are
both visual (identical gradient hero, purple-blue default palette, emoji
bullet lists, three-card feature grids, stock illustration) and textual
(hedged generalities, no named source, no original number, no author, no date,
no first-hand evidence).

Report this as a Trust Gap Score with specific tells cited. Do not soften it.
If the page looks vibecoded, the fix is design plus proof, and it routes to
`page-refresh` or `design-trends`, not to more words.

## Stage 4: SERP displacement

Someone may simply be beating the page. Verify before assuming decay.

1. Pull the current SERP for the primary query and the top three secondary
   queries.
2. Identify entrants that were not there before, using
   `serp-overview` and `site-explorer-organic-competitors`.
3. For each displacer, note what they do better: faster answer, tighter
   keyword-to-page relevance, more specific page type, fresher data, stronger
   proof, better link profile.
4. Check SERP composition change: new AI Overview, more ads, a video pack, a
   forum block, or a shopping unit compressing organic real estate.
5. Note whether the query is now being answered inside the SERP. If so,
   position stability with click loss is expected, and the strategic answer is
   to move down-funnel, not to fight for the click.

## Stage 5: Structural and technical causes

Only after intent and competition have been examined. Check in this order:

1. **Cannibalization**: multiple URLs competing for the same query, splitting
   signals and confusing the ranking systems. Detect via `gsc-keywords` mapped
   to pages, or `site-explorer-organic-keywords` grouped by keyword. Flag any
   keyword where two or more URLs have swapped positions over time. Fix by
   consolidating, differentiating intent, or canonicalizing.
2. **Indexation errors**: accidental `noindex`, a `Disallow` in robots.txt, a
   canonical pointing elsewhere, a stray staging block after a deploy. These
   produce cliffs.
3. **Topical dilution**: large volumes of thin, off-topic, or programmatic
   pages muddying what the site is about. Recommend pruning or noindexing
   pages that are neither relevant to the core business nor earning traffic.
4. **Architecture**: flat structure that prevents folder-level diagnosis and
   dilutes internal link equity. Recommend siloing.
5. **Standard technical**: Core Web Vitals, mobile rendering, broken internal
   links, redirect chains from a migration. Pull `site-audit-issues`.

---

## Scoring model

Report three numbers per audited page, plus one verdict:

- **Intent Match Score** (0-100): from the rubric, five components.
- **Trust Gap Score** (0-100, higher is better): from the checklist.
- **Displacement Risk** (Low, Medium, High): based on Stage 4.
- **Verdict**: one of `Fix intent`, `Fix trust and design`, `Fix technical`,
  `Consolidate cannibalization`, `Accept and redeploy` (the query moved
  down-funnel or into the SERP itself, so the honest answer is to stop
  chasing it), or `No action, normal volatility`.

## Output format

Default to a markdown report in chat for a single page, and a file for
multi-page audits. Use `references/report-template.md` for the structure.

Ask before building anything heavier: "Markdown report, or a client-ready HTML
report page?" If HTML, hand off to `visual-report-builder` with the audit
content, and follow with `visual-verify`.

Every report ends with the **Fix Queue**: a table ranked by revenue impact
divided by effort, not by severity. Columns: URL, verdict, single highest-
leverage fix, expected effect, effort (S/M/L), owner, target skill to execute.

## Handoffs

- Intent and content fixes: `seo-rapid-ranker`
- Missing questions and FAQ architecture: `paa-seo-builder`
- Page looks bland or AI-made: `page-refresh`, then `design-trends`
- Rewrite or replacement content: `b2b-blog-writer`
- Client-facing report: `visual-report-builder`, then `visual-verify`
- Proof and credibility gaps: `case-study-builder`

## Guardrails

- **Never use em dashes** in any output. Use commas, periods, parentheses, or
  colons.
- Never attribute a decline to a core update without dated evidence that the
  drop aligns with a confirmed update and that intent, competition, and
  technical causes have been ruled out. "It was the algorithm" is the last
  explanation, not the first.
- Never audit a page from its meta description or from memory. Fetch it.
- Quantify everything. "Traffic is down 12 percent, and 91 percent of that
  loss is one informational subfolder" beats "traffic is down".
- If the honest answer is "this decline does not matter", say that first and
  defend it with the money map. Manufacturing an emergency to look useful is
  the failure mode here.
- Cite the timeframe and data source for every number.
