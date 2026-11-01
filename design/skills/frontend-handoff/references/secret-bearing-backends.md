# Secret-bearing backends: filters, fixtures, and simulation gates

For a backend whose state contains information some viewers must not see: a game
engine with hidden roles, a billing service with other tenants' rows, an ops tool
with secrets. The handoff from such a backend carries obligations that a normal
route list does not, and each one has a mechanical check.

## 1. One state, N filtered views, one is the contract

Author the full state once, then derive every renderable payload with one pure
`viewFor(state, viewer)` function. The viewer is a recipient id, not a role:
that forces the id-to-permission mapping to exist as data instead of being
re-decided at each call site.

- Server and client must call the SAME function. A hand-written "public" view on
  the transport plus a second richer one for tests is how hidden fields leak: the
  two drift, and nothing fails when the transport view grows a field nobody meant
  to publish.
- Segment a channel by audience in the data (every message carries who may read
  it), not by separate sockets or separate stores. The transport then enforces
  one rule: address messages, deliver only to the addressee.
- Document the who-sees-what table IN the handoff. The receiving lane must be
  able to assert it, and an assertion it cannot check needs the field named.
- A viewer with nothing private (a spectator, a public display) still goes
  through the same function. "No secrets here, so skip the filter" is the branch
  that publishes secrets the day someone adds a role.

## 2. The leak assertion is an acceptance criterion, not a review note

Put the privacy check in the receiving lane's runnable gate so it fails the build:
a listener opens the same channel as any eavesdropping client, records every
message addressed to the public/spectator viewer, and asserts that before the end
of the run no payload carries a privileged field. Assert on absence of KEYS, not
on absence of particular values, so a new privileged field fails without a new
test.

## 3. Give the frontend fixtures it can grade against

Generated-on-the-fly ids and random names make a UI unverifiable: any screenshot
looks right, so nobody can tell wiring from mockup. Derive fixtures by running the
real code with a fixed seed, then paste the literal output into the handoff:
the room code, the join sequence, the dealt values, the exact display strings.
The receiving lane's end-to-end run must reproduce them, which proves it imports
the real module rather than a lookalike.

- Prefer fixtures the spec itself defines, so the check has authority beyond the
  implementation. If a spec quotes "Mr. HIBT42", regenerate it with the PRODUCTION
  generator (the spec's characters can lie). A fixture outside the production
  alphabet makes the test fail while the code is correct: fix the fixture, never
  the validator.
- Ask for a fixture set covering every branch in one run, alongside the typical
  and extreme records: the hostile one (a viewer trying to read a secret it should
  not have), and the boundary one (the last legal value in the domain).

## 4. Measure emergent behaviour with a headless simulation, then report the number

When agents play the system (AI players, bots, scripted users), run the pure loop
without any UI for a few hundred seeds and print aggregate counters: outcomes,
phases entered, actions taken, and whether every run terminated. This is minutes
of work and it separates three very different failures:

1. an implementation bug (a run throws, a run ends with no winner);
2. a behaviour bug (the actors do nothing, spam, or stall);
3. a design property of the rules themselves (one side wins 75% of games and
   nothing in the implementation is wrong).

Name which of the three you are reporting. A lopsided win rate reached only after
you fixed two real bugs is not a third bug to keep hunting, and calling it one
sends the next session chasing the same dead end. The honest report states the
rate, the sample size, and the levers that would move it (role counts, timer
lengths, information the rules leak), leaving the rebalance as an explicit decision.

Tune behaviour one lever at a time against the same seed range, re-running the
simulation after each, so a change that helps one counter and hurts another shows
up as a delta rather than a fresh guess.

## 5. Name the transport limit plainly

Same-origin tab channels (BroadcastChannel, localStorage events) cannot keep
secrets from other tabs, because every tab can read every message: per-recipient
filtering is real at the engine boundary and absent at the wire. State that as a
known limit in the handoff and name the server that fixes it (one socket per
authenticated recipient), rather than letting a local demo read as a secure
deployment. Do the reverse too: a temporary local channel is fine for a prototype
if the doc says exactly what must change before players are on separate devices.
