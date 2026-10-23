# Porting a 21st.dev component to vanilla HTML

The standing rule says 21st.dev components are non-negotiable front-end work. That rule is written for React projects where `npx shadcn add` lands the component in the tree. When the deliverable is a **single self-contained HTML file** that has to open from disk (landing pages, one-pagers, artifacts, showcase pages), there is no build step and no framework, so the shadcn path does not apply and the component gets ported by hand instead of skipped. Skipping it is the failure; porting it is the compliance.

Free tier: 2 code pulls per day (`get_component`), quota visible through `get_usage`. If the pull quota is spent, the component's public page and its compiled demo bundle still give you everything below.

## 1. Get the real source and the real stylesheet

- Pull `get_component`, or open the component's page on 21st.dev. The registry payload is React plus Tailwind utility classes; treat the JSX as the structure spec and the class list as the styling spec, not as code to transpile.
- CSS-driven components often ship **keyframes only**: the payload and file carry animation keyframes and zero class rules, so the component typechecks and renders static. Find the real stylesheet by pulling the compiled demo bundle off the published CDN (`cdn.21st.dev`), taking its inline `<style>` (or grepping the bundle for the component's class prefix), and copying the rules as a scoped stylesheet.
- Strip the demo stage. Components wrap themselves in a fixed or full-screen backdrop with a hardcoded background, which lands in your layout as a black box behind the control.
- Record the component id in a CSS comment at the top of the ported block, so the credit and the origin survive.

## 2. Remap the theme, do not import it

Tailwind utilities map onto your page's own custom properties: `bg-background` to your `--bg`, `text-muted-foreground` to your `--mut`, `font-mono` to your mono stack, spacing to your spacing scale. If the ported component needs a token your page does not have (a `--radius`, an `--accent`), define it in the ported block's scope rather than editing the page's system: the page's brand skill owns the palette, the component adapts to it, never the reverse.

Keep the component's **behaviour variables** (`--p`, `--gx`, `--ry`) with their original names. They are the state channel between the script and the CSS, and renaming them is where a port silently loses its interactivity.

## 3. Give every stateful branch three exits

Any branch driven by an effect needs all three paths, in this order:

1. `prefers-reduced-motion: reduce`: end state, no particles, no pointer tracking, a flat ground where a canvas would have drawn.
2. The static export flag (`?static=1`): the same end state, so `?static=1` screenshots show what ships, not an empty or mid-animation frame.
3. The `IntersectionObserver` fallback: if the observer is missing or the flag is set, add the visible class immediately. CSS must have its own branch too, because JS that only skips the observer leaves an `opacity: 0` element hidden.

A canvas-driven component is the case that fails loudest: reduced motion must still render something. Draw the flat ground (dots at rest, a static pattern) rather than skipping the draw, and never leave the canvas blank.

## 4. Size the canvas from its container, once and on change

Canvas effects (halftone wordmarks, particle fields, glow layers) size themselves in device pixels and will stretch or blur on resize unless every draw reads a fresh box. Use `ResizeObserver` on the wrapper (`devicePixelRatio` scaled, `ctx.setTransform`), ignore the `?static=1` flag for the observer (the flag disables interaction, not layout), and bail to a flat fill when `prefers-reduced-motion` is set.

Fit the drawn motif to **both** axes of its box, not width alone. A wordmark or glyph scaled from the container's width ignores its height: on a wide, short container the glyph box is taller than its box, so the pattern overflows the edge or crowds the content sitting on top of it and reads as noise. Scale from `min(width fit, height fit)`, then assert the drawn bounds lie inside the container rect before calling the port done.

Re-run the layout-dependent code on `resize` as well when the effect reads `innerWidth`, because a canvas drawn at page load reports the load-time width forever.

## 5. Watch the mobile traps that only a split pane hits

- **The seam eats labels.** A two-column or two-pane metric chart gives each side under 180px at 390. A row that puts label and value on one line runs under the divider or out of the viewport while every overflow check stays green (wrapped text overflows nothing). Stack the label over the value below the breakpoint, shrink the label, and probe both panes against the midpoint (see the rule in the main SKILL.md).
- **Header rows need the same treatment.** A pane header carrying a label and a total fits on one line at desktop and clips at 390. Stack it in the same media query as the rows.
- **A range input or toggle is the touch equivalent of the hover.** Hover-only reveals are unusable on phones; ship a visible range, slider or segmented control that writes the same state variable the pointer writes.

## 6. Probe the port, do not eyeball it

A ported component ships interactive behaviour, so a rest-state screenshot proves nothing. In one probe run:

- state signal: `getComputedStyle(el).getPropertyValue('--p')` (or the equivalent) before and after a real `mouse.move` into the element, and again after the pointer leaves;
- clip: the computed `clip-path` the variable drives;
- hit test: `page.mouse.click()` on each side of a split and assert the correct handler fired by reading the form field or class it writes;
- input: set the range input's `value` and assert the same signal;
- mobile: every label and value clear of the seam (`right < mid - 4` / `left > mid + 4`), row tops equal across panes, and zero elements past `innerWidth + 1`;
- console: no errors, no failed requests unless the page declares external assets (favicon services are the common one; name them in the report).

Force `scrollBehavior = 'auto'` before any pointer-driven probe: a smooth scroll still in flight when the mouse moves leaves the pointer outside the element, `pointerleave` fires, and the state resets to default while the probe reports a false failure.

## 7. Report it honestly

The handoff names which components were ported, that the port is vanilla rather than installed through shadcn, the component ids credited, and any external request the page still makes (favicon CDN, remote font). A component that was looked up but not ported is not adoption: say it was skipped and why.
