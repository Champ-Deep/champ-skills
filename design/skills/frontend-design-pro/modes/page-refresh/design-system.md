# Page Refresh: Design System Reference

Tokens, presets, and component snippets for the page-refresh skill.

## Brand palette presets

Each preset defines the four CSS variables the template expects. Set these once at `:root` and the rest of the page styles itself.

```css
/* Tokens used by template */
--brand-primary       /* Hero gradient start, primary CTA, links, accents */
--brand-primary-deep  /* CTA hover, gradient end, section accents */
--brand-accent        /* Result strip highlights, secondary chart fills */
--brand-gold          /* The "outcome" highlight reserved for big wins and CTAs */
```

### LakeB2B (default for B2B growth content)

```css
--brand-primary: #6D08BE;     /* Purple */
--brand-primary-deep: #4A0581;
--brand-accent: #DD1286;      /* Magenta */
--brand-gold: #FFB703;        /* Gold */
--brand-navy: #011A6B;
```

Typography: Montserrat (primary), Alata (accent), JetBrains Mono (technical).
Tagline: ENABLING GROWTH.
Category positioning: "the B2B growth stack".

### Ampliz (healthcare and B2B data intelligence)

```css
--brand-primary: #0095A0;     /* Teal */
--brand-primary-deep: #00646B;
--brand-accent: #FF6903;      /* Bright Orange */
--brand-gold: #FFB703;
--brand-navy: #011A6B;
```

Typography: Montserrat (primary), Alata (accent), JetBrains Mono (technical).
Use case: Healthcare data, prospect intelligence, anything Ampliz/Charles/Assassins.

### SPAN Global Services (Phoenix team)

```css
--brand-primary: #1E40AF;     /* Deep Blue */
--brand-primary-deep: #1E3A8A;
--brand-accent: #FF6903;      /* Bright Orange */
--brand-gold: #FFB703;
--brand-navy: #0B1437;
```

Typography: Montserrat (primary), Inter (fallback), JetBrains Mono (technical).
Use case: SPAN sales decks, lead-gen landers, Phoenix team campaigns.

### Champions Group (parent brand, executive/corporate)

```css
--brand-primary: #F26722;     /* Champions Orange */
--brand-primary-deep: #D94F0A;
--brand-accent: #1A1A1A;      /* Near-black */
--brand-gold: #FFB703;
--brand-navy: #0B1437;
```

Typography: Fraunces (editorial serif), Inter (body), JetBrains Mono (technical).
Use case: Group-level proposals, MOUs, prospectuses, investor decks, anything "Chief"/Sreedeep/parent-brand.

### Cirralogix

```css
--brand-primary: #0EA5E9;     /* Cyan */
--brand-primary-deep: #0369A1;
--brand-accent: #14B8A6;      /* Teal */
--brand-gold: #FFB703;
--brand-navy: #0B1437;
```

Typography: Montserrat (primary), Inter (fallback), JetBrains Mono (technical).
Use case: Cirralogix client work, technical/SaaS content.

### Recruit Champ

```css
--brand-primary: #16A34A;     /* Green */
--brand-primary-deep: #15803D;
--brand-accent: #FFB703;      /* Gold */
--brand-gold: #F59E0B;
--brand-navy: #052E16;
```

Typography: Montserrat (primary), Inter (fallback), JetBrains Mono (technical).
Use case: Recruit Champ client-facing pages, RecruitTech content.

### Custom (user provides)

If the user gives a hex code, derive:

- `--brand-primary` = user's hex
- `--brand-primary-deep` = user's hex darkened 20% (use a contrast checker mentally or programmatically)
- `--brand-accent` = complementary or analogous hue
- `--brand-gold` = #FFB703 (always gold for outcome highlights, regardless of brand)

## Typography stacks

### Stack A: Editorial-Modern (default, LakeB2B/Ampliz/Cirralogix/Recruit Champ/SPAN)

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Alata&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
font-family: 'Montserrat', system-ui, sans-serif;       /* body, headings */
font-family: 'Alata', sans-serif;                       /* eyebrows, tags, accent labels */
font-family: 'JetBrains Mono', monospace;               /* meta, technical, numerals */
```

### Stack B: Editorial-Classic (Champions Group, executive)

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,700;1,9..144,400;1,9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
font-family: 'Inter', system-ui, sans-serif;            /* body */
font-family: 'Fraunces', serif;                         /* headings, editorial italics */
font-family: 'JetBrains Mono', monospace;               /* meta, technical */
```

## Spacing and layout tokens

```css
:root {
  --container-max: 1180px;
  --section-pad: clamp(48px, 7vw, 80px);
  --hero-pad: clamp(40px, 8vw, 80px);
  --card-pad: clamp(16px, 3vw, 28px);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --line: #E5E7EB;
  --line-strong: #D1D5DB;
  --surface: #FAFAFB;
  --text: #0F0A1A;
  --text-2: #2E2A3A;
  --text-3: #6B6776;
}
```

Break at `820px` for desktop-to-tablet collapse. Break at `600px` for mobile-specific tweaks.

## Component patterns (semantic guidance)

These are conceptual descriptions. See `template.html` for the actual implementations.

### Nav

Sticky top bar. Gradient logo mark (square, 32px, two-color brand gradient). Logo text in brand-primary. Right side: 4 to 5 links + one primary CTA pill. Tagline ("Enabling Growth", etc.) under the logo in Alata uppercase small caps.

### Breadcrumb

JetBrains Mono, small (13px). Slashes as separators. Current page in brand-primary. Do not use chevrons.

### Hero (3-second value prop)

Two columns at 1.05fr 1fr. Left: eyebrow chip > H1 with one phrase in brand gradient > deck paragraph > meta strip (4 to 5 facts) > primary CTA + secondary CTA. Right: hero visual.

**The H1 rule**: pick ONE outcome-y phrase to wrap in `<span>` for the brand gradient. Example: "How a healthcare SaaS leader hit <span>4.2x pipeline</span> in 90 days."

**Hero visual rules**:
- If source has a time-series outcome (week 1 through week N, day 1 through day 90, Q1 through Q4): build an SVG line chart with area fill, dashed gridlines, dotted data points, and an oversized gold ring at the peak point. Add a dark-pill callout near the peak with the peak value and label. Add x-axis labels in JetBrains Mono.
- If source has discrete categorical outcomes (channel A vs B vs C, before vs after): build a 3 to 6 bar chart instead. Same brand gradient on bars representing the winning state.
- If source has no numerics: build a metric card with 1 to 3 oversized numbers stacked vertically.
- If source is heavily visual: build a screenshot frame placeholder with `[IMAGE: replace with product screenshot]`.
- Never use stock photos.
- The chart sits inside a white card with: header (title + subtitle + "Tracked weekly" live badge), chart wrapper with callout, x-axis labels, and a 3-KPI footer divided by vertical hairlines.
- The white card sits on a gradient brand box with: subtle grid pattern overlay, brand watermark in the top-right corner, and a floating gold "Real outcome" tag with a red pulsing dot anchored to the top-left edge.
- The hero-visual container uses `overflow: visible` so the floating tag is never clipped. Background gradients are layered directly on the container, not inside a `::before` (which would require overflow: hidden).

### Result strip

Full-bleed band in brand gradient. 4-column grid of giant numbers (clamp 36px to 56px). Unit characters (`%`, `x`) in `--brand-gold`. Label underneath in white-with-85%-opacity, max 2 lines.

If source has fewer than 4 strong metrics, drop this section. Do not invent.

### Section eyebrow + H2

Eyebrow in Alata uppercase with a 24px brand-primary dash before it. H2 in 800 weight, clamp(28px, 4vw, 42px), max-width 28ch. Then a deck paragraph max-width 56ch.

### Client/context card

2-column. Left: a label-value list (Sector, Stage, ICP, Team size, etc.). Right: a "honest situation" paragraph with a 3px brand-primary left border.

### Problem-Solution-Outcome (PSO) grid

3 cards side by side. Each card has a badge (red for problem, brand-soft for solution, green for outcome), an H3, a body paragraph, and a footer stat line. On hover: lift 2px, soft shadow.

### Playbook (3-phase timeline + numbered steps)

Phase bar: 3 equal columns in a single rounded container. Each column has a brand-gradient background (deepest > primary > magenta). White text. Phase label, title, day range.

Step grid: numbered Alata 36px brand-primary numerals on the left. Step content (H4, paragraph, tag pills) in the middle. Metric card with big brand-primary value on the right. 200px right column on desktop, full-width metric below content on mobile.

### Quote panel

Dark gradient background (brand-deep > navy). Huge open-quote glyph in gold at 15% opacity. Quote text in 500 weight, clamp(22px, 3vw, 32px). Attribution: 48px gradient-gold avatar circle (initials inside) + name + role.

### Outcomes table

White background, rounded 12px, border. Header in brand-soft surface with brand-primary mono uppercase labels. Body rows alternating subtle border. Numeric columns right-aligned, JetBrains Mono. Delta badges: green up, red down, with `+` or `-` prefix and `%` or `x` suffix.

### What's included grid

6 cards in a 3-column grid (collapses to 1 on mobile). Each card has the solution badge, H3, and short paragraph. Same hover lift as PSO cards.

### CTA banner

Brand-gradient background. 2 columns: 1.5fr text + 1fr action stack. H2 (clamp 26px to 36px) max 22ch. Sub-paragraph max 44ch. Two CTAs stacked vertically: gold primary + transparent-bordered secondary. Decorative radial-gradient blob top-right in gold at 25% opacity.

### Related grid

3 cards in a row. Each: small uppercase tag, H4 title, short description, brand-primary arrow CTA at the bottom. Hover: border becomes brand-primary, lift 2px.

### Footer

Dark (use `--text` as background). 4-column: brand block (logo + tagline + blurb) + 3 link columns. Tagline in gold uppercase Alata. Links in 70% white, hover to gold. Bottom row: copyright + timestamp.

## SEO fundamentals checklist (apply to every refresh)

1. `<title>` follows formula: `[Primary Keyword]. [Unique Value Prop] | [Brand]`
2. `<meta name="description">` is 140 to 158 chars, includes primary keyword in first half
3. H1 contains primary keyword OR the outcome (whichever is the page's main hook)
4. Hero visual shows the outcome, not a stock image
5. First above-the-fold message is comprehensible in 3 seconds without reading prose
6. CTA appears in hero, mid-page (after proof), and bottom banner. Three total, not more.
7. No em-dashes in any output (use periods, commas, colons)
8. Original data, not generic AI text. If the source did not have a number, do not invent one.
9. Alt text on every image and aria-label on every chart
10. Mobile layout collapses cleanly at 820px and 600px breaks

## Content preservation rules

These are inviolable:

1. Every sentence in the source ends up somewhere in the output.
2. No rewording, no "improving the copy", no paraphrasing.
3. You may split sentences across slots (e.g., a long sentence becomes the H1 and the deck).
4. You may add structural labels (eyebrows, badges, section titles) that the source did not have. These are design furniture, not new copy.
5. If you must add a CTA label and the source has none, default to: "Book a strategy call" (primary), "Learn more" (secondary). Flag this at the end.
6. Boilerplate UI text (nav links, footer columns, breadcrumb labels) is allowed and is not considered new copy.
