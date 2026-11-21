# Auxiliary and subscription audit procedure

Use when Deep asks to re-audit auxiliary models, cut OpenRouter spend, or move work onto subscriptions. Read-only until he approves changes.

1. Attribute spend before choosing models. Every profile has its own `state.db`; `session_model_usage` has a `task` column (vision, background_review, compression, approval, title_generation...) plus `billing_provider`. Query the default DB and `profiles/*/state.db` over 7 days. OpenRouter rows store cost 0, so price them from the live catalog (`/api/v1/models`, per million tokens) times logged tokens, then check the sum against `usage_weekly` from `/api/v1/auth/key`. Within 5 percent means the attribution is usable.
2. Do not assume auxiliary jobs are the spend. A profile's main model and delegation children can dwarf them (one week: inbox main 58 percent, delegation 18 percent, true auxiliary 17 percent).
3. Separate real aux lanes from dead config: `hermes_cli/config_defaults.py` says which blocks no longer call a model (web_extract and session_search in 0.22.5). Unset blocks inherit the main model.
4. Read pool headroom live: `hermes usage`, `hermes usage --provider openai-codex`, `~/.local/bin/agy -p /usage --output-format json`. Percentages cannot be converted to tokens; measure a slice before moving volume.
5. Probe each candidate with `hermes -z "Reply with exactly: ROUTE_OK" --provider P -m M --usage-file F`. It proves routing only (the run boots the full agent, so wall time is not aux latency). Quality, JSON and tool-call behaviour need a bank of real inputs scored blind.
6. Check which profiles carry the Antigravity plugin before pinning it. The inbox profile does not.
7. Vision on the local Antigravity proxy (`custom` provider, 127.0.0.1:3187) is the existing no-key route; other profiles on OpenRouter vision go blind when the key caps.
8. Advanced Delegation (official plugin, core 0.22.5 or newer) gives named `model_map` routes for `delegate_task`; use `provider:` never `api_key:` (plain text in config).
9. Report cost as an estimate from list prices, state what was not measured, and stage the decision as a card.
