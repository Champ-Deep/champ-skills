# Board flow diagnosis: why cards are not moving

Use when Deep asks for the state of the board, why cards are not moving, how to keep them
moving, or what happens if a system is switched off. Section 2 of SKILL.md covers one stuck
card; this is the board-wide read that answers the whole class.

## Read order (one batch, before any claim)

Three sources, all read-only:

1. `~/.hermes/kanban.db` through Python's `sqlite3` in `python3 - <<'EOF'` (or `execute_code`).
   Never the shell `sqlite3 -json` CLI: card bodies carry control characters, the output
   corrupts, and you end up chasing a card that is not the one in the error.
2. `~/.hermes/state/kanban_quota.json` — live admission state (see
   `model-routing` → `references/subscription-first-routing.md` for the reserve and tier rules).
3. `~/.hermes/logs/gateway.log`, grep `kanban dispatcher` — the concurrency ceiling actually
   observed, which is what `spawned=N` per line says. The config's cap is the intent, this log
   is the fact.

Batch these reads in one turn. The answer is always a comparison of rates, so a partial read
produces a plausible-sounding but wrong diagnosis.

Queries worth having ready:

```sql
-- composition
select status, count(*) from tasks group by status order by count(*) desc;
-- rate in vs rate out, same window
select count(*) from tasks where created_at > strftime('%s','now','-7 days');
select count(*) from tasks where completed_at > strftime('%s','now','-7 days');
-- why runs ended (the health of the drain, not of the queue)
select outcome, count(*) from task_runs where started_at > strftime('%s','now','-7 days')
 group by outcome order by count(*) desc;
-- per-lane run cost, finds a hung worker that holds its whole lane
select profile, count(*),
       avg(ended_at-started_at)/60.0 avg_min, max(ended_at-started_at)/60.0 max_min
  from task_runs where started_at > strftime('%s','now','-7 days') group by profile;
-- which lane is refusing work, and why cards park
select kind, count(*) from task_events
 where created_at > strftime('%s','now','-7 days') group by kind order by count(*) desc;
-- blocked reason lives on the latest 'blocked' event, not in a tasks column
```

A fast board-wide admission view exists and is cheaper than all of the above when the
question is only "why is nothing spawning":
`hermes kanban dispatch --dry-run --max 3 --json` (it prints the event kinds for the whole
queue). Use it first when the question is dispatch, not flow.

## The four numbers that answer "why aren't they moving"

1. **Arrivals per day against completions per day, over the same window.** If arrivals exceed
   completions, the queue grows at a fixed rate and no speedup of the lanes will ever drain it:
   report the net per day, not the two totals, because the totals alone read as "busy".
2. **Dispatchable backlog** (`ready` + `todo` + `triage`) and days to clear it at today's
   completion rate. This is the number that tells Deep whether the board is a queue or a
   parking lot.
3. **Observed concurrency**: the `spawned=N` lines plus `kanban.max_in_progress` and
   `kanban.max_in_progress_per_profile` in config. A ceiling of 3 total and 1 per profile
   means seven lanes serialize; the ready count is then irrelevant to throughput.
4. **Lane headroom**: which pools are at their reserve right now, from the quota state file's
   `snapshots` (`used_percent` per window), `reserves`, `allowed_profiles`, `caps_live`,
   `running` and `target_concurrency`. A lane at reserve is closed regardless of how much work
   it has.

Add median and p90 hours from `created_at` to `completed_at` for cards finished in the window.
A board whose cards take a day to finish while intake runs hourly is not stalled, it is
understaffed, and saying so changes the recommendation.

## Interpretation: signal, meaning, move

| Signal | Meaning | Move |
|---|---|---|
| `skipped_nonspawnable`, grouped by `assignee` | That lane already holds its one card (per-profile cap), or it is off the allowlist | Waiting clears an allowlist block, never a profile-cap block; raise the cap or rotate the lane |
| `dependency_wait` with `parent_not_done` | Every `todo` card is parent-gated | Prove it with this event count before calling a `todo` pile stranded work; fix the parents, not the children |
| `scheduled` whose latest scheduled reason starts `SHELF` | A decision waiting on Deep, not timed work | Waiting on Deep is `blocked` + SHELF; report the sum, never the blocked column alone (1f) |
| `respawn_guarded` with `active_pr` | Held for an open PR, deliberately | Not a crash, not stuck |
| `crashed` / `spawn_failed` / `gave_up` outcomes | Spawn-failure class | Section 6, repair the class before releasing anything |
| One profile's `max_min` in hours while its `avg_min` is minutes | A hung worker holds that lane, and the cap is 1 per profile | `reclaim` it; one zombie stalls every queued card behind it |
| `allowed_profiles: []` with `caps_live: true` and `running` at the cap | Full board, self-clearing | Wait; report it as capacity, not as a freeze |
| `allowed_profiles: []` with free slots, or `caps_live: false` | Guard failure froze every lane | `model-routing` → `references/subscription-first-routing.md`, the guard section |

Two readings to distrust: a status column without its event kinds (the same `ready` count means
"queued behind a full lane" or "off the allowlist" depending on the event), and a "blocked is
healthy" claim taken from the blocked column alone while a shelf of hundreds sits beside it.

## "What would happen if we switched it off" is a dependency inventory

Answer it by listing what writes into the system, not by listing its features:

```bash
python3 - <<'EOF'
import json, os
jobs = json.load(open(os.path.expanduser('~/.hermes/cron/jobs.json')))
for j in jobs:
    txt = (j.get('prompt') or j.get('command') or '')
    if '<the system name>' in txt or 'kanban' in txt.lower():
        print(j.get('id'), j.get('enabled'), j.get('schedule'), (j.get('name') or '')[:50])
EOF
```

Then state the three consequences separately, because they have different costs:

1. **What freezes**: the drain. Completions per day go to whatever the replacement provides.
2. **What keeps running anyway**: every intake job above keeps writing until each is disabled
   individually, so switching the drain off without the intake produces a silent pile, not a
   stopped system.
3. **What is never lost**: the durable store (path, attachments, dependency graph, run history)
   and whatever the system was a queue *for*. The demand that arrived as mail, meetings and
   chat does not go away with the queue; it reappears wherever else it is routed.

Intake machinery being larger than drain machinery is the finding worth reporting: it means
the backlog is produced by design, not by slow workers.

## What to report

Lead with the one rate comparison that explains the behaviour, then the composition table,
then the ceiling and lane headroom, then the decision shelf. End with one recommended change
and the reason it is first. Name counts and paths for every claim (status counts, event
counts, the config keys, the state file), and flag anything you did not check as unverified
rather than omitting it: a diagnosis with a stated gap is reusable, one with a plausible gap
is not.
