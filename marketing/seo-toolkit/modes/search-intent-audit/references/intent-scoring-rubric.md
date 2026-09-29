# Intent Match Scoring Rubric

Score every audited page out of 100 across five components. Show the component
scores, never just the total. The total tells the user how bad it is. The
components tell them what to do on Monday.

## Component 1: Intent Type Alignment (30 points)

First classify the query the page actually ranks for, then classify the page.

| Query intent | Searcher wants | Correct page type |
|---|---|---|
| Informational | An explanation or a definition | Guide, article, FAQ hub |
| Commercial investigation | To compare options before buying | Comparison, alternatives, pricing, case study, list |
| Transactional | To act now (buy, book, request, download) | Service page, product page, form, demo page |
| Navigational | A specific brand or destination | Homepage, brand page, login |

Scoring:

- **30**: page type matches query intent exactly, and the page format matches
  what the current SERP rewards (check the live SERP, not assumptions).
- **20**: right intent family, wrong format (a blog answering a comparison
  query that the SERP fills with product pages).
- **10**: adjacent intent (informational page ranking for a commercial query).
- **0**: mismatched (a transactional query landing on a thought-leadership essay).

Note: an intent type mismatch cannot be fixed by editing. It needs a different
page. Say so plainly rather than recommending cosmetic changes.

## Component 2: Above-the-Fold Answer (25 points)

Simulate the first screen on mobile, since that is where most searchers land.

Measure:
- Words of preamble before the first substantive answer.
- Whether the H1 restates the query in the searcher's language.
- Whether an answer, a number, a price, a list, or a next action is visible
  without scrolling.
- Obstruction load: cookie banner, newsletter popup, chat widget, autoplay
  hero, sticky bars.

Scoring:

- **25**: answer or clear next action visible immediately, under about 30 words
  of setup, no obstruction.
- **18**: answer within the first screen but buried under a hero image or a
  paragraph of positioning.
- **10**: answer appears only after one scroll.
- **0**: the fold is pure atmosphere (brand statement, stock hero, "In today's
  fast-paced landscape"), or a popup covers the answer.

The "fluff tax" is the count of words a searcher must read past to reach value.
Report it as a number. It is the single most persuasive metric in this audit.

## Component 3: Answer Completeness (20 points)

Does the page fully resolve the query, or does it answer 60 percent and gate
the rest behind a form or a "contact us to learn more"?

Test method: write the three follow-up questions a real searcher would have
after reading. Check whether the page answers them.

Scoring:

- **20**: query fully resolved, plus the obvious follow-ups.
- **14**: main query resolved, follow-ups unaddressed.
- **7**: partial answer, key specifics (price, process, eligibility, numbers,
  timeline) missing.
- **0**: the page describes the topic without answering the question.

Compare against the top three ranking pages. If competitors answer something
this page does not, that gap is the fix.

## Component 4: Relevance Density (15 points)

How much of the page is about the query, versus about the company, versus
about nothing in particular.

Measure the ratio of on-query content to total content. Flag:
- Boilerplate "about us" blocks in the middle of an answer.
- Generic industry context that any page in any industry could carry.
- Padding written to hit a word count.
- Sections that exist because a template had a slot.

Scoring:

- **15**: high density, every section earns its place.
- **10**: some padding, core intact.
- **5**: answer diluted across long tangents.
- **0**: the query is a pretext for a sales pitch.

Shorter and denser wins. A 600-word page that answers completely beats a
2,400-word page that answers eventually.

## Component 5: Conversion Path Fit (10 points)

Intent match is not just about answering. It is about what happens next.

- **10**: the next action matches where the searcher is in the funnel (an
  informational page offering a relevant deeper resource, a transactional page
  offering an immediate action).
- **6**: a CTA exists but is mismatched to funnel stage (a "book a demo" as
  the only option on a definitional query).
- **3**: generic sitewide CTA only.
- **0**: no path forward at all.

## Total score bands

| Score | Reading | Action |
|---|---|---|
| 85-100 | Intent is not the problem | Look at Stages 3, 4, 5 |
| 65-84 | Fixable friction | Above-the-fold rewrite, add missing answers |
| 40-64 | Serious mismatch | Restructure the page around the query |
| 0-39 | Wrong page for the query | Build the right page, redirect or repurpose this one |

## Reporting format per page

```
URL: /example-page
Primary query: "example query" (commercial investigation, position 8.4, down from 3.1)
Intent Match Score: 52/100
  Intent type alignment  10/30  blog post ranking for a comparison query
  Above-the-fold answer  12/25  187-word fluff tax before the first specific
  Answer completeness    14/20  no pricing, competitors all show pricing
  Relevance density       9/15  two company-history sections mid-answer
  Conversion path fit     7/10  demo CTA only, no mid-funnel option
Highest-leverage fix: replace the opening 187 words with a comparison table
and a direct answer sentence, then add the pricing band competitors show.
```
