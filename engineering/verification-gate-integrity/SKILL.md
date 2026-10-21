---
name: verification-gate-integrity
description: "Use before reporting any test, gate or audit as passing."
tags: [testing, verification, pytest, playwright, accessibility, gates]
---

# Verification gate integrity

Before you tell anyone a check passed, prove the check ran, and prove it would have
failed. Two different claims, two different pieces of evidence.

## The rule

**A gate that was never collected is indistinguishable from a gate that passed.** The
pass count is the only surface that looks healthy, and it is healthy in both cases.

## Collection is a separate claim from passing

A test file can satisfy every naming convention and contribute nothing: the directory
is on `testpaths`, the filename matches `test_*.py`, the module imports cleanly, and
it defines no test function because it was written as a `def main()` script behind
`if __name__ == "__main__"`. Collection succeeds, zero tests are gathered, and the
suite reports a clean pass count that deleting the file would not change.

Reading the file does not reveal this. The green run does not reveal it. Only the
collected count does.

- **Gate on the collected count**, not on the existence of a file. "The suite passed"
  and "my file ran" are different claims needing different evidence.
- **Convert the script, do not re-advertise it.** A probe written as a `__main__`
  script is a manual tool. If a claim depends on it running, it needs real test
  functions in the suite.
- **Skip loudly when the harness is absent.** A browser gate needs a live server. Make
  it an explicit skip with a stated reason so "no server running" is never read as
  "the layout passed".

The same rule covers configuration: a required status check that was never added
to branch protection is a gate nobody can pass, because the PR page reports every
job green while `gh pr checks` has nothing to show for it. Read the protection
rules, do not infer them from a green PR, and report an unprotected default branch
as a finding rather than as a pass.

## The exit code you read is the exit code you piped

A patch script that asserts before it writes writes nothing when the assert trips,
and `python edit.py | tail -1` exits with tail's status, so the shell reports
success while the file is unchanged. Run edit and check scripts unpiped (or read
`PIPESTATUS`), treat any traceback in the output as a failed step even when the
pipeline exited 0, and confirm the write the way any edit is confirmed: grep the
target file for the new value before reporting it applied.

## Prove the gate by breaking what it guards

Reintroduce the exact defect, confirm the test fails and names real numbers, revert,
confirm green. Run this on converted and inherited gates, not only the ones just
written. A gate never seen failing is a gate nobody knows is armed.

## Prove "pre-existing" on the baseline, not from memory

Before reporting a red test as unrelated to your change, run that exact command on
the unchanged baseline (a stash, a worktree of the base commit, or a clean checkout)
and capture the same failure there. A failure reproduced on the baseline is a
pre-existing defect you can name with evidence; a failure you merely recognize as old
is a guess wearing the costume of a finding, and it shields your own regression when
the two happen to share a symptom.

## Promotion is a sequence of claims, not one

Deploying is a chain (find the version, deploy it, promote it), and the tool's success
message is not proof the chain did what you intended. Assert each link: match the version
you uploaded by its own identifier, never by list position or a timestamp sort; confirm the
returned version id and traffic percentage against what you requested; then fetch the live
artifact and grep it for a string only the new code contains. If a wrong version does go
live, say so in the report with the corrected version id rather than letting the original
success message stand.

## A rejection from one HTTP client is not a deployment verdict

Edge networks and WAFs block default library user-agents, so one client can get 403 while another gets 200 from the identical URL. Before reporting a deployment as down, an asset as missing, or access as broken, retry with a second client (curl, then the browser) and report which client saw what. A single-client failure is a client signal until reproduced.

## A guard that protects one site protects one site

A check wired into one repository's build (a lint, a copy guard, a dash count) protects
exactly the projects that script runs for. Before reporting a guard as in place, name which
sites the run covered, and put shared checks in the shared script or the CI config across
repos rather than in a per-repo build step. A green run on the project you happen to have
open reads as coverage you do not have.

## A test asserting the removed contract fails by design

When a deliberate redesign removes a pattern (a hover label swap, a chip UI), grep the test
tree for that symbol first and rewrite the assertions in the same change: tests encode the
old contract, so they go red by design and read as a regression, inviting a rollback of the
polish. Report the rewritten assertions alongside the new pass count.

## Name the fixture boundary of every pass

A run driven by fixture identities, seeded databases or canned provider responses
proves the code path, not the external service. Report it as exactly that: state the
fixture explicitly, then list the live behaviors still unverified (real signup, real
paid checkout, real provider network call, production migration) instead of letting a
fixture pass read as a live one. Fixture success converted into a live claim fails the
same way an unarmed gate does: the report looks healthy in both cases.

## Green lanes are not an integrated pass

When the work is split across branches, worktrees or parallel workers, each lane goes
green against its own slice and proves nothing about the seams: a duplicated shared
file, a contract both sides changed, a route wired on one side only. Copy or merge
every lane's output into one tree and run one integrated gate (build, tests, and a
browser pass over the real combined surface) before reporting done. Lane-level green
reported as done is a pass claim about code that never existed in one place.

## One branch green is the feature on that branch only

When output is composed in several branches (by result shape, by item count, by
type), an assertion driven through the query your test happens to use covers
exactly one of them. Before reporting the feature present, grep the composer for
every site that builds the shared output, anchoring on an element that already
appears in all of them, and drive each shape once; if some shapes stay undriven,
list them as untested rather than folding them into the pass. The branch a test
reaches is often not the branch production reaches most.

## Measure what the browser hands the user, not what the CSS declares

A stylesheet value is an intention. `getBoundingClientRect()` is the box a thumb
actually gets. `min-height: 42px` reads as deliberate and passes a code review; it
also fails a 44px minimum.

- **Measure every visible control**, and measure in **each state where controls exist**.
  A check that stops at the greeting measures the close button and nothing else, so
  slot buttons that only render after an interaction go unchecked entirely.
- **Assert nothing is clipped** (`scrollWidth > clientWidth`) as well as big enough. A
  target can be large enough and still cut the label, which on a value like a date and
  time means the user cannot tell what they picked.
- **Check horizontal overflow at the binding width**, not just the design width.
- **Hit-testing belongs to `document.elementFromPoint`.** Rectangle overlap is the
  weaker question and is the one that lets a floating widget sit on top of a consent
  button. The browser resolves taps, not bounding boxes.
- **Re-measure against the pre-fix values.** A new gate proven only against the fixed
  state may not discriminate. Point it at the old numbers and confirm it reports them.
- **Count what the fixtures already contain before you assert a count.** A new test
  written against a seeded database (seed rows, loaded templates, prior test runs) that
  expects the fresh data alone will report an inflated or deflated number and read as a
  product bug when it is only an unexamined pre-image. Query the fixture for the
  pre-existing rows, or scope the assertion to your own keys, before fixing the code
  the failure appears to indict.

## Browser probes: read the DOM, do not guess selectors

Labels and element order change with state. A quick action labelled one way in the
greeting is renamed once a conversation starts, and a selector chosen from the initial
snapshot times out later in the same flow.

- Dump the live DOM (ids, classes, text of interactive elements) before writing
  interactions, and re-dump after each state change.
- **Write probe scripts to a file.** Inlining JavaScript into a shell or f-string
  collides on `{}` braces and produces an error in the harness, not in the app.
- Return structured objects from `page.evaluate` and print them; a `"".join is not a
  function` trace means a DOM property, not a string, reached a string method.

## Report the shortfall

When a gate turns out not to have been running, say so plainly and quantify it. Do not
present a prior "passing" claim as still valid. The cost of an unarmed gate is that it
was believed, and the honest correction is worth more than the quiet fix.