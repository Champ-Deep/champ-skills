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

## Identify elements by role or class, never by a substring of their text

`":" in label` matches `"Source: Writing (/writing)"` as readily as `"10:30"`. The gate
then measures a citation chip and reports it as a too-small booking button, which is a
real number and a wrong claim.

Selectors must be unambiguous within the whole document, not merely plausible. When a
substring is genuinely the only handle, assert on the element's class as well.

## Dismiss overlays the way a user does

A fixed consent banner intercepts clicks at phone viewports. Reach past it with a
forced click and the gate proves nothing; instead dismiss it the way a visitor would,
and treat an interception you cannot dismiss as a real layout defect.

When bounding boxes do not overlap but a click still fails, the blocker is stacking
context or pointer-events, not geometry. `document.elementFromPoint` at the click
coordinates names the culprit.

## Prove the gate discriminates

Point the repaired gate at the pre-fix build and confirm it reports the old numbers. A
gate rewritten this session has never been seen failing, so its passing means nothing
until it has been observed to catch the defect it was written for.

## Pitfalls

- **Reading `os.environ` after a conftest override.** Reports the fixture, not the server.
- **Resolving config through `settings` in a subprocess.** Silent SQLite fallback, no tables.
- **Hardcoding per-tenant copy in an expectation.** The gate silently stops testing.
- **Selecting elements by a text substring.** Measures the wrong control with a real number.
- **Forcing clicks past an overlay.** Hides exactly the defect the gate exists to catch.
- **Reporting a green run without a seen failure.** Pass counts prove collection, not coverage.
