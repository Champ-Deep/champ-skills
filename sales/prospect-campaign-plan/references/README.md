Chunked as `references/` files. Load only what the current task needs.

Chunk index:
- `references/content-framework.md` — Patterns for the strategy, email and LinkedIn sections: persona cards, hypotheses, channel selection logic.
- `references/html-structure.md` — The CSS scaffold and component patterns for the plan document. Copy and adapt, do not reproduce verbatim.

Rules of use: pick the chunks named by the task, load them with
`skill_view(name, file_path=...)`, and ignore the rest. Do not load the whole
set at once.