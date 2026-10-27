# Analytics and entry-schema depth

## First-party analytics: how it is wired and how to prove it

The site collects its own events via `analytics.js` to `/api/collect`, stored in
Workers Analytics Engine. **PostHog was considered and rejected:** a third-party
script on a site whose footer says "no cookies, no trackers", needing a wide CSP
relaxation, and unverifiable from the vault. If PostHog is ever wanted, forward
the existing payload from `/api/collect` rather than adding a script tag.

The dataset `deependhq_events` **must exist in the Cloudflare dashboard before
the `analytics` binding is added to wrangler.jsonc**, or the deploy fails on the
binding. The endpoint answers 204 when the binding is absent, so once the
dataset exists it starts recording with no code change.

`scripts/query-analytics.mjs` reads it back. It exits 2 with setup instructions
when `CLOUDFLARE_API_TOKEN` and `CF_ACCOUNT_ID` are absent, and never prints
placeholder numbers. Analytics Engine indexes are **exactly 20 bytes**, so
queries must truncate with the same rule the write path uses.

### Proving a beacon works needs CDP, not a screenshot

`sendBeacon` returning `true` proves nothing: the browser queues the request and
discards it silently if the response lacks CORS headers, and a Blob with
`type: application/json` triggers an OPTIONS preflight that must be answered.
Headless `--screenshot` and `--dump-dom` never flush these, so events appear to
"not work" when the code is correct. The reliable check is
`scripts/`-adjacent CDP with `Fetch.enable` intercepting the collect URL, which
removes CORS, server timing and beacon flush timing from the equation entirely.
Verified that way: 7 events, correct path, scroll marks, outbound click labelled
`book_a_call`, and the easter egg.

### A module-scope `root` collides with the prerender sandbox

`analytics.js` is bundled into the prerender sandbox, which already has a
module-scope `root` for the site directory. A second `const root` is a
SyntaxError that kills the whole bundle, and it surfaces only as a browser-side
exception. Name it `dhRoot`.

## Extending the entry schema

New fields must be **optional**, so all existing entries stay valid and nothing
needs migrating. The set worth adding, because the design can render them as
visuals instead of prose:

- `metrics[]` of `{k, v, unit?}` - every number worth writing in the prose is
  worth being a chip. Cap 4.
- `artifacts[]` of `{kind, label, href?}` where kind is
  `doc|repo|deck|site|deal|hire` - what exists now that did not exist
  yesterday. Cap 3. `href` only when public, never a client name.
- `signals[]` from a controlled vocabulary only: `shipped, hosted,
  external-meeting, budget-unlocked, hire, blocked, unblocked, launch, deal`.
  Never invent one.
- `energy` 1 to 5, honest. A 5 every day is noise, not signal.
- `github_commits` - already accepted by `ingest-entry.mjs` but routed to
  `status` and discarded per-entry. Store it on the entry. It is the most
  credible number on the site and it is currently thrown away nightly.
