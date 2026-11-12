---
name: champvox-development
description: "Use when changing ChampVox, Deep's macOS dictation app."
version: 1.0.0
author: Hermes for Sreedeep Surapaneni
license: MIT
metadata:
  hermes:
    tags: [macos, swift, swiftpm, dictation, tts, llm]
    related_skills: [champ-portfolio-triage, visual-verify]
---

# ChampVox development

## When to Use

Triggered by any task naming ChampVox, its dictation, Read Aloud, AI Commands or
Summarize and Speak features, its Settings or hotkeys, or a build, test or probe of
that repo. Also triggers on "the pill is stuck", "the hotkey does nothing", "add a
ChampVox feature", "merge ChampVox with OpenClicky".

Not for: assessing whether the repo is worth reviving (`champ-portfolio-triage`),
or judging what a built Settings screen looks like once a signed build can run
(`visual-verify`).

Repo `~/repos/ChampVox`, Deep's macOS dictation, text-to-speech and AI-command
app. SwiftPM only, no Xcode project: everything builds, tests and probes from the
terminal.

Where a line goes decides whether it can ever be tested:

- `Sources/ChampVoxKit` — logic with no macOS permission surface (AppConfig, LLM
  clients, CommandPromptBuilder, WAV/audio codecs). The test target covers this.
- `Sources/ChampVox` — the app: pipeline controller, menu, Settings UI, hotkeys,
  Accessibility and Screen Recording code. Unprovable headless, so its proof is a
  debug hook, below.

## Ship loop, in order

1. `swift build`.
2. `swift run champvox-tests` — hand-rolled assert harness, not XCTest; prints
   `✓ All tests passed (N checks)` and names the failing check inline on failure.
3. Prove the executable half with a headless hook from `Main.swift`, run as
   `.build/debug/ChampVox --<hook> ...`: `--transcribe-file x.wav` (STT plus
   post-processing), `--llm-test "prompt"` (provider path), `--ocr-test x.png`
   (Vision OCR), `--inject-test "text"` (needs front focus plus Accessibility).
   Each exits non-zero on failure, so the exit code is usable evidence.
4. Render the fixture you need instead of claiming the path works from a code read:
   for OCR, draw the fake screen with PIL (`/System/Library/Fonts/Helvetica.ttc`) to
   a PNG and feed it to `--ocr-test`.
5. UI wiring you cannot execute headless (hotkey tap, menu item, Settings toggle)
   gets its testable half tested (config field round-trips; add a decode test against
   a fixture that predates the field) and the rest reported as not executed. Never
   present an unexecuted path as verified.

## Adding a user-facing behavior

Every new behavior touches all five; missing one is the common defect:

1. Field on `AppConfig` whose default lets an older `config.json` still decode.
2. Settings section, plus a hotkey recorder row when it takes a shortcut.
3. Menu item, and onboarding row.
4. One test.
5. A headless hook, if any part runs outside the GUI.

Reuse before adding — a feature that reimplements these forks existing behavior:
`SelectionGrabber` (Cmd+C snapshot and restore for "current selection"),
`CommandPromptBuilder` (system plus user message assembly), `ReadAloudController`
(speak/stop/toggle plus the status pill), `HotkeyManager` (tap handler feeding the
Settings recorder), `CVLog`. Needed cross-file? Drop `private` rather than copying
the logic.

## Architecture ruling: ChampVox is the host

OpenClicky (`~/repos/openclicky`) is a donor of PATTERNS, never a merge target: screen
capture plus OCR, the conversational voice loop, an optional cursor overlay via its
local HTTP bridge. It is an Xcode-only fork carrying someone else's bundle id,
copyright and cloud STT where ChampVox is on-device and SwiftPM under our own
conventions. Port the pattern into our seams; never import its files. The picker was
run past Deep once (decider returned no precedent), so treat this as settled until he
reopens it.

## Pitfalls

- **`try await a ?? b` does not compile** ("'async' call in an autoclosure that does
  not support concurrency"): `??` takes a non-async autoclosure. Branch with `if let`
  and await inside the body.
- **Text-only history entries must skip the WAV write.** `writeWAV` on an empty buffer
  writes a 0-sample file; guard on `samples.isEmpty` for records that have no audio
  (a spoken summary, an AI command's answer).
- **Set the phase before calling `speak()`.** `speak()` moves the state to `.speaking`
  itself; a stale `.thinking` swallows the stop gesture, which only fires while
  speaking.
- **Spoken output must never get format instructions.** `CommandPromptBuilder.build`
  appends the output-format block only when formats are passed, so pass none and hand
  it a spoken system prompt for anything read aloud, or the voice reads bullets as
  "asterisk".
- **A 404 from `--llm-test` is config, not client code**: check `ollama list` and the
  provider set in `config.json` before debugging the LLM client.

## Always-on

- No em dashes in any output or write, including code strings and commit messages.
- Leave the work uncommitted on a feature branch and report the diff; Deep approves
  before any commit, push or merge.

## Related

- `champ-portfolio-triage`: read-only assessment of a Champ-Deep repo before reviving
  it.
- `visual-verify`: the look pass for Settings and menu surfaces once a signed build
  can be screenshotted.
