# Vendoring external skills into champ-skills

Bring skills written elsewhere into `~/champ-skills` so every agent reads them, without breaking the library's shape or its licensing.

## Procedure

1. **Check the license first.** Repo root, then the skill folder. If there is none, treat the code as all-rights-reserved: describe the workflow in your own words as a hand-written skill instead of copying files. MIT/Apache means copy freely; record the source in step 5.
2. **Check what ships alongside the code, not just the license file.** List the skill's asset folder before copying. MIT covers the skill's own files, not third-party brand logos, marks or reference libraries bundled inside them, and those are not yours to republish. A bundle carrying trademarks turns one copy into three options, so surface them as separate decisions: full copy, copy without the asset folder, or a link to upstream instead. Name the tradeoff rather than letting the user discover it: dropping the asset folder can disable a documented feature, such as a reference-mark search, and the skill then needs a line saying the feature is unavailable.
3. **Class-ize the structure before copying.** External libraries often ship narrow per-task or nested skill folders. Do not replicate them as a flat list. One class-level skill per idea, and anything optional or model-dependent goes under that skill's `references/`, not as sibling skills. Nested folders under a skill must stay under `references/` or the scanner surfaces them as top-level skills and bloats the list.
4. **Normalize to house rules on the way in:** no em dashes anywhere in the markdown (periods, commas, colons), no screenshots or personal notes from the source, no `.git` from the source repo.
5. **Record provenance:** add an `UPSTREAM.md` at the skill folder root with the source repo URL and the vendored commit. It states where the code came from, nothing more.
6. **Register it:** add or refresh the skill's row in `INDEX.md` and the counts in `README.md` and the category `README.md` (one-line description from the frontmatter `description`, matched to neighboring row length).
7. **Push per the `skill-repo-sync` steps**, staging only the paths this change wrote.

## Pitfalls

- **Run `python3 scripts/build_index.py` from the repo root instead of hand-editing INDEX.md** after any bulk add: it regenerates every category table and the total, so manual edits drift or get clobbered on the next rebuild. It also prints a notice listing root-level skill folders; that notice is informational, not an error.
- **Verify the skill list after a bulk add, do not assume it.** Load Hermes's own python with the repo root on `sys.path`, call `agent.skill_utils.iter_skill_index_files(<category>/skills, "SKILL.md")`, and compare the found names against the ones you intended. This catches both a skill that silently failed to index and a nested folder leaking in as its own skill.
- **Newly added skills appear from the next session, not the current one.** The running session caches its skill list, so tell the user a refresh is needed rather than re-checking repeatedly.
- **Never `git add -A` in a fresh vendor commit**: `~/champ-skills` is a live clone other sessions write to. Stage explicit paths.
