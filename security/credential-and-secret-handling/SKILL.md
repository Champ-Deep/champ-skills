---
name: credential-and-secret-handling
description: "Use when a credential lands in chat or a URL needs auth."
version: 1.0.0
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

## Storing a credential in the vault

"Save it in my Celsus vault" does NOT mean write the value into a markdown note.
Vault notes are searched, diffed, exported, and synced, so a plaintext secret
there leaks through every one of those paths. The vault route is the masked
browser prompt; the vault is for the reference, not the secret.

If a login page is not currently open, say what is needed and stop there rather
than inventing a storage location.

## Secrets in repos

When auditing a file that may hold live values, report key NAMES, value LENGTH,
and a token-shaped yes or no. Never print the value, not even truncated.

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