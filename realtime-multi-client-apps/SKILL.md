---
name: realtime-multi-client-apps
description: "Use when several screens must share one live session state."
license: MIT
version: 1.0.0
author: Deep / Champions
metadata:
  hermes:
    tags: [websocket, realtime, multiplayer, fullstack, dom, testing]
    related_skills: [webapp-testing, adapter-seam-extension, verification-gate-integrity]
---

# Real-time multi-client apps

## When to Use

Triggers: "a TV screen plus phone controllers", "everyone joins a room code", "a
host console drives what the other screens show", "hot-seat game in the browser",
"live shared state across several browsers", "a WebSocket session with roles".

Skip it for a single-page site with no server state, and for a backend API whose
clients never watch each other live.

How to build one session of live shared state that several browsers see at once: a
tv/display surface, phone-sized player clients, and a privileged controller (host,
DM, moderator) console. The procedure below is the order that avoids rework.

## Procedure

1. **Write the rules module first, before any server or screen.** Pure data and
   pure functions: every entity table, the numeric balance (HP, costs, thresholds),
   one `validate`/`resolve` function per mutation, plus any content script (levels,
   scenarios). Load the SAME file in Node (`require`/`import`) and in the browser
   (`<script>`) with no build step: no ESM syntax if the page uses plain script tags,
   no globals the other side does not define.
   Then probe it from a REPL before anything depends on it: run every validator's
   happy path and its rejection path, and check arithmetic (min/max, progression
   thresholds). Catching a bad rule here costs one edit; catching it later costs a
   server, three screens and a test.
2. **Server owns all state; screens only render and request.** One authoritative
   object broadcast wholesale on every change, plus a log of short events for
   toasts and speech bubbles. Validate every client message against a handler
   whitelist keyed by message `type`, and reject with `{type:'error', text}` rather
   than trusting a field. Never let a client post a result the server can compute
   (dice, damage, turn order).
3. **Build the engine as a node-testable core plus a thin socket harness.** Split
   `engine.js` (mutation functions over the state object) from `server.js` (HTTP
   routes, WS plumbing, persistence). The test then boots the real server and talks
   to it over real sockets (see step 6).
4. **One shared client helper for socket, DOM and animation.** A single `h(tag,
   props, ...children)` DOM builder, a reconnecting socket wrapper with
   `onState/onEvent/onMsg`, and a sprite/animation helper driven by a shared config
   constant (frame counts, grid size) so no screen hardcodes an animation length.
5. **Draw the screens last, against the state you already tested.** Display screen,
   player screen, controller console: same stylesheet, same helpers, no duplicated
   rules logic. Each screen degrades on its own (joined, seated, spectating).
6. **Prove it end to end through the socket API, not through unit calls.** One
   scripted test that: starts the server on a random port, opens several WS clients,
   performs the full happy path (join, create, act, resolve, advance), then asserts
   a few specific rejections, then shuts the server down. This catches handler-wiring
   bugs that unit tests cannot see.
7. **Then browser-check each screen for real**: render, screenshot, check the console
   for JS errors. Close with the visual gate you normally use.
8. **Deploy only after 6 and 7 are green**, with persistence on a mounted volume.

## The render loop is the sharpest edge

A screen that rebuilds its DOM on every state broadcast destroys whatever the user is
typing the moment another client acts, and it loses focus mid-form. Fix both, in this
order:

- **Defer, do not drop.** On state while an input inside the app has focus, set a
  `pending` flag instead of re-rendering; flush it on `focusout` (plus a small
  timeout). The user keeps typing, the screen catches up when they leave the field.
- **Snapshot and restore field values around the rebuild.** Before
  `replaceChildren`, capture `id -> value` for every input/textarea/select inside
  the container; after rebuilding, write them back. Keep an explicit `skipRestore`
  list for the one screen action that legitimately seeds new values (clicking a
  preset to load a form), or the restore will fight the intent.
- **Checkboxes and selected attributes**: restore `el.value` only for
  non-checkboxes; drive checked/selected from state at build time.
- **Serve state, not spinner states.** If a screen blanks to a loading message
  whenever the socket drops, a one-second reconnect turns a live session into a
  flicker. Keep the last state on screen.

## Art as a seam

When art may arrive later (a generator, an external pipeline, a commissioned set),
keep every draw call behind two functions with fixed signatures: `draw(appearance,
animation, frame)` and `drawEnemy(kind, animation, frame)`. Everything else consumes
only those two. Swapping in sprite sheets later then touches one file.
Self-generated art must be constrained (fixed cell grid, fixed frame counts, one
shared config constant) or a later asset drop silently misaligns every animation.

## Testing posture

- Happy path AND rejections in the same socket test: a locked action, a rejected
  construction, an out-of-turn message. Rules only matter if the server enforces them.
- Persist to a file path from env (`DATA_DIR`), and include a reload assertion in the
  test so persistence is proven, not assumed.
- If art or any other slice is delegated to a parallel worker, give it a complete,
  self-contained contract: exact option ids per slot, exact public API, the command
  that proves it, and the acceptance check (screenshot must show readable figures,
  not noise). Then verify the returned artifact yourself before building on it.

## Pitfalls

- **Letting the browser validate and the server trust.** Anything a client can send
  becomes a cheat or a crash; validate centrally against a handler map.
- **Rebuilding the DOM on every broadcast while a user types.** Their input is wiped
  by the next event from someone else; defer on focus and restore values.
- **Skipping the socket-level test because the engine has unit tests.** Wiring bugs
  (wrong handler key, unbroadcast mutation) are invisible to both unit and visual
  checks.
- **Rules data duplicated per screen.** A balance tweak then lands in three files and
  drifts; one shared module, loaded everywhere.
- **A loading state that replaces live content on reconnect.** Flashes the screen on
  every blip; keep rendering the last known state.
- **Deploying before tests and browser checks pass.** A green deploy proves the build,
  not the session; the first player to join finds the bug instead of the test.
- **Narrow contracts handed to parallel workers.** "Make a renderer" produces
  something that cannot be integrated; specify ids, signatures and the proof command.
