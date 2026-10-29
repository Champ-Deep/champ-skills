---
name: 3d-scroll-site
description: "Use when a hero or site must be a 3D scroll scene: product assembling, camera orbit, sky and ground. Teardown of reference sites, the Lenis + GSAP ScrollTrigger + three.js stack, asset tiers, build recipe and scroll-driven verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [3d, scroll, webgl, three, gsap, scrolltrigger, lenis, hero, showcase, motion]
    related_skills: [live-site-design-audit, scroll-journey-kit, microsite-refresh, frontend-design, visual-verify]
---

# 3D Scroll Site

A pinned stage, an environment with depth, a product that moves through it as the visitor scrolls, and copy that lands at fixed points of the scrub. This is the look Deep points at when he says a hero is "plain": Jesko Jets, Lando Norris, Breakthrough Energy, midlife.engineering (torn down 2026-10-29, numbers below). A layout with three photos sliding together is not this; a scene is.

Triggers: "3D scroll", "pod coming together", "scene setting", "like jeskojets", "cinematic hero", "scroll animation like Dribbble", "the product should assemble as you scroll", "where is the environment".

## 1. What the references actually run (measured, not assumed)

`scripts/teardown.py out/ <url...>` renders each site at 1440, sweeps ten scroll fractions, screenshots a contact sheet, probes `document.getAnimations()`, sticky and fixed counts, canvases and WebGL contexts, and greps the page plus every loaded script URL for runtime libraries. Read the sheet before copying anything; a static fetch hides every mechanic.

| Site | Runtime found | Scroll length | Mechanics on the sheet |
|---|---|---|---|
| jeskojets.com | GSAP + ScrollTrigger, Lenis, three.js, Rive, Lottie, Webflow | 12 screens, 9 sticky/fixed, one 528px WebGL canvas, 13 elements under 3D transforms | Pinned hero: cabin wall with an oval window mask that scales until the sky fills the viewport; sky, cloud and cirrus layers at different parallax rates; sky colour grades across the scrub; manifesto reveals word by word; the jet rises from the bottom edge over the headline then pins while specs scroll; dark globe section with WebGL; vertical city ticker |
| landonorris.com | ScrollTrigger, Lenis, three.js, Rive, split-type, Webflow | 15 screens, 25 sticky/fixed, a full-viewport WebGL canvas | 3D helmet in the hero on a topographic ground; section backgrounds crossfade (off-white, olive, warm grey, dark); signature draws on; split-text headlines stagger; parallax photo collages; pinned horizontal helmet carousel; footer revealed through a rounded mask |
| breakthroughenergy.org | Lenis, three.js, Rive, Splitting, two videos, one 2D canvas | 27 screens, 26 sticky/fixed | Full-bleed greyscale video hero with a staggered headline; background snaps to chartreuse and ten photos orbit the logomark then scatter outward as the line "Energy is prosperity" lands; pinned dot pagination through sector photos |
| midlife.engineering | Lenis, Rive, Framer | 13 screens, 6 sticky/fixed | Framer-built; marquee bands, a fake audio console, card stacks. Least 3D of the four; useful only for its type and spacing |

Three of four run the same stack. That is the sanctioned runtime here: **Lenis** (smooth scroll), **GSAP ScrollTrigger** (pin and scrub), **three.js** (the scene). Rive or Lottie only for vector marks. Never a hand-rolled scroll listener; `live-site-design-audit` records why.

## 2. Scene grammar

Every reference hero decomposes into the same five layers. Build all five or it reads flat.

| Layer | What it is | Wishvin M7 example |
|---|---|---|
| Stage | A wrapper 300 to 500vh tall with a `position: sticky` 100vh child. ScrollTrigger pins it and scrubs 0 to 1 across the wrapper height | 400vh track |
| Environment | Sky gradient or HDRI, fog, a ground plane that takes a soft shadow, a horizon line, optional foreground mask (Jesko's cabin wall) | Dawn gradient, light fog, sand or grass plane, pod shadow |
| Subject | The product as a three.js object, a pre-rendered frame sequence, or layered photo planes (see asset tiers) | Three M7 modules |
| Camera | A scrubbed path: start three-quarter and low, dock the modules, orbit 30 to 60 degrees, settle front-on and slightly high | Orbit while modules dock |
| Copy | Split-text reveals keyed to scrub ranges (0.0 to 0.15 headline, 0.45 to 0.6 spec chips, 0.85 to 1 CTA), not time | "Ships as three modules" at 0, "35 days, MOQ 1" at 0.5, quote CTA at 0.9 |

Section-to-section: crossfade the page background colour on scroll (Lando) and let the next section slide over the pinned stage (Jesko). One marquee per page at most.

## 3. Asset tiers: decide before building

| Tier | You have | Build | Looks like |
|---|---|---|---|
| A | A glTF or CAD model from the client (SketchUp, Rhino, STEP; convert in Blender, export glTF with Draco) | three.js scene, real materials, module groups animated by position and rotation on the scrub | Lando helmet, Apple product pages |
| B | A rendered frame sequence (90 to 180 WebP frames from Blender, Spline or the client's renderer) | `<canvas>` drawing frame `floor(progress * n)`; preload in chunks; environment still built in CSS or three.js behind the canvas | Apple AirPods, Jesko jet |
| C | Only photographs | Procedural three.js: rounded boxes for module shells, planes with the photo mapped as glass and interior textures, emissive interior at night, real ground shadow; or, if time is short, Jesko-style layered photo planes with parallax and a mask | Lower fidelity, still a scene |

Ask for Tier A assets on day one of any client build. Ship Tier C as the concept and write "model requested" in the brief. Never claim a Tier C render is the client's product geometry.

## 4. Build recipe for a "comes together" hero

1. Poster first. A static assembled image at every width in plain HTML. No JS visitor and reduced-motion visitor see this and nothing else.
2. Lazy load the scene. three.js is 150 KB gzip and more: load it after first paint and only above 700px wide with a GPU; on phones use the Tier B sequence or the poster plus CSS parallax.
3. Scene setup: `PerspectiveCamera` 35 degrees; `Fog` matched to the sky colour; `DirectionalLight` with `castShadow` plus a soft `HemisphereLight`; ground `PlaneGeometry` with `ShadowMaterial` opacity 0.25; `ACESFilmicToneMapping`, `sRGBColorSpace`.
4. Subject groups: one `Group` per module with its own start offset (x and z apart, slight y lift, 4 to 8 degree yaw). Docked position is `(0,0,0)` with yaw 0.
5. One GSAP timeline, `scrub: 0.8`, pinned to the stage: 0 to 0.55 modules dock (`power2.inOut`), 0.5 to 0.7 seam emissive flashes once then fades, 0.3 to 0.9 camera orbit on a `CatmullRomCurve3`, 0.85 to 1 camera settles and the CTA reveals. Drive copy from the same timeline so text and geometry never drift.
6. Lighting is an environment first, lamps second. Load a CC0 HDRI (Poly Haven, 1k or 2k, downloaded into `assets/env/`) through `PMREMGenerator` and set `scene.environment`; `scene.background` stays the painted sky. Set `envMapIntensity` 0.8 to 1.2 on every material. Without an environment map every PBR material reads as plastic whatever its roughness; the Wishvin v2 hero shipped this way and Deep called it a toy. Then the key light for the shadow and a low fill.
7. Surfaces need micro-detail or they read as CAD: a tiling normal map plus roughness map on shells (painted metal panel, 0.3 to 0.45 roughness, slight anisotropic grain), real texture on any wood or slat element, panel seams and door reveals as geometry with a 4 to 8 mm bevel so light catches the edge, a sand or grass albedo plus normal on the ground, and interiors recessed 150 to 300 mm behind the glass with their own emissive so the glass has depth to show. Glass gets `envMap` reflections, `transmission` 0.9, `ior` 1.5, `roughness` 0.05. Soft shadows: `PCFSoftShadowMap` at 2048 plus a baked contact-shadow plane under each module. Post: SMAA and a light ACES grade; bloom only on the emissive interiors.
8. Materials: shells `MeshPhysicalMaterial` white, roughness 0.5; glass `MeshPhysicalMaterial` with `transmission 0.9`, `thickness 0.3`; interiors as photo-textured planes behind the glass with `emissiveMap` for the lit state.
9. Textures: fetch them into the build. A host without `Access-Control-Allow-Origin` taints WebGL textures and the scene renders black; `img.waimaoniu.net` (Wishvin) sends none. Download, resize to 1024 or 2048, convert to WebP, list each in THIRD_PARTY.md as client-owned.
10. Resize handling: `ScrollTrigger.refresh()` on resize and after fonts load; renderer `setPixelRatio(min(devicePixelRatio, 2))`.
11. Teardown: stop the render loop when the stage leaves the viewport (`onLeave`/`onEnterBack`) and when the tab is hidden.

## 5. Verify by driving, never by reading the source

```text
for f in 0 .25 .5 .75 1: scrollTo(stage.top + f * (stage.height - innerHeight)); wait 300ms;
  read window.__scene.progress, each module's world position, camera.position; screenshot
```

Pass when: module distances to dock decrease monotonically to 0; camera position differs at every fraction; five screenshots differ pairwise; reduced motion yields 0 running animations and the poster; no console or WebGL errors; frame time under 16 ms at 1440 on the dev machine (`requestAnimationFrame` delta sampled over 2 s). Put the five rows of numbers in `brief.md`. Then run the `visual-verify` matrix and the `live-site-design-audit` page audit at 1440 and 390.

## 6. Pitfalls

- The stage wrapper sized to 100vh gives a zero scrub range and nothing moves; it must be taller than the viewport.
- A scene with no `scene.environment` is plastic: clearcoat and roughness cannot fix it, only reflections can. Check `grep -c PMREM` on the scene file before any visual review.
- Realism gate: alongside the scrub probe, render the final frame beside the client's product photo at the same size and ask one bounded vision question: "same object, same material family, yes or no, and the one biggest difference". Repeat until the answer is yes.
- A scene with no ground shadow floats; the shadow is what sells depth more than the model.
- Photo crops stitched in 2D cannot be made seamless; that approach was tried on the Wishvin M7 and rejected. Go to a tier in section 3 instead.
- Webflow reference sites hide the mechanic in exported custom code; the teardown's library grep over loaded script URLs finds it, the page HTML alone does not.
- `vision_analyze` on a ten-frame contact sheet can loop when asked an open question; ask one bounded question per sheet (under 200 words, name the mechanics).
- Headless Chrome `--window-size=390` renders wider than 390; measure `scrollWidth` in Playwright before calling overflow.

## Files

- `scripts/teardown.py`: Playwright probe plus contact sheet for any list of URLs (needs `playwright` and `Pillow`).
- `references/jeskojets-sheet.png`, `references/landonorris-sheet.png`: the two heroes worth copying, ten frames each.
