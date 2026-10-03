---
name: parallel-agent-lanes
description: Use when running parallel agent lanes across repos.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [orchestration, parallel, lanes, tmux, multi-repo, planning, agents]
    category: autonomous-ai-agents
    related_skills: [sprint-mode, stalled-repo-rescue, github-portfolio-audit]
---

# Parallel agent lanes

Use a bounded window of capacity (a free tier, a credit balance, an overnight, a
"2 days") to advance several repos at once, where the human reviews only short
reports instead of transcripts.

The deliverable is a lane plan plus paste-ready prompts plus a launcher. Running
the lanes is the user's call, not yours.

## 1. Measure the ceiling before planning against it

The request almost always arrives framed as "I have X of Y left, help me use it."
The premise is frequently wrong, and planning around it wastes the whole window.

Before building anything, establish four facts:

1. **Price**, from the platform's structured catalog entry, not from memory or a
   docs page. Per-token, per-second, and per-request units differ and decide
   viability.
2. **Concurrency headroom.** Fire a burst at the parallelism you intend to use and
   count non-2xx responses. Zero rejections means parallelism is not the
   constraint; stop worrying about it.
3. **Real cost attribution.** Read the account's usage counter, make one controlled
   call of known size, read it again, compare the delta. Then find what actually
   consumes the budget. In a fanout architecture the primary model is often free
   while reference, auxiliary, vision, or summarizer models do the spending.
4. **What the allowance counter does under load.** If a documented per-day counter
   does not move across a burst, that counter is not the gate for this workload.

Then state the finding **before** the plan, in a short table of measured values.
If the named scarce resource turns out not to be scarce, say so plainly and
re-optimise for whatever is actually binding. Review bandwidth is usually the real
ceiling.

Never report a config lever as working unless you verified its effect at runtime.
A config reader that prints a "key not recognised" warning is reading a file, not
the running system. Verify by observing behaviour across a call, and if you could
not verify it, label it unverified rather than dropping the caveat.

## 2. Select lanes on one test

**Is there finished work that is one push away from existing?**

Not "what is interesting to build." Anything needing a product, copy, or design
decision from the user is not a lane. Prefer work that is already committed,
already tested, already drafted, and merely unpushed.

Look specifically for:

- a branch with commits, a clean tree, and no remote counterpart. **That is the
  highest-value item in most audits and it is usually one command.** Say so at the
  top of the plan.
- a secret sitting untracked and unignored. Always goes first in its lane,
  regardless of the lane's other work, because it is one careless command away
  from permanent.
- a repo with tests but no CI on the default branch.
- a repo nobody has opened in months, where "does it still run" is the deliverable
  and a failure is a legitimate finding.

One lane per repo. Lanes never touch each other's repo. State that constraint in
each prompt.

## 3. Optimise for review cost, not token efficiency

The plan's purpose is to be approved, not to be thorough. Every lane ends in a
fixed-format short report, and the whole plan is sized so total human time is about
one hour per block.

- Fix the report line count per lane and specify the fields. Approximation by
  reading a transcript does not happen when the transcript never gets read.
- Put the entire user-facing timeline in the plan: when to launch, when to stop
  reading, when to review, when to merge.
- Say plainly what happens if the user finds themselves reading a transcript during
  a block. The lane prompt is wrong, not their discipline.
- Deliver plan, measurements, prompts, and launcher as separate files with `MEDIA:`
  absolute paths. A long plan pasted into chat is unreadable and unversioned.

## 4. Per-lane repo hazards worth checking first

Each of these has cost real time and each generalises:

- **A directory with no `.git` nested under a repo.** Git resolves upward, so
  `git add -A` from inside it stages the parent tree. Confirm with
  `git rev-parse --show-toplevel` before letting any agent write there. If the
  parent is a home directory with no remote and zero commits, the blast radius is
  everything.
- **A publish path with no gate.** A script that clones, rsyncs, commits, and
  pushes straight to the default branch means any edit reaches production with no
  PR and no review. Scope that lane to additive work only, and tell the lane not
  to run the publish script.
- **Untracked credential backups versus ignore patterns.** Patterns like `.env`,
  `.env.*.local`, `.env.production` all miss `.env.something.bak`. Enumerate the
  real files on disk and run `git check-ignore -v` on each. Never print a value:
  extract key names only, and say so in the prompt.
- **A documented schedule with no registered scheduler.** If a job is described in
  a README as running nightly, look in crontab, LaunchAgents, the agent's own cron
  store, and process managers. If nothing schedules it but the timestamps show it
  firing, the honest finding is that an interactive session did it, which means it
  has no owner and no guarantee.
- **A stale duplicate clone.** Two checkouts of one remote on different branches,
  one behind, is a confusion waiting to happen. Name both paths in the plan.

## 5. Prompt anatomy

See `references/lane-prompt-anatomy.md` for the full template and the reasoning.

Non-negotiable, and carried in **every** lane prompt so the user never repeats
them:

1. No em dashes, no en dashes, in any file or any report. Tell the lane to verify
   with a script over the changed files, never grep, and hold yourself to the same
   rule in your own deliverables.
2. Never merge to the default branch. Branch and PR only. No force-push.
3. Never print, commit, or report a credential value. Names only.
4. Real verification only. Paste the command and its output. "Should work" is not a
   result.
5. Delete no branch until containment is proven by command output.
6. Touch only the repo you were told to touch.
7. If a step needs a decision that is not in the prompt, stop and report it. Do not
   invent a product decision unattended.
8. Per-branch merits verdict before any cleanup recommendation.

## 6. Launch

One detached tmux session per lane, from `scripts/launch-lanes.sh`. Supports
`--status` to capture all panes and `--kill` to tear down.

**Multi-line prompts must go through a tmux buffer, not `send-keys`.** `send-keys`
interprets every newline as a submit, so a markdown prompt arrives as a dozen
fragmented turns. Use `load-buffer` then `paste-buffer -d`, then a single Enter.
Verify the paste path once against a throwaway session by diffing the delivered
file against the source.

Verify the agent's working directory before committing to a long run. Prompts
should open with an explicit `cd` to a shell-safe path, because a directory flag
is not guaranteed to change the working directory the agent's shell commands run
in. Where a real path contains characters that break shell quoting, create
symlinks with safe names and make every prompt use those.

Report plainly what you did not run, what you could not verify, and what remains
the user's decision. Silence reads as completion.

## Pitfalls

- **Do not plan against an unmeasured ceiling.** If the free tier is not the
  constraint, a plan built around rationing is the wrong plan.
- **Do not report state you measured earlier in a long session without
  re-measuring.** Work lands while you are surveying, and a stale claim becomes a
  wrong instruction in a prompt an agent will execute. Re-measure each repo
  immediately before writing its lane.
- **Never `send-keys` a multi-line prompt.** Fragmented turns, wasted window.
- **Never put a credential value in a plan, a prompt, a log, or a chat reply.**
  Names only, and prove the redaction worked before delivering.
- **Do not fold rescue work and new build work into one lane.** A lane that ends
  in a reviewable branch is worth more than a lane that ends in a debate.
- **Do not let the plan be the only artifact.** Prompts and the launcher must be
  files, not chat prose, or the next session rebuilds them from scratch.
- **A lane with no fixed report format will be reviewed by reading its
  transcript**, which is exactly the cost the plan was built to avoid.

## Supporting files

- `references/lane-prompt-anatomy.md` - the lane prompt template, field by field,
  with why each part exists and the failure it prevents.
- `scripts/launch-lanes.sh` - start, inspect, and tear down N detached tmux lanes
  from a prompts directory.