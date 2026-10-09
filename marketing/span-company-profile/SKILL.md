---
name: "span-company-profile"
description: "Build a SPAN company profile page (for example Zoho, HubSpot, NetSuite) with firmographics, technographics, install base, switching signals, reviews, sentiment, hiring, comparison, Markdown twin and AI buttons, interlinked with SPAN users lists. Use for \"company page\", \"company profile\", \"[company] revenue or competitors\" keywords, or when a compact-keywords brief says span-company-profile."
---

# SPAN Company Profile

One page per company that answers "who is this company, what do they run, who uses their products" and links to every SPAN list that mentions them. Reference prototype: the Zoho Company Profile artifact (Oct 2026). Pages live at `/companies/<slug>/` on spanglobalservices.com; the platform sits on its own subdomain.

Load first: `span-brand-guidelines` and `frontend-design-pro` for the visual build.

## Why it can rank
Crunchbase, ZoomInfo, Apollo, Owler and Craft rank company pages for "[company] revenue / employees / competitors". BuiltWith, HG Insights, 6sense and Landbase rank "companies using [technology]". A SPAN profile wins only with data they lack, so every profile carries the extra field.

## The extra field: switching signals
Companies that added or dropped the company's main product in the last 90 days, verified and dated, with where they came from or went to. Show counts publicly; the company list sits on the platform. If the platform cannot fill this for a company yet, hold the page.

## Blocks (hide any block with no data; never publish an empty block)
| Block | Contents | Source |
|---|---|---|
| Answer box | Who the company is in 50 words plus the SPAN install base count and date | Public facts plus SPAN |
| At a glance | Founded, HQ, employees, offices, ownership, CEO, users or customers, growth | Press releases, filings, Wikipedia, each with date |
| Switching signals | Added and dropped, by source and destination, net, one scale for all bars | SPAN platform |
| Install base | Companies using each product, by country and size, each row linking to its users list | SPAN platform |
| Internal tech stack | What the company runs, by category, verified date per card | SPAN platform |
| Reviews and sentiment | G2, Capterra, TrustRadius scores with review counts and date pulled; 90 day sentiment split and top themes | Public review sites, social listening |
| Hiring | Open roles by function, 12 week trend, top locations | Careers page or jobs API |
| Compare | 3 rivals: founded, HQ, ownership, SPAN install base, link to each profile and the comparison page | Public plus SPAN |
| FAQ | Owner, CEO, revenue, how many companies use it, affiliation | Sourced answers |
| Markdown and AI | Copy as Markdown, `.md` twin, Ask AI links | Generated |
| Platform band | One CTA to the free sample, book a call as a text link | Fixed |

## Workflow
1. Take the brief from `compact-keywords` (keywords like "[company] revenue", "[company] competitors").
2. Research public facts with WebSearch and WebFetch. Open every page you cite. Where sources disagree (for example Zoho FY25 revenue Rs 12,313 crore vs Rs 13,543 crore), show the range and name both.
3. Request platform fields from the data team: install base by product, country and size split, internal stack, switching signals. Until they arrive, mark blocks "Sample figures".
4. Write the answer box, FAQ and section leads with `span-answer-page` writing rules and `vinh-copywriting`.
5. Build the page with `frontend-design-pro`: full width, Mulish, SPAN greens, sticky "On this page" rail with related lists, bars to one scale, micro-interactions, a build notes toggle on prototypes.
6. Generate the Markdown twin with the same facts, the source URL and the "not affiliated" line.
7. Interlink: the profile links to every product users list, rival profiles and comparison pages; each of those links back with anchor text "<Company> company profile".
8. Run the gates.

## Gates
1. `no-ai-slop` Gate mode and zero em or en dashes
2. The Page Extras Gate in `span-answer-page`
3. `agent-ready`: JSON-LD Organization (about the company, with sameAs), Dataset for the SPAN figures, FAQPage, BreadcrumbList; `.md` twin; llms.txt entry
4. `visual-verify` at 390 and 1440, light and dark; tables scroll inside their own container
5. Legal line present: "SPAN Global Services is not affiliated with <Company>." Name and logo used only to identify the company; never redraw a logo.

## Scale rules (avoid scaled content abuse)
- Publish in batches of 20 to 50 profiles, not thousands at once.
- Each profile needs unique data in at least three blocks plus a written answer box.
- Every block shows its own last updated date; refresh monthly.

## Output
Published artifact or HTML for Manu's team, the `.md` twin, the brief updated in the Celsus vault under `Efforts/Active/SPAN Content/Profiles/`, and a one line request for critique.