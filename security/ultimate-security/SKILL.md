---
name: ultimate-security
description: "Use when securing, auditing or deploying any repo. Every deploy runs its gate."
version: 1.1.1
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [security, audit, gitleaks, trivy, secrets, pre-commit, ci]
    related_skills: [security-audit, credential-and-secret-handling, guarantee-audit, github-portfolio-audit]
---

# Ultimate Security

Three layers, because scanners and AI review catch different bugs and you need both.
Source: Rob Shocks, "Setup This New Security Skill Before It's Too Late" (youtu.be/O9N6D4iTYpM),
which ran Gitleaks+Trivy, /security-review, Cloudflare's skill and a plain prompt against an app
with 6 planted bugs. Cadence: Level 1 now, Level 2 monthly, Level 3 before taking payments or
touching auth or billing.

## When to Use

Any deploy of Deep's repos (the deploy gate below is mandatory). A repo is about to ship, take payments, or change auth or billing. Deep asks for a security
check, a leak scan, or "is this safe". A secret may have landed in git. A new repo needs
pre-commit and CI guards.

## What each tool actually catches (from the video's scoreboard)

- **Gitleaks**: secrets anywhere in git history, including keys deleted three commits ago.
  Cannot see code logic. 2 of 6 together with Trivy.
- **Trivy**: vulnerable dependencies. Says the package is bad but not that your admin route
  relies on middleware alone. Together they miss SQLi and tenant bugs.
- **/security-review**: reviews the diff only, so give it the whole tree if you want a full pass.
  4 of 6, ~84s, 16 cents. Misses git history and rate limiting. Not hardened against prompt
  injection: never run it on untrusted PRs.
- **Plain prompt** (below): 5 of 6, 34s, under a cent. Misses git history. Good on small apps,
  weak when the app is too big to read in one go.
- **Cloudflare security-audit** (vendored at `security/security-audit/`): 6 of 6, ~5 min, 38 cents
  on a tiny app, proves bugs in a sandbox. Cloudflare says one full run finds about half, so
  run it more than once. All three AI tools caught the agent-written hardcoded session secret
  that Gitleaks missed.
- The bug class AI agents write most: auth present but **ownership check missing** (logged in,
  but no check the record belongs to your org), delete or export with no tenant scope,
  hardcoded session secrets. Scanners cannot see these.

## Deploy gate: every internal deployment runs through this

Standing order from Deep: no internal deploy ships without this skill and the Cloudflare
`security-audit` skill. `scripts/deploy_gate.py` is the enforcement; it is wired into the deploy
paths so it runs without anyone remembering.

What the gate checks, in one run:
1. Gitleaks over git history (respects the repo's `.gitleaksignore`), values redacted.
2. Trivy on the tree: HIGH/CRITICAL vulns with a fix available, plus file secrets.
3. Cloudflare trigger: hashes every sensitive file (auth, session, token, billing, payment,
   webhook, admin, tenant, middleware, migrations, CI workflows, Dockerfile). If that surface
   differs from every recorded state, the deploy stops with `AUDIT-REQUIRED` and lists the files.

Exit 0 pass, 1 secret or vuln, 3 audit required, 2 tool failure. It fails closed.

Where it is wired (`deploy_gate.py install <repo>` does all three, idempotent):

| Deploy path | Hook |
|---|---|
| `git push` to main/master/production/prod/release (Railway, CF Workers Builds, Pages) | `pre-push` hook; husky repos get `.husky/pre-push`, kept out of commits via `.git/info/exclude`. Gates the pushed commit, not the dirty tree |
| `npm run deploy` (`wrangler deploy`) | `predeploy` script in package.json |
| `scripts/publish.sh` (deependhq family, nightly publisher) | gate runs on the mirrored clone, before commit; `PUBLISH_SKIP_GATES` does not skip it |

Agent rules for every deploy:
- Bare `wrangler deploy`, `railway up` or any CLI deploy bypasses the hooks: run
  `python3 ~/champ-skills/security/ultimate-security/scripts/deploy_gate.py check .` first.
- Before shipping, run `security-audit` in **guidance mode** over the diff being deployed (focused
  review, no artifacts). Cheap, catches the ownership-check class scanners miss.
- On `AUDIT-REQUIRED`: run `security-audit` in **full audit mode** (`standard`; `deep` for auth or
  billing) on a clean commit. When `run_status` is `complete`, record it:
  `deploy_gate.py stamp <repo> --run ~/security-audit-skill/<repo>/run-N`. Stamp refuses
  incomplete runs, invalid findings.json, dirty source refs, and any confirmed high/critical.
  Missing sandbox means most leads land in `needs_validation`; that still completes the run.
- `DEPLOY_GATE_OVERRIDE="<reason>"` passes and is logged. Only with Deep's explicit approval.
- Warn-only repos: `~/security-audit-skill/gate-config.json` `warn_only` lists repos with a
  pre-existing finding backlog. The gate runs and logs but does not block. Remove a name once its
  backlog is triaged; never add one to get a deploy out.
- Log of every gate run: `~/.hermes/logs/deploy-gate.log`. State and stamps:
  `~/security-audit-skill/<repo>/gate-stamps.json`.
- New deploy repo: `deploy_gate.py install <repo>`. Fleet check: `deploy_gate.py coverage
  ~/repos "~/Apps&Projects"`. A daily cron (`deploy-gate coverage`) runs `coverage --fix` and
  reports only when it wired something or failed to.
- `baseline` accepts the current sensitive surface without an audit (trust on first use). Only
  `install` should call it. Re-baselining to clear `AUDIT-REQUIRED` defeats the gate.
- Test: `python3 scripts/test_deploy_gate.py` (11 scenarios, throwaway repos).
- What the hooks do NOT cover, and say so in the report: the GitHub web UI's merge button,
  another person's machine, and any bare CLI deploy. Local hooks guard local pushes only, so
  merges made in the browser or pushed by a teammate skip them; that gap closes with a CI
  workflow running the same gate as a required check, not with more local hooks.

Gate pitfalls learned on rollout:
- `git rev-parse` inside a plain folder under `~` resolves to the home repo. The gate treats a
  folder as git only when it is the toplevel, or installs land in `~/.git/hooks`.
- Baselines must cover both HEAD (what pre-push checks) and the working tree (what predeploy and
  publish.sh check), or a dirty worktree reads as an unaudited change on the next push.
- **A partial install is worse than no install.** Every unwired path skips the checks silently,
  and an unwired fleet is indistinguishable from a clean one. Wire every path in one pass, fail
  loudly on the path that fails, and base any "the fleet is covered" claim on a measured count
  of wired repos rather than on the install command exiting 0.
- **A warn-only exemption needs provenance.** Record why each name is exempt (the pre-existing
  finding backlog), remove it the moment the reason clears, and never add one to get a fix out:
  without that record an exemption becomes the standing route for emergencies and the gate dies
  by a thousand exceptions.
- **A coverage watchdog must report only on change.** A cron that messages on every run trains
  the reader to ignore it; stay silent when the measurement is unchanged, and speak when it
  wired something or failed.

## Level 1: do this now (per repo)

1. **History scan, values redacted:**
   `gitleaks git --redact --no-banner .`  (exit 1 = leaks, 0 = clean). Add
   `--report-format json --report-path <scratch>/gl.json` to triage.
2. **Block new leaks on every commit.** Hook body, exits 1 on a leak (tested):
   `gitleaks git --pre-commit --staged --redact --no-banner`. Put it in `.git/hooks/pre-commit`
   (chmod +x) or in a `.pre-commit-config.yaml` entry.
3. **Dependencies and files:** `trivy fs --quiet --scanners vuln,secret --severity HIGH,CRITICAL .`
   For triage use `--format json` and print only Target, RuleID, Severity, line, never the
   match. Report every scanner finding this way (gitleaks included): the human-readable output
   of both tools echoes the captured secret, and that output reaches the report.
4. **One plain prompt before shipping:**
   "Review the codebase for security vulnerabilities. Name the file and what an attacker gets."
5. If the same mistake repeats (for example unscoped queries), write the rule into the repo's
   AGENTS.md or CLAUDE.md, such as "scope every query to the organization".

Triage rules learned running this on champ-skills:
- **Check before alarming.** A Trivy private-key hit was `.deploy_key`, gitignored, in zero
  commits, never on origin: local only, not leaked. Verify with `git ls-files --error-unmatch`,
  `git check-ignore`, `git log --all -- <file>`, and `git log origin/<branch> -- <file>`.
- **Gitleaks false positives** on 64-char hex content hashes (generic-api-key). Confirm every
  value matches `^[0-9a-f]{64}$`, then suppress with a `.gitleaksignore` line
  `<commit>:<file>:<rule>:<line>` (the JSON report redacts the line number under `--redact`,
  read it from `StartLine`). Re-run to prove clean, and prove the hit returns without the file.
- A real hit in history: rotate the secret first, rewriting history second. Deleting the file
  does not remove it from git history or forks. Follow credential-and-secret-handling.

## Level 2: every pull request, monthly sweep

- `/security-review` on trusted PRs only.
- Gitleaks and Trivy in CI (GitHub Actions) on every PR, fail the check on findings.
- Dependabot on for the repo. Quick header check with Mozilla Observatory on live sites.
- Monthly: run Level 1 across all repos under ~/repos and ~/Apps&Projects. Use
  github-portfolio-audit for the account-wide view.

## Level 3: before launch, payments, or any change to auth or billing

1. Load `security-audit` (Cloudflare) and request a **full audit**. It is guidance-only unless
   you ask for a full audit; pick profile `standard`, `deep` for auth/billing.
2. **Sandbox is mandatory.** The skill refuses to run target code without a sandbox with no
   network, empty env, read-only target, and resource limits. Without one, expect most
   findings to land in `needs_validation` (as in the video: 1 proved, 5 needs-validation).
   That is not a miss. Never relax the sandbox to get more proved findings.
3. Check the run: verifiers actually ran (on a small app the video saw zero hunters, zero
   verifiers, and the skill marked itself incomplete). Output goes to
   `~/security-audit-skill/<repo>/run-N`, outside the repo. Run two or three times.
4. Cost scales with app size and sandboxed proofs. Do not run it on every PR.
5. Staging, never production, for any AI pen tester. For anything handling money or PII at
   scale, a human professional is the final layer.
6. Passwords: Argon2id or bcrypt with per-user salt, never SHA-256 (see
   credential-and-secret-handling).

## Pitfalls

- Never run `/security-review` or the audit skill against untrusted repos or PRs with network
  or credentials in reach. Prompt injection in the target can steer the reviewer.
- A skill finding without a named boundary and result is not a finding. Do not report
  severity on `needs_validation` items.
- None of these tools attack the running app. Dynamic testing (OWASP ZAP, Shannon) is a
  separate category, staging only.
- Do not print, commit, or paste secret values into reports, cards or chat. Report file, rule,
  commit and whether the secret is live.
- Gitleaks, Trivy and the Cloudflare skill are installed on this Mac (Homebrew, 2026-10-23);
  semgrep and osv-scanner are not.
