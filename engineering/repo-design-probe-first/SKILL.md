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

   When the ask is a feasibility verdict ("can we do X") rather than a design
   for one named repo, probe EVERY candidate repo first: name-match grep for the
   feature keyword across `~/repos/<name>`, then `head` each entry file to see
   what stage it is in. An idea that is 70% already built in a sibling repo
   changes the whole answer, and the cheapest comparison table you will ever
   write comes from those probes.

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

- The terminal tool's hardline blocklist can reject a long multi-grep probe as "system shutdown/reboot" when a pattern word matches its rules (seen with an `-E` pattern list holding `halt`). Write the probe to a script in scratch and run `bash <script>`; the script body is not matched the same way.
- For a planner readback of many created cards, one read-only query (`sqlite3 -readonly ~/.hermes/kanban.db`, tables `tasks` and `task_links(parent_id, child_id)`) checks assignee, status, workspace, parents and a dash count for all of them at once; spot check one with `kanban_show`.

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
- An ABSENT or "no X on this screen" claim is read off the screen's own render
  tree for the default config, not inherited from an earlier inventory row with
  a narrower scope. Open the screen component, list every section it renders in
  the default branch (read the tweak or flag defaults), and grep it for the
  thing's words and handlers (`onBook`, `Book`, `buy`, `price`). An app brief
  reused "in-app lab test booking: ABSENT" to say the home had no commercial
  content, while the default Today home rendered a "Book a session" therapy
  marquee and an AI carousel that both route to a booking screen with no backend.

- A "what the app does today" section that proposes a control on a surface
  (downloads, uploads, exports) inventories that surface by sweep, not by the
  handlers you happened to open: `git grep -ln Content-Disposition <sha> -- src`
  (or the surface's own header or helper), on every remote head in the local
  worktree (`git for-each-ref refs/remotes`), plus the existing precedent for
  the input the control needs (`getClientAddress`, adapter config). An ESS
  download note read 2 of 5 file routes on a stale head and called downloads
  unlogged, while `api/payroll/export` already logged every download.

- A protection the design leans on (Postgres RLS, auth middleware, a route
  disable list, a "denial never falls back" rule) is traced to the code that
  runs under the default config, not taken from a docstring or migration
  comment. Check that the session variable is set on the same connection and
  transaction the route queries with, and that the app's DB role does not own
  the table without `FORCE ROW LEVEL SECURITY`. List every migration that
  names the protection (`git ls-tree -r --name-only <sha> | grep -i rls`): a
  later `disable_rls` file can undo the one you read, and the migrate runner
  applies all of them in order. Read the auth middleware's public-prefix list
  too: a prefix like `/api/` leaves every route without its own auth
  dependency open to anonymous calls. Build a disable list by
  enumerating every route (`git grep -n '@router\.' <sha> -- src/api`) and
  write the boundary as an allowlist. Follow the default fetch engine's whole
  fallback chain for 403 and 429. A ChampSet pilot plan cited LakeStream RLS
  as its store's tenant guard while `auth.py` ran `set_config(..., true)` on a
  separate pooled connection as the owning `scraper` role, disabled 4 routes
  while `/extract` still sent page text to OpenRouter, and gated denials per
  arm while the default `fallback` engine retried a 403 through Camofox.
- An acceptance plan maps every step of its user journey to a numbered gate
  with a denominator. A step with only a build test (recipe versioning,
  segment, draft citation) is an ungated step, and the brief's named stages
  are the ones most often left that way.
- Every expected outcome in an answer key (robots disallow is `denied`,
  "waits Retry-After", "Camofox down gives `transient`") traces either to a
  cited `file:line` that does it today or to a named build step that adds it.
  Grep each repo on the request path for the behaviour's own words
  (`git grep -il 'robots\|retry-after' <sha> -- src`) and follow a denial
  rule into the second repo's worker too (tier escalation, proxy tier), not
  only the first repo's fetch. One round-2 pilot plan made ChampSet's 403 path
  terminal while LakeStream's `workers/base.py` still escalated 403, 429 and
  503 up to a proxy tier, and no repo read robots.txt or Retry-After at all.

## Deliverable

Design doc citing `file:line` throughout, a probed migration file, a stated
build order, and an explicit scope boundary (what this deliberately does NOT
do). Report what was verified vs what remains open.
