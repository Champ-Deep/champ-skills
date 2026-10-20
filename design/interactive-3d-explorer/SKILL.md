---
name: interactive-3d-explorer
description: Use when building an interactive 3D viewer or avatar.
version: 0.1.0
author: Sreedeep Surapaneni, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [3d, webgl, threejs, viewer, avatar]
    related_skills: [frontend-design, visual-verify]
---

# Interactive 3D Explorer

Build the scene, the controls and the proof together. The deliverable is a running viewer plus measured evidence that it works, never a description of one. Applies to body and anatomy explorers, layered product cutaways, and any WebGL scene a user drives.

Pairs with `frontend-design` (design system before code) and `visual-verify` (mandatory closing gate). Being 3D exempts a page from neither.

## When to Use

- A request to show the inside of something in 3D: body, anatomy, organs, skeleton, product cutaway, architecture with layers.
- A request for a "replica avatar", "digital twin" or personal likeness: start here for the viewer, and read the always-on honesty rules before promising a replica.
- Any WebGL scene the user drives with orbit, zoom, pick or sliders, delivered as a local file.
- Don't use for: pre-rendered or timeline-driven motion (that is `hyperframes-*` or `manim-video`), flat diagrams (the `architecture-diagram` SVG skill), or the design system itself (`frontend-design`).

## Prerequisites

- Node and npm: the build pins `three` and `esbuild`, and `npm run build` must emit both entry points before any browser work starts.
- Python Playwright with Chromium, same setup as `visual-verify`, for the harness, the audits and the offline proof.
- The brand or design-system note for the product, read before `DESIGN.md` is written, plus any product rule that forbids scores.
- No API keys, no account, no runtime network: if the build needs a key to render, it has already failed the local-only rule.

## Build order

1. **Read the design source first.** If a brand or design-system note exists, take surface, ink, accent and type from it rather than inventing a palette. Write `DESIGN.md` before any code, per `frontend-design`.
2. **Scaffold for two entry points.** Pin `three` and `esbuild`; one build bundles `src/app.js` into a `dist/` folder for iteration and also emits a **self-contained single-file HTML** with the script and CSS inlined and the CSP rewritten to `sha256-` hashes of those inlined blocks. The standalone file is what a non-engineer opens; the `dist/` build is what gets iterated on. Both must run from disk with no install and no network.
3. **One group per layer, one record map.** Each tissue or system gets its own `THREE.Group`. Every mesh carries `userData.part`, and a single notes map keyed by part id holds label, description and measurement context, so the raycaster, the `<select>` and the inspector panel all read one source. Author the notes alongside the geometry, not after it.
4. **Layer opacity and cutaway.** Per-group opacity with `depthWrite` off below full opacity. For a half-body cutaway, give the outer layer one clipping plane and the interior layers the complementary plane.
5. **Picking.** Raycast over the meshes of visible layers, then drop any hit whose material clipping planes place the point behind them.
6. **Parametric morph.** Snapshot pristine vertex positions into `userData.original` once at build time and rebuild from that snapshot on every control change.
7. **Camera discipline.** Only explicit view buttons reset the camera. Resize and morph scale the existing camera offset by the ratio of new fit distance to old, so a user's orbit survives a height change or a panel reflow.
8. **Render on demand.** Draw on interaction and state change, not a permanent rAF loop. Cap device pixel ratio and gate auto-rotation behind `prefers-reduced-motion`.
9. **Local asset import, if any.** Validate before the loader sees the file, deny external URIs twice, show imported surfaces separately from reference anatomy. Full gates: `references/local-glb-import-gates.md`.
10. **Prove it, two layers, both required.** Deterministic unit tests over geometry finiteness, preset and layer state, morph reversibility and validator rejections; then a browser harness that drives every control against a read-only `window.<name>.getState()` hook, byte-compares one capture per state, repeats the whole run offline through `visual-verify`'s `scripts/offline-check.py`, and exercises the no-WebGL fallback.

## Always-on rules

- **Illustrative stays labelled illustrative** in the scene, the panel and the export. A surface scan cannot yield internal anatomy, so imported geometry is never registered to reference layers automatically, and shape sliders are called artistic controls, never body-fat or muscle estimates.
- **No health score, biological age, diagnosis or treatment language.** Each structure carries either a real measurement with source, units and date, or an explicit "Not measured" tag. Respect any existing product rule that forbids scores.
- **No network, no storage, no telemetry, no remote fonts or CDN.** Narrow CSP, and any exported profile carries a provenance block stating what the data is and is not.
- **The canvas needs a DOM equivalent**: a select or list of the same structures with the same descriptions, keyboard reachable, because canvas content is invisible to a screen reader.
- **Report executed numbers**: tests run, checks passed, console errors, external requests, widths audited. No success adjective without the count.

## Pitfalls

- Filter raycast hits against `material.clippingPlanes` at the hit point before selecting: `Raycaster.intersectObjects` tests only object layers, so it returns clicks on meshes that are clipped away or fully transparent.
- Rebuild morph vertices from the pristine snapshot on every input: applying a delta to current positions compounds each notch, so a slider dragged out and back never returns the original body.
- Do not call the camera-fit function on resize or on every height input frame: it overwrites the controls target and camera position, yanking anyone who orbit-tested the model back to the front view mid-drag.
- Give interior layers the complementary clipping plane, not just the outer one: otherwise limbs read as muscle capsules floating through an intact skin half, which looks like a rendering bug rather than a cutaway.
- Ship the file you actually inlined as the entry, and make the pre-JavaScript status line fail loudly: an HTML file pointing at `./app.js` when only the bundled copy exists loads zero script while the page still claims to be ready.
- A standalone CSP must hash the inlined script and style, or the browser blocks them silently and the page renders unstyled with no script and no error the user can read. Compute the hash over the exact bytes you write, and inline with a replacement **function** (`() => text`), never a replacement string: `String.replace` interprets `$&`, `` $` ``, `$'` and `$$` in a string replacement, so a minified bundle containing `$` gets silently mangled, the shipped bytes no longer match the computed hash, and the browser rejects the block with a hash that looks right.
- Treat a screenshot's "clipped control" claim as a hypothesis and measure DOM bounds first: full-page shots capture scrollable panels mid-state.
- **A human figure assembled from primitives will be rejected as bad**, however it is lit: capsule limbs and sphere joints read as a toy. Start from one continuous, anatomically proportioned base mesh with a license you can credit (CC0 sources exist; ship the license file beside the artifact), and keep unlicensed or unfitted layers as disabled controls rather than shipped visuals.
- Judge a body the way the user will: open the rendered screenshot beside reference material and name proportion defects before showing it (analyze any inspo folder they send with vision first). Concrete tells to check every round: head-to-torso ratio, limb taper, shoulder-to-arm blend, planar hands, unnatural pose stiffness. "Looks fine" from the source code has never predicted the reaction to a body.
- Place pick pins against the rendered silhouette, not remembered coordinates: after any mesh or pose change, screenshot with the markers on and confirm each pin sits on its anatomical landmark. Rebuilding the geometry moves the surface out from under pins that were correct on the old mesh.

## Verification

Done means all of these are measured, with the numbers in the handoff:

- Unit suite green: geometry finiteness, every preset's visibility and clip state, morph A to B back to A byte-identical, every validator rejection case.
- Browser harness green against the artifact the user will actually open (the standalone file, not just the served build): each control driven, state hook asserted, one capture per state byte-distinct.
- `visual-verify` run to its gate: audit zero FAIL at one mobile and one desktop width, every PNG opened and critiqued, reduced motion captured if anything animates.
- `scripts/offline-check.py` exits 0: zero external requests, zero console errors, zero storage writes.
- No-WebGL fallback exercised: the page explains itself and the text anatomy still works.

## Files

- `references/local-glb-import-gates.md` - validator recipe for user-supplied 3D files: chunk framing, complexity caps, hierarchy, extension and data-URI allowlists, and the display rules that keep an import honest.
- `references/anatomy-asset-sources.md` - where to get CC0 body meshes and shape targets (MakeHuman raw-fetch recipe), and the license-shipping and labelling rules that come with them.
