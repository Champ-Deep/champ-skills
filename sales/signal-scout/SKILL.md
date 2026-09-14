---
name: signal-scout
description: >-
  Topic-based B2B signal prospecting. Takes any buying-signal criteria — funding rounds, IPOs,
  CXO changes, expansion, hiring surges, M&A, product launches, or custom criteria — researches
  companies matching the signal in a geography/timeframe, maps decision-makers (CEO/CFO/any
  titles) with verified LinkedIn URLs for companies AND individuals, and delivers a rep-ready
  Excel with a signal-based personalized pitch per contact. MANDATORY TRIGGER for: "signal
  scout", "find signals", "companies that just [raised/hired/expanded/acquired]", "who just
  raised funding", "prospect list based on [event]", "trigger-based outreach list", "top
  [category] companies with CEO/CFO contacts", or any request combining an event/signal
  criteria, a company + people contact list, and an Excel deliverable. Also trigger when a rep
  pastes criteria like "Series B+ fintechs in India this quarter" and wants contacts or
  outreach angles.
---

# Signal Scout

Turn a buying-signal criteria into a rep-ready prospecting workbook: companies matching the
signal, the right people at each, verified LinkedIn URLs, public contact channels, and a
personalized pitch per contact anchored in the signal itself.

The core insight this skill encodes: **the signal IS the pitch**. A company that just raised
$200M has money and a mandate to spend it; a new CFO wants quick wins in their first 90 days;
a company opening a Bangalore office needs local vendors. Every stage below exists to (1) find
those moments accurately and (2) convert the *specifics* of each moment into an opener a rep
can send without editing.

## Non-negotiables (read before starting)

- **Never fabricate contact data.** No guessed email patterns, no invented LinkedIn slugs, no
  assumed phone numbers. A wrong contact costs a rep more than a blank cell. Write "Not found"
  and move on — the user's data team (Lake B2B / Ampliz) enriches blanks downstream.
- **LinkedIn URLs only when the slug surfaced verbatim** in search results or on a
  company-owned page. Common names have impostor/lookalike profiles; if ambiguous, leave it
  blank and say why in Notes.
- **Leadership changes are the #1 accuracy risk.** People move constantly — a list addressed
  to last year's CEO burns credibility. Prefer sources from the last 12 months; when a role
  changed recently, flag the row with a "CAUTION:" note naming both the old and new holder.
- **Date-stamp everything.** Signals decay. Every row carries the signal date; the workbook
  header carries the compile date.

## Stage 0 — Intake

Collect these before researching. If the user is present, ask (AskUserQuestion where
available); if unattended or the dialog fails, choose sensible defaults, state them upfront,
and proceed.

1. **Signal criteria** — which event(s) qualify a company. Preset library: funding round, IPO,
   CXO appointment/departure, geographic expansion / new office, hiring surge, M&A (either
   side), product launch, regulatory approval/win. Fully custom criteria are equally valid.
   Pin down thresholds (e.g., "$50M+ rounds", "CFO changes only").
2. **Geography & timeframe** — default: last 12 months if unstated.
3. **List size** — default: top 25. Deeper verification per company at 25; lighter at 50-100.
4. **Target roles** — which titles to map per company (default: CEO + CFO; add whatever the
   signal implies — a hiring-surge signal points at CHRO, a product launch at CMO/CPO).
5. **Pitch context** — what is being sold and by which brand (e.g., Lake B2B data services,
   Ampliz healthcare intelligence, SGS, Champions Accelerator, or a custom offer). If a brand
   voice skill exists for that brand, load it before writing pitches. If the user declines a
   product angle, write signal-only conversation openers instead.

## Stage 1 — Signal discovery

Find the companies that match. Use web search first (funding trackers, exchange/IPO pages,
press releases, appointment announcements, hiring reports); Firecrawl for JS-heavy or
structured extraction when plain fetches fail.

- Search the signal from multiple angles: aggregator roundups ("largest X in [geo] [period]"),
  time-sliced queries (per quarter/month), and source-specific queries (Entrackr, TechCrunch,
  YourStory, Inc42, Chittorgarh for Indian IPOs; Crunchbase/press wires elsewhere).
- Build a candidate table bigger than the target (find ~30 to deliver 25) so weak matches can
  be dropped.
- For each candidate, record the signal specifics NOW — amount/valuation, investors, dates,
  the announcement URL. These specifics fuel the pitch later; a vague signal produces a vague
  pitch.
- Rank by signal magnitude (deal size, IPO size, seniority of the appointment) unless the user
  gives another ordering.

## Stage 2 — Contact mapping (parallel agents)

Split companies into batches of ~5 and launch one research subagent per batch, all in a single
turn so they run concurrently. Each agent prompt should include, verbatim where possible:

- Today's date and the instruction to prefer 2025-26 (current-period) sources.
- The company list with the signal context you already found (so agents verify it, not
  re-discover it).
- The target roles and, for each person: full name, exact title, LinkedIn URL rules (only
  verbatim slugs, "Not found" otherwise), plus company LinkedIn page URL, website, HQ,
  publicly published email/phone only.
- **Findings about the person** — this is what powers personalization. Ask each agent for 1-3
  short factual notes per contact: prior companies, tenure, recent quotes/posts about the
  signal, what they said in the announcement. A pitch that references "your move from Myntra"
  or "your comment about profitability in the IPO interview" outperforms a generic one.
- The anti-fabrication rules from Non-negotiables, copied into the prompt.
- A strict output contract: JSON array only, one object per company, with a `sources` array
  per row. See `references/agent-prompt-template.md` for the full copy-paste template and
  field list.

Verification is built into the agent prompts (cross-check against company-owned leadership/IR/
board pages), so a separate verify pass is only needed for rows the agents flag as uncertain
or for high-stakes lists the user calls "must be perfect" — in that case spawn a second
skeptic agent per flagged row to refute the claim.

## Stage 3 — Pitch generation

Write the pitches yourself (not in the research agents — you have the full picture of offer +
signal + person). One pitch per target person, 40-80 words, first-line-of-a-cold-email style.

Anatomy of a signal pitch:
1. **Hook = the signal specific.** Name the actual number, investor, date, or announcement —
   proof the sender did homework. ("Congrats on the $240M Prosus round" beats "Congrats on
   your recent funding".)
2. **Bridge = what that signal implies operationally.** Post-funding → scaling GTM/hiring;
   new CFO → vendor consolidation and quick wins; expansion → new-market pipeline. One clause.
3. **Offer = the user's product angle**, framed as helping with exactly that implication.
4. **Personal thread** (when findings allow): weave one person-specific fact — prior company,
   a public statement, a flagged caution (an interim CEO gets a different pitch than a
   long-tenured founder).

Write in the brand's voice if a brand skill was loaded. Avoid flattery padding, "I hope this
finds you well", and any claim about the person you cannot source. If a row's signal is
flagged CAUTION (e.g., debt not equity, interim role), the pitch must respect the nuance —
congratulating someone on "raising $193M" when it was distressed debt is a credibility bomb.

## Stage 4 — Build the workbook

Read the xlsx skill's SKILL.md first (output-format skill — read only after research is done),
then run the bundled builder:

```bash
python scripts/build_signal_workbook.py --data findings.json --config run_config.json --out <name>.xlsx
```

The script produces the house format: title + methodology banner, dark header row, zebra
stripes, per-role name/title/LinkedIn-hyperlink column groups, company LinkedIn + website
hyperlinks, signal columns (type, specifics, date, source link), one pitch column per contact
row, red-highlighted CAUTION notes, frozen panes, autofilter, and a Sources & Method sheet.
See `references/workbook-format.md` for the exact JSON schema the script expects and the
column layout. If the user asked for a layout the script doesn't cover, extend with openpyxl
directly rather than fighting the script.

Sheet layout default: **one row per person** (not per company) — reps work person-lists.
Company-level facts repeat across that company's rows; `--layout company` collapses to one
row per company with role column-groups when the user prefers the compact view.

## Stage 5 — Deliver

- Send the .xlsx to the user (SendUserFile where available) with a one-line caption.
- Summarize: how many companies/contacts, notable CAUTION rows, what was unverifiable and why.
- Offer the natural follow-ups: extend list size, different signal, sector cut, save to the
  team project, or feed the pitches into the outbound-email skill for full 3-touch sequences.
- If the run was for a recurring need ("every Monday"), offer a scheduled task.

## Quality bar (self-check before delivering)

- Every LinkedIn URL was seen verbatim in a source — spot-check 3 random ones.
- Every pitch names at least one signal specific (number, investor, date, or quote).
- Rows with role changes in the last ~9 months carry a CAUTION note.
- Signal dates fall inside the requested window; out-of-window rows kept for completeness are
  flagged.
- The Sources & Method sheet lists market-level sources and per-company source selections.
