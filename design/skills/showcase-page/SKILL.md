---
name: "showcase-page"
description: "Builds premium scroll pages that prove a result (case studies, campaign wins, event recaps, data snapshots) with animated data visuals, MicroKit micro-interactions, 21st.dev components, Artifact plus PDF and PNG export."
---

# Showcase Page

A showcase page proves one result to a buyer who skims. It earns a second look the way Paddle and passionfroot pages do: one atmospheric moment at the top, editorial numbers, real charts that animate to their values, and small responses under the pointer that make the page feel built with care. The LakeB2B case study v2 set (Oct 2026) is the reference build: `Atlas/Context Docs/Lake B2B/Case Studies/v2/` in the Celsus vault.

The working kit lives in the vault at `Other/Skills/showcase-page/kit/` (`core.css`, `core.js`, `build.py`, `shoot.py`, worked examples). Copy it into the session and build from it. When the vault is not mounted, rebuild the same structure from `references/components.md`.

## What went wrong before (do not repeat)

The v1 LakeB2B case studies were called "really mediocre, so basic" by Deep: static, flat, one chart each, no motion, generic cards, a funnel that put accounts and contacts on one scale. A page that only restates numbers in boxes fails, however clean it is.

## Hard rules

1. **Never invent a number.** Every figure comes from the evidence (vault client folders, the Case Study Library doc, a confirmed source). Arithmetic on stated figures is allowed (rates, shares, multiples) and is labeled as computed. Anything marked Verify first, Internal only or Skip stays out.
2. **Anonymize clients** by industry, size and region. Never name an outside delivery vendor; vendors are "we" or "our team". A client works with LakeB2B or SPAN, never both. Do not name the client's target accounts either.
3. **Zero em dashes and en dashes** anywhere, including titles, chart labels, date ranges and the PDF text. Check: `grep -cP '\xe2\x80[\x93\x94]' file.html` prints 0, and `pdftotext file.pdf - | grep -c` on the same two characters prints 0.
4. **Full width.** Content runs to `--maxw:1600px` with a fluid gutter. No narrow centered column with dead space either side.
5. **Client-reported lines are labeled as client reported**, and a paraphrase says it is a paraphrase.
6. **Respect timing holds.** A case with a pending client decision carries a red HOLD pill in the nav and a HOLD suffix in its file names until the date passes.
7. **Look at the output.** Screenshots at 390 and 1440 are opened with the Read tool and critiqued before anything is called done.

## Step 1: Evidence and brand

- Gather the numbers and their sources into a short evidence table (figure, source file, allowed or not). Read the raw client files for per-row data the chart needs (per account, per market, per send).
- Brand: infer from the client or ask once ("which brand?"). Load that brand skill (`lakeb2b-brand-guidelines`, `span-brand-guidelines`, `ampliz-brand-guidelines`, `metricfox-brand-guidelines`, `champions-group-brand`) and lock its colours, fonts and logo. No brand named means the neutral theme in `references/templates.md`.

## Step 2: Pick the template

Propose one template from `references/templates.md` in a single AskUserQuestion, recommended first: Case Study, Campaign Report, Partner Pitch, Event Recap, Market or Data Snapshot (Executive One-Pager routes to its own skill). Skip the question when the request names the format.

## Step 3: Source the components (21st.dev, then MicroKit)

1. List the 3 to 5 components the page depends on (see the catalog in `references/components.md`).
2. If the 21st.dev MCP is connected (tools `search`, `get_inspiration`, `get_component`, `search_logo`), run `search` for each with the catalog query. Pull code with `get_component` for at most the two that matter most (free tier: 2 code pulls a day; `get_usage` shows the quota). Port the React and Tailwind code into the kit's vanilla files and credit the id in a CSS comment.
3. Pick the micro-interactions from `references/micro-interactions.md` (MicroKit patterns, already ported in the kit): label swap and arrow slide-through on buttons, glow follow on the primary CTA, edge shine on the ghost button, spotlight rail on step lists, tilt and sheen on stat cards, animated row reorder on sortable tables.
4. If the MCP is not connected, say so in one line and continue with the kit. Never write an API key into a file, page, or the vault.

## Step 4: Write the copy, then gate it

- Headline states the result with its number ("8 of 10 leads delivered into US manufacturers."). Lead is one or two plain sentences: who, what they needed, what we did.
- Section headings are assertions. Step titles are verbs. Captions say what a mark means.
- The closing line is the most concrete fact on the page, not an aphorism; its final clause is greyed.
- Run `no-ai-slop` in Gate mode on every line (and `slop_lint.py` from the vault when mounted). No binary contrasts, colon reveals, fragments, kickers, puffery or banned words.

## Step 5: Build with the kit

Section order for a Case Study: sticky nav with logo pill, case label, industry chip and primary button; scroll progress bar; atmospheric hero with staggered headline; three floating stat cards with count-up and comparator chips; client strip; split sticky challenge and approach; the main visual section (two or more panels on their own scales, a table where rows exist); Paddle stat band; closing line; CTA panel; footer.

- Charts follow `references/charts-tables.md`: unit charts for counts, two scales when units differ, values on the marks, computed rate columns, sortable tables.
- Motion follows `references/motion.md`: one load sequence, reveals on scroll, `prefers-reduced-motion`, `?static=1` export mode, final values in the HTML.
- Mobile at 390: one column, cards stack straight, 44px tap targets, no horizontal overflow, tables drop the inline bar column.
- `python3 build.py <ids>` writes the standalone HTML and the Artifact fragment and fails on any dash.

## Step 6: Verify

1. `python3 shoot.py <slug> --export` for each page: overflow 0 at 1440 and 390, no small tap targets, zero console errors.
2. Open the 1440 hero, the 1440 full page in two halves, and the 390 full page with the Read tool. Check: hero headline wraps in three lines or fewer, cards overlap the hero edge cleanly, no label collides on any chart, no orphaned single tile or dot row, table columns fit their panel.
3. Check one motion frame mid-scroll (bars and dots mid-animation, spy rail on the active step) and one hover state per micro-interaction.
4. Claim audit: every number on the page traces to the evidence table; computed numbers are right.
5. The Paddle bar. Would Paddle ship this? If a section is a box of text with a number in it, add the visual that proves it or cut the section.

## Step 7: Deliver

1. Publish each page with the Artifact tool (title is the page's 2 to 4 word name; one-sentence description; republish the same file path to keep the URL).
2. Save to the vault beside the client or entity material (for LakeB2B: `Atlas/Context Docs/Lake B2B/Case Studies/v2/`): standalone HTML, one-page PDF, 2x PNG, plus an index note listing live links and status (ready, hold, do-not-send conditions).
3. The message to Deep is two lines: what shipped, and the one decision he needs to make.

## References

`references/components.md`, `references/charts-tables.md`, `references/motion.md`, `references/micro-interactions.md`, `references/templates.md`, and the kit README at `kit/README.md`. When they are not in the account copy, read them from the vault at `Other/Skills/showcase-page/`.