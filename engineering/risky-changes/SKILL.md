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

Pairs with `verification-gate-integrity` (never report a pass you did not execute) and `cross-model-review` (second reader for the code).
