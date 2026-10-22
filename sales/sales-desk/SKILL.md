---
name: sales-desk
description: "Use when a rep asks for a sales job by name (find accounts, map decision makers, score fit, prep discovery, break down a call, weekly report, objection, follow-up sequence, buying signals). A free, generic sales department for Claude: six desks, 26 files, hand one file to Claude with your inputs. Internal reps: the overlay table names the house skill that does the same job with company brands, data and rules baked in."
---

# Sales Desk

Six desks. Pick the file for the job, give it to Claude with your inputs, use the output. Every file is self-contained: it tells Claude what to ask for, what to do, what to return, and what it must never do.

Nothing here needs a CRM connection. Inputs are pasted text: a company name, an ICP description, a LinkedIn profile, a transcript.

## The six desks

| Desk | Job | Files |
|---|---|---|
| Find Buyers | ICP description to the right accounts and verified decision makers | `find-buyers/icp-to-account-list.md`, `decision-maker-map.md`, `lookalike-expansion.md`, `contact-verification-checklist.md` |
| Run the Pipeline | Map, score, find a warm way in, prep discovery, break down calls, write the Monday report | `pipeline/account-map.md`, `fit-score.md`, `warm-path-finder.md`, `discovery-prep.md`, `call-breakdown.md`, `monday-report.md` |
| Guides and Playbooks | The five-day high-intent play, the 30-minute demo, the AI SDR blueprint | `playbooks/high-intent-playbook.md`, `demo-guide.md`, `build-your-own-ai-sdr.md` |
| Libraries and Prompts | Discovery questions, objections, proposal structure, negotiation moves, 30 prompts | `libraries/discovery-questions.md`, `objection-handling.md`, `proposal-structure.md`, `negotiation-moves.md`, `prompt-pack.md` |
| Signal Agents | Competitor engagement, job changes, funding rounds, top 5% ranking | `signals/competitor-engagement-agent.md`, `job-change-agent.md`, `funding-round-agent.md`, `top-5-percent-scorer.md` |
| Templates and Trackers | Three first touches, a six-touch sequence, call notes, two trackers | `templates/outreach-messages.md`, `follow-up-sequence.md`, `call-notes.md`, `pipeline-tracker.csv`, `signals-tracker.csv` |

## Routing

1. One job named: open that one file, run it, stop. Do not load the whole desk.
2. "Work this account" with no stage named: `pipeline/account-map.md`, then `fit-score.md`, then `warm-path-finder.md`, then `templates/outreach-messages.md`. Hand each output to the next.
3. "Who should I call this week": `signals/top-5-percent-scorer.md` over the rep's pasted account list.
4. A pasted transcript with no instruction: `pipeline/call-breakdown.md`.
5. Every output ends with a next step and a date. Every prospect-facing line gets a plain-language pass: no hype words, no filler, no em dashes.
6. Never invent a statistic, a customer name, an email address or a phone number. Unknown is written as unknown.

## Internal overlay (Champions Group reps only)

The pack is generic by design so it can be shared. Inside the company, the same jobs run deeper through the house skills, which carry the brand map, the CLF email rules and the data sources. Use the pack file to learn the job, then the house skill to run it for real.

| Desk | House skill |
|---|---|
| Find Buyers | `reach` (Research stage), `champions-growth-profiler` mode, `treg-contact-pipeline` |
| Run the Pipeline | `reach` (Engage, Activate, Cadence, Hold), `client-call-prep`, `meeting-prep`, `meeting-followup` |
| Guides and Playbooks | `lead-gen-playbook-builder`, `prospect-campaign-plan`, `b2b-growth-showcase` |
| Libraries and Prompts | `negotiation-coach`, `outbound-email` (owns the CLF email rules), `vinh-copywriting` |
| Signal Agents | `signal-scout`, `b2b-thought-leader-pulse` |
| Templates and Trackers | `outbound-email`, `reach` (Cadence stage), `vendor-lead-handoff` |

Prospecting email inside the company always follows `outbound-email` Phase 0: under 100 words, one link, plain text, selling-brand signature, never the parent brand.
