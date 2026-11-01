---
name: entity-resolution-benchmark
description: Free ground truth for judging an entity-matching rule, plus the threshold and tie rules.
---

# Entity resolution benchmark

Use when a matcher, dedupe rule or "is this the same company" decision needs to
be scored before it gates anything. The expensive mistake is tuning a threshold
against a handful of hand-picked pairs and shipping it.

## 1. Find a corpus that carries both a name and an identifier

The free ground truth is any source where the same row holds a human label and a
stable key: a CRM export with `company_name` plus `domain`, a catalogue with
`title` plus SKU, a directory with `name` plus email domain. Pairs sharing the
key are positives; rows with the same key are guaranteed matches, so you never
have to label them by hand.

```python
by_key = defaultdict(list)
for r in corpus:
    by_key[r["domain"]].append(r["name"])

positives = [(a, b) for names in by_key.values() for a, b in itertools.combinations(names, 2)]
```

Sample negatives from rows with *different* keys but similar names, which is
where the matcher will actually be wrong.

## 2. Score the rule, not the intuition

Run the candidate rule over both sets and report precision, recall and the
confusion counts. Save the pairs and the scores next to the work (the effort
folder, or `docs/evals/` in a repo): no record means not verified.

## 3. Threshold and tie rules

- Pick the threshold from the score distribution, not from a round number. If
  nothing separates the two distributions, the rule is not ready and no
  threshold will make it ready.
- **A name-only match never auto-resolves on a tie.** Two different companies can
  share a name across regions and domains; only an exact identifier hit settles
  a match unattended. Everything below the threshold routes to review with the
  competing candidates shown.
- Re-run the benchmark after any change to the normalisation (case folding,
  suffix stripping, alias maps), because those changes move both distributions at
  once and a threshold that held before can invert.

## 4. Report the boundary, not just the number

State which classes the rule handles (exact key, exact name plus country,
fuzzy) and which it deliberately refuses, with the review queue size implied by
the chosen threshold. A single accuracy figure hides the fact that the hard
cases all fell through to a human queue nobody sized.