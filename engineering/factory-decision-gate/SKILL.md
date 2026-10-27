---
name: factory-decision-gate
description: Use when a factory agent is about to act without Deep.
---

# Factory decision gate

Deep is not the bottleneck by choice: agents do everything reversible themselves and bring him only irreversible calls. The gate is code, so it answers in milliseconds with no model and no API key.

## Before any autonomous action

```bash
/Users/deep/laya-local/.venv/bin/python /Users/deep/laya-local/decider/decider.py act <action>
```

`decide` means go. `ask_deep` means stop, stage the action, and put it in the next digest or Telegram as ONE question with a recommended answer. Never route around an `ask_deep`.

Actions: `decide` = open_pr, push_feature_branch, create_branch, create_card, unblock_card, run_tests, retry_ci, comment_issue, file_issue, label_issue, write_report, read_logs, write_digest. `ask_deep` = merge_pr, push_main, force_push, delete_branch, deploy, release, db_migration, change_secrets, rotate_keys, spend, send_external, change_dns, delete_data, and anything unknown. The sets live in `decider/ground.py` (FACTORY_AUTO, FACTORY_ASK); edit them there and run `python -m unittest test_decider` from `decider/`.

For a business or people decision (not a code action) use `decider.py ask "<situation>"`; it matches Deep's precedents in the Celsus Decision Desk and abstains when none covers it.

## The decision model's place

Clef-flash (Cloudflare, Apache 2.0, 9B; installed under /Users/deep/laya-local, weights in ~/.cache/huggingface, runs offline) replaced Laya on 2026-10-18 (15 of 18 vs 7 of 18 on the Celsus suites). It is a classifier, not a chat model, so it cannot be a Hermes provider, worker or computer-use driver. It is about 7 s per call on this Mac, so it is a gate, not a per-click loop. It runs in shadow only (`ask --shadow`) and never changes a verdict until 300 Deep-adjudicated labels (60+ per class) show it beating the rules on date-held-out rows.

When Deep answers a digest question, record it with `decider.py label ID "situation" auto_decide|ask_deep --note ...` so the label count grows without extra work from him.

## The blocked-card sweep (kanban_clef.py)

`~/.hermes/scripts/kanban_clef.py` runs every 30 min (cron `bcd62a17f362`, no_agent, stdout delivered to Deep's Telegram, empty stdout = silent). It lists every blocked card, runs each through `ground.decide`, and:

- `decide` AND match >= 0.45 (AUTO_BAR_MATCH; ground's own 0.30 floor is fragile and produced wrong calls like auto-sending client material or rotating an API key) AND no FACTORY_GUARD word (rotate, credential, secret, 1password, merge, deploy, migrate, authorize, payment, keys) -> `hermes kanban unblock --reason <citation>`, reversible and logged on the card.
- Everything else stays blocked and joins a change-gated digest: top 10 by priority with the gate's reason, budget-approved candidates marked "auto bar: approve to unblock".
- Quiet hours 02:00-15:00 IST hold the MESSAGE only; reversible unblocks still fire silently.
- `--dry-run` changes nothing; `--force` bypasses the change gate; `--selftest` asserts the two verdict classes.

`--shadow-top N` asks Clef-flash on the top N needs-Deep cards and appends rows to `~/.hermes/state/kanban_clef_shadow.jsonl`. Pitfall found live: the sweep normally runs under the Hermes python (no torch), so the script re-execs itself into `/Users/deep/laya-local/.venv/bin/python` when `--shadow-top` is present (`env -u PYTHONPATH -u PYTHONHOME` applied by the re-exec). Cold load is 4+ minutes on this Mac, so shadow is a manually-triggered probe, never part of the cron.
