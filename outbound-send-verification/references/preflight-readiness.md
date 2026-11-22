# Pre-flight readiness across a capture + outreach pair

Use when a batch of real contacts is about to flow through an intake tool and
an outreach tool, and the ask is "make sure both are ready" rather than "prove
a send". Readiness is proven with the product's own credentials and its own
round trip, per system, before any contact exists.

## 1. Prove the intake side with the app's own key, full round trip

The capture tool has two credential surfaces: the key its web app ships and the
key operational scripts read from the host environment. They are set in
different places and drift apart silently, so a probe that passes proves
nothing about the app.

1. Read the key the shipped app actually uses (a hardcoded config value in its
   frontend bundle, or the env var it is built from). Compare the two values in
   python without printing either.
2. Call the API with the *app's* key and walk the whole loop, not one endpoint:
   `list` -> ingest one real-looking record -> `export` -> `delete` it. Each
   step is a different auth or serialization surface, and only the loop leaves
   the system in its original state.
3. Assert extracted fields against known ground truth rather than a 2xx status.
   Read the response shape before asserting: an ingest may return the parsed
   fields under `extracted_fields` *and* the stored record under `contact`, and
   a check aimed at the wrong key reports every field as mismatched while the
   extraction was in fact perfect.
4. Read the service logs for the request you just made. The endpoint's success
   tells you nothing about *which provider* did the work.

## 2. Separate "configured" from "working"

- A status endpoint that reports `configured: true` for an env var only says
  the variable is present. Ping the provider through the product's own key
  test route (`POST /api/settings/keys/test { keyName }`) with the stored key,
  and quote the verdict line, not the config flag.
- An empty usage table is not health. If an operation has written no rows in
  weeks, no call of that type has succeeded recently, so the credential behind
  it has never been exercised in the period you are looking at.
- When a fallback silently serves traffic, the primary is dead. Compare
  latency against the benchmarked fast path: a 10 to 19 s card against a 30 s
  client timeout is the fallback's signature, and it caps how fast a batch can
  run even though every request returns 200.

## 3. Measure the ceilings before promising throughput

Read these from storage and quote them in the report; they set the batch size
no code can raise:

- Per-sender mailbox quota (`domain_health.provider_limit` / `provider_used`)
  and the number of connected senders: daily ceiling = sum across senders.
- Send window policy in the outreach tool (recipient local hours) and any
  per-contact approval gate, for example a contact at a personal mailbox domain
  with no company to research. Gate codes are per-contact, so a mixed list
  yields a mixed approval outcome that must be stated before the batch runs.
- The shared model budget. One OpenRouter key often backs both drafting and
  scanning across products; check its remaining weekly balance, and if it is
  thin, name the risk that a batch stops partway instead of discovering it
  mid-run.

## 4. Prove the bridge itself as its own tier

Two systems each passing their own round trip says nothing about the link
between them. That link usually fails in one of three ways, and they need
different wording in the report:

| Tier | Question | Evidence |
|---|---|---|
| A | Does system 1 work at all? | its own key, its own full loop (sections 1 to 3) |
| B | Is system 2's receiving contract present? | the route exists and parses, at the exact path and shape system 1 calls |
| C | Has anything ever crossed? | a real record system 1 wrote, read back in system 2's storage |

- **A 404 on a "why is it not syncing" probe is tier B, not a secret problem.**
  The receiving route may not be deployed yet (an unmerged, undeployed branch),
  in which case no key can help: name the unshipped pull request as the cause
  and card its merge as the decision, rather than telling the requester to set
  a variable that will change nothing.
- **A `configured: false` flag means a secret is missing, and it gates only
  tier C.** List the exact secret names, which worker takes them, and the
  command to set them, as a decision card. An API key can never make a route
  appear, and a deployed route can never sync without the key: say which of the
  two is blocking instead of reporting the integration as "not working".
- **Exercise tier C without touching production.** Run the producer locally
  (`wrangler dev --local` with a `.dev.vars` file naming the consumer's preview
  URL and a throwaway key) pointed at a preview of the consumer, and read the
  result back from that preview's own storage. The preview must have its own
  database, never a shared or production one, or the exercise writes into
  production rows. Use synthetic records only when either repo is public.
- Report each tier separately, one line each, with the command output behind
  it. Collapsing them into "the integration works" or "it is not connected"
  hides the one tier that is actually blocking.

## 5. Report readiness as per-system evidence, plus the one decision

Table the two systems separately with the observed evidence (list 200, scan
field match, export header, provider key verdict, sender row read back), then
surface exactly one decision card for the choice only the requester can make:
which brand/senders the follow-ups should go out as. Everything else either
passed or is a stated limit.

## Pitfalls

- Never prove a capture tool by an endpoint that reads only the host key; the
  app's own key is the one that failed for real users.
- Do not claim a batch is ready on status codes alone: a 200 from a slow
  fallback plus an empty provider budget is a batch that stalls halfway.
- A changed production config variable is a state change even when no code
  moved: name the variable, the before/after relationship (not the value), and
  confirm the service redeployed, in the report.
- Clean up every probe record in the same run. Test contacts left in a live
  account are indistinguishable from real leads at import time.
