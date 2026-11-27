---
name: audio-transcription
description: Use when local audio must become text, fields or rows.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Transcription, Audio, Data, Celsus]
    related_skills: [media-use, meeting-followup, youtube-content, celsus-epicor-account-ops]
---

# Audio transcription (local, offline, batch)

Turn recorded audio into text on this machine: a single call, a batch of recordings, or structured fields extracted from what a speaker said. No API key needed.

## When to Use

- "Transcribe these recordings / this voice note" where the files are on disk.
- A client delivery ships call recordings and the work needs what the prospect said: fields, rows, a summary.
- A meeting recording or upload must become text outside a HyperFrames project.

Don't use for: YouTube URLs (`youtube-content`), a meeting that needs follow-up deliverables (`meeting-followup`), or transcription inside a HyperFrames project (use the `hyperframes` CLI, see below).

## Which engine

1. **`hyperframes` CLI (`transcribe`, Parakeet, whisper.cpp fallback)** when working inside a HyperFrames project. See the `media-use` skill and its `audio.md` reference file. It is the fastest and most accurate path available here.
2. **`faster-whisper` under `uv`** for anything outside a HyperFrames project: client call recordings, uploaded voice notes, a folder of mp3s. This is the recipe below.

## Recipe

```bash
cat > tx.py <<'EOF'
import os, glob, subprocess
import numpy as np
from faster_whisper import WhisperModel

def load(path):
    # decode to mono 16 kHz float32 ourselves; do NOT let faster-whisper decode
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le",
                          "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

m = WhisperModel("small", device="cpu", compute_type="int8")
for f in sorted(glob.glob("IN/*.mp3")):
    out = os.path.basename(f).replace(".mp3", ".txt")
    if os.path.exists(out) and os.path.getsize(out):   # resume: never redo finished files
        continue
    segs, _ = m.transcribe(load(f), language="en", vad_filter=True)
    txt = "\n".join(s.text.strip() for s in segs)
    open(out, "w").write(txt)
    print("done", out, flush=True)
EOF
HF_HUB_OFFLINE=1 uv run -q --with faster-whisper python tx.py
```

- `HF_HUB_OFFLINE=1` reuses the cached Systran small model already on disk instead of reaching the network.
- Decode with an `ffmpeg` subprocess as above. Pass the resulting numpy array to `transcribe`, never the file path.
- Pin `device="cpu"`, `compute_type="int8"`. The library will print an MPS suggestion; ignore it unless a run is measurably too slow.

### Why the decode step is not optional

`faster-whisper` decodes audio through the `av` package, and the installed combination does not survive that path: current `av` raises `TypeError: open() got an unexpected keyword argument 'metadata_errors'`, while pinning `av<15` forces a source build that fails against the current ffmpeg (`use of undeclared identifier 'AVFMT_ALLOW_FLUSH'`). Decoding outside the library with ffmpeg sidesteps `av` entirely. This is a durable dependency fact, not a transient install failure.

### Run batches in the background

A 6-8 minute recording takes roughly a minute of CPU per file on this machine; a batch of five blows past the 420 s foreground terminal timeout and the kill also loses every transcript not yet written. So:

- Launch with `terminal(command=..., background=True, notify=True)` and continue other work; the notification arrives on completion.
- Write one output file per input as each finishes, and skip non-empty existing outputs on restart, so a killed run resumes instead of starting over.
- Print progress with `flush=True`, and verify with a directory listing (`ls -la *.txt`) rather than trusting the log, which may only carry engine warnings.
- If one file runs past about 3x its audio length on `small`, it is stuck in a repetition loop: kill it and rerun that file alone on `base.en` with `condition_on_previous_text=False` (about 2 minutes for a 6 minute call).
- A file left at 0 bytes by a killed run means the write never happened: delete it before rerunning, or the resume check skips it forever.

## Filenames from vendors and clients

Files arrive with odd characters: non-breaking spaces in the middle of a name (the repr shows `\xa0`), stray double spaces, missing extensions. Match on a distinctive substring (company, person) instead of retyping the name, then pass the exact `os.listdir` entry to ffmpeg.

## Identifying which recording is which

When several candidates could be the same session's take (scratch vs
production, original vs re-export), decide by content, not metadata: transcribe
each candidate and match the distinctive lines you already know (the title
line, numbered questions, exact quoted phrasing). Exports inherit names, so
filename, folder and mtime are weak evidence. Run the batch in the background
with one output file per candidate, and report the match per candidate: the
file whose transcript matches the approved script in full is the take, one that
matches only partially is scratch or a different version. Never name a winner
from how the file looks on disk.

## From transcript to structured fields

When the point is rows rather than text, extract with a second pass over the transcripts: map each recording to its prospect, pull the fields the speaker actually states (name, title, company, country, ERP in use, timeline, authority), and label every field no source covers `Not captured`. Never fill a gap from a guess, and say in the report which fields the calls could not supply.
