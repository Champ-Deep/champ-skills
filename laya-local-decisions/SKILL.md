---
name: laya-local-decisions
description: Use when routing or scoring text with a local model.
---

# Laya local decisions

Laya (convaiinnovations/laya, 0.4B ModernBERT) answers typed questions about a text state with calibrated probabilities. It never generates text. Weights are in the HF cache; no API key.

## Run

```bash
echo '{"state": "<text or JSON>", "questions": {"q": {"type": "choice", "instructions": "...", "criteria": {"a": "...", "b": "..."}}}}' | ~/.hermes/scripts/laya_decide.py
```

Question types: `choice` (criteria is a dict), `score` (criteria is an ordered list), `noul` (yes/no). Output has `choice`/`score`/`noul`, `confidence`, `probabilities`. Each CLI call reloads the model (about 20s first, then cached by the OS).

## Rules

- English text only, 512 tokens per question; longer states are truncated, so summarise first.
- Triage and routing only: intent, urgency, phishing, tone, department. Keep arithmetic, dates and counting in code.
- It is not a judge of strategy: a vendor penalty-waiver test returned accept at 0.91. Escalate to the human below about 0.85 confidence and spot-check on Deep's own data before automating anything.
- Env lives at ~/repos/laya-local/.venv (uv, python 3.12). Rebuild: `uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python laya`.
- Clef-Flash (Cloudflare, 9B) scores higher but bf16 weights are about 18GB and its reference code targets CUDA; not run on this Mac.
