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

Fire whenever Deep asks to score, compare, or assess an LLM against his task suite, mentions the "LLM Bake-off" or "benchmark", wants a new task added to a bank, needs a checker calibrated, or asks how a model is wired into the harness. Also fire when a run's verdict, cost, or PASS/FAIL report is being prepared, and when Deep asks which model a lane should run on: "cheaper" is half the question, the other half is this suite's tier verdict for that model.

## Suite location

`/Users/deep/Celsus/Efforts/LLM Bake-off/suite`

- `docs.md` and `run.py`: read both first. `run.py` defines the Task shape, scoring, selftest, and report format.
- `tasks.py`: the intern bank. `deep_tasks.py`: Deep's personal bank, run with `--bank deep_tasks`.
- `models.json`: driver command and price per 1M tokens `[in, out]`. Drivers live here, not in prose.
- `results/`: one directory per run.

## The bank models the work of the person it is for

When Deep asks to assess a model "for the suite of tasks", the suite that matters is the bank modelling his own daily work: vendor and meeting email, notes to task ingest, cold personalization under verified-fact rules, source-only research, decision briefs, ABM plans, issue triage, PR review, bug fixes, feature recreation with hidden tests, long-context decision logs, NDA review, appraisals. The intern bank answers a different question about a different person. When it is ambiguous which bank is meant, say which one you are about to run and why in one line, then proceed.

## Eval sequence v2 is the procedure of record

`/Users/deep/Celsus/Efforts/LLM Bake-off/EVAL-SEQUENCE.md` (stages 0 to 9). Run `python3 test_run.py`, `run.py --bank v2_tasks --selftest` and `judge.py --selftest` before any comparison. Candidates k=3, frontier references k=1, parallel processes share `--root`.

Verdict shape: judge on the tier table, never on an overall mean, because one failed tier hides inside a high average. `Efficient pick per tier` means pass on every run first, then price, then speed: a model that fails a tier once in three runs is disqualified from that tier regardless of its mean. Report basic (tiers 1 to 2) and major (tiers 3 to 4) cost separately, since heavy work skews spend toward output tokens while routine work skews input. State repeats beside every score, because a reference run once and a candidate run three times are different evidence. A hosted model at full precision is a stand-in for the local quantised build only; state that gap rather than transferring its score to the 4-bit file.

## Build the candidate list from your own research

Deep's standing correction (2026-10-31): a tool's recommendation is one input, never the shortlist. Hermes's local catalog recommended Qwen3.6 35B-A3B while NVIDIA's Nemotron 3.5 Bolt sat in the same catalog unrecommended; Deep expected both found and tested. Shortlist from at least three independent sources (vendor card, independent leaderboard or review, hands-on report), and write down why each excluded model was excluded.

## Procedure

1. Read `docs.md` and `run.py` before writing tasks. The Task shape: prompt, fixtures dict, checker returning a list of `(name, bool)`, a good sample, a bad sample, a tier. Follow it exactly; `run.py` is the contract.
2. Ground fixtures in real vault material (actual NDA clauses, the social-voice rules, real decision formats) so the checks test what Deep's work actually demands. Client names stay fictional-but-plausible; check `_config/link-policy.md` before any wikilink.
3. Calibrate every task with `--bank <bank> --selftest` before any model run: good must score 1.00 and bad must score at or below the discrimination threshold (0.50 in current banks). A bad sample above the threshold means the checker is not discriminating: strengthen the bad sample or tighten the checks until it does. A good sample below 1.00 means the checks reject the answer they were written to accept, which makes every model look worse than it is; fix the checker before running anyone. Also confirm the harness can express a genuine failure: a checker with no `good` sample that would score below 1.00 reports everything as a pass and makes a model look flawless on a task it never handled.
4. Wire the driver per `references/model-drivers.md`, then smoke test ONE task through the full harness before the full run. A lane that answers a prompt has not proven it can edit files and run tests, and a lane that answered has not proven it ran the model you named: read `_usage.json` on the smoke run and compare the model id that came back to the row's key. A driver that drops the auth header still gets HTTP 200, answered by the proxy's own fallback model, which is how a free request comes back as somebody else's model.
5. Run the full bank in the background with `--repeats 3` for candidates and 1 for frontier references, sharing one `--root`. Report tier verdicts, PASS/FAIL per task, and cost with explicit units from the `models.json` price. Reports follow house rules: no em dashes, no en dashes. State each model's rows and repeats alongside its numbers: a frontier reference run once and a candidate run three times are not the same evidence, and a table that shows means without run counts invites a comparison the data cannot support.

## Pitfalls

- A run can come back clean from the wrong model: Hermes falls back to another provider on a 429/403, and a `:free` OpenRouter route whose driver dropped the auth header is answered by the proxy's own model with HTTP 200. Never score a row without comparing `_usage.json` model to the row's key (`run.py` marks a mismatch ERR), on every row's first run rather than once per setup; mechanism in `references/model-drivers.md`.
- The default Hermes profile makes models append notes to Deep ("Not covered: ...", word counts, decision cards). Checkers that count words or numbers then penalise the model for obeying house rules. Score only the text between `<answer>` tags (`run.deliverable`); the v1 footer did not ask for tags.
- Judge on the tier table, never on one overall mean: one failed tier hides inside a high average, and the efficient pick per tier means pass on every run first, then cheapest list price, then fastest. State repeats beside every score (a reference run once and a candidate run three times are different evidence), split basic (tiers 1 to 2) from major (tiers 3 to 4) cost, and mark a hosted full-precision score as a stand-in for the 4-bit file you would actually load.
- A cheap model that passes routine tiers and fails the heavy ones is not a global swap: route by tier, keeping the failing tier on the subscription model. An overall mean hides exactly the split that decides the routing, so report the tier table first and the average second.
- Judge scoring against a stale judge run silently mixes two judges. When the judge changes (a selftest fix, a prompt or rubric edit), re-score every row into a fresh `--root` and compare roots, never old rows against new ones; a table spanning two judge versions is two measurements presented as one.
- Memory pressure contaminates a measurement: with swap nearly full, a local load measures thrashing instead of the model's speed, and the disk it borrows for swap can be the disk the download just filled. Gate any local load on free memory first (`open-model-runnability-probes`).
- A shared OpenRouter key at its weekly cap still serves `:free` endpoints, but free upstreams rate-limit and may log prompts: proxy signal only, fictional fixtures only.
- Exempt the numbers the task itself demands from any "no invented numbers" check. A confidence score the prompt requires is not an invented number, and a checker that fails its own good sample is broken, not strict.
- When a check passes standalone but fails inside `score()`, diff the actual bytes of the written file before re-deriving the logic. Layered writes can double-escape backslashes in regex literals, so the harness runs a different pattern than the one you tested.
- Expected values you wrote into the prompt (reference implementations, hidden test expectations) can be wrong. Verify each by independent calculation before blaming a model for missing it.
- A task whose checker only rewards the good sample and never flags the bad one reports every model as 1.00; the pass column then measures nothing. Run `--selftest` and confirm the bad sample scores at or below the threshold before trusting any row.
- An Anthropic-compatible endpoint returns thinking blocks alongside text. When `content` comes back empty on HTTP 200, read the raw body before concluding anything.

## References

- `references/model-drivers.md`: verified wrapper recipe for driving any OpenRouter model through Claude Code headless, lane checks before a full run, and the auth check that proves which model actually answered.