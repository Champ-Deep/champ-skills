---
name: lead-site-growth-loop
description: Use when taking a data site from live to leads and revenue.
version: 1.0.0
---

# Lead site growth loop

A repeatable system for a small data or services site that must turn organic and paid search into qualified leads and then revenue. Built from the SellerLedger rollout. Reusable for any segment site.

## Order of work (do not reorder)

1. **Claims audit first.** Grep the live page for every claim word (verified, guaranteed, named contact, fresh) and tie each to a figure and method from the data owner. A claim without evidence is rewritten before any traffic. A prettier or louder page that says something false is worse.
2. **Ground truth by curl.** Status, headers, CSP, robots, sitemap count, `www` and `http` behaviour. Hash the home page and every segment URL: identical hashes mean the segments are one page and nothing is indexable. A bogus URL must return 404.
3. **Data asks.** Ask the data owner only for what changes a page claim: reconciled total, fill rate per field, definition and result of verification, source licence, refresh date, cost per delivered lead, delivery times. Do not repeat answered questions. Check the existing ledger of answers before drafting.
4. **Measurement before ads.** Search Console (domain property, DNS TXT), GA4, and first-party attribution (UTM, landing page, referrer saved on each request row). A strict CSP blocks analytics tags; change CSP and the privacy notice in the same commit as the tag.
5. **Pages only where the data supports them.** A segment page ships only with its own count, fill rates and sample. No template with swapped nouns.
6. **Report-only automation.** Daily lead digest, weekly Search Console and GA4 report, weekly claims and index check, monthly audit. Bots never auto-reply to a lead and never publish.
7. **Paid test last,** capped and dated, only after claims and measurement are clean.

## Decision rule

One metric crosses its threshold on a minimum sample on two consecutive periods before acting. Write a one-line hypothesis naming the metric, record the build timestamp, re-check after a fixed interval, revert what did not move and note that it failed.

## Revenue loop and reinvest rule

Request, qualify against deliverable segments, matched sample with a per-field coverage header, quote, invoice, delivery, replacement of bounces, testimonial. Payment: no checkout until there is a validated product; use an invoice or payment link, then a creator checkout only for a fixed self-serve pack. Paid spend extends only when two consecutive weeks of paid-sourced revenue meet or beat spend. Organic work is not capped this way.

## Vetting a GitHub tool or skill before use

Clone to scratch (never into the agent skills directory). Check licence, last commit, installer: no pipe-to-shell, pinned tag, no obfuscation or eval, outbound hosts match the stated purpose, credentials via env or 0600 files. Scan HEAD and the pinned tag, since they differ. Prefer vendoring the few scripts needed over running a full installer that writes to home config. A static scan is not a runtime test; say which you did.

## Pitfalls

- Competitor price and claim data from search snippets is reported, not verified; fetch the page before quoting.
- Do not publish numbers that do not reconcile; ask the data owner which scope each covers.
- Do not name tools you cannot identify; ask. A near-miss name is often a different product.
- Legal basis and source licence for selling contact data is a gate, not a footnote.
