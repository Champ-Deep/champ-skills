---
name: interactive-data-app-verification
description: Verify interactive HTML data apps by measuring the DOM.
---

# Interactive data app verification

A screenshot tells you something is wrong. Only the DOM tells you what. For an interactive
artefact a static screenshot is close to worthless: the animation may not have settled, the
tab you are looking at may not be the one the user opens first, and no number in the payload
tells you whether a single element rendered.

Use when building or shipping any single-file HTML tool with SVG layout, canvas, a data
payload inlined as JSON, filters, toggles or localStorage state. Triggers on "build me an
interactive graph", "make this dashboard clickable", "verify the graph", "the visualization
looks wrong", "add filters to this chart", or any deliverable that must be both correct and
beautiful.

Companion skills `link-graph-visualization` and `internal-link-audit` produce the findings
and the picture. This one proves the artefact actually works.

## Build order

```
generate payload -> render -> drive it in Playwright -> measure geometry
   -> assert interactions change state -> screenshot every view and breakpoint
   -> LOOK at the images -> fix -> repeat until the assertions pass
```

Write the checker **before** polishing the visuals. Every defect below was invisible to a
screenshot and obvious to a measurement.

## What the checker must assert

**Rendered counts, not payload counts.** A treemap whose payload holds 154 sections may
correctly render 12 tiles after grouping. Derive the expected number rather than hardcoding
a figure that changes with the design.

**Geometry at three levels.** Overlaps between nodes; overlaps and out-of-bounds for elements
*inside* nodes (a percentage badge sitting on a section name passes a node-only check); and
the bounds of the whole group.

**That every control changes state.** A filter that silently returns everything looks
identical to a working one until you count rows before and after. Toggle each one, assert
the count moved, toggle it back.

**That text direction is right.** CSS `direction:rtl` with `text-overflow:ellipsis`
truncates the *front* of a slug, which is the identifying part. Assert the first characters
are visible.

**That saved state persists and resets.** If the artefact writes to localStorage, assert
bytes were written, then clear it so the next run starts clean.

## Layout defects that survive a screenshot

- **Every coordinate `NaN`.** One unassigned anchor (`n.fx` read but never written) collapses
  the entire layout while the container still looks plausible. Check geometry attributes for
  `NaN` early.
- **A CSS minimum silently overriding computed sizes.** `min-width:74px` on laid-out tiles
  overrides the calculated width, so small cells overflow into neighbours and produce
  thousands of overlaps from a layout that is correct in the model.
- **A colour helper returning `NaN`.** A blend function that assumes hex but is handed an
  `rgb()` string emits `#7f1d3aNaNNaNNaN`, the browser drops the declaration, and the element
  goes transparent. Accept every format the caller can produce, or normalise at the boundary.
- **Overlap as a force rather than a constraint.** Raising repulsion in a spring simulation to
  remove overlaps makes clusters re-collapse into their anchors. Resolve overlap in a
  deterministic post-pass, annealing the anchor pull to zero on the final passes.
- **Text tight enough to read as overlapping.** Measure the minimum gap between label boxes,
  not just the overlap count. Boxes under about 2px apart look broken even at zero overlap.
  Give the placement test a real gutter.

## Test the algorithm outside the browser first

Squarified treemaps, force layouts and label placers should be unit tested in plain Python
before being wired to a DOM. Debugging a layout algorithm through a headless browser is far
slower and reliably sends you to blame the CSS for a maths bug. Assert on the output: total
area covered, pairwise overlaps, every element inside the bounding box.

## Mobile is a different defect class

Run the contrast and tap-target audit at 1440, 1024 **and** 390. Small widths surface
problems the desktop pass is clean on: sub-44px tap targets, and iOS Safari zooming on any
input under 16px. Also add `:focus-visible` rings and a `prefers-reduced-motion` block;
both are machine-checked.

## Console errors: dedupe before reporting

Collect errors keyed by a prefix, not appended raw. One bad coordinate can emit hundreds of
identical SVG attribute errors that bury the actual result and make a single bug look
catastrophic. Report the deduplicated list.

## Screenshot every view, not just the default

An artefact with tabs ships one tab. Capture each tab, at each breakpoint, after its animation
settles, then open every image and critique it. A defect in the second tab is invisible in a
screenshot of the first.

## Guard what you fixed

A checker written once is not a fix. Add an assertion for each specific defect you repaired
(badge/name collision, legend occlusion, header overlap) so it cannot return silently, and
re-run the whole checker after each build.

## Pitfalls

- **Do not report a render as verified on a clean audit alone.** Contrast clean means the
  maths passed, not that the picture reads.
- **Do not trust a vision pass on countable properties.** It miscounts and describes stale
  frames. Measure, then look.
- **Do not skip the looking step.** Reading the source or seeing an audit summary verifies
  nothing about how it reads.
- **Do not hardcode expected counts in the checker.** They drift with the design; derive them
  from the payload.
- **Deliver paths as `MEDIA:`** so they open, not as bare text.
- **No em dashes** in the artefact or the reply.
