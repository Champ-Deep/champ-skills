---
name: mailbox-provisioning
description: Use when buying or wiring mailboxes for an outreach domain.
version: 1.0.0
author: Deep / Hermes
license: MIT
metadata:
  hermes:
    tags: [email, mailboxes, domains, inboxkit, deliverability, avatars]
    related_skills: [outbound-send-verification, outbound-email]
---

# Outreach mailbox provisioning

## When to Use

When buying domains or mailboxes on an inbox provider, wiring them into the sending product, choosing a Google/Microsoft mix, or preparing avatar files and CSVs for import.

Buying domains/mailboxes on an inbox provider, wiring them into the sending product, and handing the list to the user.

## Always-on rules

- Match the mailbox provider to the recipient: Google-hosted mailboxes land best in Gmail inboxes, Microsoft-hosted in Outlook. Mix domains by who gets written to, not by name.
- One avatar file per person, JPEG under 2 MB, named `<username>.jpg`. GIFs and animated avatars are wasted effort: Gmail and Outlook flatten profile pictures to the first frame, and a synthetic face on a cold mail hurts trust. Funnels work, humans win; funnels where synthetic faces help are the exception.
- Always include a first.last alias row alongside the bare first-name row; sequences usually send from the alias.

## Procedure

1. Check domain and mailbox state through the provider API with a short-lived session (create, use, revoke in the same run). Read the actual key/env value before blaming a 401 on the provider: an env var holding `""` is unset, not blank.
2. Import into the sending product through its own import path so the login gets verified; an unverified connection will not send. Read back the connection table (`from_address`, `status`, `is_default`) to confirm.
3. Deliver the CSV with the file-upload column present so avatars can be dragged in directly; no separate hosting step.
4. If the test made a new connection the default sender, pin the previous default back when done.

## Pitfalls

- Purchased mailboxes are inactive until the provider's own onboarding finishes; importing before activation fails login verification and must be redone.
- Auto-publishing a provider's DNS records into someone's zone: act on the record's `purpose` field, never on its shape. An inbound `mx` record at a name that already has MX records takes over the owner's inbound mail, so report it as a conflict and add nothing; SPF merges by hand; an existing DMARC stays. Build the test fixture from the provider's documented record list (OpenMail: apex MX, long DKIM TXT, `bounce` MX + SPF, `_dmarc`), not from a guess, or the dangerous case never runs.
- Comparing a long TXT (DKIM) for idempotency: Cloudflare stores content over 255 bytes as quoted strings (`"part1" "part2"`). Join the strings before comparing, or every re-run posts a duplicate record.
- Verify availability through the provider's own check (live API call in the same session), never from a registration-page screenshot or an availability aggregator.
