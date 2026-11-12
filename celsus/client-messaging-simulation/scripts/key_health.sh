#!/bin/sh
# Model gateway key health before a paid panel run. Prints limit fields only, never the key.
# The key must already be in the environment. This script does not read a secret file.
# Usage: sh key_health.sh [VAR_NAME]
exec python3 - "${1:-MODEL_GATEWAY_KEY}" <<'PY'
import json, os, sys, urllib.request
name = sys.argv[1]
val = os.environ.get(name, "").strip().strip('"').strip("'")
if not val:
    sys.exit(f"{name} missing or empty in the environment")
req = urllib.request.Request("https://openrouter.ai/api/v1/key", headers={"Authorization": "Bearer " + val})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.load(r).get("data", {})
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}")  # status only, never the body or the key
print({k: d.get(k) for k in ("limit", "limit_remaining", "usage_weekly")})
PY
