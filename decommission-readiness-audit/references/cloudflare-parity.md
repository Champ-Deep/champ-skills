# Cloudflare side of a parity audit

Authenticated REST with the account and zone ids from `/members/v1/accounts` and `/zones`. Sleep ~0.4s between per-script calls; the settings endpoint rate-limits tight loops over a dozen scripts.

## Endpoints that answer the parity question

| Need | Endpoint |
|---|---|
| Which zones exist | `/zones?per_page=50` |
| Who actually serves a hostname | `/zones/{z}/dns_records?name=HOST` -> read `proxied`, `type`, `content` (the origin) |
| Worker scripts | `/accounts/{a}/workers/scripts` |
| What a script is bound to, and what secrets it holds | `/accounts/{a}/workers/scripts/{w}/settings` -> `bindings[]`: `type` in `d1`, `r2_bucket`, `durable_object_namespace`, `assets`, `service`, `secret_text`, `plain_text`, `version_metadata` |
| Static sites | `/accounts/{a}/pages/projects` (name + domains) |
| Account workers subdomain | `/accounts/{a}/workers/subdomain` |
| Worker traffic over a window (per-script) | `/accounts/{a}/workers/scripts/{w}/requests?since=<ISO>&until=<ISO>` -> `totals.requests`, `unblockedRequests` |
| Durable object namespaces, and which script owns each | `/accounts/{a}/workers/durable_objects/namespaces?per_page=1000` -> `id`, `script`, `class`, `deleted` |
| Containers: size, state, owning script | `/accounts/{a}/workers/containers/instances` and `/accounts/{a}/workers/containers/apps` |
| Container metrics (memory, disk, CPU seconds) | `/accounts/{a}/workers/containers/apps/{app}/instances` metrics, or `/accounts/{a}/workers/containers/apps/{app}/metrics` |
| DO namespace use (`last_updated`, `expires`) | `/accounts/{a}/workers/durable_objects/objects?namespaceID=...` |
| Bill | `/accounts/{a}/billing/history` and `/profile/billing/history` (only with a billing-capable credential; see `cloudflare-cost-audit.md`) |

## Reading bindings

- **Secret names are visible, values are not.** List the names as evidence of configured integrations; never attempt to read values.
- **`plain_text` vars are readable and are where an origin lives.** A var like `ORIGIN` holding a `*.up.railway.app` URL is the single finding that proves the worker is a proxy, not a migration.
- **A `service` binding or a proxy-shaped var set means the app still runs on the old host.** Only data bindings (`d1`, `r2_bucket`) plus no origin reference means the workload moved.
- **Pages projects and preview/staging workers do not count as production counterparts.** Match on production role: the worker that serves the apex through DNS, not a worker whose name resembles the project.
- **Zones on Cloudflare prove nothing about where the app runs.** The zone may hold only DNS while the origin answers from the old host, which is exactly what the header probe in SKILL.md step 3 separates.
