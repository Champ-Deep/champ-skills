Chunked as `references/` and `scripts/` files. Load only what the current task needs.

Chunk index:
- `references/connector-preflight.md` — Locate generation and meeting tools by capability, and decide preflight before intake.
- `references/creative-generation.md` — Model choice, low-resolution-first video, cost preflight, reference media, brand accuracy, concurrency, motion QA.
- `references/provocation-patterns.md` — The provocation structure, patterns that work, and the failure modes that deflate it.

Script: `scripts/build_creative_deck.py` builds the visual HTML version of the playbook.

Rules of use: pick the chunks named by the task, load them with
`skill_view(name, file_path=...)`, and ignore the rest. Do not load the whole
set at once.