---
name: outbound-send-verification
description: Use when proving an outreach system can send end to end.
version: 1.0.0
author: Deep / Hermes
license: MIT
metadata:
  hermes:
    tags: [outbound, email, verification, qa, cloudflare, d1]
    related_skills: [shared-checkout-safety, mailbox-provisioning, verification-gate-integrity]
---

# Verifying an outbound send path live

## When to Use

When a live test, QA proof, or BD-facing demo must show the outreach pipeline can research, draft, approve and send for real on the production deployment.

Goal: prove research -> draft -> review -> send works on the real deployment, with tool output as evidence, and report an honest result if a gate stops it.

## Always-on rules

- Exercise the product's own path (its API or UI). Never prove a send with direct SMTP, a different sender tool, or a hand-rolled curl: a proof that bypasses the product's gates proves nothing about the product.
- Read the run's gates before assuming a cause: `readiness.gates` codes (`replied`, `research_incomplete`, `jurisdiction`, ...) name the real blocker. Report the gate list, never a fabricated delivery.
- State cost up front: an AI pipeline run has a per-run price and the campaign has a spend cap. Fix the data layer before re-running instead of burning attempts.
- Clean up after: revoke the temp admin session row and delete cached token files.

## Procedure

1. Read current state first: review endpoint, run events, and the open draft's gates plus its `versionHash`. Approve with the hash you just read; a stale hash fails.
2. Fix data only when it is your own test data, through the product's database (`wrangler d1 execute "$DB" --remote --command ...`, env sourced from the cached db env file). Confirm `rows_written` on every write.
3. Re-run, re-fetch, re-check gates before claiming improvement.
4. End with one real message from a production sender to a real address the requester owns, and quote the persisted row (`outreach_emails`: id, from, to, status, error). A pipeline read-back proves the record moved; only the receiving address, reached on a domain outside this system, proves delivery.
5. Read back the live version/health endpoint and quote it in the report.

## Pitfalls

- Treat `rows_written: 0` as a failed write, not a no-op: a UNIQUE constraint (for example one profile URL per contact record) silently rejects the update and the next run reproduces the old failure.
- Reassigning a record's parent (organization, campaign) drops dependent fields the gates read, such as country for jurisdiction. Re-check gates after any reassignment.
- A draft with zero citations can never become sendable, no matter how approved: block on a missing dated public fact. Confirm the contact has a citable source before a fix loop, or report the honest outcome.
- Do not hand-edit derived columns (default flag, status) by SQL; the app computes them from ordering columns. Use the product's UI, then read the table back to verify.
- A shell exit code of 0 does not mean the deploy landed: read the log tail and the live version hash before reporting success.
- When the requester says they received nothing, ask which address before diagnosing: proof delivered to address A and "nothing at address B" are two different claims, and the second is often an address the first never targeted. Quote the address the test went to in the report so the two never get confused.
- When a gate defers the test (a send window, an approval rule), say so with the exact code (`outside_send_window`, `research_incomplete`) and the time it will fire, rather than reporting the send as pending. A test that the product's own policy intentionally holds is a working gate, and only a decision card can change it.
