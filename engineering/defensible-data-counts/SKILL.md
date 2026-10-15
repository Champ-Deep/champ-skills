---
name: defensible-data-counts
description: Use when a detected or derived number is shown to a buyer.
version: 1.0.0
license: AGPL-3.0
author: Deep
metadata:
  hermes:
    tags: [data-quality, detection, evidence, counts, provenance, audit]
    related_skills: [sqlite-fts5-search-platform, target-list-segmentation]
---

# Defensible data counts

## When to Use

Any task where a figure is inferred rather than given, and that figure will be
shown to someone who might act on it: technographic or firmographic detection,
install bases, market sizing, "N companies run X", coverage or reach claims,
count builders, list products, landing-page widgets, sales collateral.

The rule of the class: **a count is a claim, and a claim needs a gate.** The
gate is a named predicate in code, and every published figure passes it. A
number that was true when computed stops being true the moment a filter feeding
it changes, and the prose around it does not update itself.

See `references/evidence-classes.md` for the class decision table and the
quotable-gate pattern.

## Find what you hold before asking anyone

Before writing an intake questionnaire, a schema inventory, or a "where does
this data come from" question for a data team, search the filesystem for the
actual artefact. Name-insensitive, across the obvious export folders, not just
the project directory. Files that answer the question routinely sit elsewhere
under a name nobody would guess.

A meeting spent re-deriving an answer the machine already holds is the most
expensive kind of meeting, and a questionnaire built on a wrong assumption
inverts the whole conversation. Also check the assumption itself: one workbook
assumed a data file held a column that no supplied file contained, and the
audit's first job was to disprove it.

## Evidence class is a schema column, not a report convention

The most damaging detection bug is scoring weak context as strong evidence,
because the inflation is uniform and every count still looks plausible. The
canonical case: a vendor name on a **careers page** is evidence the company is
*hiring for* that product, not that it *runs* it. Never raise confidence
because a match came from a job or careers path — discount it and tag it
separately. Careers pages routinely embed whole ecosystems, so the hit rate
looks healthy right up until the counts are wrong.

Both signals are worth selling, as different products. An install list and a
hiring-intent list are different buys, and for cold outbound the intent list is
often the better one. The bug is never keeping the signal; it is counting both
as one number.

Store the split in the schema (`evidence_class`, at minimum `install` and
`intent`) and filter quotable counts on it. A convention documented in a README
gets bypassed by the next query someone writes.

## A category is not a qualification

Bucketing is not sellability. A CDN, a tracking pixel and an anti-bot challenge
all sit in plausible business categories, and a count built on them describes the
web rather than a market. Vendor pages, partner pages and testimonial pages
name a product hundreds of times while running none of it.

Keep a named exclusion list of non-qualifying attributes alongside the category
taxonomy, and route every published figure through one predicate such as
`is_quotable(category, evidence_class, attribute)` so no report can reintroduce
them. Keep the matched string on every detection row, so one result can be
audited back to the bytes that produced it.

## Provenance travels on the rows, not on the page

When real supplied data lands in a table that also holds demo or synthetic rows,
the row itself must carry where it came from: a `source` column (or equivalent)
that every query can filter on. A README explaining which rows are real is not
provenance, because the consumer of the data rarely reads the README, and the
counting code never does. Prefix the marker so one `LIKE` test separates the
real set for every downstream count and every answer given to a buyer.

Related, and equally cheap to get wrong: **the facts the consumer is told about
the data must live in the consumer's own interface.** If the consumer is a tool,
bot or querying agent, provenance notes belong in the tool's schema result, not
in documentation the agent never opens. A data note that exists only in a doc
cannot ground an answer that is generated from a database.

Keep the provenance of *aggregates* separate too: when a supplied summary covers
different scope (per region vs one market) than an existing summary table, seed
it into its own table. Overwriting a table whose readers assume one row per
subject silently changes every number those readers quote.

See `references/supplied-and-demo-data.md` for the ingest contract: preview then
commit, normalisation of supplied headers and codes, and the real-file test that
guards the field mapping.

## Both halves of a headline pass the identical gate

A market claim almost always has two halves: an entity count and a people
count. Filtering one and not the other is the quiet version of the whole bug —
one figure said 1,123 and the other 19,183, six times out, and the two numbers
sat in the same sentence.

Derive both from one shared predicate string, never two hand-written queries
that drift. Then assert the *invariant* rather than the value: the filtered
count must be strictly less than the unfiltered one whenever a filter is
active. A test pinning a magnitude breaks the moment the data changes and
teaches nothing; a test pinning the relationship catches the class.

## Sweep every published copy when a gate changes

A figure already written into a doc, deck, vault note, spreadsheet or chat reply
is a cache entry with an invalidation dependency on the filter that produced it.
When a gate changes, sweep all of them in the same commit as the fix — including
the ones you are currently looking at.

Keep a "first reported" column beside the corrected one whenever a wrong number
has already reached a reader. Silently replacing it leaves them with no way to
know the number moved, which is worse than the original error.

State what you could not source as `GAP` with the reason, in the artifact
itself. A sheet of placeholders that looks filled is more dangerous than an
empty one. When only some sources were checked, label each source's status on
its own (checked live, quoted as reported, not reachable) rather than one
blanket disclaimer over the whole artifact.

## Published numbers must agree with each other

Before a figure goes in front of anyone, audit the artifact's own arithmetic and
its neighbours:

- **Percent breakdowns must sum to 100.** A sum above 100 usually means a
  catch-all row ("Others") is counted alongside the rows it contains; restate the
  total with the exclusion named, never round the discrepancy away.
- **One quantity, one number per page.** A page quoting three different totals
  for the same thing in its headline, stat strip and table means the copy came
  from different sources. Trace the one you can source and flag the rest.
- **Identical figures on unrelated pages are copied boilerplate, not
  measurement.** A number (or product blurb) sitting on a page where it has no
  business is template residue; report it as a content defect, do not cite it.
- **An exact integer ratio across almost every row is a formula, not data.** If
  column B equals a fixed multiple of column A on nearly all rows, every one of
  them derives from one computation; say so instead of presenting them as
  independent observations.
- **Two sources disagreeing is most often a scope mismatch, not an error.** Ask
  what each covers (one country vs global, one product vs a suite) before
  calling either number wrong, and put the question to whoever owns the data.
  The same holds across measurement *models*: a vendor's modelled estimate
  against counted sessions from an analytics tag is two different measures, so
  "flat there, up here" is a mismatch to name, not a failed replication.

## A zero can mean nobody was measuring

Before publishing that a source shows nothing, or that it "does not back" a
claim, check that the source was configured to measure that thing at all.
A switched-off tracker, a wrong entity or brand key, or a range older than the
tool's own data start all return clean zeros indistinguishable from a real
absence, and a feature that is off makes "no change" look like proof of
stability. Report the configuration state alongside the number, and send the
question to whoever owns the measurement rather than resolving it yourself.

## Build the deliverable, then verify its cells against source

Writing the consumer of a number is a verification pass, not just an output
step. Producing a workbook, dashboard or sheet forces every figure back through
a query, and that is how an inflated count gets caught — a scratch script
asserting totals is not enough, because it usually shares the same mistake.

When a deliverable's cells are the interface, script the verification: read each
written value back and compare to a fresh query, and assert that no cell which
should be a `GAP` carries a number.

## Long-running probes: verify once, then stream

Detection runs are long, heartbeat-spammed, and often resume or get killed.
Answer a liveness question with a check that cannot lie:

- `pgrep -f` rather than `ps aux | grep`, because grep matches its own command
  line and reports phantom processes. Count the processes you expect, not the
  lines a grep produced.
- Confirm progress by sampling a row count twice a few seconds apart, not by
  trusting a status line. A frozen count with a live-looking process means the
  process is not the thing you think it is.
- A heartbeat for a session already seen to exit is a replay of buffered
  output, which may include output older than that run's own final state. Say
  so once, in one line, and stop. Re-verifying a settled result on every replay
  burns the session and teaches the user nothing.
- When a killed run's heartbeats keep arriving, say so once and move on.

## Report coverage bias where the count is shown

Some fraction of any scan is unreachable: bot walls, dead hosts, timeouts.
That gap is not random, it skews toward mid-market and non-global companies, and
it belongs next to the number rather than in a footnote. The same applies to a
date field that records when the source file *claims* a record was verified
rather than a live check — name the field for what it is.

## References

- `references/evidence-classes.md` — the class decision table (supplied,
  counted, estimated, demo) and the quotable-gate pattern.
- `references/supplied-and-demo-data.md` — ingest contract for a real file
  meeting a demo store: preview then commit, header and code normalisation,
  row-level provenance, scoped aggregates, the real-file test.
