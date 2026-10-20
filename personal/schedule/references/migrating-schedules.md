# Migrating a scheduled-task batch into Hermes

Depth for the SKILL.md migration section. Read once when moving three or more tasks from an external scheduler.

## 1. Inventory and parity table

- Run `hermes cron list --json` first. Two jobs on the same targets double the work and then disagree with each other.
- Read cadences from the source system's own export (Claude Desktop scheduled-task snapshot, `crontab -l`, workflow cron blocks). Never rebuild a schedule from conversation memory.
- Sources often store UTC while Hermes cron runs in local time. Convert once, and show both columns in the table so a bad conversion is visible.
- Table columns: source task, source cron, Hermes job name, job id, first local fire, known gap. This table is the approval artifact: the user pauses source jobs only after confirming it.

## 2. Classification of each source task

| Kind of task | Hermes shape | Notes |
|---|---|---|
| Deterministic check, build, sync | no-agent `--script` job | script under `~/.hermes/scripts/`, `chmod +x`, `bash -n` before use |
| Judgment work with an existing spec file | agent job: shared header + "read `<spec path>` and execute with these changes" | prompt stays short; the spec on disk stays the source of truth |
| Source prompt unreadable | agent job reconstructed from the task's output artifacts | flag the reconstruction in the report and the registry row |

## 3. Substitution header (agent jobs)

Every migrated agent prompt opens with the same header, then per-job steps:

1. Provenance: which scheduler and task this was migrated from.
2. Environment: working directory, vault root, and that there is no source-app layer here.
3. Path and tool substitutions, stated positively:
   - source app's mounted paths -> real local paths
   - source app's artifact tools -> "edit the file on disk, and say in your report the hosted artifact copy was not pushed"
   - each source connector name -> the actual MCP tool names available
   - integrations with no equivalent here -> the nearest substitute plus "report any gap in one line, never fail the run over it"
4. Standing output rules of the vault (protected files, link policy, punctuation rules).
5. Report contract: short, headline first, glanceable, because delivery lands in a chat channel.

Per-job spec differences follow the header. Do not fork the header per job.

## 4. No-agent script contract

- The cron runner delivers stdout verbatim: empty stdout sends nothing, any stdout is a message, non-zero exit or timeout is an alert. The success path prints nothing; write to files instead.
- Test matrix before scheduling: (a) first run, which may initialize a baseline and may print once; (b) immediate second run, must be exactly 0 bytes; (c) simulated failure or drift, must print and exit non-zero; (d) restore state after (c).
- Keep comparison baselines and state files outside the vault (for example `~/.hermes/state/`), so no hygiene pass sweeps them.

## 5. Create and verify

- Batch cron tool calls in one message: name, schedule, prompt or script, deliver target, workdir, skills. Shell-looping `hermes cron create` passes long prompts through quoting and an approval gate and can fail wholesale with nothing created.
- Verify by reading back: grep `hermes cron list` for the intended names, count equals the batch size, and each `next_run_at` matches the parity table.

## 6. Registry and handoff

- One registry row per job: job name, id, cadence in local time, source of truth (spec file or script), what it writes to, known gap versus the source system.
- Add a dated pointer in the source system's own inventory note so the next session knows the migration happened.
- Final report: the parity table with first-fire times, then an explicit "gaps to know before you pause the source" list.
- Do not pause or delete source jobs yourself. Parity confirmation is the user's call; irreversible deletions always go to them.
