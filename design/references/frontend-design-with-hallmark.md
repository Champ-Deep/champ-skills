---
type: skills-decision
created: 2026-06-02
status: active
decided-by: "[[Sreedeep Surapaneni]]"
tags:
  - "#skills"
  - "#design-system"
  - "#frontend"
related:
  - "[[MVA-Reference-Hub]]"
---

# Frontend Design + Hallmark — The Champions Group Visual Default

> Decided after a three-way A/B/C test on 2026-06-02 against the MVA Tuesday Weekly Brief. Frontend-design wins as the default. Hallmark layers on as the refinement and questioning system. Power-design is out for editorial work.

---

## The decision in one line

**`frontend-design` is the default skill for any visual artifact (briefs, reports, presentations, dashboards). `Nutlope/hallmark` is the layer that questions and improves the output when the user wants to push further.**

---

## What each skill is good at

### `frontend-design` (Anthropic, bundled)
The chosen baseline. Produces editorial broadsheet aesthetics with:

- Big display type paired with editorialization
- Small-text tabular metrics rendered in monospace
- Asymmetric layouts, broken grids for emphasis
- Newspaper-style mastheads and colophons
- Beautifully balanced mix of dark / light text and quoted blocks
- Tri-star (asterism) section dividers
- DESIGN.md baseline schema for design tokens

Best for: working session briefs, status reports, partner-facing decks, internal one-pagers, executive summaries.

### `Nutlope/hallmark` (third-party, MIT, install via `npx skills add nutlope/hallmark`)
The refinement layer. Adds opinionated structure on top of frontend-design:

- **Macrostructure picker** — 21 named whole-page shapes (Bento Grid, Long Document, Marquee Hero, Stat-Led, Workbench, Conversational FAQ, Manifesto, Photographic, Quote-Led, Specimen, Catalogue, Letter, Index-First, Narrative Workflow, Split Studio, Feature Stack, Type Specimen, Portfolio Grid, Map/Diagram, Ecosystem Index, Component Playground). Pick one, stamp the choice as a CSS comment, refuse to repeat it in the next build.
- **65-gate slop test** — runs before emit. Catches AI fingerprints like centred-everything heroes, Jane Doe testimonials, invented metrics, "Built for the modern team," AI nav and footer patterns.
- **Honest copy enforcement** — real names, real metrics, no marketing fluff.
- **Italic + P.S. + asterism craft** — quoted blocks, asterism dividers (⁂), postscripts that secretly carry the checklist, italic emphasis where prose breathes.
- **Single accent rule** — no multi-accent gradients.
- **Wordmark may use a different display face** as anti-AI-slop tell.
- **Structural variety doctrine** — two pages for two briefs should not be colour-swaps of the same template.

Best for: when frontend-design produces something good but the user wants to push it further into "doesn't look AI-made" territory.

### `power-design` (Paul Bakaus, bundled)
Rejected for editorial work. Produces HTML slide decks with 20 codified principles. Too text-heavy per slide, pigeonholes into 16:9 chunks, reads as the kind of artifact AI presentation tools have been generating for two years.

Reserved for: genuine slide decks where slides are the right format (board presentations, sales pitch decks). Not for briefs or reports.

---

## The standard procedure

When building any visual artifact:

1. **Default start:** invoke `frontend-design`. Produce the first version using DESIGN.md baseline + editorial broadsheet defaults.
2. **Sreedeep reviews.** If happy with the result, ship.
3. **If improvement wanted:** layer Hallmark on top. Specifically:
   - Pick a macrostructure from Hallmark's 21 catalogue. Pick a different one than was used in the prior similar artifact (the diversification rule).
   - Stamp the macrostructure in the CSS comment: `/* Hallmark · macrostructure: <slug> · theme: <name> · genre: <name> · v1.0 */`
   - Run the slop-test gates mentally before emit (or with the full skill installed, automatically).
   - Apply honest copy enforcement.
   - Add italic and P.S. craft where prose allows.
4. **Ship.**

---

## Active whitespace doctrine (added 2026-06-16)

> Plain centered single columns read as unfinished. Whitespace is an active workspace, like Stripe or Tailwind docs and Tufte editorial layouts. This is the default for any multi-section HTML (briefs, reports, dashboards), layered on top of the editorial broadsheet.

- **Content-aware grid, not a centered column.** Sticky left context sidebar, readable main column (~620 to 720px), right marginalia column.
- **Sticky TOC sidebar** (`position: sticky; top: 22px`). It doubles as navigation, and for a Narrative Workflow brief it IS the workflow spine. Highlight the active section on scroll with `IntersectionObserver`. Add a persistent legend or key whenever the doc uses a color system (status badges, roadmap, scorecard).
- **Marginalia.** Move definitions, asides, pro-tips, and mini-keys into the right margin so the body stays clean. This is also the natural home for plain-language jargon definitions (see language clarity below).
- **Ambient cues.** Top scroll-progress bar. Section dots optional. A live key or status block that updates as the reader scrolls when the content is a system.
- **Mobile and print.** Collapse to one column. The TOC becomes a static top strip or hides. Marginalia becomes inline tinted asides. Always test the print path for share-screen briefs.

Reference build: `2026-06-16-MVA-Tuesday-Weekly-Brief.html` (v2). First shown on `Trackable-KRA-Scorecards.html` (2026-06-04). Source of truth: memory `feedback-frontend-content-aware`.

---

## Language clarity, the Vinh Giang layer (added 2026-06-16)

> Apply to the words, not just the layout. A beautiful page that reads as jargon soup still fails. Drawn from Vinh Giang's communication work (five vocal foundations: rate, volume, pitch, tonality, pause).

- **Clarity over complexity.** Use the plainest word that still carries the meaning. Define jargon the first time, ideally in the margin, not the body: addendum, FBO, RBF, ICP, sandbox, API, pre-qualification.
- **One idea per sentence.** Short sentences. Pull the single most important line out as a standalone lead line in larger serif.
- **The pause, in print, is whitespace.** Short paragraphs, generous spacing, room to breathe between sections.
- **Vary the rhythm.** Mix short and long sentences. Sameness reads flat and people stop reading.
- **Signpost and use triads.** Three locks, three promises. Easy to follow, easy to recall after the call.
- **Honest, concrete verbs.** "We will" not "we are positioned to." No inflated filler.

When both layers are applied, jargon definitions live in the marginalia. The whitespace doctrine and the clarity layer reinforce each other: the margin that creates active whitespace is the same margin that holds the plain-language key.

---

## The super-skill goal (proposed, not built)

Long-term goal: consolidate `frontend-design` + the Hallmark macrostructure picker + slop-test gates + italic/asterism craft + structural-variety doctrine into a single skill called something like `champions-frontend`. Team-shareable. One invocation produces a visual artifact that:

- Uses the frontend-design baseline aesthetics
- Picks a Hallmark macrostructure with diversification rule applied
- Runs the slop-test before emit
- Saves the artifact + a one-line note explaining macrostructure choice

**Status:** not yet built. Pending. Worth scoping as a 1–2 hour skill-creation task.

---

## When this applies

| Artifact type | Use this stack | Notes |
|---|---|---|
| Working session briefs | frontend-design + Hallmark | MVA Tuesday template proves it |
| Internal status reports | frontend-design + Hallmark | Same template scales |
| Partner-facing decks | frontend-design + Hallmark | Editorial broadsheet beats slide deck |
| Dashboards | frontend-design alone | Hallmark macrostructures are page-level, less useful for live data UI |
| Marketing landing pages | frontend-design + Hallmark | The intended Hallmark use case |
| Genuine slide decks (board, sales pitch) | power-design | Reserved use, not default |
| Letters / personal notes | Hallmark Letter macrostructure standalone | Tested on the C variant, works |

---

## Reference artifacts from the decision day

- [[2026-06-02-MVA-Tuesday-Weekly-Brief]] — the Version B that became the default. Use as the structural template.
- `2026-06-02-MVA-Brief-A-PowerDesign.html` — what we are NOT doing
- `2026-06-02-MVA-Brief-B-FrontendDesign.html` — the default
- `2026-06-02-MVA-Brief-C-Hallmark.html` — the refinement direction
- [Nutlope/hallmark on GitHub](https://github.com/Nutlope/hallmark) — install via `npx skills add nutlope/hallmark`
- [Hallmark macrostructures reference](https://github.com/Nutlope/hallmark/blob/main/references/macrostructures.md) — the 21-shape catalogue

---

## Hard rules carried forward

- NEVER em-dashes
- Check contrast on dark backgrounds — text must be explicitly white/light
- Single accent per page
- Max three font families per page
- No AI nav fingerprint (no horizontal pill nav with logo-left, links-center, CTA-right)
- No AI footer fingerprint (no four-column footer with logo + nav + links + newsletter)
- No "Built for the modern team" or equivalent boilerplate
- No Jane Doe / John Smith placeholder names
- No invented metrics
- Active whitespace: sticky TOC + marginalia + scroll-progress, never a plain centered column (any multi-section HTML)
- Language clarity: define jargon in the margin, one idea per sentence, the pause via spacing, lead lines, triads

---

## Note on editing the bundled skill

The Anthropic `frontend-design` skill is a read-only cache in-session and cannot be edited here. This vault note is the canonical home for Sreedeep's customizations. To fold these doctrines into the bundled skill itself, edit via Settings > Capabilities or rebuild with `skill-creator`. Until then, this note plus the memory files carry the learnings.

---

*Decided 2026-06-02 during the MVA prep iteration. Active as the design system default for all Champions Group visual artifacts going forward.*
*Updated 2026-06-16: added the active-whitespace doctrine and the Vinh Giang language-clarity layer after the MVA brief v2 redesign.*
