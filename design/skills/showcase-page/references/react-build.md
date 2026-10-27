# React build path

When the page ships as a React app instead of one static HTML file (Deep asks for real 21st.dev components, or a Vite scaffold already exists). Everything else in the skill, especially Step 6 verification and the evidence rules, is unchanged. The vanilla alternative is `frontend-design/references/21st-vanilla-port.md`.

## 1. Scaffold once, then write the page

```bash
npm create vite@latest <app> -- --template react-ts
cd <app> && npm install
npm install motion @remixicon/react
npx shadcn@latest init    # then npx shadcn@latest add <url-or-slug> per component
```

Ship single-file delivery with `vite-plugin-singlefile` (`plugins: [react(), tailwindcss(), tsconfigPaths(), singlefile()]`), so the audit, the shoot script and the handoff all still operate on one `dist/index.html`.

## 2. Component sourcing order

1. `shadcn add <url-or-slug>` is the first attempt for every component.
2. If the registry rejects it, `npm install <slug>`; if that fails too, open the component's 21st.dev page and drop its own source files into `src/components/ui/`, keeping the imports intact. This route is still a real component, not a hand-built lookalike: credit the id in a comment and name it in the report.
3. `get_component` pulls are quota-bounded (free tier allows about two a day, check `get_usage`); registry installs are not. Reserve the pulls for the components whose source you actually need to read.

## 3. Type and config pitfalls that stop the build

These are compiler rules, not environment failures. They cost a build round each time they are missed:

- **Icon wrappers take the icon library's own type.** A step or timeline component declaring `icon: ComponentType<{ className?: string; "aria-hidden"?: boolean | "true" }>` fails `tsc` against `@remixicon/react`, because `RemixiconComponentType`'s `defaultProps` carry `Booleanish` (`"false"` is a valid value and is not assignable to `boolean | "true"`). Import and declare `icon: RemixiconComponentType` instead of a hand-written prop shape. The same reasoning applies to any wrapper typing a third-party component's props by hand: use the library's exported type.
- **`baseUrl` is removed from current TypeScript.** A scaffolded `tsconfig.json` with `"baseUrl": "."` fails with `TS5102` before any file is checked. Delete it and write the alias as `"paths": { "@/*": ["./src/*"] }` (matching `vite-tsconfig-paths`' resolution), not as `"./*"`.
- Read only the first error of a failed build: `tsc` reports one config error per file it never reaches, so fixing the config error first is what surfaces the real type errors behind it.

## 4. Gate before declaring done

`npm run build` (which must run `tsc --noEmit && vite build`, not `vite build` alone) with zero errors, then the full Step 6 verification against `dist/index.html`. Prove the interactive surface, not just the render: drive real clicks on a selection control, read back the bound text and the selected count, run the copy action against the clipboard (`permissions: ["clipboard-read", "clipboard-write"]`), and confirm the copied string equals the visible text.

A cursor-driven visual affordance (a pointer spotlight) must be driven by `onMouseMove`, not `:hover` alone, so it also works under automation and touch emulation.