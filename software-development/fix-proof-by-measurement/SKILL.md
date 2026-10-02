---
name: fix-proof-by-measurement
description: "Use when proving a fix by number, not assertion."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [performance, measurement, verification, benchmarking, calibration, regression]
    related_skills: [systematic-debugging, dogfood]
---

# Proving a fix by measurement

Triggers: jank, jitter, laggy, sluggish, "feels slow", settling time, frame rate,
memory growth, load time, render cost, or any before/after claim about
behaviour. Also when a number is about to be quoted as proof.

## The rule

**A before/after number is a claim about a cause, and it is worthless until the
instrument is shown to distinguish the fixed build from the broken one.**

The failure this skill exists to prevent: you fix a jitter bug, write a probe,
the probe reports a clean `0.00`, you ship the number. Then you run the same
probe against the pre-fix build and it also reports `0.00`, because both versions
converge to the same equilibrium. The number was never measuring the thing you
fixed. Quoting it would be a fabricated result with a real-looking decimal
point.

## Procedure

1. **Build the baseline first, before the fix.** Capture the number on the broken
   build. A fix measured only afterwards has nothing to compare to, and "it
   feels better" is not a number.
2. **Write the probe** that samples a signal frame by frame through the user's
   actual gesture, not a synthetic one. For settling, drive a constant-velocity
   drag, release, and time how long motion continues. Measure a slow and a fast
   drag separately: a spring that rings only on a hard yank is a different bug
   from one that rings on every release.
3. **Make it deterministic.** Seed every source of randomness through
   `page.add_init_script` before the page's own scripts run. Without this, a
   cross-run delta measures the seed.
4. **Run a no-input control.** Identical load, no gesture, fingerprint at the
   same two wall-clock times. It must score exactly zero. If it does not, you
   are measuring the seed or the clock, not the change.
5. **Calibrate against the pre-fix build.** Run the identical probe on the old
   code. This is the step people skip, and it is the only step that gives the
   number meaning.
6. **Report the calibration in the same breath as the number.** State what the
   probe scored on the broken build, or state plainly that it could not be shown
   to discriminate. Never present an uncalibrated number as proof.

## Reading the calibration result

| Fixed | Pre-fix | Meaning |
|---|---|---|
| 83ms settle | still moving at 1500ms | Real. Quote both numbers. |
| 0.00 delta | 0.00 delta | **No discriminating power.** Both converge to the same fixed point. Do not quote the 0.00 |
| 0.00 delta | 0.00 at endpoint, differs mid-run | The endpoint is stable in both. Measure the trajectory, not the resting state |

## Instrument confounds

Each of these produces a confident, meaningless number, and each reads as a
finding about the app rather than about the harness:

- **A throttler that re-queues onto the real clock.** Patching
  `requestAnimationFrame` to drop frames but scheduling the retry on the saved
  original gives you N rates that are all the same rate. Assert the delivered
  frame counts actually scale before trusting any cross-rate comparison.
- **Unseeded randomness in the code under test.** Layout or physics code seeding
  from `Math.random()` makes every load a different starting state. The first
  cross-run delta is the seed, not the simulation.
- **Sampling an empty region.** A canvas corner is usually empty space, so
  reporting "no content" from it makes a healthy render look broken. Sample
  where content is, and assert content is present before trusting an absence.
- **Virtual time against a live page.** CDP `setVirtualTimePolicy` deadlocks
  with any page that also runs timers. Throttle the real frame clock instead.
- **An unthrottled scan.** Thousands of `getImageData` calls per run will blow
  the command timeout. Coarsen the grid before concluding the app is slow.
- **A background run that exits 0 with empty output.** Confirm the output had
  lines before treating the exit code as a result. A killed probe reports the
  same way a passing one does.

## When the probe times out repeatedly

Suspect the probe before the app. Run a minimal probe at the slowest target rate
that does nothing else: confirm frames are delivered, content is present, and no
page or console errors fired. That separates "the app is broken at this rate"
from "my instrument is wrong", and it is the question worth answering before
another attempt.

Do not present an unresolved instrument failure as a result. If the harness never
worked, the honest report is that the claim is unmeasured, and the code comment
should be narrowed to what you can defend.

## Gates for build-free apps

When an app is a single HTML file with a single inline `<script>`, no typechecker
sees it and no test loads the page, so a stray brace is not an exception you read
in a log, it is a blank screen that every existing check reports green.

Add a script that extracts the inline script and parses it, and run it first in
CI. Then prove the gate: reintroduce the exact syntax error, confirm the gate
fails and names the line, revert. A gate never seen failing is a gate that might
not work.

## Honesty rules when the number does not land

- Report the blocker, the attempts, and what is still unmeasured, in that order.
- Never dress a dead end up as a recommended approach.
- Prefer a smaller true claim to a larger one you cannot support. "The step
  count no longer varies with the display" is defensible; "frame-rate
  independent" is not, unless a calibrated probe earned it.
- If a test also passes on the broken build, say so plainly and withdraw the
  number rather than quoting it.

## Reference

`references/perf-probe-harnesses.md` has the worked probe: seeding, throttling,
canvas fingerprinting, settle timing, Playwright gotchas, and the usual shapes
of a jitter bug.
