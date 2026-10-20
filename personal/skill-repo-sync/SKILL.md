---
name: "skill-repo-sync"
description: "Use whenever a Claude/Cowork skill is created, updated, or finalized for Champ, to sync it into his shared champ-skills GitHub repo so every agent and team reads the same library."
---

# Skill Repo Sync

Champ runs one shared skill library for every agent and team: the GitHub repo `Champ-Deep/champ-skills`, cloned locally at `~/champ-skills` on his Mac (device `sreedeeps-macbook-pro-local`). A skill created or updated for Champ, by any agent, is not finished until it is also in that repo and pushed to GitHub. Treat this as a standing step after any skill work, not a separate request he has to make each time.

## When this runs

- Right after `propose_skills` is used to create or update one of Champ's account skills, once he has saved it.
- Right after `skill-creator` (or any other skill-authoring flow) produces a finished skill folder.
- Whenever Champ asks to "update the skills repo", "sync skills to GitHub", "push my skill updates", or similar.

## Steps

1. Identify the skill's category from the repo's existing structure (see `README.md` and `INDEX.md` at the repo root). Category folders: `design/skills`, `design/brand-guidelines`, `branded-docs`, `marketing`, `sales`, `documents`, `engineering`, `productivity`, `research`, `science`, `personal`, `celsus`, `champ-suite`, `creative`, `security`, `software-development`, `video-clip-editing`, `autonomous-ai-agents`. Several finished skills also sit loose at the repo root (`adapter-seam-extension`, `first-ci-workflow`, `fleet-status-dashboard`), so root is a valid home for a standalone skill with no natural category. There is no `vault` folder: it was renamed to `personal`, so never recreate it. Match by what the skill actually does, not its name. Ask Champ once only if genuinely ambiguous.
2. Get access to `~/champ-skills` on his Mac via the remote-devices bridge (`device_request_folder_access` if this session has not already connected it). In a session that already has a direct shell on the Mac (Hermes desktop), skip the bridge entirely and run the copy and git steps straight in the terminal: the bridge routing is only for sessions that have no local shell.
3. The account's live skill files and Champ's Mac are different machines, so route the copy through this container: copy the skill's current files (`SKILL.md` plus any `references/`, `scripts/`, `assets/`, `examples/`) into `/mnt/user-data/outputs/<category-path>/<skill-name>/...`, mirroring the target repo layout exactly, then use `device_commit_files` to write each one to `/Users/deep/champ-skills/<same-path>` (batch up to 50 files per call).
4. Update `INDEX.md`: add or refresh the skill's row in its category table, using a one-line description pulled from the skill's frontmatter `description`, truncated to match the file's existing row length exactly (currently a hard 170 characters, verify against neighboring rows rather than assuming). Bump the total skill count in the header.
5. Update `README.md`: bump the total count and the affected category's count in its table.
6. In `~/champ-skills`: run `git status` FIRST, before any add. This clone is the live skills path that several agents edit, so the tree routinely carries other sessions' uncommitted work alongside yours. If the only changes are the files this sync just wrote, `git add -A` is fine. If anything else is dirty, stage only the explicit paths this change wrote and list the untouched dirty paths in your report; a broad add sweeps unrelated work into your commit and makes it unreviewable. Then `git commit -m "<what was added or updated>"`, then `git push`.
7. The sandboxed device shell has no access to Champ's personal SSH keys or agent, so `git push` can fail with a publickey error even though the commit itself succeeds. When that happens: do not treat it as done. Tell Champ plainly that the commit is made and clean but still local, give him the exact command to run himself (`cd ~/champ-skills && git push`), and mention that a dedicated deploy key for this repo (added once in GitHub's repo settings, kept inside the mounted `~/champ-skills` folder, never typed into any web form as a secret) would remove this manual step going forward, if he wants it set up.
8. When the push does succeed, confirm with `git log --oneline -1` and `git status` (clean, "up to date with origin/main") before reporting success.

## Rules

- Never delete or reorganize a skill folder other than the one being synced.
- Never skip the push step or report the job done on a commit alone. A local commit does not reach the shared library his other agents and teams read from.
- No em dashes anywhere in edits to this repo, matching every other Champ deliverable: periods, commas, colons, or restructure instead.
- Never invent PATs, tokens, or credentials into any config or file on Champ's behalf. If GitHub authentication is missing, say so and hand back the exact next step, don't work around it.
- This clone is Champ's live skills path, not a staging copy: agents read it directly, so an edit in the clone is in effect for them from the next session onward. That also means a dirty tree loads locally while GitHub stays behind. Show `git status` output when reporting, and count uncommitted skill files as not yet synced.
- Nothing automatically pulls this clone, so never call it current on the strength of a local load: `git fetch` and compare against `origin/main` first.