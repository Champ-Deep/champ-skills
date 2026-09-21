---
name: executive-one-pager
description: "Distills meeting summaries, transcripts, documents, or decks into ONE decision page: verdict on screen one, evidence as visuals, hard length budget, mobile-first, style chosen per document with brand colours locked. Trigger on one-pager, exec one-pager, executive summary page, condense this into a page, follow-up one-pager, make a leave-behind, turn this into HTML, talking points, slide-by-slide, prep someone for this deck."
---

# Executive One-Pager

A decision-maker opens this on a phone, between meetings, and gives it ninety seconds. In that time they must learn three things: what the answer is, what the numbers say, and what you want them to do. Everything else on the page is evidence they can drill into if they choose.

The page is judged by one test: **cover everything below the first screen. Can the reader still act?** If not, the page failed, however beautiful the rest is.

## What went wrong before (do not repeat)

Previous outputs from this skill were 6,000 to 9,500px tall on desktop and up to 17,000px on a phone: ten to twenty screens of editorial prose wearing a one-pager's name. The verdict was scattered across the scroll, sections were text cards dressed in mono labels and italic quotes, and every page used the same visual bones. The rules below exist to stop each of those failures.

## Two modes

- **Summary mode** (default): one distilled decision page.
- **Presenter mode**: the source is a deck and the reader must deliver or sit through it. The page opens with a one-screen verdict, then a slide-by-slide walkthrough. Trigger on "talking points", "script for each slide", "slide-by-slide", "prep [someone] for this deck", or a deck uploaded with a request to brief a presenter (including the user themselves).

## Hard rules (non-negotiable)

1. **Verdict on screen one.** The first viewport at 390px wide holds: the headline (the answer, not the topic), three numbers with comparators, and the one ask with owner and date. Nothing else comes before it.
2. **Length budget.** Summary mode: at most five sections after the verdict, at most 3,000px tall at 1440px wide, at most 6,500px at 390px. Presenter mode: the context runway before the slide cards is one desktop screen; the walkthrough itself is exempt from the cap but each slide card is at most 260px tall collapsed.
3. **Assertion headlines.** Every section heading is a full-sentence conclusion the reader could repeat in a meeting ("The TAL dispute costs a week of sends per round of revisions"), never a topic label ("The TAL dispute"). Headlines end with a period.
4. **Visual first, text second.** Every section leads with a content-derived visual (chart, timeline, comparison, option grid, status rows) and carries at most three lines of supporting text plus one takeaway line. The visual removal test: if deleting the visual loses no meaning, it is decoration; replace it with a real one or cut the section.
5. **Numbers carry comparators.** No bare figure anywhere. Every number sits beside a target, a prior period, a peer, or the counterpart's own stated goal. Stat visuals derive only from stated figures; simple arithmetic on stated figures is allowed, extrapolation is not.
6. **Progressive disclosure.** Detail (quotes, per-account rows, objection handling, full timelines) lives behind "show detail" toggles that default closed. The skim view is the default view.
7. **Style is a decision per document.** Pick a named style from `frontend-design` (`reference/styles-database.md`) that matches the document's job and audience; Warm Editorial is one option, never the reflex. Brand colours from the relevant brand skill are locked and override the style palette. Never reuse the previous one-pager's style for the next one unless the two are a matched series.
8. **Mobile-first.** Base CSS targets 390px (single column, 17px body, 44px tap targets, no horizontal overflow); `min-width` queries add desktop columns. Every horizontal timeline or multi-column grid collapses to vertical below 860px.
9. **No em dashes, no en dashes**, anywhere, including headings and date ranges. Use commas, periods, colons, or "to".
10. **Never name a delivery vendor to a client.** Vendors are "we" or "our team" in anything client-facing. A client works with Lake B2B or SPAN, never both; strip the other from client materials.

## Phase 1: Ingest and distill into a verdict brief

Accept meeting summaries or transcripts (Zoom, Otter, pasted notes), long documents (md, docx, pdf), decks (pptx via the pptx skill; pdf export read directly, page order is slide order), prior emails. If the source is a meeting the user attended, check the connected meeting tools and vault triage notes before asking for notes.

For long transcripts, delegate extraction to a subagent so raw source stays out of context. The subagent returns a **verdict brief**, not a summary:

| Field | What it holds |
|---|---|
| Reader | Who opens it and who actually decides. Write for the decider. In presenter mode the reader is the presenter. Name them if known (calendar, meeting-prep notes). |
| Answer | One sentence. The conclusion or recommendation. This becomes the headline. |
| Three numbers | The three figures that most change the reader's mind, each with its comparator and source line. |
| The ask | One action, one owner, one date. |
| Evidence | Three to five points that support the answer, each tagged with the visual that proves it (see the archetype table). |
| What they said | Two to four short verbatim quotes worth echoing, for the detail layer. |
| Options | If a decision is open: two or three options with cost, risk, and the recommended one marked. |
| Commitments | Next steps from each side with owners and dates. |
| Concerns | Objections raised; these become a risk visual, never an omission. |
| Per-slide content (presenter mode) | Every slide: headline, supporting copy, numbers and sources, and the job the slide does (open the pain, prove the market, handle an objection, close). Skip nothing. |

**Verify before building.** Product names, company spellings, and people's names get checked against the entity's public site and against sources Deep confirmed directly. Transcript-sourced names are suspect by default. In presenter mode, cross-check deck numbers against any master or fact-verification doc for the same pitch; flag illustrative figures so the presenter does not assert them as fact.

## Phase 2: Clarify (one round at most)

If brand, reader, or the ask is unknown, ask via AskUserQuestion in ONE round. Otherwise proceed with defaults: a meeting follow-up takes the brand that ran the meeting, the attendees as readers, and the agreed next step as the ask. In presenter mode, default the briefed person to the user or the most senior person on the invite who did not author the deck.

## Phase 3: Choose the style and the sections

**Style.** Load `frontend-design` and run its style selection for real: name the document's job (deal follow-up, internal review prep, partnership pitch, weekly ops readout, presenter brief) and the reader's world, then pick the named style whose mood matches. Record the choice and the reason in one line at the top of the DESIGN.md that `frontend-design` produces. Apply the brand skill's colours on top. If the source deck has a locked brand system in the workspace, match it so the brief looks like the deck it serves. If the workspace has the Warm Editorial standard (`Atlas/Context Docs/Design/Warm Editorial Design Language.md`, or `references/design-language.md` in this skill) and that style is the right call, use it; otherwise leave it alone.

**Sections.** Pick at most five from this table. Each row names the visual that carries it; a section without its visual does not ship.

| Section | Use when | The visual that carries it |
|---|---|---|
| Verdict panel (always, first) | every page | Headline, three stat tiles with comparator and direction arrow, the ask as a single action row with owner, date, and primary button |
| Where we are | there is a process, campaign, or deal in flight | Horizontal stepper or timeline with a "today" marker; done steps filled, blocked steps flagged |
| What changed | there is a before and after | Paired bars or delta tiles derived from stated numbers |
| The decision | a choice is open | Two or three option cards side by side: cost, time, risk chips; the recommended card carries a pill |
| Risks and objections | concerns were raised | Ranked rows with severity chip and the one-line answer to each; or a 2x2 (likelihood x impact) when there are four or more |
| What they said | the source is a meeting and their words matter | Two to four quote cards, each with a micro-visual of the reality it describes (a bar, a count, a status) |
| Proof | results exist to cite | Before/after bars, delta pill, dot grid for a rate; stated numbers only |
| Next steps (always, last) | every page | Two columns, "On us" and "Over to you", each row with status pill, owner, date; primary and ghost buttons |
| Slide walkthrough (presenter mode) | briefing a presenter | One card per slide in deck order: mono slide number, the slide's headline, one line on what the slide is doing, two to four talking points, and a distinct spoken-script block (serif italic on a tinted sub-panel) the presenter can read almost verbatim; grouped into the deck's acts with a label between groups; sticky slide-jump index |

Reading order follows the Z-pattern on desktop: headline top-left, numbers top-right, the ask bottom-right of the verdict panel. On a phone the same four elements stack in that order.

Layout contract for the verdict panel (desktop; stacks on phone):

```
+----------------------------------------------+------------------------------+
| KICKER: reader, occasion, date               | NUMBER 1  NUMBER 2  NUMBER 3 |
| HEADLINE. The answer, one sentence.          | vs target  vs last  vs their |
| Lead: two lines, who this is for and why now.| +12%       flat     short    |
|                                              +------------------------------+
|                                              | THE ASK: action, owner, date |
|                                              | [Primary button] [ghost]     |
+----------------------------------------------+------------------------------+
```

## Phase 4: Copy rules

Short sentences. Plain words. Headlines are assertions and end with a period. Address the reader by name in the lead when it is a follow-up or a presenter brief. Highlight at most two value phrases per section, never connective prose. Quotes go in the detail layer unless one quote is itself the evidence.

**Presenter-mode scripts.** Load `vinh-copywriting` for every spoken-script block. Complexity level 1, speech rhythm with short fragments, a line break for a natural pause (never the word "pause"), one anchor story or concrete image per script where the source supports it, and always close with the bridge to the next slide. Run the Vinh rewrite checklist on every script. Scripts sound like a person talking, not bullets read aloud.

## Phase 5: Build

One self-contained HTML file: inline CSS and JS, Google Fonts as the only external dependency. Build through `frontend-design` (DESIGN.md first, then the page), then hand to `ui-polish` and `design-trends` as their triggers require.

Build order that keeps the budget honest:

1. Verdict panel first. Render it alone at 390px and confirm it fits one viewport (headline, three numbers, the ask). Only then add sections.
2. Add sections one at a time, visual first, text second. After each, measure `document.documentElement.scrollHeight` at 1440 and 390. Stop adding when the budget is reached; move what is left into detail toggles or cut it.
3. Charts and bars: use real SVG or CSS bars with values labeled directly on the mark (no axis hunting). Bar fills are `display:block`. Dim colour for "before" or "missing", brand accent for "after" or "ours". One accent, one alert colour, neutrals for everything else.
4. Interaction: scroll progress bar, section reveal on scroll, detail toggles, hover state on rows. In presenter mode add the sticky slide-jump index. Respect `prefers-reduced-motion`. Ambient motion (aurora, particles, marquees) is allowed only if the chosen style calls for it and it never pushes content down.
5. Icons are inline stroke SVG. Never emoji, never icon fonts. Never pure #FFF or #000 text on tinted surfaces without a contrast check.

## Phase 6: Verify (mandatory, the output is visual so reading the source proves nothing)

Run the `visual-verify` gate:

```bash
python3 visual-verify/scripts/audit.py <output.html> --width 390
python3 visual-verify/scripts/audit.py <output.html> --width 1440
python3 visual-verify/scripts/shoot.py <output.html> --widths 390,1440 --themes light
```

Then add the four checks specific to this skill, and record the numbers in the delivery note:

1. **Fold test.** In the 390px top screenshot, the headline, all three numbers, and the ask are visible without scrolling. If the ask is cut off, shrink the hero, not the ask.
2. **Length budget.** `scrollHeight` at 1440 is at most 3,000px and at 390 at most 6,500px (summary mode). Over budget means cut or fold into detail toggles; never shrink type to fit.
3. **Five-second test.** Open the 1440px top screenshot and write, in one sentence, what the page recommends and what it asks for. If you cannot write that sentence from the screenshot alone, the verdict panel failed. Fix it.
4. **Visual ratio.** Count sections; count sections whose visual survives the removal test. The two numbers must match.

Also confirm: zero console errors, every bar and spark actually filled, no horizontal overflow at 390, hover works on one sampled row, zero em or en dashes (`grep -cP '\xe2\x80[\x93\x94]' <output.html>` must print 0). In presenter mode, count slide cards against source slides and check no script block is truncated. Open every screenshot with the Read tool and critique it; a screenshot not looked at has verified nothing. Zero FAILs before delivery; every WARN fixed or justified in one line. If no browser is available, say so and label the output unverified.

## Phase 7: Deliver

Save next to the counterpart's other materials (`Atlas/Clients/{name}/` for a client, `Atlas/Context Docs/{entity}/` for a partnership, `Atlas/Meetings/{date} {topic}/` for internal prep). Name the file with the date and the reader. In presenter mode, mark the file internal in its name and note that it is not for the external counterpart. If the recipient has had deliverability trouble with the sender, recommend a hosted link or a chat app over an email attachment.

The delivery message is two lines: what the page recommends, and the measured page heights at 1440 and 390 with the fold test result. Deep reads about a third of any output; the first two lines carry the whole message.