# Build Prompts

Three prompts, one per pass. Fill the brackets. Attach the files named in each prompt; the model works from the artifacts, not from memory of the last pass.

## Pass 1: Structure

```
Build a mobile app preview as a single self-contained index.html (no build step, no external JS except from cdnjs).

App: [one line purpose]
Screens: [list from screens.md with the exits between them]
Brand tokens: attached tokens.css. Use only these variables; no raw hex in components.
References: attached reference-notes.md (layout patterns from Mobbin, not screens to copy).
Assets: attached in /assets with the slot each one fills.

Constraints:
- Phone frame 390 by 844, safe areas respected, scrollable inside the frame.
- Every list and detail screen renders all five states: empty, loading, populated, error, success. Add a hidden dev toggle to switch between them.
- Real copy from copy.md, no lorem ipsum.
- CTA buttons rectangular (radius 8px or less). Button labels are not bold.
- No horizontal rule above any label or eyebrow. No section sign characters anywhere.
- Add a prefers-reduced-motion media query stub now, even though there is no motion yet.
- Default browser transitions only. Do not add animation in this pass.

When done, list every screen and state you built and anything from screens.md you could not place.
```

## Pass 2: Motion quality

```
Here is the Pass 1 build (index.html) and a recording of it (pass1.mp4). Implement motion exactly as written in the attached motion-spec.md. Nothing animates that is not in the spec.

Personality: [Calm / Energetic / Precise]. Use the tokens block from the spec as CSS variables.

Rules:
- Four layers kept separate in code: feedback, transitions, reveals, ambient. Comment each block with its layer name.
- Animate only transform, opacity and clip-path. Never width, height, top, left, margin or padding.
- Shared element transition from [list screen] card to [detail screen] header: match position, size and radius through the move (View Transitions API if available, FLIP fallback otherwise).
- Staggers capped at 8 items; items past 8 appear as a group.
- Each micro-interaction is distinct by role: primary CTA, secondary button, list card, toggle, icon button. Do not reuse one effect across roles.
- Ambient loops pause on document.hidden and are removed under prefers-reduced-motion. Feedback stays under reduced motion as opacity only.
- Target 60fps at phone size. Use will-change sparingly and only on elements about to move.

When done, produce a table mapping every row of motion-spec.md to the selector and code that implements it, and flag any row you changed with the reason.
```

## Pass 3: Sensor-driven animation

```
Here is the Pass 2 build (index.html), motion-spec.md and the Pass 2 recording. Add the sensor layer from the spec.

Implement:
- DeviceOrientation (beta, gamma) driving parallax on the layers in the depth map and rotateX/rotateY on [featured card], clamped and dead-zoned per the spec.
- Low-pass filter on all sensor values (alpha from the spec). Use requestAnimationFrame; never set styles inside the event handler directly.
- iOS permission: call DeviceOrientationEvent.requestPermission() only from the first user tap, with a one-line reason shown in the UI. Never request on load.
- Fallbacks in order: sensors, then mouse position on desktop, then ambient only. Nothing breaks without sensors.
- Remove listeners when the screen unmounts or document.hidden is true.
- Scroll velocity and shake inputs only if listed in the spec.
- Under prefers-reduced-motion disable the whole sensor layer.

Expose a small debug overlay (toggle with a long press on the header) that shows raw and smoothed beta/gamma so the review on a real phone can verify dead zone and clamping.

When done, list the device tests to run and what to look for in each.
```

## Review prompt (any pass)

```
Attached is a contact sheet of frames from the recording (contact.png) and the motion-spec.md. Compare frame by frame. Report:
1. Frames where an element jumps position between consecutive frames.
2. Staggers that are uneven or exceed the cap.
3. Two animations competing for attention in the same frame.
4. Any spec row with no visible evidence in the frames.
Give each finding as: frame number, element, what is wrong, the one-line fix. No praise, no summary.
```
