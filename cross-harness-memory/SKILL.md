---
name: cross-harness-memory
description: Use when wiring or querying cross-harness session capture.
version: 1.0.0
author: Deep + Hermes
license: MIT
metadata:
  hermes:
    tags: [memory, session-capture, beacon, cross-harness, setup]
    related_skills: [hermes-agent]
---

# Cross-harness session capture and memory

## When to Use

- Setting up, verifying, or repairing cross-harness session capture (the daemon, its
  hooks into Hermes config, its agent skills).
- A build, deploy, or setup step fails in a way that earlier work in another harness
  may already have solved, and the user asks "have we seen this before" or "what did we
  learn last time".
- The user asks what a past session in a different harness (Claude Code, Codex, Cursor)
  did or decided.

Not for: routine edits in a repo already worked in this session, or reading raw session
history when the user only wants current task context.

Multiple agent harnesses run on this machine (Hermes in several profiles, Claude Code,
Codex, Cursor). Work and corrections learned in one harness never reach the others unless
something captures the sessions into one store and a person reviews the reusable lessons
into project memory.

The capture layer in use is **Beacon**, run in **Local** mode: a CLI daemon writing a
local SQLite store plus a JSONL runtime log. Nothing leaves the box except the one
evaluator step that scores which sessions are worth reviewing.

## Rule: a memory is not a session log

Two layers, deliberately separated:

| Layer | What it is | Who writes it |
|---|---|---|
| Raw traces | Every session, every harness, unreviewed. Contains prompts, commands, output. | The daemon, automatically |
| Project memory | Reviewed, approved lessons with applicability scope. | A person, through a review loop |

Never present raw trace content as what the project knows, and never skip the review
step: an unreviewed lesson that turns out wrong gets applied to future work by every
harness.

## Procedure: install and verify capture

Run as a real setup task, not as a side effect of another job.

1. **Check what already runs** before installing anything: `beacon version`, then
   `beacon endpoint status` / `beacon endpoint doctor`. An existing install may belong to
   another profile or be in Cloud mode, which forwards sessions off-box.
2. **Install the CLI** with the system package manager, then run the installer's
   hook step explicitly: `brew install asymbo-labs/beacon/beacon`, then
   `beacon endpoint install`.
3. **Back up the config first.** The hook installer rewrites `~/.hermes/config.yaml`
   wholesale (or the active `$HERMES_HOME`), which reorders every top-level key
   alphabetically. The semantic content survives; diffs against an old backup are
   noisy from then on, so keep one backup before and treat reorder-only changes as
   expected, not as damage.
4. **Verify the hooks actually landed** by comparing parsed config, not raw text:
   read the file as YAML and diff the resulting dictionaries. This is the only
   reliable check after a wholesale rewrite.
5. **Backfill existing history** so old work is not invisible:
   `beacon endpoint traces reindex`.
6. **Prove capture end to end**, do not assume it: run one fresh session in the target
   harness, then grep the runtime log (`~/.beacon/endpoint/logs/runtime.jsonl`) for that
   session's ID and confirm both a start and an end event. Verify the event count for
   each harness with `beacon endpoint status --json`.

## Make the learned skills visible to the harness

The capture CLI installs its own agent skills into `~/.agents/skills/`. Hermes does not
scan that directory, so they stay invisible. Symlink the ones you want Hermes to load:

```bash
mkdir -p ~/.hermes/skills/beacon
ln -sfn ~/.agents/skills/<skill-name> ~/.hermes/skills/beacon/<skill-name>
hermes skills list | grep <skill-name>
```

Confirm they show as enabled before telling anyone they are available. Re-run the
symlink whenever the installer refreshes `~/.agents/skills/`.

## Run the memory loop

Scoring which sessions are worth reviewing calls a hosted evaluator (networked, costs a
fraction of a cent per trace, and sends trace projections off-box). Everything else is
local. Two paths:

- **With consent to score:** dry run first to see selection and cost, get an explicit
  yes, then run for real.
- **Without it:** skip scoring, read the traces yourself, and write each candidate
  directly with `beacon memory candidates create`. This is the default path whenever
  no evaluator key is exported.

In both paths the lesson is written by the agent from the trace's events and approved by
the person, never left as a placeholder. Check for an existing memory with the same
meaning before filing, and prefer superseding over adding a near-duplicate.

## Verify the loop closes

After approving a candidate, the proof is not the approve call's exit code:

1. `beacon memory list --project <path>` shows the new memory (scoping means a bare
   `list` from the wrong directory returns empty).
2. `beacon memory skills preview <candidate-id>` renders a valid Agent Skill with the
   lesson and its evidence trace cited.
3. The evaluator keys check is `test -n "${TYPESAFE_API_KEY:-}"` style, never printing
   the value.

## Boundaries

- Local mode only. Do not switch an existing install to Cloud mode (forwards sessions
  off-box) or run `beacon mcp connect` without the user asking for the cloud path.
- Traces hold prompts, commands, and output. Never paste them into memory, tickets, or
  chat beyond what supports the lesson, and never file anything credential-shaped.
- Never edit `memory.db` or the runtime log directly.
