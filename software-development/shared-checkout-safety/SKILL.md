---
name: shared-checkout-safety
description: "Use when another agent may be editing the same repo."
tags: [git, concurrency, branches, collaboration, verification, checkout, agents]
---

# Shared Checkout Safety

When more than one agent, terminal, or editor session has the same repository
open, `git status` is no longer a description of your work alone. This skill
covers establishing what is actually yours before you branch, commit, or report
a result as fact.

Triggers: a repo you did not just create; an uncommitted change you did not
make; a commit whose parent is not the branch you intended; a second agent, an
IDE, a watcher, or a background process touching the working tree.

## 1. Establish ownership before you touch anything

On a repo you did not just clone, run this before your first edit:

```bash
git status --short
git log --oneline --decorate -8
git reflog --date=iso -12      # who checked out what, and when
git stash list                # work parked by someone else
ps aux | grep -iE 'pytest|tsc|vite|next|webpack|npm|node' | grep -v grep
```

Reading the reflog reconstructs the real sequence of who did what and when.
Compare file mtimes against the current time to catch a writer mid-flight:

```bash
stat -f '%Sm %N' -t '%Y-%m-%d %H:%M:%S' path/to/changed-file
date '+%Y-%m-%d %H:%M:%S'
```

A build process pegging a core in the repo directory, plus files whose mtimes
are seconds old, means someone else is working there right now.

**Stop and surface it. Do not commit over it.** Ask the user whether to
proceed on a separate branch, wait, or abandon the checkout.

## 2. Verify your commit's parent, do not assume it

`git checkout -b` branches from whatever HEAD currently is. If another agent
moved HEAD, your branch inherits their base silently.

```bash
git log --format='%H %P' -1        # your commit and its actual parent
git merge-base --is-ancestor <expected-base> HEAD && echo based-on-expected
git log --oneline HEAD..origin/<expected-base>   # what you are missing
```

If the parent is not the base you intended, say so plainly and correct the
record. A branch stacked on someone else's work cannot merge until theirs lands,
which is a real consequence for the user's merge order, not a detail.

Never report a branch's base from memory or from an earlier tool result. Read it
back after the commit exists.

## 3. Isolate your commits to your own files

`git commit -a` and `git add .` sweep in whatever is in the tree, including
another agent's half-finished work. Stage explicit paths instead:

```bash
git add path/one.py path/two.py
git status --short          # confirm ONLY your paths are staged
git diff --cached --stat    # confirm the staged set is what you meant
```

Committing someone else's work makes it indistinguishable from yours in the
history and quietly steals their attribution.

## 4. Do not delete or revert what you did not create

Another agent's uncommitted changes are not debris. Do not `git checkout .`, do
not `git clean -fd`, and do not "tidy" the tree. If it blocks you, move to a
separate checkout or worktree:

```bash
git worktree add -b <my-branch> /path/sibling <base>
```

Cut it from the intended base explicitly (`main`, `origin/main`), not from
whatever HEAD the shared checkout happens to be on.

### Make the worktree runnable

A fresh worktree has no gitignored state, so it cannot run the suite out of the
box. Get it green before writing code:

1. **Symlink the primary checkout's install instead of reinstalling:**
   `ln -s ../<repo>/node_modules node_modules` (and any other gitignored
   dependency dir). Same lockfile plus same base means the tree is identical;
   you avoid a second full install and never disturb the shared checkout. If
   the worktree branch is on a different lockfile, install for real.
2. **Quote every path that contains `[]`.** Next.js dynamic route folders are
   `[keyName]`, which the shell reads as a character-class glob and silently
   expands to nothing, so `vitest run src/app/api/.../[keyName]` or an unquoted
   eslint argument can pass while running zero files. Always single-quote such
   paths, and confirm the run by test/file count, not by exit code 0.
3. **Pre-commit hooks may be missing their dependencies.** A hook that shells
   out to `node_modules/.bin/*` fails in a bare worktree. Fix it by restoring
   the install (step 1). If you bypass instead, do it for that one commit only
   (`git -c core.hooksPath=/dev/null commit ...`), then re-run the hook's checks
   by hand (lint, typecheck, the touched test directory) and say in the PR body
   that hooks were bypassed. A bypassed hook you did not re-run by hand is an
   unverified commit.
4. **Ship from the worktree, not the shared checkout:** push the branch and
   open the PR from there; the shared tree keeps its other lane's files intact.

## Pitfalls
- **Never deploy from a checkout a card worker may be on.** A deploy script reads whatever HEAD is at run time; a dispatcher-spawned worker can switch the branch between your `git status` and the build, so you ship their half-done branch. Deploy from a detached worktree pinned to the exact commit (`git worktree add <dir> origin/<branch> --detach`), copy the gitignored env file in and symlink the deploy tool's `node_modules`. If wrangler suddenly tries to CREATE a container application that already exists (POST `/containers/applications` 401 instead of PATCH), check which branch built it, and then check the Cloudflare token separately: a clean-worktree rebuild that still fails at the registry push with `unauthorized` is an auth problem, not a branch problem. A deploy wrapper that exits 0 while its wrangler step failed is still a failed deploy: confirm the live version/health endpoint matches the commit you meant to ship before reporting success, and never report success from the shell exit code alone.
- Restore any config you edited for a local run (ports, timeouts) before committing; a scratch port in `playwright.config.js` breaks every later CI run.

- **`git status` is not a description of your work alone** in a shared checkout.
  Check the reflog and running processes before trusting it.
- **A commit's parent is whatever HEAD was, not what you meant.** Verify with
  `%P` after committing and correct the record if it is wrong.
- **`git add .` and `git commit -a` do not know whose work they are taking.**
  Stage explicit paths and read `git diff --cached` before committing.
- **Another agent's uncommitted file is not garbage to clean up.** Leaving it
  alone is always safe; deleting it is unrecoverable for them.
- **A `tsc`, `vite`, or `pytest` process pegging a core in the repo means a
  live writer**, not a stale one. Check mtimes before concluding it finished.
- **Two clones of the same remote are two checkouts, not one.** If a clone
  lands in a directory that already exists as something else, you are editing
  the wrong tree. Verify `git rev-parse HEAD` matches the remote you intended
  before writing code.

## Shared scratch evidence

Give every parallel lane its own scratch subdirectory for screenshots, scripts, logs and temporary databases. Never run wildcard cleanup in the shared scratch root: it can erase another lane's verification evidence even when git worktrees are isolated. Move or remove only files whose ownership is established.

## Compound commands and approval gates

A terminal call that pairs a process kill (`pkill`, `kill`) with a state-changing git
operation (push, merge) can be rejected as unconsented in its entirety: the gate
blocks the whole chain, so the push never runs and the only output is a timeout. Keep
destructive process operations in their own terminal call, ahead of the git chain that
carries the actual intent.

Likewise, `git checkout <main-branch>` fails when another worktree holds that branch
(`'main' is already used by worktree at ...`), and the failure aborts the rest of the
chain. Push the release without switching: `git push origin <your-branch>:main` when
fast-forward, or cut a temp release branch off `origin/main`, merge, verify
`git diff <branch> HEAD` is empty, and `git push origin HEAD:main`.

## Reporting

When you find a concurrent writer, report it as a finding in its own right:
what you observed, with timestamps, what you did about it, and what the user
needs to decide. Do not bury it in a summary of your own work.

## Verification

- The reflog and process list were checked before the first edit on a repo you
  did not create.
- The parent of every commit you made is the base you intended, verified after
  committing.
- Every commit's staged set was read before committing and contained only your
  own paths.
- Nothing another writer had in the tree was modified, staged, or deleted.