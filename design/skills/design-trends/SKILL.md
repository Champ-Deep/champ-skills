---
name: design-trends
description: "Phase 3 of the design pipeline. Diagnoses whether a design is dated, overdone, or soulless, then either applies trends as intent rather than costume, or rebuilds visual identity, composition, and motion signature from the audience up, then produces the design handoff. Runs automatically after frontend-design, ui-polish, executive-one-pager, visual-report-builder, page-refresh, power-design, frontend-handoff, and any other design skill. MANDATORY TRIGGER for: 'looks dated', 'modernise this', 'design trends', 'trend pass', 'feels soulless', 'looks generic', 'looks vibe coded', 'looks like every other SaaS site', 'no personality', 'make it feel premium', 'visual identity', 'moodboard', 'pick a palette', 'wireframe this', 'section design', 'motion design', 'design handoff', 'spec this for developers', 'design tokens', 'redlines', 'component inventory', 'Figma handoff'. Full trigger list in assets/triggers.md. Brand locks are absolute."
---

# Design Trends

The last pass before anything ships. Three jobs, in this order.

1. **Diagnose.** Decide which of three failures the piece actually has, because the wrong fix makes things worse.
2. **Fix.** Either a trend pass, or an identity and composition rebuild. The diagnosis decides which.
3. **Handoff.** Produce the document set a developer, agency, or teammate can build from without asking a single question.

Source frameworks:
- Satori Graphics, *Graphic Design Trends 2026 and How to Actually Use Them* (youtu.be/yHs9-RVTwsA). The trend layer.
- Kole Jain, *The one thing vibe coding CAN'T fix about your website* (youtu.be/RCneB_MQ7qs). The soul, identity, composition, and motion layer.

---

## The two rules everything hangs off

> **1. Apply the intent, never the costume.**

Every trend that spreads is spreading because of an underlying shift in what audiences need to feel. The visual artifact is a symptom. Copying the artifact without the reason is how work ends up generic and overdone.

The gate: **before applying any trend, write one sentence naming the emotional or commercial job it does for THIS audience on THIS surface.** No sentence, no trend. A trend applied without a stated reason is decoration, and decoration is what makes a page look like everyone else's page.

> **2. Design like you have met the audience.**

The more common failure now is not that a page looks dated. It is that a page states who it is for and then designs as though it has never met them. A restaurant product that designs like it has never heard of a restaurant. A healthcare data page that could have its logo swapped for any competitor's and would need no other change.

The gate: **cover the logo and the product name, and ask whether a stranger can tell what world the buyer lives in.** If the answer is "some kind of software company," the piece has no soul, and no amount of trend work will give it one.

**Rule 2 outranks rule 1.** A soulless page wearing three trends is a well-dressed page that still does not know its audience. Identity first, trends second.

The corollary to both: a piece that adopts zero trends and executes its identity perfectly beats a piece wearing five trends badly. **Restraint is a valid output of this skill.**

---

## When this runs

**Automatic, as Phase 3 of the pipeline.**

| Phase | Skill | Owns |
|---|---|---|
| 1 | `frontend-design` | Structure, design system, first cut of styling, produces DESIGN.md |
| 2 | `ui-polish` | Removes AI tells, enforces the system harder, raises density |
| **3** | **`design-trends`** | **Diagnosis, then trends or identity, then handoff** |

Also runs after `executive-one-pager`, `visual-report-builder`, `page-refresh`, `power-design`, `pdf-to-html`, `prospect-campaign-plan`, `leaderboard`, `interactive-quiz`, `b2b-growth-showcase`, and any brand-skill deliverable. Do not wait to be asked.

**This skill can route backwards.** If the diagnosis finds soullessness, say so and run Mode B, even though it means doing identity work at Phase 3 that ideally happened at Phase 0. Better late than never, and the identity you build is reusable across every future deliverable for that brand.

**Handoff only.** When the design is settled and the ask is purely documentation, skip to Step 5.

---

## Read these first, in this order of authority

1. **Brand skill** (`lakeb2b-brand-guidelines`, `champions-group-brand`, `ampliz-brand-guidelines`, SGS tokens, `champions-ranch-docs`, `deependhq-design-system`). **Absolute authority. Never overridden by a trend or an identity exercise.** If it cannot be expressed inside the brand, it loses.
2. **DESIGN.md** from `frontend-design`.
3. **Locked design languages.** `executive-one-pager` has two, Warm Editorial and Pixel Arcade. Work within them, never replace them.
4. **Whatever you can infer** from existing code, if none of the above exist.

---

## Step 1: Diagnose, then route

Run `assets/trend-audit.md` in full. It has three diagnostic parts, and they map to three different failures with three different fixes.

| Finding | Failure | Route |
|---|---|---|
| Part A hits, dated tells | The piece looks like 2018 | **Mode A: trend pass** |
| Part B hits, overdone tells | The piece is wearing everything at once | **Mode A: trend pass**, mostly subtractive |
| Part C hits, soulless tells | The piece does not know its audience | **Mode B: identity rebuild** |
| Part C hits alongside A or B | Both | **Mode B first, then Mode A.** Never the reverse. |
| Nothing meaningful hits | The system is working | **Ship it.** Say so and stop. |

Report findings as specifics with locations. "The hero uses a 300-weight display face at 42px with 0 tracking" beats "the hero looks old." "There are no images on any of the eleven sections" beats "it feels generic."

**The ten-second version of the diagnosis:** cover the logo. If a stranger cannot name the buyer's world, it is Mode B. Everything else is Mode A.

---

# Mode A: Trend pass

Read `reference/trend-atlas.md` in full for the selected trends. Summary:

| Trend | Underlying shift it answers |
|---|---|
| **Nostalgic retro-futurism** | Future anxiety. Nostalgia is a trust shortcut. |
| **Organic imperfection** | Machine-made sameness. A human hand is now a credibility signal. |
| **Hyper-bold typography** | Scarce attention. Extreme scale is the fastest hierarchy signal available. |
| **Multi-dimensional design** | Flat design removed spatial affordance. Depth returns felt hierarchy. |
| **Modular systems** | Brands ship across hundreds of surfaces via distributed teams. |

## A1: Pick the trends, with a budget

**Two trends per surface. One dominant, one supporting. Modular systems does not count against the budget**, being structural rather than stylistic.

The ceiling exists because the failure to avoid is not choosing the wrong trend. It is choosing all of them. A page carrying five trends has no point of view, and no point of view is exactly what generic looks like.

Selection is driven by audience and surface. Full matrix in `reference/trend-application.md`. Compressed:

- **Enterprise data buyer** (LakeB2B modules, SGS datacards, healthcare, compliance): modular systems plus restrained depth. Nothing else.
- **Marketing and demand gen**: hyper-bold typography plus one of organic imperfection or retro-futurism.
- **Executive and investor**: restrained depth plus disciplined hyper-bold typography. Never retro-futurism.
- **Founder, community, event, Accelerator, Ranch**: widest licence.
- **Internal operational**: modular systems plus depth for hierarchy.

## A2: State the intent, in writing

Per trend, write the gate sentence into the trend register:

> **[Trend] at [strength]** because [this audience] on [this surface] needs to feel [X], and the piece currently does not deliver that because [Y].

Good:

> **Hyper-bold typography at dominant strength** because a CMO scanning a LakeB2B landing page in six seconds needs the single value claim to land before they scroll, and the current 42px semibold hero competes with three sibling headings.

Reject and rewrite:

> **Hyper-bold typography** because bold type is trending in 2026.

## A3: Apply, at a named strength

| Strength | Meaning | Share of surface |
|---|---|---|
| **Accent** | One or two moments. The system stays the visible logic. | Under 10 percent |
| **Supporting** | A consistent secondary layer across sections. | 10 to 30 percent |
| **Dominant** | The thing a viewer names when describing the page. | 30 to 60 percent, never more |

Past 60 percent the trend has replaced the brand, and next year it dates the whole asset at once instead of one layer of it.

---

# Mode B: Identity and composition rebuild

Run when the piece is soulless. Read `reference/soul-and-identity.md` and `reference/composition-and-motion.md` in full.

The order is fixed. Identity, then layout, then section treatment, then motion. Each step depends on the one before it.

## B1: Build the visual identity, image first

Detailed workflow in `reference/soul-and-identity.md`. The sequence:

1. **One image that carries the feeling.** Crop, darken, add noise, set the brand name on it. This composition is the mood board. Choose it specifically to escape both the bright sterile light-mode default and the flat typical dark-mode default.
2. **Extract the palette from the imagery**, rather than choosing it abstractly. A palette sampled from the buyer's environment inherits the buyer's world for free. Add one or two accents the imagery does not supply.
3. **Add texture from the domain.** Both surface texture (noise, grain, paper) and subject texture (the objects of the trade).
4. **Pair fonts for personality, not neutrality.** The second face should reference something in the buyer's world. Where the brand faces are locked, let the *treatment* carry the reference instead.
5. **Build icons from the accents**, each tied to a real capability.
6. **Close with imagery and the logo mark** in the composition.

**The governing rule for all six: none of this comes from a formula.** It is about what conveys the feeling and makes sense for the brand. The output must be defensible by pointing at the buyer, never by pointing at the process.

**Fix the heading while you are here.** The hero promises the outcome the buyer gets, in the buyer's own vocabulary. Not the category the product sits in. "Practitioner records your compliance team can defend" rather than "B2B healthcare data solutions."

## B2: Frankenstein the layout

Go section by section. For each, name a real site that solves it well **and state the modification in the same breath.** A reference without a stated change is a copy. Reference at least four different sites, and note that good modifications are usually subtractive: cut the text, drop the lines, make it less blocky.

**Then keep the wireframe and throw away every pixel of surface.** Structure, order, and relative weight survive. Colour, type, texture, and imagery do not, because those come from B1.

This is the same rule as the trend spine, applied to layout: take the intent, discard the costume. Record the reference list in the handoff.

## B3: Section by section

With the wireframe and identity settled, execution should become close to mechanical. Per section: background, texture level, type treatment, optical spacing, layered image assets, edge treatment.

**Sections must differ on purpose.** Texture level is a per-section decision that encodes what the section is for. Atmosphere sections carry texture. Product and data sections drop it. A LakeB2B page can run a moody textured hero and then go completely flat the moment the data sample appears, which is exactly how one page satisfies both the mood requirement and the data-purity rule.

**Scattered but not random.** Three invariants make apparent randomness read as intentional: larger elements below and smaller on top, an untouched margin of safety around all text, and darkened edges pulling attention to the centre.

**Optical spacing, not metric.** After a large heading, expect to roughly double the metric gap, because large type already carries space below the baseline. This gets worse as hyper-bold typography gets more dominant.

## B4: Build a motion signature

Motion is part of the identity, and it becomes identity through repetition.

**A motion signature is two named behaviours, repeated site-wide.** Not five, not one, never a different effect per section. If a developer cannot name your two behaviours after reading the handoff, you have a pile of animations rather than a signature.

Every motion decision answers one question: where is the eye now, and where should it go next. No answer means cut it.

Signature motion naturally lands on the hero and the CTA, which should behave as a matched pair, one the reverse of the other. The middle then needs its own answer, driven by content need rather than by a desire for more movement.

---

# Step 5: The handoff

Both modes end here. Read `reference/design-handoff.md`. Package:

1. **HANDOFF.md** from `assets/HANDOFF-template.md`.
2. **Token export.** CSS custom properties plus a JSON twin.
3. **Component inventory.** Every component, every state, including empty, loading, error, and long content.
4. **Redlines.** Spacing, breakpoints, type scale per breakpoint, elevation, motion timings.
5. **Asset manifest.** Every image, icon, font, and licence.
6. **Trend register.** What was applied, at what strength, why, review date.
7. **Identity provenance** (Mode B). Source images, sampled palette with the image each colour came from, texture decisions per section, the Frankenstein reference list.
8. **Motion signature** (Mode B). Both behaviours named, with triggers, timings, easings, and reduced-motion fallbacks.
9. **Acceptance checklist.**

Handoff is not optional, because the trend and motion layers are the parts most likely to be misimplemented. A developer who does not know the light source is fixed will invent one, and a developer who does not know the motion signature will animate whatever looks static.

---

# Step 6: Set review dates

| Layer | Review after |
|---|---|
| Nostalgic retro-futurism | 9 months. Fastest to saturate. |
| Multi-dimensional design | 12 months. The expression dates faster than the principle. |
| Organic imperfection | 18 months. Answers a durable shift. |
| Hyper-bold typography | 18 months. Ages well when tied to a real brand face. |
| Motion signature | 18 months, or whenever the identity changes. |
| **Visual identity** | **24 months.** It is brand capital, not a trend. |
| Modular systems | No review. Structural. |

Because the register records strength, scope, and tokens touched, retiring a layer later is a token edit rather than a rebuild.

---

## Non-negotiable guardrails

These override any trend, any identity choice, at any strength, always.

- **Contrast.** 4.5:1 body, 3:1 large text and meaningful UI, tested against every background variant. Noise over imagery is a legibility tool as much as an atmosphere one, so use it to *win* contrast rather than to excuse losing it.
- **Data stays honest.** No texture, wobble, extrusion, tilt, parallax, or count-up animation on a chart, table, metric, or compliance statement. Depth may sit on the container. It never touches the figure.
- **Motion respects `prefers-reduced-motion`**, collapsing to instant state changes and never to broken layout. Auto-rotating content pauses on hover and focus and exposes manual controls.
- **Performance budget.** LCP under 2.5s, CLS under 0.1. Texture ships as CSS or inline SVG, never a heavy PNG. Blur transitions are GPU-expensive, so verify on a low-end Android.
- **Mobile first.** Hyper-bold type checked at 360px with the longest real word in the actual copy. Section transitions simplified or disabled below 768px.
- **Divi and WordPress safety.** Every class carries the brand module prefix. No bare element selectors, no global resets, no `!important` cascades, no tokens on `:root`, z-index under 10. Verify the module renders identically inside and outside the Divi builder.
- **No em dashes** in any copy this skill writes or rewrites.

---

## Definition of done

- [ ] Diagnosis run and the mode stated explicitly.
- [ ] Logo-cover test passes. A stranger can name the buyer's world.
- [ ] Brand lock verified. No colour or typeface overridden.
- [ ] (Mode A) Two stylistic trends maximum, one dominant, each with a written intent sentence and named strength, none above 60 percent.
- [ ] (Mode B) Palette provenance recorded, source image per colour.
- [ ] (Mode B) Hero heading promises an outcome in the buyer's vocabulary.
- [ ] (Mode B) At least four Frankenstein references, each with a stated modification, surface discarded.
- [ ] (Mode B) Texture level is a deliberate per-section decision.
- [ ] (Mode B) Scatter invariants hold: large below, small on top, text margin untouched.
- [ ] (Mode B) Optical spacing applied after every display heading.
- [ ] (Mode B) Exactly two named motion behaviours, repeated site-wide.
- [ ] Contrast passes on every surface and state.
- [ ] No effect touches a number, chart, table, or compliance line.
- [ ] `prefers-reduced-motion` handled. Page fully usable and readable with motion off.
- [ ] Checked at 360px with real copy including the longest word.
- [ ] CSS scoped with the brand prefix. Divi-safe. No theme bleed.
- [ ] No em dashes anywhere.
- [ ] Full handoff package produced, review dates set.

---

## Files

| File | Use |
|---|---|
| `reference/soul-and-identity.md` | The relatability gap, vibe-coded tells, image-first identity workflow, palette extraction, identity and layout separability. |
| `reference/composition-and-motion.md` | Frankensteining, per-section treatment, scattered-not-random, optical spacing, motion signature. |
| `reference/trend-atlas.md` | The five trends: intent, signals, application by strength, anti-patterns, brand fit. |
| `reference/trend-application.md` | Audience and surface matrix, brand lock rules, Divi rules, deliverable-type guidance. |
| `reference/design-handoff.md` | Full handoff spec: tokens, inventory, redlines, manifest, agency and Figma parity. |
| `assets/trend-audit.md` | Three-part diagnostic. Run at Step 1 and again at the end. |
| `assets/snippets.html` | Scoped, Divi-safe CSS for every trend, plus identity, sectioning, and motion signature primitives. |
| `assets/HANDOFF-template.md` | Fill-in handoff template. |
| `assets/triggers.md` | Complete trigger phrase list. The description carries a compressed set. |
