---
name: registry-canvas-verification
description: "Use when adapting registry canvas UI. Verify paint."
---

# Registry canvas verification

- Install the complete registry payload and commit its exact file set separately before adapting it. This gives runtime comparisons a real upstream baseline, including helper modules.
- Observe the host's actual theme selector in the registry palette helper. CSS aliases can update DOM text while a canvas retains its old palette.
- Read canvas pixel buffers for base and path layers separately. A nonblank base does not prove a route painted; a stationary fixture should have base pixels and zero path pixels.
- Keep strict-TypeScript compatibility changes type-only, without relaxing project gates. Compare parsed transpiled functions against the installed baseline, ignoring parentheses but not changed operations, to prove playback remained unchanged.
- Drive Replay, Pause, Play, hop keyboard selection, mobile taps and error recovery on the actual consumer page, not an isolated demo.
- Measure playback from Replay to its finished DOM state, excluding navigation and font loading. Capture mid-flight and reduced-motion finished frames separately.
- Assert the mid-flight frame, do not just shoot it: every row or label whose `data-state` is still `pending` must show the component's own placeholder, not its final value. A fork that swaps a state-aware cell for a static override (`row.hop.display ?? <RttCell state=... />`) silently drops the pending branch and gives away the ending while the packet is at hop 1. Keep the override inside the cell's pending check.
- Verify screenshot collision claims against actual marker-dot, label and control rectangles before changing layout.
- Reproduce baseline lazy-import test failures against the untouched base. Calibrate only the readiness wait and containing test budget, preserving assertions and production code.
- Inspect deployment integrations before publishing a no-deploy PR. An existing automatic feature preview is not permission to trigger another deployment. Hold publication for approval or an authorized branch exclusion.

Library sync remains subject to the product task's scope and publication authorization.
