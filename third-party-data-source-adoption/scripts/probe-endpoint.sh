#!/usr/bin/env bash
# Probe one endpoint for status, content type and whether it demands a key.
# Read-only. Prints four fields and exits non-zero only on a curl transport failure.
#
# Usage: scripts/probe-endpoint.sh 'https://api.example.com/v1/catalogue' [Bearer $KEY]
set -uo pipefail

url="${1:?usage: probe-endpoint.sh <url> [auth-header]}"
auth="${2:-}"

headers=$(curl -sS -o /tmp/probe-body.$$ -D - -w '\n%{http_code}' \
  ${auth:+-H "Authorization: $auth"} --max-time 20 "$url" 2>/dev/null)
code=$(printf '%s' "$headers" | tail -n1)
hdrs=$(printf '%s' "$headers" | sed '$d')

ctype=$(printf '%s' "$hdrs" | grep -i '^content-type:' | tr -d '\r' | head -1)
size=$(wc -c < /tmp/probe-body.$$ | tr -d ' ')
rm -f /tmp/probe-body.$$

# A 401/403 with a JSON error body usually means the endpoint is real but gated.
# A 200 with JSON means the operation itself is free: check what the free tier
# actually returns before budgeting the paid tier for it.
printf 'status:    %s\ncontent:   %s\nbytes:     %s\n' "${code:-?}" "${ctype:-none}" "$size"

# Report a keyless 200 distinctly: it is the case worth reading closely.
case "$code" in
  200) echo 'verdict:   reachable without credentials (read the body before assuming it is gated)' ;;
  401|403) echo 'verdict:   gated: real endpoint, credential required' ;;
  404) echo 'verdict:   absent: check the path against the provider reference' ;;
  *) echo 'verdict:   transport or server failure, retry before concluding' ;;
esac