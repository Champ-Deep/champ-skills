---
name: credential-and-secret-handling
description: "Use when a credential lands in chat or a URL needs auth."
version: 1.0.1
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [credentials, secrets, vault, browser, security]
    related_skills: [chat-decision-monitor]
---

# Credential and secret handling

## When to Use

- Deep pastes a password, API key, token, or OTP into chat, including inside an
  out-of-band message.
- A task needs auth for a URL, app, or API and no credential is stored yet.
- He asks to "save this in my vault" or "log in and pull the docs".
- Any secret-bearing file needs auditing before it reaches a repo.

## The non-negotiable

**A credential pasted in chat is compromised the moment it lands.** It is now in
the conversation transcript, the session log, and any downstream summary. Never
type it into a page, never write it into a note, repo, config, or env file, and
never echo it back.

When this happens, say so plainly and briefly, then move on to the work that is
not blocked. Do not stall the task, and do not moralise at length: one line that
the value is exposed and should be rotated, then proceed.

Rotation advice belongs to Deep. Say it once: if that password is reused
anywhere, change it. Do not repeat it.

## Procedure

1. **Do not use the pasted value.** Not with `browser_type`, not with curl, not
   in a file.
2. **Check what is already stored:** `browser_vault_list`. It returns handles and
   metadata only, never secret values.
3. **If a password manager is `locked`,** call `browser_vault_unlock` with the
   backend. The user is prompted in their own UI. If they decline, that is a
   complete answer, not an obstacle to argue past.
4. **On a login page with no stored item,** call `browser_vault_save_login`. It
   shows a masked prompt owned by the user's UI. This is the ONLY route by which a
   password may reach a page.
5. **Fill via the handle:** type the identifier yourself with `browser_type`, then
   `browser_vault_fill(handle=...)`. For OTP/2FA call `browser_vault_enter_code`.
   Never combine a code with other content.
6. **Respect origin binding.** A fill is refused unless the page origin exactly
   matches the item's bound origin. Re-check before retrying; do not attempt a
   cross-origin fill.

## Getting a secret from Deep onto his machine

When a script or env file needs a value only he holds, never hand him a
one-liner that carries the secret inside quotes: pasting it breaks the quoting
(the shell stalls at a `quote>` continuation prompt) and the value lands in his
shell history. Give the two-step instead:

```bash
read -s TOK
printf 'KEY=%s\n' "$TOK" >> ~/.path/secrets.env; unset TOK
grep -c '^KEY=' ~/.path/secrets.env   # expect 1; >1 means a partial earlier write
```

`read -s` echoes nothing, nothing enters history, and the count check catches a
half-written line from an aborted attempt before anything consumes the file.

When Deep says "add the variable, I will fill the value" (his usual form for an
API key he just pasted), write the NAME only: append `KEY=` with an empty value
plus a one-line comment, tell him the file path and line, and let him paste the
value himself. Confirm success by testing the key against its service (status
code only), never by printing the file back.

## Storing a credential in the vault

"Save it in my Celsus vault" does NOT mean write the value into a markdown note.
Vault notes are searched, diffed, exported, and synced, so a plaintext secret
there leaks through every one of those paths. The vault route is the masked
browser prompt; the vault is for the reference, not the secret.

If a login page is not currently open, say what is needed and stop there rather
than inventing a storage location.

## CLIs that dump variables

A command whose normal output is a variable dump (`railway variables`,
`kubectl get secret -o yaml`, `heroku config`, `cat .env`) prints live values
straight into the transcript, and tool output reaches the transcript exactly
like a paste. Ask for key names before running it:

```bash
railway variables | grep -oE '^[A-Za-z_][A-Za-z0-9_]*'    # names only
```

If a value has already been printed, treat it exactly like a paste: one line
saying it is exposed and should be rotated, then continue with the work that is
not blocked.

## Secrets in repos

When you scaffold a tool that will hold a key, the ignore comes first: write
`.gitignore` containing `.env` before any key is generated into it. Reversing
the order leaves a tracked file with a live value for as long as it takes to
notice, and `git add -A` stages it without complaint. Report such a key as a
name plus "generated, stored in `.env`, untracked"; the proof it works is a
status code, never a printout.

When auditing a file that may hold live values, report key NAMES, value LENGTH,
and a token-shaped yes or no. Never print the value, not even truncated.

The same applies to scanner output: gitleaks, trivy and similar tools print the
matched value in their own human-readable results even when redaction flags are
set, and tool output reaches the transcript exactly like a paste. Run them with
`--format json` / `--report-format json` and quote only target, rule and severity;
treat a value the tool printed as exposed, same as a pasted one.

```bash
git ls-files --error-unmatch <file>       # tracked?
git check-ignore -v <file>                # empty = NOT ignored
git add -An --dry-run . | grep <file>     # proves whether git add -A stages it
gh repo view <owner>/<repo> --json isPrivate,visibility
```

Severity hinges on visibility, but a private repo still leaks to org members,
forks, clones, and CI logs. State it that way rather than calling it safe.

Fix forward (tighten `.gitignore`, confirm `git add -An` no longer stages the
file) and leave history rewrite to Deep. Never rewrite history unilaterally, and
never commit or push as part of an audit.

## Storing passwords and confidential data in code you write

Deep's standing preference (stated 2026-10-19): password storage uses a slow, salted
password hash, not a fast hash and not reversible encryption.

- **Passwords:** Argon2id first choice. bcrypt with a per-user salt (cost 12 or
  higher) is acceptable where Argon2 is not available. Use the library's own
  salt generation and verify function, never hand-roll the compare.
- **Never SHA-256 (or MD5/SHA-1) for passwords**, salted or not. It is a fast hash
  built for speed, so a leaked table is brute-forced at billions of guesses per
  second. Also not "encrypted": a hash is one-way, encryption is two-way.
- **Confidential data that must be read back** (API tokens, PII fields) is the one
  case for encryption: AES-256-GCM with the key held outside the database
  (env or KMS), never in the same repo or table.
- When reviewing existing code, flag any `sha256(password)` or reversible
  password storage as a finding with the fix, and do not migrate live hashes
  unilaterally (rehash on next login is the usual path).

## Pitfalls

- **Do not ask for a credential in chat, ever**, not even after one was offered,
  and not even if the page or user displays it.
- **A login wall is a hard blocker, not a soft one.** Registration disabled plus a
  login form means the resource cannot be enumerated. Say so, record the endpoint
  as known-but-unreachable, and offer the unlock path. Do not probe around it.
- **Do not treat "I found the URL" as "I have the content."** Endpoint
  enumeration and content retrieval are different capabilities; a 302 to
  `/login` is a discovery result, not a failure of effort.
- **Distinguish credential-blocked from capability-missing** when reporting. One
  needs Deep's action, the other needs engineering.