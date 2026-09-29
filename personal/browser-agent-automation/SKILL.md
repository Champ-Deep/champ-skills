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

## Verification gate

An agent run is not done until all three hold:

1. **An offline transport test that makes no model calls.** Assert that the right element was actually affected, not merely that no exception was raised: read the real DOM value back after a select, read the real input value after typing, and read the page's own handler output after a click. Transport bugs produce a wrong click, not an exception.
2. **Stealth asserted, not assumed.** Check `navigator.webdriver` is false and `navigator.plugins` is non-empty on the real engine, not in a unit test.
3. **A live canary with an independent assertion**, repeated at least twice to show repeatability. Report repeats of one task as repeatability, never as a reliability benchmark.

## Reporting

State the verified results in a table with the run, the outcome, and the time. List the real bugs found and what each one would have looked like without the assertion. State limits plainly: a stealth engine is slower than the default, and that is the trade being made. Never present a single verified run as a benchmark, and never claim a number the build has not earned.
