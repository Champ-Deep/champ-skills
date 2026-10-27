---
name: "microsite-refresh"
description: "Use when refreshing a site via the microsite-refresh plugin."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [microsite, refresh, plugin, templates, gates]
    related_skills: [visual-verify, no-ai-slop, frontend-design-pro]
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

Standard invocation (full bundle, 21st.dev connector on): run the whole plugin from its single entry point, `Refresh <site>` or `/refresh-site <url>`, never from a sub-skill. `refresh-site` chains intake, copy, nav, build, inner pages, gates, preview and critique, and `frontend-design-pro` pulls components from 21st.dev. This is how Boardroom ran it in the Boardroom demo (literal prompt not recorded; ask Boardroom if it is needed).

Work folder per site, beside the site's own source: one `build/` folder holding the intake (`site.json`, `catalog.json`, `page-map.json`, `notes.md`, `inspiration.md`) with the output under `build/dist/` (`artifact.html` plus `handoff/` containing `index.html`, `index.md`, `robots.txt`, `llms.txt`, `sitemap.xml`). Gate evidence goes in `build/brief.md`.

## Corporate and portfolio motion template

For a corporate group or product-suite homepage, use the opt-in `skills/venture-story/SKILL.md` route when that sibling is present in the plugin checkout. Its separate JSON contract represents ecosystems, ventures and attributed proof. Do not force corporate content through `build_site.py`, which requires a list catalog and verification offer. Keep the default verify-skin unchanged. Inspect the live reference's scroll behavior before borrowing its design language; static palette extraction does not capture scroll craft. Treat preview noindex policies separately from production crawler gates, and never report an isolated template as installed or deployed.

## Adding a new opt-in skin

A new visual direction (brutalist, editorial, terminal) ships as a sibling skill of `refresh-site` in the plugin checkout, never as a branch of `refresh-site` itself. Copy the `venture-story` shape: `SKILL.md` (when to use it and its JSON contract), `DESIGN.md`, `template.html` + `styles.css` + `motion.js`, a `build.py` with `tests/`, and `THIRD_PARTY.md` naming every vendored asset's licence. Bump `.claude-plugin/plugin.json` version and description in the same commit, or the plugin advertises a skill its checkout does not contain. Ship one worked `examples/` site and a build test that renders it, so the template is provably runnable rather than a described intention.

The dark palette of an existing site is often declared untouchable while its light mode is open for change: scope the skin's tokens to the light branch only and prove both themes still render (both widths, both schemes) before reporting it applied.

## Paid-campaign landing pages

A single-offer SPAN page starts with the portable `span-landing-page` skill in Champ-Deep/champ-skills (`design/span-landing-page/`). It bundles the implementation mirrored from this plugin's `skills/campaign-landing/`: one headline set per ad group, four primary fields, site.json driving template.html through build.py. Keep refresh-site for catalog microsites. Preserve optional source fields and omit unsupported proof sections: the MSP example has no counts, so no stat band, clients, quantitative boards or source buttons. The plugin campaign-landing route remains supported.

Three section shapes to build the right way from the start, because each has already been rejected once:

- **A slider that crops data lists is a curtain, not a comparison.** With verified counts, keep separate adjustable bento boards per book, side by side on desktop, stacked on phones. Reorder stays inside its board while pin/ratio feedback can compare across boards. Do not combine PEO and EOR into one board. Without count evidence, omit the comparison instead of inventing distributions. A stat band, when supported, is always white with green figures after the dark hero.
- **An FAQ or objections block ships one playable visual per answer, not five paragraphs.** Each answer gets a small interactive graphic that states it and responds to the reader (segment tiles that set the form, sources flowing into one record, an animating notice window, a stamped sample that tilts, role chips), with the copy underneath explaining it. A static diagram or a text-only FAQ on a paid page reads as a wall and gets skimmed past, so a rejection of a section as "shabby" or "hand drawn" means replace the composition, not recolour it.
- **Absolutely positioned data tiles need an overlap probe, not just an area sum.** Border-box means a tile shorter than its own padding still renders at padding height, so region areas can sum to 1.0 while two tiles overlap by a couple of pixels. Zero the padding on tiles too small to label, and probe pairwise rect intersection alongside the sums.

When a hand-built page is converted into a tokenized template, prove the conversion before shipping: build from the template and diff the output against the known-good artifact, normalizing only the attributes the tokens legitimately change (data labels, derived rows). Every other byte must match. After that, the template's build tests and build-time validators (dash guard, count reconciliation against stated totals, HTTPS-only URLs, escaping) become the standing gates, so copy edits land in `site.json` and never in the built HTML.

## Gate order, always

Build (reference-string guard and dash guard), then no-ai-slop `slop_lint.py`, then `agent_audit.py`, then `click_depth.py`, then `visual-verify` (`audit.py` at mobile and desktop width, both themes; `shoot.py`; the written critique). Then score the built handoff with the `ten-out-of-ten` scorecard (`references/scorecard.md` in that skill, 10 checks, evidence per check) and put the n/10 and the failing checks in `build/brief.md`; a failing proof check is an owner to-do, never filled with invented content. Every gate clean before the handoff ships. The reference-string guard means copy is never fixed in built HTML: change it in intake, rebuild, and let the guard prove every string has a home.

## Always-on rules

1. Owner rounds time out. If the workshop's owner round gets no answer, take the recommended option, self-author the rest under explicit creative delegation, and record every open decision in `site.json`, `notes.md`, and the gate evidence in `brief.md` so a human can reverse it later.
2. Carry the `visual-verify` contrast-parser fix (`color(srgb ...)` channels scaled by 255) whenever you run a vendored `audit.py`; without it every translucent colour fails the contrast gate at about 1:1. Treat a wall of identical fails as a broken checker: recompute the value yourself from the live DOM and cite your own number before reporting the gate clean or red.
3. Verify the deploy by content, not status code: byte-compare the live files against the files the worker actually serves. Fetch with `curl -sSL` plus a browser User-Agent (workers.dev 403s Python's urllib as a bot), and re-fetch once on a mismatch: `cf-cache-status: HIT` right after a deploy can serve the previous build or a stale 404. Worker-served sites may add a thin HTML wrapper the local build does not have; diff before blaming the pipeline.
4. When a refresh adopts a competitor's pricing or positioning, verify the numbers from the fetched offer page itself, never from search snippets: parse the main offer cards, check the competitor's own FAQ against those cards and record which source you used, and label the figures "advertised, not checkout-verified." Position the primary hero on the outcome the visitor came for (new reachable prospects); keep any file-cleanup tool as the secondary path. Adopted rates go into `brief.md` as a provisional test hypothesis pending fulfilment cost and margin validation, not as approved public offers, and copy changes still route through intake and rebuild per the reference-string guard. Borrow their commercial structure (package ladder, volume discount, free sample, custom-quote route), never their claims: no accuracy percentage, delivery SLA, lifetime guarantee or data-point count our fulfilment has not proven.
5. Define the billable unit in the brief before any per-lead price reaches built HTML: one distinct business matching the agreed filters plus the contact route that package promises, with extra contacts not inflating the count. A raw record count is research inventory, never "leads," and a prospect contact is never an opted-in enquiry or appointment. Publish field coverage as per-segment fill rates with estimate versus observed marked, rather than implying every column is populated.
6. 21st.dev is the default component source, not an optional extra. Prerequisite: the connector is on, URL `https://21st.dev/api/mcp`, header `x-api-key`. Verify with `hermes mcp list` (twentyfirst shows enabled) and `hermes mcp test twentyfirst` (connects, lists tools). Live check 2026-10-23: enabled, connected in about 3 s, 51 tools; a Hermes session started before it was enabled does not see the tools until restarted. Env var is `TWENTY_FIRST_API_KEY` on this machine but `API_KEY_21ST` in the plugin README; never write the key into a file, page or the vault. Free tier allows 2 `get_component` pulls a day (`get_usage` shows what is left). If it is off, say so in one line and use `references/components.md` in the plugin, and the run is not the standard run.
7. Never run sub-skills alone. Partial or single-step runs are unsupported: they skip the intake contract and the gates (slop lint, dash guard, `visual-verify`, `agent_audit`, `click_depth`, and the `ten-out-of-ten` scorecard), and `build_site.py` needs the intake files and the copy step or its reference-string guard stops the build.

## Pitfalls

- The plugin gates passing is not a 10/10: they check craft, not commerce. A build can pass slop lint, agent audit (0 fail) and click depth and still lose scorecard points for absent proof and for a heavy library loaded on first view, so run the scorecard gate and treat its failures as build work (lazy-load a heavy library on the first user action) or owner to-dos (real client names, real results), never as invented content.
- Headless Chrome `--window-size=390` renders wider than 390 and crops the screenshot, which looks exactly like horizontal overflow on a phone. Measure `document.documentElement.scrollWidth` at a 390 viewport in Playwright before calling an overflow bug; report the rendered width too, since a render wider than the requested width crops whatever it shows.
- A gate that reports a wall of identical failures is a broken checker, not a strict one. Measure the property yourself from the live DOM and cite your own number when you dismiss a checker's count, so the clean bill has evidence behind it.
- `click_depth.py` crashes on `"hub": null` groups in `page-map.json` (`g["hub"][1]` indexes a null). Null hubs are valid per the intake contract, so either list a hub per group or patch the script to `g.get("hub")`.
- The signature hero workshop can promise a scroll-scrubbed scene the site has no animation runtime for. When the refresh is meant to include scroll craft, load `scroll-journey-kit` (the LakeKit motion layer) as the sanctioned runtime and follow its checks; otherwise ship the motif as a static or CSS-only scene at every width and record the scrub version as v2 rather than pulling an arbitrary animation library in at build time.
- Source copy carries its own defects. Before rendering copy transcribed from a source document, diff it for internal contradictions: the same description printed under two different items, identical statistics for distinct items, outlier values against their neighbours. Flag the suspect text visibly in the output and report it to the owner; do not silently invent a replacement, and do not silently ship the contradiction.
- Deploy from the repo's documented command for that host (wrangler for the Cloudflare worker sites), and commit the handoff files to the site repo before deploying so the live build is reproducible from git.
- The worker serves only its configured asset directory (`assets.directory: ./public` in wrangler config), not the repo root. Copy every handoff file (`robots.txt`, `llms.txt`, `sitemap.xml`, `index.md`) into that directory, plus every asset the built `index.html` references: `dist/handoff/` omits things like `logo.png`, and a logo left out of the deploy set ships a broken image. Tell-tale that files missed the served directory: several routes answering with byte-identical bodies, because each is the not-found page.
- A deployed lead form can be a prototype. Before reporting capture as working, grep the served HTML for network calls (`fetch(`, `XMLHttpRequest`, a form `action=`) and for disclaimer or success-state strings: a handler that only flips DOM state and shows a confirmation sends nothing, and a page that renders a realistic in-browser report can still be entirely local.
- A catalog URL answering `200` is not a working funnel. Confirm the shipped script actually reads the query parameters and builds the order or sample request before calling a segment path functional; static markup routinely carries links no code consumes.
