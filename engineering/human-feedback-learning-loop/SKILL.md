---
name: human-feedback-learning-loop
description: "Use when a system learns from human corrections."
tags: [learning, feedback, personalisation, prompt, safety, migration, fail-soft]
---

# Learning from human corrections

## When to Use

Any time output is generated for a person to approve, edit, or reject, and the
edits are expected to make later output better: draft copy, suggested replies,
recommendations, classifications. The signal is already being captured and
usually discarded. This is how to capture it.

Triggers: "make it sound more like the user", "learn from preferences",
"personalise over time", "improve from feedback", "keeps learning", or any
queue where a human edits generated text before it is sent.

## Learn from the direction of the edit, not from the output

The final text alone says what the person wrote. The **diff** says what they
wanted. Classify each correction and weight accordingly:

| Signal | Weight | Why |
|---|---|---|
| Words they **added** | strongest | their own vocabulary, in their voice |
| Sentences they **deleted** | strong | the model's instincts, corrected |
| Length delta | medium | reveals tolerance for brevity |
| Approve with no edit | weak positive | says the model was fine, nothing about the person |
| Reject | counter only | says the draft was wrong, not how they write |

The most common design error is counting an approval as a voice sample. Ten
untouched approvals teach the system nothing, and treating them as evidence
produces a confident profile built on no signal at all.

```python
@property
def is_informative(self) -> bool:
    return self.kind in ("adopt", "adjust", "rewrite")   # not "accept_as_is"
```

## Gate on sample size, and scale by consistency

Two edits are a coincidence. Requiring a minimum before acting is the
difference between "this person writes short sentences" and "from two data
points, this person never uses the word however" — and the second produces a
caricature, which is worse than the default because it is confidently wrong.

Confidence is **agreement**, not volume. Ten samples that all say the same
thing is a habit; ten that half-contradict each other is noise. Treat those as
equal and you get a system that is wrong with authority:

```python
def _agreement(values, target, tolerance):
    return sum(1 for v in values if abs(v - target) <= tolerance) / len(values)
```

Then scale by sample size and cap below 1.0 — a trait inferred from writing must
never outrank a preference a person stated.

**Expose maturity as a state, and act on nothing until it is reached.** Return
`no_signal | collecting | forming | reliable | strong` plus the threshold, and
render the counting state as an explanation ("2 of 3 edits seen") rather than as
an empty panel that looks broken.

## A human veto outranks any amount of inference

Store the vetoed key permanently. Stripping a trait from the current list is
not enough: the next few edits re-learn it. Persist the refusal and filter on
every derivation, then test that more contrary evidence does not resurrect it.

Vetoes must be **visible** in the response, not silently dropped. A rejected
trait that vanishes reads as a bug; showing "you told us not to learn this" is
what makes the control feel real.

## Untrusted values do not get interpolated into a prompt

A learned value reaches an LLM as text, so treat it as an injection vector
even though a human wrote it — the value may be attacker-influenced through an
upstream dataset, or a person's client may be compromised.

- Constrain the alphabet. Alphabetic-only makes it impossible to close a quoted
  span or carry a newline into the prompt.
- Refuse instruction-shaped words. Individually innocuous words (`always`,
  `include`, `booking`) become an order when a prompt reads them in sequence.
- Discount the weakest signal. A single learned word is trivially mimicked;
  discount it below structural traits regardless of frequency.
- Sanitise again at render time. Two checks at two layers, because the first one
  is the layer that gets refactored away.

**Probe the injection, do not assume it.** Write a runnable script that puts an
adversarial edit through the real path and prints the assembled prompt. A
reported hole may not reproduce, and the real weakness may be narrower than the
headline — keep the reproduced part, and harden the underlying issue anyway.

## Layering is a safety property, so assert the order

State hard rules first, then marketer-authored voice, then learned voice last,
each marked as subordinate. Then pin the ordering with a test so a refactor
cannot silently invert it:

```python
assert system.index("Never invent facts") < system.index("Learned from")
assert "phrasing and rhythm only" in system
```

Also assert that the **absence** of the feature leaves the prompt byte-identical
to before it existed. That is the regression that proves no default path moved.

## Persist it, or it does not exist

Derived state in memory is lost on every restart and every new worker, so the
first N corrections are spent relearning what the last N established. Give it a
table and a migration, and let the repo's drift test find the wiring mistakes —
it compares two hand-written statements of the same schema and names the exact
mismatch (`modify_nullable`, `add_fk`). Nullability, `ondelete`, and JSON
`server_default` must agree on both sides.

Register the model in whatever registry imports the existing models. A model
that is not imported there is invisible to both `create_all` and the drift
test.

Recompute anything re-derivable on load rather than trusting stored output: a
stored copy from an older version of the rules can disagree with the current
rules, and the disagreement is invisible.

## Fail soft at every boundary, and prove it

Learning is a nice-to-have sitting in the path of something that already works.
If it throws, a good message stops sending. Every read returns "nothing learned
yet" and the previous behaviour stands; every write swallows its own error.

The consequence must be stated in the module docstring in one line — what is
lost when this fails and why losing it beats the alternative — so a future
maintainer can check themselves instead of guessing.

Then pin the degradation with a test that passes a deliberately broken session:

```python
assert await learned_brief(_Broken(), account_id) == ""
assert (await load_profile(_Broken(), account_id)).edit_count == 0
```

Validate storage on read, coercing per field and dropping what does not parse.
A malformed row must degrade to an empty profile, never to an exception inside
a send path.

**Fail-soft hides its own bugs.** An opaque driver error surfaced only as a log
line, and nine tests failed at once because of it. So when a fail-soft layer is
new, write the happy-path test first and watch it pass before writing the
degradation tests — otherwise a bug inside the catch block is indistinguishable
from intended degradation.

## Make the learning inspectable

Ship read-and-correct endpoints with the profile, because a system that quietly
reshapes how someone sounds based on inference is not one a person can consent
to — and consent requires seeing the thing and refusing it.

Per trait show the confidence, the evidence count, and the underlying edit
pairs. A learned trait a human cannot inspect is indistinguishable from one the
system invented.

## Prove the loop as a user, not as a test

Unit tests cover the derivation. The walkthrough is what proves the feature:
fresh state learns nothing, N-1 edits still learn nothing, the Nth unlocks it,
the brief appears in the real assembled prompt, it survives a new session
against the same database, a veto sticks, and the payload the UI renders is
JSON-safe.

Drive it with the product's own service to build fixtures (`connect_account`,
not a hand-built ORM row) — guessing model field names costs cycles and produces
failures that look like product bugs. For SQLite, use a temp **file**, not
`:memory:`: an in-memory database is per-connection, so `create_all` on one
connection leaves the next one looking at an empty schema. Call the project's
model-import registry before `create_all` or it silently skips those tables.

## Pitfalls

- **Counting untouched approvals as voice samples.** They teach nothing about
  the person and are the fastest route to a confident empty profile.
- **Confidence from volume alone.** Consistency has to be measured, or
  contradictory samples produce high confidence in noise.
- **A veto that only strips.** Store it or it is re-learned from the next edits.
- **Interpolating a learned value straight into a prompt.** Constrain the
  alphabet, refuse instruction-shaped words, sanitise at render.
- **Assuming a reported injection hole without probing it.** Run the adversarial
  value through and read the assembled prompt.
- **Persisting derived output instead of the inputs.** Recompute on load so the
  rules can change without a backfill.
- **Leaving the module unwired and calling it done.** Passing tests on a module
  nothing imports proves it compiles. Grep for the import.
- **Adding state to a loop.** Load once per run, not per item.
- **Omitting a second call site.** Grep for every caller; the second path stays
  on the old behaviour silently.
- **Letting learning break sending.** Degrade to the previous behaviour, and pin
  that with a test.
- **Blindly stringifying an identifier for a typed column.** Coerce to the
  column's type (`uuid.UUID`) at one helper, because the failure appears as an
  opaque adapter error that fail-soft then hides entirely.