# Charts and tables

Read the `dataviz` skill before writing the first chart; this file adds the house rules learned on the LakeB2B case study pages.

## Pick the chart from the data shape

| Data shape | Chart | Kit piece |
|---|---|---|
| One count the reader should feel (hundreds of items) | unit chart, 1 dot = 1 item | `[data-waffle]` |
| Small vs large on the same unit (394 vs 14,662) | two unit blocks on one dot scale, 1 dot = N | `.ucompare` + `.waffle.fixed` |
| A part of a whole, 2 to 4 parts | stacked bar with a key of shares | `.stack` + `.stack-key` |
| Stages with different units | two panels, each with its own scale and a `.scale-note` chip | `.grid-2 > .panel` |
| Ranking of 3 to 8 items | horizontal bars, value on the mark, sorted descending | `.bars > .bar` |
| Many items with one value each (38 accounts) | heat tiles sorted by value, risk flagged by outline | `.tiles` |
| Under 20 discrete things (leads, slots) | big unit dots, pending ones dashed | `.udots` |
| Rows the reader compares on several columns | table with hairlines, inline bars, a computed rate column | `table.data` |
| Geography | dot map with bubbles sized by area | `sea_map()` |
| A real sequence | timeline or stepper | `.timeline` |
| A trend over time (8+ points) | line chart, hand-built SVG or Chart.js | not in kit; follow `dataviz` |

Never mix units on one scale. Accounts and contacts, dials and conversations, sends and clicks each get their own panel or their own axis, and the panel says which scale it uses.

## Marks and labels

- Values sit on or beside the mark. The reader never hunts an axis.
- Bars are `display:block` with width from the stated number (`--w:65.04%`). Compute widths in code, never by eye.
- Bubble and dot sizes scale by area (`r = rmax * sqrt(v / vmax)`), never by radius.
- Colour encodes one thing per chart. Brand gradient for "ours" or "kept", neutral for "missing" or "to go", red outline for a risk.
- Every chart has a one-line caption that says what a mark means ("1 dot = 1 account", "Bubble area = contacts").
- A partial unit at the end of a unit chart is drawn at reduced opacity (`data-frac`).

## Tables

- Hairlines only: 1px header rule, faint row rules, no zebra, no boxed cells.
- Numbers right-aligned with `font-variant-numeric: tabular-nums`; the key number column can use the display serif.
- Computed columns are welcome and must be arithmetic on stated figures: rate = clicks / sent, share = part / total. Show one decimal for rates under 10%, and say how the column is computed in a `.fine` note under the table.
- A total row in `tfoot`, bold, with the same computation.
- Sortable headers are real `<button>`s inside `<th>` with `aria-sort`; every cell carries `data-v` with the raw sort value. Rows animate to their new place (FLIP) unless reduced motion or static mode is on.
- Tables wider than the panel scroll inside `.tbl-wrap`; the page body never scrolls sideways. Below 560px drop the inline bar column, keep the numbers.
- Header labels stay short (one word if possible) so five columns fit a half-width panel at 1440px.

## Numbers

- Every figure comes from the evidence. Rates and shares computed from stated figures are allowed; extrapolation is not.
- Round shares so they sum to 100 (67, 25, 8) and keep rates to one decimal.
- Count-up animations end on the exact stated value, formatted with thousands separators, and the HTML holds the final value so static export and no-JS readers see it.
