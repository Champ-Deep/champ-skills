---
name: schedule
description: "Create or migrate scheduled tasks in Hermes cron."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [scheduling, cron, migration, automation]
    related_skills: [hermes-agent]
---

## When to Use

The user wants something to run automatically (a recurring report, monitor, sync, sweep) or asks to move an existing schedule from another scheduler into Hermes. Not for one-off work or parallel subtasks: use `delegate_task` for those.

You are creating a reusable shortcut from the current session. Follow these steps:

## 0. Check whether the job already exists

Before creating anything, list the existing scheduled tasks and read the script
they run. The user's request ("a scheduled task to check X regularly") often
describes a monitor that already runs and only lacks a check. Extend the
existing script's config instead: two crons probing the same targets double
the alerts and then disagree with each other. A new card is warranted only
when nothing currently watches those targets.

## 1. Analyze the session

Review the session history to identify the core task the user performed or requested. Distill it into a single, repeatable objective.

## 2. Draft a prompt

The prompt will be used for future autonomous runs — it must be entirely self-contained. Future runs will NOT have access to this session, so never reference "the current conversation," "the above," or any ephemeral context.

Include in the description:
- A clear objective statement (what to accomplish)
- Specific steps to execute
- Any relevant file paths, URLs, repositories, or tool names
- Expected output or success criteria
- Any constraints or preferences the user expressed

Write the description in second-person imperative ("Check the inbox…", "Run the test suite…"). Keep it concise but complete enough that a fresh session could execute it cold.

## 3. Choose a taskName

Pick a short, descriptive name in kebab-case (e.g. "daily-inbox-summary", "weekly-dep-audit", "format-pr-description").

## 4. Determine scheduling

Decide whether the task is recurring or one-off:
- **Clearly one-off** (e.g. "refactor this function") → omit the cron expression.
- **Clearly recurring** (e.g. "check my inbox every morning") → include an appropriate cron expression.
- **Ambiguous** → propose a reasonable schedule and ask the user to confirm (Hermes: the `clarify` tool; Claude: `AskUserQuestion`) before proceeding.

**IMPORTANT: Cron expressions run in the user's local machine timezone, NOT UTC.** Use local times directly in the cron expression. For example, if the user asks for "8am every Friday", use `0 8 * * 5` — do NOT convert to UTC.

Finally, create the job with the platform's scheduling tool: `create_scheduled_task` in Claude Cowork, or the `cronjob` tool (`action: create`) in Hermes. Hermes cron fields follow the same local-timezone rule as above.

## Migrating an existing schedule into Hermes

When the ask is to move a batch of tasks from another scheduler (Claude Desktop, crontab, CI cron) into Hermes one-for-one:

1. **Take cadence from the source's own dump, never from memory or chat prose.** Convert UTC source fields to local time once, keep every other cron field byte-identical, and build a parity table (source task, source cron, Hermes job name, id, first fire) before creating anything. Check `hermes cron list` first so two jobs never watch the same target. Parity of cadence does not extend to the minute: if an existing Hermes job writes the same shared file (a task list, an index, a log), move the migrated job's minute off that job's slot, because two agent runs appending one file in the same minute interleave and corrupt each other's writes.
2. **Classify each source task three ways.** Deterministic checks, builds and syncs become no-agent `--script` jobs. Judgment work becomes an agent job whose prompt is a shared substitution header plus a pointer to the spec file already on disk; never paste a whole spec into the prompt. A source prompt you cannot read gets reconstructed from that task's output artifacts, and the reconstruction is flagged in the report and the registry. Before classifying, diff the task against jobs Hermes already runs: a source task that overlaps an existing job is migrated in part only, and the dropped half goes into the new job's prompt with the reason it was dropped, otherwise a later session reads the spec on disk and restores the duplicate.
3. **Prove every script before scheduling it:** first run, an immediate second run that must emit zero bytes, and a simulated failure that must alert. A monitor that has never fired is untested.
4. **Never fire an agent job as a test run.** Migrated jobs write into real systems (vault, mail, tickets). The first scheduled fire is the test; confirm its delivery after it runs.
5. **Register each new job** in the vault's automation registry with id, cadence, outputs and per-job gaps. Schedule parity is not data parity: a capability the source had and Hermes lacks is a named gap on that row, not a silent omission.
6. **Create jobs with the cron tool in batched calls**, not a shell loop: long prompts pushed through shell quoting and an approval gate can fail wholesale, while batched tool calls return job ids you can verify immediately.
7. **End on a decision card, not a report.** A migration leaves both schedulers live until the source copies are paused, and only the user can pause them, so the risk window stays open no matter how good the parity table looks. Put every open ruling in one kanban card in `blocked` status: which source copies to pause and when (recommended: the day after the copy's first successful fire, so no window is covered twice or zero times), any source task that overlaps a job Hermes already runs, and anything deliberately left on the source harness with the reason. Recommendation first, options numbered for a one-line reply. Report the card id in the final message alongside the parity table.

Substitution-header contents, the no-agent script contract and the registry row format live in `references/migrating-schedules.md`.

## Deterministic work runs as a no-agent script job

A recurring check that needs no judgment (a ranker, a sweep, a digest, a verifier) must not
burn a model run. Give the script `--selftest` and run it before scheduling; a scheduled
script has no session to notice it is wrong.

```bash
hermes cron create "<cron or 30m>" --name <kebab-name> --script <file.py> \
  --no-agent --deliver local --failure-deliver local
```

- `--script` takes the file name under `~/.hermes/scripts/`, not a path.
- `--deliver local` keeps stdout out of chat and `--failure-deliver local` keeps a broken
  job from nagging; report the job by the `hermes cron create` row itself (name, schedule,
  next run), which is the only proof the schedule took.
- A shadow job writes its proposals to a dated file in the vault instead of delivering
  anything. Promotion from shadow to acting is a decision for Deep, recorded in
  `factory-decision-gate`, not a flag you flip while editing the job.
- A job whose first fire should wait on a human review ships paused:
  `hermes cron create ... --paused --paused-reason "<the review owed>"`. It then sits
  visibly in `hermes cron list` and promotes with one `hermes cron resume <id>` named
  in the decision card, instead of pinging the user with output nobody has judged.
  Use it for message-producing jobs (briefs, digests); shadow (above) is for jobs that write.
- Read the script's flags from its own `--help` before wiring it; a `--no-agent` job runs
  the script exactly as declared, so a flag that does not exist fails on the first fire.

**Watching live state (sessions, cards, queues): use the change-gated shape.** Copy
`templates/change-gated-watch.py` instead of starting from scratch. The contract it
encodes: `snapshot()` reads current state (DBs opened `file:...?mode=ro`, read-only), `evaluate()`
diffs structured fields (counts, ids, status, error) against the last snapshot persisted in a
state file, and only changed elements print. Compare structure, never raw text: a timestamp or
pid inside the payload would fire a false alert every run. Save the new snapshot even when
printing nothing, or the next run re-reports the same change. Ship `--selftest` (first run
reports, immediate rerun silent, simulated failure alerts) and `--force` (full report on demand),
run the selftest before scheduling, then prove first run / silent second run as in step 3 above.

## Reconcile dedupe state before producing anything

An agent job that picks "today's item" from a state file (a log, a queue, a manifest) must reconcile that state against the artifacts actually on disk before it creates anything new. State and disk drift apart whenever items are written outside the job: a batch pre-written into one file, a run that died between state append and file write, or a human who edited the file. Without the check the job re-produces an item the state says already exists, and the duplicate lands in a real destination (a card, a post, a send) before anyone notices.

Assert both directions: a state row with no artifact means draft it from the batch source; an artifact with no state row means stop and report, do not overwrite. Put the assertion in the prompt as an explicit early step, because a fresh session sees only the prompt, never the drift it was written against.

## Changing a rule across jobs that already exist

When a standing rule (voice, formatting, addressing, delivery target) is wrong for several existing jobs, do not leave the old wording in place and add a note: each job's prompt is independent, so a stale sentence keeps firing until it is edited out.

1. Write the rule once as a skill, then attach it with `--add-skill` rather than pasting the rule into every prompt.
2. Edit each prompt in one batched pass, replacing the stale sentence (not appending a correction below it), via `hermes cron edit <job_id> --prompt "$(cat <scratch-file>)" --add-skill <skill>`. Write each long prompt to a scratch file first: quoting a multi-line prompt inline through the shell is where edits fail silently.
3. Re-read the job records from disk and assert three things per job: the old sentence is gone, the skill is attached, the new rule is present. A zero exit code only proves the CLI accepted the edit.
4. Never fire an agent job as a test run (see migration step 4); the first scheduled fire is the test.

## Related

[[Skills MOC]]
