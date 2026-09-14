---
tags: [context, skill]
created: 2026-06-03
status: active
---

# Skill: beautiful-html-templates

34 single-file HTML deck templates from `zarazhangrui/beautiful-html-templates`,
the library behind the 19k-star `frontend-slides` skill. A coding agent reads
`AGENTS.md` + `index.json`, matches the brief to a template, clones and adapts it.
Staged in `Atlas/Skills/beautiful-html-templates/` (screenshots excluded for
lean vault). Also in bundle as `deck-beautiful-html-templates`. Tier 1.

## What it does
Turns a brief into a polished single-file HTML deck (inline CSS/JS, no build step,
no node_modules). 34 named design systems: Neo-Grid Bold, Editorial Tri-Tone,
Broadside, Signal, Vellum, and more. Avoids generic AI-slop aesthetics.

## Why it fits [[Sreedeep Surapaneni|Sreedeep]]
Every pitch he ships: [[Lake B2B]], [[SPAN Global Services]], [[Champ IQ]],
prospect decks. Bigger template bench alongside existing `power-design`, `pptx`,
and `SlideSmith` work. Output is web-shareable HTML, good for [[DeependHQ]] embeds.

## Install (live)
```bash
cp -R ~/Celsus/Atlas/Skills/beautiful-html-templates ~/.claude/skills/deck-beautiful-html-templates
```

## Triggers
"make a deck", "build slides", "pitch deck for [company]".

## Related
[[External AI Skills Inventory]] , [[SlideSmith]] , [[ChampDeck]]
