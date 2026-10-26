---
name: voiceover-design
description: Use when writing a voiceover or casting a voice for video.
version: 1.0.0
author: Deep / Hermes
license: proprietary
metadata:
  hermes:
    tags: [voiceover, tts, elevenlabs, video, script]
    related_skills: [media-use, video-clip-editing]
---

# voiceover-design

## When to Use

Use when Deep asks for a voiceover, a VO script, a voice recommendation or a
voice for a video he already has footage for: the deliverable is spoken lines,
a casting decision, or a prompt to run in a studio agent (ElevenLabs Studio,
HeyGen, local TTS). Do not use for narration written with no footage, for
captions or transcription alone, or for cutting clips out of a long recording
(that is `video-clip-editing`).

The output is never
just prose: it is a beat map, a timed script, a casting call, and a prompt the
studio agent can execute. Four steps, in this order.

This skill designs and prompts. Generation runs in the studio agent (ElevenLabs,
HeyGen, or the local TTS engine documented in the `media-use` skill's
`references/audio.md`), so the prompt must be self-contained: the agent on the
other end shares no context with you.

## 0. Ground it before drafting

Search the Celsus vault (`/Users/deep/Celsus`) plus the brand-guideline skills
for the company, the campaign and any standing voice preference. Brand palette,
fonts, naming rules and client-facing restrictions live in the brand skill, never
in your own judgement. If no brand shows on screen, say which brand you assumed
and why, rather than inventing one or staying silent.

## 1. Beat map: what is on screen, second by second

Never time a script against your memory of the video. Build the map first:

```bash
ffmpeg -v error -y -i IN.mp4 -vf "fps=1,scale=320:-1,tile=6x5" -frames:v 1 sheet.jpg
```

One frame per second, read left-to-right then top-to-bottom, so cell index
`row*6+col` equals the second. Give the sheet to vision in one call and ask for
the second each key line of on-screen text first appears. That returns a usable
timeline in one pass instead of a dozen single-frame calls.

**Pitfall: drop `drawtext` from the filter chain.** Many ffmpeg builds ship
without libfreetype and the whole command dies with `No such filter: 'drawtext'`,
losing the attempt. An unlabelled tile grid loses nothing: the cell index already
carries the timestamp.

**Pitfall: the contact sheet cannot settle small text.** Sheet reads disagree on
typos, stamp years and fine print because the frame is downscaled. Pull full
resolution stills for the two or three seconds that matter (`-ss N -frames:v 1`)
and read those at native size before you report a defect, then cite the second
you pulled.

## 2. Write lines against the beats

Deliver as a table: `time | on-screen text | voice | line`, one row per spoken
line, with a silence row for the opening seconds. Constraints that decide
whether it fits:

- **One spoken line per visual beat.** Every line gets a place where the screen
  is silent enough to carry it; speech overlapping the moment it describes reads
  as narration fighting the graphic.
- **Timebox to the frame budget.** Roughly 30 spoken words fit 30 seconds at
  normal delivery with pauses. Cut first, slow down later.
- **Do not voice what the screen already says.** A written call to action or
  strapline in the final card is already delivered visually; repeat it only if
  the spoken version adds a phrase the screen lacks, and only if the remaining
  seconds allow it.
- **State timings as approximate.** Frame sampling gives roughly one second of
  resolution, so write `±1s` and tell the studio agent to snap each line to the
  moment its text appears.
- **No em dash or en dash** in any line, prompt or on-screen text.

If text types on word by word (a terminal, a typewriter reveal), generate **one
clip per word** with its own start time, not one clip per sentence: a single
sentence read at normal speed finishes long before the animation does.

## 3. Cast: pair the voices to the narrative turn

- **Pair a problem voice with a fix voice** when the piece turns from defect to
  resolution. The voice change *is* the story beat, and it lets the closing line
  sound credible rather than letting one characterized voice carry a sales claim.
  Character voices (demon, villain, robot) are for the defect half only; a
  character reading the closing claim costs credibility with a B2B buyer.
- **Place the switch on the on-screen turn**, the frame where the resolution
  appears, and cut the outgoing voice's tail on a hard boundary so the incoming
  one starts on clean silence.
- **Name the delivery register in words**, especially for a soft or chatty voice:
  `crisp, confident, matter of fact`, never `cozy`, `bedtime`, `wellness`. A
  voice tagged "friendly and comforting" will drift to sleep-app unless the
  prompt pins it, and raise stability plus a slightly faster speed when it does.
  A voice with built-in echo or processing needs no reverb added on top.
- **Deep rejects generic and cozy fix voices.** On the CRT data video he dropped a stock deep narrator (Brian) and a soft receptionist voice (Lauren B), then chose a whispery crime narrator (True, `tZssYepgGaQmegsMEXjK`) for the fix half. Offer a fix voice with texture and a human edge, and pin its register in words (`calm, clinical, case closed`) so a dark or whispery voice does not read the closing claim as creepy.
- **A character voice taunts, it does not narrate.** Lines that read out the on-screen text ("I have been scanning your contacts", "Data integrity failure") were rejected as flat. Write the character as a person reacting to the viewer ("I see you're trying to scan your contacts. Too bad for you.") and keep one special register, such as the whisper, for the single question line.
- **Say what you did not verify.** You cannot audition audio without a key or a
  player. Cast from the library description and sample text, name the voice ID,
  and tell Deep to listen to the closing line first. Never write as if you heard
  it.

## 4. The prompt you hand over

Paste-ready, self-contained, with these sections in this order:

1. **What to change and what to keep.** When replacing a voice after clips
   already exist, spell out: keep the existing clips, their takes and their
   start times; discard only the named lines and regenerate them. Regenerating
   everything on a voice swap wastes the takes that already work.
2. **Every line with its voice, its start time and the on-screen cue it lands
   on**, each line as its own clip.
3. **Delivery direction for each voice** (stability, speed, tags, what not to do
   with the register), plus the instruction: if a tag is read aloud instead of
   performed, delete it and regenerate.
4. **Mix**: duck depth under each voice (deeper for a quiet voice), hard cut at
   the handover, silence at the open, loudness target and true-peak ceiling,
   finish before the runtime.
5. **Do not**: no added words, music, spoken brand name or URL unless the video
   carries one; no rewriting or "fixing" on-screen text, flag only.
6. **Report back**: actual start and end time of each line, any line retimed,
   any overlap at the handover, then any on-screen defect with the second it
   appears on.

If the agent cannot select a voice by ID, tell it to search the library by name
and confirm the match before generating.
