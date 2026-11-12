---
name: cross-model-review
description: Use when a medium or large change needs a second-model review.
---

# Cross-model review

Adapted from David Ondrej's `gpt-review` and `total-review` (davidondrej/skills, MIT), rebuilt for our lanes. The idea: a model reviewing its own family's work shares its blind spots, so one read by a different lab's frontier model removes most serious misses. Claude still adjudicates. Routing rule "do not delegate review" stands: the other model is a second reader, never the reviewer of record.

## When
- Medium, large or risky change (auth, billing, data, send paths, migrations). Skip tiny fixes.
- Run it ONCE per change. Repeating it invents findings because the reviewer was told to find bugs. A second pass is allowed only after a large fix list.
- `total-review` (every lab) is for huge risky changes only, a few times a week at most.

## How
1. Make a `frontend` profile kanban card pinned to `model="gpt-6-astra", provider="openai-codex"` (the exception in `model-routing`; it burns the ChatGPT window, so mediums can use the default Sol). Read-only: the brief says "review only, do not change files".
2. Brief is neutral: scope, paths, base revision, intended behavior. Do not name suspected bugs or a verdict. Ask for serious or critical issues, fixes, merge readiness, and verified versus uncertain findings.
3. Include this sentence word for word: "During your final answer, rate each issue from 1 to 10 on how often it would happen, and 1 to 10 on how bad it would be."

When no second-lab model is available (key capped, lane down), do the second read
yourself as a separate pass over the diff with the reviewer's questions, and label
it a same-family read in the report. That is weaker than a cross-lab read and far
better than one pass that manufactures confidence; never present it as
cross-model.

4. When it returns, ask yourself for each finding: must fix, or overthinking? Fix frequent and serious items. Skip rare and mild ones. Do not rerun the reviewer to confirm fixes unless the change touches money or customers.
5. If the card cannot run (key capped, lane blocked), say so. Never present partial output as a finished review.

## PR and branch review loop

When the change already exists as a branch with a PR, the second read is a
`delegate_task` subagent with a read-only contract, and the loop around it is
the part that matters. The "second reader, never the reviewer of record" rule
is unchanged at every step.

1. **Dispatch bounded and read-only.** One subagent, or two in parallel on a
   large diff. The brief must carry what the diff cannot: absolute worktree
   path and branch, the SHAs to read (`git show <sha>`,
   `git diff origin/<base>...HEAD`), the product context and the rules the code
   is trying to honor (auth, tenancy, send paths, queues), an explicit
   "read only: do NOT edit, commit, push, merge or comment on GitHub or on any
   task card", the run budget, and the verdict format below. Brief skeleton:
   `templates/review-brief.md`.
2. **Require an evidence-shaped verdict:** `verdict: PASS | BLOCK`, then each
   original finding with `closed / partly closed / open` and file:line
   evidence, then new findings with severity, file:line, the concrete failure
   scenario and the smallest fix. End with "report only what you verified by
   reading code; mark anything else unverified". A verdict without file:line
   is a summary, not a review.
3. **A reviewer report is a lead, not a fact.** Open every file it names and
   confirm the path exists and the failure can actually happen before changing
   anything. Discard findings that describe a guard already doing the job, and
   weigh each proposed fix against the honest caller: a rule that blocks a
   legitimate workflow to close a corner case costs more than the corner case.
4. **Fix as a new commit on the same branch.** Never force-push a head that has
   been reviewed: every file:line the reviewer quoted stops matching and the
   re-review restarts from zero. Name the finding each hunk closes in the
   commit body.
5. **Re-review the delta, not the whole PR.** This is the "second pass only
   after a large fix list" case above, scoped narrow on purpose. Second
   dispatch gets the fix SHA's `git show` and the original findings as a
   checklist to confirm `closed`, plus a look for regressions the fix
   introduced. Re-reading the full PR invites invented findings on code that
   did not move.
6. **Merge gate is two things at the same SHA.** Re-read
   `gh pr view <n> --json statusCheckRollup,mergeStateStatus,headRefOid` at the
   fix head (an earlier head's green proves nothing about the fix), and record
   the verdict on the task card as `REVIEW: PASS <sha>`. BLOCK from a second
   read is authoritative and stops the merge; PASS from a second read never
   authorizes it. Authorizing is the reviewer of record:
   `kanban_request_review(reviewer="reviewer")`, or `/review` before merge.

## Not for
Outside PRs on public repos: be skeptical that the issue is real and not an LLM-invented edge case. Ask whether a user actually hit it.
