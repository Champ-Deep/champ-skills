# Recurring journey shapes

The endpoint-to-screen matrix gives every screen its endpoints. Some journeys are
recurring shapes in their own right: a fixed sequence with decisions and failure
modes that recur across projects. Recognise them by shape and design the whole
journey at once instead of deriving it endpoint by endpoint.

## Authenticated file download

When the API guards any route with a header (API key, bearer token), the browser's
native download paths cannot carry it: `<a href>`, `window.open`, and a form GET
all drop custom headers, so the user gets a 401 on the single action they came to
perform.

Journey: request with `fetch`, attach the credential header, read `response.blob()`,
then save it (`URL.createObjectURL` + a programmatic click, or `a[download]`).
Errors surface as states, not as a browser error page: 401 reopens the credential
dialog, 404 means the job expired.

State in the brief: the auth mode, which routes are affected, and that no bare
links exist. A builder's default is the link, and it fails only for the person
using it, after the demo.

## Spend-gated job

Any flow that spends something scarce: paid API quota, SMS credits, LLM tokens,
human review time.

```
upload/submit ──> FREE PREFLIGHT ──> estimate (what the paid step costs)
                                        │
                        confirm naming the cost ──> START (spends)
                                                     │
                                          poll progress ──> done / interrupted
                                                     │
                                              download results
```

Rules:

1. The preflight is free and returns a count: rows, valid, invalid, duplicates,
   already cached, requests needed. It is a screen, not a log line. This is the
   moment the user decides to trust the tool.
2. The confirm button names the number. "Run (147 requests)" never "Run".
3. The paid call never fires implicitly, from page load, from a re-render, or
   from a refresh. Re-submitting an already-started job is a no-op with a 409,
   not a second spend.
4. Interruption is a first-class state. Provider quota or auth failure mid-job
   keeps everything already fetched; show it as a banner over partial, still-valid
   results, never as an error page that hides the work.
5. Progress is server truth: poll `done/total`, keep the job id in the URL so a
   refresh resumes, and paginate results server-side rather than downloading them
   all to render.

## Offline pass before paid pass

Where a free local check (format parsing, dedup, type detection, a local library)
can narrow the set, run it first and show the saving: valid, invalid, duplicates
removed before any quota is spent. Invalid rows are never sent to the paid
provider. The estimate screen carries both numbers so the cost of skipping the
free pass is visible.

## Fixture for the whole journey

Ask for (or build) one fixture file that exercises every branch in a single run:
a typical record, a duplicate, a numeric-typed cell, an invalid record, a junk
record, and one record with every nullable field empty. One run then proves the
upload, the estimate, the run, the result styling, and the download instead of
six separate tests.