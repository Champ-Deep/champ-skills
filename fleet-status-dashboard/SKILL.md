---
name: fleet-status-dashboard
description: "Poll chats, repos, and endpoints into one live status view."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [monitoring, dashboard, git, endpoints, cron, status, fleets]
    related_skills: [fix-proof-by-measurement, systematic-debugging]
---

# Fleet status dashboard

Deep asks for one view spanning many moving parts: which chats are running,
which repos are at risk, which services are actually up. The deliverable is a
live poll of real sources, never a summary of what was said about them.

## Procedure

1. **Enumerate the sources before writing anything.** Session state (SQLite,
   read-only), git state per repo, and deployed endpoints. Discover the
   projects directory rather than trusting a hand-kept list, so a repo nobody
   remembered cannot hide from the view.
2. **Identify each service by a small identifying fact** — the HTML `<title>`,
   one JSON field, a short response head. Never dump a response body into
   context; one page can bury the signal under a hundred kilobytes of CSS.
3. **Rank by risk, not by name.** Unpushed commits and missing remotes first,
   then dirty files, then divergence from upstream. The top row is the thing to
   fix today.
4. **Emit two shapes from one collector.** JSON for other tools, HTML for Deep
   to read. Keep collection logic single-source so they cannot disagree.
5. **Make staleness visible.** Stamp the render time. A dashboard whose
   timestamp is hidden is indistinguishable from a stale one.
6. **Verify by re-running, then register the job and fire it once.** A poller
   that has never actually run is not a poller.

## Distinguish "running" from "not finished"

An in-flight unit of work holds an unexpired lease row, not one whose
`ended_at` is null. These diverge by an order of magnitude in practice, and
conflating them makes finished work look concurrent. Always compare the expiry
against now: a stale lease row outlives its process by weeks and will otherwise
read as live.

Status dots, tab colours, and other UI affordances are **claims to verify, not
ground truth**. Corroborate against a source you can query before either
repeating or contradicting them.

## Change-gated watcher vs plain regenerator

Different tools, and the distinction decides whether the job is useful or a
nuisance.

| | Change-gated watcher | Plain regenerator |
|---|---|---|
| Purpose | notify only on change | keep a file current |
| Output | stable fingerprint | full render + timestamp |
| Timestamp | **must be absent** | **must be present** |
| On no change | suppress the agent run | rewrite anyway |

A timestamp in a change-gate makes every tick look changed and the agent talks
every cycle for nothing. A regenerator without a timestamp hides staleness.
Decide which kind you are writing before choosing the output shape.

## Verify the verifier before reporting a defect

The most expensive failure in this work is reporting a bug that does not exist.
Before telling Deep something is broken, answer in order:

1. **Is the check itself valid?** Would it flag known-good output too? Run it
   against something already known to be fine.
2. **Are the two values comparable at all?** Different producers, encodings,
   lengths, or algorithms do not compare. State what each side actually is
   before calling them equal or unequal.
3. **Is it an artifact of how I invoked it?** Wrong working directory, relative
   path, wrong argument nesting, wrong shell quoting, browser stack unavailable.

Only after all three come back clean may you report a defect. If a check fires
on legitimate content, say so and withdraw the claim in the same turn rather
than letting a false alarm stand.

False positives worth naming: single braces in generated CSS are valid, not
unrendered template braces; a stored digest of a different length than yours is
a different quantity, not a mismatch; a nonzero exit from a relative path run
in the wrong directory says nothing about the script.

## Output honesty

- If you could not visually confirm a rendered artifact because the browser
  stack was unavailable, verify it structurally (element counts, key strings,
  injected values) and **say plainly that it was not visually checked**. Never
  imply a check that did not happen.
- Distinguish verified fact from a claim carried over from another agent's
  transcript. The transcript is a claim; run the command.
- Report credential exposure by key NAME, value LENGTH, and token shape. Never
  print a secret value.
- When a number is worse than expected, lead with it. "182 commits unpushed" is
  the finding; the dashboard is only the delivery mechanism.
- Keep cron job prompts single-purpose. A poller prompt should emit one
  formatted line and forbid commentary, or it becomes an analyst that talks
  every tick.

## Support files

- `scripts/fleet_dashboard.py` — polls session state plus every repo under the
  projects directory into a self-refreshing HTML view. `--json` for machine
  consumption. Swaps nodes in place of reloading so scroll position survives.
- `references/deployed-endpoints.md` — verifying that a live service is the
  service its console label claims, and what each failure state looks like.
