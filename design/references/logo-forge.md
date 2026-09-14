---
title: Logo Forge
tags: [skill, design, branding]
created: 2026-06-19
status: ready
---

# Logo Forge

A multi-lens logo and brand-mark skill. Point it at any repo, project folder, or a known Champions company and it auto-detects the brand context, then produces 2 to 3 genuinely different logo directions. Each direction is a written creative brief plus an editable SVG draft you refine inside Claude. No external editor in the loop.

## The thesis

In a market flooded with flawless AI-generated visuals, imperfection has become the luxury signal. Raw texture and hand-made marks read as proof that a human cared, and that proof is hard to fake at scale. So **Imperfect-Luxury** is the flagship default lens. It is not the only one, which keeps the skill useful for data, cloud, and platform brands that want engineered precision.

## The six lenses

| Lens | Leans toward |
|------|--------------|
| Imperfect-Luxury (default) | Premium, founder-led, craft, anti-AI differentiation |
| Minimal-Modern | SaaS, B2B, trust, scale |
| Geometric-Systematic | Infra, data, platforms, engineering |
| Maximal-Expressive | Consumer, youth, events, disruption |
| Heritage-Craft | Legacy, institutions, trust |
| Editorial-Type | Media, thought leadership, personal brand |

## How to use

- **Install:** open `logo-forge.skill` in this folder and click Save skill, or add it via Settings > Capabilities.
- **Invoke:** "design a few logo directions for [project / repo / brand]," or just point it at a folder. Triggers on logo, brand mark, identity, wordmark, monogram, app icon, favicon, rebrand, or logo refresh.
- **Output:** a `logo-explorations/` folder with a brand brief, per-direction briefs, editable SVGs, and a `contact-sheet.html` that compares directions on light and dark from billboard down to favicon size.
- **Iterate:** ask to push, merge, or vary any direction, then regenerate the contact sheet.

## Package and demo

- Installable package: `logo-forge.skill` (this folder, Atlas/Skills).
- Demo run: brand explorations for [[Lake B2B]] and [[Cirralogix]] under `Atlas/Marketing/Logo Explorations/`, three directions each.

## Build notes

- Marks bake the hand-made quality into the path geometry so they stay intact on export. Displacement and grain filters are an in-browser hero layer over a clean flat fallback, never the only thing holding the mark together. This was caught and fixed during verification when filtered marks flattened to black in a converter.
- Verified: every SVG is valid, renders correctly on light and dark, and holds toward favicon size.

Related: [[Lake B2B]] · [[Cirralogix]] · [[Products MOC]] · [[Sreedeep Surapaneni]]
