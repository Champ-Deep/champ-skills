---
name: paa-seo-builder
description: "Full-pipeline People Also Ask (PAA) SEO strategy builder. Takes a target domain and seed keywords, harvests PAA questions, builds topic clusters, creates FAQ hub architecture, writes content briefs, and generates an implementation roadmap. MANDATORY TRIGGER for: \"PAA strategy\", \"People Also Ask\", \"FAQ SEO\", \"question SEO\", \"build FAQ hubs\", \"PAA questions for [topic]\", \"harvest questions\", \"FAQ hub architecture\", \"question-based SEO\", \"answer engine optimization\", \"PAA plan for [site]\", \"add PAA to my SEO\", \"question optimization\", \"FAQ content strategy\", \"colony linking\", \"authority funneling\", or any request involving People Also Ask optimization, FAQ-based SEO strategy, or question-driven content architecture. Works for any web property. Pairs with seo-rapid-ranker for page-level tactical work."
---

# PAA SEO Builder

A 6-phase methodology for building question-based SEO dominance through People Also Ask
optimization. This skill turns seed keywords into a comprehensive FAQ hub architecture
with content briefs, internal linking blueprints, and a phased implementation roadmap.

The philosophy: Google's PAA boxes are the largest source of zero-click real estate.
By systematically answering the questions Google already surfaces, you become the
default authority in your niche. This isn't a quick fix — it's a content architecture
strategy that compounds over 8-16 weeks.

## When to Use This vs. Other SEO Skills

| Scenario | Use This Skill | Use seo-rapid-ranker | Use marketing:seo-audit |
|----------|---------------|---------------------|------------------------|
| "Build a PAA/FAQ strategy for my site" | Yes | No | No |
| "Rank this one page faster" | No | Yes | No |
| "Full SEO health check" | No | No | Yes |
| "What PAA questions exist for my niche?" | Yes | No | No |
| "Quick competitive gap for one keyword" | No | Yes | No |
| "Build FAQ hub architecture" | Yes | No | No |
| "Add FAQs to an existing page" | No | Yes | No |

## Inputs

Gather these before starting. If missing, ask:

1. **Target domain** — the website to build the PAA strategy for
2. **Seed keywords** (3-5) — primary topics/services the site covers
3. **Target geography** (optional) — defaults to the most relevant country
4. **Existing content inventory** (optional) — URLs of key pages already on the site
5. **Competitors** (optional) — 2-3 competitor domains for gap analysis

---

## The 6-Phase PAA Methodology

### Phase 1: Question Discovery

Harvest every PAA question Google surfaces for your niche.

**With Ahrefs MCP (preferred):**

Use these tools in sequence:

```
keywords-explorer-related-terms → each seed keyword, filter to questions
keywords-explorer-search-suggestions → each seed keyword
keywords-explorer-matching-terms → "[who/what/where/when/why/how] + seed keyword"
```

For each seed keyword, pull:
- All question-format related terms
- Search suggestions (these often match PAA boxes)
- Matching terms with question modifiers (who, what, where, when, why, how)

**With Firecrawl / Web Search:**

Search each seed keyword on Google and extract PAA boxes:
- Search "[seed keyword]" → record all PAA questions shown
- Click each PAA to expand and record the cascading questions
- Search "[seed keyword] FAQ" and "[seed keyword] questions"
- Use firecrawl to scrape competitor FAQ pages for their question lists

**Processing the harvest:**

For each question discovered:
- **Search volume**: Use keywords-explorer-overview if available
- **Intent classification**: Informational / Navigational / Transactional / Commercial
- **Difficulty score**: From Ahrefs KD or estimated from SERP competition
- **Relevance score**: 1-5 rating of how well it fits the target domain's offerings

Target: 50-100+ questions per property. Discard anything below relevance score 2.

Sort by: Relevance (desc) → Volume (desc) → Difficulty (asc)

---

### Phase 2: Content Architecture

Group questions into topic clusters and design the FAQ hub structure.

**Clustering rules:**
- Group questions by semantic similarity (same topic, different angles)
- Target 8-12 clusters per property
- Each cluster needs a clear hub theme (e.g., "pricing", "how it works", "comparisons")
- Minimum 4 questions per cluster, maximum 12

**FAQ Hub URL structure:**
```
/[topic]-faq/                    → Hub page (pillar)
/[topic]-faq/[subtopic]/         → Supporting FAQ pages
/blog/[topic]-[question-slug]/   → Deep-dive articles answering single questions
```

**For each cluster, define:**
1. Hub page title and URL
2. 4-8 primary PAA questions the hub page answers directly
3. 2-4 supporting pages for questions needing longer answers
4. 1-2 blog posts for deep-dive questions with high search volume
5. Internal linking map (which pages link to which)

**Output:** A content architecture document with all clusters, URLs, and linking maps.

---

### Phase 3: Content Creation Briefs

Write actionable content briefs for each page in the architecture.

**Hub page brief template:**
- Title tag (60 chars, includes primary question keyword)
- Meta description (155 chars, includes CTA)
- H1 heading
- 8-10 PAA questions as H2/H3 subheadings
- For each question:
  - **Featured snippet answer** (40-60 words, inverted pyramid style — answer first)
  - **Expanded answer** (200-400 words with depth, examples, data)
- Structured data: FAQ Schema markup for all Q&A pairs
- Internal links: 3-5 links to supporting pages and related hubs
- CTA placement after every 3rd question

**Supporting page brief template:**
- Same structure but focused on 3-5 questions
- Deeper treatment (500-800 words per answer)
- HowTo Schema where applicable
- Links back to hub page + 2-3 cross-links to other clusters

**Blog post brief template:**
- Long-form treatment of a single high-volume question (1500-2500 words)
- Includes related PAA questions as sections
- Links to hub page and 2 supporting pages
- Optimized for the specific long-tail question keyword

---

### Phase 4: Authority Funneling

Build internal link chains that pass PageRank to FAQ hubs.

**Authority audit:**
1. Identify the site's highest-authority pages (use site-explorer-pages-by-backlinks if Ahrefs available)
2. Map existing internal links from these pages
3. Find opportunities to add contextual links from high-authority pages to FAQ hubs

**Funnel structure:**
```
High-Authority Page → Hub Page → Supporting Pages → Blog Posts
     (most links)      (medium)     (fewer links)    (fewest)
```

**Implementation:**
- Add contextual links from top 5 highest-authority pages to each FAQ hub
- Add breadcrumb navigation with BreadcrumbList structured data
- Add "Related Questions" sections on existing service/product pages linking to FAQ hubs
- Add FAQ hub links to the main navigation or footer

---

### Phase 5: Colony Linking

Build satellite content that reinforces FAQ hub authority.

**Colony content types:**
- Blog posts that reference FAQ answers (link to specific FAQ sections)
- Resource guides that compile answers across multiple hubs
- Comparison pages ("X vs Y") that link to both relevant FAQ hubs
- "Ultimate guide" posts that link to 3-4 FAQ hubs as detailed references

**Colony linking rules:**
- Every colony page links to at least 1 FAQ hub
- Every FAQ hub receives links from at least 3 colony pages
- Colony pages link to each other sparingly (max 1-2 cross-links)
- Balance: no single hub should have more than 3x the internal links of the weakest hub

**Reciprocal linking:**
- FAQ hubs link back to colony pages in "Further Reading" or "Related Guides" sections
- Keep reciprocal ratio under 30% (most links should be one-directional toward hubs)

---

### Phase 6: Backlink Balance & External Promotion

Build external links to FAQ hubs (not just the homepage).

**Link target distribution:**
- 40% of outreach efforts point to FAQ hubs
- 30% to deep-dive blog posts (they'll pass equity to hubs via internal links)
- 20% to resource/comparison pages
- 10% to homepage/service pages

**Outreach targets:**
- Resource pages in adjacent niches ("helpful links" roundups)
- Industry publications accepting guest contributions
- Answer sites (Quora, Reddit) where FAQ content genuinely answers questions
- Broken link opportunities on competitors' backlink profiles (use site-explorer-broken-backlinks)

**Monitoring:**
- Track backlink distribution monthly (use site-explorer-referring-domains filtered by URL)
- Rebalance outreach if any hub is under-linked
- Monitor PAA box ownership with rank-tracker tools

---

## Deliverables

The skill produces three outputs:

### 1. HTML Strategy Document
A polished, self-contained HTML file with:
- Executive summary
- Question discovery results (table of all PAA questions with metrics)
- Content architecture diagram (cluster map)
- Content briefs for all pages
- Internal linking blueprint
- 12-week implementation timeline
- KPI targets

Deploy to Supabase Edge Function for easy sharing:
- Project ID: uwqhplmlceuridmhhlpp
- Function name: paa-seo-[domain-slug]
- Set verify_jwt: false for public access

### 2. Vault Markdown Note
Save to ~/Celsus/Efforts/Active/PAA-SEO-[Domain].md with:
- Strategy summary
- Phase checklist with dates
- Links to the HTML doc and any deployed URLs
- Weekly tracking section

### 3. Implementation Roadmap
A week-by-week plan:
- **Weeks 1-2:** Question discovery + architecture
- **Weeks 3-4:** Write hub page content + implement structured data
- **Weeks 5-6:** Write supporting pages + set up internal linking
- **Weeks 7-8:** Write colony content (blog posts, guides)
- **Weeks 9-10:** Authority funneling + backlink outreach begins
- **Weeks 11-12:** Monitor, adjust, fill gaps

---

## Tool Reference

**Ahrefs MCP tools (mcp__e705c4a5-*):**
- keywords-explorer-related-terms: Question harvesting
- keywords-explorer-search-suggestions: PAA proxy questions
- keywords-explorer-matching-terms: Question-modifier searches
- keywords-explorer-overview: Volume/difficulty for harvested questions
- keywords-explorer-volume-history: Trend analysis
- site-explorer-pages-by-backlinks: Authority audit
- site-explorer-organic-keywords: Competitor question coverage
- site-explorer-broken-backlinks: Link building opportunities
- site-explorer-referring-domains: Backlink balance monitoring
- serp-overview: SERP feature analysis (PAA box presence)
- rank-tracker-overview: Tracking PAA ownership over time

**Companion skills:**
- seo-rapid-ranker: For tactical, single-page optimization after hubs are built
- firecrawl: For scraping competitor FAQ pages and PAA boxes
- b2b-blog-writer: For writing the colony content (blog posts, guides)
- marketing:content-creation: For writing FAQ page content
- marketing:competitive-analysis: For competitor FAQ gap analysis

---

## Checklist

Use this to track progress through the methodology:

- [ ] Gather inputs (domain, seed keywords, geography, competitors)
- [ ] Phase 1: Question Discovery — harvest 50-100+ PAA questions
- [ ] Phase 1: Score and classify all questions (volume, intent, relevance)
- [ ] Phase 2: Cluster questions into 8-12 topic groups
- [ ] Phase 2: Design FAQ hub URL structure
- [ ] Phase 2: Create internal linking blueprint
- [ ] Phase 3: Write hub page content briefs
- [ ] Phase 3: Write supporting page content briefs
- [ ] Phase 3: Write blog post content briefs
- [ ] Phase 4: Audit existing page authority
- [ ] Phase 4: Map authority funneling opportunities
- [ ] Phase 5: Plan colony content pieces
- [ ] Phase 5: Design colony linking structure
- [ ] Phase 6: Identify backlink targets
- [ ] Phase 6: Create outreach plan with link distribution targets
- [ ] Generate HTML strategy document
- [ ] Save vault markdown note
- [ ] Deploy to Supabase for sharing
- [ ] Create 12-week implementation roadmap

## Final gate: no AI slop (mandatory before delivery)

Everything this skill produces that a person will read (client, prospect, vendor, partner, public, or the sales team) passes a no-AI-slop check before it is delivered. Load the `no-ai-slop` skill in Gate mode and run its Eval on the final copy. If that skill cannot be loaded, apply this minimum:

- Zero em dashes and en dashes anywhere, including headings, titles, subject lines, and date ranges. Use periods, commas, colons, parentheses, or restructure.
- Cut binary contrasts ("It's not X, it's Y", "Not because X. Because Y."), throat-clearing openers ("Here's the thing"), faux-insight setups ("What nobody tells you"), colon reveals ("The best part: it learns"), dramatic fragments ("That's it."), rhetorical setups, fake-profound kickers, and recap endings.
- Cut puffery and weasel attribution ("a testament to", "pivotal moment", "experts agree", "studies show"). Name the source or drop the claim. Never invent a source, stat, or quote.
- Banned words: delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, seamless, unlock, synergy, game changer, tapestry, realm, beacon, multifaceted, meticulous, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving.
- Portability test: a sentence that could move unchanged to another company is filler. Replace it with a name, number, date, or mechanism, or cut it.
- Repeat the right word instead of cycling synonyms. Active voice, human subjects, direct verbs. No decorative bold or emoji headings.
- This gate governs style only. It never overrides this skill's factual, brand, or client-safety rules (vendor firewall, entity separation, verified numbers).