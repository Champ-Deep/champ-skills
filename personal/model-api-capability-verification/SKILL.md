---
name: model-api-capability-verification
description: "Use before claiming a model API can or cannot do something."
---

# Verifying what a model API can actually do

## The rule

**Never state a platform's capability from a name search, a badge, a partial
endpoint probe, or training data. Query the platform's structured catalog and
make one live call, then report what came back.**

The failure this prevents: a model ID list looks authoritative, so grepping it for
`tts` or `whisper` feels like checking. It is not. A model named
`microsoft/mai-voice-2.1-flash` will never match a search for "tts", and a
dedicated transcription catalog may not appear in the general model list at all.
That happened, and the conclusion was wrong twice in a row despite a working key
in hand.

## Procedure

1. **Find the catalog query, not the model list.** Every platform with multiple
   modalities filters its catalog by modality or type. Use the filter:
   `?output_modalities=speech`, `?category=embedding`, `?type=video`. A bare
   model list is one category of a larger catalog and undercounts it.
2. **Read the structured fields, not the names.** Modality, supported voices,
   supported parameters, per-token/per-second/per-character pricing, and context
   length are all machine-readable on the model entry. That is where the answer
   is.
3. **Distinguish three different claims**, because conflating them is the actual
   bug:
   - *Does the endpoint exist?* An HTTP status on a malformed request proves
     routing, nothing else.
   - *Does a model exist behind it?* A `model does not exist` error on a real
     call refutes capability, and a 400 on a **wrong method** refutes nothing.
   - *Does it work end to end?* Only a successful call with real input proves it.
4. **Make the real call, and close the loop when the output is media.** Generate
   a file, then feed that file back through the inverse capability. TTS output
   read back by STT proves both halves are real rather than a stub that returns
   plausible bytes.
5. **Report cost from the catalog and from the call.** State the units
   (per second, per hour, per million characters, per token) because they differ
   per capability and per model, and they decide whether a feature is viable.

## Correcting yourself

When Deep contradicts a capability claim, treat his correction as the hypothesis
and go verify it. Say plainly which method was wrong and what the right one was,
in one line, then show the evidence:

> I grepped model IDs for `tts`, so I only found models with those letters in
> their names. The platform filters its catalog by output modality. Querying that
> returned 23 speech and 24 transcription models.

Do not defend the earlier claim, and do not silently replace it. He reads the
correction, and the method failure is the part worth recording.

## When a capability genuinely is absent

Say so, with the evidence, and name what would supply it. A capability missing
from one platform is a reason to pick a different one for that capability, not a
reason to add a key everywhere. State which is it: a provider gap (needs a second
vendor) or a genuinely missing primitive (needs a telephone number, a GPU, a
human).

## Pitfalls

- **Do not treat a 4xx from a malformed or wrong-method request as evidence of
  absence.** Retest with the correct method and a valid body before concluding
  anything. Every wrong conclusion here started as a valid 4xx read too early.
- **Do not copy a model id from a blog post or a docs page.** Versioned ids rot;
  the documented `openai/gpt-4o-mini-tts-2025-12-15` returned *does not exist*.
  Read the catalog.
- **Prefer the dedicated endpoint over a general chat endpoint for a
  specialised capability.** A chat-completions path forces streaming, returns
  raw deltas to reassemble, and mixes the specialised task into a conversation.
  The dedicated endpoint returns the artifact in one request on the same key.
- **Do not assume per-model parameters are uniform.** `response_format` and
  required fields such as `voice` are per model, and the error messages are the
  only reliable way to discover the valid set short of reading each model page.
- **Hash or mask credentials when comparing them.** To prove two processes hold
  different keys, compare `sha256` prefixes from `ps eww -p <pid>`, never print
  the values.

## References

- `references/openrouter-multimodal.md` — verified modality counts, the two
  dedicated audio endpoints with working request shapes, per-model traps, and
  cheapest-first model picks for STT and TTS.
