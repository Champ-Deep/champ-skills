---
name: b2b-growth-showcase
description: "Unified B2B growth showcase generator (v2). From just a prospect's website/domain, produces personalized sales assets in one of three modes: (A) 12 standalone premium images via Higgsfield for LinkedIn/proposals, (B) a '10 Ways [Client] Can Use B2B Data' PPTX deck, or (C) both, with the images embedded in the deck. Optional autoplay HTML walkthrough. MANDATORY TRIGGER for: growth opportunity report, prospect showcase, '10 ways' deck, '12 visuals'/'12 images', B2B data activation proposal, personalized data pitch, client website to growth visuals, or showing a client what their campaigns could look like before they buy — even with only a company name or URL. Works for LakeB2B, Ampliz, or Champions Group — ask which brand if unclear. SUPERSEDES and replaces: client-to-12-growth-visuals, b2b-visuals, b2b-visuals-to-deck, vk-b2b-visuals."
---

# B2B Growth Showcase v2 — Unified

Turns a bare company name or website into a personalized, client-ready growth showcase. One skill, three output modes. This version consolidates five earlier skills (b2b-growth-showcase v1, client-to-12-growth-visuals, b2b-visuals, b2b-visuals-to-deck, vk-b2b-visuals) into a single pipeline with shared research, shared methodology, and mandatory design guardrails.

## Output modes (pick in Step 0)

| Mode | Deliverable | When |
|---|---|---|
| **A — Images** | 12 standalone 16:9 premium images via Higgsfield MCP, each individually usable (LinkedIn post, email header, proposal insert) | "12 visuals", "growth images", mix-and-match assets |
| **B — Deck** | 13-slide PPTX ("10 Ways" narrative: cover + 10 sections + event slide + closing) via `scripts/generate_deck.js` | "deck", "presentation", one cohesive story to present end-to-end |
| **C — Both** | Mode A images embedded as the visual layer of the Mode B deck | "deck with the visuals", full pitch package |

Optional add-on for any mode: the autoplay HTML walkthrough (`assets/video_walkthrough_template.html`) that plays like a video and can be screen-recorded. There is no real video-generation path here; say so if asked for "a video".

If the user's ask clearly names the mode, don't ask. If ambiguous between images and deck, ask once — outputs and effort genuinely differ.

## Step 0 — Preflight (report result in one line)

1. **Brand:** LakeB2B, Ampliz, or Champions Group? Ask once if unclear; it changes palette and value-prop copy. Read the matching brand-guidelines skill if present.
2. **Mode:** A, B, or C (above).
3. **Connectors:** web research available; for Modes A/C, Higgsfield MCP connected (never substitute text descriptions for actual images; if disconnected, stop and offer research + ICP brief only).
4. **Compliance sanity check:** if the target domain is a government entity, state-owned company in a sanctioned/restricted sector, or otherwise high-risk for a Western data vendor to prospect, pause and flag before building a campaign against it. Skip for ordinary commercial sites.
5. **Design guardrails:** read `references/design_guardrails.md` BEFORE writing any copy, prompt, or slide. Non-negotiable.

## Step 1 — Research the client (mandatory, never skip)

Fetch the client's site (root, then `www.`/`http://` variants). If direct fetch fails, fall back to search: quoted domain, "[domain] company", LinkedIn/Crunchbase/Wikipedia snippets. Try at least 2-3 angles before treating the company as unidentifiable. If multiple distinct companies share the name, present candidates via AskUserQuestion — never guess.

Extract: correct legal/brand name (distinguish parent/subsidiaries explicitly), products and services, industries served, use cases, geographies, likely target account types, buyer departments and titles, 2-4 named competitors, one realistic buyer search query (for the SEO/AEO section), and relevant events/associations.

**Freshness rules:**
- Never reuse an ICP, messaging angle, statistic, or visual concept from a previous client run — build fresh from what this website actually says, even for structurally similar companies.
- Never invent customer names, data counts, campaign performance, or market statistics. Anything unverified is labeled **Illustrative / Estimated / Sample / To be validated against LakeB2B data** — in the ICP brief AND inside the assets themselves.
- Don't name a real target account in org-chart/account-map mockups unless the user supplies one; use a generic descriptor.

## Step 2 — ICP brief (present before generating anything)

Short structured block: client name, website, business summary, ICP (titles, industries, geos), competitors, assumptions and their labels, chosen mode, brand. Wait-free: present it and proceed unless the user interjects.

## Step 3 — Read the methodology

Read `references/ten_ways_playbook.md` in full before writing copy. It defines the 10 sections (+ event module), sample language, visual spec, and per-section guardrails. The same 10 concepts drive both modes; Mode A renders each as one image, Mode B as one slide.

## Step 4 — Generate

**Mode A (images):** for each of the 12 concepts (10 sections + webinar + event), write one Higgsfield prompt following the prompt rules in `references/design_guardrails.md` (photographic/editorial direction, palette, headline text 12 words max, brand wordmark, "Concept sample" label, explicit anti-slop negatives). Submit via `generate_image_batch` (12 max per batch), poll with `jobs_wait`, display with one `show_generation_by_ids` call. Download finals and deliver as files, not links.

**Mode B (deck):** fill `assets/config.example.json` per its inline comments, then:

```bash
node scripts/generate_deck.js path/to/config.json path/to/output.pptx
```

Palette lives in the constants block of `generate_deck.js`; change it there, never per-slide. Only lakeb2b and champions palettes are confirmed; anything else falls back with a warning.

**Mode C:** run A first, then B with `image_paths` pointing at the downloaded images (add per-slide images by extending the config; the script's `appFrame()` card is the placement target).

## Step 5 — QA (mandatory before presenting)

- Decks: run the pptx skill's validation, convert slides to images, and visually inspect every slide. Fix before presenting.
- Images: view every generated image. Reject and regenerate any with garbled text, wrong brand, missing "Concept sample" label, or AI-slop tells (see guardrails checklist).
- Copy: run the guardrails checklist in `references/design_guardrails.md` section "Pre-ship checklist".

## Step 6 — Deliver

Present files (deck and/or image set). Offer the HTML walkthrough and the "Recommended Client Deliverable" next-steps table (from the playbook) as quick adds. Don't over-explain contents.

## Reference files

- `references/ten_ways_playbook.md` — the 10-section methodology, sample copy, visual specs, guardrails. Read before writing content.
- `references/design_guardrails.md` — anti-slop design rules (derived from impeccable.style) for decks, HTML, and image prompts. Read before generating anything.
- `assets/config.example.json` — deck input schema.
- `assets/video_walkthrough_template.html` — autoplay HTML walkthrough template.
- `scripts/generate_deck.js` — parameterized pptxgenjs generator.

## Migration note

This skill replaces: `client-to-12-growth-visuals`, `b2b-visuals`, `b2b-visuals-to-deck`, `vk-b2b-visuals`, and b2b-growth-showcase v1. Their triggers all route here. Delete the old skills once this one is installed and verified.
