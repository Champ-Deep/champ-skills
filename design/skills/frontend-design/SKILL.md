---
name: "frontend-design"
description: "Create distinctive, production-grade frontend interfaces with high design quality. Use when asked to build web components, pages, artifacts, posters, dashboards, data visualizations, or apps on any platform (web, mobile, desktop, foldable, screenless companion). Avoids generic AI aesthetics. Includes a Design System Generator, 50+ styles, 161 palettes, 57 font pairings, 25 chart types across 10 stacks, a gated Expressive Tier (3D carousels, endless and scattered galleries, shader distortion), liquid-glass navigation rules, and device-class guidance for wide foldables and screenless wearables. MANDATORY TRIGGER for any UI/UX work, frontend code, design system creation, component building, dashboard design, chart creation, or mobile, foldable, and wearable companion UI."
---

---
name: "frontend-design"
description: "Create distinctive, production-grade frontend interfaces with high design quality. Use when asked to build web components, pages, artifacts, posters, dashboards, data visualizations, or apps on any platform (web, mobile, desktop, foldable, screenless companion). Avoids generic AI aesthetics. Includes a Design System Generator, 50+ styles, 161 palettes, 57 font pairings, 25 chart types across 10 stacks, a gated Expressive Tier (3D carousels, endless and scattered galleries, shader distortion), liquid-glass navigation rules, and device-class guidance for wide foldables and screenless wearables. MANDATORY TRIGGER for any UI/UX work, frontend code, design system creation, component building, dashboard design, chart creation, or mobile, foldable, and wearable companion UI."
---

This skill creates distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. It combines two systems: the **Impeccable** design language (anti-patterns and principles by Paul Bakaus, Apache 2.0) with a **Design System Generator** (concrete styles, palettes, fonts, and product-type intelligence inspired by UI UX Pro Max).

## Two-phase pipeline: build, then polish

This skill is **Phase 1**: structure, the design system, and the first cut of styling. It pairs with a **Phase 2** refinement skill, `ui-polish`, which hunts the residual "AI tells" (emoji icons, default palettes, decorative graphics where data belongs, overstuffed sidebars, static pricing) and replaces them with senior-designer choices.

Always produce the DESIGN.md (below). It is the contract the polish pass reads, so the two phases never fight. After you finish Step 3, hand off to Step 4.

## Priority System

Rules ranked by impact. When time is limited, address higher priorities first.

| Priority | Domain | Why it matters |
|----------|--------|----------------|
| CRITICAL | Accessibility | Legal compliance, user inclusion. Non-negotiable. |
| CRITICAL | Touch & Interaction | Broken touch = unusable product on 60%+ of devices. |
| HIGH | Performance | Slow apps lose users. CLS, lazy loading, image optimization. |
| HIGH | Style Selection | Wrong style = wrong audience impression. Match product type. |
| HIGH | Layout & Responsive | Mobile-first is the default. Broken layouts kill trust. |
| HIGH | Surface & Device Class | Wide foldables and screenless companions break every assumption a phone breakpoint makes. |
| MEDIUM | Typography & Color | Polish layer. Bad fonts/colors feel "off" even if functional. |
| MEDIUM | Animation & Motion | Delight layer. Missing motion feels static; bad motion feels cheap. |
| MEDIUM | Forms & Feedback | UX friction. Bad forms lose conversions. |
| HIGH | Navigation | Lost users don't convert. Consistent patterns build confidence. |
| CONTEXT | Charts & Data | Critical when present, irrelevant when absent. |
| CONTEXT | Expressive Tier | Gated. Enormous differentiation upside, enormous slop and perf downside. |

---

## Default Baseline: DESIGN.md

Every frontend output MUST be anchored on a **DESIGN.md**, an AI-readable design spec in the schema defined by [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md). This is a curated index of 60+ DESIGN.md files covering brands from Stripe to SpaceX, each with 9 standardized sections an agent can consume directly.

→ *Consult [design-md-baseline reference](reference/design-md-baseline.md) for the full schema, curated index, closest-analog table, authoring workflow, and Champions brand-skill integration rules.*

**The 9-section DESIGN.md schema:**

| # | Section | Purpose |
|---|---------|---------|
| 1 | Visual Theme & Atmosphere | Mood, density, design philosophy |
| 2 | Color Palette & Roles | Semantic color names, hex values, functional roles |
| 3 | Typography Rules | Font families, complete hierarchy tables |
| 4 | Component Stylings | Buttons, cards, inputs, navigation with all states |
| 5 | Layout Principles | Spacing scales, grid systems, whitespace philosophy |
| 6 | Depth & Elevation | Shadow systems, surface hierarchies |
| 7 | Do's and Don'ts | Design guardrails and anti-patterns |
| 8 | Responsive Behavior | Breakpoints, touch targets, collapsing strategies |
| 9 | Agent Prompt Guide | Quick color refs, ready-to-use prompts |

**Precedence chain** (highest wins):

```
Champions brand skill → venture-specific DESIGN.md → curated VoltAgent DESIGN.md → generator-built DESIGN.md
```

If a Champions Group or venture brand skill is loaded, its tokens override the DESIGN.md wherever they conflict. The DESIGN.md fills in everything the brand skill doesn't specify.

**Two additions to Section 8 (Responsive Behavior):** every DESIGN.md must now also declare a **device class** (pointer surface, wide-foldable, or screenless companion) and, if the expressive tier is used anywhere, a **motion budget** line stating the frame target and the reduced-motion fallback. See "Surface & Device Class" and "The Expressive Tier" below.

---

## Step 0: Design System Generator → DESIGN.md

Before writing any code, generate a complete design system **and output it as a DESIGN.md file** following the 9-section schema above. This is the single biggest upgrade over ad-hoc design decisions.

1. **Resolve DESIGN.md source** using the precedence chain:
   - If a Champions/venture brand skill is active → start from its tokens, populate remaining DESIGN.md sections around them.
   - If the target resembles a known brand → find the closest analog in the [curated index](reference/design-md-baseline.md) and fork it.
   - Otherwise → generate from scratch using the steps below.

2. **Identify product type** and match to recommended styles.
   → Consult [styles database](reference/styles-database.md) for product-type-to-style mapping.

3. **Select style direction** from 50+ named styles or create a hybrid.
   → Consult [styles database](reference/styles-database.md) for the full library.

4. **Generate palette** from 161 curated palettes or derive from brand colors.
   → Consult [color reference](reference/color-and-contrast.md) for palette database + OKLCH system.

5. **Select font pairing** from 57 curated pairings matched to the style.
   → Consult [typography reference](reference/typography.md) for pairing database.

6. **Define spacing/layout tokens**: 4pt base grid, semantic names.
   → Consult [spatial reference](reference/spatial-design.md) for token systems.

7. **Declare device class and motion budget.** Which surfaces does this ship to, and what is the frame and payload ceiling.

8. **Output as a DESIGN.md** with all 9 sections populated, plus CSS custom properties / design tokens ready for implementation.

**Design System Persistence**: Create a Master set of tokens. For specific pages or components, create Override layers that extend the master. This prevents drift.

```
Master tokens → Page overrides → Component overrides
(base truth)    (contextual)      (exceptional)
```

---

## Step 1: Design Context

Before building, clarify who it's for. Great design is impossible without context:

- **Target audience**: Who uses this product and in what context?
- **Use cases**: What jobs are they trying to get done?
- **Brand personality/tone**: How should the interface feel?
- **Platform**: Web, iOS, Android, desktop, wide-foldable, screenless companion, cross-platform?

If the user has brand guidelines or a brand skill, load and apply those. If ambiguous, ask. Code tells you what was built, not who it's for.

**Polish is not the whole test.** Visual polish alone does not exit the AI-slop category if the content itself is generic. A flawless layout wrapped around hollow, could-apply-to-any-brand copy is still slop, arguably worse, because the polish makes it more persuasive-looking while saying nothing. The content must earn its place same as the pixels do.

---

## Step 2: Design Direction

Commit to a BOLD aesthetic direction. "Clean and modern" is not a direction. It's a non-decision.

- **Purpose**: What problem does this solve? Who uses it?
- **Tone**: Pick from the [styles database](reference/styles-database.md) or go custom. Starting points: brutally minimal, maximalist, retro-futuristic, organic, luxury, playful, editorial, brutalist, art deco, soft/pastel, industrial, neo-grotesque, Swiss, Memphis, Scandinavian, cyberpunk, neo-brutalist, glass, neumorphic, editorial grid, monochrome, duotone, gradient mesh, paper/analog, terminal/hacker, vaporwave, hand-drawn, corporate sharp, warm tech, cold precision.
- **Constraints**: Framework, performance budget, accessibility level (AA minimum, AAA preferred).
- **Differentiation**: What makes this UNFORGETTABLE? The one thing someone remembers.

**CRITICAL**: Bold maximalism and refined minimalism both work. The key is intentionality, not intensity.

---

## Step 3: Build with the Priority System

### CRITICAL: Accessibility

Non-negotiable. Check BEFORE shipping.

- Contrast: 4.5:1 body text, 3:1 large text and UI components
- Focus states: visible ring on all interactive elements. Never `outline: none` without replacement. Use `:focus-visible` for keyboard-only rings.
- Keyboard: tab order, skip links, roving tabindex for composite widgets
- ARIA: labels on icon buttons, descriptive alt text, live regions for dynamic content
- Touch targets: 44x44px minimum (use padding/pseudo-elements for visual compactness)
- Reduced motion: `@media (prefers-reduced-motion: reduce)` is not optional
- Canvas and WebGL surfaces need a DOM equivalent. If content only exists inside a shader or a 3D scene, it does not exist for a screen reader or for search.

### CRITICAL: Touch & Interaction
→ *Consult [interaction reference](reference/interaction-design.md)*

- 44x44px minimum touch targets, 8px spacing between
- Immediate loading feedback (optimistic UI, skeleton screens over spinners)
- Progressive disclosure: simple first, advanced behind expandable sections
- Empty states that teach, not just "nothing here"
- Not every button is primary. Use ghost, text links, secondary styles.

### HIGH: Style Selection
→ *Consult [styles database](reference/styles-database.md)*

- Match style to product type and audience
- Once you choose a style, commit fully. Mixing metaphors kills cohesion.
- Use SVG icons. Never emoji as structural UI elements.
- No sparklines as decoration
- No modals unless truly no better alternative
- **No colored `border-left`/`border-right` side-tab stripes** on cards, list items, callouts, or alerts. Per Impeccable (github.com/pbakaus/impeccable), this is "the single most recognizable AI-dashboard tell." Use fill, weight, or a leading icon to signal status instead.
- **No rounded-square icon tile sitting above every section heading.** That generic-SaaS pattern (icon in a soft rounded box, centered above a heading, repeated per section) reads as templated. Vary the treatment or drop the tile.
- **No dark glows** (soft colored box-shadow blooms behind cards or text on dark surfaces) as a default decoration. If used at all, it must be load-bearing for one hero moment, not sprinkled across the UI.

**Glass: the ban stands, with one sanctioned exception.**

Decorative glassmorphism, meaning frosted panels sprinkled across cards, sections, and hero backgrounds because they look futuristic, remains banned. It is one of the loudest AI-slop tells and it wrecks contrast.

The exception is **liquid glass as a navigation material**. Platform design systems have converged here, and it now reads as native rather than as decoration. Use it ONLY on surfaces that float above scrolling content:

| Sanctioned | Banned |
|---|---|
| Floating bottom tab bars and pill navs | Content cards |
| Sticky top bars that overlay scrolled content | Page or hero backgrounds |
| Search fields and command bars that hover | Form containers, tables, dashboards |
| Toolbars, sheet handles, transient overlays | Anything static that never overlays anything |

Rules when you do use it:

- Glass is a **material for things that float**, never a texture for things that sit still. If nothing scrolls beneath it, it is decoration and it is banned.
- Contrast is measured against the **worst-case backdrop**, not a friendly screenshot. Test the nav over a white image and over a black one. If either fails 4.5:1, add a scrim or a tint layer until both pass.
- Always ship a **solid fallback**: `@supports not (backdrop-filter: blur(1px))` gets an opaque surface at the same token color.
- Respect `prefers-reduced-transparency` alongside `prefers-reduced-motion`.
- Blur is expensive. Cap it to one or two glass layers per screen and never nest them.
- Do not stack glass on a gradient mesh. That combination is the single fastest route to looking generated.

### HIGH: Layout & Responsive
→ *Consult [spatial reference](reference/spatial-design.md), [responsive reference](reference/responsive-design.md), [platform reference](reference/platform-guidelines.md)*

- Mobile-first: base styles for small screens, `min-width` queries to enhance
- Visual rhythm through varied spacing. Tight groupings, generous separations.
- `clamp()` for fluid spacing
- Asymmetry. Break the grid intentionally for emphasis.
- Don't wrap everything in cards. Never nest cards.
- Left-aligned text with asymmetric layouts > centering everything
- Container queries (`@container`) for component-level responsiveness
- Safe areas: `env(safe-area-inset-*)` for notches, home indicators

### HIGH: Surface & Device Class
→ *Consult [responsive reference](reference/responsive-design.md), [platform reference](reference/platform-guidelines.md)*

Breakpoints were built on an assumption that is now breaking: that bigger means taller. The current generation of foldables opens to a display that is **wider and shorter**, and a whole product category has arrived with **no display at all**. Decide the device class in Step 0 and design to it.

**Class A: wide foldables**

The current fold generation (Galaxy Z Fold 8 and the Apple foldable widely expected to follow) closes to a narrow squarish cover screen and opens to a short, wide panel closer to a small tablet in landscape than to a large phone.

- Never key layout off width alone. Query **aspect ratio**. A 1.5 ratio at 800px wide is a different product than a 0.6 ratio at 800px wide.
- The dangerous state is short-and-wide. Vertical space is the scarce resource. Sticky headers plus sticky footers plus a keyboard can leave almost no content window.
- Prefer **two-pane list/detail** on unfold rather than one stretched column. A 900px measure of body text is a reading failure regardless of device.
- The cover screen is a real design target, not a degraded phone. Treat it as a glanceable surface: one primary action, no multi-step forms.
- Handle **continuity**: state must survive fold and unfold, mid-scroll and mid-input. Test the transition, not just the two end states.
- Respect hinge and posture APIs where the platform exposes them. Do not place a primary control under the fold.
- Test matrix additions: cover screen, unfolded, unfolded with keyboard raised, and the fold transition itself.

**Class B: screenless companions**

Rings, screenless fitness bands, and camera or audio glasses have no canvas. The interface moved off the device and into three places: the companion app, haptics, and a status light.

- **The companion app becomes the entire product surface.** All design effort concentrates there.
- **Density inverts.** Screenless wearables produce continuous data and no place to read it, so the companion app must show far more at one glance than a normal mobile app would. Think one dense summary surface with expandable detail, not a stack of generous cards each holding one number. Google Fit's Fitbit-era redesign is the reference: everything in one place, tap to expand.
- Read the [charts reference](reference/charts-and-data.md) before building this. Glanceable density lives or dies on micro-charts, not on stat cards with icons.
- **Haptics are the only output channel on-device.** Design a vibration vocabulary the way you would design a sound palette: distinct, few, learnable, documented in the DESIGN.md. Three patterns people can distinguish beats eight they cannot.
- **A status light is a communication system.** Camera-on indication on glasses is a privacy contract, not a decoration. It must be unambiguous, non-defeatable, and legible to bystanders as well as the wearer.
- **Input is gone.** No tap targets, no gestures, no confirmation dialogs. Anything requiring a decision has to be deferred to the phone or resolved by a sensible default. Design the default, then design how the user later discovers and corrects it.
- Notification discipline is the core UX problem. A device that can only buzz must earn every buzz.
- For glasses specifically: audio and location become primary output. Directions, context, and confirmations are spoken or spatial. Write those strings with the same care as UI copy. → [ux-writing reference](reference/ux-writing.md)

### MEDIUM: Typography & Color
→ *Consult [typography reference](reference/typography.md) for 57 pairings, [color reference](reference/color-and-contrast.md) for 161 palettes*

**Typography:**
- NEVER default to Inter, Roboto, Arial, Open Sans, Lato, Montserrat
- Modular type scale with fluid sizing (`clamp` for display, `rem` for body)
- Body: 16px minimum, 1.5+ line-height, max 65ch measure
- No monospace as lazy "technical" shorthand

**Color:**
- OKLCH for perceptually uniform palettes
- Tint neutrals toward brand hue (0.01 chroma)
- Never pure black (#000) or pure white (#fff)
- 60-30-10 rule: 60% neutral, 30% secondary, 10% accent
- Avoid the AI palette: cyan-on-dark, purple-to-blue gradients, neon accents
- **Gradient text via `background-clip: text` is banned outright.** Do not clip a gradient to text for "impact." Use weight and size to create emphasis instead.
- Dark mode is NOT inverted light mode

**Optional verification.** For anything shipping as live HTML, `npx impeccable detect <path or URL>` runs a zero-LLM scan against Impeccable's 59 deterministic anti-pattern rules. Useful as a final check alongside the AI Slop Test below, not a replacement for it.

### MEDIUM: Animation & Motion
→ *Consult [motion reference](reference/motion-design.md)*

- 100/300/500 rule: 100ms feedback, 300ms state changes, 500ms layout
- Animate ONLY `transform` and `opacity`. Height: `grid-template-rows: 0fr → 1fr`
- Exponential easing: `cubic-bezier(0.16, 1, 0.3, 1)` for entries
- Never bounce or elastic
- Stagger: `animation-delay: calc(var(--i) * 50ms)`

These rules govern **product UI without exception**. The narrow set of cases where compositor-only animation is not enough is handled by the expressive tier below, under explicit gates.

### MEDIUM: Forms & Feedback
→ *Consult [interaction reference](reference/interaction-design.md), [ux-writing reference](reference/ux-writing.md)*

- Visible labels always. Placeholders are NOT labels.
- Validate on blur, not every keystroke
- Error formula: What happened? Why? How to fix?
- Undo > confirmation dialogs for destructive actions

### HIGH: Navigation
→ *Consult [platform reference](reference/platform-guidelines.md)*

- Bottom nav: 5 items max (mobile)
- Consistent back behavior
- Deep linking support
- Skip links for keyboard users
- If the nav floats, it may use liquid glass under the rules in Style Selection above. It still needs a solid fallback and a worst-case contrast check.

### Charts & Data Visualization
→ *Consult [charts reference](reference/charts-and-data.md) for 25 chart types*

When the interface includes data:
- Chart type based on the QUESTION (comparison, trend, distribution, composition, relationship)
- Accessible: don't rely on color alone. Use patterns, labels, or both.
- Tooltips for detail-on-demand
- Responsive: simplify on mobile
- Always label axes. Always include units.
- For screenless-companion apps, invert the usual restraint. Dense multi-metric summaries with drill-down beat sparse one-number cards, because this app is the only place the data can be read.

---

## Step 3.5: The Expressive Tier (gated)

A set of high-craft techniques now separates memorable sites from competent ones: cinematic 3D carousels, endless and scattered gallery canvases, and shader-driven image distortion. Used well, they are the differentiation Step 2 asks for. Used by default, they are the next generation of slop and they will tank the performance budget.

**These are opt-in, not baseline. Every gate below must pass before you reach for them.**

### The gates

1. **Surface gate.** Permitted on hero sections, portfolios, marketing pages, launch and campaign pages, and case studies. **Banned on core navigation, dashboards, forms, settings, checkout, and any task-completion flow.** If a user has a job to finish, get out of the way.
2. **Fallback gate.** A complete, good-looking non-WebGL, non-animated version must exist and must be what ships to `prefers-reduced-motion: reduce`, unsupported contexts, and low-power conditions. Build the fallback first.
3. **Performance gate.** Declare the budget in the DESIGN.md before building. Hold 60fps on mid-tier hardware, not on your laptop. Lazy-init below the fold, tear down off-screen scenes, cap texture sizes, and never block first paint on a shader compile.
4. **Semantics gate.** Real DOM content underneath. Canvas is a presentation layer, never the only copy of the information.
5. **Narrative gate.** It has to mean something. The strongest examples of these techniques are storytelling devices where the motion carries the content forward. Motion with nothing to say is decoration.

### The techniques

**Cinematic 3D carousels.** On load, cards expand outward from center toward the edges rather than sliding in a flat row. The value is sequencing: the reveal orders the story. Keep the depth subtle enough that text stays legible, keep the sequence under roughly 800ms total, and make sure the carousel is fully operable by keyboard and swipe once the entrance completes.

**Endless and scattered galleries.** Two variants. The *endless* one loops a finite set of images (ten is plenty) into an apparently infinite scroll or drag with a sense of depth. The *scattered* one abandons the grid and places elements freely on a pannable canvas, closer to a Figma board than a page, with hover and click interactions per element. Both need: a visible affordance that the canvas is draggable, an escape route back to a linear list, virtualized rendering so offscreen items cost nothing, and a genuinely usable keyboard path. The best-in-class version of this is a zoomable spatial gallery where you pull back to an overview and dive into a single piece. That is also the most expensive thing in this document. Do not attempt it without the performance gate signed.

**Shader-driven image distortion.** Displacement, ripple, grain, and refraction applied to imagery, buttons, or type. Now within reach through mainstream tooling: shader support is arriving in mainstream design tools, and Unicorn Studio exports shader and distortion effects into HTML, Framer, or Webflow. Restraint is the whole game. One distorted hero image reads as art direction. Distortion on every image reads as a filter someone discovered. Distortion works when it is tied to brand meaning, and it fails when it is a texture applied uniformly. Never distort anything a user must read, and never distort a control's hit area away from its visual area.

### The expressive-tier slop test

The 2024 to 2025 tell was a purple gradient and a glass card. The next tell is a WebGL scene that could be dropped onto any brand without changing meaning. Ask: **if I swapped this effect onto a competitor's site, would anyone notice it was wrong?** If not, it is decoration. Cut it or tie it to the story.

---

## Step 4: Polish Pass (Phase 2 handoff to ui-polish)

A first build is rarely the shippable build. Once Step 3 is functionally complete, run a polish pass before delivery.

1. **Hand the DESIGN.md to `ui-polish`.** It reads the same tokens you produced, so refinement enforces the system rather than reinventing it. If the `ui-polish` skill is installed, invoke it now as the second pass.
2. **If `ui-polish` is not available**, apply its checklist inline. The high-impact moves, cheapest first:
   - Replace any emoji with one icon family (Lucide or Phosphor) at a consistent size and weight.
   - Re-anchor the palette on one considered hue, kill cyan-on-dark and purple-to-blue gradients, tint neutrals, and avoid pure black or white surfaces.
   - Swap decorative stat-card icons for functional micro-charts (sparkline, trend delta, mini bar).
   - Consolidate the sidebar to 5 to 7 items, and move settings-type routes into an account-card popover.
   - Collapse per-row buttons into a kebab menu, and use icons with tooltips over text chips.
   - Move creation flows into a modal with advanced options collapsed by default.
   - Rebuild billing as two columns with usage donuts and a recommended, differentiated plan set.
   - On landing pages, lead with stylized screenshots of the real product over generic icons.
   - Audit glass: every frosted surface must be a floating one. Anything static goes solid.
   - Audit the expressive tier: throttle the CPU to 4x in DevTools and re-check. If it stutters, it ships as the fallback.

The goal of Phase 2 is the AI-slop test below: it should be impossible to tell an AI made this.

## The AI Slop Test

If you showed this interface and said "AI made this," would they believe you immediately? If yes, redesign.

The DON'T guidelines above are the fingerprints of AI-generated work. The classic set is 2024 to 2025 vintage: purple-to-blue gradients, cyan on dark, emoji as icons, glass everywhere, Inter for everything. The emerging set is 2026 vintage: untethered WebGL scenes, uniform image distortion, liquid glass applied as texture rather than as material, and infinite galleries with no way out. Actively avoid both.

---

## Implementation Principles

- Match code complexity to aesthetic vision
- Every design should be different. Vary themes, fonts, aesthetics. NEVER converge on common choices.
- Customize component libraries aggressively. Default components are the enemy of distinctiveness.
- Test on real devices, not just DevTools
- Check contrast on dark/colored backgrounds. Text must be explicitly light-colored.
- Creativity and performance are not a trade-off to split. The reference-quality expressive work loads fast and runs smooth. If it is jittery, it is not finished.

## Multi-Stack Support
→ *Consult [platform reference](reference/platform-guidelines.md) for detailed guidance*

| Stack | Key patterns |
|-------|-------------|
| **React / Next.js** | CSS Modules, Tailwind, CSS-in-JS. Server components for perf. |
| **Vue / Nuxt** | Scoped styles, CSS variables, Nuxt UI. |
| **Svelte / SvelteKit** | Scoped CSS, transitions API, stores for theme. |
| **Tailwind / shadcn/ui** | Customize aggressively. Override default tokens. |
| **HTML/CSS** | Vanilla with custom properties. Progressive enhancement. |
| **React Native** | StyleSheet, Animated API, platform-specific files. |
| **Flutter** | ThemeData, Material 3, custom painters. |
| **SwiftUI** | Environment values, ViewModifiers, custom shapes. |

**Design-tool interchange.** Figma is not the only source of truth to expect any more. Penpot is open source, keeps design and team features free, and its files are the likely input when a client or partner is not on Figma. Shader and distortion assets increasingly arrive from Unicorn Studio as embeddable web output rather than as a static export. When a design source is named, ask what it exports before assuming a Figma pipeline.

## Pre-Delivery Checklist

1. **DESIGN.md produced**: All 9 sections populated, precedence chain respected, device class and motion budget declared, saved alongside output
2. Accessibility: contrast passes, keyboard works, screen reader tested
3. Responsive: tested at 320px, 768px, 1024px, 1440px+, plus aspect-ratio checks if the target includes foldables
4. Performance: images optimized (WebP/AVIF), CLS < 0.1
5. Light/dark mode: both work, contrast parity verified
6. AI Slop Test: would someone immediately say "AI made this"? If yes, iterate.
7. Touch targets: 44px minimum on all interactive elements
8. Empty states, loading states, error states: all designed
9. **DESIGN.md consistency**: final output matches DESIGN.md tokens (spot-check 3+ components against spec)
10. **Polish pass complete (ui-polish Phase 2)**: emoji removed, palette de-defaulted, micro-charts in place, sidebar consolidated, account card present, creation in a modal, billing humanized, landing uses real screenshots
11. **Glass audit**: every frosted surface floats over scrolling content, worst-case backdrop contrast passes, solid fallback present, reduced-transparency respected
12. **Expressive tier gates**: surface, fallback, performance, semantics, and narrative gates all signed, or the tier is not used
13. **Device class verified**: for foldables, cover screen and unfolded and the fold transition tested; for screenless companions, haptic vocabulary documented and glanceable density reviewed

