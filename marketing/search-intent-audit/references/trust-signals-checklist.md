# Trust Gap Checklist (the AI-look problem)

A page can answer the query correctly and still lose, because the searcher
decides within about two seconds that the page is machine-produced filler and
leaves. That exit is a user signal, and user signals now carry real weight.
Correct information delivered inside an untrustworthy container does not rank.

This checklist scores the container. Score out of 100, higher is better.
Deduct points for each tell present, and cite the specific tell in the report.
Vague feedback ("make it look more premium") is useless to a designer.

## Visual tells (deduct up to 45)

| Tell | Deduct | Note |
|---|---|---|
| Default purple-to-blue gradient hero | 8 | The single most recognizable generated-site signature |
| Three-card feature grid with identical icon treatment | 6 | Especially with lucide or heroicon defaults at the same size |
| Emoji used as bullet points or section markers | 6 | Reads as generated in a professional B2B context |
| Every section the same shape (centered heading, subhead, three columns) | 6 | Rhythm never varies, so nothing feels authored |
| Generic stock illustration (isometric people, blob shapes, abstract 3D) | 5 | No original photography, no product screenshots |
| Glassmorphism cards floating on gradient with no functional purpose | 4 | Decoration in place of information |
| No real product UI anywhere on a product page | 5 | Buyers want to see the thing |
| Uniform spacing with no density variation | 5 | Real editorial design varies density on purpose |

## Content tells (deduct up to 55)

| Tell | Deduct | Note |
|---|---|---|
| No author, no byline, no named human anywhere | 8 | Anonymous authority is not authority |
| Zero original data, numbers, or first-hand evidence | 10 | The strongest single trust differentiator available |
| No sources cited, or sources cited without links | 6 | Claims floating free |
| Hedged generalities ("can help", "may improve", "is often considered") | 7 | Nobody who has done the work hedges this much |
| Opening paragraph is industry throat-clearing | 6 | "In today's rapidly evolving landscape" and relatives |
| Symmetrical list structures: every list exactly five items, every item the same length | 5 | Real thinking is asymmetric |
| No specifics: no prices, no timelines, no named tools, no versions | 8 | Specificity is the cheapest credibility available |
| No date, or a date that is clearly auto-refreshed while content is stale | 5 | Check whether the content matches the claimed date |

## Trust builders to check for (add back up to 20, capped at 100)

- Named author with a real, verifiable role and a genuine bio (+5)
- Original data: a survey, an internal benchmark, a proprietary number (+8)
- Screenshots, photos, or artifacts that could only come from doing the work (+5)
- Named customers, real quotes, verifiable case outcomes (+5)
- A stated point of view, including something the page is willing to say that
  a competitor would not (+5)
- Visible methodology or a "how we know this" note (+4)

## Scoring bands

| Score | Reading | Route to |
|---|---|---|
| 80-100 | Trustworthy container | No design action needed |
| 60-79 | Competent but forgettable | `page-refresh` for editorial treatment |
| 40-59 | Reads as generated | `page-refresh` plus `design-trends`, and add proof |
| 0-39 | Actively distrusted on arrival | Rebuild with original evidence, then redesign |

## How to report this

Say it plainly and cite the tells. Example:

> Trust Gap Score: 44/100. The page carries five generated-content signatures:
> gradient hero with stock isometric illustration, three identical feature
> cards, emoji bullets in the benefits section, no author or date, and zero
> original numbers across 1,400 words. Every claim is hedged. A buyer
> comparing three vendors will discount this page before reading it.
> Fix order: add proof first (original data, named customers, product
> screenshots), then redesign the container.

Note the fix order. Redesigning a page that has nothing original to say
produces a better-looking page that still fails. Proof first, design second.
