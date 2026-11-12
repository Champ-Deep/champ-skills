---
name: outbound-voice-call
description: Use when an AI voice agent must call a real person.
---

# Outbound voice calls

Delivering a bounded spoken message to a real person through an AI voice agent: a meeting briefing, a reminder, a confirmation, a live demo of the agent itself. A call is a write into the physical world: a phone rings, a person answers, minutes are billed. Placement is not idempotent, so every claim of success has to come from the call record, never from the placement response.

The driver is the `dial` CLI (getdial.ai). Load `dial-cli` for its command surface, flag names and onboarding; this skill owns the workflow around it.

## Procedure

1. **Check account state before you draft.** `dial number list --json` for the from-number's `callingEnabled` and `setupStatus`, then `dial billing --json` for balance. A refused placement burns a round trip, and an ambiguous failure must be checked against `dial call list` before any retry, since a blind retry places a second call.
2. **Write the instruction to a scratch file.** Multi-paragraph prompts with apostrophes and numbered lists get mangled when quoted inline. Place it as `--outbound-instruction "$(cat <file>)"`.
3. **Budget the speech to the request.** "Sub-1-minute" means about 45 to 50 seconds of spoken content: ring time, greeting and sign-off all sit inside the recipient's minute. Cap with `--max-call-duration` a little above the budget (90 seconds for a 50 second script) so the agent can close naturally instead of being cut, and keep the script inside its budget, because the platform injects a wrap-up warning roughly 40 seconds before the hard cut and an overrunning script gets truncated mid-sentence. Before placing, run the instruction file through `tts-safe-script` (`scripts/tts_safe.py --check`): no raw acronym, caps run or digit may reach the voice, and the instruction itself tells the agent to say initialisms as spaced letters and numbers as words.
4. **Choose the voice knobs, then place.** Per call there are exactly two: `--language <bcp47>` and `--voice-gender male|female`. There is no voice catalogue, voice id or accent picker anywhere in the CLI or the REST API; the voice preset belongs to the number, not the call. `references/voice-language-controls.md` says what each knob actually changes and how to A/B an accent.
5. **Track to completion, sized to the call.** `dial wait-for call.ended -f callId=<id> -t <cap + 60> --json`. The default timeout is 30 seconds and any live call beats it; a timeout exits non-zero with `{"ok":false,"timeout":true}`, which reads like a result until you check the exit code.
6. **Verify from the call record.** `dial call get <id> --json` and read `status.terminationType`, `duration`, `transcript`, `transcriptTurns`, `recordingAvailable`. The `call.ended` event can report `transcriptAvailable:false` while the transcript already exists on the record, so the event never settles whether the message was spoken.
7. **Report what was said and what it cost.** Quote the recipient's own replies from the transcript rather than summarising them favourably. Take a `dial billing --json` balance reading before placement and after completion, and state the delta; an unmeasured cost is not a claim.

## Always-on rules

- The agent must identify itself as an AI and must make no commitments, promises or plans on the principal's behalf. Both belong in the instruction text, not in the chat summary of it.
- The first sentence carries the recipient's name and whose behalf the call is on. An unnamed AI voice gets hung up on before the message starts.
- Normalize destinations to E.164 before Dial sees them; never invent a number.
- One call per person, with that person's own action items written into their instruction. A shared list read verbatim to a group tells people apart from nothing.
- One closing question, not a survey. The call is an announcement with an exit; the instruction should route a long or commercial discussion back to the principal and end the call.
- Name the placing platform and number when reporting, so the principal can tell the recipient what to expect on their caller ID.
- Calling Indian businesses from the US Dial number mostly fails: unknown +1 caller IDs go unanswered (worse on Sundays), and IndiaMART/Justdial relay lines (+91 79..., +91 80 4xxx) drop or garble audio. Prefer the business's own mobile from its website, call Mon to Sat 10:00 to 18:00 IST, and send the written ask in parallel instead of waiting on the call. Measured cost: about 66 cents for 84 s of connected India time.

## A call that must happen at a set time while nobody is there

Use a one-shot `no_agent` cron job pointing at a script under `~/.hermes/scripts`, never an agent run: a phone call must not depend on a model's mood. Worked example: `~/.hermes/scripts/lev_briefing_call.py`.

- The script dials only inside a narrow window around the target time and stays silent outside it, so a late or repeated tick cannot ring anyone.
- Write a done marker before dialing and pass `--idempotency-key`. Never retry: a failed placement is reported, not repeated.
- Give the principal a veto that the script reads just before dialing: a skip file, and the decision card (archived status, or a comment matching the "no call" option). Skip the agent's own evidence comments when scanning, and test the pattern against the real ruling formats (`Deep: C`, `Deep (via Grok Bot): C`, free text from the desktop).
- `dial` is a node script. In a bare cron PATH it fails silently, so call it by absolute path and put its own `bin` directory first on PATH. Prove it with `env -i HOME=$HOME PATH=/usr/bin:/bin python3 <script> --dry-run`.
- Return from the tick right after placement and hand the wait and the record save to a detached child, so a script timeout cannot lose the transcript.
- Free Dial accounts refuse a duration cap above 300 seconds. A four minute briefing needs about 290.
- The opening line names the system that is really placing the call. A fallback placed through the CLI must not introduce itself as the product it is standing in for.
- Create the decision card first, with the fallback as the stated default and its deadline, then schedule. A chat question asked at night times out unanswered.

## References

- `references/voice-language-controls.md` - the full voice and language control matrix, accent A/B recipe, duration cap mechanics and cost measurement.
