# Functional probes on deployed endpoints

When to use: writing or reviewing any scheduled check against a live URL, or
when a monitor reports an app down and you need to know which failure shape
it is.

A status code is a transport fact. Functionality is what the working app
returns. These are the probe shapes that hold across Deep's fleet, and the
failure each one is designed to catch.

## Probe shapes

| Probe | Assert | Catches |
|---|---|---|
| API route | the real payload (`"presets"`, a records key) | backend dead behind a healthy proxy or CDN |
| Health route with a dependency | a field naming the dependency (`"database":"connected"`) | app up, database not |
| SPA page | its `<title>` or framework asset marker | wrong site, blank deploy, error page served as 200 |
| Static marketing site | brand string in body | placeholder or parked domain |

Pick the route a user's first real action exercises. A landing page proves the
static host works; it has never once proved the backend does.

## Verify the marker before you ship the probe

Curl the live URL and read what a healthy response actually contains. A
hand-assumed marker (`<div id="root">` for a Vite app that does not use
`#root`) produces a red that never goes green, and a permanently red monitor
is ignored exactly like a broken one. Expect the first run to correct your
marker.

## Failure states and what they mean

| Symptom | Means |
|---|---|
| `unreachable` / timeout | DNS, TLS, or the host is gone; nothing to read logs for |
| `HTTP 5xx` | the app answered and failed; read deploy logs |
| `HTTP 200 but body lacks <expect>` | the shell renders while a dependency behind it is dead; this is the case a status-only probe misses |
| `HTTP 4xx` on a route that should be public | routing, auth, or path change, not an outage |

A red probe should carry the owning platform's last error lines so the alert
answers "why" on its own; see the Railway log-scoping recipe in the
`railway-deployment-ops` skill.

## Known blind spots to state, not hide

- **Auth-walled apps.** Behind a login, an unauthenticated probe can only
  prove the shell rendered. Say that in the report rather than implying a
  functional pass.
- **Health endpoints that report status without their dependency.** A
  `"status":"healthy"` that omits the database state passes while the
  database is down. Prefer a dependency field, and if the app does not expose
  one, flag the gap instead of trusting the field that exists.
