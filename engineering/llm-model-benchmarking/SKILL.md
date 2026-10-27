---
name: llm-model-benchmarking
description: "Use when assessing a model on Deep's LLM bake-off suite."
version: 1.0.0
author: Deep / Hermes
license: MIT
metadata:
  hermes:
    tags: [benchmark, eval, llm, openrouter, claude-code]
    related_skills: [model-routing, model-api-capability-verification, verification-gate-integrity]
---

# LLM model benchmarking

Class of work: build task banks with deterministic checkers, calibrate them, wire a model into the harness, run the bank, report tier verdicts.

## When to Use

Fire whenever Deep asks to score, compare, or assess an LLM against his task suite, mentions the "LLM Bake-off" or "benchmark", wants a new task added to a bank, needs a checker calibrated, or asks how a model is wired into the harness. Also fire when a run's verdict, cost, or PASS/FAIL report is being prepared.

## Suite location

`/Users/deep/Celsus/Efforts/LLM Bake-off/suite`

- `docs.md` and `run.py`: read both first. `run.py` defines the Task shape, scoring, selftest, and report format.
- `tasks.py`: the intern bank. `deep_tasks.py`: Deep's personal bank, run with `--bank deep_tasks`.
- `models.json`: driver command and price per 1M tokens `[in, out]`. Drivers live here, not in prose.
- `results/`: one directory per run.

## The bank models the work of the person it is for

When Deep asks to assess a model "for the suite of tasks", the suite that matters is the bank modelling his own daily work: vendor and meeting email, notes to task ingest, cold personalization under verified-fact rules, source-only research, decision briefs, ABM plans, issue triage, PR review, bug fixes, feature recreation with hidden tests, long-context decision logs, NDA review, appraisals. The intern bank answers a different question about a different person. When it is ambiguous which bank is meant, say which one you are about to run and why in one line, then proceed.

## Procedure

1. Read `docs.md` and `run.py` before writing tasks. The Task shape: prompt, fixtures dict, checker returning a list of `(name, bool)`, a good sample, a bad sample, a tier. Follow it exactly; `run.py` is the contract.
2. Ground fixtures in real vault material (actual NDA clauses, the social-voice rules, real decision formats) so the checks test what Deep's work actually demands. Client names stay fictional-but-plausible; check `_config/link-policy.md` before any wikilink.
3. Calibrate every task with `--bank <bank> --selftest` before any model run: good must score 1.00 and bad must score at or below the discrimination threshold (0.50 in current banks). A bad sample above the threshold means the checker is not discriminating: strengthen the bad sample or tighten the checks until it does.
4. Wire the driver per `references/model-drivers.md`, then smoke test ONE task through the full harness before the full run. A lane that answers a prompt has not proven it can edit files and run tests.
5. Run the full bank in the background. Report tier verdicts, PASS/FAIL per task, and cost with explicit units from the `models.json` price. Reports follow house rules: no em dashes, no en dashes.

## Pitfalls

- Exempt the numbers the task itself demands from any "no invented numbers" check. A confidence score the prompt requires is not an invented number, and a checker that fails its own good sample is broken, not strict.
- When a check passes standalone but fails inside `score()`, diff the actual bytes of the written file before re-deriving the logic. Layered writes can double-escape backslashes in regex literals, so the harness runs a different pattern than the one you tested.
- Expected values you wrote into the prompt (reference implementations, hidden test expectations) can be wrong. Verify each by independent calculation before blaming a model for missing it.
- An Anthropic-compatible endpoint returns thinking blocks alongside text. When `content` comes back empty on HTTP 200, read the raw body before concluding anything.

## References

- `references/model-drivers.md`: verified wrapper recipe for driving any OpenRouter model through Claude Code headless, plus lane checks before a full run.