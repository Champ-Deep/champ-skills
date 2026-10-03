---
name: repo-design-probe-first
description: Use when designing a repo feature from real file:line proof.
---

# Design against a real codebase: probe, don't assume

When asked to design a feature for an existing repo, every number and every
claim about existing behaviour must come from executing the real code. A design
doc that asserts "the gate has no parameter X" is worth nothing unless checked.

## Procedure

1. **Read before designing.** The files named in the brief, plus their callers
   (`grep` for the function, not just its definition). Find the *second* call
   site of anything you plan to change; two-path bugs are the common miss.

2. **Check whether it already exists.** `git status --porcelain` and search for
   an untracked/in-flight module covering the same ground. Another agent may
   have shipped part of it. Probe that implementation and report findings
   against it rather than silently redesigning from scratch.

3. **Write probe scripts in scratch, never in the repo.** Import the real
   modules and call them. Probe scripts must be re-runnable and must print
   their own evidence.

4. **Verify DDL with the repo's own drift test.** Copy the alembic dir to a
   tmpdir, drop the proposed migration in, `upgrade head`, then run the same
   `compare_metadata()` call the repo's migration test uses. Assert zero diff.
   Note: alembic `env.py` is async, so the URL needs an async driver
   (`sqlite+aiosqlite://`) even for a sync inspection client.

5. **Run the full suite and explain every failure.** Distinguish pre-existing
   from introduced. Check for wall-clock / env dependencies rather than
   assuming your change caused it.

6. **Correct your own probe's printed claims.** A probe that prints a wrong
   arithmetic result or a mislabelled conclusion is worse than no probe. When
   output contradicts a narrative, fix the narrative.

## Pitfalls

- A naive substring search (`'voice' in source`) matches unrelated identifiers.
  Match the import, not the word.
- Print the real result, then write the conclusion from it. Do not write the
  conclusion first and hunt for support.
- Deltas need two counters: raw (permanent, gates maturity) and decayed
  (per-review, carries current belief). Raw-only is a ratchet where a changed
  mind can never win; decayed-only makes a quiet account oscillate in and out
  of relevance.
- If a claim is only asserted, verify it. "Rule X is not gated" is checkable in
  two lines and is often load-bearing for the whole design.

## Deliverable

Design doc citing `file:line` throughout, a probed migration file, a stated
build order, and an explicit scope boundary (what this deliberately does NOT
do). Report what was verified vs what remains open.
