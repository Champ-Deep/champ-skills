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

## Dograh's realtime seam (three narrow touchpoints)

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

This is documented MLX behaviour: "the built mlx.metallib file should be either
at the same directory as the executable... or METAL_PATH defined at build time".

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

The repo's own benchmark is RTF ~0.94 / 80-95ms per step on an **M2 Max 64GB**.
So the M1 Pro is ~4.7x slower than realtime and ~1.7x slower per step.

Conclusion: quality and mechanics are PROVEN locally. Real-time voice on an
M1 Pro is not reachable at 8-bit, and the gap is compute, not code. Do not sell
this as a latency result - sell it as a correctness result.

Gotcha: `--model-id` ignores a `--local-dir` you downloaded; the CLI uses its
own cache at `~/Library/Caches/qwen3-speech/models/<org>/<repo>/`. Pre-seed
that path (copy the files in) or it re-downloads 9GB. The CLI binary is
`huggingface-cli`, not `hf`.

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