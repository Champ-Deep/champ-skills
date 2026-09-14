---
name: interactive-quiz-v2
description: >
  Extended interaction pattern library for the interactive-quiz skill. Adds 8 new
  interaction patterns focused on relational, spatial, and nuanced data capture.
  Use alongside the base interactive-quiz skill — this file provides the ADDITIONAL
  patterns and implementation references. Trigger on the same keywords as interactive-quiz
  plus: "timeline", "card sort", "constellation", "venn", "sentence builder", "confidence",
  "before/after", "relationship map", "workflow sequence", "categorize", "sort into buckets".
---

# Interactive Quiz V2 — Extended Pattern Library

This extends the base `interactive-quiz` skill with 8 new interaction patterns. The base
skill covers selection, input, quantitative, and binary patterns. This extension adds
**relational**, **spatial**, and **nuanced input** patterns.

## When to Use These Patterns

Use patterns from this extension when:
- The answer involves **sequence or order** (not just ranking by importance, but temporal flow)
- The answer involves **categorization** (sorting items into buckets)
- The answer involves **relationships between entities** (who connects to whom)
- The answer involves **overlapping categories** (things can belong to multiple groups)
- The answer needs **nuance beyond a single dimension** (confidence, emotional intensity)
- The answer involves **visual preference** between two states

## New Pattern Catalog

### Relational / Spatial Patterns

| Pattern | Best For | Feel |
|---------|----------|------|
| **Timeline Sequencer** | Ordering steps in a workflow or process | Drag cards into horizontal timeline slots |
| **Card Sorting** | Categorizing items into labeled buckets | Drag unsorted pile into 2–4 labeled columns |
| **Constellation Builder** | Mapping relationships between entities | Place dots on freeform canvas, draw connections |
| **Venn Selector** | Items that belong to overlapping categories | Drop items into overlapping circle zones |

### Nuanced Input Patterns

| Pattern | Best For | Feel |
|---------|----------|------|
| **Sentence Completer** | Structured preferences with inline choices | Fill-in-the-blank with tap-to-select word slots |
| **Confidence Meter** | Answer + certainty level as dual track | Dual slider — one for answer, one for confidence |
| **Emotional Spectrum Bubbles** | Independent intensity ratings (no tradeoff) | Tap bubbles to inflate; each grows independently |
| **Before/After Toggle** | Visual preference between two states | Swipe/toggle between two screenshots or layouts |

## Implementation Reference

### 1. Timeline Sequencer

**When to use:** "Walk me through your morning," "Order these steps," "What comes first?"
The answer is about *temporal sequence*, not importance ranking.

**Structure:** A row of empty numbered slots (the timeline) and a pool of draggable cards
below. User drags cards from the pool into slots. Cards snap to slots with a satisfying
animation. Reordering is supported — drag a card out to return it to the pool.

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
  <div class="tl-card" draggable="true" data-value="check-inbox">📥 Check inbox</div>
  <div class="tl-card" draggable="true" data-value="scan-graph">🕸️ Scan graph</div>
  <div class="tl-card" draggable="true" data-value="daily-note">📝 Open daily note</div>
  <div class="tl-card" draggable="true" data-value="review-efforts">🎯 Review efforts</div>
  <div class="tl-card" draggable="true" data-value="triage-email">📧 Triage email</div>
</div>
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
}
.tl-slot.hover { border-color:var(--accent); background:var(--accent-soft); }
.tl-slot.filled { border-style:solid; border-color:var(--green); background:rgba(34,197,94,0.06); }
.tl-num {
  position:absolute; top:4px; left:8px; font-family:'Space Mono',monospace;
  font-size:0.65rem; color:var(--text-dim); opacity:0.5;
}
.tl-pool { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
.tl-card {
  padding:10px 16px; border-radius:10px; border:2px solid var(--border);
  background:rgba(255,255,255,0.03); cursor:grab; font-size:0.85rem;
  transition:all 0.2s; user-select:none;
}
.tl-card:active { cursor:grabbing; transform:scale(1.05); box-shadow:0 4px 20px rgba(0,0,0,0.3); }
.tl-card.placed { opacity:0.3; pointer-events:none; }
```

**Key JS:** Use HTML5 drag-and-drop API with `dragstart`, `dragover`, `drop` events on slots.
On drop, move the card element into the slot, mark the card as `.placed` in the pool, and
update state with the ordered sequence. Support removing cards from slots (click to return
to pool).

**State shape:** `state.sequence = ['check-inbox', 'daily-note', 'review-efforts', ...]`

---

### 2. Card Sorting

**When to use:** "Categorize these," "Sort into groups," "Which bucket does each belong to?"
The answer is about classification, not ranking.

**Structure:** An unsorted pile of cards at the top and 2–4 labeled columns below. User
drags cards from the pile into columns. Each column has a distinct color and emoji header.
Shows count per column.

**Key CSS:**
```css
.sort-columns {
  display:grid; grid-template-columns:repeat(auto-fit, minmax(160px,1fr)); gap:12px;
}
.sort-column {
  padding:14px; border-radius:14px; min-height:200px;
  border:2px dashed var(--border); transition:all 0.3s;
}
.sort-column.hover { border-style:solid; }
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
  background:rgba(255,255,255,0.03); cursor:grab; font-size:0.82rem;
  transition:all 0.2s; user-select:none;
}
```

**State shape:** `state.sorted = { bucket1: ['item1','item3'], bucket2: ['item2'] }`

---

### 3. Constellation Builder

**When to use:** "How do these relate to each other?", "Map your ecosystem,"
"Which entities are closely connected?" The answer is about *topology* — relative
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
  Drag to reposition · Tap two nodes to connect them · Tap a line to remove
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

**Key JS:** Track node positions with mouse/touch drag. First tap selects a node (glow
effect), second tap on a different node draws an SVG line between them. Store connections
as pairs: `state.connections = [['champiq','gary'], ['gary','span']]`. Use `getBoundingClientRect()`
to compute SVG line coordinates. Redraw lines on node drag.

---

### 4. Venn Selector

**When to use:** "Which of these are personal vs professional vs both?", "Research vs
execution vs both?" Items can legitimately belong to overlapping categories.

**Structure:** 2–3 overlapping circles rendered as colored semi-transparent regions.
A pool of item chips below. User drags chips into the appropriate zone. Items in the
overlap zone belong to both categories.

**Implementation note:** For 2-circle Venn, create three drop zones: left-only, overlap,
right-only. For 3-circle Venn, create 7 zones (each individual, each pairwise overlap,
and the center). Use CSS clip-path or overlapping rounded divs with strategic z-indexing.

**State shape:** `state.venn = { left_only: [...], overlap: [...], right_only: [...] }`

---

### 5. Sentence Completer

**When to use:** Capturing nuanced preferences that are too structured for free text
but too subtle for radio buttons. Great for "how do you think about X?"

**Structure:** A paragraph of text with highlighted inline slots. Each slot is a
tap-to-cycle element that rotates through 3–5 options. The sentence reads naturally
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

---

### 6. Confidence Meter

**When to use:** When "I'm not sure" is valuable data. A "balanced" answer with low
confidence is very different from "balanced" with high confidence.

**Structure:** Two horizontally stacked sliders. Top slider = the actual answer (same
as gradient slider). Bottom slider = confidence level (0–100%). Both update independently.
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

### 7. Emotional Spectrum Bubbles

**When to use:** Independent intensity ratings where there's no tradeoff. "How important
are each of these to you?" where you CAN feel strongly about all of them. Unlike mixer
sliders (which sum to 100%), these are independent.

**Structure:** Floating circles arranged in a loose grid. Each starts small and grows
on tap (4 levels: dormant → interested → important → essential). Size and glow increase
with each level. No maximum total — all can be maxed out.

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

**Key JS:** Tap to cycle through levels 0→1→2→3→0. Update bubble size/glow/label.
Level names: 0=·, 1="Interested", 2="Important", 3="Essential"

**State shape:** `state.bubbles = { speed: 2, aesthetics: 3, automation: 3, simplicity: 1 }`

---

### 8. Before/After Toggle

**When to use:** Comparing two visual states — template layouts, dashboard designs,
graph configurations, workflow diagrams. The answer is a preference between renderings.

**Structure:** A card with a horizontal slider/dragger in the middle. Left side shows
State A, right side shows State B. Dragging the divider reveals more of one side. Or
simpler: a toggle switch that crossfades between two views. Below the toggle, a
"Which do you prefer?" selector.

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

## Pattern Selection Heuristic (Updated)

When choosing patterns for a quiz, use this expanded decision tree:

```
Is the answer about SEQUENCE/ORDER?
  → Timeline Sequencer (temporal) or Priority Ranking (importance)

Is the answer about CATEGORIZATION?
  → Card Sorting (exclusive buckets) or Venn Selector (overlapping)

Is the answer about RELATIONSHIPS?
  → Constellation Builder (topology) or Icon Chip Cards (flat multi-select)

Is the answer NUANCED with uncertainty?
  → Confidence Meter (answer + certainty) or Sentence Completer (structured flexibility)

Is the answer about INDEPENDENT INTENSITIES?
  → Emotional Spectrum Bubbles (no tradeoff) vs Mixer Sliders (zero-sum)

Is the answer a VISUAL PREFERENCE?
  → Before/After Toggle

Otherwise, fall back to base patterns:
  Single select → Concept Cards or Animated Radio Cards
  Multi select → Icon Chip Cards
  Rating → Gradient Slider
  Allocation → Mixer Sliders
  Matrix → Heat Map Grid
  Free text → Styled Textarea
  Yes/No batch → Swipe Cards
  List building → Tag Builder
```

## Combining with Base Skill

When building a quiz:
1. Read the base `interactive-quiz` SKILL.md for overall architecture, visual guidelines,
   state management, and anti-patterns
2. Read this file for the extended pattern catalog
3. The diversity rule still applies: `ceil(N * 0.6)` unique patterns minimum
4. New patterns count toward diversity — a quiz using 3 base + 3 extended patterns = 6 unique patterns
