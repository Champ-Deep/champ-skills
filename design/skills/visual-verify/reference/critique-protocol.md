# Critique Protocol

How to look at a screenshot of your own work and find what is wrong with it.

The failure mode this exists to prevent: opening a screenshot, feeling that it looks fine, and moving on. Your own output always looks fine to you, because you chose every part of it on purpose. Critique is a procedure, not a reaction. Run the procedure.

---

## Before you start

Have three things open: the screenshot, the DESIGN.md (or whatever spec the build was meant to follow), and an empty numbered list. You are going to fill the list with defects. Aim for at least five on a first pass. If you find zero, you did not run the procedure, you glanced.

Write defects in this shape:

> **3.** Hero. The eyebrow ("PLATFORM") is 14px uppercase with 0.1em tracking in the accent colour, and the h1 below it is 44px in near-black. They have similar visual weight, so the eye lands on the eyebrow first and has to correct. Drop the eyebrow to the neutral 500 tone, or cut it.

Element, observation, consequence, fix. An adjective on its own ("cramped", "bland", "off") is not a defect, it is a feeling. Convert it or discard it.

---

## Pass 1: Structure

Look at the full-page shot at 1440.

- **Squint.** What dominates? There should be one clear winner per screen. If the answer is "the three cards" on a page whose job is to explain one idea, the layout is fighting the content.
- **Trace the reading path.** Follow where your eye actually goes, first, second, third. Does that order match the order of importance? On a landing page the intended path is headline → subhead → primary CTA. On a dashboard it is the number that changed → the trend → the controls.
- **Count the sections and their rhythm.** Are they all the same height, same padding, same left-aligned-heading-then-grid shape? Sameness across sections is the most common structural tell of generated work. Real pages vary: one full-bleed, one two-column, one narrow and centred, one dense.
- **Check the alignment spine.** Pick a vertical edge and follow it down the page. Things should either share it exactly or differ obviously. Near-misses of 4 to 12px are the visual equivalent of a typo.
- **Whitespace distribution.** Space should be uneven on purpose: tight inside a group, generous between groups. If every gap is the same 24px, nothing is grouped and the page reads as a list of unrelated blocks.

## Pass 2: Type

- **Levels.** Count the distinct type styles. Three to five is a system. Nine is an accident. Two is usually under-designed.
- **Is the step between levels decisive?** If the h2 and the h3 are 24px and 21px, they read as the same level with a rendering bug. Contrast in size, weight, or colour, ideally two of the three.
- **Measure.** Body text past roughly 75 characters per line is tiring; past 90 it is a wall. Look at the actual rendered line, not the CSS.
- **Widows and orphans.** A headline breaking with one word on the last line is the fastest way to look unfinished. `text-wrap: balance` on headings, `pretty` on body.
- **Numbers.** Any column or comparison of figures needs `tabular-nums`, or the digits jitter between rows.
- **Does the font mean anything?** If the typeface could be swapped for the system stack without changing how the product feels, it is not doing work.

## Pass 3: Colour and surface

- **How many hues are actually on screen?** Count them. More than three families and the palette is not a palette.
- **Where does the accent appear?** It should mark what matters, roughly one tenth of the surface. If the accent is on the heading, the badge, the icon, the border and the button, none of them are emphasised.
- **Are the neutrals tinted?** Pure grey against a coloured brand reads as a placeholder. Neutrals should carry a trace of the brand hue.
- **Depth.** Does elevation mean anything, or is there a drop shadow on everything? Shadows should map to a real z-order: floating things have them, things sitting on the page do not.
- **Dark mode is a separate design.** Compare the light and dark shots. If the dark one is the light one with the colours flipped, the elevation is now backwards (in dark mode, higher surfaces get lighter, not more shadowed) and the accent is probably too saturated to read.

## Pass 4: Responsive

Put the 390 and 1440 shots next to each other.

- **Did the type scale, or just the container?** A 56px headline at 390px is a headline that ate the fold.
- **What happened to the grid?** Three cards becoming three full-width stretched cards is a collapse, not a responsive design. Cards that were peers at desktop often want to become a list at mobile.
- **Is the fold doing its job at 390?** The most important sentence and the primary action should be visible without scrolling. Check that the nav, an announcement bar, and a cookie banner have not eaten it between them.
- **Touch reachability.** Primary actions in the bottom two-thirds of a phone screen. A CTA pinned to the top right is a desktop habit.
- **Overflow.** The audit catches horizontal scroll numerically, but look anyway for the softer version: a table that clips, a long word that breaks the container, a fixed-width image.

## Pass 5: Content

This is where most "polished" work still fails.

- **Read the copy as a stranger.** Does the headline say what the thing does, or does it say something that could be true of any company in the category? "Built for modern teams" is not a headline, it is a placeholder that survived.
- **Look for hedging.** "Helps you to potentially improve" is the voice of something with no opinion. State the claim.
- **Placeholder residue.** Lorem, Jane Doe, Acme, a version badge nobody set, a stat that is 99.99% because it sounded plausible.
- **Are the numbers real?** Unbacked precision is worse than no number. If you cannot source it, cut it.
- **Empty, loading, error.** Look for evidence they were designed. If the only state on screen is the happy path with three perfect rows of data, two thirds of the interface does not exist yet.
- **Icons.** One family, one weight, one size, and every one of them semantically related to its label. A rocket next to "Performance" is decoration.

## Pass 6: The two tests

**The swap test.** Imagine this screenshot with a competitor's logo. Would anything else need to change? If not, the design carries no brand meaning. It is competent and anonymous. Fix by finding the one element that could only belong to this product and making it louder.

**The accessory test.** List every decorative element: gradients, glows, glass, blurs, badges, dividers, icon tiles, animated borders, background patterns. Remove the least load-bearing one. Look again. Almost always better. Repeat until removing something makes it worse. That point is the design.

---

## Turning the critique into fixes

Order the numbered list by leverage, not by how easy each is:

1. Structure and hierarchy defects. These change everything downstream, so fixing colour first wastes the work.
2. Content defects. A hollow headline undermines a perfect layout.
3. Responsive breaks.
4. Type and colour refinement.
5. Motion and micro-detail.

Fix in that order, then shoot again. Compare the before and after screenshots directly. If you cannot see the improvement in the two images side by side, you fixed something that did not matter.

---

## When there is no browser

If Playwright is genuinely unavailable, the loop degrades but does not disappear:

- Read the built HTML and trace the DOM order. Reading order is hierarchy: if the markup order does not match the intended reading path, the design is wrong regardless of CSS.
- Grep the stylesheet for the mechanical failures the audit would have caught: `outline: none`, `transition: all`, `transition:` on width or height or top or left, absence of any `prefers-reduced-motion` block, `user-scalable=no`, hardcoded `#fff` and `#000`, `background-clip: text`, `border-left:` with a saturated colour, font stacks starting with Inter or Roboto.
- Compute contrast by hand for the three most-used text and background pairs in the token set. Three pairs takes a minute and catches most of it.
- Then say, in the handoff, exactly what was not verified. Label it unverified. Do not round up to done.
