---
name: laya-local-decisions
description: Use when routing or scoring text with a local model.
---

# Laya local decisions

Laya (convaiinnovations/laya, 0.4B ModernBERT) answers typed questions about a text state with calibrated probabilities. It never generates text. Weights are in the HF cache; no API key.

## Run

```bash
cd /Users/deep/laya-local/decider && ../.venv/bin/python decider.py ask "<situation>" [--shadow]   # gate verdict, optional Clef-flash shadow (~7 s warm)
# Arbitrary typed questions (choice/score/noul, Jev shape): mcp_clef_ask via the `clef` MCP server, or decider/mcp_server.py directly.
```

Question types: `choice` (criteria is a dict), `score` (criteria is an ordered list), `noul` (yes/no). Output has `choice`/`score`/`noul`, `confidence`, `probabilities`. Each CLI call reloads the model (about 20s first, then cached by the OS).

## Rules

- English text only, 512 tokens per question; longer states are truncated, so summarise first.
- Triage and routing only: intent, urgency, phishing, tone, department. Keep arithmetic, dates and counting in code.
- It is not a judge of strategy: a vendor penalty-waiver test returned accept at 0.91. Escalate to the human below about 0.85 confidence and spot-check on Deep's own data before automating anything.
- Env lives at ~/repos/laya-local/.venv (uv, python 3.12). Rebuild: `uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python laya`.
- Clef-flash (Cloudflare, 9B, Apache 2.0) is the decision model of record since 2026-10-18 and runs on MPS from `/Users/deep/laya-local/.venv` (19 GB in the HF cache, ~7 s per call). Deep's decision gate is `/Users/deep/laya-local/decider/decider.py ask "<situation>" [--shadow]`: rules plus vault precedents decide, Clef answers in shadow only. `desk_eval.py --clef` scores both against the Decision Desk cards.
- Inside Hermes it is the stdio MCP server `clef` (`decider/mcp_server.py`, tools `mcp_clef_decide`, `mcp_clef_ask`, `mcp_clef_label`; per-call timeout 300 s for the 75 s cold load; the model unloads after 15 min idle to give 18 GB RAM back). Self-check: `env -u PYTHONPATH -u PYTHONHOME ../.venv/bin/python test_mcp_server.py --clef`. Any python run from that venv in a Hermes terminal needs `env -u PYTHONPATH -u PYTHONHOME` or Hermes's 3.14 site-packages leak in (pydantic_core errors, httpx2 timeouts). `noul` answers come back as `{"noul": p}`, not `probability`.
- Re-downloading Clef: `HF_HUB_DISABLE_XET=1` or the fetch crawls at 300 KB/s on this link (8 MB/s without Xet). Fine-tuning Clef locally is not possible (no training code shipped, 9B bf16 does not train on 32 GB MPS); the model learns the vault through the precedents retrieved into the state, not through weights.

## Training the gate from the swipe decision log

The swipe triage app (`~/.hermes/scripts/swipe_triage.py`) appends every ruling to `~/.hermes/state/decision_log.jsonl` (id, kind, choice, answer, section, ts). That log trains the gate, not Clef's weights:

```bash
cd /Users/deep/laya-local/decider && ../.venv/bin/python decider.py backfill   # seed the log from card history when thin
../.venv/bin/python decider.py label   # add a labelled ruling
../.venv/bin/python decider.py tune    # fit gate weights on the log
../.venv/bin/python decider.py eval --limit 60   # score against the current baseline
```

Ship a tune only when held-out accuracy beats the baseline; a regression keeps the old weights. Verify the eval's row count in its output (not exit 0 alone) before comparing numbers, and disable reasoning on any bulk API pass that prepares labels, or the output budget is eaten by hidden thinking.

## Confidence on each swipe card (`~/.hermes/scripts/celsus_jev.py`)

The gate above answers "should we act at all"; per-card confidence answers "which of these decisions is cheap for Deep". Both run after `celsus_compose.py` has composed the pile:

```bash
cd ~/.hermes/scripts && /Users/deep/laya-local/.venv/bin/python celsus_jev.py score --max 500   # writes ~/.hermes/state/celsus_jev.json
curl -s localhost:3177/api/cards | python3 -c "import sys,json,collections as c;d=json.load(sys.stdin);print(c.Counter(round(x['confidence'],1) for x in d if x['confidence']))"
```

Rules that keep the score honest:
- **Name the scorer.** There is no hosted-Jev credential on this Mac, so a confidence number always says which local scorer produced it; never present it as a hosted model's output.
- **The auto-execute gate is a separate boolean.** `auto_allowed` is true only when the calibration bucket at the gate confidence holds enough of Deep's own picks and precision holds; with zero labelled rows it stays false regardless of how many cards score above 0.95. Report the bucket histogram, not an average, and never report "N cards above 0.99" without checking `auto_allowed` in the same breath.
- **Only Deep's picks count as labels.** Rows whose provenance is an agent's evidence comment are not calibration data; counting them makes a gate look earned when it is not.
- **First-listed options win by construction**, because the composer puts the recommended option first. Expect and disclose that bias instead of reading it as accuracy.
