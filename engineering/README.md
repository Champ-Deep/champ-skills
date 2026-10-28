# Engineering & Dev (`engineering/`)

MCP servers, compute (Modal/SSH), testing, frontend build, site ops, webapp QA.

Install: copy a skill folder into your agent's skills dir (e.g. `cp -R {cat}/<skill> ~/.claude/skills/`). Each skill is self-contained with `SKILL.md`.

| Skill | What it does |
|---|---|
| `agent-first-products` | Use when building a standalone agent-first product or suite. |
| `android-twa-packaging` | Package a web app or PWA into an installable Android APK. |
| `clerk-auth` | Add Clerk authentication (sign-in, sign-up, user accounts, protected routes) to any web project. Use this skill whenever the user wants to add auth, add login, add sign-i |
| `cloudflare-workers-r2-apps` | Use when building a Cloudflare Worker with R2 or KV. |
| `defensible-data-counts` | Use when a detected or derived number is shown to a buyer. |
| `deterministic-analysis-pipelines` | Use when a site-wide analysis must run on many inputs. |
| `dograh-champvoice-provider` | Use when maintaining the Dograh Champvoice provider. |
| `factory-decision-gate` | Use when a factory agent is about to act without Deep. |
| `firecrawl` | Firecrawl is the PRIMARY browser and web access tool for this workspace. Use it for any web interaction, reading, research, or scraping task BEFORE reaching for the Chrom |
| `frontend-resiliency-tester` | React frontend resiliency and edge-case testing. Generates layered test suites (component, integration, E2E) using Vitest + React Testing Library and Playwright. Covers i |
| `graphify` | Transforms any directory of files, code, docs, PDFs, images, diagrams, into an interactive knowledge graph. Use this skill whenever the user wants to understand a codebas |
| `guarantee-audit` | Use when auditing healthy-looking code before a merge. |
| `human-feedback-learning-loop` | Use when a system learns from human corrections. |
| `improve-codebase-architecture` | Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve architecture, |
| `interactive-data-app-verification` | Verify interactive HTML data apps by measuring the DOM. |
| `jev-typesafe-integration` | Use when working with Jev or TypeSafe in ChampSet. |
| `link-graph-visualization` | Visualize crawled site and link data as a readable graph. |
| `live-server-browser-gates` | Use when a browser test drives a real server. |
| `llm-model-benchmarking` | Use when assessing a model on Deep's LLM bake-off suite. |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MC |
| `optional-input-degradation` | Use when an optional or external input can be absent. |
| `permissioned-send-lane` | Use when adding an outbound send path to a read-only system. |
| `rea-web-teardown` | Use when tearing down a web product with the REA CLI. |
| `repo-design-probe-first` | Use when designing a repo feature from real file:line proof. |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing sk |
| `sprite-art-pipeline` | Build layered sprite art and prove every spec renders. |
| `sqlite-fts5-search-platform` | Use when building faceted search over merged spreadsheets or any row store on SQLite, especially with full-text search, evidence-bearing detections, or many normalised en |
| `state-open-data-harvest` | Use when pulling US state open-data portals into a DB. |
| `upstream-model-integration` | Use before adopting or self-hosting an upstream model. |
| `verification-gate-integrity` | Use before reporting any test, gate or audit as passing. |
| `verifying-supplied-plans` | Use when someone hands you a plan or audit to build. |
| `visitor-tracking-and-proactive-engagement` | Use when a site acts on inferred visitor intent. |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser scre |

See the master [INDEX.md](../INDEX.md) for every skill.