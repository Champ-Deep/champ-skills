# Lane prompt anatomy

A lane prompt is read cold by a child that shares no context with you. Every field exists to remove a decision the child would otherwise make wrong, or stop to ask about. Copy the skeleton, fill every bracket, and never leave a field as a prose aspiration.

```text
GOAL          one sentence: the observable end state (branch pushed + PR open,
              test output pasted, file at an absolute path).
WORKSPACE     absolute worktree/repo path, branch name, base commit, and an
              explicit `cd` as the first instruction.
OWNERSHIP     files/dirs this lane may write; files it may never touch;
              its own port, database copy, and build output.
CONTRACT      exact exports / ids / interfaces another lane or your code will
              consume, plus the command that proves it runs. A lane that picks
              its own API returns something that cannot be wired in without
              renegotiating it.
GATES         exact commands in order, and what exit 0 means. Include the
              no-em-dash style scan over changed files.
WIP RULE      commit immediately after reading your diff, then after every
              step. Work that lives only in a dirty worktree dies with the
              session and cannot be resumed from.
REPORT        the fixed format below. Never a transcript retelling.
STOP          if a decision needed to continue is not in this prompt, stop and
              report it. Do not invent product decisions unattended.
```

The eight non-negotiables in SKILL.md (no dashes, no merge to default, no credential values, real verification output, containment before deletion, touch only your repo, stop on unknown decisions, per-branch merits verdict) are carried in every prompt verbatim, not summarized.

## Report contract

Fix the fields so review never requires reading a transcript. When dispatching through `delegate_task`, pass the same shape as `output_schema` so summaries arrive structured:

```text
status        done | blocked | needs-decision
commits       SHAs pushed, with branch
commands      each gate command and its exit code, plus the output line that proves it
gates         pass/fail per gate, counts exact ("29 passed, 1 failed", never "tests pass")
changed       file paths touched
not_verified  anything claimed but not actually executed, named explicitly
decisions     what the human must choose, each with the options and your recommendation
```

A lane's report is a self-report. Before relaying any claim that has an external handle (PR state, artifact path, deployed URL), re-verify it yourself with the command that reads that handle back.

## Wiring the chain

When lanes must run in sequence and then be combined, create the downstream task at dispatch time as a kanban card with `parents: [<previous lane task id>]`, and chain each lane the same way. Completion then promotes the next card automatically instead of depending on the human typing "continue" in chat, and each lane's comment can state what the next card expects of it.
