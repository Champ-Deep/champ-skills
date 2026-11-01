---
name: corpus-substrate-probe
description: Measuring whether a feed actually holds the data a feature needs, and reporting a zero honestly.
---

# Corpus substrate probe

A feature built on the wrong corpus runs perfectly and returns nothing. Measure
the substrate against the plan's own examples before any adapter is written.

## 1. Resolve the plan's examples into the source's identifier space

Take the example entities the plan names (companies, domains, people, products)
and map each to the identifier the provider keys on: domain, vendor id, email
domain, ticker.

```python
examples = load_plan_examples()          # from the plan document, not memory
hits = [r for r in corpus if r.get("domain") in {e.domain for e in examples}]
print(len(hits), "of", len(examples))
```

Count across the *whole* corpus, not a page of it. A provider that looks thin on
the first page and rich on the tenth is a paging bug in your probe, not a finding.

## 2. What a zero means

Zero is a finding, not a bug to debug. Three shapes, and they are different
findings:

| Shape | Diagnosis |
|---|---|
| Identifier space mismatch (your domain never appears) | Wrong key: re-probe with the provider's own identifier before concluding anything |
| Corpus genuinely lacks the entity class | Substrate defect: the plan's examples are not in this feed |
| Probe reads a filtered or paginated view | Re-run unfiltered before reporting |

Only the second is a plan-level defect worth blocking on, and only after the
first and third are ruled out with an executed probe.

## 3. Report it as a plan defect, not an implementation detail

State the substrate count as the headline when it is zero, with the alternative
data shape rather than only the verdict. "This feed lists breached websites, so
large B2B vendors never appear in it" is actionable; "vendor watch had no data"
is a symptom. Carry the alternative into the plan as a named requirement: what
data shape would satisfy the feature, and which provider plausibly holds it.

## 4. Keep the probe re-runnable

The probe script lives in scratch or `scripts/`, prints its own numbers, and
takes the example list as an argument so the next run substitutes a different
plan's examples without a rewrite.