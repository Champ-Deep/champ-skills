---
name: "deck-doctor"
description: "Executive review, fact-verification, and rebuild of any pitch/partnership/sales slide deck, producing an enhanced master source document, a sanitized deck source, and a compact cinematic NotebookLM Studio prompt. Trigger on: \"review this deck\", \"beef up this presentation\", \"bolster this deck\", \"verify the facts in this presentation\", \"executive cut\", \"too many slides\", \"make the deck cinematic/visual\", \"turn this deck into a NotebookLM prompt\", or any uploaded deck needing enhancement before a high-stakes meeting."
---

# Deck Doctor : Executive Deck Review, Fact-Verification, and Cinematic NotebookLM Rebuild

Turn any existing slide deck (or draft deck content) into three deliverables: (1) a fact-verified internal **master source document**, (2) a **sanitized deck source** safe to upload to NotebookLM, and (3) a **compact cinematic NotebookLM Studio prompt** that regenerates the deck. Works for any brand, any audience, any model. Follow the phases in order.

## Phase 0 : Intake

Establish before working (ask only if not inferable):
- **Audience and stakes:** who sits in the room (owners, REIT execs, investors, CHROs), meeting length, and whether the deck is the whole agenda or one item among several.
- **Sender entity and brand.** Load the entity's brand skill/guidelines if one exists.
- **The ask:** what the presenter wants the audience to do next. A deck without a named ask is a brochure.
- **Commercial sensitivity:** which numbers are settled versus aspirational. Unsettled numbers must never reach the rendered deck.
- Extract full deck text (for .pptx use python-pptx: iterate slides, text frames, tables, notes; for PDF use pdftotext, and if it returns almost nothing the PDF is image-based, so render pages with pdftoppm and read them visually). Preserve every number, table, and claim.

## Phase 1 : Context Mining

Search the user's vault/workspace/CRM for: prior meetings with this audience, feedback from similar pitches (objections, declines, what worked), related projects, and internal proof points (live projects, vendors, credentials). Prior-pitch feedback is gold: fold hard-won lessons into pitch-discipline notes.

## Phase 2 : Fact Research and Verification

Research BEFORE restructuring. For every market claim in the deck, and for the 3 to 6 strongest claims the deck is missing:
- Verify via web search with named, dated sources. Prefer primary/institutional sources over blogs.
- Find **precedent proof**: named, credible operators already running the same model at scale.
- Find the **buyer-specific angle**: stats about the audience's own world so at least one slide is about them, not the seller.
- Build a **Fact-Verification Register** with three statuses: VERIFIED (source name and year), INTERNAL ASSUMPTION (label "illustrative"), INTERNAL ESTIMATE (directional, "verify against partner's own numbers"). Never let an unverifiable claim appear unlabeled. Never invent numbers.

## Phase 3 : Executive Critique Rubric

1. **Decision speed.** Executives decide in the first three minutes. Pain and offer clear by slide 2.
2. **Pain before opportunity.** Open with a cost the audience already privately knows, then sell the conversion.
3. **One idea per slide; assertion headlines.** Every headline is a full takeaway sentence. The headline row alone should tell the whole story.
4. **Commercial disclosure discipline.** A first-meeting deck states the commercial concept in one qualitative line ("minimum guarantee plus performance-linked revenue share, tailored after site assessment"). Detailed tables, tiers, percentages, and fees go to a separate proposal document, NOT to a deck appendix. Appendixes get rendered and read; if numbers are unsettled they will be quoted back at you.
5. **The money slide.** Comparative math in the buyer's own unit of account, only if the underlying numbers are settled enough to defend live.
6. **Human proof.** One "day in the life" journey slide. End-users, not investment mechanics.
7. **De-risk before the ask.** Name the downside plainly plus zero-commitment proof steps (virtual tour, live-project reference, site visit).
8. **Named ask with a deadline.**
9. **Length.** 10 to 12 slides when the deck is a segment of a meeting; 12 to 14 if it is the whole meeting. No appendix in the rendered deck.
10. **Sourcing.** Every external stat carries an on-slide source attribution.

## Phase 4 : Build Two Source Documents

**A. Internal master source (complete):** one markdown doc with ALL content: one-line offer, pain open with the exact opening line, verified market case table with sources, precedent proof and competition clock, the deal, money math, responsibility matrix, full commercial model (labeled illustrative), alternative structures, economics with credibility cross-check, services, day-in-the-life, buyer-specific angle, proof/virtual-tour, risk reversal, terms, Fact-Verification Register. This is the internal reference and proposal feeder. It is never uploaded to NotebookLM.

**B. Sanitized deck source:** a second markdown doc containing only what may appear on screen. Strip every unsettled or sensitive number: prices, percentages, fee structures, guarantee amounts, membership pricing, economics. Keep verified external stats with sources, qualitative commercial framing, narrative sections, and the ask. **This redaction layer is the only reliable control: a generator will render any number it can see, regardless of prompt instructions.**

Apply the user's house style rules (for this user: never use em dashes; wikilinks when saving into the Obsidian vault; save under the relevant entity's context-docs area).

## Phase 5 : Write the Compact Cinematic NotebookLM Prompt

Hard rules learned from production use:
- **Prompt body under roughly 3,500 to 4,000 characters.** NotebookLM truncates longer prompts (a ~9,000-character prompt was cut off mid-list in practice).
- **Upload discipline:** instruct the user to upload ONLY the sanitized deck source, verify the notebook's source list contains exactly that one document, and never upload the master source or original deck alongside it.
- **Art direction block is mandatory.** Without it NotebookLM defaults to boxed text grids, line-art ornaments, and zero photography. Specify: every slide is a single full-bleed photorealistic cinematic scene (a frame from a film, editorial travel-magazine composition, golden-hour or dusk light, shallow depth of field, real human subjects mid-experience); a soft dark gradient only where text sits; a named two-tone palette plus one accent; serif headline and sans-serif support typography; a strict text budget (one assertion headline plus at most 30 words per slide); and explicit bans: no boxed text grids, no clip art, no blueprint or line-art ornaments, no decorative frames, no bullet walls.
- **Per-slide scene direction.** Each slide line gives: number, quoted assertion headline, a one-sentence photographic scene description (subject, setting, light), and which source section supplies the support text. Scene variety across the deck: aerials, interiors, human moments, split compositions, timelines.
- **Numbers ban in the prompt too:** "Never state specific prices, percentages, fees, or guarantee amounts; describe commercial terms only as [qualitative line]." Belt and braces with the sanitized source.
- Require on-slide source attribution for market statistics. No speaker notes. **Never include speaker scripts in the prompt**; talking points are authored by the assisting model AFTER the generated deck exists, slide by slide, near-verbatim.

## Phase 6 : Verify and Deliver

- Character-count the prompt body (under ~4,000).
- Grep the sanitized source for currency symbols, percentages, and fee words; every hit must be either a verified external stat with a source or removed.
- Check both files against house style rules.
- Deliver all files, then offer: (a) fold-in of further brainstormed angles, (b) slide-by-slide talking points once the generated deck comes back, (c) a separate commercial proposal document built from the master source.

## Reference : The Executive Sales Arc

Pain (you are losing money today) → Market (the world moved, sources shown) → Competition clock (the best are doing this; the window is now) → The deal in one slide, qualitative → Human proof (a day in the life) → Buyer-specific angle (their world, their war) → De-risk (proof steps + risk reversal) → The ask (named step, named deadline). Commercial detail: separate proposal, never the deck.

