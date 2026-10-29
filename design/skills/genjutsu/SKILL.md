---
name: genjutsu
description: "Use when a UI must avoid the generic AI look: one part, a page, or a site. Checklist layer on top of frontend-design; load both."
license: MIT
---

# Genjutsu

Anti-AI-slop design pipeline with three scales. Each scale is a full procedure stored under `references/`; load the one that matches, then follow it.

| Scale | Use when | Load |
|---|---|---|
| cast | One interface or interaction needs to move or feel better (pricing cards, hero, nav) | `skill_view(name="genjutsu", file_path="references/cast/SKILL.md")` |
| paint | A whole page or product look: brainstorm, MASTER.md design system, build, audit | `skill_view(name="genjutsu", file_path="references/paint/SKILL.md")` |
| bunshin | A whole multi-page site by parallel agents, with review rounds | `skill_view(name="genjutsu", file_path="references/bunshin/SKILL.md")` |

Modules (motion, GSAP, framer-motion, CSS-native, three.js, tells, design-audit, mobile and desktop principles, compose and SwiftUI) live in `references/_jutsu/<module>/SKILL.md`. The three scales load them as needed; the paths they use (`../motion-principles/SKILL.md`) resolve inside `references/_jutsu/`.

## Rules for this setup

- Default to `cast` or `paint`. Run `bunshin` only when Deep asks for it by name: it states its own cost (upstream measured about 10.5M subagent tokens over 6 to 8 hours on a large site) and needs a host that spawns subagents. If the host cannot, step down to `paint` and say so in one line.
- Before declaring a build done, load `references/_jutsu/tells/SKILL.md` and check the output against the detected defaults. It is the cheapest slop check and works with any scale.
- `paint` and `bunshin` hand parts of the work to Impeccable when it is installed. It is: `impeccable` in this library. Use it, do not re-implement.
- The `frontend-design` skill stays the visual default for Champions deliverables. Genjutsu is the escalation when the first render looks generic. The brand skill and `visual-verify` still gate delivery.
- Where a scale tells you to run a shell resolver for `_jutsu`, the directory is the `references/_jutsu` folder of this skill.

Source and licence: see `UPSTREAM.md`.
