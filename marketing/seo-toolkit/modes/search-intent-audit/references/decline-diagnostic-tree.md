# Decline Diagnostic Tree

Symptom to cause mapping. Work top down. Each row gives the test that confirms
or eliminates the cause, so the audit produces evidence rather than opinions.

## Read the shape first

Plot 16 months of clicks, impressions, and average position together. The
relationship between those three lines identifies the cause faster than any
single metric.

| Pattern | Most likely cause | Confirming test |
|---|---|---|
| Daily and weekly swings, trend still up | Normal volatility | Compare the swing amplitude to the trailing 12-month band. If inside it, no action. |
| Gradual multi-month slope down | Intent decay, staleness, or displacement | Stage 2 scoring plus SERP entrant check (Stage 4) |
| Sharp cliff on one date | Technical or manual action | Check indexation, robots.txt, canonicals, redirects, deploy log for that date |
| Impressions flat, clicks down, position flat | SERP absorption (AI Overview, featured snippet, People Also Ask) or a title that stopped earning clicks | `gsc-ctr-by-position` against historical CTR at the same position; check live SERP composition |
| Impressions down, position flat | Query demand fell, or keyword set shrank | `keywords-explorer-volume-history` for seasonality or genuine demand decline |
| Position volatile, swapping between two URLs | Cannibalization | Map query to URL over time in `gsc-keywords`; look for the swap |
| One subfolder down, rest flat | Content set problem in that folder | Segment `gsc-pages` by path prefix |
| Whole site down evenly | Domain-level: trust, technical, manual action, or a core update | Check Search Console messages, indexation totals, and update timelines |
| Brand queries down too | Brand demand or reputation issue, not SEO | Compare brand vs non-brand splits |
| New pages ranking, old pages falling | Internal displacement or intent drift | Check whether new pages target the same queries |
| Everything down, conversions flat | The lost traffic never converted | Money map (Stage 1). This is often good news. |

## Seasonality guard

Before declaring any decline, compare against the same period last year, not
the previous month. B2B traffic drops in late December and mid-summer every
year. Presenting seasonal dips as crises destroys credibility, and the credibility
is what buys the budget for the real fixes later.

## Cliff checklist (run when the shape is a cliff)

Work through in order, stopping at the first confirmed hit:

1. `noindex` present on the affected templates (view the rendered HTML, not
   just the source).
2. `Disallow` rule added to robots.txt covering the path.
3. Canonical tags pointing to another URL or to a staging domain.
4. Redirects: a migration that mapped old URLs to a generic hub instead of
   like-for-like destinations.
5. Server errors or timeouts on the affected date range.
6. Hreflang or country targeting change.
7. CDN or firewall blocking Googlebot.
8. Manual action or security issue message in Search Console.
9. A confirmed core update on that exact date, checked last, and only accepted
   after the above are cleared.

## Slope checklist (run when the shape is a slope)

1. Score intent match on the top losing money pages (Stage 2).
2. Identify new SERP entrants over the same window (Stage 4).
3. Check content freshness: dates, statistics, product names, screenshots,
   pricing that no longer matches reality.
4. Check whether competitors expanded coverage of the query cluster while this
   site stood still.
5. Check internal linking: did a redesign remove the links that supported
   these pages?
6. Check the trust signals (Stage 3). Slow erosion often tracks a site that
   was refreshed into looking generic.

## The AI and LLM question

Users will ask whether AI is taking the traffic. Answer with data, not with
narrative.

- Top-of-funnel definitional queries lose clicks to answers rendered directly
  in search results and to assistants. Expect this. It is structural, not
  recoverable, and those clicks were the lowest value in the mix.
- Bottom-of-funnel commercial queries still send clicks, because people who
  are close to spending money want to see the vendor, the pricing, the proof,
  and the terms.
- Use `site-explorer-ai-responses-count` and the Brand Radar tools to measure
  actual citation share instead of guessing.
- The strategic response is not to fight for definitional clicks. It is to
  shift effort down-funnel, where the intent is commercial and the click still
  has to happen.

State this clearly when it applies: some of the lost traffic is not coming
back, and chasing it is a worse use of the quarter than deepening the pages
that convert.
