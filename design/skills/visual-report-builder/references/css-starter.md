# CSS Starter Template

> Read this file when starting a new report. Copy the custom property block and adapt
> the palette to the brand. The class names below use `{p}` as a placeholder for your
> project prefix (e.g., `mvajv`, `span`, `amp`).

## Neutral Dark Palette (default when no brand skill applies)

```css
.{p}-root {
  --{p}-bg:           #0a0a14;
  --{p}-surface:      #14141f;
  --{p}-surface-2:    #1c1c2a;
  --{p}-line:         #2a2a3a;
  --{p}-line-2:       #3a3a4d;
  --{p}-text:         #f0eee6;
  --{p}-text-2:       #a8a5b0;
  --{p}-text-3:       #6e6b7a;

  --{p}-accent:       #9333ea;
  --{p}-accent-glow:  #c084fc;
  --{p}-positive:     #34d399;
  --{p}-warning:      #fbbf24;
  --{p}-negative:     #ef4444;
  --{p}-info:         #60a5fa;

  --{p}-display: 'Fraunces', Georgia, serif;
  --{p}-body:    'Montserrat', system-ui, sans-serif;
  --{p}-mono:    'JetBrains Mono', ui-monospace, monospace;

  font-family: var(--{p}-body);
  background: var(--{p}-bg);
  color: var(--{p}-text);
  font-size: 15px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
```

## Brand Palette Mappings

When a brand skill is loaded, remap the accent and (optionally) surface colors.
Always pull values from the actual brand skill, not from memory.

### LakeB2B (from lakeb2b-brand-guidelines)
```
--accent:       #6D08BE  (LakeB2B Purple, primary brand color, 60% gradient share)
--accent-glow:  #7A76DA  (LakeB2B Lavender)
--positive:     #0095A0  (LakeB2B Teal)
--warning:      #FFB703  (LakeB2B Gold)
--negative:     #E8033A  (LakeB2B Red)
```
Full primary: Purple #6D08BE (60%), Red #E8033A (20%), Gold #FFB703 (20%).
Secondary: Magenta #DD1286, Teal #0095A0, Lavender #7A76DA, Bright Orange #FF6903, Navy #011A6B.
Font: Montserrat (primary), Alata (secondary).

### SPAN Global Services
```
--accent:       #1E8C68  (SPAN Green, primary brand color)
--accent-glow:  #60C8A0  (SPAN Green light variant)
--positive:     #3D9648  (SPAN Green secondary)
--warning:      #A07818  (SPAN Gold)
--negative:     #c0392b  (SPAN Red)
--info:         #3B7BD5  (SPAN Blue, secondary)
```
Extended: Blue #3B7BD5, Orange #C96828, Gold #A07818, Purple #905080.
No dedicated brand skill yet. Primary green confirmed by user.

### Ampliz (from ampliz-brand-guidelines)
```
--accent:       #0071EB  (Ampliz Blue, THE brand color)
--accent-glow:  #0058B8  (Ampliz Mid Blue)
--positive:     #15803D  (Success Green, sparingly)
--warning:      #FE7678  (Ampliz Coral, accent max 15%)
--negative:     #B91C1C  (Alert Red)
```
Extended: Light Blue #E6F0FD, Dark Blue #003D80, Coral #FFC5C6.
Healthcare gradient: #0071EB to #00A3E0. Font: Roboto (300-900).

### Champions Group (from champions-group-brand)
```
--accent:       #F26722  (Champions Orange, THE brand color)
--accent-glow:  #FF8544  (Bright Orange)
--positive:     #15803D  (Success Green, sparingly)
--warning:      #D94F0A  (Deep Orange, hover/emphasis)
--negative:     #B91C1C  (Alert Red)
```
Extended: Soft Peach #FFF4EC, Warm Tint #FFE8D6, Ink #1A1A1A.
Gradient hero: #F26722 to #D94F0A. Font: Inter (web), Calibri (docs).

## Google Fonts Preconnect Block

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..700&family=JetBrains+Mono:wght@400;500;700&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

Swap font families as needed for brand, but maintain the three-tier system:
display (serif), body (sans), mono.

## Type Scale

```
h1:              clamp(38px, 9vw, 88px)   display, weight 400, tracking -0.03em
h2:              clamp(26px, 6.5vw, 44px) display, weight 450, tracking -0.02em
h3:              clamp(18px, 4vw, 24px)   display, weight 500
body:            15px                      body font
stat number:     clamp(28px, 8vw, 44px)   display, weight 500, tabular-nums
kicker/label:    10-11px                   mono, uppercase, tracking 0.18-0.24em
card title:      14px                      body, weight 700, tracking 0.04em, uppercase
card meta:       11px                      mono, tracking 0.06em
```

## Responsive Breakpoints

```css
/* Mobile-first base styles */

@media (min-width: 720px) {
  /* Stat strips: single row */
  /* Split grids: side-by-side */
  /* Action grids: 2-4 columns */
}

@media (min-width: 1024px) {
  /* Optional: wider layouts, more columns */
}
```

## Accessibility Baseline

```css
@media (prefers-reduced-motion: reduce) {
  .{p}-root *, .{p}-root *::before, .{p}-root *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
