---
name: settled-theme-audits
description: "Use when auditing animated light and dark theme changes."
---

# Settled theme audits

Load visual-verify first and run its live DOM audit on the authenticated production page.

When switching an existing app between light and dark, wait for CSS color transitions to finish before sampling contrast. Immediate sampling can mix the new background with the old foreground and report failures across correct navigation and buttons. Capture the transition separately if the animation itself is under review.

Before changing the palette in response to a cluster of contrast failures, rerun the same audit on a settled frame. Keep real failures and document a timing artifact rather than distorting the design to satisfy a mid-transition measurement.

For a screen reached after form submission, assert the transient toast has dismissed before taking its settled screenshot. Also capture the transient state when the toast is part of the requested flow. A toast covering a time in a capture is not proof that the underlying row layout is broken.

Audit the expanded mobile menu, not only its opener. A 44px opener does not prove the Home anchor, theme toggle or close button meets the same target floor.

Open every delivery screenshot and record machine findings and confirmed visual defects beside the artifact. Report hypotheses disproved by geometry so later passes do not repeat them.
