---
name: ui-library-picker
description: Use when a UI needs a component and a library might do it better than hand-built code. Task in, library out, plus the three-layer rule and 21st.dev install flow.
---

# UI library picker

AI builds toasts, drawers, command menus and number animations from scratch, with the same default look every time. The cheapest upgrade to any interface is to stop doing that and use the right library for the job. This skill is the lookup, the order of precedence, and the prompt template.

Sources: Griffin Wooldridge's video on the three types of component library (youtu.be/zsCGS-Yzjnw, 7 Nov 2026), Emil Kowalski's `pick-ui-library` list (MIT, github.com/emilkowalski/skills), and what Champ projects already run. Each row in `registry.json` names its source.

## The picker

```bash
python3 design/skills/ui-library-picker/scripts/pick.py "toast notifications"     # one pick, why, install, flags
python3 design/skills/ui-library-picker/scripts/pick.py "drag to reorder" --all   # every match, ranked
python3 design/skills/ui-library-picker/scripts/pick.py --check path/to/package.json
python3 design/skills/ui-library-picker/scripts/pick.py --list design             # a layer
python3 design/skills/ui-library-picker/scripts/pick.py --refresh                 # re-read npm versions and licences
```

Exit code 2 and "Not covered" means the task is not on the list: go to the 21st.dev search, then shadcn, and say in one line that you left the list.

## Order of precedence (first match wins)

1. **Brand skill and DESIGN.md.** A library never overrides colour, type, radius or logo from the brand.
2. **What the project already installed.** Read `package.json` (or run `pick.py --check`). If it uses a listed library, use it. If it uses a rival (react-window instead of Virtuoso), flag it, do not churn the dependency unasked.
3. **The three layers**, below, in this order: foundation, specialist, design.
4. **21st.dev search** for anything specific the layers do not cover.
5. **Hand-built**, only when nothing above fits, and say why in the report.

## The three layers

| Layer | What it is | Examples | Rule |
|---|---|---|---|
| Foundation | Behaviour, keyboard, focus, accessibility, restyled by you | shadcn/ui, Base UI, Radix | Use for buttons, inputs, dialogs, lists, tabs. Change radius, grey and font before anything ships: the default shadcn look is the AI calling card |
| Specialist | One component done very well | Sonner (toasts), Vaul (drawers), cmdk (command menu), NumberFlow (numbers), input-otp, dnd kit, Virtuoso, Recharts | Hand-built versions overlap, do not drag, or break on keyboard. Always use the specialist |
| Design | Styled, ready-made, copied into the project | Beautiful UI (AI interfaces), RareUI (showpieces), Magic UI (animated, on shadcn), Aceternity (landing effects), 21st.dev (marketplace) | One bright accent, one animated header or one interactive background per page. Ten of them is the glowing, moving, nothing-stands-out look |

Registry also carries a motion-data layer (motion, Cobe, shiki, Satori, torph) and a plumbing layer (zustand, clsx, cva, tailwind-merge, next-themes, Lucide).

## How to use them in a build (template from the video)

1. Name the library in the request or the brief: "shadcn for base components, Sonner for notifications, Vaul for the mobile sheet, Magic UI marquee for the logo strip".
2. Install through the CLI or the registry so the code lands in the project and the agent can read and edit it. Do not paste components by hand and do not hide them behind a wrapper package.
3. Retheme: radius, colours, fonts, from the brand skill. A smaller radius plus a serif heading turns the same components from SaaS template to editorial.
4. Count accents. One per page.
5. Run `visual-verify`. Install proof is typecheck plus build plus a rendered screenshot, not "the CLI said created".

## 21st.dev flow (connected: search, get_inspiration, get_component, search_logo)

Use 21st when the task is specific, no single library covers it, or the brief asks for a section pattern (hero, pricing, testimonial, filter bar, stepper).

1. Run the picker first. If a specialist or foundation row answers it, stop there.
2. `search` the task in plain words (`type: component`, limit 6). Read names and previews, pick one, and record the id.
3. `get_component` for at most two (free tier allows two code pulls a day). Install with `npx shadcn@latest add https://registry.21st.dev/r/<owner>/<name> --yes --overwrite` when the key is set.
4. Adapt to the project stack and tokens. Single-file HTML builds port the component to vanilla and credit the id in a comment.
5. Full quirks list: `frontend-design/references/21st-registry.md`.

## Install and verify (tested 11 Nov 2026)

Fresh Vite 8 + React 19 + Tailwind 4 app, shadcn CLI, `components.json` with `@/` aliases. Findings that apply to every project:

| What | Result | Fix |
|---|---|---|
| shadcn `button` | Wrote `import { cn } from "cn"` and npm-installed a package named `cn` | Create `src/lib/utils.ts` (clsx + tailwind-merge), rewrite the import to `@/lib/utils`, `npm rm cn` |
| Magic UI `marquee` (registry JSON URL) | Clean: file, keyframes into `index.css`, typecheck and build pass | none |
| Aceternity `background-beams` (registry JSON URL) | Landed, pulls `motion`, needs `@/lib/utils`; the file has an unused variable that fails `noUnusedLocals` | Delete the unused variable |
| Beautiful UI `stream-text`, `approval-card` | Installed, but `foundation.css` has an unbalanced `}` (a media query lost its opener) so the Tailwind build fails; needs the `shadow-plugin` npm package; one component needs a type-only import; writes its own folder layout | Repair the CSS and restore the media query by hand, `npm i shadow-plugin`, fix the import. Pilot only until upstream fixes it |
| RareUI | Not install-tested (CLI is `npx rareui add <name>`) | Test before first use |

The registry URL forms that work: `https://magicui.design/r/<name>.json`, `https://ui.aceternity.com/registry/<name>.json`, `https://beautifului.dev/r/<name>.json`. Magic UI listed 260 items and Beautiful UI 27 on 11 Nov.

## Mismatches to catch on sight

- Toast built by hand, or with a modal library: Sonner.
- A div-based dropdown or dialog with manual focus handling: Base UI or shadcn.
- A number animated by re-rendering text: NumberFlow.
- A 1,000+ row list rendered directly: Virtuoso.
- A bottom sheet that only opens and closes: Vaul.
- Ten glowing effects on one page: keep one.
- Emoji standing in for icons: Lucide.

## Keeping the list honest

`registry.json` holds npm version, licence and last publish per package, with a verified date. Run `pick.py --refresh` before relying on a version, and after any big upstream release. Flags (stale, pre-1.0, MPL, repo not confirmed) are part of the answer: say them, do not drop them. Add a library only when it covers a task the list does not, with its source and a tested install; `pick.py --selftest` must still pass.

## Not verified

Beautiful UI and RareUI licences (a MIT repo exists for each name, not confirmed to be the same project). RareUI install. Aceternity Pro licensing. Vaul and cmdk against React 19 in a real build. Single-file HTML flags are conservative guesses: only motion, Cobe, shiki and NumberFlow are marked as usable without a bundler.
