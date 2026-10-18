# Review: contact sheets and device tests

Review from frames, never from feel. Record, tile, look.

## Record

- Desktop preview: Playwright or the browser's own recorder at 390 by 844, 60fps.
- Real phone: iOS screen recording or Android Recorder, 60fps, hold the phone still for Pass 2 and move it for Pass 3.
- Keep each recording under 45 seconds and name it `pass1.mp4`, `pass2.mp4`, `pass3.mp4`.

## Contact sheets

```bash
# Pass 2: catch jumps and uneven staggers (12 fps, 8 across)
ffmpeg -i pass2.mp4 -vf "fps=12,scale=195:-1,tile=8x6" -frames:v 1 contact-pass2.png

# Single transition zoomed in (30 fps on a 1 second window starting at 4.0s)
ffmpeg -ss 4.0 -t 1.0 -i pass2.mp4 -vf "fps=30,scale=260:-1,tile=6x5" -frames:v 1 transition-detail.png

# Pass 3: tilt response over time (6 fps, wide)
ffmpeg -i pass3.mp4 -vf "fps=6,scale=195:-1,tile=8x5" -frames:v 1 contact-pass3.png

# Frame timing check: dropped frames show as duplicate frames
ffmpeg -i pass2.mp4 -vf "mpdecimate,showinfo" -f null - 2>&1 | grep -c "pts_time"
```

Read the contact sheet left to right. What to circle:
- An element present in one frame and in a different place in the next with nothing in between: a jump.
- List items appearing in unequal gaps: stagger drift.
- A frame where more than one region is mid-motion: competing animations.
- A spec row with no frame showing it: missing implementation.

## Device tests (Pass 3)

| Test | Do this | Pass if |
|---|---|---|
| Resting jitter | Phone flat on a table 10 seconds | Nothing moves |
| Dead zone | Tilt 1 to 2 degrees | Nothing moves |
| Response | Tilt 10 degrees left then right | Layers follow within 100ms, no overshoot past clamp |
| Over-travel | Tilt 45 degrees | Layers stop at clamp, no edge gaps |
| Permission | Fresh load, tap once | Prompt appears after the tap with a reason line |
| Denied | Deny permission | Mouse fallback on desktop, ambient only on phone, no console errors |
| Background | Switch apps and return | Listeners resume, no stuck offset |
| Reduced motion | Turn on Reduce Motion in OS settings | Sensor layer off, feedback still works |
| Battery | 5 minutes idle on the hero | No CPU spike in Safari Web Inspector timeline |

## Report format

Findings only, one line each: `frame or test, element, what is wrong, fix`. No summary paragraph.
