# Adopt bot features without replacing Hermes

Use when a video or repository promises a better personal-agent team. Compare executable source with the installed Hermes version and official docs before installing anything.

## Smallest complete adoption

- Map named teammates to existing Hermes profiles. Reuse the roster, roles and capability boundaries in Celsus `_config/bots.md`; do not create a second Inbox or parallel task board.
- Map recurring routines to native cron and durable work to Kanban. Bots talking to one another must not bypass a card's approval gate or create duplicate workers.
- Map memory to profile memory plus skills for procedures. Do not import another framework's system prompt or replace SOUL.md wholesale.
- Map screen takeover to native Hermes Bot Screen on a supported Linux gateway. On macOS, use existing local browser/computer-use surfaces. Never install a Linux virtual-display stack on the Mac to imitate a demo.
- Use the service manager already supervising Hermes for crash recovery. A running PID is liveness, not progress; verify outputs and card evidence before calling work successful.
- Preserve approval controls. A wrapper that passes `--dangerously-skip-permissions` or `--dangerously-bypass-approvals-and-sandbox` is not a safe drop-in, even if its README promises approvals later.
- Treat an interrupted send, purchase, merge or other side effect as UNKNOWN until the exact remote target has been read back. Do not replay it solely because a worker or gateway restarted. Native recovery is not an exactly-once guarantee for arbitrary tools.
- A model selection or reasoning-effort control must use the harness's supported values. Reuse per-card model/provider pins and the quota governor rather than rewriting active workers or shared credentials.

## Source-upgrade gate

1. Load `hermes-agent`; fetch current official updating docs. Run `hermes --version`, `hermes update --check`, `hermes update --plan`, and inspect source-tree status.
2. Check for commits not reachable from the target release, not merely dirty files. `git rev-list --left-right --count HEAD...<tag>` and `git log <tag>..HEAD` reveal local patches the updater might replace.
3. Preserve those commits as patches and preserve the dirty source diff before moving the checkout. Never read or export secrets for this audit. Keep private runtime evidence out of public skill repositories.
4. Verify `updates.pre_update_backup` is not explicitly disabled. Native `quick` snapshots are a baseline, not proof of a full recoverable database backup. For a production migration, use the documented full backup path and establish a rollback plan.
5. Do not run `--no-gateway-restart` against a live gateway as a pretend safe update: code/dependencies can change under lazy imports. Stage the migration until active work is drained and the authorized restart scope is clear.
6. Verify the local patches' behavior on the target release before replacing the runtime. Same feature names do not prove compatibility.
7. After the real update, verify source commit, dependency readiness, gateway and platform state, native bot handoff and Kanban regression tests. A CLI success line alone proves none of these.

## Evidence boundary

The SuperBot source inspected at 652e100fc3412239fd5a07ca7bb8566213c5b6fa names only Claude, Codex and Pi adapters. Its Claude and Codex adapters disable permission checks, and approvals are listed as unfinished. These are dated findings to recheck, not permanent claims about the project. Use SuperBot as an interaction reference until a reviewed integration supplies the missing boundary.

Official references:
- https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
- https://hermes-agent.nousresearch.com/docs/user-guide/features/bot-screen
- https://hermes-agent.nousresearch.com/docs/getting-started/updating
