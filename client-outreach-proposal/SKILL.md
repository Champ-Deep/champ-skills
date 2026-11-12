---
name: "client-outreach-proposal"
description: "Use when a client sets outreach terms to quote: channels, volume, price."
version: 1.0.0
author: Deep / Champions Group
license: internal
metadata:
  hermes:
    tags: [sales, pricing, outreach, proposal, celsus]
    related_skills: [lead-gen-playbook-builder, negotiation-coach, kanban-task-intake, reach]
---

## When to Use

Use when a client or partner hands over outreach terms to quote against: a named product, named channels, a monthly volume, an outcome-based pricing model (commission, pay per meeting, retainer), and a list of questions they want answered. Also use when someone forwards an outreach request with constraints ("product X only, channel Y only, at least N meetings a month") and asks you to move on it.

# Client outreach proposal

The deliverable is one effort note that carries the whole bid (terms, capability check, capacity, cost, price, staged reply) plus a `needs_input` decision card for Deep. Nothing goes to the client in this session: the reply is staged for the named person to send after Deep rules.

## Build sequence

Work in this order. Each step exists to stop a later one from guessing.

### 1. Extract their terms as a table

Product, channels allowed, geography, monthly volume, pricing shape (retainer, per meeting, commission), tracking system, and the explicit list of questions they ask back. Quote their volume exactly: "at least N qualified meetings" is a commitment, not a target, and the word *qualified* is unpriced until you define it.

Answer every question they asked. A reply that skips one of their questions is read as a non-answer.

### 2. Capability check before anything is costed

For each channel in their terms, confirm the tooling actually exists and name it: LinkedIn sending (a separate tool plus sender profiles), cold email (which sending system, which domains, whose brand), phone (whose telecalling roster, what hours). Their channel rules can rule out assets we already have; that goes in the note as the first fact, because it changes who can staff the campaign and what phase two looks like.

Check ownership of the geography too: APAC accounts are Rupak's, and any region split is a fact to confirm with Deep, not an assumption to make in the proposal.

If a channel is only offered as a later add-on, say what has to change for it (their rule, a domain they own, a warm-up period) instead of quietly proposing it.

### 3. Capacity math, every rate sourced

Build the funnel top to bottom for one sending seat, then work out how many seats the monthly volume needs. Give each rate a basis: a named internal playbook, a vendor figure, or the word *assumption*. The default LinkedIn invite pace is conservative and seniority cuts acceptance below generic B2B rates; when a playbook states a target range, use the bottom of it for C-level buyers and say so.

Rounds the client will count against you (qualified, held, not an existing opportunity) come off the booked number, so include that loss explicitly. Add a seat of headroom over the exact requirement: one seat at the arithmetic minimum has no buffer for ramp, and the first month always lands under target.

Label everything an assumption carries: funnel rates, FX rate, labour cost, timeline. An unlabelled assumption is indistinguishable from a sourced figure to the reader.

### 4. Cost model

Tools (per seat, from the vendor's own pricing page), labour (title and cost centre, never a named person's salary), data and enrichment, overhead. Sum to a monthly cost and divide by the volume for cost per unit. Add the one-time setup cost separately (labour for ICP, list build, messaging, profile setup, plus the first month of tools during warm-up).

Do not cost in people who are not hired, and say in the note that you did not. Their compensation being unknown is a reason to leave them out of the model, not a reason to guess.

### 5. Price: anchor, floor, and two structures

See `references/pricing-benchmarks.md` for published market ranges and tooling costs; re-check the number on the vendor's own page before it reaches the client and flag anything a secondary source could not confirm.

- **Anchor** is what you quote: high enough to cover cost per unit with margin, inside the published market range for the deal size.
- **Floor** is the walk-away, stated in the note even though the client never sees it.
- **Two structures**: quote the anchor, then offer one alternative weighted toward what the client asked for (usually more commission, less fee). Giving them two of ours to choose between beats competing against other partners.

Commission on its own is a loan: deals close months later, and a pre-fundraise or early-stage payer carries credit risk. Say that in one line in the note. Commission then buys upside, never the floor.

Terms that protect the margin go in the same section, not a later one: *qualified* defined in writing before launch (ICP, approved titles, geography, not an existing opportunity, attended), fees invoiced on a stated cycle, commission due when the client is paid, read access to their CRM for attribution, and volume as a target from a stated month rather than a penalty.

### 6. Proof: never invent it

Search the vault for a real result with the right buyer type before writing a claim. If none exists, the reply carries a `[CONFIRM: <who> supplies <what>]` placeholder and the note says in words that the reply must not be sent with the placeholder in it. An invented number, or a vague "we have results in this vertical", is worse than no claim. Where we have no proof, offer something that needs none (a free sample, a no-strings first slice).

### 7. Land it as a card, not prose

The bid is a commercial decision, so the note ends with a `Decisions for Deep` list and each independent ruling becomes its own `needs_input` card in the section 3 shape (from `kanban-task-intake`), recommendation first, naming the note path and every open check (labour assumptions, account owner, unconfirmed results). The staged reply lives inside the note as a fenced section marked NOT SENT, naming who sends it.

Pricing is Deep's call. For a business decision like this the gate is `mcp__clef__decide` on the situation, which matches precedents and returns `ask_deep` when none covers the case: a new commercial shape comes back with no verdict, so land the quote as a `needs_input` card anyway, with the abstention noted as why the card exists. A chat answer with no card has nowhere to land, so create the card before you ask, then report against its id.

### 8. Client-facing page (when Deep asks for a shareable version)

Deep rejects flat price lists: every price on the page must read as computed. Worked build: `/Users/deep/repos/runtimeai-bid/` (engine, render script, QA script). Reuse it by copying the folder and editing `engine/inputs.json` and `content.json`.

- **Engine first.** Pure `pricing.mjs` plus `inputs.json` plus a `node:test` file, written and passing before any HTML. The render script writes engine output into the HTML (so static and PDF exports carry final values) and inlines the engine verbatim for the live calculator. Assert the inlining byte for byte.
- **Anchor in three steps.** (1) Work: one seat's month on a per-seat rate card, divided by the funnel's qualified meetings per seat, rounded DOWN to the nearest 10 ("the fee never runs above the seat"). The outcome-weighted fee is the same ledger minus the labour line. (2) Value: meeting value = ACV x close rate, and a quarter of it is the most a meeting should cost. Sliders let the client enter their own numbers. (3) Market: published per-meeting ranges as range bars, with our fee and the moving value ceiling marked.
- **Commission gaps are computed, not chosen.** Use base + fee gap / (reference ACV x close), rounded UP to a whole percent. Show the commission-only equivalent as math, not as an offer. Quoted terms are calibrated once at a labelled reference deal and stay fixed while the sliders move. Test that.
- **The rate card is a price, not a cost.** The client sees it, so it goes on the decision card for Deep. Internal cost, the floor and staffing never appear on the page, and the forbidden-string sweep checks this.
- **Leak sweep uses word boundaries.** A plain substring match flags `APAC` inside "capacity".
- **Frontend cards for this lane can log `skipped_nonspawnable`.** Check `hermes kanban show <id>` about a minute after creating the card. If it says that, build the page in the main lane with the showcase kit and still send it to the reviewer.

## Always-on rules

- No em dashes anywhere in the note, the reply or the card.
- Every figure is sourced or labelled an assumption. Every rate names its basis.
- Nothing is sent, posted or committed. Stage it, name where it is staged, and end on the decision card.
- APAC is never proposed as a region for Deep's sales team; flag the account owner instead.
- Quotes are grounded in a live search or a vendor page, never in memory. The market moves; a rate recalled from training is a wrong rate waiting to happen.
- Verify the finished note before delivery: no em dashes (count them in code), wikilinks pass the vault's link checker, and the section numbers the reply and card point at actually exist.
- Do not cost in candidates under diligence, and do not name individuals in cost lines.

## Reference files

- `references/pricing-benchmarks.md`: published pay-per-meeting and retainer ranges, LinkedIn tooling costs, and the anchor/floor structure, each with its check date. Read in step 5.