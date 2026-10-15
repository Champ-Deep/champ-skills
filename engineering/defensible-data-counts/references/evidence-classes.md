# Evidence classes

How to classify a number before it is shown to anyone, and how to keep the
classification from eroding in code.

## The decision table

| Class | What it means | Where it may appear | Gate |
|---|---|---|---|
| `supplied` | Given to us by a named party, unmodified | Anywhere, quoted as reported | Label the party and the scope it covered |
| `counted` | Derived by our own predicate over a full corpus | Headlines, buyer-facing claims | Predicate named in code, corpus coverage stated |
| `estimated` | Scaled, projected or modelled from a sample | Internal sizing, never a headline | Carry the projection factor on the row |
| `demo` | Synthetic, for a demo or a test | Screens, tests, fixtures | Never in a buyer-facing figure |

The damaging failure is an `estimated` or `intent` row counted as `supplied` or
`install`, because the inflation is uniform: every count still looks plausible
and nothing raises an error.

## The quotable-gate pattern

One named predicate, called by every path that produces a published figure. Not
a filter in each report, because reports get copied and the copies drift.

```python
def is_quotable(row):
    return (row.evidence_class == "install"
            and row.category not in NON_QUALIFYING
            and row.source_kind != "partner_page")
```

Assert the *invariant*, not the value, in tests: with a filter active, the
filtered count must be strictly less than the unfiltered one. A test pinning a
magnitude breaks the moment data changes and teaches nothing; a test pinning the
relationship catches the class of bug.

## Scope is part of the class

Two supplied counts that disagree are most often two different scopes (one
market vs global, one product vs a suite), not one wrong number. Name the scope
of every supplied figure beside the figure itself, and put the reconciliation to
the party who owns the data rather than resolving it in the report.

See also `supplied-and-demo-data.md` for the ingest contract that keeps supplied
rows distinguishable from demo rows in the store.
