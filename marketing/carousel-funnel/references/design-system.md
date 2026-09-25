# Carousel design system (DESIGN.md for the template)

The contract behind `templates/carousel.html`. `frontend-design` owns structure, `ui-polish` removed the AI tells, `design-trends` ran the diagnosis and set the trend register below. Edit the template and this file together.

## 1. Visual theme

Product-UI editorial. The slides look like screens from the buyer's own tools (a saved view, a scorecard, an account card, a message thread) laid out as cards, with one hyper-bold headline per slide. Atmosphere slides (hook, CTA) carry a faint dot-grid texture on a navy or purple field. Data slides are flat white: no texture, no gradient, nothing on the numbers.

Logo-cover test: with the wordmark hidden, a stranger sees a revenue-ops world (accounts, tiers, signals, SDR messages). That is the buyer's world, which is the point.

## 2. Colour roles (LakeB2B instance)

| Role | Token | Value | Use |
|---|---|---|---|
| Primary | `--primary` | #6D08BE | bars, chips, numbered badges, Tier 1 fill |
| Primary soft | `--primary-2` | #7A76DA | secondary bar tone (recency 15 to 30) |
| Dark field | `--dark` | #011A6B | hook slide, navy cards |
| Accent | `--accent` | #FFB703 | the one highlighted bar per chart, progress marker, CTA pill, Tier 1 rows |
| Danger | `--danger` | #C1003C | disqualify chip and card tint only |
| Ink | `--ink` | #14122B | all text on light |
| Muted | `--muted` | #5E5A78 | notes, meta, secondary text (4.9:1 on paper) |
| Paper | `--paper` | #F7F5FB | slide background, tinted toward the brand hue |
| Card | `--card` | #FFFFFF | card fill |
| Tint | `--tint` | #EFE8FB | soft card fill, chip fill |
| Line | `--line` | #E6E2F0 | borders, bar tracks, dividers |

Neutrals are tinted toward purple so the page reads as one system (ui-polish 60-30-10). Other brands swap `primary`, `primary-2`, `dark`, `accent` in the JSON `brand` block; the neutrals stay.

## 3. Typography

Brand lock: LakeB2B faces are Montserrat (primary) and Alata (secondary). No serif display face, ever, on a LakeB2B surface. Fraunces, Playfair, Instrument Serif and friends are the AI-editorial default and were removed in the v2 rebuild.

| Element | Face | Weight | Size at 1080 | Tracking |
|---|---|---|---|---|
| Hook title | Montserrat | 800 | 86px | -0.035em |
| Point title | Montserrat | 800 | 60px | -0.03em |
| Kicker | Alata | 400 | 22px | 0.2em, uppercase |
| Lede / sub | Montserrat | 500 | 32 to 34px | 0 |
| Card title | Montserrat | 800 | 30px | -0.02em |
| Card text, notes | Montserrat | 500 | 22 to 26px | 0 |
| Chips, axis labels | Alata | 400 | 15 to 19px | 0.08 to 0.14em, uppercase |
| Stat tile value | Montserrat | 800 | 118px | -0.05em |
| Numbers everywhere | tabular numerals, Montserrat 800 | | | |

Floor: 15px for chip and axis labels (they are uppercase and tracked, which holds at phone size), 22px for any sentence.

## 4. Components

- Card: white fill, 1.5px `--line` border, 24px radius, one soft shadow (`0 18px 40px rgba(1,26,107,.10)`). Variants: `tint`, `solid` (primary), `navy`, `danger`, `flat` (no shadow). Never a coloured left or right border stripe.
- Chip: pill, Alata uppercase, tint fill. Variants `gold`, `navy`, `solid`, `gray`, `red`, `ghost` (on solid cards). Status is carried by fill plus an icon plus the word, never colour alone.
- Numbered badge: 54px rounded square in primary with the chapter number, sits inside the kicker.
- uicard: a product-style list (header row, rows with avatar square, name, meta, four signal squares, chip or score). Hot rows get the gold tint; dim rows drop to 42 percent opacity.
- Stat tile: value at 118px, label under it. Variant `gold` for the number that matters.
- hbars: horizontal bar chart in HTML (label column, bar plus value, wrapping note). One highlighted bar per chart, in gold. Bars 32px tall, 6px radius.
- columns: vertical bar chart in SVG with tones `primary`, `soft`, `gray`, `hi`, a value above each column, an axis label and optional sub-label below. Zero values render as a 6px stub so the category is still visible.
- bento: 2-column card grid for tiers or options.
- timeline: numbered 62px dots on a 3px rail, label in Alata above each step's text.
- messages: chat bubbles with a 56px avatar; `bad` bubble is muted grey with a red chip and an X icon, `good` is a white card with a purple chip and a check icon.
- account: account card with name, meta, a 118px score ring, and six dimension mini-bars.
- pagecard: a browser-window mock of the landing page (three dots plus URL, page title, chips) used on the CTA slide.
- Icons: one inline SVG family, 2.2px stroke, 28px, always beside a text label. No emoji anywhere.

## 5. Layout

1080 x 1350 frame, 80px padding, 56px chrome top and 48px bottom. Body is a flex column, centred, 34px gap. Every slide must use a different architecture from its neighbours: hook (title over UI card), tiles, chart, chart, bento, timeline plus output card, messages, chart plus account card, CTA with page mock. Sameness across slides is the strongest structural tell.

## 6. Depth

Two levels only. Cards sit on the paper with the one soft shadow. UI mocks on dark fields (uicard, pagecard) get a deeper shadow (`0 30px 60px rgba(0,0,0,.35)`) because they are the hero object. Nothing is layered on a chart, a number, or a table.

## 7. Do and do not

Do: one highlighted bar per chart; one bold phrase per block; texture on atmosphere slides only; tinted neutrals; tabular numerals.
Do not: serif display type; side-stripe borders; gradient text; glass panels; emoji; stock or AI imagery; more than two card variants on one slide; effects of any kind on a figure; em or en dashes.

## 8. Trend register (design-trends, Mode B then Mode A)

Diagnosis of v1 (2026-09-25): soulless (Part C) and dated tells (Part A). Serif display numerals and Inter body read as generic AI editorial; every slide shared one shape; the cover was type on a flat field with nothing from the buyer's world; tier cards and quotes used the side-stripe tell.

Mode B identity: the buyer's world is the CRM saved view and the scorecard, so the identity is product UI rendered as cards. Palette is the brand palette with purple-tinted neutrals. Texture is a dot grid (data-table grid, abstracted) on atmosphere slides only.

| Trend | Strength | Intent sentence | Review |
|---|---|---|---|
| Hyper-bold typography | Dominant | A VP Sales scanning the LinkedIn feed at phone size needs the one claim per slide to land before the thumb moves, and Montserrat 800 at 60 to 86px with tight tracking does that inside the brand face. | Mar 2028 |
| Multi-dimensional design (restrained depth) | Supporting | Cards with one soft shadow give the eye a felt hierarchy between the headline and the evidence without touching any figure; the deeper shadow on the hook's UI card makes the product world the hero. | Sep 2027 |
| Modular systems | Structural | One JSON schema, nine blocks, every brand swaps four tokens. Not counted against the budget. | none |

Not applied, on purpose: retro-futurism (wrong for an enterprise data buyer), organic imperfection (would fight the data-purity rule on eight of ten slides).

## 9. Acceptance

- `visual-verify` audit at 1080px: 0 FAIL. The `default-font` WARN on Montserrat is expected and accepted: it is the locked brand face, not a default.
- Every slide viewed at one third size; nothing needs a squint.
- No slide scaled below 85 percent by the renderer.
- No em or en dash in the JSON, the template, or this file.
