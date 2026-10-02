---
name: champ-portfolio-triage
description: Use when reviving or assessing a Champ-Deep repo.
---

# Champ portfolio triage

Read-only assessments. Verify with `gh api`, never trust a tracker score.

## Verified 2026-10-02

**ChampLantern** (`Champ-Deep/ChampLantern`, private, Python+React, 4 commits all 2026-09-30, ~17.5k LOC).
Cloned and run it: **56 pytest passed, ruff clean**. No `.github/` dir, so zero CI. No deploy anywhere. Local clone at `Apps&Projects/ChampLantern` does NOT exist (the repo is the only copy). 7 adapter files carry TODO/NotImplementedError stubs: auth, beam, calendar, enrichment, llm, meeting, messaging. `services/gideon.py` is rule-based only. **No knowledge base, no pgvector, no embeddings anywhere in the repo** — the KB in PRD section 12 is entirely unbuilt. Signal Watch (`services/signal_watch.py`) is real: labels for confirmation / t_minus_24h / t_minus_2h / outcome_prompt / reschedule_offer / vendor_confirm_call / client_brief.

The blocker is credentials and one domain decision, not code.

**Champ_Bot** (private, TypeScript) — WhatsApp team memory bot for Lake B2B, last push 2026-07-08, no local clone.

**Graphiti-knowledge-graph** (public, Python) — last push 2026-03-19, 2 commits, 3 unmerged `claude/*` branches. Stale. Upstream `getzep/graphiti` is very much alive (commits days before 2026-10-02, ~14k stars) and now supports **FalkorDB** and Amazon Neptune alongside Neo4j, so Neo4j is no longer forced.

## OSS landscape, verified 2026-10-02

- **Cal.com went closed source 2026-04-14.** The MIT community fork is `calcom/cal.diy` (48.8k stars, 16.5k commits) with Teams, Orgs, Insights, Workflows, SSO, Routing Forms, Instant Booking and audit logging **removed**. Teams, Platform/Atoms deprecated.
- **CloudMeet is `dennisklappe/CloudMeet`**, 539 stars, 39 commits, MIT, Cloudflare Workers + D1 + Svelte, Google/Outlook sync, `workers/cron-reminders`. `pjendrusik/cloudmeet` is a fork 12 commits behind. The ChampLantern PRD section 20 cites the stale fork URL; use dennisklappe.
- WhatsApp self-host: Evolution API (Baileys-based) vs Meta Cloud API. Licensing trap: self-hosting for your own business is not distribution.
- RAG: RAGFlow, Onyx, Haystack, Graphiti.
- Avatars: LiveKit Agents lists 16 avatar providers (Tavus, LiveAvatar, AvatarTalk, LemonSlice).
- Booking video: Calendly+Loom is the only shipped precedent (CTA on video end).

## Pitfall

The `Apps&Projects` tracker rows are unreliable in both directions. ChampOps is scored 70/"Operational" with zero code and an NXDOMAIN Supabase project. ChampLantern and deependhq-site are scored far below their real completion. Always re-verify.
