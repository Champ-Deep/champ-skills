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
