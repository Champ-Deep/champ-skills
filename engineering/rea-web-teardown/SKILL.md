---
name: rea-web-teardown
description: "Use when tearing down a web product with the REA CLI."
---

# REA web teardown

REA (`npx -y rea-agents@latest`, repo NabilRFG12/Reverse-Engineer-anything) reverse engineers a web app from what its client ships. Use it when Deep says "recreate this product" for a SaaS: the public JS bundle of the logged-in portal usually leaks the route map, permission flags, and API shapes, which is a product map no marketing page gives you.

## Pipeline that works (v6.5.0)

```bash
source ~/.nvm/nvm.sh; mkdir -p ~/.hermes/cache/scratch/rea-<target> && cd $_
# 1. scenario file per URL (portal login page is the richest target)
cat > portal-scenario.json <<'EOF'
{"browser":{"mode":"launch","executable_path":"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome","headless":true},
 "start_url":{"url":"https://app.example.com/","query":[]},
 "environment":{"viewport":{"width":1440,"height":1000,"device_scale_factor":1},"locale":"en-US","timezone":"UTC","color_scheme":"light","reduced_motion":"reduce","service_workers":"block"},
 "actions":[{"step_id":"settle","action":"wait_for_timeout","duration_ms":5000}],
 "storage":{"cookies":[],"local_storage":[],"session_storage":[]},"secrets":[],
 "capture":{"after_each_step":[],"at_end":["url","dom","accessibility","history","storage","screenshot"],"events":["console","page-errors","network","workers","frames","popups","downloads"],"network":{"request_body":true,"response_body":true,"header_values":true}}}
EOF
# 2. capture
npx -y rea-agents@latest capture-browser-scenario portal-scenario.json --format json --full-output > portal-capture-raw.json
# 3. strip the npm warn line and the {ok,data} envelope: export-web-scripts wants the evidence object, not the envelope
python3 -c "import json;t=open('portal-capture-raw.json').read();json.dump(json.loads(t[t.index('{'):])['data'],open('portal-evidence.json','w'))"
# 4. export scripts into an ABSENT directory, then static analysis
npx -y rea-agents@latest export-web-scripts "$PWD/portal-evidence.json" "$PWD/portal-scripts" --format json --full-output > portal-export-raw.json
npx -y rea-agents@latest analyze-javascript-application "$PWD/portal-scripts/files" --format json --full-output > portal-static.json
```

## Where the product map hides

```bash
cd portal-scripts/files/origins/*/assets
grep -oh 'can_[a-z_]*' *.js | sort -u                 # permission flags = feature inventory
grep -oh '"/[a-z0-9/_:-]*"' Sidebar*.js | sort -u     # route map incl. internal ops consoles
grep -oh '/api/[a-z0-9/_${}.:-]*' *.js | sort -u       # API surface
grep -o 'formData.append([^)]*)' *.generated*.js        # payload field names
```

Unauthenticated captures only fetch the chunks the login page loads; `*.generated-*.js` files are the API clients that happened to ship. Lazy chunks behind login stay invisible. Say so in the writeup.

## Pitfalls

- Never log in or submit personal data; the public bundle is enough and anything else is unauthorised access.
- A capture that reports `terminal status unavailable` can still hold a valid evidence envelope; check `dropped events` before trusting network counts.
- `business.*` style subdomains often redirect to the marketing site; the capture then holds ad-tech, not product.
- Pair REA with the vendor's help center. REA gives structure and names; the docs give behaviour (cadence, limits, process). The PRD needs both, tagged [REA] vs [DOC].
- Copy the artifacts out of `~/.hermes/cache/scratch` into the vault effort folder; scratch is pruned after 24h.
