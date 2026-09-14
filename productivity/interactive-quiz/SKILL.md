---
name: interactive-quiz
description: >
  Create beautiful, interactive single-file HTML quizzes, surveys, and intake forms with diverse,
  creative interaction patterns that make people actually enjoy answering questions. Use this skill
  whenever the user wants to turn questions into something interactive — quizzes, surveys,
  questionnaires, intake forms, onboarding flows, feedback collectors, assessments, ICP alignment
  forms, client intake, team pulse checks, event RSVPs, self-assessments, or any scenario where
  someone needs to collect answers from others. Also trigger when the user says "make this fun",
  "turn these questions into a quiz", "interactive form", "collect feedback", or wants to gather
  information in a way that feels engaging rather than boring. This skill works with any AI agent
  that can write HTML files — no special tools, frameworks, or dependencies required.
---

# Interactive Quiz & Survey Builder

You create single-file HTML quizzes and surveys that feel delightful to fill out. The underlying
insight is simple: people give better, more thoughtful answers when they're enjoying the experience.
A boring form with 6 text inputs gets lazy one-word answers. A polished interactive experience with
tap-to-cycle tiles, tag builders, and animated concept cards gets genuine, thoughtful responses.

## Compatibility

This skill produces a single `.html` file with zero external dependencies (Google Fonts are the
only exception, and they degrade gracefully). The output works in any browser, on any device,
opened from a file URL or a web server. No build tools, no npm, no React — just vanilla HTML/CSS/JS.

Any AI agent that can write files can use this skill. No special tools required beyond file creation.

## Core Principle: Every Question Gets Its Own Interaction Pattern

The single most important thing this skill teaches is **interaction diversity**. When a quiz has
6 questions and they're all text inputs, or even all chip selectors, it feels monotonous. The
respondent's brain goes on autopilot and answers get shallow.

Instead, map each question to the interaction pattern that best fits its *nature*. A quiz with
6 questions should ideally use 4-6 different patterns. The variety keeps attention sharp because
each question feels like a fresh mini-experience.

## Workflow

### Step 1: Analyze Each Question

For every question the user provides, identify three things:

1. **Answer shape** — Is this a multi-select, single-select, ranking, free-text, allocation, or scale?
2. **Required or optional** — Does blocking submission on this question make sense?
3. **Best interaction fit** — Which pattern from the catalog below matches this answer shape?

### Step 2: Choose a Layout

| Questions | Layout | Why |
|-----------|--------|-----|
| 1–8 | **Scrollable** (all visible) | User sees everything upfront, feels fast, avoids nav bugs |
| 9–15 | **Sectioned** (groups of 3–4) | Groups related questions, progress per section |
| 16+ | **Paginated** (one at a time) | Prevents overwhelm |

Scrollable is almost always the right call for quizzes with 8 or fewer questions. The user glances
at the page and thinks "oh that's quick" — which means they actually start filling it out instead
of abandoning it.

### Step 3: Map Questions to Interaction Patterns

Here's the full catalog. Read `references/interaction-patterns.md` for implementation details
and CSS/JS snippets for each pattern.

#### Selection Patterns (choosing from options)

| Pattern | Best For | Feel |
|---------|----------|------|
| **Icon Chip Cards** | Multi-select from categories (industries, tools, skills) | Satisfying tap with emoji + count badge |
| **Priority Ranking Tiles** | When order/importance matters, not just selection | Tap-to-cycle: Skip → 🔥 Must Have → ⚡ Nice to Have |
| **Concept Cards** | Single-select from richly described options | Illustrated cards with icon + subtitle |
| **Scope Radar Cards** | Geographic/scope selection with visual metaphor | Horizontal cards with visual scope indicator |
| **Animated Radio Cards** | Single choice from 2–5 descriptive options | Expand/glow on selection, icon per option |

#### Input Patterns (creating/entering data)

| Pattern | Best For | Feel |
|---------|----------|------|
| **Tag Builder** | Building a list of items (exclusions, names, URLs) | Type + Enter creates removable pill tags |
| **Split Drop Zones** | Two parallel lists (attendees vs sponsors, pros vs cons) | Side-by-side tag inputs with separate counters |
| **Styled Textarea** | Open-ended responses, detailed notes | Floating label, char count, glow on focus |

#### Quantitative Patterns (measuring/rating)

| Pattern | Best For | Feel |
|---------|----------|------|
| **Gradient Slider** | Rating on a continuous spectrum | Draggable thumb with floating label |
| **Mixer Sliders** | Allocating a total (budget, time, priority %) | Linked sliders that sum to 100% |
| **Heat Map Grid** | Intensity across a matrix of categories | Tap cells to increase intensity (0→4 levels) |
| **2D Position Picker** | Two-dimensional questions (strategic vs tactical) | Drag a pin on an X/Y grid with labeled quadrants |

#### Binary/Toggle Patterns

| Pattern | Best For | Feel |
|---------|----------|------|
| **Swipe Cards** | Quick yes/no decisions across multiple items | Drag left/right with colored overlay |
| **Toggle Switch** | Simple on/off with nuance labels | Animated switch with contextual labels |

**The diversity rule:** If your quiz has N questions, aim for at least `ceil(N * 0.6)` different
patterns. A 6-question quiz should use at least 4 different patterns. If you catch yourself
reusing the same pattern three times, rethink — there's almost certainly a better fit for one of
those questions.

### Step 4: Build the HTML

Create a single self-contained HTML file. Everything inline — CSS in a `<style>` block, JS in a
`<script>` block. The only allowed external resource is Google Fonts (Outfit, Space Mono, Inter),
which degrades gracefully to system fonts if unavailable.

#### File Structure
```
<html>
├── <style>
│   ├── CSS custom properties (theming)
│   ├── Base styles + ambient effects
│   ├── Question card styles
│   ├── Per-pattern styles (chips, tiles, tags, etc.)
│   ├── Progress bar
│   ├── Summary panel
│   ├── Animations (@keyframes)
│   └── Responsive breakpoints
├── <body>
│   ├── Ambient glow elements (2–3 fixed blurred circles)
│   ├── Header (title, subtitle, time estimate)
│   ├── Progress bar with counter
│   ├── Question cards (each with number, title, subtitle, priority tag, interaction widget)
│   ├── Generate Summary button (disabled until required fields complete)
│   └── Summary panel (hidden until generated)
└── <script>
    ├── State object
    ├── Visited tracking for optional fields
    ├── Per-pattern event handlers
    ├── Progress calculation
    ├── Summary generation
    ├── Clipboard copy with fallback
    └── Reset function
```

#### The Premium Visual Feel (Impeccable Design Principles)

The quiz should look like a polished product — not generic AI output. Apply these principles from the Impeccable design language to avoid "AI slop":

**Typography** — Choose distinctive fonts, not Inter/Roboto/Arial. Good alternatives: Instrument Sans, Plus Jakarta Sans, Outfit, Figtree. Pair a display font with a body font only when you need genuine contrast. Use a modular type scale with `clamp()` for fluid headings. Use `font-variant-numeric: tabular-nums` for any numerical displays.

**Color** — Use OKLCH for perceptually uniform palettes. Tint neutrals toward your brand hue (even chroma 0.01 creates subconscious cohesion). Never use pure gray on colored backgrounds — use a shade of the background color. Never use pure black (#000) or pure white (#fff). Follow the 60-30-10 rule: 60% neutral backgrounds, 30% secondary, 10% accent. Avoid the AI palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds.

**Spatial design** — Use a 4pt spacing base (not 8pt). Create visual rhythm through varied spacing — tight groupings and generous separations. Don't wrap everything in cards; use spacing and alignment for grouping. Never nest cards inside cards. Use `gap` instead of margins for sibling spacing.

**Motion** — Focus on one well-orchestrated page load with staggered reveals (50ms per item, cap total at 500ms). Use exponential easing (`cubic-bezier(0.25, 1, 0.5, 1)` for ease-out-quart). Animate only `transform` and `opacity`. For accordions, use `grid-template-rows: 0fr → 1fr`. Never use bounce/elastic easing. Always respect `prefers-reduced-motion`.

**Grain overlay** — A subtle noise texture over the entire page at very low opacity (0.03). Adds tactile quality.

**Priority tags** — Color-coded pills on each question: red for "Critical", amber for "Important", cyan for "Nice to Have". Tells respondents where to focus energy.

**The AI Slop Test** — If you showed this quiz to someone and said "AI made this," would they believe you immediately? If yes, that's the problem. Review: no glassmorphism-for-its-own-sake, no gradient text on metrics, no identical card grids, no rounded rectangles with generic drop shadows.

#### Theming with CSS Custom Properties

Define all colors, spacing, and transitions as custom properties using OKLCH where possible. This makes rebranding trivial:

```css
:root {
  --bg: oklch(8% 0.01 270);
  --card: oklch(12% 0.015 270 / 0.85);
  --accent: oklch(55% 0.25 285);
  --accent-glow: oklch(55% 0.25 285 / 0.3);
  --text: oklch(92% 0.01 270);
  --text-dim: oklch(60% 0.02 270);
  --border: oklch(22% 0.015 270);
  --green: oklch(65% 0.2 145);
  --amber: oklch(72% 0.18 75);
  --rose: oklch(60% 0.22 15);
  --cyan: oklch(72% 0.15 210);
  /* Spacing scale (4pt base) */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 48px;
}
```

If the user specifies brand colors, adapt the `--accent` and related variables accordingly. Tint neutrals toward the accent hue for cohesion.

#### State Management

Use a single central state object. Each interaction pattern updates its portion of state and
calls `updateProgress()`. This keeps the data flow predictable and makes summary generation
straightforward.

```javascript
const state = { industries: [], titles_must: [], titles_nice: [], exclusions: [], ... };
const visited = {};  // Track optional field interactions
```

**Optional field tracking:** When a user focuses an optional field (even if they leave it blank),
mark it as visited. A visited-but-empty optional field counts as "answered" for progress purposes.
This prevents the annoying UX where optional fields block the submit button.

#### Summary & Clipboard

When "Generate Summary" is clicked, compile all state into a clean, copy-paste-ready text block.
Format it with clear headers and labels so it's useful when pasted into Slack, email, or a doc.

Use a 3-tier clipboard fallback:
1. `navigator.clipboard.writeText()` (modern API)
2. `document.execCommand('copy')` (legacy fallback)
3. Select-all prompt (last resort)

Show a brief toast notification on copy success.

#### Reset

Include a "Start Over" button that clears all state, resets all UI elements to default, hides
the summary, and re-enables the generate button. Test that every interaction pattern properly
resets — this is a common source of bugs.

### Step 5: Deliver

Save the file to the user's workspace with a descriptive name: `{Topic}_Quiz.html` or
`{Topic}_Survey.html`. Briefly describe which interaction pattern you used for each question
and why.

## JavaScript Anti-Patterns to Avoid

These bugs have been found in production quizzes. Understanding *why* they happen prevents them:

**DOM reference before append** — If you create an element and try to reference its children
before appending it to the DOM, those references will be null. Always `container.appendChild(el)`
first, then query its children.

**Variable shadowing in loops** — Using the same variable name (`card`) in an outer scope and
inside a `.forEach()` creates ambiguity about which `card` event listeners reference. Use
distinct names (`card` outer, `optCard` inner).

**Navigation button multiplication** — In paginated layouts, if you rebuild navigation buttons
inside the content area that gets cleared and re-rendered, buttons multiply with each render.
Solution: put navigation in a static container that never gets cleared.

**Overlapping absolutely-positioned elements** — Concentric circles, stacked cards, or layered
elements can intercept click events intended for elements underneath. If an inner element sits
on top of an outer element's center, clicks on the outer element's center hit the inner one
instead. Use non-overlapping layouts (horizontal cards, grids) when click targeting matters.

**`innerHTML +=` in loops** — This re-parses the entire DOM on every iteration. Build elements
with `createElement` or collect HTML fragments and insert once.

## Reference Files

- `references/interaction-patterns.md` — Full CSS/JS implementation for every interaction pattern.
  Read this when you need the actual code for a specific pattern.
- `assets/VertexGrid_ICP_Quiz.html` — A complete, tested example quiz with 6 different interaction
  patterns. Use as a reference for structure, styling, and state management patterns.
