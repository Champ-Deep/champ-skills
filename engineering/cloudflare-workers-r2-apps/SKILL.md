---
name: cloudflare-workers-r2-apps
description: "Use when building a Cloudflare Worker with R2, KV, Durable Objects, WebSockets, assets, or outbound email from a Worker."
---

# Cloudflare Workers + R2 + KV apps

> **Security gate (mandatory):** every deploy runs `ultimate-security`'s deploy gate (pre-push hook, `predeploy`, or publish.sh) plus a `security-audit` guidance-mode review of the diff. A bare CLI deploy runs `python3 ~/champ-skills/security/ultimate-security/scripts/deploy_gate.py check .` first. `AUDIT-REQUIRED` means a full Cloudflare audit before shipping. Never override without Deep.

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

## Server-authoritative rooms (Durable Objects + WebSockets)

One DO per room (or per session) behind a WebSocket upgrade route, so state, the
clock and per-connection filtering live on the server and the browser only renders
what the server sends. Shape:

- `wrangler.jsonc` declares the DO binding; HTTP endpoints answer `POST /api/...`
  for create/join and the same path with `?id=` upgrades. Identity is whatever the
  socket carries (`crypto.randomUUID()` kept in sessionStorage), bound to the socket
  at connect; host controls require the host's key, everything else is refused for
  the wrong socket.
- The server owns timers and runs any AI/bot logic; clients never send ticks. Send
  each client only its own view (`{view, now, speed, host, debug}`), and let
  `spriteUrl`-style asset reads fall through to `env.ASSETS`.
- Local dev is `wrangler dev` on a fixed port plus the frontend proxying `/api`
  with `ws: true`.

**Deploy the server before the lane that builds its UI, with a holding page in
place.** Deep asks for the link, so put a real URL out first: a one-screen
`index.html` saying the server is live and the screens are being built. Then edit
the running lane's brief to deploy over it and pin the same URL as its preview.
Say plainly in the report that an unreviewed build will be publicly visible for
the window between the lane's deploy and your review, and never report the link
as finished while it serves the holding page.

## Sending email from a Worker (Cloudflare Email Service)

- Zone, DNS and sending-domain work goes through the connected Cloudflare MCP connector, not an API token: check its status first, and when it is connected use its zone / records / sending tools, which create records server-side. Ask Deep for an API token only when the connector is not connected.
- Onboard the sending domain before writing code: create the sending subdomain on the zone, then read the DNS status endpoint and require `ready` (it lists the MX, SPF and DKIM records Cloudflare made for you).
- **Onboarding a sending domain can set a domain-wide DMARC `p=reject`, which governs every sender on that domain, not just this Worker.** Check for other systems sending mail as that domain first, or their mail starts bouncing and nobody will connect it to a Worker deploy.
- Wire it as `"send_email": [{ "name": "EMAIL" }]` and feature-gate on the binding's presence (`env.EMAIL ? ... : undefined`), so a build without it disables the mail path cleanly instead of half-working. Confirm the binding in the deploy output's binding list for the environment you actually targeted; never assume a top-level binding reached an overlay environment. Types ship with `@cloudflare/workers-types` (`SendEmail.send(message)` or `send(builder)`).
- Wrap the send in try/catch and log it: mail failure must not fail the request that triggered it (a reset or invite still returns 200).
- A 200 from the endpoint plus the token row in the database proves the request path ran; only the recipient seeing the message proves delivery, and mail to enterprise addresses can land in junk. Report which of the two you hold.

## Pitfalls (each one was a real failed run)
- **A local `wrangler dev` missing a secret the deployment has reports the feature as unconfigured, which reads as a code bug.** After adding any secret, mirror it into `.dev.vars`, then compare the config or health endpoint of the local run against the deployed URL field by field: both must report the same `*_configured` flags before you debug code. Start `wrangler dev` as a tracked background process on a fixed port and stop it by name afterwards (`pkill -f "wrangler dev"` plus a port check), or a stale server keeps answering probes and later tests run against the previous build.
- **R2 `get(key, { range: request.headers })` sets `obj.range` even when no Range header was sent.** Only answer 206 when `request.headers.has('range')`, or every full request comes back partial. Default `offset` to 0 and `length` to `size - offset` (suffix ranges).
- **`wrangler deploy` intermittently fails with `Received a malformed response from the API`.** Transient: sleep 5 and rerun. Always grep the deploy output for `Deployed` before running tests, or the gate runs against the previous build.
- **workers.dev returns 403 to Python's default User-Agent** — `urllib`, and every client layered on it (`requests`, httpx defaults). Set a custom `user-agent` header on the probe. Node `fetch` and curl are fine, so one Python 403 beside a curl 200 is a client signal, not an outage.
- **Never keep a collection in one KV JSON document.** Two concurrent writers (admin edit + create) read-modify-write and one loses its change silently. One key per record (`screen:<id>`) and `list({prefix})` to enumerate.
- **KV `get` can return a 1 to 2s stale read right after `put`.** A UI that refetches after save shows the old state. Apply the PUT response locally, stamp records with `updated`, and keep the local copy when it is newer than what a refetch returns.
- **KV `list()` is eventually consistent (up to 60s)** even in the same request path. Any test that writes then lists needs a bounded retry; any online indicator built on list metadata needs a window of at least 90s.
- Wrangler OAuth token may lack `k2.*` scopes; `wrangler kv namespace create` still works, the warning is noise.
- Uploads streamed through the Worker cap at the plan request limit (100 MB free, 500 MB paid). Past that, use R2 presigned PUT.
- **A WebSocket upgrade route cannot be probed with curl or a bare `fetch`.** Node's
  fetch refuses to send an `upgrade` header, so a status-code probe of a `?id=` or
  `?ws=` route proves nothing about the upgrade. Drive a real client (browser
  WebSocket, `ws` package) and assert the first message; keep the HTTP probe only for
  the plain routes.
- **A game or session smoke test must play a whole session over the public URL,**
  through the same socket the real client uses, not just hit the create endpoint.
  Take `BASE` from env so one script runs against `wrangler dev` locally and against
  the deployed worker, print the outcome (codes, participants, winner) so the report
  carries real numbers, and include a hidden-information case: the surface that must
  not see secrets (TV, other players) is where a leak would land.
- **A contract edit does not reach a running lane.** Workers read their card body at
  spawn, so changing the transport or endpoints mid-build needs the
  reclaim -> resume-comment -> dispatch sequence in model-routing; a comment alone
  waits for the next run.
- **Confirm config and secrets on the live endpoint, never from the command's exit status.** Editing `vars` in `wrangler.jsonc` changes nothing until the next `wrangler deploy`, and a secret uploaded with an empty value reports success and still shows its name in `env_keys`, so read the health or debug flags (`*_configured`) after the deploy and treat a false flag as an unfinished deploy rather than a code bug. A value piped into `secret put` from an unset shell variable is exactly that empty upload.
- **A fetch-proxy route must ship its paste fallback before it ships.** Retailers and big consumer sites return 403/404/429 to a Worker's server-side fetch regardless of the user-agent, so a URL-classify feature that only works on bot-tolerant sites looks broken on exactly the prospects Deep will paste first. Build the "paste their copy instead" path in the same commit, and let the API error (with the real status code) auto-open it with a one-line hint naming the block. Add an SSRF allowlist before any customer self-serve; a demo-level proxy that fetches any caller-supplied URL is fine only while the URL is unlisted, and say so in a code comment and the report.

## Containers + D1 (reference: `~/repos/ChampHarbinger-cf`, `deploy/cloudflare/`)
- **Containers cannot hold a D1 binding.** Point the app's DB client at a fake host (`http://d1.internal`) and serve it from the Worker with `outboundByHost`, running each statement on `env.DB`. No public DB endpoint, no DB credential in the image.
- **`outboundByHost` needs `export { ContainerProxy } from "@cloudflare/containers"` in the entrypoint and a current `compatibility_date`.** Without them every container request 500s with `ctx.exports is undefined`.
- **Assign `MyContainer.outboundByHost = {...}` after the class; never a `static outboundByHost =` field.** The library registers handlers in a static setter; a class field (define semantics) shadows it, so interception turns on with an empty registry and the host falls through to public DNS as a 530. Tell: tail shows `ContainerProxy` answering 530, not its own 520.
- **A secret change does not recreate the Durable Object, and `envVars` only apply at container start.** A container pinged by cron never idles out, so new keys never arrive. Have the Worker (which always sees current secrets) RPC its env to the container once per isolate per fingerprint; the container stores the fingerprint `onStart` and calls `destroy()` on mismatch. Verify by `secret put` then `secret delete` and watching the running app's config both ways. `wrangler secret delete` has no `--force`: pipe `yes`.
- Apply D1 migrations in the deploy script before `wrangler deploy`, never at container boot. `--secrets-file` is additive, so a redeploy never wipes keys added later.
- Never `set -a; . env.env` in a persistent terminal: later test runs inherit the secrets and fail on leaked env. Source it inside `bash -c` only.

## Containers: one codebase shipped as N brand editions
Shape for publishing a single authenticated app as several branded sites on one
account. Verified end to end: four editions (two brands, two data variants) deployed,
each passing a 9-point smoke test, with a live A/B of two data structures on one link.

- **One router Worker per edition, and the container is reached only through it.**
  The brand URL is `qc-<brand>.<account>.workers.dev`; the Worker forwards `fetch()`
  to that edition's container. One Worker per brand keeps host-based routing in
  config rather than in if-branches shared by every brand.
- **The router must strip the scheme before forwarding to the container.** The
  library downgrades `https://` for the fetch it makes, but the `request.url` it
  passes along still carries `https://`, and the container only speaks plain http
  inside Cloudflare. The container answers 500 for every request, the rollout
  reports healthy, and the first health poll times out: the failure surfaces as
  "the deploy never came up", not as a URL bug. Forward `url.pathname + url.search`
  (or `new Request` on a downgraded URL), never the raw `request.url`.
- **One container and one database name per edition, one cluster.** Two public
  brands sharing a database leak each other's rows across domains the moment either
  uploads, and a "wipe on deploy" then wipes both. Fresh-deploy-empty is the
  default: seed data after the smoke test passes, never before, so an empty catalog
  is distinguishable from a broken one. MongoDB embedded in the container (one
  `mongod --dbpath` per container) is enough when the seed files ship in the image.
- **Admin credentials generated at deploy, held in the OS keychain, echoed as the
  keychain entry name only.** The report names the entry, never the value. Passwords
  with secure cookies mean the smoke script must log in through the router, not
  through the container port.
- **A frontend container is not a public route on its own.** Serve it through the
  router or leave it unlisted, so there is exactly one origin per brand to put in
  front of a client.
- **A deploy worktree goes stale the moment another lane commits a dependency.** A build failing with `Module not found` after pulling new commits is usually a lockfile change, not a broken environment: diff `package.json` against the last successful build, then re-run `npm ci` (not `npm install`) before rebuilding.
- **Poll a live host defensively and re-login on 401.** During a rollout the
  response shape changes under the poller: a 401 while the new container comes up,
  an error body instead of the payload, an empty seed list. `.json()["key"]` raises
  and the deploy reports a probe crash rather than a transient. Use `.get(key,
  default)`, treat 401 as "log in again" (a container restart invalidates the
  session cookie), and bound the retries. Copy seed files into the image with
  readable permissions, or seeding exits 0 having loaded nothing.
- See `public-visitor-mode` for the no-login contract the router must enforce (spend
cap, per-IP count, model lock, admin closed).

## Pushing the built site
- **A repo whose working branch is not `main` will not fast-forward `main` when you push it.** Build lanes create `build/<name>` branches, and a later hand-built round usually runs on that branch with no local `main` at all, so `git push origin main` either rejects as non-fast-forward or silently pushes a stale branch. Push the checked-out commit explicitly (`git push origin HEAD:main`), then confirm with `git fetch` plus `git rev-parse --short HEAD origin/main` that both hashes match. Before forcing anything, prove the divergence is harmless: `git merge-base --is-ancestor origin/main HEAD` says the remote's extra commits are already contained in what you hold, and only then is a plain push safe.

## Verification pattern
- Smoke test as `test/smoke.mjs` taking `BASE` and `ADMIN_TOKEN` env, run against the deployed URL, asserting status codes, byte round-trip and a 206 range.
- Browser gate with Playwright against the live URL, driving the signed-in state before auditing (visual-verify's `audit.py` cannot inject localStorage; import its `PROBE` and run it after login).
- Launch Chromium with `--autoplay-policy=no-user-gesture-required` to prove `<video>.currentTime` advances.
