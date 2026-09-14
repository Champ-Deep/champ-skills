---
name: vault-linker
description: Safe wikilink hygiene for the Celsus Obsidian vault. Audits link health, repairs broken and corrupted links, and resolves entity aliases, under a dry-run-first gate with rollback. Use when the user asks for a link audit, graph cleanup, broken link repair, duplicate or orphan node cleanup, or vault hygiene. Does NOT auto-link plain text by default, because doing so is what broke this vault once.
---

# Vault Linker

## Read this first

On 2026-09-09 an audit found that a previous version of this skill had broken **38% of the vault's links**: 1,545 dead targets across 8,922 occurrences. It did that by auto-linking every capitalised word it saw, which turned `TOOLS`, `USER`, `after`, `default` and `marketing` into phantom nodes, and by rewriting text that was already inside a wikilink, producing `[[Recruit [[Sreedeep Surapaneni|Champ]]]]`.

The lesson is the design principle of this skill:

> **Precision over recall. A missing link costs nothing. A wrong link costs trust in the whole graph.**

Auto-linking unlinked mentions is now **off by default** and requires an explicit instruction naming the entity to link.

## Governing policy

`_config/link-policy.md` is authoritative. Read it before every run. It carries the never-link list, the alias registry, and the bulk-operation rules. This skill implements that policy; it does not get to reinterpret it.

## Modes

| Mode | What it does | Writes? |
|------|--------------|---------|
| `audit` | Reports link health: totals, broken targets, orphans, nested corruption, alias drift, duplicate basenames | No |
| `repair` | Fixes the four defect classes below | Yes, after dry run |
| `alias` | Rewrites registry aliases into piped form | Yes, after dry run |
| `link {entity}` | Links plain-text mentions of ONE named entity | Yes, after dry run |

Default is `audit`. Never run `repair` or `link` without showing the dry run first.

## The four defect classes repair fixes

1. **Nested links.** `[[A [[B|C]] D]]` flattens to `[[A C D]]`. Never leave a `[[` inside a `[[`.
2. **Split names.** `[[Lake]] B2B` becomes `[[Lake B2B]]`. Never link a fragment of a multi-word name.
3. **Never-link words.** `[[TOOLS]]` becomes `TOOLS`. Deny-list lives in `_config/link-policy.md`.
4. **Malformed syntax.** Trailing backslashes, unbalanced brackets, links inside code fences.

## Hard guards, all mandatory

Any write pass must:

1. **Dry run first.** Print a per-target count of every change. Do not write until the operator has seen it.
2. **Never write inside** a fenced code block, inline backticks, YAML frontmatter, an HTML comment, a URL, a file path, or an existing `[[...]]`.
3. **Back up every file it touches**, to `_ARCHIVE-{date}/pre-linkfix-backup/`, before touching it.
4. **Cap at 500 edits per pass.** Over that, stop and show the diff.
5. **Measure before and after.** Count broken links on both sides. **If broken links went up, roll back.** This is not advisory.
6. **Be idempotent.** Running twice must produce the same result as running once.

## Procedure

1. Read `_config/link-policy.md`.
2. Resolve the vault root at runtime: `VAULT = os.path.expanduser("~/mnt/Celsus")`, or the device path the session reports. **Never hardcode a session path.** The old version hardcoded `/sessions/wizardly-ecstatic-allen/mnt/Celsus`, which broke on every new session.
3. Build the note registry: basename and relative path, both lowercased, for every `.md` outside `_ARCHIVE-*`, `.obsidian`, `.trash`, `studio`, `node_modules`.
4. Extract every `[[target]]` and `[[target|display]]`. Classify: resolved, broken, nested, denied, alias-drifted.
5. Report. Stop here if the mode is `audit`.
6. Dry run the chosen repairs, show counts, wait.
7. Apply with backups. Re-measure. Roll back on regression.
8. Write the run report to `Atlas/Ops/Vault-Reports/YYYY-MM-DD-Link-Audit.md`.

The working implementation used in the 2026-09-09 repair is at `references/linkfix.py`. Start from it rather than writing a new one.

## When a link is broken, the fix is usually a note

A broken link is a claim that a note should exist. Three legitimate responses, in order of preference:

1. **Create the note.** If 255 references point at `[[Champions Ranch]]`, the vault is telling you it needs that note.
2. **Alias it.** If the note exists under another name, add it to the registry in `_config/link-policy.md` and rewrite to piped form.
3. **Unlink it.** If it should never have been a link, unlink it and add the word to the never-link list.

Deleting the reference is almost never right. The reference is evidence of something real.

## Knowledge graph principles this skill follows

Drawn from ICM (Van Clief 2026, arXiv:2603.16021) and from what actually failed here.

| Principle | What it means in practice |
|-----------|---------------------------|
| **A link is an assertion** | Not decoration. If you would not defend the claim "this text is about that note", do not link it. |
| **Entity resolution before linking** | One entity, one canonical note, aliases registered. Spelling forks (Ketan and Kethan, Infratech and InfraTech) fragment a graph faster than missing links. |
| **Precision over recall** | 100 correct links beat 1,000 links of which 380 are wrong. A graph you cannot trust is worse than a sparse one. |
| **Hubs are curated, not generated** | MOCs are written by a human or a deliberate pass. A linker that auto-populates hubs makes them noise. |
| **Provenance** | Every automated pass writes a dated report saying what it changed and why. |
| **Idempotency** | Running twice changes nothing the second time. Non-idempotent passes compound their own errors, which is exactly how this vault ended up with links nested three deep. |
| **Reversibility** | Backup before write, always. Every pass must be undoable without reconstructing state. |
| **Layered context** | The linker reads the policy file, not the whole vault. Load Layer 3 policy plus the registry, nothing else. |
| **Degrade loudly** | Ambiguous target, duplicate basename, or an entity not in the registry means report it, do not guess. |

## Known unresolved issue

Three note titles exist in two folders at once: `Lake B2B`, `SPAN Global Services`, `InfraTech`, each in both `Atlas/Companies/` and `Atlas/Context Docs/`. Bare links to them are ambiguous in Obsidian. `Atlas/Companies/` is intended to be canonical. Resolving it means renaming the Context Docs copies and rewriting thousands of references. Flag it, do not silently pick one.
