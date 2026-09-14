# Interface Guidelines

The rules the audit enforces mechanically, plus the ones a machine cannot check but a reviewer can. Organised by what breaks when you get them wrong.

This is a working distillation. The canonical public reference is Vercel's [Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines); the accessibility patterns trace to the [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/). Where those and this differ, they win on specifics and this wins on priority ordering.

Marked **[auto]** where `scripts/audit.py` checks it for you.

---

## Keyboard and focus

- Every interactive element reachable and operable by keyboard alone. Composite widgets (menus, tabs, comboboxes, trees) follow the APG pattern for that widget rather than an invented one.
- Visible focus indicator on everything focusable. Use `:focus-visible` so pointer users do not see rings on click, and `:focus-within` to highlight the containing group. **[auto]**
- Never remove an outline without replacing it. `outline: none` with nothing in its place is the single most common accessibility regression in generated code. **[auto]**
- Focus is managed deliberately: trapped inside modals, moved to newly revealed content, returned to the trigger on close. A dialog that opens and leaves focus on the body behind it is broken for keyboard and screen reader both.
- Tab order follows visual order. If CSS reordered the layout, the DOM needs reordering too.

## Pointer, touch, targets

- Minimum hit area 44px on touch, 24px on pointer. If the visual element must be smaller, expand the hit area with padding or a pseudo-element rather than shrinking the target. **[auto]**
- Label and control share one hit target on checkboxes and radios. A gap between them is a dead zone users blame themselves for.
- `touch-action: manipulation` to kill the 300ms double-tap zoom delay.
- Never disable pinch zoom. `user-scalable=no` and `maximum-scale=1` are accessibility failures, not layout fixes. **[auto]**
- If it looks clickable it must be clickable, and the inverse: nothing decorative should carry hover affordance.
- Navigation uses `<a>`. A `<div onClick>` cannot be middle-clicked, command-clicked, copied as a link, or read as a link. **[auto, partial]**

## Forms

Forms are where interfaces are actually used, and where generated ones fail most.

- A visible label for every control. A placeholder is not a label: it vanishes exactly when the user needs it, and it fails contrast almost every time. **[auto]**
- Input `font-size` at least 16px on mobile, or iOS Safari zooms on focus and the layout jumps. **[auto]**
- Correct `type` and `inputmode` so the right keyboard appears. `autocomplete` with a meaningful `name` so password managers work.
- Never block paste. People paste verification codes, addresses, and passwords.
- Accept the input, then validate. Blocking keystrokes mid-typing fights the user. Validate on blur and on submit, not on every character.
- Keep submit enabled until the request actually starts. A button disabled by client-side validation hides the reason it is disabled.
- Loading buttons keep their label and add a spinner. A button whose text changes to "Loading" loses its meaning and resizes the layout.
- Errors inline, next to the field, and focus the first one on submit. A summary at the top of a long form is a scroll hunt.
- Warn before navigating away from unsaved changes.
- Trim whitespace on submit. Pasted values carry trailing spaces.

## State, navigation, feedback

- The URL reflects the state. Filters, tabs, pagination, expanded panels, and open dialogs should all be linkable and survive a refresh. If a user cannot send someone the thing they are looking at, the state is trapped.
- Back and forward restore scroll position.
- Confirm destructive actions, or better, do them immediately and offer an Undo window. Undo beats confirmation: it does not interrupt the common case.
- Optimistic updates reconcile on response and roll back visibly on failure.
- Toasts and inline validation announce via polite `aria-live`. Silent state changes do not exist for screen reader users.
- No dead ends. Every error, empty state, and 404 offers the next step.

## Motion

- Honour `prefers-reduced-motion`. Not as an afterthought: the reduced variant is a design, and it should still communicate the state change, just without the travel. **[auto]**
- Animate `transform` and `opacity` only. Animating `width`, `height`, `top`, `left`, `margin`, or `padding` forces layout on every frame and stutters on the hardware your users actually own. Height changes go through `grid-template-rows: 0fr → 1fr`. **[auto]**
- Never `transition: all`. It animates properties you did not intend, including ones added later. **[auto]**
- Duration ladder: about 100ms for direct feedback, 200 to 300ms for state changes, up to 500ms for large layout moves. Anything above 500ms in product UI is the user waiting.
- Easing matches the change. Entrances decelerate, exits accelerate, and nothing in a product interface bounces.
- Animations are interruptible. If a user clicks again mid-transition, the new intent wins.
- `transform-origin` set so motion begins where it physically should. A dropdown that scales from its centre looks wrong for reasons people cannot articulate.
- Every animation justifies itself: it clarifies cause and effect, shows where something came from, or gives feedback. Motion with none of those jobs is decoration and costs frames.

## Layout

- Verify at a phone width, a laptop width, and ultra-wide. Ultra-wide is simulated by zooming to 50% at 1440. Most layouts that look fine at 1440 fall apart at 2560 because nothing caps the measure. **[auto, partial]**
- Respect safe areas with `env(safe-area-inset-*)` for notches and home indicators.
- No unintended scrollbars, no horizontal scroll. **[auto]**
- Flex children need `min-width: 0` before they will truncate; without it they push the container wide. **[auto]**
- Optical alignment beats geometric alignment. An icon that measures centred often looks off by a pixel; trust the eye.
- Use flex and grid rather than measuring in JavaScript.

## Content and typography

- Skeletons mirror the shape of the real content, or they cause the layout shift they exist to prevent.
- Explicit dimensions or aspect ratio on every image. **[auto]**
- Design the empty, sparse, dense, and error states. Dense is the one everyone skips: what does the table look like with 400 rows and a 90-character name in it?
- Content resilience: test with a one-character name and a 200-character one.
- `tabular-nums` wherever figures are compared vertically.
- `text-wrap: balance` on headings, `pretty` on body, to kill widows.
- Status is never colour alone. Pair it with an icon, a label, or a shape. **[auto, partial]**
- Locale-aware dates, times, and numbers via `Intl`. Hardcoded `MM/DD/YYYY` is a bug outside the US.
- Icon-only buttons carry a descriptive `aria-label`. **[auto]**
- Prefer native semantics before reaching for ARIA. A `<button>` beats `role="button"` every time.
- One `<h1>`, no skipped heading levels, a `<title>` that matches the current view. **[auto]**

## Performance

- Profile with CPU and network throttling on, not on your machine at full speed. 4x CPU throttling in DevTools approximates a mid-range Android.
- Virtualise lists past about 50 items.
- Preload above-fold images, lazy-load everything below.
- Prevent CLS with explicit image dimensions and reserved space for anything async. **[auto, partial]**
- Preconnect to CDN origins, preload critical fonts with `font-display: swap`.
- Target under 500ms for mutations. Past that, show progress.
- Track re-renders. An input that re-renders the page on every keystroke feels broken before it is slow.

## Theming

- `color-scheme: dark` on `<html>` for dark themes, so native controls, scrollbars, and form widgets follow.
- `<meta name="theme-color">` matched to the page background so the browser chrome does not clash.
- Native `<select>` needs explicit `background-color` and `color` or it inherits inconsistently across platforms.
- Dark mode inverts elevation: raised surfaces get lighter, not darker with a bigger shadow.

## Visual craft

The rules a machine cannot check. These separate correct from good.

- **Layered shadows.** One tight, near-opaque shadow for contact plus one wide, faint one for ambient light. A single `0 4px 6px rgba(0,0,0,.1)` is the default nobody chose.
- **Crisp edges.** A semi-transparent border on top of a shadow reads sharp; a shadow alone reads soft and cheap.
- **Concentric radii.** A child's radius must be less than or equal to its parent's, ideally parent radius minus the padding. Equal radii on nested boxes look wrong at the corners.
- **Hue consistency.** Borders, shadows, and muted text all tinted toward the background hue rather than pure grey or pure black.
- **Contrast increases on hover, focus, and active.** A hover state that lowers contrast reads as disabled.
- **Charts survive colour blindness.** Never encode meaning in hue alone; add shape, pattern, or direct labels. **[auto, partial]**
- **Avoid banding** in large dark gradients. Add a trace of noise, or use an image.

---

## Priority when you cannot do everything

1. Anything that makes the interface unusable for someone: keyboard traps, missing focus, blocked zoom, contrast failures, dead tap targets.
2. Anything that makes it broken for everyone: overflow, layout shift, console errors, unlabelled forms.
3. Anything that makes it feel cheap: layout-property animation, default shadows, flat hierarchy, placeholder residue.
4. Refinement: optical alignment, concentric radii, layered shadows, widow control.

Work top down. A beautifully optically-aligned button that cannot be reached by keyboard is a failure with good manners.
