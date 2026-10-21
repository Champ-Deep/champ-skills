# Supplied and demo data in one store

Contracts for the moment a real file from a data team meets a database that was
built on demo rows. The rules here extend `SKILL.md`'s provenance section.

## Ingest contract: preview, then commit

An inbound file is never written straight to the live tables. Two stages:

1. **stage + preview** — parse the workbook, guess a field mapping per column,
   return per-sheet row counts by error kind (ok / bad domain / bad state / bad
   employees / no domain / missing technology) and the technologies detected.
   The human or admin UI confirms the mapping here.
2. **commit** — apply the confirmed mapping, write rows, record every changed or
   inserted row in a history table so an ingest can be rolled back.

One workbook can carry several sheets; commit them as separate batches rather
than assuming one batch per file.

## Newest-wins upsert and rollback need different stamps

When a re-load replaces a row on its natural key instead of inserting one, two
facts must stay separate: which batch created the row (rollback's handle) and
which batch last touched it (freshness). Overwriting the creating batch id with
the newest one turns rollback into a delete: the stored pre-image then carries
the new batch id, the rollback removes a row it should have restored, and the
count silently loses rows.

- keep the creating batch id on the row for its whole life; put the latest load
  in separate `updated_at` / `updated_by` columns so newest-wins and `as_of`
  freshness never move the rollback handle;
- snapshot the whole row as the pre-image, so the older timestamp travels back
  with it, and assert that in the rollback test;
- regression-test the triple: load A, re-load B over it (value and timestamp both
  change), roll back B (value and timestamp both return to A), roll back A (the
  pre-A row returns).

Freshness belongs with the number the consumer sees: expose `as_of` from the
newest contributing row so an answering agent can date the count it quotes.

## Field mapping pitfalls (all hit on real supplier files)

- **Technology from the sheet name, not the columns.** Supplier workbooks name a
  sheet after the product and carry no technology column. Fall back to the sheet
  name when no technology column is found; the mapping screen should prefill it
  so the operator confirms instead of types.
- **Normalise headers before matching.** Parentheticals (`Revenue (In M$)`),
  whitespace and case all break an exact-name matcher. Strip them first and keep
  the fallbacks (`revenue`, `revenu`, `arr`, `annual`) after normalisation, or a
  sheet silently loses its revenue band.
- **Normalise country and state codes.** Suppliers write `USA`, `United States`,
  `u.s.a.`; the store uses `US`. A lookup table on lowercase input fixes it;
  leaving variants raw splits every country filter and no error is raised.
- **Expect stray rows with no identifier.** A file can carry a note row between
  header and data. Preview counts it as rejected, and the test asserts the
  expected count per sheet, not "all rows succeeded".

## Provenance of uploaded rows

Real uploaded rows share tables with demo rows, so carry provenance on the row:
a `source` column set to `upload:<filename>` for imported rows and to the
provider name for seeded demo rows. Then:

- one `WHERE source LIKE 'upload:%'` filter gives the real set for any count;
- an answer can say which parts of it are real without a human remembering;
- a wipe of demo data never touches supplier data.

## Keep aggregates scoped like their reader

A supplied summary is only correct for the scope it was measured on. When the
data team starts reporting per region after having reported one market only:

- **do not overwrite the existing summary table** whose readers assume one row
  per subject (one row per technology, say). Add a second table keyed by subject
  *and* scope, and let each reader pick the table matching its own claim.
- **seed the new table from a checked-in file**, not from a one-off script run,
  so a rebuilt or freshly deployed database gets the numbers deterministically.
- **seed on migrate, not only at build.** An already-deployed database never runs
  the build script again; the migration path is what upgrades it.

## The real-file test

A field-mapping heuristic is only ever proven by the supplier's actual file. Keep
the received sample in the repo and assert against it:

- every sheet imports, with the expected row count per sheet;
- the guessed mapping resolved to the right fields (technology, industry,
  country, revenue, employees);
- the committed rows are distinguishable (count by source prefix);
- normalisation landed (one country code in the store, no raw variants).

Run it against a temporary copy of the seed database, never the live one, and
skip with a clear message when the optional spreadsheet parser is missing.

## Grounding an answering agent on this data

An agent that answers questions from the store must be told, in its own input,
what is real and what is demo. The schema-introspection tool is the right place:
a `notes` array listing which tables are mock, which are real, which rows carry
the upload marker, and the boolean/date conventions. The same statement goes in
the agent's system prompt so the prose a buyer reads matches the schema. If the
golden question set cannot reach a new table, say so in the report rather than
quietly skipping coverage.
