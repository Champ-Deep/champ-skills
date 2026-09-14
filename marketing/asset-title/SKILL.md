---
name: "asset-title"
description: "Generate high-converting, ICP-matched titles for any marketing or sales asset (case study, blog post, whitepaper, one-pager, report, deck, webinar, ebook). MANDATORY TRIGGER for: \"asset title\", \"title for this\", \"what should we call this\", \"name this case study/whitepaper/blog\", \"headline for this asset\", \"subject line for this content\", \"title suggestions\", \"rename this asset for [audience]\", or any time someone provides a link, file, or pasted content and wants a title, headline, or name for it before sending to prospects or clients. Works for any Champions Group brand (LakeB2B, SPAN Global Services, Ampliz, MetricFox, Recruit Champ, and others). Analyzes the actual content, confirms sender company and target ICP with the user, then produces scored, channel-ready title options."
---

# Asset Title Generator

Turn any piece of content into a title that a specific buyer actually wants to click. The title is the asset's first impression: most prospects decide from the title alone whether the asset is "for them". This skill exists because a generic title ("FinTech Case Study") wastes good content, while a matched title ("How a FinTech CMO 1.5x'd Campaign ROI by Enriching Data Before Launch") earns the click by promising a specific, provable outcome to a specific person.

The core principle, backed by CTR research: relevance beats cleverness. A title wins when it matches the reader's live problem, promises one concrete outcome, and is provable from the asset itself. Everything below serves that principle.

---

## Workflow Overview

1. Ingest the content (link, file, or pasted text)
2. Analyze it and build a Proof Inventory
3. Ask the user ONE batched round of questions (sender company, ICP, channel)
4. Confirm the strategic angle
5. Generate 8 to 10 titles across frameworks, score them, present the top picks
6. Iterate with the user until confirmed

Do not skip step 3. The same asset gets a different winning title for a FinTech CMO than for a Healthcare VP of Sales, and a different one from LakeB2B than from SPAN.

---

## Step 1: Ingest the Content

Accept any of these inputs:

| Input | How to read it |
|---|---|
| URL | Fetch the page. If the fetch returns a shell or partial content, use browser tools to get the full rendered text. |
| Attached file (PDF, docx, pptx, md, html) | Read it directly. Use the pdf/docx/pptx skills if extraction is needed. |
| Pasted text | Use as-is. |
| Vault path | Read from the vault. |

If the user gave nothing yet, ask for the content first. Never generate titles without reading the actual asset. Titles invented without the content produce unprovable promises, which is the one unforgivable failure mode of this skill.

## Step 2: Analyze and Build the Proof Inventory

Read the full asset and extract, in a compact internal table:

- **Asset type**: case study, blog, whitepaper, report, webinar, one-pager, deck
- **Quantified outcomes**: every number, percentage, multiplier, dollar figure, timeframe. These are title gold. Note exactly where each appears so the promise is provable.
- **Mechanisms**: the "how" behind each outcome (e.g., "enriched data before campaign launch", "added intent signals", "consolidated 3 vendors"). Mechanism is what makes a number believable instead of clickbait.
- **Named entities**: client names (and whether they are recognizable or anonymized), industries, roles mentioned
- **The unique angle**: what this asset says that a competitor's version of the same topic would not
- **Gaps**: if the asset has NO quantified outcome, flag it. You will pivot to mechanism, insight, or question framings, and you should tell the user which single stat would most strengthen the asset if they can add one.

## Step 3: One Batched Intake (AskUserQuestion)

Ask everything in ONE AskUserQuestion call, up to 4 questions. Pre-fill smart defaults from the content analysis (e.g., if the case study is about a FinTech client, the ICP industry option list should lead with FinTech).

1. **Sending company**: Which brand is this going out from? Offer the likely candidates: LakeB2B, SPAN Global Services, Ampliz, MetricFox, Recruit Champ, Champions Group, Other. If the content itself makes it obvious, put that first as "(Recommended)".
2. **Target ICP, role**: Who is this landing in front of? Offer role families relevant to the asset (e.g., CMO / VP Marketing, VP Sales / CRO, Ops / RevOps, HR / Talent, IT / Data leaders). Ask for seniority if ambiguous.
3. **Target ICP, industry/segment**: e.g., FinTech, Healthcare, SaaS, Manufacturing, Education, or "broad/multiple". If multiple, titles will be generated in an industry-neutral form plus one personalized variant.
4. **Channel**: Where does this title live? Options: Email subject line, LinkedIn ad/post, Landing page / asset cover, All of the above. Channel changes the length rules (Step 5), so this matters.

If the user already stated any of these in their message, do not re-ask. Only ask what is genuinely unknown. One round only: if something is still ambiguous after their answers, state your assumption and proceed.

## Step 4: Sender Company Context

The sending brand changes vocabulary, positioning, and what outcomes are credible to claim. Apply the matching context:

| Company | Positioning lens for titles | Brand skill to load if available |
|---|---|---|
| LakeB2B | "The B2B growth stack." Data-driven growth, enrichment, ABM, multi-channel. | lakeb2b-brand-guidelines |
| SPAN Global Services | Data-driven marketing services, demand gen, nurture. | (use champions-group-brand as fallback) |
| Ampliz | B2B and Healthcare data intelligence. Healthcare titles lean clinical-credible, compliance-aware. | ampliz-brand-guidelines |
| MetricFox | Marketing services / performance. | (fallback: champions-group-brand) |
| Recruit Champ | Talent and recruitment solutions. Titles speak to HR/TA leaders. | (fallback: champions-group-brand) |
| Champions Group / other ventures | Parent-brand executive tone. | champions-group-brand |

Hard rule (standing client-separation policy): clients work with LakeB2B OR SPAN Global Services, never both. If the asset mentions the other entity and the title/asset is going out under one of them, flag it to the user and keep the other brand out of the title entirely.

If a brand guidelines skill exists for the chosen company, load it before writing titles so vocabulary and tone match.

## Step 5: Channel Constraints

Titles must fit where they will actually be read. Generate to these limits:

| Channel | Limit | Rule |
|---|---|---|
| Email subject line | 25 to 50 characters ideal | Front-load the key noun/number in the first 30 characters; mobile clients truncate around 37 to 40. Cold outreach skews shorter (25 to 40). |
| LinkedIn sponsored headline | 50 to 60 chars, hard cap 70 | Anything past 70 is cut with no "see more". |
| LinkedIn lead gen form CTA headline | 30 characters | Ultra-compressed: outcome + audience only. |
| Landing page H1 / asset cover | Up to ~65 characters for full SERP display | Can add a subtitle line for the mechanism. |
| Deck/PDF cover title | Flexible | Pair a short main title with an outcome-bearing subtitle. |

When the user picked "All of the above", deliver the recommended title adapted per channel rather than forcing one string everywhere.

## Step 6: Generate Titles

Produce 8 to 10 candidates spanning these frameworks. Vary the frameworks; do not produce ten variations of one formula.

1. **Quantified Outcome**: How [ICP peer] achieved [one number] in [one timeframe]. One number, one timeframe, one customer. Example: "How a FinTech CMO 1.5x'd Campaign ROI in One Quarter"
2. **Mechanism Reveal**: Lead with the how, which builds credibility and curiosity together. Example: "The Pre-Launch Data Enrichment Step That 1.5x'd a FinTech Team's ROI"
3. **Peer Proof**: Name the client if recognizable and approved; otherwise name the segment. Example: "Inside [Client]'s Pipeline Turnaround: 3 Channels, 90 Days"
4. **Question They Are Already Asking**: Mirror the exact question the ICP types into Google or asks an AI assistant. Example: "Why Are Your Campaign CPLs Rising? A FinTech Data Audit"
5. **Contrarian / Myth-Bust**: Challenge a default belief the ICP holds. Example: "More Channels Won't Fix Your ROI. Cleaner Data Will."
6. **Cost of Inaction**: Quantify what doing nothing costs. Example: "The Hidden 23% Budget Leak in Unverified Contact Data"
7. **Playbook / Blueprint**: Promise a repeatable process. Example: "The 3-Step Enrichment Playbook Behind a 1.5x ROI Lift"
8. **Time-Bound Sprint**: Outcome inside a concrete window. Example: "90 Days to a Fuller Pipeline: A FinTech Growth Story"

### Non-negotiable quality rules

- **The Promise Check**: every claim in a title must be provable from the asset. If the asset says 47%, the title says 47%, not "nearly 50%" and never a rounder, sexier invented number. If a framework needs a stat the asset lacks, skip that framework.
- **Specific beats vague**: "1.5x campaign ROI" beats "better marketing results". Concrete nouns beat abstractions.
- **Plain language**: short words, no filler, no marketing jargon the ICP would not use themselves ("synergize", "leverage", "unlock" are out). If a technical term is essential to the ICP, keep it; jargon that signals insider fluency to that role is fine, generic buzzwords are not.
- **Reader-first framing**: the title promises what the READER gets, not what the sender did. "How to cut your CPL 30%" beats "How we cut a client's CPL 30%" for ads; the "How [peer] did X" form is for case studies where peer proof IS the value.
- **Never use em-dashes** in any title or output. Use colons, periods, or restructure.
- **No clickbait mechanics**: no withheld-noun curiosity gaps ("You won't believe what this CMO did"), no fake urgency. Curiosity should come from a specific, surprising fact, not from hiding information.

## Step 7: Score, Present, Confirm

Score each candidate 1 to 5 on five dimensions and present as a table:

| Dimension | What it measures |
|---|---|
| ICP Relevance | Would this exact role in this exact industry feel it was written for them? |
| Specificity | Concrete number, timeframe, or mechanism present? |
| Value Clarity | Is the reader's payoff obvious in under 3 seconds? |
| Provability | Is every claim backed inside the asset? |
| Channel Fit | Within length limits, key words front-loaded? |

Present the output in this structure:

1. **Recommended title** with a 2 to 3 sentence rationale tied to the ICP's likely pain and the asset's strongest proof point
2. **Channel adaptations** of the recommended title (subject line version, LinkedIn version, cover version) when relevant
3. **Full scored table** of all candidates so the team can pick a different angle
4. **Optional subtitle / supporting line** carrying the mechanism when the main title carries the number
5. **One improvement note**: if the asset itself could be strengthened (e.g., "adding a payback-period stat would unlock two stronger title angles"), say so in one line

Then confirm: ask if the recommended pick works or if they want a different angle pushed further (more contrarian, more conservative, different proof point). Iterate on request. Small iterations do not need a new intake round.

## Edge Cases

- **No metrics in the asset**: say so plainly, use frameworks 4, 5, and 7, and tell the user which single stat to add.
- **Anonymized client**: use segment descriptors ("a Series C FinTech", "a top-10 medical device maker"). Never fabricate a name; never de-anonymize without user confirmation.
- **Multiple ICPs**: produce one neutral base title plus one personalized variant per ICP, clearly labeled.
- **Asset going to an existing client vs. cold prospect**: cold titles need more context-setting; client-facing titles can reference the shared engagement. Ask only if the intake answers left this unclear.
- **Translation/localization requests**: keep the number and mechanism intact; adapt idioms, not the promise.
