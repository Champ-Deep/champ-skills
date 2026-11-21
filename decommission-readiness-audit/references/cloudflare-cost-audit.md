# Pricing the Cloudflare side of a decommission or cleanup decision

Use when the audit or the card has to say what something costs, or what deleting it saves. The dashboard's billing page is the authority; everything below is the fallback for when the API available to you cannot read the invoice (a dashboard OAuth token is routinely refused on `/billing/*`, `/profile/*` and `/subscriptions`). Say in the report which of the two you used.

## Method: compute from what is provisioned, then label it an estimate

1. List the running instances: `GET /accounts/{a}/containers/instances` (join to `/workers/durable_objects/namespaces` when an instance has no script of its own), and `/workers/containers/apps` for per-app `max_instances`, `sleepAfter` and instance size.
2. Read each app's live use with `GET /accounts/{a}/workers/containers/apps/{name}/instances` metrics or the metrics endpoint from `cloudflare-parity.md`, and read `durable_objects/objects` for `last_updated` plus `expires` on each namespace object: a namespace object with no `expires` is never evicted, so it bills 24/7 while a request-scoped object expires and stops.
3. Estimate monthly spend for one instance running continuously:
   `GiB x 730 h x memory_rate + GB x 730 h x disk_rate`, with the published rates and the Workers Paid free allowance applied first. CPU and Durable Object time are separate line items you cannot see from instance size, so the total is a floor.
4. Report it as `estimated $N/mo from provisioned resources, invoice not read`, and put the number in the decision card as `about $N`.

## The three findings that drive the delete set

- **Orphans**: containers whose owning Worker no longer exists (namespace `script` is null or names a script absent from `/workers/scripts`), and durable object namespaces bound to no script. Nothing uses them; they run forever. They are the cheapest, least controversial deletes, so name them first in the card.
- **Over-provisioned but live**: an app with `max_instances: 3` and no `sleepAfter` serving a handful of requests a month. The fix is config, not deletion.
- **Preview and staging copies**: environments that exist to serve a PR or a throwaway test. Ask the owner where the project belongs to somebody else.
- Pair every candidate with its 30-day request count from `workers/scripts/{w}/requests` or the per-worker invocations metric. Zero-or-near-zero requests is the evidence that it is deletable; a busy preview Worker is not.

## Rules for the card

- The delete set and the keep set are separate totals, and both go in the card body.
- Quote what you could not price: CPU, DO time, bandwidth, and anything behind the invoice you couldn't read. An estimate presented as a bill gets re-quoted later as fact.
- Never fold a delete into a verification report; the deletion is the decision being asked for.