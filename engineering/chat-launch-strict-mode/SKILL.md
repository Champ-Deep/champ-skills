---
name: chat-launch-strict-mode
description: Use when a chat launch URL opens without a request.
version: 0.1.0
author: Sreedeep Surapaneni, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [react, chat, strict-mode, browser-verification]
    related_skills: [webapp-testing]
---

# Chat launch verification

## When to use
Use for query-driven chat launches that navigate correctly but never start the agent, especially when a chat hook owns request cleanup.

## Procedure
1. Drive the actual launcher through the real route in a browser. Record the navigation URL and outgoing chat payload separately. A correct URL does not prove a request occurred.
2. Read the installed chat hook's lifecycle. If its effect cleanup stops requests, test the launch under React Strict Mode, not only a mocked router.
3. For an automatic first turn, defer kickoff with a cancellable zero-delay timer in the effect. Set the once-only ref inside that callback, not before scheduling it. Return clearTimeout from cleanup so the discarded Strict Mode pass cannot consume the launch.
4. Keep manual chat submission unchanged. Add a regression asserting hook setup, cleanup, second setup, then exactly one kickoff. Assert the actual text and campaign context in the browser payload.
5. With API fixtures, label the assistant response visibly as a test fixture. Report local wiring separately from live authentication, provider execution and tool safety.

## Pitfalls
- Capturing a Playwright screenshot before hydration can add caret styles to server-rendered inputs and cause a hydration mismatch. Wait for a client-only readiness signal and use caret='initial' while investigating.
- A symlinked node_modules outside a Next Turbopack root can prevent resolution. Try the existing webpack CLI option before changing product config.
- A dependency's cleanup behavior can change between installed versions. Read the installed source before applying a timing fix.

## Verification
Require a real browser trace with exactly one initial chat request, a matching domain command, zero console errors, and a Strict Mode regression test. Fixture intake screenshots do not prove a live model returned the intake questions.
