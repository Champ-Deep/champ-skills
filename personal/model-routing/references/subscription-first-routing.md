# Subscription-first background routing

Use the existing Hermes profiles and native fallback chain. Do not build a second router service.

## Routes

Four pools, all read live every 5 minutes: Anthropic direct (`hermes usage`), ChatGPT (`hermes usage --provider openai-codex`), Antigravity (`agy -p /usage --output-format json`, three buckets: Gemini, Claude and GPT, Argon), shared OpenRouter key (paid). Reserves: Anthropic 25%, ChatGPT 15%, Antigravity buckets 20%, OpenRouter 20%. Unknown quota is treated as empty.

Tiers, decided by card priority when no human pin exists (Deep, 2026-11-07):

| Tier | Priority | Model | Pool |
|---|---|---|---|
| Hardest | 90+ | Claude Opus 5.5 | whichever of Anthropic direct or Antigravity Claude has more headroom; both at reserve: pin Anthropic and wait, never downgrade |
| Important | 75 to 89 | Gemini 4 Hydrogen High (`antigravity-subscription-directsdk/gemini-4-hydrogen-high`, Deep 2026-11-22, t_93eeedab) | Gemini bucket of the Antigravity plan; at its 20% reserve: Claude Sonnet 5.5 by the Hardest-tier pool rule. A card on Hydrogen stays put on a missed quota read. Hydrogen cut off 1 of 3 long-context runs at the output limit, so the reviewer watches long outputs on these cards |
| Routine | below 75 | GPT-6.2 Sol on ChatGPT | at the ChatGPT reserve: Antigravity Gemini Flash; only when that is also at reserve: bounded paid OpenRouter Auto |

The tiers apply to worker cards only. Since 2026-11-21 frontend always runs its profile default, the frontier GPT (`gpt-6.2-astra`), at every priority; it has no fallback chain and waits at the ChatGPT reserve (Deep's rule: never downgrade front-end work).

Antigravity model ids carry an effort suffix: `claude-opus-5-5-medium`, `claude-sonnet-5-5-medium`, `gemini-4-argon-medium`, `gemini-3.8-flash-medium`. Provider id `antigravity-subscription-directsdk` (plugin in each executing profile's `plugins/`; a profile without the plugin reports Unknown provider and silently falls through to the paid chain, so check `hermes -p <profile> plugins list` first). Proven with real tool calls on frontend and worker for Argon, Flash and Opus (2026-11-07).

Governor pins are sticky: a tiered card stays on its Claude pool until that pool is known to be at reserve. Headroom differences and a failed quota read never move a card (a missed `agy` read once flapped four cards between pools in one cycle). `agy` is resolved at `~/.local/bin/agy` because the cron PATH lacks it.

The governor applies these to unpinned ready frontend and worker cards and rebalances only the pins it made (`managed_routes` in the state file). A human pin at any priority is left alone. Set the priority honestly at `kanban_create`: priority is the tier switch.

Native `fallback_providers` per profile, for runtime errors mid-card: frontend none (`[]`, a failed call retries on Astra); worker Antigravity `gemini-3.8-flash-medium`, then Auto.

Primary on `openai-codex` (ChatGPT subscription): frontend `gpt-6.2-astra`, worker and content `gpt-6.2-sol`. Native `fallback_providers` has Antigravity Gemini before the paid entry (see Routes). Main judgment, planner and reviewer keep their separate Anthropic lanes. Do not auto-escalate repeat failures to Opus.

The `providers.openrouter-budget` definition in each executing profile must have:

- api `https://openrouter.ai/api/v1`, transport `chat_completions`, key_env `OPENROUTER_API_KEY`, catalog_provider `openrouter`.
- `extra_body.max_tokens: 4096`.
- `extra_body.provider.max_price: {prompt: 1, completion: 4}` (USD per million tokens), `require_parameters: true`.
- `extra_body.plugins: [{id: auto-router, cost_tier: low, allowed_models: [deepseek/*, z-ai/*, xiaomi/*, moonshotai/*]}]`.
- session_affinity_header `x-session-id`.

Do not buy OpenAI or Anthropic tokens again through this fallback. Do not raise the shared key credit limit without approval. Query `/api/v1/auth/key` before a paid probe. Limits belong to that key, not to a remembered dollar amount.

**Pinning a card while a governor tick is in flight loses the pin.** The tick reads rows first and writes pins later, so a card you pin to Sol in that window (priority 75+ is a Claude tier) is re-pinned to Opus 20 s afterwards and recorded as managed. Read the card's events after the next tick; if a governor `model_override_set` follows yours, pin again and drop the id from `managed_routes`. The pin is what makes a high-priority frontend card the lane head on the ChatGPT pool instead of waiting behind the reviewer for the one Anthropic slot.

## Admission and quota switching

`~/.hermes/scripts/kanban_quota_guard.py --apply`, scheduled by script-only cron `f84b5393e7df` every5min, uses live `hermes usage --provider ... --json` snapshots. Reserves are25% Anthropic,15% ChatGPT,20% OpenRouter. Unknown snapshots deny admission and do not trigger paid routes.

**Reading live lane headroom: the state file, not memory.** `~/.hermes/state/kanban_quota.json` is rewritten every 5 minutes and is the authority on which pools may claim a card this tick: `snapshots.<pool>.windows[].used_percent` (lower is better; an `unavailable_reason` means the quota is unknown, and unknown counts as empty), `reserves`, `allowed_profiles` (who may claim now), `target_concurrency` against `running` (whether the board is at its ceiling), `caps_live` with `caps_configured_at` and `gateway_boot_at` (numeric caps apply only once the gateway booted after they were written), and `managed_routes` (the pins the governor owns, so it re-pins those and leaves human pins alone).

Slots each pool grants, by headroom read from `allowance()` in `kanban_quota_guard.py` (re-read that function when the answer matters; it is the source of truth): Anthropic 0 at or below 25% left, 1 below 60%, 2 above; ChatGPT 0 at or below 15%, 1 below 40%, 2 above; Antigravity buckets 0 at or below 20%, 1 below 50%, 2 above; shared OpenRouter 0 at or below 20% else 1. So a pool reading 12% against a 20% reserve is closed while another reads two open slots: "that lane is busy" and "that pool is empty" are different states with different fixes, and answering one as the other sends Deep to restart a gateway that is working. State the headroom together with the reserve whenever you report which lanes can run.

Ordinary queued frontend/worker Sol cards switch to bounded Auto at the ChatGPT reserve, using `hermes kanban set-model`, with a routing comment and exact DB read-back. Only routes recorded as managed by this governor return to Sol when the window recovers. Preserve explicitly pinned specialist models and never touch running cards. Paid fallback on an actual runtime provider error uses Hermes's native fallback chain, not a Jev cross-provider rewrite.

**The guard fails safe by emptying the allowlist.** Its cron wrapper runs `hermes config set kanban.dispatch_profiles '[]'` whenever `--apply` exits non-zero, so one broken guard run (an interpreter lacking the modules `hermes_cli` imports is the usual cause) freezes every lane while `ready` cards pile up with `skipped_nonspawnable`. Read the guard's job row in `hermes cron list` first, fix the script, and let a clean `--apply` write the allowlist back; hand-setting the key while the guard still fails only delays the next freeze. Diagnosis order and the `skipped_nonspawnable` class live in `kanban-task-intake` section 2.

**Moving held cards to another pool on Deep's instruction.** Tier is priority, so while Anthropic is at reserve every `default`, `planner`, `reviewer` card and every priority 75+ card waits, and "run my side projects now" means the ChatGPT pool instead: `hermes kanban set-model <id> --provider openai-codex gpt-6.1-sol` per ready card (it takes effect on the next dispatch). Then remove those ids from `managed_routes` in `~/.hermes/state/kanban_quota.json`, because the governor only skips a pin it does not own and will re-route a managed card on its next tick. Read the pins back from `tasks` before reporting which cards moved, and say in the card comment which pool the card is now on, so a later ruling about quota is not read as a reassignment.

Global maximum3 workers, maximum1 per profile. `dispatch_profiles` is live per claim, but numeric caps are captured at gateway boot. Governor leaves admission empty until the observed gateway boot is newer than `caps_configured_at` in `~/.hermes/state/kanban_quota.json`. A gateway restart must be run from the user's own external Terminal, after active workers finish. Do not bypass the tool's self-restart protection. The five-minute quota reserve is an admission policy, not a per-token hard budget. The existing provider key limit remains the paid hard backstop.

## Worker Auto Router trial (worker-auto-trial-v1)

`WORKER_AUTO_TRIAL` in `kanban_quota_guard.py`. For each unpinned, routine-tier worker card the governor asks OpenRouter's Auto Router (Jev powered) which model it would pick, with `max_tokens: 1` on the card brief (about $0.0003 to $0.002 per card, logged as `route_preview` in `~/.hermes/state/jev_decisions.jsonl`). Deep's gate: a `google/*` pick runs on Antigravity Gemini, an `anthropic/*` pick on the Claude pool with headroom, an `openai/*` pick on the ChatGPT Sol default; anything else runs through `openrouter-budget/openrouter/auto`, whose worker profile plugin config excludes `google/*, anthropic/*, openai/*` and keeps the $1/$4 ceilings. Frontend is not in the trial. Judge it from the Sunday report (`route_preview` rows against run outcomes), then flip the flag or move it to the state file.

## Grounded retro loop (retro-v1)

`kanban_retro.py` (cron `kanban-grounded-retro`, every 6 hours, script-only). Finished lane cards with a real worker handoff summary are gated by Jev (review or skip, fails toward review), batched 8 per reviewer card, max 2 cards per run, pinned by `claude_pool` to the Opus pool with headroom. The reviewer verifies one concrete claim per completion, comments `Retro: verified|gap|human check` on the original card, and creates follow-up cards by lane with `retro-<id>-<slug>` idempotency keys. Checkpoint and per-card verdicts live in `~/.hermes/state/kanban_retro.json`. Bookkeeping completions (rulings, archives) have no run summary and never reach the reviewer.

## Jev on OpenRouter

`typesafe/jev-1.14` answers typed decisions at `POST https://openrouter.ai/api/alpha/decisions` with the shared OpenRouter key; no TypeSafe key is needed. `celsus_jev.py` uses it when `TYPESAFE_API_KEY` is absent. Cost is input-only, about $0.00003 per card. Jev picks `ask` for most residual blocked cards by design (the instructions prefer ask when facts are missing), so it releases only clearly reversible agent work.

## Prove the real path

Read back the two executing profiles, not just the root. Run config check. Verify a real terminal tool executed through the subscription route and separately through the bounded route. Canonical profile `state.db` sessions contain model, billing_provider, billing_mode, tool_call_count and api_call_count; messages with role=tool confirm actual execution. Custom providers may be stored as billing_provider `custom`, so lookup the exact session id instead of filtering only by the configured provider name. `hermes chat` may not emit the root --usage-file artifact; do not invent it.

Run `~/.hermes/hermes-agent/venv/bin/python -m unittest -v test_kanban_decisions.py` in `~/.hermes/scripts` for quota and Jev safety tests. Obtain the actual selected paid model and usage.cost from a real OpenRouter response, never from the requested `openrouter/auto` alias. A successful text echo alone is not tool protocol proof.

Do not widen ceilings to solve a router503. A bounded Auto Code request can return `No measured models satisfy the Auto Code policy and request restrictions`. General Auto with the same family allowlist and price ceilings is a valid fallback when a real tool-call probe passes. Keep Auto Code off until it satisfies the unchanged controls. General Auto can itself return Jev decision metadata; do not add a second paid Jev call per turn just to replicate it. Hosted Jev for deciding board actions remains a separate system, fail-closed until its own credential is configured.
