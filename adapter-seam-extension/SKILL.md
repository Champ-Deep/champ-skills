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

## Pitfalls

- **A `*_provider` setting in config that the factory ignores.** Check the
  factory, not the config.
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