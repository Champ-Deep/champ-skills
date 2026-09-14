---
name: b2b-visuals-to-deck
description: "Client Website to 12 B2B Growth Visuals, combined into a PowerPoint deck"
---

# Client Website to 12 B2B Growth Visuals — Combined into a PowerPoint Deck

When the user provides a client/prospect website URL (optionally with a request for "a deck", "PPT", "PowerPoint", or "combine into slides"), research the company, produce 12 separate B2B growth visuals showing how LakeB2B data can support its growth, and assemble all 12 into a single, presentation-ready `.pptx` file. This skill is the vk-b2b-visuals / client-to-12-growth-visuals pipeline plus a mandatory deck-assembly stage — use it whenever the user wants the 12 visuals delivered as one file rather than (or in addition to) 12 separate images.

## Primary input
Required:
- Client website URL

Optional:
- Target geography
- Priority product or service
- Target industry
- Known ideal customer profile
- Campaign objective
- Preferred image format or dimensions

Do not require optional information before starting. Infer reasonable inputs from the website and clearly label uncertain assumptions.

## Step 0 — Compliance / sensitivity check

Before doing any research, sanity-check the target domain. If it clearly belongs to a government entity, a state-owned company in a sanctioned or heavily restricted sector (defense, nuclear, sanctioned-jurisdiction energy/finance), or otherwise looks like a high-risk account for a Western B2B data vendor to prospect, pause and flag this to the user explicitly before generating a full sales campaign against it. Use AskUserQuestion with options like "Proceed anyway", "Research only, pause before visuals", and "Wrong link — let me swap it". Note the compliance concern in the ICP brief regardless of the answer. Skip this step for ordinary commercial websites — it exists for the edge cases, not as a default gate.

## Mandatory website research

Before creating visuals:
1. Browse the client's official website (WebFetch the homepage and an "about"/English-language page if the primary site isn't English).
2. Identify:
   - Correct company name
   - Parent company and subsidiaries
   - Products and services
   - Industries served
   - Customer use cases
   - Geographic markets
   - Likely target account types
   - Likely buyer departments and job titles
   - Competitors and market alternatives
   - Relevant events, associations and industry communities
   - Brand colors (read from visible site styling; note as illustrative if not explicit)
3. Distinguish the client from its subsidiaries, parent company and affiliated brands.
4. Build the ICP from the website being analyzed.
5. Never reuse the ICP, messaging, statistics or visual concepts created for a previous client.
6. Verify important claims through credible public sources (WebSearch) when the website alone is thin.
7. Do not invent customer names, data counts, campaign performance or market statistics.
8. Mark unverified quantities as: Illustrative / Estimated / Sample / To be validated against LakeB2B data.

## ICP output before visual generation

Present briefly (as chat text, not a file yet):
- Client name
- Website
- Business summary
- Primary ICPs
- Secondary ICPs
- Target industries
- Target geographies
- Target company sizes
- Priority buyer roles
- Core business problems addressed
- Recommended campaign message
- Brand colors identified
- Any assumptions requiring validation

Then proceed directly to visual creation — do not wait for approval unless Step 0 flagged a compliance concern the user hasn't resolved yet.

## Required output: 12 individual visuals, then combined into one deck

Generate 12 individual 16:9 images via the image-generation tool available in this environment (e.g. Higgsfield `generate_image_batch` with `nano_banana_pro` or an equivalent text-and-diagram-capable model, resolution `2k`, `aspect_ratio: "16:9"`). Submit all 12 as one batch call, then poll with the batch tool's wait/status call until every job is terminal, retrying any individual failure once before giving up on it.

Each image must:
- Focus on one use case only
- Use the client's actual ICP
- Use the client name in bold text
- Avoid the client logo unless the user explicitly requests logo use
- Follow a consistent premium visual system (same palette, same type treatment) across all 12
- Reflect the client's industry and website brand colors
- Include realistic interface mock-ups, diagrams, campaign examples or dashboards
- Use concise, readable text
- Show the connection between LakeB2B data and the client's commercial objective
- Include "Powered by LakeB2B" discreetly
- Be suitable for presentations, LinkedIn and executive sales proposals
- Use landscape 16:9 composition
- Avoid excessive text, tiny labels and generic stock-style layouts

### The 12 images

1. **Personalized email campaign** — target ICP, job titles, geography, personalized subject line, email copy, personalization fields, CTA, data-to-meeting workflow. Headline: "How [Client Name] Can Reach [Priority ICP] Through Personalized Email"
2. **LinkedIn and social outreach** — connection request, follow-up message, sponsored LinkedIn ad, optional Meta ad (only if ICP suits Meta), audience filters, multichannel sequence. Headline: "Engage [Target Decision Makers] Across Social Channels"
3. **AI-agent telemarketing** — calling interface, opening script, qualification questions, call dispositions, meeting-booking flow, human handoff, compliance/opt-out handling. Headline: "Turn Verified B2B Contacts into Qualified Conversations"
4. **SEO and AEO visibility opportunity** — buyer search query, search-results mock-up, AI-answer-engine mock-up, competitor visibility, client visibility gap, recommended content themes. Label generated interfaces "Illustrative search visibility analysis." Never fabricate a real screenshot. Headline: "Help [Client Name] Be Found Where Buyers Search and Ask AI"
5. **Talent acquisition and passive recruitment** — hard-to-find role, passive-candidate profile (fictional, no real photo), personalized recruiting message, job-board vs. passive comparison, filters, recruitment funnel. Headline: "Reach Specialist Talent Beyond Traditional Job Boards"
6. **KOL and buying-committee identification** — economic buyer, technical buyer, business sponsor, procurement, operations, legal/compliance/infosec where relevant, internal champion, end users, external KOLs/consultants/analysts, influence relationships tailored to the client's industry. Headline: "Map Every Stakeholder Influencing the Purchase"
7. **Data and industry opportunity analysis** — CRM/file analysis, missing data & duplicates, customer concentration, industry/geography distribution, lookalike accounts, adjacent sectors, white-space markets, cross-sell opportunities, TAM/SAM/priority-account universe. Use illustrative figures unless real data is available. Headline: "Reveal Where [Client Name]'s Next Growth Opportunities Are Hiding"
8. **Company org charts and profiles** — sample target-account org chart, departments, buyer hierarchy, executive profile (fictional, clearly labeled sample — no real name/photo), responsibility area, buying role, personalized conversation opener, recommended outreach channel. Headline: "Understand Priority Accounts from the Inside Out"
9. **B2B data powering LLMs and APIs** — LakeB2B data API, CRM enrichment, AI copilot, lead scoring, account recommendations, market intelligence, natural-language queries, sample structured response, data-validation layer, client applications. Headline: "Power [Client Name]'s AI, CRM and Applications with B2B Intelligence"
10. **Client-owned industry platform** — branded platform concept ("[Client Name] Connect" or similar) with directory, people profiles, supplier/partner discovery, AI search, content hub, events, community, lead gen, premium intelligence, marketplace, subscription/sponsorship. Headline: "Build the Digital Platform That Connects [Client Name] to Its Market"
11. **Webinar invitation campaign** — webinar title, target ICP, personalized email invite, LinkedIn invite, speaker/panel concept, registration landing page, reminder sequence, attendee qualification, post-webinar conversion. Use a fictional future date, label "Sample webinar." Headline: "Fill Client Webinars with the Right Decision Makers"
12. **Event networking, roundtable or executive lunch** — relevant industry event type, invitation-only executive lunch/dinner/roundtable, target accounts and buyer roles, personalized invitation, limited-seat positioning, meeting scheduler, networking agenda, on-site lead capture, post-event follow-up. Never state the client is attending or sponsoring a real named event unless verified. Headline: "Convert Industry Events into High-Value Executive Meetings"

### Visual quality requirements

Use: premium corporate design, strong hierarchy, large readable headlines, high-quality industry imagery, realistic interface mock-ups, data visualization, clear buyer personas, consistent typography and spacing, client-specific colors derived from its website, one dominant message per image.

Avoid: 12-panel collages instead of individual images, unreadably small text, repetitive layouts, random numbers, fake testimonials, fake customer logos, unverified claims, carrying over a previous client's ICP, using subsidiary ICPs for the parent company without evidence, logos without permission, generic imagery that doesn't match the client's industry.

After generation, verify: correct client name and ICP appear in every visual, no misspellings, no unreadable text. Regenerate any image that fails this check before moving on.

## Mandatory final stage: combine into a PowerPoint deck

This is what distinguishes this skill from the plain 12-images workflow — always finish by assembling the 12 visuals into one `.pptx` deliverable, not just displaying 12 separate images.

1. Download all 12 generated image URLs into a working directory (`curl -sL -o imgNN.png <url>`, zero-padded 01–12).
2. **Compress before embedding.** Full-resolution 2K PNGs from image-gen tools commonly run 4–6 MB each; 12 of them will blow past typical upload size limits (~30 MB). Convert every image to JPEG at roughly 1920×1080, quality ~80–85, e.g.:
   ```
   convert imgNN.png -quality 82 -resize 1920x1080 jpg/imgNN.jpg
   ```
   This typically brings a 12-image deck from 60+ MB down to 2–4 MB with no visible quality loss at presentation size. Confirm this stayed under budget with `du -sh` before moving on; tighten quality/resolution further only if still oversized.
3. Read the `pptx` skill's SKILL.md before building (it is a separate skill in this environment — invoke it via the Skill tool) and follow its `pptxgenjs` gotchas (set `pres.layout` before adding slides; hex colors with no `#`; one `new pptxgen()` per file; etc).
4. Build the deck with `pptxgenjs`:
   - `LAYOUT_WIDE` (13.333" × 7.5") so 16:9 images fill the slide edge-to-edge with no letterboxing.
   - **Title slide**: client name, "N B2B Growth Visuals for [Client]", website, one-line note that figures are illustrative pending validation against live LakeB2B data. Dark background (e.g. charcoal) for contrast with a light title slide → content → dark closing "sandwich" structure, using the client's accent color as the sole accent.
   - **12 image slides**: one full-bleed image per slide (`x:0, y:0, w:13.333, h:7.5`), each with a small, unobtrusive page-number chip (e.g. "3/12") in a bottom corner using the client's accent color — do not add any other decoration on top of the visuals, they are already fully designed.
   - **Closing "Next Steps" slide**: 3–5 numbered action items (e.g. validate ICP/figures against real data, confirm any compliance clearance needed, pick 2–3 pilot channels, build a sample account list), "Powered by LakeB2B" footer.
5. Validate: `python scripts/office/validate.py deck.pptx` (from the pptx skill's `scripts/` directory) must pass before delivery.
6. Content QA: `markitdown deck.pptx` — confirm all 14 slides present, headlines match, no placeholder text.
7. Visual QA: convert to images via the pptx skill's `soffice.py` + `pdftoppm` recipe and actually look at the title slide, the closing slide, and at least 2–3 of the image slides at full resolution to confirm no cropping, no letterboxing, legible chip placement, and image quality holding up after compression.
8. Deliver the `.pptx` with SendUserFile. If it still exceeds the upload limit, compress further (lower JPEG quality or resolution) and rebuild rather than sending a broken/oversized file.

## Save to project (when session is project-attached)

Write the ICP brief (business summary, ICPs, target geos/roles, recommended message, brand colors, assumptions, any compliance flag from Step 0) to the project as a markdown doc, e.g. `claude/[client-slug]-icp-brief.md`, so the research persists independent of the deck file.

## Default user experience

When the user sends only a URL, respond: "I'll analyze the company, identify its actual ideal customer profiles, create 12 separate B2B growth visuals tailored to the business, and combine them into a single PowerPoint deck." Then begin research without asking unnecessary questions (aside from the Step 0 compliance check, when applicable).

## After delivery

Optionally offer further formats: a one-page summary collage, a PDF proposal, a short video storyboard, or a LinkedIn carousel adaptation of the same 12 concepts.
