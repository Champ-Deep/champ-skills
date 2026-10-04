---
name: podcast-meet-tile-recut
description: Use when cutting vertical clips from a Meet/Zoom tile grid.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
      - video
      - podcast
      - meeting-recording
      - reframing
      - captions
    related_skills:
      - talking-head-recut
      - video-clip-editing
      - hyperframes
      - hyperframes-animation
---

# Podcast meet-tile recut

Cutting social clips from a meeting recording whose layout is a **static grid of
speaker tiles** (Meet, Zoom, Teams). The hard parts are all attribution and
framing, not editing. For single-camera footage use `/talking-head-recut`; for
plain subtitles use `/embedded-captions`.

## When to Use

Use this when ALL of these hold:
- the source is a screen recording of a meeting client showing a **fixed grid of
  speaker tiles**, and
- output is a reframed vertical/short-form clip, and
- you must know **who is speaking when** to pick or cut moments.

Do NOT use when the source is a single camera (no grid, so no attribution
problem), when only subtitles are wanted, or when there is no meeting client
border to read.

## A loop variable that shadows a function parameter

`mix(slug, dur, ...)` took the clip duration as a parameter. Inside the PiP
pre-scale loop I reused the name `dur` for the *segment* length:

    for seg in segments:
        dur = seg["out"] - seg["in"]      # clobbers the clip duration

Everything after that loop used the segment length instead. The final `-t dur`
became `-t 48.5` and truncated clip C to 48.5s against an EDL duration of
61.69s — the last 13s of the answer gone, with no error.

I first blamed `overlay=shortest=1` and changed it to `eof_action=pass`. That
change was harmless and worth keeping, but it was **not the bug**, and I spent a
render cycle proving it wasn't. The real cause was the shadowed name, found by
reading the actual `-t` argument rather than reasoning about the filter graph.

Rules:

- Never reuse a parameter's name as a loop variable. `seg_dur` costs three
  characters.
- When an output is the wrong length, print the exact `-t` value before touching
  the filter graph. The duration argument is one read away; the filter chain is
  a hypothesis.
- When you split one `cmd` into a second pass, build the second command from
  scratch rather than appending to the first. Reusing it kept stale input
  indices, which pointed the music bed at an overlay that had no audio stream.
- Check `ffprobe -show_entries stream=codec_type` on the muxed output, not just
  its duration and size. An audio-only mux was the right length at 2.0 MB.
- Change one thing at a time when fixing a render. I changed the overlay mode and
  re-rendered, which made it look like the fix landed when it had not.

## `overlay=shortest=1` silently truncates your clip

When compositing a rendered overlay onto a video base, `overlay=...:shortest=1`
ends the output when the **shortest** input ends. If the overlay frame sequence
is even one or two frames short of the clip's stated duration, the whole output
is silently cut to the overlay's length.

Here it shipped clip C at **48.5s against an EDL duration of 61.69s** — the last
13 seconds of the speaker's answer simply vanished, with no error and no warning.
`render_final.py` printed "rendered 1851 overlay frames (61.7s)", so the log
looked fine while the file was wrong.

Use `eof_action=pass` instead: the video base is the authority, the overlay draws
on top and may simply run out, leaving the tail as clean bars. Then trim to the
exact duration with `-t`.

Corollary: **assert the output duration against the EDL, do not trust the render
log.** The log reports frames rendered; the file is what ships. A one-line
`ffprobe` on the delivered file catches what the renderer will not.

## Captions are selected by word MIDPOINT, so they can overrun

`build_captions()` picks words whose midpoint falls inside the window. A phrase
can therefore *start* inside the window and *end* past it. Harmless on a single
segment; after rebasing captions onto a cut timeline it pushed 10 captions of
clip C beyond its duration, burning subtitles onto frames that do not exist.

Trim captions to the clip duration in the EDL, and drop any whose end exceeds it.
The words genuinely are not spoken within the clip.

## Two overlays cannot share one bar; and start != end

A persistent brand strip added to the top bar collided with the opening title
card: the strip's right-hand "GTM INTELLIGENCE" printed straight through the hook
title ("GTM INTE" crossing "PRIVATE"). Two absolutely-positioned elements in the
same 300px bar collide unless one **defers** - here the strip starts at 4.6s,
after the title ends.

Then the fix broke the feature entirely. One expression was computed and used for
both `data-start` and `data-duration`:

    data-start="{max(dur - 3.6, 4.6)}"  data-duration="{max(dur - 3.6, 4.6)}"

On a 46.2s clip that is `data-start="42.60" data-duration="42.60"` - the strip
rendered only in the final 3.6s, underneath the end card, so the bar read as
empty for the whole clip. Start and end are different numbers:

    strip_start = 4.6
    strip_end   = max(dur - 3.6, strip_start)
    strip_dur   = strip_end - strip_start

Also: each element on a timeline needs its own `data-track-index`. Reusing the
progress bar's track (5) for the strip was a lint **error**, not a warning.

## A music bed that is present but inaudible is a silent failure

A bed authored at -34 dB RMS and then trimmed by a further -34 dB in the mix
lands ~47 dB under the voice: in the file, silent on a phone. Every other check
passed, because a whole-mix RMS is dominated by the voice and cannot see it.

Two lessons:
- **A trim is not a level.** Decide whether `BED_DB` is an absolute target or an
  offset on the authored file, and say so in the comment. Here it was documented
  as "34 dB under the voice" while being applied to an already-quiet file.
- **Measure the thing you care about.** Compare the delivered mix against
  voice-only audio from the same source window; the difference is the bed's real
  contribution.

And do NOT try to isolate the bed with a low-pass. Speech carries most of its
energy below 400 Hz, so a low-pass measures the voice. A band-split check
"measured" the bed at -21.4 dB in the broken file and came within 1.3 dB of the
voice - it would have passed the exact file it was written to catch.

## Reconsider the crop when one tile must fill the frame

A Meet tile is ~416 px wide. Filling 1080 with one tile is a **4.27x upscale** -
that is why the face filled the frame and looked soft, and no amount of unsharp
fixes it. Laying both tiles side by side uses 825 source px and needs only
**1.31x**.

Prefer the two-up whenever the source has more than one usable tile. It fixes the
softness, keeps both speakers visible (so the edit reads as a conversation), and
removes the listener-PiP class of bugs entirely - with both people on screen, an
inset of the listener is redundant, so replace it with an active-speaker ring
drawn as a **border**, never a fill.

## Captions are the floor, not the ceiling

A talking head with karaoke captions, a progress bar and a pull quote still reads
as "talking head with captions". What separates a clip from a top B2B podcast
clip is that it **DRAWS the argument**.

Mine the transcript for the concrete, drawable claim in every clip, then cue a
diagram to the exact words it illustrates:

    network collapsing to one hub | before/after state change | stat callout
    ($100/yr vs $15/mo)           | workflow arrow change

Get the cue times from the transcript, never by hand: locate the phrase that
should trigger the beat, resolve it to its token index, and use that token's
timestamp. A diagram a beat late reads as decoration.

Rules that mattered:
- **Fill the shapes.** Outline-only boxes read as a wireframe; vision called them
  "thin, flat, basic" and "sparse". Give panels a filled body.
- **Trim connectors to node edges.** A line drawn centre-to-centre pierces the
  label. Shorten the segment by the node half-size along its own direction.
- **Own a band and a paint order.** Put diagrams on their own timeline track and
  an explicit `z-index`. The overlay composites to one PNG per frame, so a quote
  drawn later appears ON TOP and reads as ghosting behind the graphic.
- Animate only **transform aliases** (`scale`, `x`, `y`, `opacity`, `rotate`) -
  never `width`/`height`/`top`/`left`.
- **Watch CSS specificity in SVG.** A generic `.dg-svg rect { fill: ... }`
  overrode `.dg-svg .d-panel rect { fill: ... }` in practice and every panel
  rendered as a hollow wireframe. Declare generic type rules FIRST, class rules
  after, and prove it by sampling the rendered pixels - not by reading the CSS.
- **Keep diagram styling in ONE file.** The rules existed in both the spec and
  the emitter and drifted: authored in one, never emitted, so the source claimed
  the panels were filled while the render showed outlines. Add a check that every
  selector in the spec is present in the emitted composition.
- **Do not stack two full-band graphics on one timeline track by z-index.**
  HyperFrames stacks by `data-track-index`, so CSS `z-index` did nothing. When
  two elements share a band, remove the overlap at build time (drop the quote
  that collides with a diagram) rather than trying to layer them.

## A check that cannot fail is not a check

Three separate "is the diagram there?" checks all passed a file that had no
diagram, because each measured the wrong thing:

1. bright-pixel fraction - a pull quote alone puts 2.7% ink in the band.
2. peak minus median baseline - the quote IS the peak, so the lift was the same
   on both files.
3. "brighter than 170" - the purple scrim's BLUE channel is 188, so 98% of the
   background counted as ink. Keyed on **saturation** instead (scrim is deeply
   saturated, strokes are not), and on **solid-row coverage** rather than total
   ink, because text is thin and a diagram is a block.

Always prove a new check against a **known-bad** file before trusting it on the
good one.

## Compositing insets: scale in the SHARED chain, not per-branch

When an inset (listener PiP, logo bug) is fed to `overlay`, its `scale`/`crop`
must live in the **shared** filter chain, not inside the branch that happens to
need it.

The failure here was self-inflicted and invisible to a mean-based check: adding a
second-speaker cut meant pre-scaling each per-segment inset, so `scale`/`crop` was
"moved out of the shared chain". Single-segment clips then overlaid a full
1080x1920 tile at y=333. The inset ran off the bottom of the frame and covered the
caption bar's right third. Vision saw it immediately ("the bottom caption bar only
covers roughly the left two-thirds"); a verifier that averaged two margin windows
did not, because a graphic over a third of the bar barely moves a mean of two
small clean samples.

Two rules:

- Scaling in the shared chain is **idempotent** for an already-scaled input, so
  put it there even when a branch pre-scales. Correctness beats DRY here.
- **Verify bars by their worst row, not their best samples.** Averaging two
  margin windows is a fair check for "is the bar the right colour" and a broken
  check for "is anything on top of the bar". Take the least-purple row across the
  bar and require a high fraction of near-brand pixels. A mean cannot hide behind
  a favourable average; a minimum can.

Corollary for any overlay: a mean over hand-picked clean regions will pass a frame
that is visibly wrong. Always check the worst case in the region the audience
actually looks at.

**And test the test.** A revised check that "excluded text by brightness" (only
counting pixels with luminance < 200) passed a deliberately broken file, because
the thing it needed to catch - a white brick wall, a pale face - is exactly what
brightness excludes. Brightness cannot separate "glyph" from "video". Run length
can: glyph runs at 62px type are well under 120px, an inset is hundreds. Always
verify a new check against a **known-broken** file before trusting it on clean
ones, or you have written a check that cannot fail.

## The two failures that cost the most

**1. A classifier's headline accuracy hides a useless minority class.** Audio
diarization (MFCC + k-means, or supervised on labels) reaches ~87% CV accuracy
while scoring **0.55 precision on the minority speaker**. Selecting clips from
that produces a clip that opens on the wrong person asking a question, carries a
title about the other person's argument, and ends before the answer lands. The
accuracy number looked fine; the clip was unusable.

**2. Cropping on face-at-rest loses the head once the speaker moves.** Solve the
crop from one frame, and the moment the speaker leans toward the camera their
temple and glasses rim leave frame. Three of four clips shipped this way. The
crop arithmetic was identical across all four, so a spot check on the first clip
looked fine.

## Speaker attribution: read the client's own border first

Meet outlines the active speaker with a light-blue border. That is **ground
truth from the application**, not an estimate. Score it directly:

- Find the border colour by sampling tile edges over a few frames (it fires only
  when a tile is active, so average across a window and take the recurring hue).
- Measure each tile's inner edge columns/rows and compare border-pixel counts.
- Keep the winner only when it leads by a margin, then merge sub-1.6s flickers.
- Sweep the whole recording at 2-4 fps and keep every run over ~20s. Those runs
  are your candidate windows.

Then **gate every window**: reject a clip unless the intended speaker holds a
majority (55%+) of it. Print the percentage per clip so a failure is visible.

**Stream frames, never buffer.** Decoding a 56-minute source into one bytes
object is tens of GB and will OOM. Pipe ffmpeg rawvideo to stdout and reshape
frame by frame:

```python
cmd = ["ffmpeg","-v","error","-ss",str(t0),"-t",str(dur),"-i",SRC,
       "-vf",f"fps={fps}","-f","rawvideo","-pix_fmt","rgb24","-"]
raw = subprocess.run(cmd, capture_output=True).stdout
n = len(raw) // (W*H*3)
frames = np.frombuffer(raw[:n*W*H*3], np.uint8).reshape(n, H, W, 3)
```

## Crop solving: per tile, and width is often the binding constraint

A 9:16 crop of height H is `H*9/16` wide. Two speakers with different framing in
the same grid may not both admit a comfortable centred crop. Solve each tile
separately, searching height **and** horizontal placement together:

- reject a candidate unless the face clears both baked bars
- allow the face left of centre when the tile forces it
- prefer the **least upscaled** candidate that survives
- **hard-constrain the whole head**, not just the face: the crop must contain
  the measured head extent, or skip it

## Measure head drift, do not assume stillness

Build a column-occupancy profile of the head band (hairline to below the eyes,
which is where the profile still means head position) across the whole clip.
Dark pixels against a bright background give the drift reliably. Face detection
is not needed and often is not trustworthy: on webcam footage under a brick
wall, YuNet placed landmarks on the wall.

Take the worst-case head extent across all clips and constrain every crop to
contain it. Then verify the shipped output: sample frames across each clip and
assert the head never touches x=0 or the right edge.

A cheap guard: the first source column that is **not** the border colour is
often further left than you assume. Measure it, don't hardcode a margin.

## Text and captions

- **Whisper emits contractions as separate tokens** (`don`, `'`, `t`). Rejoin
  them before display or the screen reads `don 't`. Also restore a leading `it`
  when a caption opens with a bare `'s` (whisper dropping it across a sentence
  boundary: `currency. it's not` -> `Currency. 's not`).
- **Whisper capitalises every utterance, not every sentence**, so a capital
  mid-thought is an artefact. Lower stray capitals, then capitalise the phrase
  head once.
- **Strip filler words** (`um`, `uh`, `you know`, `kind of`). No editor burns a
  subtitle on them. Their timings can simply go uncovered.
- **Whisper word timings butt against each other** by 10-20ms. Two timed clips
  on one track then overlap and the renderer rejects it. Give each caption a
  ~40ms guard band at its end.
- An inline-block span containing only a space **collapses to zero width**, so a
  title built from per-character spans for a stagger renders as one run-on word
  (`EMAILWASPRIVATEONCE`). Give the space span an explicit width.

## Layering

With several tiles available, do not leave the others unused: put the listener
in a **picture-in-picture** so the clip reads as a conversation. Composite the
real tile video underneath in ffmpeg and leave the composition's PiP interior
**transparent** with only a frame and label. An opaque fill reads as a broken
placeholder box.

## Verify before delivering

Assert per file: container spec, duration vs EDL, no border-coloured pixels in
the video band, exact brand colour on the bars (sampling only outer margins —
averaging the full width pulls in white glyphs and reports a colour that is not
in the file), audio present and not music-dominated, captions 2-4 words with no
artefacts and no track overlap, head never clipped at either edge.

Sample real frames near the boundaries and look at them. Several bugs here were
invisible to every numeric check.