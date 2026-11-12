#!/bin/sh
# OpenRouter key health before a paid panel run. Prints limit fields only, never the key.
# Run by path; do not paste the body into a kanban comment (the board redactor mangles inline secret reads).
# Usage: sh key_health.sh [VAR_NAME]   default OPENROUTER_API_KEY
exec python3 - "${1:-OPENROUTER_API_KEY}" <<'PY'
import json, pathlib, sys, urllib.request
name = sys.argv[1]
lines = (pathlib.Path.home() / ".hermes" / ".env").read_text().splitlines()
vals = [l.split("=", 1)[1].strip().strip('"').strip("'") for l in lines if l.startswith(name + "=")]
if not vals or not vals[0]:
    sys.exit(f"{name} missing or empty in ~/.hermes/.env")
req = urllib.request.Request("https://openrouter.ai/api/v1/key", headers={"Authorization": "Bearer " + vals[0]})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.load(r).get("data", {})
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}")  # status only, never the body or the key
print({k: d.get(k) for k in ("limit", "limit_remaining", "usage_weekly")})
PY
