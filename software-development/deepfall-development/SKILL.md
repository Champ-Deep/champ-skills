---
name: "deepfall-development"
description: "Use when changing or deploying the Deepfall game repo."
---

# Deepfall development

> **Security gate (mandatory):** every deploy runs `ultimate-security`'s deploy gate (pre-push hook, `predeploy`, or publish.sh) plus a `security-audit` guidance-mode review of the diff. A bare CLI deploy runs `python3 ~/champ-skills/security/ultimate-security/scripts/deploy_gate.py check .` first. `AUDIT-REQUIRED` means a full Cloudflare audit before shipping. Never override without Deep.

Deep's couch co-op pixel RPG: one TV stage, phones as controllers, a DM console. Repo
`/Users/deep/repos/deepfall`, production at `https://deepfall-production.up.railway.app`.
The repo carries the game design and loop; read it in-repo instead of restating it here.

## When to Use

Triggered by any task naming Deepfall, its `/tv` / `/play` / `/dm` screens, its descent,
boon or combat rules, or a Railway ship of the game. Also triggers on "the game looks
wrong", "add a screen", "the night spec is failing", "deploy the game".

Not for: pure art-asset work (`sprite-art-pipeline`), post-deploy service debugging
(`railway-deployment-ops`), or visual QA outside this repo (`visual-verify`).

## Ship loop: all four gates, in order

1. **Units.** `npm test` from the repo root; three test files must print `PASS`. One of
   them is a headless bot that plays a whole descent through the real server, so a rule
   change that breaks the bot broke the game, not just a test.
2. **The full night.** `npm run e2e` (equivalently `npx playwright test`): one spec drives
   the TV at 1080p plus phone and DM contexts through join, combat, and every flow you
   added. It writes PNGs into `test-results/`.
3. **Look.** Open those PNGs with vision before reporting anything; the spec is the
   screenshot factory, not the look pass. Take a critique-shaped question per surface (see
   `visual-verify`'s Step 3 prompt discipline). When a screen gains a new interaction, add a
   leg to the night spec rather than shooting by hand, so the evidence stays tied to the
   flow.
4. **Ship.** `railway up --service deepfall --ci`, wait ~25s, then prove the bytes:
   `curl -s https://deepfall-production.up.railway.app/<asset> | grep -c <marker>` where the
   marker is a string only the new code contains. "Deploy complete" prints before the
   container serves the new build, so the exit code and a `200` on the root both lie.
   Re-run gate 2 against production when the change is visual.

## Surfaces

Three pages, one stylesheet: `/tv` (canvas stage, procedural backdrops), `/play` (phone
controller), `/dm` (DM console), all in `public/` and all served by `public/style.css`.
One chrome edit lands on all three at once, so check all three after touching it, and keep
phone-side and TV-side assertions of the same flow in the same spec leg.

Sprites are LPC composites drawn from a manifest; the stage backdrop is drawn in code.
Keep the backdrop quantised to the sprite texel grid; the rule and its reasoning live in
`sprite-art-pipeline`'s pitfalls, and `visual-verify`'s fidelity check judges the result.

## Always-on rules for this work

- No em dashes in any output or write, including code strings, commit messages, and docs.
- The deployed artifact is the proof after every ship; a green local server is not.

## Pitfalls

- **A native `confirm()` in a UI flow stalls the Playwright run.** Wire the spec's dialog
  auto-accept when you add the dialog, not when the run hangs on it.
- **A style change ships to three surfaces.** Editing `style.css` without re-running the
  phone and DM screens of the spec leaves two of the three unverified.

## Related

- `visual-verify`: the render, shoot, look, fix gate this loop closes with.
- `sprite-art-pipeline`: how the character art is built and tested.
- `railway-deployment-ops`: debugging the service after it ships (logs, ssh, schema drift).
