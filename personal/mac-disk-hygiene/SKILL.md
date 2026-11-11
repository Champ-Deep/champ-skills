---
name: mac-disk-hygiene
description: "Use when cleaning Deep's Mac disk or inventorying AI models."
version: 1.0.0
author: Deep / Hermes
license: MIT
metadata:
  hermes:
    tags: [disk, storage, cleanup, ollama, huggingface, models, maintenance]
    related_skills: [open-model-runnability-probes, apps-projects-backup, llm-model-benchmarking]
---

# Mac disk hygiene

Class of work: inventory what is on the disk (especially AI models), reclaim space in tiers with load-bearing checks, prove the reclamation with numbers, and keep a free-space floor.

## When to Use

Any "clean up my disk / storage is full" ask, before a big install (model pull, repo clone), when asked which models live on the machine, and for periodic maintenance.

## Procedure

1. **Measure.** `df -h /System/Volumes/Data`. That line is the real number; the Macintosh HD header is not. Note before-values in GB.
2. **Inventory models.**
   - Ollama: `ollama list`; abandoned downloads show as `find ~/.ollama -name "*.partial"`.
   - HF cache: per `~/.cache/huggingface/hub/models--*`, run `du -skL <dir>/snapshots`. A 0-byte result means dangling symlinks: nothing to reclaim, keep or purge the entry but never count it as space.
   - GGUF/weights elsewhere: targeted `find <dir> -maxdepth 3 -name "*.gguf" -size +100M` on likely dirs (Downloads, repos, Models). Never a full-home find or du: on a 400GB home it crawls for minutes and returns mid-scan garbage.
3. **Load-bearing check before proposing any model or large-cache deletion.** Grep `~/.hermes/config.yaml` for the path, then grep the consumer code for the model id: `grep -rn "<id>" <consumer-dir>`. If referenced, it is live: exclude it and report the file:line evidence. The largest cache entry in a cleanup pass can be exactly this (an MCP's scoring model), and deleting it breaks a live lane. Recorded answers for this machine: `models--Cloudflare--clef-flash` (18 GiB, the largest HF entry here) is live, loaded by `kanban_clef.py` and `celsus_jev.py` every 30 minutes; `~/.hermes/models/gemma-4-26B_q4_0-it.gguf` (14 GiB) is referenced nowhere in config, scripts, profiles or skills and held by no process.
4. **Size candidates:** `du -sk <paths> | sort -rn` and `du -sk ~/Library/Caches/* | sort -rn | head -8` for the cache breakdown.
5. **Tier the cleanup:**
   - A: pure regenerable caches (npm, pnpm store, brew, pip, Chrome/Google caches). Runs on approval, near-zero risk.
   - B: regenerable with re-download cost (camoufox, go modcache). Playwright browsers: **keep** when automations use them; state the re-download cost for anything removed here.
   - C: human review only (Downloads folders, migration archives, app data). Print sizes, never `rm`.
6. **Reuse the installed `~/.hermes/scripts/disk_sweep.py` and its weekly wrapper.** Read the approval card before execution, then run `test_storage_guard.py` and the dry run. Script comments and skill tiers are not authorization: assert the exact approved path list, and remove any broader deletion branches before `--apply`. Current cache-only approval covers native uv, npm and pip download caches plus Homebrew's `Library/Caches/Homebrew` via `brew cleanup --prune=all` (added 2026-11-03, card `t_2e4acdd3`), and pnpm store prune for the weekly job (ruling C on `t_e5ac9ec0`, 2026-11-06; card `t_1ebb2210` lands it), not Docker or workspaces. An approval to "add X to the weekly job" is met only by a job-list entry in `disk_sweep.py`: a one-off prune grows back (pnpm went 3.6 to 5.0 GiB in 6 days). Use additional cleaners only after explicit scoped approval. Keep tests isolated from real disk free space.
7. **Verify and report:** df delta in GB, `ollama list`, survivors (`ls hub | grep models--`), personal folders intact. Report as a before/after table, then flag every judgment call taken (items kept, items held back).
8. **Verify the ongoing loop, do not duplicate it.** Existing weekly cleanup is Sunday 16:00 IST; the existing factory watchdog checks disk every 30 minutes, warning below 40 GiB and critical below 20 GiB. Inspect actual cron delivery: `deliver=local` only saves output and does not notify Deep, even when registry prose claims Telegram. Before proposing a delivery change, read `disk-sweep-guard` (21a70308670f): it already delivers to Telegram below 30 GiB, so only the warning band and recovery are open. Stage any delivery change for approval as its own needs_input card, because a question parked in completion metadata dies with the card. Do not download missing models as a cleanup side effect.

## Standing rules

- When one message's removal list contains a later keep clause, the keep wins. State that interpretation in the reply; do not ask.
- A broad "remove the downloads" order covers top-level installers/archives only (`-maxdepth 1` on `*.dmg *.apk *.zip *.pkg *.tar* *.iso`). Personal folders (Family, name folders, work decks) stay until explicitly named.
- Never delete beyond the approved list in one pass. Caches are re-downloadable, user files are not.
- Before pulling any model: check free space and the model's actual size on disk first, and `ollama rm` the replaced model the same day.

## Pitfalls

- `docker system df` first. Docker (images, build cache, volumes) hid 145GB that no `du` of home surfaced because it lives in one disk image under Library/Containers. `docker builder prune -af` is Tier A (pure regenerable); images are Tier B; volumes and stopped containers are Tier C (they hold Postgres data).
- Finished task workspaces can retain large install directories. Inventory them through `~/.hermes/kanban.db`, but do not infer deletion permission from done/archived status: directories may contain deliverables or active previews. All workspaces stay outside the cache-only weekly cleanup. A separate approved retention pass must check processes, git state, remote containment and redirected paths before deletion. The `kanban/kanban.db` next to the workspaces is an empty decoy.
- `du` on this 400GB home exceeds the 420s terminal cap even per top-level dir. Run the survey as a background job writing to a scratch file, and use `du -sk <dir>` per directory rather than `du -d1` (which printed nothing).
- A long-running `uv run` service can hold `~/.cache/uv/.lock` indefinitely. Bound the native cleaner to 35 seconds, inspect the lock owner with `lsof`, report partial cleanup honestly and leave the service running. Never force the lock or stop an app to free caches.
- Chrome's cache cannot be fully removed while Chrome runs (directory not empty, long hang). Skip it.
- The weekly scheduler is `~/.hermes/scripts/disk_sweep.py` via cron `disk-sweep-weekly` (Sun 16:00 IST). Extend its job list in the script.
- Auto-clean guard: cron `disk-sweep-guard` (every 30m, `disk_sweep_guard.sh` = `disk_sweep.py --if-low 30`) is silent above 30 GiB free, below it runs caches + Docker `container prune --filter until=72h` + `image prune -a --filter until=720h` (never volumes) and reports to Telegram. Docker unused images were the biggest reclaim (about 34 GB in one pass); `docker system df` underestimates it.

- Free space here moves by tens of GiB with no deletion by the agent: one session read 11 GiB available, then 35 GiB minutes later, as macOS reclaimed purgeable space. Measure immediately either side of each action and report only those deltas; a session-wide before/after claims gained space the agent never freed.
- Claude Desktop is a top holder on this Mac: `vm_bundles/claudevm.bundle` (20.3 GiB, regenerable but the app re-downloads 20 GiB on the next local agent session) and `local-agent-mode-sessions` (22.9 GiB). Date the INNER session dir before calling that one stale, because the outer dir read as February while an inner dir was written 2026-10-31. Its browser-style caches (`Cache`, `Code Cache`, `GraphiteDawnCache`, `GPUCache`) are safe to remove whenever no Claude process runs, about 1.5 GiB.
- Cowork `local-agent-mode-sessions` was absorbed 2026-11-06 (sha256-verified) into `Celsus/Other/Archive/Claude Cowork-2026-11-06/` (memory, deliverables not already in the vault, missing skills, index note) and `~/Documents/Claude Cowork Archive 2026-11-06/` (files over 10 MB, transcripts tar.gz). Deletion waits on card t_4a608227. Before absorbing anything into the vault, dedupe by sha256 against the vault (2,036 of 2,539 sessions had Celsus mounted, so half the outputs were already there) and put it under `Other/Archive/`, which the Celsus OS walker skips. Check `vm_bundles/claudevm.bundle/sessiondata.img` mtime before calling the VM stale.
- Other large holders measured 2026-11-03: `~/Library/Application Support` 64.9 GiB (Claude 46.9, Wispr Flow 5.7, Google 4.0), `~/repos` 28 GiB, `~/Library/Caches` 7.1 GiB (trivy 1.6 and ms-playwright 1.16 are the two real ones), `~/Downloads` 6.8 GiB (personal spreadsheets and videos, never delete). Antigravity and a Playwright Chrome for Testing instance run in the background, so their caches stay.
- A guard firing is an alert, not a rescue: while a `uv run` service holds `~/.cache/uv/.lock` (found pid 52233 running `uv run uvicorn champoracle.api:app`), the pass recovers about 0.05 GiB and exits 1, which cron shows as an error. Read exit 1 on `disk-sweep-guard` as "fired", and confirm in the output which jobs reported CLEAN.
- Counting HF space from directory listings overcounts: broken symlinks and shared blobs inflate it. `du -skL` on snapshots per model is the truth.
- `brew cleanup --prune=all` frees old formula versions and its cache; installed formulae stay. Safe in Tier A.
- Deleting browser caches (Chrome, playwright, camoufox) always succeeds but pushes a re-download onto the next automation run. Say so before removing, and keep Playwright when QA pipelines are active.
- `npm cache clean --force` and `pnpm store prune` print scary warnings and are still safe; capture their tail output in the log rather than treating warnings as failures.

- Context safety before any cleanup: the vault is covered by `celsus-backup` (Drive, vault only); Hermes sessions, memory, kanban, cron, scripts and profile DBs are covered by `hermes_state_backup.py` (cron `hermes-context-backup`, daily 15:00, Drive `Hermes Backup`, keep 3, `--verify` lists and checks for leaked credentials). Both use one age key at `~/.config/celsus-backup/key.txt`; if Deep has not stored it off-machine, every Drive backup dies with the laptop. Beacon local history (`beacon endpoint traces reindex`) only reaches back as far as the runtime log, about two days.
- ~/repos is about 90% regenerable (node_modules/.next/.venv): 39 of 44 GiB measured 2026-11-11. Back them up with `GHB_ROOT=~/repos GHB_KEEP_PUBLIC=1 python3 backup.py` (background, 30+ min) before trimming anything there.

## Clearing local clones (Deep's standing rule: defined ideas live on GitHub and in cloud sessions)

- Classify every folder in ~/repos and ~/Apps&Projects: KEEP when referenced by config, cron, scripts, LaunchAgents or docker mounts, an open kanban card names its path, or a process runs in it; ACTIVE when any non-.git, non-node_modules file changed in 7 days (list it as a move-to-cloud candidate); CLEAR when verify.py says SAFE and neither applies.
- Re-check at delete time: `git fetch --all`, no unpushed commits, no stash. A dirty tree is clearable only when `GIT_INDEX_FILE=<copy> git add -A && git write-tree` equals the tree of a pushed `backup/<date>/*` snapshot. Remove linked worktrees with `git worktree remove --force` from the common dir; keep a parent whose worktrees remain.
- After build-folder trimming, clones are small (51 clearable folders were 2.4 GiB). The space is in kanban workspaces, Docker and app data, not source.
- Done-task workspaces: archive (tar excluding node_modules/.next/.venv | zstd | age) to Drive `Hermes Backup/kanban-workspaces-done-*.tar.zst.age`, verify the listing has every dir, then delete. 133 workspaces went into an 827 MiB archive.
- OrbStack's data lives in `~/Library/Group Containers/HUAQ24HBR6.dev.orbstack` (49 GiB), invisible to du of the home dir. `docker builder prune -af` plus `image prune -af` freed 36 GB; named volumes holding model weights or build state (ollama data, buildx state) are regenerable; DB volumes are Deep's call.
- The backup key's off-machine copy is made by Deep running `~/Desktop/Backup Key to 1Password and Drive.command` (his passphrase, Drive `Backup Key/`, plus 1Password once its CLI integration is on). Agents never handle the key or passphrase.

## RAM, not only disk

- Swap IS disk here: `/System/Volumes/VM` shares the APFS container, so 20 GiB of swapfiles took free space from 50 to 5.6 GiB (2026-11-06). When free space drops with no new files, run `sysctl vm.swapusage` and `ls /System/Volumes/VM` first; killing the RAM holders gave back 10 GiB in 30 seconds.
- Two standing guards now prevent the repeat: `celsus_compose_cron.sh` skips the clef-flash jev step unless 20 GiB RAM is available and 30 GiB disk is free (skips logged to `~/.hermes/logs/jev_skips.log`), and cron `dev-server-reaper` (every 30m, `dev_server_reaper.py --apply`) SIGTERMs then SIGKILLs agent-started dev servers (leader has `__hermes_exit_file`) whose kanban task is not running, or older than 6h elsewhere. wrangler/workerd ignore SIGTERM. Check both before writing new prevention.
- `node_modules`, `.next`, `.turbo`, `.wrangler` inside done-task workspaces are regenerable and were 8 GiB; blocked-task workspaces keep `node_modules` (they may resume) but lose build caches. Source, evidence and zips stay.
- Starting OrbStack to prune Docker auto-starts `restart=always/unless-stopped` containers (open-webui, sledgehammer, openbot, softphone). Prune, then `orb stop` to restore the prior state. Unused named volumes (buildx state, miroshark ollama data) are Deep's call.

- `laya-local/decider/mcp_server.py` (the decider MCP) held 18 GB RSS after 4 days up, with swap at 20 GiB. SIGTERM is safe; the next Hermes session respawns it. Swapfiles do not shrink immediately after the kill, so do not count it as freed disk until `sysctl vm.swapusage` drops.
- "Memory" on this Mac usually means swap thrash, not disk: check `sysctl vm.swapusage` and `top -l 1 -o mem -stats pid,mem,cmprs,command` before `df`. The holder was `celsus_jev.py score` (19 GB RSS, clef-flash on MPS) fired by the celsus-compose cron whenever a new blocked card needed a score; `kanban_clef.py` loads no model unless `--shadow-top` is passed. The model crons now run on a 2h cron expr; keep any model-loading step off a 30-minute interval on a 32 GB machine.
- Finished kanban workspaces leave `next dev`, `vite` and `.verify/server.mjs` servers running for days (3 to 4 GB RSS mostly in swap). Find them with `lsof -a -d cwd -p <pid>` under `~/.hermes/kanban/workspaces/`, check the task status in `kanban.db`, then `kill -- -<pgid>`.
- `docker builder prune -af` plus `docker image prune -af` reclaimed 32 GB in one approved pass; `timeout` does not exist on macOS, run long docker commands as a background job.

## Maintenance cadence

- Weekly: run the existing approved native uv/npm/pip cleanup, then re-check `df`; keep additional caches outside that policy until separately approved.
- Target: 40 GiB free, warning below 40 GiB, critical below 20 GiB. Inventory before a large download and compare free space with its actual peak requirement. These alerts are not a reserved-space guarantee.
- Model shelf hygiene: dangling 0-byte cache entries and replaced Ollama models get purged in the same pass, not saved for later.
