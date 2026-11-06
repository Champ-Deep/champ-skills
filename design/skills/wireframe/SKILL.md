---
name: wireframe
description: "Use when exploring page structure before visual design. Grayscale low-fi layout options."
---

# Wireframe

Rough, grayscale, structure-only layouts, built before any brand or polish work. Local
equivalent of Claude Design's Prototype > Wireframe toggle.

## Process

1. Restate the page goal and the one action the visitor should take, in one sentence.
2. List sections in scroll order, each with its job (not its copy).
3. Produce 3 layout options as separate single-file HTML files. Each differs in
   structure (hero split, stacked, sidebar), not in styling.
4. Output rules: grayscale only (#fff, #eee, #999, #222), system font, 1px borders, labelled
   boxes for images ("IMG 16:9"), real section names, placeholder text such as
   "Headline", "Body copy 2 lines". No brand colours, icons, shadows, gradients, motion.
5. Make it responsive: one breakpoint at 768px so mobile order is visible.
6. Show all three side by side (or a numbered list with file paths), name a recommendation
   and the one trade-off per option. Stop. Do not start styling.

## Handoff

Once Deep picks a layout, pass that file to `frontend-design` (build), then `impeccable`
`polish` (refine). Check trends via `awwwards-inspiration` or `popular-web-designs` only
after the structure is chosen.

## Do not

- Do not write final copy or choose brand fonts and colours here.
- Do not ship a wireframe as the deliverable.
