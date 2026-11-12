# Review brief (copy, fill the brackets, dispatch read-only)

Goal: [one line: what the change must do, and for whom]

Repo: [absolute worktree path], branch [branch]. PR [url or "no PR"].
Commits: [feature sha], plus [fix sha] when this is a re-review.

Read only. Do NOT edit files, commit, push, merge, or comment on GitHub or on
any task card. You may read files and run read-only commands only.

## How to see the change

    cd <worktree> && git show <sha>                 # the commit under review
    cd <worktree> && git diff origin/<base>...HEAD  # the whole change

## Product context the diff cannot tell you

- [what the system does and who uses it]
- [where auth, tenancy, money and outbound send paths live]
- [the rules this code is meant to honor: caps, windows, allowlists, scoping]

## Check specifically

1. [prior finding, or omit for a first read]
2. [...]

## Run budget

`pnpm exec tsc -p tsconfig.json --noEmit` plus `pnpm exec vitest run <named
files>` only. Do NOT run the full suite, do not touch the network, do not
touch production.

## Return, as JSON

    {
      "verdict": "PASS | BLOCK",
      "original_findings": [{"finding": "...", "status": "closed|partly closed|open",
                             "evidence": "path:line", "reason": "..."}],
      "new_findings": [{"severity": "blocker|should-fix|nit", "file": "path:line",
                        "scenario": "concrete failure, one or two sentences",
                        "fix": "smallest change that closes it"}]
    }

BLOCK means at least one blocker remains or was introduced. Report only what
you verified by reading code; mark anything else unverified.
