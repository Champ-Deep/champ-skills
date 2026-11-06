# Model cost comparison for a workload

Use when Deep asks to cut model spend, compares two models, or pastes an OpenRouter activity table. Deliverable: per-role cost math on live prices plus the one measurement that decides the choice, not a generic price list.

## 1. Attribute the spend line first

Every OpenRouter line can come from Hermes or from one of Deep's product repos.

- Hermes side: slugs live in `~/.hermes/config.yaml` (`auxiliary.*`, `delegation`, `fallback_providers`), `~/.hermes/profiles/*/config.yaml`, and cron `model_snapshot` values in `~/.hermes/cron/jobs.json`. Actual per-model spend: sqlite `~/.hermes/state.db`, table `session_model_usage` (estimated_cost_usd, input/output/cache tokens, first_seen/last_seen); cron fire history in `~/.hermes/cron/usage_audit.jsonl`.
- If the slug appears in none of those, it is a product repo: grep his repos for the slug or provider name.
- Pitfall: when Deep states which product owns a spend line, start the investigation inside that product. Re-deriving attribution across his whole stack costs turns and reads as disbelief. One confirmation query, then move on.

## 2. Read the target repo's call sites

Map each model role to the code that calls it and classify its token shape:

- Single-shot structured calls (schema inference, classification): small input, output-heavy, no cache reuse. Winner = low output price.
- Agent loops (orchestrator/subagent frameworks that resend full history every step): input-dominated, most input is re-sent prefix. Winner = low cache-read price.
- Estimate per-call input/output from the code itself: system prompt size, tool-result truncation constants, max steps, calls per unit of work (per row, per run). Do not guess from model names.

## 3. Fetch live pricing, compare at the workload's mix

```
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | select(.id=="<slug>") | .pricing'
```

No auth needed. OpenRouter prices are per token; multiply by 1e6 for per-million.

- Convert every price programmatically with `Decimal(str(value)) * 1000000`, including cache reads and writes. Preserve `pricing.overrides` separately, because long-input rates can differ. Verify batch variants against the current base price rather than assuming they are half-price.
- Separate catalog support, public quality evidence, and end-to-end behavior in the user's harness. A modality flag proves accepted input types, not OCR accuracy; a large context window proves capacity, not compaction fidelity. Benchmark scores at maximum reasoning do not establish quality with reasoning off.
- When subscription access matters, distinguish provider implementation, billing entitlement, and vendor permission. Fetch the full current primary-source text for disputed policy clauses, because extraction snippets can omit the operative paragraph. Do not count a third-party OAuth route as included subscription usage merely because authentication or usage diagnostics succeed.

- Never compare headline in/out alone. Cost = I*[(1-c)*in + c*cache_read] + O*out. Compute at realistic cache rates (0 / 0.7 / 0.85 / 0.95) and solve the break-even cache hit rate where the two models cross:

  c = (d_in + d_out*(O/I)) / (d_in - d_cache),  where each d = price_A - price_B

  Above that cache rate the model with the cheaper cache-read price wins; below it the cheap-fresh-input model wins. Cache-read prices differ up to ~6x between cheap models, so this term usually decides the answer, not headline rates.
- Same-family dated snapshots (e.g. deepseek-v4-flash 0423 / 0731 / latest) can have inverted in/out pricing: one cheap-input-expensive-output, the other the reverse. Pick by the workload's output share, not by version recency.

## 4. Repo-side checks before recommending

- Hardcoded price constants: cost dashboards and usage pages often hardcode the current model's rate (e.g. `FLASH_IN`/`FLASH_OUT` consts in a usage route). A model switch must update them or the dashboard lies.
- Role config location: app-wide model slugs may live in a DB row set by an admin dashboard, in env defaults, or both. Say exactly where to change it.
- Key health: `GET https://openrouter.ai/api/v1/auth/key` with the repo's own key. 401 "User not found" = dead or rotated key. The response also shows the weekly limit and `limit_remaining`.
- The activity/generations listing API needs a management key (403 otherwise), so per-call token breakdowns are usually unavailable. Do not promise them.
- Do not run paid probes from the Hermes OpenRouter key when `limit_remaining` is near zero; report the math instead and state what could not be verified.

## 5. Report shape

Table per role with cost at each cache rate for both models, the break-even cache rate, one "cheaper lever you did not ask about" (often a sibling snapshot or the repo's own unused fallback model), and an explicit "could not verify" list (live quality, actual cache hit rates) naming the one measurement that would settle it.

## 6. Which model a delegation actually runs

Before quoting what a `delegate_task` fan-out costs, read the live `delegation:` block in `~/.hermes/config.yaml`: children inherit that provider and model, not the model the chat runs on, and the resolved slug is what shows up in `session_model_usage`. This is the single most common misattribution when Deep asks "which subscription did this burn".

- Command that settles it: `grep -A6 '^delegation:' ~/.hermes/config.yaml` plus one row from `session_model_usage` for the session in question.
- Fan-out multiplies the call count, not the window: a five-child batch of judgement work is five parallel cheap sessions, so "spend down my Claude plan before it resets" can never be satisfied by delegating. That work is done inline in the current chat, or as cards pinned to the quota model.
- Never assert a subagent's model from the parent's model or from the child's self-description in its summary; the child reports its own slug, but the config is authoritative and is checked first.
