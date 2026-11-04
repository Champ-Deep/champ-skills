---
name: third-party-data-source-adoption
description: "Use when evaluating or building on an external data source."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [data-sources, licensing, terms, api, due-diligence, entity-resolution, adapters]
    category: engineering
    related_skills: [verifying-supplied-plans, competitive-research-verification]
---

# Third-party data source adoption

Load when a product or plan proposes building on an external feed, API or
dataset: a breach feed, a news API, a compliance registry, a firmographics
provider, a fraud or identity service. The work is not "call the API". It is
deciding whether this source can legally and factually carry the feature before
anyone builds against it.

**Trigger on:** 'use X's API for our product', 'here is a data provider to
integrate', 'we need a feed of ...', 'is this API good enough for the feature',
'they say it's free for business use', a plan table naming third-party sources,
or any adapter layer whose sources are not all equally usable.

## The rule

**A source is not usable until its terms permit your use AND its corpus contains
the data your feature needs. Both checks are cheap and both come before the
build.** A plan that treats a source as usable because its pricing page looks
friendly has verified neither.

These fail independently and each kills the feature differently:

| Failure | Symptom | Cost |
|---|---|---|
| Terms forbid the use | Works in dev, unlawful in the product | Legal exposure, takedown, rebuild |
| Corpus lacks the data | Feature runs, returns nothing | The feature is the pitch; the pitch is empty |

**First: reuse the connection broker if one exists.** When the platforms the feature
needs already sit behind a broker Deep uses (Treg, treg.to), build the adapters against
the broker's documented endpoint shapes instead of implementing per-platform OAuth,
app review and token storage: the broker holds every platform credential and your code
holds none. Verify the broker's auth before promising a live pull (`treg connections`);
a broker 401 is a human login step, so stage the exact login and token-mint commands as
a blocked decision rather than retrying or stubbing the pull. If the broker bills per
call, pass its cost-cap and attribution headers so one retry loop cannot run the bill.

**Check the catalog one level down, before writing a direct client.** The same
broker often carries the individual vendor we were about to integrate (an HLR
network, a lookup API, a search provider) as its own routes:
`treg catalog search <vendor>` returns endpoints named
`<vendor>.<domain>.<action>`, each with the upstream route, a price and an
answer shape. When the vendor is there, call it through the broker: the
credential already exists, prices are visible at adoption time, and no
procurement step lands in the path. Building the direct client instead buys a
second credential that has to be bought and provisioned by a human, which turns
a feature that could ship today into a capability block. If the search returns
nothing, the direct client is correct and the credential becomes a blocked
decision card. See `references/broker-routes-and-billing.md` for the full
recipe, including how to tell reported price from actual spend.

## Procedure

0. **Check the account's own dashboard for an account-level default before
   designing config for a required block.** Many providers (a registrar, a
   payments processor, an ads platform) accept a contact or profile block once
   at the account level, or hold one on file already. Read the provider's UI, or
   an unauthenticated probe, before concluding the block must ship in every
   payload: the answer decides whether a missing human input blocks the first
   test at all, and it costs two minutes against a blocked deliverable.

1. **Read the terms page, not the pricing page.** Fetch the terms and search for
   the clause naming your use: commercial use, redistribution, re-serving as an
   API, white label, monetisation of derived insights. The pricing page advertises
tiers; the terms grant rights, and the two are written separately. A
vendor can advertise a free tier and forbid commercial use of it: free
*access* and the right to *resell* are different grants. See
   `references/licence-and-terms-checks.md` for the clause checklist and the
   flags that mean "do not build on this yet".

   **Then map each clause onto a specific line of your own system, and bucket it
   before you report.** A clause you cannot point at a file, table or flow for is
   a clause you will argue about twice. Two buckets, decided by what the clause
   tests, and never by which section number it carries:

   - **Entity-scoped**: tests *who the customer is*. Eligibility, competitor
     exclusions, who counts as an Authorized User. A different contracting entity,
     or keeping an affiliate's staff off the key, can settle these outright.
     Verify the corporate relationship from records rather than assuming it, and
     state the condition that keeps it satisfied.
   - **Artefact and clock-scoped**: tests *what you built and how long you hold
     it*. No dataset or derivative derived from the service, retention limited to
     the term, deletion with proof on exit, no making results available to third
     parties. A different entity and a different database move these not at all.

   Reporting the agreement as one verdict is wrong in both directions: all-blocked
   hides a restriction behind a clause you already solved, all-cleared lets a solved
   clause carry one it never addressed. Report the split, name for each clause the
   code path it touches (the write-back's upsert target, the sync, the client
   deliverable), and give the remedies as options rather than a refusal: a written
   permission the terms themselves invite, a non-persisting design that stays
   inside the grant, or an exposure ruled on knowingly. Refusing to build is one
   option, not the default.

2. **Probe what the paid tier actually gates, before budgeting for it.** Plans
   routinely price a subscription that the feature does not need, because the
   gated operation is not the operation the feature performs. Call the
   unauthenticated endpoint and read the status:

   ```bash
   scripts/probe-endpoint.sh 'https://api.example.com/v1/catalogue'
   ```

   Metadata and catalogue endpoints are frequently public and keyless while only
   *search by subject* is gated. If the company-level layer is free and only the
   per-subject layer is paid, the free tier is enough to validate the product and
   the purchase belongs to a later gate.

3. **Measure the substrate against the plan's own examples.** Before building a
   feature on a feed, resolve the plan's example entities to the source's
   identifier space and count hits across the *whole* corpus:

   ```python
   hits = [r for r in corpus if r.get("domain") in {v.domain for v in example_entities}]
   print(len(hits), "of", len(example_entities))
   ```

   Zero is a finding, not a bug to debug, and it arrives far too late if skipped.
   See `references/corpus-substrate-probe.md` for what a zero means and how to
   report it as a plan-level defect rather than an implementation detail.

4. **Gate the adapter in code on the terms finding.** When a source's terms forbid
   or gate the intended use, keep the adapter and have it refuse:

   ```python
   commercial_use = "approval-required"   # free | approval-required | prohibited

   def fetch_events(self, since=None):
       guard_commercial_use(self.id, self.commercial_use, self.approved)
       ...  # transport lives below the guard, never above it
   ```

   Guard before the network call so an unapproved build never touches the
   endpoint. A later written approval then switches the feature on without a
   rewrite, and the licence problem cannot ship by accident.

5. **Build only to the plan's own gate.** When a plan phases work behind
   validation gates, build only the earliest phase a gate has not foreclosed.
   Work done behind an unpassed gate is thrown away rather than extended.

6. **Send the provider its own field names, and its own required-block rules.**
   A provider validates its documented payload, not your internal model: an
   unknown field name is rejected or silently treated as absent, so a request
   shaped like your types fails where your types were wrong. Read the provider's
   reference (or a captured real response) for the literal names and for which
   blocks are mandatory, and pin those names in a test so a rename on either side
   breaks a test instead of a live transaction. Where a block needs data only a
   human can supply (identity, contact, billing details), send the configured real
   value or omit the block entirely: a placeholder that would become a real-world
   fact is accepted by the provider and lands somewhere it cannot be recalled.
   Stage the missing human input as a decision request listing the exact fields.

## Attribution is a product requirement

A CC BY source requires visible attribution **wherever its data appears**,
including the empty case. A renderer that emits attribution only when rows exist
drops the licence requirement precisely when a customer reads the page and finds
nothing, which is when they ask where the data came from.

Carry attribution on the event, not in the template, and assert it in a test that
covers the empty path. Fix the renderer when such a test fails; editing the test
converts a caught defect into a shipped one.

## Reporting

Rank the terms defect with the other plan-level wrong claims. A source that cannot
legally carry the product is not a footnote under the data table.

State the substrate count as the headline when it is zero, with the alternative
data shape rather than only the verdict. "This feed lists breached websites, so
large B2B vendors never appear in it" is actionable; "vendor watch had no data" is
a symptom.

## Price ceilings that actually bind

When one request fans out across paid layers (phone check, reverse lookup, email
verify, person and company enrich), "cheapest provider first" is a preference, not
a cap: when the cheap answer does not come back the router spends whatever the
policy reaches next, and one row lands on a provider priced far above the tier it
was sold as. Encode the tier as a per-call ceiling checked **before** the network
call, so an over-price attempt costs nothing instead of being logged after the
money moved, and encode a run-level spend cap that marks later work
`skipped (spend cap reached)` rather than dropping it silently or spending past
the limit.

- **Assume a layer can bill on a miss.** A paid lookup that charges for no answer
  has to show that cost beside the miss, or the row's cheapest route reads as
  expensive and nobody can see which layer spent the money.
- **Carry the per-layer cost on the result itself**, next to the serving provider
  and the endpoint used. A pipeline reporting only a total cannot be audited for a
  leak after the fact; the evidence row is what makes the next tier decision a
  measurement instead of a guess.
- **Price a tier from the rows you expect, not from one lucky row.** Each row picks
  one path through the chain, so a single sample measures one provider path. Run
  the same realistic set through each tier, put both totals next to each other,
  and let the default tier be a decision with both numbers on it: it is a price
  paid per row, not a config default.

## Pitfalls

- **Writing per-platform OAuth when a broker already holds the connections.** App
  review, refresh rotation and secret storage are the broker's job; duplicating them
  buys you credentials that rot and a compliance review you did not need.
- **Reading the pricing page for rights.** Rights live in the terms, and the two
  are written by different teams.
- **Reporting an agreement as one verdict when its clauses test two different
  things.** Entity-scoped clauses and artefact-and-clock clauses answer to
  different fixes, so a single "cleared" or "blocked" always hides the half that
  decides the build.
- **Asserting where your own write path lands from a spec diagram.** An
  architecture drawing names the destination the design intends, while the code
  names the one it uses, and the two differ whenever a sync step is deferred or
  optional. Read the write path in the repository before describing where data
  goes, then cite the file.
- **Treating a Deep pushback on a findings verdict as something to concede or
  defend.** He names an entity, a target or a scope; check it against the records
  and the code first, concede what verifies in the correction-first order, and hold
  only what his correction did not move.
- **Re-opening a clause Deep has already ruled on.** A ruling ends the analysis,
  not the need to record it: move the overridden clauses into a dated ruling
  section saying what he decided and what he delegated, rewrite the verdict as
  what was actually built, and keep only the constraint the ruling did not cover.
  The licence scope of the output survives an exposure accepted as boilerplate
  (internal use only, written permission before any client deliverable), so name
  that one line and drop the rest. A findings list that still marks a ruled clause
  as an open risk asks him for the same decision twice.
- **Treating a free key as a commercial right.** It is access, not resale.
- **Budgeting the paid tier before probing the free one.** The gated operation is
  often not the one the feature performs, so the purchase can be deferred past the
  gate that would justify it.
- **Building a headline feature on an unmeasured feed.** Count hits for the plan's
  own examples over the whole corpus; a correct feature over the wrong corpus is
  still empty.
- **Letting a gated adapter fail at import or at the call site.** Gate it in the
  method, above the transport.
- **Dropping attribution on the empty result.** Licence duty, not cosmetics.
- **Letting a name-only match auto-send on a tie.** Two different companies can
  share a name; only an exact identifier hit settles that unattended.
- **Fixing the assertion instead of the defect** when a test catches a real gap.
- **Building the payload from our own field names.** The provider validates its
  contract, not our types, so an invented name surfaces as a missing required
  field on the first live call while every unit test stays green; pin the
  provider's literal names in a test.
- **Letting the router climb when the cheap provider misses.** A miss is a reason
  to report unknown, not a licence to spend; the ceiling is what stops it.
- **Filling a required human-only block with placeholder data.** Omit the block or
  wait for the real value: invented identity or contact data is accepted, then
  cannot be recalled.

## References

- `references/licence-and-terms-checks.md` — clause checklist, probe recipes, the
  flags that gate a source.
- `references/corpus-substrate-probe.md` — measuring whether a feed holds the data
  a feature needs, and reporting a zero honestly.
- `references/entity-resolution-benchmark.md` — free ground truth from a corpus
  that carries both a name and an identifier, plus threshold and tie rules.
- `scripts/probe-endpoint.sh` — status/content-type/key-required probe for one
  endpoint.
