# Pillar 3: Feature and Interaction Design

This pillar is about the moments where a person *does* something: creating an object, paying you, or exploring their data. AI defaults make these moments either sparse and tedious or static and lifeless. Each one is a chance to feel like a real product.

## Contents
- Modals for creation
- Humanize billing
- Rich analytics

---

## Modals for creation

The AI default for "create a new link" is a full route with three fields floating on an empty page. It wastes the screen, loses the context the user was in, and makes a simple action feel heavy.

**Use a focused modal for creation flows.** The person stays where they were, the task is framed, and the surrounding list is still visible behind the overlay.

Make the modal good:
- **Lead with the one required field.** For a link tool, that is the destination URL. Everything else is optional and should look optional.
- **Collapse advanced options by default.** Custom slug, tags, UTM parameters, expiry, password, device targeting: all of it lives behind a "Advanced options" disclosure that is closed on open. This is progressive disclosure. The common path is two clicks, the power path is one more.
- **Show the result inline.** As the user fills the form, preview the short link or the outcome live so the modal feels responsive.
- **Primary action is unmistakable.** One clear "Create" button, a quiet "Cancel," and keyboard support (Enter to submit, Escape to close).
- **Do not trap the user.** Click-outside and Escape both close it. Focus moves into the first field on open and returns to the trigger on close.

A creation modal with a clean primary field and a collapsed advanced section is in `assets/snippets.html`.

When NOT to use a modal: genuinely long, multi-step creation (more than about eight fields or true wizard flows) deserves a dedicated page or a stepper. Modals are for focused, mostly-short creation.

---

## Humanize billing

Billing and pricing are where AI builds give up. The usual output is three identical static cards, no sense of where the user stands, and no reason to pick one plan over another. This screen should do real work: show usage honestly and make the upgrade obvious.

A humane billing screen, in two columns:

**Left column, your current standing:**
- **Usage as donut charts**, not text. Clicks used against the plan cap, links created against the limit, team seats filled. A donut answers "how close am I to the ceiling" at a glance and creates a natural, non-pushy reason to upgrade.
- **Plan summary**: current plan, renewal date, payment method, all calm and factual.

**Right column, the plans:**
- **A clear hierarchy.** Recommend one plan visibly (a subtle highlight or "Most popular" marker), do not present all tiers as equal.
- **Show the saving.** If annual billing is cheaper, state the actual saving ("save 20%" or "2 months free"), do not make people do the math.
- **Differentiate features.** Make the jump between tiers legible: what does Pro unlock that Free does not. A short differential list beats a giant identical feature matrix on every card.
- **One clear action per plan**, with the current plan shown as current, not as a buyable option.

The mindset shift: a pricing page is a product surface, not a brochure. It should reflect the user's real usage and guide a decision.

A two-column billing block with usage donuts and differentiated pricing tiers is in `assets/snippets.html`.

---

## Rich analytics

A dashboard that repeats the same KPI tile six times is not analytical, it is wallpaper. Richness comes from letting people *compare* and *drill in*.

Moves that make analytics feel real:
- **Comparative toggles.** A "split into individual links" switch turns one aggregate line into a per-link breakdown, which is the comparison people actually want. Offer "compare to previous period" the same way.
- **Interactive maps over plain bars.** Geographic data belongs on a choropleth or a dotted world map with hover detail, not a bar chart of country names. It reads faster and feels far more capable.
- **Detail on demand.** Charts respond to hover with a precise tooltip (exact value, exact date). The overview stays clean, the precision is one hover away.
- **Vary the chart to the question.** Trend over time is a line. Composition is a stacked bar or donut. Distribution is a histogram. Relationship is a scatter. Do not answer every question with the same chart.
- **Real ranges and filters.** A working date-range picker and one or two meaningful filters (by link, by source, by country) turn a static report into a tool.

The principle: analytics earns trust when it answers follow-up questions without a new screen. Build for the second and third question, not just the first number.

---

## Quick wins, in order
1. Move creation flows into a modal with advanced options collapsed.
2. Rebuild billing as two columns with usage donuts and a recommended, differentiated plan set.
3. Add a comparative toggle (split or compare) to the main analytics view.
4. Replace a bar-of-countries with an interactive map and add hover tooltips to every chart.
