---
name: ui-polish
description: "Second-pass UI refinement that turns vibe-coded, AI-default interfaces into professional, data-dense, production-grade products. Runs automatically as Phase 2 after the frontend-design skill, reading the same DESIGN.md so tokens stay consistent, and also runs on demand. Use this whenever a UI needs polishing, whenever someone says a design \"looks AI-made\", \"looks generic\", \"vibe-coded\", \"has too many emojis\", \"make it look professional\", \"tighten this up\", or \"refine the dashboard\", or when they want better icons, a cohesive color palette, functional micro-charts, consolidated navigation, an account card, creation modals, humane billing and pricing, richer analytics, or a trust-building landing page. MANDATORY TRIGGER after building any dashboard, SaaS app, admin panel, link or analytics tracker, settings or billing screen, or data-dense interface, even when the user does not say the word \"polish\". Also triggers on link-management and tracking dashboards such as Champ Beam."
---

# UI Polish

The job of this skill is to take an interface that *works* and make it look like a team of professionals shipped it, not an AI on its first pass. It is the refinement layer that runs after `frontend-design` has produced the structure and the first cut of styling.

Most AI-built UIs fail in the same predictable ways: emoji standing in for icons, the default bright palette, decorative graphics where data should be, a sidebar stuffed with everything, and pricing pages that are three dead cards in a row. Each of those is a recognizable "tell." This skill is a checklist and a kit for hunting those tells and replacing them with the choices a senior product designer would make.

The north star: **professional, data-dense, and user-centric.** Move away from defaults. Make every pixel earn its place.

---

## When this runs

**Phase 2 of the design pipeline (automatic).** After `frontend-design` builds a UI, run this as the polish pass. The two skills are a pipeline: `frontend-design` decides structure and the design system, `ui-polish` refines the surface. There is no need to wait for the user to ask.

**Standalone (on demand).** Any time someone hands over an existing interface and wants it to look less generic, more professional, or more data-rich. Phrases like "this looks AI-made", "make it less vibe-coded", "tighten up the dashboard", "swap the emojis", "the pricing page is boring."

---

## The handoff: read the DESIGN.md first

`frontend-design` anchors every build on a **DESIGN.md** (the 9-section AI-readable spec). This skill consumes that same file so the polish never fights the system.

1. **Locate the DESIGN.md** produced alongside the build. Pull the color roles, type scale, spacing tokens, elevation system, and the chosen icon family.
2. **If no DESIGN.md exists** (standalone polish on someone else's UI), infer a lightweight one from the code: extract the dominant colors, fonts, and spacing, and note them so your changes stay coherent. Do not redesign the system. Refine within it.
3. **Brand precedence still applies.** If a Champions Group or venture brand skill is loaded, its tokens win over the DESIGN.md, which wins over anything you infer. Never override brand color or type to chase a trend.

The point of reading the spec first is that polish is about *consistency and intent*, not personal taste. You are enforcing the system harder, not inventing a new one.

---

## The Polish Pass (run in this order)

Work cheapest-to-most-impactful so the UI improves visibly at every step.

0. **Machine audit first.** Before you look at anything, run the deterministic pass. It writes half your punch list for you, in about four seconds, and it finds the class of defect that eyes reliably miss.

   ```bash
   python3 visual-verify/scripts/audit.py <file-or-url> --width 390
   python3 visual-verify/scripts/audit.py <file-or-url> --width 1440
   ```

   Every FAIL is a polish item with a known fix. Every WARN tagged `side-stripe`, `emoji-as-icon`, `gradient-text`, `static-glass`, `default-font`, `three-card-row`, or `placeholder-content` maps directly onto a row of the cheat sheet below. Start the manual pass with those already resolved so your attention goes to the things only judgement can catch.

1. **Audit.** Walk the interface against `assets/polish-audit.md` and mark every AI tell you find. Be specific: "stat cards use emoji", "sidebar has 11 items", "create-link is a full sparse page".
2. **Pillar 1: Aesthetic refinements.** Icons, color, data density. Highest perceived-quality gain for the least effort. See `reference/aesthetic-refinements.md`.
3. **Pillar 2: Layout and hierarchy.** Consolidate navigation, build the account card, optimize cards. See `reference/layout-and-hierarchy.md`.
4. **Pillar 3: Features and interaction.** Creation modals, humane billing, rich analytics. See `reference/interaction-and-features.md`.
5. **Pillar 4: Landing page.** Trust through presentation, real product screenshots over generic icons. See `reference/landing-page-strategy.md`.
6. **Swap in the kit.** Use `assets/icon-map.md` and `assets/snippets.html` instead of writing these from scratch each time.
7. **Verify.** Re-run the audit, check contrast on every surface, and apply the final test below.

---

## The four pillars at a glance

### Pillar 1: Visual and aesthetic refinements
- **Replace emojis with a real icon library.** Pick one family (Lucide or Phosphor) and use it everywhere at a consistent size and stroke weight. Emojis render differently on every OS and read as amateur. Icons are semantic, not decorative.
- **Use purposeful color theory.** Abandon the AI-default palette: cyan-on-dark, purple-to-blue gradients, neon accents. Choose one considered, cohesive direction instead (for example a deep forest green rather than a harsh dark blue). Apply 60-30-10 and tint your neutrals toward the brand hue.
- **Increase data density.** Where a card holds a decorative icon, put a functional micro-chart instead: a sparkline, a trend delta, a mini bar. The graphic should carry information, not fill space.

→ `reference/aesthetic-refinements.md`

### Pillar 2: Layout and information hierarchy
- **Consolidate navigation.** The sidebar is for the 5 to 7 destinations people use constantly. Hide the rest (custom domains, teams, integrations) behind a primary tab or a disclosure. A crowded sidebar is a tell.
- **Build an account card.** Replace the generic gradient avatar circle with a real account popover that tucks settings, billing, team switching, and secondary links into one clean menu.
- **Optimize the cards.** Collapse rows of buttons into a single kebab (triple-dot) menu, center dates, and swap text-heavy chips for icons with tooltips. Reduce noise so the content leads.

→ `reference/layout-and-hierarchy.md`

### Pillar 3: Feature and interaction design
- **Use modals for creation.** A complex form like "new link" belongs in a focused modal, not a sparse full page. Keep advanced options collapsed by default so the common path stays clean (progressive disclosure).
- **Humanize billing.** Two-column layout, donut charts for usage, and a pricing hierarchy that actually sells: highlight the recommended plan, show the annual saving, and make feature differences legible. Static pricing cards are a wasted screen.
- **Make analytics rich.** Stop repeating identical KPI tiles. Add comparative tools (a "split into individual links" toggle), an interactive map instead of a plain bar chart, and detail-on-demand on hover.

→ `reference/interaction-and-features.md`

### Pillar 4: Landing page strategy
- **Presentation over complexity.** A landing page sells trust. Show the value immediately with high-quality, stylized screenshots of the real analytics dashboard rather than a row of generic feature icons. People believe a product they can see working.

→ `reference/landing-page-strategy.md`

---

## The AI-tells cheat sheet

If you see the thing on the left, do the thing on the right. This is the fastest path through a polish pass.

| AI tell | Professional fix |
|---------|------------------|
| Emoji used as UI icons | One icon family (Lucide or Phosphor), consistent size and weight |
| Cyan-on-dark, purple-to-blue gradient, neon accent | One cohesive considered palette, 60-30-10, tinted neutrals |
| Decorative icon inside a stat card | Functional micro-chart: sparkline, trend delta, mini bar |
| Everything crammed into the sidebar | Consolidate to 5 to 7 items, hide the rest behind a tab or disclosure |
| Gradient avatar circle for account | Account card popover with settings, billing, team, links |
| Rows of text buttons and text chips | Kebab menu, icons with tooltips, centered dates |
| Full-page sparse "create" form | Creation modal with advanced options collapsed |
| Three static pricing cards in a row | Two-column billing, donut usage charts, plan differentials |
| Identical repeated KPI tiles | Comparative toggles, interactive maps, detail-on-demand |
| Generic icon hero on the landing page | Real, stylized product screenshots |
| Pure black (#000) or pure white (#fff) surfaces | Near-black and off-white, neutrals tinted toward brand hue |
| Colored `border-left`/`border-right` side-tab stripe on cards, list items, or alerts | Per Impeccable (github.com/pbakaus/impeccable), this is the single most recognizable AI-dashboard tell. Signal status with fill, weight, or a leading icon instead |
| Rounded-square icon tile sitting above every section heading | Vary the treatment per section, or drop the tile and let the heading carry the weight |
| Soft colored glow (dark box-shadow bloom) behind cards or text | Remove it, or reserve it for one load-bearing hero moment, never repeated per-section decoration |
| Hedging UI copy ("maybe consider", "could be helpful", "this might help") | Decisive, expert-voice copy that states the recommendation plainly |
| Every section built to the same shape: heading, subhead, then a grid | Vary the section architecture. One full-bleed, one two-column, one narrow and centred, one dense. Sameness across sections is the strongest structural tell. |
| An eyebrow label above every single heading ("PLATFORM", "WHY US") | At most one per three sections, and only where it genuinely disambiguates |
| Section numbers as decoration ("001 · Capabilities") | Cut them. They imply a sequence that does not exist. |
| Fake ambient detail: a locale strip, a live clock, a scroll cue, an unset version badge | Remove. These are texture pretending to be information. |
| Invented names and companies: Jane Doe, Acme, Nexus, SmartFlow | Real names with permission, or clearly-labelled illustrative placeholders. Never a fake testimonial. |
| Unbacked precision: 99.99% uptime, 10x faster, +240% growth | Source it or cut it. An unbacked number costs more trust than no number. |
| Two CTAs meaning the same thing on one screen ("Get started" and "Try it free") | One primary intent per screen. A second CTA must offer a genuinely different path. |
| Button label wrapping to two lines at desktop width | Shorten the label. A wrapped button is a hard fail, not a cosmetic one. |
| A single flat `0 4px 6px rgba(0,0,0,.1)` on everything | Two layers: one tight and near-opaque for contact, one wide and faint for ambient light. Add a semi-transparent border for a crisp edge. |
| Nested boxes sharing the same corner radius | Concentric radii: child radius equals parent radius minus the padding, never more than the parent |
| Pure grey borders and shadows against a coloured brand | Tint borders, shadows, and muted text toward the background hue |
| Figures in a column that jitter between rows | `font-variant-numeric: tabular-nums` wherever numbers are compared |
| A headline breaking with one word on the last line | `text-wrap: balance` on headings, `pretty` on body copy |
| Dark mode that is light mode inverted | Raised surfaces get *lighter* in dark mode, not more shadowed. Desaturate accents; a colour that sings on white shouts on near-black. |

---

## Asset kit (use these, do not reinvent)

- `assets/icon-map.md` : a lookup table from the emojis AI reaches for to the exact Lucide and Phosphor icon names, plus import snippets and the one-family rule.
- `assets/snippets.html` : a single self-contained file of paste-ready components in a cohesive dark-green theme with Lucide icons and inline-SVG micro-charts. Open it in a browser to see the target quality, then lift the pieces you need.
- `assets/polish-audit.md` : the run-after checklist, organized by pillar, that doubles as the audit in step 1 and the verification in step 7.

---

## Final test before you hand back

Polish is the phase most likely to be declared complete without evidence, because the changes feel visible while you are making them. Close it with the render gate.

1. **Re-run the machine audit.** Zero FAILs at 390 and 1440. Every remaining WARN has a one-line reason.
2. **Screenshot and look.** `python3 visual-verify/scripts/shoot.py <target> --widths 390,1440 --themes light,dark`, then open every PNG with the Read tool. Compare against the before shots. If you cannot see the improvement in the two images side by side, you polished something that did not matter.
3. **The AI-slop test.** If you showed this screen and said "an AI made this," would they believe you instantly? If yes, you are not done.
4. **The swap test.** Put a competitor's logo on the screenshot. Would anything else need to change? If not, the polish made it competent and anonymous. Find the one element that could only belong to this product and give it more weight.
5. **The accessory test.** List every decorative element still present: gradient, glow, glass, badge, divider, icon tile, background pattern. Remove the least load-bearing one and look again. Repeat until removing something makes it worse. That point is the design.
6. **Contrast.** Every text color passes 4.5:1 on its **composited** background, which is what the audit measures and what your intended hex does not tell you. On dark or colored surfaces, text is explicitly light and not inheriting a darker parent color.
7. **One icon family, no emojis** anywhere in the chrome.
8. **Every stat earns its graphic.** No decorative icons where a micro-chart could inform.
9. **The checklist is clean.** Re-run `assets/polish-audit.md`. Nothing left unchecked without a reason.

Hand back with an honest statement of what was verified and at what widths. If no browser was available, list the unverified items rather than implying they passed.

→ Full protocol: the `visual-verify` skill.

Keep the writing in any UI copy plain and human. Avoid em-dashes in generated copy. When in doubt, remove a word, a chip, or a card: the most professional version of almost every AI-built screen is a calmer one.

