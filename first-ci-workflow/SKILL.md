---
name: first-ci-workflow
description: Use when a repo has tests but no CI, or a green suite.
version: 0.1.0
license: MIT
metadata:
  hermes:
    tags: [ci, github-actions, verification, testing, automation]
---

# Writing a repo's first CI workflow

Triggers: a repo with a complete, passing, non-trivial suite that only runs when
a human remembers; "add CI"; a build contract nobody enforces; a release gate
that lives in a README.

For reviving an already-CI'd repo that has gone red, or for proving a pushed
branch green, use the CI verification skill instead. This one is the first-time
case: no workflow exists, so every choice is being made for the first time and
the YAML is the deliverable.

## Why this is high value

A suite that only a human runs is a suite that will rot, and it rots silently:
nothing is red, so nothing gets fixed, and the next person to trust the count is
trusting a memory. Adding the workflow converts every future refactor from
"someone should run this" into a gate, which is why it is usually the
highest value-per-hour work in a stalled portfolio. It is pure engineering with
no credentials and no product decisions.

## Procedure

### 1. Read the project's own contract, do not invent a gate list

A well-built repo states its verification commands in a build contract, a
Makefile, or a docs section. That file is the specification; the workflow
implements it.

```bash
search_files(pattern='^#+ .*[Vv]erification', path='<repo>')
read_file(path='<repo>/BUILD.md')            # a numbered contract section, usually near the end
read_file(path='<repo>/Makefile')           # reusable targets: test, lint, build
read_file(path='<repo>/pyproject.toml')     # requires-python, ruff target-version, dev extras
read_file(path='<repo>/package.json')       # scripts: build, typecheck, test, e2e, contrast
```

Run every one of those commands locally, in workflow order, before writing any
YAML. A workflow nobody ran locally is a guess.

### 2. Pin the versions the contract assumes

Use `requires-python`, the ruff `target-version`, and the Node version the
lockfile was generated under. Never `latest` or a bare `node-version: 22.x`:
a silent runner upgrade changes results with no diff to show for it, and the
next failure is unexplainable.

### 3. Split one job per concern

So a red X names its cause without opening a log. A typical set: backend tests
and lint, frontend typecheck plus build, browser e2e, and any repo-specific
character lint.

Give each job only the dependencies it declares. A suite whose config starts
its own dev server and runs in mock mode needs no API process, no database, and
no `services:` block, which also means it cannot pass merely because something
else happened to already be listening on the port.

### 4. Install from the lockfile, and prove it in the runner's image

Use `npm ci`, never `npm install`. `npm ci` installs strictly from the lockfile
so a lockfile that only resolves on one platform fails loudly; `npm install`
quietly repairs it, which means CI passes on a lockfile the runner cannot
reproduce.

```bash
docker run --rm -v "$PWD":/w -w /w node:22-slim sh -c "node -v; npm -v; npm ci"
```

One command turns a future red X into a local red line. Read the lockfile first
for the packages that break this way: many `node_modules/<pkg>/<platform>`
entries means platform-specific optional deps, and esbuild plus rollup together
ship around seventy, so any lockfile with them was resolved against one OS.

### 5. Install test-runner binaries as their own named step

A browser-driven suite ships as a library plus a separately downloaded browser.
`npm ci` and `pip install -e .` deliver the library only, so a machine that ran
the download once keeps passing while a fresh runner dies at
`browserType.launch` with "Executable doesn't exist".

```yaml
- name: Install Chromium
  run: npx playwright install --with-deps chromium
```

Keep it separate and named. The symptom reads as a test failure and is actually
an environment failure, which is exactly why it deserves a visible step rather
than being folded into a general install where nobody notices it later.

### 6. Inline checks that would otherwise depend on make

If the contract lists a `make` target, inline the command so the runner needs no
build tool:

```bash
if git grep -InP '[\x{2014}\x{2013}]' -- . ; then
  echo "::error::character forbidden by the brand contract"; exit 1
fi
```

### 7. Exclude what the environment cannot support, and say so in a comment

If migrations need a live Postgres that does not exist yet, that gate does not
belong in the first workflow. Leave it out and put a comment in the YAML saying
what is missing and when it can be added. A comment there is the difference
between a deliberate omission and an oversight someone re-adds in a panic.

### 8. Write the trap into the comment

The comments get read more often than the YAML, and each should say what breaks
if the line changes, because the line looks arbitrary otherwise: why `npm ci`
and not `npm install`, why the version is pinned, why the browser download is a
separate step, why that job omits a service. Stale comments become lies, so
update them in the same commit as the line they describe.

### 9. Add concurrency cancellation

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

A red X on a commit nobody is working on any more is noise, and noise trains
people to ignore the badge.

### 10. Push a branch and let the provider decide

Never call this done on a local green run. Push, read per-job conclusions by
name, and read the log while it is red. A first workflow nearly always has at
least one job that only fails on the runner, and finding that is the exercise.

```bash
git push -u origin <branch>
gh run list --branch <branch> --limit 3
gh run view <run-id> --json jobs --jq '.jobs[] | "\(.conclusion // .status)\t\(.name)"'
gh run view <run-id> --log-failed        # only while red
```

Report the per-job conclusions and the run id, never a test count. Hand the
branch over without merging, per the standing rules in `stalled-repo-rescue`.

## Pitfalls

- **A first workflow with no failing run has never been tested.** Reintroduce
  one failure deliberately, confirm the job goes red and names the step, revert.
  A gate never seen failing is a gate that might not work.
- **Do not let a green first run hide a gate you never wired.** Diff the YAML's
  commands against the contract's list and confirm every command appears.
- **`on: push` with no branch filter plus `cancel-in-progress` will cancel a
  run on a force-push you wanted to keep.** Scope the group to the ref.
- **Do not fix a red install by deleting a dependency.** If the deploy artifact
  genuinely uses that feature, removing it from the shared manifest silently
  deletes it from production while CI goes green. Replicate the fix the
  Dockerfile already uses.
- **Do not add a service container the suite does not need.** It slows every
  run and creates a second thing that can fail.
- **A suite that passed locally and failed on the runner is a finding, not an
  inconvenience.** Read the log rather than theorising; the local shell and the
  runner shell resolve globs, paths and case differently.

## Verification

- Every command in the project's verification contract appears in the YAML.
- Versions are pinned to what the contract declares, not floating.
- A fresh clone of the pushed branch installs from the lockfile on the runner's
  image.
- The provider reports every job green by name, with a run id.
- At least one gate was observed failing and then fixed.
- Nothing was merged and no branch was deleted.
