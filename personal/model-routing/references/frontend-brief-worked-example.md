# Frontend brief: worked example

Assembles `frontend-brief-template.md` into five cards in one pass: one shared
rules block at the top of every card, then each card's own numbered spec.

## Shared rules (identical block on all five cards)

- Stack: Next.js App Router, Tailwind, shadcn/ui. Components come from the
  21st.dev registry; the key is in the environment. Block kind=capability if the
  key is missing rather than hand-rolling a substitute.
- Design tokens: `--background #0B0F14`, `--accent #FFB703`, `--muted #8B93A1`.
  The reference mock's blue is not ours: map mock-accent to `--accent` and never
  copy its palette.
- Data honesty: every figure cites its source file in `data/*.json`. Unknown
  fields are empty strings in `config.json` and the element hides, never a
  placeholder value.
- Acceptance: `npx tsc --noEmit` clean, `npm run build` clean, Playwright pass at
  390 and 1440 with screenshots to `/tmp/shots/<section>/`, zero console errors,
  `grep -rn '—' src/` returns nothing.
- Do not touch: `data/`, `research/`, any branch other than `feat/<card-slug>`.
  No commits to main, no pushes outside this branch.
- If you must block: DECISION / A recommended / B / C / default / reply format.

## Card 1: hero and nav

Reuse: `src/components/nav.tsx` (restyle only), `public/logo.svg` (port exactly).
Spec: (1) sticky nav, 64px, logo left, three links right, collapses to a menu
below 768px. (2) Hero headline from `config.json#heroTitle`, subhead, one CTA
linking to `#pricing`, terrain SVG background with a reduced-motion fallback to
a static frame.
Gate: nav collapses at 768px, CTA href is exactly `#pricing`, the 390 screenshot
shows `scrollWidth <= 390`.

## Card 2: pricing table

Reuse: `data/pricing.json` verbatim (prices and names are correct, port exactly).
Spec: three tiers, monthly and annual toggle, the annual figure read from the
same file. An empty `config.json#taxNote` hides the footnote.
Gate: the toggle renders the annual figure from the file; the footnote is absent
when the field is empty; screenshots at 390 and 1440.

## Card 3: FAQ accordion

Reuse: `data/faq.json` verbatim.
Spec: seven items, first open by default, only one open at a time, keyboard
operable (Enter and Space toggle, visible focus ring).
Gate: driving every item open and closed in Playwright logs no console error,
and the open count never exceeds one.

## Card 4: footer

Reuse: `src/components/footer.tsx` (restyle only).
Spec: four columns, no social icons for which we hold no asset: omit them, do
not substitute an icon set.
Gate: `grep -rn 'href="#"' src/components/footer.tsx` returns nothing.

## Card 5: handover

No build. The worker collates: stack choice, screenshots by absolute path in
`artifacts`, every empty field in `config.json`, each gate's output verbatim, and
what was skipped. Opens a draft PR into `main`, never merges.
Gate: PR exists with the section names in its description; `artifacts` carries at
least ten screenshot paths; the completion summary quotes every gate's output.