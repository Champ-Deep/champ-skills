---
name: upstream-model-integration
description: "Use before adopting or self-hosting an upstream model."
tags: [integration, self-hosting, protocol, evaluation, voice-ai, gpu, cost-model, adoption]
related_skills: [competitive-product-teardown, model-api-capability-verification, fix-proof-by-measurement]
---

# Integrating an upstream model or service

## When to use this

Trigger on: "can we use X in Y", "self-host X", "swap our voice/LLM/STT/embedding provider",
"would X be faster/cheaper/better than what we run", "integrate <upstream repo>", "build a
brand voice", or any recommendation that a specific upstream model or service replaces or
joins something already running.

Also trigger when the proposal rests on "it has an API", "it supports a custom base_url", or
"you can BYOK that" — those are exactly the claims this skill exists to test.

## The rule

**A candidate that looks pluggable is not integrated until you have read the bytes on both
sides of the socket.** The five checks below are cheap, they run before anyone plans around
the idea, and each one has been the thing that turned a "one-line config change" into a
second engineering project.

Run them in order. Each can independently kill the proposal, and finding that out before a
plan exists is the entire point.

## 1. Wire protocol, not constructor signature

A service class accepting `base_url` is a routing parameter, not a protocol guarantee. It
tells you the hostname is configurable and nothing else. Read what the client sends and
parses, then read the server's receive loop to see what it accepts:

```bash
# client side: what goes on the socket and what comes off it
grep -nE 'send_bytes|send_str|recv|MsgType|kind ==|json\.loads' <client>
# server side: what it will accept, and what codec it decodes
gh api repos/ORG/REPO/contents/PATH --jq '.content' | base64 -d \
  | grep -nE 'receive|MsgType|kind ==|OpusStream|Decoder'
```

Typed JSON event protocols and binary codec protocols (framed messages with a type prefix
byte, codec-encoded payloads, packed multi-channel frames) are different worlds with no
shim between them.

## 2. Does OUR config have a seam for it

Before quoting any effort, grep our own config schema and service factory for that specific
provider:

```bash
grep -n 'class .*<ServiceType>' <our config module>   # does the enum entry exist?
grep -n 'provider ==\|base_url' <our service factory> # does the branch pass a URL?
```

Three answers, differing by an order of magnitude in cost: the enum has an entry and the
factory passes a URL (configuration); the entry exists but has no URL field (fork plus
schema change plus factory branch); no entry at all (all three, plus a rebase bill).

Report the rebase honestly. Forking an upstream moving hundreds of commits a month is a
standing maintenance cost, not a one-time edit.

Run this per service type, not once per project. Frameworks routinely expose `base_url` on
their cascaded STT/LLM/TTS providers while hardcoding the realtime and transport services,
because those have bespoke clients. A single project can therefore be configuration on one
path and a fork on another.

## 3. The reference server's concurrency model IS the cost model

This is the check that most often flips the verdict, and no marketing artifact will tell you
the answer:

```bash
gh api repos/ORG/REPO/contents/PATH --jq '.content' | base64 -d \
  | grep -n 'lock\|Lock\|reset_streaming\|self\.[a-z_]* ='
```

- A single global state object with a lock held for the whole conversation means **one call
  per unit of hardware**, regardless of throughput claims.
- Per-request config written to shared object attributes means concurrent callers silently
  overwrite each other, mid-call.
- Batched or per-request generator instances mean concurrency scales with VRAM and you can
  actually price it.

The pattern to recognise, common across full-duplex speech model servers: one state object
holding the codecs and the generator, warmed once, at a single route; the handler resolves
per-connection config from query parameters, assigns it to the **shared** generator,
acquires a process-wide lock, resets streaming state, runs its loops until the first
completes, releases. That shape is one call per process, and it means production concurrency
is a separate build with its own VRAM arithmetic. Price it as a second project.

Only after this can you answer what a minute of this costs in production. Anyone quoting
per-minute economics before reading the lock scope is guessing, and the guess is optimistic
by roughly the number of concurrent sessions.

## 4. Capability parity with what we are FOR

Before recommending a candidate as the primary engine, state what our platform exists to
do, then check the candidate serves that. The headline differentiator rarely outranks a
missing primitive.

Check for: function/tool calling, structured output, streaming, cross-turn session state,
and anything our workflows depend on. A model can win every benchmark in its category and
still lack the one capability our framework exists to provide.

For speech-to-speech specifically, the three architecture levels decide this, and the
distinction is decisive rather than incremental:

| Level | Shape | Full duplex | Function calling |
|---|---|---|---|
| 1 | Native speech-to-speech, thinks in speech tokens | yes, intrinsic | no |
| 2 | Text LLM plus speech encoder/decoder | varies | no or unreliable |
| 3 | Cascaded STT -> LLM -> TTS, each streaming | no | yes |

If the host framework's value is tool calls, workflows, and MCP, levels 1 and 2 cannot be
the primary engine however good their latency. Do not reject level 3 on reflex either:
streaming STT plus a vLLM-served tool-calling LLM plus streaming TTS measures near 950 ms
P50 time-to-first-audio on a single modest GPU, which is often good enough and keeps tools.

When parity fails, the honest shape is a split, not a dead end: the fast model for work that
needs no tool calls, the existing pipeline where tool calls live.

## 5. The benchmark hardware is not the user's hardware

Read the card's test hardware, compare it to the machine that will actually run this, and
check whether the local or consumer path is wired or merely present:

```bash
grep -nE 'Literal\["cuda"\]|Literal\["cpu"\]|mps|device\.type|torch\.cuda\.is_available' <server>
```

A device selector reading `Literal["cuda"] | Literal["cpu"]` with the consumer branch
commented out means that path was abandoned, not merely slow. When the model does not fit
locally, that becomes a hosting and cost decision for the user, and it needs the concurrency
number from check 3 as its input. Flag that at low call volume a warm but idle container can
dominate the bill, since serverless platforms bill a retention window after the last request
and that window is usually longer than a phone call.

## Sequencing: prove standalone before building the adapter

Order the work so the cheap experiment gates the expensive one.

1. Get the candidate working alone, with no framework in the loop, and reproduce its headline
   claim **on our real input over the transport we would actually use**. Codec and network
   leg change latency numbers, so a browser demo does not settle a telephony claim.
2. Only once the number reproduces, build the integration.

If the claim does not reproduce, the direction is dead and you saved the adapter work. Say so
plainly; that is a good outcome, not a failure.

## Reporting

Lead with the verdict and the check that produced it. If a check killed the proposal, that is
the headline, not a caveat.

Separate verified from inferred. For capability and cost claims, cite the file and line. "I
read the lock scope in server.py and it wraps the whole conversation, so this is one call per
GPU" is worth more than a paragraph of summary.

Give the user the decisions only they can make, with numbers attached: licence or credential
acceptance only they can perform, hardware spend, and which capability gap they accept. Name
those up front, because nothing runs until they are done.

## Pitfalls

- Do not treat a `base_url` parameter as proof of integrability. It configures a hostname,
  not a protocol.
- Do not quote per-minute or per-seat economics before reading the server's concurrency
  primitives.
- Do not accept a capability claim from a comparison table without checking it against what
  our own platform is for.
- Do not let a benchmark-hardware line stand in for the hardware that will run it.
- Do not build the adapter first. Standalone proof first, and let it gate.
- Do not present a licence-gated or credential-gated model as testable today. Name the
  acceptance step that belongs to the user, and say that nothing runs until it is done.
- Do not conclude "no transport exists" from a docs index. Grep the framework's own service
  tree; absence of a first-class transport is what makes this an adapter rather than an
  impossibility.
- Do not report "incompatible" without naming which of the five checks failed. The number is
  the deliverable.
- Do not assume voice conditioning requires training. Where the model conditions on a voice
  prompt, a brand voice is an embedding derived from a short reference clip, so the
  deliverable is a good recording rather than a fine-tune. Use the stock packaged voices for
  a first measurement and swap in your own once there is a baseline to compare against.