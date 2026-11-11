---
name: browser-agent-automation
description: "Use when driving a browser with a model, not selectors."
---

# Browser agent automation

A browser agent picks its own actions from what is on the page. That is a different job from scripting selectors against an app you control, and it fails in different ways. This covers the class: stealth engines, decision-model loops, and the verification that makes the results trustworthy.

For hand-written Playwright against a local webapp you own, use `webapp-testing` instead. For fetching a page that returns 403 or sits behind a bot wall, use `blocked-page-recovery`.

## Before writing any code, settle three things

1. **Does the tool the user named actually exist, and is it what they meant?** Search for it and read its README before designing around it. Users misspell, misremember, and conflate adjacent tools, and a plan built on the wrong tool wastes a whole build. When a named component is a library, a model, or a browser, confirm the name and the role separately: a name can be real while the role is misattributed. If a component would need a fresh toolchain on the machine, say so before it enters the plan, not after.
2. **Is the decision layer or the browser layer the new work?** Forking an existing agent and swapping its transport is a different job from writing a fresh loop, and it is usually the cheaper one. Ask which, and prefer the fork when a proven decision architecture exists.
3. **What proves success?** Write the independent check before the code, not after. See the verification gate below.

## Porting a loop between browser engines

A DOM reader is almost always portable. A transport usually is not.

- **Firefox has no CDP.** Any layer built on the Chrome DevTools Protocol must be rewritten for Playwright, not configured. CDP calls map like this: `Runtime.evaluate` becomes `page.evaluate`, `Input.dispatchMouseEvent` becomes `page.mouse`, `Input.insertText` becomes `page.keyboard.insert_text`, `Page.captureScreenshot` becomes `page.screenshot`, `Target.createTarget` becomes a new context and page.
- **Check the reader for engine-specific APIs before planning the port.** Grep the extracted script for `chrome.`, `window.chrome`, CDP calls, and vendor-prefixed animation frames. Pure DOM plus standard ARIA runs unmodified on a current engine, which is what makes a reader-plus-transport split worth preserving.
- **Inherit the safety properties, rewrite the mechanism.** When forking, keep whatever consumes a decision once, logs execution before observing the result, and refuses to retry a mutation. Those are the properties that prevent double-clicks and silent no-ops. Re-derive them from the upstream code and say which are inherited.

## Pitfalls that produce a confident wrong answer

These do not raise. The agent reports success and the result is wrong, which is worse than a crash.

1. **A click that navigates reads the page it just left.** After dispatching a click, the new navigation has not begun, so `document.readyState` correctly reports the *old* document as complete. Polling `readyState` returns the pre-navigation page, the loop sees no change, and the agent concludes it is finished on the wrong URL. Wait for `page.url` to actually differ from the pre-click URL, and only then wait for load. Waiting on URL movement costs nothing when a click changes nothing on the page.
2. **`DONE` is a claim, not evidence.** A model reporting completion proves nothing about the page state. Always finish with an independent assertion evaluated in the page, and print a literal VERIFIED or NOT VERIFIED. This is the single highest-value line in the whole tool: both real bugs in the first build of a stealth-browser agent were invisible to the model and caught instantly by the assertion.
3. **Playwright dispatches the wheel at the current mouse position**, which defaults to the top-left corner and can land outside the page's scroll container. Park the mouse mid-viewport before scrolling.
4. **Synthetic actions carry no role.** Generated scroll and wait controls have no `role` key. Any code reading `action["role"]` over the full action list raises `KeyError` on those entries, which reads as a broken reader rather than a bad assumption. Filter or use `.get()`.
5. **Do not name a scratch script after a stdlib module.** A probe called `inspect.py` shadows the stdlib `inspect` that dataclasses imports, and the resulting circular-import error points at your own module instead of the real cause.
6. **Check free disk before installing a browser stack.** A patched browser plus its extras is hundreds of megabytes, and an install that dies partway leaves a venv that looks present but cannot launch. Clearing regenerable caches is usually enough, but ask before deleting anything on the user's machine and report the space reclaimed.

## An authenticated walkthrough belongs to the user's session

Driving a hosted app with the user's own account, for a demo, a staging walkthrough or feedback on their real data, is a different job from scripting an app you control:

1. **Never enter a credential.** Check the password manager for a saved login on that exact origin first and fill it from there; if there is none, open the browser **headed** on the login page and let the user sign in themselves. A locked or empty password manager is a reason to hand over the window, never a reason to type a password yourself or ask for one in chat.
2. **Build one session and reuse it.** Launch a persistent context with `--remote-debugging-port=<port>` and reconnect from later scripts with `p.chromium.connect_over_cdp("http://localhost:<port>")`. A fresh context per call throws away the login the user just completed, so every subsequent screen reads unauthenticated and the walkthrough silently degrades into screenshots of login walls.
3. **Hold the window open.** The script that opens the browser must not exit when it finishes its checks, because process exit closes the browser and the session with it. Keep it as a long-lived background process, and put navigations and assertions in separate short-lived scripts that attach over CDP.
4. **Keep the profile off the user's live browser directory.** Point the persistent profile at a scratch path: a running browser holds a lock on its own profile, so a second browser on that path either fails to start or risks the user's real session.
5. **Google does not survive a copied profile.** With Hermes `use_real_profile`, GitHub opened signed in but Google opened signed out, though the snapshot held the same Google cookies as the live profile (likely device-bound session credentials). Route Gmail, Calendar and Drive through the `gog` CLI or the connectors. For Google web UI with no API, use a dedicated Chrome user-data-dir the user signs into once and attach with `/browser connect`, because the real-profile snapshot re-syncs its auth files on every fresh session and drops any login made inside it.
6. **Report the boundary you actually crossed.** Name the screens you drove authenticated and the ones you only saw behind a gate you never crossed.

Two more ways the same boundary gets crossed, both on a vendor's console rather
than on an app you control:

- **A step-up verification ends the run, it does not start a workaround.** When a
  console action pops "enter the code we emailed you", stop there: that code
  belongs to the user's inbox. Trigger the action if triggering is free, then
  hand over the exact path (app > instance > section > control) and say the mail
  is from you. Never ask him to paste the code into chat, and do not go and fetch
  it from his mailbox on your own initiative; either turns a 30-second console
  click into a credential handoff. If he explicitly tells you to pull the code
  from his mail, that is his call to make, not a default you infer.
- **Match the control by exact text and assert the count before clicking.** A
  vendor settings page puts the benign control and the irreversible one ("delete
  instance", "set all passwords as compromised") in the same scroll, so a fuzzy
  selector or a `.first()` on a label match can fire the wrong one. Filter on an
  exact trimmed-text match, require exactly one hit, and only then click; read
  the page's own confirmation state back afterwards instead of assuming the
  click landed.

## When no browser server is running: drive headless Chrome over CDP directly

The Hermes browser tools need a browser server on port 9377. `~/.hermes/tools/camofox` is only
the client library: it has no `start` script, so `npm start` there fails with `Missing script:
"start"` and no amount of retrying installs the server. Do not spend a turn on it. Node 24 has a
global `WebSocket`, so a single `.mjs` drives headless Chrome with no dependency and no venv:
launch `--headless=new --remote-debugging-port=<port>`, read `/json` for the page target, then use
`Runtime.evaluate`, `Input.dispatchMouseEvent`, `DOM.setFileInputFiles` and `Page.captureScreenshot`.
Two traps, both silent:

1. **Seeding `localStorage` needs the target origin first.** A fresh target sits on `about:blank`,
   where `setItem` throws `SecurityError: Access is denied`. Navigate to the app, *then* seed, then
   reload.
2. **A hash-only navigation does not remount a SPA.** Calling `Page.navigate` to the same URL with
   a different `#fragment` is a same-document navigation, so React never re-mounts and the app keeps
   whatever state it mounted with (a seeded key reads as empty and every request 401s). Use
   `Page.reload` after seeding, and drive tabs by clicking them.

Read values back rather than trusting the click: a React-controlled input needs the native setter
plus a dispatched `input` event, and a real `Input.dispatchMouseEvent` at the element's centre
beats `.click()` when a button is disabled, since clicking a disabled button silently does nothing.

## Verification gate

An agent run is not done until all three hold:

1. **An offline transport test that makes no model calls.** Assert that the right element was actually affected, not merely that no exception was raised: read the real DOM value back after a select, read the real input value after typing, and read the page's own handler output after a click. Transport bugs produce a wrong click, not an exception.
2. **Stealth asserted, not assumed.** Check `navigator.webdriver` is false and `navigator.plugins` is non-empty on the real engine, not in a unit test.
3. **A live canary with an independent assertion**, repeated at least twice to show repeatability. Report repeats of one task as repeatability, never as a reliability benchmark.

## Reporting

State the verified results in a table with the run, the outcome, and the time. List the real bugs found and what each one would have looked like without the assertion. State limits plainly: a stealth engine is slower than the default, and that is the trade being made. Never present a single verified run as a benchmark, and never claim a number the build has not earned.
