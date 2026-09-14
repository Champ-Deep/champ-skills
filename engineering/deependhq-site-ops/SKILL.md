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

## Known traps

| Trap | What to do |
|---|---|
| `.git/index.lock` in the worktree | A sandbox cannot delete it. Remove it on the Mac: `rm -f <repo>/.git/index.lock`. `publish.sh` is immune; local git commands are not. |
| Worktree is on branch `initial-site` | Production is `main`. `publish.sh` hardcodes `main` correctly. `publish-native.sh` pushes `HEAD:main` from whatever is checked out, so verify before relying on the fallback. |
| `rsync --delete` clobbers newer remote commits | The worktree mirrors onto the clone. If someone fixed something directly on GitHub, reconcile first. Check `git log origin/main` freshness before publishing. |
| `pending-entry.json` in scripts/ | A fossil from June 2026, gitignored and rsync-excluded. Misleading clutter, not a signal. Safe to delete. |
| `ingest-shoutouts.mjs` | Orphaned. Nothing calls it. It writes a review queue that is never auto-published, by design. Wire it into a weekly cadence or delete it. |
| rsync copies `deependhq-next/node_modules` nightly | Hundreds of MB for nothing. Add `--exclude 'deependhq-next/node_modules'` and `--exclude '**/.next'`. |
| Documentation drift | `PIPELINE.md`, `DEPLOY.md`, the public `Pipeline.jsx`, and two copies of the `daily-note-recap` skill all describe different schedules and deploy targets. Only the vault copy at `Scheduled/daily-note-recap/SKILL.md` is authoritative. Reconcile before debugging by the docs. |

## Hardening checklist

When asked to make this more reliable, these are the fixes that matter, in order:

- [ ] **Preflight in Part B.** Assert the daily-notes directory exists, the deploy key exists, and `content.json` parses. Hard fail before any authoring. This is what distinguishes "a quiet day" from "a broken sensor".
- [ ] **Make live verification unconditional.** Currently gated on a successful push, which means the one guard designed to catch staleness is bypassed by the exact condition it exists to detect. Always fetch live `data.js` and compare `brand.today_date` against IST-yesterday, push or no push.
- [ ] **Independent watchdog.** A separate small task at 09:00 IST that only fetches the live `data.js` and alerts if it is more than 2 weekdays behind. It must share no code, no mount and no state with the publishing task. The current health counter lives inside the daily notes, which is the very thing that breaks.
- [ ] **Two consecutive "nothing to publish" nights is an alarm**, not a shrug.
- [ ] Widen `check-gaps.mjs` to 30 days and replace the break-on-first-hit walk with a full-range scan, so holes older than the newest entry are still found.
- [ ] Add a naming denylist scrubber alongside the existing em-dash scrubber in `build-data.mjs`. Naming rules are currently enforced only by the authoring self-check, with no deterministic backstop.
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
