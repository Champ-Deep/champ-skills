# SPAN agent UI stack

Where: `ui/` inside the worktree. React 19 + TypeScript, esbuild (`build.mjs`), hand-written CSS with CSS variables switched by `data-theme`, plus Tailwind v4 utilities.

## Commands

```bash
cd /Users/deep/repos/span-data-cards/ui
source ~/.nvm/nvm.sh && nvm use default    # Deep's canonical node
npm run typecheck     # tsc --noEmit
npm run build         # esbuild -> dist/, served by server.py
```

## Tailwind v4: utilities only

`src/tw.css` imports Tailwind for utilities and deliberately not preflight. Preflight would restyle every element the existing stylesheet already owns, and the app's CSS variables (`--bg`, `--ink`, `--line`, `--accent`, ...) stay the source of truth for both themes.

## shadcn components

```bash
cd ui && npx shadcn@latest add <component> --yes --overwrite
grep -rn 'from "cn"' src/components/ui/ || true
sed -i '' 's#from "cn"#from "@/lib/utils"#' src/components/ui/*.tsx   # macOS sed
npm run typecheck
```

- The CLI writes `from "cn"` when it cannot resolve the `@/` alias. The fix is the import rewrite plus `src/lib/utils.ts` exporting `cn` (clsx + tailwind-merge). Installing an npm package named `cn` satisfies nothing: the code means the local utils module.
- Components land in `src/components/ui/` and are imported through `@/components/ui/...`.
- Unimported components sit outside the esbuild graph, so adding ten of them does not move bundle size. Size changes only once something imports them; a flat bundle is not a failed install.

## Map basemaps: generate, do not hand-draw

A build script fetches Natural Earth GeoJSON (public domain), filters to the region, projects coordinates into the same planar frame the world paths use (`x = (lon+180)*960/360`, `y = (90-lat)*480/180`), and writes a `.ts` module whose header records the source URL and the SHA256 of the downloaded file. Pattern: `ui/build-us.py` producing `src/us.ts` (51 entries: 50 states + DC). Fix shapes by re-running the generator, never by editing generated path data.

## 21st.dev components

The Filter Bar (`serafimcloud/filter-bar`) is installed from 21st.dev under `src/components/ui/filter-bar.tsx`, alongside shadcn primitives (`command.tsx`, `popover`, `badge`, `button`, `toggle-group`, ...). The key lives in `~/.hermes/.env` as `TWENTY_FIRST_API_KEY`. Install procedure and registry quirks: see `frontend-design/reference/21st-registry.md`.

- Controlled usage: `FilterBar` takes `value`/`onValueChange` over `FilterState`; views render as tabs, groups as multi-select facets with counts, toggles as chips, plus a collapsible search and an actions slot.
- The facet counts come from `GET /api/facets` (`facet_counts()` in `server.py`): technology counts marked `source: "data_cards"` are real SPAN-supplied US counts; everything else counts demo company records and must be labelled as such in the UI (`defensible-data-counts`).
- Do not add imports for a component that was only planned; `npm run typecheck` decides what is actually installed.
