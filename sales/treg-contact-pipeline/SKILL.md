---
name: treg-contact-pipeline
description: "Build, verify and deliver account-based contact lists through the Treg API gateway with a staged, budget-gated workflow (discover, filter, verify, then buy contact data). Use for any Treg contact pull, lookalike account check or contact verification."
---

# Treg contact pipeline

Treg (treg.to) is an API gateway, not a database. One key, one base URL, 3,400 plus third-party endpoints, each priced per call or per row and relayed verbatim. It verifies the call, never the fact. Every dollar spent on a row that does not reach the deliverable is waste, so this skill runs in gated stages and pays only for rows that survived the previous gate.

First use on the Virtusa build (17 to 18 Sep 2026) cost $17.93 for 489 usable contacts, with about $12 of that on rows never delivered. Run this way, the same output costs $6 to $8.

## Non-negotiables

1. The API key lives in an environment variable only (export TREG_API_KEY=...). Never in a file, a script, a log, a vault note or a chat reply. Grep the working folder for the key before finishing.
2. Snapshot the balance before and after every stage: GET /orgs then GET /orgs/{id}/balance. Read X-Treg-Cost-Micro on every response and keep a ledger file (stage, endpoint, calls, cost). Report the ledger with the deliverable.
3. Set a dollar cap per stage before the first call and stop at the cap. Ask the user before any stage expected to cost more than $5, and before any endpoint priced above $0.05 per call.
4. Save every raw response under raw/ so nothing is bought twice.
5. No em dashes or en dashes in any file or output.

## Stage 0: scope (free)

Write down before any paid call: the account list with domains (search subsidiary and brand domains for global groups: UBS Americas needs ubs.com, IG Wealth needs ig.ca and igmfinancial.com), the persona (levels and functions in, levels and functions out), geography rule, per-account cap, what the deliverable is (client approval file without contact data, internal calling file with it, or both), and the total budget. Use free endpoints to size: companyenrich.companies.search.count is free; GET /catalog/search and GET /catalog/endpoints/{id} are free and give price, latency and success rate. Estimate cost before running: rows expected times price per row, plus verification, plus email finds.

## Stage 1: discover names and titles (cheap, no contact data)

Goal: a roster of name, title, LinkedIn URL per account. Do not buy emails or phones here.

- Cheapest roster: leadmagic employee finder at about $0.00125 per row, no title filter, so pull the roster and filter locally.
- QuickEnrich quickenrich.people.search.domain (GET, company_url plus comma title list) returns name, title, LinkedIn and also email and sometimes phone, billed $0.0048 per row that carries contact data and free otherwise. Use it only when the title list is tight, because every off-persona row with an email is billed. Title string is capped at 255 characters (split into several calls), pages are fixed at 20.
- companyenrich.people.search has the best filters (seniority, department, countries) and fresh titles but costs $0.0196 per row, bills the full pageSize whatever comes back, and returns no email or phone. Only worth it when filters cut the pull by more than half.
- Rejected for this job: routed treg.people.search (ignored country and limit), pdl job-title enrich ($0.38), contactout ($0.65).

Title keywords for financial services must never be bare CIO, Technology, Digital or Data. Chief Investment Officers, technology investment bankers, digital marketing and data scientists all match. Use the full title phrases (Chief Information Officer, Vice President Information Technology, Director of Enterprise Architecture) and let the local filter do the rest.

## Stage 2: persona filter (free, local)

Run the classifier on every roster row before spending again. A row passes only if it has a leadership token and a function token and no exclusion token.

- Leadership tokens: chief, CIO, CTO, CDO, CDIO, head of, director, vice president, VP, SVP, EVP, managing director.
- Function tokens: information technology, IT, technology, digital, data, analytics, AI, platform, application, enterprise architecture, architecture, transformation, modernization, engineering, infrastructure, cloud, systems, ERP, software, innovation, business technology, omni, ecommerce, automation, integration.
- Exclusion tokens (any one drops the row): investment banking, equity research, research, co-head, partner, M&A, corporate development; executive assistant, administrative assistant, assistant to, chief of staff, office of the CIO or CTO; analyst, engineer (not engineering), developer (not development), scientist, designer, agilist; audit, compliance, risk, security, privacy, financial crimes, AML, fraud, GRC, controls, supervision, asset protection, investigations; marketing, advertising, media, content, sales, selling, HR, human resources, people, talent, learning, education, recruit, culture; vendor management, VMO, procurement, sourcing, support, service desk, help desk; regional, Europe, Asia, APAC, EMEA, China, India, offshore; former, emeritus, interim, fellow, retired; associate director, assistant director, associate or assistant vice president; program or project or product manager, product owner, program or project or portfolio management, PMO, program director; CFO, finance, FP&A, accounting; chief investment officer, co-CIO, CIO of a fund or equities group; field applications, applications engineering, product applications, system applications, quantum, product definition, product marketing, R&D; solutions architect, solution architect, application architect, data architect, software architecture (individual contributors); digital trust, secure digital operations, cyber, customer experience, customer success, loyalty; manager, supervisor, business relationship, market data, data protection.

Adjust the lists per client persona and record the adjustment. Keep dropped rows in a QA log with the token that removed them; the client may widen the persona.

Geography: company-record country from providers is the company HQ, not the person. Never drop a row on it. Flag it, search subsidiary domains, and verify in Stage 3.

## Stage 3: verify in role (before buying contact data)

The client's first complaint on any list is people who have moved. Verify survivors before spending on emails.

- Company-only check: scrapecreators.linkedin.user.profile, about $0.0019 per call, private profiles return 404 free. Returns the experience list with company names, no titles. Enough to remove movers and retirees.
- Company plus title check: harvestapi.linkedin.user.profile.main (GET, main=true, url=LinkedIn URL), $0.004 per call, billed on misses too. Returns headline and experience with position, company and start and end dates (endDate Present marks a current role). Run 8 workers; 3 to 8 seconds per call.
- Order: C, Head, VP, then Director. If budget is tight, run the title check on C, Head and VP and the company-only check on Directors.
- Statuses: CURRENT (company matches the account or a known parent or brand, title same or obvious variant), TITLE_CHANGED (same company, materially different title; re-run the persona filter on the new title and keep it if it passes), MOVED (different employer, retired entry, or account role with an end date and no current role), UNVERIFIED (private or missing profile). Only CURRENT and passing TITLE_CHANGED rows go to the client. Expect about one in twelve profiles to be private.
- Company match must tolerate parents and brands: Raymond James Financial, CI Financial for Assante, Fifth Third Bank for Bancorp, Columbia Banking System for Columbia Bank and Umpqua, IGM Financial for IG Wealth, Transformco for Sears.

## Stage 4: contact data, only on verified persona rows

- Email: treg.people.email.find (served by trykitt), $0.005 per hit, returns verified true or false. Only run for rows without an email. Re-verify any email older than 60 days before a send.
- Phone: quickenrich.people.phone.find is free on a miss and cheap on a hit; the routed phone finder is $0.245 per hit and refuses under a low cost cap. Buy phones only for the calling file and only on request.
- Never run backfills in a parallel burst; Hunter returns 403 on bursts, so run sequentially with a short gap.

## Stage 5: deliverables

Produce three workbooks with openpyxl, bold navy header, freeze panes, autofilter:

1. Client approval file: sheet What we need approved (numbered decisions with a Why column and a blank Your answer column), sheet Contacts for approval (Account, Contact Name, Title, Level, LinkedIn, City, State or Province, Country, Verified date), sheet Summary (per account counts by level plus the verification note). No email, no phone. Optional sheet Expansion accounts with fit score and one-line reasoning per company.
2. Internal calling file: the same rows plus Business Email, Email Status and Direct Phone. Never sent to the client.
3. QA log: every pulled row with status, provider current company and title, decision (SEND, HOLD, REMOVE) and the reason; a Counts sheet by stage; the cost ledger.

Describe the source to the client as our contact build. Do not name providers.

## Cost model to quote before starting

Per usable contact, staged: roster $0.002 to $0.005, verification $0.002 to $0.004, email $0.005 (on about 20 percent of rows), total about $0.012 to $0.015. Unstaged (buy contact data first, filter later) ran at $0.037 on the Virtusa build. Company lookalike checks: about $0.007 per named company across two providers; avoid CompanyEnrich company-search pages unless the free count shows 80 or more rows and the rows themselves are the deliverable.

## Provider quirks seen

TheCompaniesAPI mislabels industries (a trust company as home health care, an asset manager as nuclear power) and resolves some domains to affiliates; Hunter gave a 143 headcount for a 6,000 person firm; CompanyEnrich returns HTTP 400 with an empty body for bucket names it does not accept (valid: 201-500, 501-1K, 1K-5K, 5K-10K, over-10K); HarvestAPI bills 404 profile lookups; QuickEnrich tags every employee to the company HQ country. Cross-check any field you will put in front of a client.