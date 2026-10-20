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

1. **Take cadence from the source's own dump, never from memory or chat prose.** Convert UTC source fields to local time once, keep every other cron field byte-identical, and build a parity table (source task, source cron, Hermes job name, id, first fire) before creating anything. Check `hermes cron list` first so two jobs never watch the same target.
2. **Classify each source task three ways.** Deterministic checks, builds and syncs become no-agent `--script` jobs. Judgment work becomes an agent job whose prompt is a shared substitution header plus a pointer to the spec file already on disk; never paste a whole spec into the prompt. A source prompt you cannot read gets reconstructed from that task's output artifacts, and the reconstruction is flagged in the report and the registry.
3. **Prove every script before scheduling it:** first run, an immediate second run that must emit zero bytes, and a simulated failure that must alert. A monitor that has never fired is untested.
4. **Never fire an agent job as a test run.** Migrated jobs write into real systems (vault, mail, tickets). The first scheduled fire is the test; confirm its delivery after it runs.
5. **Register each new job** in the vault's automation registry with id, cadence, outputs and per-job gaps. Schedule parity is not data parity: a capability the source had and Hermes lacks is a named gap on that row, not a silent omission.
6. **Create jobs with the cron tool in batched calls**, not a shell loop: long prompts pushed through shell quoting and an approval gate can fail wholesale, while batched tool calls return job ids you can verify immediately.

Substitution-header contents, the no-agent script contract and the registry row format live in `references/migrating-schedules.md`.

## Related

[[Skills MOC]]
