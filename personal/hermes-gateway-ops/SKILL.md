---
name: hermes-gateway-ops
description: "Use when the Hermes gateway or a messaging platform fails."
version: 1.0.0
---

# Hermes gateway ops

Operating and repairing the Hermes message gateway and its platform adapters. For MCP connectors use `hermes-mcp-wiring`; for agent config beyond this skill's scope use the bundled `hermes-agent` skill.

## Triage order: state, then logs, then the provider

1. **Read the state file first, logs second.** `~/.hermes/gateway_state.json` is the machine-readable verdict: `gateway_state` is `running` | `startup_failed` | ..., and `platforms.<name>` carries `state`, `error_code`, `error_message`. A gateway that "won't restart" is usually `startup_failed` with a fatal platform error, and the state file names the cause without any log archaeology.
2. **Then read the logs to get the timeline.** `~/.hermes/logs/gateway-restart.log` is the startup transcript with one `=== gateway-restart started ===` block per attempt, so it shows whether the current failure is new or a repeat. `gateway-exit-diag.log` and `gateway-shutdown-diag.log` explain a prior process's death (signal, parent, load average, OOM evidence). `gateway.log` is the live operational log.
3. **Verify the credential against the provider, not against Hermes.** Before concluding anything about a token, call the provider's own API directly, independent of the gateway:

   ```bash
   TOK=$(grep -E '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
   curl -s --max-time 20 "https://api.telegram.org/bot${TOK}/getMe"
   ```

   `{"ok":true,...}` means the credential is fine and the fault is elsewhere. `{"ok":false,"error_code":401,"description":"Unauthorized"}` means the token is revoked or invalid, and no amount of restarting will fix it. This single call separates "Hermes is broken" from "the credential is dead" in one shot, which is the decision the whole repair hinges on.
4. **Only the credential holder can mint a new one.** A revoked bot token is fixed by regenerating it in the provider's admin console, then writing it into `~/.hermes/.env` yourself. Do not fabricate, guess, or reuse a token. A regenerated token can come back with a DIFFERENT numeric ID and username than the old one: compare the ID prefix before and after, and if it changed, tell the user, because their saved contacts, group admin lists, and shortcuts all point at the old handle and will silently fail.

## Restart semantics

```bash
hermes gateway restart
```

One gateway per host serves every profile. On a single-profile host a restart can legitimately answer "The host gateway already serves profile 'default', nothing to start" with a live PID: that is a successful restart, not a refusal, so do not keep re-issuing it. To target a profile explicitly use `hermes -p <profile> gateway restart`. After any restart, confirm the outcome in `gateway_state.json` (`gateway_state: running` and the platform `state: connected`) rather than trusting the CLI's one-line reply.

## Pitfalls that cost real time

1. **A warning's suggested remedy can be the bug.** Never apply the fix a log line recommends until you have read the code gate it names. The auxiliary paid-lane warning tells you to set `auxiliary.free_only: true`, but that gate rejects explicitly configured models as well as paid fallbacks, so enabling it silences the warning while killing the vision lane you were trying to keep. The correct lever for a spend ceiling on the fallback lane alone is `auxiliary.openrouter_model` pointed at a `:free` model, which leaves explicit per-task models untouched. When a warning proposes a config change, find the enforcing code and confirm what else the gate rejects before writing anything.
2. **Do not trust a warning's label for which config slot it means.** Some warning strings are hardcoded to the word "fallback" even when the code path was handed an explicit model, so the model it names may be a per-task setting rather than the fallback. Resolve the actual effective values before concluding anything about your configuration: import the resolver and print what it returns rather than inferring from the message. A warning that fires for a model you deliberately configured is describing your intent, not a defect.
3. **Resolving config by reading the module beats reading it by eye.** Confirm the real values with the repo venv, which has the runtime deps:
   ```bash
   cd ~/.hermes/hermes-agent && ./venv/bin/python3 -c "
   from agent.auxiliary_client import _aux_openrouter_settings, _is_free_model
   print(_aux_openrouter_settings())"
   ```
   The Hermes tools python cannot import these modules (missing runtime deps); the checked-in venv can.
4. **Distinguish a crash from a clean exit before hunting a bug.** A fatal platform error makes the gateway exit deliberately and cleanly, and a restart storm can leave broken-pipe tracebacks in the worker wrapper that look like the cause but are only the downstream symptom. Read the first real error line, not the traceback tail.
5. **Establish the timeline before changing anything.** A platform that connected and then stopped working minutes later points at credential rotation or a deliberate SIGTERM, not at a config regression. Check what changed in the env file and who sent the signal before editing config.

## Reporting

Deep expects executed evidence, not a narrative. Show the raw provider response and the `gateway_state.json` fields that prove the repair, state plainly which of the requested changes turned out to be unnecessary, and name anything you deliberately did NOT do and why. When the configuration is already correct, say so and change nothing: making a change to satisfy a request that was built on a wrong premise is worse than reporting the premise was wrong.

Secrets never enter chat. Read them from `~/.hermes/.env` into a shell variable, print only masked prefixes, and let the user paste replacements in themselves.
