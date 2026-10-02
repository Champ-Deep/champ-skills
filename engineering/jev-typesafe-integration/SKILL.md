---
name: jev-typesafe-integration
description: Use when working with Jev or TypeSafe in ChampSet.
version: 1.0.0
license: AGPL-3.0
author: Deep
metadata:
  hermes:
    tags: [jev, typesafe, scoring, champset, gates]
    related_skills: []
---

# TypeSafe JEV integration

## When to Use

Any change touching `backend/src/jev/` in ChampSet, the confidence score, the
Gate 1/2/3 routing, or a new "ask JEV to judge X" question. Also when a
per-item judgement is being added anywhere and you are deciding whether to loop
or batch.

ChampSet uses JEV for probabilistic judging (gates 1 to 3) in
`/Users/deep/Apps&Projects/ChampSet/backend/src/jev/`. Upstream docs live at
`docs.typesafe.ai`; the client is `@typesafe-ai/sdk`.

## Score is 0-indexed (the rule that keeps biting)

A `score` question with N criteria returns **0 to N-1**, not 1 to N. The SDK
documents `ScoreCriteria` as "at least two descriptions indexed by score from
zero", and the API normalises by `criteria.length - 1`.

**Why:** a 1-based legend in the prompt plus a `0..N-1` validator plus a `+1`
remap silently turns "does not fit" into a middling score. This shipped in
ChampSet and was never tested at the boundary.

**How to apply:** write score criteria as a bare ordered list with no numeric
prefixes and let the wire format define the indices. If you need a 1-based
score downstream, remap once, in one place, and test the boundary.

## Speculative fan-out: batch, never loop

TypeSafe evaluates every question in ONE request against the same state, in
parallel and in isolation. Answers do not depend on what else is in the batch.
This is their documented recommended pattern.

**Why:** calling once per item is N round trips and pays the document cost N
times. Their cookbook measures 12.2x cheaper and 10.0x faster for 13 batched
questions, with no change in answers.

**How to apply:** build a `questions` object keyed per item (`page_type_0`,
`page_type_1`, ...) and make one call. Gate 1 does this now. Any new per-item
judgement should batch the same way.

## SDK basics

`new TypeSafeClient({apiKey, timeout, retry})` then
`client.systemOne({state, questions, model})`. Needs `TYPESAFE_API_KEY`.
Builders: `choice(instructions, criteria)`, `noul(instructions)`,
`score(instructions, criteria)`. Model defaults to `jev-latest`; pin via
`JEV_MODEL` when you need reproducible scoring.

## Failure modes to respect

Read `docs.typesafe.ai/model-jaggedness/jev-1.13` before trusting a judgement.
The ones that matter for data work: it does not count reliably (count in code),
score levels are weakly calibrated in numeric terms (use scores for buckets,
not magnitudes), and it reads instructions literally (state the exact condition,
put boundary cases in the criteria).

## Content-addressed records cannot hold a single owner

ChampSet's evidence passages are content-addressed: `passageId` is
sha256(url + index + text). Two rows scraped from the same page resolve to the
IDENTICAL passage id, so any mutable single-owner field on that record lets the
last writer steal it from the others. It shipped: one row lost every citation
and another was handed evidence it never cited.

**Why:** the id identifies content, but ownership is a relationship. Storing
ownership as a scalar on the content record cannot express sharing.

**How to apply:** put the relationship on the side it is expressed in. Rows
already carried `passageIds` / `evidenceByColumn`, so that became the
authoritative link and the write to the passage's `rowId` was deleted. Resolve
by joining from the owner (`evidence/row-scope.ts`). General rule: if a record
is keyed by content and more than one thing can reference it, never store the
reverse pointer as a single field.

**Testing trap worth remembering:** a unit test that calls the new helper
directly still PASSES when a caller reverts to the buggy grouping. I proved
this by reintroducing the bug and watching the tests go green. Cover the call
site too, here by reading the source and asserting the bad pattern is absent.
See `tests/evidence-ownership-guard.test.ts`.

## Design rule learned the hard way

A missing judgement must never score better than a successful one. ChampSet
shipped `fitScore === undefined -> factor 1.0`, so JEV being down made rows look
*more* trustworthy. Degraded paths get a mild penalty (`UNJUDGED_FACTOR`),
never a free pass. Keep a regression test asserting unjudged <= judged.

## The rule engine under JEV is the real product

Ship a deterministic scorer that runs with no API key, and let JEV sharpen a
ranking code already produced. Two reasons: the product still works when JEV is
down, and every score carries a written rationale a human can check. Blend in
one place only (`0.45*rule + 0.55*jev_normalised`) and keep the rule score in
its own column so a bad judgement is visible after the fact.

Score buckets, not magnitudes. "Migration deadline / Multi-threading ready /
Warming / Long tail" is a defensible output; a 0.742 is not, because the levels
are weakly calibrated.

## Two traps when normalising JEV into a stored score

**The 0-index trap compounds with any multiplier.** `score` returns 0..N-1, so
N=4 means normalise by 3, not 4. Divide by exactly one place, then assert the
boundary in a test (`0 -> 0.0`, `3 -> 1.0`).

**Blend weights must not resurrect the inverted case.** If a judged score can
land lower than an unjudged one, any weighted average hides it. Keep
`UNJUDGED_FACTOR` applied *after* the blend, and assert
`unjudged_max <= judged_min` in the test suite, not `unjudged <= judged` on one
row.
