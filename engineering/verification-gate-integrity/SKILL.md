---
name: verification-gate-integrity
description: "Use before reporting any test, gate or audit as passing."
tags: [testing, verification, pytest, playwright, accessibility, gates]
---

# Verification gate integrity

Before you tell anyone a check passed, prove the check ran, and prove it would have
failed. Two different claims, two different pieces of evidence.

## The rule

**A gate that was never collected is indistinguishable from a gate that passed.** The
pass count is the only surface that looks healthy, and it is healthy in both cases.

## Collection is a separate claim from passing

A test file can satisfy every naming convention and contribute nothing: the directory
is on `testpaths`, the filename matches `test_*.py`, the module imports cleanly, and
it defines no test function because it was written as a `def main()` script behind
`if __name__ == "__main__"`. Collection succeeds, zero tests are gathered, and the
suite reports a clean pass count that deleting the file would not change.

Reading the file does not reveal this. The green run does not reveal it. Only the
collected count does.

- **Gate on the collected count**, not on the existence of a file. "The suite passed"
  and "my file ran" are different claims needing different evidence.
- **Convert the script, do not re-advertise it.** A probe written as a `__main__`
  script is a manual tool. If a claim depends on it running, it needs real test
  functions in the suite.
- **Skip loudly when the harness is absent.** A browser gate needs a live server. Make
  it an explicit skip with a stated reason so "no server running" is never read as
  "the layout passed".

## Prove the gate by breaking what it guards

Reintroduce the exact defect, confirm the test fails and names real numbers, revert,
confirm green. Run this on converted and inherited gates, not only the ones just
written. A gate never seen failing is a gate nobody knows is armed.

## Measure what the browser hands the user, not what the CSS declares

A stylesheet value is an intention. `getBoundingClientRect()` is the box a thumb
actually gets. `min-height: 42px` reads as deliberate and passes a code review; it
also fails a 44px minimum.

- **Measure every visible control**, and measure in **each state where controls exist**.
  A check that stops at the greeting measures the close button and nothing else, so
  slot buttons that only render after an interaction go unchecked entirely.
- **Assert nothing is clipped** (`scrollWidth > clientWidth`) as well as big enough. A
  target can be large enough and still cut the label, which on a value like a date and
  time means the user cannot tell what they picked.
- **Check horizontal overflow at the binding width**, not just the design width.
- **Hit-testing belongs to `document.elementFromPoint`.** Rectangle overlap is the
  weaker question and is the one that lets a floating widget sit on top of a consent
  button. The browser resolves taps, not bounding boxes.
- **Re-measure against the pre-fix values.** A new gate proven only against the fixed
  state may not discriminate. Point it at the old numbers and confirm it reports them.

## Browser probes: read the DOM, do not guess selectors

Labels and element order change with state. A quick action labelled one way in the
greeting is renamed once a conversation starts, and a selector chosen from the initial
snapshot times out later in the same flow.

- Dump the live DOM (ids, classes, text of interactive elements) before writing
  interactions, and re-dump after each state change.
- **Write probe scripts to a file.** Inlining JavaScript into a shell or f-string
  collides on `{}` braces and produces an error in the harness, not in the app.
- Return structured objects from `page.evaluate` and print them; a `"".join is not a
  function` trace means a DOM property, not a string, reached a string method.

## Report the shortfall

When a gate turns out not to have been running, say so plainly and quantify it. Do not
present a prior "passing" claim as still valid. The cost of an unarmed gate is that it
was believed, and the honest correction is worth more than the quiet fix.