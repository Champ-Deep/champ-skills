---
name: champions-b2b-workspace-development
description: "Use when building Champions B2B Workspace features."
---

# Champions B2B Workspace development

Use this for product work in the Champions B2B Workspace, including vendor access, client operations, mailbox intake, file delivery, and workflow automation. This is not Champbeam.

## Start with the shipped product

1. Verify repository identity and branch state before planning:
   ```bash
   git -C '/Users/deep/Apps&Projects/champ-workspace' fetch origin
   git -C '/Users/deep/Apps&Projects/champ-workspace' status --short --branch
   git -C '/Users/deep/Apps&Projects/champ-workspace' remote -v
   git -C '/Users/deep/Apps&Projects/champ-workspace' log --oneline --decorate -12
   ```
   Preserve uncommitted and unpushed prerequisite work. Do not silently reset to `origin/main` or start a feature from an older base.
2. Read `CONTEXT.md`, `README.md`, and the existing `DESIGN.md` before changing behavior or UI.
3. Trace the relevant lane end to end. For vendor work, inspect `backend/app/vendorops.py`, the `/api/vendor/*` and `/api/clientops/*` routes in `backend/app/main.py`, vendor models and migrations, `backend/tests/test_vendor_*.py`, `frontend/app/vendor/page.tsx`, and `frontend/lib/api.ts`.
4. Inspect reusable adjacent lanes before adding infrastructure. Mail ingestion lives in `backend/app/mailbox.py`; guarded client files live in `backend/app/sources.py`; drive hooks live in `backend/app/driveintake.py`.

## Extend the vendor portal, do not replace it

The vendor portal already has Clerk-backed vendor identities, client and campaign assignments, scoped client reads, approved-work access, a two-way update thread, and a path fence. Treat it as an existing product surface, not a greenfield portal.

- Make `VendorAssignment` the authorization grant. Every vendor-created delivery must resolve through the signed-in `person_id`, an active assignment, the assigned client, and the optional assigned ticket.
- Keep vendor endpoints under `/api/vendor/*`. Keep team review, configuration, replies, dispatch, and overrides under `/api/clientops/*`.
- Never grant access from a client name supplied by the browser. Derive client and ticket scope from the assignment row.
- Preserve the vendor fence: a vendor can reach `/api/me` and `/api/vendor/*`, not the general workspace APIs.

## Build one vertical slice at a time

Follow RED, GREEN, REFACTOR for each behavior:

1. Add one failing API test that proves authorization, state transition, or file safety.
2. Run the exact test and confirm it fails because the behavior is absent.
3. Add the smallest model, migration, service, and route change that makes it pass.
4. Run the focused test, then the full backend suite.
5. Add the typed frontend API function and one usable UI path.
6. Run the frontend type, lint, build, and visual gates.

Keep business logic in a focused module such as `vendorops.py` or a sibling delivery module. Routes should authenticate, validate the request shape, call the service, and map domain errors to HTTP responses.

## Delivery model and file rules

Lead files and call recordings are delivery objects, not chat messages or ordinary prompt sources. Store durable metadata in the database and bytes in managed file or object storage.

A minimal delivery has one active assignment, one lead file, zero or more recordings, a vendor note, a processing status, and an event history. Record assignment, client, optional ticket, kind, original name, safe storage key, byte size, media type, checksum, uploader, status, and timestamps. Do not put raw bytes or extracted lead content in audit events.

Use this state machine:

```text
uploading -> received -> validating -> needs_review -> ready -> delivered
                      \-> failed
            \-> rejected
```

`received` proves the bytes and checksum exist, not that the file is safe. `ready` means the exact recipient, body, and attachment set passed validation. `delivered` requires read-back evidence from the outbound provider.

- Sanitize the original name, generate the storage key server-side, and reject path traversal.
- Do not trust the browser's MIME type or filename extension as proof of content.
- Check assignment scope before accepting any bytes.
- Never use `await request.body()` or a database binary column for large recordings. Stream small lead files with a hard byte cap. Use a presigned direct upload for large audio or video.
- Quarantine new objects until validation succeeds. Failed validation must not leave an apparently deliverable row.
- Make retries idempotent with a client-supplied upload id or a checksum plus assignment identity.
- Use temporary directory storage in tests and a settings-selected managed storage adapter in production.

## Automation boundary

Automate the queue around the portal, not inside a single request:

1. Ingest from a vendor upload or a mailbox provider into the same delivery record.
2. Apply deterministic sender, assignment, file, duplicate, and required-field rules first.
3. Use a model only for bounded classification or structured extraction. Require schema-valid JSON and retain the source evidence.
4. Format client workbooks and filenames with deterministic code and versioned client profiles.
5. Validate recipient, required fields, appointment status, workbook metadata, vendor leakage, duplicates, and recording availability.
6. Create a reviewable draft or `ready` item. Start with human approval; automatic send is a later policy decision backed by observed accuracy.
7. Write every state transition and refusal to the audit spine without copying sensitive source content into error messages.

Laya can be an optional classifier over a small derived state. It is not the mailbox reader, attachment store, formatter, sender, or authorization layer. A classifier score cannot invent an assignment, choose an unconfigured recipient, or bypass a missing field. The first release must work without model fine-tuning.

For mailbox ingestion, portal uploads and mailbox messages should converge on one contract:

```text
source reference + assignment candidate + files + note -> delivery queue
```

The portal supplies an authenticated assignment. Mailbox ingestion must resolve sender and client through configured vendor rules and stop in `needs_review` when resolution is ambiguous.

## Keep authentication planes separate

Verify each credential plane independently and report them separately:

- An interactive Hermes Microsoft 365 connector proves the current agent session can access a mailbox.
- The workspace mailbox poller uses its own production credentials and configuration.
- An unattended Graph poller normally uses application permissions with admin consent. Delegated `offline_access` belongs to an interactive user flow, not a headless daemon by default.

Never infer that the deployed product is configured because an MCP connector is authenticated, or that the connector is broken because the product lacks Graph credentials. Check provider parity too: IMAP attachment support does not prove the Graph or webhook provider downloads attachments. Listing Graph messages without fetching `/attachments` is only partial ingestion.

For outbound delivery, persist the provider message id and read back the draft or sent item before transitioning to `delivered`.

## UI rules

Use the existing `DESIGN.md` and the current dark operational shell. Do not generate a second design language for one feature.

- Put delivery upload and status in the assigned-client context so scope is visible before a file is selected.
- Show separate lead-file and recording affordances, accepted formats, maximum size, progress, retry, and the resulting processing state.
- Preserve keyboard access, visible labels, 44px touch targets, focus states, and mobile stacking.
- Display operational states such as `uploading`, `received`, `validating`, `needs_review`, `ready`, `delivered`, and `failed`; never collapse them into a generic success message.
- Reuse existing tokens and API error patterns. Add visual emphasis through hierarchy and status fill, not decorative card stripes or a new palette.

## Verification and shipping

From `backend/`, run the focused test first and then:

```bash
python -m pytest tests/ -q
```

From `frontend/`, run the scripts present in `package.json`, including lint and production build. Render `/vendor` with an assigned vendor at desktop and mobile widths, exercise an upload, inspect browser console output, and verify failure, empty, progress, success, and retry states.

Work on a `feat/...` branch. Do not commit, push, or open a PR unless Deep asks. If API behavior changes, update the repository's API and deployment documentation in the same change.

## Pitfalls

- Do not use the Champbeam skill or `/Users/deep/Apps&Projects/ChampUTM`; that is a different product.
- Do not call the vendor portal missing merely because upload is missing; authentication, assignment scoping, threads, and approved-work reads already exist, so a replacement would duplicate security-critical behavior.
- Do not reuse the small source upload path for large audio or video; it buffers the whole request and can exhaust the worker.
- Do not route every mailbox message through an LLM; deterministic filtering avoids cost, latency, and model authorization mistakes.
- Do not report a successful send from a created draft, queued row, or successful API call alone; read back the exact dispatch or sent state.
