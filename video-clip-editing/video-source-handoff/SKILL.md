---
name: video-source-handoff
description: Use when asked for the raw or uncut clip for someone else.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
      - video
      - handoff
      - source-export
      - podcast
      - meeting-recording
    related_skills:
      - video-clip-editing
      - podcast-meet-tile-recut
      - talking-head-recut
---

# Video source handoff

Exporting source footage so **someone else** does the editing. Trigger on "give
me the raw clip", "the uncut version", "hand this to another agent/editor",
"I want to grab X's face and add graphics myself", or any request to stop
packaging and pass the material along.

For producing the finished clip yourself, use `/video-clip-editing`. For cutting
a grid of speaker tiles with attribution, `/podcast-meet-tile-recut`. For
layering designed cards onto a clip, `/talking-head-recut`.

## The word "raw" means native resolution, uncropped, unscaled

This is the whole skill. A reframed vertical export - **even a perfect one** -
is not raw. It has baked in the framing decision and resampled the pixels, so
the receiving editor can no longer reframe either speaker or place graphics over
clean areas. Shipping your own reframe under a name like `raw/` gets it sent
back.

**If you catch yourself adding a `scale` filter to a "raw" export, stop.** You
are rebuilding the deliverable you were asked to stop building.

Deliver per clip:

| File | Spec |
|---|---|
| `<slug>_master.mov` | full source frame, all tiles, nothing cropped or scaled |
| `<slug>_tileA.mov` | speaker A at **native width, 1:1, no upscale** |
| `<slug>_tileB.mov` | speaker B at native width, 1:1 |
| `<slug>_voice.wav` | voice only, uncompressed |

The WAV matters: it stops the editor re-deriving audio from a compressed
video's already-lossy track.

## Export recipe

Measure tile geometry from decoded frames rather than assuming it. One
full-frame decode reshaped in numpy beats per-frame `ffmpeg crop` probing:
locate each tile by finding the flat background gutters between them, or scan
the row/column profile for the active-speaker border hue and take the runs.

**Force even crop width and height.** On `yuv420p` an odd `crop` snaps down by
1-2px, shifting every column and quietly eating a sliver of the face; a measured
`crop=824:553:13:112` comes back 822 px wide. Keep tiles of differing width as
separate deliverables rather than forcing a common size.

```bash
# master: nothing cropped, nothing scaled
ffmpeg -v error -y -ss $IN -t $DUR -i "$SRC" \
  -filter_complex "[0:v]scale=1280:720:flags=lanczos,setsar=1[v]" \
  -map "[v]" -c:v prores_ks -profile:v 2 -pix_fmt yuv422p10le \
  -c:a pcm_s16le -ar 48000 -ac 1 out_master.mov

# one speaker at 1:1 - no scale filter at all
ffmpeg -v error -y -ss $IN -t $DUR -i "$SRC" \
  -filter_complex "[0:v]crop=416:552:13:112,setsar=1[v]" \
  -map "[v]" -c:v prores_ks -profile:v 2 -pix_fmt yuv422p10le \
  -c:a pcm_s16le -ar 48000 -ac 1 out_tileA.mov

# voice, uncompressed
ffmpeg -v error -y -ss $IN -t $DUR -i "$SRC" \
  -vn -ac 1 -ar 48000 -c:a pcm_s16le out_voice.wav
```

The absence of a `scale` filter on the tile exports is the entire point.

ProRes keeps it lossless for their tool. Check it exists first
(`ffmpeg -encoders | grep prores_ks`); fall back to
`dnxhd -profile:v dnxhr_hq` or high-bitrate H.264 `-crf 14`, and say which you
used. Also emit an `.srt` per clip if captions were derived - phrases are
already short and on the CUT timeline, so re-timing them is wasted work. Check
disk before a multi-gigabyte export; ProRes runs roughly 250-380 MB per 50 s
clip including masters.

## State the upscale arithmetic, it governs their layout

A conferencing tile is ~416 px wide. One tile to a 1080 frame is a **2.59x**
upscale; both tiles side by side is **1.31x**. Put this in the handoff notes
rather than letting them discover it through softness. Offer `hqdn3d` plus mild
unsharp as defensible on a solo tile, and warn that heavy sharpening crawls on
motion and reads worse than honest softness.

Handing over 416 px of real data lets them choose the scale in their NLE, so
resampling and sharpening happen once with their settings instead of being
fixed by your script.

## Verify the handoff instead of asserting it

Dimensions and duration must match the EDL exactly:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,codec_name,pix_fmt,r_frame_rate \
  -of csv=p=0 out_tileA.mov
ffprobe -v error -show_entries format=duration -of csv=p=0 out_tileA.mov
```

Then prove the file carries none of your styling, because a bar or a music bed
that leaked in is invisible until someone else opens it:

```python
PURPLE = np.array([107, 8, 189])
npr = (np.abs(a - PURPLE).max(axis=2) < 40).mean()   # must be ~0.0
```

A reading in the tens of percent means bars survived into a file you called
clean.

Confirm each tile holds the right person **numerically** rather than from a
vision readout, which truncates. Score the client's active-speaker border - it is
ground truth from the application:

```python
top = a[0].mean(axis=0)   # blue border when active: [152.8 178.6 222.1]
                          # inactive tile:             [17.8 15.9 21.6]
```

## Pair the files with a brief

A directory of files gets re-derived work. Ship a short README beside them:
brand tokens (hex, fonts, tagline) from the company brand-guideline skill;
source in-point and length per clip in a table; speaker mapping by tile index
**and** physical description so it is confirmable in one glance; each clip's
concrete drawable claim with **exact cue times resolved from the transcript**,
never hand-placed; and an honest constraints section.

Flag content gaps rather than papering over them. "Clips B and D are guest-only;
the nearest host lines are 2.0s and a 34.7s ramble" is actionable. Silently
shipping two single-speaker clips is not.

## When a composed edit is rejected twice, hand off

If a finished edit has been rejected twice, **stop iterating on the composite**.
Source handoff plus a brief is what actually unblocks the work, and it is a
small step from where you already are. Re-rendering a third variation of a
composition someone has already called a failure is the wrong move.

This generalises past video: when a deliverable is rejected twice, ask whether
the useful move is a better version of the same artifact or a different,
smaller artifact that hands the decision downstream.

## Verify every claim about the footage

Do not describe what is in the files from memory or from the render script.
Sample pixels, probe streams, read the actual durations. Several faults here
survived because the source agreed with the claim being made about it.