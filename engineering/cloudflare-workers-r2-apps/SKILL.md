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

## Static SPA plus one API route (the Workers + Assets shape)

For a built frontend (Vite) with a small API: `wrangler.jsonc` sets `main` to the worker, `assets.directory` at `./app/dist` with `binding: ASSETS` and `not_found_handling: "single-page-application"`, plus `run_worker_first: ["/api/*"]` so only API paths hit the worker and everything else falls through to `env.ASSETS.fetch(request)`. One deploy serves both; no Pages project needed.

- Local dev: `vite.config.ts` proxies `/api` to `http://localhost:8787` and wrangler dev runs from the repo root in a second terminal; if that stalls, the UI path that never calls the API still ships and can be tested.
- Deploy proof: the hash check in `verification-gate-integrity` (served index hash vs local dist, then grep the served bundle for a feature string added this round).
- `wrangler deploy` writes `.wrangler/cache/`, so gitignore `.wrangler/` or the first commit carries junk.

## Pitfalls (each one was a real failed run)
- **R2 `get(key, { range: request.headers })` sets `obj.range` even when no Range header was sent.** Only answer 206 when `request.headers.has('range')`, or every full request comes back partial. Default `offset` to 0 and `length` to `size - offset` (suffix ranges).
- **`wrangler deploy` intermittently fails with `Received a malformed response from the API`.** Transient: sleep 5 and rerun. Always grep the deploy output for `Deployed` before running tests, or the gate runs against the previous build.
- **workers.dev returns 403 to Python `urllib` default User-Agent.** Set a custom `user-agent` header. Node `fetch` and curl are fine.
- **Never keep a collection in one KV JSON document.** Two concurrent writers (admin edit + create) read-modify-write and one loses its change silently. One key per record (`screen:<id>`) and `list({prefix})` to enumerate.
- **KV `get` can return a 1 to 2s stale read right after `put`.** A UI that refetches after save shows the old state. Apply the PUT response locally, stamp records with `updated`, and keep the local copy when it is newer than what a refetch returns.
- **KV `list()` is eventually consistent (up to 60s)** even in the same request path. Any test that writes then lists needs a bounded retry; any online indicator built on list metadata needs a window of at least 90s.
- Wrangler OAuth token may lack `k2.*` scopes; `wrangler kv namespace create` still works, the warning is noise.
- Uploads streamed through the Worker cap at the plan request limit (100 MB free, 500 MB paid). Past that, use R2 presigned PUT.
- **A fetch-proxy route must ship its paste fallback before it ships.** Retailers and big consumer sites return 403/404/429 to a Worker's server-side fetch regardless of the user-agent, so a URL-classify feature that only works on bot-tolerant sites looks broken on exactly the prospects Deep will paste first. Build the "paste their copy instead" path in the same commit, and let the API error (with the real status code) auto-open it with a one-line hint naming the block. Add an SSRF allowlist before any customer self-serve; a demo-level proxy that fetches any caller-supplied URL is fine only while the URL is unlisted, and say so in a code comment and the report.

## Containers + D1 (reference: `~/repos/ChampHarbinger-cf`, `deploy/cloudflare/`)
- **Containers cannot hold a D1 binding.** Point the app's DB client at a fake host (`http://d1.internal`) and serve it from the Worker with `outboundByHost`, running each statement on `env.DB`. No public DB endpoint, no DB credential in the image.
- **`outboundByHost` needs `export { ContainerProxy } from "@cloudflare/containers"` in the entrypoint and a current `compatibility_date`.** Without them every container request 500s with `ctx.exports is undefined`.
- **Assign `MyContainer.outboundByHost = {...}` after the class; never a `static outboundByHost =` field.** The library registers handlers in a static setter; a class field (define semantics) shadows it, so interception turns on with an empty registry and the host falls through to public DNS as a 530. Tell: tail shows `ContainerProxy` answering 530, not its own 520.
- **A secret change does not recreate the Durable Object, and `envVars` only apply at container start.** A container pinged by cron never idles out, so new keys never arrive. Have the Worker (which always sees current secrets) RPC its env to the container once per isolate per fingerprint; the container stores the fingerprint `onStart` and calls `destroy()` on mismatch. Verify by `secret put` then `secret delete` and watching the running app's config both ways. `wrangler secret delete` has no `--force`: pipe `yes`.
- Apply D1 migrations in the deploy script before `wrangler deploy`, never at container boot. `--secrets-file` is additive, so a redeploy never wipes keys added later.
- Never `set -a; . env.env` in a persistent terminal: later test runs inherit the secrets and fail on leaked env. Source it inside `bash -c` only.

## Verification pattern
- Smoke test as `test/smoke.mjs` taking `BASE` and `ADMIN_TOKEN` env, run against the deployed URL, asserting status codes, byte round-trip and a 206 range.
- Browser gate with Playwright against the live URL, driving the signed-in state before auditing (visual-verify's `audit.py` cannot inject localStorage; import its `PROBE` and run it after login).
- Launch Chromium with `--autoplay-policy=no-user-gesture-required` to prove `<video>.currentTime` advances.
