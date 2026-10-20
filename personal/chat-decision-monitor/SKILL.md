---
name: chat-decision-monitor
description: "Watch Deep's other chats for open decisions and lost work."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, monitoring, sessions, decisions, cron, state.db]
    related_skills: [hermes-agent]
---

# Chat decision monitor

Watches every Hermes chat except the current one, surfaces decisions that are
still open, and verifies risk claims against real repos before reporting them.
Long-running form: a `no_agent` cron script (`chat_digest.py`) that only speaks
when something changed.

## When to Use

- Deep asks to monitor, watch, or keep an eye on his other chats or sessions.
- He asks what is running, what is blocked, or what needs a decision from him.
- He asks whether work is at risk of being lost across repos or branches.
- Before a sync, standup, or end of night, to find what stalled.
- Any time a report about another chat's claims needs verifying rather than
  repeating.

Not for steering a running chat. This skill reports; it never injects.

## The one thing that is easy to get wrong

**A chat is RUNNING only if it holds an unexpired `session_turn_leases` row.**

```sql
SELECT conversation_id, acquired_at, expires_at
FROM session_turn_leases WHERE expires_at > strftime('%s','now');
```

`sessions.ended_at IS NULL` does **not** mean running. It means unfinished. On
Deep's box, 25 sessions had `ended_at IS NULL` while exactly 2 were actually
live. Reporting the first number as "active chats" overstates by 10x.

**Never inject into a live turn.** The lease exists to prevent exactly that. A
monitor reports; it does not steer the running chat.

## The green dots are NOT a running signal

Deep reads the green dot on a session tab as "running." Verified false. In a
screenshot showing 8 tabs, 6 had solid green dots while **exactly one session
held a lease** (this one). Green means something cosmetic (selection, health,
recent activity), not an in-flight turn. Idle times for those green tabs ranged
0.5h to 2.5h.

When Deep asks "which chats are running," answer from leases and say plainly
that the dots do not mean running. Misreading the dots makes 6 finished chats
look concurrent, which is how work gets double-assigned or a live turn gets
interrupted.

Also: a stale lease survives. `20260908_193251_2438ec` still held a lease row
24 days after its process died. Always compare `expires_at > now`, never just
"a row exists."

## Scan

`~/.hermes/scripts/decision_scan.py` is the scanner (read-only on `state.db`).
It separates live from idle, then mines the last ~18 messages of each recent
chat for four signal classes:

| class | meaning | example marker |
|---|---|---|
| `blocked` | could not complete | `I can't`, `401`, `no *_API_KEY` |
| `awaiting-you` | needs a human decision | `should I`, `approve`, `leave it for now` |
| `risk` | work that can be lost | `unpushed`, `no remote`, `CRITICAL` |
| `undelivered` | promise not yet landed | `has NOT yet been delivered` |

`~/.hermes/scripts/decision_watch.py` wraps it as a **deterministic fingerprint**
for cron `monitor` mode.

## Rules that make the output trustworthy

- **Verify every `risk` before reporting it.** Other chats' transcripts are
  claims, not facts. Real example: a chat reported "ChampLantern tree is clean"
  (true) and missed that 6 commits / 35 files / 5,023 insertions existed only on
  that laptop with no upstream. Run `git` and quote real numbers.
- **Run git for risk yourself; do not also mine the chat text for it.** The
  scanner's `risk` regexes are a second, weaker source on the same fact, so a
  script that already executes git should drop `risk` from its chat-signal set
  and keep only `awaiting-you` and `blocked`. Two sources disagree, and the
  transcript one is always the one that is wrong.
- **An `ahead`/`no-remote` count only means work at risk from commits not on a
  remote.** Check per branch: `git for-each-ref --format='%(refname:short)'` then
  `rev-list --count <branch> --not --remotes`. Glob excludes (`--exclude=backup/*`)
  do not behave as written against `refs/heads/...`, and a silent miss inflates
  the number you report; confirm the exclusion with that per-branch loop.
  `backup/*` branches are deliberate snapshots, not unpushed work.
- **`dirty >= 10` files, not `> 0`.** A couple of modified files is normal work
  in progress; reporting it trains Deep to ignore the line that matters.
- **No remote at all is the top severity**, not a footnote: every commit in that
  repo exists on one disk.
- **Age out stale decisions instead of nagging them forever.** A chat that has
  not spoken in 3 days drops out of the brief; it stops being a decision and
  becomes history.
- **Check undelivered promises** in `delivery_obligations` (`state != 'delivered'`).
- **Report blocked items as parked, not failed**, when Deep deferred them. Say
  what still needs him even if the blocker is a missing credential.
- **Green gates are a trap.** A merge-ready branch can be merge-ready and still
  carry a live RCE path. Call that out.

## Change-gate (this is what makes it tolerable)

Cron `monitor` compares output bytes to the previous tick; identical output
skips the agent entirely. Therefore the fingerprint **must not contain
timestamps or minute-level ages**, or every tick looks changed and the agent
talks every 30 minutes for nothing. Emit chat titles, session ids, and decision
kinds only.

## Secret sweep (run this whenever a chat mentions a key, token, or .env)

A `risk` finding about credentials is the highest-severity class. Verify it
properly:

```bash
git ls-files --error-unmatch <file>       # tracked?
git check-ignore -v <file>                # empty = NOT ignored
git add -An --dry-run . | grep <file>     # proves whether git add -A stages it
git log --all --diff-filter=A --name-only # secrets ever committed
gh repo view <owner>/<repo> --json isPrivate,visibility   # severity hinges on this
```

Lessons from a real sweep across Deep's repos:

- `.gitignore` rules like `.env`, `.env.local`, `.env.*.local` **do not cover
  `.env.openrouter.bak`**. The `.bak` suffix falls through every one. Add `*.bak`.
- `.env.openrouter.bak` was the single EXPOSED file across all of
  `/Users/deep/Apps&Projects`; every other `.env` was properly ignored.
- A secret can be in history while HEAD looks clean. HEAD only had
  `.env.example`, yet `.env.bak-2026-09-08` and `.env.bak-preswap` existed in
  commit `675cd50`, which was pushed to `origin/feature/gamified`. **History is
  the exposure surface, not the working tree.**
- Repo was `isPrivate: true`, which downgrades public-leak severity but not
  blast radius (org access, forks, clones, CI logs).
- Fix forward: tighten `.gitignore` and confirm `git add -An` no longer stages
  it. History rewrite is Deep's call, never unilateral.
- Never print secret values. Report key NAMES, value LENGTH, and a
  token-shaped yes/no.

## The brief must be a script, not an agent run

`decision_watch.py` in cron `monitor` mode still wakes an LLM, which costs a
model call per real change and then writes prose that reads like a status
report. The shape that works is a **`no_agent` job running a deterministic
script** (`~/.hermes/scripts/chat_digest.py`), which reuses
`decision_scan.summarize()` for decisions and runs `git` itself for risk.

Its `plan(current, state, now, hour)` is a pure function over a persisted
state file (`~/.hermes/state/chat_watch.json`), so it can be self-tested with
fixed clocks before it ever sends. Build it that way: gather -> plan -> save ->
print, with the print step the only side effect.

Rules each line of the brief follows (from agent-supervision threads:
Moltbook heartbeats, agent-tether, the Paperclip Telegram plugin):

- **Nothing changed, print nothing.** Empty stdout is quiet; every run must
  earn its message.
- **One batched message per run, and every line says why now**: `NEW` or
  `still open Nd`. Never one chat per line per run.
- **Re-nag on a backoff (1d, 3d, 7d), then stop.** A blocker reported on every
  tick is negative value: the alert loses all meaning and Deep stops reading.
- **Quiet hours** (02:00-15:00 IST) hold everything except commits that exist
  nowhere else, which is the one class worth waking him for.
- **One digest per day**, at the first run after 15:00: the full open list,
  sent even when nothing changed. New items are withheld from that run if they
  were already sent in the hourly batches.
- **He steers it in chat, not via buttons**: `snooze N [days]`, `done N`,
  `list`. Inline Telegram buttons need a gateway callback handler that does
  not exist yet, so do not promise tap-to-snooze.
- **Silent when idle, loud only about work that can be lost.** No dead-man
  switch exists: if the cron scheduler dies, nothing here can report that.

## Wiring

```
schedule: every 30m
script:   chat_digest.py         # no_agent: true, prompt: "", monitor_script: null
deliver:  telegram:<chat_id>     # NOT 'local', or Deep never sees it
enabled_toolsets: null           # see Gotchas; [] strips every tool
```

`decision_watch.py` remains the change-gate fallback if a job must stay in
`monitor` mode.

**Verify a no-LLM job by running it, not by reasoning about it.**
`hermes cron run <id>` fires it immediately and writes the exact deliverable to
`~/.hermes/cron/output/<id>/<YYYY-MM-DD>_<HH-MM-SS>.md`. Read that file: a job
reporting `succeeded` proves the process exited 0, not that the message is the
one you intended (a quiet-hours hold and a failure look identical from the
exit code).

## Gotchas hit while building this

- `cronjob_manage(enabled_toolsets=...)` serializes to a nested
  `[{"item": [...]}]` and then to a junk `[""]` on clear. The CLI has no
  toolsets flag at all. Fix in `~/.hermes/cron/jobs.json`, where the key is
  **`id`**, not `job_id`.
- **`"enabled_toolsets": []` on an agent job means it has zero tools.** It
  then fails every single run with `no command-execution tool` and mails a
  failure alert each tick, which looks like a broken watcher rather than one
  bad config field. The correct value is `null` (default toolsets). Symptom to
  recognize: the same cron failure notification repeating on every schedule.
  When editing `jobs.json` by hand, copy it to `jobs.json.bak-<reason>` first,
  write through a temp file, then `os.replace`, because the gateway holds it.
  Edit with the patch tool, never `sed -i` (BSD sed needs `-i ''` and eats the
  script when it does not get it).
- A monitor job's first tick always runs as a baseline, so expect one report on
  create even with no change.
- `hermes cron incidents` and `hermes cron doctor` are the health checks; a late
  fire on an unrelated job is pre-existing noise.
- To read another session's exchange: join `messages` on `session_id`, order by
  `timestamp`, filter `role IN ('user','assistant')`, and bind parameters in
  order `(session_id, *roles, limit)`.
