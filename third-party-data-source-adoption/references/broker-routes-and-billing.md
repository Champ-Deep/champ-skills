# Adopting a data source through an existing broker

Recipe for the case where the vendor we want (an HLR network, a firmographics
API, a search provider) already sits inside a broker Deep keys (treg, treg.to).
Use it before writing any direct HTTP client for that vendor.

## 1. Search the broker's catalog for the vendor by name

```bash
treg catalog search <vendor>          # e.g. treg catalog search hlr
```

- Hits come back as catalog endpoints named `<vendor>.<domain>.<action>` (for
  example `hlrlookup.people.phone.verify`), each with its route, its price and
  its answer shape. Read prices from the catalog at adoption time; do not
  hardcode them into code or briefs, because they move.
- If the search returns nothing, the vendor is not on the broker: build the
  direct client and expect a credential procurement step (a capability block
  for Deep, which stalls the feature until a human buys it).
- Three routes at one vendor often split by capability and price: a live check,
  a cheaper network/port lookup, and a free type-only lookup. Take the one that
  answers the question the feature asks, not the cheapest, and say in the
  report which one you take and why the cheaper ones do not answer it.

## 2. Send the flags that make the answer live

Providers return a syntactically valid degraded answer when a mode flag is
absent, and bill it the same as a real one:

- Cache controls (`cache_days_global`, `cache_days_private`, `save_to_cache`)
  left unset can return a stored value presented as a current one.
- A region switch (for example a `usa_status` flag gating North American
  coverage) left unset returns a status meaning "not checked there" rather
  than an error, so the row looks answered while it was never queried.

Read these flags out of the provider's reference or the catalog entry, put them
in the request, and prove one live answer carries the field the feature needs
before reporting the layer as working.

## 3. Auth, caps and attribution

- Check broker auth before promising a live pull (`treg connections`). A broker
  401 is a human login step: stage the exact login and token-mint commands as a
  blocked decision, never retry-loop it.
- Pass the broker's cost-cap and attribution headers on every call so one loop
  cannot run the bill, and put the feature tag in the metadata header so spend
  is attributable to the feature that caused it.
- Report the per-call price as the reported charge, not as spend.

## 4. Read spend from the ledger, never from the response header

A per-call cost header says what the route is worth, not what was deducted.
The broker serves on team-owned provider keys first, so a call can be answered
without the balance moving at all:

```bash
treg balance --limit 40 --json | python3 -c \
  "import json,sys; i=json.load(sys.stdin)['entries']['items']; print(len(i), i[0]['created_at'])"
```

- `entries` is an object (`limit`, `offset`, `items`), not a list: index
  `items`, or the parse fails before any row is read.
- No new row and an unchanged balance means the call was served on a key the
  team already owns; a row with a negative `amount_micro` means it was charged.
- State both facts when reporting cost: the header's figure and whether the
  ledger shows a deduction. Quoting only the header overstates spend, and
  quoting only the ledger understates what the same call costs once the team's
  own key runs out.
