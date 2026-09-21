# Champ Skills

Shared agent skills for the Champions Group teams. Published for collaborators to clone and drop into any Claude Code / Cursor / Gemini / agent-skill runtime.

**128 skills** across 8 categories. Start at **[`INDEX.md`](INDEX.md)** for the full searchable list.

## Categories

| Category | Folder | What's inside | Count |
|---|---|---|---|
| Design & Creative | `design/skills/` | UI/UX, frontend design, decks, visuals, infographics, art | 26 |
| Brand Guidelines | `design/brand-guidelines/` | Official brand systems for Champions Group companies | 5 |
| Marketing & Content | `marketing/` | Blog, campaign, SEO, copywriting, social, thought leadership | 16 |
| Sales & Outreach | `sales/` | REACH stages, prospecting, negotiation, lead gen, outreach | 16 |
| Research & Science | `research/` | Literature review, papers, bioinformatics (AlphaFold/Boltz etc.) | 19 |
| Documents & Contracts | `documents/` | NDAs, docs co-authoring, one-pagers, ranch docs, reports | 7 |
| Engineering & Dev | `engineering/` | MCP, compute, testing, frontend build, site ops, webapps | 18 |
| Productivity & Meetings | `productivity/` | Daily notes, meetings, planners, onboarding, interviews, quizzes | 17 |
| Vault & KM | `vault/` | Celsus knowledge management, memory, linking, habits | 4 |

## Layout

```
champ-skills/
  INDEX.md                searchable index of all 128 skills
  design/
    skills/               design skills (frontend-design, impeccable, power-design, ...)
    brand-guidelines/     Champions Group, Lake B2B, Ampliz, SPAN Global, DeepEnd HQ brand systems
    references/           design docs and template libraries (open-design, logo-forge, beautiful-html-templates, hallmark)
    assets/               Lake B2B brand assets
    bundles/              portable single-file .skill packs
  marketing/  sales/  research/  engineering/  documents/  productivity/  vault/
```

## Install

Each skill is a self-contained folder with `SKILL.md`. Clone, then copy or symlink the folders into your agent's skills directory:

```bash
git clone https://github.com/Champ-Deep/champ-skills.git

# Claude Code
cp -R champ-skills/design/skills/frontend-design ~/.claude/skills/
cp -R champ-skills/sales/reach-engage ~/.claude/skills/

# Cursor
cp -R champ-skills/design/skills/impeccable ~/.cursor/skills/

# Bulk: copy a whole category
cp -R champ-skills/sales/* ~/.claude/skills/
```

## How to read this

- `INDEX.md` is the master searchable catalog (skill, category, one-line description).
- Each category folder has its own `README.md`.
- Each skill folder is independently usable; drag it into any agent runtime that reads `SKILL.md`.

No em dashes.
