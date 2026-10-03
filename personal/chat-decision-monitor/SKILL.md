---
name: chat-decision-monitor
description: "Watch Deep's other chats for open decisions and lost work."
version: 1.0.0
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

## Wiring

```
schedule: every 30m
monitor:  decision_watch.py      # change-gate, deterministic
deliver:  telegram:<chat_id>     # NOT 'local', or Deep never sees it
attach_to_session: true           # he can reply and the brief stays in context
```

## Gotchas hit while building this

- `cronjob_manage(enabled_toolsets=...)` serializes to a nested
  `[{"item": [...]}]` and then to a junk `[""]` on clear. The CLI has no
  toolsets flag at all. Fix in `~/.hermes/cron/jobs.json`, where the key is
  **`id`**, not `job_id`.
- A monitor job's first tick always runs as a baseline, so expect one report on
  create even with no change.
- `hermes cron incidents` and `hermes cron doctor` are the health checks; a late
  fire on an unrelated job is pre-existing noise.
- To read another session's exchange: join `messages` on `session_id`, order by
  `timestamp`, filter `role IN ('user','assistant')`, and bind parameters in
  order `(session_id, *roles, limit)`.
