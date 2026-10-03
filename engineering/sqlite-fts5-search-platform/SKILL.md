---
name: sqlite-fts5-search-platform
description: Use when building faceted search over merged spreadsheets or any row store on SQLite, especially with full-text search, evidence-bearing detections, or many normalised enum columns.
version: 1.0.0
license: AGPL-3.0
author: Deep
metadata:
  hermes:
    tags: [sqlite, fts5, facets, search, taxonomy, data-quality]
    related_skills: []
---

# SQLite FTS5 faceted search platform

## When to Use

Building a searchable, filterable store out of spreadsheets or any row data:
merged contact/company lists, technographic or firmographic detection, faceted
buyer UIs, live counts. Also when a schema or a Jev-driven product needs a
fast, zero-infrastructure query layer the team can actually run.

## Parse once, persist many

Reading 117MB of xlsx costs ~3.5 minutes. Writing 676k rows costs seconds. Split
the pipeline: normalise into in-memory structures, `pickle` them next to the
store, and let the persist phase reload the cache. Tuning a taxonomy rule then
costs 40 seconds instead of 4 minutes, which is the difference between
iterating and not.

Bulk-assign primary keys in memory and `executemany` the inserts. Per-row
`execute()` + `last_insert_rowid()` is ~1.4M round trips and turns a 40-second
write into a 7-minute one.

## The vocabulary rule

Category and enum values that are stored in a column AND filtered on must have
exactly one definition, in a dependency-free module. Three copies is the failure
mode: short codes in the detector, display names in the signature table, a
third list in the query layer. Every filter then matches zero rows while the
data looks perfect and no test fails. Symptom to watch for: a filter that
returns 0 on data you can see. The category module must not import the code that
needs the network, or a plain search inherits an HTTP dependency.

## Short tokens need word boundaries

`if "cto" in title` matches "dire**cto**r". This routed 13,509 "Director" rows
into an IT bucket and inflated apparent coverage to 98.5% when the true figure
was lower. Match tokens of <=5 characters on `(?<![a-z0-9])token(?![a-z0-9])`,
and keep phrase matching as substring so longer needles still match inside
longer titles.

The same bug recurs one layer up. Adding "president" to a founder tier made every
"Vice President" a founder. Ambiguous phrases get stripped before matching, not
patched title by title, and `Product Owner` is an IT delivery role that matches
"owner" as a business-owner test.

## Semantic traps in real title data

Missing spaces are the norm: `SalesDirector`, `Chief MarketingOfficer`,
`FounderCEO`, `Managing DirectorIndia`. Split camel case before matching, and
strip a glued country suffix. A dual role reports at its most senior tier, so a
Founder & CEO outranks a standalone CEO.

Validate the taxonomy against the real data, not against expectations. Sample
100k raw titles, print the buckets, and hand-label 30-50 of the highest-volume
ones. A taxonomy that looks right on paper is routinely wrong on 24k messy
strings, and the test that catches it is the one that prints what the rules
actually produce.

## Facets: join once, never EXISTS-per-row

`EXISTS (SELECT 1 FROM contacts x WHERE x.company_id=c.company_id AND x.fn IN
(...))` is semantically identical to a join and took over 45 seconds against
588k companies, because it re-evaluates the contact predicate per company. One
join with the shared WHERE clause: 231ms.

Build the WHERE clause with an explicit alias contract. Contact-level filters
(function, quality, phone) reference `p.`; a company-only query has no `p` and
raises "no such column". Emit the contact predicate against the contacts alias
in every query that has one.

Facet counts must equal the corresponding search counts. Assert it:
`facets()["states"][0]["count"] == search({"states":[key]})["total_contacts"]`
for every facet. If they disagree, one of them is being quoted to a buyer.

Unfiltered facet calls degenerate: an `IN (SELECT ...)` subquery over every row
is slower than querying the table directly. Branch on whether a filter is
active. Covering indexes in filter-then-group order
(`(quality, fn, company_id)`) take a 949ms facet call under a second.

## FTS5 injection

Never interpolate user text into `MATCH`. Tokenise to `[A-Za-z0-9]+`, quote each
token, and escape quotes by doubling. A bare `*(` raises `fts5: syntax error`
and returns HTTP 500. Validate after tokenisation as a second gate, and skip the
`MATCH` clause entirely when nothing survives, or an empty expression is worse
than no clause.

## A web platform is not an install

If you detect technology from live sites, a marketing site's framework is
evidence about the *website*, not the company's business systems. Give every
detection an evidence class and a confidence, and exclude weak classes from
every quotable count. Store the matched string on each row so any single result
can be audited back to the bytes that produced it.

Two false-positive generators to expect: a generic session cookie name (`SID`)
attributes the vendor's product to every site on that stack, and a vendor's own
partner page names their product hundreds of times. Only vendor-namespaced
cookies count, and matches on pages reading "our clients" or "become a partner"
get a confidence penalty.

## Grade every record

Claims like "verified people you can call" are only defensible if each record
carries its own grade. Compute it, store it, and let the UI show it. The three
signals that dominated real data: single-character or initial-only names,
role/generic mailboxes (`info@`, `sales@`), and an email domain that does not
match the company's own domain. Never drop these rows, grade them and let the
buyer filter. Roll the grade up per company so a company with no clean records is
visible in the store rather than implied.

## Assert provenance survives refactors

A `sources` table went permanently empty because a refactor moved its INSERT into
a function that no longer owned a connection, and nothing failed loudly. Assert
the provenance table is populated and its row counts sum to the raw input. Same
class of bug: a foreign key or alias that only exists in one of two code paths.

Benchmark each facet case in its own process with a hard timeout. A Python
`signal.alarm` does not interrupt a blocking SQLite call, so one slow query
silently eats the whole run and the remaining cases never report.

## A UI that no test ever paints ships broken

88 facet-key assertions, 98 end-to-end assertions and a UI-contract suite all
went green while the shipped page had no pagination, a blank filter sidebar on
first paint, and a one-line regex that made the most-used suggested query return
zero. Every suite had asserted `/api/*`. None had asserted the page.

It happens because the environment has no browser, so rendering feels impossible
and asserting the markup exists feels like the next best thing. It is not:
markup that exists has still never been painted.

Headless substitute, no browser required:
1. **Execute the page's own JS against the live API.** Extract the real
   filter-construction function (a natural-language parser), run it in node,
   assert the output is a filter the API accepts. This is the highest-risk code
   in the UI and it is pure logic, so it is fully testable without a browser.
2. **Assert the arithmetic a buyer reads**, not just that a query succeeds:
   page 2 must not repeat page 1's rows, and the total must stay stable across
   pages.
3. **Walk the DOM in user order**: boot, then click each suggestion, then read
   the result. A boot call like `run(false)` that skips first-paint facet
   rendering is invisible to per-function tests.
4. **Assert absence of failure text**: no bare `no records matched` empty state,
   no raw placeholder where a real value belongs.

Pulling JS out of HTML: never regex to the first `}`. A body containing braces
yields a silently truncated function, which is a `SyntaxError` far from the
cause. Count braces to match, re-attach the signature, and remember `.mjs`
forbids top-level `return`, so export a wrapper rather than the bare body.

Language-level bug classes (acronym casing, word boundaries, `sap` inside
`GSAP`) belong in a table-driven test listing raw and expected side by side.

## A chart and the search beside it must quote the same number

A dashboard added on top of a working search introduced a disagreement that no
API test could see: the bar showed 1,435 companies running WooCommerce, clicking
through gave 294. The chart counted *held* companies; the search counts
companies *reachable by a contact*. Both defensible, both true, and a bar whose
number moves when you click it loses the deal in the room.

Store both counts and draw on the one the buyer can act on. Label the gap rather
than dropping it, because the gap is the finding: the 1,141-company difference
was real firms we hold no person for.

Then assert the agreement: for the top N chart rows, the chart's number must
equal the search's number for the same filter. This is the single highest-value
assertion in a product whose output gets quoted to customers.

The same trap with a word. The funnel said "callable people 442,498" meaning
grade A plus a phone, while the search's equivalent filter returned 43,956
(phone, LinkedIn and a corporate email together). One meaning per number, and
the note beside each step must state the definition in full.

## Chart data comes from precomputed aggregates, not live GROUP BY

`SELECT fn, COUNT(*) FROM contacts GROUP BY fn` over 675k rows took 8.3s. A
chart cannot wait for that on every paint. Build small aggregate tables once
(api/viz_build.py, ~4s for all seven) and have both the API and the page read
them. Rebuild them from the same `run.sh` guard that checks the store exists, so
a missing build step reads as a build step rather than as empty panels.

## Axis labels are the distinct values, not the rows

The bubble chart's x-axis was built by iterating rows, producing 65 slots for 9
functions, so every bubble was positioned against its own private column and the
grid rendered empty. It was genuinely empty. Build axes from
`set(values)`, and assert `0 <= index < len(axis)` for every point. This is the
visual twin of "a filter that returns 0 on data you can see".

## Plain-language parsers need table-driven tests run in node

A natural-language-to-filter parser in a page is pure logic, so it is fully
testable without a browser: extract the real function out of the shipped file,
run it in node, assert the filter it produces returns rows. Two traps when
slicing JS out of HTML:

- Never regex to the first `}`. Count braces, and include the signature. A
  truncated body is a `SyntaxError` far from the cause; a body without its
  header is an `Illegal return statement`.
- Slicing a `const X = {...};` needs brace AND bracket depth plus a stop at a
  semicolon at depth zero. Parens alone walk straight past an object literal
  whose values are arrays and emit the next statement as data.

Assert the *absence* of bad inference, not just the presence of good: "CTO does
not add a cloud category". The bug that mattered was a single regex mapping a
job title onto a technology category, which made the most-used suggested query
return zero while real matching records sat in the store.

## Facet geography: a city is not a state

Check what the column actually stores before trusting a UI's location list.
`hq_state` holds `Maharashtra`; the list also offers `Pune` and `Bengaluru`, so
`states=["Pune"]` matched nothing while 25,050 companies sat in that city. A
location filter must resolve a city against the city column, and the city set
belongs in one shared module with the other vocabularies, not typed into a JS
list where it drifts from the data.

Zero results from a location facet is a vocabulary mismatch before it is a data
gap.