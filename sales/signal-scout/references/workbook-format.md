# Workbook format & builder input schema

`scripts/build_signal_workbook.py` consumes two JSON files.

## findings.json

An array of company objects exactly as returned by the Stage 2 agents (see
agent-prompt-template.md), with one addition made by the orchestrator in Stage 3: each contact
gains a `"pitch"` string. Optional per-company `"rank"` (int) controls ordering; otherwise
input order is kept.

## run_config.json

```json
{
  "title": "India — $100M+ Funding Signals: Decision-Maker List",
  "signal_criteria": "Funding rounds of $100M+ in India, Jul 2025 – Jul 2026",
  "compiled_date": "14 Jul 2026",
  "pitch_context": "Lake B2B data enrichment services",
  "brand_color": "E8611A",
  "layout": "person",
  "market_sources": ["https://...", "https://..."],
  "disclaimer": "Public sources only; personal emails/mobiles to be enriched via Lake B2B / Ampliz."
}
```

`layout`: `"person"` (default — one row per contact, company facts repeated) or `"company"`
(one row per company, role column-groups like CEO / CEO LinkedIn / CFO / CFO LinkedIn ...).

## Output anatomy (both layouts)

- Row 1: brand-color title bar. Row 2: italic methodology line (criteria, window, compile
  date, disclaimer). Row 3: dark header row. Data rows zebra-striped in a light tint of the
  brand color.
- Hyperlinks: person LinkedIn ("LinkedIn ↗"), company LinkedIn, website, signal source
  ("Source ↗") — real hyperlinks, blue underlined. Missing profile → grey italic "Not found".
- Person layout columns: Rank | Company | Sector | Signal Type | Signal Specifics | Signal
  Date | Source | Role | Name & Title | Person LinkedIn | Person Findings | Personalized
  Pitch | Company LinkedIn | Website | HQ | Public Email | Public Phone | Notes.
- Notes starting with "CAUTION" render dark-red so risky rows are visible at a glance.
- Second sheet "Sources & Method": methodology prose, market-level sources, per-company
  source list, compile credit line.
- Font Arial throughout; frozen panes at the first data cell; autofilter on the header row.
- No formulas are written, so no recalc step is required. If you add computed columns, follow
  the xlsx skill's recalc rules.

## Extending

The script is intentionally small and readable. For bespoke layouts (extra columns, a
per-sector tab, a summary dashboard) import its helpers or copy the styling constants rather
than restyling from scratch — visual consistency across runs is part of the product.
