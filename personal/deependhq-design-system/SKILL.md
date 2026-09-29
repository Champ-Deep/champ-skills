---
name: "deependhq-design-system"
description: "The locked design system for deependhq.com (Deep's personal build-in-public site). MANDATORY TRIGGER for any work touching deependhq.com or The Deep End: building or editing a page, section, or component; \"update my site\", \"fix the homepage\", \"add a section to deependhq\", \"redesign the command page\"; reviewing or implementing a designer's mockups or a Figma handoff for the site; producing a new design handoff spec; or any question about the site's colors, type, spacing, components, or accessibility rules. Also trigger for personal-brand surfaces built in the same language. Enforces the editorial-shell / terminal-core hybrid, the density law, measured contrast, and the honesty rule."
---

# deependhq.com Design System

The locked design language for deependhq.com, Sreedeep Surapaneni's ("Deep") public build-in-public site. Apply this to every surface of that site, and to any personal-brand surface built in the same language.

## Before anything else

1. Never use em dashes. Anywhere. Copy, code, comments, annotations. Periods, commas, colons, or restructure.
2. Never name real team members on any public surface. The group patriarch is "Chief" and nothing else. Anonymize external prospects and clients in active deals to roles.
3. Deep's standing instruction: **visual-first, always.** A card full of paragraph text next to blank space is a rejected design, not a draft.

## The direction: editorial shell, terminal core

Every surface is either **editorial** or **operator**. Never both. The mode is set on a section wrapper and changes exactly four things: display typeface, accent hue, density, measure. Everything else is shared, which is what stops the site reading as two sites.

| | Editorial | Operator |
|---|---|---|
| Applies to | hero, manifesto, proof, writing index, post body, now, about, CTA, footer top | command, journey log, toolkit, field notes, status board, ticker, heatmap, constellation, terminal, build lanes |
| Display type | Fraunces 700/800, tracking -0.015em | Inter 700/800, tracking -0.03em |
| Body type | Inter 400 at 17px, lh 1.6 | JetBrains Mono 400 at 15px, lh 1.65 |
| Accent | `--win` gold #C9A84C | `--build` green #30E060 |
| Measure | 65ch cap | uncapped |
| Card padding | 24 to 32px | 16 to 20px |
| Density | one idea per block | maximum information per 100px of scroll |

Mode boundaries use one of two devices only: a 1px `--line` hairline with a 48px gold-to-green gradient at the content gutter, or an eyebrow handoff (editorial eyebrows are gold Inter 600 small caps, operator eyebrows are green mono uppercase with a leading dot).

Not doing: gold everywhere, terminal everywhere, a light mode, or a visible accent-theme switcher. The theme switcher stays as a terminal easter egg only.

## Tokens

Copy these verbatim. Do not invent new values. If something needs a value not on a scale, the design is wrong.

```css
/* surfaces */
--bg:#0D0F14; --surface:#12151D; --card:#181C26; --card-2:#1E2330;
--line:#2A2E3A; --line-2:#3A3F50;

/* text: three tiers. all AA on bg, card and card-2. */
--text:#E8E4DC;   /* 15.12:1 on bg, 13.43:1 on card */
--muted:#A8A8A2;  /*  8.02:1 on bg,  7.13:1 on card */
--dim:#8A8A92;    /*  5.60:1 on bg,  4.97:1 on card, 4.58:1 on card-2 */

/* accents, by meaning */
--build:#30E060;   /* shipped, running, live. 9.70:1 on card */
--think:#4A7BF7;   /* thinking, in progress */
--win:#C9A84C;     /* a real outcome, money, a signed thing. 7.45:1 on card */
--human:#E052C0;   /* off the clock */
--danger:#E05030;  /* broken, stale, needs attention */

/* text-only twins: the saturated hue fails AA as small text on a card */
--think-text:#6D95FF;   /* 6.00:1 on card */
--human-text:#E96BCC;   /* 6.03:1 on card */
--danger-text:#EC6A4A;  /* 5.46:1 on card */
/* think, human and danger keep full saturation for borders, dots, fills, strokes */

--{accent}-hover: color-mix(in oklab, var(--{accent}) 85%, white);
--{accent}-dim:   color-mix(in oklab, var(--{accent}) 45%, var(--card));
--{accent}-wash:  color-mix(in oklab, var(--{accent}) 12%, transparent);
--{accent}-glow:  0 0 20px color-mix(in oklab, var(--{accent}) 18%, transparent);

/* type */
--font-display:'Fraunces',Georgia,serif;      /* editorial headings ONLY */
--font-ui:'Inter',system-ui,sans-serif;        /* operator headings, all UI, editorial body */
--font-mono:'JetBrains Mono',ui-monospace,monospace;  /* operator body, all data */

--text-hero:clamp(2.5rem,5vw,4.25rem);
--text-h1:clamp(1.875rem,3.2vw,2.75rem);
--text-h2:clamp(1.375rem,2.4vw,1.875rem);
--text-h3:1.125rem; --text-lg:1.0625rem; --text-md:.9375rem;
--text-sm:.8125rem; --text-xs:.6875rem;
--track-display:-.03em; --track-serif:-.015em; --track-caps:.08em;

/* spacing: 4px base, 11 steps, no exceptions */
--s1:4 --s2:8 --s3:12 --s4:16 --s5:20 --s6:24 --s8:32 --s10:40 --s12:48 --s16:64 --s24:96

--pad:20px;  /* 32px at 40rem, 48px at 64rem. responsive page padding is mandatory */
--content-max:1200px; --prose-max:65ch; --bento-gap:14px;
--section-y:64px; --section-y-lg:96px;   /* 96px is the ceiling */

--r-sm:4px --r-md:6px --r-lg:10px --r-pill:100px
--shadow-1:0 1px 3px rgba(0,0,0,.3)
--shadow-2:0 4px 12px rgba(0,0,0,.4)
--shadow-3:0 8px 32px rgba(0,0,0,.5)
--dur-1:120ms --dur-2:200ms --dur-3:400ms
--ease-out:cubic-bezier(.16,1,.3,1)

/* breakpoints, rem based, five names, no others */
--bp-sm:30rem --bp-md:40rem --bp-lg:48rem --bp-xl:64rem --bp-2xl:73.75rem
```

Design and test at 375, 768, 1280, 1600. **375 is the binding constraint.** Grid tracks use `minmax(min(100%, 280px), 1fr)`, never a bare 300px, which overflows every phone below 414px.

## The density law

Five rules. A component failing any of them is not done.

1. No card contains more than **3 lines** of body prose. Needs more? It needs a stat, a meter, a chip row, or a link to a detail page.
2. **No section has an empty column.** A two-thirds content block in a full-width section means the remaining third carries instrumentation, meta, or a visual.
3. No two sibling cards end with identical text. Vary the CTA by content kind.
4. Interactive graphics click through to something. A node you can hover but not open is decoration.
5. Section padding tops out at 96px. Larger reads as abandonment.

Company cards must never look inactive. The phrase "quiet in the public log" is banned. Fallback order when there is no recent entry: product chips, then tags, then last-ship date. There is always something to show.

## Accessibility acceptance criteria

Non-negotiable. Verify, do not assume.

- Every text-on-background pair measures **4.5:1 or better** at body size, 3:1 at 24px+ or 19px bold. Compute it, do not eyeball it.
- **Never apply `opacity` to text.** Use `--dim`. Every historical contrast failure on this site came from stacking opacity onto already-muted color.
- Every interactive element has a visible `:focus-visible`: 2px solid `--accent`, 2px offset. No `outline: 0` without a designed replacement.
- Every touch target is **44x44 minimum**, measured including padding. A 36px control is only permitted inside 8px of surrounding padding.
- Every hover-revealed fact has a focus and a touch equivalent. Data visualizations are the usual offenders.
- Skip link and `<main>` on every page.
- Colour is never the only carrier of state. Active nav gets `aria-current`. Arc colour is paired with a text tag.
- Modals: `aria-modal`, focus trap, focus restore, Escape. Close on click, not `mousedown`.
- Reduced motion is designed, not merely disabled. A paused ticker must still convey what a scrolling one conveys.

## The honesty rule

The site's entire claim is that it is live and self-updating. So:

- Anything displaying a date shows its own age and turns `--danger` past a threshold: journal 2 weekdays, `now` 21 days, build lanes 21 days, shoutouts 30 days.
- Anything that cannot be true is not rendered. A hardcoded weather string on a Day 287 site is worse than no weather.
- Every derived number is derived at build time, never stored. Stored counts drift.
- Every failure state is designed: fetch failure, empty, stale, offline. An undesigned graceful fallback still looks like a bug.
- If the newest journal entry is more than 2 weekdays old, a stale banner renders at the top of the site, in Deep's voice. Building in public means publishing the misses.

## Performance budget

- No component's primary content requires client JS to render. Islands are for interaction, not text.
- CSS budget 40KB gzipped sitewide.
- Fonts self-hosted, subset, `font-display: swap`, maximum 4 files.
- Third-party CDN scripts only on `/command`, all with SRI, all deferred, all with a designed fallback.
- No full-viewport WebGL running while the tab is hidden.

## Implementing a designer's handoff

When mockups or a Figma file come back:

1. Diff the returned design against the tokens above. Any new value is a decision that needs an explicit reason, not a silent addition.
2. Map Figma names to code paths. The convention is `Primitive/*` to `components/ui/*`, `Journal/*` to `components/journal/*`, `Card/*` to `components/cards/*`, `Live/*` to `components/client/*`, `Editorial/*` to `components/editorial/*`. Variant properties are `mode`, `size`, `state`, `accent`.
3. Build against the Next.js app, not the legacy static kit. Target stack is Next App Router, React 19, Tailwind v4 via `@theme inline`, TypeScript strict, no `any`.
4. Server components read content directly. Client components never import the data module, they receive serializable props from a server parent.
5. Run the definition of done below before claiming a route is complete.

## Definition of done

- [ ] Renders at 375, 768, 1280, 1600 with zero horizontal scroll
- [ ] Every text pair measures 4.5:1 or better, verified
- [ ] Every interactive element has a visible focus state
- [ ] Every touch target 44x44 or larger
- [ ] No hover-only information
- [ ] No card exceeds 3 lines of prose
- [ ] No section has an empty column
- [ ] No two sibling cards end with identical text
- [ ] Every date shows its age and fails loudly when stale
- [ ] Every fetch has a designed loading, empty and error state
- [ ] Reduced-motion variant designed
- [ ] Zero em dashes
- [ ] Primary content renders without client JS

Sign off with: *That's the deep end.*
