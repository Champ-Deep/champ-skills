---
name: voice-agent-telephony
description: "Use when wiring voice-agent calls: trunks, tests, latency."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [voice, telephony, sip, twilio, exotel, latency, credentials]
    category: champ-suite
    related_skills: [dograh-personaplex-lane-b, dial-cli]
---

# Voice Agent Telephony

Outbound/inbound calling infrastructure for AI voice agents: provider choice,
SIP trunking, BYO IP, test-call procedure, and failure triage.

For Dograh-fork internals (realtime providers, PersonaPlex, the Pipecat seam)
load `dograh-personaplex-lane-b`. This skill owns the *calling* layer.

## When to Use

Choosing a telephony/voice provider for a voice agent; deciding between
Twilio, Exotel and BYO IP; wiring a SIP trunk; placing a first real test call;
answering "the call failed, why"; or measuring call latency.

## RULE: never conclude a credential is bad from a failing request

A tool call can mangle, truncate or redact a secret literal before it reaches
the network. A 401 then looks like "the user's key is invalid" when the real
fault is yours. This has burned two full rounds in one session: the agent
declared a working ElevenLabs key invalid because the literal it sent was 6
characters, and the user had to push back twice before it was re-tested.

**Before reporting any credential as invalid or rejected:**

1. Re-send it from a value the tooling cannot alter: a 0600 key file, or a
   value rebuilt in-process from parts. Never a bare literal in a command
   string or an f-string.
2. Confirm what the *receiving process* actually holds, not what you intended
   to send. `scripts/check-secret-transit.py` in this skill does exactly this.
3. Only after both checks may a 401 be attributed to the credential.

Same rule in reverse: when a user asserts a credential works and your test
says otherwise, your test is the suspect until proven otherwise. Re-verify
before defending the conclusion — this is a correctness rule, not deference.

## RULE: secrets never transit a command line or the HTML

Ship keys to a process via a 0600 file (`ELEVENLABS_KEY_FILE`) or the
environment, never as a literal in a shell command or embedded in a page. A
browser cannot call these vendor APIs directly anyway (CORS), which is exactly
why a small server-side proxy holding the key is the correct shape. The console
HTML must stay shareable.

## Procedure: place a real test call

1. **Read account state, never assume it.** List what actually exists
   (agents, phone numbers, their provider and status) before building a payload
   against guessed ids. Where the account id came from matters: a value pasted
   into chat is not verified just because it is plausible.
2. **Verify the number's transport is alive BEFORE dialling** if it is your own
   infrastructure. A dead trunk costs a round trip and returns an opaque
   platform error. Probe it directly (`ping`, then a SIP `OPTIONS` to UDP 5060).
3. **Select the endpoint that matches how the number is connected.** A
   SIP-trunk number id sent to the Twilio endpoint returns 422. See
   `references/providers.md`.
4. **Send all required fields.** ElevenLabs outbound needs three, not two.
5. **Place, then read the conversation back** by id to confirm `status`,
   `cost`, and whether media ever connected. A 200 with `success: false` is a
   failure, not a success.
6. **Check cost before reporting.** A failed transaction usually bills nothing;
   say so explicitly rather than implying a charge.

Validate input before the config check when both can fail, so a bad phone
number is reported as a bad phone number and not masked by a missing key.

## Diagnose by failure signature

| Signature | Cause | Where to look |
|---|---|---|
| 401 `invalid_api_key` | usually YOUR mangled literal | `scripts/check-secret-transit.py` first |
| 401 `auth token is not valid for account` | missing/other auth token | the account you authenticated against |
| `success:false`, empty `sip_call_id`, 0 cost | trunk unreachable | ping + SIP OPTIONS on the trunk host |
| 401 `account ... status 4 is not active` | carrier subaccount suspended | the subaccount, not the parent account |
| 422 on outbound-call | missing field, or wrong endpoint for the number's provider | required-fields list + endpoint choice |

A Twilio error naming a subaccount SID that differs from the one the user
quoted means the number is bound to a *different, suspended* account. Check the
number's own provider config rather than the number in the build sheet.

## Latency: measure it or do not claim it

Time-to-first-audio after end-of-speech is the number that matters, and most
vendors publish nothing. getdial.ai publishes no latency figures anywhere in
its docs corpus, so treating it as "the gold standard" is a judgement about
polish, not a measurement. If latency is the differentiator, publish ours.

Where a path pins telephony narrowband, say so plainly: an Asterisk ARI
transport hardcoded to 8 kHz cannot carry a wideband native S2S model end to
end. If someone wants their own IP *and* low latency, check the codec before
recommending the architecture — the two goals can conflict.

## References

- `references/providers.md` — provider matrix, verified pricing, endpoint
  contracts, and account/number inventory.
- `references/call-diagnosis.md` — deeper triage, probe recipes, and the
  endpoint-selection trap.
- `scripts/check-secret-transit.py` — prove what a running process actually
  received. Run this before blaming a credential.

## Benchmark: the Dial platform

Deep holds getdial.ai as the quality bar. Treat it as a capability reference,
not a latency baseline. The `dial-cli` skill is the authoritative reference for
that platform; install it via `curl -fsSL https://getdial.ai/skills.md` if
`dial` is not on PATH.