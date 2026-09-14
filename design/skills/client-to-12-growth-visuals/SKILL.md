---
name: client-to-12-growth-visuals
description: Turn a client/prospect website URL into 12 separate, premium, client-specific B2B visuals showing how LakeB2B data can support that company's growth. MANDATORY TRIGGER for "turn this website into 12 visuals", "create 12 B2B growth visuals for [URL]", "client website to growth visuals", "12-image LakeB2B data activation proposal", "analyze this company's ICP and generate campaign images", or any request combining a client website URL with a request for multiple sales/marketing visuals showing LakeB2B's value to that prospect. Produces an ICP brief first, then 12 individual 16:9 images (not a collage) via Higgsfield, covering email, social, AI telemarketing, SEO/AEO, recruiting, buying-committee mapping, data opportunity analysis, account org charts, AI/API data, a client-owned platform concept, webinars, and event/roundtable outreach.
---

# Client Website to 12 B2B Growth Visuals

Takes one client or prospect website URL and turns it into a researched ICP brief plus 12 separate, premium, on-brand B2B visuals showing how LakeB2B's data and intelligence can support that company's growth. This is a LakeB2B-branded sales-enablement asset generator, not a generic image tool: every visual is generated in LakeB2B's own visual system, sized for the client's ICP, and watermarked "Powered by LakeB2B."

## Primary input

Required: a client website URL (or, if the URL is unreachable, a confirmed company name from the user — see Step 1 below).

Optional, never block on these: target geography, priority product/service, target industry, known ICP, campaign objective, preferred image format/dimensions.

Default response when the user sends only a URL: state the plan in one line ("I'll analyze the company, identify its actual ICPs, and create 12 separate B2B growth visuals tailored to the business.") and go straight into research. Do not gate the first research pass on a clarifying question.

## Step 0: Connector preflight

Before researching or generating anything, confirm:
1. **Web research tools** (WebFetch/WebSearch or equivalent) are available — needed for Step 1.
2. **Image generation** (Higgsfield MCP or equivalent) is connected. If it is not connected or unauthenticated, stop before generating images, tell the user which connector needs authorizing and where, and offer to proceed with research + ICP brief only in the meantime. Never substitute a text description of what an image "would look like" for an actual generated image.
3. **LakeB2B brand guidelines** — check for a `lakeb2b-brand-guidelines` skill or equivalent brand doc in this session. If present, `Read` it before writing any generation prompts and use its actual colors/typography/logo rules rather than inventing a palette. If absent, ask the user for LakeB2B's brand colors once, or fall back to a reasonable premium purple/gold enterprise-data palette and say clearly that it's an assumption pending the real brand kit.

Report the preflight result in one line before starting research.

## Step 1: Website research

1. Try fetching the client's site directly (root domain, then `www.` and `http://` variants if the first attempt fails). If every direct-fetch attempt fails with SSL/robots errors (this happens — some client domains are unreachable to automated fetch), fall back to web search: search the bare domain in quotes, search "[domain] company", search likely business-description terms, and cross-reference LinkedIn/company-database snippets (ZoomInfo, Crunchbase, Dealroom, Wikipedia, the parent company's main site if one turns up). Do not give up after one failed fetch — try at least 2-3 different search angles before treating the company as unidentifiable.
2. If research keeps surfacing multiple distinct, unrelated companies with similar names (this happens with short/common brand words), do not guess. Use `AskUserQuestion` to present the plausible candidates found so far (with one-line descriptions of what each does) plus an "none of these, let me clarify" option, and let the user confirm. Record whichever caveat applies (e.g., "the root domain could not be independently verified; identity confirmed by the user") and carry it into the final ICP brief and into every generated visual's underlying research — this is a fact the user and their team need to see, not a detail to bury.
3. Once the company is identified, extract: correct legal/brand name, parent company and subsidiaries (distinguish them explicitly — never reuse a subsidiary's ICP for the parent or vice versa without evidence), products and services, industries served, customer use cases, geographic markets, likely target account types, likely buyer departments and job titles, competitors/market alternatives, and any relevant events/associations/communities.
4. Verify important claims through credible public sources (company's own site, Wikipedia, stock exchange filings if public, LinkedIn). Never invent customer names, data counts, campaign performance figures, or market statistics. Any quantity that isn't independently verified gets labeled **Illustrative**, **Estimated**, **Sample**, or **To be validated against LakeB2B data** — both in the ICP brief and inside the generated visuals themselves.
5. Never reuse an ICP, messaging angle, statistic, or visual concept from a previous client run in this or another session. Build fresh from what this website actually says.

## Step 2: ICP brief (present before generating anything)

Output, briefly, in prose or a short structured block:
- Client name
- Website
- Business summary
- Primary ICP(s)
- Secondary ICP(s)
- Target industries
- Target geographies
- Target company sizes
- Priority buyer roles/job titles
- Core business problems addressed
- Recommended campaign message (one line, framed as "LakeB2B data helps [Client] do X")
- Any assumptions requiring validation (domain-verification gaps, uncertain brand relationship, inferred buyer titles, etc.)

Then proceed directly to visual generation — do not wait for approval unless the user's request or session context signals they want to review the brief first.

## Step 3: The 12 visuals — shared visual system

Every image: 16:9 landscape, one dominant message, the client's name in bold text, LakeB2B's real brand colors and typography (from Step 0), a discreet "Powered by LakeB2B" watermark, realistic interface mockups/diagrams/dashboards rather than generic stock-photo layouts, and imagery that actually reflects the client's industry (an industrial/construction client gets steel-structure and factory motifs, not generic SaaS abstract shapes; a healthcare client gets clinical motifs; etc.). No client logo unless the user explicitly asks for one and a real logo asset is available (never let a generative model invent a client's logo — see the brand-accuracy rule in creative-generation references if this skill is paired with `prospect-creative-campaign-builder`). No fake testimonials, no fake customer logos, no invented statistics presented as fact, no claim that the client is attending/sponsoring a real event unless independently verified.

The 12 images, in order, each with its own single focus:

1. **Personalized email campaign** — headline "How [Client] Can Reach [Priority ICP] Through Personalized Email." Show: ICP tag, target job titles, target geography, an email client mockup with subject line + personalization fields ({{FirstName}} etc.) + CTA, and a workflow diagram "LakeB2B Verified Data → Personalized Email → Meeting Booked."
2. **LinkedIn/social outreach** — headline "Engage [Target Decision Makers] Across Social Channels." Show: LinkedIn connection request, LinkedIn follow-up message, a sponsored LinkedIn ad mockup, an audience-filter panel, and a multichannel sequence timeline. Only include a Meta/Facebook ad element if the ICP is actually plausible for Meta targeting (consumer-adjacent, not enterprise/industrial); otherwise omit it and don't force it in.
3. **AI-agent telemarketing** — headline "Turn Verified B2B Contacts into Qualified Conversations." Show: AI calling interface, a client-specific opening script line, qualification-question checklist, call-disposition chips, meeting-booking flow, human-handoff icon, and a compliance/opt-out badge.
4. **SEO and AEO visibility opportunity** — headline "Help [Client] Be Found Where Buyers Search and Ask AI." Show: an illustrative Google-style search-results mockup (explicitly labeled "Illustrative search visibility analysis," no real logos/brands), an illustrative AI-answer-engine mockup, a visibility-gap comparison chart against generic "Competitor A/B/C," and a recommended-content-themes panel.
5. **Talent acquisition / passive recruitment** — headline "Reach Specialist Talent Beyond Traditional Job Boards." Show: a hard-to-find role card relevant to the client's industry, a fictional passive-candidate profile card labeled "(fictional)," a personalized recruiting message mockup, a job-board-vs-passive comparison chart, skill/experience/geography filters, and a recruitment funnel.
6. **KOL and buying-committee identification** — headline "Map Every Stakeholder Influencing the Purchase." An org-chart/network diagram of roles tailored to the client's actual industry (economic buyer, technical buyer, business sponsor, procurement, operations, compliance/legal/InfoSec where relevant, internal champion, end users, external KOLs/consultants), connected by influence lines. Generic silhouette icons only, never real people.
7. **Data and industry opportunity analysis** — headline "Reveal Where [Client]'s Next Growth Opportunities Are Hiding." Show: a CRM/data-analysis dashboard with missing-data/duplicates indicator, a customer-concentration chart, a geography/industry distribution map, a lookalike-account panel, adjacent-sector suggestions, and a TAM/SAM/priority-account funnel — all figures explicitly labeled illustrative unless the user has supplied validated data.
8. **Company org charts and profiles** — headline "Understand Priority Accounts from the Inside Out." A sample target-account org chart clearly labeled "(fictional)," a fictional executive profile card (responsibility area, buying role, likely priorities), a personalized conversation-opener snippet, and a recommended outreach channel. Never use a real person's name or photo unless independently sourced and necessary — default to labeled fictional samples.
9. **B2B data powering LLMs and APIs** — headline "Power [Client]'s AI, CRM and Applications with B2B Intelligence." A system diagram: LakeB2B Data API at the center, connected to CRM enrichment, AI copilot, lead scoring, account recommendations, market intelligence; a natural-language query box with a sample structured response; a data-validation-layer badge.
10. **Client-owned industry platform** — headline "Build the Digital Platform That Connects [Client] to Its Market," platform name "[Client] Connect" or similar. Show a branded platform dashboard mockup with a nav bar drawing from: company directory, people profiles, supplier/partner discovery, AI-powered search, content hub, events, community, lead generation, premium intelligence, marketplace/subscription — pick whichever subset fits the client's business.
11. **Webinar invitation campaign** — headline "Fill [Client] Webinars with the Right Decision Makers." A sample webinar title relevant to the client's business, explicitly labeled "Sample Webinar" with a fictional future date, target ICP tag, personalized email + LinkedIn invitation mockups, a fictional speaker-panel concept, registration landing-page mockup, reminder-sequence timeline, and a post-webinar-to-sales-meeting funnel.
12. **Event networking / executive roundtable** — headline "Convert Industry Events into High-Value Executive Meetings." A generic, explicitly-labeled "Illustrative Event Concept" (never a real named event unless verified), an invitation-only roundtable/lunch concept with a limited-seats badge, target accounts/buyer roles, a personalized invitation mockup, a 1:1 meeting-scheduler mockup, a networking agenda, on-site lead-capture mockup, and a post-event funnel to partnership/pipeline outcomes.

## Step 4: Generation

Use the connected image-generation MCP (Higgsfield, if that's what's available in this environment). Practical pattern that has worked well:

- Model: a model tuned for text-rendering and diagrams (e.g. `nano_banana_pro`/`nano_banana_2`) — these visuals are text- and UI-mockup-heavy, not photoreal scenes, so a diagram/text-capable model matters more than a photoreal one.
- Aspect ratio `16:9`, resolution `2k` (or the model's equivalent "sharp, presentation-ready" tier).
- Preflight cost with `get_cost: true` on one representative prompt, and check balance before submitting a batch of 12.
- Submit all 12 as one batch call if the tool supports parallel batch submission (up to its per-call limit); otherwise submit in groups matching the platform's concurrency cap.
- Poll for completion in a loop until all jobs are terminal, then render/display the full set in one call rather than one-by-one.
- Each prompt should explicitly spell out: the LakeB2B color palette (or client-specific palette if this is being run for a different brand), the exact headline text, every UI element and label to include, "Powered by LakeB2B" placement, and instructions that all text must be crisp/correctly spelled/legible and that no real logos, real people, or fabricated-as-fact statistics should appear.

## Step 5: Deliver and verify

1. Download all 12 result images locally and verify byte counts (a corrupt/truncated download is usually a tiny file — re-fetch if any file looks suspiciously small).
2. Spot-check at least 2-3 images directly (open them) for: correct client name spelling, correct headline text, no fabricated real-looking stats presented without an "illustrative" label, no invented real-brand logos, and legible text overall. Regenerate any image that fails this check — misspelled names, wrong ICP, or unreadable text are not acceptable to ship.
3. Deliver all 12 as individual files via the file-delivery tool (never bundle them into one collage image unless the user explicitly asks for that as a *separate* follow-on deliverable).
4. If there's a durable project/knowledge base attached to this session, write a short summary doc there: client name, verification caveats, ICP summary, and what was delivered — so a future session doesn't have to redo the research.

## Step 6: Optional follow-ons

After delivering the 12, offer (don't build unprompted): a one-page summary collage, a PowerPoint deck, a PDF proposal, a short video storyboard, or a LinkedIn carousel adaptation of the same 12 concepts.

## Hard rules

- Never require the optional inputs (geography, product, industry, ICP, objective, format) before starting — infer reasonable defaults and label uncertain assumptions instead.
- Never reuse a prior client's ICP, messaging, or visual concepts.
- Never fabricate customer names, data counts, campaign performance numbers, or market statistics — label illustrative/estimated/sample/to-be-validated instead.
- Never claim the client is attending or sponsoring a real event unless verified.
- Never use a real person's name or photo in a sample profile — use clearly labeled fictional samples.
- Never use a client's logo without explicit user permission and a real logo asset.
- If the client's website can't be independently verified, say so plainly in the ICP brief and in any downstream document — this is a fact worth surfacing, not a detail to smooth over.
- Regenerate (don't ship) any visual with a misspelled company name, wrong ICP, or unreadable text.
