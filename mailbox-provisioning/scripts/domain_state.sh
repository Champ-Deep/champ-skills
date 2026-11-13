#!/usr/bin/env bash
# domain_state.sh <domain> [domain...]
# Live registration and mail-hosting state for one or more domains.
# Answers, per domain: registered?, who hosts it (NS), what receives mail (MX),
# and which SPF / DMARC / DKIM-selector records are published.
# Read-only: no registrar, provider or zone is touched.
#
# Reading the output:
#   registered      -> RDAP 200 from a server that serves that TLD
#   NOT registered  -> RDAP 404. Confirm at checkout: this is a race, not a hold,
#                      and a 404 can also mean this TLD has no RDAP endpoint.
#   MX = registrar forwarding + SPF for the forwarder
#                      -> parked or forwarded, no mailboxes are hosted there
#   NS empty          -> never delegated: nothing is configured
#   DMARC <none>      -> publish one before any send; p=reject with rua/ruf to an
#                      address on a different domain than the sending domain
set -u

[ $# -ge 1 ] || { echo "usage: $0 <domain> [domain...]" >&2; exit 2; }

for d in "$@"; do
  tld="${d##*.}"
  case "$tld" in
    com) rdap="https://rdap.verisign.com/com/v1/domain/$d" ;;
    net) rdap="https://rdap.verisign.com/net/v1/domain/$d" ;;
    *)   rdap="https://rdap.org/domain/$d" ;;
  esac
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 15 -L "$rdap")
  if [ "$code" = "200" ]; then reg="registered"; else reg="NOT registered (rdap=$code)"; fi

  printf '== %s  [%s]\n' "$d" "$reg"
  printf '   NS    %s\n' "$(dig +short NS "$d" | tr '\n' ' ')"
  printf '   MX    %s\n' "$(dig +short MX "$d" | tr '\n' ' ')"
  spf=$(dig +short TXT "$d" | grep -i 'v=spf1' | tr '\n' ' ')
  printf '   SPF   %s\n' "${spf:-<none>}"
  dm=$(dig +short TXT "_dmarc.$d" | tr '\n' ' ')
  printf '   DMARC %s\n' "${dm:-<none>}"
  # Common selector names; a hit proves the provider's DKIM is published.
  for sel in zoho zmail google selector1 selector2 s1 s2 k1 mail; do
    k=$(dig +short TXT "${sel}._domainkey.$d" | tr -d '\n' | cut -c1-40)
    [ -n "$k" ] && printf '   DKIM  %s._domainkey: %s...\n' "$sel" "$k"
  done
done
