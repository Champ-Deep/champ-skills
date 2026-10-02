---
name: video-clip-editing
description: "Cut long video into vertical social clips."
---

# Long video to vertical social clips

Turning one long recording into N standalone 9:16 clips that hold up to someone
who never saw the original. The pipeline below is the order that works; the
pitfalls are the ones that actually cost time.

`references/meet-tile-diarization.md` carries the speaker-detection technique and
the audio fallback. `references/whisper-toolchain.md` carries the transcription
setup and exact CLI flags. `scripts/detect_static_tiles.py` measures tile geometry
and proves a layout never changes.

## GATE: find the governing context before asking Deep anything

Deep's own material already answers most brief questions, and searching for it is
faster than waiting on him. Before asking for audience, brand, glossary or
end card, search the Celsus vault (`/Users/deep/Celsus`) for the effort, the
meeting prep note and the company. A discovery call recording almost always has
a prep note that names the series, the format, the audience and the open
questions. `_config/glossary.md`, `_config/identity.md` and `_config/org-map.md`
carry term spellings, his handles and the company map. Brand palette and fonts
live in the company brand-guideline skill, never in your own judgement.

Ask only what the vault genuinely does not answer, and batch those asks into one
round.

## 1. Triage the source before planning any edit

Run `ffprobe` and immediately answer: is this a single camera, or a composited
multi-tile layout?

A screen-recorded call (Google Meet, Zoom, Teams) is NOT a camera shot. Detect
near-black gutter columns and rows programmatically:

```
ffmpeg -i IN -vf "fps=1/30,scale=320:-1,tile=6x10" -frames:v 1 sheet.png
```

then find gutters with numpy (columns where >90% of pixels sum < 60). Vision
analysis of a frame is good at saying "three tiles, two people" and unreliable at
pixel boundaries: measure the geometry, never estimate it from a screenshot.

Sample the WHOLE timeline in at least two sheets (start, then offset past the
midpoint). A layout that holds for the first half can still switch to a
spotlight or a screen share later. If `scripts/detect_static_tiles.py` finds
identical tile bounds at several sample points, you have a static layout and can
plan exact crops.

**This decision changes the entire reframe.** A static portrait tile is a crop
calculation; a real camera shot is face tracking. Guessing wrong wastes the
whole edit.

## 2. Transcribe before promising anything

Word-level timestamps are required for captions and for cutting on word
boundaries. See `references/whisper-toolchain.md` for setup and exact flags.

Run transcription ALONE, on its own, and let it finish. A 56-minute file at
large-v3 on Metal runs roughly 2x realtime.

**Pitfall: never run a memory-heavy analysis job beside a long transcription.**
A full-tensor FFT over a 56-minute 16 kHz file allocates over 10 GB and will
starve a concurrent whisper process into dying silently, losing all its work.
Chunk every per-frame computation (`CH = 20000` frames per block) and keep
buffers float32. Serialise the long jobs.

**Pitfall: a transcription that died writes no output and leaves no error in the
log you were tailing.** After any long background job, verify the artifact
exists on disk and is non-trivial in size before building on it. Do not infer
success from the absence of a crash.

## 3. Diarize speakers, then judge whether you can trust it

Two people talking in one mono stream needs real speaker attribution, because a
wrong cut shows the wrong face. See `references/meet-tile-diarization.md` for the
full method, which uses the conferencing client's own active-speaker highlight as
training data.

**Pitfall: unsupervised k-means on MFCC collapses when one speaker dominates.**
With a 73/27 split both clusters resolve to the same person and the mapping looks
confident while being wrong. If you have any partial ground truth, train on it
supervised instead.

**Pitfall: overall accuracy hides the failure that matters.** 87% CV with 0.55
precision on the minority speaker is unsafe for speaker-focused cuts even though
the headline number looks fine. Read the per-class report and the confusion
matrix, and state the minority precision before you promise to cut on speakers.
Report the cross-validated number, never a train-set number.

## 4. Propose candidates and STOP for approval

Never render a full clip set before Deep picks the moments. Find more candidates
than he asked for, rank them, and bring a table: in/out timestamps, the exact
hook line, the one idea, why it stands alone, length after tightening, proposed
on-screen title.

He decides. Then proceed.

## 5. Edit and reframe

- Open on the hook line. No "so", "yeah" or throat-clearing.
- Cut on word boundaries from the word timestamps, pad 40 to 80 ms, crossfade
  audio 10 ms so nothing clicks.
- Alternate scale (100% / ~112%) on talking-head jump cuts so they read as
  intentional.
- Keep text and faces clear of top 250 px, bottom 400 px, right 120 px.
- Never crop away screen-share content.

**Pitfall: a 3:4 tile cropped to 9:16 is a big upscale.** A 417x554 tile yields
only about 312 px of real width for a 1080 px frame. That is the main quality
risk in the whole job. Say so plainly rather than hiding it behind sharpening,
and prefer a slightly wider crop over aggressive zoom.

## 6. Build in HyperFrames, then verify

Read the HyperFrames skill before writing composition code; do not guess its API.
Write `DESIGN.md` before any HTML, sourced from the company brand guideline.

No em dash or en dash in any on-screen text, captions or copy, and no invented
quotes or claims. Only what the speaker actually said.

Verify before claiming done: pull frames at 0, 1, 2 s, every 5 s and the final
frame; diff captions against the transcript; run `ffmpeg ebur128` and confirm
loudness and peak targets; ffprobe every output.

**Always render one throwaway smoke composition before building the real ones.**
A 4-second 1080x1920 title card proves the whole toolchain end to end in about
20 seconds. Finding a broken render path after building three full compositions
costs far more than the smoke test ever does.

## Standing rules

- Never claim a clip is rendered or postable without real tool output behind it.
- If something is blocked, name the blocker plainly instead of substituting
  plausible output.
- Deliver finished files as `MEDIA:` cards, never bare paths.