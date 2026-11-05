---
name: adapter-seam-extension
description: "Use when adding a new adapter/seam to an existing backend."
tags: [architecture, adapters, seams, tdd, backend, python]
---

# Adapter Seam Extension

How to add a new capability to a backend that already has an adapter registry,
without breaking every existing implementation or silently degrading the ones you
did not touch.

## The shape

Champions backends (ChampLantern, Champions B2B Workspace, Champbeam) register
capabilities behind a `get_x(provider)` factory: `get_messaging`,
`get_meeting`, `get_calendar`, `get_llm`. Settings carry a `*_provider` string.
Before extending one, check whether the setting is actually honoured. A
`calendar_provider` field that exists in config while the factory ignores it and
always returns one hardcoded class is a common state, and it is the first thing
to fix.

## Split what is ours from what is theirs

When a seam mixes two different sources of truth, give each its own method
rather than one method with flags:

- `declared(rep)` returns what WE say this resource does. Our data, trusted,
  editable, and legitimately incomplete.
- `busy(rep, start, end)` returns what THEIR system says. Foreign data, the only
  thing standing between an offer and a real-world conflict.

Conflating them produces the failure where a config value silently stands in for
a fact you never checked.

## An unimplemented method raises. It never returns empty.

An empty collection is a factual claim: "this resource is entirely free". For a
busy-calendar, missing-answer-as-empty means offering exactly the slots the seam
exists to remove, and it is indistinguishable from success in production.

```python
class CalendarAdapter:
    def busy(self, rep, window_start, window_end) -> list[Busy]:
        raise NotImplementedError
```

Keep this in the base class. Then write the test that pins it, because returning
`[]` is the tempting shortcut and the failure is silent:

```python
def test_an_adapter_that_cannot_answer_fails_loudly(db):
    class Legacy(CalendarAdapter):   # predates the seam
        def declared(self, rep): ...
    with pytest.raises(NotImplementedError):
        availability.slots(db, rep, campaign, "UTC", now)
```

Same rule for remote providers: a per-calendar access denial must raise, not
degrade to empty. `{calendars: {id: {errors: [...]}}}` is an error, not a free
calendar.

## Fetch per unit of work, never per candidate row

Any seam consulted inside a loop over generated candidates multiplies one user
action into hundreds of API calls and exhausts the quota immediately. Fetch once
for the whole horizon, then filter in memory:

```python
committed = [*held_appointments, *_calendar_busy(rep, earliest, latest)]
```

Pin it with a test that asserts the call count, not just the outcome:

```python
def test_busy_is_fetched_once_for_the_whole_horizon(db):
    stub = _use(StubCalendar([]))
    availability.slots(db, rep, campaign, "UTC", now)
    assert len(stub.calls) == 1
```

## One seam, two providers: substitute first, live second

A seam that cannot yet reach its real provider (no key on the machine) is still
buildable end to end. Put the substitute behind the same `get_x(provider)` factory
and select it by config, so the live provider is a config change rather than a
code change. Make the substitute deterministic and rule-based, never model-based:
reproducible assertions on scores, picks and counts are the whole point of testing
without a key. Any scoring rule the substitute encodes is a stand-in for the real
judgment, so report it as such and name the provider as never-yet-called rather
than letting the substituted numbers read as provider output.

## Read the fixture contract before writing tests

Seam tests fail on the fixture long before they test the seam. Grep for an
existing minimal-world helper (`make_world`, `load_world`, `seeded`) and copy
its exact call signature, including whether it takes `db` as a parameter and
what window/campaign defaults it sets. Inventing a session accessor or guessing
that a fixture namespace has a field it does not have burns several cycles and
produces failures that look like product bugs.

Then sanity-check the arithmetic before asserting on it. A window opening after
the notice cutoff yields zero slots, and a buffer wider than expected removes two
slots rather than one. When an assertion fails on a count, first work out whether
the count is arithmetically correct before changing the code.

## Prove the seam end to end, then report it

A green suite proves the seam is wired. It does not prove it changes behaviour.
Drive one recorded fixture payload from the real provider through the real
registry selection and print the before/after. "14 slots became 8, and here are
the six removed, on one API call" is evidence; "the adapter is implemented" is a
claim.

State plainly what is not live yet. If per-resource links still come from an env
setting rather than a table, say the seam is not yet reading any real data.

## Build the payload from the provider's contract, never from our model

A seam that mirrors our own field names onto a foreign API is the version that
passes every unit test and fails the first real call. Providers validate names,
not intent: an unknown name is dropped, or rejected as *missing*, so the request
does not fail where our model was wrong, it fails where the provider looked for a
value we believed we had sent. Take the field names from the provider's own
reference or a captured real response, and pin them in the seam's test as literal
strings so a rename on either side breaks a test instead of a transaction.

Three rules that travel with it:

- **Pin the miss shape alongside the field names.** What "no result" looks like
  (empty array, null, a status field) is part of the contract, and it is what the
  caller's fall-through to the next provider keys off. A test that exercises only
  the hit shape never proves the adapter no-ops on a miss instead of inventing a
  row.
- **Omit an optional block rather than filling it with a placeholder.** A
  placeholder that would become a real-world fact (a contact record, an address,
  an identity field on a registration) is worse than an absent block: the provider
  accepts it and the false data lands somewhere it cannot be recalled. Send the
  configured real value or send nothing.
- **When the provider's source is on disk, read each route handler before
  writing the call**: required query params, which auth dependency guards it
  (a per-org guard refuses a valid personal key), and side effects it triggers
  (an import that auto-queues paid enrichment). A route you can read is a fact
  to check, not an "assumption to verify later". Make the fixture refuse what
  the real handler refuses, because a fixture that answers any path under the
  route hides a missing required param. Any side effect belongs in the preview
  a human approves.
- **Configure the human-only inputs as one named env set**, and request the
  missing fields as a single decision listing them exactly. The seam then goes
  live on one redeploy instead of a redesign, and the same input serves the UI
  path that writes through the same provider.

## Ingestion into keyed records: fold, coalesce, isolate

Any writer that upserts into a table keyed by business values (technology,
dimension, value) inherits three failure classes, and each one is silent in a
single-upload demo:

- **Fold variants before you key on them.** "United States", "USA" and "US",
or "na" and "North America", are one fact typed two ways. Normalise through the
existing country/state helpers and a small region alias map at parse time;
otherwise every spelling becomes its own row and any later sum over-counts.
The alias map is the known vocabulary: a new spelling lands as its own row
until it is added.
- **A partial update must coalesce, never overwrite.** A re-upload carrying
only the contacts figure sends no companies figure and no source line. Writing
them with `COALESCE(?, companies)` and `COALESCE(?, source)` preserves the
original number and its provenance; a plain `SET source=?` replaces a real
attribution with a derived default. Same for the pre-image: save it once per
distinct key per batch, not once per row, so a key repeated inside one file
does not report a phantom update or claim to roll back two rows.
- **A bad row is a row error, not a failed upload and not stored junk.** An
unknown dimension in a closed set, or a count too large to be real, should be
collected with its row number while the rest of the file loads. Storing the
typo'd key makes it unqueryable forever; aborting the whole file punishes the
four good rows for one bad one. Keep one exception: a malformed header is the
file's contract, so that one does abort.

Keep the invariant stated in prose for whoever reads the tool's output:
dimensions are separate cuts of one population, and adding across them is
always wrong. Say it where the consumer sees it, not only in the schema.

## A registry entry is never one file

The adapter is the easy half. Before writing it, grep the previous provider's
identifier across the repo to find every site that enumerates providers: the
priority table, the reliability or confidence table, the engine's registration
call, the integrations registry, the per-provider key tester, the example env
file. One of those is usually *derived* from another, and a coverage test that
asserts every allowed name has an entry over there turns a single-file addition
into a change that stays red until the whole set lands in the same commit. Find
that binding first and land the set together.

Two economics rules belong in the same change:

- **A flat-priced provider in a per-call cost table** gets the nominal figure the
  table expects, with a comment saying billing is flat. The escalation order then
  stays a useful ordering rather than a false precision nobody can defend.
- **A metered sub-field stays unclaimed.** When a field (a mobile number, a
  sub-lookup) bills per hit at a rate far above the tier's nominal cost per call,
  leave it out of the first version. Unclaimed is a decision you can point at and
  switch on later; silently claimed is a budget bug the first batch discovers.

## The deploy lineage is its own reading pass

A repo that ships from a second lineage (an integration branch, a
platform-specific stack) does not inherit a change landed on the default branch,
and the second lineage is what the live app runs from. Treat the port as its own
pass rather than a copy:

- **Diff the target lineage's enumeration sites against the source's before
  copying anything.** Priority table, provider list, cost table: a slot present on
  one side can be absent on the other, so rank numbers and neighbour order are not
  portable, and a comment explaining the source's ordering may describe a slot the
  target never had.
- **Re-derive what that branch's own tests enforce.** Beyond the allowlist and the
  coverage test binding names to testers, a branch may carry an explicit
  "implemented providers" enum that a console reads to decide whether to report
  code behind a slot. Missing it is a silent UI lie, not a test failure. Grep that
  branch's tests for list-shaped assertions and expect every one to need updating
  in the same commit.
- **Run the target lineage's suite, not the source's.** The file count differs, so
  a green run on the branch you started from says nothing about the port.
- **Carry deploy wiring with the code.** An instance cannot see a new provider key
  until the example env file, the deploy script's name array and the worker's
  forwarded-env list all name it. Where a test keeps those three in step, missing
  the third is caught only by running that branch's suite.

## Pitfalls

- **Calling a deployment covered because the change is merged.** Merged into which
  branch? The platform builds what it is pinned to, and an unmerged local commit
  says nothing about whether a deployment exists at all.
- **A `*_provider` setting in config that the factory ignores.** Check the
  factory, not the config.
- **Assuming a new provider is one file.** Derived allowlists and the coverage
  test binding them to their testers keep a single-entry addition red until every
  enumeration site changes with it.
- **Empty-returning new methods on a base class.** Silent success, wrong
  behaviour, no exception to trace.
- **Fetching inside a loop.** One page view becomes hundreds of quota burns.
- **Guessing the fixture shape.** It is the seam's biggest time sink; grep first.
- **Trusting a count assertion over the arithmetic.** Buffers and notice cutoffs
  both move counts legitimately.
- **Declaring the dependency is optional because the happy path never needs it.**
  If signing or encoding is on the main path, the library is a real dependency;
  a hand-rolled stdlib substitute is a bug waiting to be found by the first
  production run.
- **Overwriting a file you have not read in full.** Read it, then patch narrowly,
  so an external writer's changes survive.
- **Payload field names copied from our own types.** The provider validates its
  contract, not ours, so an invented name surfaces as a missing required field on
  the first live call while every unit test stays green.
- **A placeholder standing in for a real-world fact.** Omit the block; never ship
  invented identity or contact data through a registration or an order.