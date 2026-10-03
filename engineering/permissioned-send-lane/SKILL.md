---
name: permissioned-send-lane
description: "Use when adding an outbound send path to a read-only system."
---

# Building a send lane in a read-only system

## When to Use

Any time an existing system can ingest (mail, webhooks, polling, transcripts)
but has no way to emit, and something downstream needs it to: replies, follow-ups,
pass-backs, notifications to a third party. The read side usually exists long
before anyone needs the write side, so the gap is discovered late and rushed.

## First: prove the gap is a gap

Grep the tree for transport primitives before planning. For mail:
`smtplib`, `sendmail`, `send_message`, `SMTP_`, `api.resend.com`. Zero hits is a
fact worth stating, because "the workspace can read a client for months and
cannot reply" reframes the task from feature work to blocker removal. Check for
an existing adjacent module too: a voiceover module is not a mail transport, and
a per-audio-asset path is not a general send lane.

## Approval attaches to a shape, not to a message

The requirement that drives the design is latency: a hot inbound must not wait
for a human who is not at a desk. So the reusable unit is a template family
(`audience`, `template_key`, `intent_class`, `client_key`, `expires_at`,
`approved_by`, `revoked_at`), and each send records which template covered it or
which human did.

Return the **reason**, not a boolean. `cover_decision()` must say which rule let
a message through or stopped it (`semantic_drift`, `expired`, `revoked`,
`not_approved`, `scope_mismatch`), checked in the same order `live_template`
tests them. A bare boolean means the only way for an operator to learn the rules
is to send something wrong, and a wrong reason sends them to fix the wrong thing.

Four rules, each with a test:

1. No human signer means no permission. A row an agent wrote with an empty
   `approved_by` is a proposal and never authorizes a send.
2. A live template clears a matching send immediately, with no human on the day.
3. **Semantic drift breaks the cover.** A stable `intent_class` key is what makes
   "same shape, different meaning" detectable. Same `template_key` with a
   changed intent must NOT be covered.
4. Client withdrawal kills precedent. Keep withdrawal cues deliberately narrow: a
   broad phrase list silently expires live approvals on ordinary prose, which is
   the worst failure available here because it blocks mail a human explicitly
   cleared.

Who may approve a template is a separate decision from who may approve one
message. The template is the more consequential grant, so gate it to admin.

## Three invariants that stop a test run from widening production

1. **A simulated send writes no precedent.** Give the test transport a
   `simulated=True` result and skip the precedent write. Otherwise a test run
   quietly widens the permissions of a real deployment.
2. **A sent row is terminal.** Re-approving it is the first step of a double
   send. Map the domain `ValueError` to an explicit 4xx or it surfaces as a 500
   and looks like an outage rather than a guard.
3. **Unfilled placeholders block before the transport resolves**, so a literal
   `{{client.name}}` can never reach a recipient. Flatten newlines in substituted
   values: a value must not be able to inject a header.

## Refuse loudly; never degrade to a no-op

Missing provider, read-only mode, and placeholders must all raise and persist a
`blocked` row carrying the reason. A transport that silently accepts and drops
messages is worse than one that refuses to start: the failure is a request
nobody received, and nothing reports it.

For testability, ship a `record` provider that logs and sends nothing, and say so
in its own status string. That gives a real database and a real transport
interface to exercise approve -> send -> precedent against, with no possibility
of mailing anyone.

## Where an LLM restates a human

Any step that rewrites what a person said must be able to report what it could
not carry across, and a non-empty report must BLOCK rather than warn.

- A message referring to a conversation must carry a quote **matched against the
  stored pool**, not merely a non-empty quote string.
- Forwarding someone's message onward must list anything dropped in a
  `fabrications` field; if it is non-empty, stage the send as blocked and let a
  human decide what the recipient actually hears.
- Withdraw stale quotes from the pool entirely rather than marking them: a stale
  quote in an outbound message is a wrong statement, and hiding it is cheaper
  than sending it.

Require the model to emit schema-valid JSON and parse it tolerantly (fenced,
prose-wrapped, outermost brace span). A model failure here must be recorded as a
failed attempt, never raised into a poller that would drop every pending item.

## Scoping learned preferences: exclude, do not deprioritise

For per-client preferences, filter `client_key == this OR client_key == ""`.
Ordering global-below-specific leaks client A's habits into client B's mail (an
internal cc address, a wrong timezone, a wrong salutation). Test that
cross-client preferences are **absent**, not merely ordered lower.

Give every preference evidence and a confidence, with an actionable floor below
which it is displayed but not acted on alone. Learn from a repeated signal only:
one rejection is an incident, three is a pattern. Reuse the tally the system
already computes rather than adding a second one that can disagree with it.

## Documentation is part of the deliverable

Every env var the code reads must appear in the example env file, and every var
documented there must be read by something. When a repo tests this, it usually
fails in both directions: a new read that nothing documents, then a documented
var that no literal read matches. Read env vars with a literal
`os.environ.get("NAME")` at module scope; a helper taking the name as an
argument will not satisfy a source scanner.

Ship the credential list in the order to apply it, with the safe intermediate
mode named first (log-don't-send), and name the external lead times (OAuth
verification, DNS records for deliverability) as separate from the code work.

## Alembic and test-fixture traps when adding tables to an existing repo

- If the test suite builds schema from MIGRATIONS rather than `create_all`, a new
  model with no migration fails every test. Write the migration first.
- **The repo may already have more than one alembic head** from an uncommitted
  branch. `alembic upgrade head` then fails with "Multiple head revisions". Run
  `alembic heads` and parent to the real head. Do not hand-roll a parser to
  diagnose it: `revision = 'x'` uses single quotes in some files, so a
  double-quote-only regex misses revisions and invents a broken chain.
- **Tests that call modules directly never trigger an API fixture's table
  wipe.** Give them their own cleanup, using `Model.__table__.delete()`.
- **`db.add()` without `db.commit()` makes rows invisible to the next query.**
  The signature is a test that passes alone and fails in sequence, which reads
  like ordering or fixture pollution. Check for the missing commit first.

## Route registration in a large existing file

- Match the file's existing conventions rather than assuming FastAPI imports.
  In one codebase `Query` was not imported at all, so using it broke the module
  at import time; existing routes used plain defaults.
- Duplicate decorators on the same path silently shadow. Count the routes after
  adding them.
- Inventing a dependency name (`_role`) fails at import. Check for an existing
  `require_admin`-style dependency before writing a gate.