---
name: executive-one-pager
description: "Distills meeting summaries, transcripts, documentation, or presentations into a single visually-driven HTML one-pager in the Warm Editorial design language. MANDATORY TRIGGER for \"one-pager\", \"exec one-pager\", \"executive summary page\", \"condense this into a page\", \"follow-up one-pager\", \"shorten this deck/doc into one page\", \"make a leave-behind\", or any request to compress source material into one shareable page. Also handles \"presenter prep\" one-pagers for a slide deck: deck context plus slide-by-slide talking points and a natural spoken script per slide for whoever is presenting or sitting in on the pitch, trigger on \"talking points\", \"script for each slide\", \"slide-by-slide\", \"prep [someone] for this deck\". Works with any brand: swaps the accent color per brand guidelines."
---


# Executive One-Pager

Turn dense source material (meetings, docs, decks) into one scrolling HTML page that a decision-maker can absorb in ninety seconds. The output is not a summary document. It is a visually-driven page where every section earns a visual and every number carries evidence.

Two output modes, decided in Phase 1:

- **Summary mode** (default): condense source material into a single distilled narrative page. This is the original behavior.
- **Presenter mode**: the source is a slide deck (pptx/pdf/keynote export) and the reader needs to actually deliver or sit through it. The page still opens with the summary-mode hero and context sections, then adds a slide-by-slide walkthrough: one card per slide with talking points and a natural spoken script. Trigger presenter mode when the user asks for "talking points," "a script for each slide," "slide-by-slide," "prep [someone] for this deck," or uploads a deck alongside a request to brief a presenter (including briefing the user themselves before they present it).

## Phase 1: Ingest and distill

Accept any combination of: meeting summaries or transcripts (Zoom/Otter/pasted notes), long documents (md, docx, pdf), presentations (pptx: use the pptx skill to extract; pdf export of a deck: read directly, page order is slide order), or prior emails. If the source is a meeting the user attended, check connected meeting tools (Zoom MCP, vault triage notes) before asking for notes.

Extract into an intelligence brief. For large transcripts, delegate extraction to a subagent so raw source stays out of context. The brief must capture:

1. **Audience**: who reads this, and who actually decides. Write for the decider even when sending to the forwarder. In presenter mode, the "reader" is the presenter, not the deck's external recipient. Identify them by name if known (check calendar/meeting-prep notes for the meeting the deck is going into).
2. **What they said**: their business reality, pain points, and 3-6 short verbatim quotes worth echoing back.
3. **What we offered**: the proposal, mechanism, and differentiators.
4. **Numbers**: every figure stated (budgets, volumes, percentages, timelines). Never invent or extrapolate beyond simple arithmetic on stated figures.
5. **Commitments**: next steps from EACH side, with owners and dates.
6. **Objections and concerns**: these become trust sections, not omissions.
7. **The one action**: what the reader should do at the end (book a slot, confirm a date, forward it).
8. **(Presenter mode only) Per-slide content**: for every slide, capture its headline, its supporting copy, any numbers/sources on it, and what job that slide does in the pitch (open the pain, prove the market, handle an objection, close). This becomes the raw material for talking points and the script; do not skip slides.

**Verify facts before building.** Product names, company spellings, and titles get checked against the entity's public website. Transcripts mangle names. In presenter mode, cross-check deck numbers against any master source or fact-verification doc for the same pitch if one exists in the vault/workspace; flag illustrative/internal-assumption figures as such in the talking points so the presenter doesn't over-assert them as external fact.

## Phase 2: Clarify (only if needed)

If brand, audience, or the desired CTA is unknown, ask via AskUserQuestion in ONE round. Otherwise proceed: a meeting follow-up defaults to the brand that ran the meeting, the attendees as audience, and the agreed next step as CTA. For presenter mode, if it's ambiguous who is being briefed, default to the user themselves or the most senior person on the invite who isn't the deck's author.

## Phase 3: Architecture

Read `references/design-language.md` in this skill NOW (it contains the full token set, component recipes, animation library, and binding design rules). If the workspace has a fuller local standard (e.g. `Atlas/Context Docs/Design/Warm Editorial Design Language.md` in the Celsus vault), prefer that and use the skill copy as fallback. If the source deck itself has a locked brand design system in the workspace (colors, type, do/don't rules), prefer that brand's tokens over the generic Warm Editorial accent swap so the one-pager visually matches the deck it is briefing.

Map content to section archetypes. Use only what the content supports, in roughly this order:

| Archetype | Use when | Key components |
|---|---|---|
| Hero + living vignette | always | serif headline (one italic word, ends with period), personal lead, meta row, simulated micro-UI card animating the core offer |
| Topic marquee | there is a domain vocabulary | serif scrolling strip of the reader's world (standards, markets, products) |
| "What we heard" | source is a meeting | 2x2 hairline grid; each cell: mono kicker, title, MICRO-VISUAL derived from their reality, one line, verbatim quote in serif italic |
| The offer / engine | there is a proposal | two-col: prose + score bars + nested compact stats left, cadence timeline card right |
| Trust / compliance card | they raised concerns | key-value rows with hover verify glyphs, chips, status pills |
| Proof | there are results to cite | evidence cards: before/after bars, delta pill + rising spark, dot grid for rates |
| Recommendation | a path was proposed | numbered horizontal timeline (01/02/03) |
| Statement band | there is a big reciprocal or vision moment | full-width serif statement with italic pivot |
| **Slide walkthrough (presenter mode)** | briefing someone to deliver or sit through a specific deck | one card per slide in deck order: mono slide number, the slide's own headline restated, a short "what this slide is doing" line, 2-4 talking-point bullets (facts/numbers to hit), and a distinct spoken-script block (serif italic, quote-styled, feels transcribed not written) the presenter can read almost verbatim; group into the deck's natural acts (e.g. open/market case/model/close) with a mono section label between groups |
| Next steps | always | two cards: "On us" / "Over to you", each row with status pill and date; CTA buttons (primary + ghost) |
| Footer | always | brand wordmark, tagline, counterparts, context |

In presenter mode, keep the hero + context sections short (deck name, audience, occasion, the one-line offer, why this meeting matters) so the slide walkthrough is the bulk of the page. Do not literally reproduce every deck section archetype above the walkthrough; two or three context sections is enough runway before the per-slide cards start.

## Phase 4: Copy rules

Short sentences. Plain words. No em-dashes ever (periods, commas, colons). Headlines end with a period. Echo their own quotes back in serif italics. Highlight 2-4 VALUE phrases per section with the `.hl` shimmer span (the phrases a skimming CEO must catch), never connective prose. Address the reader by name in the hero lead when it is a follow-up or a presenter briefing.

**Presenter-mode script writing.** Load the `vinh-copywriting` skill for every spoken-script block before finalizing copy. Treat each slide's script as "Talking Points / Speaking Notes" per that skill's calibration guide: Complexity Level 1, speech rhythm with short fragments, mark a natural pause with a line break rather than the literal word "pause," one anchor story or concrete image per script where the source supports it, and always close with the bridge to the next slide so the deck reads as one conversation, not twelve disconnected blurbs. Run the Vinh Rewrite Checklist (banned-word purge, friend test, one idea per block) on every script before it ships. Scripts must sound like something a person would actually say out loud, not a bullet list read aloud.

## Phase 5: Build

One self-contained HTML file (inline CSS + JS, Google Fonts only external). Apply the design tokens verbatim; swap ONLY the accent color for the brand (consult the brand's guidelines skill if installed; re-derive accent-soft at ~10% alpha and the card shadow tint from the new accent). Include: aurora background, hero particle canvas with radial mask, scroll-reveal observer, scroll progress bar, marquee duplication, at least one animated micro-UI vignette, keyword highlights, interactive rows. In presenter mode, add a sticky or floating slide-jump index (mono numbers) so the presenter can jump straight to a slide mid-meeting, and visually distinguish the talking-points block from the script block within each slide card (e.g. bullets in sans vs. script in serif italic on a slightly tinted sub-panel) so a presenter skimming mid-pitch can tell them apart at a glance.

Binding rules from the design standard: no text-only cards (every card carries a content-derived micro-visual); stats nest into dead space as compact 2x2 grids, never full-width strips; stat cards carry visual evidence derived from stated numbers only; bar-fill elements must be `display:block` (inline spans ignore width); check contrast on every tinted surface; respect `prefers-reduced-motion`.

## Phase 6: Verify

Screenshot the page at 4-6 scroll positions with Playwright (or the browser extension) after animations settle (~1.5-2s per position). Check: console errors are zero, every bar/spark/donut actually filled, highlights wiped in, nothing overflows, hover states work on one sampled row. In presenter mode, also verify every slide in the source deck has a corresponding card (count them) and that no script block got truncated. Fix and re-shoot before presenting.

## Phase 7: Deliver

Save next to the client's other materials (e.g. `Atlas/Clients/{name}/` in a vault, or the relevant `Atlas/Context Docs/{entity}/` folder for a partnership pitch). Present the file. If the recipient has had email deliverability issues with the sender, recommend sharing as a hosted link or via chat app instead of attachment. In presenter mode, mention this is for internal prep, not for the external counterpart, when saving/naming the file.


---

## Verify before delivery — MANDATORY

This output is visual, so reading the source does not tell you whether it worked. Render it and look at it.

```bash
python3 visual-verify/scripts/audit.py <output.html> --width 390
python3 visual-verify/scripts/audit.py <output.html> --width 1440
python3 visual-verify/scripts/shoot.py <output.html> --widths 390,1440 --themes light
```

Then **open every screenshot with the Read tool** and critique it. Not the file listing, the images. A screenshot you did not look at has verified nothing.

The four things this catches that nothing else does:

1. **Contrast measured against the composited background**, including transparency stacking, rather than against the hex you intended.
2. **Horizontal overflow at 390px**, with the offending element named.
3. **Content that overflows its container** once real text length replaced the sample.
4. **Flat hierarchy** — three elements competing where one should dominate. Only the eye finds this.

Zero FAILs before delivery. Every WARN either fixed or justified in one line. If no browser is available, say so and label the output **unverified**, listing what was not checked.

→ Full protocol: the `visual-verify` skill.
