# Warm Editorial Design Language (embedded reference)

Self-contained implementation reference for the executive-one-pager skill. Extracted from independenceos.ai (2026-07-08) and refined through first-proof review. If a fuller local standard exists in the workspace, prefer it.

## The five moves

1. **Warm paper, not white.** Canvas `#EDEBE1` with soft radial washes and drifting specks. Nothing pure white or black.
2. **Serif voice, sans body, mono data.** Spectral speaks the big ideas (one italic emphasis word per headline), Hanken Grotesk carries reading, letterspaced uppercase mono labels every datum.
3. **Hairlines, not boxes.** 1px dividers at 7-12% ink alpha structure the page.
4. **The page is alive.** Micro-UI vignettes, pulsing dots, steppers, typewriters. Ambient telemetry, not fireworks.
5. **One accent, generous space.** Accent at 100% and ~10% alpha does 90% of color work. Prose measure 620-680px.

## Tokens (copy verbatim, swap only --accent per brand)

```css
:root {
  --paper:#EDEBE1; --cream:#F6F4EC; --cream-2:#FBFAF4;
  --ink:#1C1D16; --muted:#7C7B6B;
  --hairline:rgba(20,21,15,.12); --hairline-soft:rgba(20,21,15,.07);
  --accent:#2C8175;                      /* SWAP per brand; deepen if needed for paper contrast */
  --accent-soft:rgba(44,129,117,.10);    /* accent at ~10% alpha */
  --green:#2C8A5C; --green-soft:rgba(44,138,92,.11);
  --amber:#B08C46; --amber-soft:rgba(176,140,70,.13);
  --shadow-card:0 18px 40px -22px rgba(28,52,44,.34), 0 6px 30px -8px rgba(44,129,117,.18); /* tint from accent */
  --r-chip:2px; --r-ui:6px; --r-card:14px; --r-pill:999px;
  --serif:'Spectral',Georgia,serif;
  --sans:'Hanken Grotesk',-apple-system,'Segoe UI',sans-serif;
  --mono:ui-monospace,'SF Mono',Menlo,monospace;
}
```

Fonts: `Spectral:ital,wght@0,400;0,500;1,400;1,500` + `Hanken+Grotesk:wght@400;500;600;700`.

Known brand accents: Champions Group `#E05A14` (from #F26722, deepened for paper), Lake B2B `#6D08BE` purple (+gold #FFB703 aurora), Ampliz per its guidelines. Always re-derive `--accent-soft` and the shadow tint.

## Typography

h1: Spectral 500, 40-58px, lh 1.06, ls -0.018em, one `<em>` word, ends with period. h2: sans 600, 26-31px, ls -0.015em, ends with period. Serif tagline: Spectral 400 20-22px with italic pivot. Body: sans 400 17px lh 1.62. Micro-label: mono 10.5-11px uppercase ls .08-.14em muted. Prose max-width 620-680px.

## Atmosphere

```css
.aurora { position:fixed; inset:-15% -28%; z-index:0; pointer-events:none; filter:blur(30px);
  background:
    radial-gradient(40% 42% at 20% 24%, /*accent @ .08*/, transparent 72%),
    radial-gradient(38% 40% at 82% 38%, /*secondary @ .09*/, transparent 72%),
    radial-gradient(34% 36% at 55% 92%, /*tertiary @ .05*/, transparent 72%);
  animation:aurora 34s ease-in-out infinite alternate; }
@keyframes aurora { 0%{transform:translate3d(-2.5%,-2%,0) scale(1)} 50%{transform:translate3d(2%,1.5%,0) scale(1.06)} 100%{transform:translate3d(-1.5%,2.5%,0) scale(1.03)} }
```

Hero particle field: `<canvas>` absolute over hero, ~40-60 specks (dots 1-2.5px + small `+` crosses, ink at 8-14% alpha, ~30% in accent), slow drift (0.05-0.2px/frame), twinkle via sin, wrap at edges, and critically:
`mask-image:radial-gradient(130% 120% at 50% 28%, #000 45%, transparent 95%);`

## Reveal + progress

```css
.rise { opacity:0; }
.rise.in { animation:rise .8s cubic-bezier(.2,.6,.2,1) forwards; animation-delay:calc(var(--i,0)*80ms); }
@keyframes rise { from{opacity:0; transform:translateY(16px)} to{opacity:1; transform:none} }
```
IntersectionObserver (threshold .12, rootMargin '0px 0px -6% 0px') adds `.in`. Fixed 2px scroll progress bar in accent at top.

## The alive keyframe library

```css
@keyframes pulse   {0%{transform:scale(1);opacity:.7} 80%,100%{transform:scale(3.4);opacity:0}}   /* live-dot ::after ring */
@keyframes wavebob {from{transform:scaleY(.5)} to{transform:scaleY(1)}}                            /* waveform bars, alternate, random .5-1s */
@keyframes mstep   {0%,100%{opacity:.35} 5%,20%{opacity:1}}                                        /* pipeline nodes, shared duration, staggered delays */
@keyframes mcaret  {0%,100%{opacity:1} 50%{opacity:0}}                                             /* typewriter caret */
@keyframes mblink  {0%,100%{opacity:1} 50%{opacity:.3}}                                            /* syncing */
@keyframes mscan   {from{transform:translateX(-130%)} to{transform:translateX(320%)}}              /* shimmer sweep */
@keyframes mglow   {0%,100%{box-shadow:0 0 0 0 transparent} 50%{box-shadow:0 0 0 3px var(--accent-soft)}}
@keyframes mreorder{0%,16%{opacity:0} 24%,72%{opacity:1} 82%,100%{opacity:0}}                      /* looping notification */
@keyframes mbump   {0%,100%{transform:scale(1)} 40%{transform:scale(1.14)}}                        /* number update */
@keyframes mrise   {from{opacity:0;transform:translateY(7px)} to{opacity:1;transform:none}}        /* row entrance */
@keyframes cmapflow{to{stroke-dashoffset:-17}}                                                     /* SVG dashed connector flow */
@keyframes mqscroll{to{transform:translateX(-50%)}}                                                /* marquee */
```

Discipline: waveforms/steppers may be dense; pulse rings max 3-4 visible; loops slow and low-contrast.

## Component recipes

**Eyebrow**: 6px accent square + 13px semibold label, opens every section.
**Section numbers**: bare mono `01`, never "§".
**Card**: cream-2, 1px hairline, r-card 14px, tinted shadow, padding ~20px; hover translateY(-2px) + deeper shadow, transitions `box-shadow .3s, transform .3s`.
**mock-head**: mono 11px uppercase ls .11em + live-dot + right context label.
**Code rows**: cream bg, r-ui, mono 11.5px, accent keyword + value + right-aligned status; enter with mrise staggered.
**Chips**: mono 10.5px, 2px radius, tinted bg. **Pills**: 999px, tinted bg + matching text.
**Key-value rows**: label left, value right, hairline-soft dividers. INTERACTIVE: hover tints bg accent-soft, pads left 9px, reveals mono `✓ verified` glyph (opacity 0→1).
**Stepper**: 11px circle nodes + hairline bars, mono labels, nodes animate mstep with staggered delays.
**Vertical cadence timeline**: nodes on a hairline spine, mono date kicker in accent, title + muted line.
**Horizontal numbered timeline**: outlined mono-number circles joined by a hairline, kicker + title + body.
**Marquee**: duplicate children once, flex track, `mqscroll 52s linear infinite`, hairline top/bottom, serif 19-20px muted names, pause on hover.
**Statement band**: Spectral 400 24-31px lh 1.42 with one italic pivot phrase.
**Keyword highlight (.hl)**:
```css
.hl { font-weight:600; padding:0 3px; border-radius:3px; position:relative;
  background-image:linear-gradient(120deg,var(--accent-soft),var(--accent-soft));
  background-repeat:no-repeat; background-size:0% 82%; background-position:0 62%;
  transition:background-size .9s cubic-bezier(.2,.6,.2,1) .3s; }
.in .hl { background-size:100% 82%; }
.hl::after { content:''; position:absolute; inset:0; border-radius:3px; pointer-events:none;
  background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.55) 50%,transparent 70%);
  background-size:220% 100%; background-position:200% 0; }
.hl:hover::after { animation:hlshine .9s ease forwards; }
@keyframes hlshine { to{background-position:-20% 0} }
```

## Micro-visual vocabulary (for insight cards and stats)

- **Channel/mix bars**: mono label (78px) + 5px track + fill (`display:block`!) animating to `var(--w)` on `.in`; dim fills `rgba(20,21,15,.20)` for the "missing" channels.
- **Region/entity rows**: live-dot + name + right-aligned status pill, hairline-soft dividers.
- **Rising spark**: flexed `<i>` bars (max-width ~300px), scaleY(0)→1 staggered via inline transition-delay, last bar full opacity.
- **Before/after bars**: two labeled rows, dim fill for "before", accent for "after", widths derived from stated numbers only.
- **Delta pill**: mono `↑ 25%` on green-soft.
- **Dot grid**: 20-col grid of tiny circles, N lit in accent for a rate (4.2% → 4 of 100 lit), lit dots mblink.
- **Compact stat grid**: 2x2 hairline grid nested into a column's dead space; num 25px + mono label. Full-width stat strips: one per page maximum.

## Binding rules (non-negotiable)

1. No em-dashes anywhere.
2. No text-only cards: every card carries a content-derived micro-visual.
3. Stats nest into dead space; audit every section for dead space before shipping.
4. Highlight only VALUE phrases, 2-4 per section.
5. Rows respond to hover individually; CSS-only, no layout shift.
6. Stat visuals derive from stated numbers only; never invent benchmarks.
7. Icons: inline stroke SVG (18/12px, stroke 1.5, currentColor). Never emoji, never icon fonts.
8. Never pure #FFF/#000. Check contrast on every tinted surface. Text color always explicit.
9. Headlines end with a period.
10. Bar/spark fills must be `display:block` (inline spans silently ignore width/height).
11. `prefers-reduced-motion`: disable all animation, `.rise { opacity:1 }`.

## JS snippets

```js
// reveal
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), {threshold:.12, rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rise').forEach(el => io.observe(el));

// marquee
const mq = document.getElementById('mq'); mq.innerHTML += mq.innerHTML;

// typewriter: type 34-80ms/char, hold 2100ms, delete 13ms/char, loop lines

// waveform: 14 bars, height 6-26px random, duration .5-1s, negative random delay

// particle field: devicePixelRatio-aware canvas, see atmosphere section
```
