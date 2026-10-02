---
name: vault-keeper
description: >-
  Unified Celsus vault maintenance: root sweep and file sorting, code-out-of-vault, inbox triage, client and prospect capture, thin-note enrichment, daily notes, note creation from templates, weekly review and triage, MOC coverage, zero-orphan healing, deep triage, Excalidraw companions, TASKS.md dedupe, and safe wikilink hygiene. Absorbs vault-linker, celsus-cortex and celsus-task-dedupe. Every link write runs through the vault-linker dry-run gate with backup, a 500-edit cap and rollback, because an aggressive auto-linker once broke 38% of the vault's links. MANDATORY TRIGGER for: "vault keeper", "fix my graph", "vault hygiene", "vault audit", "link audit", "broken links", "inbox triage", "sort my files", "clean up vault", "vault update", "daily note", "new person", "new client", "new company", "new effort", "new meeting", "MOC audit", "weekly review", "weekly triage", "enrich notes", orphan or disconnected nodes, and before ANY append to TASKS.md (dedupe first).
---

## Absorbed modes

| Mode | Use when | Read |
|---|---|---|
| **vault-linker** | Any link write, link audit, broken link repair, alias rewrite, orphan or phantom fix. This is the gate; its rules override anything below | `modes/vault-linker/MODE.md` |
| **celsus-cortex** | Template details for new notes, effort tracking, weekly review generation | `modes/celsus-cortex/MODE.md` |
| **celsus-task-dedupe** | Every time anything is about to be appended to TASKS.md. Search, then append | `modes/celsus-task-dedupe/MODE.md` |

# Vault Keeper: Unified Vault Intelligence

> The librarian, organizer, and plumber of the Celsus vault. Named for the Library of Celsus
> at Ephesus. This skill keeps the knowledge alive and connected.

## Design Philosophy

Proactive vault maintenance, with one hard exception: **every link write goes through the vault-linker gate** (`modes/vault-linker/MODE.md`). On 2026-09-09 an aggressive auto-linker broke 38% of this vault's links. Root sweeps, triage, note creation, daily notes, code-out-of-vault and reports can run on autopilot. Link changes, orphan and weak-node healing, phantom fixes and MOC additions are dry-run first, capped at 500 edits, backed up, and rolled back if broken links go up. `_config/link-policy.md` is authoritative.

**The golden rule**: Every file in the vault must be reachable from `[[🏠 Home]]` within
3 hops. If it's not, something is broken.

**The root rule**: Only 4 files live in the vault root: `🏠 Home.md`, `CLAUDE.md`,
`How to Use.canvas`, and `DB.base`. Everything else belongs in one of the 6 canonical
top-level folders. If anything else is in the root, the vault-keeper must sort it.

---

## Vault Structure (ACE Framework)

```
🏠 Home.md              -> Root hub, links to all 9 MOCs
CLAUDE.md               -> Master AI context (stays in root)
How to Use.canvas       -> Obsidian canvas (stays in root)
DB.base                 -> Database file (stays in root)

Atlas/                   -> Timeless knowledge (the WHAT)
  |- People/             -> Contact profiles
  |- Companies/          -> Internal company profiles (12+ companies)
  |- Products/           -> Product profiles (17+ products, including planned)
  |- Clients/            -> ALL external entities: clients, prospects, partners, contacts
  |    |- {Client}/      -> Per-client subfolders for deliverables/context
  |- Context Docs/       -> Brand guidelines, PRDs, reference material
  |    |- Champions/     -> Champions Accelerator, Ranch, Club docs
  |    |- Champions Group/ -> Parent company docs (MOUs, NDAs, prospectuses)
  |    |- Lake B2B/      -> Lake B2B brand, strategy, assets
  |    |- SPAN Global Services/ -> SPAN docs
  |    |- Ampliz/        -> Ampliz docs
  |    |- ChampIQ/       -> ChampIQ product docs
  |    |- General/       -> Cross-company and uncategorized docs
  |- MOCs/               -> Maps of Content (9 MOCs)
  |- Email Triage/       -> Automated email triage notes
  |- Me/                 -> Owner's profile
Calendar/                -> Time-bound notes (the WHEN)
  |- Daily Notes/        -> YYYY/MM/YYYY-MM-DD.md (nested only)
  |- Meetings/           -> Meeting notes
  |- Weekly Reviews/     -> Weekly review notes
Efforts/                 -> Active work (the HOW)
  |- Active/             -> Current projects and sprints
Inbox/                   -> Quick capture, TEMPORARY holding
  |- Reference Notes/    -> Reference material awaiting classification
  |- Data/               -> Data files (CSVs, etc.)
  |- Media/              -> Media files
Excalidraw/              -> Visual diagrams (.excalidraw + companion .md files)
Other/                   -> Templates, skills, archive, vault meta
  |- Templates/          -> Excluded from graph via filter
  |- Skills/             -> Custom AI skills
  |- Archive/            -> Old skill files, eval outputs, deprecated content
```

### The 9 MOCs

All 9 must be linked from 🏠 Home.md. If any are missing from Home, add them.

| MOC | Covers | Links to |
|-----|--------|----------|
| [[Companies MOC]] | All internal companies + Champions Group parent | Atlas/Companies/ |
| [[Products MOC]] | All products (including planned/back-burner) | Atlas/Products/ |
| [[People MOC]] | All team members + internal contacts | Atlas/People/ |
| [[Clients MOC]] | ALL external entities (clients, prospects, partners) | Atlas/Clients/ |
| [[Efforts MOC]] | Active projects and sprints | Efforts/Active/ |
| [[Meetings MOC]] | All meeting notes | Calendar/Meetings/ |
| [[Context Docs MOC]] | Brand guidelines, PRDs, reference docs | Atlas/Context Docs/ |
| [[Skills MOC]] | Custom AI skills | Other/Skills/ |
| [[Email Triage MOC]] | Automated email triage notes | Atlas/Email Triage/ |

---

## Core Workflows

### Workflow 0: Root Sweep (the "Bouncer")

This is the first thing to run on any vault cleanup. The root accumulates clutter fast
because various sessions dump their outputs there.

**What it does:**

#### 0A. Detect and Remove Junk

Before sorting, clean out files that should not exist:
- **Lock files**: `.~lock.*.xlsx#`, `.~lock.*.docx#` -> DELETE
- **Word temp files**: `~$*.docx` -> DELETE
- **macOS cruft**: `.DS_Store` -> IGNORE (don't move, don't delete)

#### 0B. Sort Non-MD Files from Root

For every file in the vault root that is NOT one of the 4 protected files
(🏠 Home.md, CLAUDE.md, How to Use.canvas, DB.base):

**Classify by content/filename, then move:**

| File Type | Classification Logic | Destination |
|-----------|---------------------|-------------|
| `.html` (daily kickoffs) | Filename contains "Daily_Kickoff" or "daily-kickoff" or "Morning_Kickoff" | `Calendar/Daily Notes/` |
| `.html` (eval/skill outputs) | Filename contains "eval-", "eval_", "-eval-review" | `Other/Archive/Eval Outputs/` |
| `.html` (company content) | Match company name in filename | `Atlas/Context Docs/{company}/` |
| `.docx` (company docs) | Match company/client name | `Atlas/Context Docs/{company}/` or `Atlas/Clients/{client}/` |
| `.xlsx` (client data) | Match client name | `Atlas/Clients/{client}/` |
| `.xlsx` (general) | KRA templates, general ops | `Atlas/Context Docs/Client-Materials/` |
| `.pptx` | Match company name | `Atlas/Context Docs/{company}/` |
| `.pdf` (client) | Match client name | `Atlas/Clients/{client}/` |
| `.skill` files | Old skill development artifacts | `Other/Archive/Skills/` |
| `.py`, `.base` (non-DB.base) | Scripts and databases | `Other/Archive/` |
| `.md` files | Classify by content (see below) | Varies |

**For .md files in root** (excluding CLAUDE.md):
- Blog posts -> `Atlas/Context Docs/Client-Materials/`
- Email drafts mentioning a client -> `Atlas/Clients/{client}/`
- LinkedIn scripts, marketing content -> `Atlas/Context Docs/Champions/`
- EU-India or other deal-specific content -> `Atlas/Context Docs/Champions/`
- Market analysis, research notes -> `Atlas/Context Docs/Client-Materials/`

**Company name matching** for classification (check filename for these patterns):
- "Champions_Ranch", "Champions_Club", "Champions_Accelerator", "Prithvi" -> `Atlas/Context Docs/Champions/`
- "Champions_Group", "CG_Branded", "KOGA", "Sector_Teaser" -> `Atlas/Context Docs/Champions Group/`
- "Lake_B2B", "LakeB2B", "b2b-pulse" -> `Atlas/Context Docs/Lake B2B/`
- "SPAN", "Subhakar", "SIG", "Phoenix" -> `Atlas/Context Docs/SPAN Global Services/`
- "[[Ampliz]]", "ampliz", "healthtech" -> `Atlas/Context Docs/Ampliz/`
- "[[VertexGrid]]" -> `Atlas/Clients/VertexGrid/`
- "Dhruv", "Chatterjee" -> `Atlas/Clients/Dhruv Chatterjee/`
- "[[Unibuild]]" -> `Atlas/Clients/Unibuild/`
- "Cirrologix", "[[Cirralogix]]" -> `Atlas/Context Docs/Client-Materials/`
- "Recruit_Champ" -> `Atlas/Context Docs/Client-Materials/`

Create destination directories as needed with `mkdir -p`.

#### 0C. Sort Rogue Directories from Root

Directories in the vault root that aren't one of the 6 canonical folders
(Atlas, Calendar, Efforts, Excalidraw, Inbox, Other):

| Pattern | Destination |
|---------|-------------|
| Skill eval folders (e.g., `b2b-blog-writer-eval-outputs/`) | `Other/Archive/` |
| Skill development folders (e.g., `b2b-blog-writer/`) | `Other/Archive/` |
| `memory/` | `Other/memory/` |
| Deal-specific folders (e.g., `EU-India Send Pack/`) | `Atlas/Context Docs/{company}/` |
| Unknown | `Other/Archive/` |

If a rogue directory is empty after its contents have been moved elsewhere, delete it.

#### 0D. Detect Duplicate/Malformed Folders

Check for folders with escaped spaces or similar naming issues:
- `Atlas/Context\ Docs/` alongside `Atlas/Context Docs/` -> merge into the proper one
- Any `folder\ name/` pattern -> merge contents into the unescaped version, delete the escaped one

This happens when files are created via CLI without proper quoting. Always use quoted
paths in mv/cp commands to prevent this.

---

### Workflow 1: Full Vault Scan (the "Plumber")

This is the heavy-duty link scan. Run it after Workflow 0 (or standalone if root is clean).

**What it does, in order:**

#### 1A. Build the Canonical Registry

Scan every `.md` file in the vault (excluding `.obsidian/`, `.skills/`, `.trash/`, `.git/`,
`.local-plugins/`, `Other/Templates/`). Build a map of `note_name -> file_path`.

- Atlas/ paths are canonical. If the same name exists in Atlas/ and Inbox/, Atlas/ wins.
- Also extract YAML `aliases: [...]` from each file and add to the registry.

#### 1B. Link health (through the vault-linker gate)

Do NOT wikify plain text across the vault. Run vault-linker `audit` mode, then `repair` for the four defect classes (nested links, split names, never-link words, malformed syntax). Link plain-text mentions only with `link {entity}` for an entity the user named. Dry run, show counts, back up, cap at 500 edits, re-measure, roll back on regression. Full procedure: `modes/vault-linker/MODE.md`, implementation `modes/vault-linker/references/linkfix.py`.

#### 1C. Eliminate Orphans

After the link-health pass, scan for files with ZERO outgoing wikilinks (excluding Other/Skills/).

For each orphan:
- Read its content (first 500 chars + tags)
- Auto-connect it by appending a `## Related` section with links to the most relevant
  Atlas entity AND the relevant MOC
- If it's in the vault root, move it first (Workflow 0), then link

**Goal: Zero orphans outside Other/Skills/.** Skill reference files are acceptable orphans
because they're consumed by the AI, not by Obsidian's graph.

#### 1D. Fix Phantom Links

Find all `wikilinks` that point to non-existent files.

**Auto-fix alias map** (apply these substitutions across the entire vault):

| Phantom | Fix to |
|---------|--------|
| `[[Champ IQ]]` | `[[Champ IQ]]` |
| `[[SPAN Global Services|SPAN]]` | `[[SPAN Global Services]]` |
| `[[SPAN Global Services|SGS]]` | `[[SPAN Global Services]]` |
| `[[Home]]` | `[[🏠 Home]]` |
| `[[Champions]]` | `[[Champions Group]]` (but NOT inside "Champions Accelerator" etc.) |
| `[[CA]]` | `[[Champions Accelerator]]` |
| `[[CI]]` | `[[Champions Infometrics]]` |
| `[[Champions Lagoons]]` | `[[InfraTech]]` |
| `[[Champions Ranch]]` | `[[InfraTech]]` |
| `[[Champions Beach Cities]]` | `[[InfraTech]]` |
| `[[Champions Smart Beach Cities]]` | `[[InfraTech]]` |

**Additional rules:**
- Links containing file paths like `[[Atlas/Context Docs/...]]` -> fix to just the note name
- If a phantom is referenced 2+ times and looks like a real entity -> create a stub note
  in the appropriate Atlas subfolder, with at minimum: frontmatter tags, a `## Related`
  section linking to the relevant MOC and parent entity

#### 1E. MOC Coverage Audit

For each of the 9 MOCs, verify it links to ALL files in its category folder:
- `People MOC` -> every `.md` file in `Atlas/People/`
- `Companies MOC` -> every `.md` file in `Atlas/Companies/`
- `Products MOC` -> every `.md` file in `Atlas/Products/`
- `Clients MOC` -> every top-level `.md` file in `Atlas/Clients/` (not subfolder files)
- `Efforts MOC` -> every `.md` file in `Efforts/Active/`
- `Meetings MOC` -> every `.md` file in `Calendar/Meetings/`
- `Context Docs MOC` -> every `.md` file in `Atlas/Context Docs/` (recursive)
- `Skills MOC` -> every SKILL.md in `Other/Skills/`
- `Email Triage MOC` -> every `.md` file in `Atlas/Email Triage/`

If anything is missing, list it, show the additions as a dry run, then add them, placing each in the most
appropriate section. If no section fits, add an `## Uncategorized` section.

**Also check**: Does `🏠 Home.md` link to ALL 9 MOCs? If any are missing, add them.

#### 1F. Strengthen Weak Nodes

After all the above, find files with outgoing links but no incoming links ("weak nodes").

For each weak node:
- Determine which Atlas entity it most relates to
- Add a `[[reference note name]]` link from that entity's note back to this file
- OR add the file to the appropriate MOC section
- OR link from a relevant Daily Note

**Priority connections:**
1. Person <-> Effort (who's working on what)
2. Effort <-> Product (which project serves which product)
3. Daily Note <-> Effort (what got done today maps to which project)
4. Client <-> Reference Note (what docs exist for this external entity)
5. Meeting <-> Effort (which meeting relates to which project)

---

### Workflow 2: Inbox Triage (the "Sorter")

Run when the user says "inbox triage" or as part of any vault cleanup.

#### 2A. Detect and Remove Inbox Junk

Before triaging, scan Inbox for things that don't belong:
- **Entire app/project directories** (e.g., `OpenClaw copy 2/`, `pikvita-quiz-main/`,
  random GitHub repos) -> Move to `Other/Archive/`
- **Sensitive files** (e.g., `github-recovery-codes.txt`, `.env`, credentials) ->
  FLAG TO USER with a warning. Do not move or delete. Say: "Found sensitive file
  at [path]. You should move this somewhere secure outside the vault."
- **Installer files** (`.dmg`, `.pkg`, `.exe`) -> Flag to user, suggest deletion
- **Duplicate files** -> Flag to user

#### 2B. Classify Reference Notes

**For each `.md` file in `Inbox/` and `Inbox/Reference Notes/`:**

1. Read the file's content, tags, and frontmatter
2. Classify:
   - Tagged `#client` or mentions an external company -> Check if client exists in
     `Atlas/Clients/`. If not, create a stub. Link the reference note to the client.
   - Tagged `#meeting` or looks like meeting prep -> Link from `Calendar/Meetings/` and
     `Meetings MOC`
   - Contains company/product docs -> Link to the relevant company/product note and
     `Context Docs MOC`
   - Is a catalog, proposal, or strategy doc -> Link to relevant entity in Atlas/Clients/
   - Can't classify -> Leave in Inbox, add `[[Lake B2B]]` or `[[Champions Group]]` as
     a fallback connection based on content keywords
3. Always add at least one wikilink to an Atlas entity
4. Always add a link to the relevant MOC

**Client capture rule**: Any time a new external entity appears in a reference note,
meeting note, or daily note that isn't already in `Atlas/Clients/` or `Atlas/People/`,
create a stub in the appropriate folder with proper tags.

---

### Workflow 3: Enrich Thin Notes (the "Fattener")

This workflow finds notes that technically exist but are too thin to be useful, and
enriches them with cross-references, context, and related documents.

#### What counts as "thin"?

- Client notes with fewer than 35 lines OR fewer than 5 wikilinks
- Company notes with fewer than 50 lines OR fewer than 10 wikilinks
- Product notes with fewer than 30 lines OR fewer than 5 wikilinks
- Person notes with fewer than 20 lines OR fewer than 3 wikilinks

#### How to enrich:

1. **Search for related content**: Grep the entire vault for mentions of the entity name.
   Check Inbox/Reference Notes/, Calendar/Meetings/, Atlas/Context Docs/, and Efforts/.
2. **Add a `## Related Documents` section** linking to every file that mentions this entity.
3. **Add a `## Context` section** summarizing what we know from related files.
4. **Add cross-references**: Link to the parent company, related products, team members,
   and any efforts involving this entity.
5. **Check for context doc subfolders**: If a company/client has documents in
   `Atlas/Context Docs/{name}/` or `Atlas/Clients/{name}/`, make sure the entity note
   links to them.

**Gap detection**: After enriching, report which high-priority entities still lack context
doc subfolders. For Deep Focus companies (Lake B2B, SPAN, Cirralogix, Recruit Champ),
having a context doc subfolder is expected.

---

### Workflow 4: Daily Note Generation

When the user requests a daily note or "what happened today":

1. Create note at `Calendar/Daily Notes/YYYY/MM/YYYY-MM-DD.md` (nested, per `_config/conventions.md`; never flat at the Daily Notes root)
2. Pre-populate:
   - Yesterday's link: `YYYY-MM-DD`
   - Tomorrow's link: `YYYY-MM-DD`
   - Active efforts from `Efforts/Active/`
   - Any meetings from today
3. Standard sections:
   - Day at a Glance
   - Claude Sessions
   - Email & Communications
   - Meetings
   - Active Efforts Progress
   - Vault Activity
   - Ideas & Insights
   - Tasks
   - Tomorrow's Focus

### Workflow 5: Note Creation (On-Demand)

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

### Workflow 6: Weekly Review / Weekly Triage

This runs on the scheduled weekly triage (Fridays 11 PM IST) or when the user says
"weekly review" or "weekly triage".

**The weekly triage is lighter than a full cleanup.** It focuses on what changed in the
past week rather than auditing the entire vault from scratch.

**Steps:**
1. **Root sweep** (Workflow 0): Check for any new files dumped in root during the week
2. **Inbox triage** (Workflow 2): Classify anything new in Inbox/
3. **Link audit on new/changed files** (vault-linker `audit`, scoped to the last 7 days; repairs only after the dry run)
4. **MOC coverage check** (Workflow 1E): Ensure any new files are in their MOCs
5. **Thin note detection** (Workflow 3): Flag any new stubs that need enrichment
6. **Weekly summary**: Scan daily notes from the past 7 days, summarize completed tasks,
   effort progress, meetings held, new notes created
7. **Effort health check**: Flag any Active efforts untouched in 3+ days
8. **Output**: Vault health report (see Output section below)

### Workflow 7: Excalidraw Integration

Excalidraw files (`.excalidraw`) have companion `.md` files that Obsidian uses for the
graph. These companion files often have no wikilinks, making them orphans.

**Auto-fix**: Read the Excalidraw companion `.md` file. Based on the filename and any
text content, add a `## Related` section linking to relevant efforts, meetings, or
companies.

---

## Integration with Morning Routine

This skill is Step 1 of the `daily-start` skill's morning routine.

**Phase 1+2 combined (Vault Keeper):**
1. Run Workflow 0 (Root Sweep) if needed
2. Run vault-linker `audit` on yesterday's notes + any new files and report link issues. No link writes during the morning routine
3. Run Workflow 2 (Inbox Triage) on anything in Inbox/
4. Generate today's daily note (Workflow 4) if it doesn't exist
5. Report the Celsus OS Decide deck depth: open `http://localhost:3043/api/state?sort=unsure`, read
   `deckSize` and the `run` date, and name the single most uncertain card as one line for Deep. This
   is the only system that reports what the vault does not know, so it belongs in the routine. Do
   not answer cards on his behalf: the deck is the human-in-the-loop surface, and a model-supplied
   answer is exactly the gap he is trying to close.
6. Produce the context summary for the user:
   - Yesterday's Wins (from yesterday's daily note)
   - Needs Follow-Up (incomplete tasks, unflagged meetings)
   - From Your Inbox (urgent items from email digest)
   - Effort status snapshot table

**Handoff to Step 2 (dashboard wizard):** Link issues are reported, today's daily note exists, the
context summary is ready, and the Decide deck depth is on the record.

---

## Conventions

### File Naming
- Atlas notes: `{Display Name}.md` (e.g., `Gary.md`, `Lake B2B.md`)
- Daily notes: `Calendar/Daily Notes/YYYY/MM/YYYY-MM-DD.md` (nested, never flat)
- Meetings: `{Date} - {Topic}.md`
- Efforts: `{Project Name}.md`

### Frontmatter
Every note should have YAML frontmatter with at minimum:
- `tags:` -- array of relevant tags (#company, #client, #product, #person, #effort, etc.)
- Client stubs also get: `industry:`, `status:` (Active/Prospect/Inactive)

### Graph Config
- Exclude: `Other/Templates/` via search filter
- 7 color groups: People=orange, Companies=blue, Products=green, MOCs=yellow,
  Context Docs=coral, Clients=teal, Efforts=purple

### The 3-Hop Rule
Every file must be reachable from `[[🏠 Home]]` within 3 hops:
```
🏠 Home -> MOC -> Entity Note -> Reference Note / Daily Note / Meeting
```
If a file violates this, the vault-keeper must create the missing link.

---

## Output: Vault Health Report

After any run, output a before/after comparison:

```
=== Vault Keeper Report ===

Registry: X notes indexed
Root files sorted: N (was M)
Links: broken before N, after M (rolled back if M > N); Y link edits after dry run
Orphans: Z remaining (was N, eliminated M)
Phantoms: P fixed (Q stubs created)
MOCs: 9/9 at 100% coverage (or list gaps)
Weak nodes: W remaining (was M)
Thin notes flagged: T
New clients created: C
Inbox triaged: I files classified
Junk removed: J files (lock files, temp files)

Graph density: avg X.Y links/note (was X.Z)
3-hop compliance: NN% of files reachable from Home
Sensitive files flagged: [list if any]
```

---

## Quick Invocation

| User says | What runs |
|-----------|-----------|
| "vault keeper" / "fix my graph" / "vault hygiene" / "vault audit" | Workflow 0 + 1 (full sweep + scan) |
| "sort my files" / "clean up root" | Workflow 0 (Root Sweep only) |
| "inbox triage" | Workflow 2 (Inbox Triage) |
| "enrich notes" / "fatten stubs" | Workflow 3 (Enrich Thin Notes) |
| "daily note" | Workflow 4 (Daily Note) |
| "new [person/client/company/...]" | Workflow 5 (Note Creation) |
| "weekly review" / "weekly triage" | Workflow 6 (Weekly Triage) |
| Called by daily-start (morning routine) | Workflow 0 + link audit (report only) + Workflows 2+4 + context summary |
| "vault update" | Workflows 0+1+2 (sweep + scan + triage) |
| "connect my notes" / "link audit" / "broken links" | vault-linker audit, then repair after dry run |
| "what am I unsure about" / "where are the gaps in my context" / "correct my context" / "what am I missing" / "fix my vault" | **Celsus OS Decide deck** at `http://localhost:3043`, not a hand-rolled grep. It is the only tool here that reports a confidence per judgement and queues the uncertain ones as cards for Deep. `celsus doctor` if it looks wrong |
| About to append to TASKS.md | celsus-task-dedupe mode first |

---

## Performance Notes

Lessons from real vault cleanups (to avoid wasting context window):

1. **Use Python scripts for bulk operations**, and for link writes use `modes/vault-linker/references/linkfix.py` so the dry run, backup and rollback come with it.
2. **Parallelize independent work.** Root sorting and inbox triage are
   independent. Use subagents to run them concurrently when available.
3. **Create directories before moving files.** Always `mkdir -p` the destination before
   `mv`. Paths with spaces need double-quoting.
4. **Watch for escaped-space duplicates.** CLI tools sometimes create `folder\ name/`
   alongside `folder name/`. Check for these every run.
5. **Weekly triage is lighter than full audit.** Scope link audits and MOC checks to
   files modified in the last 7 days rather than scanning everything.
6. **Don't re-read files already in context.** If a continuation summary says "file X has
   Y lines covering Z sections", trust it and start working.
7. **Batch mv commands.** Moving 80+ files one at a time is slow. Group by destination
   and use shell loops or xargs.

---

## Workflow 7: Code-Out-Of-Vault Enforcement (NEW, mandatory every run)

> Added 2026-04-29 after vault hit 1.4 GB with a Next.js `node_modules` (559 MB) living
> inside an Effort folder. The vault is for knowledge. Code lives in `~/Apps/`.

### Detection

Every run, scan for these and refuse to leave them in place:

| Signal | What it means | Action |
|--------|---------------|--------|
| `node_modules/` directory | JS/TS project | Externalize the whole parent project |
| `__pycache__/` directory | Python project | Externalize the whole parent project |
| `.next/`, `dist/`, `build/`, `target/` | Build artifacts | Externalize parent |
| `venv/`, `.venv/` | Python virtualenv | Externalize parent |
| `.git/` directory at >1 level deep (i.e., not the vault root's git) | Embedded repo | Externalize |
| `package.json` + `package-lock.json` | Node project root | Externalize |
| `requirements.txt` + `*.py` files (3+) | Python project root | Externalize |
| `Cargo.toml`, `go.mod`, `pyproject.toml` | Project root | Externalize |
| Folders > 5 MB that aren't `Excalidraw/` or asset libraries | Likely code | Investigate and externalize |

```bash
# Quick scan command
find . -maxdepth 6 -type d \( -name node_modules -o -name __pycache__ -o -name .next \
  -o -name dist -o -name build -o -name venv -o -name .venv \) \
  -not -path "./.obsidian/*" -not -path "./.claude*/*"
```

### Externalization protocol

When code is found inside the vault:

1. **Create staging area** at `Other/Archive/_Code-To-Externalize/` mirroring the original
   relative path. Example:
   - In vault: `Efforts/Active/Deep End Weekend Sprint/the-deep-end-site/`
   - Staged at: `Other/Archive/_Code-To-Externalize/efforts/Deep End Weekend Sprint/the-deep-end-site/`

2. **Move with `mv`** (single command, allow up to 45s for large folders).

3. **Write/update `MANIFEST.md`** at the staging root listing every moved item, original
   path, size, suggested final destination (`~/Apps/`), and the related vault note.

4. **Write `CODE-LOCATION.md`** in the original parent folder. Frontmatter:
   ```yaml
   ---
   tags: [effort, code-reference]
   project: "[[Effort Name]]"
   ---
   ```
   Body explains where the code now lives, the staging path, and the action required
   (move to `~/Apps/<name>` and delete the staging copy).

5. **Never delete code without confirmation.** Staging means the user can verify and
   move it themselves. Deletion is the user's call, not the skill's.

### Vault lean policy (absolute)

The vault contains only:
- Markdown notes (`.md`)
- Excalidraw diagrams (`.excalidraw` + companion `.md`)
- Canvas files (`.canvas`)
- Lightweight reference files (single HTML reports, single PDFs, presentation decks)
- The two protected root files (`dashboard.html`, `TASKS.md`)

The vault NEVER contains:
- `node_modules/`, `__pycache__/`, `.next/`, build outputs of any kind
- Source trees with their own `.git/`
- Generated artifacts (compiled CSS, JS bundles, logs)
- Heavy media libraries (videos, image archives)

If found: stage and externalize. No exceptions.

---

## Workflow 8: Zero-Orphan Policy (NEW, mandatory every run)

> Added 2026-04-29 after the user explicitly said: "So many orphan nodes is unacceptable."

### Definition

- **Orphan**: a `.md` file with NO incoming wikilinks AND NO outgoing wikilinks.
- **Weak node**: outgoing links exist, but no incoming links.

### The retry loop

Run orphan elimination, then **re-run it once** to verify zero orphans. If a second pass
still finds orphans, log them by path and elevate to the user. Acceptable steady state:
**0 orphans across the entire vault**.

### Auto-healing strategy

Every `## Related` append below is a link write: generate the full list, show it as a dry run, back up, cap at 500 edits per pass, re-measure broken links and roll back on regression, exactly as `modes/vault-linker/MODE.md` requires. "Mandatory every run" means the audit runs every time, not that writes skip the gate.


For each orphan, append a `## Related` section. The link list is derived from:

1. **Folder default** (longest matching prefix in `FOLDER_DEFAULT_LINKS`):
   - `Atlas/People/*` → `[[People MOC]]`
   - `Atlas/Companies/*` → `[[Companies MOC]]`
   - `Atlas/Products/*` → `[[Products MOC]]`
   - `Atlas/Clients/*` → `[[Clients MOC]]`
   - `Atlas/Context Docs/Lake B2B/*` → `[[Lake B2B]]`, `[[Context Docs MOC]]`
   - `Atlas/Context Docs/SPAN Global Services/*` → `[[SPAN Global Services]]`, `[[Context Docs MOC]]`
   - `Atlas/Context Docs/Champions/*` → `[[Champions Group]]`, `[[Context Docs MOC]]`
   - `Atlas/Context Docs/InfraTech/*` → `[[InfraTech]]`, `[[Context Docs MOC]]`
   - `Atlas/Context Docs/Meeting Prep/*` → `[[Meetings MOC]]`, `[[Context Docs MOC]]`
   - `Atlas/Context Docs/Internships/*` → `[[Champions Group]]`, `[[Context Docs MOC]]`
   - `Atlas/Email Triage/*` → `[[Email Triage MOC]]`
   - `Atlas/Ops/*` → `[[ChampOps Autonomous Maintenance Loop]]`
   - `Calendar/Daily Notes/*` → `[[🏠 Home]]`
   - `Calendar/Meetings/*` → `[[Meetings MOC]]`
   - `Efforts/Active/*` → `[[Efforts MOC]]`
   - `Excalidraw/*` → `[[🏠 Home]]`
   - `Inbox/*` → `[[🏠 Home]]`
   - `Other/Skills/*` → `[[Skills MOC]]`
   - Anything else → `[[🏠 Home]]`

2. **Keyword hints** (regex scan of file content):
   - `SPAN|SGS|Phoenix` → `[[SPAN Global Services]]`
   - `Lake B2B|LakeB2B|Lake Current|Lake Stream|Lake Harvest` → `[[Lake B2B]]`
   - `Champ IQ|ChampIQ|AI SDR` → `[[Champ IQ]]`
   - `Champmail|ChampMail` → `[[Champmail]]`
   - `ChampGraph|Champ Graph` → `[[ChampGraph]]`
   - `InfraTech|Aventura|Ranch|Beach Cities` → `[[InfraTech]]`
   - `Champions Club|Sunil` → `[[Champions Club]]`
   - `Black & Beige|B&B` → `[[Black & Beige]]`
   - `Diksha|Yotta` → respective entity
   - meeting/call/sync → `[[Meetings MOC]]`

3. **Cap at 5 links** to keep `## Related` sections readable.

### Weak node policy

Weak nodes (outgoing links present, no incoming) are auto-healed for these folders only:
`Atlas/`, `Calendar/`, `Efforts/`, `Inbox/`, `Excalidraw/`. Notes in `Other/` (skills,
plans, archive) are allowed to be weak, they're reference material, not knowledge nodes.

### MOCs are exempt

MOCs are pure hubs. They have outgoing links by design and need no incoming policy.
Skip files matching `*MOC.md` from weak-node healing.

---

## Workflow 9: Reference Stub Generation

When the skill creates new entity stubs (Workflow 4) or moves code out (Workflow 7),
the resulting stub MUST:

1. Have YAML frontmatter with `tags` array including the entity type
2. Include at least one `wikilink` to a parent entity or MOC
3. End with a `## Related` section listing 2-5 connected nodes
4. Be reachable from `[[🏠 Home]]` within 3 hops

A stub that doesn't satisfy all four checks is itself an orphan and must be re-healed
in the next pass.

---

## Health Targets (post-2026-04-29)

| Metric | Target | Failure mode |
|--------|--------|--------------|
| Orphans | **0** | Re-run orphan eliminator |
| Root files | ≤ 4 (`🏠 Home.md`, `CLAUDE.md`, `dashboard.html`, `TASKS.md`) | Run root sweep |
| `node_modules/` in vault | **0** | Run code externalization |
| MOC coverage | 100% on all 10 MOCs | Run MOC audit |
| Vault size | < 800 MB target, 500 MB ideal | Investigate large folders |
| 3-hop compliance | 100% from `[[🏠 Home]]` | Add MOC stitching |

If any target is missed at the end of a run, the report MUST flag the miss and propose
the next action.

---

## Workflow 10: Deep Triage (NEW, mandatory when user asks for "real" cleanup)

> Added 2026-04-29 after the user's directive: *"Help me really triage my vault out properly. Help me understand all of the orphan files: where they're from, why they're there, and how we get rid of them. Ideally, you put all of them into one folder."*

### Trigger phrases

"deep triage", "really triage", "lots of orphans", "graph still messy", "what should I delete", "where is all this stuff coming from", "comprehensive cleanup", "understand my orphans", "vault feels bloated", a user-shared graph view screenshot showing peripheral cloud.

### The single-folder rule

When the user asks for deep triage, do NOT scatter staging across multiple `_To-Delete-*/`, `_Code-To-Externalize/`, `_Junk-*/` folders. Build **one** review folder at the vault root:

```
_VAULT-TRIAGE-YYYY-MM-DD/
├── REVIEW.md                                ← master manifest, written FIRST
├── 01_DELETE_NOISE_DSStore/                 ← system noise, no review needed
├── 02_DELETE_JUNK_AND_DUPLICATES/           ← malformed, stale, duplicate
├── 03_EXTERNALIZE_CODE_TO_APPS/             ← + MANIFEST.md inside
├── 04_REVIEW_<DOMAIN_SPECIFIC>/             ← e.g. graphified repo artifacts
├── 05_REVIEW_<...>/                         ← duplicate bundles, etc.
├── 06_REVIEW_THIN_TEMPLATE_STUBS/           ← user judgment needed
└── 07_REVIEW_<MISC_SCRIPTS_OR_GRAY_AREA>/
```

Bucket numbering: lower numbers = more confident "delete this". Higher numbers = "review this, your call". The user opens REVIEW.md, walks bucket-by-bucket, and deletes the whole `_VAULT-TRIAGE-*` folder when done.

### Classification heuristics (the 10 categories)

| Category | Detection | Bucket |
|---|---|---|
| **CODE** | `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.sh`, `package.json`, `requirements.txt`, `pyproject.toml` | `03_EXTERNALIZE_CODE_TO_APPS/` |
| **JUNK_NOISE** | `.DS_Store`, `~$*`, `.~lock.*`, filenames starting with `[[` or `[L` | `01_DELETE_NOISE_DSStore/` (or 02 for malformed) |
| **DUPE_STEM** | Two `.md` files with identical stem; the one with fewer lines AND fewer backlinks is the loser | `02_DELETE_JUNK_AND_DUPLICATES/` |
| **STALE_DAILY** | `Calendar/Daily Notes/*.md` modified > 90 days ago AND ≤ 2 backlinks | Bucket per user discretion |
| **STALE_TRIAGE** | `Atlas/Email Triage/*.md` modified > 30 days ago | Optional bucket |
| **WEAK_THIN** | `.md` with ≤ 1 backlink AND < 25 lines AND not a MOC and not a recent stub | `06_REVIEW_THIN_TEMPLATE_STUBS/` |
| **STALE_ARCHIVE** | `Other/Archive/<dir>/` where latest file mtime > 60 days | List in REVIEW.md, optionally bucket |
| **GRAPHIFIED_RUBBLE** | Folder under `Atlas/GraphifiedRepos/` with auto-generated per-class/per-function `.md` stubs | `04_REVIEW_GRAPHIFIED_REPO_ARTIFACTS/` |
| **EMPTY_FOLDER** | Directory with zero contents (Finder may lock these) | List in REVIEW.md (can't be moved) |
| **NON_MD_ROOT** | Any `.html`/`.docx`/`.pptx`/etc. at vault root that isn't a protected file (`dashboard.html`) | Move to canonical home OR bucket |

### What NEVER goes into the triage folder

- Files in `Atlas/MOCs/` (always keep)
- The 4 protected root files (`🏠 Home.md`, `CLAUDE.md`, `dashboard.html`, `TASKS.md`)
- Files in `Other/Templates/` (excluded from graph by Obsidian config anyway)
- Files modified in the last 7 days (assume work-in-progress)

### REVIEW.md spec

Must include, per bucket:

1. **Recommendation** (DELETE ALL / REVIEW EACH / EXTERNALIZE)
2. **Count + size**
3. **Per-item table** with columns: file/folder, original location, why it's here
4. A "what to do if you want to keep one" instruction (drag back before deleting bucket)
5. **Empty Folders to Delete from Finder** section listing the dirs the sandbox couldn't remove
6. **Health snapshot** at the bottom: orphan count, reachability %, avg backlinks, root files count
7. **After-you-process** instructions (run vault keeper to clean phantom links left by removed templates)

### The retry loop after deep triage

Removing template stubs leaves phantom links in the parent client notes. The next vault-keeper run MUST:

1. Detect phantom wikilinks pointing to files in `_VAULT-TRIAGE-*` paths or to since-deleted files
2. Either remove the broken `link` lines from the parent's `## Sub-Notes (Auto-Linked)` section, OR convert the phantom into a TODO marker (e.g. `~~[[old link]]~~ removed by triage`)
3. Re-verify orphan count = 0

### Why "true orphans" alone isn't enough

The user's actual judgment of "is the graph clean" comes from looking at Obsidian's graph view. That view shows:

- True orphans (no incoming, no outgoing)
- Loose-clusters (connected to a single hub but otherwise isolated)
- Peripheral nodes (1-2 backlinks far from the main mass)

Workflow 8's zero-orphan policy handles the first. Deep triage handles the second and third by **removing low-value content from the vault entirely**. A vault with 800 well-connected notes beats a vault with 1500 notes where 700 are barely connected.

### Health Targets (additional, post-deep-triage)

| Metric | Target |
|---|---|
| Files with ≤ 1 backlink AND < 25 lines | < 30 (was 68 before this triage) |
| Avg backlinks per note | ≥ 10 |
| Files older than 90 days with no recent linkage | < 50 |
| Empty folders | 0 (excluding macOS-locked) |
| Single triage folder per cleanup pass | 1 (never spawn N parallel `_To-Delete-*/`) |
