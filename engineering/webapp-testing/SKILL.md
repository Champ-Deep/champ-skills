---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots (including authenticated screens for demo kits and video briefs), and viewing browser logs.
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

  - **An old browser build crashes on a modern page and blames the app.** A
  bundled Chromium older than the page's baseline dies on APIs it never shipped
  (`Element.roundRect` and friends) with no JS error, in a flow that works fine
  in a normal window. Before reporting a page bug, relaunch the same step
  against a current browser: `p.chromium.launch(channel="chrome", headless=True)`
  or `executable_path` to an installed Chrome. When driving a third-party app or
  hosted onboarding whose baseline you do not control, pick the current browser
  channel from the first launch instead of discovering it after a crash.

  ❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

⚠️ **Exception: animated pages never go idle.** A page with a continuous canvas
animation, globe, ticker, or polling loop keeps issuing requests, so `networkidle`
times out even though the app is healthy. On those pages wait for `load` plus
`page.wait_for_selector('<known element>')` and a short `wait_for_timeout` instead,
and treat the timeout as a property of the page, not a failure of the app.

## Capturing a set of real screens (demo, walkthrough, video brief)

When the deliverable is a shot list other people read (a demo kit, a handout, a
prompt for an external video studio), capture before you write:

1. **Put the capture script inside the repo tree** (e.g. `<repo>/capture.mjs`,
   untracked, deleted after the run). Node resolves `node_modules` by walking up
   from the script's own path, not from the working directory, so a script written
   to scratch or `/tmp` cannot import the repo's Playwright or app modules no
   matter where you invoke it from (Node and Bun both resolve upward from the
   script's path, not the cwd). The symptom is a bare `ERR_MODULE_NOT_FOUND`
   for a package that is plainly installed.
2. **Seed the minimum data the screens need** (one campaign, one uploaded list,
   one populated state) before shooting. An empty app produces a shot list that
   describes nothing.
3. **Reach authenticated screens by minting a session, not by driving the login
   form**: call the app's own auth API (register / invite / login endpoint) with
   `curl`, then inject the cookie into the browser context
   (`context.add_cookies([{name, value, domain, path}])`). One call beats selector
   churn, and it works on routes that only render for a live session.
4. **Revoke that session and delete the seeded account when the captures are
   done.** A throwaway session left alive is an open door on a production host.
5. **When the user offers his own session, use it instead of minting one.** Open a
   visible browser window, have him sign in once, then drive that signed-in
   context: his real account carries his real data, so the capture shows the
   screen he will actually see, where a seeded throwaway shoots an empty workspace
   and produces copy that describes rows nobody has. This is the reliable route
   past an auth gate whose flow you cannot call directly. The two rules above bind
   only sessions you created: never log out of, clear, or revoke his session when
   the run ends.
5. **Open every capture before writing copy that describes it.** Narration,
   walkthrough steps and video-prompt copy must state only what the pixels show:
   exact control labels, wording of empty states, send caps and spend limits read
   from the source at capture time. What the code suggests a screen says and what
   it renders differ at precisely the moment the copy matters, and a brief that
   promises a nonexistent screen ships a broken demo.
6. **Report the capture list as file names** alongside the brief, so the reader
   opens the same frames you verified.

## Driving a hosted onboarding or wizard flow

Multi-step setup flows (account setup, first-run checklists, plan selection) are
reworded between steps and between releases, so one hard-coded label per step breaks
on the step you least expect.

1. **Give each step an ordered alternation list of candidate labels** ("Continue",
   "Skip for now", "Start using X"), click the first match found, and log which
   candidate hit so the next run starts from the list that worked.
2. **Screenshot after every step.** The next screen's copy decides the next
   selector, and reading the rendered words beats guessing from the product's docs.
3. **Distinguish "unreachable" from "not entitled".** A step that reports a
   service as unreachable may just be a cold start or a timeout; the product's own
   runtime entitlement call (see the `competitive-research-verification` skill)
   tells you whether the feature is gated by plan, which is a different finding
   and changes the evaluation.

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