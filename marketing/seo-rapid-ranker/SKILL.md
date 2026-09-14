---
name: seo-rapid-ranker
description: >
  Fast-action, surgical SEO workflow for ranking a specific service or product page
  higher on Google — quickly. Based on a 5-step competitive gap + question optimization
  + internal linking methodology. Use this skill whenever the user wants to rank a
  specific page faster, boost a service page, outrank competitors for a keyword, do a
  quick competitive SEO gap analysis, optimize a page for People Also Ask / FAQ,
  or find questions to add to a page. MANDATORY TRIGGER for: "rank this page",
  "rank faster", "outrank competitors", "boost my page", "why am I not ranking",
  "competitive gap", "what are competitors doing better", "add FAQs to my page",
  "find questions people ask about [topic]", "quick SEO fix", "rapid rank",
  "fast ranking", "rank #1", "page optimization sprint", "SEO sprint", or any
  request to quickly improve a single page's Google ranking. This is NOT a full
  site audit — use marketing:seo-audit for comprehensive audits. This is the
  tactical, page-level, "do this today and see results this week" workflow.
---

# SEO Rapid Ranker

A surgical, fast-action workflow for ranking a specific page higher on Google.
Instead of running a full-site audit, this skill focuses on one page and does
five things to give it the best shot at climbing the SERPs quickly.

The philosophy is simple: don't guess — analyze what's already winning, find
the gaps, fill them, and build supporting content. This typically takes 1-2
hours of focused work and can show ranking improvements within days to weeks.

## When to Use This vs. Other SEO Skills

| Scenario | Use This Skill | Use marketing:seo-audit |
|----------|---------------|------------------------|
| "I need to rank this service page faster" | Yes | No |
| "Full SEO health check of my site" | No | Yes |
| "What questions should I add to my page?" | Yes | No |
| "Comprehensive keyword research" | No | Yes |
| "Quick competitive gap for one keyword" | Yes | No |
| "Technical SEO issues across my site" | No | Yes |

## Inputs

Gather these from the user before starting. If missing, ask:

1. **Target URL** — the specific page they want to rank higher
2. **Target keyword** — the primary search term they want to rank for
   (e.g., "roof repair dallas", "b2b data provider", "yoga classes bangalore")
3. **Country** (optional) — defaults to the country most relevant to the keyword

If the user gives a keyword but no URL, that's fine — the workflow adapts.
If they give a URL but no keyword, ask what service/topic the page is about.

---

## The 5-Step Rapid Ranking Workflow

### Step 1: Competitive Reconnaissance

Google the target keyword and identify who's currently winning.

**With Ahrefs MCP (preferred):**

Use `site-explorer-organic-competitors` to find who competes for the same
keyword space, then use `serp-overview` to see who currently holds the top
positions for the target keyword:

```
serp-overview → target keyword, country
site-explorer-organic-keywords → competitor URLs, filtered to the target keyword
```

Pull the top 5 ranking pages. For each, note:
- Their URL and domain authority signals
- What position they hold
- How much estimated traffic they get from this keyword

**Without Ahrefs:**

Use web search (Firecrawl search or WebSearch) to Google the target keyword.
Identify the top 5 organic results (skip ads). Record their URLs.

**Output of this step:** A ranked list of 3-5 competitor URLs currently
outranking the user's page.

### Step 2: AI-Powered Competitive Page Analysis

This is the key differentiator. Use Claude's analytical capabilities to
compare competitor pages against the user's page.

**Scrape the pages:**

Use Firecrawl (or WebFetch) to pull the content of:
- The user's target page
- Each of the top 3-5 competitor pages

**Run the comparison analysis.** For each competitor page vs. the user's page,
evaluate:

- **Content depth** — How many words? How many sections/headings? Do competitors
  cover subtopics the user's page misses?
- **Heading structure** — What H2s and H3s do competitors use? What topics do
  they cover that the user doesn't?
- **Keyword usage** — Where and how often do competitors use the target keyword
  and related terms? Is the user's page under-optimized or keyword-stuffed?
- **Trust signals** — Do competitors have testimonials, certifications, stats,
  case studies, or social proof the user lacks?
- **CTAs and conversion elements** — How do competitors structure their calls
  to action?
- **FAQ sections** — Do competitors have FAQ schemas? What questions do they
  answer?
- **Internal linking** — Do competitors link to supporting blog posts or
  related service pages?
- **Schema markup** — Are competitors using structured data (FAQ, HowTo,
  LocalBusiness, Service) that might earn rich snippets?

**Present findings as a gap report:**

```
## Competitive Gap Report: [keyword]

### What competitors do that your page doesn't:
1. [Gap 1 — e.g., "3 of 5 competitors have FAQ sections with 5-8 questions"]
2. [Gap 2 — e.g., "Top-ranking page has 2,400 words vs. your 800 words"]
3. [Gap 3 — e.g., "Competitors link to 2-3 supporting blog posts"]

### What your page does well:
1. [Strength — e.g., "Strong testimonials section that competitors lack"]

### Priority fixes (do today):
1. [Most impactful gap to close first]
2. [Second priority]
3. [Third priority]
```

### Step 3: Question Mining

Find the actual questions real people are asking about the target topic.
These become H2s, FAQs, or content sections on the page.

**Method 1 — Answer Socrates (primary):**

Scrape `https://answersocrates.com/` for the target keyword using Firecrawl.
This tool visualizes Google's "People Also Ask" data in a question tree.

```
Firecrawl scrape → https://answersocrates.com/find?q=[keyword]&lang=en
```

**Method 2 — Ahrefs Keywords Explorer (if available):**

Use `keywords-explorer-related-terms` with the target keyword to find question
variations:

```
keywords-explorer-related-terms → keyword, country, select relevant fields
Filter for question-type keywords (starting with how, what, why, when, does, etc.)
```

Also use `keywords-explorer-search-suggestions` for autocomplete-style queries.

**Method 3 — Google "People Also Ask" via web search:**

Search the target keyword and extract PAA questions from the results.

**Output of this step:** A prioritized list of 5-10 questions, sorted by:
1. Relevance to the target page's service/product
2. Search volume (if Ahrefs data available)
3. Whether competitors already answer them (gap = opportunity)

### Step 4: On-Page Content Enhancement

Now apply the findings from Steps 2 and 3 to the user's page.

**Generate the content additions.** For each priority item:

**FAQ / Question Section:**
- Take the top 3-5 questions from Step 3
- Write concise, authoritative answers (50-150 words each)
- Format as an FAQ section with proper heading hierarchy:

```html
<h2>Frequently Asked Questions</h2>

<h3>[Question from Step 3]</h3>
<p>[Direct, helpful answer. Front-load the answer in the first sentence,
then elaborate. Include the target keyword naturally.]</p>
```

- Recommend FAQ schema markup for rich snippet eligibility

**Additional H2 Sections:**
- If competitors cover subtopics the user's page misses (from Step 2),
  draft 1-2 new H2 sections with 150-300 words each
- These should address the content depth gap without making the page bloated

**Quick On-Page Fixes:**
- Title tag optimization (if the target keyword isn't in the title)
- Meta description with the keyword + a compelling CTA
- H1 tag check (should contain or closely match the target keyword)
- First-paragraph keyword placement
- Image alt text suggestions
- Internal link recommendations (link TO this page from other relevant pages)

**Present as copy-paste-ready content** that the user or their dev can
immediately add to the page.

### Step 5: Supporting Content + Internal Linking

The final piece: create a supporting blog post that answers a related
question and links back to the service page. This builds topical authority
and passes link equity.

**Choose the blog topic:**

From the questions mined in Step 3, pick one that:
- Is closely related to the service but deserves its own page
- Has enough depth for a 600-1000 word blog post
- Isn't already covered on the user's blog

Good pattern: if the service page is "roof repair dallas", the blog might be
"How to Tell If Your Roof Needs Repair: 7 Warning Signs" — it answers a
real question, attracts informational searchers, and naturally links to the
service page.

**Draft the blog post outline:**

```
## Blog Post: [Title with target keyword variation]

### Target keyword: [related long-tail keyword]
### Internal link to: [the service page URL]
### Word count target: 800-1,200 words

### Outline:
- Introduction (mention the main service page topic, link opportunity)
- [H2: Section 1]
- [H2: Section 2]
- [H2: Section 3]
- Conclusion with CTA linking to the service page
```

**Optionally, draft the full blog post** if the user asks for it. Use the
b2b-blog-writer skill if available for full-pipeline blog creation.

**Internal linking strategy:**

- The new blog post links to the service page (1-2 contextual links)
- Identify 2-3 existing pages on the user's site that should also link
  to the service page (check with Ahrefs `site-explorer-pages-by-internal-links`
  or by crawling the site)
- Suggest anchor text for each internal link (use keyword variations, not
  exact match every time)

---

## Output Format

Present the complete workflow results as an actionable report:

```
# SEO Rapid Ranker Report: [Target Keyword]
## Target Page: [URL]

### 1. Competitive Landscape
[Top 3-5 competitors with positions and key observations]

### 2. Gap Analysis
[What competitors do that you don't — prioritized]

### 3. Questions to Add
[5-10 questions with recommended answers, ready to paste]

### 4. Page Optimization Checklist
- [ ] Title tag: [recommended title]
- [ ] Meta description: [recommended description]
- [ ] Add FAQ section with [N] questions
- [ ] Add H2 section on [missing subtopic]
- [ ] Fix H1 to include [keyword]
- [ ] Add internal links from [pages]
- [ ] Add FAQ schema markup

### 5. Supporting Blog Post
[Topic, outline, and internal linking plan]

### Estimated Impact
[Realistic assessment: what ranking improvement to expect and timeline]
```

## Follow-Up

After presenting the report, offer:

"Want me to:
- Draft the full FAQ section with schema markup?
- Write the supporting blog post? (I can use the blog writer skill for this)
- Check your other service pages with the same process?
- Set up Ahrefs rank tracking to monitor progress?
- Run a deeper analysis with a full SEO audit?"

---

## Key Principles

1. **Speed over perfection.** This is about making meaningful improvements
   today, not producing a 50-page audit. Ship the changes, monitor, iterate.

2. **Competitor intelligence, not guesswork.** Every recommendation is grounded
   in what's actually working for pages that currently rank above you.

3. **Questions are gold.** Adding real questions people ask — as H2s or FAQs —
   is one of the fastest ways to capture featured snippets and PAA boxes.

4. **Internal links are free authority.** A supporting blog post that links to
   your service page is the easiest link you'll ever build.

5. **One page at a time.** Resist the urge to audit the whole site. Pick your
   most important page, rank it, then move to the next one.
