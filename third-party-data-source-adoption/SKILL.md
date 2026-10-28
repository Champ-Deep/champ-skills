---
name: third-party-data-source-adoption
description: "Use when building on an external data feed or API."
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

## Procedure

1. **Read the terms page, not the pricing page.** Fetch the terms and search for
   the clause naming your use: commercial use, redistribution, re-serving as an
   API, white label, monetisation of derived insights. The pricing page
   advertises tiers; the terms grant rights, and they are written separately. A
   vendor can advertise a free tier and forbid commercial use of it — free
   *access* and the right to *resell* are different grants. See
   `references/licence-and-terms-checks.md` for the clause checklist and the
   flags that mean "do not build on this yet".

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

## Pitfalls

- **Writing per-platform OAuth when a broker already holds the connections.** App
  review, refresh rotation and secret storage are the broker's job; duplicating them
  buys you credentials that rot and a compliance review you did not need.
- **Reading the pricing page for rights.** Rights live in the terms, and the two
  are written by different teams.
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

## References

- `references/licence-and-terms-checks.md` — clause checklist, probe recipes, the
  flags that gate a source.
- `references/corpus-substrate-probe.md` — measuring whether a feed holds the data
  a feature needs, and reporting a zero honestly.
- `references/entity-resolution-benchmark.md` — free ground truth from a corpus
  that carries both a name and an identifier, plus threshold and tie rules.
- `scripts/probe-endpoint.sh` — status/content-type/key-required probe for one
  endpoint.
