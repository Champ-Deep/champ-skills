# Caption and motion craft

## Evidence and boundaries

- School of Motion, Joey Korenman, [Graph Editor](https://schoolofmotion.com/blog/intro-to-the-graph-editor-in-after-effects) and [Flow](https://www.schoolofmotion.com/blog/flow-after-effects): use the speed/value curve to shape movement, not just a universal easing preset; save curves for reuse without treating a preset as a substitute for animation judgment. These are professional After Effects teaching materials, not evidence of short-form conversion lift.
- [IBM Carbon motion](https://carbondesignsystem.com/guidelines/motion/overview/): distinguish entrance, on-screen movement and exit; increase duration with distance/size change; reserve expressive motion for important moments. Its curves and timing examples are for interactive UI. Borrow the principles, not its interaction durations as universal video rules.
- [Material 1 duration/easing](https://material.io/archive/guidelines/motion/duration-easing.html): asymmetric acceleration/deceleration and distance-aware duration. This is an archived, unmaintained design system, not current product guidance.
- [BBC Subtitle Guidelines](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles): readable proportional sans serif, grammatical line grouping, rendered width and reading-time checks. BBC guidance concerns closed subtitles, not a mandate for kinetic social captions. Do not call our emphasis captions BBC-compliant.
- [Manrope](https://fonts.google.com/specimen/Manrope), Mikhail Sharanda; available from [Google Fonts](https://github.com/google/fonts/tree/main/ofl/manrope) with its SIL Open Font License. Use actual font files and retain OFL.txt when distributing. It is a candidate chosen for this series, not a font endorsed by the references above.
- [GSAP CustomEase](https://gsap.com/docs/v3/Eases/CustomEase): register the plugin, create a named curve once and reuse it. Four CSS Bezier coordinates are accepted. A CSS cubic-bezier string is not directly interchangeable with a GSAP easing name without registration.

## Caption direction

Give dialogue its own type role instead of applying the diagram's bold UI heading font to everything. First candidate: Manrope SemiBold 600, 64px on a1080px canvas, line-height1.13, neutral tracking. Keep Inter700 for graphic headings as a separate role. Treat these as audition settings, not an approved permanent font choice.

Use sentence case, deliberate phrase wrapping, a stable edge-anchored baseline and a compact high-contrast backing where needed. Read `layout-and-caption-staging.md`: center the whole caption unit and reserve top/bottom space around the person rather than filling the middle. Differentiate readable dialogue from selected emphasis and explanatory graphics; a repeated plain badge is not a finished design for every passage. Wrap at grammatical boundaries, never between a negation and its verb or inside a proper name. Measure pixel width with the actual loaded font; character counts alone cannot prove fit. Caption backing can follow line width but should not jump position between cues.

Do not animate every word independently. Introduce a phrase quietly, let it remain readable, then replace it at the speech boundary. A change in keyword color must not change the line width. Never enlarge a word mid-line and cause reflow. Maintain a verbatim subtitle sidecar even if an exact on-screen diagram label replaces a display caption. Audio accessibility information is not optional if present in the source.

Inspect at actual phone scale, not only1080px screenshots. Check first/last letters, two-line boxes, short cues, face/gesture clearance and low-resolution footage. Flag reading-time pressure; do not silently accelerate speech or remove words to hide it. Retain the source meaning when retiming the edit.

## Natural motion direction

Diagnose the cause before changing a curve: overly long travel, all elements starting together, equal durations for different masses, abrupt scale jumps, or no readable hold can all look mechanical even with easing applied.

Use a small vocabulary: restrained phrase settle, weighted object entrance, progressive diagram reveal, shared-object transition and accelerating exit. Set duration by distance and visual mass. The candidate tokens are editorial starting values we chose, not measurements reported by the cited sources.

Let the primary shape lead, then its label, then supporting detail. Two or three frames of overlap at30fps can establish relation without turning every item into a delayed cascade. Check that connectors never lead into invisible nodes. Establish a readable hold before another important movement begins.

Use asymmetry: decisive travel and a longer deceleration tail for arriving objects; faster departure than arrival where appropriate. Keep a continuing object's speed continuous through adjacent segments rather than stopping on each keyframe. Small overshoot or anticipation is optional for an expressive object, not a default for speech, diagrams or every card. Do not translate professional advice into 'add bounce everywhere'.

Shrink travel and scale changes before adding spring/blur plugins. A node appearing from0.70 scale calls attention to the effect; a subtle0.96-to1 settle can support the label. Do not apply artificial motion blur to small captions. If motion blur is used on a fast moving object, inspect actual intermediate exported frames and keep text separate.

Judge at normal playback speed first; slow playback helps diagnose the cause. Static checks and screenshots can prove bounds or state progression, not smoothness. Preserve that distinction in the report.
