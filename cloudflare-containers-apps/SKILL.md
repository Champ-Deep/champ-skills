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

## Deploy failures that are config, not code

- **A CI build that reaches `wrangler deploy` and dies there is a config
  mismatch, not a build problem.** The `account_id` in `wrangler.jsonc` must
  equal the account the build actually runs under; confirm with
  `npx wrangler whoami`, which prints the logged-in email, account name and
  account ID, before editing anything. A stale account ID fails only at
  deploy time, after the image build has already succeeded.
- **A mismatched Worker `name` in config is a warning, not the failure**, but
  fix it anyway or Cloudflare opens an automated PR against the repo that
  changes the config for you. Rename in the config and in the deploy docs in
  the same commit.
- **A one-line body like `This deployment is not configured yet.` is a
  deliberate fail-closed check.** Grep the Worker source for that exact
  string to find the list of required secrets it enforces, then set those
  secrets rather than debugging the route. Repo code refuses to boot with a
  demo secret published in the source, so the fix is always new secrets, not
  a code change.
- **Set a secret without ever printing it: generate the value, pipe it on
  stdin.** `printf '%s' "$VAL" | npx wrangler secret put NAME` keeps it out of
  argv, shell history and the transcript. When a human needs the value later
  (a lab password), write it once to a `umask 077` file outside the repo and
  hand over the path, not the value. A random secret nobody can read is a
  lockout: save it somewhere retrievable at set time.
- **Prove the fix on the live URL, not on the CLI exit code.** Probe the
  health route, the protected route both without credentials (expect 401) and
  with them (expect 200), and the discovery endpoint (`/.well-known/...`), in
  one batch of curls. An unauthenticated 401 beside an authenticated 200 is
  the shortest proof that secrets took effect and the guard is behaving.

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

## Container lifecycle pitfalls

- **PID 1 ignores SIGTERM unless the process installs a handler.** `stop()` and `sleepAfter` both send SIGTERM, so a plain Python or Node server never dies and keeps billing until the kill grace period ends (minutes). Install a SIGTERM handler (flush state, then `os._exit(0)`) in the final process, including any 503 fallback server. Prove it with a stop and a timed cold start, not by the `stop()` return value.
- Any request, even a polled 503, renews `sleepAfter`. Do not poll a broken container to wait it out.
- First deploy of a container application can answer "no Container instance available" for a few minutes while it provisions. Retry before debugging.
- A Worker secret change or a new image does not replace a running instance until it stops. Add a token-guarded `/__state/stop` route to force a restart and to time cold starts.
- Pass secrets into the container through `envVars` set in the Container subclass constructor from `env`; forward by name prefix so new settings need no Worker change.
- Keep snapshot integrity metadata on the same R2 object (`customMetadata`, 2 KB cap) so a crash between two uploads cannot leave a blob and its checksum out of step.

## Cutover from an external origin (Railway, a VM)

- **A flip made with `wrangler deploy --var MODE:container` lasts until the next plain `wrangler deploy`**, which reads the toml default and silently sends traffic back to the old origin. Writes then split between the R2 snapshot and the origin, and the next flip restores a snapshot that lacks the origin's writes. In the switch runbook, commit the new mode in `wrangler.toml` and deploy from that commit; keep `--var` for the rollback only.
- **Copy the origin's database last.** Create buckets, deploy the container application (image build takes minutes) and set secrets first; then copy, seed, verify the seeded object's sha256 and switch back to back, so the lost-write window is minutes, not the whole runbook. Copy a live WAL-mode SQLite with the backup API (`sqlite3 src ".backup /tmp/x.db"` or `Connection.backup`), not `tar` of the volume.
- **Take the env var list from the origin itself, names only** (`railway variables --kv | cut -d= -f1`, never values), not from the repo docs. A doc-derived list drops mode flags (for example `SPAN_CARDS_ONLY=1`) that change what clients see, and the container boots without them.
- **Rehearse on staging with the origin's plain settings** (mode flags like cards-only), or the proof covers a different app: Span Agent's MCP tool list is 8 normally and 4 in cards-only mode, and its DEPLOY.md says 6. Assert on what the real mode returns, not on a doc number.
- Pulling a live SQLite from Railway needs no extra tool: `railway ssh -- sh -c 'python3 -c "...Connection.backup..." && base64 /tmp/x.db; rm -f /tmp/x.db' | base64 -d > x.db`, then `integrity_check` locally. The container re-snapshots after its first request, so the R2 object's sha256 changes after the switch; verify the sha before switching and counts after.
- Re-read real data after the switch (an admin count against the snapshot manifest), not only `/healthz` and 401s: health answers the same from an empty seed.

## Cost guardrails

Containers bill for provisioned resources whether or not they serve traffic, so an always-on container is the largest line item a Workers account carries.

1. **Set `sleepAfter` on every container that is not genuinely constant-traffic**, and size each app at the smallest instance it needs (`max_instances: 1` unless concurrency demands otherwise). A config with three large instances and no sleep timer is the shape that produces an unexpectedly large bill, and it is a config fix, not a code fix.
2. **Tear preview and staging containers down when their PR merges.** A preview that outlives its branch bills continuously and, by default, shares production's bindings.
3. **Read the bill as a computed estimate when the API refuses it**: count running instances, multiply provisioned memory and disk by hours, label the number `estimated`. Method, rates and the three delete-set categories live in the `decommission-readiness-audit` skill under `references/cloudflare-cost-audit.md`.
4. **Find orphans before blaming live code for a spike.** A container or durable object namespace whose owning script no longer exists keeps running until it is deleted. Join container instances and DO namespaces against the current worker list, and treat any entry with no script as deletable.
5. **A `last_updated`-only health check never times out.** A DO namespace object with no `expires` is pinned for the life of the namespace, so it counts as running around the clock whether or not requests arrive.

## Verification before reporting a deploy as done

1. `curl` an unauthenticated endpoint and an authenticated one on the live
   URL, and report both statuses.
2. Trigger the state path once (create a row, then restart or re-read) and
   show it survived.
3. Confirm the secret the new code needs is listed on the Worker **and** that
   the container restarted after it was set.
