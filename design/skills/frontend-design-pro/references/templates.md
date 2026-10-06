# Page templates

Propose one at the start, in a single AskUserQuestion with the recommended template first, unless the request already names the format. Each template is a section order plus the components it uses (see `components.md`). Brand comes from the brand skill; with no brand named, use the neutral theme at the bottom.

## 1. Case Study (the LakeB2B v2 set)

For: one client result a prospect should see themselves in.
Order: sticky nav, progress bar, atmospheric hero (result as the headline), three floating stat cards, client strip, split sticky challenge and approach, main visual section (two panels plus a table or map), Paddle stat band, closing line, CTA, footer.
Components: floating stat cards, unit chart or before and after units, stacked bar or funnel on two scales, sortable table, timeline when there is a process, callout for any client-reported line.
Budget: 4,500 to 6,500px at 1440.
Reference build: `Atlas/Context Docs/Lake B2B/Case Studies/v2/` in the Celsus vault.

## 2. Executive One-Pager

For: a decision-maker who gives the page ninety seconds.
Order: verdict (headline, three numbers with comparators, the ask), at most five evidence sections, next steps.
Components: Docket or Deal Room treatment, status board, aging bar, tick strip, stepper; `details` for depth.
Budget: 3,000px at 1440, 6,500px at 390. Transform-only reveals.
Owner skill: `executive-one-pager`.

## 3. Campaign Report

For: a client or internal review of a campaign's numbers.
Order: editorial hero with stat strip, per-channel panels (email table with computed rates, calling bars, meetings dots), what changed week over week, risks, next steps.
Components: sortable table with inline bars, stacked bar, big unit dots, timeline of sends.
Budget: 4,000 to 6,000px at 1440.
Owner skill: `visual-report-builder` (dark editorial default) or `campaign-visualization`.

## 4. Partner Pitch

For: a partner or prospect deciding whether to work with us.
Order: split hero with a product card, logo marquee, three proof cards, how it works (timeline), story cards, comparison table, CTA.
Components: split hero, story cards, comparison table, CTA with glow.
Budget: 5,000 to 7,000px at 1440.
Owner skill: `frontend-design-pro` landing-page mode.

## 5. Event Recap

For: attendees, sponsors and the team after an event.
Order: atmospheric hero with the event name and one result, stat band (attendees, sessions, meetings), photo or quote strip, sessions timeline, sponsor marquee, what's next CTA.
Components: Paddle stat band, timeline, quote callouts (verbatim only), logo marquee.
Budget: 4,000 to 6,000px at 1440.
Owner skill: `showcase-page`.

## 6. Market or Data Snapshot

For: a dataset or market cut the reader can explore (contacts by country, accounts by industry).
Order: editorial hero, map, ranked bars, heat tiles, sortable table, method note, CTA.
Components: dot map, heat tiles, sortable table, `.fine` method notes.
Owner skill: `showcase-page` or `visual-report-builder`.

## Neutral theme (no brand named)

```css
:root{--paper:#FBFAF7;--sand:#EFECE6;--ink:#17161A;--ink-2:#45434B;--mute:#85828C;
--purple:#3B4BD8;--red:#D9480F;--gold:#E8B400;--magenta:#8B5CF6;--teal:#0F8B8D;--lavender:#8E94F2;
--brand-grad:linear-gradient(100deg,#3B4BD8,#8B5CF6 50%,#D9480F)}
```
Fonts: Fraunces display, Inter Tight body, IBM Plex Mono labels. Hero gradient stops shift to ink blue and amber.

## Brand locks

| Brand | Skill | Primary | Fonts | Logo rule |
|---|---|---|---|---|
| LakeB2B | `lakeb2b-brand-guidelines` | Purple #6D08BE 60%, Red #E8033A 20%, Gold #FFB703 20% | Montserrat body, serif display allowed for headlines | full colour on light grounds, reversed on dark, all-white on purple; 180px minimum |
| SPAN | `span-brand-guidelines` | per skill | per skill | per skill |
| Ampliz | `ampliz-brand-guidelines` | per skill | per skill | per skill |
| MetricFox | `metricfox-brand-guidelines` | per skill | per skill | per skill |
| Champions Group | `champions-group-brand` | fill #F26722, ink text on orange | per skill | per skill |

A client works with LakeB2B or SPAN, never both; strip the other brand from client pages.
