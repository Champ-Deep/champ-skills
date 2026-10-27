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
