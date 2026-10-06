---
name: executive-one-pager
description: "Distills meetings, transcripts, documents, decks, or a week of workstreams into ONE decision page: verdict and asks on screen one, evidence as visuals, hard length budget, mobile-first, light and dark, brand colours locked, published as an Artifact. Trigger on one-pager, exec one-pager, executive summary page, condense this into a page, follow-up one-pager, leave-behind, turn this into HTML, talking points, slide-by-slide, prep someone for this deck, weekly readout, walk Chief through my work, status page for the chairman, make the one-pager premium, it looks basic."
---

# Executive One-Pager

A decision-maker opens this on a phone, between meetings, and gives it ninety seconds. In that time they learn three things: what the answer is, what the numbers say, and what you want them to do. Everything else is evidence they can open if they choose.

One test judges the page: **cover everything below the first screen. Can the reader still act?** If not, the page failed, however good the rest looks.

## What went wrong before (do not repeat)

- **Too long.** Early outputs ran 6,000 to 9,500px on desktop and up to 17,000px on a phone: ten to twenty screens of editorial prose under a one-pager's name.
- **Generic look.** The September 2026 readout for Chief shipped as an orange-gradient hero, a four-up stat grid, and eight white rounded cards with a pill in the corner. That is the default every generator produces. It happened because the skill said "pick a style from another skill", and under time pressure the builder picked nothing and fell back to the template.
- **Numbers with no comparator.** "9 active workstreams" and "5 open P0s" told the reader nothing.
- **The headline over-counted.** It said three items needed a call; the third item said it needed nothing back.
- **Topic labels for headings** ("LakeB2B client campaigns"), text cards with one progress bar between eight of them, and no ask with an owner.

The rules and the house kit below exist to stop each of those.

## Three modes

- **Summary** (default): one distilled decision page from a meeting, document, or thread.
- **Presenter**: the source is a deck and the reader must deliver or sit through it. One-screen verdict, then a slide-by-slide walkthrough. Trigger on "talking points", "script for each slide", "slide-by-slide", "prep [someone] for this deck".
- **Readout**: a status walkthrough across several workstreams for a boss, chairman, or board ("walk Chief through my week", "weekly readout", "status page"). The verdict is what needs the reader; the body is a status board, the next seven days, and what was settled.

## Hard rules (non-negotiable)

1. **Verdict on screen one.** At 390 by 844 the first viewport holds the headline (the answer, not the topic), three numbers with comparators, and the first ask. Summary and Presenter carry one ask; Readout carries at most three.
2. **Length budget.** Summary and Readout: at most five sections after the verdict, at most 3,000px tall at 1440px, at most 6,500px at 390px. Presenter: the runway before the slide cards is one desktop screen; each slide card is at most 260px tall collapsed.
3. **Assertion headlines.** Every section heading is a full-sentence conclusion the reader could repeat in a meeting ("Three of nine are blocked, and each one has a known unblock."), never a topic label. Headlines end with a period.
4. **Visual first, text second.** Every section leads with a visual derived from the content (status mix bar, aging bar, tick strip, rail, split, tree, before/after bars) and carries at most three lines of text. Removal test: if deleting the visual loses no meaning, it is decoration.
5. **Numbers carry comparators.** Every figure sits beside a target, a deadline, a prior period, or a share of the whole ("2 of 30, 19 days left"). Simple arithmetic on stated figures is allowed (28 to go, about 1.5 a day); extrapolation is not.
6. **Claim audit.** Every count in the headline or lead equals what the page renders: asks, blocked items, workstreams. An FYI item never sits in an asks list; it gets its own "FYI, no reply needed" line.
7. **The accent means the reader.** The brand colour marks only what the reader must act on: the ask panel, the headline phrase that names their decision, the "on you" status. Progress bars, charts and decoration use ink and neutrals.
8. **Status is shape plus colour.** Blocked is a square, on the reader is a diamond, moving is a half-filled ring, on track is a dot, done is a check. Colour confirms; shape carries.
9. **Progressive disclosure.** Detail (quotes, per-account paragraphs, objection answers) sits behind native `<details>` toggles that default closed. The page is fully readable at rest: no content parked at `opacity:0` waiting on a scroll observer.
10. **Mobile-first, both themes.** Base CSS targets 390px (single column, 16 to 17px body, 44px tap targets, no horizontal overflow); `min-width:860px` adds columns. Light palette on bare `:root`, dark tokens under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`, repeated under `:root[data-theme="dark"]`. `body` paints its own background.
11. **No em dashes, no en dashes**, anywhere, including headings, labels and date ranges. Use commas, periods, colons, "to", or a slash in mono labels.
12. **Never name a delivery vendor to a client.** Vendors are "we" or "our team" in client-facing pages. A client works with Lake B2B or SPAN, never both; strip the other. Internal readouts for Chief may name vendors.
13. **No invented specifics.** No dates, durations, effort estimates or causes that the source does not state. "Restore this week" never becomes "by Fri 18 Sep"; "small task" never becomes "a few minutes".
14. **Full width, never a narrow column.** The page container runs to 1440px with a fluid gutter (`clamp(16px,4vw,64px)`). Deep dislikes pages that sit in a narrow centered column with dead space either side.
15. **Considered, not static.** Every interactive element has a hover and focus response from the shared micro-interaction set, and the evidence visuals animate to their values once (transform only, see rule 9). A flat page with boxes of numbers fails the "would Paddle ship this?" bar in Phase 6.

## Phase 1: Ingest and distill into a verdict brief

Sources: meeting summaries or transcripts (Zoom, Otter, Wispr, pasted notes), documents (md, docx, pdf), decks (pptx via the pptx skill; for a pdf export, page order is slide order), email threads. If the source is a meeting the user attended, check the connected meeting tools and vault triage notes before asking for notes. For Readout mode, pull from the vault when mounted: `TASKS.md`, `dashboard.html`, the relevant `/areas/` and Efforts notes, this week's daily notes and meeting notes. Judge freshness by the date a file asserts, never its mtime.

For long sources, delegate extraction to a subagent so raw text stays out of context. It returns a **verdict brief**, not a summary:

| Field | What it holds |
|---|---|
| Reader | Who opens it and who decides. Write for the decider. Presenter mode: the presenter. |
| Answer | One sentence. Becomes the headline. |
| Three numbers | The figures that most change the reader's mind, each with comparator and source line. |
| Asks | Summary and Presenter: one action, owner, date. Readout: up to three, each with owner, date (or "no date set"), and what it is paired with. |
| FYIs | Things moving that the reader should know about but not answer. |
| Evidence | Three to five points, each tagged with the visual that proves it. |
| Workstreams (Readout) | Per workstream: name, entity, status (blocked, on you, moving, on track, done), one-line state, key date, the unblock. |
| Settled (Readout) | Decisions closed this period, each with the before/after or structure it created. |
| What they said | Two to four verbatim quotes for the detail layer. |
| Options | For an open decision: two or three options with cost and risk, the recommended one marked. |
| Commitments | Next steps from each side with owners and dates. |
| Concerns | Objections raised; these become a risk visual, never an omission. |
| Per-slide content (Presenter) | Every slide: headline, copy, numbers and sources, the job the slide does. Skip nothing. |

**Verify before building.** Product, company and people's names get checked against public sites and sources Deep confirmed. Transcript-sourced names are suspect by default. In Presenter mode, cross-check deck numbers against any master or fact-verification doc; flag illustrative figures.

## Phase 2: Clarify (one round at most)

If brand, reader, or the ask is unknown, ask via AskUserQuestion in ONE round. Otherwise default: a meeting follow-up takes the brand that ran the meeting, the attendees as readers, the agreed next step as the ask. In Presenter mode, default the briefed person to the user or the most senior person on the invite who did not author the deck. Readout for Chief defaults to Champions Group brand, Docket treatment, internal.

**Brand step.** Infer the brand from the source or ask "which brand?" in the same round. Load that brand skill (`lakeb2b-brand-guidelines`, `span-brand-guidelines`, `ampliz-brand-guidelines`, `metricfox-brand-guidelines`, `champions-group-brand`) and lock its colours, fonts and logo before choosing a treatment. No brand named means the neutral theme in `references/templates.md`.

**Template step.** When the reader would be better served by a scroll page than a one-pager (a client case study, an event recap, a partner pitch), say so in the same round and offer the matching template from `references/templates.md`; those route to the `showcase-page` or `frontend-design-pro` skills.

## Phase 3: Choose the treatment, then the sections

**Treatment.** Pick one of the house treatments by the document's job. Record the choice and the reason in one HTML comment at the top of the `<style>` block. Brand colours from the brand skill are locked and override treatment colours; if the brand skill names a typeface, headings and body stay in that family (a display cut of the same family is fine).

| Treatment | Job | Ground and structure | Type (Google Fonts) | The one bold move |
|---|---|---|---|---|
| **Docket** | internal readouts, chairman and board updates, internal review prep | near-white ground, 1px hairlines, 3 to 4px radii, a mono docket line over a 2px ink rule, rows instead of cards | Inter Tight 800 display, Inter body, JetBrains Mono labels | the ask panel as a solid brand-colour block with ink text |
| **Deal Room** | client follow-ups, leave-behinds, partnership pitches | white surfaces on a faint brand-tinted ground; one full-bleed verdict band in the brand's deepest colour | Schibsted Grotesk display, Source Sans 3 body, IBM Plex Mono labels (or the brand family) | the three numbers set huge inside the verdict band |
| **Cue Card** | Presenter mode | paper ground; slide cards in deck order grouped by act, sticky slide-jump index | Newsreader for spoken scripts (italic), Inter body, JetBrains Mono slide numbers | script blocks as tinted cue cards the presenter can read aloud |

Spend boldness in one place and keep the rest quiet. If the source deck has a locked brand system in the workspace, match it so the brief looks like the deck it serves. Do not reuse the previous one-pager's treatment and layout for the next one unless the two are a matched series. If none fits, run `frontend-design` style selection for real and write why.

**Looks to avoid unless Deep asks for them by name:** a brand-gradient hero with a four-up stat grid; the same white rounded card with a corner pill repeated down the page; cream paper with a serif display and a terracotta or teal accent (the old Warm Editorial default); purple-to-blue gradients; emoji markers; 01/02/03 numbering on things that are not a sequence; coloured side-stripe borders on cards.

**Source the components before building (21st.dev, then MicroKit).** List the 3 to 5 components the page depends on (verdict block, status board, the main evidence visual, the ask panel, a table). If the 21st.dev MCP is connected (`search`, `get_inspiration`, `get_component`), search each with the query in `references/components.md`, read the previews, and pull code for at most the two that matter (free tier: 2 code pulls a day). Port to the house kit's vanilla CSS and credit the id in a comment. Take hover and focus details from `references/micro-interactions.md` (MicroKit patterns). If the MCP is not connected, say so in one line and build from the house kit. Never write an API key into a file or page.

**Brand accents.** Champions Group: fill `#F26722`; accent text `#B8420A` on light and `#FF9A62` on dark; ink `#1A1A1A` text on the orange fill (white on `#F26722` is about 3:1 and fails). Lake B2B: `#6D08BE`. Ampliz, SPAN, Ranch: per their brand skills. Semantic colours (red blocked, green on track) are separate from the accent.

**Sections.** At most five after the verdict. Each row names the visual that carries it; a section without its visual does not ship.

| Section | Use when | The visual that carries it |
|---|---|---|
| Verdict (always, first) | every page | Headline, three number cells with comparators, the ask panel with owner and date |
| Status board (Readout) | several workstreams | Segmented mix bar (one cell per workstream, coloured by status) plus a legend with counts; grouped rows: shape glyph, name, entity tag, one-line state, key date right, `<details>` for the paragraph |
| Decision aging | a decision is overdue | Horizontal bar from opened to today, deadline tick, overrun hatched; labels at open, deadline, today |
| Pace | a target with a deadline | Tick strip of N cells with delivered cells in ink, plus "X to go in Y days" |
| Next 7 days (Readout) | dated items ahead | Rail with filled dots for fixed times and open dots for soft ones; horizontal on desktop, vertical on phone |
| Settled (Readout) | decisions closed | One card per decision with a micro-visual of its result: split (who owns what), tree (brand order), chips (focus areas) |
| Where we are | a process or deal in flight | Stepper with a today marker; done filled, blocked flagged |
| What changed | a before and after | Paired bars or delta cells from stated numbers |
| The decision | a choice is open | Two or three option cards side by side with cost, time, risk chips; the recommended one marked |
| Risks and objections | concerns raised | Ranked rows with severity glyph and a one-line answer each; a 2x2 when there are four or more |
| What they said | the source is a meeting | Two to four quote cards, each with a micro-visual of the reality it describes |
| Proof | results exist to cite | Before/after bars, delta pill, dot grid for a rate; stated numbers only |
| Next steps (Summary, last) | every summary page | Two columns, "On us" and "Over to you", rows with status glyph, owner, date |
| Slide walkthrough (Presenter) | briefing a presenter | One card per slide: mono slide number, headline, the slide's job in one line, two to four talking points, a cue-card script block; grouped into acts; sticky jump index |

Verdict layout (desktop; on a phone the same pieces stack in this order: headline, numbers, asks):

```
+-------------------------------------------+------------------------------+
| DOCKET LINE: brand / occasion / date / to |                              |
| HEADLINE. The answer, one sentence.       | ON YOUR DESK            2    |
| Lead: two or three lines, who and why now.| 01 Ask as a verb phrase.     |
|                                           |    one line of context       |
| NUM 1        | NUM 2        | NUM 3       |    [micro-visual]            |
| comparator   | comparator   | comparator  |    OWNER x   DUE y           |
|                                           | 02 ...                       |
|                                           | FYI, no reply needed: ...    |
+-------------------------------------------+------------------------------+
```

## Phase 4: Copy

Short sentences, plain words, active voice. Headlines are assertions and end with a period. Asks start with a verb ("Give the Ranch go/no-go."). Address the reader by name in the lead for follow-ups and presenter briefs. Key dates in rows are a bold time plus a few mono words ("**Tonight** review needs a call"). Highlight at most two value phrases per section, never connective prose. Quotes go in the detail layer unless one quote is itself the evidence.

Run `no-ai-slop` in Gate mode on every line of copy before building: no binary contrasts, throat-clearing, colon reveals, dramatic fragments, kickers, puffery, or banned words.

**Presenter scripts.** Load `vinh-copywriting` for every script block: complexity level 1, speech rhythm, a line break for a natural pause (never the word "pause"), one concrete image per script where the source supports it, and always a bridge to the next slide. Run the Vinh rewrite checklist on every script; scripts sound like a person talking, not bullets read aloud.

## Phase 5: Build

One self-contained HTML fragment for the Artifact tool (no doctype, html, head or body tags; `<title>` first, then the fonts `<link>`, then `<style>`). Inline CSS and JS; Google Fonts is the only external request. Icons are inline stroke SVG, never emoji or icon fonts.

Build order that keeps the budget honest:

1. Verdict first. Put `data-fold` on the headline, each of the three numbers, and the first ask's heading. Measure it at 390 before adding anything else.
2. Add sections one at a time, visual first. Stop when the budget is reached; move the rest into `<details>` or cut it.
3. Bars and strips are `display:block` elements with widths from stated numbers; values sit on or beside the mark. Ink for "ours" and "done", neutral line colour for "missing" or "to go", the accent only for the reader's items.
4. Interaction stays small and deliberate (see `references/micro-interactions.md` and `references/motion.md`):
   - Buttons and the ask panel's action: label swap on hover and focus, arrow slide-through.
   - Rows and status board: hover tint plus a brand accent bar on the first cell; chevron rotation on `<details>`.
   - Evidence visuals: bars grow, tick strips fill, steppers draw once when they enter view, using transform only so the content is readable at rest (rule 9). Count-ups end on the exact stated value, which is also the value in the HTML.
   - Visible `:focus-visible` outlines, `prefers-reduced-motion` honoured, a `?static=1` mode for PDF and PNG exports.
   - No ambient particles or auroras in Docket or Deal Room; no tilt cards (that belongs to showcase pages).

**House kit (Docket tokens and core components).** Copy, then swap the brand values:

```css
:root{
  --ground:#FBFAF8; --surface:#FFFFFF; --sunk:#F4F1EE;
  --ink:#1A1A1A; --ink-2:#3B3632; --muted:#6B645E;
  --line:rgba(40,28,18,.12); --line-2:rgba(40,28,18,.07);
  --accent:#F26722; --accent-ink:#B8420A; --on-accent:#1A1A1A; --accent-soft:#FFF4EC;
  --red:#B91C1C; --red-soft:#FCEBEA; --green:#15803D; --green-soft:#E6F3EB; --prog:#5A534D;
  --display:'Inter Tight','Inter',-apple-system,'Segoe UI',Arial,sans-serif;
  --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,'SF Mono',Menlo,monospace;
}
/* dark: same token names under the media query and [data-theme="dark"] */
/* --ground:#12100E --surface:#1A1714 --sunk:#221E1A --ink:#F4EFEA --ink-2:#D8D0C8 --muted:#A59C93
   --line:rgba(255,236,218,.13) --accent-ink:#FF9A62 --accent-soft:#2A1B12 --red:#F2877F --green:#6CCB8C --prog:#CFC6BD */
body{margin:0;background:var(--ground);color:var(--ink);font:16px/1.55 var(--sans);padding-inline:16px}
.page{max-width:1440px;margin:0 auto;padding-block:18px 64px;padding-inline:clamp(0px,3vw,48px)}
.mono{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.docket{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 18px;padding-bottom:12px;border-bottom:2px solid var(--ink);color:var(--muted)}
h1{font:800 clamp(30px,6.4vw,50px)/1.04 var(--display);letter-spacing:-.032em;max-width:16ch;text-wrap:balance}
h1 .you{color:var(--accent-ink)}
.nums{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line)}
.nums>div+div{padding-left:12px;border-left:1px solid var(--line)}
.n{font:800 clamp(26px,5.6vw,40px)/1 var(--display);letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.desk{background:var(--accent);color:var(--on-accent);border-radius:4px;padding:18px}
/* aging bar: deadline at (deadline_day / days_open * 100)% */
.age-track{position:relative;height:12px;background:rgba(26,26,26,.16)}
.age-over{position:absolute;inset:0 0 0 var(--dl);background:repeating-linear-gradient(135deg,#1A1A1A 0 3px,rgba(26,26,26,.55) 3px 6px)}
.age-tick{position:absolute;left:var(--dl);top:-4px;bottom:-4px;width:2px;background:#1A1A1A}
/* status glyphs */
.g{display:block;width:11px;height:11px}
.g-b{background:var(--red)}                                   /* blocked: square */
.g-y{background:var(--accent);transform:rotate(45deg) scale(.86)} /* on the reader: diamond */
.g-m{border-radius:50%;background:conic-gradient(var(--prog) 0 50%,transparent 0);box-shadow:inset 0 0 0 1.5px var(--prog)} /* moving */
.g-t{border-radius:50%;background:var(--green)}               /* on track: dot */
details.row{border-bottom:1px solid var(--line)}
details.row>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:14px 1fr 18px;gap:4px 12px;padding:13px 4px;min-height:44px}
details.row>summary:hover{background:var(--sunk)}
.ticks{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:2px;max-width:260px}
.ticks i{display:block;height:12px;background:var(--line)} .ticks i.on{background:var(--ink)}
@media (min-width:860px){
  .verdict{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:40px}
  details.row>summary{grid-template-columns:14px minmax(0,1fr) 230px 18px;align-items:center}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
```

A full worked example (Readout, Docket, both themes) lives at `Other/Skills/executive-one-pager/docket-readout.html` in the Celsus vault and is published as the "Deep's Work, Walked Through" artifact. Start from it when the vault is mounted; match its quality when it is not.

## Phase 6: Verify

Run the gate script (also saved in the vault as `Other/Skills/executive-one-pager/measure.py`). It wraps an Artifact fragment the way the publisher does, then checks three renders:

```python
# measure.py <file.html> [--shots]
import sys, re
from playwright.sync_api import sync_playwright
path=sys.argv[1]; shots='--shots' in sys.argv
html=open(path,encoding='utf-8').read()
if '<html' not in html.lower():
    html='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>'
print('dashes', len(re.findall('[\u2013\u2014]', html)))
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h,t in [(390,844,'light'),(1440,900,'light'),(390,844,'dark')]:
        pg=b.new_page(viewport={'width':w,'height':h},color_scheme=t); pg.set_content(html,wait_until='networkidle')
        r=pg.evaluate("""()=>({H:document.documentElement.scrollHeight,over:document.documentElement.scrollWidth>innerWidth,
          miss:[...document.querySelectorAll('[data-fold]')].filter(e=>e.getBoundingClientRect().bottom>innerHeight).map(e=>e.textContent.trim().slice(0,40))})""")
        print(f"{w} {t}: height {r['H']}, overflow {r['over']}, fold missing {r['miss']}")
        if shots: pg.screenshot(path=f'shot-{w}-{t}.png', full_page=(w==1440))
    b.close()
```

Pass conditions: zero dashes; no overflow; nothing missing from the fold at 390; height within budget; zero console errors. A failed Google Fonts request inside a sandbox is expected and not a page error.

Then look once: open the 390 light, 390 dark, and 1440 full screenshots with the Read tool and check six things.

1. **Five-second test.** From the 1440 top alone, write one sentence: what the page recommends and what it asks. If you cannot, fix the verdict.
2. **Visual ratio.** Every section's visual survives the removal test.
3. **Claim audit.** Counts in the headline and lead match what renders (rule 6).
4. **Crowding.** Labels on bars do not collide at 390; key-date text does not wrap awkwardly at 1440.
5. **The Paddle bar.** Would Paddle ship this? Numbers sit on hairlines with mono labels, every section has a real visual, every button and row responds to hover and focus. If a section is a text box with a number in it, add its visual or cut it.
6. **Width.** At 1440 the content spans the page with a gutter, not a narrow column.

Make one pass of fixes, re-run the script, and publish. In Presenter mode, count slide cards against source slides and confirm no script block is truncated. For client-facing pages, also run `visual-verify` (`audit.py` at 390 and 1440) for contrast and tap targets. If no browser is available, say so and label the page unverified.

## Phase 7: Deliver

1. Publish with the Artifact tool. The `<title>` is a short name specific to the subject (the reader and occasion), stable across redeploys; a one-sentence `description`; a favicon on first publish. Updating an existing page: pass its URL so the link stays the same.
2. Save a copy in the vault beside the counterpart's materials: `Atlas/Clients/{name}/` for a client, `Atlas/Context Docs/{entity}/` for a partnership, `Atlas/Meetings/{date} {topic}/` for internal prep, `Calendar/Meetings/` for readouts. File name carries the date and the reader. Presenter pages are marked internal in the name and are not for the external counterpart. If the recipient has had deliverability trouble with the sender, recommend the hosted link or a chat app over an email attachment.
3. The delivery message is two lines: what the page asks of the reader, and the measured heights at 1440 and 390 with the fold result. Deep reads about a third of any output.

## References

| File | Read when |
|---|---|
| `references/components.md` | choosing and sourcing components (21st.dev queries, kit fallbacks) |
| `references/charts-tables.md` | any chart or table: which chart fits the data, labels on marks, two scales, computed columns |
| `references/motion.md` | reveal timings, easing, reduced motion, static export mode |
| `references/micro-interactions.md` | hover, focus and touch responses (MicroKit patterns, ported) |
| `references/templates.md` | proposing a page template and locking a brand |
| `references/design-language.md` | the Warm Editorial language, only when it is the right call |

When these files are not in the account copy of the skill, read them from the Celsus vault at `Other/Skills/executive-one-pager/references/`.
