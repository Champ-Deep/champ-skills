# SPAN design system (content pages)

Consolidated 3 Nov 2026 from the built SPAN pages (Zoho company profile prototype, Oracle users list and company profile, MSP and PEO/EOR landing pages). Agreed plan from the 2 Nov design setup call: one system that defines colours, type, spacing and components (buttons, icons), saved as the standard after Deep reviews it, then revisited in a weekly or monthly design review. Today it is this file plus the bundled landing page builder. There is no Figma library yet.

## 1. Pick the dialect

| Page | Dialect | Where the rules are |
|---|---|---|
| Landing page, ad page (noindex) | Brand: Montserrat, Inter, navy and SPAN Green | `SKILL.md` of this skill, then `span-landing-page` |
| Answer page, users list, company profile, comparison | Content: Mulish, mint and forest greens | This file |

## 2. Content tokens

Define these on `:root`. Dark mode follows the system setting unless `data-theme="light"` is set, and `data-theme="dark"` forces dark.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | #f6f9f7 | #0c1711 | Page |
| `--surface` | #ffffff | #122119 | Cards, answer box, menus |
| `--mint` | #eef8f1 | #163024 | Hover, audio strip, soft fills |
| `--rule` | #dce7df | #24392d | Borders, dividers, bar tracks |
| `--ink` | #35453b | #cfdcd3 | Body text |
| `--head` | #2e4a3a | #e3efe7 | Headings, strong text |
| `--muted` | #5b6b61 | #97aa9d | Meta, captions, labels |
| `--green` | #27b441 | #3fcf5c | Focus ring, bar fills, accents |
| `--green-d` | #036733 | #7fdc90 | Links, primary button ground (light) |
| `--deep` | #06331c | #0a2a18 | Monogram tile, dark ink on light green |
| `--on-deep` | #e9f6ee | #e9f6ee | Text on `--deep` |
| `--amber` | #7a4d00 | #f2c062 | Amber pill text (use #7a4d00 on light, not #a86a00, for contrast) |
| `--amber-bg` | #fff4dc | #3a2d10 | Amber pill ground |
| `--red` | #b5432f | #f08d78 | Dropped, negative |
| `--red-bg` | #fbe9e5 | #3a1c16 | Red pill ground |

Dark mode contrast rule: `--green-d` turns light in dark mode, so white text on a primary button or play button fails. In dark mode set the primary button ground to `--green` and its ink to #06331c. Same for a selected segment button.

## 3. Type

Mulish only (`family=Mulish:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400`), system sans as fallback. Title case headings. No eyebrow line above a heading.

| Use | Size | Weight |
|---|---|---|
| Body | 16px, line-height 1.6 | 400 |
| Answer box, section lead | 18px, line-height 1.65, lead capped at 72ch | 400 |
| H1 | clamp(2rem, 3.6vw, 3.1rem), letter-spacing -.01em | 800 |
| H2 | clamp(1.5rem, 2.2vw, 2rem) | 800 |
| H3 | 1.15rem | 700 |
| Meta, crumbs | .88 to .9rem, `--muted` | 400 |
| Fact label | .78rem, uppercase, letter-spacing .06em, `--muted` | 700 |

Headings use `line-height: 1.2` and `text-wrap: balance`. Numbers use `font-variant-numeric: tabular-nums`.

## 4. Layout and spacing

- Content width: `max-width: 1560px`, side gutter `clamp(16px, 4vw, 56px)`.
- Page grid: main column plus a 300px "On this page" rail, gap `clamp(24px, 4vw, 64px)`. Below 1100px it is one column and the rail drops below main.
- Section gap 72px, `scroll-margin-top: 90px`, page padding 40px top and 80px bottom.
- Radii: card 16px, answer box 14px, button 10px, monogram tile 12px.
- Focus ring: `outline: 3px solid var(--green); outline-offset: 2px` on every interactive element.
- Tap targets 44px or more. Tables scroll inside their own container, never the page.
- Check at 390px and 1440px, light and dark.

## 5. Components

| Component | Spec |
|---|---|
| Top bar | Sticky, 64px min height, 88% `--bg` with blur, bottom rule. Brand left, breadcrumbs, tools right. |
| Button | 42px high, 10px radius, 1px `--rule` border, `--surface` ground, 700 weight, 16px inline SVG icon. Hover: border `--green`, lift 1px. |
| Primary button | `--green-d` ground, white ink, 52px min height, arrow nudges 5px on hover. One per page region. |
| Ask AI menu | Button opens a 230px menu of four links (ChatGPT, Claude, Perplexity, Google AI Mode), each with a prompt naming the page URL. |
| Answer box | `--surface`, 1px border mixing 40% `--green` into `--rule`, 14px radius, 22px 24px padding, 18px text. 40 to 60 words. |
| Audio strip | `--mint` ground, 44px round play button, 6px track, transcript in a `details` element. |
| Card | `--surface`, 1px `--rule`, 16px radius, 24px padding. |
| Facts grid | Two columns, label above value, hairline between rows. 3 to 5 facts. |
| Bars | One scale for every bar in a block. Fill width equals value. Track is `--rule`. |
| Segment counter | Region by size selector returning companies and contacts, driven by the data team's breakdown sheet. |
| Rail | "On this page" links plus related lists. |
| Build notes toggle | Prototype only. Lists open items. Remove before publish. |

Icons: inline SVG, 16px in buttons, stroke style, `currentColor`. No icon font, no emoji.

For anything interactive beyond these, take a component from 21st.dev and port it to vanilla if the page is static. Credit the source in the build notes.

## 6. Rules that apply to every SPAN page

- Zero em and en dashes (`grep -cP '\xe2\x80[\x93\x94]' file` prints 0).
- Every number has a source and a date. SPAN counts come from the data team in writing. Unconfirmed numbers stay out or sit in [brackets] on a prototype.
- Never redraw a third-party logo. Name and logo only to identify the company.
- Light and dark both ship, or the page says which it supports.

## 7. Governance

1. Harsha builds. Writers supply structured content only.
2. The first two or three pages get Preeti's or Manu's approval before any deployment, then review is weekly.
3. A token, component or spacing change goes into this file first, with a one-line reason, then into pages. Pages never carry a private variant.
4. Deep reviews this file. A weekly or monthly design review keeps it current.

## 8. Known gaps

- No icon set is defined beyond "inline 16px stroke SVG".
- No spacing scale beyond the values above.
- No Figma library. If one is built, it must mirror section 2 token for token.
- The reference CSS lives in Deep's vault prototypes (Zoho company profile, Oracle pages). Ask Deep for a copy until it is bundled.
