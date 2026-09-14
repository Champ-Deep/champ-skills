# Champ Skills

Shared agent skills for the Champions Group teams. Published for collaborators to clone and drop into any Claude Code / Cursor / Gemini / agent-skill runtime.

## Layout

```
design/
  brand-guidelines/   Champions Group, Lake B2B, Ampliz, SPAN Global, DeepEnd HQ design systems
  skills/             Design skills (SKILL.md + reference/, scripts/, assets/)
  references/         Design docs and template libraries (open-design, logo-forge, html-anything, beautiful-html-templates, hallmark decision)
  assets/             Brand assets (Lake B2B brand book, logos)
  bundles/            Portable single-file .skill packs (frontend-design, power-design)
```

## Install

Clone the repo, then point your agent at any skill folder. Each skill is a self-contained folder with a `SKILL.md` entry point:

```
git clone https://github.com/Champ-Deep/champ-skills.git
cp -R champ-skills/design/skills/frontend-design ~/.claude/skills/
```

For Claude Code, symlink or copy folders into `.claude/skills/`. For Cursor, use `.cursor/skills/`. For other runtimes, copy into their skills directory.

## design/skills quick reference

| Skill | What it does |
|---|---|
| frontend-design | Production-grade UI/UX across web, mobile, desktop, foldables; 50+ styles, 161 palettes, 57 font pairings, 25 chart types, design-system generator |
| impeccable | Out-of-distribution craft: design, critique, audit, polish, animate, extract. Live-browser iteration |
| power-design | Design systems + brand-style playbooks for major brands |
| ui-polish | Polish pass on existing interfaces |
| design-trends | Current design trend research to ground decisions |
| canvas-design | Canvas-based design generation |
| deck-doctor | Review and fix presentation decks |
| prospect-deck | Build prospect-facing decks |
| prospect-creative-campaign-builder | Creative campaign assets for prospect outreach |
| b2b-visuals | B2B visual assets |
| b2b-visuals-to-deck | Turn B2B visuals into a deck |
| client-to-12-growth-visuals | Client growth-visual set |
| vk-b2b-visuals | Lake B2B visual palette from the vault |
| visual-report-builder | Executive visual reports |
| visual-verify | Verify rendered visuals against spec |
| web-artifacts-builder | Single-file HTML artifacts from any input |
| algorithmic-art | Generative / programmatic art |
| page-refresh | Redesign a page with a design system + template |
| notebooklm-slide-deck | Build decks for NotebookLM-friendly output |
| pdf-to-html | Convert PDFs to HTML |
| figure-composer | Compose scientific / data figures |
| figure-style | Apply consistent figure style |
| theme-factory | Generate reusable themes |
| landing-page | Landing page builder |
| frontend-handoff | Handoff-ready frontend notes |

## design/brand-guidelines

- champions-group-brand
- lakeb2b-brand-guidelines
- ampliz-brand-guidelines
- span-brand-guidelines
- deependhq-design-system

## design/references

- open-design, logo-forge, html-anything (design skills landed from the nexu-io / open-source ecosystem)
- beautiful-html-templates (28 single-file HTML deck design systems, with AGENTS.md operating manual)
- frontend-design-with-hallmark (the Champions Group visual-default decision doc)

No em dashes. Plain, this is a working skills bench for the team.
