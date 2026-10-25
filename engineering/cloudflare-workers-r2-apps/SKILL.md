---
name: cloudflare-workers-r2-apps
description: Use when building a Cloudflare Worker with R2 or KV.
---

# Cloudflare Workers + R2 + KV apps

Reference build: `~/repos/ChampCast` (Worker + R2 media + KV state + static admin and player pages, zero build step).

## Layout that needs no bundler
- `wrangler.jsonc` with `main: src/worker.js`, `assets: { directory: ./public, binding: ASSETS }`, `r2_buckets`, `kv_namespaces`.
- Worker handles `/api/*` and byte routes; everything else falls through to `env.ASSETS.fetch(request)`. `/tv` serves `public/tv.html` automatically.
- Secrets: `printf '%s' "$TOK" | npx wrangler secret put NAME`; mirror into `.dev.vars` (gitignored) for `wrangler dev` and tests.

## Pitfalls (each one was a real failed run)
- **R2 `get(key, { range: request.headers })` sets `obj.range` even when no Range header was sent.** Only answer 206 when `request.headers.has('range')`, or every full request comes back partial. Default `offset` to 0 and `length` to `size - offset` (suffix ranges).
- **`wrangler deploy` intermittently fails with `Received a malformed response from the API`.** Transient: sleep 5 and rerun. Always grep the deploy output for `Deployed` before running tests, or the gate runs against the previous build.
- **workers.dev returns 403 to Python `urllib` default User-Agent.** Set a custom `user-agent` header. Node `fetch` and curl are fine.
- **Never keep a collection in one KV JSON document.** Two concurrent writers (admin edit + create) read-modify-write and one loses its change silently. One key per record (`screen:<id>`) and `list({prefix})` to enumerate.
- **KV `get` can return a 1 to 2s stale read right after `put`.** A UI that refetches after save shows the old state. Apply the PUT response locally, stamp records with `updated`, and keep the local copy when it is newer than what a refetch returns.
- **KV `list()` is eventually consistent (up to 60s)** even in the same request path. Any test that writes then lists needs a bounded retry; any online indicator built on list metadata needs a window of at least 90s.
- Wrangler OAuth token may lack `k2.*` scopes; `wrangler kv namespace create` still works, the warning is noise.
- Uploads streamed through the Worker cap at the plan request limit (100 MB free, 500 MB paid). Past that, use R2 presigned PUT.

## Verification pattern
- Smoke test as `test/smoke.mjs` taking `BASE` and `ADMIN_TOKEN` env, run against the deployed URL, asserting status codes, byte round-trip and a 206 range.
- Browser gate with Playwright against the live URL, driving the signed-in state before auditing (visual-verify's `audit.py` cannot inject localStorage; import its `PROBE` and run it after login).
- Launch Chromium with `--autoplay-policy=no-user-gesture-required` to prove `<video>.currentTime` advances.
