Chunked as `references/` files. Load only what the current task needs.

Chunk index:
- `references/pitch-frameworks.md` — The two pitch frameworks, with annotated cold, follow-up and breakup touches plus subject-line rules.
- `references/service-catalogue.md` — Service definitions and the signal-to-service mapping used to pick the 2 to 3 pitch options.
- `references/persona-matrix.md` — Tone, word-count and CTA rules by title tier, with industry vertical modifiers layered on top.
- `references/cold-email-benchmarks.md` — Evidence behind the word-count, subject-length, send-window, follow-up and reply-rate rules.

Rules of use: pick the chunks named by the task, load them with
`skill_view(name, file_path=...)`, and ignore the rest. Do not load the whole
set at once.