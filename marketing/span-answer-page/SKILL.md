---
name: "span-answer-page"
description: "Write short, answer-first SPAN pages (users lists, customers lists, comparisons) to the SPAN page standard with audio overview, Ask AI, copy as Markdown, preferred source button and infographics. Use for any SPAN SEO page under 1,000 words, page refreshes, or when a compact-keywords brief says span-answer-page."
---

# SPAN Answer Page

Turns one compact-keywords brief into a short page that answers the search in the first fold and sends the reader to the next page. Model page: "Companies That Use Zoho CRM" in the SPAN Content Playbook doc (Oct 2026). Writer: Aishwarya; reviewer: Preeti.

Load first: `span-brand-guidelines` (or the SGS design notes: Mulish, heading #2e4a3a, 18px body, title case headings, no eyebrows), `vinh-copywriting`.

## Inputs
A brief from `compact-keywords`. If there is none, run that skill first. Do not start from a bare topic.

## The page (in this order)
1. **H1:** the keyword in plain words, title case, under 60 characters.
2. **Answer box (first fold):** 40 to 60 words. The count, the verified date, who they are, and the next step with a link. A reader who stops here got the answer.
3. **Extras row:** audio overview, Ask AI (ChatGPT, Claude, Perplexity, Google AI Mode), copy as Markdown, preferred source.
4. **Key facts strip:** 3 to 5 facts (count, countries, median size, last verified).
5. **H2s:** 3 to 5, each the buyer's next question in their words, answered in 2 to 4 short paragraphs with one practical takeaway (who to contact, what to pitch next).
6. **One infographic** where data has a shape. Alt text is a sentence that states the finding.
7. **One tool or resource** only when it helps (segment counter, sample download, comparison table).
8. **Related links:** company profile, users list, one comparison, one related technology, the platform.
9. **FAQ:** 3 to 5 PAA questions, two sentence answers, FAQPage schema.
10. **CTA:** "Get a Free Sample" with `?utm_source=<type>&utm_medium=cta&utm_campaign=<slug>`. "Book 30 Minutes With Span" (https://scheduler.zoom.us/span-global-services/30-mins-with-span-global) stays a text link.

Length: 400 to 900 words. If the draft passes 900, cut sections, not sentences.

**Comparison mode** ("X vs Y"): the answer box gives a two-column count and the one difference that matters; H2s cover size split, industry split, who switches and why; one overlap infographic; link both users lists and both company profiles.

## Writing rules
- Level 1 to 2 language (vinh-copywriting Law 1). Active voice, "you" and "we".
- Every fact about a vendor has a public source and a date. SPAN numbers stay in [brackets] until the data team fills them.
- One pain point from forums, G2 reviews, Reddit or a sales call, noted in the brief and used in the copy.
- Never invent a customer story, a stat or a quote.

## Page Extras Gate (span-company-profile uses this too)
Tick every line before handoff:
- [ ] Answer box present and under 60 words
- [ ] Audio overview: 90 seconds to 2 minutes, made from the final copy (NotebookLM audio overview or text to speech), transcript on the page
- [ ] Ask AI links with a prompt naming this page's URL: `https://chatgpt.com/?q=`, `https://claude.ai/new?q=`, `https://www.perplexity.ai/search?q=`, `https://www.google.com/search?udm=50&q=`
- [ ] Copy as Markdown button (top right) reading the `.md` twin at the same URL
- [ ] Preferred source: `<script async src="https://news.google.com/swg/js/v1/publisher.js"></script>` in head and `<div google-add-preferred-source-btn></div>` near the byline, or the deeplink `https://www.google.com/preferences/source?q=spanglobalservices.com`. Track clicks in GA4.
- [ ] At least one original infographic with sentence alt text
- [ ] 3 to 6 internal links, all returning 200 (curl each)
- [ ] FAQPage, Article and BreadcrumbList JSON-LD
- [ ] Byline, data reviewer, "Last verified" date
- [ ] One primary CTA with UTM tags

## Gates (in order)
1. `vinh-copywriting` pass on body, subheads and CTA lines
2. `no-ai-slop` Gate mode, plus zero em and en dashes (`grep -cP '\xe2\x80[\x93\x94]'` prints 0)
3. Page Extras Gate above
4. `agent-ready` (markdown twin, llms.txt entry, JSON-LD, raw HTML content)
5. `visual-verify` at 390 and 1440, light and dark, when a designed page is built

## Output
- The page copy as Markdown (for the editor) and, when asked, the WordPress-safe HTML with inline styles (SGS editor does not accept style or script blocks; extras scripts go in the site template).
- The brief updated with status, URL and publish date, saved in `Efforts/Active/SPAN Content/` in the Celsus vault.
- One line asking for critique, then turn durable notes into rule edits for this skill.