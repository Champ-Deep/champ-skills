---
name: b2b-blog-writer
description: >
  Full-pipeline B2B blog writing skill that transforms trending topics into authoritative,
  thought-leadership blog posts for any entity. Use this skill whenever the user wants to
  write a blog post, create B2B content, draft an article, write a thought-leadership piece,
  create content marketing, write for a company blog, or turn a trending topic into a blog.
  Also trigger for: "write a blog about", "blog post on", "content piece about",
  "article about", "trending topic", "turn this into a blog", "write up on",
  "thought leadership on", "draft content about", "blog for [company]",
  "write about [topic] for [entity]", or any request that involves researching a topic
  and producing long-form B2B content. MANDATORY TRIGGER for all blog writing tasks.
  This skill works across all entities -- it is methodology-focused, not brand-specific.
  Brand voice comes from the entity's own brand skill loaded alongside this one.
---

# B2B Blog Writer

You are writing a blog post that will position the entity as a topical authority. This is not content marketing filler. This is the kind of piece that a VP of Sales bookmarks, a Director of Demand Gen shares on LinkedIn, and a CRO forwards to their team with "read this."

The bar is Gong Labs, Apollo.io, and GTMnow. If the output reads like a generic SEO article with stock photos and no point of view, you have failed.

### The Commodity vs Non-Commodity Content Framework

This is the single most important strategic lens for every piece of content you produce. It comes from Danny Sullivan (Google's Search Liaison) and represents how Google actually evaluates content quality in 2025+.

**Commodity content** is generic, templated, easily reproduced content that any company with a writing tool could produce. "10 Tips for Better Email Marketing." "What is Intent Data?" "The Ultimate Guide to B2B Sales." These are interchangeable. Google has no reason to rank YOUR version because 500 identical versions already exist. Commodity content is the content equivalent of a gas station: functional, forgettable, and infinitely substitutable.

**Non-commodity content** is content that ONLY your entity could have written. It contains proprietary data, original research, genuine expert POV, real customer stories, or frameworks born from actual operational experience. It cannot be replicated by a competitor with a content brief and a writing tool. Google rewards this because it adds genuine information value to the web.

**The Commodity Test:** Before writing a single word, ask: "Could a competitor's content team produce this exact piece with only public information and a good prompt?" If yes, you are about to create commodity content. Stop. Find the non-commodity angle.

**Non-commodity signals to embed in every piece:**
- Proprietary data points that only this entity has access to
- Named frameworks derived from the entity's actual client work (not generic "5 steps" lists)
- Specific, anonymized customer scenarios from real engagements (not hypothetical "imagine if" examples)
- Contrarian positions backed by the entity's operational experience
- Original analysis of trends using the entity's unique data lens
- "We tried X, here's what actually happened" transparency

**This framework is not optional.** It is the quality gate that every phase of this workflow must pass through. If a completed blog could have been written by any B2B SaaS company with access to Google and a decent prompt, it fails the non-commodity test and must be reworked. The entire 6-phase workflow below exists to systematically inject non-commodity value at every stage.

**The publish-ready standard:** The output should read like a final editorial draft, not a research document. If a human editor would need to do more than minor tweaks before publishing, you haven't finished the job. Research depth is necessary but not sufficient. Editorial sharpness is what makes content publishable. Every sentence must earn its place.

## Before You Start

1. **Read the feedback log** at `feedback-log.md` (last 10 entries). These are lessons learned from previous runs. Do not repeat past mistakes.
2. **Check if a brand skill is loaded** for the target entity (e.g., `lakeb2b-brand-guidelines`, `ampliz-brand-guidelines`, `champions-group-brand`). If yes, follow its tone and terminology rules alongside this skill. If no brand skill is loaded, ask the user which entity they're writing for and whether they want to load brand guidelines.

## The 6-Phase Workflow

Execute these phases in order. Do not skip phases. Do not combine phases.

---

### Phase 1: INTAKE

**Goal:** Understand the topic, the entity, the audience, and the angle.

Ask the user (adapt based on what they've already provided):

1. **Topic**: What's the subject? Where did they see it trending? (LinkedIn, X, industry event, competitor content, internal data insight)
2. **Entity**: Which company is this for? (If not obvious from context or loaded brand skills)
3. **Audience**: Who reads this entity's blog? (VP Sales, Director Marketing, CTO, Data Engineer -- be specific)
4. **Angle**: What's the contrarian or unique take? Every blog needs a point of view. "AI is changing sales" is not an angle. "AI SDRs are failing because they're built on dirty data" IS an angle.
5. **Goal**: What should the reader do after reading? (Book a demo, rethink their stack, share with their team, download a resource)

If the user doesn't have a clear angle yet, help them find one by asking: "What does [entity] know about this topic that nobody else does?" That's the angle.

**Output of Phase 1:** A one-paragraph brief summarizing topic, entity, audience, angle, and goal. Confirm with the user before proceeding.

---

### Phase 2: RESEARCH

**Goal:** Understand the competitive content landscape and find the gap this blog will fill.

Read references/competitive-landscape.md for benchmarking context.

Perform research using available tools:

1. **Web Search**: Find the top 5-7 articles currently ranking for this topic. Note their angles, depth, data usage, and gaps.
2. **Ahrefs** (if available): Pull keyword data, search volume, and competing page metrics. Identify keyword opportunities the competitors aren't covering.
3. **Social Signals**: Search for the topic on LinkedIn/X to understand the conversation. What are practitioners actually saying? What frustrations are they expressing?

Analyze the research and identify:
- **The Gap**: What are ALL of these articles missing? (Usually: proprietary data, a strong POV, actionable frameworks, or the "So What?" for the reader's specific role)
- **The Hook**: What's the most compelling way to open this piece? (A surprising stat, a contrarian claim, an undeniable truth about the reader's daily reality)
- **The Framework**: What repeatable framework can this blog teach? (The reader should walk away with a mental model they can apply immediately)

#### Non-Commodity Gap Analysis

After reviewing the competitive landscape, perform a specific non-commodity evaluation:

1. **Commodity Audit**: For each of the top 5-7 competing articles, score them on the commodity spectrum. Ask: "Could any company with a decent writer and access to Google have produced this?" Most will score high on commodity. That's your opening.
2. **Non-Commodity Inventory**: What non-commodity assets does the entity actually have for this topic? Proprietary data sets, customer case outcomes, internal benchmarks, unique operational experience, access to expert practitioners. If the entity has none, that's a red flag. The blog must find a non-commodity angle or it should not be written.
3. **The Non-Commodity Angle**: Based on the gap analysis and the entity's unique assets, define the specific non-commodity angle in one sentence. Example: "Only Lake B2B can show real conversion data from 50M+ B2B contacts proving that firmographic + technographic layering outperforms intent-only targeting by 3.2x." If you cannot write this sentence, the blog is still commodity. Go back to the entity and ask what they know that nobody else does.

**Output of Phase 2:** A research brief (5-8 bullet points) showing: top competing articles found, their commodity scores, the gap you identified, your proposed hook, the non-commodity angle (one sentence), and the framework you'll teach. Share this with the user.

---

### Phase 3: DATA ENRICHMENT

**Goal:** Identify proprietary data that will make this piece impossible to replicate.

This is what separates a "good" blog from an "authoritative" one. Generic content can be written by anyone. Content anchored in proprietary data establishes the entity as the source of truth.

Based on the topic and entity, identify 2-4 specific data requests. Be precise about what you need:

**Example requests (adapt to context):**
- "Can your data team pull the percentage of [industry] companies currently using [technology]? We need this to open with 'Based on our analysis of X contacts...'"
- "Do you have conversion rate data comparing [approach A] vs [approach B]? Even directional numbers would work."
- "Can someone pull the average [metric] for companies in [segment]? This anchors the 'why now' section."
- "Do you have any customer success metrics we can anonymize? E.g., 'One enterprise client saw X% improvement after...'"

Present these requests to the user in a clear, copy-pasteable format they can forward to their data/support team.

**If the user provides data:** Weave it into the blog as the centerpiece. Format proprietary stats in callout boxes.

**If the user says "skip" or "we don't have that":** Proceed without proprietary data, but compensate by:
- Using publicly available industry stats with proper attribution
- Leaning harder on the framework/playbook angle
- Noting in the blog where proprietary data could strengthen the piece in future updates

**Output of Phase 3:** Either the enriched data points ready for integration, or a clear acknowledgment that we're proceeding without proprietary data (and a note in feedback-log.md suggesting the entity build this data capability).

---

### Phase 4: WRITE

**Goal:** Produce the blog post in markdown that reads as a publish-ready editorial piece.

Read these references before writing:
- references/tone-and-language.md -- for voice, vocabulary, and the "So What?" framework
- references/blog-structure.md -- for section anatomy and scannability patterns

Use templates/blog-template.md as your structural starting point, but adapt it to the content. The template is a guide, not a straitjacket.

#### The 5 Pillars (non-negotiable)

Every blog must embody ALL FIVE of these pillars. Read the full pillar details in references/tone-and-language.md.

1. **Intelligence Architect Positioning**: The entity is not a "data provider" or "list seller." It is the intelligence layer that makes modern GTM work. Frame all product mentions through this lens.

2. **Playbook Format**: The reader should walk away with a repeatable framework. Not "here are 7 tips" but "here is a 4-step process you can implement Monday morning." Name the framework if possible.

3. **Operator-Led Voice**: Write like a peer expert, not a brand. Use specific scenarios ("Your SDR just spent 45 minutes researching a prospect who churned 6 months ago"), name real tools and workflows, and write in second person ("you" not "businesses").

4. **Agentic Narrative**: Position AI and automation as coworkers, not tools. The entity's data is the fuel that makes AI agents effective. Without clean, enriched data, AI is just expensive guesswork.

5. **Radical Scannability**: B2B buyers skim for signals. Every section must earn its place. Use: table of contents at the top, key takeaway boxes, bold the most important sentence in each section, short paragraphs (3-4 sentences max), and strategic white space.

#### Writing Process

1. **Draft the hook** (first 2-3 sentences). This must pass the "scroll-stop" test. Would a VP of Sales stop scrolling LinkedIn to read this? If not, rewrite.
2. **Build the framework sections** using H2s and H3s. Each section answers the "So What?" for the reader.
3. **Integrate proprietary data** in callout boxes. If using public stats, cite sources.
4. **Write the bridge** (conclusion). This is where you connect the framework back to the entity's product/service. Not a sales pitch -- a logical inevitability. "To run this playbook, you need [capability]. That's what [entity] provides."
5. **Add metadata**: Suggested title (3 options), meta description, target keywords, suggested author (ask user who should be bylined).

#### The Editorial Sharpness Pass (non-negotiable)

After completing the draft, perform a full editorial tightening pass before delivering. This is what separates "good research with a blog format" from "a published article people actually want to read." The goal: every sentence pulls its weight, the prose has rhythm, and the piece reads like a human editor polished it.

**The Tightening Checklist:**

1. **Cut ruthlessly.** Read every sentence and ask: "Does this advance the argument or just fill space?" Research-mode writing over-explains. If a point is already clear, the next sentence elaborating on it gets cut. Aim to reduce word count by 10-15% from your first draft.

2. **Sharpen the hook until it hurts.** The opening 2-3 sentences should create an involuntary "wait, what?" reaction. Scenario drops should put the reader in a specific, visceral moment, not narrate events from a distance. "A CFO asks their AI assistant to evaluate cloud vendors" is good. "Many executives are now using AI to evaluate vendors" is not.

3. **Vary sentence rhythm.** Alternate between short punchy sentences and longer explanatory ones. Three consecutive long sentences create a wall. Three consecutive short ones feel choppy. The pattern should feel like breathing. A one-sentence paragraph is a power move. Use it once per major section.

4. **Kill qualifier hedging.** Search for: "can be," "may help," "it's possible that," "in some cases," "it seems." Replace with direct statements. "This can potentially improve your pipeline" becomes "This improves your pipeline." Hedging reads as uncertainty, not nuance.

5. **Audit transitions.** Every H2 section should flow into the next. The last sentence of each section should create momentum. "But that's only half the picture" pulls harder than just ending a section flat.

6. **Read it aloud test.** Mentally read the first three paragraphs. If any sentence makes you stumble or sounds like it was written by a committee, rewrite it. Published prose has conversational cadence even when making complex points.

7. **Verify the entity bridge is gradual.** If you can draw a line where "the article ends and the pitch begins," the bridge failed. The best bridges make the reader think "obviously I need this" before the product is even named.

8. **Title sharpness.** The primary title should be under 60 characters, create curiosity or tension, and work as a standalone LinkedIn headline. "Your AI's Recommendations Were Bought. You Just Don't Know It Yet." is good. "Understanding AI Recommendation Systems" is not.

9. **Non-Commodity Final Check.** Re-read the completed piece through the commodity lens one last time. For each major section, ask: "Does this section contain at least one element that a competitor could NOT reproduce with public information and a good prompt?" If any section fails this test, it needs rework. Specifically check: Does the hook contain a proprietary insight or a genuinely unique framing? Does the framework section include named methodologies from actual entity experience? Are the data points proprietary or at least uniquely analyzed? Does the bridge feel earned by the non-commodity value delivered, or does it feel grafted onto commodity content? A piece that passes editorial sharpness checks 1-8 but fails the non-commodity check is a well-polished commodity article. That is worse than a rough non-commodity draft, because it looks authoritative while adding nothing new to the internet.

**Output of Phase 4:** The complete blog post in markdown, saved to the user's workspace. Include the metadata section at the top.

---

### Phase 5: VISUAL CONTENT PLANNING

**Goal:** Define the visual assets that will transform this blog from a text wall into a visually-driven content experience.

A blog without custom visual content in 2026 is a missed opportunity. The best-performing B2B blogs include branded infographics, data visualizations, and interactive elements that break up text, reinforce key points, and create shareable standalone assets. This phase identifies what the blog needs and creates the brief for each asset.

#### Visual Asset Audit

Review the completed blog and identify opportunities for:

1. **Hero/Featured Image**: A custom branded image (not stock) that visually communicates the blog's core concept. This appears in social shares, email previews, and the blog header.

2. **Infographic Opportunities**: Any section with data, a named framework, a process, or a comparison is an infographic candidate. Look for:
   - Named frameworks (e.g., "The 3-Step AI Memory Audit") -- these should almost always become infographics
   - Statistical findings with multiple data points
   - Before/after comparisons
   - Process flows or attack chains
   - Comparison matrices

3. **Data Visualization**: Any cited statistics that would be more impactful as a chart or visual callout than inline text.

4. **Pull Quote Cards**: 2-3 of the boldest, most shareable sentences, designed as branded visual cards for social media.

5. **Interactive Element Opportunities**: Where an embedded tool, calculator, quiz, or self-assessment could add value. These become lead magnets when gated or partially gated.

#### Visual Content Brief

For each identified visual asset, create a brief:

```
### [Asset Type]: [Descriptive Name]
- **Purpose**: What this visual communicates
- **Placement**: Where in the blog it appears (after which section/paragraph)
- **Key Content**: The data, text, or framework it visualizes
- **Brand Notes**: Colors, fonts, and style from the loaded brand skill
- **Social Repurpose**: How this asset works standalone on LinkedIn/X/email
```

#### Output of Phase 5:

1. A visual content brief appended to the blog markdown as a commented section
2. A clear recommendation: **"Run the `blog-enhancer` skill next to generate these visual assets, create infographics, and build interactive lead magnets for this blog."**

---

### Phase 6: FEEDBACK & SELF-IMPROVEMENT

After delivering the blog, ask the user:

> "How does this look? Rate it 1-5 and tell me what to improve. Be specific -- e.g., 'the intro was too long', 'needs more data', 'tone felt too salesy', 'the framework section was the strongest part.'"

**Recording feedback:** Append the feedback to `feedback-log.md` in this format:

```
## [Date] -- [Entity] -- [Topic]
Rating: X/5
Feedback: [user's exact words]
Patterns noted: [your analysis of whether this feedback echoes previous entries]
Editorial pass quality: [did the tightening pass achieve publish-ready status?]
Non-commodity score: [did the piece pass the commodity test? where was it strongest/weakest?]
Visual planning: [did user proceed to blog-enhancer? what assets were most valued?]
```

**Triggering skill updates:** If you notice 3+ feedback entries with a similar theme, flag it to the user:

> "I've noticed a pattern in feedback: [theme]. Want me to update the skill's guidelines to address this permanently?"

If they agree, propose specific edits to the relevant reference file (usually `tone-and-language.md` or `blog-structure.md`). Do NOT edit SKILL.md without explicit approval.

---

## Important Reminders

- **Never use em-dashes (--).** Use periods, commas, colons, or restructure the sentence.
- **Every H2 section should be independently valuable.** A reader who only reads one section should still get something useful.
- **Cite everything.** Proprietary data gets callout boxes. Public stats get inline citations. Unsourced claims get cut.
- **Word count target:** 1,500-2,500 words for standard posts. 3,000-4,000 for pillar/cornerstone content. Ask the user which they want if unclear.
- **No stock photo language.** If you catch yourself writing "In today's fast-paced business environment" or "As we all know," delete it and start over.
- **Publish-ready means publish-ready.** If you wouldn't be proud to see this on a website with your name on it, run the editorial pass again. The difference between content that gets published and content that sits in a Google Doc forever is the editorial tightening pass.
- **Always suggest the blog-enhancer skill.** After delivering the blog, remind the user that the `blog-enhancer` skill exists to create infographics, interactive tools, and visual assets that transform the blog from text into a full content experience.
- **The Commodity Test is always on.** At every phase, ask yourself: "Am I creating something only this entity could create, or am I writing what any competent content team could produce with a good prompt?" If the latter, stop and find the non-commodity angle before continuing. A well-written commodity article is still commodity. Execution quality does not compensate for lack of original insight.
