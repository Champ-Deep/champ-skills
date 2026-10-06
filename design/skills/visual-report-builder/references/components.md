# Component library

The pieces a premium page is built from. Each entry says when to use it, the 21st.dev query that finds a good base, the MicroKit micro-interaction that pairs with it, and the tested vanilla fallback in the showcase kit (`Other/Skills/showcase-page/kit/core.css` and `core.js` in the Celsus vault). The kit classes are the default build. 21st.dev is where you look for a better base before building; MicroKit is where the hover and focus details come from.

Rules that apply to every component: brand colours come from the brand skill and override everything here; layout uses the full width (`--maxw:1600px`, gutter `clamp(16px,4.2vw,72px)`); nothing ships with an em dash or en dash; every number on a component comes from the evidence.

## How to source a component (run before building)

1. Pick the 3 to 5 components the page depends on most (usually hero, stat cards, the main chart, the table, the CTA).
2. For each, call the 21st.dev MCP `search` (free) with the query in the table below, `type:"component"`, limit 6. Use `get_inspiration` instead when the project has a `.21st/design.json`.
3. Read names, descriptions and preview images. Pick at most two to pull with `get_component` (the free tier allows 2 code retrievals a day; check `get_usage` first).
4. Adapt the pulled React and Tailwind code into the kit's vanilla HTML, CSS and JS, keeping the brand tokens. Credit the source in a CSS comment with the 21st.dev id.
5. When the MCP is not connected, say so in one line and build from the kit fallback below. Never block on it.

Connection: Cowork reads the MCP as a custom connector (`https://21st.dev/api/mcp`, header `x-api-key`). Claude Code reads it from `.mcp.json` (`npx @21st-dev/cli init --client claude --write`, then set `API_KEY_21ST`). Keys live in the environment or the connector settings, never in a skill file, a page, or the vault.

## Catalog

| Component | Use when | 21st.dev query (ids seen Oct 2026) | MicroKit pairing | Kit fallback |
|---|---|---|---|---|
| Sticky blurred nav | every page | `sticky header blur navbar` (27109, 8137) | glow follow on the primary button | `.nav` + `.nav-pill` + `.btn.btn-dark.mk-glow`; turns light past the hero via `.nav.light` |
| Scroll progress bar | any page over two screens | `scroll progress` | none | `.progress > i`, width from `--p` |
| Hero: atmospheric gradient | case studies, recaps, anything with one result to state | `hero gradient night sky`, `hero dithering card` (9940) | none | `.hero` with `{{STARS}}` and `{{CLOUDS}}` (SVG feTurbulence clouds, CSS twinkle stars), headline split by `data-words` |
| Hero: split with product card | product or partner pitch with a UI to show | `split hero product screenshot` (19078, 4710) | label swap on the CTA | grid 6/6, text left, `.panel` with the live UI right, deep soft shadow |
| Hero: editorial | reports and one-pagers where restraint wins | `editorial hero serif` | none | paper ground, mono docket line, big serif `h1`, no image |
| Floating stat cards | the three numbers that carry the story | `stat card`, `tilt card` (27139, 12244) | pointer tilt and sheen (from 27139) | `.floaters .row > .fcard` with `--tilt`, `--lift`, `data-count`, comparator `.cmp`, `.mini` bar or `.flags` |
| Client strip | anonymized client facts | `badge pills tags` | top rail glow on hover (social-highlight-cards) | `.client .pills > .pill > b` |
| Split sticky section | challenge and approach, how it works | `scroll sticky section` | spotlight rail (spotlight-indicator) | `.split .stick` left, `.steps > .step` right; JS adds the scroll-spy rail |
| Paddle stat band | results, 3 or 4 headline numbers | `stats section` (29870, 1195) | none | `.band` with `.num` (Fraunces light) and `.lab` (mono uppercase) on hairlines |
| Story cards | a grid of customer stories or case links | `case study customer story card metrics` (5574, 2201) | arrow slide-through on the card link | `.panel` with logo, serif headline, two stat rows on hairlines (see snippet) |
| Comparison table | us vs them, before vs after on several rows | `comparison table` (26827, 21218) | row accent on hover | `table.data` with a highlighted column |
| Sortable data table | rows the reader may want to reorder | `sortable data table` (35036) | animated row reorder (FLIP, from 35036) | `table.data[data-sortable]`, `th > button`, `td[data-v]`, `.ibar` inline bars |
| Timeline or stepper | a real sequence of steps | `timeline stepper scroll animation` (3734) | dots pop in on draw | `.timeline` with `--n` and `.tstep`; vertical below 760px |
| Funnel, two scales | stages with different units (accounts, then people) | `funnel chart` (10127, 2398) | none | two `.panel`s side by side, each with `.scale-note`; never one bar chart mixing units |
| Unit or dot chart | a count the reader should feel (691 accounts, 1 dot each) | `dot matrix chart` | none | `[data-waffle]` with `data-total`, `data-on`, `data-cols`, `data-cols-sm`, `data-frac` |
| Before and after units | small vs large on one unit scale (394 vs 14,662) | `before after comparison` | none | `.ucompare` with two `.waffle.fixed`, same `--dot` |
| Heat tiles | one tile per account or market | `bento grid` (9594) | lift on hover | `{{TILES}}` from build.py, `.tile.thin` flags a risk |
| Stacked bar | parts of one whole (fit, borderline, out) | `stacked bar` | none | `.stack > div[--v,--c]` plus `.stack-key` |
| Big unit dots | under 20 things (leads, meeting slots) | none needed | scale on hover | `.udots`, `.udots.ten`, `.udots.sm`, `.pend` for dashed |
| Dot map | contacts or accounts by country | `world map dots` | ring grows on hover | `sea_map()` in build.py; rasterize Natural Earth to dots, bubbles by area |
| Callout or quote | a client-reported line, labeled as such | `editorial testimonial` (9637) | none | `.callout` with `.mono` label and `small` source note |
| Closing line | the last concrete fact, large | `centered testimonial` (18914) | none | `.closing blockquote` with the final clause in `span` (greyed) |
| CTA panel | every external page | `gradient cta section` (28147) | label swap, arrow slide-through, glow follow, edge shine on the ghost button | `.cta` with `.btn-light.mk-glow` and `.btn-ghost.mk-shine` |
| Logo marquee | partner or client logos the reader may see | `logo marquee` (18221, 20147) | pause on hover | snippet below; logos via 21st.dev `search_logo` (svgl.app) |

## Snippets for pieces not in the kit page

Story card:

```html
<article class="panel story">
  <img src="data:image/svg+xml;base64,..." alt="Client logo" height="28">
  <h3 class="display">{Assertion headline: the result, stated plainly}</h3>
  <dl class="rows"><div><dt class="mono">{Label 1}</dt><dd>{Number 1}</dd></div><div><dt class="mono">{Label 2}</dt><dd>{Number 2}</dd></div></dl>
  <a class="more" href="#">Read the case<span class="arr"><i>&#8594;</i><i>&#8594;</i></span></a>
</article>
<style>
.story{display:flex;flex-direction:column;gap:18px}
.story .rows div{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--line);padding-top:12px}
.story dd{margin:0;font-family:var(--f-display);font-size:2.4rem;font-weight:350}
</style>
```

Logo marquee:

```html
<div class="marquee" aria-label="Clients"><div class="track"><img ...><img ...><!-- repeat the set twice --></div></div>
<style>
.marquee{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent);mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}
.marquee .track{display:flex;gap:64px;width:max-content;animation:mq 40s linear infinite}
.marquee:hover .track{animation-play-state:paused}
@keyframes mq{to{transform:translateX(-50%)}}
</style>
```

Logo on dark grounds: LakeB2B's logo may only sit on white, light grey, purple or navy. On the night hero it sits in a white pill (`.nav-pill`), 180px minimum width.
