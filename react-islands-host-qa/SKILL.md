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
- Stage local previews with synthetic records, verify served bundle bytes and host console output, and stop owned servers before the lifecycle transition. If a helper's CLI board comment is refused, use the primary board comment tool after verifying the URL. Do not bypass the refusal.
- When vision calls time out, report the exact images not inspected. Geometry and contrast results do not replace the missing visual inspection gate.
