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