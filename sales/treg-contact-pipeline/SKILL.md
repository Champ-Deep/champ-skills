---
name: treg-contact-pipeline
description: "Build, verify and deliver account-based contact lists through the Treg API gateway with a staged, budget-gated workflow (discover, filter, verify, then buy contact data). Use for any Treg contact pull, lookalike account check or contact verification."
---

# Treg contact pipeline

Treg (treg.to) is an API gateway, not a database. One key, one base URL, 3,400 plus third-party endpoints, each priced per call or per row and relayed verbatim. It verifies the call, never the fact. Every dollar spent on a row that does not reach the deliverable is waste, so this skill runs in gated stages and pays only for rows that survived the previous gate.

First use on the Virtusa build (17 to 18 Sep 2026) cost $17.93 for 489 usable contacts, with about $12 of that on rows never delivered. Run this way, the same output costs $6 to $8.

## Non-negotiables

1. The API key lives in one place: TREG_API_KEY in /Users/deep/Celsus/.env (dotfile so Obsidian and Obsidian Sync skip it; mode 600; git-excluded), filled by Deep with read -s. ~/.hermes/.env holds only a pointer comment, never the key. Load it per run with `set -a; . /Users/deep/Celsus/.env; set +a`. Never in a vault .md note, a script, a log or a chat reply; a key pasted in chat is exposed, so ask for rotation and never use it. Grep the working folder for the key before finishing.
2. Every Treg call is made with that API key so spend is tracked per key. The treg CLI must be logged in with `treg login --token "$TREG_API_KEY"`, never a browser or email session: a session token in ~/.treg/config.json bills the org without an API key attached, which is the untracked spend Deep wants gone. Code reads TREG_API_KEY only; do not add a TREG_TOKEN fallback.
3. Snapshot the balance before and after every stage: GET /orgs then GET /orgs/{id}/balance. Read X-Treg-Cost-Micro on every response and keep a ledger file (stage, endpoint, calls, cost). Report the ledger with the deliverable.
4. Set a dollar cap per stage before the first call and stop at the cap. Ask the user before any stage expected to cost more than $5, and before any endpoint priced above $0.05 per call.
5. Save every raw response under raw/ so nothing is bought twice.
6. No em dashes or en dashes in any file or output.

## Stage 0: scope (free)

Write down before any paid call: the account list with domains (search subsidiary and brand domains for global groups: UBS Americas needs ubs.com, IG Wealth needs ig.ca and igmfinancial.com), the persona (levels and functions in, levels and functions out), geography rule, per-account cap, what the deliverable is (client approval file without contact data, internal calling file with it, or both), and the total budget. Use free endpoints to size: companyenrich.companies.search.count is free; GET /catalog/search and GET /catalog/endpoints/{id} are free and give price, latency and success rate. Estimate cost before running: rows expected times price per row, plus verification, plus email finds.

Free sizing loop, run it before quoting any universe number:
1. Find and inspect the endpoint: `treg catalog search show <name>` (the bare `treg catalog show <name>` form is rejected; the CLI answers with the exact typed form, so run what it suggests). It prints cost, the `treg call ...` invocation, and an example response.
2. Count with the whole filter object at zero cost: `treg call companyenrich.companies.search.count --method POST --data '{"countries":["IN"],"keywords":["crypto"]}'`. The count endpoint accepts every filter the real search accepts, so tune countries, keywords, industries and employee_ranges here and pay only for the final row pull. Returns `count` (capped at the plan page limit) and `total` (the true match count); quote `total`.
3. Scan a `companyenrich.companies.search.preview` (free, top 25) BEFORE you request data from a partner or write it into a plan. The preview returns a mixed bag: competitors of the client, media and blogs, tools, and personal-name domains. Exclusions and splits are decided from that sample, not assumed, and a headline count that is half junk must not be quoted to a client as an audience.

When the universe is a partner's to hold (their data team, not ours), the request that goes out specifies per segment: record count, email count, mobile count after DND scrub, consent basis, last refresh date, and a masked sample of 25 to 50 rows, plus a flag for anything that cannot go on RCS or phone. Company counts are not people counts: sizing the company base is free, people rows behind it bill per row, so hold that pull until the partner states what they already hold. Plan with count placeholders and never invent a number.

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
- Gap fill on an existing list: separate each gap from the work you did yourself. Three statuses, one per source: already in the source file (never re-billed), found by this run (billed, with cost), not found (say so, do not guess an address from a naming pattern). A reviewer's first question is which of the three a given cell is.
- Finding a person when only the role is known: for a company that gives up no named HR or function head, stage two candidates, not one. First the company's own people directory for that title, then a firm-wide people search filtered to senior titles (CHRO, CHRO, CHRO, HR head, HR director, HR manager). Rank by seniority and only promote a row whose name and title both came back with an email; a manager who can route the invitation still counts as a hit, so label it by seniority instead of calling it not found.
- Never let a role search run on an over-long title list: QuickEnrich caps the title string at 255 characters and raises an assertion after the call is built. Join the list, assert the length, and add that assert to the self-test so the guard fires before any spend.
- Reconcile the returned address against an allowlist before it reaches the deliverable: the email domain must be the company domain, a subsidiary domain, or a listed parent or alternate. Expect a few legitimate mismatches (a group on a corporate parent domain); report them as a named group with their domains rather than filtering them out silently.
- Keep raw responses keyed on the request, not just the row, and distinguish an empty result from an error. An error cached as a result is the failure that silently deletes work on resume: the run looks complete and the gap is invisible.
- Make the run idempotent and resume rather than restart. Snapshot the balance before the first call, persist every raw response as it lands, and on a crash re-run the same command: cached rows cost nothing, only the failed row is re-billed.
- Self-test on the real fixtures before spending: a dry-run self-test that reads the actual raw response files proves data-level assumptions (field names, length caps, null handling) that a syntax check never touches. Run it after every edit to a parsing function, not just once at the start.
- Phone: quickenrich.people.phone.find is free on a miss and cheap on a hit; the routed phone finder is $0.245 per hit and refuses under a low cost cap. Buy phones only for the calling file and only on request.
- Never run backfills in a parallel burst; Hunter returns 403 on bursts, so run sequentially with a short gap.
- Durability: run long paid jobs as a background process with notify-on-complete rather than a foreground poll. A foreground timeout kills the run at the row it was on and loses everything after the last write, which is exactly the spend a resume is built to protect.

## Stage 5: deliverables

Produce three workbooks with openpyxl, bold navy header, freeze panes, autofilter:

1. Client approval file: sheet What we need approved (numbered decisions with a Why column and a blank Your answer column), sheet Contacts for approval (Account, Contact Name, Title, Level, LinkedIn, City, State or Province, Country, Verified date), sheet Summary (per account counts by level plus the verification note). No email, no phone. Optional sheet Expansion accounts with fit score and one-line reasoning per company.
2. Internal calling file: the same rows plus Business Email, Email Status and Direct Phone. Never sent to the client.
3. QA log: every pulled row with status, provider current company and title, decision (SEND, HOLD, REMOVE) and the reason; a Counts sheet by stage; the cost ledger.

Describe the source to the client as our contact build. Do not name providers.

## Capping the spend inside a product

When the pull is wired into a user-facing agent rather than run by an operator, the budget
gates must live in the request path, not in the operator's discipline. Three layers, all in
code: (1) per-request scope, a hard maximum on companies per pull and title chunks per
company; (2) a per-run dollar ceiling checked before each provider call, so a runaway loop
stops at cents; (3) a per-day total across all requests. Make repeat pulls free by caching
per company plus title-chunk, so re-asking the same question costs nothing. Surface the
cap and spend-to-date in the UI (a "budget today" tile): the user sees the ceiling without
opening the console, and the visible number doubles as the check on which config the
deployed build is actually running.

## Own keys first (BYOK), and where a vendor key must live

Treg's routed endpoints (treg.people.enrich, treg.people.email.find, treg.people.search) run
"own keys first": a vendor key connected with `treg connections connect --provider <vendor>`
is tried before any Treg-billed provider and is charged 0 markup (X-Treg-Cost-Micro: 0,
X-Treg-Served-By names the vendor). Deep's standing rule: a user's own key outranks the house
key, and Treg is the first paid source in any product waterfall (ChampHarbinger
`src/lib/enrichment/config.ts`, treg rank 12, moltsets on the house key behind it).

Pitfall: connections belong to the Treg identity that holds them, not to every key you own.
A product whose TREG_API_KEY was minted under a different Treg login or org will route past
your connected vendor and pay a Treg-billed provider instead, while the call never appears
in your `treg audit`. Before claiming a vendor is live in a product, call the product with a
known contact and check (a) the vendor shows as the field source or X-Treg-Served-By and
(b) the call appears in `treg audit` under the account that holds the connection. If it does
not, either mint the product's key in that org (`treg org agent-new <product>`, so spend
has its own audit trail) or connect the vendor in the account the product key belongs to.
The MoltSets connection (2026-11-03) lives in the Champions Accelerator org under
deep@championsmail.com; direct call proof: moltsets.people.enrich.linkedin hit, 0 micro.

## Cost model to quote before starting

Per usable contact, staged: roster $0.002 to $0.005, verification $0.002 to $0.004, email $0.005 (on about 20 percent of rows), total about $0.012 to $0.015. Unstaged (buy contact data first, filter later) ran at $0.037 on the Virtusa build. Company lookalike checks: about $0.007 per named company across two providers; avoid CompanyEnrich company-search pages unless the free count shows 80 or more rows and the rows themselves are the deliverable.

## Provider quirks seen

TheCompaniesAPI mislabels industries (a trust company as home health care, an asset manager as nuclear power) and resolves some domains to affiliates; Hunter gave a 143 headcount for a 6,000 person firm; CompanyEnrich returns HTTP 400 with an empty body for bucket names it does not accept (valid: 201-500, 501-1K, 1K-5K, 5K-10K, over-10K); HarvestAPI bills 404 profile lookups; QuickEnrich tags every employee to the company HQ country. Cross-check any field you will put in front of a client.