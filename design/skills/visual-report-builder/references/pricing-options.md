# Priced options pages (proposals, pilots, packages)

For: a proposal or quote where the reader picks between two or more priced tiers,
usually after a discovery call. Two formats cover nearly every case. When Deep does not
name one, offer both in a single question with A first: he is choosing what to put in
front of the client, and he picks by seeing them.

## A. Editorial options page (recommend first)

For: one reader who should be steered to a tier, or a sales lead walking a call.
Order: hero with a three-or-four-cell stat strip (options, pilot length, categories scored,
reporting cadence), proof block (the case study that opened the door, navy band with gold
big numbers and a chip row of capability streams), three tier cards, add-on card grid,
guarantee band, methodology, flow timeline, closing joint-session ask.
Tier cards: price in display serif, a `Recommended` pill on the middle card plus an accent
border, a three-number strip inside each (accounts, days, per account), then a `<dl>` of
what that tier carries. The card line is the tier's whole argument in one sentence.
Ordering matters: the middle tier must be the obvious read, so give it the pill, the accent
column, and the longest feature list.

## B. Build-your-own matrix

For: a client assembling their own scope, or a call where options are live on screen.
Order: one matrix section first, then guarantees, proof, methodology, timeline. Sticky
sidebar beside the matrix carries the reasoning the table cannot: why the middle tier,
add-ons, how we price.
Matrix rows: grouped under mono group headers (intelligence in every tier, managed
execution, dedicated team, add-ons) so 15 to 20 rows scan as four blocks. Cell values are
glyphs (`Included` solid, `Add-on` ring, `Not in tier` faint) with short text where a
glyph cannot say "Set in week one." Column headers carry price in display serif plus the
per-account line. Highlight the recommended column with a tint that runs the full height.
Legend above the table: three glyphs, no caption needed.

Both formats are built from one content block per tier and one cell matrix, so the two
files cannot disagree. Generate them from a single script, never by editing two HTML files.

## Client-facing gates (apply before any file leaves for the prospect)

- **Strip the internals, then prove it.** Remove frontmatter, draft notes and every internal
  name, person, cost floor or ceiling, competitor-inventory aside, and per-record price.
  Then assert on the rendered text, not the source: strip tags and grep the result for the
  internal token list. "No internal words appear in my source" passes while an uncleared
  comment or an embedded string still leaks.
- **Stamp it.** Every prospect page carries `Draft for internal review` until Deep clears
  it, and the footer names who it is prepared for.
- **Name the client's own stack back to them when it proves a point.** Comparing against
  tools the client already pays for is fair and lands; quoting what we charge per record
  is not. The line is the reader's own cost, never ours.
- **Unclear commercial numbers go to a question, not a guess.** When the call left a figure
  open (credit volumes, budget slices, display price), deduce the candidates from the
  transcript, then ask in one batch with the recommended option first. Build only after
  the answers, and mark whatever stays open on the page as agreed in week one rather than
  inventing a number.

## Verify

Overflow and screenshot at 1440 and 390, zero console errors, interactions driven in
Playwright. Use `behavior:'instant'` when scrolling to a section before a screenshot:
`scroll-behavior: smooth` still animates at capture time and the shot lands mid-page.
Re-run the internal-token grep on each generated file; two files from one script means
two checks.
