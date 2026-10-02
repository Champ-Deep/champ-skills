---
name: ci-green-verification
description: "Use when proving a branch is green on CI runners."
tags: [ci, github-actions, verification, delegation, subagents, npm, pytest, environment-divergence]
---

# CI Green Verification

Make "the branch is green" a statement you can point at, rather than one you
inferred from a local run, a test count, or somebody else's summary.

## Core rule: green is a claim until the provider says so

The only acceptable evidence is the provider's own per-job conclusion for the
pushed branch. Everything else — a local `npm ci` that worked, a subagent
reporting 563 tests passing, a lockfile that installs on your laptop — is a
hypothesis about the runner.

```
LOCAL ENVIRONMENT                          RUNNER
node_modules present                       npm ci from the lockfile
caches warm                                empty module cache
a database on :5432                        nothing unless a service declares it
shell expands globs                        same shell, different quoting rules
your Node 24 / npm 11                      the workflow's pinned Node 20 / npm 10
```

Any of those six rows can turn a local pass into a red X. Read the runner log
instead of theorising about it.

## 1. Push, then read the provider

```bash
git push -u origin <branch>
gh run list --branch <branch> --limit 3
gh run view <run-id> --json jobs --jq '.jobs[] | "\(.conclusion // .status)\t\(.name)"'
gh run view <run-id> --log-failed        # only while red
```

Two results that both mean "not verified", and are not the same thing:

- **No run at all.** The workflow's trigger does not cover this branch. An
  absent run is not a pass; check the `on:` block and add the branch.
- **A run that exists and is red.** Triage per job. One job red usually means
  one environmental cause, not one code bug.

Confirm from a **fresh clone of the pushed branch**, never the working tree: the
working tree carries `node_modules` and caches that hide a broken lockfile.

```bash
git clone --depth 1 --branch <branch> <url> /tmp/verify && cd /tmp/verify
```

## 2. Classify the divergence before fixing it

Read the first real error, not the last line of the log. The families and their
fixes are tabulated in `references/divergence-taxonomy.md`. The ones that recur
most:

- **Lockfile generated under a different npm major.** npm 10 and npm 11 resolve
  optional platform-specific dependencies differently, so a lockfile written on
  one fails `npm ci` on the other with `EUSAGE` and a list of "Missing:" entries.
  Regenerate on the runner's platform and Node version, in a container if the
  runner is Linux, then prove `npm ci` on every Node version you support.
- **The suite's own conftest overwrites the CI environment.** `os.environ["X"] = ...`
  at import time silently discards whatever the workflow passed. Use
  `setdefault` so the environment wins.
- **Two dependency manifests, one installed.** Tests import a package declared
  in `requirements.txt` while CI installs `-e ".[dev]"` from `pyproject.toml`.
  Install both, or declare it in both.
- **A test asserting a real dependency the dev machine happened to have.** A
  health route that runs `SELECT 1` returns 503 without Postgres, so the test
  passes at home and fails on the runner. Give the job a real service.

## 3. Prove a fix in both directions

A fix that makes the suite green has not been shown to work; it has been shown
to stop a failure. Prove it both ways, with the environment variable that
selects the behaviour:

```bash
# must FAIL
DATABASE_URL=...@localhost:59999/... python -m pytest tests/api/test_endpoints.py -q
# must PASS
DATABASE_URL=...@localhost:<real-db>/... python -m pytest tests/api/test_endpoints.py -q
```

Then re-read the provider. Local green after a fix is not the end of the loop.

## 4. Verifying work you delegated

When you fan out subagents to build or rescue repos, their green claims are
starting hypotheses, not results. Each one verifies in its own working tree with
its own caches, lockfile and services. After the batch returns:

1. For every branch a subagent claims is done, read the provider's conclusion.
2. A subagent that ran out of iterations before pushing has produced nothing
   durable. Push from its local clone yourself, after verifying it.
3. Where a subagent self-reported a test count, reproduce it independently
   before repeating the number to the user.
4. Report the divergence you found between the claim and the runner. A subagent
   saying "all green" while the runner is red is the finding, not an annoyance.

Never summarise a delegated branch as green before this step.

## 5. Rank health by conclusion, never by workflow count

Counting workflows rewards a repo with four broken ones. Four `.github/workflows`
files and a red run means red. Check the last run before calling anything the
healthiest in a set, and correct any ranking you already published.

## Pitfalls

- **Do not fix a red install by deleting a dependency.** The obvious remedy for
  a legacy package that will not build is to drop it from the manifest. Check
  first whether the deploy artifact genuinely uses that feature; the production
  Dockerfile may install it separately, and removing it from the shared manifest
  silently deletes the feature from production while CI goes green. Prefer
  replicating the fix the Dockerfile already uses.
- **A lockfile that installs locally proves nothing.** Verify it on every Node
  and npm version the workflows pin, and on the runner's OS.
- **A husky or lint-staged hook can rewrite a file mid-commit.** After any
  commit that triggers one, re-check the committed blob's hash and re-run the
  gate; a formatter can reintroduce the exact state you just fixed.
- **A no-op test is worse than a red one.** A test whose result depends on the
  developer's laptop is not a gate. Prove it fails when the dependency is absent.
- **Never route around a blocked write.** If a tool refuses to write a file,
  report it as not written. Do not substitute a different path or claim success.
- **Stale workflow comments become lies.** When you change what a job installs,
  fix the comment describing it, or the next reader trusts the wrong contract.

## Verification

- Every branch reported as green has a provider run id and per-job conclusions.
- Every fix is demonstrated failing before and passing after.
- Every lockfile change is proven across all Node versions the workflows pin.
- No branch is described as green on the strength of a subagent report, a local
  run, or a test count alone.

## Supporting files

- `references/divergence-taxonomy.md` - local-green/CI-red failure families with
  the diagnosis command and the fix for each.
