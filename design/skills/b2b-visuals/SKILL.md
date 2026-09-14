---
name: b2b-visuals
description: "Given only a client or prospect website URL, researches the company and produces 12 separate, standalone, presentation-ready visual images (not a slide deck, not a collage) showing how LakeB2B B2B data could power that client's growth: personalized email, LinkedIn/Meta social, AI telemarketing, SEO/AEO visibility gap, passive-candidate recruiting, KOL/buying-committee map, data & industry analysis, org chart/account intelligence, LLM/API workflow, client-owned platform, webinar invitation, and event/executive-lunch campaign. MANDATORY TRIGGER when the user pastes a client website URL and asks for growth visuals, a '12 image'/'12 visual' showcase, a LakeB2B data activation proposal, or to turn a company's website into a personalized campaign showcase — even with no input beyond the URL. Distinct from b2b-growth-showcase: that builds one slide-deck narrative; this produces 12 independent, LinkedIn/proposal-ready image files, each usable on its own."
---

# B2B-Visuals — 12 Personalized Growth Images from a Website URL

Turns a bare client website URL into 12 separate, individually usable, premium-designed images — each one a standalone visual for LinkedIn, an executive proposal, or a sales deck — showing that specific company what LakeB2B data could do for them.

**This is a sibling skill to `b2b-growth-showcase`, not a replacement.** Use `b2b-growth-showcase` when the person wants one cohesive slide-deck narrative (a `.pptx` to present end-to-end). Use `b2b-visuals` when they want 12 independent images they can drop individually into LinkedIn posts, an email, or mix-and-match into someone else's deck. If it's ambiguous which they want, ask — the outputs and workflows are genuinely different.

## Trigger

- A bare client/prospect website URL with an ask for "12 visuals," "growth images," "B2B data activation proposal," or similar
- "Analyze this company's ICP and generate 12 personalized campaign images"
- "Turn this customer's website into an email, social, AI calling, webinar and event campaign showcase"

Don't wait for optional inputs (geography, product priority, industry, known ICP, campaign objective, image dimensions) before starting — infer reasonable defaults from the website itself and label uncertain assumptions clearly in the ICP summary (Step 2).

## Workflow

### Step 1 — Research the client (mandatory, before any visual work)

`web_fetch` the client's actual website. Don't skip this even if the company is familiar. Identify:

- Correct company name (and how it's distinct from its parent company, subsidiaries, or affiliated brands — don't blend them)
- Products and services, industries served, customer use cases
- Geographic markets
- Likely target account types, buyer departments, and job titles
- Competitors and market alternatives (`web_search` — needed for Image 4)
- Relevant events, associations, or industry communities (useful for Images 11–12)

**Never reuse the ICP, messaging, statistics, or visual concepts from a previous client run in this conversation.** Every company gets its own research pass, even if it's structurally similar to one just built (e.g., don't let a Konica Minolta run bleed into an Epson run just because they're both in office imaging). If the current client is a subsidiary or parent of a company already analyzed in this conversation, build the ICP fresh from the current site — don't assume the earlier ICP still applies.

Verify important claims through credible public sources. Never invent customer names, data counts, campaign performance figures, or market statistics. Anything not independently verified gets labeled illustrative, estimated, sample, or "to be validated against LakeB2B data" — both in the ICP summary and inside the images themselves (see guardrails).

### Step 2 — Present the ICP summary before generating anything

Reply with this before touching the image generator:

- Client name, website
- One-line business summary
- Primary ICP(s) and secondary ICP(s)
- Target industries, geographies, company sizes
- Priority buyer roles
- Core business problems addressed
- Recommended campaign message
- Any assumptions that need validation

Then proceed directly to image generation — don't wait for approval unless something about the request is genuinely ambiguous (see proactivity norms: ambiguity is a reason to state an assumption and continue, not to stall).

### Step 3 — The SEO/AEO image needs a real, dated search

Same rule as `b2b-growth-showcase`: run an actual `web_search` (and `web_fetch` the best result) for a query this client's real buyers would type. Populate the generator config's `seo_search` block with the real query, source, dated ranking, and the client's real position — or a genuine "not mentioned" finding if that's what the search actually shows. Never fabricate a screenshot or force a competitive-gap narrative that isn't real; if the client's own rank is unknown, label the image "Illustrative search visibility analysis" instead of presenting it as a live result.

### Step 4 — Generate the 12 images

Copy `assets/config.example.json`, fill it from Steps 1–3, then:

```bash
node scripts/generate_visuals.js path/to/config.json path/to/output_dir/
```

This builds one 16:9 landscape composition per use case (see `references/twelve_images_playbook.md` for the exact spec and headline pattern for each), then rasterizes each one to its own standalone PNG — 12 separate files, never a combined collage, each named for its use case (`01_email_campaign.png` … `12_event_networking.png`). Read the top of `generate_visuals.js` before editing; the `posterSlide()` helper is the shared layout system all 12 images build on — change the palette or type scale there, not per-image.

**Always QA before presenting**: open a few of the rendered PNGs (`view` tool) and check for the client's correct name/spelling, correct ICP, and no clipped or unreadably small text. Regenerate anything that fails this check — don't ship a misspelled company name or an unreadable label.

### Step 5 — Deliver

Present all 12 PNGs (`present_files` with all 12 paths). After delivery, optionally offer — don't build unprompted — a one-page summary collage, a PowerPoint version (hand off to `b2b-growth-showcase` for that), a PDF proposal, or a LinkedIn carousel adaptation.

## On "Image Generation," "Canvas," and other capabilities from a ChatGPT-style spec

If a person hands you a spec written for a ChatGPT Custom GPT (mentioning turning on "Web Search," "Image Generation," "Code Interpreter," "Canvas" in a GPT editor), those toggles don't map onto this environment and there's nothing to configure — translate instead of trying to replicate the settings panel:

- **Web Search** → already on by default here (`web_search` / `web_fetch`).
- **Code Interpreter & Data Analysis** (for uploaded CRM/customer files) → already available (`bash_tool`, Python/pandas in the sandbox); use it directly if the person uploads a file to analyze per Image 7.
- **Image Generation** → there's no diffusion/generative image model in this environment. This skill produces the polished, on-brand visuals a different way: designed layouts rendered through code (`pptxgenjs` → PDF → rasterized PNG), not an AI-generated illustration. That's what `generate_visuals.js` does. Don't claim or imply the output came from an image-generation model.
- **Canvas** → not applicable; delivered files serve the same purpose.

Say this plainly if asked, rather than pretending an equivalent toggle exists.

## Reference files

- `references/twelve_images_playbook.md` — the exact spec, headline pattern, and required visual elements for each of the 12 images. **Read before generating.**
- `assets/config.example.json` — input schema; copy and fill per client.
- `scripts/generate_visuals.js` — builds the 12 compositions and hands off to the rasterization step described in its header comment.

## Guardrails

- Never reuse a previous client's ICP, messaging, stats, or visual concepts.
- Never invent customer names, data counts, campaign performance, or market statistics — label unverified numbers illustrative/estimated/sample/to-be-validated, in plain descriptive language (not as an instruction to the presenter — see the no-builder-notes rule below).
- No builder/internal instructions inside any rendered image text ("confirm this before presenting," "verify against live data") — that's a note to you, not copy for the client. Say what's illustrative in language a client would find normal to read.
- Don't fabricate a live search-engine screenshot (Image 4) — real and dated, or explicitly labeled "Illustrative search visibility analysis."
- Don't use the client's real logo unless explicitly requested — use bold client-name typography instead.
- Don't use real people's names or photos for the sample executive profile (Image 8) — clearly labeled fictional sample only.
- Don't fabricate customer names, testimonials, or customer logos anywhere.
- Don't recommend Meta/Facebook targeting (Image 2) when the client's ICP is enterprise/technical and not consumer-adjacent — check fit before including it.
- Don't state the client is attending or sponsoring a real named event (Image 12) unless verified from the research step.
- Distinguish the client from its parent company and subsidiaries throughout — don't blend their ICPs or claims.
