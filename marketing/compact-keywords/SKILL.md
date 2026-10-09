---
name: "compact-keywords"
description: "Find compact keywords (short, warm, low difficulty buyer phrases) for SPAN, LakeB2B or any Champions Group site and turn each into a one-page brief routed to the right page skill. Use for keyword research, \"what pages should we write\", content calendars, or before any new SEO page."
---

# Compact Keywords

Adapted from Edward Sturm's Compact Keywords method (edwardsturm.com/compact-keywords) for Champions Group data sites. A compact keyword is a short, specific phrase (usually 3 to 6 words) typed by someone ready to buy, use or contact, that big sites under-target. Each one gets a short, answer-first page.

This skill picks the keywords and writes the briefs. It never writes the page. It hands each brief to a page skill.

## Rules

1. **Warm, not cold.** Keep phrases that signal a buyer: users list, customers list, companies that use, companies using, vs, alternatives, pricing, revenue, competitors, sample. Drop pure learner phrases (what is, how does) unless they feed a warm page.
2. **Find the language gap.** A keyword qualifies when the top 10 is thin, off-intent, or from sites we can beat, and keyword difficulty is under 20.
3. **One page per intent, not per phrase.** Group phrases whose searcher wants the same answer ("companies that use NetSuite" and "NetSuite customers list"). Split phrases that want different answers ("Zoho revenue" and "Zoho vs HubSpot").
4. **Real data first.** For SPAN, only brief a page where the data team confirms a strong count. No count, no page.
5. **Volume is a tiebreaker, not the filter.** A 50 search phrase with KD 0 and a clear buyer beats a 2,000 search phrase full of learners. Use traffic potential to spot families: HubSpot customers list had volume 150 but traffic potential 2,100 (Oct 2026).

## Workflow

### 1. Seeds
Ask for, or pull, the seed list: technologies (Workday, NetSuite, Zoho CRM), companies, and verticals. For SPAN, start with the technology categories the platform covers and the top 10 existing tech pages.

### 2. Expand (Ahrefs MCP)
Read `doc` for each tool once, then:
- `keywords-explorer-matching-terms` per seed with terms: users list, customers list, companies that use, companies using, vs, alternatives, revenue, competitors, employees
- `keywords-explorer-overview` on the shortlist for volume, difficulty, traffic_potential, cpc, intents
- `serp-overview` on the top candidates to read who ranks and why
Render every Ahrefs table with `render-data-table`. CPC comes back in cents.
Without Ahrefs, use WebSearch and Google autocomplete, and say volumes are unknown.

### 3. Pull questions
Run `paa-seo-builder` Phase 1 (question discovery) on each winning keyword to collect 3 to 5 People Also Ask questions for the FAQ.

### 4. Route to a page type
| Searcher wants | Page type | Skill |
|---|---|---|
| A list of companies running a product | Answer page | span-answer-page |
| Facts about one company (revenue, employees, competitors, tech stack) | Company profile | span-company-profile |
| Two products side by side | Comparison page | span-answer-page (comparison mode) |
| A topic that truly needs 1,500+ words | Long blog | span-blog-builder |

### 5. Write the brief (one per page)
```
Keyword: <primary>            Also covers: <grouped phrases>
Volume / KD / TP: <numbers, country, date pulled>
Page type and skill: <type>, <skill>
URL: <slug matching the keyword>
Title (under 60 chars): <keyword first>
First fold answer must include: <the count, the date, the who, the next step>
H2s (the buyer's next questions): <3 to 5>
FAQ (from PAA): <3 to 5>
Tool or resource: <one, or "none">
Infographic: <what data has a shape>
Links out: <profile, users list, comparison, related tech, platform>
Links in: <3 existing pages that should link here>
Data needed from SPAN: <fields, in brackets>
Pain point source: <forum, review or sales call to read first>
```

### 6. Deliver
- A keyword sheet (xlsx skill) with one row per page: keyword, grouped phrases, volume, KD, TP, page type, URL, owner, status.
- The briefs, saved to the Celsus vault under `Efforts/Active/SPAN Content/Briefs/`.
- One line telling the user which page to write first and why.

### 7. Close the loop
At week 4 and week 8 after publishing, pull positions (Search Console or Ahrefs rank tracker). Pages on page two go to `seo-rapid-ranker`. Pages that drop go to `search-intent-audit`. Both send back a refresh brief through step 5.

## Example (SPAN, US, Ahrefs, 8 Oct 2026)
| Keyword | Vol | KD | TP | Route |
|---|---|---|---|---|
| companies that use workday | 500 | 0 | 800 | span-answer-page, groups "workday customers list" |
| zoho vs hubspot | 450 | 7 | 700 | span-answer-page, comparison |
| zoho revenue | 250 | 5 | 1,000 | span-company-profile: Zoho |
| hubspot customers list | 150 | 1 | 2,100 | span-answer-page |

## Never
- Stuff "email list" or "buy" into every title (the March 2024 spam update hit that pattern).
- Brief a page without a confirmed data count.
- Use em or en dashes anywhere in briefs or sheets.