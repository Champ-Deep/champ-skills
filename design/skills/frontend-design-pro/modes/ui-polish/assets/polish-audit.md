# Polish Audit Checklist

Run this twice: once in step 1 to find the AI tells, and once in step 7 to verify they are gone. Mark each item. Anything left unchecked needs a reason.

## Step 0: pull the system

- [ ] Located the `DESIGN.md` from `frontend-design` (or inferred a lightweight one from the code).
- [ ] Noted the color roles, type scale, spacing tokens, elevation, and icon family.
- [ ] Confirmed brand precedence: any loaded Champions or venture brand skill tokens win over DESIGN.md.

---

## Pillar 1: Aesthetic refinements

- [ ] No emojis anywhere in the chrome. One icon family (Lucide or Phosphor) only.
- [ ] Icons share one size and one stroke weight per context.
- [ ] Palette is one cohesive considered direction, not the AI default (no cyan-on-dark, no purple-to-blue gradient, no neon accent).
- [ ] 60-30-10 holds: one dominant neutral, one secondary, one accent.
- [ ] Neutrals tinted toward the brand hue. No pure black (#000) or pure white (#fff) surfaces.
- [ ] Decorative stat-card icons replaced with functional micro-charts (sparkline, delta, mini bar).
- [ ] At most one accent color (plus positive and warning colors for deltas).

## Pillar 2: Layout and hierarchy

- [ ] Sidebar is 5 to 7 primary destinations. Settings-type routes moved out.
- [ ] Generic gradient avatar circle replaced with an account-card popover.
- [ ] Account card holds settings, billing, team or workspace switch, and secondary links.
- [ ] Per-row buttons collapsed into a kebab menu (at most one inline quick-action).
- [ ] Text chips replaced with icons plus tooltips. Dates quieted and aligned consistently.
- [ ] Each card has one clear focal point. Column rhythm is consistent across rows.

## Pillar 3: Features and interaction

- [ ] Creation flows use a focused modal, not a sparse full page.
- [ ] Advanced options in the modal are collapsed by default (progressive disclosure).
- [ ] Modal supports Enter to submit, Escape and click-outside to close, with correct focus handling.
- [ ] Billing is two columns: usage as donut charts on one side, plans on the other.
- [ ] Pricing has a clear hierarchy: a recommended plan, the annual saving stated, feature differentials legible.
- [ ] Analytics offers a comparative tool (split or compare) and detail-on-demand on hover.
- [ ] Geographic data uses an interactive map, not a bar chart of country names.

## Pillar 4: Landing page

- [ ] Hero leads with a stylized screenshot of the real product, not generic feature icons.
- [ ] Screenshots are framed, cropped to the value moment, and use realistic data.
- [ ] Headline is a specific value proposition with one primary call to action.
- [ ] One row of social proof near the hero (logos or a real metric).

---

## Final verification

- [ ] **AI-slop test.** If shown this screen and told "an AI made this," would they believe it instantly? If yes, keep going.
- [ ] **Contrast.** Every text color passes 4.5:1 on its real background. On dark or colored surfaces, text is explicitly light and not inheriting a darker parent.
- [ ] **States.** Empty, loading, and error states all designed, not just the happy path.
- [ ] **Calm.** Asked "what does this tell me?" of every graphic and removed or upgraded the ones that answered "nothing."
- [ ] **Copy.** Plain, human microcopy. No em-dashes. Fewer words where possible.
