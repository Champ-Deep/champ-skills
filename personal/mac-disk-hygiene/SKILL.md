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
3. **Load-bearing check before proposing any model or large-cache deletion.** Grep `~/.hermes/config.yaml` for the path, then grep the consumer code for the model id: `grep -rn "<id>" <consumer-dir>`. If referenced, it is live: exclude it and report the file:line evidence. The largest cache entry in a cleanup pass can be exactly this (an MCP's scoring model), and deleting it breaks a live lane.
4. **Size candidates:** `du -sk <paths> | sort -rn` and `du -sk ~/Library/Caches/* | sort -rn | head -8` for the cache breakdown.
5. **Tier the cleanup:**
   - A: pure regenerable caches (npm, pnpm store, brew, pip, Chrome/Google caches). Runs on approval, near-zero risk.
   - B: regenerable with re-download cost (camoufox, go modcache). Playwright browsers: **keep** when automations use them; state the re-download cost for anything removed here.
   - C: human review only (Downloads folders, migration archives, app data). Print sizes, never `rm`.
6. **Execute through `scripts/stage_cleanup.sh`** (dry-run by default, `--apply` to execute, Tier C printed as sizes only). Explicit paths only, no wildcards outside named dirs.
7. **Verify and report:** df delta in GB, `ollama list`, survivors (`ls hub | grep models--`), personal folders intact. Report as a before/after table, then flag every judgment call taken (items kept, items held back).
8. **Offer, do not create:** a df watchdog cron; re-install of a removed winner model once free space is shown.

## Standing rules

- When one message's removal list contains a later keep clause, the keep wins. State that interpretation in the reply; do not ask.
- A broad "remove the downloads" order covers top-level installers/archives only (`-maxdepth 1` on `*.dmg *.apk *.zip *.pkg *.tar* *.iso`). Personal folders (Family, name folders, work decks) stay until explicitly named.
- Never delete beyond the approved list in one pass. Caches are re-downloadable, user files are not.
- Before pulling any model: check free space and the model's actual size on disk first, and `ollama rm` the replaced model the same day.

## Pitfalls

- `docker system df` first. Docker (images, build cache, volumes) hid 145GB that no `du` of home surfaced because it lives in one disk image under Library/Containers. `docker builder prune -af` is Tier A (pure regenerable); images are Tier B; volumes and stopped containers are Tier C (they hold Postgres data).
- `~/.hermes/kanban/workspaces/t_*` of done/archived tasks keep their `node_modules`/`.venv`/`.next`. Join dir names to `~/.hermes/kanban.db` (`select id from tasks where status in ('done','archived')`) and remove only those install dirs. The `kanban/kanban.db` next to the workspaces is an empty decoy.
- `du` on this 400GB home exceeds the 420s terminal cap even per top-level dir. Run the survey as a background job writing to a scratch file, and use `du -sk <dir>` per directory rather than `du -d1` (which printed nothing).
- `uv cache clean` blocks for 300s and exits 2 while any long-running `uv run` service holds `~/.cache/uv/.lock` (champoracle uvicorn does). Do not `--force`; report it as held.
- Chrome's cache cannot be fully removed while Chrome runs (directory not empty, long hang). Skip it.
- The weekly scheduler is `~/.hermes/scripts/disk_sweep.py` via cron `disk-sweep-weekly` (Sun 16:00 IST). Extend its job list; never add a second disk cron.

- Counting HF space from directory listings overcounts: broken symlinks and shared blobs inflate it. `du -skL` on snapshots per model is the truth.
- `brew cleanup --prune=all` frees old formula versions and its cache; installed formulae stay. Safe in Tier A.
- Deleting browser caches (Chrome, playwright, camoufox) always succeeds but pushes a re-download onto the next automation run. Say so before removing, and keep Playwright when QA pipelines are active.
- `npm cache clean --force` and `pnpm store prune` print scary warnings and are still safe; capture their tail output in the log rather than treating warnings as failures.

## Maintenance cadence

- Monthly: run the script's Tier A (+ Tier B as needed), re-check `df`.
- Floor: keep at least 15GB free; when free space drops below it, inventory before any new pull.
- Model shelf hygiene: dangling 0-byte cache entries and replaced Ollama models get purged in the same pass, not saved for later.
