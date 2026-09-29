# Interaction Pattern Implementation Reference

Full CSS/JS implementation details for every interaction pattern. Read this when building a
specific pattern. Patterns are organized by category.

## Dopamine CSS Kit (include in EVERY quiz)

These reusable animations and utilities make interactions feel alive. Include them in the
`<style>` block of every quiz. Individual patterns reference these by class name.

```css
/* === DOPAMINE ANIMATIONS === */

/* Scale bounce: used on selection (chips, cards, bubbles) */
@keyframes popIn {
  0% { transform:scale(0.85); opacity:0; }
  60% { transform:scale(1.08); }
  100% { transform:scale(1); opacity:1; }
}

/* Glow pulse: used on state changes */
@keyframes glowPulse {
  0% { box-shadow:0 0 0 transparent; }
  50% { box-shadow:0 0 25px var(--accent-glow); }
  100% { box-shadow:0 0 12px var(--accent-glow); }
}

/* Fade + slide up: used for card entrance stagger */
@keyframes fadeSlideUp {
  from { opacity:0; transform:translateY(20px); }
  to { opacity:1; transform:translateY(0); }
}

/* Count badge bump: used when a counter changes */
@keyframes countBump {
  0% { transform:scale(1); }
  50% { transform:scale(1.4); color:var(--accent); }
  100% { transform:scale(1); }
}

/* Ripple expansion: used on tile/card click for color wash effect */
@keyframes rippleOut {
  0% { transform:scale(0); opacity:0.4; }
  100% { transform:scale(2.5); opacity:0; }
}

/* Slot machine reel: used for Sentence Completer word cycling */
@keyframes slotUp {
  0% { transform:translateY(0); opacity:1; }
  40% { transform:translateY(-100%); opacity:0; }
  60% { transform:translateY(100%); opacity:0; }
  100% { transform:translateY(0); opacity:1; }
}

/* Ambient glow drift: used for background blobs */
@keyframes ambientDrift {
  0%, 100% { transform:translate(0, 0) scale(1); }
  33% { transform:translate(30px, -20px) scale(1.05); }
  66% { transform:translate(-20px, 15px) scale(0.95); }
}

/* Success flash: used on progress milestones */
@keyframes successFlash {
  0% { background-position:0% 50%; }
  50% { background-position:100% 50%; }
  100% { background-position:0% 50%; }
}

/* Bubble inflate with overshoot */
@keyframes bubbleInflate {
  0% { transform:scale(1); }
  60% { transform:scale(1.15); }
  100% { transform:scale(1); }
}

/* Landing bounce: used when items are placed in slots/columns */
@keyframes landBounce {
  0% { transform:translateY(-8px); opacity:0.7; }
  60% { transform:translateY(3px); }
  100% { transform:translateY(0); opacity:1; }
}

/* The magic easing: use this on all selection transitions */
:root {
  --bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --smooth: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Micro-particle burst (attach to ::after pseudo-element on selected items) */
.micro-burst::after {
  content:''; position:absolute; inset:-4px; border-radius:inherit;
  background:radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
  opacity:0; animation:glowPulse 0.4s var(--bounce) forwards;
  pointer-events:none; z-index:-1;
}

/* Progress bar celebration at milestones */
.progress-bar.milestone {
  animation:successFlash 0.8s ease;
  background-size:200% 100%;
}
```

**Usage:** Reference these in each pattern's CSS. For example, when a chip is selected:
`.icon-chip.selected { animation: popIn 0.25s var(--bounce); }`. When a sort item lands
in a column: `.sort-item.just-landed { animation: landBounce 0.3s var(--smooth); }`.

## Table of Contents

### Selection Patterns
1. [Icon Chip Cards](#icon-chip-cards)
2. [Priority Ranking Tiles](#priority-ranking-tiles)
3. [Concept Cards](#concept-cards)
4. [Scope Radar Cards](#scope-radar-cards)
5. [Animated Radio Cards](#animated-radio-cards)

### Input Patterns
6. [Tag Builder](#tag-builder)
7. [Split Drop Zones](#split-drop-zones)
8. [Styled Textarea](#styled-textarea)
9. [Sentence Completer](#sentence-completer)

### Quantitative Patterns
10. [Gradient Slider](#gradient-slider)
11. [Mixer Sliders](#mixer-sliders)
12. [Heat Map Grid](#heat-map-grid)
13. [2D Position Picker](#2d-position-picker)
14. [Confidence Meter](#confidence-meter)
15. [Emotional Spectrum Bubbles](#emotional-spectrum-bubbles)

### Relational / Spatial Patterns
16. [Timeline Sequencer](#timeline-sequencer)
17. [Card Sorting](#card-sorting)
18. [Constellation Builder](#constellation-builder)
19. [Venn Selector](#venn-selector)

### Binary / Toggle / Comparison Patterns
20. [Swipe Cards](#swipe-cards)
21. [Before/After Toggle](#beforeafter-toggle)

### Output
22. [Summary Generation](#summary-generation)

---

## Icon Chip Cards

**When to use:** Multi-select from 4-20 predefined categories (industries, TOOLS, skills, topics).

**Structure:** Grid of rounded cards, each with an emoji icon and a label. Tapping toggles
selection with a satisfying scale + glow animation. Shows a count badge ("3 selected") and
supports an "Other" text input.

**Key HTML:**
```html
<div class="icon-chip-grid">
  <div class="icon-chip" data-value="IT/ITES">
    <span class="ic-emoji">💻</span>
    <span class="ic-label">IT / ITES</span>
  </div>
  <!-- more chips... -->
</div>
<div class="chip-count" id="industryCount">0 selected</div>
<input class="text-input-mini" id="industryOther" placeholder="Others? Type here..." />
```

**Key CSS:**
```css
.icon-chip-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(130px,1fr)); gap:10px; }
.icon-chip {
  display:flex; flex-direction:column; align-items:center; gap:6px;
  padding:16px 12px; border-radius:14px; cursor:pointer;
  border:2px solid var(--border); background:rgba(255,255,255,0.02);
  transition:all 0.25s ease; user-select:none;
}
.icon-chip:hover { border-color:var(--border-accent); transform:translateY(-2px); }
.icon-chip.selected {
  border-color:var(--green); background:rgba(34,197,94,0.08);
  box-shadow:0 0 20px var(--green-glow); transform:scale(1.03);
}
.ic-emoji { font-size:1.6rem; }
.ic-label { font-size:0.78rem; color:var(--text-dim); text-align:center; }
.chip-count {
  font-family:'Space Mono',monospace; font-size:0.75rem; color:var(--green);
  opacity:0; transition:opacity 0.3s;
}
.chip-count.visible { opacity:1; }
```

**Key JS:**
```javascript
document.querySelectorAll('.icon-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    chip.classList.toggle('selected');
    const selected = [...document.querySelectorAll('.icon-chip.selected')]
      .map(c => c.dataset.value);
    state.industries = selected;
    const countEl = document.getElementById('industryCount');
    countEl.textContent = selected.length + ' selected';
    countEl.classList.toggle('visible', selected.length > 0);
    updateProgress();
  });
});
```

---

## Priority Ranking Tiles

**When to use:** When you need to know not just *which* items matter, but *how much* they matter.
Instead of a flat multi-select, this lets respondents assign priority tiers.

**Behavior:** Tap once = Must Have (level 1, red). Tap again = Nice to Have (level 2, amber).
Tap a third time = back to unselected (level 0). Each tile shows its current level label.

**Key HTML:**
```html
<div class="priority-grid">
  <div class="priority-tile" data-value="CIO" data-level="0">
    <div class="pt-title">CIO</div>
    <div class="pt-level"></div>
  </div>
  <!-- more tiles... -->
</div>
<div class="priority-legend">
  <span><span class="dot" style="background:var(--rose)"></span> Must Have</span>
  <span><span class="dot" style="background:var(--amber)"></span> Nice to Have</span>
  <span><span class="dot" style="background:var(--border)"></span> Skip</span>
</div>
```

**Key CSS:**
```css
.priority-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr)); gap:10px; }
.priority-tile {
  padding:18px 14px; border-radius:12px; text-align:center; cursor:pointer;
  border:2px solid var(--border); background:rgba(255,255,255,0.02);
  transition:all 0.25s ease; user-select:none;
}
.priority-tile[data-level="1"] {
  border-color:var(--rose); background:rgba(244,63,94,0.1);
  box-shadow:0 0 15px rgba(244,63,94,0.2);
}
.priority-tile[data-level="2"] {
  border-color:var(--amber); background:rgba(245,158,11,0.1);
  box-shadow:0 0 15px rgba(245,158,11,0.15);
}
.pt-title { font-weight:600; font-size:0.95rem; }
.pt-level { font-size:0.7rem; margin-top:6px; min-height:1.2em; }
```

**Key JS:**
```javascript
document.querySelectorAll('.priority-tile').forEach(tile => {
  tile.addEventListener('click', () => {
    let level = parseInt(tile.dataset.level);
    level = (level + 1) % 3;
    tile.dataset.level = level;
    const labels = ['', '🔥 MUST HAVE', '⚡ NICE TO HAVE'];
    tile.querySelector('.pt-level').textContent = labels[level];
    state.titles_must = [...document.querySelectorAll('.priority-tile[data-level="1"]')]
      .map(t => t.dataset.value);
    state.titles_nice = [...document.querySelectorAll('.priority-tile[data-level="2"]')]
      .map(t => t.dataset.value);
    updateProgress();
  });
});
```

---

## Concept Cards

**When to use:** Single-select from options that need more description than a simple label.
Each option is a card with an icon, title, and subtitle. Useful for event themes, plan tiers,
approach options.

**Key CSS:**
```css
.concept-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:12px; }
.concept-card {
  padding:20px 14px; border-radius:14px; text-align:center; cursor:pointer;
  border:2px solid var(--border); background:rgba(255,255,255,0.02);
  transition:all 0.3s ease;
}
.concept-card:hover { border-color:var(--border-accent); transform:translateY(-3px); }
.concept-card.selected {
  border-color:var(--accent); background:var(--accent-soft);
  box-shadow:0 0 25px var(--accent-glow);
}
.cc-icon { font-size:2rem; margin-bottom:8px; }
.cc-title { font-weight:600; font-size:0.9rem; }
.cc-desc { font-size:0.7rem; color:var(--text-dim); margin-top:4px; }
```

**Behavior:** Only one card can be selected at a time. Clicking a selected card deselects it.
Include a "Custom" text input below that clears the card selection when the USER types.

---

## Scope Radar Cards

**When to use:** Geographic scope, reach levels, or any selection where each option represents
an expanding scope. Each card has a mini radar/scope icon that visually represents the
breadth of the selection.

**Structure:** Horizontal stacked cards, each with a small radar icon (3 concentric rings),
title, description, and an estimated reach/count badge. Each scope level gets its own color.

**Key CSS:**
```css
.scope-radar { display:flex; flex-direction:column; gap:8px; }
.scope-option {
  display:flex; align-items:center; gap:16px; padding:14px 18px;
  border-radius:12px; cursor:pointer; border:2px solid var(--border);
  background:rgba(255,255,255,0.02); transition:all 0.3s ease;
}
.scope-option.selected { transform:translateX(4px); }
.scope-option[data-scope="1"].selected { border-color:var(--accent); background:rgba(124,58,237,0.08); }
.scope-option[data-scope="2"].selected { border-color:var(--cyan); background:rgba(6,182,212,0.08); }
.scope-option[data-scope="3"].selected { border-color:var(--amber); background:rgba(245,158,11,0.08); }
.scope-option[data-scope="4"].selected { border-color:var(--green); background:rgba(34,197,94,0.08); }
.scope-reach {
  margin-left:auto; font-family:'Space Mono',monospace; font-size:0.7rem;
  padding:3px 10px; border-radius:20px; border:1px solid var(--border);
}
```

**Radar icon:** Three concentric rings using CSS borders. On selection, rings light up based
on scope level (1 ring for narrow, all 3 for widest scope).

---

## Animated Radio Cards

**When to use:** Single choice from 2-5 descriptive options where each option needs a bit more
visual weight than a standard radio button. Good for preference questions, strategy choices.

**Structure:** Vertical stack of cards with icon, title, and short description. Selected card
expands slightly and glows with accent color. Unselected cards dim.

**Key CSS:**
```css
.radio-cards { display:flex; flex-direction:column; gap:10px; }
.radio-card {
  display:flex; align-items:center; gap:14px; padding:16px 20px;
  border-radius:14px; cursor:pointer; border:2px solid var(--border);
  background:rgba(255,255,255,0.02); transition:all 0.3s ease;
}
.radio-card:hover { border-color:var(--border-accent); }
.radio-card.selected {
  border-color:var(--accent); background:var(--accent-soft);
  box-shadow:0 0 20px var(--accent-glow); transform:scale(1.02);
}
.radio-card:not(.selected) { opacity:0.6; }
.rc-icon { font-size:1.5rem; flex-shrink:0; }
.rc-content { flex:1; }
.rc-title { font-weight:600; font-size:0.9rem; }
.rc-desc { font-size:0.75rem; color:var(--text-dim); margin-top:2px; }
```

**Behavior:** Single select. Clicking a new card deselects the previous. Smooth transitions
between states so unselected cards gracefully fade while the new selection pops.

---

## Tag Builder

**When to use:** When the respondent needs to build a list of items (exclusion companies,
dream accounts, names, URLs). More engaging than a textarea because each item becomes a
visible, removable pill.

**Structure:** A text input with a subtle "type + press Enter" hint. Each submitted entry
becomes a colored pill tag with an X button.

**Key CSS:**
```css
.tag-wall { display:flex; flex-wrap:wrap; gap:8px; min-height:20px; margin-top:10px; }
.tag-pill {
  display:inline-flex; align-items:center; gap:6px;
  padding:6px 12px; border-radius:20px; font-size:0.82rem;
  background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.25);
  color:#fca5a5; animation:tagPop 0.3s ease;
}
.tag-pill .remove {
  cursor:pointer; opacity:0.6; font-size:0.9rem;
  transition:opacity 0.2s;
}
.tag-pill .remove:hover { opacity:1; }
@keyframes tagPop { from { transform:scale(0.8); opacity:0; } to { transform:scale(1); opacity:1; } }
```

**Key JS:**
```javascript
const input = document.getElementById('exclusionInput');
function addTag(value) {
  if (!value.trim()) return;
  state.exclusions.push(value.trim());
  const pill = document.createElement('span');
  pill.className = 'tag-pill';
  pill.innerHTML = `${value.trim()} <span class="remove">✕</span>`;
  pill.querySelector('.remove').addEventListener('click', () => {
    state.exclusions = state.exclusions.filter(e => e !== value.trim());
    pill.remove();
    updateProgress();
  });
  document.getElementById('exclusionWall').appendChild(pill);
  input.value = '';
  updateProgress();
}
input.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); addTag(input.value); } });
```

---

## Split Drop Zones

**When to use:** When you need two parallel lists. Example: "Who do you want as attendees?"
and "Who should be sponsors?" Same question concept, two buckets.

**Structure:** Two side-by-side zones, each with its own colored header (e.g., Attendee
Targets in green, Sponsor Targets in amber), tag input, and tag wall with count.

**Key CSS:**
```css
.split-zones { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.drop-zone {
  padding:16px; border-radius:14px; border:2px dashed var(--border);
  background:rgba(255,255,255,0.01); transition:border-color 0.3s;
}
.drop-zone.has-items { border-style:solid; }
.zone-header { display:flex; align-items:center; gap:8px; margin-bottom:10px; }
.zone-count {
  margin-left:auto; font-family:'Space Mono',monospace;
  font-size:0.75rem; min-width:20px; text-align:center;
  padding:2px 8px; border-radius:10px;
}
```

Each zone gets its own accent color. Tags within each zone use that zone's color scheme.
Count badges update in real-time.

---

## Styled Textarea

**When to use:** Open-ended responses. This is your fallback for questions that genuinely
need free-form text. One per quiz is fine; more than two starts feeling lazy.

```css
.styled-textarea {
  width:100%; min-height:100px; padding:14px; resize:vertical;
  background:rgba(255,255,255,0.03); border:2px solid var(--border);
  border-radius:12px; color:var(--text); font-family:inherit; font-size:0.95rem;
  transition:border-color 0.3s, box-shadow 0.3s;
}
.styled-textarea:focus {
  outline:none; border-color:var(--accent);
  box-shadow:0 0 20px var(--accent-glow);
}
```

---

## Sentence Completer

**When to use:** Capturing nuanced preferences that are too structured for free text
but too subtle for radio buttons. Great for "how do you think about X?" questions.

**Structure:** A paragraph of text with highlighted inline slots. Each slot is a
tap-to-cycle element that rotates through 3-5 options. The sentence reads naturally
regardless of which options are selected.

**Key HTML:**
```html
<div class="sentence-block">
  When I start my day, I first want to see
  <span class="sc-slot" data-key="first_view" data-options='["my inbox","the graph","active efforts","what changed overnight"]' data-idx="0">my inbox</span>,
  and the thing I value most is
  <span class="sc-slot" data-key="priority" data-options='["speed","completeness","visual connections","minimal friction"]' data-idx="0">speed</span>.
  If Claude could only do one thing automatically, it should
  <span class="sc-slot" data-key="auto_action" data-options='["link new mentions","generate daily notes","sort my inbox","update MOCs"]' data-idx="0">link new mentions</span>.
</div>
```

**Key CSS:**
```css
.sentence-block {
  font-size:1.05rem; line-height:2; color:var(--text);
}
.sc-slot {
  display:inline-block; padding:4px 14px; border-radius:8px; cursor:pointer;
  background:var(--accent-soft); border:1px solid var(--accent);
  color:var(--accent); font-weight:600; transition:all 0.2s;
  position:relative;
}
.sc-slot:hover { background:rgba(124,58,237,0.15); transform:scale(1.03); }
.sc-slot::after {
  content:'↻'; margin-left:6px; font-size:0.7em; opacity:0.5;
}
```

**Key JS:** On click, increment `data-idx`, wrap around, update text content from the
options array. Store current selection in state per key.

**State shape:** `state.sentences = { first_view: 'my inbox', priority: 'speed', auto_action: 'link new mentions' }`

---

## Gradient Slider

**When to use:** Rating on a continuous spectrum between two labeled endpoints.

**Implementation:** Custom-styled `<input type="range">` with a floating label above the
thumb that updates as you drag. Track has a CSS gradient matching the semantic meaning.

```css
.gradient-slider input[type="range"] {
  -webkit-appearance:none; width:100%; height:8px; border-radius:4px;
  background:linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
}
.gradient-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance:none; width:28px; height:28px; border-radius:50%;
  background:white; box-shadow:0 2px 10px rgba(0,0,0,0.3), 0 0 20px var(--accent-glow);
  cursor:grab;
}
```

Use an array of labels that map to slider positions. Update the floating label on `input` event.

---

## Mixer Sliders

**When to use:** Allocating a total (100%) across categories: budget splits, time distribution,
priority weighting.

**Behavior:** Multiple horizontal sliders linked together. Moving one up proportionally adjusts
others down. Shows percentages live. Total indicator turns green when balanced.

```javascript
function updateMixerSliders(changedIndex, newValue, sliders) {
  const total = 100;
  const values = sliders.map(s => parseInt(s.value));
  values[changedIndex] = newValue;
  const remaining = total - newValue;
  const othersSum = values.reduce((sum, v, i) => i === changedIndex ? sum : sum + v, 0);
  if (othersSum === 0) {
    const each = Math.floor(remaining / (values.length - 1));
    values.forEach((v, i) => { if (i !== changedIndex) values[i] = each; });
  } else {
    const scale = remaining / othersSum;
    values.forEach((v, i) => { if (i !== changedIndex) values[i] = Math.round(v * scale); });
  }
  // Fix rounding
  const diff = total - values.reduce((a, b) => a + b, 0);
  if (diff !== 0) {
    for (let i = 0; i < values.length; i++) {
      if (i !== changedIndex) { values[i] += diff; break; }
    }
  }
  return values;
}
```

---

## Heat Map Grid

**When to use:** Showing intensity/preference across a matrix ([[SKILL]] proficiency, interest
levels across categories, experience depth).

**Behavior:** Each cell starts at level 0. Tapping increments (0->1->2->3->4->0). Color deepens
with intensity using increasing opacity of the accent color. Include a legend explaining
the levels.

```css
.heatmap-cell[data-intensity="0"] { background:rgba(255,255,255,0.03); }
.heatmap-cell[data-intensity="1"] { background:rgba(99,102,241,0.2); }
.heatmap-cell[data-intensity="2"] { background:rgba(99,102,241,0.4); }
.heatmap-cell[data-intensity="3"] { background:rgba(99,102,241,0.6); color:white; }
.heatmap-cell[data-intensity="4"] { background:rgba(99,102,241,0.85); color:white; box-shadow:0 0 15px var(--accent-glow); }
```

**Legend guidance:** The legend should clearly explain what each level means in context. For a
[[SKILL]] assessment: "0 = No experience, 1 = Aware, 2 = Can use with help, 3 = Proficient,
4 = Expert". Generic labels like "Low" and "High" without context leave respondents guessing.

---

## 2D Position Picker

**When to use:** Questions with two meaningful dimensions (strategic vs tactical + internal
vs external, urgency vs importance).

**Implementation:** A square area with labeled axes and quadrant labels. User drags a pin
to their position. Show coordinates or quadrant name as they drag. Support both mouse and
touch events.

---

## Confidence Meter

**When to use:** When "I'm not sure" is valuable data. A "balanced" answer with low
confidence is very different from "balanced" with high confidence.

**Structure:** Two horizontally stacked sliders. Top slider = the actual answer (same
as gradient slider). Bottom slider = confidence level (0-100%). Both update independently.
Show a combined label like "Balanced (72% confident)".

**Key CSS:**
```css
.confidence-wrap { display:flex; flex-direction:column; gap:16px; }
.confidence-answer-track, .confidence-level-track {
  position:relative;
}
.confidence-level-track input[type="range"] {
  background:linear-gradient(90deg, rgba(255,255,255,0.1), var(--cyan));
}
.confidence-combined {
  text-align:center; font-size:0.9rem; margin-top:8px;
}
.confidence-combined .conf-pct {
  font-family:'Space Mono',monospace; color:var(--cyan);
}
```

**State shape:** `state.answer = { value: 'balanced', confidence: 72 }`

---

## Emotional Spectrum Bubbles

**When to use:** Independent intensity ratings where there's no tradeoff. "How important
are each of these to you?" where you CAN feel strongly about all of them. Unlike mixer
sliders (which sum to 100%), these are independent.

**Structure:** Floating circles arranged in a loose grid. Each starts small and grows
on tap (4 levels: dormant -> interested -> important -> essential). Size and glow increase
with each level. No maximum total: all can be maxed out.

**Key CSS:**
```css
.bubble-field { display:flex; flex-wrap:wrap; gap:20px; justify-content:center; padding:20px 0; }
.spectrum-bubble {
  display:flex; flex-direction:column; align-items:center; gap:8px;
  cursor:pointer; user-select:none; transition:all 0.4s ease;
}
.sb-circle {
  width:60px; height:60px; border-radius:50%; border:2px solid var(--border);
  display:flex; align-items:center; justify-content:center;
  font-size:1.3rem; transition:all 0.4s cubic-bezier(0.34,1.56,0.64,1);
  background:rgba(255,255,255,0.02);
}
.spectrum-bubble[data-level="1"] .sb-circle {
  width:70px; height:70px; border-color:rgba(124,58,237,0.4);
  background:rgba(124,58,237,0.08); box-shadow:0 0 10px rgba(124,58,237,0.1);
}
.spectrum-bubble[data-level="2"] .sb-circle {
  width:85px; height:85px; border-color:rgba(124,58,237,0.6);
  background:rgba(124,58,237,0.15); box-shadow:0 0 20px rgba(124,58,237,0.2);
}
.spectrum-bubble[data-level="3"] .sb-circle {
  width:100px; height:100px; border-color:var(--accent);
  background:rgba(124,58,237,0.25); box-shadow:0 0 35px var(--accent-glow);
}
.sb-label { font-size:0.72rem; color:var(--text-dim); text-align:center; max-width:80px; }
.sb-level { font-size:0.65rem; font-family:'Space Mono',monospace; color:var(--accent); }
```

**Key JS:** Tap to cycle through levels 0->1->2->3->0. Update bubble size/glow/label.
Level names: 0=dot, 1="Interested", 2="Important", 3="Essential"

**State shape:** `state.bubbles = { speed: 2, aesthetics: 3, automation: 3, simplicity: 1 }`

---

## Timeline Sequencer

**When to use:** "Walk me through your morning," "Order these steps," "What comes first?"
The answer is about *temporal sequence*, not importance ranking.

**Structure:** A row of empty numbered slots (the timeline) and a pool of draggable cards
below. User drags cards from the pool into slots. Cards snap to slots with a satisfying
animation. Reordering is supported: drag a card out to return it to the pool.

**Key HTML:**
```html
<div class="timeline-track" id="timelineTrack">
  <div class="tl-slot" data-slot="1"><span class="tl-num">1</span></div>
  <div class="tl-slot" data-slot="2"><span class="tl-num">2</span></div>
  <div class="tl-slot" data-slot="3"><span class="tl-num">3</span></div>
  <div class="tl-slot" data-slot="4"><span class="tl-num">4</span></div>
  <div class="tl-slot" data-slot="5"><span class="tl-num">5</span></div>
</div>
<div class="tl-pool" id="timelinePool">
  <div class="tl-card" data-value="check-inbox">📥 Check inbox</div>
  <div class="tl-card" data-value="scan-graph">🕸️ Scan graph</div>
  <div class="tl-card" data-value="daily-note">📝 Open daily note</div>
  <div class="tl-card" data-value="review-efforts">🎯 Review efforts</div>
  <div class="tl-card" data-value="triage-email">📧 Triage email</div>
</div>
<div class="tl-instructions">Click a card, then click a slot to place it. Click a placed card to return it.</div>
```

**Key CSS:**
```css
.timeline-track {
  display:flex; gap:8px; padding:16px; background:rgba(255,255,255,0.02);
  border-radius:14px; border:2px dashed var(--border); min-height:80px;
  overflow-x:auto;
}
.tl-slot {
  flex:1; min-width:100px; min-height:60px; border-radius:10px;
  border:2px dashed var(--border); display:flex; align-items:center;
  justify-content:center; position:relative; transition:all 0.3s;
  cursor:pointer;
}
.tl-slot.awaiting { border-color:var(--accent); background:var(--accent-soft); animation:pulse 1.5s infinite; }
.tl-slot.filled { border-style:solid; border-color:var(--green); background:rgba(34,197,94,0.06); }
.tl-num {
  position:absolute; top:4px; left:8px; font-family:'Space Mono',monospace;
  font-size:0.65rem; color:var(--text-dim); opacity:0.5;
}
.tl-pool { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
.tl-card {
  padding:10px 16px; border-radius:10px; border:2px solid var(--border);
  background:rgba(255,255,255,0.03); cursor:pointer; font-size:0.85rem;
  transition:all 0.3s ease; user-select:none;
}
.tl-card.selected {
  border-color:var(--accent); background:var(--accent-soft);
  box-shadow:0 0 15px var(--accent-glow); transform:scale(1.05);
}
.tl-card.in-slot { cursor:pointer; } /* Placed cards are clickable to return to pool */
.tl-instructions { font-size:0.72rem; color:var(--text-dim); margin-top:8px; text-align:center; }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.6; } }
```

**Key JS (CLICK-TO-PLACE, not HTML5 drag-and-drop):**
```javascript
let selectedCard = null;
const pool = document.getElementById('timelinePool');
const track = document.getElementById('timelineTrack');

// Click a card in the pool to select it
pool.querySelectorAll('.tl-card').forEach(card => {
  card.addEventListener('click', () => {
    if (selectedCard === card) {
      card.classList.remove('selected');
      track.querySelectorAll('.tl-slot').forEach(s => s.classList.remove('awaiting'));
      selectedCard = null;
      return;
    }
    if (selectedCard) selectedCard.classList.remove('selected');
    selectedCard = card;
    card.classList.add('selected');
    // Highlight empty slots as targets
    track.querySelectorAll('.tl-slot').forEach(s => {
      s.classList.toggle('awaiting', !s.querySelector('.tl-card'));
    });
  });
});

// Click a slot to place the selected card
track.querySelectorAll('.tl-slot').forEach(slot => {
  slot.addEventListener('click', (e) => {
    // If clicking a card already in a slot, return it to pool
    const placedCard = slot.querySelector('.tl-card');
    if (placedCard && !selectedCard) {
      pool.appendChild(placedCard);
      placedCard.classList.remove('in-slot');
      slot.classList.remove('filled');
      updateTimelineState();
      return;
    }
    if (!selectedCard) return;
    // If slot already has a card, swap it back to pool
    if (placedCard) {
      pool.appendChild(placedCard);
      placedCard.classList.remove('in-slot');
    }
    slot.appendChild(selectedCard);
    selectedCard.classList.remove('selected');
    selectedCard.classList.add('in-slot');
    slot.classList.add('filled');
    selectedCard = null;
    track.querySelectorAll('.tl-slot').forEach(s => s.classList.remove('awaiting'));
    updateTimelineState();
  });
});

function updateTimelineState() {
  state.sequence = [];
  track.querySelectorAll('.tl-slot').forEach(slot => {
    const card = slot.querySelector('.tl-card');
    state.sequence.push(card ? card.dataset.value : null);
  });
  updateProgress();
}
```

**State shape:** `state.sequence = ['check-inbox', 'daily-note', 'review-efforts', ...]`

---

## Card Sorting

**When to use:** "Categorize these," "Sort into groups," "Which bucket does each belong to?"
The answer is about classification, not ranking.

**Structure:** An unsorted pile of cards at the top and 2-4 labeled columns below. User
drags cards from the pile into columns. Each column has a distinct color and emoji header.
Shows count per column.

**Key CSS:**
```css
.sort-columns {
  display:grid; grid-template-columns:repeat(auto-fit, minmax(160px,1fr)); gap:12px;
}
.sort-column {
  padding:14px; border-radius:14px; min-height:200px;
  border:2px dashed var(--border); transition:all 0.3s; cursor:pointer;
}
.sort-column.awaiting { border-color:var(--accent); border-style:solid; background:var(--accent-soft); }
.sort-column-header {
  font-weight:600; font-size:0.85rem; margin-bottom:12px;
  display:flex; align-items:center; gap:8px;
}
.sort-column-count {
  margin-left:auto; font-family:'Space Mono',monospace;
  font-size:0.72rem; padding:2px 8px; border-radius:10px;
}
.sort-pile { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px; min-height:40px; }
.sort-item {
  padding:8px 14px; border-radius:8px; border:1px solid var(--border);
  background:rgba(255,255,255,0.03); cursor:pointer; font-size:0.82rem;
  transition:all 0.3s ease; user-select:none;
}
.sort-item.selected {
  border-color:var(--accent); background:var(--accent-soft);
  box-shadow:0 0 12px var(--accent-glow); transform:scale(1.05);
}
.sort-instructions { font-size:0.72rem; color:var(--text-dim); margin-top:8px; text-align:center; }
```

**Key JS (CLICK-TO-PLACE with return-to-pile support):**

CRITICAL: Items placed in columns MUST be returnable. Clicking a placed item selects it,
then clicking the pile (or another column) moves it. This is non-negotiable UX.

```javascript
let selectedSortItem = null;
const pile = document.querySelector('.sort-pile');

// Attach click handlers to ALL sort items (pile and column items)
function attachSortItemHandler(item) {
  item.addEventListener('click', (e) => {
    e.stopPropagation();
    // Toggle selection
    if (selectedSortItem === item) {
      item.classList.remove('selected');
      clearSortHighlights();
      selectedSortItem = null;
      return;
    }
    if (selectedSortItem) selectedSortItem.classList.remove('selected');
    selectedSortItem = item;
    item.classList.add('selected');
    // Highlight all drop targets: columns AND the pile (for returning items)
    document.querySelectorAll('.sort-column').forEach(c => c.classList.add('awaiting'));
    pile.classList.add('awaiting');
  });
}

// Initialize handlers on all items
document.querySelectorAll('.sort-item').forEach(attachSortItemHandler);

// Click a column to place the selected item there
document.querySelectorAll('.sort-column').forEach(col => {
  col.addEventListener('click', () => {
    if (!selectedSortItem) return;
    const itemsArea = col.querySelector('.sort-column-items') || col;
    itemsArea.appendChild(selectedSortItem);
    // Dopamine: brief glow pulse on the column border
    col.classList.add('just-received');
    setTimeout(() => col.classList.remove('just-received'), 400);
    selectedSortItem.classList.remove('selected');
    selectedSortItem = null;
    clearSortHighlights();
    updateSortState();
  });
});

// Click the pile to RETURN the selected item (from any column back to unsorted)
pile.addEventListener('click', () => {
  if (!selectedSortItem) return;
  pile.appendChild(selectedSortItem);
  selectedSortItem.classList.remove('selected');
  selectedSortItem = null;
  clearSortHighlights();
  updateSortState();
});

function clearSortHighlights() {
  document.querySelectorAll('.sort-column').forEach(c => c.classList.remove('awaiting'));
  pile.classList.remove('awaiting');
}

function updateSortState() {
  state.sorted = {};
  document.querySelectorAll('.sort-column').forEach(col => {
    const key = col.dataset.bucket;
    state.sorted[key] = [...col.querySelectorAll('.sort-item')].map(i => i.dataset.value);
  });
  // Update count badges with digit-roll animation
  document.querySelectorAll('.sort-column-count').forEach(badge => {
    const col = badge.closest('.sort-column');
    const newCount = col.querySelectorAll('.sort-item').length;
    if (badge.textContent !== String(newCount)) {
      badge.textContent = newCount;
      badge.classList.add('count-bump');
      setTimeout(() => badge.classList.remove('count-bump'), 300);
    }
  });
  updateProgress();
}
```

**Additional CSS for return-to-pile and dopamine feedback:**
```css
.sort-pile.awaiting { border-color:var(--amber); border-style:solid; background:rgba(245,158,11,0.05); }
.sort-column.just-received { border-color:var(--green); box-shadow:0 0 20px rgba(34,197,94,0.3); }
.sort-column-count.count-bump { animation:countBump 0.3s ease; }
@keyframes countBump { 0% { transform:scale(1); } 50% { transform:scale(1.3); } 100% { transform:scale(1); } }
```

**Instructional micro-copy:** Below the pile, add a small helper:
`<div class="sort-instructions">Click an item to select it, then click a column to sort it. Click a sorted item to move it back.</div>`

**State shape:** `state.sorted = { bucket1: ['item1','item3'], bucket2: ['item2'] }`

---

## Constellation Builder

**When to use:** "How do these relate to each other?", "Map your ecosystem,"
"Which entities are closely connected?" The answer is about *topology*: relative
proximity and connections.

**Structure:** A dark canvas area. Pre-placed labeled dots (entities) that the user
can drag to reposition. Tap two dots sequentially to draw a connection line between them.
Closer dots = more related. Connection lines show relationship strength.

**Key HTML:**
```html
<div class="constellation-canvas" id="constellationCanvas">
  <svg class="constellation-lines" id="constellationSVG"></svg>
  <div class="constellation-node" data-entity="champiq" style="left:30%;top:20%;">
    <span class="cn-dot"></span>
    <span class="cn-label">ChampIQ</span>
  </div>
  <!-- more nodes... -->
</div>
<div class="constellation-instructions">
  Drag to reposition. Tap two nodes to connect them. Tap a line to remove.
</div>
```

**Key CSS:**
```css
.constellation-canvas {
  position:relative; width:100%; height:350px; border-radius:14px;
  background:rgba(0,0,0,0.3); border:1px solid var(--border); overflow:hidden;
}
.constellation-lines { position:absolute; inset:0; pointer-events:none; }
.constellation-lines line {
  stroke:var(--accent); stroke-width:2; opacity:0.4;
  stroke-dasharray:4,4; pointer-events:auto; cursor:pointer;
}
.constellation-lines line:hover { opacity:0.8; stroke-width:3; }
.constellation-node {
  position:absolute; transform:translate(-50%,-50%); cursor:grab;
  display:flex; flex-direction:column; align-items:center; gap:4px; z-index:2;
}
.cn-dot {
  width:16px; height:16px; border-radius:50%; background:var(--accent);
  box-shadow:0 0 12px var(--accent-glow); transition:all 0.2s;
}
.constellation-node.selected .cn-dot {
  width:22px; height:22px; box-shadow:0 0 20px var(--accent);
}
.cn-label { font-size:0.72rem; color:var(--text-dim); white-space:nowrap; }
```

**Key JS (click-based connection drawing):**
```javascript
let firstNode = null;
const canvas = document.getElementById('constellationCanvas');
const svg = document.getElementById('constellationSVG');

document.querySelectorAll('.constellation-node').forEach(node => {
  // Click to select/connect nodes
  node.addEventListener('click', (e) => {
    e.stopPropagation();
    if (!firstNode) {
      firstNode = node;
      node.classList.add('selected');
    } else if (firstNode !== node) {
      // Draw connection
      drawLine(firstNode, node);
      const pair = [firstNode.dataset.entity, node.dataset.entity].sort();
      // Toggle: if connection exists, remove it; otherwise add it
      const existing = state.connections.findIndex(c =>
        c[0] === pair[0] && c[1] === pair[1]);
      if (existing >= 0) {
        state.connections.splice(existing, 1);
        redrawAllLines();
      } else {
        state.connections.push(pair);
      }
      firstNode.classList.remove('selected');
      firstNode = null;
      updateProgress();
    } else {
      firstNode.classList.remove('selected');
      firstNode = null;
    }
  });

  // Mouse drag to reposition nodes
  let isDragging = false, startX, startY, startLeft, startTop;
  node.addEventListener('mousedown', (e) => {
    isDragging = false; startX = e.clientX; startY = e.clientY;
    startLeft = node.offsetLeft; startTop = node.offsetTop;
    const onMove = (e2) => {
      const dx = e2.clientX - startX, dy = e2.clientY - startY;
      if (Math.abs(dx) > 3 || Math.abs(dy) > 3) isDragging = true;
      if (isDragging) {
        node.style.left = (startLeft + dx) + 'px';
        node.style.top = (startTop + dy) + 'px';
        redrawAllLines();
      }
    };
    const onUp = () => {
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
    };
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  });
});

function drawLine(nodeA, nodeB) {
  // Implementation uses getBoundingClientRect() relative to canvas
}
function redrawAllLines() {
  svg.innerHTML = '';
  state.connections.forEach(([a, b]) => {
    const nodeA = canvas.querySelector(`[data-entity="${a}"]`);
    const nodeB = canvas.querySelector(`[data-entity="${b}"]`);
    if (nodeA && nodeB) drawLine(nodeA, nodeB);
  });
}
```

Store connections as pairs: `state.connections = [['champiq','Gary'], ['[[Gary]]','span']]`.
Use `getBoundingClientRect()` relative to the canvas container for SVG line coordinates.
Redraw all lines on every node reposition.

---

## Venn Selector

**When to use:** "Which of these are personal vs professional vs both?", "Research vs
execution vs both?" Items can legitimately belong to overlapping categories.

**Structure:** 2-3 overlapping circles rendered as colored semi-transparent regions.
A pool of item chips below. User drags chips into the appropriate zone. Items in the
overlap zone belong to both categories.

**Implementation (click-to-place):** For 2-circle Venn, render three clickable zones as
positioned divs: left-only, overlap, right-only. A pool of item chips sits below. User clicks
a chip to select it (glow), then clicks a zone to place it. Clicking a placed chip returns it
to the pool. Same click-to-place pattern as Card Sorting and Timeline Sequencer.

For 3-circle Venn, create 7 zones. Use CSS for the visual overlap effect but use simple
rectangular hit-target divs positioned over each zone area for reliable click detection.

**State shape:** `state.venn = { left_only: [...], overlap: [...], right_only: [...] }`

---

## Swipe Cards

**When to use:** Quick yes/no or agree/disagree decisions across multiple items.

**Implementation:** Card stack with TWO interaction methods that always work:
1. **Buttons (primary, always visible):** A thumbs-up (green) and thumbs-down (red) button below
   the card. Clicking either triggers the card's exit animation and advances to the next card.
2. **Mouse/touch drag (enhancement):** Drag right = yes (green overlay fades in), left = no
   (red overlay fades in). On release past threshold, fling animation. On release below threshold,
   snap back. Use `mousedown`/`mousemove`/`mouseup` AND `touchstart`/`touchmove`/`touchend`.

Always show the button fallback. Show remaining count badge. After all cards are swiped, show
a summary of yes/no decisions.

---

## Before/After Toggle

**When to use:** Comparing two visual states: template layouts, dashboard designs,
graph configurations, workflow diagrams. The answer is a preference between renderings.

**Structure:** A card with a toggle switch or horizontal slider. Left side shows
State A, right side shows State B. Toggling crossfades between views. Below the toggle,
a "Which do you prefer?" selector.

**Key CSS:**
```css
.ba-container { position:relative; border-radius:14px; overflow:hidden; height:250px; }
.ba-before, .ba-after {
  position:absolute; inset:0; display:flex; align-items:center;
  justify-content:center; padding:20px; transition:opacity 0.5s ease;
}
.ba-before { background:rgba(244,63,94,0.06); z-index:1; }
.ba-after { background:rgba(34,197,94,0.06); z-index:0; }
.ba-container.showing-after .ba-before { opacity:0; }
.ba-container.showing-after .ba-after { z-index:1; }
.ba-toggle {
  display:flex; justify-content:center; gap:12px; margin-top:12px;
}
.ba-toggle-btn {
  padding:8px 20px; border-radius:8px; border:2px solid var(--border);
  background:transparent; color:var(--text-dim); cursor:pointer;
  font-family:inherit; font-size:0.82rem; transition:all 0.3s;
}
.ba-toggle-btn.active { border-color:var(--accent); color:var(--accent); background:var(--accent-soft); }
```

**State shape:** `state.preference = 'before' | 'after'`

---

## Summary Generation

After all questions are answered (or "Generate Summary" is clicked), compile state into a
structured text block. Format it for easy copy-paste into Slack/email/docs:

```
=== [Quiz Title] ===
Completed: [date]

1. [Question]
   -> [Answer or comma-separated list]

2. [Question]
   Must-Have: CIO, CTO
   Nice-to-Have: CISO, CDO

...

--- Copy-Paste Ready ---
[Formatted text block appropriate for the use case]
```

Use the clipboard API with 3-tier fallback (navigator.clipboard -> execCommand -> manual select).
Show a toast notification on copy success.
