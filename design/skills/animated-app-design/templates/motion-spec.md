# Motion Spec: [App name]

Personality: [Calm / Energetic / Precise]
Base durations: fast 120ms, normal 250ms, slow 400ms
Easings: enter `cubic-bezier(0.16, 1, 0.3, 1)`, exit `cubic-bezier(0.7, 0, 0.84, 0)`, move `cubic-bezier(0.65, 0, 0.35, 1)`, spring `stiffness 400, damping 30, mass 1`
Stagger: 40ms per item, cap 8 items
Reduced motion: feedback layer stays (opacity only), everything else off

## Tokens

```css
:root {
  --dur-fast: 120ms;
  --dur-normal: 250ms;
  --dur-slow: 400ms;
  --ease-enter: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-exit: cubic-bezier(0.7, 0, 0.84, 0);
  --ease-move: cubic-bezier(0.65, 0, 0.35, 1);
  --stagger: 40ms;
  --tilt-max: 8deg;
  --parallax-max: 24px;
}
```

## Feedback layer

| Element | Trigger | Property | From | To | Duration | Easing | Communicates |
|---|---|---|---|---|---|---|---|
| Primary CTA | press | scale | 1.00 | 0.97 | 120ms | ease-out | registered the tap |
| Primary CTA | release | scale | 0.97 | 1.00 | spring | spring | done |
| List card | press | scale, shadow | 1.00, s2 | 0.98, s1 | 120ms | ease-out | this card |
| Toggle | tap | knob x, track color | off | on | 180ms | ease-move | state changed |
| Icon button | press | rotate or scale | 0 | -6deg | 100ms | ease-out | registered |

## Transitions layer

| From screen | To screen | Technique | Duration | Easing | Notes |
|---|---|---|---|---|---|
| Home list | Detail | shared element (card to header) | 350ms | ease-move | match position, size, radius |
| Any | Bottom sheet | translateY 100% to 0, backdrop fade | 300ms | ease-enter | drag to dismiss, velocity aware |
| Detail | Home | reverse shared element | 280ms | ease-exit | faster than entry |
| Tab | Tab | crossfade plus 8px slide in tab direction | 200ms | ease-move | indicator slides with spring |

## Reveals layer

| Screen | Elements | Order | Stagger | Entry | Notes |
|---|---|---|---|---|---|
| Home | header, stat cards, list | top to bottom | 40ms | translateY 16px to 0, opacity 0 to 1 | cap at 8 list items |
| Stats | numbers | together | 0 | count up 600ms ease-out | start from 0 |
| Chart | line or bars | left to right | 0 | stroke draw or clip-path 500ms | once per mount |
| Success | check mark, confetti, copy | check, confetti, copy | 150ms | scale spring, particle burst, fade up | confetti removed under reduced motion |

## Ambient layer

| Screen | Element | Motion | Period | Amplitude | Pauses when |
|---|---|---|---|---|---|
| Home | hero gradient | hue drift | 12s | 10deg hue | tab hidden |
| Card | glow | breathe opacity | 4s | 0.6 to 0.8 | tab hidden |

## Sensor layer (Pass 3)

| Input | Element | Mapping | Clamp | Dead zone | Smoothing | Fallback |
|---|---|---|---|---|---|---|
| Tilt gamma | hero layers | depth * parallax-max | ±24px | 3deg | 0.15 | mouse x |
| Tilt beta | hero layers | depth * parallax-max | ±24px | 3deg | 0.15 | mouse y |
| Tilt | featured card | rotateX, rotateY | ±8deg | 2deg | 0.12 | mouse |
| Scroll velocity | list items | skewY | ±2deg | 0 | 0.2 | none |
| Shake | current screen | spring reset | n/a | 15 m/s² | n/a | none |

## Depth map

| Layer | Depth | Direction |
|---|---|---|
| Background gradient | 0.0 | against tilt |
| Mid illustration | 0.4 | against tilt |
| Card | 0.7 | with tilt |
| Card content | 1.0 | with tilt |
