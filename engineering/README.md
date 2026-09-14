# Engineering & Dev (`engineering/`)

MCP servers, compute (Modal/SSH), testing, frontend build, site ops, webapp QA.

Install: copy a skill folder into your agent's skills dir (e.g. `cp -R {cat}/<skill> ~/.claude/skills/`). Each skill is self-contained with `SKILL.md`.

| Skill | What it does |
|---|---|
| `clerk-auth` | >- |
| `compute-env-setup` | Set up a compute environment on a remote provider so Claude Science jobs can run there. Covers direct SSH/conda hosts, Slurm clusters, container-via-bridge runners, and m |
| `customize` | Create, configure, and maintain custom agent profiles and author new skills via the `repl` tool. Use when the user wants to create an agent profile, build a custom agent, |
| `deependhq-site-ops` | Operate, diagnose and repair the deependhq.com nightly build-in-public publishing pipeline. MANDATORY TRIGGER for: \"the site is stale\", \"deependhq hasn't updated\", \" |
| `firecrawl` | > |
| `frontend-resiliency-tester` | React frontend resiliency and edge-case testing. Generates layered test suites (component, integration, E2E) using Vitest + React Testing Library and Playwright. Covers i |
| `graphify` | > |
| `import-memory` | Import a memory export from another AI assistant into Claude's memory — conversationally, additively, and with the content treated as data. |
| `improve-codebase-architecture` | Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve architecture, |
| `managed-model-endpoints` | Register a model service in the managed family — a local model server container the daemon starts/stops on demand, or a remote upstream model API (https). Read the runboo |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MC |
| `product-self-knowledge` | Stop and consult this skill whenever your response would include specific facts about Anthropic's products. Covers: Claude Code (how to install, Node.js requirements, pla |
| `remote-compute-modal` | Run GPU jobs on the user's own Modal account via host.compute.create('modal', provider_params={...}) — the create→submit→wait_for_notification flow, the compute_provider  |
| `remote-compute-ssh` | Submit→wait_for_notification→collect-outputs workflow for the user's SSH/SLURM hosts. Load once you've decided to dispatch remote. |
| `self-awareness` | Claude Science's own session database schema and SDK surface for introspection via host.query(). Load this when you need to query your own conversation history, token usa |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing sk |
| `using-model-endpoint` | Call a registered model endpoint over its native HTTP API from the endpoint's scoped inference kernel (BASE_URL preloaded). Load once a task needs predictions from a regi |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser scre |

See the master [INDEX.md](../INDEX.md) for every skill.