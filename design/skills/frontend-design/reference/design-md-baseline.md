# DESIGN.md Baseline Reference

This reference anchors the frontend-design skill on the **DESIGN.md** format — a plain-text, AI-readable design system document that agents consume directly. The format originates from Google Stitch and is curated by [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md).

> "Markdown is the format LLMs read best." — Copy a site's DESIGN.md into your project root, tell your AI agent to use it, and every generated component will be on-brand.

---

## 1. The 9-Section Schema

Every DESIGN.md follows this structure. All 9 sections are required for a complete spec.

### Section 1: Visual Theme & Atmosphere

Captures mood, density, and design philosophy. Describes the *feeling* of the interface.

```markdown
## Visual Theme & Atmosphere
- **Overall Mood**: Professional yet approachable; clean information density
- **Design Philosophy**: Content-first, invisible chrome, functional elegance
- **Visual Density**: Medium — generous whitespace with compact data areas
- **Key Aesthetic**: Muted palette with one bold accent; no decoration for decoration's sake
```

### Section 2: Color Palette & Roles

Semantic color names with hex values and functional roles. Not just a list of colors — each must have a *job*.

```markdown
## Color Palette & Roles
| Role | Light Mode | Dark Mode | Usage |
|------|-----------|-----------|-------|
| Primary | #635BFF | #7A73FF | CTAs, links, active states |
| Surface | #F6F9FC | #1A1F36 | Page background |
| Card | #FFFFFF | #2A2F45 | Elevated containers |
| Text Primary | #1A1F36 | #F6F9FC | Body text, headings |
| Text Secondary | #697386 | #A3ACB9 | Captions, metadata |
| Success | #30B566 | #3ECF7A | Positive states |
| Warning | #ED8B00 | #F5A623 | Alerts |
| Error | #DF1B41 | #FF4D6A | Destructive actions, errors |
| Border | #E3E8EE | #3A3F55 | Dividers, card borders |
```

### Section 3: Typography Rules

Font families and a complete hierarchy table with sizes, weights, and line heights.

```markdown
## Typography Rules
- **Display**: [Font Family], [weight], [tracking]
- **Body**: [Font Family], [weight], [tracking]
- **Mono**: [Font Family] for code blocks

| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| H1 | 36px | 700 | 1.2 | Page titles |
| H2 | 28px | 600 | 1.3 | Section headings |
| H3 | 22px | 600 | 1.3 | Subsections |
| Body | 16px | 400 | 1.6 | Paragraphs |
| Small | 14px | 400 | 1.5 | Captions, labels |
| Mono | 14px | 400 | 1.5 | Code, data |
```

### Section 4: Component Stylings

Buttons, cards, inputs, navigation — with ALL states (default, hover, active, disabled, focus).

```markdown
## Component Stylings

### Buttons
- **Primary**: bg-primary, text-white, radius-8, py-10 px-16, shadow-sm
  - Hover: darken 8%, shadow-md
  - Active: darken 12%, shadow-none
  - Disabled: opacity 0.5, cursor not-allowed

### Cards
- bg-card, radius-12, border 1px border-color, shadow-sm
- Hover (if interactive): shadow-md, translateY(-1px)

### Inputs
- bg-surface, border 1px border-color, radius-8, py-10 px-12
- Focus: border-primary, ring 3px primary/20%
- Error: border-error, ring 3px error/20%
```

### Section 5: Layout Principles

Spacing scales, grid systems, whitespace philosophy.

```markdown
## Layout Principles
- **Base Unit**: 4px
- **Spacing Scale**: 4, 8, 12, 16, 24, 32, 48, 64, 96
- **Max Content Width**: 1200px
- **Grid**: 12-column, 24px gutter, fluid within max-width
- **Section Spacing**: 64px between major sections, 32px within
- **Whitespace Philosophy**: Generous — let content breathe
```

### Section 6: Depth & Elevation

Shadow systems and surface hierarchies.

```markdown
## Depth & Elevation
| Level | Shadow | Usage |
|-------|--------|-------|
| 0 | none | Flat surfaces |
| 1 | 0 1px 3px rgba(0,0,0,0.08) | Cards, inputs |
| 2 | 0 4px 12px rgba(0,0,0,0.12) | Dropdowns, popovers |
| 3 | 0 8px 24px rgba(0,0,0,0.16) | Modals, dialogs |
| 4 | 0 16px 48px rgba(0,0,0,0.20) | Toast notifications |
```

### Section 7: Do's and Don'ts

Design guardrails and anti-patterns specific to this design system.

```markdown
## Do's and Don'ts
### Do
- Use the spacing scale consistently — no magic numbers
- Keep CTAs visually distinct from secondary actions
- Use border-radius consistently (one value for cards, one for buttons, one for inputs)

### Don't
- Mix rounded and sharp corners in the same context
- Use more than 2 accent colors simultaneously
- Place text over images without an overlay or text-shadow
- Use pure black (#000) or pure white (#fff)
```

### Section 8: Responsive Behavior

Breakpoints, touch targets, and collapsing strategies.

```markdown
## Responsive Behavior
| Breakpoint | Width | Layout Changes |
|-----------|-------|---------------|
| Mobile | < 640px | Single column, bottom nav, stacked cards |
| Tablet | 640–1024px | Two columns, side nav collapses |
| Desktop | > 1024px | Full layout, side nav visible |

- Touch targets: 44px minimum
- Font scaling: clamp() for display text
- Images: srcset with WebP/AVIF, lazy loading below fold
```

### Section 9: Agent Prompt Guide

Quick color references and ready-to-use prompts for AI agents.

```markdown
## Agent Prompt Guide
When generating components for this design system:
- Always use CSS custom properties: var(--color-primary), var(--spacing-4), etc.
- Default to the Light Mode palette unless dark mode is specified
- Buttons: primary for main CTA, ghost/outline for secondary actions
- Cards: always include border AND shadow-sm for depth
- Use the mono font for any data display, code, or technical content

Quick palette: primary=#635BFF, surface=#F6F9FC, text=#1A1F36, accent=#ED8B00
```

---

## 2. Curated Index — VoltAgent/awesome-design-md

60+ production DESIGN.md files organized by category. Each includes the full 9-section spec plus `preview.html` and `preview-dark.html` visual catalogs.

### AI & LLM Platforms (12)
Claude, Cohere, ElevenLabs, Minimax, Mistral AI, Ollama, OpenCode AI, Replicate, RunwayML, Together AI, VoltAgent, xAI

### Developer Tools & IDEs (7)
Cursor, Expo, Lovable, Raycast, Superhuman, Vercel, Warp

### Backend, Database & DevOps (8)
ClickHouse, Composio, HashiCorp, MongoDB, PostHog, Sanity, Sentry, Supabase

### Productivity & SaaS (7)
Cal.com, Intercom, Linear, Mintlify, Notion, Resend, Zapier

### Design & Creative Tools (6)
Airtable, Clay, Figma, Framer, Miro, Webflow

### Fintech & Crypto (6)
Binance, Coinbase, Kraken, Revolut, Stripe, Wise

### E-commerce & Retail (4)
Airbnb, Meta, Nike, Shopify

### Media & Consumer Tech (10)
Apple, IBM, NVIDIA, Pinterest, PlayStation, SpaceX, Spotify, The Verge, Uber, WIRED

### Automotive (6)
BMW, Bugatti, Ferrari, Lamborghini, Renault, Tesla

---

## 3. Closest-Analog Table

When building for a product type and no custom DESIGN.md exists, fork the closest curated analog:

| Building for… | Fork this DESIGN.md | Why |
|--------------|--------------------|----|
| **B2B SaaS dashboard** | Linear or PostHog | Clean data density, professional tokens |
| **Developer tool / CLI** | Warp or Cursor | Terminal aesthetics, monospace-first |
| **API docs / dev portal** | Stripe or Mintlify | Developer-grade typography, code-friendly |
| **AI/ML product** | Claude or Mistral AI | Conversational UI, clean density |
| **E-commerce** | Shopify or Nike | Product cards, checkout flows |
| **Fintech / payments** | Stripe or Revolut | Trust signals, number typography |
| **Creative / design tool** | Figma or Framer | Canvas UI, toolbar patterns |
| **Productivity app** | Notion or Linear | Content-first, keyboard-friendly |
| **Marketing site** | Vercel or Webflow | Hero sections, conversion-optimized |
| **Consumer mobile app** | Airbnb or Uber | Mobile-first, gesture-driven |
| **Data/analytics platform** | ClickHouse or PostHog | Chart-heavy, dense tables |
| **Media / content site** | The Verge or WIRED | Editorial grid, reading experience |
| **Automotive / luxury brand** | Tesla or Ferrari | Premium feel, cinematic imagery |
| **Enterprise / corporate** | IBM or HashiCorp | Formal, accessible, scalable |
| **Champions Group venture** | Start from Champions brand skill | Orange + white identity, then fill gaps from closest product-type analog |

---

## 4. Authoring Workflow

How to produce a DESIGN.md during Step 0 of the frontend-design skill:

### From Scratch (no brand skill, no analog)

1. Complete Steps 0.2–0.6 of the main skill (product type → style → palette → fonts → spacing).
2. Populate each of the 9 sections using your generated tokens.
3. Write the Agent Prompt Guide last — it's a summary of what you just defined.
4. Save as `DESIGN.md` alongside your output files.

### By Forking a Curated Analog

1. Identify the closest analog from the table above.
2. Fetch the DESIGN.md from `https://github.com/VoltAgent/awesome-design-md/tree/main/designs/{brand-name}/`.
3. Replace palette, fonts, and brand-specific tokens while preserving structural patterns.
4. Update the Agent Prompt Guide to reference new token values.

### From a Brand Skill

1. Load the brand skill (Champions Group, Ampliz, Lake B2B, etc.).
2. Extract its color tokens, font rules, and component styles.
3. Build a DESIGN.md skeleton, populating sections 2–4 from brand tokens.
4. Fill remaining sections (Atmosphere, Layout, Depth, Responsive, Do's/Don'ts, Agent Guide) using the product-type's closest analog as a scaffold.
5. Brand skill tokens always win on conflict.

### Using the Generator

For brands not in the curated index, [getdesign.md](https://getdesign.md) can generate a DESIGN.md from any live website URL.

---

## 5. Champions Brand-Skill Integration Rules

The precedence chain ensures brand consistency across all Champions Group ventures:

```
Champions brand skill → venture-specific DESIGN.md → curated VoltAgent DESIGN.md → generator-built DESIGN.md
```

### Rules

1. **Champions brand skill is loaded?** Its orange (#FF6B00) + white identity, typography, and component styles are the *floor*. No DESIGN.md can override them.

2. **Venture-specific brand skill exists?** (e.g., Ampliz, Lake B2B) — that skill's tokens override the parent Champions tokens for that venture's output. A venture DESIGN.md extends, not replaces, the venture brand skill.

3. **No brand skill loaded?** Use the curated VoltAgent DESIGN.md closest to the product type. If none fits, generate one.

4. **Sections the brand skill doesn't cover** (typically: Depth & Elevation, Responsive Behavior, Agent Prompt Guide) — fill from the closest curated analog or generate fresh.

5. **Conflict resolution**: When a brand skill specifies `primary: #FF6B00` but a forked DESIGN.md has `primary: #635BFF`, the brand skill wins. The DESIGN.md's value is discarded for that token.

### Integration Checklist

- [ ] Brand skill loaded and tokens extracted?
- [ ] DESIGN.md sections 2–4 reflect brand tokens, not analog defaults?
- [ ] Agent Prompt Guide references correct brand colors?
- [ ] Do's and Don'ts include brand-specific guardrails (e.g., "Don't use gradients on the Champions orange")?
- [ ] Final output spot-checked against brand skill for 3+ components?
