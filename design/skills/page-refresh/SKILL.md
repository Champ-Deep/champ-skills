---
name: page-refresh
description: Reskin bland pages with an outcome-first editorial design language (gradient hero, color result strip, PSO grid, 3-phase playbook timeline, dark quote panel, outcomes table with delta badges, brand-locked CTA banner). Use this skill whenever the user wants to refresh a page's look without rewriting the copy. MANDATORY TRIGGER for: "refresh this page", "make this look better", "reskin this", "give this a fresh look", "apply the showpiece design", "make this bland page look like our case study", "editorial design for this content", "redesign this page", "give it a glow up", "make this less bland", "design pass on this", "polish this page", "fresh look", "page-refresh", "showpiece design", "elevate this page", or any request to upgrade visual design while preserving content. Preserves every word of the original copy. Applies SEO fundamentals: 3-second value prop, title tag formula, outcome-focused hero visual, original data over stock, clear CTA pattern.
---

# Page Refresh

Take an existing page (HTML, Markdown, plain text, pasted copy, a URL) and reskin it in the LakeB2B-style editorial design language. Content stays. Design transforms.

## Core promise

Every word of the original copy stays. You restructure, you do not rewrite. If the source has a sentence, that sentence ends up somewhere on the new page. The user already approved that copy. They are paying you for design judgment, not editorial.

If the source is genuinely missing something the design needs (a stat for the hero chart, a quote, a CTA), insert a placeholder like `[PLACEHOLDER: add 1-line outcome stat]` and flag it at the bottom of your reply. Never invent.

## When to trigger

This skill activates on requests like:

| Trigger | Example |
|---|---|
| Direct ask | "Refresh this page", "reskin this", "give it a fresh look" |
| Comparison | "Make this look like our case study", "apply the showpiece design" |
| Quality complaint | "This page is bland", "this looks dated", "this feels generic" |
| Implicit | User pastes a URL or copy and says "design this" or "make this nicer" |
| Brand swap | "Make this work for Ampliz", "skin this for SPAN Global Services" |

Do NOT trigger when the user wants the COPY rewritten (use marketing:draft-content or b2b-blog-writer instead). This skill is design-only.

## Workflow

### Step 1: Confirm the source and the brand (one round, batched)

Use `AskUserQuestion` ONLY if any of the following are unclear after reading the user message. Batch into one call.

1. **Source content**: Where is it? (URL, file path, pasted text, attached doc.) If the user already provided it, skip.
2. **Brand**: Which brand palette? Default options: LakeB2B (purple), Ampliz (teal/orange), SPAN Global Services (blue/orange), Champions Group (orange), Cirralogix (cyan), Recruit Champ (green), Custom (user provides hex). See `design-system.md` for the full list.
3. **Page type**: Landing page, case study, blog post, internal report, one-pager. Default is whatever the source structure suggests.
4. **Output format**: Single self-contained HTML file (default), or vault note + HTML (for Obsidian-linked work).

If 95% confident on all four, proceed without asking.

### Step 2: Read the source

Load all source content into context. Do this once, in parallel if multiple files. Identify these slots:

| Slot | What to extract | If missing |
|---|---|---|
| `eyebrow` | Category/section label | Derive from page type |
| `headline` | The main H1 | Required. If absent, flag. |
| `accent_phrase` | The 1-3 word phrase inside the H1 to color with the brand gradient | Pick the most outcome-y phrase |
| `deck` | Subhead / one-paragraph summary | Required. If absent, flag. |
| `hero_visual_data` | Numbers, before/after, chart data | Use placeholder chart if absent |
| `meta_facts` | Industry, region, duration, etc. | Optional |
| `result_metrics` | 4 big numbers for the color strip | Pull from copy. If <4, drop the strip. |
| `client_or_context` | Who, what, why now | Optional |
| `problem_solution_outcome` | Three cards of story | If only 2 exist, use 2-card grid |
| `playbook_steps` | Numbered sequence | If absent, skip the playbook section |
| `quote` | Customer testimonial or pull quote | Optional |
| `outcomes_table` | Before/after metrics | Optional |
| `cta_main` and `cta_secondary` | CTAs | Required, even if generic |
| `related_links` | Three follow-on resources | Optional |

If the source is purely prose, segment it into these slots based on intent. Do not paraphrase.

### Step 3: Load the design system

Read `design-system.md` to pull the brand palette tokens, typography, and component snippets. Do NOT re-read the template if you have it in context from a recent run.

### Step 4: Apply SEO fundamentals (non-negotiable)

These are baked into the template, but verify each one before output:

1. **Title tag formula**: `<title>[Primary Keyword]. [Unique Value Prop] | [Brand]</title>`
2. **3-second value prop**: H1 + hero visual must communicate value without scrolling, without reading prose
3. **Outcome-focused hero**: The hero visual shows the result, not a stock photo. If source has numbers, build a bar chart. If not, build a metric card.
4. **Title attributes on hero visual**: Add `aria-label` describing the chart for accessibility
5. **One brand primary, one accent**: Do not introduce a third color family. Brand purple/teal/etc. + one gold or one bright orange. Period.
6. **CTA pattern**: One primary CTA in hero, one mid-page after proof, one banner. Never more than three placements.
7. **No em-dashes ANYWHERE in output**. Use periods, commas, colons. (Hard rule across all of Sreedeep's projects.)
8. **Light text on dark gradients only with explicit white declarations**. Never inherit color from parent.

### Step 5: Build the page

Open `template.html` as your starting point. It has every component in skeleton form with CSS variables exposed for the brand palette.

Replace placeholders. Delete sections that have no source content. Never invent a section just because the template has the slot.

Order of sections in the final page (omit any without source content):

1. Nav
2. Breadcrumb (auto-derived from page type)
3. Hero (eyebrow, H1, deck, meta strip, CTAs, outcome visual)
4. Result strip (4 big numbers in colored band)
5. Client/context card
6. PSO grid (Problem, Solution, Outcome cards)
7. Playbook (3-phase timeline + numbered steps)
8. Quote panel (dark gradient)
9. Outcomes table
10. What's included grid (six cards)
11. CTA banner
12. Related grid
13. Footer

### Step 6: Verify

Before presenting, grep your output for:

- `—` or `–` (em-dash / en-dash). Replace immediately.
- `[Placeholder]` or `TODO`. Either fill from source or flag.
- Any sentence in your output that did NOT come from the source (excluding boilerplate nav/footer/UI labels). If you added prose, undo it.
- Text color on colored or dark backgrounds: must be explicitly `color: white` or `color: var(--text)` in inline style or CSS. Do not rely on inheritance.
- Title tag follows the formula.

### Step 7: Save and present

- Save to `/Users/deep/Celsus/{descriptive-name}.html` (vault root, so the user can open immediately).
- If the source was a vault note, also offer to update the source note with a wikilink to the refreshed page.
- Present using a single computer:// link with a one-line description. Do not over-explain.

## Component reference

See `design-system.md` for:

- Brand palette presets (LakeB2B, Ampliz, SPAN Global Services, Champions Group, Cirralogix, Recruit Champ)
- Typography stack (Montserrat primary, Alata accent labels, JetBrains Mono technical, Fraunces editorial italic for some brands)
- Spacing tokens
- Every component snippet (nav, hero, result strip, PSO grid, playbook, quote, outcomes table, CTA banner, footer)

See `template.html` for the complete page skeleton with all components in place.

## Constraints and edge cases

- **If the source is a URL**: Use mcp__workspace__web_fetch first. If JS-rendered (returns shell), escalate to Chrome MCP to render and extract.
- **If the source has heavy imagery**: Reference each image with a placeholder `[IMAGE: filename.jpg . original alt text]`. Do not fabricate image content.
- **If the source is a competitor page**: Do NOT replicate their brand. Apply Sreedeep's chosen brand palette. The skill is design-language transfer, not visual plagiarism.
- **If the source is internal Obsidian note**: Strip `[[wikilinks]]` from the rendered HTML but keep the link target as an `<a href>` if the user wants the HTML to live outside Obsidian. If staying inside the vault, preserve wikilinks.
- **Mobile**: The template is responsive by default. Verify by mentally walking through clamp() values and the @media break at 820px.
- **Print**: The template includes a basic `@media print` reset. No need to add more unless asked.

## Output naming convention

`{Brand}_{Topic-or-Title}_{Type}.html`

Examples:
- `LakeB2B_CaaS_CaseStudy.html`
- `Ampliz_HealthcareData_LandingPage.html`
- `SPAN_Q2Report_OnePager.html`

## What this skill is NOT

- Not a copywriting skill. Use `b2b-blog-writer`, `marketing:draft-content`, or `marketing:campaign-plan` for copy.
- Not a brand-discovery skill. The brand presets are pre-loaded. Use `brand-voice:discover-brand` to extract a new brand.
- Not a Figma/Canva skill. Output is HTML/CSS only.
- Not a full design system builder. Use `design:design-system-management` for that.

Page refresh is the fast lane between "this looks bland" and "this looks like a showpiece" without touching a single word of the user's copy.

---

## Verify before delivery — MANDATORY

This output is visual, so reading the source does not tell you whether it worked. Render it and look at it.

```bash
python3 visual-verify/scripts/audit.py <output.html> --width 390
python3 visual-verify/scripts/audit.py <output.html> --width 1440
python3 visual-verify/scripts/shoot.py <output.html> --widths 390,1440 --themes light
```

Then **open every screenshot with the Read tool** and critique it. Not the file listing, the images. A screenshot you did not look at has verified nothing.

The four things this catches that nothing else does:

1. **Contrast measured against the composited background**, including transparency stacking, rather than against the hex you intended.
2. **Horizontal overflow at 390px**, with the offending element named.
3. **Content that overflows its container** once real text length replaced the sample.
4. **Flat hierarchy** — three elements competing where one should dominate. Only the eye finds this.

Zero FAILs before delivery. Every WARN either fixed or justified in one line. If no browser is available, say so and label the output **unverified**, listing what was not checked.

→ Full protocol: the `visual-verify` skill.
