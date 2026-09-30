---
name: "campaign-visualization"
description: "Turns a dull campaign report (vendor rollouts, lead sheets, meeting recaps) into a full-width visual review page for sales and marketing readers, like the Virtusa and Epicor campaign reviews. Trigger on campaign report, campaign review, campaign learnings, beautify this report, visualize the campaign, client review page."
---

# Campaign Visualization

A campaign report arrives as tables in emails, a lead workbook, and a meeting recap. This skill turns that into one page a sales or marketing leader can read in three minutes and act on: what ran, what came out, what the calls and emails taught us, what we own, what changes. The reader may be the client (Li zhen at Epicor, Aseem at Virtusa) or the internal team. Savvy readers will check the arithmetic, so every chart must sum and every figure must trace to a source.

Reference pages, both from 29 Sep 2026, are the standard. Copy their structure and token system rather than inventing a new look:

- `Atlas/Clients/Epicor/Epicor Campaign Review 29 Sep.html` (standalone HTML, latest version of the system)
- The Virtusa Campaign Learnings page (same system, one generation earlier)

The sibling skill `executive-one-pager` is for one decision on one screen. This skill is for a campaign's full evidence, laid out wide, with more charts and a leads table. If the reader needs a verdict and one ask, use that skill instead.

## Hard rules

1. **Full width.** Sticky left rail (230px) plus a 12-column canvas up to 1680px. Each section splits into a 4-column claim and an 8-column evidence panel. Never a narrow centred column with dead space either side. The rail carries the brand line, section index, running figures, the next review with its decisions, and a reading key, so nothing below it sits empty on a tall screen.
2. **Zero em dashes and en dashes.** Anywhere, including date ranges ("21 to 25 Sep"). Check the rendered file for the characters before delivering.
3. **Client-facing conduct.** Never name a delivery vendor or a second source; the client sees one campaign run by "we". Never quote a conversion rate, show rate, or closing average. Never estimate; state zero as zero. Never call a tentative slot "confirmed" or "booked meeting". If a figure cannot be reconciled, leave it out and say so in the footer.
4. **Every chart sums.** Bars in a breakdown add up to the population they describe (15 slots means 15). Stacked email bars add up to the sent total. Run the arithmetic in a script before the screenshot.
5. **Bars to scale, labels in text.** Each bar is scaled against the largest group in its own chart and says so in the caption. Every bar carries its number as text. Hover tooltips list the accounts behind a bar. No axis hunting, no dual axes, no pie charts.
6. **Assertion headings.** Every h2 states the finding ("Malaysia gave nine of the fifteen from the smallest list"), never the topic ("Market breakdown").
7. **Own the misses in one band.** A dark full-width band lists what we got wrong in how we ran it, each item ending with what changes. No apologies, no process narration.
8. **No AI slop.** Run the `no-ai-slop` gate on all copy before delivery.

## Phase 1: Pull the sources (do this before any design work)

Gather everything, then reconcile. Typical sources for a LakeB2B or SPAN campaign:

| Source | Where | What it gives |
|---|---|---|
| Emailer rollout reports | Outlook, sender is the delivery vendor's digital lead | Sent, opened, clicked, unsubscribed by country, per send |
| Lead reports | Outlook, one email per lead, workbook plus recording attached | Contact, ERP or platform today, challenge, project status, decision authority, timeline, tentative slot |
| Lead walkthrough or tracker | `Atlas/Clients/{client}/` | Full list of slots with bands and status |
| Weekly review recap | `Calendar/Meetings/{date} - {client} ... Review.md` | Decisions, open items, script changes, scoring rules |
| Daily dispatch and handoff notes | `Atlas/Ops/Dispatch/Daily/{date}/client/`, `Atlas/Clients/{client}/Daily/` | Latest leads, nurture decisions, standing rules |
| Client file and update log | `Atlas/Clients/{client}.md`, `{client}_Update_Log.md` | Commercial terms, target, timeline, what not to say |

Confirm with the sender which report is the latest (Sean confirmed Emailer 5 as latest on 29 Sep before the Epicor page used it). Sort search results by date yourself; the mail search is relevance ranked.

Reconcile before building:

- Per-send email figures must sum: clicked plus opened-without-click plus not-opened equals sent. Compute opened-without-click as opened minus clicked. If a vendor's "no engagement" column does not reconcile, use the arithmetic, not the column.
- Flag metrics that are not comparable (a cumulative first-send open figure against single-week sends) in the caption rather than silently charting them side by side.
- Slot statuses come from the last recorded review. If outcomes after that date are not in the vault or the mailbox, say "as of {date}" and make confirming them the first item in the plan. Do not infer outcomes.
- Count every population twice: total slots, by market, by band, by status. They must agree.

## Phase 2: Decide the reader and the mode

- **Client review** (default when the page is "for {client}"): conduct rules above apply in full, the footer reads "Prepared by {name}, {entity}. Confidential to {client}."
- **Internal review**: may show source split, billing, and vendor names. Mark the file internal in its name and never publish it to a client-shared artifact.

One clarifying round at most (AskUserQuestion) if the reader or the entity is unknown. Otherwise default to the client the folder belongs to and the entity that runs the campaign.

## Phase 3: Sections, in this order

Use the ones the data supports. Each row names the visual that carries it; a section without its visual is cut.

| # | Section | Visual |
|---|---|---|
| Hero | Eyebrow (segment, markets, date range), assertion h1, three-sentence lede, one-line meta, four stat tiles (the last tinted as the number that matters) | Stat tiles with the split in the caption ("Singapore 2, Malaysia 9, Indonesia 4") |
| 01 What ran, in order | Timeline track, 8 to 10 steps, key steps filled in the accent, pauses and deadlines as dashed dots | Horizontal track, stacks vertical on phone |
| 02 The leads or slots | Status breakdown bars (to scale) beside the claim; full-width table grouped into bands (A strongest fit, B re-qualify, C nurture) with pills for the qualifying answers | Table with band rows, pills: go, warn, neutral for "not asked" |
| 03 By market or by account | Three market tiles (slots as the big number, contacts emailed and list size beneath, one email rate) or the per-account strip from the Virtusa page | Tiles with a scaled meter, or account strip |
| 04 The client's qualifying questions | One small bar chart per question (project status, decision authority, current platform, timeline), then four learning cards each ending in a Change line | Three cards in a row, four learning cards below |
| 05 Email | Stacked bars per send (clicked, opened no click, not opened), legend, per-country table for the latest send, two learning cards | Stacked bars, sequential single hue |
| 06 What we own | Dark band, four items, each a bold miss plus what changes | Band |
| 07 What changes | Learned-to-changes table, plus an outlined box with the proposal for the client's decision (numbered, five lines at most) | Table plus proposal box |
| Footer | Sources with dates, definitions ("slot booked", "not asked"), "No figure on this page is an estimate", prepared-by line | Three columns |

The rail, top to bottom: brand line and date; numbered section nav; running figures (four); next review box (date, three decisions to leave with); reading key (what each pill and bar colour means, hover hint, the definition of the lead unit).

## Phase 4: Build

One HTML file, inline CSS and JS, Google Fonts as the only external dependency. Start from the Epicor file's `<style>` block and token system and change only the copy, the data arrays, and the brand tokens:

- Tokens: bg, panel, panel-2, ink, ink-2, ink-3, rule, accent, accent-soft, s-hi, s-mid, s-lo (the sequential stack), track, warn, warn-soft, band, band-ink, band-2. Light values on `:root`, dark values under `prefers-color-scheme: dark` guarded by `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`.
- Accent comes from the entity's brand skill (LakeB2B purple on both reference pages). Status colours (warn) are separate from the accent.
- Fonts: a display face for h1, h2 and big numbers; a body face for everything else. Tabular numerals on every figure.
- Data lives in small JS arrays at the bottom (sends, leads, accounts) and the page renders the stacks, the table, and the tooltips from them. Editing the report next week means editing the arrays.
- Breakpoints: 1180px collapses the rail to a top row and every section to one column; 760px stacks the timeline, tiles and email rows.

When publishing as an artifact, write the content without doctype, html, head or body tags and let the Artifact tool wrap it. For the vault copy, wrap the same content in a minimal skeleton (charset, viewport with viewport-fit=cover, the small reset) so it opens standalone.

## Phase 5: Verify (the output is visual; reading the source proves nothing)

1. Arithmetic: a script prints every chart's sum against its population and every email stack against its sent total. All must match.
2. Dashes: count of U+2014 and U+2013 in the file is zero.
3. Conduct: grep the file for vendor names, "second source", "vendor", "conversion". Zero hits on a client page.
4. Screenshot at 1600px wide, full page, in light and dark. Open it with the Read tool and check: no horizontal scroll, the rail column is filled on a tall screen, every bar has its number, no clipped text, tables that overflow scroll inside their own container.
5. Run `no-ai-slop` on the copy (headings, ledes, learning cards, own band, proposal box).
6. Two-line test: the h1 and the lede alone must tell the reader the count against target, whether it has been scored or accepted, and the one thing the campaign taught us.

## Phase 6: Deliver

Publish with the Artifact tool (private until shared; say so) and save a standalone copy to `Atlas/Clients/{client}/{Client} Campaign Review {d Mon}.html` beside the campaign's other files. The delivery message is two lines: what the page says, and what still needs confirming before it goes to the client. Then list, briefly, what was handled carefully (non-comparable metrics, unrecorded outcomes, proposals not yet cleared commercially) and any pushback on the plan.