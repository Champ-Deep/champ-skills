---
name: meeting-growth-visuals
description: "Formerly vk-b2b-visuals. From a client website URL and the context of a named meeting, research the client and build 12 separate, client-specific 16:9 visuals showing how a Champions Group brand (LakeB2B, CIPL, Ampliz or Champions Infratech) drives the client's real commercial goal, plus a live-meeting showing order. Use when the user names a meeting or wants standalone images rather than a deck."
---

# Meeting Growth Visuals: client website to 12 meeting-ready visuals

When the user provides a client website URL and a meeting (a date, a name, or "we are seeing them on Thursday"), research the client and create 12 separate, client-specific visuals that show how the chosen Champions Group brand supports the client's actual commercial objective. Ship them with a showing order for the meeting.

> Overlap note: `b2b-growth-showcase` also produces 12 images and a deck and is the default when no meeting is named. Use this skill when the user asks for it by name (including "VK visuals"), names a meeting, or wants standalone images with a showing order. If both would apply, ask once which one.

## Primary input
Required:
- Client website URL

Optional (infer if missing, label assumptions):
- The meeting: who, when, what they asked for
- Champions Group brand to present as (default LakeB2B; CIPL for an Indian client buying data and marketing; Ampliz for healthcare data; Champions Infratech for a developer, landowner or hospitality client)
- Target geography
- Priority product or service
- Target industry
- Known ICP
- Campaign objective
- Preferred dimensions (default 1600x900, exported at 2x)
- Brand look: client look (default), Champions brand look, or neutral

## Step 0: Pull meeting context first
Before researching the website, search email, calendar, Zoom, Notion, Drive and the Celsus vault (`Atlas/Clients`, `Calendar/Meetings`, any marketing audit or meeting prep for this client) for the client name and contacts. Extract:
- What the client said they want, in their words
- Confirmed numbers already shared with them (counts, TAM, ranges). These may be used and labeled "Confirmed [month year]".
- Objections and requests from past calls. At least one visual must answer each request directly.
- Open decisions (sender identity, scope, pricing). Reflect them as "to confirm" labels, never as settled facts.
- If a marketing audit exists for the client, reuse its ICP, channel findings and confirmed figures rather than re-researching.

## Step 1: Pick the brand, detect the client's real objective, then remap
The 12 use cases were written for LakeB2B presenting to a client that sells to businesses. Many clients want something else. Identify the objective from the website plus meeting context, then remap every image before building.

| Objective | Who the "buyer" in each visual becomes | Example remaps |
|---|---|---|
| Sell to businesses (default) | Target accounts and buying committee | Use the use cases as written |
| M&A or practice acquisition | Owners of target companies and their advisors | Buying committee becomes decision unit (owner, partners, CPA, attorney, family). Data analysis becomes deal universe. Webinar and event become owner-options sessions. Platform becomes an owner-facing partnership site. |
| Recruiting | Passive candidates | Email and social become candidate outreach. Org chart becomes team maps at source companies. |
| Partnerships or channel | Partner companies | Buying committee becomes partner decision makers. |
| Real estate developer selling homes (LakeB2B or CIPL as the brand) | HNI and NRI homebuyers, upgraders, channel partners | Email and social become pre-launch audience programmes. Buying committee becomes the household decision unit (buyer, spouse, parents, NRI relative, channel partner). Data analysis becomes launch demand sizing by micro-market and diaspora city. Org chart becomes channel partner tiering. Webinar becomes an NRI launch preview. Event becomes a sales gallery or roadshow evening. |
| Real estate developer, land or hospitality client (Champions Infratech as the brand) | The developer's buyers and the developer's board | Replace the data stack with the Infratech stack: waterfront masterplan on the client's parcel, senior living and longevity concept, wellness and hospitality layers, sustainability and water metrics, NRI and HNI demand, channel partner activation, launch absorption case. Keep the Infratech claim boundaries: no uplift percentages, lagoon costs, IRRs or completed-project counts unless the user supplies approved figures. |

State the chosen brand, the detected objective and the remap in the ICP brief. If the objective is ambiguous, pick the most likely one, say so, and continue.

## Mandatory website research
1. Browse the client's official website. Capture brand colors and fonts from computed styles, plus one screenshot.
2. Identify: correct company name, parent and subsidiaries, products and services, industries served, use cases, geographies, likely target account types, buyer roles, competitors and alternatives, relevant events and associations.
3. Distinguish the client from subsidiaries, parent and affiliates.
4. Build the ICP from this website and this client's meetings only. Never reuse a previous client's ICP, copy, statistics or concepts.
5. Verify important claims through credible public sources.
6. Never invent customer names, data counts, campaign performance or market statistics.
7. Label every number with one tag: Confirmed, Illustrative, Estimated, Sample, or To be validated.

## ICP brief (send before building)
Send briefly: client name, website, business summary, brand chosen, detected objective and remap, primary and secondary ICPs, industries, geographies, company sizes, priority roles, core problems, recommended campaign message, the meeting requests each visual will answer, and assumptions to validate. Then proceed without waiting.

# Required output: 12 separate images
Each image must:
- Focus on one use case
- Use the client's actual ICP under the detected objective
- Show the client name in bold in the eyebrow on every image, and in the headline where natural
- Avoid the client logo unless the user explicitly allows it
- Follow one consistent visual system across all 12, with varied layouts
- Use the client's website colors and font by default
- Include realistic interface mock-ups, diagrams, campaign examples or dashboards
- Use concise, readable text (body text no smaller than 13px at 1600 wide)
- Connect the chosen brand's offer to the client's objective
- Include "Powered by [brand]" discreetly (LakeB2B, CIPL, Ampliz or Champions Infratech)
- Carry a footer note stating what is confirmed, sample or illustrative

## The 12 use cases
Adapt headlines to the remap. Headline templates below are for the default objective.

1. **Personalized email.** ICP, titles, geography, subject, client-specific copy, personalization fields, CTA, workflow from data to meetings. "How [Client] Can Reach [ICP] Through Personalized Email"
2. **LinkedIn and social.** Connection request, follow-up message, sponsored ad, audience filters, sequence. Include Meta only when the ICP can be targeted there, and say why when excluded. "Engage [Decision Makers] Across Social Channels"
3. **AI agent calling.** Calling interface, opening script, qualification questions, dispositions, booking flow, human handoff, compliance (DNC and TCPA scrub, AI disclosure, opt-out). "Turn Verified B2B Contacts into Qualified Conversations"
4. **SEO and AI answer visibility.** Real buyer query, search results mock-up, AI answer mock-up, competitor visibility as labeled samples, client gap, content themes, schema. Label "Illustrative search visibility analysis". "Help [Client] Be Found Where Buyers Search and Ask AI"
5. **Talent and passive recruiting.** A hard-to-fill role tied to a verified client fact, fictional passive candidate, personalized message, job board vs passive comparison (proportions labeled illustrative), filters, funnel.
6. **KOL and buying committee (or decision unit).** Roles tailored to the objective, influence relationships, what each role needs to hear.
7. **Data and market opportunity.** TAM to shortlist, CRM or list check (overlap, net new, stale), white space. Do not draw values of very different magnitudes on one scale. Mark "not drawn to scale".
8. **Target account profile.** Fictional labeled sample org chart, profile, priorities, opener, best channel, diligence signals.
9. **Data powering LLMs and APIs.** Natural-language query, pipeline with validation layer, sample structured response, where it plugs into the client's existing tools.
10. **Client-owned platform.** Branded concept with a client-specific name, modules, and why it pays off. Label "Concept mock-up, name and URL illustrative".
11. **Webinar campaign.** Title, invite, registration page, reminder sequence, qualification, follow-up. Label "Sample webinar".
12. **Event, roundtable or executive dinner.** Invitation, limited seats, agenda, 1:1 scheduler, capture, follow-up. Never imply attendance at a real event unless verified. Label "Sample event".

For the Champions Infratech remap, replace 1 to 12 with: waterfront masterplan on the client's parcel; launch absorption case (confirmed figures only); senior living and longevity concept; wellness and hospitality layer; sustainability and water metrics for green finance and ratings; NRI and HNI demand map; channel partner activation; experience centre journey; brand licence structure options (labels only, no terms); phased delivery view; community programming calendar; the working session agenda. Label concept visuals "Concept, indicative, subject to technical session".

# How to build
Build visuals as HTML and render them to PNG with Playwright, one section per image, at 2x. This keeps names, numbers and copy exact. Use image generation only for background imagery or texture, never for text-bearing layouts.

Design system:
- Tokens from the client site: primary dark, primary, accent, light tint, neutral gray, font.
- One recurring brand texture from the client site, applied to atmosphere zones only. Never on data, charts or numbers.
- Alternate light and dark slides for rhythm. White cards on dark slides must reset to light-surface text colors.

## Trend pass (from design-trends)
Audience for these visuals is usually an executive buyer. Apply at most two stylistic trends and write the reason for each:
- **Dominant: disciplined hyper-bold headlines** (about 54px, weight 800, tight tracking), because an executive scanning a screen share needs the single claim to land in seconds.
- **Supporting: restrained depth** (layered shadows on mock-up containers only), because depth separates the mock-up from the explanation. Never on figures.
- Modular component system is structural and does not count.
Skip retro-futurism for executive audiences. Run the logo-cover test: hide the client name and confirm a stranger can still name the client's world.

# Verification gate (from visual-verify)
Before delivering:
1. Render all 12 and run an overflow check for elements escaping each slide.
2. Open every PNG, or a contact sheet plus any image with a fix, and look at it.
3. Write a numbered defect list naming elements (for example: white text on white card, headline overlapping body, nodes overlapping in a diagram, empty lower third).
4. Fix, re-render, re-check.
5. Grep all copy for em and en dashes. There must be none.
6. Check the client name spelling and ICP on every image.
7. Run the no-ai-slop gate on every line of copy.

# Deliverables
- 12 PNGs named `[CLIENT]_[NN]_[Use_Case].png`, plus a zip
- A live-meeting showing order: the 4 or 5 visuals that answer what the client asked for, in showing order, with one line on what to say for each. Hold the rest in reserve and map each to the topic that would justify showing it.
- Save the set and the showing order to the Celsus vault under `Atlas/Clients/[Client]/` when the vault is mounted.
- Optional follow-ons: run of show for the meeting, PowerPoint deck, PDF proposal, LinkedIn carousel

# Visual quality rules
Use: strong hierarchy, large readable headlines, realistic mock-ups, clear personas, consistent spacing, one dominant message per image.

Avoid: collages when separate images were requested, tiny text, repetitive layouts, random numbers, fake testimonials, fake logos, unverified claims, previous-client carryover, subsidiary ICPs applied to the parent, gradient text, side-stripe accent borders, emoji, and generic industry imagery that does not match the client.

# Copy rules
- No em or en dashes anywhere
- Follow no-ai-slop: no "It's not X, it's Y", no throat-clearing, no buzzwords such as leverage, delve or streamline
- Outreach copy in Round 1 leads with the recipient's situation, not the offer
- Never put firm prices, multiples or timelines in sample outreach unless the client approved them
- Champions Infratech visuals never carry uplift percentages, lagoon costs, IRRs, licence territory or exclusivity terms unless the user supplies approved figures

# Default user experience
When the user sends only a URL and a meeting, reply: "I'll research the company, pick the brand, identify its real ICP and objective, and create 12 separate growth visuals with a showing order for the meeting." Then begin research without asking unnecessary questions.