---
name: blog-enhancer
description: >
  Transforms text blogs into visual content experiences with branded infographics (Gemini gems/NotebookLM), interactive AI tools as lead magnets (Google AI Studio), and page design upgrades. Natural follow-up to b2b-blog-writer. MANDATORY TRIGGER for: "enhance blog", "blog infographic", "blog lead magnet", "beautify blog", "add visuals", "blog assets", "content magnet", "blog looks plain", "create a gem", "AI studio tool", "upgrade blog page", or after b2b-blog-writer completes. Also trigger for any published blog URL needing visual enrichment.
---

# Blog Enhancer

You are transforming a text-based B2B blog into a visually-rich content experience that drives engagement, social sharing, and lead capture. The input is a completed blog (either from the `b2b-blog-writer` skill or a published URL). The output is a suite of visual assets, interactive tools, and page design recommendations that make the blog impossible to ignore.

**The standard:** A reader should encounter at least one custom visual element every 300-400 words. The blog page should feel like a designed content experience, not a text wall with a header image. Think: HubSpot's pillar pages, Gong Labs' data-driven posts, Intercom's illustrated guides.

## Before You Start

1. **Check for the blog content.** Either:
   - The b2b-blog-writer skill just ran and the blog markdown is available in the workspace
   - The user has provided a blog URL to enhance
   - The user has pasted blog content directly
   If none of the above, ask the user for the blog content.

2. **Check if a brand skill is loaded** for the entity. You need brand colors, fonts, and visual identity to create on-brand assets. If no brand skill is loaded, ask which entity this is for.

3. **Read the visual content brief** if one exists (Phase 5 of b2b-blog-writer appends this as a comment block in the blog markdown). This brief identifies specific visual opportunities already. Use it as your starting point.

## The 4-Phase Workflow

---

### Phase 1: CONTENT ANALYSIS & VISUAL MAPPING

**Goal:** Identify every opportunity to replace text with visuals, embed interactive elements, or add shareable assets.

Read through the entire blog and create a visual opportunity map:

#### What to look for:

**Infographic Candidates** (highest impact)
- Named frameworks or methodologies (e.g., "The 3-Step AI Memory Audit")
- Process flows or step-by-step sequences
- Attack chains, workflows, or system diagrams
- Statistical findings with 3+ data points
- Before/after comparisons
- Comparison matrices or decision frameworks
- Timelines of events or research findings

**Data Visualization Candidates**
- Any cited statistics that are currently just text
- Percentages, growth figures, or trend data
- Survey results or research findings
- Industry benchmarks

**Interactive Tool Candidates** (lead magnet potential)
- Self-assessment opportunities ("Is your AI memory compromised?")
- Calculators or estimators ("Calculate your data decay rate")
- Diagnostic checklists ("Score your data hygiene in 60 seconds")
- Configurators ("Build your ideal data stack")

**Social Asset Candidates**
- The 2-3 boldest/most quotable statements
- Key statistics that stand alone
- Framework summaries that fit a single LinkedIn image
- Contrarian takes that would spark comment threads

#### Output of Phase 1:

A prioritized visual opportunity map with each item tagged:

```
[INFOGRAPHIC] The 3-Step AI Memory Audit — process flow showing Steps 1-3
  Priority: HIGH | Placement: After "The 3-Step Audit" section
  Social reuse: LinkedIn carousel, email header

[DATA VIZ] Microsoft research findings — 31 domains, 14 industries, 50+ patterns
  Priority: HIGH | Placement: After "What Microsoft Found" section
  Social reuse: Standalone stat card for X/LinkedIn

[INTERACTIVE] "Is Your AI Memory Compromised?" self-assessment quiz
  Priority: HIGH | Placement: Embedded after the audit section OR standalone landing page
  Lead magnet potential: Gate the detailed results behind email capture

[SOCIAL CARD] "Your AI's recommendations were bought. You just don't know it yet."
  Priority: MEDIUM | Placement: N/A (social distribution only)
```

Present this map to the user and confirm priorities before proceeding.

---

### Phase 2: INFOGRAPHIC CREATION PIPELINE

**Goal:** Create branded infographics that visualize the blog's key frameworks, data, and processes.

There are three production paths for infographics. Choose based on what the team has available:

#### Path A: Custom Gemini Gem (Recommended for teams producing regular content)

A custom Gemini gem is a branded AI assistant pre-loaded with the entity's brand book, color palette, fonts, and design guidelines. Once created, it produces on-brand infographics from simple text prompts, making it the fastest path for ongoing content.

**Setting up the gem (one-time):**

1. Go to Google AI Studio (aistudio.google.com) or Gemini (gemini.google.com/gems)
2. Create a new Gem with these instructions:

```
You are [Entity]'s branded infographic designer. Every visual you create must follow these brand guidelines:

COLORS:
- Primary: [hex from brand skill]
- Secondary: [hex from brand skill]
- Accent: [hex from brand skill]
- Background: [hex or white/dark from brand skill]
- Text: [hex from brand skill]

FONTS:
- Headlines: [font from brand skill]
- Body: [font from brand skill]

STYLE:
- Clean, modern B2B aesthetic
- Data-forward design (charts, icons, process flows)
- Minimal decoration, maximum information density
- Always include the entity logo and URL at the bottom
- Use icons instead of stock imagery

When given blog content or a framework, create an infographic that:
1. Captures the core concept in a single visual
2. Is readable at LinkedIn image dimensions (1200x627 or 1080x1080)
3. Uses the brand color palette exclusively
4. Includes a clear visual hierarchy (title > key insight > supporting data > CTA)
```

3. Upload the entity's brand book PDF as a knowledge source for the gem
4. Test with a sample prompt from the blog

**Using the gem for this blog:**

For each infographic identified in Phase 1, feed the gem a prompt:

```
Create an infographic for the following blog framework:

Title: [Framework Name]
Steps:
1. [Step 1 with key detail]
2. [Step 2 with key detail]
3. [Step 3 with key detail]

Key stat: [Most impactful number from this section]
CTA: [What the reader should do next]
Format: [1200x627 for blog embed / 1080x1080 for social / 1080x1920 for story]
```

#### Path B: NotebookLM (Quick and accessible, lower brand control)

Google NotebookLM can generate visual content summaries from source material. This is the fastest path when you need something now and brand precision is less critical.

**Process:**

1. Go to notebooklm.google.com
2. Create a new notebook
3. Upload the blog content as a source (paste the markdown or upload the file)
4. Also upload the entity's brand book as a second source
5. Use the "Briefing Doc" or content generation features to create visual summaries
6. Prompt NotebookLM: "Create a visual summary infographic of [specific section/framework] using the brand colors and style from the uploaded brand book"
7. For audio content: Use NotebookLM's Audio Overview feature to create a podcast-style discussion of the blog content (this becomes an additional content format for distribution)

**Limitations:** NotebookLM's visual output is less customizable than a dedicated Gemini gem. The output may need manual refinement in Canva or similar tools to match brand guidelines precisely.

#### Path C: Direct Creation (When AI image tools are available)

If the user has access to image generation tools (Canva AI, Adobe Firefly, DALL-E, or any tool connected via MCP), create the infographics directly:

1. Use the visual content brief from Phase 1 as the design spec
2. Apply brand colors, fonts, and style from the loaded brand skill
3. Generate in multiple formats: blog embed (1200x627), social square (1080x1080), story (1080x1920)

#### Output of Phase 2:

For each infographic:
- The asset itself (or detailed generation prompts for the user to run through their gem/tool)
- Placement instructions (exactly where in the blog HTML/markdown it should be inserted)
- Social distribution versions with suggested post copy
- File naming convention: `[entity]-[blog-slug]-[asset-type]-[number].[format]`

---

### Phase 3: INTERACTIVE TOOL CREATION (LEAD MAGNETS)

**Goal:** Build AI-powered interactive tools that serve as embedded lead magnets within the blog or as standalone landing page elements.

This is the highest-leverage enhancement. An interactive tool transforms a blog from "content someone reads once" into "a resource someone bookmarks, shares, and returns to." When gated (even partially), these tools capture leads that a plain blog never would.

#### Building Custom Tools with Google AI Studio

Google AI Studio lets you create custom AI-powered tools without code. These tools can be embedded in blog pages or deployed as standalone experiences.

**The process:**

1. **Go to Google AI Studio** (aistudio.google.com)
2. **Create a new prompt/chat** with system instructions tailored to the blog's topic
3. **Configure the system prompt** to create an interactive experience:

**Example: "AI Memory Audit Tool" for the recommendation poisoning blog:**

```
System Instruction:
You are an AI Memory Security Auditor. Your job is to walk users through checking
whether their AI assistant's memory has been compromised by prompt injection attacks.

Ask the user which AI assistant they use (ChatGPT, Copilot, Claude, Gemini).
Based on their answer, give them specific step-by-step instructions for:
1. Finding the memory/personalization settings
2. What to look for (suspicious entries mentioning specific vendors, "always recommend" language)
3. How to clear compromised entries
4. How to set up a monthly review process

After the walkthrough, provide a risk score (Low/Medium/High) based on what they found.
End by recommending they share this tool with their team and offering to email them
a PDF summary of the audit.

Tone: Helpful security expert. Not alarmist, but direct about the risks.
Speak in second person. Be specific about UI elements and menu paths.
```

4. **Test the tool** with a few interactions to verify it works
5. **Deploy options:**
   - **Embed in blog**: Use the AI Studio sharing features to get an embeddable URL or widget
   - **Standalone landing page**: Create a dedicated page for the tool with the blog as context
   - **Gated access**: Offer the basic tool for free, gate the detailed report/PDF behind email capture

#### Tool Ideas by Blog Type

Match the tool type to the blog's content:

| Blog Content | Tool Type | Lead Capture |
|---|---|---|
| Framework/methodology | Interactive walkthrough | Gate the personalized action plan |
| Data/research findings | Self-assessment quiz | Gate the detailed benchmark comparison |
| How-to/tutorial | Step-by-step configurator | Gate the custom implementation guide |
| Industry trends | Impact calculator | Gate the full report |
| Security/risk topic | Diagnostic checker | Gate the remediation playbook |

#### Multi-Channel Distribution

The tool isn't just a blog embed. It's a content asset that works across channels:

- **Blog embed**: The tool lives within the blog post, increasing time-on-page and engagement
- **Social teaser**: Post a screenshot of the tool's output with "Try it yourself: [link]"
- **Email nurture**: "We built a free [Tool Name] based on our latest research. Try it: [link]"
- **Sales enablement**: Reps can share the tool with prospects ("I thought this might be relevant to your team")
- **Webinar/event follow-up**: "Missed our session on [topic]? Here's the interactive tool we demoed: [link]"

#### Output of Phase 3:

For each interactive tool:
- Complete system prompt / configuration for Google AI Studio
- Embedding instructions for the blog page
- Gating strategy (what's free vs. what's behind email capture)
- Social distribution plan with suggested post copy
- Email nurture snippet for drip campaigns

---

### Phase 4: PAGE DESIGN RECOMMENDATIONS & DELIVERY

**Goal:** Provide actionable recommendations for transforming the blog page from a text template into a designed content experience, and deliver all assets.

#### Common Blog Page Problems (and fixes)

These are the patterns that make B2B blog pages feel like template filler:

**Problem: Floating/sticky sidebar forms**
Fix: Kill them. Replace with inline content gates at natural break points. Place a value-forward offer (checklist download, tool access, framework one-pager) at the point in the blog where the reader has received enough value to want more. This converts better and doesn't disrupt reading.

**Problem: No visual breaks in long text**
Fix: Insert a visual element every 300-400 words. Alternate between infographics, pull quote cards, data callout boxes with visual styling, and embedded interactive elements. The reader's eye should never face more than 3-4 paragraphs of unbroken text.

**Problem: Generic stock header image**
Fix: Replace with a custom branded hero that communicates the blog's specific concept. If the blog is about AI memory poisoning, the image should visualize that concept, not show a generic "person using laptop" stock photo.

**Problem: No reading progress indicator**
Fix: Add a sticky progress bar at the top of the page (many WordPress plugins and simple JS snippets can do this). This replaces the sticky form as the persistent page element and actually helps the reader.

**Problem: Flat text styling**
Fix: Use CSS-styled callout boxes for key takeaways, data points, and expert quotes. Use branded background colors for alternating sections. Add subtle borders or left-accent bars to blockquotes. These are pure CSS changes that any developer can implement in an hour.

**Problem: No social sharing integration within content**
Fix: Add "click to tweet/share" functionality on the strongest pull quotes. When a reader sees a bold statement they agree with, make it one click to share it with their network (with a link back to the blog).

**Problem: Weak or missing CTA architecture**
Fix: Use a three-tier CTA strategy:
1. **Soft CTA** (25% through): A relevant resource or tool mention, not gated
2. **Value CTA** (50% through): The interactive tool or lead magnet, lightly gated
3. **Direct CTA** (conclusion): The entity's core offer, positioned as the natural next step

#### Delivery Checklist

Package and deliver all assets to the user:

1. **Updated blog markdown** with visual placement markers showing where each asset goes
2. **Infographic assets** (or generation prompts for the user's gem/tool)
3. **Interactive tool configurations** (Google AI Studio system prompts, ready to deploy)
4. **Social distribution kit**: Pull quote cards, infographic social versions, suggested post copy for LinkedIn/X
5. **Page design recommendation document** with specific, implementable changes
6. **Email nurture snippets** that reference the blog and its interactive tools
7. **Gemini Gem setup instructions** (if the team doesn't have one yet) for ongoing infographic production

#### Output of Phase 4:

All deliverables saved to the user's workspace in an organized folder structure:

```
blog-enhancement-[slug]/
├── infographics/
│   ├── [entity]-[slug]-framework-infographic.md (or generation prompts)
│   ├── [entity]-[slug]-data-viz.md
│   └── social-versions/
├── interactive-tools/
│   ├── [tool-name]-system-prompt.md
│   └── embedding-instructions.md
├── social-kit/
│   ├── pull-quote-cards.md
│   └── suggested-posts.md
├── page-design/
│   └── recommendations.md
├── email-nurture/
│   └── snippets.md
└── blog-updated.md (with visual placement markers)
```

Tell the user: "Your blog enhancement kit is ready. The most impactful things to do first are: (1) set up the Gemini gem if you don't have one yet, (2) generate the infographics, and (3) deploy the interactive tool. The page design changes can happen in parallel."

---

## Important Reminders

- **Brand consistency is non-negotiable.** Every visual asset must use the entity's brand colors, fonts, and visual identity. If no brand skill is loaded, get the brand guidelines before creating any visuals.
- **Lead magnets must provide genuine value.** The interactive tool should be useful even without the entity's product. Readers who feel tricked by a gated tool that's just a sales pitch will never come back.
- **Social assets are not afterthoughts.** Every infographic and pull quote card should be designed to work as a standalone social post. This multiplies the blog's reach from 1 URL to 5-10 shareable assets.
- **The Gemini gem is the long game.** Helping the team set up a custom branded gem means every future blog gets infographics faster. Invest the time in the setup.
- **Interactive tools are the highest-leverage play.** A blog with an embedded AI-powered tool gets bookmarked, shared, and returned to. A blog without one gets read once and forgotten. Always push for at least one interactive element.
