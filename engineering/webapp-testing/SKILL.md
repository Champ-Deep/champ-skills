---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

- **The launching shell's environment can shadow the venv.** A `PYTHONPATH`
  inherited from the agent runtime makes the venv interpreter import the wrong
  packages (or fail on a module that is plainly installed), so the app dies at
  import time and looks like a missing dependency. Start the server with the
  variable unset (`env -u PYTHONPATH .venv/bin/python -m ...`, or a wrapper
  script that unsets it) and hit one route before debugging application code.

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

⚠️ **Exception: animated pages never go idle.** A page with a continuous canvas
animation, globe, ticker, or polling loop keeps issuing requests, so `networkidle`
times out even though the app is healthy. On those pages wait for `load` plus
`page.wait_for_selector('<known element>')` and a short `wait_for_timeout` instead,
and treat the timeout as a property of the page, not a failure of the app.

## Waiting without `eval`: respect the page's CSP

`page.wait_for_function("...")` passes a **string**, which Chromium evaluates with
`eval`. Any page shipping a strict `Content Security Policy` (typical for a Cloudflare
Worker: `script-src 'self'`) rejects it with `EvalError: Evaluating a string as JavaScript
violates ... 'unsafe-eval'`, and the test dies even though the app is healthy. The failure
names CSP, not a broken selector, so do not start editing the page.

✅ **Do** express every wait as a locator or assertion, which run as real selectors and
never eval:

```python
from playwright.sync_api import sync_playwright, expect

page.locator('#form-status.success').wait_for(state='visible')   # state wait
expect(page.locator('#category')).to_have_value('beauty')        # value assertion
expect(page.locator('#navigation')).to_be_visible()              # visibility assertion
```

Rule of thumb: if your wait or assertion is a JavaScript string in `wait_for_function` or
`page.evaluate`-style predicate, rewrite it as `expect(locator)` or `locator.wait_for`.
Reserve string predicates for pages you control that ship no `script-src` CSP, and even
there the locator form is the safer default because the same test keeps working if a CSP
lands later.

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation