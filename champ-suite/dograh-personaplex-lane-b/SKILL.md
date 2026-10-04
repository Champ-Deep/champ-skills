---
name: dograh-personaplex-lane-b
description: Use when wiring PersonaPlex into our dograh fork.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [voice, dograh, personaplex, pipecat, realtime, s2s]
    category: champ-suite
    related_skills: [remote-compute-modal]
---

# Dograh + PersonaPlex (Lane B)

Champ-Deep/dograh is our fork of dograh-hq/dograh (BSD-2). Lane B = wire a
self-hosted NVIDIA PersonaPlex full-duplex S2S model into Dograh's realtime
slot. Lane A (cascaded STT->LLM->TTS) was rejected in favour of Lane B on
2026-10-01.

## When to Use

Load this when: adding or debugging a realtime provider in our dograh fork;
integrating any self-hosted speech-to-speech model; working the PersonaPlex or
Moshi protocol; doing brand-voice conditioning; or answering what Dograh's
realtime seam allows. It records the protocol mismatch, the `base_url` gap, the
single-session lock, and the licence traps that are expensive to rediscover.

## Verified facts (read from source, do not re-derive)

- **PersonaPlex is Moshi-lineage.** 7B, full-duplex, 24kHz, NVIDIA ADLR.
  Code MIT, weights NVIDIA Open Model License (commercially usable). Weights
  are GATED: accepting the licence is not enough, an `HF_TOKEN` with read
  access is required.
- **It is NOT an OpenAI Realtime server.** Pipecat's `OpenAIRealtimeLLMService`
  takes `base_url` (default `wss://api.openai.com/v1/realtime`), which makes it
  *look* like you can point it anywhere. You cannot. PersonaPlex ships
  `moshi/moshi/server.py` speaking Kyutai's binary Opus WebSocket protocol:
  `ws.send_bytes(b"\x01" + msg)` for audio, `b"\x00"` handshake, MIME
  negotiation. Pipecat ships NO Moshi transport. An adapter is required.
- **The reference server is hard single-session.** One `ServerState`, one
  `LMGen`, and `async with self.lock:` wraps the ENTIRE conversation
  (server.py ~line 259). Voice prompt is set on the shared generator before
  the lock, so a second concurrent caller also silently overwrites the first
  call's voice. One call per GPU. Concurrency needs a custom batched server.
- **Hardware:** NVIDIA benchmarked on A100 80GB. In its own server the MPS path
  is commented out (`DeviceString = Literal["cuda"] | Literal["cpu"] #| Literal["mps"]`).
  Not viable on Apple Silicon via the NVIDIA path.
- **No function calling.** Moshi-lineage models cannot call tools. Dograh's
  realtime mode therefore also requires an `llm` (text LLM follows the
  workflow behind the voice). This is why PersonaPlex is Lane B (greeting,
  FAQ, after-hours) and not the sole engine.

## Local inference on Apple Silicon (VERIFIED WORKING)

`moshi_mlx` (PyPI) CANNOT load PersonaPlex: `LmConfig.from_config_dict` raises
`KeyError: 'dim'`. PersonaPlex nests config under `temporal`/`depformer`/`mimi`
with `model_type: personaplex`; moshi_mlx expects a flat schema and is base
Moshi only (no voice-prompt or text-prompt API). Do not download 9GB hoping.

**The working local path is Swift:** https://github.com/soniqo/speech-swift
(Apache-2.0, actively maintained). PersonaPlex is a first-class library product
and there is a ready CLI.

```bash
git clone --depth 1 https://github.com/soniqo/speech-swift.git
swift build -c release --product speech --disable-sandbox
./.build/release/speech respond --input in.wav --voice NATM0 --verbose --transcript
```

Model: `aufklarer/PersonaPlex-7B-MLX-8bit` (~9.1GB, ungated).
`huggingface-cli download aufklarer/PersonaPlex-7B-MLX-8bit --local-dir <dir>`
(the binary is `huggingface-cli`, NOT `hf`, at least on 0.28.1).

Useful flags: `--full-duplex` (per-frame ms/step timing, the real latency
number, saves input+output wavs to `--debug-dir`), `--json` (rtf, elapsed,
transcript), `--system-prompt customer-service`, `--system-prompt-text`,
`--list-voices`, `--list-prompts`, `--max-steps` (12.5Hz frames; no EOS token,
so this controls response length), `--compile`.

Test input: `Tests/PersonaPlexTests/Resources/test_audio.wav` in speech-swift -
24kHz mono 20s of speech, the model's native rate.

Reference perf from the repo (M2 Max 64GB): RTF ~0.94, full-duplex ~80-95ms per
step. Gapless audio needs <80ms/step. M1 Pro is slower than M2 Max; measure,
do not assume.

## THE BIG LATENCY FIND: use `speech voice-chat`, not `speech respond`

`speech` (soniqo/speech-swift) has MORE than PersonaPlex. `speech voice-chat`
runs **Nemotron VoiceChat 11B** with TRUE live duplex:
https://huggingface.co/aufklarer/VoiceChat-11B-Perception-MLX-int5
- 8.6 GB, ungated, licence `openmdw-1.1`
- `--system-prompt` override, `--greet`
- live microphone capture, **Apple acoustic echo cancellation** (`--no-aec` to
  disable), **NVIDIA RNN-T turn-taking** safety fallback
- `--prebuffer-frames` (80ms each, default 3) tunes the interruption/latency
  tradeoff directly: lower = faster turn but more clipped interruptions
- `--input` to use a WAV instead of the mic, then exit
- **MCP tool-calling** (`--mcp-config`, `--mcp-server`, write-policy) - the
  thing PersonaPlex and Moshi cannot do at all

This is the correct local target for a phone agent: it is the only local engine
with live mic + turn-taking + AEC + tools. `speech respond` is file-in/file-out
inference, useful for measuring ms/step, NOT for a conversation.

Other useful subcommands: `vad-stream` (32ms chunks), `turn` (Smart Turn v3.2
turn detection), `transcribe`, `speak`, `audio-translate`.

### Model recommendation by job (latency is the priority)

Human perception threshold is ~250 ms end-to-end (Inworld's benchmark calls
anything under it "instantaneous"). Published figures:

| model | avg latency | interruption | notes |
|---|---|---|---|
| PersonaPlex (NVIDIA, 7B) | 170-205 ms | **240 ms** | 100% interruption success; best open full-duplex quality |
| Moshi (Kyutai, 7B) | ~160-205 ms | ~257 ms | fastest; CC-BY-4.0 |
| Qwen2.5-Omni | ~257 ms | 1.3 s | near-duplex, not full duplex |
| Gemini Live | 953 ms | 1.4 s | far too slow |
| OpenAI Realtime | ~320 ms | - | API cost |
| ElevenLabs ConvAI | (not published) | - | what we use today |

So: **PersonaPlex or Moshi for latency**, and both are native audio full-duplex
(Moshi/PersonaPlex 0.99-1.00 turn-taking vs Qwen 0.00, and 100% vs 60.6% vs
43.9% interruption success). Cascaded STT->LLM->TTS adds ~200-400 ms and is
the wrong architecture when latency is the goal.

**Dial (getdial.ai) publishes NO latency numbers at all** - grepped the full
docs corpus. That is our opening: publish measured numbers.

### MLX can hit the macOS GPU watchdog under load (real crash, 2026-10-05)

A local run aborted with exit -6 / SIGABRT:
```
libc++abi: terminating due to uncaught exception of type std::runtime_error:
[METAL] Command buffer execution failed: Caused GPU Timeout Error (00000002:***)
```
Crash report confirms `EXC_CRASH / Abort trap: 6`, blocked in
`semaphore_wait_trap` -> `_dispatch_semaphore_wait_slow` -> `RespondCommand.run`,
dying during **Mimi codec load** (~80%), after weights had loaded fine.

This is the **macOS GPU watchdog killing a long-running Metal command buffer**,
not a model or flag bug. Trigger: concurrent heavy I/O/GPU work (it happened
while an 8.6 GB model download was saturating the box). It leaves no partial
output, so the run just vanishes.

**Rule: never run local MLX inference while something else is loading models or
building.** The console now retries once with a5s backoff and reports
`note: recovered from a GPU timeout on retry`. If a local run dies with no
output, check `~/Library/Library/Logs/DiagnosticReports/speech-*.ips` - these
are JSON: first line is metadata, remainder is the body with `usedImages` and
`threads` to walk the frames.

Also: a *missing* output file does not mean the flag was rejected - read the
exit code and stderr before concluding anything.

### THE 80 ms FRAME FLOOR (from speech-swift's own docs)

`docs/inference/voicechat.md`: the engine consumes **one 80 ms input frame**
(1,280 samples @ 16 kHz) at a time and emits **one 1,764-sample output frame**
per frame. Audio cadence is therefore capped at **80 ms / 12.5 fps**, no matter
how fast the Mac is. This is the architectural floor, not a tuning target.

**Its reference numbers are from an M5 Pro 48 GB, not our M1 Pro 32 GB:**
- mic actor service 118 ms p95 / 172 ms max
- accumulated lateness past the 80 ms deadlines: 139 ms p95 / 231 ms max
- first speech after a tool result: 472 ms; full post-tool speech ~3.5 s
- INT5 bundle: **8.56 GB on disk**, ~8.70 GB RSS, 15.64 GB macOS physical memory
- tool calls: 1,425-1,793 ms to native call start (JSON emitted in ~27 steps)

Note the deadline-overrun metric is the honest one: RTF and per-call time look
fine while real queues still slip 139-231 ms past the 80 ms budget.

Docs also warn: **do not raise the token chunk size.** A 32-token schedule cut
prefills from 3 to 2 but pushed sync 291 -> 658 ms and worst mic stall 146 ->
465 ms. The bounded 16-token schedule is deliberate. Do not "optimise" this.

### Bundle completeness is all-or-nothing

`speech voice-chat` requires `encoder/`, `llm/`, and `tts/` complete. A partial
download fails at load with `Error: no model.safetensors at .../llm/model.safetensors`
even though the encoder loaded fine. Check
`find <bundle> -name '*.incomplete'` returns nothing before trying to load - the
presence of a directory or a config.json proves nothing.

- **`--greet` and `--system-prompt` are MUTUALLY EXCLUSIVE.** Passing both exits
  immediately with `Error: use either --greet or --system-prompt, not both`.
  To greet *and* use a custom prompt, put the greeting instruction in the
  prompt text instead of passing the flag.
- The bundle must contain `encoder/model.safetensors`. A partially downloaded
  directory fails with `Error: no model.safetensors at .../encoder/model.safetensors`
  - so do not treat "the directory exists" as "the model is ready".
- `--model` accepts a local directory or an HF repo id.
- Progress prints `Loading VoiceChat bundle: <path>` then percentages.

**Launching it needs mic permissions**, so it must run in a real terminal as
the logged-in user, not from a sandboxed helper. Long runs go via
`terminal(background=True, notify=True)`; poll `/voicechat/status` rather than
sleeping in a loop.

### HEADLESS MEASURED: VoiceChat 11B on M1 Pro 32GB (2026-10-05)

`voice-chat --input <16k wav>` runs the whole duplex pipeline from a FILE -
no microphone, no TTY needed. This unblocks throughput measurement on our
hardware, which was previously stuck on a human-only live-mic test.

```
you     Can you guarantee
soniqo  I cannot guarantee a Thursday callback, but I can offer one if you would like.
        Would you like me to schedule it?
frames 200, total p50 166.3 ms, p95 260.6 ms, real time NO
live-frame RTF normal 2.62x   behind 0.0s   last 164 ms for 80 ms audio
RNN-T forced starts 1   barge-ins 0   speaker gaps 0
```

Reply audio written: 22.05 kHz mono, 16.0 s, RMS 0.0091, peak 0.149, 9.8%
non-silent. A real spoken answer, and the reply is on-point (it refuses to
guarantee an unconfirmed callback, which is exactly the prompt rule).

**Verdict: NOT real time on an M1 Pro.** RTF 2.62x means it needs ~2.6 s of
compute per second of audio, ~3x too slow. p50 166 ms/frame against an 80 ms
budget. It holds no backlog ("behind 0.0 s") only because file input has no
real-time deadline.

So: earlier "GPU host required" was RIGHT for VoiceChat, and my later
"model loading fits so it may be fine" was WRONG - loading fine says nothing
about streaming throughput. Both PersonaPlex (RTF 1.54) and VoiceChat
(RTF 2.62) miss realtime on this Mac. Do not repeat the second claim.

**MCP tool-calling works** - that is the capability PersonaPlex lacks, and
`--mcp-config` is the hook for booking a real callback.

Input must be **16 kHz mono**; the repo test clip is 24 kHz, so resample.

### BIGGEST LOCAL WIN: `--no-rnnt-turn-taking` (measured)

| flags | RTF | p50 | p95 |
|---|---:|---:|---:|
| default | 2.62x | 166.3 ms | 260.6 ms |
| `--prebuffer-frames 1` | 2.33x | 152.9 ms | 284.6 ms |
| `--prebuffer-frames 4` | 2.29x | 149.1 ms | 283.2 ms |
| **`--no-rnnt-turn-taking`** | **1.44x** | **112.9 ms** | **125.3 ms** |

That single flag removes ~45% of the per-frame cost. **Turn-taking runs a
greedy RNN-T decode per 80 ms frame, interleaved with the 11B decode, and it
dominates the budget.** p95 also improves hugely (260 -> 125 ms) because the
spiky interleave disappears.

**What you give up:** RNN-T is the turn detector - it decides when the caller has
finished speaking so the agent replies. Docs: the checkpoint has no standalone
VAD head, so without RNN-T you lose turn detection and must rely on silence
timing. That is fine for **file-in/file-out** and for benchmark throughput, but
it is NOT acceptable for a live phone agent: you would talk over the customer.

So: use `--no-rnnt-turn-taking` for offline generation, quality passes and any
throughput measurement. Keep it ON for live duplex. Do not ship it in a
production voice path on the strength of these numbers.

`--no-transcript` hides captions only and does not affect speed.

### Both local engines share the SAME 12.5 Hz frame budget

- PersonaPlex: `--max-steps` docs say 200 steps = ~16 s => **12.5 Hz**
- VoiceChat: one 80 ms input frame => **12.5 Hz**

So they are not different problems. Both need **< 80 ms/frame** to be real time,
and both miss it on an M1 Pro. Switching between them buys quality and
tool-calling, never latency. Do not present a model swap as a latency fix.

### PersonaPlex streaming flags (verified working)

```
speech respond --stream --chunk-frames 5 ... --json --transcript
```
-> RTF **1.62**, output 24.8 s of real speech (24 kHz, RMS 0.0347, peak 0.459),
and `--json` confirms `"system_prompt": "custom (37 tokens)"` - proving a custom
brief reaches the model rather than a preset.

The flag is `--chunk-frames`, **not** `--stream-chunk-size` (that name is
rejected). Smaller chunks cut time-to-first-audio, which matters for perceived
latency even when RTF is unchanged. Also present: `--full-duplex` (ring-buffer
input), `--debug-dir`. RTF is unaffected by streaming - it is a chunking dial,
not a speed dial.

### `--prebuffer-frames` is a real dial (measured)

Same int5 bundle, file input:
- default (8 frames): live-frame **RTF 2.62x**, p50 166.3 ms, p95 260.6 ms
- `--prebuffer-frames 1`: **RTF 2.33x**, p50 152.9 ms, p95 284.6 ms

Lower prebuffer buys ~11% throughput but worsens p95 (more underrun risk on a
real mic). For a phone agent under load prefer throughput - a dropped frame is
worse than 200 ms of extra latency. Never raise it: the docs warn that raising
chunk size inflates prefill sync badly.

### DEAD END: `mlx-community/NemotronLabs-VoiceChat-11B-4bit` cannot be used

Looked like the obvious latency lever (4-bit = less bandwidth = faster step)
and it is **not loadable**. Verified against the HF API before wasting disk:

- Layout is **wrong**: a flat `model-00001-of-00002.safetensors` pair at the repo
  root, **no `encoder/`, `llm/` or `tts/` dirs at all**.
- `speech voice-chat` requires `encoder/` + `llm/` + `tts/`, so it fails at
  load with `no model.safetensors at .../llm/model.safetensors`.
- It is also **9.17 GB, LARGER than the 8.56 GB int5 bundle** we use, so even if
  the layout matched it was not the smaller model.
- No EAR-TTS weights, so it cannot speak regardless.

**Lesson: check layout compatibility against the loader BEFORE downloading.**
A 9 GB pull costs ~30 min and 9 GB of disk to learn something one API call tells
you. The only bundles that work are the `aufklarer/*`-style ones with the
`encoder/ llm/ tts/` split.

Net effect on the latency question: **there is no local quantization lever left.**
The int5 bundle is the fastest loadable option, and it measures RTF 2.29-2.62x.
Real-time on this hardware needs an NVIDIA GPU, not more tuning.

### `--plain` is mandatory when capturing output

`voice-chat` uses the **alternate screen** and redraws a live dashboard in
place. Piping it or running under a non-TTY yields only the startup lines, so a
run looks like it "produced nothing" even though it was conversing. Always pass
`--plain` for append-only output intended to be captured or grepped.

That dashboard is also why a 20 s run can exit 0 with a transcript that never
appears in captured output. Do not conclude the run failed. From a backgrounded
tool process it exits 0 having loaded the model and never spoken - the live
conversation has to be run by the human in their own Terminal.

### VERIFIED: the INT5 bundle loads clean on an M1 Pro 32 GB

`aufklarer/VoiceChat-11B-Perception-MLX-int5`, 8.56 GB (encoder 518 MB,
llm 6.5 GB, tts 1.0 GB), all four load stages pass:
```
[  8%] perception encoder and RNN-T
[ 28%] 11B language model
[ 72%] EAR-TTS and audio codec
[ 90%] Verifying and warming the audio codec
[100%] VoiceChat model ready
```
Peak load was ~10 with 27% system-wide memory free. Docs require ~15.64 GB
physical; the M1 32 GB clears it. **Model loading on this Mac is therefore not
the constraint** - only live conversational throughput is still unmeasured.

### VERIFIED Dograh deployment shape for self-hosted PersonaPlex

`verify_personaplex_provider.py` runs 17 checks against the REAL registry and
passes (`python3` on this box has pydantic 2.10.4; the pp-local venv does NOT).
Two requirements it proved, both of which are silent-failure traps:

1. **`is_realtime` must be True.** Set it False and the whole realtime block is
   silently DROPPED with no error.
2. **`BYOKRealtimeAIModelConfiguration` requires an `llm` field** even though
   PersonaPlex has no function calling - see
   `api/schemas/ai_model_configuration.py:74`. That llm is Dograh's **tool
   channel**, so a PersonaPlex deployment still needs one (OpenAILLMService is
   what the repo uses). Do not assume the S2S model handles tools.

Also confirmed PersonaPlex is the only realtime provider exposing `base_url`;
all others return `[]`. And `service_factory.py:1281` dispatches per provider
(`elif provider == ...`), with `AWS_NOVA_SONIC` the closest analogue for a
self-hosted binary-audio transport.

1. `api/services/configuration/registry.py` - `ServiceProviders` enum,
   `ServiceType.REALTIME` bucket, `@register_service(ServiceType.REALTIME)`.
2. `api/services/pipecat/service_factory.py:1243` `create_realtime_llm_service()`
   dispatches on provider, one `elif` per provider.
3. `api/services/pipecat/realtime/*.py` - thin subclasses layering Dograh engine
   quirks on a vendor class. `openai_realtime.py` is the reference; its
   docstring lists what every provider inherits (silent-while-muted, greeting
   triggers, workflow-control deferral).

**`base_url` did not exist on ANY realtime config.** `BaseServiceConfiguration`
carries only `api_key`. Added for PersonaPlex; also unblocks other self-hosted
realtime backends.

## CRITICAL: MLX needs a Metal compiler, and CLT-only Mac has none

If the machine has Command Line Tools but no full Xcode, `swift build`
SUCCEEDS and links a binary that dies at runtime with:
`MLX error: Failed to load the default metallib`.

Cause: there is no `metal` compiler. Verify with
`xcrun -sdk macosx metal -c /tmp/t.metal` -> "unable to find utility metal".
The SwiftPM build has no metal step, so it silently ships a GPU-broken binary.

Fix WITHOUT installing Xcode (verified working): take the prebuilt metallib from
the matching-version Python wheel and drop it next to the executable. The
version MUST match the C++ checkout exactly, or the kernels are rejected -
check `Source/Cmlx/mlx/mlx/version.h`.

```bash
uv pip install 'mlx==0.31.1'   # match version.h, not "latest"
cp .venv/lib/python3.12/site-packages/mlx/lib/mlx.metallib .build/release/
```

**Verify the metallib is real, not a stub** - speech-swift's AGENTS.md warns
that without a compiled metallib "inference runs ~5x slower due to JIT shader
compilation", so a fallback that merely loads is not good enough:

```bash
file .build/release/mlx.metallib       # expect: MetalLib executable (MacOS)
strings -a .build/release/mlx.metallib | grep -cE 'kernel|mlx'   # expect: thousands
```

Ours: 131 MB, `MetalLib executable`, 6,486 kernel strings. It is the genuine
optimisation.

The repo's own `scripts/build_mlx_metallib.sh` cannot run without full Xcode
(`xcrun: unable to find utility "metal"`), which is why the wheel route matters
on a Command Line Tools machine.

Sanity-check the GPU independently before blaming the model:
`python -c "import mlx.core as mx; a=mx.random.normal((512,512)); mx.eval(a); print(a.sum())"`.

## MEASURED on M1 Pro 32GB, MLX 8-bit (2026-10-03)

Two runs, both coherent customer-service dialogue, real 24kHz audio
(RMS~1250, non-silent, non-clipped).

| metric | value |
|---|---|
| generation | **148.0 ms/step** |
| prefill | 0.69s total (91 steps batched) |
| RTF | **4.42** (NOT realtime) |
| voice prompt | 51 frames, 0.35s |
| transcript decode | 81.55s (!) |

### REPEATED MEASUREMENT: run-to-run variance is huge (2026-10-05)

Six runs now, in two batches of three, all with identical config:

| batch | samples (ms/step) | median |
|---|---|---|
| A | 131.2, 158.3, 194.5 | 158.3 |
| B | 148.5, 128.6, **783.0** | 148.5 |

Clean samples (excluding the contended one): **126.6 - 194.5 ms/step**,
median ~150. The **783 ms/step** sample is RTF 9.83 - a 6x outlier caused by
concurrent load, almost certainly the 8.6 GB `huggingface-cli` VoiceChat
download saturating the machine while the benchmark ran.

**Therefore: never benchmark while anything else is running on the box.**
Check `uptime` load average first; a load average above ~10 makes every
number meaningless. This also retroactively invalidates comparing runs taken
at different times of day. Quote the median of >=3 clean runs and state the
load average alongside it.

**`--compile` is SLOWER, not faster**: 184.3 vs 160.0 ms/step in a paired run.
Do not reach for it expecting a win on Apple Silicon.

Best clean observation: **126.6 ms/step, RTF 1.63**. Gapless full-duplex needs
< 80 ms/step, so an M1 Pro is still ~1.6x too slow. That gap is compute, not
code. A GPU host is the fix, not more tuning.

**Benchmarking discipline learned twice the hard way:** a polling loop inside
`execute_code` that waits on an artifact WILL hit the 300s cell timeout and
kill the child process. But note: `terminal(background=True)` children can
OUTLIVE an `execute_code` kernel death and still deliver a completion
notification - so "I killed it" is not always true. Check for the process and
read the notification before reporting a job as dead.

Gotcha: `--model-id` ignores a `--local-dir` you downloaded; the CLI uses its
own cache at `~/Library/Caches/qwen3-speech/models/<org>/<repo>/`. Pre-seed
that path (copy the files in) or it re-downloads 9GB. The CLI binary is
`huggingface-cli`, not `hf`.

## Provider landscape (verified from vendor docs, 2026-10-03)

**We already run ElevenLabs ConvAI + Twilio in production.** Found in
`Champ-Deep/Champ-Voice-Agent` -> `docs/CHAMP Call Initiator.json`, an n8n
workflow (Salesforce lead poll -> ElevenLabs outbound call). Real ids there:
- `agent_id` = `agent_3501kf4e3ak0eqkrxg1rttttk881`
- `agent_phone_number_id` = `phnum_4901kg4yjvgpetqbeknvhgm1stk4` (and a second
  `phnum_0001kfb01hv9f3e901kr4kgskqjm` in the code node)
- Dynamic vars used: `lead_name`, `leadId`, `company`, `email`
- Endpoint: `POST https://api.elevenlabs.io/v1/convai/twilio/outbound-call`

**ElevenLabs outbound-call requires THREE fields**, not two: `agent_id`,
`agent_phone_number_id`, `to_number`. Omitting any yields 422.
`conversation_initiation_client_data.dynamic_variables` is optional.
`call_recording_enabled` is optional and turns on Twilio recording.
ElevenLabs data-residency hosts exist and INCLUDE INDIA:
`https://api.in.residency.elevenlabs.io` (also US/EU/SG).

**Twilio outbound to India** (docs.twilio.com/voice/pricing/in):
- India mobile: **$0.0496/min**
- India local / major cities: **$0.0699/min**
- US local/toll-free: $0.0140/min (so India is ~4-5x US cost)
- BYOC trunking / SIP: $0.0040/min

**Sarvam AI** (Indian, rupee-priced, best fit for India volumes):
- Voice Agents platform: BYO telephony OR rent a number from Sarvam;
  campaigns with calling schedules; 11 languages; console at indus.sarvam.ai/samvaad
- STT Rs30/hr, TTS (Bulbul v3) Rs30/10k chars, Sarvam 105B LLM Rs29.28/1M input tokens
- Voice modality is ASR -> LLM -> TTS (cascaded, not S2S)

**Dograh's own outbound API** (our fork) - no UI needed:
`POST /api/v1/public/agent/{uuid}` body `{phone_number, initial_context, telephony_configuration_id?, from_phone_number_id?}`.
Prompt vars are addressable as `{{initial_context.<name>}}`; reserved key
`greeting_override` rewrites the opening line. Reserved keys that external
callers may NOT set: workflow_run_id, call_id, provider,
runtime_configuration, MPS correlation id.

## BYO IP + SIP: what Dograh actually supports (verified in our fork)

Dograh has NO raw-SIP ingest. The only SIP path is **Asterisk ARI**
(`api/services/telephony/providers/ari/`), and ARI is an Asterisk control API,
not a signalling protocol. So "use our own IP" means running Asterisk as a media
gateway and letting it bridge into the ARI provider.

Media path: carrier SIP -> Asterisk -> ARI `externalMedia` (chan_websocket) ->
`run_pipeline_telephony`. Inbound calls arrive on an ARI WebSocket event
listener, not an HTTP webhook (`can_handle_webhook` returns False for ARI).

**THE LATENCY TRAP: `transport_sample_rate=8000`** (hardcoded at
`ari/__init__.py:236`). Classic telephony narrowband. That costs vocoder
quality and adds resampling overhead versus Twilio's 8k too, but it means the
ARI path can never use a wideband native S2S model end to end. PersonaPlex is
24 kHz; routing it through ARI forces 8k -> 24k resampling and back. This is
the single biggest argument for the Twilio/Exotel media path over BYO-SIP when
latency is the priority.

ARI also cannot report call cost, and needs a real Asterisk instance plus
`websocket_client.conf` connection naming (e.g. `dograh_staging`).

Dograh telephony providers present: ari, cloudonix, exotel, plivo, telnyx,
twilio, vobiz, vonage. Both Exotel and Twilio are already first-class.

## getdial.ai as the benchmark (Dial platform)

`dial` CLI is NOT installed on this machine (as of 2026-10-03).
Bootstrapping: `curl -fsSL https://getdial.ai/skills.md`, then `dial doctor`,
`dial auth login`, `dial auth verify-otp`, `dial listen install`.

Capabilities that matter as our bar: one-shot outbound AI voice call via
`dial call --to +1... --outbound-instruction "..."`, `--voice-gender`,
`--max-duration`, per-turn transcripts with `startMs`/`endMs` offsets for
pacing analysis, WhatsApp+iMessage+RCS on the same number, transfer to human,
campaigns, and a local webhook target (`dial local-target add url
http://127.0.0.1:8787/dial`). Docs index: `https://docs.getdial.ai/llms-full.txt`.

**Dial publishes NO latency figures** (grepped the full docs corpus for
latency / turn-taking / time-to-first and found nothing). So "Dial is the gold
standard" is a quality/UX judgement, not a measured number. If latency is our
edge, we should publish ours.

Free-tier limits (lift on first top-up): 5 min/call, 2 concurrent; over-limit
call returns 429 `call_limit_reached`.

## Our ElevenLabs account (VERIFIED LIVE 2026-10-03)

Key works; account `Sreedeep`, **free tier**, workspace_admin. 9 agents
including `agent_3501kf4e3ak0eqkrxg1rttttk881` (Champ Qualifier) and
`agent_8301kn3pcntvfrb94mxhhsqjjarj` (Sreedeep's personal assistant).

Two connected numbers:
- `phnum_4901kg4yjvgpetqbeknvhgm1stk4` - "+165****4291" Lake B2B SDR Line,
  provider **twilio**, agent Champ Qualifier. **DEAD**: belongs to Twilio
  subaccount `AC...c720` in **status 4 (suspended)**.
  Outbound returns "account ... with status 4 is not active".
- `phnum_0001kj85j8w7eqr9df1b5a8ep02t` - "12133586858" IPM Demo, provider
  **sip_trunk** -> `176.9.190.89` UDP, media_encryption disabled,
  has_outbound_trunk true. **Trunk host is OFFLINE**: ping = 100% loss,
  SIP OPTIONS to UDP 5060 = no response. Call reaches ElevenLabs
  (conversation created, cost 0) then dies "0 intermediate responses".

**So our own company IP IS already connected to ElevenLabs as a live SIP
trunk.** Dograh's 8 kHz ARI path is therefore NOT required to keep our own IP -
we can stay on ElevenLabs' native path. Revisit that tradeoff.

ElevenLabs endpoints (verified in their API reference):
- `POST /v1/convai/phone-numbers` - import a number (Twilio/Exotel/SIP).
  Twilio body: `phone_number, label, sid (AC-prefixed account SID or SK-prefixed
  API key SID), token, provider`.
- `POST /v1/convai/twilio/outbound-call` - twilio numbers ONLY.
- `POST /v1/convai/sip-trunk/outbound-call` - sip_trunk numbers ONLY.
  Sending one kind of number to the other's endpoint = 422.
- A **GET with a JSON body returns HTTP 400**. Only serialise a body on
  non-GET. (Cost me a false "not found" in duplicate detection.)

## Test number for our own use

`+1 (971) 405-8440`, PN `PNdd5bf15107aefd6267ef56f27fc60954`, account
`AC...3cad`, region US1, voice-capable. Purely a
test line. NOT yet imported into ElevenLabs - import needs the Twilio
**Auth Token**, which was never supplied (and must not be pasted into chat).
Get it: Twilio Console -> Account -> Auth Token, then

```bash
export TWILIO_ACCOUNT_SID=AC...3cad
export TWILIO_AUTH_TOKEN=...      # from console, keep out of chat
export TWILIO_TO_NUMBER=+19714058440
python3 import_twilio_number.py   # idempotent: imports, binds, places a call
```

Import is verified working end-to-end: with a placeholder token ElevenLabs
returns twilio_error 20003 "auth token is not valid", which proves the request
shape is right and only the secret is missing.

Exotel India host `https://api.in.exotel.com` is live (HTTP 400 unauth, so
the endpoint exists). ElevenLabs' Exotel import needs account_sid, api_key,
api_token, api_subdomain and an applet_id.

## Test console (built 2026-10-03)

`/Users/deep/Celsus/voice-test/` - `index.html` + `voice_test_proxy.py`.
Run the proxy, open http://localhost:8787, enter E.164 number + instruction.
Proxy exists because browsers cannot call api.elevenlabs.io (CORS) and the API
key must stay server-side. Secrets come from env only, never the HTML.

## Gotchas that cost time

- **`registry.py` is not pyright-clean.** Baseline 259 diagnostics (96
  `json_schema_extra`, 94 `Field`-overload, 66 invariant-override). Adding a
  provider adds ~4 of the same class. Do NOT try to reach zero; diff against a
  pristine IN-PROJECT copy or the comparison is meaningless (an out-of-project
  copy resolves no imports and reports ~176).
- **`api_key` must be `str | list[str] | None = Field(default=None, ...)`** for
  self-hosted providers.
- **`EffectiveAIModelConfiguration.strip_incomplete_realtime_when_disabled`**
  drops `realtime` when `is_realtime` is False and `api_key` is falsy. PersonaPlex
  legitimately has no api_key, so it MUST be configured with `is_realtime=True`
  or it is silently discarded. Real hazard, not theoretical.
- Validate configs with `pydantic.TypeAdapter(RealtimeConfig)`; `RealtimeConfig`
  is a bare `Annotated` union and has no `.model_validate`.
- **Pin a commit, do not track upstream `main`.** It moved to Pipecat 1.12
  within a day and is on ~874 commits. A protocol adapter against a moving
  target is a recurring merge tax.
- `Champ-Deep` is a GitHub USER account, not an org: `gh repo fork --org
  Champ-Deep` fails 422. Fork into the authenticated account instead.
- `gh repo fork <repo> --clone=false --remote=false` is rejected ("--remote is
  unsupported when a repository argument is provided"). Use `--clone=false`.

## Licence traps

- `aufklarer/PersonaPlex-7B-MLX-{4,8}bit` = **cc-by-nc-4.0, NON-COMMERCIAL**.
  Fine for internal R&D on Apple Silicon, never for a customer-facing brand
  voice. Its own author warns 4-bit "generates garbled output" and that 8-bit
  is both better and faster.
- `idle-intelligence/personaplex-7b-v1-q4_k-webgpu` is ungated and declares the
  NVIDIA licence, 4.4GB GGUF for browser WebGPU. Unverified by us.
- VoiceStudio (debpalash) is **AGPL-3.0** - unusable for a commercial product.
  That is why the brand voice comes from PersonaPlex voice-prompt conditioning
  (a short reference recording) instead.
- NVIDIA licence obligations that matter: you indemnify NVIDIA; licence is
  revocable and auto-terminates if you bypass a guardrail or sue alleging
  infringement; attribution NOTICE only on redistribution; no trademark rights;
  Delaware law. Output liability sits with us.

## Why the brand voice is cheap

PersonaPlex is conditioned on TWO prompts before a call: a **voice prompt**
(audio-token embedding capturing vocal character/style/prosody) and a **text
prompt** (role/scenario). So a Champions brand voice is a ~30s reference
recording, not a fine-tune. Stock presets ship as `.pt` embeddings:
NATF0-3, NATM0-3, VARF0-4, VARM0-4. Use a stock preset (default NATF2) to
measure the model before introducing our own casting.

## Verification

`verify_personaplex_provider.py` at the fork root exercises the real
consumption path (`BYOKRealtimeAIModelConfiguration` and
`OrganizationAIModelConfigurationV2`, not a bare alias): 16/16 pass.
Run: `python verify_personaplex_provider.py`