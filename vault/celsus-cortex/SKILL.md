---
name: celsus-cortex
description: "The thinking layer of the Celsus vault — proactive knowledge management, daily note generation, inbox triage, auto-linking, and MOC maintenance. Use this skill for any vault management task: daily notes, inbox processing, effort tracking, weekly reviews, note creation from templates, or when the user says 'morning routine', 'vault update', 'daily note', 'inbox triage', 'weekly review', 'new person/company/product/effort/meeting note', or any request to maintain, organize, or automate the Obsidian vault. MANDATORY TRIGGER for vault operations beyond simple file edits."
---

# Celsus Cortex — Vault Intelligence Layer

> Named for the Library of Celsus at Ephesus — this skill is the librarian that keeps the knowledge alive.

## Design Philosophy

The vault owner (Sreedeep / Deep) wants **Full Autopilot**: Claude proactively manages the vault — auto-links, auto-updates MOCs, suggests connections, and maintains hygiene without being asked. The vault should feel like a self-maintaining knowledge OS that feeds into AI agents (chatbot, AI SDR, digital twin).

### Time Budget (from owner's blueprint)
| Activity | Share | Cadence |
|----------|-------|---------|
| Capturing new info | 40% | Daily |
| Reviewing & refining | 30% | Daily |
| Connecting & linking | 15% | Daily |
| Building structure | 15% | Weekly |

### Priority Graph Connections
These relationships matter most and should be proactively created/maintained:
1. **Person ↔ Effort** — who's working on what
2. **Effort ↔ Product** — which project serves which product
3. **Daily Note ↔ Effort** — what got done today maps to which project

---

## Vault Structure

```
🏠 Home.md         → Root hub — all MOCs link back here
Atlas/              → Timeless knowledge
  ├── People/       → Contact profiles (Template - Person)
  ├── Companies/    → Company profiles (Template - Company)
  ├── Products/     → Product profiles (Template - Product)
  ├── Clients/      → External client profiles (Template - Client)
  ├── Context Docs/ → Brand guidelines, research, reference
  ├── MOCs/         → Maps of Content (hub notes)
  └── Me/           → Owner's profile
Calendar/           → Time-bound
  ├── Daily Notes/  → Format: YYYY/MM/DD.md (Template - Daily Note)
  └── Meetings/     → Meeting notes (Template - Meeting)
Efforts/            → Active work
  └── Active/       → Current projects (Template - Effort)
Inbox/              → Quick capture — unsorted incoming
Other/              → Templates, AI config, vault meta
  └── Templates/    → 8 templates (excluded from graph via filter)
```

### Config Files (in `.obsidian/`)
- `daily-notes.json` → format: `YYYY/MM/DD`, folder: `Calendar/Daily Notes`, template: `Other/Templates/Template - Daily Note`
- `templates.json` → folder: `Other/Templates`
- `graph.json` → search filter: `-path:"Other/Templates"`, 7 color groups

---

## Workflows

### 1. Morning Inbox Triage (Daily — Primary Entry Point)

When user starts their day or says "inbox triage" / "morning routine":

1. **Scan Inbox/** for unsorted notes
2. For each note, determine its type:
   - Person mention → move to `Atlas/People/`, apply Person template fields
   - Company mention → move to `Atlas/Companies/`, apply Company template fields
   - Meeting notes → move to `Calendar/Meetings/`, apply Meeting template fields
   - Project update → link to relevant Effort in `Efforts/Active/`
   - Research/reference → move to `Atlas/Context Docs/{relevant-subfolder}/`
   - Can't classify → leave in Inbox, flag for user review
3. **Auto-link** all moved notes (invoke vault-linker logic)
4. **Update relevant MOCs** if new Atlas entries were created
5. **Report** what was triaged with a summary

### 2. Daily Note Generation (Daily)

When user requests a daily note or at start of day:

**Depth: Balanced** (per owner preference — not minimal, not exhaustive)

1. Create note at `Calendar/Daily Notes/YYYY/MM/DD.md` using Template - Daily Note
2. Pre-populate what's knowable:
   - Link today's active efforts from `Efforts/Active/`
   - Reference yesterday's note for continuity: `[[YYYY/MM/DD-1]]`
   - Pull any tasks carried forward from yesterday
3. Sections to fill (balanced depth = fill headers + 1-2 starter bullets, leave room for user):
   - 🎯 Day at a Glance — blank, user fills
   - 🤖 Claude Sessions — auto-fill from current session context if available
   - 📧 Email & Communications — blank
   - 📅 Meetings — link to any meeting notes created today
   - 🏗️ Active Efforts Progress — auto-link active efforts
   - 📝 Vault Activity — auto-fill notes created/modified today
   - 💡 Ideas & Insights — blank
   - 📋 Tasks — carry forward incomplete tasks
   - 🔮 Tomorrow's Focus — blank
4. **Important**: Daily notes use `YYYY/MM/DD` format (nested folders), NOT `YYYY-MM-DD` (flat)

### 3. Note Creation from Templates (On-Demand)

When user says "new [person/company/product/client/effort/meeting]":

| Template | Location | Key Auto-Actions |
|----------|----------|-----------------|
| Person | `Atlas/People/{Name}.md` | Add to [[People MOC]], link company if mentioned |
| Company | `Atlas/Companies/{Name}.md` | Add to [[Companies MOC]] |
| Product | `Atlas/Products/{Name}.md` | Add to [[Products MOC]], link parent company |
| Client | `Atlas/Clients/{Name}.md` | Add to [[Clients MOC]] |
| Effort | `Efforts/Active/{Name}.md` | Add to [[Efforts MOC]], link people & products |
| Meeting | `Calendar/Meetings/{Date} - {Topic}.md` | Link attendees, link effort if related |

After creating any note:
1. Fill template fields from context (don't leave everything blank)
2. Add to relevant MOC
3. Run auto-linking on the new file
4. Create bidirectional links where priority connections exist (Person↔Effort, Effort↔Product)

### 4. Weekly Review Generation (Weekly)

When user says "weekly review" or on Fridays:

1. Create note using Template - Weekly Review
2. Auto-populate:
   - **Wins**: Scan daily notes from the past week for completed tasks and achievements
   - **Effort Status**: Pull current status from each active effort
   - **Metrics**: Leave structured but blank (user fills specific numbers)
   - **Next Week Priorities**: Carry forward any flagged items from daily notes
3. Place in `Calendar/` (or wherever weekly reviews live)
4. Link to each daily note from that week

### 5. Auto-Linking (Daily — Highest Automation Priority)

This runs as a sub-routine after ANY note creation or modification:

1. Scan the modified file for plain-text mentions of canonical note names
2. Replace with `wikilinks` using canonical case
3. Follow all vault-linker rules (see `.skills/skills/vault-linker/SKILL.md`)
4. Priority connections to always check:
   - Any person name → `[[Person Name]]`
   - Any company name → `[[Company Name]]`
   - Any product name → `[[Product Name]]`
   - Any effort name → `[[Effort Name]]`

### 6. MOC Maintenance (Weekly + Monthly)

**Weekly**: Quick coverage check
- Verify each MOC links to all files in its category folder
- Report any orphans (Atlas files not linked from their MOC)

**Monthly**: Deep audit
- Run full vault-linker scan
- Check for phantom nodes (wikilinks to non-existent files)
- Verify graph color groups are current
- Review Efforts/Active/ — archive completed efforts

---

## Integration with Other Skills

### Morning Routine (`.skills/skills/morning-routine/`)
- **Cortex is Phase 2** of the morning routine orchestrator
- Morning routine calls Cortex after vault-linker (Phase 1) has connected yesterday's context
- Cortex produces: yesterday's wins, follow-ups, inbox priorities, effort status snapshot
- This output feeds into the interactive quiz (Phase 3) and day planner (Phase 4)
- When invoked via morning routine, focus analysis on: positive momentum, email urgency, effort gaps

### Vault Linker (`.skills/skills/vault-linker/`)
- Cortex calls vault-linker logic for auto-linking
- Vault-linker handles the heavy Python-based scanning
- Cortex adds the intelligence layer (which connections to prioritize, when to run)
- In morning routine context: vault-linker runs first (Phase 1), Cortex reads the linked results

### Interactive Quiz (`.skills/skills/interactive-quiz-v2/`)
- Use for gathering structured preferences from users
- Quiz results feed back into Cortex configuration
- In morning routine context: quiz (Phase 3) uses Cortex's analysis to populate dynamic options
- See `morning-routine/references/morning-quiz-blueprint.md` for the quiz spec

### Day Planner (`.skills/skills/day-planner/`)
- Consumes Cortex's analysis output as one of its inputs
- In morning routine context: day planner (Phase 4) combines Cortex insights + quiz responses
- Standalone: day planner can run without Cortex by asking user directly

---

## CLAUDE.md Relationship

There is a single `CLAUDE.md` at the vault root — the authoritative AI context file loaded automatically by Claude Code/Cowork. It contains everything: identity, key people, all 12 companies, 11 products, clients, terms decoder, active projects, preferences, navigation hub, vault structure, and tag taxonomy.

**Rule**: Keep `CLAUDE.md` comprehensive but scannable. It's both the AI quick-reference AND the vault's master context.

---

## Conventions

### File Naming
- Atlas notes: `{Display Name}.md` (e.g., `Gary.md`, `Lake B2B.md`, `Champ IQ.md`)
- Daily notes: `YYYY/MM/DD.md` (nested year/month folders)
- Meetings: `{Date} - {Topic}.md`
- Efforts: `{Project Name}.md`

### Frontmatter
Every note MUST have YAML frontmatter with at minimum:
- `type:` — one of: person, company, product, client, effort, meeting, daily-note, weekly-review, moc, context
- `tags:` — array of relevant tags per the taxonomy in CLAUDE.md

### Wikilinks
- Always use canonical case: `[[Gary]]` not `[[gary]]`
- Use display syntax when needed: `[[Display Name|Note Name]]`
- Priority connections: Person↔Effort, Effort↔Product, DailyNote↔Effort
- Templates in `Other/Templates/` use `{{variable}}` placeholders — these are NOT real wikilinks

### Graph Hygiene
- Graph excludes: `Other/Templates/` (via search filter)
- 7 color groups: People=orange, Companies=blue, Products=green, MOCs=yellow, ContextDocs=coral, Clients=teal, Efforts=purple
- `🏠 Home` is the central hub — all MOCs link back to it

---

## Quick Invocation

User can say any of:
- "morning routine" / "inbox triage" → Workflow 1
- "daily note" / "what happened today" → Workflow 2
- "new person/company/product/client/effort/meeting" → Workflow 3
- "weekly review" / "week in review" → Workflow 4
- "link check" / "auto-link" → Workflow 5
- "MOC audit" / "vault maintenance" → Workflow 6
- "vault update" → Run relevant workflows based on context
