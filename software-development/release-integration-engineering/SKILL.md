---
name: release-integration-engineering
description: "Use when consolidating branches into a gated release."
---

# Release Integration Engineering

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

4. Compare the observed heads with the plan. If the base moved, repeat the planned dry-run merge checks before touching the release branch.
5. Confirm deployment access and required secret names without printing values. Authentication alone is not proof that the account can create the required environment, so verify project and environment access too.

## 2. Merge in the specified order

Create the integration branch directly from the remote base and use explicit merge commits whose subjects name the numbered release step.

```bash
git checkout -b release/<name> origin/main
git merge --no-ff -m 'Step N: merge <branch> into release/<name>' origin/<branch>
```

After each clean merge, capture the merge commit, parents, file summary, and clean status before proceeding.

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

Use deployment-injected variables for builds that need public runtime configuration rather than creating a local secret file. Keep command output from printing secret values.

Treat self-hosted schema and code generation commands as potentially deployment-aware. Point Convex codegen at a local or disposable preview deployment, not production, because the CLI can upload function bundles while generating bindings.

A green baseline means every required command exits zero. Warnings are not failures unless the plan or CI promotes them, but record them when they indicate future cleanup.

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

## 8. Open one PR and leave it unmerged

Push the integration branch only after all gates are evidenced. Create one PR to the specified base, preserve the requested title and merge policy, request review, and do not merge or delete branches unless explicitly instructed.

The PR body should map the release history, removals, schema and environment additions, test suite, preview URL, and every acceptance gate to evidence. Finish by reading back the PR state and checks with `gh pr view` and `gh pr checks`.

## Stop conditions

Stop instead of improvising when:

- a required file or credential is missing;
- a remote head differs and the prescribed dry run has not been repeated;
- the conflict set differs from the plan;
- a required secret name is absent from the preview;
- a destructive migration or branch deletion is outside the current phase;
- evidence cannot be produced from the real system.

Never replace a blocked gate with fabricated logs, URLs, screenshots, data, or test results.
