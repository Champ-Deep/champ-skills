---
name: editorial-video-house-style
description: Use when editing Deep's talking-face videos.
license: MIT
metadata:
  version: 0.5.0
  author: Champ
  hermes:
    tags: [video, editorial, talking-face, feedback]
    related_skills: [video-clip-editing, visual-verify]
---

# Editorial video house style

## When to Use

Use this as Deep's reusable talking-face editing and improvement workflow. The substantive narrative direction has positive user feedback; caption typography and motion polish need refinement. Do not mistake approval of the story for approval of every visual setting. The caption-only treatment remains rejected. Exact fonts, curves and new template variants remain candidates until tested and approved. Never publish private footage or upload it for analysis without permission.

## Ownership and precedence

Explicit user brief, source integrity/privacy, entity brand, candidate grammar, workflow defaults: resolve conflicts in that order. Entity brand owns logos/palette, not series pacing. Background signage is not permission for endorsement.

Load video-clip-editing for probes, transcription, cuts and QA; talking-head-recut for editable graphics and HyperFrames rendering; embedded-captions for plain caption craft, not matting busy handheld footage. Conferencing composites use podcast-meet-tile-recut. New explainers use the corresponding explainer workflow, not invented source footage.

Use talking-head-recut only for the graphics layer, not as the entire editing workflow: its untouched-clip contract cannot satisfy a substantive editing request. Do not impose an arbitrary callout count before mapping the ideas. Captions, explanatory graphics, B-roll, cuts and transitions serve different jobs; animated words alone do not constitute an explainer. Keep brand consistency without forcing every scene into the same layout.

## Fixed grammar

- Preserve meaning, factual qualifications and authentic voice, not every recorded second. Audit silence, false starts, repetitions, weak setup, retakes and endings before designing graphics. Propose a timestamped cut list and reordered hook when warranted; never manufacture mistakes or delete a meaning-changing negation. Do not claim an edit if only captions were added. No generated speech, unlicensed music or unsupported claims.
- Baseline portrait canvas: 1080x1920, source-compatible fps. Normalize rotation once, verify derivative tags. Upscaling does not restore detail.
- Separate caption typography from diagram headings. Read [Caption and motion craft](references/caption-and-motion-craft.md), then audition the versioned candidate in `templates/style-tokens.json`. Load the actual local font and its license; do not silently substitute a fallback or fake a weight. Keep two lines maximum and measure at phone scale. Inter700 is an existing diagram role, not the default answer to every caption.
- Read the palette from the frozen video token file: current caption candidate uses text #F5F3ED, opaque backing #131B23 and one keyword accent #D8ED83. Explicitly set light text on busy footage rather than inheriting a parent color. Measure rendered font, line count, bounds and contrast. Brand-specific overrides belong in that video's token snapshot, not scattered CSS changes.
- Protect the person first. Read [Face-first layout and caption staging](references/layout-and-caption-staging.md). On-camera brand/information cards must be horizontally centered, including their text, and anchored to a measured clear top-safe or bottom-safe region. Do not float them through the torso or middle of the frame. Start with top250px, bottom400px and side120px exclusions at1080x1920, then resolve actual placement from the full source and gestures. When neither edge fits, delay/omit the card or use a separate graphic scene. Sheet padding is not video space.
- Group roughly three to six words into speech clauses, adjusting for pauses and readability. Preserve exact word order and editable timings. Never silently replace a negation.
- Give captions an intentional hierarchy: quiet dialogue, selected key-phrase emphasis and genuine explanatory visuals. Do not let the middle of the edit become a run of generic badges or float captions over the talking face. Keep an edge-anchored stable baseline, phrase-level reveal and semantic emphasis without reflow; the entire caption unit must be centered, not merely its text. Audit opening, middle and ending separately. For diagrams, choreograph primary shape, label and detail with distance-aware duration and distinct entry/exit curves. No word bounce, perpetual zoom or competing callouts. End at the cue boundary without overlap.
- Select the strongest honest opening and a purposeful ending from the recording. Distinguish an authored end card from padding, then explicitly recommend keeping, replacing or removing it rather than preserving a weak ending automatically. No invented quote, claim, logo or CTA.
- Design sound deliberately: natural voice first. Deep wants a music bed and selective added energy for this talking-face series; do not equate clean editorial design with silence. Use an appropriate cleared instrumental bed, speech-aware mixing and a few event-linked accents. Keep original voice and room tone across cuts. A request for more energy does not mean whooshes on every movement or bouncing captions. Read [Sound and energy](references/sound-and-energy.md) before adding this layer.

## Semantic editing module

Start with one honest idea from the recording. Use a short proof before committing to a full series rebuild. Structure an explainer as human hook, visual contrast or problem, progressive mechanism, then return to the human consequence. A graphic must teach something the subtitles alone cannot: a relation, change of state, sequence, comparison or concrete example. Label illustrative diagrams; never imply they are product screenshots or verified customer outcomes.

Reveal diagram stages on the spoken concept, rather than displaying a finished slide immediately. Draw connectors after their endpoints appear. Use a shared object to motivate scene changes: a source record can become the next diagram surface. Keep transition-only blank space brief and inspect the midpoint, not only its endpoints. Dark problem scenes and light process scenes can share one type family and accent language without being identical layouts.

Do not duplicate a large visible diagram label or brand name with a second competing caption. Preserve the complete transcript in an editable sidecar subtitle file when display captions are selectively replaced by exact graphic labels. Test a final lower third against the actual footage; a shadow or gradient does not prove contrast against a white shirt. Use a measured opaque backing where necessary.

Keep proof work bounded on a constrained disk: inspect free space and swap, remove only authorized reproducible caches with inactive-process checks, and preserve manifests, lockfiles, originals and project source. Render with one worker and streaming output. Re-measure immediately before rendering because swap can consume recovered space. Never claim all subsequent free-space growth came from cleanup; swap reclamation is a separate cause.

Make initial hidden states explicit in CSS as well as the animation timeline. Static analyzers may not resolve selector arrays passed to timeline setters. Regenerate QA images from every new final encode; cached frames can falsely verify an earlier revision. An image-state assertion is a regression check, not evidence of good pacing or a substitute for audiovisual review.

## Format adaptations

Thoughtful interview: longer complete ideas, fewer callouts. Product demo: preserve visible evidence and keep text outside the UI. Low-resolution portrait: no aggressive crop, zoom or detail-restoration claim. Other canvas sizes: scale margins then measure actual rendered output.

## Reusable library and feedback

Read [Library and learning](references/library-and-learning.md) before a new video or after feedback. Reuse versioned patterns; freeze a token snapshot with each render. Store private corrections in the project review record using `templates/review-record.json`, not in a public skill artifact. Promote narrative, caption and motion choices independently. Specific corrections outrank general praise. Do not claim automatic learning or engagement improvement: this workflow improves through recorded feedback, a changed next output and another review.

## Workflow

1. Read brief, preserve originals, check free disk before models and renders. Prefer local/cached ASR, no paid fallback.
2. Probe rotation/fps/size/duration/audio. Inspect timeline-wide samples and actual ending. Record approved in/out and every cut.
3. Transcribe locally with word times. Preserve raw ASR separately. For unclear names or meaning-changing negations, compare a stronger local ASR pass and search the original speaker brief for proper spellings. Do not replace the actual spoken variant with a draft script. Verify ambiguous clauses against audio; if direct listening is unavailable, flag the exact timestamp for reviewer listening rather than claiming agreement between ASR runs proves it.
4. Read [Pinterest evidence](references/pinterest-evidence.md) and [Temporal reference study](references/temporal-reference-study.md). Distinguish still-derived styling from sequence-derived scene changes and unverified audio/subsecond motion. Style tokens remain hypotheses until a substantive pilot is approved.
5. Reuse the existing composition workflow. Run a short smoke render before full work. Keep editable HTML/assets, raw and corrected words, cues and cut files. Render a same-interval baseline and actual MP4 pilot.
6. Assert two-line fit, actual font/colors, centered card/caption containers and text, resolved top/bottom anchors, safe bounds, face/gesture breathing room, card/caption separation, deterministic animation and caption/transcript order. Run `scripts/check_layout.py` with measured samples. Inspect the middle of the edit, gesture peaks and animation midpoints as well as settled frames; a CSS intention or a face-only check is not clearance proof.
7. ffprobe every output; fully decode; measure integrated loudness and true peak; inspect opening/middle/ending frames. Perform full audiovisual watch-through where available. Decode and sampled frames are not a watch-through, so report any limitation plainly.
8. Deliver playable media, baseline, editable source and verification. Request independent technical review and collect focused feedback on captions, motion and narrative separately. Update the private review record and the affected library version. Reuse explicitly approved dimensions; keep unreviewed presets provisional. Publication and a new entity/format remain separate approvals.

## Evaluation

Before another render, present a reference breakdown from actual playable media or timestamped frame sequences, an honest evidence limit for sound and transitions, and a per-video edit diagnosis. Separate public view counts from retention, leads and causal claims about editing. Do not label a handful of examples the top-performing B2B corpus.

Test a rotated event selfie and a low-resolution seated explainer. Require intact meaning, portrait pixels, readable captions and local-only processing. Prove the substantive edit with source/output timing, retained/removed intervals, an opening decision, explanatory visual beats and motivated scene changes. A muted-view test must reveal the idea through visuals, not merely print the transcript. Technical decode/geometry checks cannot substitute for editorial judgment. Do not claim improved engagement without measured comparison.
