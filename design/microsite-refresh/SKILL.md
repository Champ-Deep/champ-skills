---
name: "microsite-refresh"
description: "Use when refreshing a site via the microsite-refresh plugin."
---

# Microsite Refresh

Use this for any of Deep's marketing microsites (SellerLedger and the other Champ site properties) built or refreshed through the Champ-Deep `microsite-refresh` plugin: "use the microsite refresh plugin", a site refresh with intake contracts and a handoff build.

## When to Use

Trigger on: "use the microsite refresh plugin", a refresh of SellerLedger or another Champ site property, an intake contract run (site.json, catalog.json, page-map.json), or "rebuild the microsite and ship the handoff". Not for design-system work, live-site audits, or content-only edits; this is the build-and-ship pipeline.

The plugin is the procedure; this skill is the entry point and the pitfalls. The authoritative step by step (intake contracts, signature hero workshop, build, agent-ready audit, preview and ship) lives in the plugin's own skill at `skills/refresh-site/SKILL.md` inside the repo. Read that file first and follow it; everything below is what that document assumes you already know.

## Entry

```bash
git clone https://github.com/Champ-Deep/microsite-refresh /tmp/microsite-refresh   # scratch clone, ephemeral
less /tmp/microsite-refresh/skills/refresh-site/SKILL.md                            # the procedure
```

Work folder per site, beside the site's own source: one `build/` folder holding the intake (`site.json`, `catalog.json`, `page-map.json`, `notes.md`, `inspiration.md`) with the output under `build/dist/` (`artifact.html` plus `handoff/` containing `index.html`, `index.md`, `robots.txt`, `llms.txt`, `sitemap.xml`). Gate evidence goes in `build/brief.md`.

## Corporate and portfolio motion template

For a corporate group or product-suite homepage, use the opt-in `skills/venture-story/SKILL.md` route when that sibling is present in the plugin checkout. Its separate JSON contract represents ecosystems, ventures and attributed proof. Do not force corporate content through `build_site.py`, which requires a list catalog and verification offer. Keep the default verify-skin unchanged. Inspect the live reference's scroll behavior before borrowing its design language; static palette extraction does not capture scroll craft. Treat preview noindex policies separately from production crawler gates, and never report an isolated template as installed or deployed.

## Gate order, always

Build (reference-string guard and dash guard), then no-ai-slop `slop_lint.py`, then `agent_audit.py`, then `click_depth.py`, then `visual-verify` (`audit.py` at mobile and desktop width, both themes; `shoot.py`; the written critique). Every gate clean before the handoff ships. The reference-string guard means copy is never fixed in built HTML: change it in intake, rebuild, and let the guard prove every string has a home.

## Always-on rules

1. Owner rounds time out. If the workshop's owner round gets no answer, take the recommended option, self-author the rest under explicit creative delegation, and record every open decision in `site.json`, `notes.md`, and the gate evidence in `brief.md` so a human can reverse it later.
2. Carry the `visual-verify` contrast-parser fix (`color(srgb ...)` channels scaled by 255) whenever you run a vendored `audit.py`; without it every translucent colour fails the contrast gate at about 1:1.
3. Verify the deploy by content, not status code: byte-compare the live files against the files the worker actually serves. Fetch with `curl -sSL` plus a browser User-Agent (workers.dev 403s Python's urllib as a bot), and re-fetch once on a mismatch: `cf-cache-status: HIT` right after a deploy can serve the previous build or a stale 404. Worker-served sites may add a thin HTML wrapper the local build does not have; diff before blaming the pipeline.
4. When a refresh adopts a competitor's pricing or positioning, verify the numbers from the fetched offer page itself, never from search snippets: parse the main offer cards, check the competitor's own FAQ against those cards and record which source you used, and label the figures "advertised, not checkout-verified." Position the primary hero on the outcome the visitor came for (new reachable prospects); keep any file-cleanup tool as the secondary path. Adopted rates go into `brief.md` as a provisional test hypothesis pending fulfilment cost and margin validation, not as approved public offers, and copy changes still route through intake and rebuild per the reference-string guard. Borrow their commercial structure (package ladder, volume discount, free sample, custom-quote route), never their claims: no accuracy percentage, delivery SLA, lifetime guarantee or data-point count our fulfilment has not proven.
5. Define the billable unit in the brief before any per-lead price reaches built HTML: one distinct business matching the agreed filters plus the contact route that package promises, with extra contacts not inflating the count. A raw record count is research inventory, never "leads," and a prospect contact is never an opted-in enquiry or appointment. Publish field coverage as per-segment fill rates with estimate versus observed marked, rather than implying every column is populated.

## Pitfalls

- `click_depth.py` crashes on `"hub": null` groups in `page-map.json` (`g["hub"][1]` indexes a null). Null hubs are valid per the intake contract, so either list a hub per group or patch the script to `g.get("hub")`.
- The signature hero workshop can promise a scroll-scrubbed scene the site has no animation runtime for. When the refresh is meant to include scroll craft, load `scroll-journey-kit` (the LakeKit motion layer) as the sanctioned runtime and follow its checks; otherwise ship the motif as a static or CSS-only scene at every width and record the scrub version as v2 rather than pulling an arbitrary animation library in at build time.
- Source copy carries its own defects. Before rendering copy transcribed from a source document, diff it for internal contradictions: the same description printed under two different items, identical statistics for distinct items, outlier values against their neighbours. Flag the suspect text visibly in the output and report it to the owner; do not silently invent a replacement, and do not silently ship the contradiction.
- Deploy from the repo's documented command for that host (wrangler for the Cloudflare worker sites), and commit the handoff files to the site repo before deploying so the live build is reproducible from git.
- The worker serves only its configured asset directory (`assets.directory: ./public` in wrangler config), not the repo root. Copy every handoff file (`robots.txt`, `llms.txt`, `sitemap.xml`, `index.md`) into that directory, plus every asset the built `index.html` references: `dist/handoff/` omits things like `logo.png`, and a logo left out of the deploy set ships a broken image. Tell-tale that files missed the served directory: several routes answering with byte-identical bodies, because each is the not-found page.
- A deployed lead form can be a prototype. Before reporting capture as working, grep the served HTML for network calls (`fetch(`, `XMLHttpRequest`, a form `action=`) and for disclaimer or success-state strings: a handler that only flips DOM state and shows a confirmation sends nothing, and a page that renders a realistic in-browser report can still be entirely local.
- A catalog URL answering `200` is not a working funnel. Confirm the shipped script actually reads the query parameters and builds the order or sample request before calling a segment path functional; static markup routinely carries links no code consumes.
