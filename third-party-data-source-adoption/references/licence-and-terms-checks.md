---
name: licence-and-terms-checks
description: Clause checklist and probe recipes for judging whether a third party's terms permit a planned use.
---

# Licence and terms checks

Read when a plan proposes building on an external feed or API. The job is to
decide whether the source can legally carry the feature before anyone builds
against it. The pricing page advertises tiers; the terms grant rights, and they
are written by different teams.

## 1. Fetch the terms, not the pricing page

Pull the terms of service, acceptable-use policy and any API or data-licence
page. Search each for the clause naming your intended use:

- commercial use of the data
- redistribution or re-serving as an API
- white label, or embedding in a product sold to third parties
- monetisation of derived insights (selling analysis, not raw rows)
- caching, retention and refresh-rate limits
- attribution requirements

A vendor can advertise a free tier and forbid commercial use of it: free
*access* and the right to *resell* are different grants.

## 2. Probe what the gated operation actually is

Call the unauthenticated endpoint and read the status before budgeting the paid
tier:

```bash
scripts/probe-endpoint.sh 'https://api.example.com/v1/catalogue'
```

Metadata and catalogue endpoints are frequently public and keyless while only
search by subject is gated. If the free tier already covers the operation the
feature performs, the purchase belongs to a later gate.

## 2b. Map each clause to a line of your system, then bucket it

Point every clause you found at a specific file, table or flow before reporting.
A clause with no code path attached gets argued twice: once as abstract legal
worry, once as an implementation dispute.

Bucket by what the clause tests, not by its section number:

| Bucket | Tests | Settled by | Worked examples |
|---|---|---|---|
| Entity-scoped | Who the customer is, and who may act for it | Contracting entity, ownership records, who holds the key | Competitor exclusion, eligibility, the definition of Authorized Users (usually employees plus wholly or majority owned subsidiaries) |
| Artefact and clock-scoped | What you built, and how long you hold it | The design: where results are written, whether they persist, what leaves the building | No dataset or derivative from the service (aggregated or de-identified included), retention limited to the term, deletion with proof on exit, no supplying results on behalf of a third party |

An entity change fully settles the first bucket and does not touch the second. A
design change fully settles the second and does not touch the first. Report both
rows: naming one and implying the other follows is how a real restriction gets
carried into the build unnoticed.

Each clause also needs its remedy named as an option. In order of cost: a written
permission the terms themselves may invite (a "contact us and we may enter into a
separate agreement" clause is an invitation, not a dead end), a design that stays
inside the grant (a live lookup that is never persisted, a source tag so exit
deletion is one query), or an exposure accepted knowingly and recorded as a ruled
decision. "Do not adopt" is the last option, not the first.

## 3. Flags that mean "do not build on this yet"

| Flag | Why it stops the build |
|---|---|
| Terms silent on commercial use | Absence is not permission; ask or treat as approval-required |
| Approval required, no published process | You cannot plan a launch date around an unknown review |
| No redistribution but the feature re-serves rows | The product *is* the redistribution |
| Attribution required in a place you cannot render | Attribution duty applies even on empty results |
| Retention or caching limit below the feature's refresh rate | The feature's own cadence violates the terms |
| Rate limit or price discovered only at checkout | Budget the real number before committing the build |
| A policy cites "our other terms of use" or binds "use of this Site" to Terms, and no terms page resolves | Unfound terms are a finding, not SILENT; quote the reference and list every URL tried |

A keyword sweep (scraping, robots, database, permission) misses two shapes. Also
grep for `terms of use|terms and conditions|these Terms|continued use|licensee|licen[cs]e`,
because incorporation by reference and data-reuse clauses rarely use the scraping
words. Quote an enumerated clause whole: sources often run `1) ... 2) ... 3) ...`
with no punctuation between items, so a quote cut at `2)` drops the clause about
combining the data with other sources.

## 4. Gate the adapter in code

Record the finding as `commercial_use = free | approval-required | prohibited`
and have the adapter refuse below the threshold *before* the network call, so an
unapproved build never touches the endpoint. A later written approval then
switches the feature on without a rewrite, and the licence problem cannot ship
by accident.

## 5. Report the terms defect as a plan-level finding

A source that cannot legally carry the product is not a footnote under the data
table. Rank it with the other plan-level defects and name the alternative: a
provider that permits the use, or a product shape that stays inside the grant.