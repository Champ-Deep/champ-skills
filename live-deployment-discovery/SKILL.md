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
   bug is not "an old deploy" and no redeploy will fix it.
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

- Treat Worker code, custom-domain triggers and DNS as separate outcomes. Wrangler can upload and activate a version, then exit nonzero because custom-domain attachment failed. Read deployment versions and fetch the workers.dev host before retrying; never call the custom domain live from an upload message.
- Inspect apex and www DNS before replacing parking records. An active Cloudflare zone with correct nameservers can still retain registrar parking A/CNAME records. Domain changesets can report no conflicts while attachment rejects externally managed DNS records. Preserve mail records and limit any approved change to the exact web hostnames.
- Check permissions rather than assuming Wrangler OAuth includes DNS editing. Worker/D1 access and zone metadata can work while DNS record reads return 403. If no authenticated DNS-capable channel is available, request the specific parking-record removal in the dashboard; do not request a token in chat or keep retrying the same denied API.
- Keep strict CSP during browser verification. String-evaluating waits and injected style tags may be rejected by the page. Prefer locator waits/assertions and the shipped reduced-motion mode rather than weakening CSP to make the harness pass.
- Verify request capture through the real browser and database: submit synthetic records, repeat one request id, read the exact rows, then delete only those synthetic ids and verify absence. A mocked UI success proves interaction states, not persistence or delivery notifications.

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