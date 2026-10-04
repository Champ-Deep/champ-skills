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

## A regex `||` chain tests only the LAST alternative

```js
if (/a/ || /b/ || /c/.test(t)) { ... }   // WRONG
```

`.test()` binds to `/c/` only. `/a/` and `/b/` are RegExp OBJECTS, which are
always truthy, so the branch fires on **every input**. It reads as a compound
condition and behaves as a constant.

This shipped in a query parser as `if (/it (people|team)/ || /tech (people|team)/ || /info tech/.test(t))`,
which pinned **every** query to the IT department and silently deleted 6 of 12
companies from a headline suggestion. No error, no empty state — just a
plausible wrong answer, which is the hardest kind to catch.

`.test(t)` must be on **every** alternative. Prefer:

```js
if (RX_A.test(t) || RX_B.test(t)) { ... }
```

Sweep for the shape rather than trusting a review to catch it: for each line,
count regex literals and `.test(`/`.match(` calls; `literals >= 2 && calls <
literals` is the bug. Skip comment lines, or the fix's own explanatory comment
gets flagged. Always verify the sweep against a hand-written reproduction
before trusting it to pass.

## Assert on what runs, never on what the source contains

A suite that greps `app.js` for a token proves the token exists. It does not
prove the function runs, the route accepts the verb, or the DOM updates. That
gap shipped four separate bugs in one round: a POST to a GET-only route (every
chart panel stayed a skeleton), a pager with no wrapper element, a sort control
wired to nothing, and a filter rail that scrolled away from its table. All four
passed every string assertion.

Run the page. jsdom plus a real `fetch` against the live API is enough to catch
this whole class, and it needs no browser backend:

- inline `styles.css` into the DOM, because jsdom will not fetch a linked
  stylesheet and every `getComputedStyle` assertion is otherwise vacuous
- assert each panel's *rendered child count* (`svg`/`bar`/`bubble`), not that a
  container div exists, and that nothing is left holding a skeleton class
- assert the HTTP method that was actually sent
- assert `querySelector` can find the control, not that its class name is in
  the file. A component with no wrapper element fails this and passes a grep.

This is the single highest-value test in any project whose output is a web page.

## A parser's leftover free text must be a word SET

Deciding what to send to full-text search by joining the consumed values into a
string and testing `consumed.includes(word)` is a substring test: `cto` is not
in `c_suite`, so it survived into the search box and matched nobody, while `it`
was dropped for appearing inside `IT & Technology`. Build a real `Set` of
tokens.

Then strip structure words. `shops`, `with`, `companies`, `team` match zero
records, so leaving them in the query guarantees an empty result on a filter
that is otherwise correct.

Assert the *negative* too: for each canned query, assert the function filter is
exactly what was asked for. A parser that quietly adds a plausible filter looks
identical to one that works until you count companies.

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

## Two <script> tags share a scope; window.eval() does not

Testing a multi-file page with jsdom, each `window.eval(src)` is its OWN function
scope. A `const get = ...` in the first file is invisible to the second, so the
second throws `get is not defined` on every call and its view stays a skeleton.
Concatenate the files into ONE eval so the harness matches a browser.

The same harness caught two bugs that make this permanent:

- **A duplicate top-level `const` is a SyntaxError that kills the entire
  script**, not just that line. A new file re-declaring `$`, `esc` or `fmt`
  renders nothing at all while the page still looks like it loaded. Declare
  shared helpers once, in one file, and have the others use them.
- **Script order is load-bearing**, not cosmetic. The file that DECLARES the
  helpers must load before the file that CALLS them.

Also assert that assets are *served*, not that their filenames appear in the
HTML. A `<script src="/views.js">` with no matching route 404s silently, and
"views.js is in the page" passes. Parse the HTML for the assets it references
and fetch each one. A hand-written route per asset guarantees the next file is
forgotten; mount the directory instead.

## A ratio, not a count, is the insight

"X and Y appear on 180 companies" is a fact that means little. "That is 40x more
often than chance" is the finding. Divide the observed count by the expected one
from the independent margins: `expected = total[a] * total[b] / n`. Rank
relations by lift, not by count.

Three failure modes, all of which shipped as confident nonsense:

- **Alias pairs dominate.** Before collapsing product aliases, the two strongest
  "relations" in an entire landscape were `NetSuite + Oracle NetSuite` (lift
  271) and `Tally + TallyPrime` (140) — one product spelled two ways. Tell a
  buyer that Salesforce's biggest co-occurrence is itself and they stop
  believing every other number on the page. Normalise to a product family
  BEFORE any co-occurrence maths.
- **The family map must be explicit.** A fuzzy substring rule merges Svelte
  with SvelteKit and Dynamics GP with Dynamics CRM, erasing exactly the
  distinctions a seller is paid to notice. Aliases means vendor prefixes and
  marketing editions, never separate products or separate editions.
- **Concentration must be a union.** Dividing the leader's company count by the
  LARGEST single technology in a category is dividing a number by itself, which
  yields exactly 1.00 for every category and therefore measures nothing. A
  company can run several products in one category, so the denominator is the
  union of those company sets. Assert the values DIFFER across categories;
  equal values everywhere is a bug signature, not a finding.

## Text tokens must clear 4.5:1, and the check must be numeric

A palette token that clears 2.8:1 is a fine chart fill and unreadable in a
sentence. Two tokens shipped at 2.86:1 and 2.72:1 while being used as body text
on card surfaces.

Split the token rather than moving it: keep the saturated brand value for marks
and fills (`--rose-mark`) and add a lifted value for text (`--rose`). Then assert
the ratios IN THE TEST SUITE, computed from the CSS, for every text token
against every surface it appears on. A design-system rule checked by reading the
stylesheet is not checked.

`#6E8894 -> #A0B1B9` and `#E8415A -> #F7A0AA` cleared 4.5:1 on both `--navy-2`
and `--navy-3`.

## A job ad is not a technology install

A careers page lists every tool a company has *ever bought*, plus every tool the
role might use. In one store, 244 companies carried 5-23 phantom technologies
from a single such page, and the worst held 23: a company appeared to run
Workday, SAP, Salesforce and ServiceNow simultaneously.

The failure is easy to miss because the rows are labelled `intent` and nothing
downstream read that column. A technology filter built as
`EXISTS (... i.tech IN (?))` returned those companies for a query about a system
they may not own, so every count, chart and shortlist described a stack that
does not exist.

**Evidence class belongs in the WHERE clause, not only in the response.**

    i.tech IN (?) AND i.evidence_class = 'install'

A hiring signal is real signal, so keep the rows and expose them as intent. But
never let them satisfy an install query. Assert it with a real known-bad case:
pick the company with the most intent rows and require that it does not appear
in an install filter for any technology it holds only as intent. A generic
"filter works" test passed for months while this was broken.

## Invalid CSS renders unstyled and raises nothing

`var(var(--x))` and `var(--token-that-was-never-declared)` both render as
nothing. The page loads, the DOM is correct, the numbers are right, the tests
pass, and the design is simply absent. 22 invalid declarations shipped this way.

Three checks, all cheap, all of which belong in the suite:

- every `var(--x)` is declared somewhere in the file (exempt any set inline by
  JS via a `style` attribute)
- no `var(var(` and no self-referential `--x: var(--x)`
- a bulk rename must not rewrite a value that is *already* `var(...)`

When mapping invented tokens onto an existing palette, replace the whole
`var(fake)` expression. Replacing the bare name rewrites `var(--paper)` into
`var(var(--ink))` and silently breaks every rule it touched.

## A subject line must identify its own trigger

Two angles can share a display name: "Commerce operations" is triggered by both
Shopify and WooCommerce. Rendering the angle name alone produced two identical
subjects derived from different stacks, and a draft whose headline technology
was chosen by highest confidence rather than by the angle's own trigger put
"Oracle NetSuite" in the subject of a Shopify pitch.

**Rule: the technology named in any customer-facing string must be the one the
argument actually rested on.** Pick it from the trigger, never from a parallel
`max(confidence)`. Then assert the relationship in the test: parse the tech out
of `facts_used` and require it appears in the subject.

Corollary for tests: an assertion of the form `a is None or b` passes when `a`
is None, so it verifies nothing on the exact case you added it for. Build the
lookup, require it to be found, then compare.

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