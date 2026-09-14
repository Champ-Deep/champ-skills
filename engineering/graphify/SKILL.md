---
name: graphify
description: >
  Transforms any directory of files — code, docs, PDFs, images, diagrams — into an interactive knowledge graph. Use this skill whenever the user wants to understand a codebase, map relationships between files or concepts, generate a visual graph, build an Obsidian-ready knowledge vault from source files, discover surprising connections in a project, analyze architecture, or asks about graphify, knowledge graphs, or repo exploration. MANDATORY TRIGGER for: "graphify this", "build a knowledge graph", "map this codebase", "what's connected to X", "explore this repo", "graph this folder", "show me the structure", "understand my codebase", "analyze repo relationships", "export to Obsidian from code", "who calls what", "find dependencies", or any request involving graph-based code or document analysis. Also trigger when the user pastes a path and asks "what's in here" or "map this out". Do NOT skip this skill just because the user didn't say the word "graphify" — the intent to understand structure is the cue.
---

# Graphify

Graphify turns unstructured files into queryable knowledge graphs. It reads code, documents, PDFs, and images, extracts concepts and relationships, and gives you back structure you didn't know was there — as an interactive HTML graph, an Obsidian vault, a wiki, JSON, SVG, GraphML, or a Neo4j-ready Cypher dump.

**Install once (if not already installed):**
```bash
pip install graphifyy && graphify install
```

Then invoke from any Claude Code session as `/graphify <path>`.

---

## When to Use Which Mode

Choose the right entry point before running:

| Goal | Command |
|------|---------|
| Quick map of current directory | `/graphify .` |
| Deep relationship extraction | `/graphify ./path --mode deep` |
| Only reprocess changed files | `/graphify ./path --update` |
| Auto-sync as files change | `/graphify --watch` |
| Agent-navigable wiki output | `/graphify --wiki` |
| No visualization (fast, data only) | `/graphify ./path --no-viz` |
| Export to GraphML (Gephi/yEd) | `/graphify ./path --graphml` |

After the graph is built, query it:
```bash
graphify query "what does the auth module depend on?"
graphify path "UserService" "Database"   # shortest connection path
```

---

## Pipeline Overview

Understanding the stages helps you interpret results and diagnose issues:

```
detect() → extract() → build_graph() → cluster() → analyze() → report() → export()
```

Each stage is stateless and passes plain dicts / NetworkX graphs forward. If a stage fails, it usually means an unsupported file type or a missing dependency (tree-sitter, pdfminer, etc.).

**Confidence tagging on every edge:**
- `EXTRACTED` — explicit relationship found in source
- `INFERRED` — reasonable deduction from context
- `AMBIGUOUS` — uncertain, flagged for review

Always check the `AMBIGUOUS` edges before trusting architectural conclusions. They're there for a reason.

---

## Supported File Types

| Category | Formats |
|----------|---------|
| Code (AST via tree-sitter) | Python, TypeScript, JavaScript, Go, Rust, Java, C/C++, Ruby, C#, Kotlin, Scala, PHP |
| Documentation | Markdown, plain text, reStructuredText |
| PDFs | Academic papers, reports (with citation + concept extraction) |
| Images | Screenshots, diagrams, multilingual content (via Claude vision) |

---

## Output Artifacts

After a successful run, Graphify produces:

1. **Interactive HTML graph** — click nodes, search, explore relationships in browser
2. **Obsidian vault** — drop the output folder into your vault and the graph becomes navigable wikilinks
3. **Wikipedia-style wiki** — `--wiki` flag; good for agent navigation and internal docs
4. **JSON graph** — persistent, queryable via `graphify query`
5. **SVG** — static export for embedding in docs
6. **GraphML** — import into Gephi or yEd for advanced layouts
7. **Cypher** — Neo4j-ready for enterprise graph databases
8. **Analysis report** — "god nodes" (highest-degree concepts), surprising connections, and suggested questions

---

## Key Concepts to Surface to the User

After a run, always highlight:

- **God nodes** — concepts with the most connections. These are the architectural load-bearers. If one breaks, many things break.
- **Surprising connections** — relationships the graph found that cross module/domain boundaries. Often the most interesting insight.
- **Suggested questions** — the report auto-generates questions the graph can answer. Share these with the user as next steps.
- **Token efficiency** — for larger corpora, querying the graph is dramatically cheaper than reading raw files. Remind the user to use `graphify query` instead of re-analyzing files.

---

## MCP Server (for persistent querying)

Graphify ships an MCP server that exposes the graph as tools. Once registered, these operations are available inside Claude:

| Tool | Purpose |
|------|---------|
| `query_graph` | Natural language search across nodes/edges |
| `get_node` | Fetch a specific node and its relationships |
| `shortest_path` | Find the connection path between two concepts |

The MCP server starts automatically after `graphify install`. If it's not responding, check that it was registered: run `graphify install` again.

---

## Obsidian Integration (Celsus-Specific Note)

When the user wants to bring Graphify output into the Celsus vault:

1. Run with `--wiki` to generate wikilink-compatible output
2. Copy the output folder into `Atlas/` or a new subfolder (e.g., `Atlas/GraphifiedRepos/project-name/`)
3. The generated notes will use `[[wikilinks]]` and will connect to the existing graph
4. Keep per the vault lean policy: no raw codebases, summaries and graph exports only

---

## Installation Troubleshooting

**`graphify: command not found` after pip install**
```bash
# Make sure the pip bin directory is on your PATH
export PATH="$HOME/.local/bin:$PATH"
# Or use pipx for isolated installs
pipx install graphifyy
```

**tree-sitter parse errors on code files**
The tree-sitter grammars are compiled on first use. If you see grammar errors, run:
```bash
pip install graphifyy[grammars]
```

**PDF extraction fails**
```bash
pip install graphifyy[pdf]
```

**MCP server not found in Claude Code**
```bash
graphify install   # re-registers the MCP server
# Restart Claude Code after running
```

---

## Quick Workflow

1. `cd` into the project directory (or note the path)
2. Run `/graphify .` for a baseline map
3. Open the HTML output — share the link or embed the file
4. Review the analysis report for god nodes and surprises
5. If the user wants Obsidian integration, use `--wiki` and copy to vault
6. For follow-up questions, use `graphify query` — cheaper than re-running
7. If files have changed, use `--update` to reprocess only deltas (SHA256 cache)

---

## Verify before delivery — MANDATORY

This output is visual, so reading the source does not tell you whether it worked. Render it and look at it.

```bash
python3 visual-verify/scripts/audit.py <output.html> --width 390
python3 visual-verify/scripts/audit.py <output.html> --width 1440
python3 visual-verify/scripts/shoot.py <output.html> --widths 390,1440 --themes light
```

Then **open every screenshot with the Read tool** and critique it. Not the file listing, the images. A screenshot you did not look at has verified nothing.

The four things this catches that nothing else does:

1. **Contrast measured against the composited background**, including transparency stacking, rather than against the hex you intended.
2. **Horizontal overflow at 390px**, with the offending element named.
3. **Content that overflows its container** once real text length replaced the sample.
4. **Flat hierarchy** — three elements competing where one should dominate. Only the eye finds this.

Zero FAILs before delivery. Every WARN either fixed or justified in one line. If no browser is available, say so and label the output **unverified**, listing what was not checked.

→ Full protocol: the `visual-verify` skill.
