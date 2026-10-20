# Google Workspace from the terminal

For when the job is Drive/Gmail/Chat operations by script or agent shell
instead of connector tool calls: publish/ingest jobs, scheduled syncs, Chat
message posting.

## Tool choice

| Tool | What it is | Notes |
|---|---|---|
| `gog` | Single open-source binary for Gmail, Calendar, Chat, Drive, Docs, Sheets, Slides, Admin, and more | Installed on Deep's Mac. JSON output, `--dry-run`, `--no-input`, per-service scopes |
| `gws` | Google's `googleworkspace/cli`, Discovery-Service driven, ships agent skills | Install as `npm i -g @googleworkspace/cli` or `brew install googleworkspace-cli`. Needs its own Google Cloud project + `gws auth setup` |

**Trap: `brew install gws` is a different, unrelated project** (git workspace
management). The Google Workspace CLI's brew formula is
`googleworkspace-cli`.

## gog procedure

1. `gog auth list` to see authorized accounts and scopes; `gog auth services`
   for the full scope table per service.
2. Authorize per account: `gog auth add <email>` (opens a browser round trip).
   Select with `--account <email>` per call; multiple accounts coexist.
3. Read scopes before promising a capability: Chat scopes only work for a
   **Workspace (non-gmail.com) account**, so a gmail-only auth cannot post to
   Chat spaces even though the command exists.
4. Script with `--json` (or `--plain` for TSV) and preview writes with
   `--dry-run` first; `--no-input` for non-interactive runs.

## Pitfalls

- **`oauth2: "invalid_grant"` on every call means the stored refresh token is
  dead, not that the query is wrong.** Re-run `gog auth add <email>`; do not
  debug the command or the API path.
- **Account identity beats command syntax.** Commands that exist will fail
  with a domain error if the authorized account is the wrong type (gmail vs
  Workspace). Check `gog auth list` before anything else.
- **Native Google files have no local bytes under Drive for desktop**; the
  mount holds links. Pull content through `gog docs export` /
  `gog drive download`, not by reading the mount path.
