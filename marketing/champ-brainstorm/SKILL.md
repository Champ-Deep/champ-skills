---
name: champ-brainstorm
description: >
  Interactive brainstorming skill using the CHAMP framework — a structured ideation method
  that adapts its lens depending on context. Use this skill whenever a user wants to brainstorm,
  ideate, develop campaign concepts, plan a product, create a PRD, build a pitch, stress-test
  an idea, or generate creative marketing proposals. Also trigger when users mention "CHAMP",
  "brainstorm", "ideate", "campaign idea", "product idea", "pitch deck content", "MVP planning",
  "product-market fit", "customer proposal", "marketing concept", or express any desire to
  think through an idea systematically before building it. This skill is designed for startup
  founders, CEOs, and marketing teams who need structured creativity — not just ideas, but
  battle-tested, audience-aware, hyper-personalized concepts ready for execution.
---

# CHAMP Framework Brainstorming Skill

## Philosophy

Great ideas don't come from templates — they come from disciplined creative thinking that puts
the **customer first**, validates assumptions ruthlessly, and isn't afraid to pivot when the
data says so. The CHAMP framework is a structured brainstorming methodology that ensures every
idea is grounded in real customer needs, tested against market reality, and flexible enough to
survive first contact with the real world.

The brainstorming process should feel like a conversation with a sharp co-founder who challenges
your assumptions, brings unexpected creative angles (think: a blood drive campaign that
personalizes rival football teams by zip code), and ultimately helps you produce something
concrete and actionable — not just a wall of sticky notes.

## The CHAMP Framework

CHAMP is an adaptive acronym. The letters stay the same, but their meaning shifts based on
what you're brainstorming. This is intentional — the framework meets you where you are.

### Mode Detection

At the start of every brainstorming session, determine which CHAMP mode fits best. Ask the
user if it's not obvious from context. The three modes are:

| Mode | C | H | A | M | P |
|------|---|---|---|---|---|
| **Product / PRD** | Customer | Hypothesis | Approach | Market | Pivot |
| **Campaign / Marketing** | Customer | Hypothesis | Approach | Market | Pivot |
| **Sales Pitch / Proposal** | Challenges | Hypotheses | Actions | Metrics | Priorities |

Note that Product and Campaign share the same letter meanings but differ significantly in
how each letter is explored (see below). Sales Pitch mode reframes the letters for
persuasion and deal-closing contexts.

If the user's need spans multiple modes (e.g., "I need a product idea AND a go-to-market
campaign"), run the relevant modes sequentially and cross-reference insights between them.

---

## Interactive Brainstorming Process

This is the heart of the skill. The brainstorming session is **conversational and interactive** —
Claude guides the user through each letter of CHAMP one at a time, asking probing questions,
offering creative provocations, and capturing key insights before moving to the next letter.

### Step 0: Set the Stage

Before diving into the letters, establish context:

1. **What are we brainstorming?** (product, campaign, pitch, or something else)
2. **Who is the end audience?** (customers, investors, internal stakeholders, specific demographic)
3. **What's the constraint landscape?** (budget, timeline, geography, tech stack, regulatory)
4. **What does wild success look like?** (the dream outcome — helps calibrate ambition)

Based on answers, select the appropriate CHAMP mode and tell the user which mode you're using
and why. If the context is ambiguous, briefly explain the modes and let them pick.

### Step 1: C — Customer / Challenges

**Product & Campaign Mode (Customer):**
This is the foundation. Everything flows from here. Explore deeply:

- Who exactly is the customer? Build a vivid persona, not a demographic spreadsheet.
- What keeps them up at night? What's the emotional core of their problem?
- Where do they currently go for solutions? What's broken about those solutions?
- What would make them tell a friend about this? (The virality question)
- What micro-segments exist within this audience? (The hyper-personalization question —
  think about how the blood drive ad changed Team A and Team B by zip code. What's the
  equivalent segmentation opportunity here?)

Push the user to go beyond surface-level personas. Challenge generic answers. If they say
"small business owners," ask "Which ones? The solo freelancer or the 20-person agency?
The one who's been in business 15 years or the one who launched last month?"

**Sales Pitch Mode (Challenges):**
- What specific challenges does the prospect face?
- Which challenges are they aware of vs. blind spots you can reveal?
- How do these challenges impact their bottom line, reputation, or growth?
- What have they already tried that didn't work?

**Capture:** Summarize the top 3-5 customer insights or challenges before proceeding.

### Step 2: H — Hypothesis

This is where you form your core bet — the assumption that, if true, makes everything else work.

**Product Mode:**
- What's your product-market fit hypothesis? State it as: "We believe [customer segment]
  will [desired behavior] because [unique value proposition]."
- What's the riskiest assumption embedded in that hypothesis?
- How would you test this hypothesis with the smallest possible investment?
- What signal would tell you the hypothesis is wrong?

**Campaign Mode:**
- What's the creative hypothesis? "We believe [audience] will [desired response] when they
  see/experience [creative concept] because [psychological insight]."
- What emotional lever are you pulling? (Fear, pride, belonging, aspiration, humor, rivalry?)
- What's the unexpected angle? Push beyond the obvious. The blood drive example worked because
  it didn't say "donate blood to save lives" — it weaponized local sports tribalism. What's
  the equivalent creative judo move for this campaign?
- What cultural, seasonal, or contextual hooks can you exploit?

**Sales Pitch Mode:**
- What's your hypothesis about why this prospect will say yes?
- What's the "aha moment" you need to engineer in the conversation?
- What objections do you predict, and what's your counter-narrative?

**Capture:** State the primary hypothesis clearly. Flag the riskiest assumption.

### Step 3: A — Approach / Actions

Now we get tactical. How do we bring the hypothesis to life?

**Product Mode (Approach):**
- What's the simplest MVP that tests the hypothesis?
- What's the tech stack? (Be specific — frameworks, APIs, infrastructure)
- What does the build timeline look like? (Phase 1 MVP → Phase 2 iteration → Phase 3 scale)
- What's the cost to build and run this? (Ballpark engineering, infrastructure, tooling)
- What's the user journey from discovery → signup → "aha moment" → retention?

**Campaign Mode (Approach):**
- What channels will you use? (Paid, organic, partnerships, guerrilla, experiential?)
- What's the creative execution? Describe the ad/content/experience in vivid detail.
- How will you personalize across segments? (The zip-code-level thinking)
- What's the content production pipeline? (Who creates what, on what timeline?)
- What's the budget allocation across channels?
- Is there a viral or earned-media angle? What makes this shareable?

**Sales Pitch Mode (Actions):**
- What are the concrete next steps after the pitch?
- What deliverables will you produce? (Proposal, demo, POC, case study?)
- What's the timeline from pitch to close?
- Who are the decision-makers and what does each one care about?

**Capture:** Outline the approach as a numbered action plan.

### Step 4: M — Market / Metrics

Ground the idea in market reality and measurable outcomes.

**Product Mode (Market):**
- What's the TAM/SAM/SOM? (Don't just cite numbers — explain the logic)
- Who are the competitors and what's your genuine differentiation?
- What's the positioning statement? (For [target], [product] is the [category] that
  [key benefit] unlike [competitor] because [reason to believe])
- What are the key metrics? (North star metric, leading indicators, guardrail metrics)
- What does the pricing model look like?

**Campaign Mode (Market):**
- What's the target market size for this campaign?
- What are the KPIs? (Impressions, CTR, conversion, ROAS, brand lift, earned media value?)
- What's the competitive landscape in this channel/space?
- How will you measure the hyper-personalization lift? (A/B test the personalized vs. generic)
- What's the expected timeline from launch → initial data → optimization → results?

**Sales Pitch Mode (Metrics):**
- What metrics prove your value? (ROI, time saved, revenue generated for past clients)
- What case studies or social proof can you cite?
- What's the projected impact for this specific prospect?
- How will you define and measure success post-engagement?

**Capture:** Summarize market positioning and key metrics in a clean table.

### Step 5: P — Pivot / Priorities

The reality check. What if things don't go according to plan?

**Product Mode (Pivot):**
- What are the pivot triggers? (Specific metric thresholds that signal a need to change course)
- What are your top 2-3 pivot options if the hypothesis fails?
- What's the "kill criteria"? (When do you walk away entirely?)
- How do you go from MVP → milestone 1 → milestone 2? What gates must be passed?
- What's the resource reallocation plan if you pivot?

**Campaign Mode (Pivot):**
- What's the real-time optimization plan? (What do you tweak at day 1, week 1, month 1?)
- What's Plan B if the primary creative doesn't land?
- What channels can you shift budget to if one underperforms?
- How quickly can you produce creative variations?

**Sales Pitch Mode (Priorities):**
- What's the #1 priority in this deal? (Closing? Relationship building? Foot in the door?)
- What's the sequencing of your ask? (Start with a small win or swing for the fences?)
- What's the fallback if they say no to the primary proposal?
- What's the long-game strategy for this account?

**Capture:** Document the pivot plan as a decision tree or if/then table.

---

## Consolidation & Output

After completing all five letters, consolidate everything into a structured output.
Always ask the user what format they prefer. Offer these options:

### Output Format Options

1. **CHAMP One-Pager** — A single-page executive summary covering all 5 letters.
   Dense, scannable, designed for sharing with stakeholders or pinning to a wall.
   Format as a polished markdown document. See `references/one-pager-template.md`.

2. **Detailed Brainstorm Report** — A comprehensive document expanding on every
   insight from the session. Includes the full reasoning, creative concepts,
   action plans, and pivot strategies. Good for PRD foundations or campaign briefs.
   Format as a structured markdown document with clear sections.

3. **PRD Draft** (Product mode only) — A product requirements document built from
   the brainstorming session. Includes: problem statement, target user, hypothesis,
   MVP scope, tech stack, success metrics, timeline, cost estimate, milestone plan,
   and pivot criteria. See `references/prd-template.md` for the template structure.

4. **Campaign Brief** (Campaign mode only) — A creative brief for the marketing team.
   Includes: objective, target audience with segments, creative concept, channel plan,
   personalization strategy, KPIs, budget allocation, timeline, and contingency plan.
   See `references/campaign-brief-template.md` for the template structure.

5. **Pitch Deck Outline** (Sales Pitch mode only) — A slide-by-slide outline for
   a customer proposal or sales deck. See `references/pitch-template.md` for structure.

The user can request multiple formats (e.g., "Give me the one-pager AND the full PRD").
Always generate the one-pager alongside any other format — it serves as the anchor summary.

When generating document outputs, use the docx skill if the user requests a Word document,
or produce clean, well-formatted markdown by default.

---

## Creative Provocation Techniques

Throughout the brainstorming session, employ these techniques to push thinking beyond the obvious:

- **Inversion**: "What if the opposite were true? What if customers actually WANTED the problem?"
- **Analogy Transfer**: "What industry has solved a similar problem? How did they do it?"
  (The blood drive example transferred sports tribalism to healthcare)
- **Constraint Injection**: "What if you had 1/10th the budget? What would you do differently?"
- **Audience Swap**: "What if your target were teenagers instead? Retirees? Dogs?"
- **Time Warp**: "What would this campaign look like in 2030? In 1995?"
- **Personalization Push**: "How could you make 100 versions of this, each tailored to a
  micro-segment? What data would you need?"
- **Competitor Steal**: "What's your competitor's biggest weakness that you can exploit
  in this campaign/product?"
- **Virality Test**: "Would someone screenshot this and share it? Why or why not?"

Use these sparingly and contextually — the goal is to spark unexpected connections,
not to run a checklist.

---

## Conversation Style

- Be a **creative collaborator**, not a questionnaire. Riff on the user's ideas, add unexpected
  angles, challenge weak spots, and celebrate strong insights.
- Use **vivid examples** to illustrate points. Reference real-world campaigns, products, and
  strategies to anchor abstract concepts.
- **Push back constructively** when ideas are too generic, too safe, or not grounded in customer
  reality. "That's a start, but who specifically are we talking about?" is better than
  accepting vague answers.
- Keep the energy **playful but rigorous**. This is brainstorming, not a board meeting —
  but every idea needs to survive scrutiny.
- **Summarize frequently**. After each CHAMP letter, recap what was captured before moving on.
  This prevents losing threads and gives the user a chance to correct or add.
- When the user provides an idea that's genuinely excellent, say so. Enthusiasm is fuel.

---

## Session Flow Summary

```
1. Greet & Set Context
   ↓
2. Detect Mode (Product / Campaign / Sales Pitch)
   ↓
3. Walk through C-H-A-M-P interactively (one letter at a time)
   ├── Ask probing questions
   ├── Offer creative provocations
   ├── Capture key insights
   └── Summarize before moving on
   ↓
4. Consolidation
   ├── Recap all 5 letters
   └── Ask: "What format do you want this in?"
   ↓
5. Generate Output(s)
   ├── Always: CHAMP One-Pager
   └── Optional: Detailed Report / PRD / Campaign Brief / Pitch Outline
   ↓
6. Review & Iterate
   └── "What would you change? Want to stress-test any section?"
```
