# Library selection and component adoption

Use the three-layer idea from https://youtu.be/zsCGS-Yzjnw (Griffin Wooldridge, "UI Libraries for Claude Code", 7 Nov 2026): foundation for accessible behaviour, specialist for a difficult interaction, design library for a composed visual accent. Confirmed against the caption transcript on 11 Nov 2026: the three layers and the libraries named in each, retheme radius, colour and type on shadcn, one standout moment per page, name the library in the prompt, and install through the CLI or registry so the code lives in the project where the agent can read it. Ours, not the video's: the selection order below, the 21st.dev discovery step on every brief, and the licence, dependency and mounted-use proof. Captions are machine text; nothing shown only on screen was read.

## Selection order

Brand skill and DESIGN.md win. Read the host manifest and existing components next. Reuse suitable installed primitives before adding packages. Run the picker from its resolved skill directory, not from the project's cwd:

`python3 /Users/deep/champ-skills/design/skills/ui-library-picker/scripts/pick.py "<interaction or section>" --all`

The CLI ranks keyword matches, not compatibility, licence clearance or production quality. Its first result is a candidate, not an install decision. Check official docs with Context7 before writing library code. Preserve the host framework, package manager and lockfile.

| Job | Starting candidates | Reject or limit when |
|---|---|---|
| Inputs, menus, dialogs, tabs | Existing house kit, shadcn/ui, Base UI or Radix | A second primitive system duplicates the host; preserve keyboard and focus behaviour |
| Toasts | Existing feedback system, Sonner | A new package only changes minor style; essential status cannot depend on a disappearing notice |
| Mobile sheet | Existing sheet, Vaul | Drag-only dismissal or host compatibility is unproved |
| Command menu | Existing menu, cmdk | Search is not wired to real destinations or focus fails |
| Changing numbers | NumberFlow | Animation implies invented metrics; keep static and reduced-motion states |
| Large lists | Existing virtualization, Virtuoso | Small lists do not need virtualization; retain accessibility and print behaviour |
| Drag/reorder | Existing DnD, dnd kit | No keyboard alternative or dragging is not the user's job |
| Charts | Existing chart kit, Recharts, host-native SVG | Decorative charts, unsupported inference or fabricated values |
| Product/AI interfaces | Kokonut UI, Beautiful UI, 21st.dev candidates | Licence, CSS or dependency flags unresolved |
| Hero, proof, pricing, timeline, upload | 21st.dev candidates, Kokonut UI | Composition does not fit, source is locked or dependencies exceed the host |
| One expressive accent | Magic UI, Aceternity, MicroKit, RareUI candidates | Motion exceeds the story, unclear licence or no static fallback |
| Vue, Svelte, native, single-file HTML | Host-native kit; 21st.dev as named pattern reference | Never migrate to React/Tailwind for a component |

These are candidate routes, not licence or compatibility endorsements. Keep registry flags visible. Do not add a dependency merely because this table names it.

## Live 21st.dev flow

1. Call `get_usage`. Read code-retrieval quota and `aiGenerationEnabled` independently. On 11 Nov 2026 Deep's connector returned paid with unlimited component retrieval, hosted AI generation off and AI credits 0. Recheck later. A universal two-pull limit is wrong; AI credit exhaustion does not mean component access is unavailable.
2. Search the 3 to 5 structural regions before the frontend brief exists, including when the picker recommends an existing specialist. Inspect actual preview images, not only descriptions. A result id is a demo id.
3. Retrieve selected source with `get_component`; check `locked` and `found` before claiming access. Read source, demo, dependency files and licence. A preview or install URL is not component code. Never call generation when AI is disabled.
4. Main writes the selection table: region, library, name/author/id or official URL, role, host file, adaptation, licence/compatibility flags, verification. Frontend implements those picks.
5. Use the actual returned or officially documented install command, not a guessed registry endpoint. Keep credentials in the configured connector or existing secure loader, never in logs, reports, git or screenshots. Inspect CLI diffs and avoid blanket `--overwrite` on existing files.
6. Mount on the real route and wire real data/actions. Remove demo names, prices, invented metrics, remote uploads and placeholder callbacks. Client validation is not server validation or authorization.
7. Retheme fonts, neutrals, spacing, radius, elevation and states from DESIGN.md. One expressive accent is a maximum, not a minimum. Preserve a coherent family rather than stacking impressive components.
8. Prove adoption with source/import, route use, relevant build/tests, browser interaction and responsive screenshots. State whether installed source, build-rendered source or a credited native/vanilla pattern port was used. Search, bookmarking and unused installation do not count.

If the connector fails, record the failure and use a licence-cleared, previously verified local fallback when safe. If the brief requires unavailable source with no approved fallback, report a capability blocker. Do not invent ids or describe a local fallback as a live retrieval.

## Polish use

Audit before replacing. Record the top three defects and smallest fixes. Prioritize keyboard/focus, labels, contrast, loading/error/empty states, tap targets and overflow before cosmetics. Preserve the existing component family and content unless redesign is in scope. Replace with a specialist for broken behaviour or missing capability, not novelty.

Capture before/after at phone, tablet and desktop. Exercise one real interaction per changed component and reduced motion for animated ones. Close with `visual-verify` and `responsive-viewport-qa`. Report any unexercised browser, dependency, licence or device gate plainly.

## Maintain the registry

Extend `registry.json` only for an uncovered use case. Record official URL/package, layer, tasks, provenance, licence status, compatibility, checked date, install evidence and limitations. Do not call a library install-tested because npm metadata loaded. Run `pick.py --selftest` after registry/scoring changes. Sibling skills point here, never copy the rules.
