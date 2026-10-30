---
name: live-deployment-discovery
description: "Find and verify what a live web app actually runs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [deployment, vercel, cloudflare, coolify, railway, health-endpoint, credentials]
    category: devops
    related_skills: [systematic-debugging, fix-proof-by-measurement]
---

# Live deployment discovery

Use when a task touches a deployed app: deploying it, adding an API key to it,
debugging it, or getting a team onto it. The user's mental model of the topology
is often incomplete or out of date, and acting on it produces confident wrong
answers about what is missing.

## Core rule: the running system is the only source of truth

**Do not act on a recollection of the topology, and do not act on a hosting
dashboard. Find the host that is actually serving requests, read its health
endpoint, and let that drive what you tell the user.** The user is the source of
intent, not of current state.

## Procedure

1. **Find the real API host from the deployed frontend's own bundle.** The
   frontend ships its API base as a literal string, so it names the backend even
   when every dashboard points elsewhere:

   ```bash
   curl -sL <frontend-url> | grep -o '/_next/static/chunks/[^"]*\.js' | sort -u
   for c in <chunks>; do
     curl -sL "<frontend-url>$c" | grep -oE 'https?://[a-zA-Z0-9.-]+\.[a-z]{2,}[^"'\s,)]*'
   done | grep -vE '<cdn>|<auth-provider>|w3\.org|schema\.org' | sort -u
   ```

   A hashed preview URL and the apex domain are frequently different things, and
   the apex can 404 while the deployment is perfectly healthy. Test both.
1b. **Compare the deployed service topology against what the repo declares,
before debugging any 502.** A reverse proxy answering `200` for static paths
while `Connection refused` on `/api/*` means the process it proxies to does not
exist in that project, not that the code is broken:

```bash
railway deployment list                    # recent FAILED vs SUCCESS: prod may be an older image
railway variables --json | python3 -c "import json,sys; print(sorted(json.load(sys.stdin).keys()))"
<repo>: grep -nE '^\s*name:|dockerfilePath' railway.toml / compose file
```

The config file declares the intended services; the platform's variable set
names what was actually provisioned. A declared backend service that never got
created, and a proxy env var left at its container default (`localhost:<port>`),
is the whole diagnosis: the repair is provisioning plus one variable, not a code
change. Read the failed build's log too; if the image never built, production is
still running the last successful one, and fixing the build must come first.

2. **Read the backend health endpoint.** It is ground truth on configured versus
   merely declared:

   ```bash
   curl -s <api-host>/api/health
   ```

   Read every field as a status report:
   - `configured: true` + `connected: false` + a `detail` saying no call has
     completed means **the key is already deployed and has simply never run.**
     Do not add it again.
   - A `detail` naming a specific missing var is the fix list. Quote it verbatim
     rather than inferring the env var name yourself.
   - `app_env` tells you whether you are looking at production.
   - A protected route returning 401 is the cheapest proof that auth is really
     on rather than dev-bypassed.
2b. **Isolate a user-reported broken feature before touching code.** Split the
   path at the network boundary, cheapest evidence first:
   - Hit the backend endpoint directly with a synthetic input (a curl POST with a
     generated fixture file, an auth token from a throwaway registered user).
     Registering one throwaway account on prod is the cheapest way to get past
     auth; never report the API as untestable because you had no credentials.
     A correct response proves the API, the API key, and the model provider all
     work, so the break is upstream in the client. This answers "is it an API key
     issue?" with a measurement instead of a guess.
   - Then drive the deployed frontend headlessly (Python Playwright, mobile
     viewport): log in, open the feature, exercise it through the real UI, and
     capture console plus every response status. Screenshots at each step are
     evidence a later session can re-read.
   - If both pass, say so plainly: the break is device-side (stale cached PWA
     build, denied permission, cold-start timeout). Name the candidates rather
     than shipping a speculative code fix.
2c. **Rule out a stale deployment by comparing bytes, not by trusting the
dashboard.** Hash the served HTML and its chunks against the local branch:
identical hashes mean the deployed build is the branch you are reading, so the
bug is not "an old deploy" and no redeploy will fix it. When several hosts serve
the same product (apex, www, workers.dev, staging), hash each one's index HTML
and asset filenames against each other too: three different bundle hashes mean
three different live builds, so "the link works" may be pointing at a stale one.
2d. **For an SPA behind an auth provider, an HTTP 200 that renders a loading
message is a failed login config, not a working deploy.** Confirm it with a
headless browser (the stuck loading text is the evidence), then corroborate at
the platform: an empty or auth-key-free `secret list` names the missing config.
You may also scan the shipped JS bundle for a configured key literal as a
boolean only; never print a found key.

2e. **Confirm which branch the platform deploys before you trust any merge.**
Repo default branch and deploy branch are separate settings. A service pinned to
an old feature branch keeps serving the pre-merge build no matter what lands on
the default branch, and two services of one product routinely end up pinned to
different branches for days (frontend from one, API from another), so the app and
its API become different generations while every dashboard reads green.

Read the pin from the platform API, not the dashboard:

```bash
# Railway: the CLI has no command for this. Query field path, with the token
# from user.token in ~/.railway/config.json, POST to backboard.railway.com/graphql/v2:
#   service(id:$SID) { repoTriggers { edges { node { branch repository } } } }
# Vercel: deployments API carries errorMessage that `vercel inspect --logs` does not.
# Token from ~/Library/Application Support/com.vercel.cli/auth.json, then:
#   GET api.vercel.com/v13/deployments/<deployment-url>  -> readyState, errorMessage,
#   meta.githubCommitSha
```

**Before switching a deploy pin, check the pinned branch is not ahead of the
target.** Merging to the default branch and then repointing the service silently
drops whatever the pinned branch had that the default does not: live features
vanish on the next deploy. Diff first with `git log --oneline origin/<target>..origin/<pinned>`,
land the pinned branch's commits on the target as a reviewed PR, and only then
switch the pin.
3. **Check what each credential actually belongs to before setting it.**
   Similar names are different vendors' secrets. An `*_MCP_TOKEN` naming an AI
   gateway is that gateway's own catalog token, not the key for a tool or MCP
   registry. Adding the wrong secret under a plausible name looks configured and
   then fails silently.
4. **Let runtime constraints pick the host.** A stateful service that keeps a
   database file on a volume, runs work on background tasks, and polls on a
   daemon thread cannot run on a request-scoped ephemeral edge runtime: none of
   those three survive a request. When a user asks for an edge platform, say
   plainly which half cannot move, then offer the split that works. Static
   frontend on the edge, stateful API where it can hold a volume.
4b. **Probe the serving stack before writing any build or output spec for a
   replacement site.** `curl -sIL <domain>` reveals the runtime (Plesk/nginx with
   `X-Powered-By: PHP` and no Node means the host only serves files), so the
   deliverable becomes a self-contained static folder plus a deploy doc rather
   than a framework project the host cannot build. The same probe shows redirects
   and the real apex (`bake.fit` 301s to `www.bake.fit`), which decides which
   hostname the deploy doc targets. Specifying the stack first and probing later
   produces a repo the live host cannot run.
5. **Report credentials as a presence table, never as values.** Show which vars
   are set, which are missing, and what each missing one blocks.

6. **Verify a claimed UI change by driving the page, not by reading its HTML.**
   Nav and menu items rendered by delayed scripts do not exist until the page has
   been interacted with (a pointer move, a scroll, a focus keypress), so an
   untouched screenshot of an empty header reads as "the change is missing".
   Interact first, wait, then read. In automation hover often will not open a mega
   menu: click each top-level item, read the open panel's visible text from the
   DOM, and screenshot each open state as evidence. Then check the footer, which
   typically keeps links the header dropped and tells you whether the removal was
   header-only.

## Cloudflare static Worker cutovers

- Query a Worker's real state without cd'ing into its repo: Wrangler OAuth is
  account-scoped, not repo-scoped, so from any repo where wrangler is installed
  and authenticated, `npx wrangler deployments list --name <worker>` (which
  head, when), `secret list --name <worker>` (names only; `[]` means no
  secrets so nothing can authenticate), `d1 info <db>` (table count,
  created_at) and `r2 bucket list` all answer against the target account.
  Run `wrangler whoami` first to confirm which account you are on before
  trusting any of it.
- A worker answering `200` proves the link is warm, not that the release is
  deployed. Pair the HTTP probe with the deployment age and the secret list
  before saying anything is "working": a warm shell with zero secrets cannot
  log in, and reporting the 200 alone reads as "the new code is live".
- Treat Worker code, custom-domain triggers and DNS as separate outcomes. Wrangler can upload and activate a version, then exit nonzero because custom-domain attachment failed. Read deployment versions and fetch the workers.dev host before retrying; never call the custom domain live from an upload message.
- Inspect apex and www DNS before replacing parking records. An active Cloudflare zone with correct nameservers can still retain registrar parking A/CNAME records. Domain changesets can report no conflicts while attachment rejects externally managed DNS records. Preserve mail records and limit any approved change to the exact web hostnames.
- Check permissions rather than assuming Wrangler OAuth includes DNS editing. Worker/D1 access and zone metadata can work while DNS record reads return 403. If no authenticated DNS-capable channel is available, request the specific parking-record removal in the dashboard; do not request a token in chat or keep retrying the same denied API.
- A committed deploy config (`wrangler.jsonc`, a `deploy.sh`, a DEPLOY doc that
  prints a URL) is intent, not state. Confirm with `wrangler deployments list
  --name <worker>`: an error that the Worker does not exist means the config was
  never run, and the documented URL is aspirational.
- On big platform JSON (`railway status --json` can exceed 50 KB), parse and
  print a reduced projection inside `execute_code` instead of letting the raw
  dump hit the terminal: service name, status, sha, domains only.
- Keep strict CSP during browser verification. String-evaluating waits and injected style tags may be rejected by the page. Prefer locator waits/assertions and the shipped reduced-motion mode rather than weakening CSP to make the harness pass.
- Verify request capture through the real browser and database: submit synthetic records, repeat one request id, read the exact rows, then delete only those synthetic ids and verify absence. A mocked UI success proves interaction states, not persistence or delivery notifications.

## Host and domain migrations

When the task is moving an app to a new host, these orderings decide whether
the cutover is safe:

- **Separate three claims that sound alike:** the zone already resolves through
  Cloudflare NS (DNS only), the app now runs on Cloudflare (hosting), and the
  domain's account/zone moved to a different owner (account transfer). Verify
  each independently; NS records prove nothing about where the app runs, and
  response headers (`server:`, `cf-ray`, `x-railway`, `x-vercel`) say which one
  is really serving.
- **Order: replacement fully proven before any traffic flip.** Login, existing
  deep links, file/data integrity and TLS on the real hostname all pass first;
  then flip the one record that routes traffic. Never flip a host record to a
  target that has not yet served a real authenticated session.
- **Keep the old origin running through verification, and write the rollback
  before the change.** A rollback after users have written to the new backend
  needs a data-reconciliation step, not just the old DNS record back.
- **Nameserver and cert propagation run on their own clock.** Do not promise a
  same-hour window that includes a zone move; prefer flipping traffic inside a
  zone that is already propagated, and stage cert/ownership TXT records a day
  ahead.
- **Limit external help to the exact record.** For a partner-owned zone, ask IT
  for one CNAME plus the generated TXT records with the saved prior value, never a
  nameserver or mail change.

### Re-verify a claimed migration before reporting it as done

A card completion summary and a subagent's report are self-reports, and a migration
claim ("now on <new platform>, no <old platform> left") is exactly the claim a
summary is most likely to get wrong or stale: a parallel session can finish that work
between your answer and his next question. Re-run the whole battery yourself before
repeating any part of a claim:

1. Platform state, not the config: `wrangler deployments list --name <w>`,
   `wrangler containers list` (name, state, live instance count), `wrangler d1 list`
   plus `wrangler d1 info <db>` (`num_tables`, `write_queries_24h`, `rows_written_24h`).
   `wrangler d1 list` can report `num_tables: 0` for a database that is in fact
   populated, so read `d1 info` before reporting an empty schema, and compare its table
   count against the migration SQL files' table count.
2. Response identity: `curl -sSI <url>` and read `server:`, `cf-ray`, `x-railway`,
   `x-vercel`, plus any auth-provider header naming the provider that was removed.
3. Old provider absent from what actually ships: grep the **working tree** (not the
   last commit) for old hostnames and for the removed driver's imports (`from 'pg'`,
   `pg-boss`, `postgres`), excluding tests, docs and archived migrations. A database
   swap leaves old hostnames alive in comments, `.env.example` and docstrings; a hit is
   a finding to report, not a pass.
4. Settings presence table by name only: an `awk` one-liner printing
   `LINE: NAME set|empty` per variable, plus `git check-ignore` on any backup file in
   the deploy folder, so a stale `.bak` holding old keys is not committed by a later
   worker.
5. Run the repo's own check and smoke scripts unpiped and read their exit codes:
   `./deploy/.../deploy.sh --check` (its `REQUIRED` list is the authority on what the
   deploy needs, not the example env file, which lags a redesign) and
   `./deploy/.../smoke.sh <url>` against production, confirming the smoke run cleans up
   the throwaway account it creates.

Then report three lists in this order: findings table, the open decisions (as numbered
options when more than one independent ruling must fit one reply), and what was **not**
 exercised. A smoke suite covering auth and one write proves the plumbing, never
 drafting, mail connect, approved send or enrichment, and the unstated list is what he
 will hit first in real use.

- **Live code that exists only as uncommitted local changes is a decision, not a
  note.** After a migration, run `git status --porcelain | wc -l` and
  `git ls-remote --heads origin <branch>`: if the deployed build's source is nowhere
  upstream, the app's only copy is that disk and losing it loses the running product.
  Card it as a decision (commit and open a draft PR, versus hold), rather than
  mentioning it in prose where it reads as trivia.
- **A platform left running after a successful migration is a cost and a data
  decision.** Name the leftover services and their sizes, say the new build does not
  use them, and card the retirement with the data question attached (keep as fallback
  for a stated window, copy the data across, hold). Never fold "shut it down" into a
  verification report; stopping a service that holds data is his call.

## Reporting honestly

State what you found before what you plan. A user asking for a key to be added
frequently does not know the key is already there, and telling them so is more
useful than adding it again. When your discovery contradicts the request, lead
with the correction and the evidence for it.

Distinguish three blockers, because they need different people:

| Blocker | Who resolves it |
|---|---|
| A credential that is absent and must be purchased or issued | The user |
| A credential present but never exercised | You, by triggering a call |
| Access to a control plane you cannot reach | The user, by authenticating a CLI or sharing a dashboard URL |

Say which one each item is. "Blocked on credentials" collapses three different
asks into one sentence and sends the user away to do the wrong thing.

When reporting a set of findings (deploy state, open gates, credential status,
blockers), Deep wants one compact table of findings followed by the open asks,
not a chronological narration of what was tried. State every credential as
`name: issued / pending / absent`, and name the exact durable fix (token URL,
env var) for each pending one.

## Pitfalls

- Do not treat a `404` on an apex domain as an undeployed app. Check the hashed
  deployment URL before concluding anything.
- Do not add a credential the health endpoint already reports as configured.
- Do not read a redacted `env pull` as an absent value. Sensitive values come back
  as `[SENSITIVE]`; use `env ls` for variable names and the health endpoint for
  real state.
- Do not assume the hosting platform the user names is the one serving the API.
  A frontend on one platform routinely calls a backend on a bare IP with a
  wildcard-DNS hostname.
- Do not offer to authenticate a CLI you cannot drive. An unauthenticated CLI
  means the user runs one command; it is not a reason to abandon the task.
- Do not present a port-forward or local tunnel as the plan. If the user asked for
  a durable host, name the durable host.
- Do not debug a proxy's `Connection refused` by editing the proxy. Trace the
  upstream target and confirm the upstream service exists on the platform first;
  the config default usually points at a process that was never deployed.
- Do not batch credential logins. Each pairing link expires on its own short
  clock, so deliver one, confirm it, then start the next.
- Do not confirm a deploy from a version string. Two different builds routinely
  report the same version, so a health field reading the new version is not
  evidence the new code is live; compare the deployed commit SHA against the
  commit you merged.
- Do not read a 0 ms deploy failure with no build logs as a broken build. Nothing
  was built: the platform rejected the config before building (a schema violation
  in the deploy config names the offending property), and `vercel inspect --logs`
  prints only `status Error`. The deployments API's `errorMessage` is the message.
- Do not treat a green frontend deploy as a deploy of the backend. Each host is
  pinned and builds independently; verify the commit on every host you claim about.