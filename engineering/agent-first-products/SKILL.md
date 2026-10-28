---
name: "agent-first-products"
description: "Use when building a standalone agent-first product or suite."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [agent-first, mcp, api, webhooks, prediction-ledger, verification]
    category: engineering
    related_skills: [mcp-builder, third-party-data-source-adoption, visual-verify]
---

# Agent-first products

Build order for a standalone product whose primary caller is an agent working for a
person, with a human console as the secondary surface.

## When to Use

Trigger on: "standalone application", "expose it via API or webhook or MCP", "make it
agent-first", "simulated audience or simulated users for testing messaging", "bring X
and Y into one suite", or any new tool where an agent, not a person, is expected to
call it first. Not for a feature inside an existing product (use that product's
development skill) and not for an MCP server on its own (use `mcp-builder`).

Each step gates the next.

## 1. Scope it standalone, before any code

- Own repo, own entry points, own API key. Sibling products (ChampIQ and any other
  internal app) are callers of the surface in step 3, never design dependencies.
- Cut a requested internal tie-in at scoping time, not mid-build: drop the branding and
  the shared assumptions, keep the generic integration seam, and record the cut in the
  spec so nobody re-adds it.
- Put the depth where the user's named primary use case is (for example a simulated
  audience for testing messaging). Everything else stays behind the generic surface
  until a real caller asks for it.

## 2. Data comes through the connection broker

Platform data (analytics, search, LinkedIn, Meta, ads) routes through the broker Deep
already uses (Treg, treg.to): the adapters hold no platform tokens and the product
needs no platform app review. Run the adoption checks in
`third-party-data-source-adoption` first; here, also:

- Verify broker auth (`treg connections`) before promising a live pull. A 401 is a
  human login step: stage a blocked card with the exact login and token-mint commands
  plus the acceptance check, never a retry loop and never a stubbed response.
- Ship a CSV path as a first-class fallback so the product works with zero connections.
- Pass the broker's cost-cap and attribution headers on every call, so one retry loop
  cannot run up the bill.

## 3. The surface every agent-first product ships

1. REST under `/v1`, bearer key minted once at init, OpenAPI at `/docs`.
2. MCP over HTTP at `/mcp/`, bearer auth, host allow-list configured for deployment.
3. MCP over stdio through a console entry point reading the key from env: the local
   agent path.
4. Agent instructions served at `/llms.txt` from the same source file as the packaged
   AGENT_SKILL.md. One file, two routes: copies drift and an agent obeys whichever copy
   it fetched.
5. Signed webhooks (HMAC-SHA256 over the raw body, header name documented) for result
   events, so callers react instead of polling.

Prove items 2 and 3 from an external client; see `mcp-builder`.

## 4. If it predicts or ranks: lock, tag, learn, score

- **Lock before results, at the database.** A trigger that rejects UPDATE and DELETE on
  prediction rows. An application-level promise is not a lock, and every accuracy claim
  rests on it.
- **Tag every prediction.** One tracking key per prediction, shipped in the
  destination's own attribution field (`utm_content=co_...`), so reconciliation is a
  join instead of a guess.
- **Fit, do not assert, the simulation's trust weight.** How far simulated judgment
  moves a number is re-fitted from real prediction/outcome pairs, and that fit is proven
  by a synthetic-recovery test that regenerates a planted weight within a tolerance. A
  hand-set weight is a placeholder and gets labeled as one.
- **Score honestly.** Accuracy is computed only from forward pairs. Demo and synthetic
  back-tests are labeled non-evidence in every report, and no accuracy claim reaches
  marketing until the forward scorecard carries it. Benchmarks carry their citation in
  the data file; ranges nobody measured are labeled derived.

## 5. Verification gate, in order

1. Tests: the full API loop plus at least one MCP test.
2. Lint with a project config: known-idiomatic patterns become project-level ignores,
   not per-file suppressions.
3. Restart the server before re-driving anything. A running process serves the pre-fix
   code, and the next hour goes into hunting a bug that is already fixed.
4. UI: Playwright driving the real flow at 390 and 1440, console errors zero, then the
   full `visual-verify` gate (audit, shoot, look, fix, re-run).
5. An external MCP client over stdio proving the packaged launch path, per `mcp-builder`.
6. Dash count zero on generated HTML.

Numeric assertions take a tolerance wherever either side is rounded for display:
harmless display rounding must not fail the gate, and the fix for that is a tolerance,
never a weakened assertion.

## 6. Copy and provenance

- Normalized forms (stems, slugs, ids) are for matching; humans see the original words.
  Produce the display form where the data is created, not in each view, and grep the
  test tree for the old token in the same edit, since tests assert on strings.
- Vendor third-party skill sets with a provenance pin (a SOURCE_SHA file naming the
  upstream repo and commit) and their licence, so the rules can be re-synced and
  attributed.

## Handoff

Anything that needs Deep (broker login, credentials, approvals) becomes a blocked card
carrying the exact commands, the acceptance check, and no secrets. The report states
what ran, what passed with counts, and what is unverified.
