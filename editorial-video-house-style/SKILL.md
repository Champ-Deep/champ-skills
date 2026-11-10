---
name: editorial-video-house-style
description: Use when testing a consistent editorial video style.
version: 0.1.0
author: Champ
license: MIT
metadata:
  hermes:
    tags: [video, editorial, candidate]
    related_skills: [video-clip-editing, visual-verify]
---

# Editorial video house style

## When to Use

Rejected pilot treatment, not an approved default. Do not reuse the caption-only pilots as the target aesthetic. Use this skill for reassessment until a genuinely edited pilot is approved. Keep existing defaults. Never publish private footage or upload it for analysis without permission.

## Ownership and precedence

Explicit user brief, source integrity/privacy, entity brand, candidate grammar, workflow defaults: resolve conflicts in that order. Entity brand owns logos/palette, not series pacing. Background signage is not permission for endorsement.

Load video-clip-editing for probes, transcription, cuts and QA; talking-head-recut for editable graphics and HyperFrames rendering; embedded-captions for plain caption craft, not matting busy handheld footage. Conferencing composites use podcast-meet-tile-recut. New explainers use the corresponding explainer workflow, not invented source footage.

Use talking-head-recut only for the graphics layer, not as the entire editing workflow: its untouched-clip contract cannot satisfy a substantive editing request. Do not impose an arbitrary callout count before mapping the ideas. Captions, explanatory graphics, B-roll, cuts and transitions serve different jobs; animated words alone do not constitute an explainer. Keep brand consistency without forcing every scene into the same layout.

## Fixed grammar

- Preserve meaning, factual qualifications and authentic voice, not every recorded second. Audit silence, false starts, repetitions, weak setup, retakes and endings before designing graphics. Propose a timestamped cut list and reordered hook when warranted; never manufacture mistakes or delete a meaning-changing negation. Do not claim an edit if only captions were added. No generated speech, unlicensed music or unsupported claims.
- Baseline portrait canvas: 1080x1920, source-compatible fps. Normalize rotation once, verify derivative tags. Upscaling does not restore detail.
- Use bundled local Inter 700 and GSAP from talking-head-recut. Caption starting size 64px, line height 1.14, two lines maximum, outer width 840px on 1080 canvas.
- Text #F5F3ED on opaque #171918 backing where imagery is busy. One restrained keyword accent #D9EE8A. Explicit light text, not inherited parent color. Measure rendered font, line count, bounds and contrast.
- Exclude top 250px, bottom 400px and right 120px. Resolve placement from the whole clip, avoiding faces and meaningful gestures. Sheet padding is not video space.
- Group roughly three to six words into speech clauses, adjusting for pauses and readability. Preserve exact word order and editable timings. Never silently replace a negation.
- Phrase reveal: opacity plus 12px upward settle, 220ms ease-out. Sparse emphasis: left-to-right mask, 240ms, starting size 72px. No word bounce, perpetual zoom or simultaneous competing callouts. End at cue boundary without overlap.
- Select the strongest honest opening and a purposeful ending from the recording. Distinguish an authored end card from padding, then explicitly recommend keeping, replacing or removing it rather than preserving a weak ending automatically. No invented quote, claim, logo or CTA.
- Design sound deliberately: natural voice first, selective licensed effects or a restrained bed when they support the idea. Do not add a whoosh to every motion or infer sound from a silent demo. Preserve intentional pauses and room tone across cuts; retain source color unless correction is justified.

## Format adaptations

Thoughtful interview: longer complete ideas, fewer callouts. Product demo: preserve visible evidence and keep text outside the UI. Low-resolution portrait: no aggressive crop, zoom or detail-restoration claim. Other canvas sizes: scale margins then measure actual rendered output.

## Workflow

1. Read brief, preserve originals, check free disk before models and renders. Prefer local/cached ASR, no paid fallback.
2. Probe rotation/fps/size/duration/audio. Inspect timeline-wide samples and actual ending. Record approved in/out and every cut.
3. Transcribe locally with word times. Preserve raw ASR separately. For unclear names or meaning-changing negations, compare a stronger local ASR pass and search the original speaker brief for proper spellings. Do not replace the actual spoken variant with a draft script. Verify ambiguous clauses against audio; if direct listening is unavailable, flag the exact timestamp for reviewer listening rather than claiming agreement between ASR runs proves it.
4. Read [Pinterest evidence](references/pinterest-evidence.md) and [Temporal reference study](references/temporal-reference-study.md). Distinguish still-derived styling from sequence-derived scene changes and unverified audio/subsecond motion. Style tokens remain hypotheses until a substantive pilot is approved.
5. Reuse the existing composition workflow. Run a short smoke render before full work. Keep editable HTML/assets, raw and corrected words, cues and cut files. Render a same-interval baseline and actual MP4 pilot.
6. Assert two-line fit, correct font/colors, safe bounds, face/gesture clearance, deterministic animation and caption/transcript order. Inspect mid-reveal as well as settled frames.
7. ffprobe every output; fully decode; measure integrated loudness and true peak; inspect opening/middle/ending frames. Perform full audiovisual watch-through where available. Decode and sampled frames are not a watch-through, so report any limitation plainly.
8. Deliver playable media, baseline, editable source and verification. Request independent technical review, then a named Keep/Adjust/Reject decision. Activate only after explicit Keep, scoped to approved formats and entities.

## Evaluation

Before another render, present a reference breakdown from actual playable media or timestamped frame sequences, an honest evidence limit for sound and transitions, and a per-video edit diagnosis. Separate public view counts from retention, leads and causal claims about editing. Do not label a handful of examples the top-performing B2B corpus.

Test a rotated event selfie and a low-resolution seated explainer. Require intact meaning, portrait pixels, readable captions and local-only processing. Prove the substantive edit with source/output timing, retained/removed intervals, an opening decision, explanatory visual beats and motivated scene changes. A muted-view test must reveal the idea through visuals, not merely print the transcript. Technical decode/geometry checks cannot substitute for editorial judgment. Do not claim improved engagement without measured comparison.
