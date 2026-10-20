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
3. **Budget the speech to the request.** "Sub-1-minute" means about 45 to 50 seconds of spoken content: ring time, greeting and sign-off all sit inside the recipient's minute. Cap with `--max-call-duration` a little above the budget (90 seconds for a 50 second script) so the agent can close naturally instead of being cut, and keep the script inside its budget, because the platform injects a wrap-up warning roughly 40 seconds before the hard cut and an overrunning script gets truncated mid-sentence.
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

## References

- `references/voice-language-controls.md` - the full voice and language control matrix, accent A/B recipe, duration cap mechanics and cost measurement.
