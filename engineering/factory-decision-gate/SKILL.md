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

- **Probing the gate with a spend-carrying action proves nothing.** `spend` sits in FACTORY_ASK, so any test card that mentions a cap, a price or a purchase returns `ask_deep` however healthy the gate is, and it reads as a broken gate. Probe with a spend-free action (`open_pr`, `run_tests`), and treat `ask_deep` on anything priced as the designed answer to work around by staging, never by loosening the set.

For a business or people decision (not a code action) use `decider.py ask "<situation>"`; it matches Deep's precedents in the Celsus Decision Desk and abstains when none covers it.

## A new proactive automation ships record-only first

Any recurring job that acts on Deep's work without him starts in shadow: it writes one dated proposal note (what it would queue, why, per candidate) into the vault and creates, merges and sends nothing. Promote it to live only after he has read about a week of those proposals and said go. The first live form then takes one bounded action per run (one PR-only worktree card, named spend cap, no deploy, no sends), not a batch.

Why this shape: coverage earns the gate the same way a precedent does, by being adjudicated. An unadjudicated automation writing to real cards has nothing behind it, and the shadow note is the thing he can rule on in one pass. Keep the shadow job's stdout out of chat (`--deliver local`, see the `schedule` skill) so a silent run stays silent.

A job that only *reports* ships paused instead of shadow. Shadow is for jobs that write to cards, repos or mail, which have something to stage. A brief has nothing to stage: create its cron with `--paused --paused-reason "<the review he owes>"`, paste the top N of its ranking with the reason for each row into the decision card body, flag the entries you doubt yourself, and let his ruling unpause it (`hermes cron resume <id>`). An unreviewed ranking that starts firing daily pings him with output nobody has judged.

One derivation, one home: when a new surface (endpoint, brief, export) needs something an existing sweep already computes (due dates, scores, clusters), extract the shared function and import it. A second copy of the same regex drifts from the first, and the board then contradicts itself about what counts as overdue.

## Meeting follow-through gate (Deep's ruling, 28 Oct 2026, precedent P41)

The meeting watcher (cron `d741846ee693`) and intake sweep (`9a042ac04419`) act on Deep's items without him: emails he committed to, docs, NDAs (champions-nda), and 30-minute ideation slots with a prep note in `Efforts/Active/Ideation/`. Only DECISION items gate: hard-hold list first (spend, pricing, payments, signing other than the standard NDA, HR and reporting lines, credentials, legal disputes, Chief-owned), then `decide` (precedent), then one `clef_ask`; proceed only if `auto_proceed >= 0.95`. Everything else is a blocked decision card on the board, never only a Telegram line.

- `clef_ask` criteria must be a dict `{label: description}`; a list raises inside `systemone` and the tool returns a bare "Error executing tool".
- Clef is conservative, not calibrated: a routine internal deadline-confirmation email scored auto_proceed 0.34, a contract signing 0.05. At a 0.95 bar Clef alone frees almost nothing; the pre-approved action classes and precedents do the work. Grow coverage by adding precedents (Decision Desk `Task Decision Precedents.md`, verify with `decider.py ask`), not by lowering the bar.

When a decision card asks whether to loosen a hold, answer with a backtest, not an assertion: leave-one-out over the labels already adjudicated, reporting per-category n and precision at the proposed bar (default n>=30 at 0.99). No category clearing the bar is itself the recommendation, and those numbers go in the card. A hold argued with a confusion table survives review; a hold argued with taste gets loosened.

## Blocked is not the same as needs Deep

Measure before tuning the gate: on 5 Nov 2026, 306 of 487 blocked cards had no block_kind and were created already blocked (`initial_status`, no reason) by the sweeps. They are parked to-dos, not decisions. Fix at the creator: a sweep creates a `todo` linked as child of one decision card (parent to child gating promotes it when the parent is done), and only that decision card is blocked. Group decisions by type so one ruling covers many cards (`scripts/decision_clusters.py`, dry run). Two cluster shapes inflate the board: cards whose job is to raise another decision card, and daily recurring packs (Send Pack, social posts): rule them once as a policy.

`scripts/kanban_escalate.py` (cron f84b5393e7df, silent when idle) pins a todo/ready card with 3+ block_recurrences to claude-opus-5-5 high, 5+ to xhigh, via kb.set_model_override and kb.set_reasoning_effort. It skips blocked cards and capability walls: a stronger model cannot sign in to M365 for Deep.

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
