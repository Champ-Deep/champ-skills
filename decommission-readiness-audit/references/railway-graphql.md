# Railway GraphQL depth for decommission audits

Endpoint `https://backboard.railway.com/graphql/v2`, header `Authorization: Bearer $RAILWAY_TOKEN`. Responses are often under `errors` with an empty `data`, so every call site must check both keys. Fields are `camelCase` even where the dashboard shows PascalCase.

## Queries that worked

**Inventory (projects -> services -> instances -> custom domains, plus env and volume names):**

```graphql
query { projects(first: 100) { edges { node {
  id name
  environments { edges { node { id name } } }
  services { edges { node {
    id name
    serviceInstances { edges { node {
      environmentId
      domains { customDomains { domain } edgeInfo { id } }
      variables { edges { node { name } } }
    } } }
  } } }
} } } }
```

**Liveness, per service instance, 7-day window (sum the returned daily points):**

```graphql
query($p:String!,$s:String!,$e:String!,$t:DateTime!) {
  metrics(projectId:$p, serviceId:$s, environmentId:$e, startDate:$t,
          measurements:[NETWORK_TX_GB, CPU_USAGE], sampleRateSeconds:86400) {
    measurement values { value }
  }
}
```

`NETWORK_TX_GB` summed over the window is the go/no-go signal for in use versus idle. `CPU_USAGE` points are not a percentage when summed; use them only to rank relative activity.

**Data footprint (MB per volume per environment):** `projects -> edges -> node -> volumes -> edges -> node { name volumeInstances { edges { node { currentSizeMB environment { name } } } } }`. This is the size of what a delete destroys, and it belongs in the decision card.

**Live traffic (hostnames that called in):** resolve the latest deployment first with `deployments(first:1, input:{projectId, serviceId, environmentId})`, then `httpLogs(deploymentId:$id, limit:200){ timestamp path method httpStatus host }`.

## Pitfalls

- **400 Bad Request means a bad projection field, not a dead API.** Wrap the call, catch `urllib.error.HTTPError`, read `e.read()` for the message, and retry with fewer fields. One nested field (`serviceInstance.serviceName` inside a volumes query) was enough to reject the whole query.
- **Logs cover the latest deployment only.** Zero rows there is not zero traffic; cross-check against the metrics query before calling a project idle.
- **Custom domains in the inventory are claims, not truth.** They can point at a host that no longer serves the domain; always pair with a live header probe.
- **The workspace id is only needed for some root queries** (`projects(first, workspaceId)`); `projects(first:100)` without it worked for inventory.
- Keep the raw dumps (projects, metrics, volumes) in the scratch dir and cite the paths in the report, so a follow-up session re-reads instead of re-querying.
