# Research agent prompt template (Stage 2)

Copy, fill the [brackets], and launch one per batch of ~5 companies — all batches in a single
turn so they run in parallel. Keep the anti-fabrication language intact; it is the part that
keeps the output trustworthy.

---

Today is [DATE]. You are researching CURRENT leadership contacts and person-level context for
companies that recently matched this buying signal: [SIGNAL CRITERIA, e.g., "raised $100M+
funding in India, mid-2025 to mid-2026"].

Companies in your batch (with the signal context we already found — verify it, don't
re-discover it):

1. [Company — signal specifics: amount/event, date, investors/counterparty, announcement URL]
2. ...

For EACH company, use web search (and page fetches of company leadership / board /
investor-relations pages) to find:

- For each of these roles: [ROLES, e.g., CEO, CFO]:
  - Full name and exact current title
  - LinkedIn profile URL — ONLY if the linkedin.com/in/ slug appears verbatim in search
    results or on a company-owned page. Common names have lookalike profiles; if you cannot
    disambiguate, write "Not found" and explain in notes. Never construct or guess a slug.
  - person_findings: 1-3 short factual notes usable for personalization — prior companies,
    tenure/joined date, anything they publicly said about this signal (quotes from the
    announcement, interviews, LinkedIn posts). Only facts you actually saw in a source.
- Company LinkedIn page URL (linkedin.com/company/...), website, HQ city
- Publicly published corporate email and/or phone (IR, press, support, compliance pages).
  Do NOT guess or fabricate email patterns. Blank beats wrong.
- Confirm the signal: amount/event, date (month/year), counterparties, and note any nuance
  (debt vs equity, "up to" amounts, first-close vs full round, interim titles).

Leadership changes are the biggest accuracy risk — prefer sources from the last 12 months and
if a role changed recently, report BOTH the old and new holder in notes prefixed "CAUTION:".

Return ONLY a JSON array, one object per company:

```json
{
  "company": "", "company_linkedin": "", "website": "", "hq": "",
  "sector": "",
  "signal": {"type": "", "specifics": "", "date": "", "counterparties": "", "source_url": ""},
  "contacts": [
    {"role": "", "name": "", "title": "", "linkedin": "", "person_findings": ["", ""]}
  ],
  "public_email": "", "public_phone": "",
  "sources": ["url1", "url2"],
  "notes": ""
}
```

Use "" / "Not found" rather than omitting fields. Your final message must be the JSON only.

---

## Why these rules exist (context for the orchestrator)

- **Signal context passed in, not re-discovered**: agents that re-research the signal burn
  tokens and sometimes "find" a different event for the same company, corrupting the row.
- **person_findings is the personalization fuel**: Stage 3 pitches quoting a person's own
  words about the signal are the highest-performing openers this workflow produces. An agent
  that skips this field produces a technically complete but commercially weak row.
- **JSON-only final message**: the orchestrator parses agent outputs directly; prose wrappers
  around the JSON are tolerable but summaries *instead of* JSON are not.
