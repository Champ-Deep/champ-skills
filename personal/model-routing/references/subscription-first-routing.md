# Subscription-first background routing

Use the existing Hermes profiles and native fallback chain. Do not build a second router service.

## Routes

Four pools, all read live every 5 minutes: Anthropic direct (`hermes usage`), ChatGPT (`hermes usage --provider openai-codex`), Antigravity (`agy -p /usage --output-format json`, three buckets: Gemini, Claude and GPT, Argon), shared OpenRouter key (paid). Reserves: Anthropic 25%, ChatGPT 15%, Antigravity buckets 20%, OpenRouter 20%. Unknown quota is treated as empty.

Tiers, decided by card priority when no human pin exists (Deep, 2026-11-07):

| Tier | Priority | Model | Pool |
|---|---|---|---|
| Hardest | 90+ | Claude Opus 5.5 | whichever of Anthropic direct or Antigravity Claude has more headroom; both at reserve: pin Anthropic and wait, never downgrade |
| Important | 75 to 89 | Claude Sonnet 5.5 | same |
| Routine | below 75 | GPT-6.1 Sol on ChatGPT | at the ChatGPT reserve: Antigravity Gemini (Argon for frontend when its bucket allows, Flash otherwise); only when that is also at reserve: bounded paid OpenRouter Auto |

Antigravity model ids carry an effort suffix: `claude-opus-5-5-medium`, `claude-sonnet-5-5-medium`, `gemini-4-argon-medium`, `gemini-3.8-flash-medium`. Provider id `antigravity-subscription-directsdk` (plugin in each executing profile's `plugins/`; a profile without the plugin reports Unknown provider and silently falls through to the paid chain, so check `hermes -p <profile> plugins list` first). Proven with real tool calls on frontend and worker for Argon, Flash and Opus (2026-11-07).

The governor applies these to unpinned ready frontend and worker cards and rebalances only the pins it made (`managed_routes` in the state file). A human pin at any priority is left alone. Set the priority honestly at `kanban_create`: priority is the tier switch.

Native `fallback_providers` per profile, for runtime errors mid-card: frontend Sol, then Antigravity `gemini-4-argon-medium`, then `openrouter-budget/openrouter/auto`; worker Sol, then Antigravity `gemini-3.8-flash-medium`, then Auto.

Frontend and worker primary: provider `openai-codex`, model `gpt-6.1-sol`, ChatGPT subscription. Native `fallback_providers` has Antigravity Gemini before the paid entry (see Routes). Main judgment, planner and reviewer keep their separate Anthropic lanes. Do not auto-escalate repeat failures to Opus.

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
