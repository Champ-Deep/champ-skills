---
name: span-agent-development
description: "Use when changing or deploying the SPAN agent."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [span, data-cards, globe, react, esbuild, deployment]
    related_skills: [visual-verify, defensible-data-counts, release-integration-engineering, credential-and-secret-handling]
---

# SPAN agent development

The SPAN agent (spantechiq) is `server.py` (Python stdlib HTTP) plus a React/TypeScript UI bundled by esbuild in `ui/`, over a knowledge base of data cards. This skill is the workflow, the stack quirks, and the gates.

## When to Use

- Any change to the SPAN agent's backend (`server.py`, `cards.py`, `ingest.py`, `explorer.py`), data cards, globe/US map, or search UI.
- Deploying or merging the agent's branches into the production checkout.
- Adding a shadcn or 21st.dev component to `ui/`.
- Debugging a count, a dimension, or a provenance label in the agent's API.

## Always-on rules

- **No deploy, and no push to the deploy checkout, without Deep's explicit go.** The work branch and the production deploy source are different checkouts: verify with `git status` in both `/Users/deep/repos/span-data-cards` and `/Users/deep/repos/span-intelligent-ui` before claiming a merge changes what runs.
- **Local runs use `SPAN_ENRICH_PROVIDER=mock`.** The real provider bills contact lookups against client budgets; only production uses it.
- **Every count carries its source.** `GET /api/counts` answers from data cards first and falls back to demo company records; either way the payload includes `source` and a human-readable `note`, and the UI must render them. A map or figure built on the fallback says so on the figure itself.
- **Close every change with the visual gate** from `visual-verify`: light and dark, 1440 and 390, screenshots opened and judged, zero console errors, zero horizontal overflow.

## Globe and map direction

Deep's reference is the Harbinger signal globe (live at https://champharbinger-production.up.railway.app/, component `signal-globe` in the ChampHarbinger-home repo; search the repo for the name).

- Dark sphere, dot-matrix land, slow rotation that stops under the pointer with inertia. Solid colour blobs and unlabelled shapes are the failure mode he named.
- Every region pin shows its count; hover or focus reveals companies, contacts, and source.
- Globe and US choropleth read from `/api/counts` plus a technology selector, never from hard-coded numbers.
- The US opens on double-click AND with the keyboard: while the globe canvas has focus the caption switches to the arrow-key and Enter hint, Enter opens the state map, Escape returns. Deep's direction is no control chrome on the canvas itself (no rotate arrows, no reset, no "Open US map" button): drag and double-click carry pointer interaction, and the focused caption carries the keyboard path. A visible button on the globe is the failure he named.
- Captions state the data source, both themes pass contrast, and `prefers-reduced-motion` stops auto-rotation.

## Procedure

1. Orient: `git -C /Users/deep/repos/span-data-cards status --short --branch` and `git log --oneline -3`. Confirm the branch before editing.
2. Backend change: run `python3 -m pytest evals/ -q`, the whole suite, not only the file you touched. Every fixed defect gets its regression test in the existing test file in the same change.
3. Exercise live: start the server as a background terminal process (a bare `&` in a foreground command is rejected) with `PORT=31xx SPAN_DB=... SPAN_ENRICH_PROVIDER=mock SPAN_LLM=rules python3 server.py`, curl the endpoint, kill it.
4. UI change: `cd ui && nvm use default && npm run typecheck && npm run build`.
5. Visual gate, then commit with a message naming what landed. Report what changed, what is verified, and what is left, then wait for the go on any deploy.

## Hero and home-page layout

- **Dead space under the hero copy is fixed by relocating content, not by trimming margins.** When one column of a two-column hero runs much taller than the other, do not just top-align or nudge gaps: move an existing panel (the "Build a search" filter bar is the natural candidate) from the tall column into the short one, so the copy column runs heading, text, search bar, panel with even gaps. Measure the gaps before and after with bounding boxes rather than eyeballing the screenshot.
- The hero grid is `align-items:start` with the left column as its own grid (`.ch-left`), so both columns hang from one top line. Centring the short column leaves symmetric air above and below and still reads as dead space.
- Side effect to name in the report: moving a panel between columns reorders it at 390 too (the globe then follows the filters on mobile).

## Admin access

- `/admin` (UI and its API) is gated by one shared token in the `SPAN_ADMIN_TOKEN` env var, read at request time: rotate by editing the variable in Railway, which invalidates the old token on the next request; there is no username/password and no per-user account. Point a teammate at the URL plus the variable name, and never paste the value into chat.
- The gate is presentation only. The API stays bearer-token protected, and a token check that runs only in the client is a door with no lock.

## Local runs and ports

- 127.0.0.1 is shadowed by another app on this machine, so test servers are driven through the machine's LAN address (`ipconfig getifaddr en0`), not localhost. Re-derive the address rather than hardcoding it.
- Parallel runs need one `PORT` and one copied `SPAN_DB` file per server; sharing a database file between two servers produces write contention that looks like an app bug.

## Verification scripts

- Playwright selectors must disambiguate canvases: once the page has more than one `<canvas>` (the search orb plus the globe), `canvas` resolves to whichever comes first in DOM order and a focus or keyboard test silently drives the wrong element. Target `canvas[tabindex]` for the globe and assert the caption text changed after focusing, not just that focus moved.

## Pitfalls

- `npx shadcn@latest add` can emit `import { cn } from "cn"` when it cannot resolve the `@/` alias. Rewrite those imports to `@/lib/utils`, make sure `ui/src/lib/utils.ts` exports `cn`, typecheck, and never `npm install cn`.
- Tailwind v4's entry imports utilities only. Preflight is off on purpose: switching it on restyles the whole shipped app.
- An unknown `dimension` on `/api/counts` returns 400 naming the allowed values. Take the list from that error instead of hardcoding it, and let the 400 guard new callers.
- A brand-new test failing on counts usually means the seed and fixtures hold different numbers than assumed. Check the fixture before suspecting the code.
- Never write imports for a component that was only planned (see `references/ui-stack.md` on 21st.dev). Typecheck is the proof that something is installed.
- A guard you write to protect a file edit (`assert` on a match count) will trip on its own earlier lines if the pattern appears more than once in the file. Verify the count against the real number of intended sites before the write, or the edit silently does not land and the next step runs against stale code.
- Adding or renaming a component requires regenerating the spec (`cd ui && npm run gen:prompt`) before anything downstream runs: the server validates component names against `harness/openui/system-prompt.json`, and a component name absent from the spec fails at runtime, not at build.

## References

- `references/ui-stack.md` — esbuild, Tailwind v4 utilities-only, the shadcn alias fix, basemap generation, bundle notes.
