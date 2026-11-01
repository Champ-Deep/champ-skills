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

## 3. Flags that mean "do not build on this yet"

| Flag | Why it stops the build |
|---|---|
| Terms silent on commercial use | Absence is not permission; ask or treat as approval-required |
| Approval required, no published process | You cannot plan a launch date around an unknown review |
| No redistribution but the feature re-serves rows | The product *is* the redistribution |
| Attribution required in a place you cannot render | Attribution duty applies even on empty results |
| Retention or caching limit below the feature's refresh rate | The feature's own cadence violates the terms |
| Rate limit or price discovered only at checkout | Budget the real number before committing the build |

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