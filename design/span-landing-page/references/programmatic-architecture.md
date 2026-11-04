# Programmatic page families: architecture rules

Depth for taking SPAN variant families from generated HTML files to a real system. The full plan (DDL, Sanity schemas, route table, phases, decisions for Preeti) lives in the Celsus vault, Ideation folder: "SPAN programmatic pages, Astro Sanity Supabase plan". These are the rules that must survive into any version of that build.

## Rendering and routing

- Static output, rebuilt on publish. Hundreds of pages, no live database on the public path; the DB is a build input, not a runtime dependency.
- One URL per ad variant (`/lp/<technology>/<variant>`), `?hl=` headline overrides only as a preview affordance. A URL per variant gives ads clean tracking and its own meta.
- Ad landing pages are always `noindex`. Indexed pages (comparison, users lists) pass a gate: counts present plus a minimum length of unique intro copy, else downgraded to `noindex` and logged. This is the doorway-policy defence; never index thin generated copy.
- Serve indexed pages under paths on the main domain via a Worker route in front of the existing site, not a subdomain: authority is inherited from the main domain, and only the three path prefixes route.

## Two sources, one join

- CMS (Sanity) owns written content and the page registry: one document per page, and `approved` status IS the publish gate. Data store (Supabase Postgres) owns dimensions and facts: technology, industry, role, counts, sample job titles, comparison pairs. Data team gets a table editor and CSV import without anyone building an admin.
- Join on slugs in a single function at build time. A reference to an unknown slug fails the build loudly; the previous deploy stays live.
- `verified_at` is a stored date from the import, never computed at render time, so "counts verified <month>" on the page is true by construction.
- Pages exist only as approved documents. Never generate from the cross product of dimensions; that is how thousands of thin pages appear.

## Rebuild triggers

- CMS publish -> webhook -> deploy hook. Data publish -> one row inserted into an explicit `publish_requests` table -> same deploy hook.
- Pitfall: Supabase database webhooks fire per row after commit, so a hook on the counts table sends one request per changed row and a single CSV import fires a hundred rebuilds. Trigger from one explicit publish row instead.
- Code push -> Git integration on main. Add a nightly deploy-hook cron as a safety net.

## Editorial split

Data team never touches the CMS; the writer never touches counts; Preeti approves in the Studio and owns which pages are indexable; frontend owns components, routes and the Worker route. Deep owns the variable model and gate thresholds.
