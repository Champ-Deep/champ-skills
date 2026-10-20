---
name: repo-issue-autopilot
description: "Wire a repo's GitHub issues into scheduled kanban cards."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, kanban, automation, cron, agents]
    related_skills: [hermes-agent, sdlc-review, stalled-repo-rescue]
---

# Repo Issue Autopilot

## When to Use

Use when the user wants a repository's GitHub issues to keep moving without a
human relaying work card by card: scan open issues, dispatch them as agent
work, and return PRs for review. Also use when building or repairing the
scanner script, its cron registration, or the card bodies it creates.
Not for a one-off triage of a handful of issues (create those cards by hand),
or for reviving an already-stalled repo (that is `stalled-repo-rescue`).

Turn a repository's open GitHub issues into a self-sustaining queue of agent
implementation cards, on a schedule, without a human relaying work card by
card. The scanner is a `no_agent` cron script; the workers are kanban cards on
an implementation profile; the output is feature branches and PRs, never
merges.

## Standing rules (every instance of this class)

- **PRs only, never merge.** Every card body says implementation ends at a
  pushed branch and an open PR. Merging is Deep's decision, always.
- **One branch per card.** Related issues share one card and one feature
  branch (bugs together, a feature's subtasks together). Unrelated issues on
  one branch produce an unreviewable diff and a PR that blocks on its slowest
  item.
- **Skip issues assigned to a human.** An assignee is a decision someone
  already made; the scanner is for unowned work.
- **Every queued issue gets an `agent-queued` label plus a comment naming the
  card and branch.** The tracker stays truthful about what the agents are
  doing, and the comment is the audit trail from issue to PR.
- **Idempotency on every creation.** Cards are created with a deterministic
  key derived from repo + issue numbers, and the script keeps a local
  `queued` map, so a re-run or a double-fire never duplicates a card.
- **Diagnose before you dispatch.** Read the relevant code yourself first and
  put `path:line` proof and hard verification gates in the card body. A card
  handed a hypothesis instead of a diagnosis spends its first third
  rediscovering what you already know.
- **Dry run first, always.** The scanner prints what it would create; read it
  before any live run so a mis-batched grouping is caught while it is still
  text.

## Procedure

### 1. Inventory the repo's open issues

```bash
gh issue list -R OWNER/REPO --state open --limit 100 \
  --json number,title,body,labels,url,assignees
```

Group them: bugs on one branch, each feature (or coherent subtask cluster) on
its own. Cap each card at ~3 issues. Anything with a human assignee drops out.

### 2. Write the scanner as a quiet-when-idle cron script

A `no_agent` cron job runs a script on a schedule and **delivers its stdout
verbatim; empty stdout sends nothing at all**. So the script splits its
output: diagnostics go to **stderr**, and **stdout carries only the run
report** (created cards, warnings). The job then behaves as a watchdog,
pinging only when something changed.

State lives next to the script:

- `issue_autopilot_config.json` — repo list, assignee profile, labels,
  caps. Expand by appending a repo, not by editing code.
- `issue_autopilot_state.json` — `queued` map of issue key to card id.

Scanner logic per repo: list open issues, drop assigned and already-queued
ones, group the survivors, then per group: create the card, label the issues,
comment the card id back. `--dry-run` prints the plan and exits without
writing state. If `gh issue list` fails for a repo, record a warning event
and continue with the other repos rather than aborting the run.

Test it directly before scheduling (run the copy under this skill's
`scripts/`, or the live one under `~/.hermes/scripts/` once installed):

```bash
python3 issue_autopilot.py --dry-run
python3 issue_autopilot.py   # one live run, then inspect the board
```

### 3. Register the schedule

`cronjob_manage(action='create')` with `no_agent: true`, `script:
"issue_autopilot.py"` (paths resolve under `~/.hermes/scripts/`), a recurring
schedule like `every 2h`, and `deliver` set to where the report should land.
Verify the returned `next_run_at` and `enabled: true`; a create that comes
back paused or erroring is not a schedule.

Create cards with the CLI, not by hand, and check the flag names against
`hermes kanban create --help` before scripting: the goal-loop flag is
`--goal` (not `--goal-mode`), `title` is positional, and `--body-file -`
reads the body from stdin so embedded newlines and flag-looking lines in an
issue body survive. `--idempotency-key` is the dedupe: an existing card with
the same key returns its id instead of creating a duplicate.

### 4. Shape the card body so the worker needs no chat context

Dispatcher workers get a fresh session. The body must carry everything:

- the issue numbers, titles, and links, and which branch they share;
- the diagnosis you already did: `path:line` findings, the mechanism of the
  bug, and the intended approach;
- a workspace hint (existing local checkout path if one exists, so work
  continues in the real tree instead of a throwaway scratch dir);
- hard verification gates with the actual commands: `tsc --noEmit`, build,
  test suite with the specific assertions expected to pass;
- the contract: push `feature/...`, open a PR, do not merge, then
  `kanban_request_review`;
- goals measured by files changed, verification run, and PR opened.

Create it with `goal_mode: true` so a one-shot miss gets judged and retried in
the same session instead of silently completing. Set `assignee` to the
implementation profile and name the shared branch inside the body.

### 5. Verify the loop end to end once

- The card appears on the board and is claimed by the right profile
  (`kanban_list`).
- The issue carries the label and the comment.
- The worker's completion summary names a pushed branch and a PR URL; check
  the PR exists before repeating the word "done".
- The second scanner run creates nothing (idempotency proved, not assumed).

## Pitfalls

- **Chatty watchdog scripts spam the delivery channel.** If every tick prints,
  the user learns to ignore the job and misses the tick that mattered. Keep
  status on stderr; stdout is reserved for events.
- **A card with no diagnosis burns its budget rediscovering the bug.** Include
  `path:line` proof up front; the card body is the only context the worker
  gets.
- **Batching unrelated issues into one card couples their PRs.** Group by a
  shared branch, never by "they were all open at once."
- **Re-running a scanner without an idempotency key duplicates the queue.**
  Deterministic keys plus a local state file make every run safe to retry.
- **Queueing issues a human already owns invites work being overwritten.**
  Filter on `assignees` being empty.
- **Filing an issue you have not grounded in the code produces a card that
  implements a guess.** Read the code and cite lines first.
- **Scripting kanban creates from memory gets the flags wrong.** `--goal`, a
  positional title, and `--body-file -` for stdin are the real spellings;
  guess them and the card silently loses its body or its goal loop. Read
  `hermes kanban create --help` first.

## Supporting files

- `scripts/issue_autopilot.py` — the scanner/creator; configure it via
  `issue_autopilot_config.json` beside it, dry-run before the first live run.
