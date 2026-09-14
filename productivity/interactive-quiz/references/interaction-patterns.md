# Interaction Pattern Implementation Reference

Full CSS/JS implementation details for every interaction pattern. Read this when building a
specific pattern. Patterns are organized by category.

## Table of Contents
1. [Icon Chip Cards](#icon-chip-cards)
2. [Priority Ranking Tiles](#priority-ranking-tiles)
3. [Concept Cards](#concept-cards)
4. [Scope Radar Cards](#scope-radar-cards)
5. [Animated Radio Cards](#animated-radio-cards)
6. [Tag Builder](#tag-builder)
7. [Split Drop Zones](#split-drop-zones)
8. [Styled Textarea](#styled-textarea)
9. [Gradient Slider](#gradient-slider)
10. [Mixer Sliders](#mixer-sliders)
11. [Heat Map Grid](#heat-map-grid)
12. [2D Position Picker](#2d-position-picker)
13. [Swipe Cards](#swipe-cards)

---

## Icon Chip Cards

**When to use:** Multi-select from 4–20 predefined categories (industries, tools, skills, topics).

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

**Behavior:** Tap once → 🔥 Must Have (level 1, red). Tap again → ⚡ Nice to Have (level 2, amber).
Tap a third time → back to unselected (level 0). Each tile shows its current level label.

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
    // Collect state
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
Include a "Custom" text input below that clears the card selection when the user types.

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
/* Color per scope level */
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

## Tag Builder

**When to use:** When the respondent needs to build a list of items (exclusion companies,
dream accounts, names, URLs). More engaging than a textarea because each item becomes a
visible, removable pill.

**Structure:** A text input with a subtle "type + press Enter" hint. Each submitted entry
becomes a colored pill tag with an ✕ button.

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
and "Who should be sponsors?" — same question concept, two buckets.

**Structure:** Two side-by-side zones, each with its own colored header (e.g., 🎯 Attendee
Targets in green, 💎 Sponsor Targets in amber), tag input, and tag wall with count.

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

**When to use:** Allocating a total (100%) across categories — budget splits, time distribution,
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

**When to use:** Showing intensity/preference across a matrix (skill proficiency, interest
levels across categories, experience depth).

**Behavior:** Each cell starts at level 0. Tapping increments (0→1→2→3→4→0). Color deepens
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
skill assessment: "0 = No experience, 1 = Aware, 2 = Can use with help, 3 = Proficient,
4 = Expert". Generic labels like "Low" and "High" without context leave respondents guessing.

---

## 2D Position Picker

**When to use:** Questions with two meaningful dimensions (strategic vs tactical + internal
vs external, urgency vs importance).

**Implementation:** A square area with labeled axes and quadrant labels. User drags a pin
to their position. Show coordinates or quadrant name as they drag. Support both mouse and
touch events.

---

## Swipe Cards

**When to use:** Quick yes/no or agree/disagree decisions across multiple items.

**Implementation:** Card stack. Drag right = yes (green overlay), drag left = no (red overlay).
Satisfying "fling" animation when released past threshold. Show remaining count.

---

## Styled Textarea

**When to use:** Open-ended responses — this is your fallback for questions that genuinely
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

## Summary Generation

After all questions are answered (or "Generate Summary" is clicked), compile state into a
structured text block. Format it for easy copy-paste into Slack/email/docs:

```
=== [Quiz Title] ===
Completed: [date]

1. [Question]
   → [Answer or comma-separated list]

2. [Question]
   Must-Have: CIO, CTO
   Nice-to-Have: CISO, CDO

...

--- Copy-Paste Ready ---
[Formatted text block appropriate for the use case]
```

Use the clipboard API with 3-tier fallback (navigator.clipboard → execCommand → manual select).
Show a toast notification on copy success.
