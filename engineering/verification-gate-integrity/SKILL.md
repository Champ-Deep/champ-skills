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
- **Report passed and skipped as two numbers.** "199 tests pass" from a suite
  that silently skips 112 without its database is a total, not a pass count.
  Quote the pytest summary line verbatim and name the service each skip needs.
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

The same discipline applies to processes: stop a test server you started by its own
PID or its background-job handle, never a broad `pkill -f <script name>`. The pattern
matches every process with that name on the machine, so it takes down whatever else is
running under it, and your own run reports success either way.

The inverse direction bites too: a script can report success as a failure, because
`sys.exit("message")` prints to stderr and returns 1. Never gate a step on the exit
code of a script you or a teammate wrote; gate on the effect, by calling what the step
provisioned (the user, the route, the file) and asserting it answers. Wrapping such a
step in `|| true` to make it green is the same error in reverse: it swallows the real
failure too.

Backgrounding multiplies the same error, because the harness reports the pipeline's status as the job's: a command run as `deploy.sh 2>&1 | tee log` finishes with tee's zero, so a run that died mid-build surfaces as "completed normally (exit code 0)". When you background anything that can fail, redirect instead of piping (`deploy.sh > log 2>&1`), and before repeating any wrapper status, grep the log for the script's own failure markers and probe the target's live identity. A completion notification is a statement about the wrapper, never about the work.

## A test that passes only in file order is not a gate

A test that relies on state an earlier test left behind (a config row an admin test
wrote, a seeded provider) passes in the full run and fails, or worse, takes a live
path, when run alone, filtered with `-t`, or shuffled. Before reporting new tests
green, run each one alone (`npx vitest run <file> -t "<name>"`) and require the same
verdict. Set offline defaults in the test bindings themselves (a `mock` provider, no
real upstream URL), so a stray test can never reach a paid third-party API with a fake
key. A test named for a negative guarantee ("the refused write changed nothing") must
create the before-state, attempt the write with a value that differs from it, and read
it back in the same test.

## A refusal gate is a classifier: probe both directions on held-out prompts

A safety or refusal rule set (regex gates, keyword lists) that passes its own bank proves only the bank, because the bank is what it was tuned on. Before reporting it done, run at least 10 held-out prompts it must refuse and 10 it must answer, written after the rules, in the product's real phrasing ("can I have magnesium-rich food" is a food question that a drug-name list will refuse). Paste the per-prompt table, and list every miss in either direction as a stated limit or a fix. A widened term list mostly buys recall with false refusals, and only the must-answer half shows that.

## A fix fitted to the reported input is proven on that input only

A precision fix for a heuristic (a scraper, a classifier, a parser rule) that is
validated on the one site or sample named in the bug report shows it beat that
sample, not that the class of defect is gone: the next site carries the same junk
in a shape the new rule never saw. Before reporting a precision fix done, run
the extractor on a held-out set of at least 8 real inputs the fix was not built
from, and report the junk rate per input (rows or links that are not the target
entity) alongside the reported case. A fix that only clears the reported input
goes back as a fix to the rule, not a ticket for the next site.

An input that yields zero rows tests nothing about precision, so the 8 count
only inputs that produced output. Spread the set across organisers and
platforms (one trade-fair operator's sites share one template and fail
together), and include page shapes known to fool the rule class, such as news,
blog and session grids with tag or category labels. Run the old and new rules
on the same set: a row dropped by the new rule is a precision win or a recall
loss, and only reading it tells which.

## A rebuild from the package proves reproducibility only if it equals the shipped build

"The extracted ZIP builds" proves the package compiles, not that it reproduces the artifact you shipped beside it. Build tools that scan a directory (Tailwind `@source`, glob imports) pick up files the packager left out, so the shipped build and the rebuild can differ silently. After rebuilding from the extracted package, diff its output against the shipped artifact (bytes, or the generated class or module list) and either package the missing inputs, rebuild the shipped artifact from the package, or report the delta and why it is inert.

Run the package's own test suite **from the extracted tree**, not from the repo checkout. The mechanism is the same missing-file class one layer down: an untracked fixture, a config file or a seed data file the packager skipped passes in-repo and fails extracted, and that gap is exactly what the bundle is about to hand its next owner. Quote the exit code and the collected test count from the extracted run as their own claim, and never let the in-repo green stand in for it. Package by explicit exclusion (caches, bytecode, worktrees, `.git`) rather than by inclusion list, so a new source file is carried by default.

## Prove the gate by breaking what it guards

Reintroduce the exact defect, confirm the test fails and names real numbers, revert,
confirm green. Run this on converted and inherited gates, not only the ones just written. A
gate never seen failing is a gate nobody knows is armed.

A `disabled` assertion is vacuous when the fixture trips a second disabling condition. A
Send button asserted disabled "while unpublished" on an event with an empty team, with
audience `team`, stays disabled for the empty team even after the publish guard is removed.
Build the fixture so the guard under test is the only reason for the state (a team member,
a filled message, audience `everyone`), then delete that guard and require red.

## A removal is proved by absence

Checking that the new shape exists proves nothing about what was taken out: an old field can
still be emitted beside the new one and every presence check stays green. After removing a
provider, a column, a flag or a route, grep the consumer's own artifact for the removed
symbol (response fields, the generated header row, the exported column list, the served
bundle) and require zero hits, then read that artifact back end to end. Report the symbol you
grepped and the artifact you grepped, never "the field is gone". The same applies to config:
a health endpoint that still advertises the removed capability is a leak of the same kind and
counts as a failed removal.

## The gate you wrote for a deployment has never run anywhere

A smoke script, deploy check or post-rollout probe is unverified code until something
has executed it. Run it against a local instance in the same configuration first, so
its first run diagnoses the deployment instead of debugging itself: a missing env
var, a wrong path or a malformed assertion otherwise surfaces as "the deploy failed"
and gets reported upward as a platform problem. Then break the guard locally and
confirm it goes red, so the live run means something. Only after both does the same
script pointed at the real host earn the word "passed".

## Prove "pre-existing" on the baseline, not from memory

Before reporting a red test as unrelated to your change, run that exact command on
the unchanged baseline (a stash, a worktree of the base commit, or a clean checkout)
and capture the same failure there. A failure reproduced on the baseline is a
pre-existing defect you can name with evidence; a failure you merely recognize as old
is a guess wearing the costume of a finding, and it shields your own regression when the
two happen to share a symptom.

Compare the *set* of failures, not the count, and compare it across two runs of the
same tree as well as against the baseline. A run reporting one more failure than the
next identical run means the suite contains a flaky test: name it as flaky instead of
folding it into the pass, because a gate that grades differently per run is a gate
whose green you cannot rely on. Report the final set, and disclose any run whose set
did not reproduce.

## A deflake is proven only under the load that caused the flake

Green runs of a timeout flake on an idle machine cannot discriminate: the unfixed code passes there too. Before claiming a deflake, reproduce the failure on the base commit (run base and fix suites concurrently, or under the same machine load the report came from), then run the fix under that same load. Report the flaky test's own duration against its timeout in every run (`--reporter=verbose` prints it), not just the pass count: a fix that moves 5.2s to 4.3s under load still has under 1s of margin and will fail again. If the base failure never reproduced, say the green runs are unproven rather than calling them proof.

## Time a delay inside the page, not around the driver

A hover-intent or debounce assertion written as `hover(); wait_for_timeout(60); expect closed` measures Playwright's own actionability, scroll and IPC time as part of the window, so a correct 120 ms open delay fails whenever the first browser context is cold. Record timestamps in the page (`performance.now()` on `pointerenter` and when the open class lands, via a `MutationObserver`) and assert the difference, or drive the event with `dispatchEvent` and read state on the next frame. Run any timing gate three times before reporting it green: one red in three is a flaky gate, not a pass.

## A test that reads credentials from your shell is not hermetic

A suite asserting on an exported key passes on a machine where the variable is
unset and fails, or behaves differently, where it is exported, so the failure
tracks the shell rather than your change. Re-run with the variable explicitly
unset before calling such a failure pre-existing: the unset run restores the
state the test assumes, which makes it the discriminating probe.

Read that output before you paste it anywhere. An assertion comparing a real
credential prints the credential, so capture the run, scrub it, and name the
exposed token for rotation instead of letting it ride into a report or a
transcript.

## The printout is not the artifact

Output reaches you through a display layer that can mask PII-shaped tokens
(phone numbers, card digits) before you read them, so a response printing
`+141****6273` may be a redacted view of a value holding every digit on disk.
Decide whether a value is masked, truncated or corrupted by inspecting the file
itself (`len(value)`, digit count, `'*' in value`, a hash) rather than by reading
the printed copy: a healthy value judged corrupt from its redacted printout sends
a fix round at a defect that is not there, and a genuinely corrupted value judged
redacted ships. Never quote a printed identifier as proof of what the file holds.
Measure the artifact, report the measurement.

## An edit is claimed only after the file reads back changed

A script that raises before its `write` leaves the file as it was, and every
later gate (count, dash grep, parse) still passes on the old content, because
none of them checks the fix. Before reporting a fix, read the field you changed
back from disk and assert the new value (`json.load(...)[...] == expected`), and
check the file's mtime moved. One ledger fix round claimed three JSON edits; the
script had errored on its first assert, the JSONs kept their old mtime, and
only the markdown summary was rewritten.

## Promotion is a sequence of claims, not one

Deploying is a chain (find the version, deploy it, promote it), and the tool's success
message is not proof the chain did what you intended. Assert each link: match the version
you uploaded by its own identifier, never by list position or a timestamp sort; confirm the
returned version id and traffic percentage against what you requested; then fetch the live
artifact and grep it for a string only the new code contains. For a bundled SPA
the cheapest form is to diff the hashed entry asset: read the `index-<hash>.js`
name out of the served `index.html`, compare it to the hash in the local
`dist/index.html`, then fetch that asset and grep it for the feature strings
added this round. A mismatched hash means the old build is still being served
even though the deploy command printed success. If a wrong version does go
live, say so in the report with the corrected version id rather than letting the original
success message stand.

## A stored secret is not a used secret

Rotating or swapping a credential in a deployment proves only that the new value is
stored. A running process keeps the old secret in memory until it restarts, and a
gateway that holds a connection under a different identity bills elsewhere while the
call still succeeds, so the swap looks live from every config view and is not.

Split the claim in three, and prove each: read the config back (stored), restart or
redeploy the process that must pick it up (loaded), then prove use from the
*provider's* side with an identity only the new credential can produce: the call
appearing in the owning account's own audit, a response header naming the serving
vendor or route, a per-key usage counter that increments. Config read-backs and CLI
success messages prove storage; only the upstream's own record proves use. When they
disagree, report the storage change as made and use as unverified instead of calling
the swap live.

## Some endpoints cannot be probed with the HTTP client you reach for

A WebSocket upgrade route answers only a real handshake: Node's `fetch` refuses to
send an `upgrade` header and curl does not complete the handshake either, so a
status code from either says nothing about whether the route works. Probe the
plain HTTP routes with curl and the upgrade route with a real client (browser
WebSocket, `ws` package) that asserts the first message back, and report which
kind of probe produced which evidence instead of folding both into "the endpoint
responded".

## A rejection from one HTTP client is not a deployment verdict

Edge networks and WAFs block default library user-agents, so one client can get 403 while another gets 200 from the identical URL. Before reporting a deployment as down, an asset as missing, or access as broken, retry with a second client (curl, then the browser) and report which client saw what. A single-client failure is a client signal until reproduced.

## Behind an auth gate, a real route and a fake one answer alike

When every request is refused by an auth layer before routing, a path that does not exist returns exactly what a real path returns: the same 401, the same redirect. No outside probe can tell the two apart, and comparing two builds only proves the bundle changed, not that any route or feature works. Establish a control probe first (an obviously fake path), compare it against the real one, and when the two are identical report the surface as **not verified from outside**, wording it as "served by this build" rather than "works". Getting to a working claim needs an authenticated session, a fixture account, or a route that answers differently from the control.

Compare like with like: a status that moves between two probes usually means the probe's auth context changed, not that the code did. Signed in, an absent route returns a real `404` because routing ran; unsigned, the same path answers a `307` or `401` from the gate that fires before routing. So a `404` becoming a `307` across a deploy is no evidence the route arrived, and reading it that way reports a feature that does not exist. Hold the same session, cookies and client for both sides of any before/after, read an authenticated `404` as "the gate passed and the route is absent", and reserve "now it works" for a signed-in probe that renders the screen.

## "Testable" means deployed

An endpoint, screen or flow is testable by a person only in the build actually serving traffic. Code merged to the release branch but not yet deployed is not testable, and a report that lists it beside live capabilities reads as an invitation to test something that will 404. Split every capability list by deployment state: live now, live after the deploy, and dormant until a named key or config arrives. A code path present but missing its credential is dormant rather than broken, so name the missing variable instead of calling the feature broken or omitting it.

## A guard that protects one site protects one site

A check wired into one repository's build (a lint, a copy guard, a dash count) protects
exactly the projects that script runs for. Before reporting a guard as in place, name which
sites the run covered, and put shared checks in the shared script or the CI config across
repos rather than in a per-repo build step. A green run on the project you happen to have
open reads as coverage you do not have.

## A count of your own output cannot prove coverage

"7 items, 7 host lines" checks a list against itself, so it passes whether the list is
complete or not. When acceptance says "every X covered", derive the denominator from the
canonical record independently of the list (in Celsus, grep TASKS.md and the dated notes for
the same action phrase, open rows and later dates included), then diff the two sets and
report each item on the record but absent from the output with a one-line reason it was
excluded. A brief that names N items is a starting list, not the denominator, when the
record has kept growing since the brief was written.

## A quote matched against your own transcription is not a citation check

A strict citation pass that compares a ledger quote with a vision transcription you wrote
checks the transcription against itself. Vision models both invent and autocorrect typos:
one brief told a writer to fix "Candiate" in a graphic that OCR reads as "Candidate". Before
any finding that rests on exact image spelling or a figure read from an image, run OCR with
language correction off (`tesseract img.png -`, or Apple Vision `VNRecognizeTextRequest`
with `usesLanguageCorrection=false`) and require two readers to agree. Report the image
quote as transcribed, not as verified.

## A test asserting the removed contract fails by design

When a deliberate redesign removes a pattern (a hover label swap, a chip UI), grep the test
tree for that symbol first and rewrite the assertions in the same change: tests encode the
old contract, so they go red by design and read as a regression, inviting a rollback of the
polish. Report the rewritten assertions alongside the new pass count.

## A library can switch its own guard off under test

Some auth libraries relax a security check when they detect a test runtime (Better Auth
skips its Origin/CSRF check when `NODE_ENV=test`). A suite that runs under that default
proves the request shape works, not that the guard rejects anything. Pin the production
value explicitly in the config (`advanced.disableOriginCheck: false`), then break it once
to confirm the cross-site test goes red. Grep the library's context setup for `isTest` or
`NODE_ENV` before trusting any green security test built on it.

## Name the fixture boundary of every pass

A run driven by fixture identities, seeded databases or canned provider responses
proves the code path, not the external service. Report it as exactly that: state the
fixture explicitly, then list the live behaviors still unverified (real signup, real
paid checkout, real provider network call, production migration) instead of letting a
fixture pass read as a live one. Fixture success converted into a live claim fails the
same way an unarmed gate does: the report looks healthy in both cases.

The boundary can be an environment, not just a fixture: when the full application
cannot start locally (uninstalled runtime deps, no database), a compile check plus a
pure-function suite proves the logic layer only. Name the unexercised layer (HTTP
routes, wiring, migration) as an explicit gap in the report, or land a follow-up card
covering it, instead of presenting a tiered pass as end-to-end verification.

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
- **When a vision read and a DOM measurement of the same page disagree, the measurement
  decides.** A screenshot review will report overlaps, clipping and drift that
  `getBoundingClientRect()` shows do not exist, because it is describing pixels and
  patterns rather than boxes it measured. Take the vision pass as a prompt to write the
  geometry probe (chip right edge versus text left edge, `scrollWidth <= clientWidth`,
  card-to-card overlap, `naturalWidth` on images), print the counts, and act only on what
  the probe counts. Reverting a correct layout because a screenshot sounded wrong is the
  same error as trusting a green gate that never ran, in the other direction.
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
- **A mount call that returned is not a render.** When a harness mounts several surfaces,
  assert each one by its own selector (non-empty content, its heading) before claiming it
  mounted. An imperative handle on a React root (`open()` dispatching an event that a
  `useEffect` listens for) is dropped when called in the same tick as the mount, because the
  effect has not attached yet: test "mount then call immediately" as its own case.
- **Write probe scripts to a file.** Inlining JavaScript into a shell or f-string
  collides on `{}` braces and produces an error in the harness, not in the app.
- Return structured objects from `page.evaluate` and print them; a `"".join is not a
  function` trace means a DOM property, not a string, reached a string method.

## A green gate does not clear a human hold

Technical verification and human approval are separate claims about the same artifact.
Once the owner has rejected a design, every later gate passing on that build says
nothing about the rejection, and a completed verification child must never be the thing
that releases it. Keep the hold as an explicit dependency on the publishing task (parent
gating, not a comment), so completing verification cannot satisfy the publish gate on
its own, and confirm the hold still stands immediately before any release step. Name the
hold in the report's verdict line, not only in a comment, or the green checklist reads
as sign-off.

## A gate's own label decides whether it gated

Read the gate's configuration line, not just its verdict word: a finding printed as a block beside `WARN-ONLY (in gate-config.json warn_only)` stopped nothing, so "the gate passed" then describes the config rather than the code. Quote the classification back, and when a required audit was skipped because the owner said to proceed, carry the skip into the PR body and the report as an unproven item instead of letting the green checklist stand in for it.

## Report the shortfall

When a gate turns out not to have been running, say so plainly and quantify it. Do not
present a prior "passing" claim as still valid. The cost of an unarmed gate is that it
was believed, and the honest correction is worth more than the quiet fix.

## Split the verification across a deploy window

A rollout takes minutes, and everything run inside that window measures the old
build. Divide the checks first: probes served by the *current* build (database
reads, third-party lookups, static pages) are valid now and cost nothing to run
early; only the rollout-dependent checks wait for the platform's own "LIVE" or
commit-identity signal. Read that identity field back before any post-deploy
claim, because a check issued during the window reports the previous code and
reads exactly like a failed fix. Never edit the working tree while the image
builds: the snapshot is already taken, so the change ships next time and the
after-check silently grades the old code again.

Read the whole deploy log after the rollout line, not just the line itself: some
deploy scripts emit their own failure summary, a failed post-deploy smoke for
instance, *after* the platform reports the container live. Quoting the first line
alone reports success for a build that just failed its own gate.

## Score a comparison with the same probe on both variants
When two designs are being compared (two data structures, two schemas, two layouts),
running each variant's own test proves only that each one works, not that one is
better, and the scores are not comparable across different question sets. Define one
probe (the identical question battery, the identical gesture, the identical metric),
run it against both variants, and report the two scores side by side. A verdict like
"the recommended structure answers better" is only a number once the same probe
produced both numbers, and the losing variant's failures should be listed, not just
counted, so the reader sees which questions it got wrong. If a variant cannot run the
probe at all, that is the result, and it belongs in the table rather than in a
footnote.