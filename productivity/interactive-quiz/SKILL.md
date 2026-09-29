---
name: interactive-quiz
description: >-
  Create beautiful, interactive single-file HTML quizzes, surveys, questionnaires and intake forms with diverse, dopamine-designed interaction patterns people enjoy answering, including relational, spatial and nuanced capture (timeline, card sort, constellation, venn, sentence builder, confidence meter, emotional spectrum, before and after, relationship map, workflow sequence, bucket categorize). Use whenever questions need to become something interactive: quizzes, surveys, onboarding flows, feedback collectors, assessments, ICP alignment forms, client intake, team pulse checks, event RSVPs, self-assessments. Trigger on "make this fun", "turn these questions into a quiz", "interactive form", "collect feedback", "card sort", "timeline", "relationship map", "categorize", "sort into buckets". No frameworks or dependencies needed. Replaces interactive-quiz-v2.
---

## Extended patterns (absorbed from interactive-quiz-v2)

The core library below and `references/interaction-patterns.md` cover most questions. The v2 pattern notes are in `modes/interactive-quiz-v2/MODE.md`; read it when a question is about order, grouping, relationships, confidence or change over time and the core file lacks the pattern.

# Interactive Quiz & Survey Builder

You create single-file HTML quizzes and surveys that feel delightful to fill out. The underlying
insight is simple: people give better, more thoughtful answers when they're enjoying the experience.
A boring form with 6 text inputs gets lazy one-word answers. A polished interactive experience with
tap-to-cycle tiles, tag builders, constellation maps, and animated concept cards gets genuine,
thoughtful responses.

## Compatibility

This skill produces a single `.html` file with zero external dependencies (Google Fonts are the
only exception, and they degrade gracefully). The output works in any browser, on any device,
opened from a file URL or a web server. No build TOOLS, no npm, no React: vanilla HTML/CSS/JS.

Any AI agent that can write files can use this skill. No special tools required beyond file creation.

## Core Principle: Every Question Gets Its Own Interaction Pattern

The single most important thing this skill teaches is **interaction diversity**. When a quiz has
6 questions and they're all text inputs, or even all chip selectors, it feels monotonous. The
respondent's brain goes on autopilot and answers get shallow.

Instead, map each question to the interaction pattern that best fits its *nature*. A quiz with
6 questions should ideally use 4-6 different patterns. The variety keeps attention sharp because
each question feels like a fresh mini-experience.

## Psychology of Interaction Design

This is not a widget library. Each interaction pattern exploits a specific psychological mechanism
to extract better, more honest, more complete data from respondents. Understanding WHY each
pattern works is what separates a "form with fancy UI" from an instrument that reads people.

**Cognitive ease principle**: People give better answers when the answering mechanism matches
how they naturally think about the topic. Asking someone to "type your top 3 priorities" forces
serial recall under pressure. Showing them 8 bubbles they can tap to inflate lets them scan,
recognize, and respond in parallel. Recognition is always easier than recall.

**The IKEA effect**: When people physically manipulate elements (drag cards into slots, inflate
bubbles, draw connections), they invest effort and therefore value their answers more. A dragged
answer feels more "mine" than a clicked radio button. Use drag-based patterns (Timeline Sequencer,
Card Sorting, Constellation Builder) for questions where you need respondents to actually think.

**Variable reward loops**: When each question presents a novel interaction, the brain gets a
micro-hit of novelty reward. This is the same mechanism that makes social media feeds addictive.
Six different interaction types = six moments of "oh, what's this one?" Keep respondents in
discovery mode, not form-filling mode.

**Anchoring through physicality**: Sliders and position pickers anchor responses to a physical
space. A Gradient Slider from "Burned Out" to "Thriving" gives the respondent a felt sense of
where they are on a spectrum. A text input asking "rate your wellbeing 1-10" is abstract.
The physical metaphor produces more calibrated, less noisy data.

**Social desirability bypass**: Some questions trigger the "what's the right answer?" reflex.
Sentence Completers and Emotional Spectrum Bubbles bypass this because there's no obvious
"correct" choice. When the interaction feels like play rather than evaluation, people drop
their guard. Use these for sensitive topics (satisfaction, morale, preferences).

**Commitment escalation**: Start with low-effort patterns (Icon Chip Cards, Animated Radio Cards)
and progress to higher-effort ones (Tag Builder, Constellation Builder). By the time they reach
the harder interactions, respondents are already invested. Never front-load a Styled Textarea.

### Hard Rules

1. **Maximum ONE Styled Textarea per quiz.** If you have two open-ended questions, convert one
   to Sentence Completer, Swipe Cards, or Tag Builder. Free text is the laziest pattern and
   should only appear as a final "anything else?" catch-all.

2. **Maximum ONE Tag Builder per quiz.** Two tag inputs in a row feels like a form. If you need
   two list-building questions, make one a Split Drop Zone or Card Sorting instead.

3. **Zero plain text inputs.** Never use a raw `<input type="text">` as a primary interaction.
   The only acceptable text inputs are: the "Other" field inside an Icon Chip Card, the tag
   input inside a Tag Builder, or the custom option inside a Concept Card. If a question seems
   to require free text, challenge that assumption: can it be a Sentence Completer? A Swipe Card
   batch? A Tag Builder?

4. **Drag-based patterns must work on touch AND desktop.** Every drag interaction (Timeline
   Sequencer, Card Sorting, Constellation Builder, Venn Selector) MUST implement a click-based
   fallback: click to select (item glows), click destination to place. This is non-negotiable.
   HTML5 drag-and-drop alone will break on mobile.

5. **Front-load low-effort, back-load high-effort.** First 1-2 questions should be tappable
   (chips, radio cards, concept cards). Middle questions can be sliders, bubbles, or sentence
   completers. Drag/build patterns go near the end. The Styled Textarea (if used) is always last.

### Psychological Pattern Mapping

When analyzing a question, don't just ask "what widget fits?" Ask "what psychological mechanism
extracts the best answer?"

| What You Need | Psychology | Best Pattern |
|---------------|-----------|--------------|
| Quick multi-select with low cognitive load | Recognition over recall | Icon Chip Cards |
| Prioritization with nuance (not just yes/no) | Graduated commitment | Priority Ranking Tiles |
| Single choice where options need explanation | Informed decision-making | Concept Cards, Animated Radio Cards |
| Building a custom list | IKEA effect (creation = ownership) | Tag Builder |
| Rating where "I'm not sure" matters | Metacognitive awareness | Confidence Meter |
| Allocation with real tradeoffs | Loss aversion (moving one slider costs another) | Mixer Sliders |
| Independent feelings (no forced tradeoff) | Parallel processing, social desirability bypass | Emotional Spectrum Bubbles |
| Temporal ordering | Spatial-temporal cognition | Timeline Sequencer |
| Classification into categories | Gestalt grouping instinct | Card Sorting |
| Relationship mapping | Systems thinking, spatial reasoning | Constellation Builder |
| Structured preference without "right answer" | Social desirability bypass, playfulness | Sentence Completer |
| Quick binary judgments across many items | Decision fatigue reduction via simplification | Swipe Cards |
| Overlapping category membership | Nuanced thinking, resist false dichotomies | Venn Selector |
| Comparing two options visually | Direct comparison, anchoring | Before/After Toggle |
| Multi-dimensional rating | Spatial anchoring, nuance capture | Heat Map Grid, 2D Position Picker |

## Workflow

### Step 1: Analyze Each Question

For every question the USER provides, identify three things:

1. **Answer shape**: Is this a multi-select, single-select, ranking, free-text, allocation, scale,
   sequence, categorization, relationship map, or visual preference?
2. **Required or optional**: Does blocking submission on this question make sense?
3. **Best interaction fit**: Which pattern from the catalog below matches this answer shape?

### Step 2: Choose a Layout

| Questions | Layout | Why |
|-----------|--------|-----|
| 1-8 | **Scrollable** (all visible) | User sees everything upfront, feels fast, avoids nav bugs |
| 9-15 | **Sectioned** (groups of 3-4) | Groups related questions, progress per section |
| 16+ | **Paginated** (one at a time) | Prevents overwhelm |

Scrollable is almost always the right call for quizzes with 8 or fewer questions. The user glances
at the page and thinks "oh that's quick", which means they actually start filling it out instead
of abandoning it.

### Step 3: Map Questions to Interaction Patterns

Here is the full catalog of 21 interaction patterns organized by category. Read
`references/interaction-patterns.md` for implementation details and CSS/JS snippets for each one.

#### Selection Patterns (choosing from options)

| Pattern | Best For | Feel |
|---------|----------|------|
| **Icon Chip Cards** | Multi-select from categories (industries, tools, skills) | Satisfying tap with emoji + count badge |
| **Priority Ranking Tiles** | When order/importance matters, not just selection | Tap-to-cycle: Skip > Must Have > Nice to Have |
| **Concept Cards** | Single-select from richly described options | Illustrated cards with icon + subtitle |
| **Scope Radar Cards** | Geographic/scope selection with visual metaphor | Horizontal cards with visual scope indicator |
| **Animated Radio Cards** | Single choice from 2-5 descriptive options | Expand/glow on selection, icon per option |

#### Input Patterns (creating/entering data)

| Pattern | Best For | Feel |
|---------|----------|------|
| **Tag Builder** | Building a list of items (exclusions, names, URLs) | Type + Enter creates removable pill tags |
| **Split Drop Zones** | Two parallel lists (attendees vs sponsors, pros vs cons) | Side-by-side tag inputs with separate counters |
| **Styled Textarea** | Open-ended responses, detailed notes | Floating label, char count, glow on focus |
| **Sentence Completer** | Structured preferences with inline choices | Fill-in-the-blank with tap-to-select word slots |

#### Quantitative Patterns (measuring/rating)

| Pattern | Best For | Feel |
|---------|----------|------|
| **Gradient Slider** | Rating on a continuous spectrum | Draggable thumb with floating label |
| **Mixer Sliders** | Allocating a total (budget, time, priority %) | Linked sliders that sum to 100% |
| **Heat Map Grid** | Intensity across a matrix of categories | Tap cells to increase intensity (0-4 levels) |
| **2D Position Picker** | Two-dimensional questions (strategic vs tactical) | Drag a pin on an X/Y grid with labeled quadrants |
| **Confidence Meter** | Answer + certainty level as dual track | Dual slider: one for answer, one for confidence |
| **Emotional Spectrum Bubbles** | Independent intensity ratings (no tradeoff) | Tap bubbles to inflate; each grows independently |

#### Relational / Spatial Patterns (ordering, grouping, mapping)

| Pattern | Best For | Feel |
|---------|----------|------|
| **Timeline Sequencer** | Ordering steps in a workflow or process | Drag cards into horizontal timeline slots |
| **Card Sorting** | Categorizing items into labeled buckets | Drag unsorted pile into 2-4 labeled columns |
| **Constellation Builder** | Mapping relationships between entities | Place dots on freeform canvas, draw connections |
| **Venn Selector** | Items that belong to overlapping categories | Drop items into overlapping circle zones |

#### Binary / Toggle / Comparison Patterns

| Pattern | Best For | Feel |
|---------|----------|------|
| **Swipe Cards** | Quick yes/no decisions across multiple items | Drag left/right with colored overlay |
| **Before/After Toggle** | Visual preference between two states | Toggle/crossfade between two views with preference selector |

**The diversity rule (STRICT):** If your quiz has N questions, you MUST use at least `ceil(N * 0.7)`
different patterns. A 6-question quiz must use at least 5 different patterns. A 5-question quiz
must use at least 4. You may NEVER reuse the same pattern more than twice, period. If you find
yourself reaching for the same pattern a third time, stop and find the psychologically correct
alternative from the mapping table above.

**The anti-text rule (STRICT):** A quiz with 6 questions should have AT MOST 1 text-based
interaction (Styled Textarea or Tag Builder). The remaining 5 must be visual/spatial/interactive
patterns. If more than 20% of your quiz is text-entry, you have failed at interaction design.

### Pattern Selection Heuristic

For each question, run through this decision tree IN ORDER. Take the first match. The tree is
ordered from most-specific (best UX) to most-generic (acceptable fallback).

```
TIER 1: SPATIAL/RELATIONAL (highest engagement, use whenever possible)
  Is the answer about TEMPORAL SEQUENCE?
    -> Timeline Sequencer (drag cards into order)
  Is the answer about SORTING INTO CATEGORIES?
    -> Card Sorting (exclusive buckets) or Venn Selector (overlapping membership)
  Is the answer about RELATIONSHIPS or CONNECTIONS?
    -> Constellation Builder (draw lines between nodes on a canvas)

TIER 2: NUANCED CAPTURE (high engagement, captures subtlety)
  Does the answer have uncertainty or confidence dimension?
    -> Confidence Meter (dual slider: answer + how sure)
  Is the answer about INDEPENDENT FEELINGS toward multiple items?
    -> Emotional Spectrum Bubbles (tap to inflate, no forced tradeoff)
  Is the answer a structured preference with nuance?
    -> Sentence Completer (tap-to-cycle inline word slots)
  Is the answer comparing two options/states?
    -> Before/After Toggle (crossfade between views)

TIER 3: INTERACTIVE SELECTION (medium engagement)
  Is the answer about PRIORITIZATION (not just selection)?
    -> Priority Ranking Tiles (tap-to-cycle: Skip > Must Have > Nice to Have)
  Is the answer about ALLOCATION with tradeoffs?
    -> Mixer Sliders (linked sliders summing to 100%)
  Is the answer a RATING on a spectrum?
    -> Gradient Slider (draggable thumb with floating label)
  Is the answer about INTENSITY across a matrix?
    -> Heat Map Grid (tap cells to increase intensity)
  Is the answer a quick YES/NO across many items?
    -> Swipe Cards (drag left/right)

TIER 4: SELECTION (baseline interactive)
  Is the answer a SINGLE CHOICE from rich options?
    -> Concept Cards (icon + title + description) or Animated Radio Cards
  Is the answer MULTI-SELECT from a list?
    -> Icon Chip Cards (emoji + label, tap to toggle)
  Is the answer about GEOGRAPHIC SCOPE?
    -> Scope Radar Cards (expanding scope visual)

TIER 5: TEXT (last resort, max 1 per quiz)
  Does the user need to BUILD A LIST of custom items?
    -> Tag Builder (type + Enter = pill tag)
  Does the user need to provide TWO PARALLEL LISTS?
    -> Split Drop Zones (side-by-side tag inputs)
  Is this genuinely open-ended with no structure possible?
    -> Styled Textarea (ONLY as final question, max 1 per quiz)
```

**IMPORTANT: Before defaulting to Tier 5, ask yourself: "Can I restructure this as a Tier 1-3
pattern?" Almost always, yes.** "Tell us about your ideal customer" is NOT a textarea question.
It's a Sentence Completer: "My ideal customer is a [tap: CTO/VP Sales/Director] at a
[tap: startup/mid-market/enterprise] company in [tap: tech/healthcare/finance] who struggles
with [tap: lead gen/data quality/outreach]." Same data, ten times more engaging, ten times
more structured.

### Step 4: Build the HTML

Create a single self-contained HTML file. Everything inline: CSS in a `<style>` block, JS in a
`<script>` block. The only allowed external resource is Google Fonts (Outfit, Space Mono, Inter),
which degrades gracefully to system fonts if unavailable.

#### File Structure
```
<html>
  <style>
    CSS custom properties (theming)
    Base styles + ambient effects
    Question card styles
    Per-pattern styles (chips, tiles, tags, timeline, constellation, etc.)
    Progress bar
    Summary panel
    Animations (@keyframes)
    Responsive breakpoints
  </style>
  <body>
    Ambient glow elements (2-3 fixed blurred circles)
    Header (title, subtitle, time estimate)
    Progress bar with counter
    Question cards (each with number, title, subtitle, priority tag, interaction widget)
    Generate Summary button (disabled until required fields complete)
    Summary panel (hidden until generated)
  </body>
  <script>
    State object
    Visited tracking for optional fields
    Per-pattern event handlers
    Progress calculation
    Summary generation
    Clipboard copy with fallback
    Reset function
  </script>
</html>
```

#### Dopamine Design System

The quiz must feel addictive to fill out. Not just "polished" but genuinely fun. Every single
interaction should produce a micro-reward that makes the user want to interact with the next
element. Think mobile game UX, not enterprise form.

**The core loop:** Action -> Instant visual feedback -> Satisfaction -> Curiosity about the next
question. If any interaction feels flat or "form-like," you've broken the loop.

##### Ambient Foundation (the backdrop that says "this isn't a boring form")

**Ambient background glow**: 2-3 fixed, blurred circles (200-400px diameter, 0.15-0.25 opacity)
using accent [[colors]]. Slowly animate their position with CSS keyframes (30-60s cycle, subtle drift).
This creates a living, breathing background.

**Grain overlay**: Noise texture at 0.03 opacity. Adds tactile quality. Use a CSS SVG filter
or a tiny base64 noise image.

**Stagger entrance animations**: Each question card fades in and slides up with increasing delay.
Use `animation: fadeSlideUp 0.6s ease forwards; animation-delay: calc(var(--i) * 0.12s);` where
`--i` is the question [[INDEX]]. The stagger creates a waterfall reveal that feels alive.

**Glassmorphism cards**: `backdrop-filter: blur(20px)`, semi-transparent backgrounds, and a
1px border with rgba(255,255,255,0.06). Cards should feel like they float.

##### Micro-Reward Animations (the dopamine triggers)

Every interaction MUST have at least two of these feedback layers:

**Scale bounce on selection**: When an item is selected (chip, card, bubble), use
`transform: scale(1.08)` with `cubic-bezier(0.34, 1.56, 0.64, 1)` easing. The overshoot
(1.56) creates a "pop" that feels physical, like pressing a real button.

**Glow pulse on state change**: When anything changes state, its `box-shadow` should briefly
intensify. Use a CSS animation: `@keyframes glowPulse { 0% { box-shadow: 0 0 0 rgba(...) }
50% { box-shadow: 0 0 30px rgba(...) } 100% { box-shadow: 0 0 15px rgba(...) } }`. Duration:
0.4s. This "flash" signals success.

**Color transition, not color swap**: Never instantly change [[colors]]. Always use `transition`
(0.25-0.35s). The eye catches the movement and interprets it as responsiveness.

**Count/progress celebrations**: When the progress bar hits 25%, 50%, 75%, and 100%, trigger
a brief accent-colored pulse across the bar. At 100%, the Generate Summary button should
animate in with a glow effect. The bar itself should use a gradient that subtly shifts.

**Particle-like micro-effects**: When a chip is selected, briefly spawn 3-5 tiny dots that
expand outward and fade (use CSS animations on pseudo-elements or spawned spans). These take
<50ms to trigger and 0.5s to fade. Subtle but they make selections feel "alive."

**Completion confetti state**: When "Generate Summary" is clicked, briefly animate the
background glows (increase opacity and speed for 1s) before showing the summary panel.
This marks the transition from "working" to "done" and feels rewarding.

##### Interaction-Specific Dopamine Hooks

**Icon Chip Cards**: On selection, the chip does a quick scale-bounce (0.15s) and the count
badge increments with a digit-roll animation (number slides up, new number slides in from below).

**Priority Ranking Tiles**: Each tier change triggers a color wash animation. The tile's
background color doesn't just switch. It ripples outward from the click point using a radial
gradient transition.

**Gradient Slider**: The thumb leaves a faint trail glow as it moves. The floating label should
fade-scale in from 0.8 to 1.0 on each position change.

**Emotional Spectrum Bubbles**: Each level-up should feel like inflation. Use `cubic-bezier(0.34,
1.56, 0.64, 1)` on the size transition so the bubble slightly overshoots then settles. At
level 3 (Essential), add a subtle continuous pulse animation to the glow.

**Card Sorting / Timeline Sequencer**: When an item is placed in a slot/column, the slot should
briefly flash its border color brighter (0.3s). The item should "land" with a subtle bounce
(translateY overshoot). When ALL slots are filled, animate the entire track border to green.

**Sentence Completer**: Each word-cycle should slide the old word up and the new word in from
below (like a slot machine reel). Duration: 0.2s. This turns a simple click into a satisfying
mechanical interaction.

##### Typography That Pops

Use **Outfit** (or Inter) for body text and **Space Mono** for technical elements (counts,
percentages, labels). The contrast between a clean sans-serif and a monospace font creates
visual hierarchy that feels intentional and techy.

Question numbers should be oversized (2rem+), low-opacity monospace. They create rhythm
without competing for attention.

##### Priority Tags (visual urgency cues)

Color-coded pills on each question: rose for "Critical", amber for "Important", cyan for
"Nice to Have". These create urgency hierarchy and tell respondents where to invest thought.
Tags should have a subtle left-border accent line on the question card matching the tag color.

#### Theming with CSS Custom Properties

Define all [[colors]], spacing, and transitions as custom properties at the top. This makes rebranding
trivial: change 5 variables and the whole quiz adapts.

```css
:root {
  --bg: #0a0a0f;
  --card: rgba(18,18,26,0.85);
  --accent: #7c3aed;
  --accent-glow: rgba(124,58,237,0.3);
  --accent-soft: rgba(124,58,237,0.08);
  --text: #e4e4eb;
  --text-dim: #8888a0;
  --border: #2a2a3a;
  --green: #22c55e;
  --amber: #f59e0b;
  --rose: #f43f5e;
  --cyan: #06b6d4;
}
```

If the user specifies brand [[colors]], adapt the `--accent` and related variables accordingly.

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
resets: this is a common source of bugs, especially for drag-based patterns like Timeline
Sequencer, Card Sorting, and Constellation Builder where DOM elements move around.

### Step 5: Deliver

Save the file to the user's workspace with a descriptive name: `{Topic}_Quiz.html` or
`{Topic}_Survey.html`. Briefly describe which interaction pattern you used for each question
and why.

## JavaScript Anti-Patterns to Avoid

These bugs have been found in production quizzes. Understanding *why* they happen prevents them:

**DOM reference before append**: If you create an element and try to reference its children
before appending it to the DOM, those references will be null. Always `container.appendChild(el)`
first, then query its children.

**Variable shadowing in loops**: Using the same variable name (`card`) in an outer scope and
inside a `.forEach()` creates ambiguity about which `card` event listeners reference. Use
distinct names (`card` outer, `optCard` inner).

**Navigation button multiplication**: In paginated layouts, if you rebuild navigation buttons
inside the content area that gets cleared and re-rendered, buttons multiply with each render.
Solution: put navigation in a static container that never gets cleared.

**Overlapping absolutely-positioned elements**: Concentric circles, stacked cards, or layered
elements can intercept click events intended for elements underneath. If an inner element sits
on top of an outer element's center, clicks on the outer element's center hit the inner one
instead. Use non-overlapping layouts (horizontal cards, grids) when click targeting matters.

**`innerHTML +=` in loops**: This re-parses the entire DOM on every iteration. Build elements
with `createElement` or collect HTML fragments and insert once.

**Drag-and-drop MUST use click-to-place as the primary mechanism, NOT HTML5 drag-and-drop.**
HTML5 `draggable` + `dragstart`/`dragover`/`drop` is broken on mobile, inconsistent across
browsers, and produces janky UX. Instead, implement ALL drag-like patterns using this universal
click-to-place approach:

1. User clicks/taps an item in the source pool. Item gets a `.selected` class (glow effect).
2. User clicks/taps a destination slot/column. Item moves to that destination with a CSS
   transition animation.
3. Clicking a placed item returns it to the pool (or opens it for re-placement).
4. This works identically on desktop AND mobile with zero additional code.

Optionally, you CAN add mouse-drag enhancement on top (using `mousedown`/`mousemove`/`mouseup`),
but the click-to-place must always work as the baseline. Test by clicking only, never dragging.

**The concrete implementation pattern for click-to-place:**
```javascript
let selectedItem = null;
pool.querySelectorAll('.item').forEach(item => {
  item.addEventListener('click', () => {
    if (selectedItem === item) { item.classList.remove('selected'); selectedItem = null; return; }
    if (selectedItem) selectedItem.classList.remove('selected');
    selectedItem = item;
    item.classList.add('selected');
  });
});
slots.forEach(slot => {
  slot.addEventListener('click', () => {
    if (!selectedItem) return;
    slot.appendChild(selectedItem);
    selectedItem.classList.remove('selected');
    selectedItem.classList.add('placed');
    selectedItem = null;
    updateState();
  });
});
```

**SVG line coordinate drift**: When drawing connection lines in Constellation Builder, use
`getBoundingClientRect()` relative to the canvas container, not absolute page coordinates.
Recalculate on every node reposition to keep lines attached.

## Reference Files

- `references/interaction-patterns.md`: Full CSS/JS implementation for every interaction pattern
  (all 21 patterns). Read this when you need the actual code for a specific pattern. The file
  has a table of contents: jump directly to the pattern you need.
- `assets/VertexGrid_ICP_Quiz.html`: A complete, tested example quiz with 6 different interaction
  patterns. Use as a reference for structure, styling, and state management patterns.
