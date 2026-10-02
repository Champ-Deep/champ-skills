---
name: guarantee-audit
description: "Use when auditing healthy-looking code before a merge."
tags: [audit, code-review, verification, concurrency, test-quality, merge-gate, security, delegation]
---

# Guarantee Audit

Audit code that already passes its own checks. The question is not "does it
build" but "which of the things it promises are actually enforced, and which
are only asserted in a comment".

Typical triggers: a contractor or AI-authored branch reported as done, a feature
branch you are asked to merge, "audit this and merge it if it works well",
a suite that passes suspiciously cleanly, or any merge decision where the
author is not the person who will run it in production.

## The core rule

**A green suite is evidence about the happy path and nothing else.** The
failure this skill exists to prevent: a branch ships hundreds of passing tests
while the one property the product sells, a cap that cannot be raced past, is
violated several-fold on the first concurrent load. Nothing is red, nothing
warns, and the merge looked uneventful.

The happy path being covered is not a finding. The interesting surface is
where the code makes a promise in prose and the tests never try to break it.

## Procedure

### 1. Establish the baseline yourself

Never take the suite's word from the branch author, a tracker, or an agent.
Run it, in order, in a clean checkout of the pushed commit:

```bash
# backend
uv venv --python 3.11 .venv-audit && uv pip install --python .venv-audit/bin/python -r requirements.txt
.venv-audit/bin/python -m pytest -q --tb=short 2>&1 | tee /tmp/pytest.log
# frontend
npm ci && npx tsc --noEmit && npm run build && npm run lint
```

A lint script that exits non-zero on warnings is part of the baseline, not a
detail. Record the pass/fail of each gate before analysing anything, so later
findings have something to be measured against.

### 2. Harvest the claims the code makes about itself

Docstrings are a to-do list of probes, because they are written as intent and
read as fact. Grep for the vocabulary of guarantees and read each hit's
implementation:

```bash
grep -rn -iE "atomically|race|never exceed|always |guarantee|fails closed|exactly one|idempot" --include=*.py --include=*.ts src/
```

A comment claiming a property is the highest-yield finding in an unfamiliar
repo, and checking it costs one script.

### 3. Probe each claim by executing it

For each claim, write the smallest thing that would prove it false, and run it.
The probe must exercise the real dependency, not a double (step 4).

| The claim | The probe |
|---|---|
| "atomically consume" | N concurrent workers against a cap of 1, injected clock |
| "never exceeds the daily cap" | 10 simulated days, assert the running sum |
| "fails closed" when a secret is unset | boot it with the variable absent |
| "always within active hours" | tick the scheduler at the last hour of the window |
| "one process per account" | count the processes, not the config |
| "fully encapsulated" | grep for the secret on every outbound path |

```bash
# a real dependency, not the test double
docker run -d --name probe-redis -p 6399:6379 redis:7-alpine
# ... run the probe against 127.0.0.1:6399 ...
docker rm -f probe-redis
```

### 4. Check whether the test double can express the failure

This is the step that explains a green suite hiding a real bug. A fake removes
the very condition the code must survive:

- `fakeredis`, `memsim`, an in-memory dict, any `Fake`-prefixed store executes
  commands one at a time, so the interleaving that breaks the code cannot
  occur under test.
- A mocked subprocess or transport that returns the value under test proves
  the caller handles that value. It proves nothing about producing it, so a
  selector, payload shape or spawn path can be entirely unvalidated while
  coverage reads 90 percent, because coverage counts the module body rather
  than the branch taken.
- A `set()`- or dict-backed fake has no ordering under concurrency by
  construction.

When the double removes the condition, no test in the suite can catch that
class. Re-run the probe against the real service before reporting anything.

### 5. Verify delegated findings yourself

Fan out for breadth only after step 1, then re-execute every candidate you
intend to report. A subagent reporting `file:line` is a pointer to a place to
look, not a result.

Budget for roughly one finding in three not reproducing, and expect false
negatives too: an audit that credited a healthcheck as correct while the
compose file's version discarded its return value and always exited 0. The
parent keeps the claim or drops it based on its own run, never the child's.

### 6. Audit the merge path, not just the code

The deploy config is where a suite cannot help you at all. Execute each one:

```bash
docker compose build <service>          # a nonexistent build target fails here
docker run --rm -d --name run -p 8477:8000 <image>
curl -s -w '\nHTTP=%{http_code}\n' http://localhost:8477/healthz
docker inspect <image> --format 'ENTRYPOINT={{.Config.Entrypoint}}'
```

Check every one of these, because each has taken down a real deploy:

- **Build targets that do not exist.** A compose file requesting a stage the
  Dockerfile never declares, so the documented first command fails.
- **Published port versus bound port.** `8080:8080` published while the
  process binds `8000` leaves the app unreachable and everything else green.
- **A healthcheck that cannot fail.** `python -c "...; check()"` discards the
  return value and exits 0 whatever happened. Run the exact command with the
  dependency absent to prove it goes red.
- **`depends_on: condition: service_healthy` on a service with no
  `healthcheck:` block**, which deadlocks startup forever.
- **`command:` overrides on an image with no `ENTRYPOINT`**, replacing the CMD
  with bare argv that nothing executes.
- **A `.env.example` describing a stack the code does not use**, while omitting
  every variable the auth path actually reads.

### 7. Check the kill switches

Search for env vars that disable a safety property, then check each for a
guard and for test coverage:

```bash
grep -rn "verify_signature\|UNSAFE\|SKIP\|DISABLE\|_BYPASS" --include=*.py --include=*.ts src/
```

A dev-mode flag with no environment guard and no test is a total bypass. Prove
it against the built image rather than reasoning about it: forge a token, get a
role, and show the response. Unauthenticated websockets, tenant streams with no
ownership check, and a `None`-defaulted dependency that skips its own guard when
unset are the same bug wearing different clothes.

### 8. Branch verdicts by containment

```bash
for b in main other-branch; do
  git merge-base --is-ancestor origin/$b origin/<candidate> \
    && echo "$b: CONTAINED" \
    || echo "$b: $(git rev-list --count origin/<candidate>..origin/$b) unique"
done
git rev-list --max-parents=0 origin/<branch>    # differing roots = different projects
```

A branch with unique commits needs a verdict on each one. "Superseded" needs
its reason stated: solved differently on the candidate branch, or a file that
exists only on the abandoned branch and is still worth reading.

## Reporting

Lead with the verdict and the number of blockers, then the gates that passed,
so the reader knows the shape of the answer before the detail. Every finding
carries its reproduction, not adjectives.

State the omissions as findings in their own right: what you could not verify,
what you did not fix, and whether you merged or deleted anything. Silence
reads as oversight. A cleanup you deliberately did not do, with its size and
the reason, is a decision the reader can argue with.

Pair the written report with a single-file HTML version when the reader is not
the author. Run the visual verification gate and open the screenshots.

## Pitfalls

- **A green suite is not a verified guarantee.** It asserts the happy path ran.
  Probe the boundary the guarantee rests on.
- **A docstring claiming a property is a lead, not a proof.** "Atomically" over
  a two-round-trip implementation is the most productive thing to grep for in
  an unfamiliar codebase.
- **A fake that serialises cannot test a race.** Prove concurrency against the
  real service, and say in the report which double the suite uses.
- **A subagent's finding is a pointer, not a result.** Re-run it. One in three
  does not reproduce, and a child's silence is not an all-clear.
- **A healthcheck that discards its return value always passes.** Assert on the
  exit code and prove it red with the dependency absent.
- **A guard in the route is not a guard in the service.** Any non-HTTP caller
  bypasses it. Check where the refusal actually lives.
- **Local green is not the deployed system.** A container that boots healthy
  and a documented `docker compose up` that fails on its first command are
  both ordinary, and only running each one finds them.
- **Do not merge as part of an audit.** Report the verdict, leave the base
  branch untouched, and let the reviewer decide.

## Verification

- The suite, typecheck, build and lint were run by me, and each result recorded.
- Every safety claim in prose has been probed by execution, and each claim that
  did not survive appears as a finding with its reproduction.
- Every reported finding was reproduced against the real dependency or the
  built image, not inferred from a reading or a delegated report.
- Every branch has a containment verdict backed by command output.
- The base branch is untouched, and what was not done is stated.

## Supporting files

- `references/guarantee-probes.md` - copy-pasteable probes for the common
  guarantee classes, and the test doubles that hide each one.