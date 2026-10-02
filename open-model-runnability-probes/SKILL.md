---
name: open-model-runnability-probes
description: Use when checking if an upstream model will actually run.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [model, self-hosting, evaluation, huggingface, licensing, gpu]
    category: engineering
    related_skills: [upstream-model-integration]
---

# Open-model runnability probes

Cheap probes that settle whether an upstream model can actually run in a given
environment, BEFORE downloading weights or writing an adapter.

## When to Use

Load this when someone proposes adopting or self-hosting an upstream model and
you need to know whether it will run, whether it is downloadable, or whether a
community port is real. Pair with `upstream-model-integration`, which owns the
broader adoption verdict; this skill is the fast pre-flight that stops an
expensive download from being the discovery mechanism.

## The rule

**Never let a multi-gigabyte download be the thing that discovers a format
mismatch.** Every probe below costs seconds. Run them in order and report which
one settled the question.

## 1. Parse the config through the loader that would read it

A successful parse proves the schema matches. A `KeyError` on a nested key proves
incompatibility for the price of one HTTP request:

```bash
curl -s https://huggingface.co/ORG/REPO/raw/main/config.json | head -40
python -c "from <pkg>.models.lm import LmConfig; import json,urllib.request as u; \
  print(LmConfig.from_config_dict(json.load(u.urlopen('https://huggingface.co/ORG/REPO/raw/main/config.json'))))"
```

Compare `model_type` and the **nesting shape**, not parameter counts. A flat
schema and a nested `temporal`/`depformer`/`mimi` schema are different loaders
wearing the same model name, and a reference implementation for the base model
will usually only parse the flat one.

## 2. An artifact existing is not the artifact being loadable

Community ports and quantisations are published as inert weights more often than
not. Before planning around "the <port> build exists", confirm all three:

- a loader exists that reads this exact file layout,
- it exposes the feature you are buying (voice-prompt API, batching path),
- the package version you install actually contains that code path.

Grep the candidate library for the feature, not just the model card. A conversion
whose only working consumer is a Swift package is not reachable from Python.

## 3. Probe credential gating with an HTTP status, never from memory

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://huggingface.co/ORG/REPO/resolve/main/config.json
```

`401`/`403` means gated. A licence accepted in the user's browser session does
**not** grant API access, only a token does. "I accepted the licence" is
unverified until this returns `200`; re-probe rather than trusting the report.

## 4. Check `runtime.stage` before handing over a hosted demo

```bash
curl -s https://huggingface.co/api/spaces/OWNER/NAME | python3 -c \
  "import sys,json; print(json.load(sys.stdin)['runtime']['stage'])"
```

Most community Spaces for a new model are dead. `BUILD_ERROR`, `RUNTIME_ERROR`,
`CONFIG_ERROR` and `PAUSED` all return HTTP 200 on the space page while the app
is unusable. Verify `RUNNING` before passing a link, and state plainly that a
hosted demo can assess quality but cannot settle a latency claim.

## 5. Read the licence on the CONVERSION, not only on the base model

A community quantisation of a commercially-licensed base may itself be
non-commercial (`cc-by-nc-*`). Check the conversion repo's own licence field
before planning any customer-facing use and label R&D-only builds as such out
loud. A commercial base licence does not travel with a derivative somebody else
relicensed.

## 6. Check the local device path is wired, not merely present

```bash
grep -rnE 'Literal\["cuda"\]|Literal\["cpu"\]|mps|device\.type' <server module>
```

A device selector reading `Literal["cuda"] | Literal["cpu"]` with the consumer
branch commented out means that path was abandoned, not merely slow.

## Reporting

Lead with the verdict and the probe that produced it. If a probe killed the
proposal, that is the headline. Separate verified from inferred: name the file,
the line, and the status code. Give the user only the decisions they can make,
with numbers attached, and say plainly what will not run until they act.