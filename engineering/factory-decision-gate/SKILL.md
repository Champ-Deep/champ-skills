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

## Laya's place

Laya (Convai, installed at /Users/deep/laya-local, weights cached in ~/.cache/huggingface, runs offline) is a classifier, not a chat model, so it cannot be a Hermes provider or worker model. It runs in shadow only (`ask --shadow`) and never changes a verdict. Promote it only after 300 Deep-adjudicated labels (60+ per class) and a fine-tuned checkpoint that beats the rules on date-held-out rows. Base Laya failed on client and personnel cases, so do not shortcut this.

When Deep answers a digest question, record it with `decider.py label ID "situation" auto_decide|ask_deep --note ...` so the label count grows without extra work from him.
