---
name: research-to-visual
description: "Entry point for any visual page built from text; routes to one-pager, report or showcase. Turns text research (notes, reports, transcripts, briefs, memos, data dumps) into a single-file visual HTML page. Three formats from one pipeline: executive one-pager (decision page), visual report (editorial, multi-section), showcase page (scroll page that proves a result). Use whenever the user wants research made visual, a one-pager, a report page, a leave-behind, a case study page or a 'make this look premium'."
---

# Research to Visual

Input is text we already researched. Output is ONE self-contained `.html` file a busy reader understands in ninety seconds, on a phone, in light or dark. You do not add research. You find the answer in the text, find the numbers, decide what the reader must do, and give each piece of evidence a visual.

Start from `assets/starter.html` (tokens, verdict block, bars, tick strip, table, option cards, details, motion). Copy it, swap the brand tokens, delete what you do not need. Check your result with `scripts/verify.py` when a browser is available.

## The one test

Cover everything below the first screen. Can the reader still act? If not, the page failed, however good the rest looks.

## Step 1: Pick the format

If the user named one, use it. Otherwise pick by the reader's job and say which in one line. Ask at most one question, only if the reader or the ask is truly unknowable from the text; otherwise state your assumption and proceed.

| Format | Use when | Shape | Height budget | Then load |
|---|---|---|---|---|
| **One-pager** (default) | A decision-maker needs the answer and an ask. Summaries, follow-ups, leave-behinds, status readouts | Verdict, at most 5 evidence sections, next steps | 3,000px at 1440, 6,500px at 390 | `executive-one-pager` |
| **Report** | A reader will study it or come back to it. Audits, campaign results, market scans, competitor landscapes, strategy briefs | Hero with stat strip, 4 to 8 numbered sections each with a thesis heading and a visual, closing question, footer | 4,000 to 6,000px at 1440 | `visual-report-builder`; for a campaign report also `campaign-visualization` for its full-width review layout |
| **Showcase** | The page must prove one result to a skeptical buyer. Case studies, campaign wins, event recaps, partner pages | Atmospheric hero with the result as headline, 3 floating stat cards, split challenge/approach, main chart section, stat band, closing fact, CTA | 4,500 to 6,500px at 1440 | `showcase-page` |

This skill decides the format and the verdict brief; the "Then load" skill carries the craft for that format (templates, components, export). Load it after Step 2, before any HTML. An audit or pitch document rendered for a chairman or a client is a Report, never a Showcase: a showcase proves a result we delivered, an audit proves a problem we found.

When writing a card for the `frontend` lane, name `research-to-visual` plus the chosen format in the brief ("research-to-visual, Report format, Champions brand"), not the format skill alone. A card that names only `visual-report-builder` skips the format decision and the verdict brief, and the worker starts at the template.

When in doubt between one-pager and report, choose one-pager: shorter wins.

## Step 2: Distill the text into a verdict brief

Before any HTML, write this brief (in your working notes, not in the page). Every field comes from the source text.

| Field | What it holds |
|---|---|
| Reader | Who opens it and who decides. Write for the decider. |
| Answer | One sentence. Becomes the headline. State the conclusion, not the topic. |
| Three numbers | The figures that most change the reader's mind. Each with a comparator (target, deadline, prior period, share of whole) and a source. |
| Ask | One action with owner and date. Reports may carry up to three. If the source states no ask, the ask is the decision the answer implies; say it is inferred. |
| Evidence | Three to five points, each tagged with the visual that proves it (Step 4). |
| Gaps | What the research did not establish. These become visible "not established" items, never silent omissions. |
| Detail | Quotes, per-item paragraphs, source notes. These go behind `<details>`. |

If the research has few numbers, do not invent any. Use structure visuals instead: comparison matrix, ranked list with status glyphs, timeline, 2x2, option cards, a source-agreement strip ("3 of 8 sources agree").

## Step 3: Hard rules

1. **Never invent a fact.** No numbers, dates, durations, names, causes or estimates that the text does not state. Arithmetic on stated figures is allowed (rates, shares, multiples, "28 to go") and is labeled as computed. No extrapolation. If the text gives "this week", the page says "this week", not a calendar date.
2. **Keep the source trail.** Every figure and finding keeps its source (document, person, date) in a small mono line or the detail layer. Mark each claim as stated by the source, computed by you, or inferred. Sources that conflict are both shown.
3. **Audit the source before quoting it.** Add up tables before quoting a headline total. If a total does not equal its breakdown, show both and say so. If a percentage has no stated comparison period, label it "vs an unstated prior period". A metric that moved the same week as a change is "same week", never "because". Figures you did not re-measure get a footer line: "As reported, not independently re-measured."
4. **Verdict on screen one.** At 390 by 844 the first viewport holds the headline, three numbers with comparators, and the first ask.
5. **Assertion headlines.** Every section heading is a full-sentence conclusion the reader could repeat in a meeting, ending with a period ("Three of nine are blocked, and each has a known unblock."). Never a topic label ("Campaign results").
6. **Visual first, text second.** Each section leads with a visual and carries at most three lines of text. Removal test: if deleting the visual loses no meaning, it is decoration; cut it or replace it.
7. **Numbers carry comparators.** "62%" alone is nothing. "62% of 40 accounts, vs 35% target" is a finding.
8. **Claim audit.** Every count in the headline or lead equals what the page renders. An FYI never sits in an asks list. Re-run this after every content edit.
9. **The accent means the reader.** The brand accent marks only what the reader must act on: the ask panel, the decision phrase in the headline, "on you" items. Charts and decoration use ink and neutrals.
10. **Status is shape plus colour.** Blocked is a square, needs-the-reader is a diamond, moving is a half ring, on track is a dot, done is a check. Include a small legend.
11. **Progressive disclosure.** Detail sits in native `<details>`, closed by default. The page is fully readable at rest: nothing parked at `opacity:0` waiting on a script.
12. **No dashes.** Zero em dashes and zero en dashes anywhere (headings, labels, date ranges, chart text). Use commas, periods, colons, "to", or a slash.
13. **No AI tells.** No short horizontal rule before an eyebrow. No emoji as markers. No purple-to-blue gradients. No four-up stat grid under a gradient hero. No identical white rounded card with a corner pill repeated down the page. No coloured side-stripe on cards. No 01/02/03 numbering on things that are not a sequence. Hero eyebrow is plain sentence-case text; keep spaced mono uppercase for small data labels only.
14. **Copy gate.** No binary contrasts ("not X but Y"), no colon reveals as a rhythm device, no dramatic fragments, no kicker aphorisms, no puffery, no throat-clearing. Short sentences, plain words, active voice. Asks start with a verb. The closing line is the most concrete fact on the page.
15. **Full width.** Container up to 1440px (showcase: 1600px) with a fluid gutter `clamp(16px,4vw,64px)`. Never a narrow centered column with dead space either side.
16. **Mobile-first, both themes.** Base CSS targets 390px: one column, 16 to 17px body, 44px tap targets, no horizontal overflow. `min-width:860px` adds columns. Light on bare `:root`, dark under `prefers-color-scheme: dark` plus `[data-theme="dark"]`. `body` paints its own background. Grid tracks use `minmax(0,1fr)`; wide tables sit in an `overflow-x:auto` wrapper.
17. **Contrast is measured, never eyeballed.** Text 4.5:1 (3:1 for 24px+ or 18.66px+ bold), including text on the accent. White on `#F26722` fails; use ink text on that orange. Dark text on a light accent panel: tint insets with white, never with ink.
18. **Real logos only.** Use a logo file the user supplied, never a drawn substitute, and never box it in a white pill. No logo supplied: use a plain text wordmark.
19. **Client-facing pages anonymize.** Describe clients by industry, size and region. Never name an outside delivery vendor to a client; vendors are "we" or "our team". Internal pages may name them. Respect any hold or do-not-send note in the source.
20. **One file, no frameworks.** Inline CSS and JS. Google Fonts is the only external request (Chart.js from jsDelivr only if a line chart is unavoidable). Icons are inline stroke SVG. Scope or namespace classes if the page may be embedded.

## Step 4: Choose the visual from the data shape

| Data shape | Visual |
|---|---|
| One headline count | Big number cell with comparator |
| Ranking of 3 to 8 items | Horizontal bars, value on the mark, sorted descending |
| Part of a whole, 2 to 4 parts | Stacked bar with a key of shares (round so they sum to 100) |
| Progress toward a target | Tick strip of N cells, plus "X to go in Y days" |
| Before and after | Paired bars or delta cells from stated numbers |
| A count the reader should feel (under about 500) | Unit dots, 1 dot = 1 item, caption says so |
| Many items with one value each | Heat tiles sorted by value |
| Stages with different units (accounts, then people) | Two panels, each with its own scale and a "Scale: ..." note. Never one chart mixing units |
| Rows compared on several columns | Hairline table, right-aligned tabular numerals, a computed rate column, a `tfoot` total, a note saying how it is computed |
| Options for an open decision | Two or three option cards with cost, time, risk chips; recommended one marked |
| Several workstreams or findings with status | Status board: segmented mix bar plus rows with shape glyph, name, one-line state, date, `<details>` for the paragraph |
| An overdue decision | Aging bar from opened to today, deadline tick, overrun hatched |
| A real sequence or next 7 days | Timeline or stepper with a today marker |
| Objections or risks | Ranked rows with severity glyph and a one-line answer each; 2x2 for four or more |
| Source agreement or confidence | Strip of N cells, one per source, filled when it agrees |
| Geography | Ranked bars by country (a dot map only if you can draw it cleanly) |
| A trend over 8+ points | Hand-built SVG line, or Chart.js |

Chart rules: values sit on or beside the mark; bar widths are computed from the stated number, never by eye; dot and bubble sizes scale by area; colour encodes one thing per chart (accent or ink for "ours", neutral for "missing", red outline for a risk); every chart has a one-line caption saying what a mark means; each unit gets its own scale.

## Step 5: Design treatment

Pick one by the page's job, and record the choice and the reason in one HTML comment at the top of `<style>`. Spend boldness in one place; keep the rest quiet. Do not reuse the previous page's treatment unless the pages are a matched series.

| Treatment | Job | Structure and type | The one bold move |
|---|---|---|---|
| **Docket** | internal readouts, board and chairman updates | near-white ground, 1px hairlines, 3 to 4px radii, mono docket line over a 2px ink rule, rows not cards. Inter Tight 800 display, Inter body, JetBrains Mono labels | the ask panel as a solid brand-colour block with ink text |
| **Deal Room** | client follow-ups, leave-behinds, partner pitches | white surfaces on a faint brand-tinted ground, one full-bleed verdict band in the brand's deepest colour. Schibsted Grotesk display, Source Sans 3 body, IBM Plex Mono labels | the three numbers set huge inside the verdict band |
| **Editorial dark** | visual reports | dark ground, serif display (Fraunces) with one italic word, sans body, mono data labels, section tags like "01 / The setup", stat strip on hairlines | stat strip and numbers as the heroes |
| **Atmospheric** | showcase pages | one atmospheric hero moment (gradient sky, glow horizon), word-by-word headline, floating stat cards, Paddle-style stat band, real charts | the hero and the animated main chart |

One-pager defaults to Docket (internal) or Deal Room (external). Report defaults to Editorial dark. Showcase uses Atmospheric. `assets/starter.html` is Docket; adapt it for the others.

### Brand

If the user names or supplies a brand, lock its colours, fonts and logo; brand rules override every treatment colour. Take brand accents from this table when the brand is named; otherwise use the neutral theme.

| Brand | Accent | Notes |
|---|---|---|
| Champions Group | fill `#F26722`; accent text `#B8420A` on light, `#FF9A62` on dark | text on the orange fill is ink `#1A1A1A` |
| Lake B2B | purple `#6D08BE`, red `#E8033A`, gold `#FFB703` | Montserrat body; full-colour logo on light, reversed on dark; 180px minimum |
| Neutral (no brand) | `#3B4BD8` blue, `#D9480F` orange | paper `#FBFAF7`, ink `#17161A`; Fraunces display, Inter Tight body, IBM Plex Mono labels |

A client works with Lake B2B or SPAN, never both; strip the other from client pages. For a brand you have no tokens for, measure the dominant colours from the supplied logo, take one geometry cue (corner treatment, dot or ring), and note the derived tokens in a CSS comment. Never invent a palette and call it theirs.

## Step 6: Interaction and motion

Every interactive element gets a hover and a `:focus-visible` response; one micro-interaction per element, 200 to 500ms, `cubic-bezier(.16,1,.3,1)`, brand colours.

| Element | Response |
|---|---|
| Primary button | label swap (a duplicate label rises in) and arrow slide-through |
| Table row | tint plus accent bar on the first cell |
| Pills and chips | lift 2px |
| Panels | shadow deepens |
| `<details>` | chevron or plus rotates |
| Filters, tabs, toggles | a `radiogroup` with roving focus, a live count of what is shown, and a selected state that reads in both themes (light: ink fill, white text; dark: brand fill, ink text). Never animate `width` or `height` of the travelling thumb; animate `clip-path` |
| Showcase only | pointer tilt on floating stat cards, spotlight rail on step lists, sortable table with row glide |

Motion rules:
- Motion explains (a bar grows to its value) or it does not ship.
- Opt-in by script: add `html.motion` only when JS runs, IntersectionObserver exists, reduced motion is off, and the URL has no `?static=1`. Hidden start states are written under `.motion`, so a page without JS is complete.
- Final values live in the HTML. Count-ups end on the exact stated value.
- Animate `transform` and `opacity` only.
- One-pager: transform-only reveals (start at `translateY(12px)`, full opacity) or none; no ambient particles, no tilt cards. Showcase and report may rise-and-fade on scroll (28px, 900ms) with 60 to 150ms sibling stagger, bars growing with `scaleX` over 1.1s, one orchestrated load sequence in the hero.
- `prefers-reduced-motion: reduce` removes every animation and transition.
- `?static=1` adds `html.static`: no animation, every reveal in its end state. Use it for PDF and PNG export.
- Interactive controls must be proved by driving them: assert the filtered count, the selected state, state after reload, and reset. A page that looks right can still have dead buttons.

## Step 7: Build order

1. Copy `assets/starter.html`. Set brand tokens and treatment.
2. Build the verdict first. Put `data-fold` on the headline, each of the three numbers, and the first ask heading. Measure it at 390 before adding anything else.
3. Add sections one at a time, visual first. Stop at the budget; move the rest into `<details>` or cut it.
4. Write copy (Step 3, rules 5 and 14) as you go, not after.
5. `<title>` is a short name specific to the subject and reader.

## Step 8: Verify (do not skip)

1. Run `python3 scripts/verify.py page.html --shots` (adjust `--budget1440` and `--budget390` for report and showcase). It checks dashes, horizontal overflow, the fold at 390, height budgets, tap targets and console errors at 390 light, 1440 light and 390 dark. A failed Google Fonts request in a sandbox is expected and ignored.
2. Open the screenshots and look at them. Check: five-second test (from the 1440 top alone, write one sentence of what the page recommends and what it asks), every section's visual survives the removal test, labels on bars do not collide at 390, selected states are visible in dark, the content spans the page at 1440.
3. Measure contrast for every text class you shipped, against the composited background, including the element's own `opacity`.
4. Re-run the claim audit (rule 8) and a source check: every number traces to the research text or is labeled computed.
5. If the page is over budget, measure the height of each top-level block, cut the tallest, re-run. Cheap levers first: widen assertion headline `max-width` to about 44ch, shorten sub-lines under 82 characters, match grid column count to item count, then padding. Leave at least 100px of slack at both viewports.
6. The bar: would a design-led SaaS company ship this? If a section is a text box with a number in it, add its visual or cut it.
7. If no browser is available, say so and label the page UNVERIFIED, listing what was not checked.

## Mechanism figure: the Anatomy skill (verified 2026-10-26)

When a page must explain HOW something works and the idea has a physical mechanism (rate limiter, cache, pipeline, deploy flow, verification gate), an `anatomy` isometric figure can replace a whole paragraph: a real object built from shaded parts, SVG output, optional WebGL, one HTML file the reader can poke.

- Installed at `~/.hermes/skills/creative/anatomy` (wheresryan22/anatomy, MIT, 0 npm deps, Node 20.10+). Verified here: its 290 tests pass and `examples/push-button/build.mjs` builds and renders a complete framed figure with a live readout.
- It is NOT a chart library: no axes, no series, no data plots. Numbers only appear as a live readout inside the figure. Charts stay with this skill's chart set.
- It is slow to build on purpose (parts list, geometry, audit of every joint). Budget one long session; use it only when the figure earns its place over a flat diagram.
- Capture scripts need Chrome. Build with `node <example>/build.mjs` (`--light` for a light card).
- Trigger words from the user: isometric, exploded view, cutaway, "how it works" as a figure. Otherwise keep the existing flat style.

## Step 9: Deliver

Save the file with a name carrying the date and the reader. Reply in two or three lines: what the page asks of the reader, the measured heights at 1440 and 390 with the fold result, and any claim you could not source or any gap in the research the page makes visible. For PDF or PNG export, load the page with `?static=1` at 1440x900, device scale 2, take a full-page screenshot, and print the PDF at width 1440px and height equal to `scrollHeight` with backgrounds and zero margins; then confirm the PDF text has zero dashes.
