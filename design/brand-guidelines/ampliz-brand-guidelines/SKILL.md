---
name: ampliz-brand-guidelines
description: Brand guidelines for Ampliz, a B2B and Healthcare Data Intelligence company. Use when creating any Ampliz-branded content including presentations, documents, social media posts, marketing materials, emails, sales assets, or any design work requiring Ampliz branding. Also use when users ask about Ampliz brand colors, fonts, logo usage, visual identity standards, or healthcare-specific design guidelines. Also trigger for anything involving Charles, Advik, or the Ampliz/Assassins team.
---

# Ampliz Brand Guidelines

Brand guidelines for Ampliz, enabling creation of on-brand content and materials.

## Brand Overview

**Company:** Ampliz (child company of Champions Group)
**Tagline:** Data To Power Your Business
**Industry:** B2B Data Intelligence & Healthcare Data Solutions
**Certifications:** ISO 27001
**HQ:** Emeryville, California, USA

Ampliz is the APAC B2B and Healthcare Data Intelligence platform powered by Contextual Intelligence — transforming data points into qualified pipeline. Healthcare is a dominant vertical.

## Product Suite

| Product | Short Name | Description |
|---------|-----------|-------------|
| Ampliz Enterprise | Enterprise | B2B company & contact intelligence (120M+ contacts, 7M+ companies) |
| Ampliz Healthcare Intelligence | Healthcare Intelligence | HCP data platform (4M+ physicians, 9K+ hospitals, 200K+ clinics) |
| Ampliz SalesBuddy | SalesBuddy | Chrome extension for real-time prospect intelligence |

**Naming:** Always capitalize "Ampliz". SalesBuddy is one word, camelCase. Product names: "Ampliz [Product]" — never hyphenated.

## Quick Reference

### Primary Colors (80% of designs)

| Color | Name | Hex | RGB | Usage |
|-------|------|-----|-----|-------|
| 🔵 | Ampliz Blue | #0071EB | 0, 113, 235 | THE brand color — CTAs, headers, links, primary buttons |
| ⚫ | Ampliz Black | #000000 | 0, 0, 0 | Body text, headlines, logo on light backgrounds |
| ⚪ | Ampliz White | #FFFFFF | 255, 255, 255 | Backgrounds, reversed text, whitespace |

### Accent Color

| Color | Name | Hex | RGB | Usage |
|-------|------|-----|-----|-------|
| 🔴 | Ampliz Coral | #FE7678 | 254, 118, 120 | Accent only — max 15% of composition. Highlights, hover states, badges. |

### Extended Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Light Blue | #E6F0FD | Background tints, cards |
| Mid Blue | #0058B8 | Hover states, darker blue needs |
| Dark Blue | #003D80 | Deep backgrounds, footer |
| Light Coral | #FFC5C6 | Soft accent backgrounds, tags |
| Gray 100 | #F5F5F5 | Page backgrounds |
| Gray 300 | #D1D5DB | Borders, dividers |
| Gray 600 | #6B7280 | Secondary text, captions |
| Gray 900 | #1F2937 | Alternative to pure black |

### Gradients

| Name | Values | Usage |
|------|--------|-------|
| Blue Gradient | #0071EB → #003D80 | Hero sections, CTA backgrounds |
| Healthcare Gradient | #0071EB → #00A3E0 | Healthcare-specific materials |
| Coral Fade | #FE7678 → #FFC5C6 | Accent highlights, data viz |

### Typography

- **Primary:** Roboto (Light 300, Regular 400, Medium 500, Bold 700, Black 900)
- **Fallback:** -apple-system, BlinkMacSystemFont, Segoe UI, Arial, sans-serif
- Headlines: Roboto Bold/Black. Body: Roboto Regular. Buttons/Nav: Roboto Medium.

## Logo Rules

- Minimum digital: 150px width
- Minimum print: 25mm width
- Clear space: Height of lowercase "l" on all sides
- The "A" features a distinctive upward-angled crossbar (growth/amplification)
- Approved backgrounds: White, light gray, dark blue, black

**Never:** Stretch, rotate, recolor outside palette, add shadows/glows, place on busy backgrounds, combine with Champions Group branding in client-facing materials.

## Brand Voice

| Attribute | Description |
|-----------|-------------|
| **Authoritative** | We know data. Cite stats, use industry terms correctly. |
| **Precise** | Data accuracy IS our product. Use specific numbers (99% accuracy, 4M+ physicians). |
| **Accessible** | Complex data, simple language. Make intelligence approachable. |
| **Empowering** | Customer is the hero. Focus on their outcomes, use "you" language. |
| **Trustworthy** | ISO 27001, HIPAA-aware, GDPR-compliant. Transparency earns trust. |

**Frame Ampliz as:** "Intelligence platform" — never "data vendor" or "email list provider."

## Healthcare-Specific Rules

- Always reference data compliance and privacy
- Use proper medical terminology (HCP not "doctor")
- Never make clinical claims or show patient data
- Use Healthcare Gradient (#0071EB → #00A3E0) for healthcare materials
- Include "Healthcare Intelligence" sub-brand label on healthcare content

## Image Guidelines

- Clean, professional, diverse representation
- Healthcare settings: modern and digital, not clinical
- Blue duotone overlays for hero images
- Flat/semi-flat illustrations with Ampliz Blue dominant
- Rounded corners (8-12px) for card images and screenshots

## Key Stats (for content)

| Metric | Value |
|--------|-------|
| B2B Contacts | 120M+ |
| Companies | 7M+ |
| Physicians | 4M+ |
| Hospitals | 9,000+ |
| Clinics | 200K+ |
| Data Accuracy | 99% |
| Certification | ISO 27001 |

## Frontend Development Standards

When building Ampliz-branded React frontends, follow these standards to ensure code quality matches brand quality.

### Stack
React 19 + TypeScript (strict) + Tailwind CSS + React Query (TanStack Query)

### Ampliz Tailwind Config Essentials
- **Brand colors as CSS variables / Tailwind theme extensions:** `ampliz-blue: #0071EB`, `ampliz-coral: #FE7678`, `ampliz-dark-blue: #003D80`, `ampliz-light-blue: #E6F0FD`
- **Font:** Roboto (300–900) via Google Fonts. Fallback: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif`
- **Border radius:** Buttons 6px, Cards 12px, Images 8–12px
- **Use `cn()` from `clsx` + `tailwind-merge`** for conditional class merging — never concatenate className strings with template literals
- **Use `cva` (class-variance-authority)** for component variants (e.g., Button primary/secondary/accent/dark matching brand button specs)
- **Never mix inline styles with Tailwind** — use arbitrary value syntax `bg-[#0071EB]` instead

### Component Architecture
- **One responsibility per component** — split when they grow beyond a screenful
- **Feature-based folder structure** (not type-based): `features/dashboard/`, `features/contacts/`, `features/healthcare/`
- **Always type props** with TypeScript. Never use `any`.
- **Custom hooks** for reusable logic (`useContacts`, `useHealthcareSearch`). Prefix with `use`.
- **React Query** for all server state — never `useEffect` + `useState` for data fetching
- **Naming:** PascalCase components, camelCase functions/variables, `is/has/can` booleans, SCREAMING_SNAKE_CASE constants

### Ampliz Component Patterns
- **Buttons:** Use `cva` variants matching brand specs (Primary `#0071EB`, Secondary outline, Accent `#FE7678` sparingly, Dark `#000000`)
- **Cards:** White background, `1px solid #E5E7EB` border, 12px radius, `0 1px 3px rgba(0,0,0,0.1)` shadow, blue-tinted hover shadow
- **Data tables:** Header `#F9FAFB`, alternating rows `#FFFFFF` / `#F5F5F5`, highlight row `#E6F0FD`
- **Compound components** over prop drilling for complex UI (Card + Card.Image + Card.Body + Card.Title + Card.Footer)
- **Early returns** over nested ternaries for loading/error/empty states

### React 19 Features (Use These)
- `useActionState` for form submissions (replaces manual loading/error state juggling)
- `useOptimistic` for instant UI feedback (e.g., like counts, toggle states)
- `use()` for conditional context reading and promise unwrapping
- `ref` as a regular prop — no more `forwardRef`

### Testing Standards
For comprehensive testing patterns, see the **frontend-resiliency-tester** skill which covers component, hook, integration, and E2E tests aligned with these standards.

## Detailed References

- **Full brand book:** See [Ampliz-Brand-Guidelines.md](Ampliz-Brand-Guidelines.md)
- **Design system (buttons, cards, tables, spacing):** See Section 5 of the full brand book
- **Content templates:** See Section 6 of the full brand book
- **Competitive differentiation:** See Section 8 of the full brand book
- **Brand assets:** See [assets/](assets/) (to be sourced)
