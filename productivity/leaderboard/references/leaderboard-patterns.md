# Leaderboard Patterns Reference

> Read this file before writing any leaderboard HTML. Contains the complete CSS system,
> component templates, brand adaptation, print styles, and live artifact boilerplate.
> Inherits from visual-report-builder's design methodology (css-starter.md).

---

## Table of Contents

1. [CSS Custom Properties](#1-css-custom-properties)
2. [Podium Component](#2-podium-component)
3. [Ranking Table](#3-ranking-table)
4. [Delta Badges & Trend Arrows](#4-delta-badges--trend-arrows)
5. [Metric Summary Cards](#5-metric-summary-cards)
6. [Topbar & Footer](#6-topbar--footer)
7. [Print Stylesheet](#7-print-stylesheet)
8. [Wall-Display Mode](#8-wall-display-mode)
9. [Brand Color Mappings](#9-brand-color-mappings)
10. [Live Artifact Boilerplate](#10-live-artifact-boilerplate)
11. [Static HTML Boilerplate](#11-static-html-boilerplate)
12. [Responsive Breakpoints](#12-responsive-breakpoints)

---

## 1. CSS Custom Properties

Use `lb` as the project prefix. Inherits the three-tier type system from css-starter.md.

```css
.lb-root {
  /* Surfaces */
  --lb-bg:           #0a0a14;
  --lb-surface:      #14141f;
  --lb-surface-2:    #1c1c2a;
  --lb-line:         #2a2a3a;
  --lb-line-2:       #3a3a4d;

  /* Text */
  --lb-text:         #f0eee6;
  --lb-text-2:       #a8a5b0;
  --lb-text-3:       #6e6b7a;

  /* Semantic */
  --lb-accent:       #9333ea;
  --lb-accent-glow:  #c084fc;
  --lb-positive:     #34d399;
  --lb-warning:      #fbbf24;
  --lb-negative:     #ef4444;
  --lb-info:         #60a5fa;

  /* Podium-specific */
  --lb-gold:         #fbbf24;
  --lb-gold-glow:    rgba(251, 191, 36, 0.15);
  --lb-silver:       #94a3b8;
  --lb-silver-glow:  rgba(148, 163, 184, 0.10);
  --lb-bronze:       #d97706;
  --lb-bronze-glow:  rgba(217, 119, 6, 0.10);

  /* Typography */
  --lb-display: 'Fraunces', Georgia, serif;
  --lb-body:    'Montserrat', system-ui, sans-serif;
  --lb-mono:    'JetBrains Mono', ui-monospace, monospace;

  /* Spacing */
  --lb-gap:     clamp(16px, 3vw, 32px);
  --lb-radius:  12px;
  --lb-radius-sm: 6px;

  font-family: var(--lb-body);
  background: var(--lb-bg);
  color: var(--lb-text);
  font-size: 15px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
```

### Google Fonts Block

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..700&family=JetBrains+Mono:wght@400;500;700&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

---

## 2. Podium Component

The podium is the emotional centerpiece. Top 3 get hero treatment. #1 is center and
tallest, #2 flanks left, #3 flanks right. On mobile, stack vertically with #1 on top.

### Layout

```css
.lb-podium {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: var(--lb-gap);
  padding: clamp(24px, 5vw, 48px) 0;
}

.lb-podium-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: clamp(20px, 3vw, 32px);
  border-radius: var(--lb-radius);
  background: var(--lb-surface);
  border: 1px solid var(--lb-line);
  position: relative;
  transition: transform 0.2s ease;
}

/* #1: Center, tallest */
.lb-podium-card[data-rank="1"] {
  order: 2;
  min-height: 240px;
  border-color: var(--lb-gold);
  background: linear-gradient(180deg, var(--lb-gold-glow) 0%, var(--lb-surface) 60%);
  transform: scale(1.08);
}

/* #2: Left */
.lb-podium-card[data-rank="2"] {
  order: 1;
  min-height: 200px;
  border-color: var(--lb-silver);
  background: linear-gradient(180deg, var(--lb-silver-glow) 0%, var(--lb-surface) 60%);
}

/* #3: Right */
.lb-podium-card[data-rank="3"] {
  order: 3;
  min-height: 180px;
  border-color: var(--lb-bronze);
  background: linear-gradient(180deg, var(--lb-bronze-glow) 0%, var(--lb-surface) 60%);
}
```

### Position Badge

```css
.lb-position-badge {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--lb-mono);
  font-weight: 700;
  font-size: 14px;
  color: var(--lb-bg);
  margin-bottom: 12px;
}

.lb-position-badge[data-rank="1"] { background: var(--lb-gold); }
.lb-position-badge[data-rank="2"] { background: var(--lb-silver); }
.lb-position-badge[data-rank="3"] { background: var(--lb-bronze); }
```

### Podium Name & Score

```css
.lb-podium-name {
  font-family: var(--lb-body);
  font-weight: 700;
  font-size: clamp(14px, 2.5vw, 18px);
  color: var(--lb-text);
  margin-bottom: 4px;
  letter-spacing: 0.02em;
}

.lb-podium-score {
  font-family: var(--lb-display);
  font-weight: 500;
  font-size: clamp(28px, 8vw, 48px);
  color: var(--lb-accent-glow);
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
}

.lb-podium-card[data-rank="1"] .lb-podium-score {
  font-size: clamp(36px, 10vw, 64px);
  color: var(--lb-gold);
}

.lb-podium-metric-label {
  font-family: var(--lb-mono);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--lb-text-3);
  margin-top: 4px;
}
```

### HTML Template

```html
<div class="lb-podium">
  <!-- #2 -->
  <div class="lb-podium-card" data-rank="2">
    <div class="lb-position-badge" data-rank="2">2</div>
    <div class="lb-podium-name">Lam</div>
    <div class="lb-podium-score">87</div>
    <div class="lb-podium-metric-label">Deals Closed</div>
    <div class="lb-delta lb-delta-up">+12</div>
  </div>
  <!-- #1 -->
  <div class="lb-podium-card" data-rank="1">
    <div class="lb-position-badge" data-rank="1">1</div>
    <div class="lb-podium-name">Gary</div>
    <div class="lb-podium-score">112</div>
    <div class="lb-podium-metric-label">Deals Closed</div>
    <div class="lb-delta lb-delta-up">+24</div>
  </div>
  <!-- #3 -->
  <div class="lb-podium-card" data-rank="3">
    <div class="lb-position-badge" data-rank="3">3</div>
    <div class="lb-podium-name">Tim</div>
    <div class="lb-podium-score">71</div>
    <div class="lb-podium-metric-label">Deals Closed</div>
    <div class="lb-delta lb-delta-down">-3</div>
  </div>
</div>
```

### Edge Cases

- **2 participants:** Remove data-rank="3" card. Show #1 center, #2 right, empty left.
- **1 participant:** Single hero card, centered, no podium layout. Use a solo hero section.
- **Tie:** Show both at same rank. Both cards get the same position badge and border color.
  Adjust `order` so tied cards sit side by side.

---

## 3. Ranking Table

The full ranking list below the podium. All participants, including top 3 (repeated
for completeness). Optimized for scan speed: position, name, score, delta, trend.

### Table CSS

```css
.lb-table-wrap {
  overflow-x: auto;
  margin: var(--lb-gap) 0;
}

.lb-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 14px;
}

.lb-table thead th {
  font-family: var(--lb-mono);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--lb-text-3);
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--lb-line);
  position: sticky;
  top: 0;
  background: var(--lb-bg);
  z-index: 2;
}

.lb-table thead th.lb-col-num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.lb-table tbody tr {
  transition: background 0.15s ease;
}

.lb-table tbody tr:hover {
  background: var(--lb-surface);
}

.lb-table tbody tr:nth-child(even) {
  background: var(--lb-surface);
}

.lb-table tbody tr:nth-child(even):hover {
  background: var(--lb-surface-2);
}

.lb-table tbody td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--lb-line);
  vertical-align: middle;
}

/* Position column */
.lb-table .lb-col-rank {
  width: 48px;
  text-align: center;
}

.lb-rank-num {
  font-family: var(--lb-mono);
  font-weight: 700;
  font-size: 14px;
  color: var(--lb-accent-glow);
}

/* Top 3 get colored rank numbers */
tr[data-rank="1"] .lb-rank-num { color: var(--lb-gold); }
tr[data-rank="2"] .lb-rank-num { color: var(--lb-silver); }
tr[data-rank="3"] .lb-rank-num { color: var(--lb-bronze); }

/* Name column */
.lb-col-name {
  font-weight: 600;
  color: var(--lb-text);
}

/* Score column */
.lb-col-score {
  font-family: var(--lb-mono);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  text-align: right;
  color: var(--lb-text);
}

/* Delta column */
.lb-col-delta {
  text-align: right;
  width: 80px;
}

/* Trend column */
.lb-col-trend {
  text-align: center;
  width: 48px;
}
```

### HTML Template

```html
<div class="lb-table-wrap">
  <table class="lb-table">
    <thead>
      <tr>
        <th class="lb-col-rank">#</th>
        <th>Name</th>
        <th class="lb-col-num">Score</th>
        <th class="lb-col-num">Delta</th>
        <th class="lb-col-trend">Trend</th>
      </tr>
    </thead>
    <tbody>
      <tr data-rank="1">
        <td class="lb-col-rank"><span class="lb-rank-num">1</span></td>
        <td class="lb-col-name">Gary</td>
        <td class="lb-col-score">112</td>
        <td class="lb-col-delta"><span class="lb-delta lb-delta-up">+24</span></td>
        <td class="lb-col-trend">
          <svg class="lb-trend-arrow lb-trend-up" width="16" height="16" viewBox="0 0 16 16">
            <path d="M8 3L13 9H3Z" fill="var(--lb-positive)"/>
          </svg>
        </td>
      </tr>
      <!-- repeat for each participant -->
    </tbody>
  </table>
</div>
```

---

## 4. Delta Badges & Trend Arrows

### Delta Badges

Pill-shaped inline indicators showing change from previous period.

```css
.lb-delta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 10px;
  border-radius: 999px;
  font-family: var(--lb-mono);
  font-size: 12px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.lb-delta-up {
  color: var(--lb-positive);
  background: rgba(52, 211, 153, 0.10);
}

.lb-delta-down {
  color: var(--lb-negative);
  background: rgba(239, 68, 68, 0.10);
}

.lb-delta-flat {
  color: var(--lb-text-3);
  background: rgba(110, 107, 122, 0.10);
}
```

### Trend Arrows (inline SVG)

Use inline SVG, not emoji. Consistent across all screens and print.

```html
<!-- Up arrow -->
<svg class="lb-trend-arrow lb-trend-up" width="16" height="16" viewBox="0 0 16 16" fill="none">
  <path d="M8 3L13 9H3Z" fill="var(--lb-positive)"/>
</svg>

<!-- Down arrow -->
<svg class="lb-trend-arrow lb-trend-down" width="16" height="16" viewBox="0 0 16 16" fill="none">
  <path d="M8 13L3 7H13Z" fill="var(--lb-negative)"/>
</svg>

<!-- Flat / no change -->
<svg class="lb-trend-arrow lb-trend-flat" width="16" height="16" viewBox="0 0 16 16" fill="none">
  <rect x="3" y="7" width="10" height="2" rx="1" fill="var(--lb-text-3)"/>
</svg>

<!-- Strong up (double arrow) -->
<svg class="lb-trend-arrow lb-trend-surge" width="16" height="16" viewBox="0 0 16 16" fill="none">
  <path d="M8 1L13 6H3Z" fill="var(--lb-positive)"/>
  <path d="M8 6L13 11H3Z" fill="var(--lb-positive)" opacity="0.5"/>
</svg>
```

```css
.lb-trend-arrow {
  vertical-align: middle;
  flex-shrink: 0;
}
```

### Position Change Badge

Shows how many spots a person moved since last period.

```css
.lb-pos-change {
  font-family: var(--lb-mono);
  font-size: 11px;
  font-weight: 600;
}

.lb-pos-change-up { color: var(--lb-positive); }
.lb-pos-change-up::before { content: "\25B2 "; font-size: 8px; }

.lb-pos-change-down { color: var(--lb-negative); }
.lb-pos-change-down::before { content: "\25BC "; font-size: 8px; }

.lb-pos-change-same { color: var(--lb-text-3); }
.lb-pos-change-same::before { content: "\2014 "; }
```

---

## 5. Metric Summary Cards

2 to 4 cards providing context to the rankings. Sits below the ranking table.

```css
.lb-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: var(--lb-gap);
  margin: var(--lb-gap) 0;
}

.lb-metric-card {
  background: var(--lb-surface);
  border: 1px solid var(--lb-line);
  border-radius: var(--lb-radius);
  padding: clamp(16px, 2.5vw, 24px);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.lb-metric-label {
  font-family: var(--lb-mono);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--lb-text-3);
}

.lb-metric-value {
  font-family: var(--lb-display);
  font-weight: 500;
  font-size: clamp(24px, 6vw, 36px);
  font-variant-numeric: tabular-nums;
  color: var(--lb-text);
  line-height: 1.1;
}

.lb-metric-context {
  font-family: var(--lb-body);
  font-size: 12px;
  color: var(--lb-text-2);
}
```

### HTML Template

```html
<div class="lb-metrics">
  <div class="lb-metric-card">
    <div class="lb-metric-label">Team Total</div>
    <div class="lb-metric-value">487</div>
    <div class="lb-metric-context">deals this quarter</div>
  </div>
  <div class="lb-metric-card">
    <div class="lb-metric-label">Team Average</div>
    <div class="lb-metric-value">81.2</div>
    <div class="lb-metric-context">per person</div>
  </div>
  <div class="lb-metric-card">
    <div class="lb-metric-label">Gap to #1</div>
    <div class="lb-metric-value" style="color: var(--lb-warning)">25</div>
    <div class="lb-metric-context">#2 behind leader</div>
  </div>
  <div class="lb-metric-card">
    <div class="lb-metric-label">Best Streak</div>
    <div class="lb-metric-value" style="color: var(--lb-gold)">5w</div>
    <div class="lb-metric-context">Gary at #1</div>
  </div>
</div>
```

### Suggested Metrics by Context

| Context | Good Cards |
|---------|-----------|
| Sales (pipeline) | Team Total, Average, Gap to #1, Biggest Mover |
| Sales (outreach) | Total Sent, Best Response Rate, Top Booker, Avg per Day |
| Activity | Team Total, Most Consistent, Biggest Spike, Days Active |
| Custom | Sum, Average, Gap, Streak (default set if nothing better fits) |

---

## 6. Topbar & Footer

### Topbar

```css
.lb-topbar {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: clamp(16px, 3vw, 24px) 0;
  border-bottom: 1px solid var(--lb-line);
  margin-bottom: var(--lb-gap);
}

.lb-topbar-title {
  font-family: var(--lb-display);
  font-weight: 450;
  font-size: clamp(22px, 5vw, 36px);
  letter-spacing: -0.02em;
  color: var(--lb-text);
}

.lb-topbar-kicker {
  font-family: var(--lb-mono);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.24em;
  color: var(--lb-accent-glow);
  display: block;
  margin-bottom: 4px;
}

.lb-topbar-meta {
  font-family: var(--lb-mono);
  font-size: 11px;
  color: var(--lb-text-3);
  text-align: right;
}
```

### HTML

```html
<header class="lb-topbar">
  <div>
    <span class="lb-topbar-kicker">Phoenix Team</span>
    <h1 class="lb-topbar-title">Pipeline Leaderboard</h1>
  </div>
  <div class="lb-topbar-meta">
    <div>May 2026</div>
    <div>Updated <time id="lb-updated"></time></div>
  </div>
</header>
```

### Footer

```css
.lb-footer {
  padding: clamp(12px, 2vw, 20px) 0;
  border-top: 1px solid var(--lb-line);
  margin-top: var(--lb-gap);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lb-footer-source {
  font-family: var(--lb-mono);
  font-size: 10px;
  color: var(--lb-text-3);
  letter-spacing: 0.06em;
}

.lb-footer-brand {
  font-family: var(--lb-mono);
  font-size: 10px;
  color: var(--lb-text-3);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
```

---

## 7. Print Stylesheet

Critical for physical leaderboard printouts. Switch to light background, ensure all
text is dark, hide interactive elements, and add a print header.

```css
@media print {
  .lb-root {
    background: #ffffff !important;
    color: #1a1a1a !important;
    font-size: 12px;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .lb-topbar, .lb-footer {
    border-color: #d0d0d0 !important;
  }

  .lb-topbar-kicker {
    color: #555 !important;
  }

  .lb-topbar-title {
    color: #1a1a1a !important;
  }

  .lb-topbar-meta {
    color: #666 !important;
  }

  .lb-podium-card {
    background: #f8f8f8 !important;
    border-color: #d0d0d0 !important;
    box-shadow: none !important;
  }

  .lb-podium-card[data-rank="1"] {
    border-color: #b8860b !important;
    background: #fff8e7 !important;
  }

  .lb-podium-card[data-rank="2"] {
    border-color: #808080 !important;
    background: #f5f5f5 !important;
  }

  .lb-podium-card[data-rank="3"] {
    border-color: #a0522d !important;
    background: #fef6f0 !important;
  }

  .lb-podium-name { color: #1a1a1a !important; }
  .lb-podium-score { color: #1a1a1a !important; }
  .lb-podium-card[data-rank="1"] .lb-podium-score { color: #8b6914 !important; }

  .lb-table thead th {
    background: #ffffff !important;
    color: #555 !important;
    border-bottom-color: #333 !important;
  }

  .lb-table tbody tr:nth-child(even) {
    background: #f5f5f5 !important;
  }

  .lb-table tbody tr:hover {
    background: inherit !important;
  }

  .lb-table tbody td {
    border-bottom-color: #e0e0e0 !important;
    color: #1a1a1a !important;
  }

  .lb-rank-num { color: #333 !important; }
  tr[data-rank="1"] .lb-rank-num { color: #8b6914 !important; }
  tr[data-rank="2"] .lb-rank-num { color: #666 !important; }
  tr[data-rank="3"] .lb-rank-num { color: #8b4513 !important; }

  .lb-col-score { color: #1a1a1a !important; }

  .lb-delta-up { color: #15803d !important; background: transparent !important; }
  .lb-delta-down { color: #b91c1c !important; background: transparent !important; }
  .lb-delta-flat { color: #666 !important; background: transparent !important; }

  .lb-metric-card {
    background: #f8f8f8 !important;
    border-color: #d0d0d0 !important;
  }

  .lb-metric-label { color: #555 !important; }
  .lb-metric-value { color: #1a1a1a !important; }
  .lb-metric-context { color: #666 !important; }

  .lb-footer-source, .lb-footer-brand { color: #888 !important; }

  /* Hide interactive-only elements */
  .lb-refresh-btn,
  .lb-auto-scroll { display: none !important; }

  /* Force page break before table if podium is long */
  .lb-table-wrap { page-break-before: auto; }

  /* Print header */
  .lb-print-header {
    display: block !important;
    text-align: center;
    font-family: var(--lb-body);
    font-size: 10px;
    color: #888;
    margin-bottom: 12px;
  }
}

/* Hide print header on screen */
.lb-print-header { display: none; }
```

---

## 8. Wall-Display Mode

For leaderboards on mounted screens. Large type, high contrast, optional auto-scroll.

```css
.lb-root.lb-wall-mode {
  /* Override type scale for distance readability (3+ meters) */
  --lb-wall-score-size: clamp(48px, 12vw, 96px);
  --lb-wall-name-size:  clamp(20px, 4vw, 32px);
  --lb-wall-rank-size:  clamp(14px, 3vw, 22px);
}

.lb-wall-mode .lb-podium-score {
  font-size: var(--lb-wall-score-size);
}

.lb-wall-mode .lb-podium-name {
  font-size: var(--lb-wall-name-size);
}

.lb-wall-mode .lb-table {
  font-size: clamp(14px, 2.5vw, 20px);
}

.lb-wall-mode .lb-table tbody td {
  padding: 18px 20px;
}

.lb-wall-mode .lb-metric-value {
  font-size: clamp(32px, 8vw, 56px);
}
```

### Auto-Scroll for Long Lists

```css
@keyframes lb-scroll {
  0%   { transform: translateY(0); }
  40%  { transform: translateY(0); }
  60%  { transform: translateY(calc(-100% + 100vh)); }
  100% { transform: translateY(calc(-100% + 100vh)); }
}

.lb-auto-scroll .lb-table-wrap {
  animation: lb-scroll 20s ease-in-out infinite;
  overflow: hidden;
}

/* Pause on hover (for interactive screens) */
.lb-auto-scroll .lb-table-wrap:hover {
  animation-play-state: paused;
}
```

### Auto-Refresh Indicator

```css
.lb-refresh-indicator {
  position: fixed;
  bottom: 16px;
  right: 16px;
  font-family: var(--lb-mono);
  font-size: 10px;
  color: var(--lb-text-3);
  background: var(--lb-surface);
  padding: 4px 10px;
  border-radius: var(--lb-radius-sm);
  border: 1px solid var(--lb-line);
  opacity: 0.6;
}
```

---

## 9. Brand Color Mappings

Same source as css-starter.md. Brand is a color swap on the accent/semantic properties.
Everything else (layout, type, patterns) stays identical.

### LakeB2B

```css
.lb-root.lb-brand-lakeb2b {
  --lb-accent:       #6D08BE;
  --lb-accent-glow:  #7A76DA;
  --lb-positive:     #0095A0;
  --lb-warning:      #FFB703;
  --lb-negative:     #E8033A;
}
```

### SPAN Global Services

```css
.lb-root.lb-brand-span {
  --lb-accent:       #1E8C68;
  --lb-accent-glow:  #60C8A0;
  --lb-positive:     #3D9648;
  --lb-warning:      #A07818;
  --lb-negative:     #c0392b;
  --lb-info:         #3B7BD5;
}
```

### Ampliz

```css
.lb-root.lb-brand-ampliz {
  --lb-accent:       #0071EB;
  --lb-accent-glow:  #0058B8;
  --lb-positive:     #15803D;
  --lb-warning:      #FE7678;
  --lb-negative:     #B91C1C;
}
```

### Champions Group

```css
.lb-root.lb-brand-champions {
  --lb-accent:       #F26722;
  --lb-accent-glow:  #FF8544;
  --lb-positive:     #15803D;
  --lb-warning:      #D94F0A;
  --lb-negative:     #B91C1C;
}
```

### Brand Selection Logic

1. If a brand skill is loaded or user specified a brand, use that mapping.
2. If context is Champions Group internal and no brand specified, default to Champions Orange.
3. If context is a specific subsidiary (SPAN, Ampliz, Lake B2B), use that brand.
4. If no brand context at all, use the neutral dark palette (purple accent).

Apply brand via a class on the root element: `<div class="lb-root lb-brand-span">`.

---

## 10. Live Artifact Boilerplate

Use this when building a Cowork artifact that refreshes data on each page load.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{LEADERBOARD_TITLE}}</title>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..700&family=JetBrains+Mono:wght@400;500;700&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* === Paste full .lb-root custom properties here === */
    /* === Paste all component CSS here === */
    /* === Paste print stylesheet here === */
    /* === Paste wall-display mode if needed === */

    @media (prefers-reduced-motion: reduce) {
      .lb-root *, .lb-root *::before, .lb-root *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body>
<div class="lb-root {{BRAND_CLASS}}">

  <div class="lb-print-header">
    {{LEADERBOARD_TITLE}} | Printed <span id="lb-print-date"></span>
  </div>

  <header class="lb-topbar">
    <div>
      <span class="lb-topbar-kicker">{{TEAM_NAME}}</span>
      <h1 class="lb-topbar-title">{{METRIC_NAME}} Leaderboard</h1>
    </div>
    <div class="lb-topbar-meta">
      <div>{{PERIOD_LABEL}}</div>
      <div>Updated <time id="lb-updated"></time></div>
    </div>
  </header>

  <div class="lb-podium" id="lb-podium">
    <!-- Populated by JS -->
  </div>

  <div class="lb-table-wrap">
    <table class="lb-table">
      <thead>
        <tr>
          <th class="lb-col-rank">#</th>
          <th>Name</th>
          <th class="lb-col-num">{{METRIC_NAME}}</th>
          <th class="lb-col-num">Delta</th>
          <th class="lb-col-trend">Trend</th>
        </tr>
      </thead>
      <tbody id="lb-tbody">
        <!-- Populated by JS -->
      </tbody>
    </table>
  </div>

  <div class="lb-metrics" id="lb-metrics">
    <!-- Populated by JS -->
  </div>

  <footer class="lb-footer">
    <div class="lb-footer-source">Source: {{DATA_SOURCE}}</div>
    <div class="lb-footer-brand">{{BRAND_LABEL}}</div>
  </footer>

</div>

<script>
// ============================================================
// LIVE ARTIFACT DATA LAYER
// ============================================================
// This script fetches data from connected MCPs on each page load.
// Replace the fetchData() function body with the actual MCP calls
// needed for this specific leaderboard.

const METRIC_NAME = '{{METRIC_NAME}}';
const HIGHER_IS_BETTER = true; // flip for metrics like response time

// SVG arrow templates
const ARROW_UP = '<svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 3L13 9H3Z" fill="var(--lb-positive)"/></svg>';
const ARROW_DOWN = '<svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 13L3 7H13Z" fill="var(--lb-negative)"/></svg>';
const ARROW_FLAT = '<svg width="16" height="16" viewBox="0 0 16 16"><rect x="3" y="7" width="10" height="2" rx="1" fill="var(--lb-text-3)"/></svg>';

async function fetchData() {
  // REPLACE THIS with actual MCP calls. Example:
  // const result = await window.cowork.callMcpTool('outlook_email_search', { ... });
  // Return array of { name, score, prevScore } objects.

  // Placeholder data for template:
  return [
    { name: 'Person A', score: 112, prevScore: 88 },
    { name: 'Person B', score: 87,  prevScore: 75 },
    { name: 'Person C', score: 71,  prevScore: 74 },
  ];
}

function buildLeaderboard(data) {
  // Sort
  data.sort((a, b) => HIGHER_IS_BETTER ? b.score - a.score : a.score - b.score);

  // Assign ranks (handle ties)
  let rank = 1;
  data.forEach((d, i) => {
    if (i > 0 && d.score === data[i - 1].score) {
      d.rank = data[i - 1].rank;
    } else {
      d.rank = rank;
    }
    rank++;
    d.delta = d.prevScore != null ? d.score - d.prevScore : null;
  });

  renderPodium(data.slice(0, 3));
  renderTable(data);
  renderMetrics(data);

  document.getElementById('lb-updated').textContent = new Date().toLocaleString();
  const printDate = document.getElementById('lb-print-date');
  if (printDate) printDate.textContent = new Date().toLocaleDateString();
}

function renderPodium(top3) {
  const podium = document.getElementById('lb-podium');
  podium.innerHTML = '';
  const order = [1, 0, 2]; // display order: #2, #1, #3
  order.forEach(idx => {
    if (!top3[idx]) return;
    const d = top3[idx];
    const card = document.createElement('div');
    card.className = 'lb-podium-card';
    card.dataset.rank = d.rank;
    card.innerHTML = `
      <div class="lb-position-badge" data-rank="${d.rank}">${d.rank}</div>
      <div class="lb-podium-name">${d.name}</div>
      <div class="lb-podium-score">${d.score.toLocaleString()}</div>
      <div class="lb-podium-metric-label">${METRIC_NAME}</div>
      ${d.delta != null ? `<div class="lb-delta ${d.delta > 0 ? 'lb-delta-up' : d.delta < 0 ? 'lb-delta-down' : 'lb-delta-flat'}">${d.delta > 0 ? '+' : ''}${d.delta}</div>` : ''}
    `;
    podium.appendChild(card);
  });
}

function renderTable(data) {
  const tbody = document.getElementById('lb-tbody');
  tbody.innerHTML = '';
  data.forEach(d => {
    const arrow = d.delta > 0 ? ARROW_UP : d.delta < 0 ? ARROW_DOWN : ARROW_FLAT;
    const deltaClass = d.delta > 0 ? 'lb-delta-up' : d.delta < 0 ? 'lb-delta-down' : 'lb-delta-flat';
    const tr = document.createElement('tr');
    tr.dataset.rank = d.rank;
    tr.innerHTML = `
      <td class="lb-col-rank"><span class="lb-rank-num">${d.rank}</span></td>
      <td class="lb-col-name">${d.name}</td>
      <td class="lb-col-score">${d.score.toLocaleString()}</td>
      <td class="lb-col-delta">${d.delta != null ? `<span class="lb-delta ${deltaClass}">${d.delta > 0 ? '+' : ''}${d.delta}</span>` : '<span class="lb-delta lb-delta-flat">-</span>'}</td>
      <td class="lb-col-trend">${d.delta != null ? arrow : ARROW_FLAT}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderMetrics(data) {
  const metrics = document.getElementById('lb-metrics');
  const total = data.reduce((s, d) => s + d.score, 0);
  const avg = (total / data.length).toFixed(1);
  const gap = data.length > 1 ? data[0].score - data[1].score : 0;

  metrics.innerHTML = `
    <div class="lb-metric-card">
      <div class="lb-metric-label">Team Total</div>
      <div class="lb-metric-value">${total.toLocaleString()}</div>
      <div class="lb-metric-context">${METRIC_NAME.toLowerCase()} combined</div>
    </div>
    <div class="lb-metric-card">
      <div class="lb-metric-label">Average</div>
      <div class="lb-metric-value">${avg}</div>
      <div class="lb-metric-context">per person</div>
    </div>
    <div class="lb-metric-card">
      <div class="lb-metric-label">Gap to #1</div>
      <div class="lb-metric-value" style="color: var(--lb-warning)">${gap}</div>
      <div class="lb-metric-context">#2 is ${gap} behind</div>
    </div>
  `;
}

// Init
fetchData().then(buildLeaderboard).catch(err => {
  console.error('Leaderboard data fetch failed:', err);
  document.getElementById('lb-tbody').innerHTML =
    '<tr><td colspan="5" style="text-align:center;color:var(--lb-text-3);padding:40px">Data unavailable. Check connector access.</td></tr>';
});
</script>
</body>
</html>
```

---

## 11. Static HTML Boilerplate

Use this when building from user-provided data (no live refresh needed). Same structure
as the live version, but data is embedded directly in the HTML.

The key difference: replace the `fetchData()` function with a hardcoded array:

```javascript
async function fetchData() {
  return [
    { name: 'Gary',    score: 112, prevScore: 88 },
    { name: 'Lam',     score: 87,  prevScore: 75 },
    { name: 'Tim',     score: 71,  prevScore: 74 },
    { name: 'Travis',  score: 64,  prevScore: 61 },
    { name: 'Murugan', score: 58,  prevScore: 42 },
    { name: 'Preeti',  score: 52,  prevScore: 55 },
  ];
}
```

Save as a single `.html` file in the workspace folder. Provide a `computer://` link.

---

## 12. Responsive Breakpoints

```css
/* Mobile-first: podium stacks vertically */
@media (max-width: 719px) {
  .lb-podium {
    flex-direction: column;
    align-items: center;
  }

  .lb-podium-card {
    width: 100%;
    max-width: 320px;
  }

  .lb-podium-card[data-rank="1"] { order: 1; }
  .lb-podium-card[data-rank="2"] { order: 2; }
  .lb-podium-card[data-rank="3"] { order: 3; }

  .lb-podium-card[data-rank="1"] {
    transform: none;
  }

  .lb-topbar {
    flex-direction: column;
    gap: 8px;
  }

  .lb-topbar-meta { text-align: left; }

  .lb-footer {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}

/* Tablet+: podium side-by-side */
@media (min-width: 720px) {
  .lb-podium-card {
    flex: 1;
    max-width: 240px;
  }
}

/* Desktop: wider table, more breathing room */
@media (min-width: 1024px) {
  .lb-root {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 clamp(16px, 3vw, 40px);
  }
}
```

---

## Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  .lb-root *, .lb-root *::before, .lb-root *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Focus visible for keyboard navigation */
.lb-table tbody tr:focus-visible {
  outline: 2px solid var(--lb-accent-glow);
  outline-offset: -2px;
}
```

Trend arrows use semantic fill colors (green/red/gray) which are distinguishable
even without color via the arrow direction (up/down/flat shape).
