---
name: risky-changes
description: Use when a change touches data, billing, defaults or customer-visible behavior.
---

# Risky changes

Adapted from David Ondrej's `risky-changes` (davidondrej/skills, MIT). Origin: a filter passed every test and turned off 99% of the feature on live data. Tests prove the code does what was written. Only measurement proves it is useful.

## Applies when a wrong call is expensive or visible
Public fields or filters, dropping or reordering upstream data, billing or quotas, thresholds and defaults, scoring that a buyer sees (see `defensible-data-counts`), any assumption about external data. Unsure means apply it.

## Steps
1. List the assumptions. Mark each evidenced or unverified.
2. Research each unverified one separately: how leading products decide it, what real data looks like, what users need. Contradicting evidence means redesign. Say gaps out loud.
3. Measure 10 to 20 realistic cases against the real source. Hard numbers, before and after. Save the cases and results next to the work (for Celsus efforts: the effort folder; for repos: `docs/evals/YYYY-MM-DD-<focus>.md`). No record means not verified.
4. Anything customers see or pay for goes to Deep as a decision card with the numbers. Never buried in a default.
5. Within one day of shipping, measure on real traffic, read-only. Report differences from the plan.

## Removing a layer from a live pipeline

Dropping a provider, a paid step or a feature flag out of a pipeline another lane is already
building against. Steps 1 to 5 above still apply; these are the ones a removal adds.

1. **Prove the remaining path carries the result set alone, before removing anything.** Run
   the same realistic cases with the layer forced off and compare output field by field
   against the full run. If a field only the removed layer supplied still needs a value, the
   removal is not safe, and the measurement names which layer has to take it over.
2. **Remove the layer's derived state, not just its call site.** A provider leaves behind
   spend caps and quota counters, capability flags, preflight and estimate fields, result
   columns, cache keys with their TTLs, and the request parameter that turns it on. Anything
   left behind reads as a live feature that silently does nothing, and a cache key left behind
   serves the removed provider's answers as if they were fresh. The absence proof lives in
   `verification-gate-integrity`.
3. **Reset per-run derived state whenever a re-run can change the layer set.** A job re-run
   with fewer layers answers out of the previous run's leftovers unless you clear them, so an
   old network name or company reads as this run's result. Clear at the start of every run,
   then prove it: run once with everything on, run again with everything off, and assert every
   layer reports as not requested.
4. **Ignore unknown parameters instead of rejecting them for the change window.** The
   consumer's already-served bundle keeps sending the removed flag until it redeploys, and a
   422 on a stale parameter turns a cosmetic staleness into a broken screen. Reject only what
   you can prove no running client sends.
5. **Hand the consumer lane the field-level diff, then hold the deploy line.** Removed
   fields, added fields, changed fields and every health flag that moved, written on their
   card, and no further deploy until they confirm they are building against what you shipped:
   a deploy behind their back invalidates the contract you just handed over.
6. **Leave the removed provider's credential in place and name the delete command.** Deleting
   a secret is Deep's action, not a cleanup step; report it as set, unread, delete with this
   command, so it is one decision away without being made for him.

Pairs with `verification-gate-integrity` (never report a pass you did not execute) and `cross-model-review` (second reader for the code).
