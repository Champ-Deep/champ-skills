---
name: live-server-browser-gates
description: "Use when a browser test drives a real server."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [testing, playwright, browser, gates, multi-tenant, verification]
    related_skills: [verification-gate-integrity, optional-input-degradation]
---

# Live-server browser gates

## When to Use

A Playwright test that drives a real server against a real database, rather than
`TestClient` and in-memory fixtures. Applies when a gate needs cookies set by the
server, a row written by a request, or two processes talking over HTTP.

Triggers: "the browser test passes but the feature is broken", "it reads the wrong
database", "the test only works against one customer", "the click times out in the test
but not by hand".

Companion `verification-gate-integrity` owns the general rules on proving a gate is
armed. This one covers the specific ways a gate that drives a live system interrogates
the wrong system and stays green.

## The rule

**A gate pointed at the wrong target is worse than no gate, because it is believed.**

Unlike a unit test, a live gate cannot be trusted to fail when its inputs drift. It
reads real shared state, real configuration and real copy, and every one of those can
move out from under it while the assertion text stays identical.

## Read the server's environment, not the test runner's

A `conftest.py` that sets `DATABASE_URL` for unit tests does so at import time, so
every later read of `os.environ` in the same process returns the overridden value. A
browser test that spawns a subprocess to inspect the database therefore inspects the
in-memory SQLite fixture while the server wrote to Postgres, and a consent decision
that was recorded correctly reports as unrecorded.

Capture the live value *before* it is replaced, in a module imported first for that
ordering, and pass it explicitly:

```python
LIVE_DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg://localhost/app")
os.environ["DATABASE_URL"] = "sqlite+pysqlite://"   # unit tests only
```

Going through `app.config.settings` is not a fix. Settings loads a `.env` relative to
the current working directory, finds none under `backend/`, and silently falls back to
a SQLite file with no tables.

## Never hardcode one tenant's copy

Launcher labels, headings and button text are per tenant. A gate that expects
`"See times"` stops testing the widget the moment it is pointed at a site whose label
is `"Book a time"`, and it fails for a reason that has nothing to do with touch
targets or accessibility.

Read the expected value from the same API the page reads it from, and fail loudly if
the key is missing rather than falling back to a default that belongs to one site.

## Put every new server state into every client's predicate

A live gate usually drives several screens at once, and each screen decides what to
show by OR-ing the states it knows: `hidden = !!(combat || check || vote || ...)`. When
the server gains a new top-level state key (a run, a phase, a mode), that enumeration
is stale everywhere it was not edited, and the stale screen falls through to its
default: a lobby overlay reappears mid-game, a "waiting" banner shows over live play.
Grep the whole client for the derived predicates (`hidden =`, `classList.toggle`,
`display:`), not just the file you are adding the feature to, and add the new key to
each. The symptom in the gate is an assertion failing against copy that should never
be visible, which looks like a timing flake and is not.

## The background server predates your edit

A server launched with `background=true` in an earlier call keeps serving the code
as it was then, while the files on disk show your new code, so the gate measures
the previous build and the mismatch surfaces as a puzzling logic bug. Kill and
relaunch it after every server-side edit, relaunch with the env pinned explicitly
for this run (the backend path under test, the database, the port) so ambient
config cannot pick a different path, and confirm the new process is the one
listening before re-running.

## Repeat the run before calling it green

A multi-client scenario with vote resolution, timers and reconnects can pass once and
fail twice; a single green run proves nothing about stability. Loop the spec until you
have N consecutive passes or the first failure (capture the failing assertion text on
the first failure, not a re-run), and only then report. A failure that appears in the
loop and not after is still a real defect: hunt it in the assertion rather than
rerunning until it disappears.

## Identify elements by role or class, never by a substring of their text

`":" in label` matches `"Source: Writing (/writing)"` as readily as `"10:30"`. The gate
then measures a citation chip and reports it as a too-small booking button, which is a
real number and a wrong claim.

Selectors must be unambiguous within the whole document, not merely plausible. When a
substring is genuinely the only handle, assert on the element's class as well.

Prefer structural or role selectors over presentational classes: a restyle that
renames the class (a grid row, a button variant) breaks the spec for a reason unrelated
to behaviour, and the red run then reads as a regression. When a restyle is
intentional, change markup and selector in the same edit and re-run the whole spec in
the same pass.

## Dismiss overlays the way a user does

A fixed consent banner intercepts clicks at phone viewports. Reach past it with a
forced click and the gate proves nothing; instead dismiss it the way a visitor would,
and treat an interception you cannot dismiss as a real layout defect.

When bounding boxes do not overlap but a click still fails, the blocker is stacking
context or pointer-events, not geometry. `document.elementFromPoint` at the click
coordinates names the culprit.

## Read security headers off the artifact that ships

A CSP or security-header gate must assert against the same bundle and configuration
that will deploy, not against the dev server: dev and deploy reach header middleware
through different paths, so a green dev read can pass while the shipped Worker or
container serves different headers. Stage the built deploy artifact with a copy of
its static assets (a dry-run bundle plus a copied asset snapshot is enough, local
database included) and assert on the served response there. One served-header read
from the deploy-shaped bundle replaces any number of dev-server reads.

## Prove the gate discriminates

Point the repaired gate at the pre-fix build and confirm it reports the old numbers. A
gate rewritten this session has never been seen failing, so its passing means nothing
until it has been observed to catch the defect it was written for.

## Run the same gate against every target, and survive your own last run

A journey that only ever hit localhost has never seen production's env vars, domain
or database, and a green deploy status does not substitute: the status reports the
container, not the journey. Parameterize the base URL and credentials inside the
script and run the identical file against each deployed URL after every deploy.

Log one `STEP <what succeeded>` line per stage so a timeout names the stage that
died instead of only the selector it died on, and make creation steps idempotent
(check the entity exists before creating it): a journey that assumes a clean world
dies on a duplicate during its second run, and a gate that cannot be re-run after a
partial failure is a gate you get exactly one attempt with.

## A third party's origin allowlist is not your bug

A widget served from an allowlisted host rejects your preview origin with no
`Access-Control-Allow-Origin`, and every state of the gate goes red at once. That is the
service enforcing its policy, not a defect in the site or the service, so never widen
the allowlist, weaken CSP, or deploy the build to production just to make the gate
color-change: each trades a test result for a real security or traffic change.

Serve the exact build under an origin the third party already allows: run the local
server, then map the allowed hostname to it in the browser only
(`--host-resolver-rules=MAP <allowed-host> 127.0.0.1:<port>`), and re-run the identical
gate. The third party sees an origin it trusts, nothing on the network or in config
changes, and the pass is honest. Report the method with the result (local origin
mapping, no CORS/CSP change, no deploy) plus what stayed untested (real provider call,
physical devices, other browsers), so a mapped-origin pass is never read as a test of a
production deploy.

## Pitfalls

- **Reading `os.environ` after a conftest override.** Reports the fixture, not the server.
- **Resolving config through `settings` in a subprocess.** Silent SQLite fallback, no tables.
- **Hardcoding per-tenant copy in an expectation.** The gate silently stops testing.
- **Selecting elements by a text substring.** Measures the wrong control with a real number.
- **Forcing clicks past an overlay.** Hides exactly the defect the gate exists to catch.
- **Reporting a green run without a seen failure.** Pass counts prove collection, not coverage.
- **Asserting on copy that a new server state can still make visible.** Derived
  `hidden`/visible predicates enumerate old states; the new one re-reveals an overlay.
- **One run of a timing-dependent multi-client spec.** Flake or defect, one pass cannot
  tell them apart; loop to N consecutive passes and capture the first failure's text.
- **Selecting by a class the restyle is about to rename.** Gate red for cosmetic
  reasons; update selector and markup together.
- **Running the journey only against localhost after a deploy.** Production env and
  domain differ; re-run the identical parameterized script at the prod base URL.
- **Creation steps that assume a clean world.** The second run dies on duplicates;
  check existence before creating so a partial run can resume.
- **Reading CSP or security headers off the dev server.** Dev and deploy middleware
  differ; assert against the staged deploy bundle instead.
- **Driving a server started before the edit.** Files new, process old; restart
  with a pinned env and confirm the listener, or the gate grades the old build.
- **Widening an origin allowlist to make a preview gate pass.** Buys green with a real
  security change; map the allowed hostname onto the local build instead.
- **Reporting a mapped-origin pass as a production test.** Same origin string, different
  deployment; state the method and the untested remainder with the verdict.
