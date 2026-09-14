---
tags: [context, skill]
created: 2026-06-03
status: active
---

# Skill: html-anything

Agentic HTML editor from `nexu-io/html-anything` (same team as [[open-design]]).
78 skills across 9 surfaces. Harvested as `ha-*` in `champ-skills-bundle`.
Tier 2. The full app is Next.js; we lifted the skills, not the app.

## What it does
Turns any input (Markdown, CSV, Excel, JSON, SQL, raw notes) into ship-ready
single-file HTML. Surfaces: magazine, deck, poster, social post, prototype,
data report, HyperFrames. One-click export to HTML/PNG (and WeChat/X/Zhihu).
Reuses an existing `claude login` session, zero extra API key.

## Why it fits [[Sreedeep Surapaneni|Sreedeep]]
Social content engine for [[Social Automator]], the [[LakeB2B Social Post Generator]],
and the daily social triage. Data-report surface is good for client-facing
summaries; poster/magazine for campaign assets.

## Install (live, skills only)
```bash
# from champ-skills-bundle
cp -R skills/ha-* ~/.claude/skills/     # then restart
```

## Triggers
"turn this into HTML", "make a social post", "data report from this CSV".

## Related
[[External AI Skills Inventory]] , [[open-design]] , [[Social Automator]]
