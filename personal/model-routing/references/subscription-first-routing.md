# Subscription-first background routing

Use the existing Hermes profiles and native fallback chain. Do not build a second router service.

## Routes

Frontend and worker primary: provider `openai-codex`, model `gpt-6.1-sol`, ChatGPT subscription. Native `fallback_providers` has one entry: `openrouter-budget`, model `openrouter/auto`. Main judgment, planner and reviewer keep their separate Anthropic lanes. Do not auto-escalate repeat failures to Opus.

The `providers.openrouter-budget` definition in each executing profile must have:

- api `https://openrouter.ai/api/v1`, transport `chat_completions`, key_env `OPENROUTER_API_KEY`, catalog_provider `openrouter`.
- `extra_body.max_tokens: 4096`.
- `extra_body.provider.max_price: {prompt: 1, completion: 4}` (USD per million tokens), `require_parameters: true`.
- `extra_body.plugins: [{id: auto-router, cost_tier: low, allowed_models: [deepseek/*, z-ai/*, xiaomi/*, moonshotai/*]}]`.
- session_affinity_header `x-session-id`.

Do not buy OpenAI or Anthropic tokens again through this fallback. Do not raise the shared key credit limit without approval. Query `/api/v1/auth/key` before a paid probe. Limits belong to that key, not to a remembered dollar amount.

## Admission and quota switching

`~/.hermes/scripts/kanban_quota_guard.py --apply`, scheduled by script-only cron `f84b5393e7df` every5min, uses live `hermes usage --provider ... --json` snapshots. Reserves are25% Anthropic,15% ChatGPT,20% OpenRouter. Unknown snapshots deny admission and do not trigger paid routes.

Ordinary queued frontend/worker Sol cards switch to bounded Auto at the ChatGPT reserve, using `hermes kanban set-model`, with a routing comment and exact DB read-back. Only routes recorded as managed by this governor return to Sol when the window recovers. Preserve explicitly pinned specialist models and never touch running cards. Paid fallback on an actual runtime provider error uses Hermes's native fallback chain, not a Jev cross-provider rewrite.

Global maximum3 workers, maximum1 per profile. `dispatch_profiles` is live per claim, but numeric caps are captured at gateway boot. Governor leaves admission empty until the observed gateway boot is newer than `caps_configured_at` in `~/.hermes/state/kanban_quota.json`. A gateway restart must be run from the user's own external Terminal, after active workers finish. Do not bypass the tool's self-restart protection. The five-minute quota reserve is an admission policy, not a per-token hard budget. The existing provider key limit remains the paid hard backstop.

## Prove the real path

Read back the two executing profiles, not just the root. Run config check. Verify a real terminal tool executed through the subscription route and separately through the bounded route. Canonical profile `state.db` sessions contain model, billing_provider, billing_mode, tool_call_count and api_call_count; messages with role=tool confirm actual execution. Custom providers may be stored as billing_provider `custom`, so lookup the exact session id instead of filtering only by the configured provider name. `hermes chat` may not emit the root --usage-file artifact; do not invent it.

Run `~/.hermes/hermes-agent/venv/bin/python -m unittest -v test_kanban_decisions.py` in `~/.hermes/scripts` for quota and Jev safety tests. Obtain the actual selected paid model and usage.cost from a real OpenRouter response, never from the requested `openrouter/auto` alias. A successful text echo alone is not tool protocol proof.

Do not widen ceilings to solve a router503. A bounded Auto Code request can return `No measured models satisfy the Auto Code policy and request restrictions`. General Auto with the same family allowlist and price ceilings is a valid fallback when a real tool-call probe passes. Keep Auto Code off until it satisfies the unchanged controls. General Auto can itself return Jev decision metadata; do not add a second paid Jev call per turn just to replicate it. Hosted Jev for deciding board actions remains a separate system, fail-closed until its own credential is configured.
