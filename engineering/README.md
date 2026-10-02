# Engineering & Dev (`engineering/`)

MCP servers, compute (Modal/SSH), testing, frontend build, site ops, webapp QA.

Install: copy a skill folder into your agent's skills dir (e.g. `cp -R {cat}/<skill> ~/.claude/skills/`). Each skill is self-contained with `SKILL.md`.

| Skill | What it does |
|---|---|
| `clerk-auth` | Add Clerk authentication (sign-in, sign-up, user accounts, protected routes) to any web project. Use this skill whenever the user wants to add auth, add login, add sign-i |
| `defensible-data-counts` | Use when a detected or derived number is shown to a buyer. |
| `firecrawl` | Firecrawl is the PRIMARY browser and web access tool for this workspace. Use it for any web interaction, reading, research, or scraping task BEFORE reaching for the Chrom |
| `frontend-resiliency-tester` | React frontend resiliency and edge-case testing. Generates layered test suites (component, integration, E2E) using Vitest + React Testing Library and Playwright. Covers i |
| `graphify` | Transforms any directory of files, code, docs, PDFs, images, diagrams, into an interactive knowledge graph. Use this skill whenever the user wants to understand a codebas |
| `improve-codebase-architecture` | Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve architecture, |
| `jev-typesafe-integration` | Use when working with Jev or TypeSafe in ChampSet. |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MC |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing sk |
| `sqlite-fts5-search-platform` | Use when building faceted search over merged spreadsheets or any row store on SQLite, especially with full-text search, evidence-bearing detections, or many normalised en |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser scre |

See the master [INDEX.md](../INDEX.md) for every skill.