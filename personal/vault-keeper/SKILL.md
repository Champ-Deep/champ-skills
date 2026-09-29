---
name: vault-keeper
description: >-
  Unified Celsus vault maintenance: inbox triage, client and prospect capture, daily note generation, note creation from templates, weekly review, MOC coverage, orphan and phantom repair, Excalidraw companions, TASKS.md dedupe, and safe wikilink hygiene. Absorbs vault-linker, celsus-cortex and celsus-task-dedupe. Every link write runs through the vault-linker dry-run gate with backup, a 500-edit cap and rollback, because an aggressive auto-linker once broke 38% of the vault's links. MANDATORY TRIGGER for: "vault keeper", "fix my graph", "vault hygiene", "link audit", "broken links", "inbox triage", "vault update", "clean up vault", "organize my vault", "daily note", "new person", "new client", "new company", "new product", "new effort", "new meeting", "MOC audit", "weekly review", "connect my notes", "graph cleanup", orphan or disconnected nodes, and before ANY append to TASKS.md (dedupe first).
---

## Absorbed modes

| Mode | Use when | Read |
|---|---|---|
| **vault-linker** | Any link write, link audit, broken link repair, alias rewrite, orphan or phantom fix. This is the gate; its rules override anything below | `modes/vault-linker/MODE.md` |
| **celsus-cortex** | Template details for new notes, effort tracking, weekly review generation | `modes/celsus-cortex/MODE.md` |
| **celsus-task-dedupe** | Every time anything is about to be appended to TASKS.md. Search, then append | `modes/celsus-task-dedupe/MODE.md` |

# Vault Keeper, Unified Vault Intelligence

> The librarian, organizer, and plumber of the Celsus vault. Named for the Library of Celsus
> at Ephesus, this skill keeps the knowledge alive and connected.

## Design Philosophy

Proactive vault maintenance, with one hard exception: **every link write goes through the vault-linker gate** (`modes/vault-linker/MODE.md`). On 2026-09-09 an aggressive auto-linker broke 38% of this vault's links. Triage, note creation, daily notes and reports can run on autopilot. Link changes, orphan fixes, phantom fixes and MOC additions are dry-run first, capped, backed up, and rolled back if broken links go up. `_config/link-policy.md` is authoritative.

**The golden rule**: Every file in the vault should be reachable from `[[🏠 Home]]` within 3 hops. A file that is not is reported, then fixed through the gate.

---

## Vault Structure (ACE Framework)

```
🏠 Home.md              → Root hub, all MOCs link back here
Atlas/                   → Timeless knowledge (the WHAT)
  ├── People/            → Contact profiles
  ├── Companies/         → Internal company profiles (12 companies)
  ├── Products/          → Product profiles (11 products)
  ├── Clients/           → ALL external entities: clients, prospects, partners, contacts
  ├── Context Docs/      → Brand guidelines, PRDs, reference material
  ├── MOCs/              → Maps of Content (hub notes, 8 MOCs)
  └── Me/                → Owner's profile
Calendar/                → Time-bound notes (the WHEN)
  ├── Daily Notes/       → Format: YYYY/MM/YYYY-MM-DD.md (nested only)
  └── Meetings/          → Meeting notes (YYYY-MM-DD - Topic.md)
Efforts/                 → Active work (the HOW)
  └── Active/            → Current projects and sprints
Inbox/                   → Quick capture, TEMPORARY holding. Everything here should
  └── Reference Notes/     eventually move to Atlas/ or get linked to an Atlas entity.
Excalidraw/              → Visual diagrams (.excalidraw files + companion .md files)
Other/                   → Templates, skills, archive, vault meta
  └── Templates/         → Excluded from graph via filter
```

### The 8 MOCs

| MOC | Covers | Links to |
|-----|--------|----------|
| [[Companies MOC]] | All 12 internal companies + Champions Group parent | Atlas/Companies/ |
| [[Products MOC]] | All 11 products | Atlas/Products/ |
| [[People MOC]] | All team members + internal contacts | Atlas/People/ |
| [[Clients MOC]] | ALL external entities (clients, prospects, partners, contacts) | Atlas/Clients/ |
| [[Efforts MOC]] | Active projects and sprints | Efforts/Active/ |
| [[Meetings MOC]] | All meeting notes | Calendar/Meetings/ |
| [[Context Docs MOC]] | Brand guidelines, PRDs, reference docs | Atlas/Context Docs/ |
| [[Skills MOC]] | Custom AI skills | Other/Skills/ |

---

## Core Workflows

### Workflow 1: Full Vault Scan (the "Plumber")

Steps 1C to 1F below are proposals until the vault-linker dry run is shown. Never skip the gate because a step says "auto".

This is the heavy-duty scan. Run it when the user says "fix my graph", "vault hygiene",
or as Phase 1 of the morning routine.

**What it does, in order:**

#### 1A. Build the Canonical Registry

Scan every `.md` file in the vault (excluding `.obsidian/`, `.skills/`, `.trash/`, `.git/`,
`.local-plugins/`, `Other/Templates/`). Build a map of `note_name → file_path`.

- Atlas/ paths are canonical, if the same name exists in Atlas/ and Inbox/, Atlas/ wins.
- Also extract YAML `aliases: [...]` from each file and add to the registry.

#### 1B. Link health (through the vault-linker gate)

Do NOT wikify plain text across the vault. Run vault-linker `audit` mode, then `repair` for the four defect classes (nested links, split names, never-link words, malformed syntax). Link plain-text mentions only with `link {entity}` for an entity the user named. Dry run, show counts, back up, cap at 500 edits, re-measure, roll back on regression. Full procedure: `modes/vault-linker/MODE.md`, implementation `modes/vault-linker/references/linkfix.py`.

#### 1C. Eliminate Orphans

After wikifying, scan for files with no incoming AND no outgoing links.

For each orphan:
- Read its content (first 500 chars + tags)
- Auto-connect it to the most relevant entity by appending a `## Related` section
- If it's in the vault root, move it to `Inbox/` or the appropriate Atlas subfolder

**Goal: Zero orphans.** Every file must have at least one connection.

#### 1D. Fix Phantom Links

Find all `[[wikilinks]]` that point to non-existent files.

**Auto-fix rules:**
- `[[ChampIQ]]` → `[[Champ IQ]]` (canonical name)
- `[[SPAN]]` → `[[SPAN Global Services]]`
- `[[Home]]` → `[[🏠 Home]]`
- `[[Champions]]` → `[[Champions Group]]`
- Links containing file paths like `[[Atlas/Context Docs/...]]` → fix to just the note name
- If a phantom is referenced 2+ times and looks like a real entity → create a stub note

#### 1E. MOC Coverage Audit

For each of the 8 MOCs, verify it links to ALL files in its category folder.
- `People MOC` → every file in `Atlas/People/`
- `Companies MOC` → every file in `Atlas/Companies/`
- `Products MOC` → every file in `Atlas/Products/`
- `Clients MOC` → every file in `Atlas/Clients/`
- `Efforts MOC` → every file in `Efforts/Active/`
- `Meetings MOC` → every file in `Calendar/Meetings/`
- `Context Docs MOC` → every file in `Atlas/Context Docs/` (recursive)

If anything is missing, list it and add it after the dry run. MOCs are curated hubs: add entries, never regenerate a MOC wholesale.

#### 1F. Strengthen Weak Nodes

After all the above, find files with outgoing links but no incoming links ("weak nodes").

For each weak node:
- Determine which Atlas entity it most relates to
- Add a `[[reference note name]]` link from that entity's note back to this file
- OR add the file to the appropriate MOC section
- OR link from a relevant Daily Note

**Priority connections** (from Celsus Cortex design):
1. Person ↔ Effort (who's working on what)
2. Effort ↔ Product (which project serves which product)
3. Daily Note ↔ Effort (what got done today maps to which project)
4. Client ↔ Reference Note (what docs exist for this external entity)
5. Meeting ↔ Effort (which meeting relates to which project)

---

### Workflow 2: Inbox Triage (the "Sorter")

This is the inbox organizer. Run it when the user says "inbox triage" or as part of
the morning routine.

**For each file in `Inbox/` and `Inbox/Reference Notes/`:**

1. Read the file's content, tags, and frontmatter
2. Classify:
   - Tagged `#client` or mentions an external company → Check if client exists in
     `Atlas/Clients/`. If not, create a stub. Link the reference note to the client.
   - Tagged `#meeting` or looks like meeting prep → Link from `Calendar/Meetings/` and
     `Meetings MOC`
   - Contains company/product docs → Link to the relevant company/product note and
     `Context Docs MOC`
   - Is a catalog, proposal, or strategy doc → Link to relevant entity in Atlas/Clients/
   - Can't classify → Leave in Inbox, add `[[Lake B2B]]` or `[[Champions Group]]` as
     a fallback connection based on content keywords
3. Always add at least one wikilink to an Atlas entity
4. Always add a link to the relevant MOC

**Client capture rule**: Any time a new external entity (company name, person name) appears
in a reference note, meeting note, or daily note that isn't already in `Atlas/Clients/` or
`Atlas/People/`, create a stub:
- External company/person → `Atlas/Clients/{Name}.md` with `#client` tag
- Internal team member → `Atlas/People/{Name}.md` with `#person` tag

---

### Workflow 3: Daily Note Generation

When the user requests a daily note or "what happened today":

1. Create note at `Calendar/Daily Notes/YYYY/MM/YYYY-MM-DD.md` (nested, per `_config/conventions.md`; never flat at the Daily Notes root)
2. Pre-populate:
   - Yesterday's link: `[[YYYY-MM-DD]]`
   - Tomorrow's link: `[[YYYY-MM-DD]]`
   - Active efforts from `Efforts/Active/`
   - Any meetings from today
3. Standard sections:
   - 🎯 Day at a Glance
   - 🤖 Claude Sessions
   - 📧 Email & Communications
   - 📅 Meetings
   - 🏗️ Active Efforts Progress
   - 📝 Vault Activity
   - 💡 Ideas & Insights
   - 📋 Tasks
   - 🔮 Tomorrow's Focus

### Workflow 4: Note Creation (On-Demand)

When user says "new [type] [name]":

| Type | Location | Auto-Actions |
|------|----------|-------------|
| Person | `Atlas/People/{Name}.md` | Add to People MOC, link company |
| Company | `Atlas/Companies/{Name}.md` | Add to Companies MOC |
| Product | `Atlas/Products/{Name}.md` | Add to Products MOC, link company |
| Client | `Atlas/Clients/{Name}.md` | Add to Clients MOC, link reference notes |
| Effort | `Efforts/Active/{Name}.md` | Add to Efforts MOC, link people & products |
| Meeting | `Calendar/Meetings/{Date} - {Topic}.md` | Add to Meetings MOC, link attendees |

After creating any note: fill template fields, add to MOC, propose links for the new file through vault-linker `link {entity}` mode,
create bidirectional links.

### Workflow 5: Weekly Review

When user says "weekly review":

1. Scan daily notes from the past 7 days
2. Summarize: completed tasks, effort progress, meetings held, new notes created
3. Check effort statuses, flag any untouched in 3+ days
4. Run a mini vault scan (Workflow 1) as maintenance

### Workflow 6: Excalidraw Integration

Excalidraw files (`.excalidraw`) have companion `.md` files that Obsidian uses for the
graph. These companion files often have no wikilinks, making them orphans.

**Auto-fix**: Read the Excalidraw companion `.md` file. Based on the filename and any
text content, add a `## Related` section linking to relevant efforts, meetings, or
companies. For example:
- `Marketing-Sales-Q1-Kickoff.excalidraw` → link to `[[Lake B2B]]`, `[[SPAN Global Services]]`
- `Prescription-Delivery-Conversation-Map.excalidraw` → link to `[[Health.fit]]`

---

## Integration with Morning Routine

This skill is Phases 1 and 2 of the `daily-start` skill's morning routine.

**Phase 1+2 combined (Vault Keeper):**
1. Run vault-linker `audit` on yesterday's notes + any new files and report issues. No link writes during the morning routine
2. Run Workflow 2 (Inbox Triage) on anything in Inbox/
3. Generate today's daily note (Workflow 3) if it doesn't exist
4. Produce the analysis output for Phase 3 (quiz):
   - 🟢 Yesterday's Wins (from yesterday's daily note)
   - 🟡 Needs Follow-Up (incomplete tasks, unflagged meetings)
   - 🔴 From Your Inbox (urgent items from email digest)
   - Effort status snapshot table

**Handoff to Phase 3 (Quiz):** Link issues are reported, daily note exists, analysis
is ready for the interactive quiz to consume.

---

## Conventions

### File Naming
- Atlas notes: `{Display Name}.md` (e.g., `Gary.md`, `Lake B2B.md`)
- Daily notes: `Calendar/Daily Notes/YYYY/MM/YYYY-MM-DD.md` (nested, never flat)
- Meetings: `{Date} - {Topic}.md`
- Efforts: `{Project Name}.md`

### Frontmatter
Every note should have YAML frontmatter with at minimum:
- `tags:`, array of relevant tags (#company, #client, #product, #person, #effort, etc.)
- Client stubs also get: `industry:`, `status:` (Active/Prospect/Inactive)

### Graph Config
- Exclude: `Other/Templates/` via search filter
- 7 color groups: People=orange, Companies=blue, Products=green, MOCs=yellow,
  Context Docs=coral, Clients=teal, Efforts=purple

### The 3-Hop Rule
Every file must be reachable from `[[🏠 Home]]` within 3 hops:
```
🏠 Home → MOC → Entity Note → Reference Note / Daily Note / Meeting
```
If a file violates this, report it and fix it through the vault-linker gate.

---

## Output: Vault Health Report

After any run, output a summary:

```
=== Vault Keeper Report ===

Registry: X notes indexed
Links: broken before N, after M (rolled back if M > N)
Link edits: Y (dry run shown, backup at _ARCHIVE-{date}/pre-linkfix-backup/)
Orphans: Z eliminated (was N)
Phantoms: P fixed
MOCs: 8/8 at 100% coverage ✓ (or list gaps)
Weak nodes: W remaining (was M)
New clients created: C
Inbox triaged: T files classified

Graph: avg X.Y links/note
3-hop compliance: NN% of files reachable from 🏠 Home
```

---

## Quick Invocation

| User says | What runs |
|-----------|-----------|
| "fix my graph" / "vault hygiene" / "vault keeper" | Workflow 1 (Full Scan) |
| "inbox triage" | Workflow 2 (Inbox Triage) |
| "daily note" | Workflow 3 (Daily Note) |
| "new [person/client/company/...]" | Workflow 4 (Note Creation) |
| "weekly review" | Workflow 5 (Weekly Review) |
| Called by daily-start (morning routine) | Link audit (report only) + Workflows 2+3 + Analysis output |
| "vault update" | Workflows 1+2 (scan + triage) |
| "connect my notes" / "link audit" / "broken links" | vault-linker audit, then repair after dry run |
| About to append to TASKS.md | celsus-task-dedupe mode first |
