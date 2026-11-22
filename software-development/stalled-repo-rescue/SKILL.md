---
name: stalled-repo-rescue
description: "Use when reviving a stalled repo into one verified branch."
tags: [github, git, ci, consolidation, refactor, monorepo, typecheck, dead-code, verification]
---

# Stalled Repo Rescue

Bring a repo that has stalled back to a state a human can review: one branch
containing everything worth keeping, a real test suite, green CI on the
provider's own runners, and a written account of what was decided and what was
deliberately left out.

Typical triggers: CI red for months, branches nobody merged, a large feature
sitting in a folder nothing builds, a Docker build failing on a frontend that
"works fine", or a request to consolidate and finish something half-built.

## Deep's standing rules for this class of work

These apply to every rescue. They are not per-repo choices.

- **Consolidate, do not merge main.** Build ONE fresh branch (`v2-<name>` or
  `rescue/<name>`) off the remote base that carries every remaining branch plus
  the open PRs. Never merge a feature branch into another feature branch.
- **Hand the branch over, do not merge it.** Push the V2 branch, open nothing
  destructive, merge nothing to main, and delete nothing, until Deep reviews it.
  Report before any merge. When CI only fires on pull requests or on the default
  branch, a push to the V2 branch collects no runs at all; open it as a **draft
  PR** instead. The PR event fires every job, draft status blocks an accidental
  merge, and `gh pr checks <n>` gives you the per-job evidence the report needs.
- **Give a per-branch merits verdict.** For every branch: fully contained, has
  unique work, or is not even the same project. Say which, with the command
  output that proves it. "Delete the stale ones" is not a plan; a containment
  proof is.
- **Report the omissions explicitly.** Anything you chose not to do (wiring a
  new package into the Dockerfile, replacing a legacy service) goes in the
  report under what you did not do, with the reason. Silence reads as oversight.
- **Do not delete a branch whose work you have not proven is contained.** Cheap
  to keep, expensive to lose.

## 1. Inventory before changing anything

```bash
git clone <repo> && cd <repo>
git branch -a
git log --oneline -12
gh run list --limit 5          # when was CI last red, and on what?
gh api repos/OWNER/REPO/actions/workflows --jq '.workflows[].name'
```

**Count local-only commits before anything else.** The approved work is often unpushed: `for b in $(git for-each-ref --format='%(refname:short)' refs/heads); do echo $b $(git rev-list --count $b --not --remotes=origin); done`, plus every worktree HEAD (`git worktree list`). Pushing V2 publishes those commits, so name it in the report and scan them (`gitleaks detect --log-opts=origin/main..HEAD`) first. A rebased copy of a stacked PR (`rebase/prN-on-<sha>`) is the carrier: merge it, then prove the PR head and the stacked PR head are ancestors of V2.

**Look for a rescue of this repo that has already run before you inventory it.** A done card holding a V2 branch and per-branch verdicts is the starting inventory: take its branch as the base and classify only what has moved since. Re-deriving containment for work that was already proven produces a second base and a second set of verdicts that disagree with the first.

Record the branch tips, dates, and which branch is the base. Then classify
every branch with a containment check, not a name:

```bash
git fetch origin --prune
for b in main feature-a feature-b; do
  if git merge-base --is-ancestor origin/$b origin/v2-consolidation 2>/dev/null; then
    echo "$b: CONTAINED"
  else
    echo "$b: $(git rev-list --count origin/v2-consolidation..origin/$b) unique commit(s)"
  fi
done
```

**Squash merges make containment lie both ways.** `merge-base --is-ancestor` says "unique" for every branch whose PR was squashed (157 branches, 3 ancestors). Prove a squashed PR with `git diff <squash>^ <squash> | git patch-id --stable` equal to `git diff <merge-base> <PR head> | git patch-id --stable`, then test each branch tip as an ancestor of that PR head (`gh pr list --state all --json headRefOid,mergeCommit`). For leaf commits cherry-picked into a squash, grep the squash message for `(cherry picked from commit <sha>)`, or test `git apply --check -R` of the commit against the squash tree. File byte identity is weaker evidence: label it and keep the branch.

**Carry stack tips, not every PR.** Merge only the head of each stack (`merge-base --is-ancestor` among open PR heads finds them); a bundle PR (a base that holds three others) shows up the same way. Run the merge loop once with `git merge --abort` on conflict to get the conflict map before resolving anything. Two PRs that redesign the same page (nav, Home, dashboard) are a product call: leave both PRs out of V2 with the conflicted file list instead of choosing.

**Sweep unpushed work outside the remotes.** `git rev-list --no-merges <every local branch> <every worktree HEAD> --not --remotes=origin <V2>` found 8 unpushed commits in the canonical checkout (three real fixes, a deflake, a whole separate tool). Cherry-pick the small ones with `-x`; report the separate tool instead of publishing it.

**Migrations that all took the next number.** Eight PRs wrote `0009_*.sql`. Take ours for `_journal.json` and the incoming snapshot during the merge, `git mv` the incoming SQL to the next number and append the journal entry (`when` greater than the last), then once at the end run `drizzle-kit generate` against a clean tree: every generated statement must already appear verbatim in the renumbered files, keep only its snapshot as the last number, delete its SQL, and confirm the next run says "No schema changes". Then `wrangler d1 migrations list <db> --remote` (read only) to state what prod has not applied. Tests that open a migration by its number break on renumbering; match by name.

**Mocks drift silently.** After merging an API change (`getModelSync` became async `getModel`, a key store was retired), the textually clean merge fails in tests that mock the old shape. Run the whole suite right after the last merge and fix mocks, never assertions.

**Check root commits before treating a branch as salvageable work.** Two
branches in one repo can have different root commits, meaning they are two
different projects that were started in one directory and never reconciled:

```bash
git rev-list --max-parents=0 origin/<branch>
git ls-tree -r --name-only origin/<branch> | head -30
```

A branch whose root differs and whose language or stack differs is a dead
prototype, not work to merge. Say so and let the user decide; do not port it.

## 2. Reproduce the failure locally before theorising

Red CI with expired logs is common, and guessing produces confident wrong
answers. Reproduce each CI step by hand in the order the workflow runs them.
Record the raw error count per step.

```bash
npm ci && npx tsc --noEmit 2>&1 | tee /tmp/tsc.txt
grep -cE 'error TS' /tmp/tsc.txt
grep -oE 'error TS[0-9]+' /tmp/tsc.txt | sort | uniq -c | sort -rn
```

The error-code histogram is the diagnosis. A single dominant code across many
files means one structural cause, not many small bugs. Fix the cause.

**A build that stalls on downloading rather than compiling is not a code
failure.** Read the provider's own progress counter in the log before theorising:
packages trickling in one or two a minute against an `ETIMEDOUT` on a fetch means
the network path inside the container is at fault, not a dependency. On a
container bridge (OrbStack, Docker Desktop on macOS) Node 19+ races the address
families with a 250 ms happy-eyeballs budget per connection, so an unreachable
IPv6 answer burns that budget on every attempt and installs crawl or die while
the same install on the host succeeds. Set the knob in the Dockerfile's build
stage, because the build does not inherit your shell:

```dockerfile
ENV NODE_OPTIONS=--network-family-autoselection-attempt-timeout=2000
```

A retry loop is the wrong fix: it re-rolls the same losing family, while the
longer timeout lets the IPv4 fallback land. Confirm with the download rate
moving from roughly one package per 80 s to hundreds in 30 s, then keep the fix
as a measured result rather than a theory. The same export on the host makes npm
and npx behave alike there too.

**Prefer package scripts over raw tool invocations** (`npm run build`, not
`npx vite build`) so you run what CI runs, and redirect to a log file so a
long output does not trip command guards.

## 3. Prove unreachability before calling code dead

This is the step that saves the work. Code the entrypoint never imports is
usually *misplaced*, not abandoned.

Run a reachability analysis from the real entrypoint, resolving relative
imports transitively and separating bare (third party) from relative imports:

```
scripts/reach.py <repo> <entrypoint>
```

It reports reachable files, the dead set, and any Node-only bare imports
reachable from browser code. See `references/reachability-probe.md`.

Before deleting anything in the dead set, ask: **does it import packages that
`package.json` never declares?** That is the signature of a real feature whose
dependencies were never added, not of abandoned work. Check for a design doc
(`plan.md`, `README`, ADR) describing it, and check the file's size and internal
coherence. Hundreds of lines with consistent naming, a barrel export, and a
matching spec file is a product. Deleting it is destroying someone's work.

**Isolate, do not delete.** A coherent Node or server-side package living inside
a browser `src/` tree is a packaging bug. Give it its own directory, its own
`package.json` with the dependencies it actually imports, and its own
`tsconfig.json`. Use `git mv` so history follows the files.

## 3b. A clean or hand-resolved merge is not a working merge

After every merge of an overlapping PR run the full typecheck and suite before the next one. Textually clean merges still break: a shared component changed meaning (a spinner that gained `role="status"`), a default tab moved, a status label was renamed, a security flag one lineage removed (an admin role permission) was relied on by the other's test. Fix the semantic seam, never the assertion's intent, and write the choice into the report. When two lineages answer the same security question, take the later audited one and adapt the older test with a comment saying why.

Auto-merge also drops tests silently. After the last merge compare every test title on every carried branch AND on the base branch with the V2 tree (`it(`/`test(` titles and `def test_`) and re-add or record each rename. A title the base has that V2 lacks is usually a carried PR removing it on purpose (a policy PR that replaced a warm-up ramp dropped 4 main titles while the report said "no other title is missing"): name the PR and commit, because it is a behaviour change, not a merge loss.

**List what changes on the base when V2 lands.** One merge of 50+ PRs replaces 50 separate decisions, so the report needs a short section of prod-visible behaviour each carried PR switches on, with its number: send caps and policies, auth and key systems (two inbound key schemes shipping side by side is a second copy of a feature, so it gets a verdict line), new unauthenticated routes (`git diff <base> V2 -- <proxy or route allowlist>`), retired integrations. Test results do not tell the approver any of this.

**The decision card must reach the desk and absorb the per-PR decisions.** Create it blocked at the live desk floor plus one (`sqlite3 ~/.hermes/kanban.db "select min(priority) from (select priority from tasks where status='blocked' order by priority desc limit 15)"`), not a fixed 95: one V2 decision at p95 was shelved 8 minutes after creation under a floor of 104. Then search open cards for per-PR merge, rebase or retarget decisions on any carried PR (`title or body like '%<repo>/pull/%'`), list them in the decision text as made moot by A, and comment a pointer on each. A carried PR merged singly from one of those cards (its migration lands under its original number) breaks V2's renumbering.

A PR is superseded when the same subject exists on the base (`git log --format=%s origin/main | grep -xF <subject>`) and the diff reverse-applies (`git diff c^ c | git apply --check -R` prints nothing on the base tree); a branch whose merge is textually clean against V2 may still need closing because it adds a second copy of a feature, so say that in the verdict.

Migrations: do not renumber by reflex. Run `wrangler d1 migrations list <db> --remote` (read-only) first; wrangler applies by name, so a database that already applied a name re-runs it under a new one. Report the unapplied list as that command prints it, never as the PRs' own migrations: a carried branch with its own deploy env that shares `migrations_dir` puts its migrations into the production database too, and a column it adds to a shared schema file makes the main app's full-row selects fail until that migration runs. Then "one revert removes it" and "inert unless MODE=true" are false; say so in the report.

Public repos: a PR that committed QA screenshots or VERIFICATION files gets them removed in their own commit, and the report says only a squash merge keeps them out of history.

**Re-list open PRs on every fix round.** A PR opened after intake (often a runbook or cutover card running in parallel) can conflict with V2's files or contradict a config V2 carries. Before each re-handoff run `gh pr list --state open`, `git merge-tree --write-tree --name-only <new-pr-head> HEAD` for each PR not in the verdict table, and grep its docs for the carried PRs' numbers. Put the conflicted files, the land order and any contradiction (one runbook said a carried `*/*` zone route must not ride along) in the report and the decision text.

## 4. Fix the structural cause, then the residue

After the split, re-run the typecheck. A strict tsconfig will surface a small
residue of real issues. Fix them by narrowing or modelling the true shape. Do
not reach for `any`, `!`, or `@ts-ignore` to quiet the compiler, and do not
loosen a strictness flag you just added to make errors disappear.

Two classes are worth checking explicitly, because they are the ones that make a
package fail to compile for reasons unrelated to its own code:

- **A transitive dependency version.** A library resolving to a version older
  than the code expects (a missing export, a removed API) is a pin problem, not
  a code problem. Check the installed version and the package's own exports
  before editing call sites.
- **Module-interop under `NodeNext`.** See `references/node-ci-gotchas.md` for
  the named-vs-default import rule and the others.

## 5. Boundary validation for anything untrusted

A TypeScript interface is erased at runtime and proves nothing about what
actually arrives. Express types `req.body` as `any`. Any value crossing a
trust boundary (HTTP body, webhook, queue message, config file, env) needs a
runtime schema (zod or equivalent) and a typed parse of the result.

**Acknowledge only after the payload is known good.** Responding 2xx before
parsing, then swallowing errors in a catch, is silent data loss: the sender
records success, never retries, and the payload is gone with no trace. Parse
and authenticate first, return 4xx on bad input so the sender can retry, and
only then acknowledge. A fast ack is still fine for genuinely cheap async work
after the payload has been accepted.

Write a regression test for this. It is the one bug in this class that a green
suite will not otherwise catch.

## 6. Verify: local green is not CI green

Run the full matrix locally, then push and read the provider's own result. A
build script can pass locally and fail on the runner for quoting, path, or
version reasons.

**Run the widest suite you have at least once, and name the command behind
every pass count.** A path-filtered run (`npx vitest run src/lib/x`) is a report
about those paths and nothing else, yet its total reads as a branch-wide green.
Run the whole suite once on your branch and once on the baseline, compare the
totals, and state which command produced each number, so a red test outside your
filter becomes a finding instead of something never observed.

```bash
# each package, from a clean clone of the PUSHED branch
npm ci && npx tsc --noEmit && npm run build
cd <subpackage> && npm ci && npm run typecheck && npm run build && npm test
docker build -t <name>:v2test .
docker run --rm -d --name <name>-run -p 4701:3001 <name>:v2test
curl -s -w '\nHTTP=%{http_code}\n' http://localhost:4701/health
```

Verify from a **fresh clone of the pushed branch**, not the working tree. The
working tree has `node_modules` and caches that hide a missing lockfile.

Then confirm on the provider and iterate until green:

```bash
gh run list --branch <branch> --limit 3
gh run view <run-id> --json jobs --jq '.jobs[] | "\(.conclusion // .status)\t\(.name)"'
gh run view <run-id> --log-failed          # only while it is red
```

A suite that passed locally and failed on the runner is a real finding. Read
the runner log rather than guessing; the local shell and the runner shell
resolve globs and paths differently.

For integration tests that need a service, declare it as a workflow service so
CI provisions it, and have the test read its URL from an env var with a local
default. Never let a test suite default to a production datastore: it writes
and deletes keys.

## 7. Governance floor

Cheap, and it is what makes the repo legible to the next agent:

- `AGENTS.md` recording the layout, the commands, the type discipline, and the
  sharp edges that cost you time. Write down the trap you just hit, in one
  paragraph, with the reason. That is the highest-value paragraph in the file.
- `LICENSE`, matching the convention already used on the user's other repos.
  Check one before choosing.
- `.env.example` covering every variable the code actually reads, including
  test-only ones, with secrets blank.
- `.gitignore` extended for every new package's `node_modules` and build dirs.
- CI split into one job per package plus the image build, each with a clear
  name, and a status gate that requires all of them.

## 8. Report

Write the report as a file in the repo, committed on the V2 branch, and deliver
it. It should carry: what was wrong and why, what was delivered, the executed
verification (commands and results, not adjectives), the per-branch merits
verdict table, what you did not do and why, and the suggested merge order.

State plainly what is unverified. A figure you could not confirm is labelled
unverified rather than reported.

## Pitfalls

- **Unreachable from the entrypoint does not mean dead.** It usually means
  misplaced. Check whether the dead set imports packages absent from
  `package.json` before deleting anything.
- **A local-green suite proves nothing about the runner.** Shell glob quoting
  alone made a suite pass locally and fail on CI. Always read the runner log.
- **A `2xx` sent before validation is data loss, not speed.** Parse and
  authenticate first.
- **Different root commits mean different projects.** One repo, two root
  commits, two stacks, and a shared name is a trap that a name-based triage will
  merge straight into production.
- **Containment is proven with `merge-base --is-ancestor`,** never inferred from
  branch names, dates, or the appearance of similar commits.
- **A build that "works" locally may never have run.** Reproduce the CI steps
  in order before forming a theory, and get the error-code histogram, not a
  sample of errors.
- **Do not add features during a rescue.** The deliverable is a reviewable
  branch. Scope creep makes the diff unreviewable, which defeats the point.
- **Reporting a stalled download as a dependency or code failure.** Read the
  provider's own progress counter first: a crawling package fetch is the
  container's network path, and killing the build repeats the same transfer from
  zero. Widen Node's family-autoselection timeout in the Dockerfile build stage
  (see `references/node-ci-gotchas.md`) instead of adding retries.

## Verification

- Every package typechecks and builds with zero errors, run from a clean clone
  of the pushed branch.
- The test suite passes locally and on the provider's runners, and the pass count
  came from the full suite with its command named, not from a path-filtered run.
- The image builds, and the container answers a health check and serves its
  entrypoint.
- CLI or binary entrypoints were actually invoked, not just built.
- CI is green on the provider, per job, by name.
- Every branch has a containment verdict backed by command output.
- Nothing was merged and nothing was deleted.

## Supporting files

- `references/reachability-probe.md` - the dead-code analysis method, the
  mixed-runtime detection, and how to read the results.
- `references/node-ci-gotchas.md` - Node/TS packaging traps that make a
  resurrected package fail to compile, the container-build network timeout that
  reads as a dependency failure, and local-versus-runner CI divergence.
- `scripts/reach.py` - reachability probe; run it before any deletion decision.
