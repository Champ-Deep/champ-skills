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

## A real key is already on this machine, and the mock is the real risk

`$HOME/.hermes/.env` holds a working `OPENROUTER_API_KEY`. Copy it into
`backend/.env` before concluding that "no LLM call has ever run" (G7 in
AUDIT.md) is still true. Verified 2026-10-01: real runs serve on
`deepseek/deepseek-v4.1-flash` and `z-ai/glm-5.3-flash` through
`openrouter/auto`.

Two traps that cost real time, both worth checking before debugging the app:

- **A stale `OPENROUTER_API_KEY` in the Hermes runtime env silently wins.**
  `app/__init__.py` deliberately never overwrites a real environment variable,
  so a server launched from this agent inherits the runtime's key, not
  `backend/.env`. Symptom: health says `OpenRouter HTTP 401` and a direct
  `httpx` call with the `backend/.env` key returns 200. Compare with
  `ps eww -p <pid>` (hash the value, never print it). Fix: start the server
  with `env -u OPENROUTER_API_KEY ...`.
- **Port 3000 is OrbStack, not the workspace.** Something else on this machine
  already serves 3000, and it answers 200, so a naive curl check passes while
  you screenshot a completely different application. Use 3100, and confirm
  `document.title` before trusting any visual result. `npx next dev` also
  pulls a *different* Next major than the installed one; run
  `node node_modules/next/dist/bin/next dev` instead.

**Lost `node_modules/.bin` and `.venv` mid-session, with disk at 47 GB free.**
Both had their packages present and only the executables missing. `npm install`
is unnecessary: recreate the shims (`ln -sf ../next/dist/bin/next
node_modules/.bin/next`, same for `../typescript/bin/tsc`) and
`python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r
requirements-dev.txt`. Check whether the packages still exist before assuming
you must reinstall.

## Only a real run finds the bugs 1,055 green tests cannot

Mock LLM responses are well-formed. Real ones are not. Two failures in the
first live ticket, both invisible to the suite:

- `llm.chat` returned `content: null` (OpenRouter does this for
  reasoning-only and token-capped responses), and the first thing most callers
  do is `text.strip()`, so it surfaced as `'NoneType' object has no attribute
  'strip'` three frames from the HTTP payload that said null. Fixed once in
  `llm._content_of` for both `chat` and `chat_messages`, with
  `tests/test_llm_content_none.py` pinning it.
- Ad creatives crashed the whole design stage on that null, so the ticket
  never reached Gate 2. After the fix a full run produced 8 artifacts (plan,
  3 newsletters, 3 ad creatives, canvas) and stopped at Gate 2 correctly.

Rule: a green suite proves the mock world works. Only a real run proves the
product works. Run one end to end before calling anything done.

## Verify by pressing the buttons, not by calling the functions

Four real defects shipped green through the module-level suite and were found in
one pass by driving the loop over HTTP the way a person would. All four needed a
*request sequence* rather than a function call, which is exactly what a unit test
does not supply:

1. `llm.chat` refuses in mock mode unless the CALLER supplies a `mock=`.
   A new agent that omits it is not degraded, it is dead, and every test that
   stubs `llm.chat` hides that. Pass one, following the convention in
   `app/agents/*`.
2. A `as_dict()` that forgets a field is invisible until the moment somebody
   needs it. `provider_message_id` was omitted, so "the client says they never
   got it" had no answer.
3. An integration missing from `/api/health` looks identical to one that has
   not tried. This is what `mailbox.provider_status()` exists to prevent; apply it
   to every new integration.
4. Two lanes that enforce the same rule will drift. The vendor draft refused to
   run without citations and the client draft did not, so a client message could
   be built from nothing behind a guard that was protecting nothing.

Method that worked: write a script that plays the role (health, ingest, brief,
draft, approve, send, passback, record, review), run it against a real server,
then run the abuse cases where every call *should* fail. Then render the page in
headless Chrome and measure the DOM for overflow, clipping, and empty state
tiles. A 200 with the right HTML shell proves nothing; the data arrives
client-side.

## Pixel office: the layout trap that hides every fix

The office already animates properly (a 140 ms master clock in `useAnimationClock`,
real walk cycles, and seats derived in `backend/app/office.py` from the same rows
the Kanban reads). When a change to it "does nothing", check render order before
touching motion.

`app/page.tsx` used to render InFlightStrip, NeedsYou, WorkloadStrip and
LatestAssets BEFORE `{view === "office" && <PixelOffice .../>}`. The office
therefore sat below the fold and got cropped by the viewport, and a screenshot of
it looked "static" when the floor was animating correctly all along.

The office answers "what is happening right now", so it renders above the
obligation strips, and the view switcher travels with it: a switcher placed below
the view it controls is its own bug. When you change the ordering, move the
`<div className="mb-4 flex flex-wrap items-center gap-3">` switcher block too.

Three aliveness defects worth knowing, all fixed 2026-10-01:

1. Idle agents were placed by array index into fixed `IDLE_SPOTS` and never
   reassigned, so the lounge stood still for a whole session. The fix is an epoch
   state bumped every `WANDER_MS` (9 s) plus a DETERMINISTIC shuffle,
   `shuffled(spots, epoch)`. Never `Math.random`: the 6 s poll would reshuffle
   the room and bodies would teleport mid-walk.
2. A crashed run empties every seat, so a `failed_designing` ticket reads as a
   quiet day. `office.py` now also queries `PipelineTask.status == "failed"` and
   seats those agents with `failed: True`, drawn as a full red STUCK bar. A red
   outline on an empty track reads as "no data", not "stopped".
3. Per-agent progress comes from `_agent_progress()`, which credits an agent only
   for ITS OWN artifact kind through `AGENT_KIND`. Do not count artifacts per
   ticket: a revision re-runs a stage, so counting rows reports three newsletters
   where one current newsletter exists.

Seat overflow used to add a constant x bump, which dropped the third body on the
same tile as a seat three rows further along. That is how two identical sprites
ended up standing on each other. Overflow rows now step back into the room
(`x - overflow * 16`, `y + overflow * 30`), and each working sprite carries a
name plate lifted by `tier * 15` so plates at one station stack instead of
overlapping.

SVG gotcha that cost a round trip: a CSS `transform` on the same element as an SVG
`transform` ATTRIBUTE wins and discards the attribute. `AgentPlate` nests an outer
animated group around an inner translated group for exactly this reason.

## Pitfalls

- Do not use the Champbeam skill or `/Users/deep/Apps&Projects/ChampUTM`; that is a different product.
- Do not call the vendor portal missing merely because upload is missing; authentication, assignment scoping, threads, and approved-work reads already exist, so a replacement would duplicate security-critical behavior.
- Do not reuse the small source upload path for large audio or video; it buffers the whole request and can exhaust the worker.
- Do not route every mailbox message through an LLM; deterministic filtering avoids cost, latency, and model authorization mistakes.
- Do not report a successful send from a created draft, queued row, or successful API call alone; read back the exact dispatch or sent state.
