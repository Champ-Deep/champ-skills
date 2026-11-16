---
name: react-islands-host-qa
description: "Use when mounting React islands in a legacy web host."
---

# React islands in a legacy host

- Search every caller and DOM identifier owned by the replaced surface before deleting it. Include profile-load and settings callbacks, draft-entry callers, speech handlers, logout and invalid-session cleanup. An isolated harness misses these paths.
- Set light text explicitly on colored buttons in scoped, unlayered CSS. A legacy unlayered preflight can override layered Tailwind utility colors while the utility class remains present. Verify computed color and background in the shipping page.
- Keep the scan dialog mounted when it owns an offline queue. Store the external open flag independently of the first React commit, and test same-tick open, native modal inertness, Tab cycling, Escape and returned focus.
- Make feed requests cancelable and token guarded. Remember whether a failed request was a reset or a next page, so retrying a changed filter cannot append old rows or use an old offset. Test a transport that ignores abort.
- Gate synthetic state fixtures by loopback hostname, label them visibly and prove the hooks are inert on a non-loopback host. Synthetic replies are not provider evidence.
- Separate browser API-double state proofs from real backend HTTP proofs. Extraction failure without a vision provider is a capability gap, not successful OCR. Real semantic retrieval can still be verified independently of a missing chat model.
- Use persistent selectors when a control changes its accessible name after activation. A locator targeting More's old aria-label cannot inspect Less after the click.
- A selected chip may paint its fill in an absolutely positioned sibling. A contrast checker walking only ancestor backgrounds reports false white-on-white results. Measure the actual sibling fill and report the numeric ratio, without weakening the check for ordinary text.
- Probe contrast only after the component's own transitions settle: wait on `el.getAnimations({subtree:true}).length === 0`, never a fixed sleep. Reduced motion still runs short colour transitions, and an animated chip swaps its label colour a frame before its fill moves, so an 80ms wait read white on white (ratio 1) in about one run of seven and turned a required verifier flaky. The same applies to focus rings: host transitions animate `outline-color`, so read the ring after it settles.
- Pick free loopback ports in every runner, for the static server and the backend alike. A literal port collides with another worker's server on this machine sooner or later, which is the exact QA defect the feed verifier was fixed for.
- On an async state change inside a modal (camera denied, extraction done), move focus to the new state's heading or first action. The unmounted button drops focus to body, and the native trap only recovers on the next Tab.
- Grade a runner by its assertion lines, not its exit code, when the host is loaded. Above a 1m load of about 25x the core count, these runners crash before asserting anything (`AppState is not defined` right after `goto(networkidle)`, `wait_for_selector` 30s, uvicorn not up in 20s), and vitest's 5s default times out a different test on the base commit too. Record `uptime` beside each run, count `^FAIL` lines (zero means contention), and rerun at lower load instead of carding the code. Twelve fresh page loads that read the host global at moderate load separate a harness race from a page defect.
- Stage local previews with synthetic records, verify served bundle bytes and host console output, and stop owned servers before the lifecycle transition. If a helper's CLI board comment is refused, use the primary board comment tool after verifying the URL. Do not bypass the refusal.
- When vision calls time out, report the exact images not inspected. Geometry and contrast results do not replace the missing visual inspection gate.
