# Audit Report Template

Use this structure for every audit. Fill only the sections the evidence
supports, and delete the rest. A short report backed by data beats a long one
padded with maybes.

Remember the output rule: no em dashes anywhere.

---

## 1. Verdict (three lines maximum)

Lead with the answer, not the methodology.

> Traffic is down 18 percent over 90 days. 84 percent of that loss sits in
> /blog/ definitional posts that produced 2 conversions all year. Money pages
> are down 4 percent, and that 4 percent is one page: /solutions/data-append,
> which lost position 3 to a competitor that answers pricing above the fold.

## 2. The shape of the decline

- Pattern: noise, slope, cliff, or split
- Window and comparison basis (state it: year over year, not month over month)
- Clicks, impressions, average position, and conversions in one table
- One chart if the interface supports it

## 3. The money map

| Segment | Clicks change | Conversion change | Share of total loss | Priority |
|---|---|---|---|---|
| Money pages | | | | Critical |
| Commercial support | | | | High |
| Brand and navigational | | | | |
| Top-of-funnel informational | | | | Low |

Follow with one sentence on what this means. If most of the loss is
low-value, say that first and say it without hedging.

## 4. Page-level intent audit

One block per priority page, using the format at the end of
`intent-scoring-rubric.md`. Order by revenue impact, not by score.

Include for each:
- Primary query, intent type, position now vs before
- Intent Match Score with the five components
- Fluff tax (word count before the first substantive answer)
- What the top three competitors do that this page does not
- The single highest-leverage fix

## 5. Trust gap

Trust Gap Score per priority page with the specific tells cited. Skip this
section entirely if scores are above 80. Do not pad.

## 6. SERP displacement

- New entrants per query, with the date they appeared
- What each displacer does better, in concrete terms
- SERP composition changes (AI Overview, ads, video, forums)
- Queries where the click is now being absorbed inside the results page, and
  the honest recommendation for each

## 7. Structural and technical findings

Only confirmed findings, each with the test that confirmed it:

- Cannibalization: keyword, competing URLs, evidence of position swapping
- Indexation errors: exact directive, affected URL count, date introduced
- Topical dilution: count of thin or off-topic pages, prune or noindex list
- Architecture: flat vs siloed, and what it costs in diagnosis and link equity
- Technical: only issues that plausibly affect the decline in question

## 8. Fix Queue

The section the client will actually act on. Rank by impact divided by effort,
not by severity.

| # | URL | Verdict | Highest-leverage fix | Expected effect | Effort | Owner | Execute with |
|---|---|---|---|---|---|---|---|
| 1 | | | | | S/M/L | | seo-rapid-ranker |
| 2 | | | | | | | page-refresh |
| 3 | | | | | | | paa-seo-builder |

## 9. What not to do

Explicitly list the tempting actions that the evidence does not support. This
section prevents wasted quarters and it is where most of the value sits.

Examples:
- Do not rewrite the /blog/ archive. Those clicks were never converting and
  the loss is structural.
- Do not chase the definitional queries now answered inside search results.
- Do not blame the March update. The dates do not line up and the cliff
  matches the deploy on the 14th.

## 10. Evidence appendix

Data sources, date ranges, tools used, and any assumptions made because access
was unavailable. Every number in this report should be traceable to a row in
this appendix.
