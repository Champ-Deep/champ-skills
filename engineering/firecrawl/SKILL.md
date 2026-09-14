---
name: firecrawl
description: >
  Firecrawl is the PRIMARY browser and web access tool for this workspace. Use it
  for any web interaction, reading, research, or scraping task BEFORE reaching for
  the Chrome extension or computer-use tools. Firecrawl runs a managed remote
  browser fleet — no user screen involved, no approval dialogs, fully parallel.
  MANDATORY TRIGGER for: reading any public web page, searching the web, scraping
  docs, checking domain availability, reading provider documentation, researching
  anything online, crawling a site, extracting structured data from URLs, or
  interacting with JS-heavy pages. The Chrome extension and computer-use are
  LAST RESORT — only needed when a task explicitly requires the user's logged-in
  authenticated session AND Firecrawl Browser Sandbox cannot inject the credentials.
  When in doubt, try Firecrawl first.
---

# Firecrawl — Primary Browser Layer

Firecrawl is a managed remote browser environment for AI agents. It renders
JavaScript, handles dynamic content, and returns clean LLM-ready data. It runs
in Firecrawl's cloud — completely independent of the user's machine and browser.

## Priority Hierarchy

Always follow this order. Move down only when the tier above cannot complete the task.

| Tier | Tool | When |
|------|------|------|
| 1 | **Firecrawl** (this skill) | Any public-web task: reading, searching, scraping, interacting |
| 2 | **WebFetch / WebSearch** | Firecrawl is rate-limited or the page is static and simple |
| 3 | **Claude in Chrome extension** | Task requires user's authenticated session (logged-in dashboards) |
| 4 | **computer-use** | Native desktop apps only, no web equivalent available |

The Chrome extension should feel like a last resort — something you reach for
only when Firecrawl's Browser Sandbox genuinely cannot handle the auth requirement.

## Key Setup

Keys are stored in the sandbox env file. Source it before every Firecrawl call:

```bash
source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env
# Provides: $FIRECRAWL_KEY_DEFAULT and $FIRECRAWL_KEY_DOCKER
# Use $FIRECRAWL_KEY_DEFAULT for all standard operations
```

Base URL: `https://api.firecrawl.dev/v1`
Auth header: `Authorization: Bearer $FIRECRAWL_KEY_DEFAULT`

---

## Mode 1: Scrape — Single URL

Use for: reading docs, checking a page, pulling content from any public URL.

```bash
source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env

curl -s -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/docs",
    "formats": ["markdown"],
    "onlyMainContent": true
  }' | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d['data']['markdown'] if d.get('success') else f'Error: {d}')
"
```

Available formats: `markdown`, `html`, `rawHtml`, `screenshot`, `links`.
Set `onlyMainContent: true` to strip nav/footer noise. Omit it when you need full page structure.

**Parallel scraping** — batch multiple URLs in one call:

```bash
curl -s -X POST https://api.firecrawl.dev/v1/batch-scrape \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://url1.com", "https://url2.com", "https://url3.com"],
    "formats": ["markdown"],
    "onlyMainContent": true
  }'
```

---

## Mode 2: Search — Web Search + Scrape

Use for: finding current information, researching a topic, getting live web results.
Replaces WebSearch for most tasks — returns full page content, not just snippets.

```bash
source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env

curl -s -X POST https://api.firecrawl.dev/v1/search \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Porkbun API domain registration pricing 2025",
    "limit": 5,
    "scrapeOptions": {
      "formats": ["markdown"],
      "onlyMainContent": true
    }
  }' | python3 -c "
import sys, json
d = json.load(sys.stdin)
for r in d.get('data', []):
    print(f\"### {r.get('title')} — {r.get('url')}\")
    print(r.get('markdown', r.get('description', ''))[:1000])
    print()
"
```

Use `category: "research"` for academic/in-depth results, `category: "github"` for code repos.

---

## Mode 3: Browser Sandbox — Interact with JS Pages

Use for: pages that require clicks, form fills, waiting for dynamic content,
or multi-step navigation on public pages.

The Browser Sandbox keeps a live browser session alive so you can chain interactions.

### Step 1: Start the session (scrape creates a persistent browser)

```bash
source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env

RESPONSE=$(curl -s -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown"],
    "keepAlive": true
  }')

SESSION_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin).get('sessionId',''))")
echo "Session: $SESSION_ID"
```

### Step 2: Interact via natural language prompt

```bash
curl -s -X POST https://api.firecrawl.dev/v1/scrape-execute \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d "{
    \"sessionId\": \"$SESSION_ID\",
    \"prompt\": \"Click the Pricing tab and wait for the page to load\"
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('markdown','') or d)"
```

### Step 2 (alternative): Interact via Playwright code

```bash
curl -s -X POST https://api.firecrawl.dev/v1/scrape-execute \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d "{
    \"sessionId\": \"$SESSION_ID\",
    \"code\": \"await page.click('#pricing-tab'); await page.waitForLoadState('networkidle');\"
  }"
```

### Step 3: Cleanup

```bash
curl -s -X DELETE "https://api.firecrawl.dev/v1/scrape-browser/$SESSION_ID" \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT"
```

**Keep prompts small and focused.** One action per call is more reliable than
chaining many actions in a single prompt. Use Playwright code when you need
precision (specific selectors); use NL prompts when the page structure is unknown.

---

## Mode 4: Extract — Structured JSON from URLs

Use for: pulling specific structured data from one or more pages (pricing tables,
contact info, product specs, any defined schema).

```bash
source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env

# Start extract job
JOB=$(curl -s -X POST https://api.firecrawl.dev/v1/extract \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://porkbun.com/products/domains/TLD/chart"],
    "prompt": "Extract all TLD names and their registration prices",
    "schema": {
      "type": "object",
      "properties": {
        "tlds": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "tld": {"type": "string"},
              "price_per_year": {"type": "string"}
            }
          }
        }
      }
    }
  }')

JOB_ID=$(echo $JOB | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

# Poll until complete (usually 10-30 sec)
sleep 15
curl -s "https://api.firecrawl.dev/v1/extract/$JOB_ID" \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(json.dumps(d.get('data', d), indent=2))
"
```

Extract is asynchronous. Always poll the job ID. Status will be `processing`, then `completed`.

---

## Mode 5: Map — Discover All URLs on a Site

Use for: understanding a site's structure before deciding what to scrape,
finding specific pages within a domain.

```bash
source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env

curl -s -X POST https://api.firecrawl.dev/v1/map \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com",
    "search": "api authentication"
  }' | python3 -c "
import sys, json
d = json.load(sys.stdin)
for url in d.get('links', [])[:20]:
    print(url)
"
```

Use `search` param to filter URLs by keyword. Fast and cheap (1 credit vs 1 per page).

---

## Mode 6: Crawl — Multi-Page Site Traversal

Use for: pulling full documentation sites, building a knowledge base from a domain.
Crawl is async and can take minutes. Use Map first to scope what you need.

```bash
source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env

# Start crawl
JOB=$(curl -s -X POST https://api.firecrawl.dev/v1/crawl \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com",
    "maxDepth": 2,
    "limit": 20,
    "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": true}
  }')

CRAWL_ID=$(echo $JOB | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

# Check status
curl -s "https://api.firecrawl.dev/v1/crawl/$CRAWL_ID" \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"Status: {d.get('status')} — {d.get('completed')}/{d.get('total')} pages\")
"
```

---

## Browser Session — Full Playwright Control (Advanced)

For complex multi-step workflows where you need persistent browser state across
many operations. More powerful than the interact mode above.

```bash
source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env

# Create a browser session
SESSION=$(curl -s -X POST https://api.firecrawl.dev/v1/browser \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d '{"options": {"headless": true}}')

SESSION_ID=$(echo $SESSION | python3 -c "import sys,json; print(json.load(sys.stdin).get('sessionId',''))")

# Execute Playwright code against the live session
curl -s -X POST https://api.firecrawl.dev/v1/browser-execute \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT" \
  -H "Content-Type: application/json" \
  -d "{
    \"sessionId\": \"$SESSION_ID\",
    \"code\": \"
      await page.goto('https://example.com');
      await page.click('button#signup');
      const text = await page.textContent('h1');
      return text;
    \"
  }"

# Always clean up
curl -s -X DELETE "https://api.firecrawl.dev/v1/browser/$SESSION_ID" \
  -H "Authorization: Bearer $FIRECRAWL_KEY_DEFAULT"
```

---

## When Chrome Extension IS Still Required

Firecrawl runs its own browser with no access to the user's accounts.
For these specific tasks, fall through to the Chrome extension:

- Generating API tokens inside a provider dashboard (Vercel, GitHub, Porkbun)
- Completing a purchase that requires the user's payment session
- Any form submission that requires the user to be logged in

Even then, use Firecrawl first to read the UI documentation and map the exact
click path, so the Chrome session is as short as possible.

---

## Credit Awareness

Each Firecrawl API call consumes credits. Be efficient:

- Use `onlyMainContent: true` on scrapes to reduce token cost
- Use Map before Crawl to scope what pages you actually need
- Batch scrapes (`/v1/batch-scrape`) instead of looping individual scrape calls
- Extract is async and costs more — use for structured data needs only
- Search with `limit: 5` is usually enough; don't over-fetch

---

## Helper Function (save in scripts for reuse)

```python
# /sessions/vibrant-elegant-lamport/fc.py — quick firecrawl helper
import subprocess, json, os

def fc_scrape(url, formats=None, main_content=True):
    """Scrape a URL via Firecrawl. Returns markdown string."""
    env = {}
    result = subprocess.run(
        ['bash', '-c', 'source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env && echo $FIRECRAWL_KEY_DEFAULT'],
        capture_output=True, text=True
    )
    key = result.stdout.strip()
    
    import urllib.request
    payload = json.dumps({
        "url": url,
        "formats": formats or ["markdown"],
        "onlyMainContent": main_content
    }).encode()
    
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        d = json.loads(resp.read())
    return d.get("data", {}).get("markdown", "") if d.get("success") else str(d)

def fc_search(query, limit=5):
    """Search the web via Firecrawl. Returns list of {title, url, markdown}."""
    result = subprocess.run(
        ['bash', '-c', 'source /sessions/vibrant-elegant-lamport/.secrets/firecrawl.env && echo $FIRECRAWL_KEY_DEFAULT'],
        capture_output=True, text=True
    )
    key = result.stdout.strip()
    
    import urllib.request
    payload = json.dumps({
        "query": query,
        "limit": limit,
        "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True}
    }).encode()
    
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/search",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        d = json.loads(resp.read())
    return d.get("data", [])
```
