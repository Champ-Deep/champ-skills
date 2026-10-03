---
name: visitor-tracking-and-proactive-engagement
description: "Use when a site acts on inferred visitor intent."
tags: [tracking, analytics, consent, identity, outreach, widgets]
related_skills: [adapter-seam-extension, defensible-data-counts]
---

# Visitor tracking and proactive engagement

How to build site-side features that watch an anonymous visitor's behaviour and act
on it: repeat-visit detection, intent scoring, personalised greetings, and reaching
out before the visitor asks.

## The class rule

**A widget that greets someone differently is making a claim about them.** Every
personalised surface needs a named gate, and the weakest signal must degrade the
*content*, not just the confidence score.

Degrade by withholding the specific claim and keeping the useful part. If a shared
office IP makes the company name unsafe to say, drop the name and still deliver the
help. Blocking outright discards a real buying signal because an office shares an
egress address.

## Identity is company-level, and that is a design constraint

Reverse-IP resolution gives an organisation, not a person. Design every downstream
surface around what that means:

- **No person fields in any payload.** Shipping empty or guessed name/email/role makes
  a CRM render a company signal as if it were a contact. Put the reason on the record
  instead; it is what the human actually reads first.
- **The channel follows from the identity.** With no verified address, you cannot
  honestly cold-email anyone. Deliver proactive messages in the surface the visitor
  is already in. This dodges consent-to-cold-email and anti-spam exposure at once,
  and it is usually the better experience anyway.
- **Weak identification is a first-class state**, not a boolean to normalise away.
  Track it, badge it in the rep UI, and run the guard *before* the copy branch so the
  sensitive value can never leak into the wrong template.

## Consent is a hard precondition, not a field

Store consent as a timestamp plus the notice version, never a bare boolean: the burden
of proving notice sits with you. Withdraw it by nulling the timestamp, then verify the
downstream rows are actually gone, not merely hidden.

Gate every enrichment action on consent, and let a hard legal exclusion (a minor flag)
outrank consent.

## Tracking mechanics worth getting right

- **Set identity cookies server-side with `Set-Cookie`, never from JavaScript.**
  Safari's tracking prevention caps cookies *created in JavaScript* far more aggressively
  than one set on your own origin. Setting it from JS silently resets it on exactly the
  returning visitors you built the feature to recognise.
- **A cross-origin embed needs `credentials: "include"` on every call, or the cookie is
  dropped in both directions** and every visit looks like a new person. This reproduces
  the exact symptom the feature exists to fix, so it survives unit tests.
- **Compute a session gap from the last-seen field, never from the field you only write
  when you detect a gap.** Measuring from the gap field is circular and can never
  advance, so every return folds into one session. Initialise counters at 1, not 0, or
  every count is short by one.
- **Dedupe within a batch as well as in the database.** A DB check cannot see rows that
  are not committed yet, so N people from one company become N queue items.

## Test the tone, do not trust it

Generated user-facing copy is the product here, so its constraints are testable and
must be. See `references/copy-tone-constraints.md` for the banned-phrase sweep recipe.
The short version: creepiness shows up as "again" and "times", not anything dramatic,
and a one-per-visitor message rule belongs in the model rather than in a judgement call.

## The fixture trap that hides all of this

**A green suite proves only the assertions that executed.** Behavioural tests fail most
often because the fixture quietly discards the field under test, so the guarded branch
never runs and the test passes for the wrong reason. This session hit it three separate
times, each time on the guard that mattered most (weak identification, consent,
returning-visitor state).

Defences:

- End fixture builders with `assert not kwargs, f"fixture ignored {kwargs}"`.
- Assert the **branch**, not just the end state: the reason string, the log line, the
  chosen branch name. Two branches returning the same value are indistinguishable.
- When a test expectation disagrees with the code, decide which is wrong *before*
  editing either, and re-derive the count from the definition. Several "product bugs"
  were arithmetic errors in the test.
- A helper that accepts a parameter and never uses it is a dead feature that reads as
  implemented. Search for it by name after wiring anything new.

## Verify against the real thing, not the harness

A widget harness and the real site differ in origin, cookie handling and CORS, so a
feature proven only in the harness can be dead in the browser. Drive the real flow with
a real cookie jar and a real browser, and confirm the identity actually persists across
visits rather than assuming it.

Count what the browser rendered, not what the payload contained, and read the console.

## Pitfalls

- **Announcing what you watched.** Reciting a visit history proves the widget was
  watching them. Let the visitor complete a vague forward reference themselves.
- **A cron that only ever runs by hand.** If the queue is populated only by a rep hitting
  an endpoint, it is dead code in production. Hang the scan on the existing worker, with
  per-tenant error isolation so one bad row cannot stop every other tenant.
- **Burning a once-per-visitor chance at generation time.** Acknowledge on *render*, so
  a message the embed failed to display does not silently consume the visitor's single
  chance. A duplicate ack must not reopen the window.
- **Inventing an API.** Check the real module for the type, request-body and
  tenant-scope helpers before writing an endpoint. A strict contract interface is
  usually the fastest way to discover you guessed wrong.