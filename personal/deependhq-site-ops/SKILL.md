---
name: "deependhq-site-ops"
description: "Operate, diagnose and repair the deependhq.com nightly build-in-public publishing pipeline. MANDATORY TRIGGER for: \"the site is stale\", \"deependhq hasn't updated\", \"publish the site\", \"why is the journal stuck\", \"backfill the missing days\", \"the nightly job failed\", \"check the pipeline\", \"did the site publish\", any question about the daily note to journey entry to live site loop, or any report that a scheduled task is silently succeeding without producing output. Also use when adding fields to the journey entry schema or changing what the nightly authoring step writes."
---

# deependhq.com Site Ops

Operate and repair the nightly loop that publishes deependhq.com from Deep's Obsidian vault.

## The system in one paragraph

A nightly scheduled task named `daily-note-recap` runs at 01:03 IST. Part A writes the day's vault note at `Calendar/Daily Notes/YYYY/MM/YYYY-MM-DD.md`. Part B reads that note, authors a journey entry in Deep's voice, ingests it into `content.json`, regenerates `data.js`, pushes to `Champ-Deep/deependhq-site@main` over SSH, and verifies the live site. Cloudflare Workers Builds deploys the Worker `deependhq` from `main`. A Mac LaunchAgent at 02:15 is the fallback publisher.

Repo worktree: `Efforts/Active/TheDeepEndHQ/deependhq-site/` inside the vault. **It is a worktree only. Never run a writing git command against its `.git` from a sandbox.** `publish.sh` clones fresh and rsyncs onto the clone, which is why it works from anywhere.

## Diagnose first, in this order

Run these before touching anything. Most "the site is broken" reports are one of the first three.

```bash
# 1. what does the live site actually serve
curl -s "https://deependhq.com/data.js?cb=$(date +%s)" | head -c 400
#    read brand.today_date. compare to yesterday (IST, weekdays only).

# 2. what does local content think
node -e "const d=require('./content.json');console.log(d.brand.today_day,d.brand.today_date,d.journey.length)"

# 3. which weekdays are missing
node scripts/check-gaps.mjs      # read-only, safe. prints MISSING_DAYS=...

# 4. is local identical to live
diff <(curl -s https://deependhq.com/data.js) data.js && echo "local == live"

# 5. can the task reach what it needs
ls "$VAULT_ROOT/Calendar/Daily Notes" && ls "$VAULT_ROOT/Other/.secrets/"
```

### Reading the result

| Finding | Diagnosis |
|---|---|
| local == live, both stale | **Publishing is fine. Authoring never ran.** Look upstream at Part A and the mount. |
| local newer than live | Push failed, or it went to `initial-site` instead of `main`, or Workers Builds failed. |
| local stale, live stale, daily notes missing for those dates | Part A could not write. Almost always a vault mount or path problem. |
| daily notes exist, no journey entries | Part B's "nothing to publish" escape hatch fired. Check whether the note had usable material. |
| `check-gaps` prints nothing but the site is old | The gap is more than 10 days back and has fallen out of the scan window. Widen the window before it becomes permanent. |

## The failure that has already happened once, so check it first

The scheduled task's sandbox stopped mounting the whole vault as one folder. Three things broke at once and none of them errored:

1. `find "$(ls -d /sessions/*/mnt/Celsus)"` returns nothing, so the vault activity scan is empty.
2. `Calendar/` is outside the mount, so the daily note cannot be read or written. Part B's escape hatch then reports "nothing to publish" and the run **exits successfully**.
3. `publish.sh` locates the deploy key by walking four directories up from the repo. That heuristic only works when the whole vault is one mount, so the key is not found.

Symptom: the task is enabled, `lastRunAt` is recent, and the site has not moved in days. If the vault-wide check shows that *every* scheduled task stopped writing around the same date while Mac cron and interactive sessions kept working, this is it.

Fix: restore the single-folder mount, or replace both path heuristics with explicit env vars (`VAULT_ROOT`, `DEEPENDHQ_DEPLOY_KEY`) resolved once and asserted before use. The env-var route is more durable and fixes every scheduled task, not just this one.

## Publish manually

```bash
cd <vault>/Efforts/Active/TheDeepEndHQ/deependhq-site

# author and ingest one entry (single-line JSON, or --file, or stdin)
node scripts/ingest-entry.mjs '{"date":"2026-08-18","mood":"...","shipping_now":"...","yesterday_thread":"...","raw_thought":"...","arcs":["Lake B2B"],"arc_color":"green"}'
# this rewrites content.json and then runs build-data.mjs for you

bash scripts/publish.sh
# PUBLISHED: <repo>@main <sha>   -> good
# NOTHING-TO-PUBLISH             -> only acceptable if the live site is already current
# PUBLISH-FAILED: ... exit 2     -> deploy key missing or host keys unpinnable
#                        exit 3  -> clone failed
#                        exit 4  -> push rejected, deploy key likely read-only

sleep 90
curl -s "https://deependhq.com/data.js?cb=$(date +%s)" | grep -o '"today_date":"[^"]*"'
```

**Always verify against the live site.** A successful push is not a successful publish. Workers Builds can fail after a good push, and pushing to `initial-site` produces a preview build that never reaches production.

## Backfill missing days

Order matters and there is a deadline.

1. Run `node scripts/check-gaps.mjs` to get `MISSING_DAYS`.
2. For each, **oldest first**, excluding today: read that date's daily note, author an entry, ingest it.
3. Publish once at the end, not once per day.
4. Verify all backfilled dates appear in the live `data.js`.

`check-gaps.mjs` only looks back **10 days**. Anything older falls out of the window and becomes a permanent hole in the log. Backfill inside that window or widen it first.

Inserting an older day is safe: `build-data.mjs` re-sorts the journey newest-first and realigns `brand.today_day` to `journey[0]`, so the day counter never gets disturbed.

## Authoring rules for a journey entry

Voice: Deep's. Lowercase, direct, specific, dry. One idea per sentence. End with the point, not a setup for the point.

Required fields: `date`, `shipping_now`. Everything else has a default.

```json
{
  "date": "YYYY-MM-DD",
  "mood": "one emoji",
  "shipping_now": "the day's headline. concrete artifact or number, always.",
  "yesterday_thread": "the secondary thread. may be empty.",
  "raw_thought": "the honest reflection. this is the line people quote.",
  "arcs": ["one or two labels"],
  "arc_color": "green | blue | gold",
  "github_commits": 14
}
```

Quality gate, all five must pass before ingesting:

1. **Founder-stop test.** Would a founder scrolling past stop on this?
2. **Concrete.** At least one artifact or number that did not exist yesterday.
3. **Zero corporate speak.** No "leveraged", "synergy", "excited to announce".
4. **Naming rules.** No real team members. The patriarch is "Chief". External prospects and clients in active deals are anonymized to roles. Team codenames are fine, individuals are not.
5. **No em dashes.** `build-data.mjs` strips them mechanically as a backstop, but do not rely on it.

One rewrite permitted. If neither a metric nor an artifact can be extracted honestly, say that in `raw_thought` rather than padding the entry.

`arc_color`: green = building and shipping, blue = thinking and exploring, gold = a real outcome, money, something signed.

## A publish that says PUBLISHED may not have deployed (2026-09-26)

Two separate failures looked like successful publishes. Check the live site, not
the publish output, before believing a deploy landed.

**`package.json` is tracked and esbuild is a RUNTIME dependency.** Cloudflare
builds may install with `NODE_ENV=production`, which skips devDependencies; if
esbuild sits in devDependencies, prerender has no bundler and pages publish with
an empty `#root`. Keep it in `dependencies`. Never delete package.json: the old
DEPLOY.md told you to.

**`node_modules/` must be in `.assetsignore`.** Cloudflare builds runs
`npm install` in the checkout, and `node_modules/workerd` alone is 135MB against
a 25MB per-asset limit. Without the ignore the build dies and nothing deploys,
while publish.sh still prints PUBLISHED.

**Verify a deploy landed:**

```
curl -s https://deependhq.com/data.js | sed -n '3p'    # Built <timestamp>
curl -sI https://deependhq.com/ | grep -i content-security-policy
```

No CSP header means the Worker did not deploy. A `Built` timestamp older than
your local `data.js` means the same.

## Gates must fail loudly, and you must prove they do

`publish.sh` now runs guard, build-data, prerender and link-check before
pushing. A gate nobody has seen fail is a gate nobody knows is armed, so each
has a self-test that injects the bad input and asserts a non-zero exit:

- `node scripts/guard-selftest.mjs` (6 cases, naming and disclosure)
- `node scripts/ingest-selftest.mjs` (23 cases, entry schema v2)
- `node scripts/link-check.mjs` with a link injected into a page

**Assert your injection landed before trusting a pass.** A link-check test
"passed" once because the python injection used an anchor that no longer existed
in the file, so nothing was injected and the gate was never exercised. Same class
of bug as the first naming matcher, where `pip` and `hospitali` matched
"pipeline" and "hospitality". Both times the fix was to verify the premise, not
to trust the green. When a gate passes unexpectedly, suspect the test.

## One file per entity, or Google indexes one page for all of them (2026-10-01)

`post.html` was prerendered once with `search: ''` in the sandbox, so
`params.get('slug')` was null at build time and `posts[0]` was baked into the
HTML for **every** post URL. All fifteen essays served the newest one's body,
title and H1. `week-44-the-discipline-arc` returned week 45's headline. The
prerender now renders one file per record at `post/<slug>/index.html` and
`company/<slug>/index.html`, each with its own `<title>`, description,
self-referencing canonical and JSON-LD.

Four things that fix had to get right, each of which failed first:

- **The component must read the slug from the path too.** `PostPage.jsx` read
  only `?slug=`, so at `/post/<slug>/` it fell back to `posts[0]`: correct
  title in the served HTML, then React overwrote it on hydration. The bug was
  invisible in a curl and only showed up in a screenshot. Same fix in
  `CompanyPage.jsx`.
- **Nested pages need `<base href="/">`.** Two directories deep, every relative
  href resolved against `post/<slug>/` and 404'd, styling included.
- **`link-check.mjs` must honour `<base>`,** or it reports 996 false
  failures. And when computing the base directory use `resolvePath(root, '.'+href)`,
  never `dirname(join(root, href))`: the latter keeps a trailing slash and
  `dirname` of that is the *parent* of root.
- **`link-check.mjs` treated `/` as broken.** It appended `.html`, looked for
  `/.html`, and failed all 27 entity pages. `/` is served by `index.html`.

Verify this class of bug in a browser, not with curl. Hydration is the whole
point of the prerender, and curl cannot see it.

## Entity links must be rewritten too, or the fix is invisible to a crawler

Moving pages to `/post/<slug>/` while every internal link still pointed at
`post.html?slug=` leaves the new paths orphaned: correct, indexable, linked by
nobody. Eight JSX files build those hrefs (Footer, Ecosystem, Home,
WritingPage, CompanyPage, PostPage, ShippingNow, JourneyPage, SecondCTA,
PillarsPage). A worker 301 keeps old external links alive, so legacy URLs are
fine to leave, but internal ones should be canonical.

## A redirect into a 404 is worse than an ugly URL

The Worker shipped `301 /field-notes -> /mission-log` for a page that was never
built. Two publishes succeeded and every old link 404'd. Nav and footer point at
`journey.html`, so the redirect targets `/journey`. When a pretty route does not
exist yet, redirect to the route that does. `scripts/link-check.mjs` fails the
build on any link to a missing page, and runs after prerender because it reads
the built HTML.

## CSP blocked Cloudflare's own analytics beacon: resolved 2026-10-01

`static.cloudflareinsights.com` was missing from `script-src` and was refused on
every page. It is now allowed, in both the `/showcase` branch and the plain
asset pass-through, because a domain missing from the first header and present
in the second is the kind of thing that silently half-works.

The footer's "no cookies, no trackers" line was reconciled with this in the same
publish. Cloudflare Web Analytics is cookieless and does not set identifiers, so
the claim stays true. Do not re-add a tracker that needs consent without
revisiting that sentence.

## A new page class must be added to four places, or it half-exists (2026-10-02)

Adding `/privacy` needed all four on the same day. Missing any one of them
produces a page that looks fine locally and fails in a different way:

1. `PAGES` in `scripts/prerender.mjs`, or it is never prerendered (empty root).
2. `ALL_PAGES` in the same file, or the bundle has no component.
3. `window.ThePage = ThePage` at the bottom of the new `.jsx`, or the render
   dies with `X is not defined`. Every page file does this and it is easy to miss.
4. `run_worker_first` in `wrangler.jsonc`, or the page is served straight from
   the asset store with **no CSP and no security headers**.

Plus: the `.jsx` must load before `page.jsx` in the HTML, and the shell's script
order must match the other shells exactly (Sys, Nav, Footer, page body,
Palette, page.jsx, widgo-gate, analytics).

## Analytics: first-party, and how to prove it works

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

## A property and a method with the same name blanked the whole site (2026-10-02)

The costliest bug in this repo's history, and the pattern to check first if the
site ever returns 200 with a body of about sixteen bytes.

`Personalize` stored its classification on `this.segment` and also defined a
method called `segment(el)`. The prototype method shadowed the property. The
HTMLRewriter handler called `p.segment(el)`, got a string, and threw partway
through the response stream. Every page on the site served `<!doctype html>`
and nothing else: the homepage, every essay, every company page.

Why it was so hard to see: the status was 200, the CSP was present, the
security headers were right, and the deploy reported success. Nothing in the
response said "broken". A browser shows a blank page, not an error.

The fix is a renamed field, `this.seg`. The lasting part is
`scripts/selftest-worker.mjs`, which constructs the real class and asserts two
things: that calling `p.segment(el)` does not throw, and that no constructor
property shares a name with a method in that class.

**After any Worker change, run the selftests before publishing.** All five must
pass:

```
node scripts/selftest-worker.mjs
node scripts/selftest-segment.mjs
node scripts/selftest-copy.mjs
node scripts/selftest-digest.mjs
node scripts/selftest-privacy.mjs
```

**To tell a blank site from a working one, check the body length, not the
status:**

```
curl -s https://deependhq.com/ | wc -c     # healthy homepage is about 87000
```

A `200` with a small number is a broken site. A `200` with a normal number and
no content in the browser is a script error, and the console log is where to look.

## `node_modules/.bin/esbuild` was a Linux binary on this Mac

**Publishing blind is how the outage shipped.** A patch tool call reported
success, the fix was never written to disk, and I read the success message
instead of grepping the file. A patch is not applied until the file on disk
shows it. After any fix to `worker/index.js`, run
`grep -n 'this.seg\|this.segment' worker/index.js` and confirm the change is
actually there before publishing.

The local `node_modules` had been installed on Linux, so both
`node_modules/.bin/esbuild` and `node_modules/@esbuild/darwin-arm64/bin/esbuild`
were ELF executables. Symptom: `ENOENT` or `Exec format error` from prerender,
which reads as "esbuild is not installed" and sends you down the wrong path.
Fixed by fetching the real darwin-arm64 build and swapping it in. Cloudflare
builds on Linux and was never affected. Check with
`file node_modules/.bin/esbuild` before reinstalling anything.

This **recururs**. It came back after a publish, because a `.linux.bak` left in
the tree got restored. If `prerender: FAILED ... ENOEXEC` appears again, check
`file` first and delete any `*.linux.bak`. Note `workerd` has the same problem,
which is why `wrangler` cannot run locally on this machine; the CF API is still
reachable with curl if a token is exported.

## Known traps

| Trap | What to do |
|---|---|
| `.git/index.lock` in the worktree | A sandbox cannot delete it. Remove it on the Mac: `rm -f <repo>/.git/index.lock`. `publish.sh` is immune; local git commands are not. |
| Worktree is on branch `initial-site` | Production is `main`. `publish.sh` hardcodes `main` correctly. `publish-native.sh` pushes `HEAD:main` from whatever is checked out, so verify before relying on the fallback. |
| `rsync --delete` clobbers newer remote commits | The worktree mirrors onto the clone. If someone fixed something directly on GitHub, reconcile first. Check `git log origin/main` freshness before publishing. |
| `pending-entry.json` in scripts/ | A fossil from June 2026, gitignored and rsync-excluded. Misleading clutter, not a signal. Safe to delete. |
| `ingest-shoutouts.mjs` | Orphaned. Nothing calls it. It writes a review queue that is never auto-published, by design. Wire it into a weekly cadence or delete it. |
| rsync copies `deependhq-next/node_modules` nightly | Hundreds of MB for nothing. `publish.sh` now excludes `node_modules`, `deependhq-next/node_modules`, `**/.next`, `scripts/.prerender-cache`, `scripts/.shots` and `.wrangler`. The excludes are load-bearing: without them the deploy repo gains hundreds of MB every night. |
| Documentation drift | `PIPELINE.md`, `DEPLOY.md`, the public `Pipeline.jsx`, and two copies of the `daily-note-recap` skill all describe different schedules and deploy targets. Only the vault copy at `Scheduled/daily-note-recap/SKILL.md` is authoritative. Reconcile before debugging by the docs. |

## Hardening checklist

When asked to make this more reliable, these are the fixes that matter, in order:

- [ ] **Preflight in Part B.** Assert the daily-notes directory exists, the deploy key exists, and `content.json` parses. Hard fail before any authoring. This is what distinguishes "a quiet day" from "a broken sensor".
- [ ] **Make live verification unconditional.** Currently gated on a successful push, which means the one guard designed to catch staleness is bypassed by the exact condition it exists to detect. Always fetch live `data.js` and compare `brand.today_date` against IST-yesterday, push or no push.
- [ ] **Independent watchdog.** A separate small task at 09:00 IST that only fetches the live `data.js` and alerts if it is more than 2 weekdays behind. It must share no code, no mount and no state with the publishing task. The current health counter lives inside the daily notes, which is the very thing that breaks.
- [ ] **Two consecutive "nothing to publish" nights is an alarm**, not a shrug.
- [ ] Widen `check-gaps.mjs` to 30 days and replace the break-on-first-hit walk with a full-range scan, so holes older than the newest entry are still found.
- [x] Add a naming denylist scrubber alongside the existing em-dash scrubber in `build-data.mjs`. Naming rules are currently enforced only by the authoring self-check, with no deterministic backstop. **Done 2026-09-26:** `scripts/guard.mjs` plus `scripts/denylist.json`, runs in `publish.sh` and fails the build.
- [ ] Derive every computed number at build time. Stored counts drift: `weekly_narratives_count` is why the site has rendered "week 38 of 31".
- [ ] Emit a `health` object into `data.js` on every build: `built`, `newest_entry`, `weekdays_stale`, `missing_days`, and a `stale_sections` list computed from every `*.updated` field. The site's stale banner and per-section age affordances read from it, so the site tells the truth about itself without anyone remembering to update a string.
- [ ] Delete or wire the hardcoded `status` fields (`weather`, `listening`, `uptime_d`). A fake liveness signal is worse than none.

## Extending the entry schema

New fields must be **optional**, so all existing entries stay valid and nothing needs migrating. The set worth adding, because the design can render them as visuals instead of prose:

- `metrics[]` of `{k, v, unit?}` — every number worth writing in the prose is worth being a chip. Cap 4.
- `artifacts[]` of `{kind, label, href?}` where kind is `doc|repo|deck|site|deal|hire` — what exists now that did not exist yesterday. Cap 3. `href` only when public, never a client name.
- `signals[]` from a controlled vocabulary only: `shipped, hosted, external-meeting, budget-unlocked, hire, blocked, unblocked, launch, deal`. Never invent one.
- `energy` 1 to 5, honest. A 5 every day is noise, not signal.
- `github_commits` — already accepted by `ingest-entry.mjs` but routed to `status` and discarded per-entry. Store it on the entry. It is the most credible number on the site and it is currently thrown away nightly.

Sign off with: *That's the deep end.*
