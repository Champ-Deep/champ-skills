---
name: release-integration-engineering
description: "Use when consolidating branches into a gated release."
---

# Release Integration Engineering

> **Security gate (mandatory):** every deploy runs `ultimate-security`'s deploy gate (pre-push hook, `predeploy`, or publish.sh) plus a `security-audit` guidance-mode review of the diff. A bare CLI deploy runs `python3 ~/champ-skills/security/ultimate-security/scripts/deploy_gate.py check .` first. `AUDIT-REQUIRED` means a full Cloudflare audit before shipping. Never override without Deep.

Build one testable release branch from multiple feature branches without hiding merge risk or weakening verification. Treat the release plan as an executable contract: preserve its order, stop on unexpected conflicts or missing prerequisites, and collect evidence while the work is performed.

## 1. Inventory before changing history

1. Read the release plan and every named input file. If any required file is absent, stop and name it exactly.
2. Confirm repository access using the required transport. For SSH-only work, verify SSH directly instead of treating API authentication as equivalent.
3. Fetch and prune, then record the exact remote heads:

```bash
git fetch --all --prune
git rev-parse origin/main origin/<feature-a> origin/<feature-b>
git status --short --branch
```

4. Read the CI workflows and rebuild their exact gates locally. Before any merge, extract the commands and pinned versions from `.github/workflows/*.yml` so the local run mirrors the runner instead of guessing at "run the tests":

```bash
ls .github/workflows
grep -nE '^  [a-z-]+:$|node-version|python-version|\s+run:' .github/workflows/<ci>.yml
```

Ignore release/publish workflows that fire only on tags; the test workflow is the gate. If the repo pins Node 22 while this machine defaults on Node 24, switch with the version manager before installing, or the lockfile resolves differently than it will on the runner. If the base has no `.github/workflows` directory at all, say so explicitly and derive the gates from the package scripts and repository docs; never write that CI passed when no workflow ran.

5. Compare the observed heads with the plan. If the base moved, repeat the planned dry-run merge checks before touching the release branch.
6. Confirm deployment access and required secret names without printing values. Authentication alone is not proof that the account can create the required environment, so verify project and environment access too. Also establish which checkout and commit the deployment actually runs from: when that checkout holds uncommitted changes, commit the exact running state as its own checkpoint before merging anything into it. Work that exists only in a working tree cannot be reverted to, bisected, or reproduced after the next push, and the first conflict resolution destroys the only copy of what production is running.
7. **Bootstrap control-plane credentials one at a time, in the order they are needed.** Several CLIs are involved across repos (git host, deploy platform, DNS, preview host) and each needs its own login. When a CLI refuses to log in because stdin is not a TTY, do not conclude it cannot be driven: switch to its browserless/pairing mode, which prints a URL plus a short pairing code, open that URL directly with `open "<url>"`, and have the user approve the code shown on the page. Pairing sessions expire within minutes, so deliver the link immediately instead of batching logins. For a scheduled sweep that must keep access without a browser, the durable form is an API token the user places in the environment; ask for that specifically rather than re-pairing every cycle.

## 2. Merge in the specified order

Create the integration branch directly from the remote base and use explicit merge commits whose subjects name the numbered release step.

```bash
git checkout -b release/<name> origin/main
git merge --no-ff -m 'Step N: merge <branch> into release/<name>' origin/<branch>
```

After each clean merge, capture the merge commit, parents, file summary, and clean status before proceeding.

Once the last input branch is merged, prove none was skipped; a clean history is not evidence that the set is complete:

```bash
for b in <input-branches>; do git merge-base --is-ancestor origin/$b HEAD || echo "MISSING $b"; done
```

This same containment proof is the gate for any later claim that a branch's commits are carried, including closing its PR and deleting the branch.

**Cut the release from current remote main even when the inputs forked an older base.** Merge the finished inputs forward onto today's base, never the reverse. Regenerated-from-source outputs (content JSON, feeds, prerendered pages) are newest-wins data, not merge text: an older branch's regeneration can silently roll production content back while every merge looks clean. After each regeneration, assert the newest production record survived with an exact count or identifier check, not by eyeballing the diff.

## 3. Prove the conflict set before resolving it

When the plan predicts conflicts, run the merge and inspect the unmerged set before editing anything:

```bash
git diff --name-only --diff-filter=U
git grep -n '^<<<<<<< ' -- <expected-files>
```

Compare the observed set exactly with the plan. Stop and report before resolving if any file is missing from or added to the expected set. An unexpected conflict can indicate a moved base or changed branch and invalidates the recorded resolution instructions.

Resolve each region according to the plan, usually by composing both sides rather than selecting ours or theirs wholesale. Then verify before staging:

```bash
git grep -n -E '^(<<<<<<<|=======|>>>>>>>)' -- ':!<lockfile>' || true
git diff --check
```

Stage only the resolved files, confirm `git diff --name-only --diff-filter=U` is empty, commit the merge, and verify both parent SHAs with `git show -s --format='%H%n%P%n%s' HEAD`.

## 4. Establish a green merged baseline before feature work

Install each workspace with the package manager and frozen lockfile it already owns. Run code generation, build, typecheck, and lint for every runtime named by the plan. Fix merge-induced errors before adding new behavior, then commit the baseline as its own numbered step.

When several input branches each touched `package.json`, a composed conflict there can leave the lockfile stale, and the frozen install then fails for a reason no side caused. Regenerate the lockfile with the pinned package manager and commit it as part of the baseline; never hand-merge lockfile hunks, and never relax the frozen flag to get past the drift.

Use deployment-injected variables for builds that need public runtime configuration rather than creating a local secret file. Keep command output from printing secret values.

Treat self-hosted schema and code generation commands as potentially deployment-aware. Point Convex codegen at a local or disposable preview deployment, not production, because the CLI can upload function bundles while generating bindings.

A green baseline means every required command exits zero. Warnings are not failures unless the plan or CI promotes them, but record them when they indicate future cleanup. Honor `continue-on-error` steps as non-gates but record their counts, and before attributing a linter's errors to the release, confirm the erroring files are byte-identical to the base: pre-existing debt is reported as pre-existing, not as a regression you introduced.

**A failing test on a byte-identical base is a candidate stale test, not automatically pre-existing debt.** Check whether the assertion encodes behavior the product has since retired (a removed route, a renamed field, a legacy classification). When it does, rewrite the test to the current contract, assert the retirement path itself (the redirect, the alias, the replacement), and prove the new assertion fails when that contract breaks. Never bend product logic to satisfy an expectation the product deliberately dropped, and keep the file's other assertions intact: a stale test is reconciled by making it test the truth, not by deleting it.

A test that passes alone but times out only in the full suite is contention against the global test timeout, not a logic failure. Diagnose it by rerunning that test alone with a raised timeout to learn its true cost, then give the test an explicit per-test timeout and keep the global timeout where it was. Excluding the test, lowering the suite, or reporting the subset as green hides a flake that lands on the CI runner.

## 5. Implement each release phase as a verified vertical slice

For every numbered phase:

1. Write the smallest test that expresses the phase gate.
2. Run it and verify the expected failure.
3. Implement only that phase.
4. Run the focused test, then the full suite, typecheck, lint, and relevant build.
5. Inspect the diff for unrelated edits, secrets, generated noise, and forbidden text.
6. Commit with a subject that names the numbered phase.

Do not combine later phases to save commits. Ordered commits make rollback, review, and evidence mapping possible.

## 6. Deploy to a disposable preview

Create or clone a preview environment only after the branch is locally green. Set every required variable explicitly, even when cloning another environment, and verify required secrets by name only.

Deploy stateful services first, then internal dependencies, backend, and frontend. Seed any legacy compatibility records before schema deployment when the release gate is specifically proving backward compatibility. Never run a cleanup migration that the plan reserves for after merge.

Read back exact service state after each external write. A successful CLI exit is not enough. Verify deployments, domains, variable names, health endpoints, and logs from the target environment.

Give the preview a new name with no production routes, domains, or data bindings, then prove it serves *this* release rather than a stale build: fetch an emitted asset (favicon, bundle) from the preview URL and compare its hash or a known content marker against the release checkout. A 200 from the preview domain only proves a server answered.

Preview origin is not production origin for integrations: third-party services that allowlist origins (chat/assistant backends, webhook receivers) will reject the preview URL through CORS or auth. Treat those rejections as a named boundary to retest on the production origin after publication, not as a release defect and not as a pass. Record them explicitly in the handoff so the publisher reruns that exact check live.

## 7. Run acceptance tests and collect evidence as artifacts

Run browser smoke tests against the preview, save traces and screenshots, and exercise both ordinary and guardrail paths. Query the preview data store for the exact records and histograms required by the plan. Export and inspect generated files rather than assuming their sheets or metadata exist.

Build an evidence ledger mapping every gate to a concrete artifact:

| Gate | Evidence |
|---|---|
| Merge behavior | merge SHA, parents, observed conflict set |
| Local quality | command and zero exit status |
| CI | workflow run URL and conclusion |
| Runtime routing | timestamped preview log excerpt |
| Data writes | bounded query output from preview |
| UI behavior | screenshot and Playwright trace |
| Export behavior | generated file inspected for required structure |
| Secret and vulnerability checks | scanner run URLs |

Do not mark a gate passed because a neighboring gate passed.

## 8. Recover a handoff that died mid-gate

**A lane whose status says running is not evidence of progress.** Judge liveness by three signals together: the transcript's last timestamp, an actual on-disk diff in its workspace, and `git log` in its branch. A stalled worker usually leaves an uncommitted diff worth keeping, so re-dispatch it to resume from that diff with instructions to commit a WIP checkpoint after every step, rather than restarting the lane from scratch.

When a delegated worker is interrupted (runtime cap, turn budget) its local clone still holds the partial result, and that clone is the only copy if it never pushed. Recover from it before re-dispatching anything:

```bash
cd <its-clone> && git status --short --branch   # branch, ahead-count, stray files
git log --oneline -15
git diff --name-only --diff-filter=U            # unmerged set: empty or not?
git grep -n -E '^(<<<<<<<|=======|>>>>>>>)' -- ':!package-lock.json'
git ls-remote --heads origin <branch>           # did it push at all?
tail -30 <its-transcript-log>                   # which gate was it in?
```

If the merges are complete, markers are absent and the remote has nothing, the handoff failed on the gates, not the merge: take the gates over yourself in a background process that logs each exit code separately (`npm ci`, typecheck, tests, lint, build, backend suite), then push on green. Do not replay the merge steps and do not re-dispatch a worker into a tree that is already merged.

## 9. Open one PR and leave it unmerged

Push the integration branch only after all gates are evidenced. Create one PR to the specified base, preserve the requested title and merge policy, request review, and do not merge or delete branches unless explicitly instructed.

If the integration branch has no CI run of its own, a push to it proves nothing: some workflows only trigger on pull requests or on the default branch. Open the PR as a **draft** to get the provider's own per-job conclusions without inviting a merge, then read them back:

```bash
git push -u origin <branch>
gh pr create --draft --base <base> --head <branch> --title <title> --body-file <path>
sleep 60   # image builds and frontend jobs take minutes, not seconds
gh pr checks <pr-number>
```

**Write the PR body to a file and pass `--body-file`.** Shell heredocs inside a `$(...)` command substitution break on `$`, backticks and parentheses in the body, and the failure surfaces as `bad substitution` with the whole PR uncreated.

State in the body what is deliberately unmerged, and name the workable seams for the reviewer: the follow-up commits not in any input branch, the conflicts resolved and how, the ops prerequisites that block merge (missing secrets, absent required status check, an environment that does not exist yet), and the exact command output each gate produced.

The PR body should map the release history, removals, schema and environment additions, test suite, preview URL, and every acceptance gate to evidence. Finish by reading back the PR state and checks with `gh pr view` and `gh pr checks`.

Two more things the reviewer needs in that body:

- **The environment surface, names only.** List every variable the release adds relative to the base so deployment can be planned before merge: `git diff origin/main HEAD -- <source-dirs> | grep -oE "os\.(environ\.get|getenv)\(['\"][A-Z_]+|import\.meta\.env\.[A-Z_]+"`. Never print values.
- **The superseded set.** A table of each PR/branch this release replaces, with its conflict summary and the close-with-reason text you intend to use, so closing them is a reviewable act rather than a cleanup you perform unasked.

A check that can never conclude is not a gate: a job wired to a deploy platform, secret, or environment this repo has never configured will sit pending forever and makes "all checks green" unreachable. Resolve it explicitly before merge (remove the job, make it non-blocking, or create the missing platform resource) and state which you chose; never report the check set as satisfiable while one job cannot run.

A consolidation branch carries commits from several identities: the user, agents, upstream authors. Check who is on it with `git log origin/main..HEAD --format='%ae' | sort | uniq -c`. If the repo was forked from an upstream that ships its own workflows (a CLA assistant, an old release pipeline), those will fail or fire on identities upstream never saw: read the failed run's log, determine whether the check is actually required before treating it as a blocker, and surface a keep/delete decision for that workflow file to the user. Do not edit an inherited workflow unasked, and do not silently accept red as "known".

## 10. Act only on an explicit go

Report first: the branch and PR, a per-input merits call (land vs close-with-reason), the exact merge command you would run, and every open decision. Then wait for the go.

**A scope change mid-run is a new go; make it durable.** When the user widens the authorization while work is in flight (for example preview-only becomes publish-to-production), record it where it survives the session: comment the new scope on the running work item and open the downstream task gated on it, stating both what is now authorized and what still is not (spending, migrations, policy changes). Do not carry the narrower earlier instruction forward just because it was the original brief.

**A release is not published until the scheduled publisher cannot undo it.** Before marking a site release complete, locate the cron/nightly publishing path that will next overwrite production (often a different checkout from the release branch) and reconcile it onto the release tree. Preserve any newer content or uncommitted work in that source before syncing; overwriting it trades a rollback bug for lost work. If the source can't be reconciled cleanly, report the unresolved conflict instead of choosing a side.

On the go, in order: merge the release PR; close each superseded PR with a reason that names the new PR and the containment proof (`Superseded by #<new>, commits contained, verified with git merge-base --is-ancestor`); close conflicting bot PRs such as dependency bumps with a note that the bot re-opens them against the new base. Delete a superseded branch only after the containment command succeeds for it. Containment, not a clean merge, is the deletion gate. If the base branch has no required-check protection, adding it is its own explicit step so the next push cannot land ungated.

## Stop conditions

Stop instead of improvising when:

- a required file or credential is missing;
- a remote head differs and the prescribed dry run has not been repeated;
- the conflict set differs from the plan;
- a required secret name is absent from the preview;
- a destructive migration or branch deletion is outside the current phase;
- evidence cannot be produced from the real system;
- a delegated worker's interrupted clone shows unmerged files or conflict markers, which means the merge set is incomplete and the plan, not the gates, must be re-run.

Never replace a blocked gate with fabricated logs, URLs, screenshots, data, or test results.
