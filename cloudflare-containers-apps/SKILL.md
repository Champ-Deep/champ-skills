---
name: cloudflare-containers-apps
description: Use when deploying to a Cloudflare Container App or Worker.
version: 1.0.0
author: Champ
platforms: [macos]
metadata:
  hermes:
    tags: [cloudflare, containers, deploy, worker]
---

# Cloudflare Containers and Workers

Procedural notes for running a long-lived service (a FastAPI API, a job
container) behind a Worker on Cloudflare, and for reading the state it keeps.

## Deploy

1. Write config in the repo, never only in the dashboard: `wrangler.toml` (or
   `.jsonc`) with the container block, the Worker routes, and `secrets_store`
   bindings for anything sensitive. A deploy that only set a secret in the
   dashboard does not exist in the repo, so it cannot be reviewed or rebuilt.
2. `wrangler deploy` for code and config; `wrangler secret put <NAME>` for
   values (they are never printed back, and never read out of a file into
   chat). Bulk-check what a Worker has with `wrangler secret list`.
3. **A secret change needs a container restart to take effect.** The running
   process read its env at boot; bumping an image tag or forcing a redeploy is
   how you flush it. After any secret change, verify by calling an endpoint
   that reads the new value, not by seeing the name in `secret list`.
4. **A 5xx can hide inside a 200.** Some fetch wrappers return 200 with an
   `error` payload instead of raising the status, so a failed downstream call
   looks like a successful one at the only place that checks. Log and assert on
   the response body's error field and on the inner status, and prefer failing
   loudly at the boundary. This is the same class of bug as an auth verifier
   returning a token object for a rejected call: treat "200 with an error body"
   as a defect in the caller, not an acceptable shape.
5. **Default HTTP clients get blocked by Cloudflare.** `urllib.request` sends a
   `Python-urllib/3.x` user agent and is refused on many endpoints even with
   correct auth, which reads as a 403 auth failure. Set a normal
   `User-Agent: <YourApp>/<version>` header on any server-side fetch.

## State and backups

- Persist anything a container loses on restart (workspaces, API keys, report
  rows) into object storage (R2) on a schedule: upload after writes, restore on
  boot.
- **A restore must never overwrite good state with garbage.** Validate the
  downloaded blob (non-empty, parses, row count sane) before it replaces the
  local file, and on a failed restore keep the existing copy and log. A
  corrupted download that overwrites the working backup destroys the only copy
  the recovery path had.
- Check the backup actually lands: read the object list (or `wrangler r2 object
  get` metadata) after the first upload rather than trusting the upload's exit
  code.

## Private app and durable-write boundaries

- Keep container backup/restore callbacks reachable without a human Access session. Use a separate private state Worker, a scoped service path or a properly configured machine policy; protecting every callback behind browser OTP breaks cold-start restore. Require machine authentication, keep the bucket private and expose no account data on health routes.
- Persist a consistent SQLite backup before acknowledging successful hosted mutations. A periodic best-effort upload can lose changes the UI already called saved. Keep a dirty flag after upload failure, retry before later success and validate downloaded SQLite integrity, schema and relationships before installing it. `with sqlite3.connect(...)` commits but does not close the connection: use explicit close or `contextlib.closing` for snapshot connections.
- Read back deployed HTML, JavaScript and CSS and compare their hashes with the final source. A successful image rollout does not prove an already-running container has changed. Verify an actual stop/start, stored mutation survival and restoration of the test mutation. Record any first-request transient separately instead of hiding it behind a later successful retry.
- Use the approved Cloudflare connector for Access policy changes when Wrangler OAuth lacks those scopes. Never extract tokens from Wrangler credential files or silently grant broad access. If a generated MCP `get` schema contains identical string alternatives in `oneOf`, use an exact-filtered list endpoint for readback rather than changing permissions or guessing another identifier.

## Verification before reporting a deploy as done

1. `curl` an unauthenticated endpoint and an authenticated one on the live
   URL, and report both statuses.
2. Trigger the state path once (create a row, then restart or re-read) and
   show it survived.
3. Confirm the secret the new code needs is listed on the Worker **and** that
   the container restarted after it was set.
