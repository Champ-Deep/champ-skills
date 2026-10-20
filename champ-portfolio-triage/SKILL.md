---
name: champ-portfolio-triage
description: Use when reviving or assessing a Champ-Deep repo.
---

# Champ portfolio triage

Read-only assessments. Verify with `gh api`, never trust a tracker score.

## Product nicknames to repos

Deep's product names do not match repo or folder names; confirm with `gh search repos <name>` before concluding a repo does not exist. Verified: **ChampSets / Champ Set = `Champ-Deep/ChampSet`** (private fork of tinyfish-io/bigset, AGPL-3.0), whose only local clone is the folder **`/Users/deep/champ-bigset`** (check `git remote -v`, not the folder name). Its stack: Next.js frontend + Fastify backend + self-hosted Convex, agents in `backend/src/mastra`, three admin-set model roles stored in the Convex `__global__` modelConfig row with env fallbacks in `.env`. No other champ-sets-like repo exists in the org or his account.

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

## Pitfalls

The `Apps&Projects` tracker rows are unreliable in both directions. ChampOps is scored 70/"Operational" with zero code and an NXDOMAIN Supabase project. ChampLantern and deependhq-site are scored far below their real completion. Always re-verify.

When Deep asserts where something (spend, a bug, a feature) comes from, treat it as a routing fact and go there; do not re-derive attribution across the whole stack first.

## Method: rank on moveable progress, not on a score

The tracker score ranks what has already been built, so a repo that is one review away from done and a repo that needs a quarter of new code can sit within a few points of each other. Choose the next repo to push by what a session can actually finish:

1. Read every open PR and every blocked task first (`gh pr list`, plus the board), because blocked work is a decision or an access gate, not more coding.
2. Score the artifacts, not the tracker: open PRs already green, an existing readiness or gap report, an identifiable blocker, and how much of the remaining work is mergeable versus greenfield.
3. Take the oldest finished work first. Branches that have been green and unmerged for weeks are stalled on review bandwidth, and unblocking them is one session's work.
4. Prove CI coverage before trusting any green claim: a repo with no workflow that fires on feature branches reports no runs, and no runs looks like nothing wrong.
5. Fold what you learn back into the tracker row before you stop. A row left saying "agent running" after the branch was consolidated is the same stale data that made step 1 necessary.

Report the runner-up as well as the pick, with its one blocking decision, so the choice stays revisable.
