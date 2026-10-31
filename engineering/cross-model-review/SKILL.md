---
name: cross-model-review
description: Use when a medium or large change needs a second-model review.
---

# Cross-model review

Adapted from David Ondrej's `gpt-review` and `total-review` (davidondrej/skills, MIT), rebuilt for our lanes. The idea: a model reviewing its own family's work shares its blind spots, so one read by a different lab's frontier model removes most serious misses. Claude still adjudicates. Routing rule "do not delegate review" stands: the other model is a second reader, never the reviewer of record.

## When
- Medium, large or risky change (auth, billing, data, send paths, migrations). Skip tiny fixes.
- Run it ONCE per change. Repeating it invents findings because the reviewer was told to find bugs. A second pass is allowed only after a large fix list.
- `total-review` (every lab) is for huge risky changes only, a few times a week at most.

## How
1. Make a `frontend` profile kanban card pinned to `model="gpt-6-astra", provider="openai-codex"` (the exception in `model-routing`; it burns the ChatGPT window, so mediums can use the default Sol). Read-only: the brief says "review only, do not change files".
2. Brief is neutral: scope, paths, base revision, intended behavior. Do not name suspected bugs or a verdict. Ask for serious or critical issues, fixes, merge readiness, and verified versus uncertain findings.
3. Include this sentence word for word: "During your final answer, rate each issue from 1 to 10 on how often it would happen, and 1 to 10 on how bad it would be."
4. When it returns, ask yourself for each finding: must fix, or overthinking? Fix frequent and serious items. Skip rare and mild ones. Do not rerun the reviewer to confirm fixes unless the change touches money or customers.
5. If the card cannot run (key capped, lane blocked), say so. Never present partial output as a finished review.

## Not for
Outside PRs on public repos: be skeptical that the issue is real and not an LLM-invented edge case. Ask whether a user actually hit it.
