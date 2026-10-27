# Model drivers for the bake-off suite

`run.py` spawns the `cmd` from `models.json` with `{prompt}` substituted, with the task directory as cwd. For agentic tasks the driver must be a headless CLI that edits files and runs tests unattended. The suite ships `agy` (Gemini) and `claude` (Anthropic) drivers; for any other model, wrap Claude Code against an Anthropic-compatible endpoint.

## Wrapper recipe (verified working)

`orclaude.sh`, self-contained because cwd changes per task:

```bash
#!/bin/bash
set -a; source ~/.hermes/.env 2>/dev/null; set +a
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""
export ANTHROPIC_DEFAULT_SONNET_MODEL="<provider/model-id>"
export CLAUDE_CODE_MAX_CONTEXT_TOKENS="<model context window>"
exec claude -p "$1" --model sonnet --output-format text \
  --permission-mode acceptEdits --dangerously-skip-permissions \
  --strict-mcp-config --settings <abs path>/cc-settings.json
```

`models.json` entry:

```json
"<provider/model-id>": {"cmd": ["bash", "<abs path>/orclaude.sh", "{prompt}"], "price": [in_per_1m, out_per_1m]}
```

## Why this shape

- Claude Code validates the model name against its catalog before any request goes out. Pass `--model sonnet` (a name the catalog accepts) and let `ANTHROPIC_DEFAULT_SONNET_MODEL` decide what `sonnet` resolves to on the wire. Passing an unknown id directly to `--model` dies at the catalog check.
- Do not retry the `modelPicker` route in a `--settings` JSON to smuggle an unknown id past the catalog: the catalog check runs before any settings override, so that path cannot work. Keep the settings file only for TUI labelling, and keep it beside the wrapper rather than in a pruned scratch directory.
- Keys come from `~/.hermes/.env` at runtime and are never stored in the wrapper or printed.
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS` must match the model's real window, or long-context tasks are truncated by a default.
- `--permission-mode acceptEdits` plus `--dangerously-skip-permissions` is required because the harness is non-interactive: the model must edit fixtures and run tests with nobody to approve.
- Price comes from the provider's list price per 1M tokens, entered in `models.json`; state the units in every cost report.

## Lane checks before a full run

1. Prompt check: `bash orclaude.sh "Reply with: lane ok"`. Text comes back alongside thinking blocks; assert on the text.
2. Agentic check: `python3 run.py --bank deep_tasks --models <entry> --tasks <id>` for one task, then read the scored result. Prompt success alone proves nothing about file edits.
3. Empty `content` on HTTP 200 is not success: print the raw body first.