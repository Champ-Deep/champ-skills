# Refresh lanes and multi-repo dispatch

Depth for running parallel UI lanes across the deependhq refresh branches. The always-on rules (subdomain checklist, the four places a page class is registered) live in SKILL.md; this file is the how.

## Prove the merge before anyone starts

Do not assume the newest branch is the sum of the work. Feature branches in this repo live in separate worktrees, each cut at a different moment, so the branch that looks freshest can still miss another's files.

```bash
git fetch -q origin
git merge-tree --write-tree --name-only <base> <branch>    # per pair, no checkout
git merge-base --is-ancestor <base> <branch> && echo in   # is base already in it
```

- Conflicts reported here cost a minute; the same conflicts discovered in the final merge cost a lane. Resolve small conflicts in the integration branch first, then hand every lane a clean base. Two lanes that each resolve the same conflict their own way make the final merge the expensive one.
- Check `git log --oneline main..<branch>` and how far the release branch sits behind `origin/main`: nightly publishing moves `content.json` and `data.js` on `main` every night, so a feature branch that sat still for a week is behind by every journey entry, not by code.
- Create the lanes' worktrees from the final integration commit before the dispatching card completes (`git worktree add -b <lane-branch> <path> <commit>`). A child card inherits `workspace_path` and dies at spawn if the path does not exist.

## What a lane brief must carry

**Exact source identifiers, not descriptions.** Name the component ids and theme ids from the design MCP (`get_component` for code, `get_theme` for tokens) plus the command that proves the source was reachable. A brief that says "use the loading animation he saved" makes the lane guess, and a model with a generation tool in scope will generate an approximation of a component it could have read. Pulling the real code is the whole point of having the paid account.

**The runtime constraint, stated as a boundary.** This site is static prerendered JSX plus a Cloudflare Worker: no Tailwind, no component-library runtime, no framework migration. Port component logic into house JSX/CSS; a lane that imports 21st.dev component classes into a plain-CSS page gets an unstyled or broken build. Pair the boundary with what stays out (content files, publish scripts, other lanes' surfaces), because a card that only forbids reads as ambiguous the moment the donor code contradicts it.

**A verdict file as proof of research.** Require `docs/<lane>-component-verdicts.md`, one row per pulled item: used / adapted / rejected plus a one-line reason. It is the only artifact that shows the source was actually read, and it is what Deep reviews when he asks why a direction was taken.

## Keep the static site's integrity gates in every lane

Each lane runs before it pushes: `node scripts/prerender.mjs`, `node scripts/link-check.mjs`, and the five `scripts/selftest-*.mjs` Worker checks if any Worker file moved. Lanes push their own branch only; merging, deploying and remote D1 migrations belong to the integration card and then to Deep.
