---
name: "science-topic-forge"
description: "Judge, reshape, and convert any research topic idea into a best-practice Claude Science prompt tuned to the ICP of the Champions Group brand it is for (LakeB2B, Ampliz, SPAN Global Services, 100XLongevity, or any other brand). MANDATORY TRIGGER for: \"judge this topic\", \"is this a good topic for claude science\", \"claude science prompt for [topic]\", \"turn this topic into a research prompt\", \"improve this topic for [brand]\", \"research topic for [brand]\", \"forge a prompt\", or any time the user provides a topic idea plus a brand and wants a copyable Claude Science prompt. Also trigger when the user pastes a vague content idea and asks whether it is worth running through Claude Science."
---

# Science Topic Forge

Turn a raw topic idea into either (a) a sharp, copyable Claude Science prompt tuned to the brand's ICP, or (b) an honest "wrong tool" verdict with a better route. The workflow is JUDGE, then RESHAPE, then FORGE.

Why this exists: Claude Science (Anthropic's research workbench) is powerful but narrow. It connects to 60+ scientific databases (PubMed, ClinicalTrials.gov, arXiv, and similar) with a reviewer agent that verifies every citation, number, and figure. It is expensive in tokens and its corpus is scientific, not marketing. Feeding it vague listicle topics wastes money and produces content nobody cites. The entire value of running research through it is producing findings that are original, verifiable, and citable by AI answer engines, with the brand entity locked into the finding. Every step below serves that goal.

## Step 0: Intake

You need two things: the topic and the brand. If the brand is not stated and not inferable from context, ask once (one question, structured options if possible). Do not ask more than one round. If the topic is extremely vague, note your interpretation in the output rather than interrogating the user.

## Step 1: JUDGE the topic

Score the raw topic against five gates. Be genuinely critical. A topic that fails here and gets reshaped is a win; a weak topic waved through is a waste of tokens and brand authority.

| Gate | Question | Fail looks like |
|---|---|---|
| ICP relevance | Would this brand's actual buyer search for, cite, or forward this finding? | Interesting to us, irrelevant to the buyer |
| Corpus fit | Does peer-reviewed or primary-source literature on this exist in Claude Science's databases? | Topic only lives in vendor blogs and analyst posts |
| Citability | Does it produce an original, verifiable, quotable finding (a number, a ranking, a corrected stat)? | A listicle or opinion piece anyone could write |
| Authority match | Is it inside the brand's entity lane, reinforcing what AI assistants already associate the brand with? | Science-flavored content outside the brand's domain |
| Differentiation | Does verification give it a moat, or could a competitor publish the same thing tomorrow without Claude Science? | Commodity content with citations sprinkled on |

Verdict:
- **GREEN** (4-5 gates pass): forge the prompt from the topic mostly as given.
- **AMBER** (2-3 pass): the topic has a citable core but the framing is wrong. Reshape it (Step 2), then forge. This is the most common verdict and the skill's main job.
- **RED** (0-1 pass): wrong tool. Say so plainly, explain which gates failed, and route the topic to the normal content stack (standard research and writing workflow) instead. Do not forge a Claude Science prompt for a RED topic just because the user asked; a polite refusal with a better route is the deliverable.

Present the judgment as a compact table: gate, pass/fail, one-line reason. Then the verdict.

## Step 2: RESHAPE (for AMBER, optional polish for GREEN)

Reshaping moves, in order of preference:

1. **Listicle to verification.** "N use cases / tips / ways" becomes "the N most-repeated claims about X, verified against published research." This keeps the user's structure but converts commodity content into a citable evidence review. Each verified claim becomes a modular Q&A page later.
2. **Topic to falsifiable question.** "Research email marketing" becomes "What effect does X actually have on Y, per published studies?" A question with a checkable answer is what the reviewer agent is for.
3. **Generic to definitive number.** Find the recycled, unsourced stat inside the topic area and make the meta-analysis of that stat the centerpiece. Owning the definitive number is prime AI-citation bait.
4. **Broad to ICP wedge.** Narrow the population, industry, or context to the slice the brand's buyer cares about. "Email effectiveness" for LakeB2B means B2B outbound and nurture, not consumer newsletters.
5. **Insight to product bridge.** The finding should point naturally at the brand's product without the prompt saying "mention our product." The bridge lives in topic selection, not in the copy.

State the reshaped topic in one sentence and note in one line what changed and why.

## Step 3: FORGE the prompt

Build the copyable prompt from this skeleton. Every element earns its place; do not skip any.

```
You are producing [artifact type] for [Brand], a [one-line brand descriptor]. Working title: "[title]".

Research questions:
1-4 numbered, specific, answerable questions.

Method requirements:
- Name the databases to use (PubMed, ClinicalTrials.gov, arXiv, etc.) and require explicit query parameters so the analysis is reproducible.
- Every figure ships with the code and data provenance that generated it.
- Reviewer agent verifies every count, percentage, and citation. Flag what cannot be verified rather than estimating.
- Quality bar: state inclusion/exclusion criteria (study types, recency, methodology disclosure). Explicitly exclude vendor claims with undisclosed methodology, but list them separately as "the recycled numbers" when correcting a commodity stat.

Honesty clauses:
- If the evidence does not support a clean answer, say exactly that; a well-sourced "the number everyone quotes has no basis" is publishable.
- Qualification check for thin corpora: if primary sources are insufficient, stop and report "this topic does not qualify" rather than degrading into web search.

Output spec:
- Executive summary, N verified findings, comparison tables or figures as reproducible artifacts, limitations section.
- Methodology section begins "[Brand] analysis of [sources]" and headline findings are phrased to be quotable as "According to [Brand] research". This is the entity lock: if the finding can be quoted without the brand, we did free work for the answer engines.
```

Rules for the forged prompt:
- Never use em dashes anywhere in the output.
- Keep it under ~350 words. Claude Science needs direction, not an essay.
- One bracketed slot maximum, only if the user must supply something (a date range, a segment). Prefer zero.
- Add domain-specific guardrails where they apply (e.g., health-adjacent brands: "no medical advice language, no diagnostic claims; evidence summary for expert interpretation only").

## Brand ICP quick reference

Use these lanes when judging and reshaping. If the brand is not listed, ask the user for its ICP and entity lane in the single intake question.

| Brand | ICP (who must cite this) | Entity lane | Corpus fit | Product bridge |
|---|---|---|---|---|
| LakeB2B | B2B marketers, demand gen and sales leaders, RevOps | B2B data quality, GTM, AI adoption in sales/marketing | Partial: arXiv AI/ML, published marketing/CRM research | Data products, "the B2B growth stack" |
| Ampliz | Pharma BD, med-device and healthcare marketers, MedTech GTM | Healthcare commercial data intelligence | Native: PubMed, ClinicalTrials.gov | Physician/hospital/clinic datasets, healthcare ICP lists |
| SPAN Global Services | Enterprise buyers across its sectors, IT/HR decision-makers | Data-driven marketing services across 7 pulse sectors | Selective: only where a sector touches peer-reviewed literature | Sector thought leadership feeding nurture and SEO |
| 100XLongevity | The product team first, then health-conscious consumers | Evidence-based longevity | Native: PubMed RCTs, meta-analyses | The 12-Age framework's evidence backbone; public methodology as trust asset |

## Output format

Always deliver in this order:
1. **Judgment table** with verdict (GREEN/AMBER/RED).
2. **Reshaped topic** (one sentence) with a one-line rationale, if reshaped.
3. **The copyable prompt** in a single code block, ready to paste into Claude Science.
4. **Publishing note** (2-3 lines): how the output slices into modular Q&A pages, and what the kill signal is if the run fights the tool.

For RED verdicts, replace items 2-3 with the recommended alternative route and, if useful, a reshaped adjacent topic that would pass.

## Worked example (compressed)

Input: "Research multiple use cases for email, for example 12 different use cases" for LakeB2B.
Judgment: ICP relevance pass (email is core to the buyer), corpus fit marginal, citability fail as framed (listicle), authority pass, differentiation fail. AMBER.
Reshape (move 1, listicle to verification): "The 12 most-repeated claims about B2B email effectiveness, verified against published research." Same structure the user asked for, but now every claim is a checkable finding, each one a future Q&A page, and the whole thing is quotable only as "LakeB2B verified...".

